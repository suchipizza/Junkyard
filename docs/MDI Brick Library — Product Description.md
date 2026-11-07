# MDI Brick Library — Product Description

Nov 7, 2026 · @Noémie Rakotomalala

## Summary

The Brick Library is an open library of adjustable, 3D-printable mechanical parts that AI agents pick and size instead of drawing geometry from scratch. It is the buildable layer of Mechanical Design Intelligence (MDI): MDI tells an agent *which* mechanism fits a need; a brick lets the agent *produce* that mechanism as a printable file.

**Promise:** an agent calls `gripper(type="fin_ray", servo="SG90", opening_mm=40)` and gets geometry that someone has already printed, assembled and tested, sized to that motor, with the checks it passed and the limits it was not tested beyond.

**Analogy:** shadcn/ui for web interfaces. You do not install a black box; the agent copies the brick's source into the user's project, where it can be read and modified. Each brick stays small, readable and self-contained.

**Current phase:** library and database only, consumed by agents through a package and MCP tools. No end-to-end pipeline (vague goal → requirements → selection → assembly → printed robot) is built in this phase.

## How it fits inside MDI

MDI is the map of mechanisms; the Brick Library is the set of roads already built. Every brick realizes an MDI mechanism record, but many MDI records will never become bricks, and that is by design.

&#91;embedded content: how bricks fit inside MDI · 4 kinds of realization\]

The agent uses MDI to answer "which mechanism fits this need, and why", then the library to answer "give me one I can print". When a selection lands on a record with no brick, the agent says so honestly instead of improvising geometry.

What this changes in the existing MDI plan:

- MDI records gain a `realized_by` field: brick IDs, component IDs, recipe IDs, external reference designs, or none.
- MDI's evidence tiers (E0 to E4) apply to bricks through test records (see Quality).
- MDI's taxonomy stays broad (18 families); the library starts narrow (desktop, FDM, hobby actuators).
- Records whose selections often end in "no brick" form the library's build queue.

**This phase builds the library and its database for agents only.** The agent does the orchestration; no goal-to-robot pipeline is built here.

## Problem

Agents can write code that draws 3D parts (CadQuery, OpenSCAD), but parts generated from scratch usually fail physically, even when the mechanism choice was right. Typical failures:

- **Sizing:** a flexure too thin that cracks, a servo too weak for the load at full reach.
- **Printability:** unsupported overhangs, walls under the nozzle minimum, no clearance on moving fits.
- **Fit:** shaft, spline or mounting holes that do not match the real motor or bearing.
- **Assembly:** parts that collide, or cannot physically be put together.

These failures are invisible until something is printed, which costs hours and material per iteration. Software vibecoding works because its feedback loop is seconds long; hardware has no equivalent.

**Why bricks fix it:** agents are reliable at choosing a known block and filling in numbers, and unreliable at inventing precise geometry. A brick moves the hard knowledge (dimensions, clearances, printing rules, motor interfaces, validity limits) out of the agent's guesswork and into tested code with explicit checks. The agent's job shrinks to selection, parameters and composition.

## Users and jobs to be done

The primary user is an AI coding agent (Claude Code, Cursor, any MCP client) building hobby and maker robots on behalf of a person. Humans are secondary users who review, tweak and print.

| User | Job to be done | What they get |
| --- | --- | --- |
| Coding agent (primary) | Turn a chosen mechanism into a part that prints and fits | Typed generator, parameter ranges, interfaces, checks it can run |
| Maker or hobbyist | Get a working gripper, joint or gearbox without CAD expertise | Printable files that worked for someone else, sized to their motor |
| Robotics developer or student | Prototype fast with known-good subassemblies | Editable source code, test records, assembly notes |
| Agent and CAD tool builders | Add reliable mechanical parts to their product | Open package and MCP tools, no platform lock-in |
| Contributors | Share a proven design in a reusable form | A brick template, a review process, credit on every use |

Out of scope as users for now: production engineering teams, safety-critical and medical devices, metal machining shops.

## Anatomy of a brick

