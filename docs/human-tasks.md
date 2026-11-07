# Human tasks

Things only a person can do: confirm decisions, check datasheets, review
content. Agents add a line here whenever they leave a value `null` or need a
decision (PRD §0 rule 3, §16).

## Decisions

- [ ] Confirm O1 domain, O2 waitlist endpoint, O3 analytics (`docs/decisions/open.md`).
- [ ] Write the `/next` page copy (placeholder `TODO(owner)` until then; M5).
- [ ] Review the M1 defaults in `docs/decisions/open.md` (M1-01 … M1-18), especially
      M1-04 (part classes for non-actuators) and M1-12 (import-license allow-list).
- [ ] Confirm `bd_warehouse`'s license is Apache-2.0-compatible before M2 uses it (D1).
      If not, gears, threads and fasteners get reimplemented.
- [ ] Check that `junkyard-robotics` is still free on PyPI and reserve it before M7.

## Part specs

- [ ] Verify part datasheets and flip `verification` to `datasheet` (from M3).
  No real part records exist yet, so no spec values are pending. Every null
  spec added later gets a line here naming the part, the field and what source
  would settle it.

## Reviews

- [ ] Review `vocab/functions.yaml` (84 functions): wording of definitions, missing
      jobs, and whether the aliases match how people and agents phrase requests.
- [ ] Review Atlas drafts and mark them `reviewed` (from M3/M6).
- [ ] Review renders and README tone in each category PR (from M2).

## Release

- [ ] Submit to MCP registries, awesome-lists and maker communities (M7).
