"""Brick manifest (``bricks/<category>/<slug>/brick.yaml``), PRD 5.1 and 5.3.

Checks here only need the manifest itself. Checks that need other records
(vocabulary, parts, mechanisms, files on disk) live in ``junkyard.registry``.
"""

from __future__ import annotations

import re
from enum import StrEnum
from typing import Literal

from pydantic import Field, field_validator, model_validator

from junkyard.models.common import (
    SNAKE_RE,
    UNIT_SUFFIX,
    BrickId,
    FamilyId,
    Frame,
    MaterialId,
    MechId,
    PartId,
    Record,
    Snake,
    Tag,
    Text,
    Unit,
    Url,
    VersionedRecord,
    VocabId,
)

#: Section headings every brick README must contain, in order (PRD 5.2).
README_SECTIONS = (
    "## What it does",
    "## How it works",
    "## Typical uses",
    "## Choosing parameters",
    "## Strengths",
    "## Watch out for",
    "## Assembly",
    "## Customizing the code",
    "## Related bricks",
)

#: Licenses an imported file may carry (PRD 12.5, invariant I8). SPDX identifiers.
IMPORT_LICENSE_ALLOWLIST = (
    "CC0-1.0",
    "MIT",
    "Apache-2.0",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "CC-BY-3.0",
    "CC-BY-4.0",
)

MAX_HERO_PARAMS = 2  # 5 steps per hero param, at most 25 variants (PRD 7.2)

Scalar = bool | int | float | str


class Stage(StrEnum):
    """Software maturity of code and docs (D12), not physical validation."""

    experimental = "experimental"
    beta = "beta"
    stable = "stable"


class Difficulty(StrEnum):
    """Assembly effort."""

    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class Mdi(Record):
    realizes: MechId
    families: list[FamilyId] = Field(default_factory=list)


class Actuation(Record):
    accepts_classes: list[VocabId] = Field(min_length=1)
    default_part: PartId | None = None


# --- params -----------------------------------------------------------------


class ParamType(StrEnum):
    float = "float"
    int = "int"
    bool = "bool"
    enum = "enum"
    part_ref = "part_ref"
    material = "material"


def _is_number(v) -> bool:
    return isinstance(v, int | float) and not isinstance(v, bool)


class Param(Record):
    name: Snake
    type: ParamType
    unit: Unit | None = None
    default: Scalar
    range: tuple[float, float] | None = Field(
        default=None,
        description="Values for which the generator produces valid geometry (CI-enforced).",
    )
    options: list[Text] | None = None
    allowed_classes: list[VocabId] | None = None
    description: Text | None = None

    @model_validator(mode="after")
    def _consistent(self) -> Param:
        t = self.type
        numeric = t in (ParamType.float, ParamType.int)
        if not numeric:
            for field in ("unit", "range"):
                if getattr(self, field) is not None:
                    raise ValueError(f"{t} param {self.name!r} cannot have a {field}")
        if t != ParamType.enum and t != ParamType.material and self.options is not None:
            raise ValueError(f"{t} param {self.name!r} cannot have options")
        if t != ParamType.part_ref and self.allowed_classes is not None:
            raise ValueError(f"{t} param {self.name!r} cannot have allowed_classes")

        if numeric:
            self._check_numeric()
        elif t == ParamType.bool:
            if not isinstance(self.default, bool):
                raise ValueError(f"bool param {self.name!r} needs a true/false default")
        elif t == ParamType.enum:
            if not self.options:
                raise ValueError(f"enum param {self.name!r} needs options")
            if len(set(self.options)) != len(self.options):
                raise ValueError(f"enum param {self.name!r} has duplicate options")
            if self.default not in self.options:
                raise ValueError(
                    f"default {self.default!r} of {self.name!r} is not one of {self.options}"
                )
        elif t == ParamType.part_ref:
            if not self.allowed_classes:
                raise ValueError(f"part_ref param {self.name!r} needs allowed_classes")
            PartIdCheck.model_validate({"id": self.default})
        elif t == ParamType.material and not isinstance(self.default, str):
            raise ValueError(f"material param {self.name!r} needs a material id as default")
        return self

    def _check_numeric(self) -> None:
        name, t = self.name, self.type
        if t == ParamType.float and self.unit is None:
            raise ValueError(f"float param {name!r} needs a unit (D9)")
        if self.unit is not None:
            suffix = UNIT_SUFFIX[self.unit]
            if not name.endswith(suffix):
                raise ValueError(
                    f"param {name!r} has unit {self.unit!r}, so its name should end with "
                    f"{suffix!r} (D9)"
                )
        if self.range is None:
            raise ValueError(f"{t} param {name!r} needs a range")
        lo, hi = self.range
        if not lo < hi:
            raise ValueError(f"range of {name!r} must be [low, high] with low < high")
        if not _is_number(self.default):
            raise ValueError(f"{t} param {name!r} needs a numeric default")
        if t == ParamType.int:
            if not isinstance(self.default, int):
                raise ValueError(f"int param {name!r} needs an integer default")
            if lo != int(lo) or hi != int(hi):
                raise ValueError(f"int param {name!r} needs an integer range")
        if not lo <= self.default <= hi:
            raise ValueError(
                f"default {self.default:g} of {name!r} is outside its range [{lo:g}, {hi:g}]"
            )


