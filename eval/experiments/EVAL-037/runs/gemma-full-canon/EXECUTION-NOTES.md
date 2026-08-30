# EVAL-037 — lane `gemma-full-canon` execution notes

Factual worker record. No creative judging, no media generation, no merge.

## Dispatch

| Gate | Result |
|---|---|
| `freeze_fingerprint` | intact — `5fc021d96d23299e977600735cc8cf0f950f61d6ed7cd8b39099f9a10aa189ee` |
| `common_substrate_digest` | intact — `d8b2c045c61e22668bf6bb8b6b387250efce8c80b1e909029e21d3d6a6c0ebc2` |
| canon `full_knowledge` | `cbd321aa3be7464e785a0d42de1764cdccc8bdd33bc023a376740f8f196bde60` |
| canon `qa` | `1313c0babe2194a7bc71c1628f9fbec5fa4f35ca5ff5edc7f594662101dc62bd` |
| trial order | recomputed from `sha256("EVAL-037|"+trial_id)`, matches the frozen plan |
| model preflight | `gemma-4-31b-it` resolves as an exact id on the Google Gemini API (models.list; no generation call) |
| runner frozen | commit `ba4e44b`, before trial 1 |

## Starting commit

The lane was dispatched from `396de89` (tip of `work/eval-037-freeze`), the commit whose
bytes verify clean against both recorded digests.

`main` (`002beec`) was not usable as the starting point: it contains no
`eval/experiments/` tree at all, and `canon_base_commit c6f8d91` is not an ancestor of
it — `main` is an ancestor *of* `c6f8d91`. The lane's own rule is "any checkout that
contains the approved frozen substrate and has `canon_base_commit` as an ancestor";
`396de89` satisfies both and has `main` as an ancestor.

A pre-existing checkout at `media-intelligence-worktrees/eval-037` carried uncommitted
post-freeze edits to `runner.py`, `providers.py` and `fake_provider.py`
(computed `965c469a…` vs recorded `5fc021d9…`). Those were excluded: this lane ran from
a clean worktree at `396de89`. They are untouched, not reverted.

## Credential

The lane names `GEMINI_API_KEY`. `~/.mi-keys` provides the Gemini credential as
`GOOGLE_API_KEY`; it was exported into `GEMINI_API_KEY` for the run. No substrate change.

## Outcome

18/18 trials executed in the frozen order. 15 `complete`, 3 `format_repaired`
(B01-R1, B05-R2, B03-R2 — one format-only repair each, within the max of 1).
0 technical failures, 0 execution failures, 0 retries. All 18 remain
`eligible_for_media_generation`. Validator: 32/32 gates green.

- Canon tool calls: **0** across all 18 trials.
- `website_read` calls: **5**, all on B01/B02, all served from the sealed snapshots.

Canon exposure was verified from the retained request payloads: `canon_catalog`,
`canon_search`, `canon_read` (plus `website_read` on B01/B02) were present in
`config.tools`, and the FULL_CANON addendum was present in `config.system_instruction`.
Config carried only `max_output_tokens: 8192` — no sampling or reasoning controls.
Zero Canon use is therefore the tested model's own choice under model discretion, not a
harness fault. It is recorded, not judged.

## Recorded anomaly — token usage not captured (NOT corrected)

`lane_usage_totals` reports every token field as `null` with
`*_turns_reporting: 0` of 26 provider turns.

The provider did report usage. `turn_record()` in `tools/providers.py` reads
`_get(raw, "usage")`; the `google-genai` response object names the field
**`usage_metadata`**, which is not in that lookup list. The Anthropic and OpenAI
branches both read `usage` and are unaffected. The result is that no token count
reached the ledger for this lane.

Per obligation 9 ("make no runner, prompt or config change after the first call") the
runner was **not** modified and the lane was **not** rerun. The ledger's `null` +
`turns_reporting: 0` is honest — it reports a missing total rather than a partial one
passed off as complete.

The data is not lost. Every attempt's raw response retains the provider's verbatim
`usage_metadata`. Computed post-hoc from the 21 retained `raw/*.json` files, purely for
the controller's information and **deliberately not written back into the evidence**:

| | tokens |
|---|---|
| prompt | 37,980 |
| candidates | 23,463 |
| thoughts | 15,386 |
| total | 76,829 |

That covers the 21 final turns. The 5 intermediate tool-call turns have no retained raw
response under the frozen runner, so their usage is not recoverable from this run.

`lane_calculated_cost_usd` is `null`, basis
"price not established for gemma-4-31b-it at freeze time" — the frozen price snapshot
carries no entry for this model. That is the specified behaviour, not a gap.

This is a substrate finding for the controller, affecting any Gemini-family lane.
