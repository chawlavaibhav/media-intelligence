# Decisions waiting for the Controller — 10 September 2026

Both audits end in the same place: a short list of things **only you** can decide. This sheet puts
them on one page. Nothing here has been decided by anyone else. Write your answer on the line, and a
worker will turn each answered item into a proper record under `coordination/decisions/`.

Free decisions first. Nothing on this page costs money to *decide*.

---

## Group 1 — close the audit (all USD 0)

**C-1. The two cap crossings.** Video piece 1 consumed USD 10.364 against a USD 9.96 cap; the Wan 2
round consumed USD 11.840 against its final USD 11.53 cap. Both are real; neither could have been
caught, because the cap was enforced inside one run folder while the authorisation covered three or
four runs. That mechanism is now repaired.
*Option A:* accept both as recorded, note the mechanism is fixed, move on.
*Option B:* annul them and re-issue the authorisations at the true amounts.
Consequence either way: no evidence changes; only the governance record changes.
**Your ruling: ______________________**

**C-2. Ledger versus vendor billing.** The ledger counts money the moment a request may have left the
machine. USD 10.11 of it produced nothing at all, and at least USD 2.88 of that your own Wan 2 record
says was never charged. So the project has an upper bound on its costs, not its costs.
*Decide:* who reads the four statements (fal, Google Cloud, Sarvam, ElevenLabs) for 8–10 September,
and whether a cap in future is measured against the ledger or against the bill.
**Your ruling: ______________________**

**C-3. The elimination rule.** Three runs counted provider balance locks and request-shape faults
*outside* the denominator, which the frozen rules do not allow ("nothing is changed mid-run"). One
route's survival depends on which reading you take, and the routing map's own wording disagrees with
its results file on that route.
*Option A:* rule that infrastructure faults never count, and amend the frozen rules by a new task,
then regenerate the affected numbers.
*Option B:* apply the frozen rule literally and let the recomputed numbers stand.
See `AUDIT-2026-09-10-EVIDENCE-RECOMPUTE.md` for exactly what changes under each.
**Your ruling: ______________________**

**C-4. The tainted human-acceptance cells.** Auditor A proposes this exact wording, and Auditor B
agrees with it: *any Stage-A human-routing cell affected by duplicated dispatched trial identities,
smoke-as-extra-draw, or infrastructure exclusions contrary to E1/E2 is descriptive product-learning
evidence only, until recomputed or cleanly replaced. Deterministic Registry evidence is untouched.*
*Decide:* adopt that sentence as a ruling, yes or no. It costs nothing and it stops contaminated
numbers becoming production truth without throwing away useful work.
**Your ruling: ______________________**

**C-5. WITHDRAWN — there was no judge breach.** Both auditors reported the judge as having made 206
calls against a 200-call authority. Both were wrong: `calls: 206` is a *row* count written by an
offline rebuild, and only 190 of the 210 screened rows carry any evidence of a call at all (the rest
are audio trials, decided without sending anything). At most 190 calls were sent against 200. Nothing
to rule. The "not qualified" verdict stands on its own merits — agreement kappa 0.33, false-accept
22 %. *The real defect was that a live screening run kept no authoritative counter, so a rebuild could
substitute a different number unnoticed; that is fixed on the repair branch.*

**C-5b. The one call limit that WAS exceeded.** The stand-in picture run made 19 paid calls where the
record authorised "≤ 16". Money stayed inside the cap. Same ruling shape as C-1: accept as recorded,
or annul.
**Your ruling: ______________________**

**C-6. State of record.** `PROJECT-MEMORY.md` — the file every new session is told to read first —
said the Registry was empty. Three factual corrections are applied on this branch, but the file still
predates the whole two-day run. *Decide:* order a full Governor refresh now, or after C-1…C-5 are
ruled.
**Your ruling: ______________________**

**C-6a. What an amendment does to a cap — found while repairing the ledger.** The signed
authorisation files are **edited in place** when you raise a cap, so the file's fingerprint changes.
The repaired ledger pools spend by that fingerprint, which means an amendment starts a fresh pool.
Replaying the real ledgers through the new code: video piece 1 is caught completely (the call that
would cross USD 9.96 is refused, and the 0.404 overrun never happens); Wan 2 is caught only for the
first half (8.480 against 8.39, refused) because the later runs sit under the amended file's new
fingerprint.
*Option A — an amendment starts a new budget:* simple, matches how the files are written today, but a
cap raised in place forgets what was already spent.
*Option B — an amendment keeps one budget for the whole piece:* closes the Wan 2 gap completely. The
change is one line, already located and documented in the code; it was deliberately not made, because
"a raised cap re-uses the old spend" is your policy call, not an executor's.
**Your ruling: ______________________**