class PartIdCheck(Record):
    """Helper so part_ref defaults get the same id check as other part ids."""

    id: PartId


class Derived(Record):
    """An output agents can read without generating (``expr``) or that the build fills."""

    name: Snake
    unit: Unit | None = None
    expr: Text | None = None
    from_: Literal["bbox"] | None = Field(default=None, alias="from")

    @model_validator(mode="after")
    def _one_source(self) -> Derived:
        if (self.expr is None) == (self.from_ is None):
            raise ValueError(f"derived {self.name!r} needs exactly one of 'expr' or 'from'")
        if self.unit is not None and not self.name.endswith(UNIT_SUFFIX[self.unit]):
            raise ValueError(
                f"derived {self.name!r} has unit {self.unit!r}, so its name should end with "
                f"{UNIT_SUFFIX[self.unit]!r} (D9)"
            )
        return self


# --- ports ------------------------------------------------------------------


class Gender(StrEnum):
    male = "male"
    female = "female"
    neutral = "neutral"


class Port(Record):
    """A named, typed connection point with a frame (PRD 5.3)."""

    name: Snake
    type: VocabId
    gender: Gender
    params: dict[Snake, Scalar | None] = Field(default_factory=dict)
    params_from: Snake | None = Field(
        default=None, description="Name of a part_ref param whose part supplies port params."
    )
    frame: Frame
    description: Text | None = None


# --- print hints, BOM, visuals, provenance ----------------------------------


class Supports(StrEnum):
    none = "none"
    minimal = "minimal"
    required = "required"


class PrintHints(Record):
    """Recommendations only; nothing here is verified."""

    material: list[MaterialId] = Field(default_factory=list)
    layer_height_mm: float | None = Field(default=None, gt=0)
    infill_percent: float | None = Field(default=None, ge=0, le=100)
    supports: Supports | None = None
    orientation: dict[Snake, Text] = Field(default_factory=dict)


class BomLine(Record):
    part: str = Field(description="A part id, or '@<param>' to use the part chosen by a param.")
    qty: int = Field(ge=1)
    note: Text | None = None

    @field_validator("part")
    @classmethod
    def _part_or_param(cls, v: str) -> str:
        if v.startswith("@"):
            if not re.fullmatch(SNAKE_RE, v[1:]):
                raise ValueError(f"bom param reference must look like '@servo', got {v!r}")
            return v
        PartIdCheck.model_validate({"id": v})
        return v


ColorRole = Literal["input", "output", "moving", "fixed"]


class Visuals(Record):
    hero_params: list[Snake] = Field(min_length=1, max_length=MAX_HERO_PARAMS)
    color_roles: dict[ColorRole, list[Snake]] = Field(default_factory=dict)


class Origin(StrEnum):
    original = "original"
    adapted = "adapted"
    imported = "imported"


class ImportedFile(Record):
    path: Text
    source_url: Url
    license: Text = Field(description="SPDX identifier; must be in the allow-list (I8).")

    @field_validator("license")
    @classmethod
    def _allowed(cls, v: str) -> str:
        if v not in IMPORT_LICENSE_ALLOWLIST:
            raise ValueError(
                f"license {v!r} is not in the allow-list ({', '.join(IMPORT_LICENSE_ALLOWLIST)}); "
                "link the source as inspiration and reimplement instead (I8)"
            )
        return v


