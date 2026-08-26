# Generic control authoring packet — for a fresh session with no Canon access

**Status:** `FRESH_CONTROL_SESSION_REQUIRED` — this work has **not** been done
**Created:** 26 Aug 2026, Controller decision C-C3 · **Machine-readable input:** `control-authoring-input.json`

---

## 1. Why this packet exists

The value gate compares two ways of planning the same commercial brief: one given explicit Canon
knowledge, one given generic professional craft guidance. The generic side is the **control**, and a
comparison is only as good as its control.

The controls currently in this repository were written by the same worker session that had already
read the Canon material for the same twelve briefs. **Their independence cannot be demonstrated.**
A worker who has just read a source's argument about pacing cannot show that the paragraph they then
wrote about pacing was not shaped by it. The influence might be large; it might be nil. Nothing in
the artifact distinguishes those cases, and that is the whole problem — a Canon win measured against
those controls would not be interpretable.

**Re-writing them in the same session fixes nothing.** The same worker still cannot unsee the Canon.
The only remedy is a control authored by a session that never had access to it.

## 2. Who should do this

A session that has **never read**, and **cannot read**:

- `canon/knowledge/` — the accepted source extractions
- `canon/audit/` — the audit records
- `canon/experiments/v1/value-gate/oracle-contexts/` — the Canon contexts being compared against
- `canon/experiments/v1/value-gate/generic-contexts-DRYRUN-CONTAMINATED/` — the invalidated controls
- `canon/planning/` — the coverage map, which names sources and what they cover

**It does not need to be a different model, and it does not need to be a human.** What it needs is
genuine absence of the Canon from its context. A session that has read this repository's Canon and is
merely instructed to ignore it does not qualify — that is the situation being corrected.

The safest arrangement is a session given **only `control-authoring-input.json`** and no repository
access at all. That file is self-contained.

## 3. What the fresh session receives

`control-authoring-input.json`, and nothing else. It contains:

| Included | Why |
|---|---|
| The 12 customer briefs, verbatim | The control must address the actual brief |
| `media_class` and `duration_seconds` | Static and video need different guidance |
| `target_words`, `min_words`, `max_words` per brief | Length matching — see §5 |
| The planning procedure the context will be used with | Both arms are used identically |
| Authoring rules | §4 |

**Withheld, and mechanically proven absent:**

- every accepted source's name, directory, `source_id` and content
- every Canon reference id (`scs_*`, `sk_*`, `t_*`, `bnd_*`)
- every line of every oracle context
- **`authoritative_intent`** — the scoring material, which never reaches an authoring or planning arm

`build_control_packet.py` assembles the file and then scans the assembled bytes for all of the above.
**It fails closed**: if leakage is detected the packet is not written at all.

## 4. The authoring rules, and the one that matters most

> **Write a strong control. A weak control invalidates the experiment it is part of.**

This is the instruction most likely to be quietly disregarded, because a session told it is writing
"the generic arm" may reasonably infer it is meant to be the lesser one. It is not. If the generic
guidance is vague filler, the Canon arm wins and the win means nothing — and that failure is
invisible in the results, which will simply show Canon ahead.

The full rules are in the JSON. In summary:

1. Strong, genuinely useful professional craft guidance. Do not soften it.
2. **No named books, authors, frameworks or sources. No attributions of any kind.**
3. No headings or structure that mirror a particular source's organisation of ideas.
4. General professional practice only.
5. Stay inside `min_words`–`max_words`. Hard requirement.
6. Match the house format: `# Craft context`, then `## ` sections of short paragraphs, ending with a
   `## Before finishing` section.
7. Address what the brief actually needs. A context that would suit any brief equally is not doing
   its job.

## 5. Why word counts are supplied, and why that is safe

Each brief carries a target and a ±15% band.

**The reason is a real bias that was caught here.** In the first build, the Canon contexts were
**22–37% longer** than their controls on ten of twelve briefs. More context produces longer, more
detailed plans, and reviewers reward that. Left alone, the Canon arm would have carried a systematic
advantage that no reviewer could have seen and no result would have revealed.

A word count is a number of words. It says nothing about what those words are. Supplying it removes a
serious confound and leaks nothing.

## 6. Where the output goes, and what happens then

Write one file per brief to **`generic-contexts-real/<brief_id>.md`**.

`prepare_real_run.py` then:

1. **refuses to run** if `generic-contexts-real/` does not exist;
2. **refuses to run** if pointed at the contaminated directory;
3. re-checks length matching against the oracle contexts and refuses if any pair drifts past 15%;
4. generates a fresh sealed A/B mapping (see `PROTOCOL.md` §C-C4) and commits only a hash of it.

Until step 1 can succeed, **the real gate cannot be run**. That is intentional.

## 7. Status

**`FRESH_CONTROL_SESSION_REQUIRED`.**

This was not done in the authoring session, and the reason is worth stating plainly rather than
working around: **that session had already read the Canon.** No subagent it could launch would have
helped either — a subagent here shares the same filesystem and can read `canon/knowledge/` directly,
so it would reproduce the contamination with an extra step in between. Claiming otherwise would have
been the dishonest option.

This is the one blocker standing between the corrected package and a runnable real gate.
