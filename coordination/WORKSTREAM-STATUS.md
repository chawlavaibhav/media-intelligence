# Workstream Status

**Snapshot, updated at integration checkpoints.** Detail lives in each stream's `HANDOFF.md`.

| Stream | Status | Current approved task | Blocking item / next gate |
|---|---|---|---|
| Canon | Schemas locked (SPEC-01–05). Six historical probes re-audited; no fresh current-schema extraction yet. | `CANON-001` — first fresh SPEC-03/04/05 extraction from Molly Bang | Controller review of CANON-001 output before scaling ingestion |
| Eval | One checker-calibration study done. No battery, no Registry. | `EVAL-001` — design Capability Battery V0; no generation spend | Controller review of battery/instrument plan before any benchmarking |
| Resources | Research plan exists; no external dataset acquired yet. | `RES-001` — bounded corpus acquisition pilot | Stop on legal/access ambiguity or 20 GB hard cap |

## Cross-stream dependency chain

```
CANON-001 current-schema extraction ──► validate ingestion shape ──► later bounded curriculum ingestion

EVAL-001 battery design ──► Controller approval ──► Capability Lab runs ──► Capability Registry
                                   ▲
                                   │
RES-001 corpus acquisition ────────┘

Canon-consumption experiments are intentionally paused for now. No worker should run or extend
`canon/experiments/CANON-EXPERIMENT-V0.md` unless the Controller explicitly opens a new task for it.
```

Three approved starter tasks are now active in the operating model. Workers must use their own
worktrees/branches, produce Controller Briefs, and stop at the gates in `shared/AUTONOMY-POLICY.md`.
