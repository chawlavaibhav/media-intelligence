# Workstream Status

**Snapshot, updated at integration checkpoints.** Detail lives in each stream's `HANDOFF.md`.

| Stream | Status | Blocking item | Next milestone (proposed, not approved) |
|---|---|---|---|
| Canon | Schemas locked (SPEC-01–05). Curriculum + Coverage Map designed, awaiting approval. | Controller sign-off on `canon/experiments/CANON-CURRICULUM-V0.md` | Ingest V0 curriculum → run Experiment A |
| Eval | One calibration study done (Devanagari checker). No battery, no Registry. | Battery design not started | EVAL-001: Devanagari benchmark research |
| Resources | Research plan only, nothing downloaded. | Every dataset licence unverified | RES-001: verify Pitt Ads + Devanagari gap |

## Cross-stream dependency chain

```
Canon curriculum approval ──► Experiment A (planning) ──► Experiment B (evaluation)
                                                                  ▲
Resources: corpus sourcing ──────────────────────────────────────┘

Eval: battery design ──► Capability Registry ──► hypothesis 15 (routing), blocked on both
                                                   Canon (requirements) and Eval (Registry)
```

Nothing is currently running. All three streams are at the same gate: Controller review of this
setup and of the Canon Curriculum/Coverage Map.
