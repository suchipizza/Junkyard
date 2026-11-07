"""Forward-compatibility formats (PRD section 14): ``assembly.json`` and the
``<file>.junkyard.json`` sidecar. Data formats only; no analysis or validation."""

from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator

from junkyard.models.brick import Scalar
from junkyard.models.common import (
    BrickId,
    CatalogHash,
    PartId,
    Record,
    SchemaVersion,
    SemVer,
    Snake,
    Text,
)

DISCLAIMER = (
    "Generated geometry is not verified for printability, fit or strength. Check before printing."
)


class AssemblyItem(Record):
    key: Snake = Field(description="Instance name, unique within the assembly.")
    brick: BrickId
    version: SemVer = Field(description="Library version the brick came from.")
    params: dict[Snake, Scalar] = Field(default_factory=dict)
    part_refs: dict[Snake, PartId] = Field(
        default_factory=dict, description="Resolved part for each part_ref param."
    )


class PortRef(Record):
    item: Snake
    port: Snake


class Transform(Record):
    """Pose of connection side ``b`` relative to side ``a``, from the port frames.

    ``matrix`` is a 4x4 homogeneous transform, row-major, translation in mm.
    """

    matrix: tuple[
        float, float, float, float,
        float, float, float, float,
        float, float, float, float,
        float, float, float, float,
    ]  # fmt: skip


class Connection(Record):
    a: PortRef
    b: PortRef
    transform: Transform | None = None


class BomRollupLine(Record):
    part: PartId
    qty: int = Field(ge=1)
    from_items: list[Snake] = Field(default_factory=list)


class Assembly(Record):
    format: Literal["junkyard.assembly"] = "junkyard.assembly"
    schema_version: SchemaVersion
    library_version: SemVer
    catalog_hash: CatalogHash
    items: list[AssemblyItem] = Field(min_length=1)
    connections: list[Connection] = Field(default_factory=list)
    bom: list[BomRollupLine] = Field(default_factory=list)
    disclaimer: Literal[DISCLAIMER] = DISCLAIMER  # type: ignore[valid-type]
    note: Text | None = None

    @model_validator(mode="after")
    def _refs(self) -> Assembly:
        keys = [i.key for i in self.items]
        dupes = sorted({k for k in keys if keys.count(k) > 1})
        if dupes:
            raise ValueError(f"duplicate item keys: {dupes}")
        for n, c in enumerate(self.connections):
            for side in (c.a, c.b):
                if side.item not in keys:
                    raise ValueError(f"connections[{n}] refers to unknown item {side.item!r}")
        return self


class Sidecar(Record):
    """Written next to every generated file as ``<file>.junkyard.json``."""

    format: Literal["junkyard.sidecar"] = "junkyard.sidecar"
    schema_version: SchemaVersion
    brick: BrickId
    library_version: SemVer
    catalog_hash: CatalogHash
    params: dict[Snake, Scalar]
    output: Snake = Field(description="Name of the solid in this file.")
    file_format: Literal["stl", "step", "glb"]
