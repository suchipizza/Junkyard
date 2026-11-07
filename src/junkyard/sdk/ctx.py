"""Generator context: the only way a generator reads part specs (invariant I2)."""

from __future__ import annotations

import difflib

from junkyard.errors import MissingSpec, UnknownPart
from junkyard.models.part import PartRecord
from junkyard.registry import Registry


class Ctx:
    """Passed to every generator. Resolves parts and hands out spec values.

    ``spec()`` never returns ``None``: a null or unrecorded spec raises
    :class:`MissingSpec`, so a generator cannot silently build around a guess.
    """

    def __init__(self, registry: Registry) -> None:
        self._registry = registry

    def part(self, part_id: str) -> PartRecord:
        try:
            return self._registry.part(part_id)
        except KeyError:
            match = difflib.get_close_matches(part_id, list(self._registry.parts), n=1)
            raise UnknownPart(part_id, match[0] if match else None) from None

    def spec(self, part: PartRecord | str, field: str) -> float | int | str:
        record = self.part(part) if isinstance(part, str) else part
        entry = record.specs.get(field)
        if entry is None:
            raise MissingSpec(record.id, field, reason="not_recorded")
        if entry.value is None:
            raise MissingSpec(record.id, field, reason="null")
        return entry.value
