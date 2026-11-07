from __future__ import annotations

import shutil
from collections.abc import Callable
from pathlib import Path

import pytest
import yaml

from junkyard.registry import Registry, load_registry

REPO = Path(__file__).resolve().parents[1]
VOCAB = REPO / "vocab"
FIXTURES = REPO / "tests" / "fixtures"
CATALOG = FIXTURES / "catalog"
INVALID = FIXTURES / "invalid"


@pytest.fixture(scope="session")
def fixture_registry() -> Registry:
    return load_registry(CATALOG, vocab_dir=VOCAB)


@pytest.fixture(scope="session")
def repo_registry() -> Registry:
    return load_registry(REPO)


@pytest.fixture
def catalog_copy(tmp_path: Path) -> Callable[..., Path]:
    """Copy the valid fixture catalog to tmp and let a test edit one YAML file.

    ``edit("bricks/gripper/x/brick.yaml", fn)`` loads the file, calls ``fn(data)``
    to mutate it and writes it back. Returns the catalog root.
    """
    root = tmp_path / "catalog"
    shutil.copytree(CATALOG, root)

    def edit(rel: str | None = None, fn: Callable[[dict], None] | None = None) -> Path:
        if rel is not None and fn is not None:
            path = root / rel
            data = yaml.safe_load(path.read_text())
            fn(data)
            path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True))
        return root

    return edit
