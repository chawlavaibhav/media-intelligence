# Controller — Audit closeout: how the Stage-A human-acceptance evidence is counted — 2026-09-14

**Status:** APPROVED CONTROLLER DECISION.
**Role:** materialised by the governance closeout lane (Agent A) on branch `work/closeout-a-governance`, recording the human Controller's words without reinterpretation.
**Answers:** items **C-3**, **C-4**, **C-6b**, **C-6c** and **C-6d** of `coordination/audits/AUDIT-2026-09-10-CONTROLLER-DECISIONS.md`; the same questions appear as Decisions 1–4 of `coordination/audits/AUDIT-2026-09-10-EVIDENCE-RECOMPUTE.md` §5 and as open questions OPEN-1, OPEN-2 and OPEN-3 of `eval/capability-map/TAINT-REGISTER-v1.yaml`.
**Frozen rule these rulings apply:** `eval/empirical-planning/STAGE-A-FREEZE-2026-09/ELIMINATION-RULES.md` (E1 — out at 37.5 % refusals or hard errors of the *planned* trials; E2 — out at 25 % accepts or fewer of the planned trials; E4 — elimination is per (route, question); line 27 — a refusal or error counts as a reject; line 29 — "Nothing here is changed mid-run; a change is a new task").

## Provenance

The rulings below were delivered by the Controller to the lead implementation agent in the assignment brief of 14 September 2026, which states: *"These are now APPROVED Controller decisions. Materialise them durably under coordination/decisions/ with provenance. Do not reinterpret them."* They answer the items of `coordination/audits/AUDIT-2026-09-10-CONTROLLER-DECISIONS.md`. Each ruling is quoted verbatim; every "mechanical consequence" below is drawn only from the strict/literal columns of `AUDIT-2026-09-10-EVIDENCE-RECOMPUTE.md` §2 and its §3 quarantine list, and each names the ruling it follows from.

## What this is about, in plain English

Before any money was spent, the project wrote down one rule for throwing a model route out of a test question. Three runs then wrote a different rule into their own results files (dropping provider refusals or request faults from the count), several draws were sent twice under the same name without the second sending being declared a re-do, two runs eliminated routes per case instead of per question, and in one place the same four draws carry two different verdicts. The audit recomputed every number both ways and left the choice to the Controller. These five rulings make that choice. **The 575 deterministic Registry rows are not touched by any of them** — they never read a human verdict (`AUDIT-2026-09-10-EVIDENCE-RECOMPUTE.md` §4).

## Authority — the Controller's words

**C-3 (the elimination rule):**

> "Apply the frozen elimination rule literally. Infrastructure/request failures count wherever the preregistered rule says they count. Any different treatment must be prospective."

**C-4 (the tainted human-acceptance cells):**

> "Adopt exactly this policy: 'any Stage-A human-routing cell affected by duplicated dispatched trial identities, smoke-as-extra-draw, or infrastructure exclusions contrary to E1/E2 is descriptive product-learning evidence only, until recomputed or cleanly replaced. Deterministic Registry evidence is untouched.'"

**C-6b (how a re-sent draw counts):**

> "STRICT interpretation. A failed Wan 2 draw remains a failure under the frozen experiment. The six HTTP-422 failures are not erased by later undeclared re-sends. RR-16 therefore cannot remain clean Stage-A image-to-video routing truth. Successful re-sends may remain clearly-labelled descriptive product evidence. Do not delete them."

**C-6c (the exact-text cell collision):**

> "Re-key exact-text mechanisms. These are DIFFERENT route mechanisms: A. the generative model itself draws exact text; B. the generative model produces a textless visual plate and deterministic code composes exact text afterward. They must have different route identities. Rewrite RR-1 so its evidence says precisely what was accepted. Never imply the model rendered the accepted exact copy when code did."

**C-6d (per question or per case):**

> "Elimination is per (route, question), exactly as frozen E4. Recompute affected derivative cells accordingly."

## Decision

1. **C-3 — the frozen elimination rule is applied literally to everything already run.** The denominator is the planned trial count; a provider refusal (for example a fal HTTP 403 balance lock) or a request-shape fault (for example an HTTP 422) counts as a reject, because line 27 of the frozen rule says so. A run's own results-file rule ("infrastructure refusals not counted", "harness request-shape faults not counted") has no force over the frozen rule. Any different treatment of such failures is **prospective only** — it must be written into a new frozen rule by a new task before the draws it governs are dispatched. (This is option B of C-3 on the decision sheet.)
2. **C-4 — the quarantine policy is adopted in the exact words quoted above.** A Stage-A human-routing cell touched by duplicated dispatched trial identities, a smoke draw counted as an extra production draw, or an infrastructure exclusion contrary to E1/E2 is *descriptive product-learning evidence only* until it is recomputed under the frozen rule or cleanly replaced by fresh draws. Deterministic Registry evidence is untouched.
3. **C-6b — the strict reading.** A draw that failed stays a failure under the frozen experiment. The six Wan 2 image-to-video HTTP-422 failures in run `vid-wan2` are not erased by the undeclared re-sends in `vid-wan2-i2v`. Consequently RR-16 cannot remain clean Stage-A image-to-video routing truth. The successful re-sent clips are kept, clearly labelled as descriptive product evidence; nothing is deleted.
4. **C-6c — two exact-text mechanisms, two route identities.** Mechanism **A**: the generative model itself draws the exact text. Mechanism **B**: the generative model produces a textless visual plate and deterministic code composes the exact text afterwards. They must carry different route identities in every derivative artifact (routing map, taint register, router inputs). RR-1 is rewritten so its evidence line says precisely what was accepted, and no wording anywhere may imply the model rendered the accepted exact copy when code did.
5. **C-6d — elimination is per (route, question), exactly as frozen E4.** Per-case eliminations written by individual runs have no force; affected derivative cells are recomputed on the per-question basis.

