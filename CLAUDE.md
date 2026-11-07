# CLAUDE.md

Guidance for coding agents working in this repo. The spec is
`docs/03_JUNKYARD_PRD.md`; where companion docs disagree, the PRD wins.

## Hard rules

1. **Never invent component dimensions.** Part specs (servo body size, hole
   pitch, bearing bore…) come from a datasheet or cited reference drawing. If
   you cannot open the source: `value: null`, `verification: unverified`, add a
   line to `docs/human-tasks.md`, and let generators raise `MissingSpec`.
2. **Do not build verification.** No printability, interference, strength or
   torque checks, no test records, no benchmarks.
3. **Invariants (below) are hard rules**, each backed by a test. If a feature
   conflicts with one, stop and add a `DECISION NEEDED:` entry to
   `docs/decisions/open.md`.
4. One branch and PR per milestone, small commits, a `CHANGELOG.md` entry, green CI.

## Invariants (PRD §13, tests in `tests/invariants/`)

| ID | Rule | Status |
|---|---|---|
| I1 | Every non-null part spec value has a `source`. | Tested (M1) |
| I2 | A generator never reads a null spec silently; it raises `MissingSpec`, surfaced as `missing_spec`. | Tested (M1) |
| I3 | Every MCP response and JSON record includes `library_version` and `catalog_hash`; every brick response includes the disclaimer. | M4 |
| I4 | MCP `get_brick` equals `/api/v1/bricks/{id}.json` for shared fields. | M4 |
| I5 | Same query + same catalog → byte-identical output. | M2 |
| I6 | No rendered visual without a caption stating brick ID, version and params. | M2 |
| I7 | No `motion.json` for bricks without `kinematics.py`. | M2 |
| I8 | No text, image or CAD file copied from a source without an allow-listed license. | Enforced by the model (M1); gate test M2 |
| I9 | "tested", "proven", "validated", "verified" never describe bricks in generated pages or tool output. | M5 (see open.md M1-17) |

## Conventions

- **Units** explicit and in field names: `_mm _deg _nm _n _g _v _s _rpm _percent` (D9).
- **Unknown is `null`**, never `0`, `false` or `""`. The models reject the latter.
- **IDs** are stable forever: bricks `<category>.<slug>`, parts `part.<kind>.<slug>`,
  mechanisms `mech.<slug>`. Files live at `bricks/<category>/<slug>/brick.yaml`,
  `parts/<kind>/<slug>.yaml`, `atlas/mechanisms/<slug>.yaml`, and the loader
  checks that path and id agree.
- **Generators read specs only through `ctx.spec(part, field)`**, never `part.specs`
  (a static check enforces this).
- **Schemas** in `schemas/` are generated; never hand-edit. After changing a model:
  `uv run python -m junkyard.models.export`.
- Every constant in a generator gets a comment naming its origin (param, part
  spec, standard such as ISO 4762, or "design choice").
- Original text only in READMEs and Atlas records; link sources, never copy them.
- Releases describe software maturity (`experimental`/`beta`/`stable`), never physical validation.

## Commands

```sh
uv sync                                     # install
uv run pytest                               # tests, including invariants
uv run ruff check . && uv run ruff format --check .
uv run python -m junkyard.models.export     # regenerate schemas/
uv run python -m junkyard.models.export --check
uv run python -c "from junkyard.registry import load_registry; load_registry()"
```

## Layout

`src/junkyard/models/` Pydantic schemas · `vocab.py` and `registry.py` loaders and
reference resolution · `sdk/` generator context and `MissingSpec` · `vocab/`
controlled vocabularies · `tests/fixtures/` fictional records for tests (never
copy fixture values into `parts/`) · `docs/decisions/` accepted and open decisions.

## Milestone status

M1 Foundations: done on branch `m1-foundations`. Next: M2 (`joint.pin_revolute`
end to end).