A brick is one folder: a small parametric generator plus the knowledge that makes it safe to use. Every part below is required unless marked optional.

| Part | What it contains | Why it matters |
| --- | --- | --- |
| Generator | A CadQuery Python function returning solids, exportable to STL and STEP | The buildable core; readable and editable like shadcn source |
| Parameters | Typed inputs with units, defaults, and a **tested range** per parameter | The agent knows what it may change, and how far |
| Interfaces | Named connection points: motor mount (component ID), shaft, bolt pattern, mating face, with position and orientation | Bricks and components snap together; fit errors become checkable |
| Checks | Executable rules: min wall vs nozzle, overhang angle, clearance, stress estimate, torque budget vs chosen component | Fails fast in software instead of after a print |
| Print profile | Material, layer height, orientation, infill, supports, tolerance offsets that were tested | Same file prints differently on different settings |
| Assembly notes | Bill of materials (screws, bearings, motor), steps, gotchas | A part is useless if it cannot be assembled |
| MDI link | The mechanism record ID it realizes, plus its family and functions | Selection in MDI ends in a buildable brick |
| Provenance and license | Original source, author, license, what was reimplemented vs imported | Rights stay clean; credit flows to contributors |
| Test record | Who printed it, printer, material, what was measured, photos, date | Turns "proven" from a claim into evidence |
| Kinematic model (optional) | URDF/MJCF fragment, joint limits | Later use in simulation; not required in v1 |

**Unknown stays unknown.** A parameter outside its tested range is allowed but flagged `untested`, never silently accepted. Checks report `pass`, `fail` or `not_evaluated`, never a guess.

## Example agent interaction

A user asks their coding agent: "Make a soft gripper for my desk arm that can pick up a grape, driven by an SG90." The agent (not the library) handles the conversation; the library answers its calls.

1. `search_bricks(function="grip_fragile_irregular", actuator="hobby_servo")` returns Fin Ray finger and compliant parallel jaw, each with its MDI mechanism ID and tested ranges.
2. `get_brick("gripper.fin_ray")` returns parameters, interfaces, print profile and test record.
3. `check_brick("gripper.fin_ray", {servo: "SG90", opening_mm: 40, material: "TPU95A"})` returns: wall thickness pass; servo torque at 40 mm opening pass with margin stated; grip force on a grape `not_evaluated` (no test data).
4. `generate_brick(...)` writes the source file into the user's project and exports STL.

The agent tells the user what passed, what was never tested, and what to print first. Composing several bricks into a full robot is the agent's job in this phase; the library supplies interfaces so that composition can be checked.

Call names are illustrative; the final tool list is in Agent interfaces.

## V1 scope

V1 covers desktop-scale, FDM-printable mechanisms driven by hobby servos and small steppers: about 20 bricks and 20 components.

**In scope:** PLA, PETG and TPU on common FDM printers; hobby servos, NEMA 17 steppers, small DC gear motors; standard screws, bearings and belts.

**Out of scope for v1:** resin and metal processes, MEMS, molded soft robotics, high loads, anything safety-critical or medical. These stay in MDI as knowledge-only entries.

### Initial bricks

| Category | Bricks | MDI family |
| --- | --- | --- |
| Joints | Printed pin revolute, bearing revolute (608), living hinge, cross-axis flexure pivot | F03, F01 |
| Motor interfaces | Servo horn adapter, servo mount, NEMA 17 mount, shaft coupler | F03 |
| Grippers | Parallel jaw (rack or linkage), Fin Ray finger, underactuated two-phalanx tendon finger | F12, F08 |
| Reducers | Printed planetary (single stage), printed cycloidal | F04 |
| Linear motion | Belt stage (GT2), lead-screw stage (T8), rack and pinion | F05, F06 |
| Linkages | Four-bar with configurable link lengths, parallelogram arm segment | F02 |
| Locking | Ratchet and pawl, over-center latch | F10 |
| Routing | Cable and tendon guide, pulley | F05 |

### Minimum component catalog

