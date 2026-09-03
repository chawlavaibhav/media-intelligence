# History — durable project narrative

**What this directory is.** The durable home for detailed historical narrative that used to live
inside `PROJECT-MEMORY.md`. During the 2026-08-28 context-architecture migration,
`PROJECT-MEMORY.md` became a compact current project map; nothing was deleted — the detail moved
here.

**What this directory is not.** It is not authority. History files describe how the project got to
its current state. What is *currently* true is established by committed evidence, deterministic
validators and durable Controller decisions, navigated via `PROJECT-MEMORY.md` and
`coordination/CONTROL-STATE.md`. If a history file and a newer Controller decision disagree about
current state, the decision governs — the history file is simply describing an earlier point in
time.

**Historical facts are never rewritten.** These files may be superseded by newer chapters; they are
not mutated to match current numbers.

**Ownership.** `history/**` is Governor-maintained project-wide derived narrative. It may archive or
summarise already-accepted project history, but it never owns scientific/domain evidence and never
replaces stream-owned authoritative artifacts or Controller decisions. Stream-specific authoritative
history/evidence stays inside its owning stream.

## Contents

| File | Covers |
|---|---|
| `PROJECT-MEMORY-PRE-CONTEXT-MIGRATION-2026-08-28.md` | Byte-for-byte snapshot of `PROJECT-MEMORY.md` immediately before the context migration (last refreshed by GOV-006). SHA-256 `73369e8936cd1eaef971154e6d1ef93c6c34a151fb37543194c47b8fb239d313`. |
| `CONTROL-STATE-PRE-CONTEXT-MIGRATION-2026-08-28.md` | Byte-for-byte snapshot of `coordination/CONTROL-STATE.md` immediately before its compaction in the same migration. SHA-256 `44d9e82f4f04c7154c912b2146f0edfb8e66697c787d039caffe7110467d3f9a`. |
| `PROJECT-MEMORY-PRE-EVAL-038-REFRESH-2026-09-01.md` | Byte-for-byte snapshot of `PROJECT-MEMORY.md` immediately before the 2026-09-01 Governor refresh (REP-07 admission batch, EVAL-038, CANON-SHAPE-v1). SHA-256 `84599ac8d16981bf443ed8e42af15185fcde3edc806a1666d92e74955ea45fc1`. |
| `CONTROL-STATE-PRE-EVAL-038-REFRESH-2026-09-01.md` | Byte-for-byte snapshot of `coordination/CONTROL-STATE.md` immediately before the same refresh. SHA-256 `9591dfe8d9ff1a51b82b6fedc80a57e15afc42336063871f768fbb4a9cc2ac38`. |
| `EMP-001.md` | The full first-paid-tranche chronology: qualification history, the literalness mechanism finding, spend, evidence sealing, EVAL-029/024/030. |
| `GOVERNANCE-2026-08.md` | The August 2026 governance and planning narrative: V1 overnight, the macro reset, the pre-execution freeze, EVAL-008, GOV-001…GOV-006, external research posture. |
| `PROJECT-MILESTONES.md` | The dated milestone table with evidence pointers. |

Anything covered in a chapter file is also present, in its original wording, in the pre-migration
snapshot above — the snapshot is the completeness guarantee; the chapters are the readable route in.
