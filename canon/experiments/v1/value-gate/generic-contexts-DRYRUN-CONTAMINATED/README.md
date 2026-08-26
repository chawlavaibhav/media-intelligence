# DRY-RUN ONLY — contaminated for the real gate

**Status:** `DRY_RUN_CONTAMINATED` · **Invalidated for real use:** 26 Aug 2026, Controller decision C-C3

## What is wrong with these files

The generic control contexts in this directory were written by the same worker session that had
already read the Oracle Canon material for the same twelve briefs.

**The problem is not that they are bad.** They are careful, substantive craft guidance, and they were
deliberately written strong so the comparison would be fair. The problem is that their independence
**cannot be demonstrated**. A worker who has just read Murch's Rule of Six cannot show that the
"pace is a decision with consequences" section they then wrote was not shaped by it. The influence
could be large or nil, and **nothing in the artifact distinguishes those cases**.

That makes any Canon win measured against these controls uninterpretable. It does not mean Canon
would lose — it means the result would not answer the question that was asked.

## Why they were not simply rewritten

Re-authoring them in the same session fixes nothing: the same worker still cannot unsee the Canon.
The only real remedy is a control authored by a session that has never had access to it. See
`../GENERIC-CONTROL-AUTHORING-PACKET.md`.

## Why they are kept at all

1. **They are working dry-run fixtures.** The scoring and blinding pipelines are exercised against
   them with synthetic labels, which needs no independence at all.
2. **They are evidence of what was done.** Deleting them would erase the record of a method error.
   Historical artifacts are superseded in this repository, not silently removed.

## Enforcement

`prepare_real_run.py` **refuses to build a real run** that points at this directory, and refuses to
run at all until `generic-contexts-real/` exists. That refusal is covered by a negative-control test.
