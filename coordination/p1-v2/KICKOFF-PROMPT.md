# Prompt to start the P1 v2 build session

Paste everything below the line into a new Claude Code session opened in the `media-intelligence` repository.

---

You are building **Media Intelligence P1 v2**. The founder has approved a design; your job is to build it, cleanly, with
**no spending and no live tests**.

1. Check out branch `claude/p1-v2-build-spec`, then create your working branch `claude/p1-v2-build` from it.
2. Read these three files completely before writing any code, in this order:
   - `coordination/p1-v2/P1-MISSION-ADDENDUM.md` — the founder's standard. It wins any disagreement.
   - `coordination/p1-v2/P1-V2-BUILD-SPEC.md` — what to build: structure diagram, workers, rulebook cards (KRAs), forms,
     flow and send-back rules, storage, retrieval, routes, models, cost, tests, build order.
   - `coordination/p1-v2/P1-V2-FOUNDER-CHECKLIST.md` — how the founder will judge your work.
   For background on why v1 failed, read `coordination/p1/P1-REVIEW-ENTRY.md`. The private evidence repo
   `chawlavaibhav/mi-p1-evidence` holds the 23-September job records, which you can use as test fixtures.
3. Follow the rules in §0 of the spec without exception. In particular:
   - simulated mode only; no paid calls;
   - no cloud changes;
   - no merge;
   - you are never the operator — only the founder can override a check, and the code must enforce that;
   - test first.
4. Build in the phase order in §13. Finish each phase with its tests green before starting the next. Commit after each phase
   with a clear message. Push the branch and keep one **draft** PR up to date.
5. If anything in the spec is ambiguous or looks wrong, stop and ask the founder. Don't guess.
6. When finished, fill in `P1-V2-FOUNDER-CHECKLIST.md`: every item marked Done / Partly / Not done, with evidence (file,
   test name, or command and output). Also list any spec changes you made and why, and any open questions. Then stop.
   Do not start live testing.

The founder is non-technical: write reports in plain English, lead with what works and what doesn't, and keep jargon out of the summary.
