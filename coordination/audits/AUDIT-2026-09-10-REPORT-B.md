# Independent audit — media-intelligence, 10 September 2026 (Report B)

**Auditor:** second independent auditor (a parallel audit is running; this file is deliberately a separate
document and overwrites nothing).
**What was audited:** the whole project as it stands on `main` at commit `dcfa6af` — the Capability Lab run
(EVAL-040 to EVAL-043), the harness, the Registry, the routing map, the money, the governance papers, and the
Canon workstream at a lighter level.
**How:** read-only. Nothing was edited except this file. No model was called, no money was spent, no cloud
account was touched. Every number below was re-computed from the committed files, not copied from a summary.
**One caution on paths:** the main working copy on this machine sits 89 commits behind `origin/main`. The audit
was run against the real `main` (`dcfa6af`) using a temporary read-only copy. Nothing in the repository or in
any other worktree was changed.

---

## Part 1 — Findings

Severity: **High** = money, evidence or governance can be wrong. **Medium** = a claim is weaker than it reads.
**Low** = tidy-up. **Info** = worth knowing, no action forced.

### F-1 (High) — Two spending caps were crossed, and the machine could not have stopped it

| Piece | Signed cap | Actually spent | Over by |
|---|---|---|---|
| Video piece 1 (text into motion) | USD 9.96 | **USD 10.364** | 0.404 |
| Wan 2 contender round | USD 11.53 | **USD 11.840** | 0.310 |

The money in each case is small. The mechanism is the problem. Each *run* keeps its own separate ledger folder,
and the cap is checked only inside that folder (`eval/harness-v2/ledger.py:271`, in its own words: "Cumulative
spend for one EVAL-040 run"). One signed authorisation was used by three or four runs (`topo3-plates`,
`topo3-smoke`, `topo3-video`; and `vid-wan2`, `vid-wan2-smoke`, `vid-wan2-i2v`, `vid-wan2-i2v-smoke`), and each
new run started with the whole cap available again.

Evidence: every run's `ledger/<run>/run.json` + `spend-ledger.jsonl` under
`eval/experiments/EVAL-040/runs/`; caps at
`coordination/decisions/CONTROLLER-SPEND-AUTHORISATION-IMAGE-HALF-TWO-AND-VIDEO-PIECE-1-2026-09-09.md:92`
and `coordination/decisions/CONTROLLER-SPEND-AUTHORISATION-WAN2-CONTENDER-ROUND-2026-09-10.md:24,40`.
The Wan 2 record is also internally inconsistent: §1 sizes the round at "USD 8.00 (+ smoke 0.48) ≈ USD 8.5"
while §2 sets the cap at USD 8.39 — below its own estimate.

**Fix in one line:** keep one ledger per authorisation file (not per run id), so every run under the same signed
cap draws from the same pot.

### F-2 (High) — The headline spend figure in the state-of-record does not match the ledgers

`coordination/CONTROL-STATE.md:266-268` says: "Ledger total USD 110.7 (cash USD 67.0 on fal; GCP credits
USD 43.8 incl. the USD 3.16 judge run…)".

Re-computed from all 39 run ledgers at `dcfa6af`:

| Pool | Recomputed |
|---|---|
| Cash (fal) | **USD 77.5235** |
| Cloud credits (Vertex/GCP) | **USD 41.5522** |
| Sarvam | **₹0.894** (USD 0.0094) |
| ElevenLabs plan credits | **1,198** (no cash) |
| **Total in run ledgers** | **USD 119.085** |
| Vision-judge run (outside every run ledger) | USD 3.156 |
| **Grand total** | **USD 122.24** |

The Sarvam and ElevenLabs figures in `CONTROL-STATE` are right. The cash and credit figures are not; the total
understates by about USD 11.5. The most likely cause is that the line was written before the Wan 2 round and
never recomputed.

**Fix in one line:** recompute the total from the ledgers and restate that paragraph.

### F-3 (High) — About USD 10.11 of recorded spend produced no artifact, and at least USD 2.88 of it was never charged

