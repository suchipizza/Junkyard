# Hooks for the next product

The next Junkyard product will read structured descriptions of what agents
build. This library prepares the data formats only; it contains no analysis or
validation code (PRD §14).

- **`assembly.json`** (`schemas/assembly.schema.json`): the bricks an agent
  combined (`items`: brick id, library version, params, resolved part refs),
  how they connect (`connections`: port pairs plus a 4×4 transform from the
  port frames), a BOM rollup, `library_version`, `catalog_hash` and the
  standard disclaimer. Written by `export_assembly` / `jy.export_assembly()` (M4).
- **Sidecars** (`schemas/sidecar.schema.json`): every generated STL/STEP/GLB file
  gets `<file>.junkyard.json` with brick id, library version, params, output
  name and catalog hash (M4).
- **Stable IDs, ports with frames, units in every field name.**
