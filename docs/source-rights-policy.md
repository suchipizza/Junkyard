# Source rights policy

Default: **reimplement, don't import.** Bricks are written fresh as parametric
code. Ideas and dimensions-as-facts can be used; specific CAD files, drawings,
photos and text belong to their authors.

| Source license | What we can do |
|---|---|
| CC0, MIT, Apache-2.0, BSD, CC BY | Import or adapt, with attribution recorded in `provenance.imported_files` |
| CC BY-SA, CERN-OHL-S, GPL | Reference only, and reimplement |
| Any NonCommercial (NC) license | Never import; link as a reference design |
| No license, or "all rights reserved" | Link only |

- Check the license file itself, not a README's "open source" claim.
- A downloadable file is not automatically licensed for reuse.
- Patents are a separate question from copyright; flag known risks per brick.
- The loader rejects any `imported_files` entry whose license is not on the
  allow-list (invariant I8). The exact SPDX list is in
  `src/junkyard/models/brick.py` (`IMPORT_LICENSE_ALLOWLIST`).
