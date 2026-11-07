# Junkyard — Product Requirements Document (v1 build)

**Version:** 0.2 · **Date:** 7 November 2026 · **Owner:** Noémie · **Audience:** Claude Code (implementer) and human reviewers
**Repo:** https://github.com/suchipizza/Junkyard · **PyPI distribution:** `junkyard-robotics` (`Junkyard` is taken) · **Import name / CLI:** `junkyard`
**Companions:** `MDI Brick Library — Product Description.md`, `01_PROJECT_SPECIFICATION.md`, `02_RESEARCH_AND_BUILD_PLAN.md`. Where they disagree with this PRD, **this PRD wins**: physical validation, checks, test records, maturity levels and benchmarks described there are out of scope for this product.

---

## 0. How to use this document (read first, Claude Code)

1. Read sections 1–3 for intent, then build milestone by milestone (section 15). Each milestone has acceptance criteria that must pass before the next starts.
2. **Invariants in section 13 are hard rules**, each backed by a test. If a feature conflicts with one, stop and add a `DECISION NEEDED:` note to `docs/decisions/open.md`.
3. **Never invent component dimensions.** Part specs (servo body size, hole pitch, bearing bore…) come from a datasheet or a cited reference drawing. If you cannot open the source, write `null`, keep `verification: unverified`, add a line to `docs/human-tasks.md`, and make generators raise `MissingSpec` rather than guess. A brick that fits the wrong servo is worse than no brick.
4. **Do not build verification.** No printability analysis, interference detection, stress/torque checks, test records or benchmarks. Those belong to a later product built with other tools. This library generates parts and describes them well.
5. Small commits, one branch and PR per milestone, `CHANGELOG.md` entry, green CI.

---

## 1. Product summary

**Junkyard** is a free, open-source library of parametric mechanical parts for robots (**bricks**: joints, motor mounts, grippers, gears and reducers, linear stages, linkages, locks, pulleys, structure, wheels). Each brick is a small, readable build123d Python generator that turns parameters into STL/STEP, plus the metadata an agent needs to choose, size, combine and explain it.

**Goal:** be the most complete, best-documented, most agent-ready parametric robot parts library available, so that AI coding agents and makers reach for it by default. It is a **funnel**: free, generous, no lock-in, building the audience and the structured data the next Junkyard product will use. It is not the moat and does not need to be.

**What "really good" means here:**
- **Complete:** ~50 bricks and ~40 real parts at v1, covering most of what a desktop hobby robot needs.
- **Correct dimensions:** mounts, shafts, splines, bearing seats and screw holes match the real components (sourced specs, clearance as a parameter).
- **Readable source:** shadcn-style; `junkyard add <id>` copies the code into the user's project to read and modify.
- **Agent-ready:** MCP server, typed parameters with units and valid ranges, function-first search, named connection points (ports), Markdown and JSON twins of every page, `llms.txt`, an agent skill.
- **Beautiful website:** every brick rendered from its code in 3D and in technical-plate style, animated where the motion is simple, with parameter sliders.

**Users:** primary, coding agents (Claude Code, Cursor, any MCP client) building robots for a person; secondary, makers and students browsing the site.

**Three layers, one repo:**

| Layer | What it is | v1 size |
|---|---|---|
| **Bricks** | Parametric generators + metadata | ~50 |
| **Parts** | Spec records for off-the-shelf components bricks are sized against | ~40 |
| **Atlas** (MDI-lite) | Mechanism records: what each mechanism does, alternatives, `realized_by` brick | ~50 (one per brick) + ~15 "no brick yet" |

**Explicitly out of scope:** printability/interference/strength checks, physical testing, test records, maturity levels, benchmarks, goal-to-robot pipeline, electronics/firmware, accounts, hosted DB, paid tier.

---

## 2. Decisions