## Mechanical consequences — drawn only from `AUDIT-2026-09-10-EVIDENCE-RECOMPUTE.md` (strict / literal columns, §2 and §3)

Each line below is what the audit's own recomputation says follows once the ruling named is applied. Nothing here is a new judgement; a reader can regenerate every figure with `python3 coordination/audits/tools/recompute_elimination.py`.

### Under C-3 (literal rule; refusals and request faults count; planned denominator)

- **VID-T2V / `kling-v3-pro-audio`**: recorded 2 / 6 kept → **2 / 8, eliminated on E2** (2 accepts of 8 planned sits exactly on the E2 line). RR-15's word "eliminated" was already correct; the `eliminated: false` flags in `vid-t2v/RESULTS.yaml:640` and the map cell at `ROUTING-EVIDENCE-MAP-v0.yaml:8060` are what is wrong. RR-15's practical advice (Gemini Omni first, MiniMax H3 Max as cash fallback) does not change (§3b).
- **VID-T2V / `minimax-h3-max`** and **`wan-3.0-prime`**: denominators become 8, not 7 — 5 / 8 and 4 / 8, both kept, one failure each recorded (§2d). The map already prints these literal fractions; only the results files and RR-15's quoted fractions ("5/7", "4/7") are the reduced ones.
- **VID-2SPK / `kling-v3-pro-audio+A_native`**: 0 / 2 with **2 failures** → out on **E1 and E2** (was out on E2 alone). Fate unchanged; reason changes (§2b).
- **AUD-LIP / `kling-lipsync-a2v+chain`**: 0 / 6 with **1 failure** recorded (was 0). Out on E2 either way (§2b).
- **IMG-CORE / `seedream-5-pro`**: 6 / 8 with 1 failure recorded; kept (§2b).
- **IMG-CORE / `flux-2-pro`, `gpt-image-2`, `qwen-image-3`** (network-outage first sendings re-done in `img-r1-redo`): under the strict reading the failed first sending counts — 4 / 8, 6 / 8 and 6 / 8 respectively, all kept; only ranks shift (§2c).

### Under C-6b (strict; a failed draw stays a failure)

- **VID-I2V / `wan-2.2-a14b-i2v`**: recorded 7 / 8 kept → **2 / 8 with six failures → eliminated on E1 and E2** (§2a). The map's current denominator of **14** for this cell (both the failed and re-sent draws counted, `ROUTING-EVIDENCE-MAP-v0.yaml:6298`) is the double-count made visible (§3a); under the literal rule the denominator is the 8 planned draws.
- **RR-16 is withdrawn as clean Stage-A image-to-video routing truth.** Its rule text ("Wan 2.2 A14B … replaces Wan 3.0 Prime as the cheap Wan tier for image-to-video") cannot stand; the route has left the VID-I2V question under the frozen rule. The seven successful clips remain, labelled descriptive product evidence under C-4 and C-6b.
- Under RR-8's fallback chain inside VID-I2V, `wan-2.2-a14b-i2v` leaves the chain (§3b); RR-8's own text is unaffected.
- The two Kling two-speaker draws re-sent in `vid-2spk-kling` follow the same reading: the first sendings stay failures (they are what makes the E1 reason above appear).

### Under C-6c (two mechanisms, two route identities)

- The two IMG-TEXT cells that today share `route_key: flux-2-pro` and `arm: C_composite_textless_base` (`ROUTING-EVIDENCE-MAP-v0.yaml:3629` and `:3784`) become two distinct route identities:
  - **Mechanism A — model draws the text**: the bare FLUX.2 Pro plate as judged in `img-r1` — **1 / 4, eliminated on E2** (`img-r1/RESULTS.yaml:1287-1300`; three rejects noted "wrong spelling" / "40% twice").
  - **Mechanism B — textless plate + deterministic code composition**: the composited outputs, sealed as their own artifacts and judged in `img-r1-composite` — **4 / 4 accepted**.
- **RR-1's evidence line is rewritten** to say that the 4 / 4 were plate-plus-code-composed outputs whose exact strings were set by code — never that the image model rendered the accepted copy. The routing advice RR-1 gives (code-set text on a cheap textless plate where exactness is contractual) is about mechanism B and is stated as such.
- The two IMG-TEXT cells no longer collide for a router matching on route key plus arm — the collision the decision sheet named as blocking the production wedge.

