# D2C brand discovery + commercial research

**Owner:** the scheduled D2C prospecting agent (unattended cloud run, Mon + Thu, 09:00 IST).
**Scope:** this folder only. The agent writes nothing outside `coordination/commercial/d2c-prospecting/`.

## What this workstream is for

To find real Indian D2C / consumer brands for which **one exceptionally strong unsolicited spec ad**
has a credible chance of producing: a real production test for the runtime; a send-worthy portfolio
asset; a conversation with the brand; and recurring paid creative work.

The loop it feeds: promising brand → understood advertising opportunity → one brand chosen → one spec
ad produced → **the Controller judges SEND / PORTFOLIO ONLY / DISCARD** → send if appropriate →
measure response → if converted, run real paid briefs through the runtime.

This is commercial prospecting. It does not modify the Media Intelligence architecture, Canon, the
Capability Registry, evidence, or any policy profile.

## Files

| File | What it is |
|---|---|
| `PROSPECT-PIPELINE.md` | Durable source of truth. One row per brand. Stages from `CONTACTED` onward are set by the Controller only. |
| `runs/YYYY-MM-DD.md` | One dated record per run: funnel, quick-screen, deep research, scoring, admissions, rejections, top 3. |
| `dossiers/<brand-slug>.md` | Top-3 only. The handoff to the eventual production agent. A dossier does **not** choose the final ad. |

## Standing rules the agent operates under

- **Evidence honesty.** Every evidence item is labelled `OBSERVED` (the page was fetched and seen) or
  `INFERRED` (press, job post, marketplace, second-hand, or a search-engine summary of a page that
  could not be fetched), and carries the date it was gathered. Never "they are running N Meta
  creatives" unless observed.
- **Meta Ad Library + Instagram check recommended by hand for the Top 3 before spend.** From an
  unattended cloud run these cannot be logged into and largely do not render.
- **No contact.** The agent never contacts a brand, DMs a founder, emails anyone, or submits a form.
  No public claim that any brand is a client. No personal phone numbers or private emails are sourced.
- **No invented relationships or conflicts.** Warm paths are recorded only where the repository's
  authorised project context states one. As of the first run the repository states none.
- **Scoring is not inflated.** 85–100 exceptional · 75–84 strong · 70–74 worth retaining ·
  60–69 watchlist · <60 discard. Only 70+ enters the active shortlist.

## What the product can actually make today — read before writing a spec-ad hypothesis

Every spec-ad hypothesis in this folder is shaped to the frozen Alpha-1 family
(`runtime/ALPHA-1.md`; Controller ruling C-7, `coordination/CONTROL-STATE.md` §2):

- **In:** one static commercial ad whose exact copy (price, offer, legal line, brand name) is
  **composed onto the plate by code**, so it is exact by construction and script-independent;
  optionally one **short silent motion version derived only from the accepted still**.
- **Out by ruling:** talking heads, lip-sync, native speech / voiceover, multi-shot stories, and
  **generated in-scene exact text**.
- **Conditional:** supplied-photo work, behind the identifiable-person consent gate, and today routed
  to a person (the `IMG-EDIT` / `IMG-REF` evidence is directional only).

A brand whose core creative need is creator-led talking-head UGC is therefore a **weaker** target than
its brand strength suggests, however well it is doing.

**And note the current hard dependency:** the runtime has never called a provider. Every run to date
is dry, `spend_authority.status: none` on every profile, and live transport is deliberately unwired.
Producing the first spec ad needs the three things named in `coordination/CONTROL-STATE.md` §9 —
a decision on where the plan comes from, live transport behind `ExecutionBridge.run()`, and a signed
runtime spend record. **This workstream can select a brand; it cannot unblock production.**