| ID | Decision | Rationale |
|---|---|---|
| D1 | **CAD kernel: build123d** (OCCT via OCP); `bd_warehouse` allowed for threads, gears, fasteners, bearings (confirm its license is Apache-2.0-compatible first; else reimplement). | Pythonic, Apache-2.0, native joints map onto ports. |
| D2 | **Source of truth = files in Git.** No hosted DB. | Reviewable, forkable; the catalog fits in an agent's context. |
| D3 | **Schemas as Pydantic v2 models**, exported to JSON Schema in `schemas/`. | One definition for validation, docs, tool signatures. |
| D4 | **Compiled outputs:** `catalog.json`, per-entity JSON, `catalog.sqlite` (FTS5), `llms.txt`, per-entity Markdown, visual assets. | Agents query by MCP, HTTP or reading files. |
| D5 | **Local MCP server (stdio)** in the package (`junkyard mcp`). | Generation needs the kernel locally. |
| D6 | **Static website:** Astro + React islands + three.js; GitHub Pages or Cloudflare Pages. | No server; visuals rendered at build time. |
| D7 | **Visuals rendered from brick code**, never hand-drawn or AI-generated; each carries a "rendered from vX at params…" caption. | Rights-clean; the picture is the part. |
| D8 | **Deterministic search** with documented ordering; no embeddings in v1. | Reproducible, explainable. |
| D9 | **Units explicit, mm/deg/N·m/N/g**, unit suffix in field names. | No guessing. |
| D10 | Python ≥ 3.11, `uv`, `ruff`, `pytest`, `typer`, official MCP Python SDK (FastMCP), `pnpm` for web. | Mainstream. |
| D11 | **License:** code Apache-2.0 (`LICENSE`); data, docs, renders CC BY 4.0 (`LICENSE-DATA`). | Confirmed. |
| D12 | **Release stage per brick** (`experimental` → `beta` → `stable`) describes **software** quality (API stability, docs completeness), not physical validation. | Honest without a testing program. |
| D13 | **Standard disclaimer** on every brick page, Markdown and MCP response: "Generated geometry is not verified for printability, fit or strength. Check before printing." | One sentence; no verification machinery. |
| D14 | **No telemetry in the package.** Funnel measured via site analytics (privacy-friendly, e.g. Plausible), PyPI downloads, GitHub stars, waitlist signups. | Trust for an open tool. |

Open (default used until the owner confirms): **O1** domain (`junkyard.dev` placeholder in config). **O2** waitlist provider (default: a plain form posting to a configurable endpoint; no vendor hard-coded). **O3** analytics provider (default: none wired; config slot only).

---

## 3. Scope of this build

**In:** monorepo, schemas, vocabularies, build pipeline, CI; ~50 bricks in two waves (section 11); ~40 parts; Atlas-lite records; Python API; CLI; MCP server; agent skill; website with gallery, brick pages, viewer, parts, atlas, docs, agent endpoints, waitlist CTA; assembly export format for future tools (section 14).

**Out:** see section 1.

---

## 4. Repository layout

```text
Junkyard/
  README.md  LICENSE  LICENSE-DATA  CHANGELOG.md  CLAUDE.md  pyproject.toml
  src/junkyard/
    __init__.py          # public API: search, get, generate, add, export
    models/              # Pydantic schemas (section 5)
    vocab.py  registry.py
    sdk/                 # @brick, @kinematics, Param, Port, Ctx, MissingSpec
    query/               # search, filters, port compatibility lookup
    build/               # build pipeline (section 7)
    render/              # GLB, PNG, SVG plate, motion frames
    export/              # STL, STEP, GLB, assembly.json (section 14)
    cli.py  mcp_server.py
    data/                # embedded catalog.json at release
  bricks/<category>/<slug>/
    brick.yaml  generator.py  kinematics.py (optional)  README.md  tests/ (optional)
  parts/<kind>/<slug>.yaml
  atlas/mechanisms/<slug>.yaml
  vocab/  functions.yaml  ports.yaml  actuator_classes.yaml  categories.yaml  materials.yaml
  schemas/               # generated, do not hand-edit
  skill/  SKILL.md  junkyard-agent-guide.md
  web/                   # Astro site
  docs/  decisions/  human-tasks.md  authoring-a-brick.md  schema.md  agents.md
         contributing.md  source-rights-policy.md
  tests/
  .github/workflows/  .github/ISSUE_TEMPLATE/
```

IDs: bricks `<category>.<slug>` (`gripper.fin_ray_finger`), parts `part.<kind>.<slug>` (`part.servo.sg90`), Atlas `mech.<slug>`. Stable forever; renames add aliases.

---

## 5. Data model

Every record has `id`, `schema_version`, `updated_at`. Unknown values are `null`, never `0`/`false`/`""`.

### 5.1 Brick manifest (`brick.yaml`)

