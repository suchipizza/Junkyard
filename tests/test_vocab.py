from __future__ import annotations

import pytest

from junkyard.issues import RegistryError
from junkyard.vocab import Vocab

from .conftest import VOCAB


@pytest.fixture(scope="module")
def vocab() -> Vocab:
    return Vocab.load(VOCAB)


def test_at_least_60_functions_each_with_definition_and_aliases(vocab):
    assert len(vocab.functions) >= 60
    for term in vocab.functions.values():
        assert term.definition and term.aliases


def test_functions_named_in_the_prd_exist(vocab):
    for fid in ["grip_parallel", "grip_fragile_irregular", "linear_actuation_vertical"]:
        assert fid in vocab.functions


@pytest.mark.parametrize(
    ("phrase", "function"),
    [
        ("pick up a grape", "grip_fragile_irregular"),
        ("make it go up and down", "linear_actuation_vertical"),
        ("Pick Up A Grape", "grip_fragile_irregular"),
        ("grip_parallel", "grip_parallel"),
        ("grip parallel", "grip_parallel"),
    ],
)
def test_aliases_resolve(vocab, phrase, function):
    assert vocab.function_for(phrase) == function


def test_unknown_phrase_resolves_to_none(vocab):
    assert vocab.function_for("launch a rocket") is None


def test_initial_port_types_from_prd(vocab):
    expected = {
        "servo_horn_spline", "servo_body_mount", "nema17_face", "nema14_face", "n20_face",
        "shaft_round", "shaft_d", "bearing_seat", "bolt_pattern", "finger_mount_m3_pair",
        "pin_bore", "gt2_belt_clamp", "extrusion_2020_slot", "rod_8mm", "leadscrew_t8_nut",
    }  # fmt: skip
    assert set(vocab.ports) == expected


def test_bolt_pattern_matches_prd(vocab):
    bolt = vocab.ports["bolt_pattern"]
    assert bolt.params["screw"] == "enum[M2,M2.5,M3,M4,M5]"
    assert bolt.match_keys == ["screw", "count", "pitch_x_mm", "pitch_y_mm"]


def test_actuator_classes_categories_materials_match_prd(vocab):
    assert set(vocab.actuator_classes) == {
        "hobby_servo_9g", "hobby_servo_standard", "hobby_servo_high_torque", "nema17_stepper",
        "nema14_stepper", "geared_stepper_28byj48", "n20_gearmotor", "tt_gearmotor", "manual",
    }  # fmt: skip
    assert set(vocab.categories) == {
        "joint", "motor", "gripper", "gear", "linear", "linkage", "lock", "transmission",
        "structure", "wheel",
    }  # fmt: skip
    assert set(vocab.materials) == {"PLA", "PETG", "TPU95A", "ABS", "ASA", "Nylon"}


def test_materials_carry_no_property_values():
    text = (VOCAB / "materials.yaml").read_text()
    for word in ("density", "modulus", "strength", "temperature"):
        assert word not in text


def _copy_vocab(tmp_path):
    d = tmp_path / "vocab"
    d.mkdir()
    for f in VOCAB.glob("*.yaml"):
        (d / f.name).write_text(f.read_text())
    return d


def test_alias_collision_is_rejected(tmp_path):
    d = _copy_vocab(tmp_path)
    path = d / "functions.yaml"
    path.write_text(path.read_text().replace("[parallel gripper,", "[pick up a grape,", 1))
    with pytest.raises(RegistryError, match="alias 'pick up a grape' already resolves to"):
        Vocab.load(d)


def test_unknown_parent_is_rejected(tmp_path):
    d = _copy_vocab(tmp_path)
    path = d / "functions.yaml"
    path.write_text(path.read_text().replace("parent: grip\n", "parent: gripp\n", 1))
    with pytest.raises(RegistryError, match="parent 'gripp' is not a known function"):
        Vocab.load(d)


def test_missing_vocab_file_is_reported(tmp_path):
    d = _copy_vocab(tmp_path)
    (d / "ports.yaml").unlink()
    with pytest.raises(RegistryError, match=r"ports\.yaml: vocabulary file is missing"):
        Vocab.load(d)
