"""Static checks on generator source (invariant I2).

Generators must read part specs through ``ctx.spec()``, which raises
``MissingSpec`` on null values. Touching ``.specs`` directly could read a null
silently, so it is flagged.
"""

from __future__ import annotations

import ast
from pathlib import Path


def raw_spec_reads(source: str) -> list[int]:
    """Line numbers where ``source`` accesses a ``.specs`` attribute."""
    tree = ast.parse(source)
    return sorted(
        node.lineno
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute) and node.attr == "specs"
    )


def generator_files(bricks_dir: Path) -> list[Path]:
    """Every Python file inside brick folders (generators, kinematics, helpers)."""
    if not bricks_dir.is_dir():
        return []
    return sorted(p for p in bricks_dir.rglob("*.py") if "tests" not in p.parts)