```yaml
id: gripper.parallel_jaw_rack
schema_version: 0.2.0
name: Parallel jaw gripper (rack and pinion)
category: gripper
stage: beta                                   # experimental | beta | stable (D12)
summary: Two jaws on racks driven by one servo pinion; jaws stay parallel through the stroke.
description_md: README.md                     # sections in 5.2
functions: [grip_parallel, grip_fragile_irregular]
mdi: { realizes: mech.parallel_jaw_rack_gripper, families: [F12, F06] }
tags: [servo, gripper, beginner]
difficulty: beginner                          # beginner | intermediate | advanced (assembly effort)
actuation:
  accepts_classes: [hobby_servo_9g, hobby_servo_standard]
  default_part: part.servo.sg90
params:
  - name: opening_mm
    type: float
    unit: mm
    default: 40
    range: [20, 70]                           # generator produces valid geometry here (CI-enforced)
    description: Maximum distance between jaw faces.
  - name: pinion_teeth
    type: int
    default: 16
    range: [12, 24]
  - name: servo
    type: part_ref
    default: part.servo.sg90
    allowed_classes: [hobby_servo_9g, hobby_servo_standard]
  - name: clearance_mm
    type: float
    unit: mm
    default: 0.25
    range: [0.1, 0.6]
    description: Sliding-fit clearance; tune to your printer.
derived:                                      # computed outputs agents can read without generating
  - { name: stroke_mm, unit: mm, expr: "opening_mm" }
  - { name: envelope_mm, unit: mm, from: bbox }        # filled by the build
outputs: [base, pinion, jaw_left, jaw_right] # named solids
ports:
  - name: servo_body
    type: servo_body_mount
    gender: female
    params_from: servo
    frame: { origin_mm: [0, 0, 0], z_axis: [0, 0, 1], x_axis: [1, 0, 0] }
  - name: jaw_left_face
    type: finger_mount_m3_pair
    gender: female
    params: { spacing_mm: 10 }
    frame: { origin_mm: [-20, 0, 30], z_axis: [1, 0, 0], x_axis: [0, 0, 1] }
  - name: base_mount
    type: bolt_pattern
    gender: female
    params: { screw: M3, count: 4, pitch_x_mm: 30, pitch_y_mm: 20 }
    frame: { origin_mm: [0, 0, -5], z_axis: [0, 0, -1], x_axis: [1, 0, 0] }
print_hints:                                  # recommendations, not verified
  material: [PETG, PLA]
  layer_height_mm: 0.2
  infill_percent: 30
  supports: none
  orientation: { base: bottom_down, racks: flat }
bom:
  - { part: "@servo", qty: 1 }
  - { part: part.screw.m3x8_shcs, qty: 6 }
  - { part: part.insert.m3_heat_set, qty: 4 }
assembly_steps:
  - Press heat-set inserts into base.
  - Center servo at 90° before fitting pinion.
  - Slide racks in; check they move freely before tightening.
pairs_well_with: [gripper.fin_ray_finger, motor.servo_mount]
visuals:
  hero_params: [opening_mm]
  color_roles: { input: [pinion], output: [jaw_left, jaw_right], fixed: [base] }
provenance:
  origin: original                            # original | adapted | imported
  authors: ["Junkyard contributors"]
  inspired_by: []                             # links to reference designs (ideas only)
  imported_files: []                          # { path, source_url, license }
license: { code: Apache-2.0, data: CC-BY-4.0 }
```

Param types: `float`, `int`, `bool`, `enum` (`options`), `part_ref` (`allowed_classes`), `material` (enum from vocab). Numeric params need `unit` and `range`. Values outside `range` are rejected by `generate` with `outside_range` unless `force=true` (then a warning is attached).

### 5.2 Brick README sections (rendered on site and in Markdown twin)

`## What it does` · `## How it works` (2–5 sentences, original text) · `## Typical uses` · `## Choosing parameters` (what each key param changes, trade-offs) · `## Strengths` · `## Watch out for` (design notes, labeled as such) · `## Assembly` · `## Customizing the code` (where to edit for common changes) · `## Related bricks`.

### 5.3 Ports

Declared once in `vocab/ports.yaml` with typed params and a match rule; used for **discovery** ("what mounts on this?") and for assembly export, not for verification.

```yaml
- type: servo_horn_spline
  params: { spline_teeth: int, spline_od_mm: float }
  mates_with: servo_horn_spline
  gender_rule: opposite
  match_keys: [spline_teeth]
- type: servo_body_mount
  params: { body_l_mm: float, body_w_mm: float, tab_hole_pitch_mm: float, tab_hole_d_mm: float }
  match_keys: [servo_class]
- type: bolt_pattern
  params: { screw: enum[M2,M2.5,M3,M4,M5], count: int, pitch_x_mm: float, pitch_y_mm: float }
  match_keys: [screw, count, pitch_x_mm, pitch_y_mm]
```

Initial types: `servo_horn_spline`, `servo_body_mount`, `nema17_face`, `nema14_face`, `n20_face`, `shaft_round`, `shaft_d`, `bearing_seat`, `bolt_pattern`, `finger_mount_m3_pair`, `pin_bore`, `gt2_belt_clamp`, `extrusion_2020_slot`, `rod_8mm`, `leadscrew_t8_nut`. Each port has a `frame` (origin + z/x axes) used for build123d `RigidJoint`s, viewer gizmos and `assembly.json`.

### 5.4 Part record (`parts/servo/sg90.yaml`)

```yaml
id: part.servo.sg90
schema_version: 0.2.0
name: SG90 micro servo (9 g class)
class: hobby_servo_9g
aliases: [TowerPro SG90, 9g servo]
specs:
  body_l_mm:         { value: null, source: null, verification: unverified }
  body_w_mm:         { value: null, source: null, verification: unverified }
  body_h_mm:         { value: null, source: null, verification: unverified }
  tab_hole_pitch_mm: { value: null, source: null, verification: unverified }
  spline_teeth:      { value: null, source: null, verification: unverified }
  stall_torque_nm:   { value: null, at_voltage_v: 4.8, source: null, verification: unverified }
  mass_g:            { value: null, source: null, verification: unverified }
variance_note: Clones vary; measure fit-critical dimensions on your unit.
ports: [ ... ]
datasheets: [ { url: null, title: null, retrieved: null } ]
where_to_buy: []                               # generic search terms only, no affiliate links in v1
```

