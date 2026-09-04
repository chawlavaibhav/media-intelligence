# POST-HOC USAGE RECOVERY — gemma-no-canon

**Derived evidence. Not a rerun, not a correction, not a replacement.**

`result.json` and `attempt-ledger.json` are the sealed experimental record and are
byte-unchanged. This note and `POSTHOC-USAGE-RECOVERY.json` sit *alongside* them.
Zero model calls were made to produce them.

## The defect

The frozen `tools/providers.py` reads `usage` off the Gemini response. The
`google-genai` SDK exposes it as **`usage_metadata`**. Every Gemini turn therefore
recorded `input_tokens`, `output_tokens`, `reasoning_tokens` and
`provider_reported_usage` as `null` in the sealed evidence — even though the provider
did report them.

The substrate was **not** modified to fix this. Changing the runner after the first
experimental call, or changing any file the freeze fingerprint covers, is forbidden by
the execution contract. Recovery is derived instead.

## Method

Purely mechanical, from retained bytes only:

1. Every provider turn recorded in `attempt-ledger.json` is enumerated (26 turns).
2. Each turn is joined to a retained raw response by the provider's **own**
   `response_id`, matched against the turn's `provider_request_id` — not by filename
   order or position. Duplicate ids would abort the extraction; there were none.
3. Where the join lands, the raw response's `usage_metadata` block is read **verbatim**
   and these fields are lifted unchanged: `prompt_token_count`,
   `candidates_token_count`, `thoughts_token_count`, `cached_content_token_count`,
   `total_token_count`.
4. Nothing is estimated, interpolated, averaged or carried across turns. A turn with no
   retained raw response contributes to no total.

Each recovered turn also records the raw file it came from and that file's sha256, so
the derivation can be re-checked against the committed bytes.

## Three outcomes, kept distinct

| Outcome | Turns | Meaning |
|---|---|---|
| **RECOVERED** | 20 of 26 | raw response retained; `usage_metadata` read verbatim |
| **UNKNOWN — raw not retained** | 6 of 26 | no raw response exists for this turn; usage unrecoverable |
| **Field reported as null by the provider** | see below | raw retained, provider itself reported no value |

The third row is a separate thing from the second and must not be read as a gap in
retention. `cached_content_token_count` is `null` in **all 20** retained responses: the
provider reported no cached-content tokens. `thoughts_token_count` was reported by all
20.

## Why 6 turns are unrecoverable

The frozen runner writes **one raw response per attempt** — the final turn's. The six
trials on briefs B01 and B02 each called `website_read` once, so each ran two provider
turns, and only the second was retained. The six lost turns are exactly the
`turn_index: 0` tool-call turns of:

`B01-R1`, `B01-R2`, `B01-R3`, `B02-R1`, `B02-R2`, `B02-R3`

Their usage is **UNKNOWN** and stays UNKNOWN. It is not estimated from the sibling
turn, from the other trials, or from the prompt.

## What the recovered numbers are, and are not

Across the 20 turns with retained raw responses:

| Field | Recovered sum | Turns reporting |
|---|---:|---:|
| `prompt_token_count` | 28,170 | 20 |
| `candidates_token_count` | 20,504 | 20 |
| `thoughts_token_count` | 11,543 | 20 |
| `cached_content_token_count` | null | 0 |
| `total_token_count` | 60,217 | 20 |

Internal check: 28,170 + 20,504 + 11,543 = 60,217, matching the summed
`total_token_count` exactly.

**These are not lane totals.** They cover 20 of 26 provider turns and are a strict
**lower bound** on true lane usage. 12 of 18 trials have complete usage; the 6 website
trials do not. `POSTHOC-USAGE-RECOVERY.json` marks each trial with
`trial_usage_complete` so a partial figure can never be mistaken for a complete one.

## Cost

**UNKNOWN.** Two independent reasons, either sufficient on its own:

1. `common/price-snapshot.yaml` records no established input/output price for
   `gemma-4-31b-it` at freeze time (`input: null`, `output: null`).
2. Six provider turns have unrecoverable usage.

No price is inferred and no usage is estimated, so no cost is stated.

## Note for the controller

Validator gate R17 passes on this defect: it checks that trial totals equal the sum
over turns, and consistent nulls satisfy that. The validator cannot presently tell
"the provider exposed nothing" from "the adapter read the wrong field". Any other lane
running on the Gemini API is likely affected the same way, and its raw responses are
likely recoverable the same way.
