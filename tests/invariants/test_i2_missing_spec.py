"""I2: a generator never reads a null spec silently; it raises MissingSpec,
surfaced as a ``missing_spec`` error naming the field."""

from __future__ import annotations

import pytest

from junkyard.sdk import Ctx, MissingSpec, UnknownPart
from junkyard.sdk.lint import generator_files, raw_spec_reads

from ..conftest import FIXTURES, REPO

SERVO = "part.servo.fixture_micro"


@pytest.fixture
def ctx(fixture_registry) -> Ctx:
    return Ctx(fixture_registry)


def test_null_spec_raises_missing_spec_naming_the_field(ctx):
    with pytest.raises(MissingSpec) as info:
        ctx.spec(ctx.part(SERVO), "body_l_mm")
    err = info.value.to_error()["error"]
    assert err["code"] == "missing_spec"
    assert err["field"] == "body_l_mm"
    assert err["part"] == SERVO
    assert "body_l_mm" in err["message"]
    assert err["hint"]


def test_unrecorded_spec_raises_missing_spec(ctx):
    with pytest.raises(MissingSpec, match="'spline_od_mm' is not recorded"):
        ctx.spec(SERVO, "spline_od_mm")


def test_sourced_spec_is_returned(ctx):
    assert ctx.spec(SERVO, "mass_g") == 1.0


def test_every_null_spec_in_every_catalog_raises(ctx, fixture_registry, repo_registry):
    checked = 0
    for registry in (fixture_registry, repo_registry):
        c = Ctx(registry)
        for part in registry.parts.values():
            for field, spec in part.specs.items():
                if spec.value is None:
                    with pytest.raises(MissingSpec):
                        c.spec(part, field)
                    checked += 1
    assert checked > 0


def test_unknown_part_raises_unknown_part(ctx):
    with pytest.raises(UnknownPart) as info:
        ctx.part("part.servo.fixture_micr")
    assert info.value.to_error()["error"]["code"] == "unknown_part"
    assert "part.servo.fixture_micro" in info.value.hint


def test_static_check_flags_direct_spec_reads():
    bad = (FIXTURES / "generators/bad_generator.py").read_text()
    good = (FIXTURES / "generators/good_generator.py").read_text()
    assert raw_spec_reads(bad) == [4]
    assert raw_spec_reads(good) == []


def test_no_generator_reads_specs_directly():
    offenders = {
        p.relative_to(REPO).as_posix(): lines
        for p in generator_files(REPO / "bricks")
        if (lines := raw_spec_reads(p.read_text()))
    }
    assert offenders == {}, f"use ctx.spec() instead of .specs: {offenders}"