`verification`: `unverified` → `datasheet` (a human confirmed against the cited source). Source object: `{ url, title, kind: datasheet|reference_drawing|standard|web, retrieved, location }`.

Parts can also carry a simple **reference model** generator (`parts/<kind>/<slug>.py`, optional) producing an envelope solid for visual context in the viewer (e.g. a gray SG90 block in the mount). Reference models are clearly labeled "reference shape, not for printing".

### 5.5 Atlas record (MDI-lite)

Subset of `01_PROJECT_SPECIFICATION.md` §7: `id`, `entity_type`, `canonical_name`, `aliases`, `families` (F01–F18), `functions`, `input_motion`, `output_motion`, `summary` (original text), `strengths[]`, `watch_outs[]`, `alternatives[]` (`target`, `context`, `tradeoffs`), `realized_by[]` (`kind: brick|part|external_reference|none`, `id`/`url`), `sources[]`, `review_status: draft|reviewed`. Atlas records with no brick power the **"No brick yet"** list (contribution roadmap).

### 5.6 Vocabularies

- `functions.yaml`: ≥ 60 function IDs with `label`, `definition`, `aliases` (natural phrases agents use: "pick up a grape" → `grip_fragile_irregular`; "make it go up and down" → `linear_actuation_vertical`), `parent`.
- `actuator_classes.yaml`: `hobby_servo_9g`, `hobby_servo_standard`, `hobby_servo_high_torque`, `nema17_stepper`, `nema14_stepper`, `geared_stepper_28byj48`, `n20_gearmotor`, `tt_gearmotor`, `manual`.
- `categories.yaml`: `joint`, `motor`, `gripper`, `gear`, `linear`, `linkage`, `lock`, `transmission`, `structure`, `wheel`.
- `materials.yaml`: names and process only (`PLA`, `PETG`, `TPU95A`, `ABS`, `ASA`, `Nylon`); no property values in v1.

---

## 6. Brick author SDK

### 6.1 Generator

```python
from junkyard.sdk import brick, Ctx, MissingSpec
from build123d import *

@brick("gripper.parallel_jaw_rack")
def generate(p, ctx: Ctx) -> dict[str, Part]:
    """Return named solids matching brick.yaml `outputs`."""
    servo = ctx.part(p.servo)      # resolved part record; ctx.spec(servo, "body_l_mm") raises MissingSpec if null
    ...
    return {"base": base, "pinion": pinion, "jaw_left": jl, "jaw_right": jr}
```

Rules: pure and deterministic; no I/O or network; ≤ ~250 lines (split helpers into `_helpers.py` in the brick folder if needed); every constant commented with its origin (param, part spec, standard such as ISO 4762, or "design choice"); named solids only; readable over clever (agents will edit it). Shared geometry helpers (fillets, counterbores, heat-set insert holes, nut traps, involute gears) live in `junkyard.sdk.features` and are also copied by `junkyard add` when used.

### 6.2 Kinematics (optional, for animation only)

```python
@kinematics
def model(p, ctx):
    return {
      "input":   Joint("pinion", kind="revolute", axis=[0,0,1], range=(-90, 90), unit="deg"),
      "coupled": { "jaw_left":  lambda t: {"translate_mm": [-r(p)*rad(t), 0, 0]},
                   "jaw_right": lambda t: {"translate_mm": [ r(p)*rad(t), 0, 0]} },
      "outputs": { "opening_mm": lambda t: p.opening_mm/2 + 2*r(p)*rad(t) },   # motion graph
    }
```

Only for rigid motion that is simple to describe (revolute, prismatic, gear/rack coupling, linkage solved by closed-form or a small numeric solver in `sdk.linkage`). Compliant bricks (living hinge, Fin Ray, flexure pivot) have no animation; the site shows them static. Captions say "kinematic illustration".

---

## 7. Build pipeline (`junkyard build`)

