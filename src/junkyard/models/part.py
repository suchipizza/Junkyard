"""Part record (``parts/<kind>/<slug>.yaml``), PRD 5.4.

A part is an off-the-shelf component that bricks are sized against. Its spec
values come from a cited source or stay ``null`` (PRD section 0, rule 3).
"""

from __future__ import annotations

import re
from datetime import date
from enum import StrEnum

from pydantic import ConfigDict, Field, model_validator

from junkyard.models.brick import Port
from junkyard.models.common import (
    PartId,
    Record,
    Snake,
    Source,
    Text,
    Url,
    VersionedRecord,
    VocabId,
)

CONDITION_KEY_RE = r"^at_[a-z][a-z0-9_]*$"
_CONDITION_KEY = re.compile(CONDITION_KEY_RE)


class Verification(StrEnum):
    unverified = "unverified"
    datasheet = "datasheet"  # a human confirmed the value against the cited source


class SpecValue(Record):
    """One spec value with its source and verification state.

    Extra keys starting with ``at_`` record the conditions a value holds under,
    e.g. ``at_voltage_v`` for a stall torque.
    """

    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "patternProperties": {CONDITION_KEY_RE: {"type": ["number", "null"]}},
            "additionalProperties": False,
        },
    )

    value: float | int | str | None
    source: Source | None
    verification: Verification = Verification.unverified
    note: Text | None = None

    @model_validator(mode="after")
    def _rules(self) -> SpecValue:
        for key, cond in (self.model_extra or {}).items():
            if not _CONDITION_KEY.fullmatch(key):
                raise ValueError(
                    f"unknown key {key!r}; only value, source, verification, note and "
                    "'at_<condition>' keys are allowed"
                )
            if cond is not None and (isinstance(cond, bool) or not isinstance(cond, int | float)):
                raise ValueError(f"condition {key!r} must be a number or null")
        v = self.value
        if v is not None and (v == "" or isinstance(v, bool) or v == 0):
            raise ValueError(f"value {v!r} is not allowed; use null for unknown values")
        if v is not None and self.source is None:
            raise ValueError(
                f"value {v!r} has no source; every non-null spec value needs a source (I1). "
                "If you cannot cite one, set value to null and add a line to docs/human-tasks.md"
            )
        if self.verification == Verification.datasheet and (v is None or self.source is None):
            raise ValueError("verification 'datasheet' needs both a value and a source")
        return self


class Datasheet(Record):
    url: Url | None = None
    title: Text | None = None
    retrieved: date | None = None


class PartRecord(VersionedRecord):
    id: PartId
    name: Text
    class_: VocabId | None = Field(
        default=None,
        alias="class",
        description="Actuator class from vocab/actuator_classes.yaml; null for non-actuators.",
    )
    aliases: list[Text] = Field(default_factory=list)
    specs: dict[Snake, SpecValue] = Field(default_factory=dict)
    variance_note: Text | None = None
    ports: list[Port] = Field(default_factory=list)
    datasheets: list[Datasheet] = Field(default_factory=list)
    where_to_buy: list[Text] = Field(
        default_factory=list, description="Generic search terms only; no affiliate links in v1."
    )

    @property
    def kind(self) -> str:
        return self.id.split(".")[1]

    @model_validator(mode="after")
    def _unique_ports(self) -> PartRecord:
        names = [p.name for p in self.ports]
        dupes = sorted({n for n in names if names.count(n) > 1})
        if dupes:
            raise ValueError(f"duplicate ports: {dupes}")
        return self
