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

**The canonical project entry point is the root `PROJECT-MEMORY.md`.** It is a map to the evidence,
not a source of truth: committed artifacts, deterministic validators and durable Controller decisions
establish project truth, and detailed domain artifacts remain authoritative for their own facts. The
Governor is downstream of all of them.

**Audit freeze.** All new domain work is frozen. **The freeze remains in force until the Controller
explicitly lifts or re-scopes it** — it is not tied to any task or pull request completing, and
merging governance work authorizes no domain work.

**GOV-001** established this layer: `PROJECT-MEMORY.md`, the Governor contract, the first audit, and
targeted control-plane corrections. **GOV-002 has not been assigned and must not be self-started.**