**C-6b. How a re-sent draw counts — the one ruling that moves a routing rule.** Six Wan 2
image-to-video draws failed with HTTP 422 in one run and the same trial identities were sent again in
a second run whose plan records no link to the first (`vid-wan2-i2v/PLAN.yaml:36`).
*Option A — a failed draw stays a failure:* Wan 2.2 A14B is out of image-to-video on both elimination
rules (2 accepts of 8, six failures), and **RR-16 cannot stand as written** — "Wan 2.2 A14B replaces
Wan 3.0 Prime as the cheap Wan tier for image-to-video" would have to be withdrawn.
*Option B — the last sending counts:* it is 7 of 8 and RR-16 stands.
Nothing else in either audit swings a routing rule's substance this way. Note the routing map currently
runs three different denominators at once — 8 for one question, 14 for this one, 2 for another — so
this ruling also has to say which convention the map uses everywhere.
**Your ruling: ______________________**

**C-6c. The exact-text cell collision — this one touches the production wedge directly.** The four
composite trials carry two different Controller verdicts (3 rejects + 1 accept when the bare textless
plate was judged; 4 accepts when the same plate with code-set text was judged), and the routing map
holds them as two cells with **the same route key and the same arm**
(`ROUTING-EVIDENCE-MAP-v0.yaml:3629` and `:3784`). RR-1's headline "4/4 accepted" — the rule the first
production wedge is built on — rests on the second cell. The *mechanism* is sound: the composited
outputs were sealed as their own artifacts and accepted 4/4. What is not sound is a router matching on
route key plus arm, which would get an ambiguous answer, and a reader taking "4/4" to mean the image
model produced correct text. It did not; code did.
*Decide:* re-key these two cells distinctly before any router reads the map, and re-word RR-1's
evidence line so it says what was actually accepted.
**Your ruling: ______________________**

**C-6d. Is a route thrown out per question, or per case? (found by the taint register; no earlier
item covered it.)** The frozen rules say elimination is per (route, question) — rule E4. Two runs
applied it per (route, *case*) instead, which is a different and stricter test when a question holds
several cases. C-3 settles the denominator; it does not settle the scope. Two cells
(AUD-TTS/elevenlabs-v3-direct and VID-REF/veo-3.1-fast-ref2v) sit blocked on this alone.
*Option A:* per question, as E4 says — apply it everywhere and recompute those two.
*Option B:* per case where a question mixes clearly different jobs — but then E4 must be amended by a
new task, not by a run file.
**Your ruling: ______________________**

---

## Group 2 — where the project goes next (USD 0 to decide)

**C-7. The first launch use case.** Freeze the first job family you will actually sell. Without this,
"more testing" has no stopping rule. Both audits name this as the decision that unblocks everything
downstream.
**Your ruling: ______________________**

**C-8. Human release policy for the first alpha.** Every output gets your approval before it leaves,
yes or no. Auditor A recommends yes; Auditor B agrees, because the automatic judge agrees with you
only two-thirds of the time and wrongly accepts 22 % of what you reject.
**Your ruling: ______________________**

**C-9. Stop widening the Lab.** Both audits recommend: do not benchmark more premium models, do not
compile the remaining eight Canon packs, do not chase a perfect judge, do not expand every two-draw
cell for neatness. Build the smallest complete production path instead.
**Your ruling: ______________________**

**C-10. Canon.** Authorise Injection v1 and the template/empirical-memory work only; defer the other
eight packs until a real runtime failure demands one. Build cost USD 0.
**Your ruling: ______________________**

**C-11. The public-release bar.** Adopt Auditor A's T8 condition list (twelve conditions) as the
formal gate for public delivery.
**Your ruling: ______________________**

---

## Group 3 — the ones that cost money (decide the order, then size each separately)

Nothing below is authorised by this sheet. Each needs its own spend record, before dispatch, in
writing — not in chat.

| # | Item | Rough size | Why |
|---|---|---|---|
| C-12 | Cheapest-tier floor round (Wan / Kling cheapest live tiers) | ≈ USD 10–15 | Closes the tier gap you caught yourself: "havent we failed the very principle". |
| C-13 | One Gemini API smoke for the two recommended still routes | ≈ USD 1 | Those routes are now priced on a surface that has never carried a single call. |
| C-14 | Judge v2 | ≈ USD 3–5 per attempt | Or decide it stays human — see C-8. |
| C-15 | Clean re-runs of only the tainted cells that will route launch traffic | single digits to low tens | Only after C-3, C-4 and C-7 tell us which cells matter. |
| C-16 | Round two of stills, more draws per cell | ≈ ₹4,300 | Turns "directional" into "reliable". Both audits say do this narrowly, not everywhere. |
| C-17 | Stage B on launch-critical routes only | tens of USD | Only after the first vertical slice names the routes. |
| C-18 | **Stage C — accepted outcomes and cost per accepted outcome** | size after C-17 | The one experiment worth spending on. It answers whether the whole system beats a simpler workflow. Settle HED-1 first. |

**Order you want: ______________________**
