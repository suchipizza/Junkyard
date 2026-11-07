"""Errors with the codes agents see (PRD 9.1)."""

from __future__ import annotations

from typing import ClassVar


class JunkyardError(Exception):
    """Base error. ``to_error()`` gives the ``{"error": {...}}`` envelope body."""

    code: ClassVar[str] = "junkyard_error"

    def __init__(self, message: str, hint: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.hint = hint

    def to_error(self) -> dict:
        return {"error": {"code": self.code, "message": self.message, "hint": self.hint}}


class MissingSpec(JunkyardError):
    """A generator asked for a part spec that is null or not recorded (invariant I2).

    Generators must never guess a dimension; they raise this instead.
    """

    code: ClassVar[str] = "missing_spec"

    def __init__(self, part_id: str, field: str, reason: str = "null") -> None:
        self.part_id = part_id
        self.field = field
        self.reason = reason
        what = "is null (no sourced value yet)" if reason == "null" else "is not recorded"
        super().__init__(
            message=f"{part_id}: spec '{field}' {what}; the generator cannot use a guessed value",
            hint=(
                f"Add a sourced value for '{field}' to the part record (see "
                "docs/human-tasks.md), or choose a part whose spec is known."
            ),
        )

    def to_error(self) -> dict:
        body = super().to_error()
        body["error"]["part"] = self.part_id
        body["error"]["field"] = self.field
        return body


class UnknownPart(JunkyardError):
    code: ClassVar[str] = "unknown_part"

    def __init__(self, part_id: str, suggestion: str | None = None) -> None:
        self.part_id = part_id
        hint = f"Did you mean {suggestion!r}?" if suggestion else "List parts to see valid ids."
        super().__init__(f"unknown part {part_id!r}", hint)