24 ledger entries are settled as `spend` but have no sealed result file. This is by design: once a request may
have left the machine, the reservation is settled at the estimate whatever comes back
(`eval/harness-v2/adapters/base.py:355-387`). It is the safe direction for a cap, but it means **the ledger is
an upper bound on money, not a record of money**.

The clearest case: six Wan 2 image-to-video draws were refused by fal with HTTP 422 before anything was made.
The Controller's own record says "nothing generated, nothing charged"
(`CONTROLLER-SPEND-AUTHORISATION-WAN2-CONTENDER-ROUND-2026-09-10.md:38`), yet USD 2.88 sits in the ledger as
spent. Five image trials in `img-r1` were settled after a network failure and then drawn again in `img-r1-redo`
— paid twice in the ledger, one result kept.

**Fix in one line:** check the fal and Google bills once against the ledger, and mark the entries that were
never actually charged.

### F-4 (Medium) — Limits written as "no more than N calls" are not enforced anywhere (one real overrun, one false alarm)

* The stand-in picture run made **19 paid calls** where the record authorises "≤ 16 calls, ≈ USD 1.1"
  (`CONTROLLER-SPEND-AUTHORISATION-IMAGE-HALF-TWO-AND-VIDEO-PIECE-1-2026-09-09.md:23-28`); it cost USD 1.605.
  The same paragraph gives two different estimates for the same work (≈ USD 1.41 and ≈ USD 1.1).
* ~~The vision-judge report records **206 calls** against an authorised maximum of 200.~~
  **CORRECTED 10 Sep 2026 — there was no breach.** The report's `calls: 206`
  (`eval/experiments/EVAL-040/QUALIFICATION-REPORT-2026-09-09.yaml:2067`) is a *row* count produced by the
  offline rebuild, not a count of calls sent. The 14 committed `SCREEN-RESULTS.yaml` files hold **210 rows**,
  of which only **190 carry any evidence of a call** (a `usage` block or an `http_status`); the other rows are
  audio trials, which are decided `cannot_judge` without sending anything. So at most 190 calls were sent
  against the authorised 200, the live counter never tripped, and the report's empty `stopped` field was
  correct all along. Both auditors reported this as a governance breach; both were wrong. The reason it could
  not be settled from the repository is the real defect: the live run persisted no authoritative counter, so a
  rebuild silently substituted a different number — that is now fixed in `qualify_screen.py`.

Money stayed inside the USD caps in both cases. After the correction above, **one** stated call limit was
actually exceeded (the fixtures run), not two.

**Fix in one line:** put a call ceiling in the ledger next to the money ceiling, and have the judge tool record
its live call count in the report — both done on `work/audit-b-zero-spend-fixes`.

### F-5 (Medium-High) — The first document every worker is told to read is out of date and says the opposite of the truth

`PROJECT-MEMORY.md` was last refreshed on 7 September, before the whole two-day run. It still says the
Capability Registry "exists as a schema and validator with **zero rows**" (`PROJECT-MEMORY.md:39-40`) and lists
"the empty Capability Registry by deliberate admission policy" as a standing blocker (`:228`). There are 575
rows. `coordination/CONTROL-STATE.md:25` instructs every worker to read that file first.

**Fix in one line:** a Governor refresh of `PROJECT-MEMORY.md` (Canon's own open-work list already asks for it —
`canon/CANON-SHAPE-v1.md` §7 item 5).

### F-6 (Medium) — A pre-registered elimination rule was changed in the middle of the run, and one route's fate turns on it

The frozen rules say a route is out if it is accepted 2 times or fewer out of 8, that a refusal or error still
counts in the denominator, and — in as many words — "Nothing here is changed mid-run; a change is a new task"
(`eval/empirical-planning/STAGE-A-FREEZE-2026-09/ELIMINATION-RULES.md`).

Three runs (`vid-t2v`, `vid-2spk`, `vid-wan2`) record a different rule in their own results file, for example
`eval/experiments/EVAL-040/runs/vid-t2v/RESULTS.yaml`: "over judged trials; fal balance locks are infrastructure
refusals, not counted". With the smaller denominator, Kling v3 Pro audio (2 accepts) **survives**; under the
frozen rule (2 of 8) it is **eliminated**. The routing map's own rule RR-15 describes it as "eliminated", so the
map's words and the results file disagree. No Controller decision records the change.

