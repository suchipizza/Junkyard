"""assembly.json and sidecar formats (PRD section 14). Formats only."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from junkyard.models import DISCLAIMER, Assembly, Sidecar

HASH = "sha256:" + "0" * 64
IDENTITY = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]


def _assembly(**overrides):
    data = {
        "schema_version": "0.2.0",
        "library_version": "0.1.0",
        "catalog_hash": HASH,
        "items": [
            {"key": "gripper", "brick": "gripper.parallel_jaw_rack", "version": "0.1.0",
             "params": {"opening_mm": 40}, "part_refs": {"servo": "part.servo.sg90"}},
            {"key": "finger_l", "brick": "gripper.fin_ray_finger", "version": "0.1.0"},
        ],
        "connections": [
            {"a": {"item": "gripper", "port": "jaw_left_face"},
             "b": {"item": "finger_l", "port": "mount"},
             "transform": {"matrix": IDENTITY}},
        ],
        "bom": [{"part": "part.servo.sg90", "qty": 1, "from_items": ["gripper"]}],
    }  # fmt: skip
    data.update(overrides)
    return data


def test_assembly_validates_and_carries_disclaimer():
    a = Assembly.model_validate(_assembly())
    assert a.disclaimer == DISCLAIMER
    assert a.format == "junkyard.assembly"


def test_connection_to_unknown_item_is_rejected():
    data = _assembly()
    data["connections"][0]["b"]["item"] = "finger_r"
    with pytest.raises(ValidationError, match="unknown item 'finger_r'"):
        Assembly.model_validate(data)


def test_transform_must_be_4x4():
    data = _assembly()
    data["connections"][0]["transform"]["matrix"] = IDENTITY[:12]
    with pytest.raises(ValidationError):
        Assembly.model_validate(data)


def test_bad_catalog_hash_is_rejected():
    with pytest.raises(ValidationError, match="catalog hash must look like"):
        Assembly.model_validate(_assembly(catalog_hash="abc"))


def test_sidecar_validates():
    s = Sidecar.model_validate({
        "schema_version": "0.2.0", "brick": "joint.pin_revolute", "library_version": "0.1.0",
        "catalog_hash": HASH, "params": {"pin_d_mm": 5}, "output": "link_a", "file_format": "stl",
    })  # fmt: skip
    assert s.format == "junkyard.sidecar"