Bricks need real parts to size against. V1 ships spec records (dimensions, mounting pattern, shaft or spline, torque, speed, voltage, mass, datasheet link) for about 20 of the most common maker parts: SG90, MG90S, MG996R and one 35 kg servo; NEMA 17 variants; N20 gear motors; 608, 623 and 625 bearings; GT2 belt and pulleys; T8 lead screw and nut; M2 to M5 screws and inserts. Spec values come from datasheets and are labeled with their source; measured values are added when tested.

## Agent interfaces

One source of truth (bricks and components as files in Git) exposed three ways. No hosted database or search engine in v1: the whole catalog fits in an agent's context.

- **Python package** (`pip install`): import a brick and call its generator; a CLI copies brick source into a project (`add gripper.fin_ray`), shadcn-style.
- **MCP server**, platform-neutral, with these tools:
  - `list_bricks(filters)`: catalog with functions, MDI IDs, maturity.
  - `search_bricks(function, actuator, constraints)`: candidates with reasons, never ranked on hidden scores.
  - `get_brick(id)`: parameters, ranges, interfaces, print profile, test record, license.
  - `check_brick(id, params)`: runs all checks; returns pass, fail or not\_evaluated per check.
  - `generate_brick(id, params, format)`: STL or STEP plus the source file.
  - `check_interface(brick_a, port_a, brick_b, port_b)`: do two parts mate?
  - `get_component(id)` and `list_components(filters)`.
- **Agent skill** (Claude skill and plain-markdown equivalent): how to use bricks well, including when not to (no brick fits, so say so).

Every response carries the library version, so results are reproducible.

## Sourcing and licensing

Default: **reimplement, don't import.** Most bricks are written fresh as parametric code from engineering principles and public design knowledge. Ideas and dimensions-as-facts are not copyrighted; specific CAD files, drawings and photos are. Importing a file is the exception and needs a license that matches ours.

| Source license | What we can do |
| --- | --- |
| CC0, MIT, Apache-2.0, BSD, CC BY | Import or adapt with attribution |
| CC BY-SA, CERN-OHL-S, GPL | Only if the library adopts a compatible copyleft license; otherwise reference and reimplement |
| Any NonCommercial (NC) license | Never import; link as a reference design and learn from it |
| No license or "all rights reserved" | Link only |

Patents are a separate check: a reimplemented design can still be under patent. Flag commercial-use risk per brick when known.

**Library license (proposed, to decide):** Apache-2.0 or MIT for code, CC BY 4.0 for records and docs. Permissive keeps adoption easy for agent and CAD vendors, which matters more here than copyleft protection.

### Case study: Unitree Qmini

