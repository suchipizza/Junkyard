"""Validation issues collected while loading the catalog.

Loading reports every problem at once, each as ``<file>: <location>: <message>``,
so an author can fix a batch of mistakes in one pass.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import ValidationError


@dataclass(frozen=True, order=True)
class Issue:
    path: str
    loc: str
    message: str

    def __str__(self) -> str:
        return (
            f"{self.path}: {self.loc}: {self.message}"
            if self.loc
            else f"{self.path}: {self.message}"
        )


@dataclass
class Issues:
    items: list[Issue] = field(default_factory=list)

    def add(self, path: str, loc: str, message: str) -> None:
        self.items.append(Issue(path, loc, message))

    def add_validation_error(self, path: str, exc: ValidationError) -> None:
        for err in exc.errors(include_url=False):
            self.add(path, format_loc(err["loc"]), clean_message(err))

    def __bool__(self) -> bool:
        return bool(self.items)


class RegistryError(Exception):
    """Raised when the catalog has any validation or reference issue."""

    def __init__(self, issues: list[Issue]) -> None:
        self.issues = sorted(issues)
        lines = "\n".join(f"  - {i}" for i in self.issues)
        super().__init__(f"{len(self.issues)} catalog issue(s):\n{lines}")


def format_loc(loc: tuple) -> str:
    out = ""
    for part in loc:
        if isinstance(part, int):
            out += f"[{part}]"
        elif str(part).startswith(("function-", "tagged-union")):
            continue  # pydantic internals, not useful to authors
        else:
            out += f".{part}" if out else str(part)
    return out


def clean_message(err: dict) -> str:
    msg = err["msg"]
    for prefix in ("Value error, ", "Assertion failed, "):
        if msg.startswith(prefix):
            msg = msg[len(prefix) :]
    if err["type"] == "extra_forbidden":
        msg = "unknown field (check the spelling; see schemas/ for allowed fields)"
    elif err["type"] == "missing":
        msg = "required field is missing"
    return msg