### Under C-6d (per question, exactly as E4)

- **AUD-TTS / `elevenlabs-v3-direct+native`**: the run's per-case "out on E2" for the Hinglish case has no force; per question the route is **4 / 6, kept** (frozen TTS denominator 6, E2 line 1 — §2e). RR-12's per-case advice (Hinglish 0 / 2; Sarvam 6 / 6) is unchanged.
- **VID-REF / `veo-3.1-fast-ref2v+native`**: the run's per-case "out on E2" for the person case has no force; per question the route is **2 / 4, kept** (frozen reference-to-video denominator 4, E2 line 1 — §2e). RR-11's per-case advice (tin 2 / 2, person 0 / 2) is unchanged.
- The two `eliminated: true` entries in those sealed results files are wrong under E4 and stay as written; the correction lives in the derivative map and register (see below).

### What is not affected (OBSERVED, §4)

The 575 Registry rows in `eval/registry/registry-v1.jsonl`; all 49 of the 62 (question, route, arm) groups not named in §2, including all of IMG-EDIT, IMG-EXT, IMG-REF, IMG-COMP, VID-KNEE, VID-MS, VID-TOPO3, MUS and the Sarvam AUD-TTS route; and the practical advice of RR-2, RR-3, RR-6, RR-7, RR-11, RR-12, RR-14 and RR-15.

## Consequences / what changes

- **Sealed evidence is never edited.** No file under `eval/experiments/**` (results files, plans, ledgers, artifacts) changes because of these rulings. Where a sealed results file now disagrees with the frozen rule, the file stays as written and the correction is carried by the *derivative* artifacts — the routing map, the taint register and the tools that regenerate them.
- **The derivative map and register are being regenerated by a separate lane on this branch** (the evidence lane) to reflect C-3, C-4, C-6b, C-6c and C-6d. This record does not state that regeneration is complete; the evidence lane's own commits and the register's summary counts are the proof.
- **OPEN-1 closes** — C-6d answers it: per (route, question).
- **OPEN-2 closes by the sealed-evidence rule.** The three undeclared re-do runs (`vid-wan2-i2v`, `vid-2spk-kling`, `img-r1-composite`, each with `redo_of: null`) are not corrected in place, because sealed files are never edited. The duplicate-identity chain is recorded and recomputable in the derivative tools (`coordination/audits/tools/recompute_elimination.py`, `build_taint_register.py`) and in this record; that is where a future reader finds it. (This corresponds to option B of the audit's Decision 5; the choice follows mechanically from the project's immutability convention plus C-6b's "Do not delete them".)
- **OPEN-3 is moot for counting under C-6c, but remains an unresolved factual question.** Because mechanism A and mechanism B are different route identities by definition, the two IMG-TEXT cells no longer compete for one count and the 1 / 4 and 4 / 4 figures each attach to their own mechanism. Whether the four `img-r1` and `img-r1-composite` draws were the same bytes judged twice or two different pictures sharing an id is **still not established** — `img-r1/RESULTS.yaml` carries no artifact hash, and a byte comparison of the two runs' artifact directories has not been done (`AUDIT-2026-09-10-EVIDENCE-RECOMPUTE.md`, verification note). This record does not resolve it.
- **Trial-id naming is not settled by C-6c.** C-6c speaks of *route* identities. The audit's suggested fix for the collision at trial level — a new object (a composited output built from a plate) gets a new trial id, never the plate's (`AUDIT-2026-09-10-EVIDENCE-RECOMPUTE.md` §5 Decision 3, option B) — is consistent with C-6c but is not stated by it. Adopting it for future runs would be a prospective rule change under C-3's last sentence and is not made here.
- **Cells that lose their number under these rulings need fresh draws before they can carry one again** (the taint register's `replacement_needed`). Whether and when those draws happen is a spend decision (Group 3 of the decision sheet, C-15) and is **not** authorised here.

## Context only — not a ruling

C-5 (the supposed 206-vs-200 judge breach) was withdrawn by the audit itself — `calls: 206` was a row count, at most 190 calls were sent, no breach. Nothing to rule.

## What this does NOT authorise

- No edit to any sealed file under `eval/experiments/**`, `eval/registry/**` or `eval/empirical-planning/STAGE-A-FREEZE-2026-09/**`, and no edit to any `*.local.yaml`.
- No deletion of the successful re-sent clips, the smoke draws or any artifact — they remain, labelled as descriptive product evidence.
- No amendment of the frozen elimination rule for work already run; any different treatment of infrastructure failures is prospective and needs a new task and a new frozen rule.
- No fresh draws, no re-run of any tainted cell, no clean replacement of RR-16's route — those are Group 3 (paid) items and remain unauthorised.
- No Registry row is created, removed or changed by these rulings.
- No verdict on whether Canon works; that remains reserved to the Controller.
- **Adopting the Alpha policy is NOT spend authorisation. No paid dispatch is authorised by any decision above.**