class Provenance(Record):
    origin: Origin
    authors: list[Text] = Field(min_length=1)
    inspired_by: list[Url] = Field(
        default_factory=list, description="Reference designs (ideas only)."
    )
    imported_files: list[ImportedFile] = Field(default_factory=list)

    @model_validator(mode="after")
    def _origin_matches_files(self) -> Provenance:
        if self.origin == Origin.original and self.imported_files:
            raise ValueError("origin 'original' cannot list imported_files; use 'imported'")
        if self.origin == Origin.imported and not self.imported_files:
            raise ValueError("origin 'imported' needs at least one entry in imported_files")
        if self.origin == Origin.adapted and not (self.inspired_by or self.imported_files):
            raise ValueError("origin 'adapted' needs inspired_by or imported_files")
        return self


class BrickLicense(Record):
    code: Literal["Apache-2.0"] = "Apache-2.0"
    data: Literal["CC-BY-4.0"] = "CC-BY-4.0"


# --- manifest ---------------------------------------------------------------


class BrickManifest(VersionedRecord):
    id: BrickId
    name: Text
    category: VocabId
    stage: Stage
    summary: Text
    description_md: Text = "README.md"
    functions: list[VocabId] = Field(min_length=1)
    mdi: Mdi
    tags: list[Tag] = Field(default_factory=list)
    difficulty: Difficulty
    actuation: Actuation | None = None
    params: list[Param] = Field(default_factory=list)
    derived: list[Derived] = Field(default_factory=list)
    outputs: list[Snake] = Field(min_length=1, description="Named solids the generator returns.")
    ports: list[Port] = Field(default_factory=list)
    print_hints: PrintHints | None = None
    bom: list[BomLine] = Field(default_factory=list)
    assembly_steps: list[Text] = Field(default_factory=list)
    pairs_well_with: list[BrickId] = Field(default_factory=list)
    visuals: Visuals
    provenance: Provenance
    license: BrickLicense = Field(default_factory=BrickLicense)

    @field_validator("description_md")
    @classmethod
    def _relative_md(cls, v: str) -> str:
        if v.startswith("/") or ".." in v.split("/") or not v.endswith(".md"):
            raise ValueError(
                f"description_md must be a .md file inside the brick folder, got {v!r}"
            )
        return v

    @model_validator(mode="after")
    def _internal_refs(self) -> BrickManifest:
        prefix = self.id.split(".", 1)[0]
        if prefix != self.category:
            raise ValueError(
                f"id prefix {prefix!r} does not match category {self.category!r}; "
                "brick ids are <category>.<slug>"
            )
        _unique("functions", self.functions)
        _unique("outputs", self.outputs)
        _unique("tags", self.tags)
        params = {p.name: p for p in self.params}
        _unique("params", [p.name for p in self.params])
        _unique("ports", [p.name for p in self.ports])
        _unique("derived", [d.name for d in self.derived])
        clash = sorted(set(params) & {d.name for d in self.derived})
        if clash:
            raise ValueError(f"derived outputs {clash} reuse param names")

        part_refs = {n for n, p in params.items() if p.type == ParamType.part_ref}
        for port in self.ports:
            if port.params_from is not None and port.params_from not in part_refs:
                raise ValueError(
                    f"port {port.name!r}: params_from {port.params_from!r} is not a part_ref "
                    f"param (part_ref params: {sorted(part_refs) or 'none'})"
                )
        for line in self.bom:
            if line.part.startswith("@") and line.part[1:] not in part_refs:
                raise ValueError(
                    f"bom entry {line.part!r}: no part_ref param named {line.part[1:]!r}"
                )
        for hero in self.visuals.hero_params:
            p = params.get(hero)
            if p is None:
                raise ValueError(f"hero param {hero!r} is not a declared param")
            if p.type not in (ParamType.float, ParamType.int):
                raise ValueError(f"hero param {hero!r} must be numeric (float or int)")
        seen: dict[str, str] = {}
        for role, solids in self.visuals.color_roles.items():
            for solid in solids:
                if solid not in self.outputs:
                    raise ValueError(
                        f"color role {role!r} names {solid!r}, which is not in outputs "
                        f"{self.outputs}"
                    )
                if solid in seen:
                    raise ValueError(
                        f"output {solid!r} has two color roles ({seen[solid]!r}, {role!r})"
                    )
                seen[solid] = role
        if self.print_hints:
            _unique("print_hints.material", self.print_hints.material)
        return self


def _unique(what: str, values: list[str]) -> None:
    dupes = sorted({v for v in values if values.count(v) > 1})
    if dupes:
        raise ValueError(f"duplicate {what}: {dupes}")
