# Audit — what the human-acceptance numbers become under the frozen rule

Date: 2026-09-10
Auditor task: read-only recompute. Nothing under `eval/experiments/`, `eval/registry/`,
`eval/capability-map/` or `eval/empirical-planning/` was changed. No model call, no network
call, no cloud command was made.

Tool that produces every number below:
`coordination/audits/tools/recompute_elimination.py`
Run it from the repository root with `python3 coordination/audits/tools/recompute_elimination.py`.
It reads only sealed files and prints the same three sections as this report.

---

## What this audit is about, in one paragraph

Before any money was spent, the project wrote down one rule for throwing a route out of a
question. That rule is in
`eval/empirical-planning/STAGE-A-FREEZE-2026-09/ELIMINATION-RULES.md`. It says a route is out
if refusals or hard errors reach 37.5 % of the **planned** trials (line 5), and out if accepts
are 25 % of the planned trials or fewer (line 5, line 21). It says plainly that a refusal or an
error also counts as a reject (line 27), and it says "Nothing here is changed mid-run; a change
is a new task" (line 29).

Three runs did not use that rule. They wrote a different rule into their own results file,
threw some failed draws out of the count, and made the bottom of the fraction smaller. A fourth
problem is separate: several draws were sent twice, once in one run and once in another, and in
two places the second sending was never written down as a re-do. This report says exactly which
numbers move and which do not.

**Nothing here is a decision.** Where the evidence can be read two ways, both readings are
shown and the choice is left to the Controller.

### The two readings used throughout

Because the frozen rule never provided for sending a failed draw again, a re-sent draw can be
read two ways, and the report shows both side by side:

* **Strict reading** — a draw that failed once stays a failure, whatever the second sending
  produced. This is what the frozen text says on its face, because the frozen text has no
  re-do at all.
* **Lenient reading** — the last sending of a draw is the one that counts, so a successful
  re-send replaces the failure. This is what the runs actually did.

---

## 1. Every trial id that was sent twice

A "logical trial id" is one planned draw, for example
`VID-I2V-01__wan-2.2-a14b-i2v__core__r1`. 267 distinct ids were sent; there were 300 sendings.
**28 ids were sent more than once.** Across all their sendings the ledger records USD 21.96,
of which **USD 9.25 sits on sendings that no `RESULTS.yaml` ever judged**.

Money in the table below is the settled `spend` row in that run's own ledger
(`eval/experiments/EVAL-040/runs/<run>/ledger/<run>/spend-ledger.jsonl`). Every one of these
rows carries `billing_state: reported`, that is, settled — including the rows for the draws
that failed.

### 1a. Eleven of the 28 are only a smoke draw re-used as a production draw (harmless to the maths, not to the money)

There are 17 smoke runs, each planning exactly one trial, and every one of them uses a trial id
that also belongs to a production run (verified for all 17). Those smoke draws are never judged
and never enter any count, so they change no acceptance number. They do cost money: **USD 6.32
across the 17 smoke runs**.

| trial id | runs (in time order) | judged | not judged | money on both? |
|---|---|---|---|---|
| `AUD-LIP-01__kling-lipsync-a2v__chain__r1` | aud-lip-smoke, aud-lip | aud-lip (reject) | aud-lip-smoke | yes, USD 0.14 each |
| `AUD-TTS-01__elevenlabs-v3-direct__native__r1` | aud-tts-eleven-smoke, aud-tts-eleven | aud-tts-eleven (accept) | smoke | yes, USD 0.00 each (plan credits) |
| `AUD-TTS-01__sarvam-bulbul-v3__native__r1` | aud-tts-sarvam-smoke, aud-tts-sarvam | aud-tts-sarvam (accept) | smoke | yes, USD 0.00 each |
| `IMG-CORE-01__nano-banana-2__core__r1` | img-r1-smoke, img-r1 | img-r1 (accept) | smoke | yes, USD 0.07 each |
| `IMG-EDIT-01__nano-banana-pro-edit__edit__r1` | half2-smoke, half2 | half2 (reject) | smoke | yes, USD 0.15 each |
| `MUS-01__lyria__native__r1` | aud-music-lyria-smoke, -smoke2, -smoke3, aud-music-lyria | aud-music-lyria (accept) | three smoke runs | yes, USD 0.06 × 4 |
| `VID-2SPK-01__wan-3.0-prime__A_native__r1` | vid-2spk-smoke, vid-2spk | vid-2spk (accept) | smoke | yes, USD 1.12 each |
| `VID-REF-01__veo-3.1-fast-ref2v__native__r1` | vid-ref-smoke, vid-ref-smoke2, vid-ref | vid-ref (accept) | two smoke runs | yes, USD 0.60 + 0.80 + 0.80 |
| `VID-T2V-01__minimax-h3-max__core__r1` | vid-t2v-smoke, vid-t2v | vid-t2v (accept) | smoke | yes, USD 0.48 each |
| `VID-T2V-02__wan-2.2-a14b__core__r1` | vid-wan2-smoke, vid-wan2 | vid-wan2 (accept) | smoke | yes, USD 0.48 each |
| `VID-TOPO3-01__minimax-h3-max-i2v__A_cheap_still_to_cheap_i2v__r1` | topo3-smoke, topo3-video | topo3-video (reject) | smoke | yes, USD 0.48 each |

