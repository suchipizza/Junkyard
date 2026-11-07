"""JSON Schemas are generated from the models and committed (PRD 12.2)."""

from __future__ import annotations

import json
import re

import yaml

from junkyard.models import BrickManifest
from junkyard.models.export import SCHEMAS, render_schemas, stale_schemas

from .conftest import REPO


def test_committed_schemas_match_models():
    stale = stale_schemas(REPO / "schemas")
    assert stale == [], f"run `python -m junkyard.models.export`; stale: {stale}"


def test_every_record_type_has_a_schema():
    names = set(SCHEMAS)
    for expected in ("brick", "part", "mechanism", "assembly", "sidecar"):
        assert f"{expected}.schema.json" in names
    for vocab in ("functions", "ports", "actuator_classes", "categories", "materials"):
        assert f"vocab.{vocab}.schema.json" in names


def test_schema_rendering_is_deterministic():
    assert render_schemas() == render_schemas()
    for text in render_schemas().values():
        schema = json.loads(text)
        assert schema["$id"].endswith(".schema.json")
        assert schema["x-junkyard-schema-version"] == "0.2.0"


def test_prd_example_brick_manifest_validates():
    """The brick.yaml example in PRD 5.1 is valid, once given the updated_at field
    that PRD section 5 requires on every record."""
    prd = (REPO / "docs/03_JUNKYARD_PRD.md").read_text(encoding="utf-8")
    section = prd.split("### 5.1", 1)[1]
    block = re.search(r"```yaml\n(.*?)```", section, re.S).group(1)
    data = yaml.safe_load(block)
    data["updated_at"] = "2026-11-07"
    manifest = BrickManifest.model_validate(data)
    assert manifest.id == "gripper.parallel_jaw_rack"
    assert [p.name for p in manifest.ports] == ["servo_body", "jaw_left_face", "base_mount"]