Everything else checks out: I recomputed all 63 elimination entries; 60 match the frozen arithmetic exactly.

**Fix in one line:** one short Controller ruling on whether a provider balance lock counts in the denominator,
then regenerate the map and correct RR-15.

### F-7 (Medium) — The video and audio rounds were blind by good behaviour, not by construction

The two image rounds were done properly: the true mapping was written to a file outside the repository, and only
a salted fingerprint of it was committed. I re-computed both fingerprints from the off-repo keys — **both
match** (`img-r1`, 75 items; `half2`, 36 items).

Every video and audio round did it differently: `MAPPING.json` sits in plain sight next to the answer sheet, and
the results files say so honestly (`commitment_verified: false`). Worse for later checking, the blind copies the
Controller actually watched (K01…, W01…) were never sealed into the repository — only the mapping and the
verdicts survive. Nobody can now prove that the clip watched as "K01" was the file the mapping names.

**Fix in one line:** run video and audio judging through the same packet tool as the images, and seal the blind
copies.

### F-8 (Medium) — For 17 trials there are two provider draws and only one is judged

Smoke tests reuse the same trial name as the real run (for example
`VID-T2V-02__wan-2.2-a14b__core__r1` exists in both `vid-wan2-smoke` and `vid-wan2`). The smoke draw is paid for,
sealed, and never judged. Nothing suggests a bad draw was quietly dropped — the smoke always ran first — but the
practice means a route's real number of draws is not what the map says.

**Fix in one line:** give smoke draws their own trial names.

### F-9 (Medium) — The two routes the map recommends for text on stills have never run on the surface the project now intends to use

Every one of the 319 paid calls ran on fal, Vertex, Sarvam or ElevenLabs. **No call has ever run on the Gemini
Developer API.** The roster was re-pointed on 10 September so that Nano Banana 2 / Pro / Pro-edit and Gemini Omni
now price against the Gemini API (USD 0.134 per image), and the audit index presents this as done. The master
price index still carries the old fal price (USD 0.15) for `nano-banana-pro-edit`; the new price lives only in a
sub-index (`eval/empirical-planning/price-pins-2026-09/gemini-api/PIN-INDEX.yaml`).

**Fix in one line:** one small paid smoke on the Gemini API before quoting those routes or their prices, and
refresh the master pin index.

### F-10 (Low-Medium) — The frozen package is not byte-identical to what its own generator now produces

I rebuilt the whole Stage-A package from `tools/build.py` into a temporary folder. Every file matches except one
line of `COST-TABLE.yaml`, which records `roster_last_commit: 10464b2` and `working_tree_matches_head: false`,
where a rebuild at `dcfa6af` gives `d8399d8` and `true`. **All prices are identical.** The committed package was
built from an uncommitted roster and then committed.

**Fix in one line:** rebuild and commit the package so its own provenance line is true.

### F-11 (Low) — One authorisation was committed a minute after the calls it covers

The composite re-run (`img-r1-composite`) was paid for at 19:53–19:54 IST on 8 September; the addendum
authorising it was committed at 19:54 (`51ba23d`). The addendum itself quotes the Controller approving it at
"~15:45 IST" — four hours earlier — so the authority looks real; only the paper is late. Every other tranche's
record was committed before, or in the same minute as, its first paid call.

### F-12 (Low) — Two of the judge's price quotes are not literal quotes

I checked all 42 pinned price pages: files, byte counts and fingerprints all match, and every quoted price
string appears literally in the fetched bytes. The exception is the judge's own price index, whose two quotes are
joined with "…" and so are not literal. The underlying facts are in the page (`gemini-3.5-flash`, `$1.50`,
`$9.00`). The figure "1,548 tokens per image" used in the cost calculation is **not** in the pinned bytes; the
page gives 258 tokens and a crop formula.

### F-13 (Low) — Verdicts arrive as one line of free text and are transcribed by a worker