(Two more smoke ids appear in the sections below because they also carry a re-do:
`VID-2SPK-01__kling-v3-pro-audio__A_native__r1` and
`VID-I2V-01__wan-2.2-a14b-i2v__core__r1`.)

### 1b. Five ids where a network outage was re-done, and the re-do was written down properly

`eval/experiments/EVAL-040/runs/img-r1-redo/PLAN.yaml:30` sets `redo_of` with the previous run
id and the reason. Every one of these rows in `img-r1/RESULTS.yaml` also carries a filled-in
`redo_of` block. This is the correct pattern.

| trial id | runs | judged | not judged | money on both? |
|---|---|---|---|---|
| `IMG-CORE-03__flux-2-pro__core__r1` | img-r1 (error, network_failure), img-r1-redo (ok) | img-r1-redo (accept) | img-r1 | yes, USD 0.03 each |
| `IMG-CORE-03__gpt-image-2__core__r1` | img-r1 (error, poll_network_failure), img-r1-redo (ok) | img-r1-redo (reject) | img-r1 | yes, USD 0.05 each |
| `IMG-CORE-03__qwen-image-3__core__r1` | img-r1 (error, network_failure), img-r1-redo (ok) | img-r1-redo (accept) | img-r1 | yes, USD 0.04 each |
| `IMG-CORE-03__seedream-5-pro__core__r1` | img-r1 (error, network_failure), img-r1-redo (ok) | img-r1-redo (reject) | img-r1 | yes, USD 0.07 each |
| `IMG-CORE-04__gpt-image-2__core__r1` | img-r1 (error, network_failure), img-r1-redo (ok) | img-r1-redo (accept) | img-r1 | yes, USD 0.05 each |

### 1c. Eight ids where the re-do was NOT written down as a re-do

This is the deviation that matters. In all three runs below the plan header says
`redo_of: null` even though the run exists only to re-send draws that another run had already
sent and paid for:

* `eval/experiments/EVAL-040/runs/vid-wan2-i2v/PLAN.yaml:36` — `redo_of: null`
* `eval/experiments/EVAL-040/runs/vid-2spk-kling/PLAN.yaml:29` — `redo_of: null`
* `eval/experiments/EVAL-040/runs/img-r1-composite/PLAN.yaml:27` — `redo_of: null`

Every one of the trial rows for these ids in the results files also has `redo_of: null` (for
example `eval/experiments/EVAL-040/runs/vid-wan2/RESULTS.yaml:263` and `:278`).

| trial id | runs | judged | not judged | money on both? |
|---|---|---|---|---|
| `VID-I2V-01__wan-2.2-a14b-i2v__core__r1` | vid-wan2 (error http_422), vid-wan2-i2v-smoke (ok), vid-wan2-i2v (ok) | vid-wan2-i2v (accept) | vid-wan2 error row is in the file but has no verdict; the smoke draw is in no file | yes, USD 0.48 × 3 |
| `VID-I2V-01__wan-2.2-a14b-i2v__core__r2` | vid-wan2 (error http_422), vid-wan2-i2v (ok) | vid-wan2-i2v (accept) | vid-wan2 (no verdict) | yes, USD 0.48 each |
| `VID-I2V-02__wan-2.2-a14b-i2v__core__r1` | vid-wan2 (error http_422), vid-wan2-i2v (ok) | vid-wan2-i2v (reject) | vid-wan2 (no verdict) | yes, USD 0.48 each |
| `VID-I2V-02__wan-2.2-a14b-i2v__core__r2` | vid-wan2 (error http_422), vid-wan2-i2v (ok) | vid-wan2-i2v (accept) | vid-wan2 (no verdict) | yes, USD 0.48 each |
| `VID-I2V-03__wan-2.2-a14b-i2v__core__r1` | vid-wan2 (error http_422), vid-wan2-i2v (ok) | vid-wan2-i2v (accept) | vid-wan2 (no verdict) | yes, USD 0.48 each |
| `VID-I2V-03__wan-2.2-a14b-i2v__core__r2` | vid-wan2 (error http_422), vid-wan2-i2v (ok) | vid-wan2-i2v (accept) | vid-wan2 (no verdict) | yes, USD 0.48 each |
| `VID-2SPK-01__kling-v3-pro-audio__A_native__r1` | vid-2spk (error http_403), vid-2spk-kling-smoke (ok), vid-2spk-kling (ok) | vid-2spk-kling (reject) | the vid-2spk failure is in **no** results file at all | yes, USD 1.34 × 3 |
| `VID-2SPK-01__kling-v3-pro-audio__A_native__r2` | vid-2spk (error http_403), vid-2spk-kling (ok) | vid-2spk-kling (reject) | the vid-2spk failure is in **no** results file at all | yes, USD 1.34 each |

