"""Load and check the controlled vocabularies in ``vocab/``."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml
from pydantic import BaseModel, ValidationError

from junkyard.issues import Issues, RegistryError
from junkyard.models.vocab import (
    ActuatorClass,
    ActuatorClassesFile,
    CategoriesFile,
    Category,
    FunctionsFile,
    FunctionTerm,
    Material,
    MaterialsFile,
    PortsFile,
    PortTypeDef,
)
from junkyard.yamlio import load_yaml

VOCAB_FILES: dict[str, type[BaseModel]] = {
    "functions.yaml": FunctionsFile,
    "ports.yaml": PortsFile,
    "actuator_classes.yaml": ActuatorClassesFile,
    "categories.yaml": CategoriesFile,
    "materials.yaml": MaterialsFile,
}


def normalize_phrase(text: str) -> str:
    """Lowercase, treat ``_`` and ``-`` as spaces, collapse whitespace."""
    return re.sub(r"\s+", " ", re.sub(r"[_\-]", " ", text.lower())).strip()


@dataclass
class Vocab:
    functions: dict[str, FunctionTerm]
    ports: dict[str, PortTypeDef]
    actuator_classes: dict[str, ActuatorClass]
    categories: dict[str, Category]
    materials: dict[str, Material]
    _phrases: dict[str, str]

    def function_for(self, text: str) -> str | None:
        """Resolve an exact function id or alias phrase to a function id."""
        if text in self.functions:
            return text
        return self._phrases.get(normalize_phrase(text))

    @classmethod
    def load(cls, directory: Path, issues: Issues | None = None, display_root: Path | None = None):
        """Load all vocab files. Raises RegistryError unless ``issues`` is given."""
        own = issues is None
        issues = Issues() if own else issues
        parsed: dict[str, BaseModel | None] = {}
        for name, model in VOCAB_FILES.items():
            path = directory / name
            shown = _display(path, display_root)
            if not path.exists():
                issues.add(shown, "", "vocabulary file is missing")
                parsed[name] = None
                continue
            try:
                parsed[name] = model.model_validate(load_yaml(path))
            except yaml.YAMLError as exc:
                issues.add(shown, "", f"invalid YAML: {exc}")
                parsed[name] = None
            except ValidationError as exc:
                issues.add_validation_error(shown, exc)
                parsed[name] = None

        def index(name: str, attr: str, key: str) -> dict:
            data = parsed[name]
            if data is None:
                return {}
            out: dict = {}
            for n, item in enumerate(getattr(data, attr)):
                k = getattr(item, key)
                if k in out:
                    issues.add(
                        _display(directory / name, display_root),
                        f"{attr}[{n}]",
                        f"duplicate {key} {k!r}",
                    )
                out[k] = item
            return out

        vocab = cls(
            functions=index("functions.yaml", "functions", "id"),
            ports=index("ports.yaml", "ports", "type"),
            actuator_classes=index("actuator_classes.yaml", "actuator_classes", "id"),
            categories=index("categories.yaml", "categories", "id"),
            materials=index("materials.yaml", "materials", "id"),
            _phrases={},
        )
        vocab._check(directory, issues, display_root)
        if own and issues:
            raise RegistryError(issues.items)
        return vocab

    def _check(self, directory: Path, issues: Issues, display_root: Path | None) -> None:
        fpath = _display(directory / "functions.yaml", display_root)
        for fid, term in self.functions.items():
            if term.parent is not None and term.parent not in self.functions:
                issues.add(fpath, fid, f"parent {term.parent!r} is not a known function")
        for fid in self.functions:  # cycle check
            seen, cur = set(), fid
            while cur is not None and cur in self.functions:
                if cur in seen:
                    issues.add(fpath, fid, "parent chain forms a cycle")
                    break
                seen.add(cur)
                cur = self.functions[cur].parent

        owner: dict[str, str] = {normalize_phrase(fid): fid for fid in self.functions}
        for fid, term in self.functions.items():
            for alias in term.aliases:
                phrase = normalize_phrase(alias)
                other = owner.get(phrase)
                if other is not None and other != fid:
                    issues.add(fpath, fid, f"alias {alias!r} already resolves to {other!r}")
                    continue
                owner[phrase] = fid
        self._phrases = owner

        ppath = _display(directory / "ports.yaml", display_root)
        for ptype, port in self.ports.items():
            for target in port.mates_with:
                if target not in self.ports:
                    issues.add(ppath, ptype, f"mates_with {target!r} is not a known port type")


def _display(path: Path, root: Path | None) -> str:
    if root is not None:
        try:
            return path.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            pass
    return path.as_posix()
