"""Load every catalog record from disk, validate it and resolve references.

``Registry.load(root)`` reads ``vocab/``, ``bricks/``, ``parts/`` and
``atlas/mechanisms/`` under ``root`` and raises :class:`RegistryError` listing
every problem found: schema errors, path/id mismatches, duplicate ids and
dangling references (PRD 7.1: fail on dangling refs).
"""

from __future__ import annotations

import ast
import difflib
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from pydantic import BaseModel, ValidationError

from junkyard.issues import Issues, RegistryError
from junkyard.models.brick import README_SECTIONS, BrickManifest, ParamType, Port
from junkyard.models.mechanism import MechanismRecord, RealizationKind
from junkyard.models.part import PartRecord
from junkyard.models.vocab import enum_options
from junkyard.vocab import Vocab
from junkyard.yamlio import load_yaml

REPO_ROOT = Path(__file__).resolve().parents[2]

_EXPR_FUNCS = {"min", "max", "abs", "round"}
_EXPR_NODES = (
    ast.Expression, ast.BinOp, ast.UnaryOp, ast.Name, ast.Constant, ast.Load, ast.Call,
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow, ast.USub, ast.UAdd,
)  # fmt: skip


@dataclass
class LoadedBrick:
    manifest: BrickManifest
    directory: Path


@dataclass
class Registry:
    root: Path
    vocab: Vocab
    bricks: dict[str, LoadedBrick] = field(default_factory=dict)
    parts: dict[str, PartRecord] = field(default_factory=dict)
    mechanisms: dict[str, MechanismRecord] = field(default_factory=dict)
    _part_paths: dict[str, Path] = field(default_factory=dict, repr=False)
    _mech_paths: dict[str, Path] = field(default_factory=dict, repr=False)

    # --- lookups ------------------------------------------------------------

    def brick(self, brick_id: str) -> BrickManifest:
        return self.bricks[brick_id].manifest

    def part(self, part_id: str) -> PartRecord:
        return self.parts[part_id]

    def mechanism(self, mech_id: str) -> MechanismRecord:
        return self.mechanisms[mech_id]

    # --- loading ------------------------------------------------------------

    @classmethod
    def load(cls, root: Path | str = REPO_ROOT, vocab_dir: Path | str | None = None) -> Registry:
        root = Path(root)
        vocab_dir = Path(vocab_dir) if vocab_dir is not None else root / "vocab"
        issues = Issues()
        vocab = Vocab.load(vocab_dir, issues, display_root=root)
        reg = cls(root=root, vocab=vocab)
        reg._load_bricks(issues)
        reg._load_parts(issues)
        reg._load_mechanisms(issues)
        _Resolver(reg, issues).run()
        if issues:
            raise RegistryError(issues.items)
        return reg

    def _rel(self, path: Path) -> str:
        try:
            return path.resolve().relative_to(self.root.resolve()).as_posix()
        except ValueError:
            return path.as_posix()

    def _read(self, path: Path, model: type[BaseModel], issues: Issues):
        shown = self._rel(path)
        try:
            data = load_yaml(path)
        except yaml.YAMLError as exc:
            issues.add(shown, "", f"invalid YAML: {exc}")
            return None
        if not isinstance(data, dict):
            issues.add(shown, "", "expected a mapping at the top level")
            return None
        try:
            return model.model_validate(data)
        except ValidationError as exc:
            issues.add_validation_error(shown, exc)
            return None

    def _load_bricks(self, issues: Issues) -> None:
        base = self.root / "bricks"
        if not base.is_dir():
            return
        for category_dir in sorted(p for p in base.iterdir() if p.is_dir()):
            for brick_dir in sorted(p for p in category_dir.iterdir() if p.is_dir()):
                path = brick_dir / "brick.yaml"
                if not path.exists():
                    issues.add(self._rel(brick_dir), "", "brick folder has no brick.yaml")
                    continue
                m = self._read(path, BrickManifest, issues)
                if m is None:
                    continue
                expected = f"{category_dir.name}.{brick_dir.name}"
                if m.id != expected:
                    issues.add(
                        self._rel(path),
                        "id",
                        f"id {m.id!r} does not match its folder (expected {expected!r})",
                    )
                if m.id in self.bricks:
                    issues.add(self._rel(path), "id", f"duplicate brick id {m.id!r}")
                    continue
                self.bricks[m.id] = LoadedBrick(m, brick_dir)

    def _load_parts(self, issues: Issues) -> None:
        base = self.root / "parts"
        if not base.is_dir():
            return
        for path in sorted(base.rglob("*.yaml")):
            rel = path.relative_to(base)
            if len(rel.parts) != 2:
                issues.add(self._rel(path), "", "part records live at parts/<kind>/<slug>.yaml")
                continue
            p = self._read(path, PartRecord, issues)
            if p is None:
                continue
            expected = f"part.{rel.parts[0]}.{path.stem}"
            if p.id != expected:
                issues.add(
                    self._rel(path),
                    "id",
                    f"id {p.id!r} does not match its path (expected {expected!r})",
                )
            if p.id in self.parts:
                issues.add(self._rel(path), "id", f"duplicate part id {p.id!r}")
                continue
            self.parts[p.id] = p
            self._part_paths[p.id] = path

    def _load_mechanisms(self, issues: Issues) -> None:
        base = self.root / "atlas" / "mechanisms"
        if not base.is_dir():
            return
        for path in sorted(base.glob("*.yaml")):
            m = self._read(path, MechanismRecord, issues)
            if m is None:
                continue
            expected = f"mech.{path.stem}"
            if m.id != expected:
                issues.add(
                    self._rel(path),
                    "id",
                    f"id {m.id!r} does not match its file name (expected {expected!r})",
                )
            if m.id in self.mechanisms:
                issues.add(self._rel(path), "id", f"duplicate mechanism id {m.id!r}")
                continue
            self.mechanisms[m.id] = m
            self._mech_paths[m.id] = path

    def part_path(self, part_id: str) -> Path:
        return self._part_paths[part_id]