Two differences inside this block are worth naming:

* For the six Wan 2 draws, the failures were at least kept in the file:
  `eval/experiments/EVAL-040/runs/vid-wan2/RESULTS.yaml:249-338` lists all six with
  `status: error`, `error_class: http_422` and
  `verdict_basis: harness_request_shape_fault_not_counted`.
* For the two Kling two-speaker draws, the failed rows were **removed from the trial list**.
  `eval/experiments/EVAL-040/runs/vid-2spk/RESULTS.yaml` contains eight trial rows, all with
  `status: ok`; the two `http_403` failures appear only in
  `eval/experiments/EVAL-040/runs/vid-2spk/RUN-LOG.jsonl` and in that run's ledger. The removal
  is not concealed — a prose note at `vid-2spk/RESULTS.yaml:187` says "first two attempts were
  fal-side balance refusals (run vid-2spk, recorded as infrastructure); the judged draws are run
  vid-2spk-kling" — but no machine-readable row survives, so any recount that reads only the
  trial list will miss them. The Registry still holds them (see section 4).

### 1d. Four ids that carry two different Controller verdicts

`IMG-TEXT-01__flux-2-pro__C_composite_textless_base__r1` and `__r2`, and
`IMG-TEXT-02__flux-2-pro__C_composite_textless_base__r1` and `__r2` were sent in `img-r1` and
sent again in `img-r1-composite`. Both sendings succeeded, both were charged USD 0.03, and both
were judged — differently.

| trial id | img-r1 verdict | img-r1-composite verdict |
|---|---|---|
| `IMG-TEXT-01__flux-2-pro__C_composite_textless_base__r1` | reject, note "wrong spelling" (`img-r1/RESULTS.yaml:342-356`) | accept (`img-r1-composite/RESULTS.yaml:15-22`) |
| `IMG-TEXT-01__flux-2-pro__C_composite_textless_base__r2` | reject, note "wrong spelling" (`img-r1/RESULTS.yaml:912-926`) | accept (`img-r1-composite/RESULTS.yaml:23-30`) |
| `IMG-TEXT-02__flux-2-pro__C_composite_textless_base__r1` | reject, note "40% twice" (`img-r1/RESULTS.yaml:447-461`) | accept (`img-r1-composite/RESULTS.yaml:31-38`) |
| `IMG-TEXT-02__flux-2-pro__C_composite_textless_base__r2` | accept (`img-r1/RESULTS.yaml:1017-1031`) | accept (`img-r1-composite/RESULTS.yaml:7-14`) |