Example, `eval/experiments/EVAL-040/runs/vid-knee/judging-video/VERDICTS.yaml`: the Controller's words are
"v1- accept, v2, v3- doesn't look like slow camera, v4- no condesation on bottle, v5- got a label, no slow
camera, v6- got a label". Item v2 carries no words of its own; the worker read it as sharing v3's reason and
recorded a reject. That reading is reasonable, but it is a reading.

**Fix in one line:** a numbered accept/reject line per item, or a tick-box sheet.

### F-14 (Low) — The review page shown to the Controller is outside the repository

`CONTROL-STATE.md:275` says "Review page published to the Controller as an Artifact". There is no copy in the
repository, so its numbers cannot be audited. Marked **UNSUPPORTED**, not wrong.

### F-15 (Info) — Honest weaknesses already recorded, restated so they are not lost

* The Registry schema is still marked `PROPOSED_NOT_IN_FORCE`.
* 524 of 575 rows rest on a single base item (`n_items: 1`), and every row says
  `independence NOT ESTABLISHED`. These are reference calculations, not statistics.
* The frozen `format_probe` resolution rule mis-fails every non-square delivery — already recorded in
  `CONTROL-STATE` and in a decision of 9 September.
* The judge is not qualified (kappa 0.33, false-accept 22 %). Stated plainly in `CONTROL-STATE` and in the
  qualification report.
* The cheapest Wan and Kling tiers were never run — the roster tier gap the Controller himself caught
  ("havent we failed the very principle"). Stated plainly.

### F-16 (Info) — This run says nothing at all about Canon, in either direction

Every prompt in the run came from a Canon blueprint (`prompt_basis`: `blueprint_main` 528 rows,
`blueprint_textless_plate` 10). There was no arm without Canon, so no comparison exists. Anyone reading the
routing map as evidence that Canon works — or does not — would be reading something that is not there.
`canon/CANON-SHAPE-v1.md` §7 still lists "Build the gate" as "the next build" although the gate was merged on
7 September; `CONTROL-STATE` says so correctly and governs.

---

## Part 2 — What is solid (checked, not assumed)

These are the things I tried hardest to break and could not.

* **Sealed evidence is intact.** All **311** sealed media files re-hash exactly to the fingerprint in their
  record file, and all match the byte counts. Git history shows **no artifact or media file was ever modified
  after sealing** — the only later edits are to results, verdicts and summaries.
* **Blind judging held where it was built to hold.** Both image commitments recompute correctly from the
  off-repo keys. Every mapping was committed before its verdicts. All **147** blind entries point at bytes that
  exist and match. The reveal keys are not in the repository (only their fingerprints).
* **The Registry is disciplined.** The validator passes: 575 rows, all `deterministic`, all carrying the
  fingerprint of the frozen pass-criteria file. No human accept/reject is encoded as a measurement. I rebuilt the
  rows for two runs from the sealed bytes — **25 of 25 came out byte-identical** to what is committed.
* **The routing map is generated, not written.** I regenerated it from the Registry and the results files: **61
  cells, identical** apart from a file path and a flag I did not pass. All 61 cells carry all four evidence tiers
  with the right "is this a Registry row" flag. **60 of 61** human-acceptance counts match the results files
  exactly (the 61st is the composite arm, which matches its own results file, 4/4). All 16 routing rules cite a
  source that exists, and their numbers match.
* **Prices are pinned properly.** All 42 pinned pages verify: file present, byte count right, fingerprint right,
  quoted price present in the bytes.
* **The harness does what it claims.** All **326 tests pass**. Network code lives only in `transports.py`. Money
  is reserved before any request leaves. Zero retries is enforced by refusing any authorisation that says
  otherwise. No key material appears anywhere in the evidence — the only pattern hits are chance letter sequences
  inside base64 images.
* **Coverage is real.** All **35 of 35** package cases were run and judged.
* **The published per-route numbers are true.** I rebuilt the acceptance table from the raw verdicts and checked
  every headline: image half two 10/12, 4/12, 3/12; image-to-video 8/8, 8/8, 7/8, 5/8; text-to-video 8/8, 5/7,
  4/7, 4/8, 2/6; two speakers 6/8; speech 6/6 and 4/6; music 4/4; lipsync 0/5; Wan 2 11/16. **Every one matches.**

