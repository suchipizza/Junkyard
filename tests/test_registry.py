"""Loading and reference resolution across records (PRD 7.1: fail on dangling refs)."""

from __future__ import annotations

import pytest

from junkyard.issues import RegistryError
from junkyard.registry import load_registry

from .conftest import VOCAB

JAW = "bricks/gripper/fixture_parallel_jaw/brick.yaml"
FINGER = "bricks/gripper/fixture_finger/brick.yaml"
SERVO = "parts/servo/fixture_micro.yaml"
MECH_JAW = "atlas/mechanisms/fixture_parallel_jaw.yaml"


def test_valid_fixture_catalog_loads(fixture_registry):
    assert set(fixture_registry.bricks) == {
        "gripper.fixture_parallel_jaw",
        "gripper.fixture_finger",
    }
    assert set(fixture_registry.parts) == {"part.servo.fixture_micro", "part.screw.fixture_m3"}
    assert len(fixture_registry.mechanisms) == 3
    assert not fixture_registry.mechanism("mech.fixture_suction").has_brick


def test_repository_catalog_loads(repo_registry):
    """The real repo (vocab plus whatever bricks/parts/atlas exist) is always valid."""
    assert len(repo_registry.vocab.functions) >= 60


def _fails(root, *fragments):
    with pytest.raises(RegistryError) as info:
        load_registry(root, vocab_dir=VOCAB)
    text = str(info.value)
    for fragment in fragments:
        assert fragment in text, text
    return text


def _set(key, value):
    return lambda d: d.__setitem__(key, value)


@pytest.mark.parametrize(
    ("rel", "mutate", "fragments"),
    [
        (JAW, _set("functions", ["grip_paralel"]),
         ["functions[0]", "unknown function 'grip_paralel'", "did you mean 'grip_parallel'"]),
        (JAW, lambda d: d.update(category="joint", id="joint.fixture_parallel_jaw"),
         ["does not match its folder (expected 'gripper.fixture_parallel_jaw')"]),
        (JAW, lambda d: d["mdi"].update(realizes="mech.nothing"),
         ["mdi.realizes", "unknown mechanism 'mech.nothing'"]),
        (JAW, lambda d: d["mdi"].update(families=["F12", "F01"]),
         ["families ['F01'] are not in mech.fixture_parallel_jaw families"]),
        (JAW, lambda d: d["actuation"].update(accepts_classes=["hobby_servo_9gg"]),
         ["unknown actuator class 'hobby_servo_9gg'"]),
        (JAW, lambda d: d["params"][2].update(default="part.servo.missing"),
         ["params[2].default", "unknown part 'part.servo.missing'"]),
        (JAW, lambda d: d["params"][2].update(allowed_classes=["hobby_servo_standard"]),
         ["is class 'hobby_servo_9g', not one of ['hobby_servo_standard']"]),
        (JAW, lambda d: d["params"][5].update(default="PEEK"),
         ["params[5].default", "unknown material 'PEEK'"]),
        (JAW, lambda d: d["derived"][1].update(expr="stroke_mm / widht_mm"),
         ["refers to unknown name 'widht_mm'"]),
        (JAW, lambda d: d["derived"][1].update(expr="__import__('os')"),
         ["may only"]),
        (JAW, lambda d: d["ports"][1].update(type="finger_mount"),
         ["unknown port type 'finger_mount'", "did you mean 'finger_mount_m3_pair'"]),
        (JAW, lambda d: d["ports"][1]["params"].update(spacing=10),
         ["port type 'finger_mount_m3_pair' has no param 'spacing'"]),
        (JAW, lambda d: d["ports"][2]["params"].update(screw="M6"),
         ["'M6' is not one of ['M2', 'M2.5', 'M3', 'M4', 'M5']"]),
        (JAW, lambda d: d["ports"][2]["params"].update(count=4.5),
         ["expected an integer, got 4.5"]),
        (JAW, lambda d: d["print_hints"].update(material=["PETG", "Wood"]),
         ["print_hints.material[1]", "unknown material 'Wood'"]),
        (JAW, lambda d: d["bom"][1].update(part="part.screw.m3x8_shcs"),
         ["bom[1].part", "unknown part 'part.screw.m3x8_shcs'"]),
        (JAW, _set("pairs_well_with", ["gripper.no_such_brick"]),
         ["unknown brick 'gripper.no_such_brick'"]),
        (MECH_JAW, lambda d: d["alternatives"][0].update(target="mech.ghost"),
         ["alternatives[0].target", "unknown mechanism 'mech.ghost'"]),
        (MECH_JAW, _set("functions", ["grab"]), ["unknown function 'grab'"]),
        (SERVO, _set("class", "hobby_servo_tiny"), ["unknown actuator class 'hobby_servo_tiny'"]),
        (SERVO, lambda d: d["ports"][0]["params"].update(servo_class="nema99"),
         ["unknown actuator class 'nema99'"]),
        (SERVO, _set("id", "part.servo.other"),
         ["does not match its path (expected 'part.servo.fixture_micro')"]),
    ],
)  # fmt: skip
def test_reference_errors_name_file_location_and_value(catalog_copy, rel, mutate, fragments):
    root = catalog_copy(rel, mutate)
    text = _fails(root, *fragments)
    assert rel in text  # the message points at the file to fix


def test_one_way_realization_link_is_reported_on_the_brick(catalog_copy):
    root = catalog_copy(MECH_JAW, _set("realized_by", [{"kind": "none"}]))
    _fails(
        root,
        f"{JAW}: mdi.realizes: mech.fixture_parallel_jaw does not list "
        "gripper.fixture_parallel_jaw in realized_by",
    )


def test_brick_realized_by_other_mechanism_is_reported(catalog_copy):
    root = catalog_copy(
        "atlas/mechanisms/fixture_finger.yaml",
        lambda d: d["realized_by"].append({"kind": "brick", "id": "gripper.fixture_parallel_jaw"}),
    )
    _fails(root, "brick gripper.fixture_parallel_jaw realizes mech.fixture_parallel_jaw")


def test_missing_readme_section_is_reported(catalog_copy):
    root = catalog_copy()
    readme = root / "bricks/gripper/fixture_finger/README.md"
    readme.write_text(readme.read_text().replace("## Strengths\n", ""))
    _fails(
        root,
        "bricks/gripper/fixture_finger/README.md",
        "missing README section(s) ['## Strengths']",
    )


def test_missing_readme_is_reported(catalog_copy):
    root = catalog_copy()
    (root / "bricks/gripper/fixture_finger/README.md").unlink()
    _fails(root, "description_md: README.md not found")


def test_part_in_wrong_folder_is_reported(catalog_copy):
    root = catalog_copy()
    (root / "parts/servo/fixture_micro.yaml").rename(root / "parts/fixture_micro.yaml")
    _fails(root, "part records live at parts/<kind>/<slug>.yaml")


def test_all_issues_are_reported_together(catalog_copy):
    root = catalog_copy(JAW, _set("functions", ["nope_one"]))
    catalog_copy(FINGER, _set("functions", ["nope_two"]))
    text = _fails(root, "nope_one", "nope_two")
    assert text.startswith("2 catalog issue(s)")