[Qmini](https://github.com/unitreerobotics/Qmini) is an open, fully 3D-printable bipedal robot from Unitree. The repo has STEP files for every mechanical part, a URDF model, a DIY PDF with bill of materials, and links a control stack. It uses 11 Unitree 8010 motors: 10 for locomotion, 1 spare at the neck.

**Verdict: useful as a reference, not as an import source.**

- **License blocks import.** The repo's [LICENSE](https://github.com/unitreerobotics/Qmini/blob/main/LICENSE) is CC BY-NC-SA 4.0: non-commercial only, and derivatives must keep the same license. Bricks derived from its STEP files would inherit NC, which conflicts with a permissive library and any future commercial use.
- **Wrong format.** STEP files are fixed geometry, not adjustable code. Converting one to a brick is a rewrite anyway.
- **Wrong scale for v1.** It is built around Unitree's own 8010 actuators, not hobby servos.

How to use it anyway:

- Link it in MDI as an external reference realization of a printed bipedal leg (families F14, F11).
- Study its design patterns (actuator housings, leg joint layout, cable routing) and reimplement the ideas from scratch with our own geometry.
- Add the Unitree 8010 motor as a component record if bipeds enter scope.
- Use it as a benchmark: "could an agent with our library produce a leg like this?"
- Ask Unitree for a permissive license on selected parts, if a specific part becomes worth importing.

The same audit applies to every candidate source: check the license file, not the README's "fully open source" claim.

## Quality and verification levels

A brick is only as good as its evidence, so each one carries a maturity level. Levels describe what was done, not a quality score, and map onto MDI's evidence tiers.

| Level | Meaning | Required to reach it | MDI tier |
| --- | --- | --- | --- |
| B0 Draft | Generator runs, schema valid | CI passes; geometry is watertight | E0 |
| B1 Checked | Static checks implemented | Printability, clearance and torque checks pass at defaults | E0–E1 |
| B2 Printed | Printed and assembled once at defaults | Test record with printer, material, settings, photos | E3 (narrow) |
| B3 Proven | Printed by 2+ independent people, across part of the parameter range | Multiple test records; tested range widened accordingly | E3–E4 |

Rules:

- Only B2 and above may be called "proven" in docs or tool output.
- The tested range comes from test records; it never grows by assumption.
- CI runs every generator at its defaults and range edges on every change; a check that regresses blocks the merge.
- Contributions need a test record to reach B2; reviewers check the record, not just the code.

## Success metrics

**North star:** on a fixed benchmark of build tasks, the share of agent-produced parts that print, assemble and move as specified on the first try, with the library versus without it. Same agent, same tasks, same printer.

Supporting metrics:

- **Benchmark uplift:** first-try success with vs without the library, broken down by failure type (sizing, printability, fit, assembly).
- **Honesty:** zero cases where the library reports `pass` on a check that failed in a physical test.
- **Coverage:** share of benchmark tasks where at least one brick fits; tasks with no fitting brick are logged as the build queue.
- **Maturity:** number of bricks at B2 and B3, not total brick count.
- **Adoption:** package installs, MCP connections, GitHub stars and forks, external projects using bricks.
- **Contribution:** bricks and test records submitted by people outside the core team.

Targets are set after the baseline study, not before.

## Plan to reach v1

The plan starts by measuring how agents fail without the library, and only scales bricks that measurably improve first-try builds. Milestones are ordered by dependency, not dated.

&#91;embedded content: plan to v1 · 6 milestones, 2 gates\]

Gate A decides whether to build at all; Gate B decides whether to grow the catalog. Brick choice in M2 and M4 follows the M0 failure histogram, not a wish list.

### First actions

- [ ] Write the 20 benchmark tasks, half phrased vaguely ("a gripper that can pick up a grape"), half specific.
- [ ] Run them with a coding agent and CadQuery, no library; print every result on one printer and log failures by type.
- [ ] Draft the brick folder format using the Fin Ray finger as the worked example.
- [ ] Write component records for SG90, MG996R and NEMA 17 from datasheets.
- [ ] Decide the library license before the first public commit.

## Risks, open questions, non-goals

| Risk | Mitigation |
| --- | --- |
| Baseline shows agents already succeed without bricks | Run the baseline first (M0); narrow to the failure types where uplift is real, or stop |
| Printer variance makes "proven" unreliable | Tolerance offsets as parameters; test records state printer and settings; B3 needs independent printers |
| Too few bricks to be useful | Pick bricks from benchmark failures, not from a wish list; compose recipes from few bricks |
| Agents don't call the tools | Test with real agents early; tune tool names and descriptions; ship the skill |
| Easy to copy (code only) | Moat is test records, component specs, interface checks and the MDI link, not the code |
| License contamination from imported files | Reimplement by default; license gate in CI; per-brick provenance |
| Users build unsafe things | V1 limited to low-load desktop parts; no medical or safety-critical claims; force limits in checks |

**Open questions**

- Library license: Apache-2.0 vs MIT for code; CC BY vs CC0 for records.
- Name and repo: inside the MDI repo, or a separate repo that depends on MDI IDs?
- Who prints for B2 in the early phase: own printer only, or paid testers?
- Does `check_brick` need simulation (MuJoCo) in v1, or are analytical checks enough?
- Which agent-side composition helpers belong in the library without becoming a pipeline?

**Non-goals for this phase**

- No end-to-end pipeline from user goal to finished robot.
- No electronics, wiring or firmware generation.
- No hosted platform, accounts or paid tier.
- No general text-to-CAD; geometry only comes from bricks.
- No guarantee of safety or fitness for any purpose.
