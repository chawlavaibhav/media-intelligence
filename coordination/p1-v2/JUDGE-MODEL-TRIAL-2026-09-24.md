# Judges' model trial — 2026-09-24

Live calls, founder-approved ("sure" to the corrected rerun; cap USD 20). Spent **USD 9.77** in total, including USD 2.16 on a
first run that was stopped because its inputs were wrong. A model trial never qualifies a judge (`qualified: false` in
every report); it only says which models are worth qualifying.

Harness: `product/qualification/judges.py` (`trial()`), cases from `JUDGE-CASES.yaml` extended with the old jobs of amendment 1
§2. Each checker was given what the design says it gets: the customer's exact words, the waiter's sheet (or the P1 intent),
the customer's product photos, and the full plan or the finished work. Only Gemini is sent video with sound; every other
model gets a contact sheet of still frames.

## Final checker (big taster) — 16 finished pieces: 7 the founder accepted, 9 not accepted

| Model | Accepted pieces it passed | Not-accepted pieces it held back | Saw | Cost (16) |
|---|---|---|---|---|
| gemini-3.1-pro-preview | **4 / 7** | 8 / 9 | video with sound | 0.89 |
| Kimi-K2.6 | 3 / 7 | 8 / 9 | stills | 0.85 |
| Mistral-Large-3 | 1 / 7 | 9 / 9 | stills | 0.33 |
| gpt-5.6-sol | 0 / 7 | 9 / 9 | stills | 1.30 |
| gpt-5.6-luna | 0 / 7 | 9 / 9 | stills | 0.06 |
| DeepSeek-V4-Flash | not run — text only | | | |

Gemini and Kimi both passed Upwork V4 (founder: specific repair). Sol, Luna and Mistral ask for a fix on almost everything.

## Plan checker (recipe checker) — 7 plans: the rejected P1 film + 6 plans of accepted jobs

| Model | Accepted plans it approved | Rejected P1 film plan | Cost (7) |
|---|---|---|---|
| Kimi-K2.6 | 3 / 6 | **approved** | 0.42 |
| DeepSeek-V4-Flash | 2 / 6 | **approved** | 0.02 |
| gpt-5.6-sol | 1 / 5 (one call hit the per-model cap) | held back | 0.64 |
| gemini-3.1-pro-preview | 1 / 6 | held back | 0.66 |
| Mistral-Large-3 | 0 / 6 | held back | 0.28 |
| gpt-5.6-luna | 0 / 6 | held back | 0.04 |

No model named the real reason the P1 plan failed (hands working zips on the video model); the models that held it back
cited audio, logo or format. The equipment sheet row that says so (EQ-001) was written from this same film, so it was
deliberately not supplied — in production the checker gets it on its tray.

On the accepted old plans the strong models' objections are specific and mostly true (RentOK: a tenant tagged rather than
cleared, obstacles reappearing with no reset; Mokobara: the arms-in-the-bag gag is high-risk). The founder accepted those
films anyway: the checker is **stricter than the founder**, because the card sends a plan back for any major issue.

## Recommendations

1. Big taster: **gemini-3.1-pro-preview** (≈ USD 0.055 per film); Kimi-K2.6 as the backup.
2. Recipe checker: no model is ready. Send back only for *blockers*; show *major* issues to the customer as notes on the
   plan-approval page (station 6, the decision point under amendment 1 §3). Always give it the equipment sheet.
3. The recipe set has 1 rejected plan in 7 — add more of the founder's past rejections before any recipe checker can qualify.
4. Luna, Mistral and DeepSeek are not judges.

## Bugs found and fixed (branch `claude/p1-v2-judge-trial`)

Product:
- `config.check_independence` judged the company by the **host** (`azure_openai` → OpenAI), so Kimi on the Aight Azure
  resource was refused as "same company as the chef". Now `config.maker()` reads the maker from the model name.
- A text-only model (DeepSeek-V4-Flash) silently dropped attached photos and judged blind. Now `config.check_vision()` refuses
  it at start-up for any worker shown pictures, and the Azure and Anthropic backends refuse media they cannot send (video,
  or any attachment to a text-only model) instead of dropping it.
- The small taster's escalation reused the clip prepared for the first model; it now prepares it for the escalation model.

Trial harness: plans cut at 24,000 characters (RentOK A/B lost their storyboard); still-image plans passed as an empty shot
list; the P1 film sent as raw video to non-Gemini models; an empty cost sum crashing the report.

Tests: `product/tests/test_v2_model_rules.py`; full suite 140 OK, 1 skipped.
