# Authoring a brick

Placeholder. The full guide is written in M2, from the first brick
(`joint.pin_revolute`) and the `junkyard new-brick` template. The steps it will
cover are in PRD §17.

Rules that already apply (enforced by the loader):

- The folder is `bricks/<category>/<slug>/` and the id is `<category>.<slug>`.
- Float params need a unit and a range, and the name ends with the unit suffix
  (`opening_mm`). Int params need a range.
- `README.md` has every section in PRD §5.2.
- `mdi.realizes` names an Atlas record that lists this brick in `realized_by`.
- Ports use types from `vocab/ports.yaml`; functions come from `vocab/functions.yaml`.
- Part dimensions come from `ctx.spec(part, field)` only.
