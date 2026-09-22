# MOKOBARA-ODYSSEY-007 — a 30-s live-action-style spec film for Mokobara, accepted on the second presentation

**Job** `AGY-2026-09-21-MOKOBARA-ODYSSEY-001` · branch `work/agency-job-mokobara-odyssey-001` · validated against commit
`130be42caae351a5bf8dc8d062b6fbf51e32b353` · base `c88c0d5` · class `spec_work` (Mokobara is a prospecting target; the human
Controller was the customer) · written 2026-09-22.

## What happened, in plain English

The customer asked for an Odyssey-shaped ad for Mokobara's Transit Backpack: a man stranded for years finds his bag on the
island, finds his wife's photo inside, and — the joke — his arms disappear into it and everything he needs to go home
comes out. He asked for the five-stage pipeline, the RentOK "feeling / framing / impact per beat" learning, a route chosen
for this film (not code-rendered animation by default), and a fast first pass. Cap USD 12.

The producer chose generated footage: one hero still of the man and the bag made from the brand's own product photos,
one still per beat anchored on it, and a Veo image-to-video clip per beat, stitched by code with the brand's own wordmark
and a code end card. The riskiest beat (the gag) was bought first and judged before the rest. The first pass took 43
minutes to a clean file and USD 5.39 (18 paid calls, one Lyria refusal counted, three re-takes). The customer's verdict
on it: **"overall excellent just few fixes"** with five items — a torn-looking bag, a paddle that came out "weird", a paddle
already on the raft that then "comes out magically again", the logo not used properly, the font.

An independent checker, working on the same file at the same time, found three things the customer had not said: the
arms never go in past the forearm (the customer's own named gag is not on screen), the food is left on the beach when the
zip closes, and the man never actually leaves the island. The Controller merged both lists into one repair round with the
customer's mandatory story events first. Nine more paid calls (USD 2.47) and two free fixes later — the straight-paddle
take was already on disk; the logo and type were redone by code with the brand's black logo measured against the real
sky pixels — v2 was ready 1 h 16 min after the job started. The customer answered the next morning: **"still some minor
issues but excellent. pass/"**.

The accepted file still carries the arms-at-forearm-depth gag (the round chose the straight paddle over arm depth), the
paddle's unexplained whereabouts for three seconds, 720p softness, and native audio nobody has listened to for stray
speech. The customer's own "minor issues" were not itemised. This case records all of that rather than calling the file clean.

## Numbers (ledger and stamps, never the packet's arithmetic)

| | |
|---|---|
| TTAO | **10:23:37** job start → ACCEPT, of which **1:15:46** was production (job start → v2 DET-clean); 0:43:29 to the v1 file; 9:07:51 waiting overnight |
| CpAO | **USD 7.857** (27 paid attempts: 26 ok, 1 HTTP 500 counted; 70 s of Veo bought for 28 s used; USD 4.27 of it on re-takes) — vendor-unreconciled upper bound |
| Cycles / versions | 2 / 2 (one independent checker round on v1; v2 not re-checked) |
| Baseline (case 001, generative video) | 7 h 54 m / USD 15.39 / 5 cycles — MET |
| RentOK V2 (case 006, code-rendered) | 0:51 / USD 0.067 / 1 cycle — a different class; slower to a clean file by 25 min and ~117x the spend, which is what generated footage costs |

## The five classes, in one line each

1. **Promoted to code: none.** Every candidate (ledger id collision, mandatory-event visibility, audio dips at cuts) fails the
   "which runtime file does it live in" half of the class-1 test; the reasons are per item in `SYSTEM-DEFECTS.yaml`. The
   earlier-promoted overlay gates ran in production here for the first time on generated footage and decided one customer item.
2. **Candidates:** the still → i2v-per-beat topology with product-photo references (the template, n = 1); micro-qualify the
   riskiest beat first (now 4 jobs, 2 briefs, 2 classes); feeling / framing / impact per beat (case 006's promotion condition —
   met in letter on a different brief, not in spirit: not code-rendered, same customer, accepted after repairs, nothing isolates
   it); end-state still + last-action clip; exit action after the goal; negative-prompt the product before its reveal; paint out
   copied reference marks; take selection before re-take; merged repair list with mandatory events first; one LJ line per
   mandatory event; brand-font fallback with the site's CSS styling; ledger lock / atomic attempt ids (exact requirement stated);
   audio-join crossfade with a nameable gate; OCR-on-texture is a flag; state source resolution.
3. **Directional:** Veo 3.1 Fast i2v from Nano Banana 2 stills — 14/14 returned, identity and bag likeness held, seven named
   limits; NB2 with product-photo references 11/11, copied the tiny wordmark 2/2, one tear-like flap then intact; Lyria 500 on a
   story-laden wording, ok on neutral (4 errors on descriptive wordings across 2 jobs; 4/4 neutral first tries across 4 jobs).
4. **Canon gaps: none new.** The humour tension in Canon (Ogilvy vs Hopkins) was resolved from existing claims; no failure traces
   to missing Canon; the eight uncompiled packs are the known gap.
5. **Job-specific:** the beats, the tagline, the colourway, the man, the Stage 1 decisions, the priority letters.

## Files

`OUTCOME.yaml` · `HUMAN-VERDICTS.yaml` · `REVISION-TRACE.yaml` · `TIME-AND-COST.yaml` · `SYSTEM-DEFECTS.yaml` ·
`ROUTE-OBSERVATIONS.yaml` · `PROMOTION-QUEUE.yaml` · `ACCEPTED-TEMPLATE.yaml` (reusable_candidate, n = 1, why stated inside) ·
`EVIDENCE-MAP.md` (every claim → path @ `130be42…` | sha256; the accepted film byte-verified).

Validate: `python3 production-learning/tools/check_case.py --case production-learning/cases/MOKOBARA-ODYSSEY-007 --source-ref 130be42caae351a5bf8dc8d062b6fbf51e32b353 --source-dir agency/jobs/AGY-2026-09-21-MOKOBARA-ODYSSEY-001` (fetch `origin/work/agency-job-mokobara-odyssey-001` first).

## Discrepancies between the record and the sync brief, stated

- The brief for this sync called the job `customer_work`; `JOB.yaml` says `spec_work`. The record wins; the case says why.
- The packet's `first_pass_usd 3.529`, `clips_bought_s 46` and `repair_round_1_minutes ~50` do not match the ledger and
  stamps (3.589 before re-takes; 70 s; 23:53). The totals and verdicts are unaffected. Recorded in `REVISION-TRACE.yaml` REC-1.
- `JOB.yaml` stamps v2 as presented 94 s before its QA completed; the case uses the QA stamp for the pipeline clock and
  says so.
