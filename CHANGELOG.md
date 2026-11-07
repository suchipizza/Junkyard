# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added (M1 Foundations)

- Repository scaffold per PRD §4, `pyproject.toml` (`junkyard-robotics`, Python ≥ 3.11),
  Apache-2.0 code license and CC BY 4.0 data license.
- Pydantic v2 models for brick manifests, part records, Atlas mechanism records,
  vocabularies, `assembly.json` and generated-file sidecars, with JSON Schema export
  to `schemas/` (`python -m junkyard.models.export [--check]`).
- Vocabularies: 84 functions with natural-language aliases, 15 port types,
  9 actuator classes, 10 categories, 6 materials.
- Strict YAML loading (duplicate keys rejected) and a registry that validates every
  record, checks path/id agreement and resolves all cross-references, reporting
  every issue as `<file>: <location>: <message>`.
- `Ctx.spec()` and `MissingSpec` (invariant I2), plus a static check that
  generators never read `.specs` directly.
- Tests: 40 invalid fixtures with expected messages, reference-resolution cases,
  vocabulary checks, schema drift, invariants I1 and I2.
- CI: ruff, schema drift, catalog load, pytest on Python 3.11 and 3.12.
- Docs: `CLAUDE.md`, `docs/decisions/` (D1–D14, O1–O3, M1 defaults),
  `docs/human-tasks.md`, `docs/next-product-hooks.md`, doc stubs.
