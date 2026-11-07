"""Strict YAML loading: safe loader that also rejects duplicate keys.

PyYAML silently keeps the last of two identical keys, which would hide typos
in hand-edited records.
"""

from __future__ import annotations

from pathlib import Path

import yaml


class DuplicateKeyError(yaml.YAMLError):
    pass


class _StrictLoader(yaml.SafeLoader):
    pass


def _construct_mapping(loader: _StrictLoader, node: yaml.MappingNode, deep: bool = False):
    seen: set = set()
    for key_node, _ in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in seen:
            line = key_node.start_mark.line + 1
            raise DuplicateKeyError(f"duplicate key {key!r} on line {line}")
        seen.add(key)
    return loader.construct_mapping(node, deep=deep)


_StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as f:
        return yaml.load(f, Loader=_StrictLoader)