---

## Part 3 — Verdict per section

| # | Section | Verdict | The one sentence that decides it |
|---|---|---|---|
| A | Governance and money | **FAIL** | Every run has a signed record, but two piece-level caps were crossed and the machine cannot enforce a cap across runs (F-1); one stated call limit was exceeded (F-4, after the judge correction). |
| B | Evidence integrity | **PASS WITH NOTES** | Nothing sealed has changed and every hash matches; the video/audio rounds' blindness rests on conduct rather than construction (F-7, F-8). |
| C | Registry discipline | **PASS** | Validator passes, no human verdict inside, rows rebuild byte-identical. |
| D | Map discipline | **PASS WITH NOTES** | The map regenerates exactly and every number traces back; one elimination rule was changed mid-run and one rule's wording no longer matches its results file (F-6). |
| E | Pricing and package | **PASS WITH NOTES** | Every price pin verifies; the package's own provenance line is stale and three prices are explained rather than literal (F-10, F-9, F-12). |
| F | Harness claims | **PASS** | 326 tests pass; network, retries, reservation-first and key hygiene all verified independently. |
| G | Method | **PASS WITH NOTES** | Blind, one call one trial and repeat-is-not-retry hold for the image rounds; weaker for video/audio, and the elimination denominator moved (F-6, F-7, F-13). |
| H | Honesty of the narrative | **PASS WITH NOTES** | Every per-route number in the summaries and the audit index is true, and both conceded failures are stated plainly; the money total is the one wrong number (F-2, F-3). |
| I | Canon | **PASS WITH NOTES** | The shape document and the gate decisions agree in substance; §7's first item is stale, and no Canon claim is supported or refuted by this run (F-16). |
| J | Risks and decisions | **delivered below** | — |

---

## Part 4 — What could still make the routing map wrong, in order

1. **Two draws per cell.** 524 of 575 Registry rows rest on one item; most human cells are 2 or 4 draws. A route
   that passed 2/2 could be a coin that landed twice. *This is the biggest one.* Fixing it costs money, not
   cleverness: more draws per cell.
2. **The judge is one person and is not reproducible.** 261 verdicts came from one pair of eyes in two evenings,
   written as free text. The machine judge that was meant to relieve him agrees only two-thirds of the time and
   wrongly accepts 22 % — not usable. Any bias in the human verdicts is baked into every rule.
3. **Constructed stand-ins, not customer photos.** The whole "work on a supplied photo" half ran on pictures the
   project generated for itself. Real customer photographs are messier: bad light, real faces, real logos.
4. **The silent Wan/Kling tier gap.** The cheapest live tiers were never run, so "cheap-first works" is proven
   against mid tiers, not against the cheapest ones. The next cheapest rung may be worse in a way that changes
   the rule.
5. **Prices and surfaces have moved under the evidence.** The recommended still routes are now priced on a
   surface that has never carried a single call (F-9). Cost-per-accepted figures in the map are on the old
   surface.
6. **Elimination arithmetic changed mid-run** (F-6): one route's survival depends on which version you apply.
7. **Selection at the input.** Image-to-video was run on stills the Controller had already accepted. The
   Registry labels this honestly (`controller_accepted_generated_still`), but it means i2v numbers are
   conditional on a good input, not on a typical one.

---

## Part 5 — Decisions only the Controller can take

Free first, then the ones that cost money.

