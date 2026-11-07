# Junkyard

A free, open-source library of parametric mechanical parts for robots
(**bricks**: joints, motor mounts, grippers, gears, linear stages, linkages,
locks, pulleys, structure, wheels). Each brick is a small, readable
[build123d](https://github.com/gumyr/build123d) generator plus the metadata an
AI coding agent needs to choose, size, combine and explain it.

> **Status: early development (milestone M1 of 7).** This repo currently holds
> the schemas, vocabularies and loaders. There are no bricks yet. See
> `docs/03_JUNKYARD_PRD.md` for the plan.

Generated geometry is not verified for printability, fit or strength. Check
before printing.

## What is here

| Path | Contents |
|---|---|
| `src/junkyard/models/` | Pydantic models for bricks, parts, Atlas mechanisms, vocabularies, `assembly.json` |
| `schemas/` | JSON Schemas generated from the models |
| `vocab/` | Functions (with the phrases agents use), port types, actuator classes, categories, materials |
| `src/junkyard/registry.py` | Loads every record, validates it and resolves references |
| `docs/` | PRD and companion specs, decisions, human tasks |

## Development

```sh
uv sync
uv run pytest
```

Python ≥ 3.11. Package name on PyPI: `junkyard-robotics`; import name `junkyard`.

## License

Code: Apache-2.0 (`LICENSE`). Data, docs and renders: CC BY 4.0 (`LICENSE-DATA`).