The two runs almost certainly judged different pictures — the second run's note says the
strings were set by code on a textless plate — but they carry the same trial id, so on the
sealed record one id has two answers. The routing map keeps both as separate cells with the
**same** `route_key` and the **same** `arm`
(`eval/capability-map/ROUTING-EVIDENCE-MAP-v0.yaml:3629` shows 1 of 4 and "eliminated"; `:3784`
shows 4 of 4, and `:3785-3786` show that its route and arm are identical to the first cell's).

---

## 2. Where the frozen rule and the recorded rule disagree

62 (question, route, arm) groups were recomputed. **13 groups disagree** with what the results
files recorded. They fall into four kinds. "Recorded" is what the committed `RESULTS.yaml`
says; "strict" and "lenient" are the two readings defined at the top.

### 2a. The verdict itself changes — three groups

| question | route | recorded accepts / denominator / verdict | strict | lenient |
|---|---|---|---|---|
| VID-T2V | kling-v3-pro-audio (core) | 2 / 6 / **kept** (`vid-t2v/RESULTS.yaml:626-641`, `eliminated: false` at `:640`) | 2 / 8 → **out on E2** | 2 / 8 → **out on E2** |
| VID-I2V | wan-2.2-a14b-i2v (core) | 7 / 8 / **kept** (`vid-wan2/RESULTS.yaml:369-382`) | 2 / 8, 6 errors → **out on E1 and E2** | 7 / 8 → kept |
| IMG-TEXT | flux-2-pro (C_composite_textless_base) | 1 / 4 / **out on E2** (`img-r1/RESULTS.yaml:1287-1300`) | 1 / 4 → out on E2 | 4 / 4 → kept |

Notes on each:

* **VID-T2V kling-v3-pro-audio.** The run wrote its own rule at
  `eval/experiments/EVAL-040/runs/vid-t2v/RESULTS.yaml:7`: "E1/E2 per (route, question) over
  judged trials; fal balance locks are infrastructure refusals, not counted". Two of the eight
  planned draws were refused by fal with HTTP 403. Dropping them makes the fraction 2 of 6, and
  2 is above the 1-accept line for a denominator of 6, so the route was kept. The frozen rule
  keeps the denominator at 8 planned (line 19 of the rules file) and counts the two refusals as
  rejects (line 27). 2 accepts of 8 is exactly the E2 line (floor of 0.25 × 8 = 2, and E2 is
  "≤"), so the route is out. Both readings agree here, because the two failures were never
  re-sent.
  The run's own prose already says so: `vid-t2v/RESULTS.yaml:727` reads "Kling v3 Pro audio
  2/6 … eliminated (E2)". The file contradicts itself: the table at `:640` says kept, the
  reading at `:727` says eliminated.

* **VID-I2V wan-2.2-a14b-i2v.** The run wrote its own rule at
  `eval/experiments/EVAL-040/runs/vid-wan2/RESULTS.yaml:7`: "harness request-shape faults not
  counted". Six of eight planned draws failed with HTTP 422 in `vid-wan2` and were sent again
  in `vid-wan2-i2v`, which was not declared a re-do. Under the strict reading six of eight
  draws failed, which is far past the 3-failure E1 line, and only two draws (both of
  VID-I2V-04) survive as clean accepts, which is at the E2 line — so the route is out twice
  over. Under the lenient reading the second sending replaces the failure and the route stands
  at 7 of 8. **This is the widest gap in the whole audit.**

* **IMG-TEXT flux-2-pro composite.** Three different answers exist for the same four draws:
  1 of 4 as recorded, 1 of 4 under the strict reading (which refuses to pick between two
  contradictory verdicts on one id and therefore does not credit them as accepts), and 4 of 4
  under the lenient reading. The recorded verdict "out on E2" and the map's second cell
  "4 of 4" cannot both be right about the same four ids.

### 2b. The verdict is the same but the failure count is wrong — three groups

These routes are out (or in) either way. The number that is wrong is `refusals_or_errors`,
which every one of these files records as 0.

| question | route | recorded | strict | lenient |
|---|---|---|---|---|
| AUD-LIP | kling-lipsync-a2v (chain) | 0 accepts / 6, 0 failures, out on E2 (`aud-lip/RESULTS.yaml:106-116`; `infra_refusals_not_counted: 1` at `:108`) | 0 / 6, **1 failure**, out on E2 | same |
| VID-2SPK | kling-v3-pro-audio (A_native) | 0 accepts / 2, 0 failures, out on E2 (`vid-2spk/RESULTS.yaml:172-186`) | 0 / 2, **2 failures**, out on **E1 and E2** | 0 / 2, 0 failures, out on E2 |
| IMG-CORE | seedream-5-pro (core) | 6 accepts / 8, 0 failures, kept | 6 / 8, **1 failure**, kept | 6 / 8, 0 failures, kept |

The `vid-2spk` case is the one the brief flagged. The run wrote its own rule at
`eval/experiments/EVAL-040/runs/vid-2spk/RESULTS.yaml:7`: "provider balance locks are
infrastructure refusals, not counted". **The route's fate does not change** — it was already
out on E2 with zero accepts. Only the reason changes, from E2 alone to E1 and E2 together.

### 2c. The accept count changes but the verdict does not — three groups

All three are `img-r1` routes hit by the network outage and re-done in `img-r1-redo`. Under the
strict reading the failed first sending counts against them; the routes still survive
comfortably.

| question | route | recorded | strict | lenient |
|---|---|---|---|---|
| IMG-CORE | flux-2-pro (core) | 5 / 8, kept | 4 / 8, 1 failure, kept | 5 / 8, kept |
| IMG-CORE | gpt-image-2 (core) | 7 / 8, kept | 6 / 8, 2 failures, kept | 7 / 8, kept |
| IMG-CORE | qwen-image-3 (core) | 7 / 8, kept | 6 / 8, 1 failure, kept | 7 / 8, kept |

### 2d. The denominator is wrong but nothing else moves — two groups

Both are in `vid-t2v`, under the same non-frozen rule at `vid-t2v/RESULTS.yaml:7`.

| question | route | recorded | strict and lenient |
|---|---|---|---|
| VID-T2V | minimax-h3-max (core) | 5 / **7**, kept (`vid-t2v/RESULTS.yaml:642-657`, `n_judged: 7` at `:648`, `infra_refusals_not_counted: 1`) | 5 / **8**, 1 failure, kept |
| VID-T2V | wan-3.0-prime (core) | 4 / **7**, kept (`vid-t2v/RESULTS.yaml:674-689`, `n_judged: 7` at `:680`, `infra_refusals_not_counted: 1`) | 4 / **8**, 1 failure, kept |

### 2e. Two groups where the run judged case by case instead of per question

These are a difference of scope, not of arithmetic. Rule E4 in the frozen file (line 8) makes
elimination per (route, question). Two runs eliminated a route on one case only.

| question | route | recorded | per-question recompute |
|---|---|---|---|
| AUD-TTS | elevenlabs-v3-direct (native) | three separate entries of 2 planned each; the Hinglish one is "out on E2" (`aud-tts-eleven/RESULTS.yaml`, rule text: "E1/E2 per (route, case) since one route ran") | 4 accepts of 6 → **kept**, because the frozen denominator for a TTS lane is 6 with an E2 line of 1 (rules file line 21) |
| VID-REF | veo-3.1-fast-ref2v (native) | two entries of 2 planned each; the person case is "out on E2" (`vid-ref/RESULTS.yaml`, rule text: "elimination per (route, case) here since one route ran") | 2 accepts of 4 → **kept**, because the frozen denominator for reference-to-video is 4 with an E2 line of 1 (rules file line 22) |

Neither of these is a hidden failure; both runs said in writing what they were doing. But under
the frozen rule as written, neither route is eliminated on its question.

---

## 3. Quarantine list — which routing-map cells and RR rules rest on an affected number

### 3a. Routing-map cells (`eval/capability-map/ROUTING-EVIDENCE-MAP-v0.yaml`)

Fourteen cells touch an affected group. The table says what each cell would say under the two
readings. **Where a cell's practical advice does not change, that is stated plainly.**

| cell | what the map shows now | strict | lenient | does the advice change? |
|---|---|---|---|---|
| VID-I2V / `wan-2.2-a14b-i2v` (line 6231; accepts 7, trials **14** at `:6297-6298`; `eliminated: false` at `:6373`) | kept, ranked last of five | out on E1 and E2 | kept, and moves from fifth to fourth (ahead of veo-3.1-fast-i2v) | **YES — the biggest change in this audit.** Under strict this route leaves the question entirely. Under lenient it is better than the map says. |
| VID-T2V / `kling-v3-pro-audio` (`eliminated: false` at `:8060`) | kept | out on E2 | out on E2 | **YES on the flag.** The acceptance number the map already prints (2 of 8) is the literal one; only the `eliminated` flag is wrong. The route's rank (last) and its fallback pointer do not change. |
| IMG-TEXT / `flux-2-pro+C_composite_textless_base` (line 3629; 1 of 4, `eliminated: true` at `:3729`) | out on E2 | out on E2 | kept at 4 of 4 | **YES under lenient.** |
| IMG-TEXT / `flux-2-pro+code_overlay` (line 3784; 4 of 4; same `route_key` and `arm` as the cell above at `:3785-3786`) | kept at 4 of 4 | 1 of 4, out on E2 | kept at 4 of 4 | **YES under strict.** These two cells describe the same route, the same arm and the same four trial ids. |
| VID-2SPK / `kling-v3-pro-audio+A_native` | out on E2 | out on E1 and E2 | out on E2 | **NO.** Out either way. Only the reason changes. |
| AUD-LIP / `kling-lipsync-a2v+chain` | out on E2 | out on E2 (with 1 failure recorded) | same | **NO.** |
| IMG-CORE / `flux-2-pro` | 5 of 8, kept | 4 of 8, kept | 5 of 8, kept | **NO.** Ranking moves only between two routes already tied. |
| IMG-CORE / `gpt-image-2` | 7 of 8, kept | 6 of 8, kept | 7 of 8, kept | **NO** for keep/drop. Under strict, gpt-image-2 drops from joint first to joint second behind nano-banana-2. |
| IMG-CORE / `qwen-image-3` | 7 of 8, kept | 6 of 8, kept | 7 of 8, kept | **NO** for keep/drop; same rank shift as above. |
| IMG-CORE / `seedream-5-pro` | 6 of 8, kept | 6 of 8, kept | same | **NO.** |
| VID-T2V / `minimax-h3-max` | 5 of 8, kept | 5 of 8, kept | same | **NO.** The map's own number is already the literal one; only `RESULTS.yaml` says 5 of 7. |
| VID-T2V / `wan-3.0-prime` | 4 of 8, kept | 4 of 8, kept | same | **NO.** Same as above. |
| AUD-TTS / `elevenlabs-v3-direct+native` | 4 of 6, kept | 4 of 6, kept | same | **NO.** The map already reads it per question; the underlying results file reads it per case. |
| VID-REF / `veo-3.1-fast-ref2v+native` | 2 of 4, kept | 2 of 4, kept | same | **NO.** Same shape as above. |

**A separate accuracy point about the map's denominators.** The map computes acceptance as
accepts divided by the number of trial rows it finds, and that number is not the same thing in
every cell:

* VID-T2V cells use 8 — the planned count, and therefore the literal one. The RR-15 prose and
  the `RESULTS.yaml` tables use 6 and 7 for the same routes.
* VID-I2V / `wan-2.2-a14b-i2v` uses **14** (`:6298`), because the six failed draws and the six
  re-sent draws were both counted. Its per-item block shows three items with "trials: 4" and
  one with "trials: 2" (`:6306-6313`), which is the double-count made visible.
* VID-2SPK / `kling-v3-pro-audio+A_native` uses 2, because the two failed draws were deleted
  from the results file entirely.

So the map currently holds three different denominator conventions at once.

### 3b. Routing rules

**Rules whose advice does NOT change under either reading — the useful negative result:**

* **RR-14** (two speakers in Hindi, line 207). It says avoid Kling v3 Pro audio for Hindi
  dialogue. Kling is 0 of 2 and is out under every reading. **The advice stands, unchanged.**
* **RR-12** (Indian speech, line 189). It cites `aud-tts-eleven` Hinglish 0 of 2. Whether or
  not ElevenLabs is formally "eliminated" on AUD-TTS as a whole, its Hinglish result is
  unchanged and Sarvam's 6 of 6 is untouched. **The advice stands, unchanged.**
* **RR-11** (reference-to-video, line 179). It cites `vid-ref` 2 of 2 for the tin and 0 of 2
  for the person; those per-case numbers are untouched. Only the formal per-question
  elimination flag moves. **The advice stands, unchanged.**
* **RR-2, RR-3, RR-6, RR-7** (still-image text rules). Every route they name is kept under both
  readings; only accept counts move by one. **The advice stands, unchanged.**

**Rules whose wording rests on a number that moves:**

* **RR-15** (plain text-to-video, line 216). Its evidence line at `:220-222` reads
  "kling-v3-pro-audio 2/6 (USD 1.01; **eliminated**)", its caveat at `:225` reads "four fal
  draws refused on balance (not counted)", and it quotes "minimax-h3-max 5/7" and
  "wan-3.0-prime 4/7".
  **The word "eliminated" is CORRECT under the literal frozen rule** (2 accepts of 8 planned is
  at the E2 line) — and it contradicts `vid-t2v/RESULTS.yaml:640` and the map cell at `:8060`,
  which both say `eliminated: false`. The fractions "2/6", "5/7" and "4/7" are the reduced
  ones; under the literal rule they are 2/8, 5/8 and 4/8. The rule's practical advice — Gemini
  Omni first, MiniMax H3 Max as the cash fallback, do not rely on Veo 3.1 fast or Kling —
  **does not change**, because the ranking of the six routes is identical under all three
  readings.
* **RR-16** (the Wan tier, line 227). Its evidence at `:231` reads "i2v 7/8 vs 8/8" and its
  caveat at `:235` reads "six i2v draws were first refused on a harness aspect fault and
  re-run". Under the lenient reading the rule stands as written. **Under the strict reading it
  does not stand at all**: Wan 2.2 A14B is out of VID-I2V on both E1 and E2, so it cannot
  "replace Wan 3.0 Prime as the cheap Wan tier for image-to-video". This is the one rule whose
  substance, not just its arithmetic, depends on the Controller's choice.
* **RR-1** (text on stills, line 87). Its evidence at `:91` reads "img-r1-composite: 4/4
  accepted". Those four accepts are the four trial ids of section 1d, which the same repository
  also records as 3 rejects and 1 accept in `img-r1`. Under the strict reading the "4/4"
  headline is not established. **The rule names no route, so it was found by the run it cites
  rather than by a route name — it is easy to miss in a route-based search.**
* **RR-8** (image-to-video, line 150) does not name Wan 2.2 and predates it, but the map's
  fallback chain inside VID-I2V does change under both readings: under strict, wan-2.2-a14b-i2v
  leaves the chain; under lenient it moves ahead of veo-3.1-fast-i2v. RR-8's own text is not
  affected.

---

## 4. What is NOT affected

**The 575 Registry rows in `eval/registry/registry-v1.jsonl` are untouched by everything
above.** Every one of them carries `evidence_tier: deterministic`. They cover five measured
capabilities and nothing else: `delivery_format_compliance` (117 rows),
`reliability_pass_at_k` (117), `latency_errors_refusals` (120), `cost_and_cpao` (120) and
`reproducibility` (101).

They are untouched for three concrete reasons:

1. **They never read a Controller verdict.** A Registry row is produced by a frozen
   deterministic instrument (`format_probe`, calibrated at
   `eval/harness-v2/instruments/PASS-CRITERIA-v0.yaml`) run over the sealed bytes of the
   artifact. No accept, no reject and no elimination rule enters the calculation, so E1 and E2
   cannot move a Registry number.
2. **They record the failures rather than hiding them.** The very draws that the three run
   files excluded are present in the Registry with their error class. Row
   `cap-7f0a6520d67b6bc6` (kling-v3-pro-audio, VID-2SPK, run `vid-2spk`) records
   `api_error_rate: 1.0` and `error_classes: [{class: http_403, n: 2}]` — the two failures that
   `vid-2spk/RESULTS.yaml` deleted. Row `cap-4a61dd46d1b190a9` (wan-2.2-a14b-i2v, VID-I2V)
   records `api_error_rate: 0.333` and `http_422, n: 2`. Row `cap-3a9ed052c0736aa1`
   (kling-v3-pro-audio, VID-T2V) records `http_403, n: 1`.
3. **Draws that never left the harness are declared, not silently dropped.** The three
   `pre_dispatch_refusal` cases (a `gcloud` authentication failure and one refusal to overwrite
   an already-sealed request) appear in the rows' `excluded_trials` field with their reason —
   see the `nano-banana-2` IMG-CORE row `cap-2f2fef9d7954bd6e`. Nothing was sent and no money
   moved on those.

One caution about the Registry that is not a fault in it: where a trial id was sent twice, the
Registry holds two rows for it, one per run, distinguishable by `run_ids`. There are 12 such
row pairs: ten for `flux-2-pro` on IMG-TEXT (two per capability across the five capabilities)
and two for `kling-v3-pro-audio` on VID-2SPK.
They must not be added together by any consumer. The `wan-2.2-a14b-i2v` rows are already
merged into single rows listing both runs, so that pair does not arise.

Also unaffected: every route and question not named in section 2. That is 49 of the 62 groups,
including all of IMG-EDIT, IMG-EXT, IMG-REF, IMG-COMP, VID-KNEE, VID-MS, VID-TOPO3, MUS, and
the sarvam AUD-TTS route.

---

## 5. Decisions this leaves to the Controller

Each decision below has two options and the consequence of each. No option is recommended here.

### Decision 1 — how a re-sent draw counts (the biggest one)

The frozen rule has no re-do. Six Wan 2 image-to-video draws and two Kling two-speaker draws
were sent, failed, and were sent again.

* **Option A — strict.** A draw that failed once stays a failure.
  *Consequence:* Wan 2.2 A14B is eliminated from VID-I2V on both E1 and E2, RR-16 cannot say
  what it currently says, and the whole "cheap Wan tier for image-to-video" finding is
  withdrawn until the route is re-run cleanly. The Kling two-speaker route stays eliminated but
  gains E1 as a second reason.
* **Option B — lenient.** The last sending counts.
  *Consequence:* all recorded numbers stand as written and RR-16 stands; but the project has
  then accepted a rule that was never pre-registered, and the rules file's own sentence
  "Nothing here is changed mid-run; a change is a new task" (line 29) has been set aside after
  the fact.

**This is the single most consequential decision.** It alone decides whether RR-16 survives.

### Decision 2 — the denominator when a provider refuses on balance or account state

Four fal HTTP 403 refusals in `vid-t2v` and one in `aud-lip` were dropped from the count.

* **Option A — literal.** Keep the planned denominator and count refusals as rejects, exactly
  as rules-file lines 19 and 27 say.
  *Consequence:* `kling-v3-pro-audio` is eliminated from VID-T2V (2 of 8 sits exactly on the E2
  line), which makes RR-15's word "eliminated" correct and makes the map cell at `:8060` and
  `vid-t2v/RESULTS.yaml:640` wrong. MiniMax and Wan 3.0 Prime move to 5/8 and 4/8 but keep
  their places.
* **Option B — keep the run's rule.** A balance lock is an infrastructure fault, not evidence
  about the model, so it is excluded and the denominator shrinks.
  *Consequence:* `kling-v3-pro-audio` survives on VID-T2V, and the internal contradiction
  between `vid-t2v/RESULTS.yaml:640` (kept) and `:727` plus RR-15 (eliminated) must be resolved
  by correcting the prose instead of the table.

### Decision 3 — the four composite draws with two verdicts each

The same four trial ids are recorded as 1 of 4 (and eliminated) in `img-r1` and as 4 of 4 in
`img-r1-composite`, and the routing map holds both as separate cells with the same route and
the same arm.

* **Option A — treat them as one draw with a contested verdict.** The strict reading credits
  none of the disputed ones as accepts; RR-1's "4/4 accepted" is not established from these
  bytes.
  *Consequence:* RR-1 needs a fresh, separately identified set of draws before it can carry a
  number.
* **Option B — treat them as two different objects that were wrongly given one id.** The plate
  was judged in `img-r1`; the plate-plus-code-overlay was judged in `img-r1-composite`.
  *Consequence:* both numbers are valid, RR-1 stands, and the fix is a naming rule — a new
  object gets a new trial id — plus a correction to the routing map so that two cells do not
  share a `route_key` and `arm`.

### Decision 4 — per-case elimination versus per-question elimination

`aud-tts-eleven` and `vid-ref` eliminated a route on a single case. E4 (rules-file line 8) makes
elimination per (route, question).

* **Option A — enforce E4.** Neither ElevenLabs v3 on AUD-TTS nor Veo 3.1 fast ref2v on VID-REF
  is eliminated.
  *Consequence:* two `eliminated: true` entries in the sealed results files become wrong, but
  RR-11's and RR-12's practical advice does not change, because both rules already speak per
  case.
* **Option B — accept per-case elimination as a refinement.** The eliminations stand.
  *Consequence:* the frozen file needs a written amendment saying elimination may be per case,
  which by its own line 29 is a new task rather than a note.

### Decision 5 — what to do about the three undeclared re-do runs

`vid-wan2-i2v`, `vid-2spk-kling` and `img-r1-composite` all have `redo_of: null` while
`img-r1-redo` fills it in properly.

* **Option A — correct the record.** Add the `redo_of` links so that any future recompute can
  see the chain without reading run logs.
  *Consequence:* sealed files change, which the project's own immutability convention treats as
  a new artifact rather than an edit; the Controller must decide the mechanism.
* **Option B — leave the sealed files alone and rely on this audit's tool.**
  *Consequence:* the record stays as it is, and every future consumer must run
  `coordination/audits/tools/recompute_elimination.py` to discover the eight duplicated
  production ids, because nothing in the plans or results files declares them.

### Decision 6 — the money on unjudged duplicate draws

USD 9.25 of settled spend sits on sendings that no results file judges (USD 6.32 of it on the
17 smoke runs, the rest on failed first sendings). Note also that the map's note on the
`vid-t2v` kling failures reads "fal 403 TOP_UP (nothing generated, nothing charged)"
(`ROUTING-EVIDENCE-MAP-v0.yaml:8041`) while the ledger records a settled
`billing_state: reported` spend of USD 1.008 for that same draw.

* **Option A — reconcile the ledger against the providers' statements** and mark the
  never-generated draws as reversed.
  *Consequence:* the cost-per-accepted-output figures in the Registry `cost_and_cpao` rows fall
  slightly for the affected routes; work is needed against three provider accounts.
* **Option B — leave the ledger conservative** (it over-states spend rather than under-stating
  it).
  *Consequence:* cost figures stay safe but pessimistic, and the map's "nothing charged" note
  remains contradicted by the ledger it is supposed to summarise.

---

## Verification note

Every figure in this report was read from a file in this worktree and can be regenerated by
`python3 coordination/audits/tools/recompute_elimination.py`, whose output is deterministic
(verified by running it twice and comparing). The three "known deviations" given to the auditor
were all confirmed against the sealed files, with two corrections worth stating:

1. The brief said `kling-v3-pro-audio` on VID-T2V "survives" under the reduced denominator and
   that RR-15 calls it "eliminated". Both are true. What the brief did not say is that the
   run's own reading text at `vid-t2v/RESULTS.yaml:727` **also** calls it eliminated, so RR-15
   is not contradicting the run alone — the run contradicts itself. **RR-15's wording is right
   under the literal frozen rule; the `eliminated: false` flag at `vid-t2v/RESULTS.yaml:640`
   and at `ROUTING-EVIDENCE-MAP-v0.yaml:8060` is what is wrong.**
2. The brief described the `vid-2spk` deviation as a rule-text change. It is more than that:
   the two failed draws were removed from `vid-2spk/RESULTS.yaml` entirely and re-sent in a
   separate undeclared run. The route's fate is unchanged, so the practical effect is nil.

One item could not be independently confirmed and is stated as such: whether the four
`img-r1` / `img-r1-composite` draws are genuinely the same picture or two different pictures
sharing an id cannot be settled from the sealed record, because `img-r1-composite/RESULTS.yaml`
lists a `sha256` for each of its four draws (`:12`, `:20`, `:28`, `:36`) while
`img-r1/RESULTS.yaml` carries no artifact hash on any row at all (zero occurrences of
`sha256` in the file). The two runs' artifact directories both hold sealed records under the same file names in
different run folders, so a byte comparison is possible but was outside this task's scope.

Finally, for the record: this worktree showed uncommitted modifications under
`eval/harness-v2/`, `PROJECT-MEMORY.md`, `coordination/CONTROL-STATE.md` and
`eval/empirical-planning/price-pins-2026-09/PIN-INDEX.yaml` while this audit ran. They were
made by other sessions, not by this audit. This audit created only
`coordination/audits/AUDIT-2026-09-10-EVIDENCE-RECOMPUTE.md` and
`coordination/audits/tools/recompute_elimination.py`, and committed nothing.
