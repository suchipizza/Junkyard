"""Controlled vocabularies (PRD 5.6 and 5.3): functions, ports, actuator classes,
categories, materials. Each lives in one YAML file under ``vocab/``."""

from __future__ import annotations

import re
from datetime import date
from enum import StrEnum
from typing import Annotated

from pydantic import AfterValidator, BeforeValidator, Field, model_validator
from pydantic.json_schema import WithJsonSchema

from junkyard.models.common import MaterialId, Record, SchemaVersion, Snake, Text, VocabId

# --- functions -------------------------------------------------------------


class FunctionTerm(Record):
    """A physical job a brick or mechanism does, with the phrases agents use for it."""

    id: VocabId
    label: Text
    definition: Text
    aliases: list[Text] = Field(
        min_length=1, description="Natural phrases that should resolve to this function."
    )
    parent: VocabId | None = None


class FunctionsFile(Record):
    schema_version: SchemaVersion
    updated_at: date
    functions: list[FunctionTerm]


# --- ports -----------------------------------------------------------------

PORT_PARAM_TYPE_RE = (
    r"^(int|float|bool|str|actuator_class|enum\[[A-Za-z0-9_.]+(,[A-Za-z0-9_.]+)*\])$"
)
_PORT_PARAM_TYPE = re.compile(PORT_PARAM_TYPE_RE)


def _check_port_param_type(value: str) -> str:
    if not _PORT_PARAM_TYPE.fullmatch(value):
        raise ValueError(
            "port param type must be int, float, bool, str, actuator_class or "
            f"enum[A,B,...], got {value!r}"
        )
    return value


PortParamType = Annotated[
    str,
    AfterValidator(_check_port_param_type),
    WithJsonSchema({"type": "string", "pattern": PORT_PARAM_TYPE_RE}),
]


def enum_options(param_type: str) -> list[str] | None:
    """Options of an ``enum[...]`` port param type, or None for other types."""
    if param_type.startswith("enum["):
        return param_type[5:-1].split(",")
    return None


class GenderRule(StrEnum):
    opposite = "opposite"  # male mates with female
    same = "same"
    any = "any"


def _as_list(value):
    return [value] if isinstance(value, str) else value


class PortTypeDef(Record):
    """A connection-point type. Used for discovery and assembly export, not verification."""

    type: VocabId
    description: Text
    params: dict[Snake, PortParamType] = Field(default_factory=dict)
    mates_with: Annotated[list[VocabId], BeforeValidator(_as_list)] = Field(
        default_factory=list,
        description="Port types this one mates with. Empty means: same type only.",
    )
    gender_rule: GenderRule = GenderRule.opposite
    match_keys: list[Snake] = Field(
        default_factory=list,
        description="Params that must agree for two ports to match "
        "(exact on enums/ints/str, ±0.1 mm on floats).",
    )

    @model_validator(mode="after")
    def _match_keys_are_params(self) -> PortTypeDef:
        unknown = [k for k in self.match_keys if k not in self.params]
        if unknown:
            raise ValueError(
                f"match_keys {unknown} are not declared in params ({sorted(self.params)})"
            )
        return self


class PortsFile(Record):
    schema_version: SchemaVersion
    updated_at: date
    ports: list[PortTypeDef]


# --- actuator classes ------------------------------------------------------


class ActuatorKind(StrEnum):
    servo = "servo"
    stepper = "stepper"
    gearmotor = "gearmotor"
    manual = "manual"


class ActuatorClass(Record):
    id: VocabId
    label: Text
    kind: ActuatorKind
    description: Text


class ActuatorClassesFile(Record):
    schema_version: SchemaVersion
    updated_at: date
    actuator_classes: list[ActuatorClass]


# --- categories ------------------------------------------------------------


class Category(Record):
    id: VocabId
    label: Text
    description: Text


class CategoriesFile(Record):
    schema_version: SchemaVersion
    updated_at: date
    categories: list[Category]


# --- materials (names and process only in v1; no property values) ----------


class Process(StrEnum):
    fdm = "fdm"


class Material(Record):
    id: MaterialId
    label: Text
    process: Process


class MaterialsFile(Record):
    schema_version: SchemaVersion
    updated_at: date
    materials: list[Material]
