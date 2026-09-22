# CUMINCO-CHOPSTICKS-003 — production-learning case

**What it is.** The first job run end to end through the `/media-agency` operator (PR #99): a spec video ad for Cumin Co.
(15 cm Ceramic Ramen Bowl) built from the brand's own chopsticks guide — two characters, three step inserts, a voice-over —
on credits-only routes (Nano Banana 2 with reference images, Veo 3.1 Fast i2v, Gemini TTS, Lyria). Opened 15 Sep 2026
13:17 UTC; three assembled versions; **all three rejected by the user**; closed 16 Sep. 50 paid attempts, **USD 5.0907**
reserved of an USD 8 cap; 10 human review cycles.

**Two conclusions, kept apart — and a third that matters more.**
Final quality: **FAILED** (V1 mix / mouths / text placement; V2 no ad structure; V3 voices overlapping).
Pipeline efficiency: **UNDERPERFORMED** (≈ 3 working hours, three versions, nothing accepted).
Process conformance: **CONFORMANT** — packet before spend, frozen copy, gated prompts, ledgered attempts, per-geometry QA, human gates —
and it still failed. The gates that existed passed on every version; every rejection landed on a dimension no gate measured.

**The core finding.** For the third case in a row the media models delivered (1 model failure reached the human; 5 pipeline/operator
failures did). This time the misses were named precisely: no gate for **VO overlap** (promoted here as `check_vo_schedule`), no gate for
**subject obstruction** under copy (candidate, implemented in the job tool), and no doctrine for **ad structure** reaching the job —
`commercial_communication` fired and is uncompiled while the ABCD rules sit in accepted Canon. That last one is a Canon gap for the
Controller, not something this case fixes.

| File | Answers |
|---|---|
| `OUTCOME.yaml` | rejected; why; what it is not evidence for |
| `HUMAN-VERDICTS.yaml` | the user's words, chat-only, per gate and per version |
| `REVISION-TRACE.yaml` | V1 → V2 → V3 with root-cause classes, repairs, cost |
| `TIME-AND-COST.yaml` | mechanical clocks, spend by route, voice-search spend, no CpAO |
| `SYSTEM-DEFECTS.yaml` | nine defects; tally 1 model / 5 pipeline reaching the human |
| `ROUTE-OBSERVATIONS.yaml` | six directional rows, exact n, `routing_authority: none` |
| `PROMOTION-QUEUE.yaml` | promoted: VO_SCHEDULE_GATE · candidates: obstruction gate, VO-first timeline, closed-mouth-under-VO, ad-structure minimum, plates per geometry, voice-by-ear-first · Canon gap: commercial_communication |
| `EVIDENCE-MAP.md` | every claim → path @ `de1f9783046d` + sha256 |

No `ACCEPTED-TEMPLATE.yaml`: nothing was accepted; `template_status: none`.

**Validate.** `python3 production-learning/tools/check_case.py --case production-learning/cases/CUMINCO-CHOPSTICKS-003 --source-ref de1f9783046d19f1c6dc5b92532c39f0bc008399 --source-dir agency/jobs/AGY-2026-09-15-CUMINCO-CHOPSTICKS-001`

**Raw evidence.** Branch `work/agency-job-cuminco-chopsticks-001` @ `de1f9783046d19f1c6dc5b92532c39f0bc008399` — job record, ledger, every attempt, every prompt, every plate, clip, voice take and assembled version. Never merged.