1. **Load & validate** YAML; resolve refs (parts, vocab, `mech.*`, ports); fail on dangling refs.
2. **Generate** each brick at defaults, at every `range` edge (one param at a time), and at hero-param steps (5 values per hero param, ≤ 25 variants). A generator failing or returning an empty/invalid solid fails the build (code correctness, not printability).
3. **Derive** `envelope_mm` (bbox at defaults), volume per part, `derived` outputs.
4. **Render** per variant GLB (meshopt, target ≤ 500 KB); at defaults PNG thumbnail (iso, 2×, transparent), SVG plate (front elevation, visible + dashed hidden lines, color roles, dimension callouts for hero params), `motion.json` (60 frames) when kinematics exists; per brick an assembled view including part reference models (gray).
5. **Emit:** `dist/catalog.json` (`library_version`, `catalog_hash`, `built_at`); `dist/api/v1/{bricks,parts,mechanisms}/index.json` and `/{id}.json`; `dist/api/v1/vocab/*.json`; `dist/api/v1/schema/*.json`; `dist/catalog.sqlite` (FTS5 over names, aliases, summaries, functions, tags); `dist/llms.txt`, `dist/llms-full.txt`; `dist/md/{bricks,parts,mechanisms}/{id}.md`; `dist/downloads/{id}/` (STL + STEP at defaults, source ZIP); `dist/assets/`; `dist/build-report.json` (timings, failures, coverage by category/function).
6. **Embed** `catalog.json` in `src/junkyard/data/`.

`--fast` skips range edges and renders. Cache by content hash per brick.

---

## 8. Query semantics

### 8.1 `search_bricks`
Inputs: `query` (free text) and/or `function` (ID), `actuator` (part ID or class), `category`, `max_envelope_mm`, `has_port` (type), `difficulty`, `stage_min`, `limit`.
1. Resolve vocabulary: ID → alias → FTS5; return `resolved` and `ambiguous` so the agent sees the interpretation.
2. Filters: exclude on explicit mismatch; a brick missing data for a filter is kept and flagged `unknown_for: [...]`.
3. Order (stated in every response): function match exactness → number of filters satisfied → `stage` → `difficulty` (simpler first) → id.
4. `gaps`: Atlas mechanisms that match but have no brick, with external references.

### 8.2 `find_compatible`
Given `(id, port)`, return bricks and parts exposing a port of a mating type whose `match_keys` agree (exact on enums/ints, ±0.1 mm on floats), with the port pair names. Discovery only.

### 8.3 Determinism
Same input + same `catalog_hash` → byte-identical JSON (sorted keys, fixed float formatting).

---

## 9. Agent surfaces

### 9.1 Response envelope
```json
{ "library_version": "0.1.0", "catalog_hash": "sha256:…", "tool": "search_bricks",
  "query": { "resolved": {}, "defaults_applied": {} }, "result": {}, "warnings": [],
  "disclaimer": "Generated geometry is not verified for printability, fit or strength. Check before printing." }
```
Errors: `{ "error": { "code": "unknown_brick|unknown_part|invalid_param|outside_range|missing_spec|generation_failed", "message": "...", "hint": "..." } }`.

### 9.2 MCP tools (`junkyard mcp`, stdio)
Descriptions written for an agent that has never seen Junkyard, ≤ ~600 chars, including when not to use the tool.

| Tool | Purpose | Inputs | Outputs |
|---|---|---|---|
| `search_bricks` | Function-first discovery | see 8.1 | results with reasons, `gaps`, `ordering` |
| `list_bricks` | Browse | `category?`, `tag?` | id, name, functions, actuation, stage |
| `get_brick` | Full record | `id` | params with units/ranges, ports, derived, print hints, BOM, assembly, README text, provenance, asset URLs |
| `generate_brick` | Make files | `id`, `params`, `formats` (`stl`,`step`,`glb`), `out_dir`, `force?` | file paths per part, resolved BOM, envelope |
| `add_brick` | Copy source into project | `id`, `dest` (default `./junkyard_bricks/`) | copied files, how to call it |
| `find_compatible` | What mates with this port | `id`, `port` | matching bricks/parts + port pairs |
| `get_part` / `list_parts` | Component specs | `id` / `class?` | specs with source + verification |
| `search_mechanisms` | Atlas lookup | `query`/`function` | mechanisms, alternatives, `realized_by` |
| `list_vocabulary` | Controlled terms | `kind` | IDs, labels, aliases |
| `export_assembly` | Write `assembly.json` for a set of bricks the agent combined | `items[]` (brick id + params), `connections[]` (port pairs) | file path (section 14) |

### 9.3 CLI
```text
junkyard search "pick up a grape" --actuator part.servo.sg90
junkyard list [--category gripper]
junkyard info gripper.fin_ray_finger
junkyard generate gripper.parallel_jaw_rack opening_mm=40 --format stl,step --out ./cad
junkyard add gripper.parallel_jaw_rack
junkyard compatible motor.servo_mount servo_horn
junkyard parts [--class hobby_servo_9g]
junkyard build [--fast]          # repo only
junkyard new-brick <category>.<slug>   # repo only
junkyard mcp
```
All support `--json`.

### 9.4 Python API
```python
import junkyard as jy
jy.search("pick up a grape", actuator="part.servo.sg90")
parts = jy.generate("gripper.parallel_jaw_rack", opening_mm=40)   # dict[str, build123d.Part]
jy.export(parts, "out/", formats=["stl", "step"])
jy.add("gripper.parallel_jaw_rack", dest="./junkyard_bricks")
```

