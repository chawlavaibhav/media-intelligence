# Elimination rules — pre-registered before any call (Stage A)

E1–E5 are copied byte-for-byte from `coordination/plans/2026-09-05-CAPABILITY-LAB-CAMPAIGN-v1.md` §C.4:

- E1 — refusal or hard error on ≥ 3 of 8 core trials → eliminated for that question (recorded as refusal-prone; may still be a fallback elsewhere).
- E2 — blind acceptance ≤ 2 of 8 → eliminated for that question.
- E3 — among survivors, the top 3 by acceptance (tie-break: lower trial cost) advance to Stage B.
- E4 — elimination is per (route, question); a route dropped on one question can advance on another.
- E5 — deterministic failures (format, baked text on a no-text item) count as rejects, never as exclusions.

**Survivor cap:** at most 3 routes per question advance to Stage B (E3).

**Proportional rule for routes with fewer core trials (stated before any call):** Seedance 2.5 runs 2 core items × 2 repeats = 4 core trials instead of 8. It is eliminated on the same *proportions*: E1 refusal/hard error on ≥ 3/8 → ≥ 37.5 % (so ≥ 2 of 4); E2 blind acceptance ≤ 2/8 → ≤ 25 % (so ≤ 1 of 4). No threshold is rounded in Seedance's favour.

**E5 in this package:** the deterministic pre-checks named at the end of every acceptance contract (format probe, baked-text scan on no-text items, duration/aspect mismatch) are rejects, never exclusions. A refusal or error is counted under E1 and is also a reject for E2's denominator.

Elimination is per (route, question) (E4); a route dropped on one question can advance on another. Nothing here is changed mid-run; a change is a new task.
