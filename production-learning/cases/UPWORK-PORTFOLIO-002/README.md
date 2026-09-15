# UPWORK-PORTFOLIO-002 — production-learning case

**What it is.** The second complex real production after UPWORK-INTRO-001: a batch of portfolio tile media for the
Upwork profile, made on 15 Sep 2026 in about an hour after the intro film was accepted. Nine tiles were delivered and
handed over; one tile (real estate, "Nivaas Homes") was skipped after two rejected attempts. Eight paid generations,
USD 4.66 reserved (three quarters of it on the two rejected attempts), five human review cycles, thirteen human-flagged
defects.

**Two conclusions, kept apart — and a third that matters more.**
Final quality: **SUCCESS** for nine tiles, **FAIL** for the story tile.
Pipeline efficiency: **not measurable as TTAO** (chat-only acceptance; lower bound 1 h 07 m for the set).
Process conformance: **NON-CONFORMANT.**

**The core finding (Controller, 15 Sep).** Good final media can coexist with a non-conformant production process.
The batch bypassed the Media Intelligence workflow that had been built and merged the same day (PR #98): no
pre-spend packet, copy invented during execution, paid calls straight after a chat "go", ad-hoc acceptance checks,
pilot scripts instead of the runtime / media-agency path, no spend amendment, ledger lines appended to the film's
lineage. The consequence is the evidence: **all four V3 failure classes from case 001 — clipped text, unreadable
contrast, accidental crops, elements over the subject — came straight back on the first tile export**, plus two
audio failures the process had no check for. This is evidence for enforcing the workflow, not evidence that the
media models regressed.

| File | Answers |
|---|---|
| `OUTCOME.yaml` | partial acceptance of a batch (9 accepted, 1 skipped), the delivered index as identity, spend recomputed from the ledger (the chat figure of USD 3.9 was wrong) |
| `HUMAN-VERDICTS.yaml` | the Controller's words per version, chat-only; the 13 defects preserved individually (HD-01…HD-13) |
| `REVISION-TRACE.yaml` | B1 → B2 → N1 → N2 → B3 with root-cause classes, repairs, cost, elapsed |
| `TIME-AND-COST.yaml` | mechanical anchors (folder birth time, ledger UTC, commits), lower-bound outcome time, cost by route/version, CpAO with its missing components |
| `SYSTEM-DEFECTS.yaml` | nine process defects (PD-01…PD-09) and the thirteen human-flagged defects classified; the tally: 10 pipeline failures reached the Controller, 2 model failures |
| `ROUTE-OBSERVATIONS.yaml` | six directional observations, exact n, `routing_authority: none` |
| `PROMOTION-QUEUE.yaml` | promoted: QA_COVERAGE_ENFORCEMENT, FORMAT_SPECIFIC_REVALIDATION, PAID_PRODUCTION_PREFLIGHT, CROSS_CLIP_VOICE_CONTINUITY, REJECTED_DESIGN_REUSE · candidates: READABILITY_MARGIN, STACK_LEVEL_FIT, SUBJECT_AWARE_CROP_ANCHORING, SINGLE_VOICE_SOURCE, STILLS_FIRST, TEXT_OVER_IMAGERY_CONDITIONAL · not promoted: Canon, Registry, routing, re-promotion of existing gates, a universal margin, a subjective judge |
| `EVIDENCE-MAP.md` | every claim → path @ `b4b77fa` + sha256 on the archival branch; what is not on disk |

No `ACCEPTED-TEMPLATE.yaml`: `template_status: job_specific` — the tile layouts are compositions on accepted plates
and are not proposed as a reusable template.

**Raw evidence.** Branch `work/upwork-portfolio-samples-2026-09-15` (HEAD `b4b77fa`), a new archival branch built on
top of the case-001 pilot history; it preserves the paid generations, the ledger and asset records, the copy, the tools,
the delivered export folder (byte copy) and both rejected/held tile-7 attempts. The case-001 ref
`work/pilot-upwork-intro-video-v4` is unchanged at `f6ca66f`.

**Validate.** `python3 production-learning/tools/check_case.py --case production-learning/cases/UPWORK-PORTFOLIO-002
--source-ref work/upwork-portfolio-samples-2026-09-15 --source-dir pilots/upwork-intro-video-2026-09-14` (needs the
generic validator from PR #99; the pilot-bound validator on `main` at the time of writing does not take `--source-dir`).

## Acceptance learning

"Required words are present" is not "the advertisement communicates correctly". Nivaas v1 was accepted by the operator
on a transcript match while a 2.9-second hole sat inside the second sentence; Nivaas v2 was accepted clip-by-clip while
the assembly had two narrators. Both are **acceptance-process defects**, not evaluator-design questions: the check
measured presence, the buyer hears delivery. No universal subjective judge is proposed; human-perceived continuity
remains the release authority (PROMOTION-QUEUE `CROSS_CLIP_VOICE_CONTINUITY`).

## Complex-production event

`COMPLEX_PRODUCTION_EVENT trigger condition: MET.` This is the second complex real production; the Controller deferred a
richer event schema until exactly this point. `OUTCOME-EVENT-v1` is **not** modified in this PR. Recommendation to the
Controller: a separate USD-0 design task, from cases 001 + 002 together, for a schema that can represent multi-asset
batches; per-asset routes; a shared commercial brief; versions/attempts; accepted and rejected assets in one production;
shared spend authority; assembly relationships; cross-asset QA (voice consistency); partial acceptance / skipped
deliverables; job-level TTAO/CpAO plus asset-level attempts.

## What this case is not evidence for

Capability Registry, Alpha-1, Canon effectiveness, Stage A/B/C, any routing rule, or CpAO completeness (triage calls and
vendor bills unreconciled).