### 9.5 Agent skill (`skill/SKILL.md` + plain `junkyard-agent-guide.md`)
When to use Junkyard; the loop search → get → (add or generate) → explain to the user (BOM, print hints, assembly steps, the disclaimer); combining bricks via ports and `find_compatible`; editing copied source; when nothing fits (say so, show `gaps`, don't silently improvise). Three worked transcripts.

### 9.6 `docs/agents.md`
Copy-paste MCP config for Claude Code, Claude Desktop, Cursor and generic clients (`uvx junkyard-robotics mcp`).

---

## 10. Website

### 10.1 Principles
1. **The picture is the part**: rendered from code at stated params, with caption.
2. **Agent parity**: every page links its `.md` and `.json` twin (`<link rel="alternate">`), and has a "Use with an agent" block.
3. **Fast and calm**: thumbnail first, viewer lazy-loaded; Lighthouse performance ≥ 90 (mobile) on gallery and brick pages.
4. Light and dark themes; `prefers-reduced-motion` respected; keyboard navigation.

### 10.2 Routes

| Route | Content |
|---|---|
| `/` | Promise in one line, MCP install snippet (tabs per client), animated hero bricks, category tiles with counts, "what's next" waitlist CTA, GitHub link |
| `/bricks` | Gallery grid; filters: category, function, actuator class, difficulty, tags; card = iso thumbnail (animates on hover if kinematics), name, functions, actuator chips |
| `/bricks/[id]` | See 10.4 |
| `/parts`, `/parts/[id]` | Spec table with source + verification badge per value; reference model; bricks that use it |
| `/atlas`, `/atlas/[id]` | Mechanisms grouped by function (IISc M2D2 style: heading, one-line definition, row of thumbnails), toggle by family F01–F18; page shows summary, alternatives, bricks realizing it or "No brick yet" |
| `/wanted` | Mechanisms with no brick: contribution roadmap |
| `/docs/*` | Quickstart, agents, Python API, CLI, schema (generated), authoring a brick, contributing |
| `/next` | Short page on the upcoming Junkyard product + waitlist form (copy is placeholder `TODO(owner)`) |
| agent endpoints | `/llms.txt`, `/llms-full.txt`, `/md/...`, `/api/v1/...`, `/catalog.json` |

### 10.3 Visual system
- **Modes:** 3D (orbit), **Plate** (orthographic front elevation, ink outlines via `EdgesGeometry`, flat role colors, hatched fixed frame, dimension callouts; inspired by the RoboticWorx atlas), **Exploded**, **Ports** (labeled gizmos), **Assembled** (with gray reference models of servos/bearings/screws).
- **Animation:** play/pause, speed ¼×–2×, labels and path toggles, synced **motion graph** (output vs input) when kinematics exists.
- **Color roles** as CSS tokens in both themes: input vermilion, output cobalt, moving gray, fixed light gray (hatched in plate), ports amber, reference parts neutral gray at 60% opacity.
- **Typography:** grotesk sans for text, monospace for values and IDs.
- **Parameter sliders** for hero params snap to the precomputed variants; the viewer, plate dimensions and derived values update. Other params shown in a table with a prefilled `junkyard generate …` command (copy button).

### 10.4 Brick page
1. Header: name, ID (copy), category, functions, stage, difficulty, license, MDI link.
2. Viewer (sticky on desktop) with modes, controls, legend, caption.
3. Parameters: hero sliders + full table (name, unit, default, range, description), derived values.
4. README sections (5.2).
5. Build it: BOM with part links, print hints, assembly steps.
6. Connects to: ports list with `find_compatible` results as cards.
7. Use it: tabs MCP / CLI / Python / Download (STL, STEP at defaults; source ZIP).
8. Provenance and disclaimer.

---

## 11. Catalog for v1

### Wave 1: reference bricks (built first, in this order, M2–M3)
`joint.pin_revolute` · `motor.servo_mount` · `gripper.parallel_jaw_rack` · `gripper.fin_ray_finger`

### Wave 2: the rest (M6), ~46 bricks

| Category | Bricks |
|---|---|
| Joints | `joint.bearing_revolute_608`, `joint.living_hinge`, `joint.cross_axis_flexure_pivot`, `joint.ball_socket`, `joint.universal`, `joint.dovetail_slide`, `joint.printed_slewing_ring` |
| Motor interfaces | `motor.servo_horn_adapter`, `motor.servo_u_bracket` (pan/tilt), `motor.nema17_mount`, `motor.nema17_l_bracket`, `motor.n20_mount`, `motor.28byj48_mount`, `motor.shaft_coupler_rigid`, `motor.shaft_coupler_oldham` |
| Grippers | `gripper.parallel_jaw_linkage`, `gripper.angular_jaw`, `gripper.tendon_finger_two_phalanx`, `gripper.three_finger_hub`, `gripper.soft_jaw_pad` |
| Gears and reducers | `gear.spur_pair`, `gear.planetary_single_stage`, `gear.cycloidal`, `gear.worm_drive`, `gear.bevel_pair`, `gear.capstan_drive` |
| Linear | `linear.belt_stage_gt2`, `linear.leadscrew_stage_t8`, `linear.rack_and_pinion`, `linear.rod_carriage_lm8uu`, `linear.scissor_lift` |
| Linkages | `linkage.four_bar`, `linkage.parallelogram_arm_segment`, `linkage.slider_crank`, `linkage.jansen_leg`, `linkage.pantograph` |
| Locks and indexing | `lock.ratchet_pawl`, `lock.over_center_latch`, `lock.detent`, `lock.geneva_drive`, `lock.cam_follower` |
| Transmission | `transmission.gt2_pulley`, `transmission.idler_pulley`, `transmission.belt_tensioner`, `transmission.tendon_guide`, `transmission.cable_chain_link` |
| Structure and wheels | `structure.mounting_plate_grid`, `structure.extrusion_2020_bracket`, `structure.standoff`, `wheel.hub_wheel` (servo/N20/TT), `wheel.ball_caster` |

Wave 2 order follows usefulness for a first robot: motor interfaces → structure/wheels → transmission → linear → gears → linkages → grippers → locks → joints.

### Parts (~40)
Servos: SG90, MG90S, MG996R, DS3218 (20 kg), one 35 kg class. Steppers: NEMA17 34/40/48 mm, NEMA14, 28BYJ-48. Gearmotors: N20 (common ratios share one body), TT yellow motor. Bearings: 608, 623, 625, 688, MR105, LM8UU. Motion: GT2 6 mm belt, GT2 20T pulley, GT2 idler, T8 leadscrew + nut, 8 mm rod, 2020 extrusion + T-nut. Fasteners: SHCS M2/M2.5/M3/M4/M5 (common lengths as one parametric record per size), hex nuts M2–M5, heat-set inserts M2/M3/M4, dowel pins 3/4 mm, 6 mm ball (caster). Standards cited where applicable (ISO 4762, ISO 4032, ISO 15 / bearing catalogs).

### Atlas
One record per brick mechanism plus ~15 without bricks (e.g. strain-wave drive, mecanum wheel, soft pneumatic gripper, suction gripper, Stewart platform, delta, Klann leg, whiffletree, sprag clutch, Hoberman linkage), all `draft` until reviewed.

---

## 12. CI (code quality only)

1. `ruff`, `pytest`.
2. YAML validates; JSON Schema regeneration produces no diff.
3. Every generator runs at defaults and at every range edge and returns valid, non-empty solids for every declared output. Failure blocks merge.
4. Geometry snapshot (volume, bbox per output at defaults) in `tests/snapshots/`; a change > 1% must update the snapshot in the same PR.
5. Provenance gate: every brick has `provenance`; `imported_files` licenses must be in the allow-list (CC0, MIT, Apache-2.0, BSD, CC BY); otherwise merge blocked.
6. README of each brick has all section headings (5.2).
7. Invariant tests (section 13).
8. Web build, link check, Lighthouse CI (warn until M5, then block below 90).

---

## 13. Invariants (tests in `tests/invariants/`)

| ID | Invariant |
|---|---|
| I1 | Every non-null part spec value has a `source`. |
| I2 | A generator never reads a null spec silently; it raises `MissingSpec`, surfaced as `missing_spec` error. |
| I3 | Every MCP response and JSON record includes `library_version` and `catalog_hash`; every brick response includes the disclaimer. |
| I4 | MCP `get_brick` equals `/api/v1/bricks/{id}.json` for shared fields. |
| I5 | Same query + same catalog → byte-identical output. |
| I6 | No rendered visual without a caption stating brick ID, version and params. |
| I7 | No `motion.json` for bricks without `kinematics.py`. |
| I8 | No text, image or CAD file copied from a source without an allow-listed license (provenance gate). |
| I9 | Words "tested", "proven", "validated", "verified" never describe bricks in generated pages or tool output (scan of `dist/`), since nothing is physically validated. |

---

## 14. Forward compatibility (hooks for the next product, no implementation of it)

The next product will consume structured descriptions of what agents build. Prepare the data, not the tool:
- `assembly.json` schema (`schemas/assembly.schema.json`): items (brick id, version, params, part refs), connections (port pairs + resolved transforms from port frames), BOM rollup, library version. Produced by `export_assembly` / `jy.export_assembly(...)`.
- Every generated file carries a sidecar `<file>.junkyard.json` (brick id, version, params, catalog hash).
- Stable IDs, ports with frames, and units everywhere.
- Do not add analysis or validation code; leave a stub `docs/next-product-hooks.md` describing these formats.

---

## 15. Milestones (in order; green CI at each)

**M1 Foundations.** Scaffold (section 4), `pyproject`, CI skeleton, Pydantic models for section 5 + assembly schema, JSON Schema export, vocab files (functions ≥ 60 with aliases, ports, actuator classes, categories, materials), loaders and ref resolution, `docs/decisions/` (D1–D14, O1–O3), `docs/human-tasks.md`, `CLAUDE.md` (conventions + invariants).
*Accept:* tests green; invalid fixtures fail with clear messages; schemas generated; I1, I2 tests pass on fixtures.

**M2 First brick end to end (`joint.pin_revolute`).** SDK (`@brick`, `@kinematics`, `Ctx`, `MissingSpec`, `sdk.features`), build pipeline steps 1–6, renders (GLB, PNG, SVG plate, motion), all emitted outputs, `junkyard new-brick` template derived from this brick.
*Accept:* `junkyard build` produces every output; thumbnail and plate images attached to the PR; I5, I6, I7 pass.

**M3 Parts and composition (`motor.servo_mount`, `gripper.parallel_jaw_rack`, `gripper.fin_ray_finger`).** First 8 parts (SG90, MG90S, MG996R, NEMA17 40 mm, 608, M3 SHCS, M3 insert, M3 nut) with sourced values or nulls + human tasks; reference models for parts; ports with frames; `find_compatible`; rack-and-pinion kinematics and motion graph; assembled view.
*Accept:* `find_compatible(gripper.parallel_jaw_rack, jaw_left_face)` returns `gripper.fin_ray_finger`; generating with a null servo spec returns `missing_spec` naming the field.

**M4 Agent surfaces.** Python API, CLI (all commands, `--json`), MCP server (all tools in 9.2), envelope, error codes, `export_assembly`, sidecars, agent skill + plain guide, `docs/agents.md`, golden-JSON MCP contract tests; I3, I4.
*Accept:* scripted MCP session: search "pick up a grape" with SG90 → get → find_compatible → add + generate → export_assembly; files land in a temp project; golden fixtures stable.

**M5 Website v1.** All routes in 10.2, viewer modes and controls, sliders, motion graph, parts, atlas, wanted, docs from schemas, `/next` waitlist (configurable endpoint), agent endpoints, both themes; I9.
*Accept:* Lighthouse ≥ 90 performance on two pages (mobile); screenshots at 375 px and 1440 px in both themes in the PR.

**M6 Catalog wave 2.** Remaining ~46 bricks and ~32 parts in the order of section 11, plus Atlas records; one PR per category. Each brick: manifest, generator, README with all sections, hero params, kinematics where simple, renders.
*Accept:* all bricks build at defaults and range edges; every category page populated; `build-report.json` shows 0 failures; `/wanted` lists the no-brick mechanisms.

**M7 Release.** PyPI publish workflow for `junkyard-robotics`, `uvx junkyard-robotics mcp` works on a clean Linux and macOS runner, README (agent-first quickstart with GIF of the viewer), CONTRIBUTING (how to add a brick, review checklist), issue templates (`new-brick`, `part-spec-correction`, `atlas-correction`, `bug`), site deploy workflow, MCP registry listing metadata (`server.json` or equivalent) prepared.
*Accept:* fresh install + search + generate succeed in CI on both OSes; site deploys from `main`.

---

## 16. Human tasks (`docs/human-tasks.md`)

- Confirm O1 domain, O2 waitlist endpoint, O3 analytics; write `/next` copy.
- Verify part datasheets and flip `verification` to `datasheet`.
- Review Atlas drafts; mark `reviewed`.
- Review renders and README tone per category PR.
- Submit to MCP registries, awesome-lists, maker communities at release.

---

## 17. Authoring a brick (`docs/authoring-a-brick.md`)

1. `junkyard new-brick <category>.<slug>`.
2. Link or create the Atlas record (`mdi.realizes`).
3. Params with units, ranges and descriptions; pick 1–2 hero params.
4. Ports from existing types (new types via a `vocab/ports.yaml` PR).
5. Generator: ≤ ~250 lines, named outputs, commented constants, `sdk.features` for common features, `ctx.spec()` for part dimensions.
6. Kinematics only for simple rigid motion.
7. README with all sections; original text only.
8. Provenance; imported files only with allow-listed licenses.
9. `junkyard build --brick <id>`, check renders, open a PR.

---

## 18. Glossary

**Brick:** parametric generator + metadata for one mechanism or mechanical part. **Part:** spec record for a purchased component. **Atlas record:** mechanism knowledge entry (MDI-lite) linked to bricks via `realized_by`. **Port:** named, typed connection point with a coordinate frame. **Range:** parameter values for which the generator produces valid geometry. **Stage:** software maturity of a brick's code and docs. **Gap / wanted:** a mechanism with no brick yet.
