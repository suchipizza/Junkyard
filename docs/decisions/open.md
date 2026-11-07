# Open decisions

Each entry states the default in use until the owner decides. Entries that
conflict with an invariant (PRD §13) are marked `DECISION NEEDED:`. None of
the M1 entries conflict with an invariant.

## From the PRD (§2)

| ID | Question | Default in use |
|---|---|---|
| O1 | Domain | `junkyard.dev` placeholder in config (no config yet; arrives with the site in M5). |
| O2 | Waitlist provider | A plain form posting to a configurable endpoint; no vendor hard-coded (M5). |
| O3 | Analytics provider | None wired; config slot only (M5). |

## Added during M1 (2026-11-07)

These are places where the PRD was silent, ambiguous, or its examples
disagreed with its rules. Each records the choice made and where it lives.

| ID | Question | Default in use | Where |
|---|---|---|---|
| M1-01 | PRD §5 says every record has `updated_at`, but the §5.1 brick and §5.4 part examples omit it. | Required on every record (the general rule wins). The test that validates the PRD's brick example adds it. | `models/common.py` `VersionedRecord`; `tests/test_schemas.py` |
| M1-02 | §5.1 says numeric params need `unit` and `range`, but its `pinion_teeth` int param has no unit. | `float` params need a unit; `int` params (counts) need a range, unit optional. | `models/brick.py` `Param` |
| M1-03 | In §5.3, `servo_body_mount` has `match_keys: [servo_class]`, but `servo_class` is not in its params. | Added `servo_class: actuator_class` to its params; every match key must be a declared param. | `vocab/ports.yaml`; `models/vocab.py` |
| M1-04 | What is a part's `class` for non-actuators (screws, bearings, belts)? | `class` must be an actuator class from `vocab/actuator_classes.yaml`, or null. So `list_parts --class` only filters actuators. Alternative: add a `part_classes` vocabulary in M3. | `models/part.py`; `registry.py` |
| M1-05 | §5.4 lists source kinds `datasheet, reference_drawing, standard, web`. Atlas records cite papers and books. | Added `literature` as a fifth kind. | `models/common.py` `SourceKind` |
| M1-06 | D9 lists mm/deg/N·m/N/g, but the PRD also uses `at_voltage_v` and `infill_percent`. | Units: mm, deg, N·m, N, g, V, s, rpm, percent. Required name suffixes: `_mm _deg _nm _n _g _v _s _rpm _percent`. | `models/common.py` `Unit`, `UNIT_SUFFIX` |
| M1-07 | Can two functions share an alias? (§8.1 returns `ambiguous` interpretations.) | No: every alias resolves to exactly one function, so alias lookup is never ambiguous. Ambiguity in search comes from full-text matches only. | `vocab.py` |
| M1-08 | How strictly must brick ↔ Atlas links agree? | Both ways: a brick's `mdi.realizes` mechanism must list the brick in `realized_by`, and vice versa. A brick's `mdi.families` must be a subset of its mechanism's families. | `registry.py` |
| M1-09 | Port gender and matching rules beyond the §5.3 examples. | Genders: male, female, neutral. `gender_rule`: opposite (default), same, any (`bolt_pattern` uses any). Empty `mates_with` means same type only. | `models/vocab.py`, `vocab/ports.yaml` |
| M1-10 | Allowed values of `print_hints.supports` (PRD example shows only `none`). | `none`, `minimal`, `required`. | `models/brick.py` `Supports` |
| M1-11 | How many hero params? | 1 or 2, numeric only (5 steps each, at most 25 variants per §7.2). | `models/brick.py` `Visuals` |
| M1-12 | Exact import-license allow-list (§12.5 says CC0, MIT, Apache-2.0, BSD, CC BY). | SPDX ids: CC0-1.0, MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, CC-BY-3.0, CC-BY-4.0. Please confirm whether older CC BY versions should count. | `models/brick.py` `IMPORT_LICENSE_ALLOWLIST` |
| M1-13 | "Unknown is null, never 0/false/empty." Should a spec value of 0 ever be allowed? | Rejected: spec values of `0`, `false` or `""` fail with "use null for unknown values". Empty strings are rejected in every text field. | `models/part.py`, `models/common.py` |
| M1-14 | I2 must pass in M1, but the SDK is M2. | M1 ships the minimal pieces I2 needs: `Ctx.part()`, `Ctx.spec()`, `MissingSpec`, `UnknownPart`, and a static check that generators never read `.specs` directly. `@brick`, `@kinematics`, features stay in M2. | `src/junkyard/sdk/`, `src/junkyard/errors.py` |
| M1-15 | Atlas `input_motion` / `output_motion` values. | Free snake_case terms for now; no vocabulary. Worth a small `motions.yaml` before the Atlas grows in M6. | `models/mechanism.py` |
| M1-16 | Transform format in `assembly.json`. | 4×4 homogeneous matrix, row-major, mm, giving side `b`'s pose relative to side `a`. | `models/assembly.py` |
| M1-17 | Heads-up for I9 (M5): the scan of `dist/` for "verified"/"validated" must not trip on part spec badges (`verification: datasheet`, "unverified") or on the D13 disclaimer ("not verified"). | No change now. When I9 is implemented, scope it to words that describe bricks, and allow these. | — |
| M1-18 | The GitHub repo was empty, so a PR had no base branch. | Created `main` with only the four spec documents, then branched `m1-foundations` from it. | git history |
