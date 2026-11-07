"""Atlas record (``atlas/mechanisms/<slug>.yaml``), PRD 5.5.

A subset of the MDI mechanism record in 01_PROJECT_SPECIFICATION section 7.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import Field, model_validator

from junkyard.models.common import (
    BrickId,
    FamilyId,
    MechId,
    PartId,
    Record,
    Snake,
    Source,
    Text,
    Url,
    VersionedRecord,
    VocabId,
)


class EntityType(StrEnum):
    mechanism_pattern = "mechanism_pattern"
    mechanism_variant = "mechanism_variant"
    implementation = "implementation"
    component = "component"
    assembly = "assembly"
    structural_principle = "structural_principle"


class Alternative(Record):
    """``alternative_to`` never means drop-in equivalent: context and trade-offs are required."""

    target: MechId
    context: Text
    tradeoffs: list[Text] = Field(min_length=1)


class RealizationKind(StrEnum):
    brick = "brick"
    part = "part"
    external_reference = "external_reference"
    none = "none"


class Realization(Record):
    kind: RealizationKind
    id: str | None = None
    url: Url | None = None
    note: Text | None = None

    @model_validator(mode="after")
    def _fields_match_kind(self) -> Realization:
        k = self.kind
        if k in (RealizationKind.brick, RealizationKind.part):
            if self.id is None:
                raise ValueError(f"realized_by kind {k!r} needs an id")
            _IdCheck.model_validate({k: self.id})
            if self.url is not None:
                raise ValueError(f"realized_by kind {k!r} takes an id, not a url")
        elif k == RealizationKind.external_reference:
            if self.url is None:
                raise ValueError("realized_by kind 'external_reference' needs a url")
            if self.id is not None:
                raise ValueError("realized_by kind 'external_reference' takes a url, not an id")
        elif self.id is not None or self.url is not None:
            raise ValueError("realized_by kind 'none' takes no id or url")
        return self


class _IdCheck(Record):
    brick: BrickId | None = None
    part: PartId | None = None


class ReviewStatus(StrEnum):
    draft = "draft"
    reviewed = "reviewed"


class MechanismRecord(VersionedRecord):
    id: MechId
    entity_type: EntityType
    canonical_name: Text
    aliases: list[Text] = Field(default_factory=list)
    families: list[FamilyId] = Field(min_length=1)
    functions: list[VocabId] = Field(min_length=1)
    input_motion: list[Snake] = Field(default_factory=list)
    output_motion: list[Snake] = Field(default_factory=list)
    summary: Text
    strengths: list[Text] = Field(default_factory=list)
    watch_outs: list[Text] = Field(default_factory=list)
    alternatives: list[Alternative] = Field(default_factory=list)
    realized_by: list[Realization] = Field(min_length=1)
    sources: list[Source] = Field(default_factory=list)
    review_status: ReviewStatus = ReviewStatus.draft

    @model_validator(mode="after")
    def _consistent(self) -> MechanismRecord:
        kinds = [r.kind for r in self.realized_by]
        if RealizationKind.none in kinds and len(kinds) > 1:
            raise ValueError("realized_by 'none' cannot be combined with other realizations")
        if any(a.target == self.id for a in self.alternatives):
            raise ValueError("a mechanism cannot be an alternative to itself")
        targets = [a.target for a in self.alternatives]
        dupes = sorted({t for t in targets if targets.count(t) > 1})
        if dupes:
            raise ValueError(f"duplicate alternatives: {dupes}")
        return self

    @property
    def has_brick(self) -> bool:
        return any(r.kind == RealizationKind.brick for r in self.realized_by)
