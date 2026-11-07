"""I1: every non-null part spec value has a source.

Checked twice: on the raw YAML (independent of the models) and through the model
validator, for the real ``parts/`` folder and for the fixtures.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from junkyard.models import PartRecord
from junkyard.yamlio import load_yaml

from ..conftest import CATALOG, INVALID, REPO

PART_FILES = sorted((REPO / "parts").rglob("*.yaml")) + sorted((CATALOG / "parts").rglob("*.yaml"))


def _unsourced(path: Path) -> list[str]:
    data = load_yaml(path) or {}
    return [
        name
        for name, spec in (data.get("specs") or {}).items()
        if isinstance(spec, dict) and spec.get("value") is not None and not spec.get("source")
    ]


def test_fixture_catalog_has_parts_to_check():
    assert any(p.is_relative_to(CATALOG) for p in PART_FILES)


@pytest.mark.parametrize("path", PART_FILES, ids=lambda p: p.relative_to(REPO).as_posix())
def test_every_non_null_spec_has_a_source(path: Path):
    assert _unsourced(path) == [], f"{path}: non-null spec values without a source"


def test_fixture_with_sourced_value_is_actually_exercised():
    data = load_yaml(CATALOG / "parts/servo/fixture_micro.yaml")
    assert data["specs"]["mass_g"]["value"] is not None
    assert data["specs"]["mass_g"]["source"]


def test_model_rejects_unsourced_value():
    path = INVALID / "part/value_without_source.yaml"
    assert _unsourced(path) == ["body_l_mm"]
    with pytest.raises(ValidationError, match=r"needs a source \(I1\)"):
        PartRecord.model_validate(load_yaml(path))
