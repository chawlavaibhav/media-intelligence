# P1 v2 — amendment 1 (founder decisions, 2026-09-23)

Applies to branch `claude/p1-v2-build` (PR #109) after its checklist was filled in. Same rules as the build spec §0: no spend,
no cloud changes, no merge, test first, simulated mode only, the builder is never the operator. Report back by adding an
"Amendment 1" section to `P1-V2-FOUNDER-CHECKLIST.md` with Done / Partly / Not done and evidence for each item below.

## 1. Cost targets (founder: agreed)

- Film AI reasoning target stays **≤ USD 0.30**.
- Image AI reasoning target becomes **≤ USD 0.08** (was 0.03). For **image jobs only**, the chef uses a cheaper model than
  the strongest one (configurable `MI_MODEL_CHEF_IMAGE`, default a mid-tier model from the same company as the film chef, so
  judge independence still holds). Film jobs keep the strongest chef.
- One recipe may produce a **set of images** (several formats/variants from one plan); the quote shows the reasoning cost
  shared across the set.
- The cost report shows both targets and whether they are met.

## 2. Judges are tested on old jobs (founder: "test with old jobs")

The private evidence repo now holds `historical/CASES.yaml` (commit `1212814` of `chawlavaibhav/mi-p1-evidence`): 14 films and
62 images the founder already judged, each hash-verified against `production-learning/cases/<case>/`:
Cumin Co. chopsticks V1–V3 (reject), Mokobara Odyssey 007 v1 (repair) and v2 (accept), RentOK A, B, V2 (accept), Upwork intro
V1 (repair), V2 (rebuild), V3 (reject), V4 (repair), V4.1 (accept), Nivaas story + tiles (reject), 57 accepted portfolio tiles.

- Add these to `product/qualification/JUDGE-CASES.yaml` for the **big taster** (films and images), reading from the evidence
  repo like the existing cases. Verdict mapping: accept → pass; specific_repair → fix; rebuild_direction / reject → fail.
- Where an old job's plan (board / direction) is on its job branch, add it as a **recipe checker** case with the job's final
  verdict as the known outcome. List any job whose plan is missing.
- Keep the set balanced when scoring: report agreement separately for accepted and not-accepted cases (57 accepted images
  must not swamp the result).
- Pass marks stay as proposed in `PASS-MARKS.yaml`; mark them `confirmed_by_founder: 2026-09-23`.
- The live qualification run itself stays **not run** until the founder gives a spend cap.

## 3. Nobody waits for the founder (founder: "I can't be there all the time… let the user take the call or the system")

The founder is no longer a required step in any job. Every place a job currently waits for the founder becomes a decision
by **the customer** (the person who sent the order — during testing, whoever is testing) or by **the system**, using the rule
below. Founder overrides stay available, founder-only, but are never required.

| Where the job waits today | New owner | Rule |
|---|---|---|
| Plan confirmation after the recipe checker | **Customer** | The existing plan-approval page (station 6) is the decision. An unqualified recipe checker's "approve" is shown to the customer as "our reviewer found no problems"; its "send back" still sends the recipe back. |
| Recipe checker sends back twice | **System, then customer** | The system takes the pantry checker's safest allowed alternative for the problem shots and re-plans once; if still sent back, the customer sees the plan with the reviewer's objections in plain words and chooses: go ahead, change the brief, or stop (USD 0 spent so far). |
| Riskiest shot fails after its re-plan | **System** | That shot switches to route FILM-A (approved still + code motion). The customer's preview notes it. The job continues. |
| Master plate approval | **Customer** | Unchanged in shape — the customer approves the look of the film. |
| Big taster says **fix** | **System** | Repair automatically, only the named shots, within the budget the customer already approved, at most 2 rounds (spec §6.2 limits). No extra spend beyond the approved budget. |
| Big taster says **fail**, or repairs are used up | **Customer** | The customer sees the film with the plain check report and chooses: accept as is, request changes (priced), or reject. |
| Unqualified big taster says **pass** | **Customer** | The customer's preview is the final check (station 11). No founder confirmation. |
| Door guard block from a measured FAIL | **System** | Still blocks (a measured defect never ships). Routes back to repair as above; if it cannot be fixed within budget, the customer is told what failed and chooses to stop or pay for a rework. |

Tests to add: each row above in simulation, including "no job ever enters a founder-only wait unless a founder chose to
intervene", and "automatic repair never exceeds the approved budget".

## 4. Learning is automated (founder: "learning has to be automated. I can't approve it every time")

Replace the lesson approval queue with automatic application inside guardrails:

| Lesson kind | Applied |
|---|---|
| Makes the kitchen **more careful** (equipment sheet → risky/cannot, a new failure-diary entry, a stricter check) | **Automatically, immediately.** |
| Makes the kitchen **bolder** (equipment sheet → reliable, a check relaxed) | Automatically once **≥ 2 accepted jobs** support it. |
| **One customer's taste** or brand fact | Automatically, **on that customer's shelf only**; never global. |
| **Rulebook card / KRA wording** | Automatically, as a new card version; the next 5 jobs are **watched**. If customer acceptance drops or blocking checks rise versus the previous 5, the change is **rolled back automatically** and the rollback is recorded. |
| **Money limits, budgets, spend caps, who may override, safety rules** | **Never** automatically. Founder only. |

- Every applied lesson is logged with the job that taught it, the evidence, and the before/after.
- The founder gets a **weekly digest** page (operator view): what was learned, from which job, with an **undo** per item. Undo
  restores the previous version and records who undid it.
- Tests: each row above; rollback triggers on a simulated drop; undo restores the exact previous version; a money/override
  lesson is refused.

## 5. Not now (founder: "will fix later")

The cheap workers default to Claude Haiku 4.5, and the Anthropic key on this Mac is invalid. Leave the configuration as it is,
but add one line to the checklist's open items: *live runs will fail at the first cheap-worker call until a valid Anthropic
key is supplied or those workers are pointed at another provider (`MI_MODEL_<WORKER>`)*.

## 6. Also noted by the independent check (no action unless trivial)

- The founder account must be created and held only by the founder; builders and scripts must never create it or store its
  password (the v1 builder held the operator login). Add this to `deploy/RUNBOOK-P1.md`.
- Full suite re-run independently on 2026-09-23: 105 tests, OK, 1 skipped with the evidence repo connected (commit 4359d5a).
