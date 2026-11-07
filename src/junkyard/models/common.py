"""Shared field types and small models used by every record.

Conventions (PRD section 5 and D9):
- Unknown values are ``null``. Empty strings are rejected so nobody writes ``""``
  to mean "unknown".
- Units are explicit and carried in field names (``opening_mm``, ``mass_g``).
- IDs are stable, lowercase and dotted: bricks ``<category>.<slug>``,
  parts ``part.<kind>.<slug>``, mechanisms ``mech.<slug>``.
"""

from __future__ import annotations

import math
import re
from datetime import date
from enum import StrEnum
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, model_validator
from pydantic.json_schema import WithJsonSchema

from junkyard import SCHEMA_VERSION

SUPPORTED_SCHEMA_VERSIONS = (SCHEMA_VERSION,)


class Record(BaseModel):
    """Base for every model: unknown keys are errors, so typos never pass silently."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True, use_enum_values=True)


# --- strings and IDs ---------------------------------------------------------


def _non_empty(value: str) -> str:
    if not value.strip():
        raise ValueError("empty string is not allowed; use null for unknown values")
    return value


Text = Annotated[str, AfterValidator(_non_empty)]


def _pattern_type(pattern: str, what: str, example: str):
    regex = re.compile(pattern)

    def check(value: str) -> str:
        if not regex.fullmatch(value):
            raise ValueError(f"{what} must look like {example!r}, got {value!r}")
        return value

    return Annotated[
        str,
        AfterValidator(check),
        WithJsonSchema({"type": "string", "pattern": pattern}),
    ]


SNAKE_RE = r"^[a-z][a-z0-9_]*$"
BRICK_ID_RE = r"^[a-z][a-z0-9_]*\.[a-z0-9][a-z0-9_]*$"
PART_ID_RE = r"^part\.[a-z][a-z0-9_]*\.[a-z0-9][a-z0-9_]*$"
MECH_ID_RE = r"^mech\.[a-z0-9][a-z0-9_]*$"
MATERIAL_ID_RE = r"^[A-Za-z][A-Za-z0-9]*$"
FAMILY_RE = r"^F(0[1-9]|1[0-8])$"
URL_RE = r"^https?://\S+$"
SEMVER_RE = r"^\d+\.\d+\.\d+([.+-][0-9A-Za-z.+-]+)?$"
CATALOG_HASH_RE = r"^sha256:[0-9a-f]{64}$"
TAG_RE = r"^[a-z0-9][a-z0-9_-]*$"

Snake = _pattern_type(SNAKE_RE, "name", "snake_case_name")
VocabId = _pattern_type(SNAKE_RE, "vocabulary id", "snake_case_id")
BrickId = _pattern_type(BRICK_ID_RE, "brick id", "<category>.<slug>, e.g. gripper.fin_ray_finger")
PartId = _pattern_type(PART_ID_RE, "part id", "part.<kind>.<slug>, e.g. part.servo.sg90")
MechId = _pattern_type(MECH_ID_RE, "mechanism id", "mech.<slug>, e.g. mech.four_bar")
MaterialId = _pattern_type(MATERIAL_ID_RE, "material id", "PETG")
FamilyId = _pattern_type(FAMILY_RE, "MDI family", "F01 … F18")
Url = _pattern_type(URL_RE, "url", "https://example.org/datasheet.pdf")
SemVer = _pattern_type(SEMVER_RE, "version", "0.2.0")
CatalogHash = _pattern_type(CATALOG_HASH_RE, "catalog hash", "sha256:<64 hex digits>")
Tag = _pattern_type(TAG_RE, "tag", "beginner")


def _check_schema_version(value: str) -> str:
    if value not in SUPPORTED_SCHEMA_VERSIONS:
        raise ValueError(
            f"schema_version {value!r} is not supported; this library reads "
            f"{', '.join(SUPPORTED_SCHEMA_VERSIONS)}"
        )
    return value


SchemaVersion = Annotated[
    str,
    AfterValidator(_check_schema_version),
    WithJsonSchema({"type": "string", "enum": list(SUPPORTED_SCHEMA_VERSIONS)}),
]


class VersionedRecord(Record):
    """Every catalog record has ``id``, ``schema_version`` and ``updated_at`` (PRD 5)."""

    schema_version: SchemaVersion
    updated_at: date


# --- MDI families (01_PROJECT_SPECIFICATION section 4, 02 plan B1) -----------

FAMILIES: dict[str, str] = {
    "F01": "Compliant mechanisms and flexures",
    "F02": "Rigid-body linkages",
    "F03": "Joints, bearings, pivots and linear guides",
    "F04": "Gears, reducers and geared differentials",
    "F05": "Tendon, cable, belt and chain drives",
    "F06": "Motion converters",
    "F07": "Cams, indexing and intermittent motion",
    "F08": "Underactuation, mechanical differentials and coupling",
    "F09": "Springs, compliance, damping and variable stiffness",
    "F10": "Clutches, brakes, ratchets and locking",
    "F11": "Serial, parallel and hybrid kinematic architectures",
    "F12": "Grippers and end-effectors",
    "F13": "Soft and continuum robotics mechanisms",
    "F14": "Locomotion, steering and suspension mechanisms",
    "F15": "Deployable, origami, morphing and reconfigurable",
    "F16": "Bio-inspired mechanisms and mechanical metamaterials",
    "F17": "Passive alignment, insertion, docking and contact adaptation",
    "F18": "Micro-mechanisms and precision stages",
}


# --- units (D9) ---------------------------------------------------------------


class Unit(StrEnum):
    mm = "mm"
    deg = "deg"
    newton_metre = "N·m"
    newton = "N"
    gram = "g"
    volt = "V"
    second = "s"
    rpm = "rpm"
    percent = "percent"


#: Field-name suffix required for each unit, so units are readable from names.
UNIT_SUFFIX: dict[str, str] = {
    "mm": "_mm",
    "deg": "_deg",
    "N·m": "_nm",
    "N": "_n",
    "g": "_g",
    "V": "_v",
    "s": "_s",
    "rpm": "_rpm",
    "percent": "_percent",
}


# --- sources -----------------------------------------------------------------


class SourceKind(StrEnum):
    datasheet = "datasheet"
    reference_drawing = "reference_drawing"
    standard = "standard"
    web = "web"
    literature = "literature"


class Source(Record):
    """Where a value or claim comes from (PRD 5.4)."""

    url: Url | None = None
    title: Text | None = None
    kind: SourceKind
    retrieved: date | None = None
    location: Text | None = Field(
        default=None, description="Page, table or section inside the source."
    )

    @model_validator(mode="after")
    def _needs_url_or_title(self) -> Source:
        if self.url is None and self.title is None:
            raise ValueError("a source needs at least a url or a title")
        return self


# --- coordinate frames (PRD 5.3) ---------------------------------------------

Vec3 = tuple[float, float, float]
_AXIS_TOL = 1e-6


def _norm(v: Vec3) -> float:
    return math.sqrt(sum(c * c for c in v))


class Frame(Record):
    """Port frame: origin in mm plus right-handed unit z and x axes."""

    origin_mm: Vec3
    z_axis: Vec3
    x_axis: Vec3

    @model_validator(mode="after")
    def _orthonormal(self) -> Frame:
        for name in ("z_axis", "x_axis"):
            length = _norm(getattr(self, name))
            if abs(length - 1.0) > _AXIS_TOL:
                raise ValueError(f"{name} must be a unit vector (length is {length:g})")
        dot = sum(a * b for a, b in zip(self.z_axis, self.x_axis, strict=True))
        if abs(dot) > _AXIS_TOL:
            raise ValueError(f"z_axis and x_axis must be orthogonal (dot product is {dot:g})")
        return self
