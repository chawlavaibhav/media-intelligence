# PROPOSED — EVAL-037 evidence annotations and spend reconciliation (drafts for a Writer-Controller session)

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

**What this is.** The exact proposed sentences (A1–A6) that a Writer-Controller-authorised session
would apply to `eval/experiments/EVAL-037/CONCLUSION.md`, `PROJECT-MEMORY.md` and
`coordination/CONTROL-STATE.md`, plus a spend-reconciliation draft. These are PROPOSALS ONLY: this
worker does not touch `eval/`, `coordination/` or `PROJECT-MEMORY.md`, and nothing here rewrites
historical text — annotation/supersession only, per frozen decision 5. Every annotation carries a
target file:line anchor and a runnable read-only recompute command; each command exits 0 in this
repository (the `origin/work/eval-037-*` refs are already fetched locally — no network). Gaps
addressed: GAP-06, GAP-17.

---

## The six annotations

### A1 — the read-count artifact

**Target:** `eval/experiments/EVAL-037/CONCLUSION.md:99` (insert immediately after line 99, "The
model saturated search but nearly ignored object reads.")

**Proposed text (verbatim):**

> ANNOTATION 2026-08-31: canon_search results embed each item's full content
> (tools/canon_tools.py _stamp), so a follow-up canon_read added no information; the low read
> count is a property of the interface, not evidence about model consumption behaviour.

**RECOMPUTE:**

```bash
sed -n '414,427p' eval/experiments/EVAL-037/tools/canon_tools.py | grep -q '"item": item' && sed -n '353,357p' eval/experiments/EVAL-037/tools/canon_tools.py | grep -q 'dict(entry)' && echo 'A1 OK: _stamp embeds the full raw item in every search envelope'
```

### A2 — Sonnet-only comparisons under a HOLD-majority diet

**Target:** `eval/experiments/EVAL-037/CONCLUSION.md:51` (insert immediately after line 51, the
accepted "Canon helps" conclusion block; the supporting claims run through line 66).

**Proposed text (verbatim):**

> ANNOTATION: the supporting comparisons are Sonnet-only — no weak-model lane ever consumed Canon
> at scale (Gemma FULL_CANON 0/18, Haiku FULL_CANON 3/18 trials) — and 53.4% of objects exposed
> to the winning lane were HOLD, not accepted Canon. This conclusion says nothing about Canon's
> value to a weak model or about an accepted-only treatment.

**RECOMPUTE:**

```bash
python3 -c "import json,subprocess; g=lambda p: json.loads(subprocess.run(['git','show',p],capture_output=True,text=True,check=True).stdout); d=g('origin/work/eval-037-sonnet-controlled-canon:eval/experiments/EVAL-037/runs/sonnet-controlled-canon/result.json'); a=sum(t['canon_items_returned']['accepted'] for t in d['trials']); h=sum(t['canon_items_returned']['hold'] for t in d['trials']); assert round(h/(a+h),4)==0.5341,(a,h); gm=g('origin/work/eval-037-gemma-full-canon:eval/experiments/EVAL-037/runs/gemma-full-canon/result.json'); hk=g('origin/work/eval-037-haiku-full-canon:eval/experiments/EVAL-037/runs/haiku-full-canon/result.json'); assert sum(1 for t in gm['trials'] if t.get('canon_used'))==0; assert sum(1 for t in hk['trials'] if t.get('canon_used'))==3; print('A2 OK: HOLD 227/425 = 53.41%; Gemma FULL_CANON 0/18; Haiku FULL_CANON 3/18')"
```

### A3 — judging uncommitted and treatment blindness structurally impossible

**Target:** `eval/experiments/EVAL-037/CONCLUSION.md:45` (annotate line 45, "Judging was blind to
model/treatment identity…").

**Proposed text (verbatim):**

> ANNOTATION: no judging artifacts (verdicts, rankings, blinding key, judge identities) are
> committed anywhere in the repository, and Canon-condition packages disclose their treatment in
> KNOWLEDGE_AND_WEBSITE_USE, so blindness to treatment was not structurally possible at package
> level.

**RECOMPUTE:**

```bash
git show origin/work/eval-037-sonnet-controlled-canon:eval/experiments/EVAL-037/runs/sonnet-controlled-canon/packages/E037SCC-sonnet-B01-R1.txt | sed -n '98p' | grep -q 'Canon knowledge used' && test -z "$(git for-each-ref --format='%(refname:short)' 'refs/remotes/origin/work/eval-037-*' | while read b; do git ls-tree -r --name-only "$b" | grep -iE 'EVAL-037/.*(judging|verdict|blinding)'; done)" && echo 'A3 OK: package line 98 discloses treatment; no judging/verdict/blinding artifact under EVAL-037/ on any fetched eval-037 ref'
```

### A4 — PROJECT-MEMORY carries the unestablished half as settled

**Target:** `PROJECT-MEMORY.md:132` (the EVAL-037 bullet accepting "Canon helps, but current
retrieval/consumption is not mature").

**Proposed text (verbatim):**

> Note: the 'Canon helps' half rests on judgments not committed to the repository, of Sonnet-only
> comparisons under a HOLD-majority information diet; committed evidence establishes the
> retrieval-immaturity half only.

**RECOMPUTE:**

```bash
sed -n '132p' PROJECT-MEMORY.md | grep -q 'Canon helps' && echo 'A4 OK: PROJECT-MEMORY.md:132 carries the Canon-helps acceptance verbatim'
```

### A5 — spend table missing EVAL-037 and PILOT-001 rows

**Target:** `coordination/CONTROL-STATE.md:120` (the "Spend authority" table, lines 114–125;
insert rows after the EVAL-030 row at line 120).

**Proposed text (verbatim):**

> EVAL-037 recorded lane spend: USD 8.372931 across committed lane results (Anthropic lanes only;
> Gemma unpriced; 16 overflow trials' turns unrecorded — true spend higher); PILOT-001: USD 1.60
> provisional. Neither is covered by the EMP-001 ceiling; no committed decision authorises
> EVAL-037 spend.

**RECOMPUTE:**

```bash
python3 -c "import json,subprocess; g=lambda l: json.loads(subprocess.run(['git','show','origin/work/eval-037-%s:eval/experiments/EVAL-037/runs/%s/result.json'%(l,l)],capture_output=True,text=True,check=True).stdout)['lane_calculated_cost_usd']; t=g('sonnet-no-canon')+g('sonnet-controlled-canon')+g('haiku-full-canon')+g('haiku-no-canon')+json.load(open('eval/experiments/EVAL-037/runs/sonnet-full-canon-repair-001/result.json'))['lane_calculated_cost_usd']+0.412806; assert round(t,6)==8.372931, t; print('A5 OK: recorded EVAL-037 lane spend recomputes to USD 8.372931 exactly')"
```

(The `0.412806` term is the original sonnet-full-canon lane's reported cost, committed at
`eval/experiments/EVAL-037/runs/sonnet-full-canon-repair-001/REPAIR-RUN.md:46`.)

### A6 — value gate listed "Concluded" but never executed

**Target:** `coordination/CONTROL-STATE.md:58` (the "Canon value gate / EVAL-037 — Concluded for
programme direction" row).

**Proposed text (verbatim):**

> The value-gate oracle-context experiment (canon/experiments/v1/value-gate/, C3) was never
> executed — 0 model calls, blocker FRESH_CONTROL_SESSION_REQUIRED standing — and EVAL-037 did
> not test hand-selected Canon; the best-case oracle question remains open.

**RECOMPUTE:**

```bash
head -6 canon/experiments/v1/value-gate/PROTOCOL.md | grep -q 'NOT EXECUTED' && test ! -e canon/experiments/v1/value-gate/generic-contexts-real && sed -n '58p' coordination/CONTROL-STATE.md | grep -q 'Concluded' && echo 'A6 OK: PROTOCOL says NOT EXECUTED, generic-contexts-real absent, CONTROL-STATE row 58 says Concluded'
```

---

## Sol asymmetry (one line, same Writer-Controller pass)

Proposed for `eval/experiments/EVAL-037/CONCLUSION.md` (the lane roster): "The two gpt-5.6-sol
lanes (36 of the 144 frozen trials) were never dispatched; the reason is unrecorded." Recompute:
`test -z "$(git ls-tree -r --name-only origin/work/eval-037-sol-no-canon | grep 'EVAL-037/runs')" && echo 'sol: no runs committed'`.

---

## Spend reconciliation draft (proposal — requires Controller attestation of chat-side approvals)

All figures are committed bytes except where flagged UNKNOWN. Recompute for each row is stated in
the right column; the EVAL-037 subtotal recomputes exactly via the A5 command above.

| Item | USD | Basis / recompute |
|---|---|---|
| EMP-001 cumulative through EVAL-024 | 2.6397905 | `history/EMP-001.md:113-123`; 1.7357905 + 0.904 (16 generation records: 8×0.053 + 8×0.060) |
| EMP-001 EVAL-030 evaluator stage | 0.024 | sealed scoring evidence; 16 rows sum to 0.0240 |
| PILOT-001 (2 Veo attempts × 0.80) | 1.60 provisional | `eval/pilot-001/evidence/records/provider-attempt-00{1,2}-cost.json`; modelled estimate at USD 0.10/generated second, NOT invoice evidence |
| EVAL-037 sonnet-no-canon | 1.138812 | `git show origin/work/eval-037-sonnet-no-canon:eval/experiments/EVAL-037/runs/sonnet-no-canon/result.json` → `lane_calculated_cost_usd` |
| EVAL-037 sonnet-controlled-canon | 2.861148 | same pattern, its branch |
| EVAL-037 haiku-full-canon | 0.400029 | same pattern, its branch |
| EVAL-037 haiku-no-canon | 0.331358 | same pattern, its branch |
| EVAL-037 sonnet-full-canon-repair-001 | 3.228778 | `eval/experiments/EVAL-037/runs/sonnet-full-canon-repair-001/result.json` (in-tree) |
| EVAL-037 original sonnet-full-canon | 0.412806 | `…/sonnet-full-canon-repair-001/REPAIR-RUN.md:46` |
| **EVAL-037 recorded subtotal** | **8.372931** | 1.138812 + 2.861148 + 0.400029 + 0.331358 + 3.228778 + 0.412806 = 8.372931 exactly |
| **Recorded grand total** | **12.6367215** | 2.6397905 + 0.024 + 1.60 + 8.372931 |

**UNKNOWN flags (explicit, per the reconciliation's own honesty rule):**

- UNKNOWN: both Gemma lanes' usage — "price not established for gemma-4-31b-it at freeze time";
  no USD figure exists to add.
- UNKNOWN: the 16 context-overflow trials of the original sonnet-full-canon lane — billed turns
  unrecorded; the repair lane's own `REPAIR-RUN.md` states real lane spend is materially higher.
  The EVAL-037 subtotal is therefore a floor, not a total.
- UNKNOWN: whether any chat-side user approval covered EVAL-037 spend. No committed decision
  authorises it (`grep -rl 'EVAL-037' coordination/decisions/` returns only the conclusion
  record); the 29-Aug reset decision required naming exact model, call count and maximum cost
  before spend. Closing this row needs a retroactive Controller statement — either an attestation
  of the approval or a record of its absence.

**Proposed disposition (not executed here):** the two missing rows (EVAL-037 ≥ 8.372931,
PILOT-001 1.60 provisional) enter `coordination/CONTROL-STATE.md`'s spend table via A5, and this
reconciliation is committed as a Controller record extending GOV-006 G6-02 (no consolidated total
exists anywhere today).
