# Morning brief — Capability Lab overnight build, 5 September 2026

**For:** Vaibhav (Controller). **From:** the Writer Controller session that ran overnight.
**Money spent overnight: USD 0. Cloud resources created: none. Files deleted or overwritten: none.**
Everything is on draft PR #87 (`controller/capability-lab-direction-2026-09-05`). `main` is unchanged
at `599ff4a`; the CANON-GATE-001 branch has not merged (idle since 01:19), so `CONTROL-STATE.md`
was not touched.

## What was built, in plain English

Three tracks, each through the five roles you asked for (planner → executor → tester → auditor →
approver), one agent at a time, with this session reviewing between roles.

| Track | What it is | Verdict |
|---|---|---|
| **A — the test cases** | 35 test cases written the way real Indian buyers write to a studio (WhatsApp / email; Hindi in Devanagari, Hinglish, Indian English; 57 % Hindi or Hinglish), each mapped to a Normalized Request, each with one frozen Canon production blueprint that every model executes identically, blind accept/reject contracts, coverage matrix, elimination rules, seed policy, evaluator plan, cost table, irreducibility argument, and a generator that rebuilds the whole package byte-for-byte | PASS WITH NOTES |
| **B — prices, access, projections** | 35 current routes with 36 vendor pages pinned as bytes; read-only checks of what AWS, Google Cloud, Azure (getaight), fal and Sarvam can reach today; the Media Factory learnings imported as dated priors; a deterministic cost projection by tranche and by pool; ten morning decisions written out with defaults | PASS WITH NOTES |
| **C — the harness** | Adapters for every route (fal, Vertex, Sarvam), seven deterministic instruments, the free geometry-evaluator qualification run, and a dry-run manifest that prices all round-one calls without sending any. 140 tests, run with the network deliberately blocked. It refuses every dispatch unless a signed authorisation file exists, and that file is never committed | PASS WITH NOTES |

### Track C, in plain English (added ~07:55 IST)

- The harness cannot spend by accident. Without your signed authorisation file every one of the 47
  routes refuses to dispatch; with it, the ceiling is whatever you sign, checked against the exact
  roster version, across cash, credits and rupees together, with zero retries. Every failed or
  ambiguous call is written down and charged conservatively.
- The free geometry-evaluator qualification ran honestly: two capabilities qualified pending your
  ratification, one left undecided because a colour tolerance was never frozen, and one
  (`object_count`) **disqualified** because the fixture pack's overlapping-circle trap caught it.
  Nothing entered the Registry.
- Every instrument threshold is a **proposal** in `PASS-CRITERIA-v0.yaml`; until you freeze them
  the instruments report "criterion not frozen" and cannot create a Registry row.
- Conditions before the first paid call (C1–C7 in `eval/tasks/EVAL-039C-APPROVER-VERDICT.md`): sign
  and materialise the authorisation file; freeze the thresholds; ratify the Q1 result; choose the
  Vertex credential file (defaults to the Aight service account until MD-9 creates the new one);
  rule on two small pricing readings (FLUX edit add-on, Omni 15-second clips); make the very first
  live call a single cheap image.
- Note for the record: vendor pages pinned earlier contained the vendors' own public site-config
  tokens; they were replaced by schema extracts in the tree, but remain in one earlier commit. The
  auditor judged them public material and recommended no history rewrite; you may disagree.

## The numbers you are being asked to approve

Round one is 288 calls (+32 only if you enable the Azure / Bedrock routes), nominal **USD 156.46**:
cash on fal **USD 115.45**, Google Cloud credits **USD 41.01**, Sarvam credits **₹0.80**. Proposed
hard caps: 1a USD 85, 1b USD 115, total USD 200 across both pools. The minimum viable round
(images + text-to-video + image-to-video only) is about USD 74.

What each round establishes, when eliminations happen, and how this reaches the Registry without
weakening it are in `coordination/plans/2026-09-05-CAPABILITY-LAB-CAMPAIGN-v1.md` §C–§F.

## What needs you, and only you

1. **Ratify or amend the direction** — `coordination/decisions/CONTROLLER-CAPABILITY-LAB-DIRECTION-2026-09-05.md`.
   Methodology is still open; nothing there is binding until you say so.
2. **Sign the spend record** — `coordination/decisions/DRAFT-SPEND-AUTHORISATION-TRANCHE-1-2026-09-05.md`
   §6, in your own words. Its §5 lists 18 small decisions with defaults; "approve with defaults" is a
   valid answer.
3. **Create the fresh cloud resources yourself** — the agents' identities were too weak (AWS cannot
   create IAM users; the Google service account cannot list services), and the permission classifier
   blocked the agent that would have created keys. Exact commands, undo commands and the key-file
   layout are in `eval/empirical-planning/MORNING-DECISIONS.md` **MD-9**. Azure = getaight
   subscription `b832f4a1…` only; the command-line default is the Wherehouse subscription and must
   never be used.
4. **Tell us the credit balances** on the three clouds (MD-1) so cash versus credits is real.
5. Optional: photos of your own for the edit / reference / compose cases (C1 in the spend record).

## Things you should know before approving

- Veo is priced per second by assumption; Google's page says "per 1 count". The assumption errs
  high, so it cannot breach a cap; the first metered bill confirms it.
- Judging is your time: about 312 minutes of blind accept / reject across round one, images first.
- The two-speaker dialogue "voice-over plus lip-sync" arm is written down but not run: no available
  lip-sync engine can be told which face is speaking. Native two-speaker routes are tested instead.
- Three routes are unpinned and outside the cap (gpt-image-2 edit, sync.so lip-sync v3, Veo Lite
  image-to-video). They can be pinned and added, or left for Stage B.
- Imagen 4 is retired on Vertex and Amazon Nova ends this month; both are dropped. Sora 2 and
  MAI-Image-2.6 exist on Azure but only after you deploy them.
- 4K is deferred to Stage B on purpose; longer clips, two speakers and music are in round one.

## What happens the moment you approve

1. You run MD-9 (fresh resources and keys) or tell us to run on the existing identities.
2. The spend record is committed with your words; EVAL-040 starts with the **image lane only**
   (about USD 10), you judge blind in one sitting, the winning still becomes the plate for every
   image-to-video route, and the rest of 1a follows.
3. Deterministic instruments write the first Registry rows from round one; your acceptances go into
   the Capability Map as product evidence; nothing human-judged enters the Registry.

## Record of the night

Commits on the PR branch, in order: direction decision and plan (3 commits), cloud survey, planner
tasks 039A / 039B / 039C, executor outputs, tester reports, auditor reports, executor corrections,
approver verdicts. Every agent report separates OBSERVED from INFERRED and lists what it could not
do. The five-role pipeline caught real problems: a false "Sarvam key empty" finding, a lip-sync
price pinned on the wrong endpoint, a square still being fed into vertical video, contract
statements that would have leaked the route to the blind judge, and eight requests where the test
had crept into the buyer's words. All were fixed and re-verified.
