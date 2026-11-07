# Accepted decisions (PRD section 2)

Copied from `docs/03_JUNKYARD_PRD.md` §2 on 2026-11-07. The PRD is the
authority; this file adds where each decision lives in the repo.

| ID | Decision | Rationale | In the repo |
|---|---|---|---|
| D1 | **CAD kernel: build123d** (OCCT via OCP); `bd_warehouse` allowed for threads, gears, fasteners, bearings (confirm its license is Apache-2.0-compatible first; else reimplement). | Pythonic, Apache-2.0, native joints map onto ports. | Not a dependency yet; added in M2. License check is in `docs/human-tasks.md`. |
| D2 | **Source of truth = files in Git.** No hosted DB. | Reviewable, forkable; the catalog fits in an agent's context. | `vocab/`, `bricks/`, `parts/`, `atlas/`; loaded by `junkyard.registry`. |
| D3 | **Schemas as Pydantic v2 models**, exported to JSON Schema in `schemas/`. | One definition for validation, docs, tool signatures. | `src/junkyard/models/`; `python -m junkyard.models.export`; CI fails on drift. |
| D4 | **Compiled outputs:** `catalog.json`, per-entity JSON, `catalog.sqlite` (FTS5), `llms.txt`, per-entity Markdown, visual assets. | Agents query by MCP, HTTP or reading files. | M2 (build pipeline). |
| D5 | **Local MCP server (stdio)** in the package (`junkyard mcp`). | Generation needs the kernel locally. | M4. |
| D6 | **Static website:** Astro + React islands + three.js; GitHub Pages or Cloudflare Pages. | No server; visuals rendered at build time. | M5 (`web/`). |
| D7 | **Visuals rendered from brick code**, never hand-drawn or AI-generated; each carries a "rendered from vX at params…" caption. | Rights-clean; the picture is the part. | M2 (renders), invariant I6. |
| D8 | **Deterministic search** with documented ordering; no embeddings in v1. | Reproducible, explainable. | M4. Schema export is already deterministic. |
| D9 | **Units explicit, mm/deg/N·m/N/g**, unit suffix in field names. | No guessing. | `models/common.py` (`Unit`, `UNIT_SUFFIX`); params and derived outputs must carry the suffix. See open.md M1-06. |
| D10 | Python ≥ 3.11, `uv`, `ruff`, `pytest`, `typer`, official MCP Python SDK (FastMCP), `pnpm` for web. | Mainstream. | `pyproject.toml`, CI on 3.11 and 3.12. typer and mcp arrive in M4. |
| D11 | **License:** code Apache-2.0 (`LICENSE`); data, docs, renders CC BY 4.0 (`LICENSE-DATA`). | Confirmed. | `LICENSE`, `LICENSE-DATA`; `BrickLicense` model fixes these values. |
| D12 | **Release stage per brick** (`experimental` → `beta` → `stable`) describes **software** quality (API stability, docs completeness), not physical validation. | Honest without a testing program. | `models/brick.py` (`Stage`). |
| D13 | **Standard disclaimer** on every brick page, Markdown and MCP response: "Generated geometry is not verified for printability, fit or strength. Check before printing." | One sentence; no verification machinery. | `models/assembly.py` (`DISCLAIMER`); used by every surface from M4. |
| D14 | **No telemetry in the package.** Funnel measured via site analytics (privacy-friendly, e.g. Plausible), PyPI downloads, GitHub stars, waitlist signups. | Trust for an open tool. | The package makes no network calls. |
