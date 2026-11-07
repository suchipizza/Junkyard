# Schema

The record formats are defined once, as Pydantic models in
`src/junkyard/models/`, and exported to JSON Schema in `schemas/`:

| File | Record |
|---|---|
| `brick.schema.json` | `bricks/<category>/<slug>/brick.yaml` |
| `part.schema.json` | `parts/<kind>/<slug>.yaml` |
| `mechanism.schema.json` | `atlas/mechanisms/<slug>.yaml` |
| `assembly.schema.json` | `assembly.json` written by `export_assembly` |
| `sidecar.schema.json` | `<file>.junkyard.json` next to generated files |
| `vocab.*.schema.json` | files in `vocab/` |

Field-by-field reference pages are generated from these schemas for the website
in M5. Until then, read the models: each field has a type and, where useful, a
description. See PRD §5 for the intent behind each record.
