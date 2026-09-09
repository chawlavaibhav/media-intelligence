# Controller — format_probe Resolution-Class Criterion Amended — 2026-09-09

**Status:** APPROVED CONTROLLER DECISION.
**Role:** Writer Controller, recording the human Controller's words.
**Amends:** `CONTROLLER-INSTRUMENT-THRESHOLDS-FROZEN-2026-09-09.md` (one criterion only).

## Authority — the Controller's words

Put to the Controller: *"The format check's 'resolution class' rule expects the long side of a 1024-class picture to
be 960 to 1100 pixels. Providers actually return 928 by 1152 for 4:5, 720 by 1280 for 9:16, 1080 by 1920 for some
routes. So every non-square picture fails that rule while passing aspect ratio. … My proposed amendment: judge the
resolution class by total pixels within 20 percent of the requested class, not by the long side."*

> **"amend as proposed"**

## Decision

`format_probe.resolution_class_ok` is amended, criteria file version **v0 → v1**:

- `NNNp` classes (720p, 1080p, …): unchanged — the short side equals NNN.
- `1024-class` (and any `<N>-class`): **total pixels within ±20 % of N²** (for 1024-class: 838,861 to
  1,258,291 pixels), regardless of aspect. 928×1152 (1,069,056), 1024×1024 and 1080×1080 pass; 720×1280 (921,600)
  passes; 1080×1920 (2,073,600) fails as a genuine class mismatch (that is a 1440-class delivery); 512×512 fails.
- Aspect stays a separate check at ±1 %.

Consequences:

1. The criteria file sha changes; every Registry row carries the criteria sha, so the 167 rows written under v0
   are **superseded and re-written** from the same sealed records under v1 (the harness re-evaluates; nothing is
   hand-edited; the v0 rows remain in git history). Rows for the other five capabilities are unchanged in
   substance but carry the new sha.
2. The decision is recorded on the criterion (`frozen_ref`, `amended_ref`) and the instrument's config hash changes.
3. No other threshold moves.

Not decided here: anything about human acceptance, Canon, or spend.