def _suggest(value: str, choices) -> str:
    match = difflib.get_close_matches(value, list(choices), n=1)
    return f" (did you mean {match[0]!r}?)" if match else ""


class _Resolver:
    """Cross-record reference checks."""

    def __init__(self, reg: Registry, issues: Issues) -> None:
        self.reg = reg
        self.v = reg.vocab
        self.issues = issues

    def run(self) -> None:
        for _, loaded in sorted(self.reg.bricks.items()):
            self._brick(loaded, self.reg._rel(loaded.directory / "brick.yaml"))
        for part_id, part in sorted(self.reg.parts.items()):
            self._part(part, self.reg._rel(self.reg.part_path(part_id)))
        for mech_id, mech in sorted(self.reg.mechanisms.items()):
            self._mechanism(mech, self.reg._rel(self.reg._mech_paths[mech_id]))

    # helpers
    def _need(self, path: str, loc: str, value: str, pool, what: str) -> bool:
        if value in pool:
            return True
        self.issues.add(path, loc, f"unknown {what} {value!r}{_suggest(value, pool)}")
        return False

    def _ports(self, path: str, ports: list[Port]) -> None:
        for n, port in enumerate(ports):
            loc = f"ports[{n}]"
            if not self._need(path, f"{loc}.type", port.type, self.v.ports, "port type"):
                continue
            spec = self.v.ports[port.type].params
            for key, value in port.params.items():
                if key not in spec:
                    self.issues.add(
                        path,
                        f"{loc}.params.{key}",
                        f"port type {port.type!r} has no param {key!r} "
                        f"(allowed: {sorted(spec) or 'none'})",
                    )
                    continue
                problem = self._port_value_problem(spec[key], value)
                if problem:
                    self.issues.add(path, f"{loc}.params.{key}", problem)

    def _port_value_problem(self, ptype: str, value) -> str | None:
        if value is None:
            return None
        options = enum_options(ptype)
        is_num = isinstance(value, int | float) and not isinstance(value, bool)
        if options is not None:
            ok = str(value) in options and isinstance(value, str)
            return None if ok else f"{value!r} is not one of {options}"
        if ptype == "int":
            return (
                None
                if isinstance(value, int) and not isinstance(value, bool)
                else (f"expected an integer, got {value!r}")
            )
        if ptype == "float":
            return None if is_num else f"expected a number, got {value!r}"
        if ptype == "bool":
            return None if isinstance(value, bool) else f"expected true/false, got {value!r}"
        if ptype == "actuator_class":
            if value in self.v.actuator_classes:
                return None
            return (
                f"unknown actuator class {value!r}{_suggest(str(value), self.v.actuator_classes)}"
            )
        return None if isinstance(value, str) else f"expected text, got {value!r}"

    # bricks
    def _brick(self, loaded: LoadedBrick, path: str) -> None:
        b = loaded.manifest
        reg, v = self.reg, self.v
        self._need(path, "category", b.category, v.categories, "category")
        for n, f in enumerate(b.functions):
            self._need(path, f"functions[{n}]", f, v.functions, "function")

        mech = reg.mechanisms.get(b.mdi.realizes)
        if self._need(path, "mdi.realizes", b.mdi.realizes, reg.mechanisms, "mechanism"):
            listed = any(r.kind == RealizationKind.brick and r.id == b.id for r in mech.realized_by)
            if not listed:
                self.issues.add(
                    path,
                    "mdi.realizes",
                    f"{mech.id} does not list {b.id} in realized_by; "
                    "add it there so the link goes both ways",
                )
            extra = sorted(set(b.mdi.families) - set(mech.families))
            if extra:
                self.issues.add(
                    path,
                    "mdi.families",
                    f"families {extra} are not in {mech.id} families {mech.families}",
                )

        if b.actuation:
            for n, c in enumerate(b.actuation.accepts_classes):
                self._need(
                    path, f"actuation.accepts_classes[{n}]", c, v.actuator_classes, "actuator class"
                )
            if b.actuation.default_part is not None:
                self._part_in_classes(
                    path,
                    "actuation.default_part",
                    b.actuation.default_part,
                    b.actuation.accepts_classes,
                )

        for n, p in enumerate(b.params):
            loc = f"params[{n}]"
            if p.type == ParamType.part_ref:
                for k, c in enumerate(p.allowed_classes or []):
                    self._need(
                        path, f"{loc}.allowed_classes[{k}]", c, v.actuator_classes, "actuator class"
                    )
                self._part_in_classes(
                    path, f"{loc}.default", str(p.default), p.allowed_classes or []
                )
            elif p.type == ParamType.material:
                self._need(path, f"{loc}.default", str(p.default), v.materials, "material")
                for k, o in enumerate(p.options or []):
                    self._need(path, f"{loc}.options[{k}]", o, v.materials, "material")

        self._derived(path, b)
        self._ports(path, b.ports)
        if b.print_hints:
            for n, mat in enumerate(b.print_hints.material):
                self._need(path, f"print_hints.material[{n}]", mat, v.materials, "material")
        for n, line in enumerate(b.bom):
            if not line.part.startswith("@"):
                self._need(path, f"bom[{n}].part", line.part, reg.parts, "part")
        for n, other in enumerate(b.pairs_well_with):
            if other == b.id:
                self.issues.add(path, f"pairs_well_with[{n}]", "a brick cannot pair with itself")
            else:
                self._need(path, f"pairs_well_with[{n}]", other, reg.bricks, "brick")
        self._readme(path, loaded)

    def _part_in_classes(self, path: str, loc: str, part_id: str, classes: list[str]) -> None:
        if not self._need(path, loc, part_id, self.reg.parts, "part"):
            return
        cls_ = self.reg.parts[part_id].class_
        if cls_ is None:
            self.issues.add(
                path, loc, f"part {part_id!r} has no class, so it cannot fill {classes}"
            )
        elif cls_ not in classes:
            self.issues.add(path, loc, f"part {part_id!r} is class {cls_!r}, not one of {classes}")

    def _derived(self, path: str, b: BrickManifest) -> None:
        known = {p.name for p in b.params}
        for n, d in enumerate(b.derived):
            if d.expr is not None:
                problem = _expr_problem(d.expr, known)
                if problem:
                    self.issues.add(path, f"derived[{n}].expr", problem)
            known.add(d.name)

    def _readme(self, path: str, loaded: LoadedBrick) -> None:
        md = loaded.directory / loaded.manifest.description_md
        if not md.exists():
            self.issues.add(path, "description_md", f"{loaded.manifest.description_md} not found")
            return
        headings = {
            line.rstrip()
            for line in md.read_text(encoding="utf-8").splitlines()
            if line.startswith("## ")
        }
        missing = [h for h in README_SECTIONS if h not in headings]
        if missing:
            self.issues.add(self.reg._rel(md), "", f"missing README section(s) {missing} (PRD 5.2)")

    # parts
    def _part(self, part: PartRecord, path: str) -> None:
        if part.class_ is not None:
            self._need(path, "class", part.class_, self.v.actuator_classes, "actuator class")
        self._ports(path, part.ports)

    # mechanisms
    def _mechanism(self, mech: MechanismRecord, path: str) -> None:
        reg = self.reg
        for n, f in enumerate(mech.functions):
            self._need(path, f"functions[{n}]", f, self.v.functions, "function")
        for n, alt in enumerate(mech.alternatives):
            self._need(path, f"alternatives[{n}].target", alt.target, reg.mechanisms, "mechanism")
        for n, r in enumerate(mech.realized_by):
            loc = f"realized_by[{n}].id"
            if r.kind == RealizationKind.brick:
                if self._need(path, loc, r.id, reg.bricks, "brick"):
                    realizes = reg.brick(r.id).mdi.realizes
                    if realizes != mech.id:
                        self.issues.add(
                            path, loc, f"brick {r.id} realizes {realizes}, not {mech.id}"
                        )
            elif r.kind == RealizationKind.part:
                self._need(path, loc, r.id, reg.parts, "part")


def _expr_problem(expr: str, names: set[str]) -> str | None:
    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError:
        return f"expression {expr!r} is not valid"
    for node in ast.walk(tree):
        if not isinstance(node, _EXPR_NODES):
            return f"expression {expr!r} uses unsupported syntax ({type(node).__name__})"
        if isinstance(node, ast.Call) and not (
            isinstance(node.func, ast.Name) and node.func.id in _EXPR_FUNCS
        ):
            return f"expression {expr!r} may only call {sorted(_EXPR_FUNCS)}"
        if isinstance(node, ast.Constant) and not isinstance(node.value, int | float):
            return f"expression {expr!r} may only use numbers"
        if isinstance(node, ast.Name) and node.id not in names and node.id not in _EXPR_FUNCS:
            return (
                f"expression {expr!r} refers to unknown name {node.id!r}{_suggest(node.id, names)}"
            )
    return None


def load_registry(root: Path | str = REPO_ROOT, vocab_dir: Path | str | None = None) -> Registry:
    """Load and validate the catalog under ``root`` (default: this repository)."""
    return Registry.load(root, vocab_dir)
