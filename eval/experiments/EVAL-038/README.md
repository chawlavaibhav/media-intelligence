# EVAL-038 — weak model + compiled packs vs strong model alone, extended to media

**Authority:** DN-07 in `canon/candidates/canon-014/REP-07-DECISION-NOTES.md` —
Controller approval recorded verbatim BEFORE any paid call: USD 10.00 hard cap total,
0 retries, execution-time route/price verification before every paid call. Design:
`canon/findings/PROPOSED-EVAL-038-SUBSTITUTION-DESIGN.md` (2 reps per Controller
directive, not the design's 3). Media generation is product learning — NOT Capability
Registry evidence.

## Layout

- `payloads/` — the exact injected system/user bytes per brief plus
  `PAYLOAD-MANIFEST.yaml` (trigger-table selection, NR mapping, digests, §5.4 quota
  proof). Built by `tools/build_payloads.py`, deterministic.
- `common/price-snapshot-038.yaml` — dispatch-gating price pins (EVAL-037 pattern,
  but here a null price REFUSES dispatch). `common/gemma-price-pin/` and
  `common/media-route-pin/` hold the pinned official bytes and live model-id
  verifications.
- `runs/spend-ledger.jsonl` — the append-only ledger every EVAL-038 paid call
  (reasoning AND media) reserves/settles against. Committed bytes.
- `runs/haiku-packs/` — weak+packs lane (Haiku, unconditional injection,
  6 briefs x 2 reps). `raw-run1-ceiling16000/` preserves the two run-1 trials that
  deterministically truncated at EVAL-037's 16k ceiling before the substrate
  correction to 32k (failure-path evidence per design §6).
- `runs/gemma-packs/` — Gemma weak+packs lane at the pinned USD 0.00 official price.
- `baseline/sonnet-no-canon/` — the 18 committed EVAL-037 Sonnet NO_CANON packages,
  reused at USD 0 (freeze commit in `FREEZE-COMMIT.txt`). Never re-run.
- `media/` — sealed generated media (EVAL-024 pattern: committed bytes + per-artifact
  record with sha256, request digest, provider evidence, consumed USD).
- `judging/` — stripped + blinded judging artifacts and the blinding commitment.
- `JUDGING-PROTOCOL.md` — what the Controller judges and how.
- `tools/` — `build_payloads.py`, `runner38.py`, `strip_blind.py`,
  `select_package.py`, `generate_media.py`.

## USD-0 pre-checks (design §5) — all executed before spend

| Check | Result |
|---|---|
| 5.1 PILOT-001 retro-test | `canon/findings/EVAL-038-RETRO-TEST-PILOT-001.md` — doctrine forbids the root-cause choice; partial silence on premium register recorded |
| 5.2 coverage-map freshness | LIVE24 map carries all 5 Indian sources (83 hits) |
| 5.3 pack validation | `validate_compiled_pack.py` all green |
| 5.4 payload dry-run | worst payload ~6.3k tokens vs 16k Gemma quota, all fit |
| 5.5 judging dry-run | strip pipeline leak-clean on two committed EVAL-037 packages (and caught the `##`-header variant before it could bite) |

## Spend conventions

Reservation before every send at worst case (estimated input + output ceiling at the
pinned price, or media unit price with margin); settlement at provider-reported usage;
anything after a send began settles conservatively at the reservation
(`settle_ambiguous`) and is never released or retried. `ledger_totals()` counts
settlements; a dispatch that would push committed + reservation past USD 10.00 is
refused and the run stops.
