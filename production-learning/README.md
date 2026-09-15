# production-learning/

Durable product learning from **real productions** — accepted or rejected commercial work executed for a
purpose outside the Lab. It is neither `eval/` (Capability Lab evidence: sealed, Registry-feeding) nor
`runtime/store/outcomes/` (OUTCOME-EVENT-v1 events written by the runtime loop for the narrow Alpha chain).
A case here never creates a Registry row, never edits Canon, and never claims routing authority; it records
what happened, what the human judged, what the system got wrong, and what is promoted as a deterministic
engineering requirement versus kept as a candidate or directional observation.

```
production-learning/
  README.md
  cases/<CASE-ID>/            one directory per production (schema PRODUCTION-LEARNING-CASE-v0, see check_case.py)
  tools/check_case.py         validator: structure and honesty of ANY case (accepted | rejected | abandoned; template optional;
                              evidence at --source-ref/--source-dir; --pilot-ref/--pilot-dir kept as aliases; an accepted asset is
                              byte-verified against its sha256; a supplied ref that cannot be inspected FAILS) — never a job's outcome
  tools/reconcile_pilot_ledgers.py   append-only JSONL ledger totals per lineage
```

Cases: `UPWORK-INTRO-001` (14 Sep 2026, accepted V4.1 — the baseline for TTAO and full CpAO); `UPWORK-PORTFOLIO-002` (15 Sep 2026, commercial portfolio batch — 9 tiles accepted, 1 skipped after 2 rejected attempts; process non-conformant; complex-production-event trigger MET; evidence on `work/upwork-portfolio-samples-2026-09-15` @ `b4b77fa`).
