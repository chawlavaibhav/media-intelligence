# Governance

This directory contains the Repository Governor operating layer.

| File | Purpose |
|---|---|
| `GOVERNOR-CONTRACT.md` | The durable Governor operating contract — role, write boundaries, per-task review protocol, verdicts, audit cadence, routing rules. **Active.** |
| `audits/` | Dated repository-health audits. Permanent evidence of what was inspected, found, corrected and routed. |
| `tasks/` | Controller-assigned Governor tasks. |
| `bootstrap/` | One-time migration input. **Historical — do not bootstrap from it.** |

The approved governance design is
`docs/superpowers/specs/2026-08-25-repository-governor-project-memory-design.md`.

**The canonical project entry point is the root `PROJECT-MEMORY.md`.** It was created by GOV-001
after an exhaustive audit of the repository; detailed domain artifacts remain authoritative for their
own facts.

**Current status:** GOV-001 is complete and under Controller review. The project-wide **audit freeze
on new domain work holds until the Controller merges it.** GOV-002 has not been assigned and must not
be self-started.