| # | Decision | Cost | Why it cannot wait |
|---|---|---|---|
| 1 | Rule on the two cap crossings (accept them as recorded, or annul them) | USD 0 | The signed-cap discipline is the project's main safety rail. |
| 2 | Order one ledger per authorisation, plus a call ceiling next to the money ceiling | USD 0 (half a day of work) | Otherwise the same overrun happens on every future multi-run piece. |
| 3 | Order one reconciliation of the ledger against the fal and Google bills, and restate the spend total | USD 0 | Every future price you quote a customer rests on this number. |
| 4 | Rule on how a provider balance lock counts in elimination, then regenerate the map | USD 0 | One route's elimination is currently ambiguous. |
| 5 | Order a Governor refresh of `PROJECT-MEMORY.md` (and §7 of the Canon shape document) | USD 0 | Every new session starts by reading something false. |
| 6 | Order video/audio judging through the sealed blind packet from now on | USD 0 | Restores provable blindness. |
| 7 | Cheapest-tier floor round (Wan/Kling cheapest live tiers) | ≈ USD 10–15 | Closes the tier gap you yourself flagged. |
| 8 | One Gemini API smoke for the two recommended still routes | ≈ USD 1 | Nothing has ever run on that surface. |
| 9 | Judge v2 (better prompt / stronger model) before any re-qualification | ≈ USD 3–5 per attempt | Human judging is the scaling bottleneck. |
| 10 | Round two of stills (more draws per cell) | ≈ ₹4,300 (USD 45) | Turns "directional" into "reliable". |
| 11 | Seedance 2.5, only where every cheap route failed | ≈ USD 6 | Two briefs are still unanswered. |
| 12 | Stage B (survivors, sweeps) — or skip it and go straight to outcomes | ≈ USD 250 | This is the fork in the road; see Part 7. |
| 13 | Stage C (outcomes and cost-per-accepted-outcome) | ≈ USD 150 | The first number that says whether the business works. |
| 14 | Settle HED-1 — which human time counts in the cost of an accepted outcome | USD 0 | Blocks any honest price. |

---

## Part 6 — Where we actually are, in plain words

**What exists and is real.** In two days the project ran 319 paid calls across 35 route variants and 35 customer-shaped
briefs, sealed 311 pieces of media, and had a human judge 261 of them against written acceptance contracts.
**174 were accepted — two out of three.** All of it cost about **USD 122** (of which about USD 45 was cloud
credit, not cash). That works out to roughly **USD 0.70 per accepted picture, clip or audio file**, and the
evidence is reproducible: I rebuilt the Registry rows and the routing map from the sealed bytes and got the same
files back.

Out of that came a **routing map with 61 cells and 16 rules** that answers, for sixteen kinds of job, which model
to send it to and what it costs. That map is the asset. It is honest about its own weakness — it says everywhere
that human acceptance is not a Registry row, and it carries its caveats in the open.

**What does not exist.** Everything that would make this a product:

* no way for a customer to send a request (no intake, no request compiler);
* no Production IR, no planner, no routing code — the map is a document a human reads, not something software
  consults;
* no repair loop when a draw is rejected;
* no cost-per-accepted-outcome measured on a real brief end to end;
* no automatic judge — today acceptance means Vaibhav watching clips one by one;
* nothing commercial at all: no terms, no output-rights position, no provider-resale review, no price list, no
  refund or re-draw policy. I searched the repository; these documents do not exist.

**The single sentence.** The measurement machine is built and trustworthy; the product is not started. The
binding constraint on going public is not model quality — it is that one person is the quality gate, and no
number yet exists for what an accepted customer outcome costs.

---

## Part 7 — A plan to get from here to a public offer

Nine steps. The money figures are provider spend only. Steps P0–P2 can start immediately; P4 is the gate that
decides whether a public price is possible at all.

**P0 — Close this audit. USD 0. About one day.**
Decisions 1–6 in Part 5: rule on the caps, one ledger per authorisation, call ceilings, reconcile the bills and
restate the total, rule on the elimination denominator, refresh `PROJECT-MEMORY.md`, and move video/audio to the
sealed blind packet. Nothing below is safe to build on until the money record is trusted.

**P1 — Finish the evidence floor. ≈ USD 60. Two or three sittings.**
The cheapest-tier floor round (USD 10–15), the Gemini API smoke (USD 1), round two of stills for more draws per
cell (₹4,300), and Seedance only on the two briefs where every cheap route failed (USD 6). At the end, the map's
rules rest on four draws per cell instead of two, and on the tiers you actually intend to buy.

