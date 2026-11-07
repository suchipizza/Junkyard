"""Every invalid fixture fails to load, with the message promised in its header."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from junkyard.issues import Issues
from junkyard.models import BrickManifest, MechanismRecord, PartRecord
from junkyard.yamlio import load_yaml

from .conftest import INVALID

MODELS = {"brick": BrickManifest, "part": PartRecord, "mechanism": MechanismRecord}
CASES = sorted(INVALID.rglob("*.yaml"))


def _expected(path: Path) -> str:
    first = path.read_text(encoding="utf-8").splitlines()[0]
    assert first.startswith("# expect: "), f"{path.name} must start with '# expect: <text>'"
    return first.removeprefix("# expect: ")


def _errors(path: Path) -> list[str]:
    try:
        data = load_yaml(path)
    except yaml.YAMLError as exc:
        return [str(exc)]
    try:
        MODELS[path.parent.name].model_validate(data)
    except ValidationError as exc:
        issues = Issues()
        issues.add_validation_error(path.name, exc)
        return [str(i) for i in issues.items]
    return []


def test_there_are_invalid_fixtures_for_every_kind():
    kinds = {p.parent.name for p in CASES}
    assert kinds == set(MODELS)
    assert len(CASES) >= 30


@pytest.mark.parametrize("path", CASES, ids=lambda p: f"{p.parent.name}/{p.stem}")
def test_invalid_fixture_fails_with_clear_message(path: Path):
    expected = _expected(path)
    errors = _errors(path)
    assert errors, f"{path.name} loaded without error"
    assert any(expected in e for e in errors), (
        f"expected an error containing {expected!r}, got:\n" + "\n".join(errors)
    )
