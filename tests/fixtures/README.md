# Test fixtures

Everything here is **fictional** and exists only to exercise the schemas and
loaders. No fixture describes a real component, and no fixture value may be
copied into `parts/`.

- `catalog/`: a small valid catalog (2 bricks, 2 parts, 3 Atlas records) loaded
  with the real `vocab/`. The fixture servo's single non-null value (`mass_g`)
  cites this README as its "source" so that invariant I1 and `ctx.spec()` can be
  tested without inventing a real dimension.
- `invalid/<kind>/*.yaml`: one broken record per file. The first line of each
  file is `# expect: <text>`; the test asserts that loading fails with an error
  containing that text.
- `generators/`: tiny Python files used to test the I2 static check (generators
  must read specs through `ctx.spec()`, never through `.specs`).