**P2 — Stop being the judge. ≈ USD 10–20 across attempts.**
Judge v2: a better prompt and a stronger model, measured against the verdicts you already gave (that comparison
set is free — it is already sealed). The bar is written down: agreement kappa 0.6 and false-accept below 10 %.
If v2 fails too, the honest answer is that a person must review every delivery, and that must be priced into the
product rather than wished away.

**P3 — Decide the fork: Stage B or straight to outcomes.**
Stage B (≈ USD 250) sweeps the surviving routes across conditions — better science, no new product knowledge.
Going straight to Stage C answers the business question sooner. **My recommendation: skip most of Stage B.** You
already have enough routing evidence to run a real brief end to end; what you do not have is a single measured
accepted outcome. Keep from Stage B only the identity and temporal checks that Stage C actually needs.

**P4 — Stage C: the first real outcomes. ≈ USD 150. This is the gate.**
Eight buyer-shaped briefs, two recipes each, two repeats, with the repair ladder (cheap route → reject → premium
route). Output: the first cost per accepted outcome, including re-draws. Settle HED-1 first so human time is
counted. **No public price should be quoted before this number exists.**

**P5 — Runtime v0. USD 0 in provider spend; the largest build.**
Turn the map into code: a deterministic lookup (no model in the loop) that takes a normalised request and returns
a route, a price and an acceptance contract; a repair loop; a Production IR captured from the recipes that were
accepted in P4. Until this exists, every order is hand-driven.

**P6 — The product surface. Build.**
Intake, delivery, the human review step made explicit and time-boxed, an order status, and a price list built on
the P4 numbers with a margin over cost per accepted outcome — not over cost per call.

**P7 — Commercial and legal. Must run in parallel with P5–P6.**
Provider terms for reselling generated output (fal, Google, Sarvam, ElevenLabs each differ); who owns the output;
what you promise about likeness and trademarks; the re-draw and refund policy; invoicing that reconciles with the
ledger. None of this exists in the repository today, and it is the kind of thing that stops a launch dead.

**P8 — Operations. Build.**
Keys off a single laptop and out of one home directory; billing alarms per provider (the fal balance ran out
twice mid-run); a plan for what happens when a provider changes a price or removes a model — the map goes stale
silently; and a decision about the evidence repository, which is already 2.3 GB, mostly base64 payloads inside
request files.

**P9 — Private pilot, then public.**
Three to five real buyers at a real price, running through P5/P6, with every outcome measured the same way as
Stage C. Public launch only when accepted-outcome rate and cost per accepted outcome hold on real customer work,
including real customer photographs.

**Rough shape of it:** P0–P2 is about a week and under USD 100. P3–P4 is another week and about USD 150. P5–P8 is
the real build and is measured in weeks of engineering, not in provider spend. Public rollout is not close, but
the expensive uncertainty — *do cheap routes actually produce work a person accepts* — has largely been bought
and answered.

---

## Part 8 — How to check this audit

Everything above is reproducible from a clean copy of `main` at `dcfa6af`:

* tests: `cd eval/harness-v2 && python3 -m unittest discover -s tests -p 'test_*.py'` → 326 tests, OK
* registry: `python3 eval/registry/validate_registry.py` → PASS, 575 rows
* rebuild rows: `python3 eval/harness-v2/registry_rows.py --run eval/experiments/EVAL-040/runs/vid-knee:vid-knee`
* rebuild the map: `python3 eval/harness-v2/evidence_map.py --results … --out /tmp/map.yaml` → 61 cells, identical
* rebuild the package: `MI_OUT=/tmp/pkg python3 eval/empirical-planning/STAGE-A-FREEZE-2026-09/tools/build.py`
* money: add `amount_usd_equiv` over every `type: spend` row in
  `eval/experiments/EVAL-040/runs/*/ledger/*/spend-ledger.jsonl`

**Where this file is:** `coordination/audits/AUDIT-2026-09-10-REPORT-B.md` in the main working copy
(`/Users/vaibhavchawla/Vaibhav_Personal_Projects/media-intelligence`). It is **uncommitted** and no pull request
was opened, as instructed. It does not touch the other auditor's report.
