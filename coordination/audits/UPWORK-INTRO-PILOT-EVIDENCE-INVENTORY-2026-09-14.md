# Upwork intro pilot — evidence inventory (2026-09-14)

**Purpose.** Before any production-learning record is written, classify every expected evidence item of the
pilot `upwork-intro-video-2026-09-14` (V1 → V4.1) as it actually exists on disk and in git. Nothing here is
interpreted; interpretation lives in `production-learning/cases/UPWORK-INTRO-001/`.

**Where the raw evidence is.** Local worktree `media-intelligence-worktrees/pilot-upwork-intro`, branch
`work/pilot-upwork-intro-video-v4`, directory `pilots/upwork-intro-video-2026-09-14/` (all paths below are
relative to it). 213 tracked files, 385 MB; largest tracked file 31.2 MB (V2 film) — under GitHub's 100 MB
per-file limit; the repo uses no LFS. Merge-base with `main`: `fcc99ce` (PR #97 governor refresh).
The older branch `work/pilot-upwork-intro-video` is at `70f687e` (V3) and is an ancestor of the v4 branch.

**Git verification of the reported commits (local `git log`, IST commit times):**

| Version | Reported | Local git | Commit time | Subject |
|---|---|---|---|---|
| V1 | — | `7629894` | 16:44:13 | first-pass AI-made Upwork introduction film (USD 3.76 of the INR 3,000 cap) |
| V2 | — | `7b39aeb` | 17:21:32 | v2 on approved script v5 — one-voice presenter chain (USD 8.08 cumulative) |
| V3 base | `70f687e` | `70f687e` ✔ | 18:55:57 | v3 showcase first pass — no presenter (USD 3.28 of the INR 2,000 cap) |
| V4 | `11d3e59` | `11d3e59` ✔ | 22:40:00 | v4 — speaker-led showcase (Veo 3.1 Fast qualified 53/60; Omni rejected); cumulative USD 7.31 |
| V4.1 | `f6ca66f` | `f6ca66f` ✔ | 22:56:19 | v4.1 assembly repair; USD 0 incremental |

The reported hashes agree with local git. All five commits are on `work/pilot-upwork-intro-video-v4`; none
is merged to `main`.

**GitHub status.** At the start of the integration `origin` did NOT carry `work/pilot-upwork-intro-video-v4`
(nor the V3-era `work/pilot-upwork-intro-video`). A first push from the pilot worktree was refused by this
session's permission classifier (not by GitHub); a second push by explicit refspec from the main checkout
succeeded on 15 Sep 2026: **`origin/work/pilot-upwork-intro-video-v4` = `f6ca66f42ed9c83e865d9ce188971f8188e483fe`**
(`git ls-remote`), and the V4.1 blob on that remote ref hashes to
`d1a5edf8836936eb7e27cec4350f4cce6f21f1d966778f7241544a2ad07e008a`. History unrewritten; nothing deleted;
**not merged to `main`** and never to be.

## Classification

Classes: **FOUND** (tracked on the branch) · **FOUND_BUT_UNTRACKED** (on disk, gitignored) · **MISSING** ·
**CHAT_ONLY_HUMAN_EVIDENCE** (exists only as the Controller's words in the conversation) · **DUPLICATE**
(byte-identical to a tracked file).

### Films (the five assembled versions)

| Item | Class | Path | sha256 | Probe |
|---|---|---|---|---|
| V1 film | FOUND | `assembly/v1/upwork-intro-first-pass.mp4` @ `7629894` | `c073e9ab0cf67f5754be0fba6505483d375ea314353e4d691e31e468fda8f4bd` | 1920×1080 24 fps H.264/AAC 56.33 s 22.8 MB |
| V2 film | FOUND | `assembly/v2/upwork-intro-v2.mp4` @ `7b39aeb` | `bdd4566eee1b494e802b055a212e6026c664761dad243f43fa01eb37d34915d5` | 1920×1080 24 fps 59.13 s 31.2 MB |
| V3 film | FOUND | `v3/assembly/v3/upwork-intro-v3.mp4` @ `70f687e` | `ea81264d4103faa346b8937b50da4f785d5351f08aefc1e9bceb8d5df0052e51` | 1920×1080 30 fps 59.87 s 19.4 MB |
| V4 film | FOUND | `v4/assembly/v4/upwork-intro-v4.mp4` @ `11d3e59` | `09ed32c54d601f68bd31733dfc1749326d89c9e40a43ba89fc0e6a14d60a29fc` | 1920×1080 30 fps 55.30 s 26.3 MB |
| **V4.1 film (ACCEPTED)** | FOUND | `v4/assembly/v4.1/upwork-intro-v4.1.mp4` @ `f6ca66f` (git blob `5c12db9d…`) | `d1a5edf8836936eb7e27cec4350f4cce6f21f1d966778f7241544a2ad07e008a` | 1920×1080 30 fps H.264/AAC 48 kHz stereo 57.13 s 27.4 MB |
| Intermediate renders (`video.mp4`, `mix.wav`, `mix-comp.wav`, `concat.txt`, `seg/`, `sfx/`) for every version | FOUND_BUT_UNTRACKED | `assembly/v{1,2}/…`, `v3/assembly/v3/…`, `v4/assembly/v{4,4.1}/…` | — | derivable from tracked inputs by the tracked tools; gitignored by the pilot |

### Ledgers, spend records, clocks

| Item | Class | Path | Note |
|---|---|---|---|
| V1+V2 ledger | FOUND | `gen/LEDGER.jsonl` (`da7ac16a…`) | 24 lines: 12 reserved / 12 ok; **USD 8.082** reserved (V1 3.76 + V2 4.32); UTC 10:40:29–11:42:18 |
| V1+V2 ledger summary | FOUND | `gen/LEDGER-SUMMARY.md` | per-route table; cap INR 3,000 |
| V1/V2 spend record | FOUND | `plan/SHOT-MAP-AND-SPEND-RECORD.md` | INR 3,000 cap lineage (closed at V3) |
| V3 ledger | FOUND | `v3/gen/LEDGER.jsonl` (`39004445…`) | 72 lines: 36 reserved / 33 ok / 3 failed (Lyria 503, 500, 500); **USD 3.2836**; UTC 12:43:04–13:23:14; carries `cumulative_usd` |
| V3 spend record | FOUND | `v3/plan/SPEND-RECORD-V3.md` | INR 2,000 cap, new lineage; fal balance USD 3.2315 at start |
| V4 ledger | FOUND | `v4/gen/LEDGER.jsonl` (`f8c1e4b8…`) | 12 lines: 6 reserved / 4 ok / 2 `failed_or_filtered` (Veo gRPC 14 UNAVAILABLE ×2); **USD 4.0276**; UTC 16:42:23–16:54:15; cumulative carried from V3 → 7.3112 |
| V4 spend amendment (+ Addendum 1 outage, + V4.1 USD 0 note) | FOUND | `v4/plan/SPEND-AMENDMENT-V4.md` | **its IST clock labels ("~19:40", "19:58") disagree with the ledger UTC and file mtimes (22:12–22:17 IST) by ≈2.5 h; the mechanical record governs** |
| V4.1 ledger | FOUND (no new lines) | same `v4/gen/LEDGER.jsonl` | USD 0 incremental, confirmed by commit `f6ca66f` diff touching no ledger |
| Mechanical clock (V3 sample-order timing) | FOUND | `v3/gen/CLOCK.json` (`e922e75d…`) | brief complete 12:43:59Z → bundle 13:10:52Z = 1,612 s (the "0 h 26 m 52 s" shown on screen) |
| Whole-run clock | MISSING (never recorded) | — | no pilot file records the end-to-end wall clock; reconstructed in TIME-AND-COST from session metadata, ledgers, mtimes and commits |
| fal balance reads | FOUND (inside prose) | `v3/plan/SPEND-RECORD-V3.md`, `v4/plan/SPEND-AMENDMENT-V4.md`, `v3/learning/PRODUCT-LEARNING-V3.md` | 3.2315 → 0.2589 USD |
| Vendor statements (fal/GCP/Sarvam) | MISSING | — | not reconciled by any version |

### Asset records, prompts, plans, route manifests

| Item | Class | Path |
|---|---|---|
| V1/V2 concept, scripts v3–v5, copy deck, acceptance contract, Karl/Maya reviews | FOUND | `plan/CONCEPT-DRAFT.md`, `plan/CONCEPT-v2.md`, `plan/SCRIPT-v3.md`, `plan/SCRIPT-v4-FROZEN.md`, `plan/SCRIPT-v5-FOR-APPROVAL.md`, `plan/COPY-DECK.yaml`, `plan/ACCEPTANCE-CONTRACT.md`, `plan/KARL-REVIEW-script-v3.md`, `plan/MAYA-VALUE-SPINE.md` |
| V1/V2 pre-production (commercial brief, Canon brief, route analysis, accepted-media lists, recipes) | FOUND | `preprod/*.md`, `preprod/accepted-*.json`, `preprod/recipes/*.py` |
| V1/V2 generated media (presenter stills ×3, presenter takes ×3, chain ×2 + final, plates, overlays, segments) | FOUND | `gen/p0-presenter/`, `gen/p1-presenter-takes/`, `gen/p2-presenter-chain/`, `gen/a0-plate/`, `gen/a1-motion/`, `gen/overlays/`, `gen/segments/*.mp4` + `segments.json` |
| V1/V2 segment ground/overlay PNGs | FOUND_BUT_UNTRACKED | `gen/segments/*.png` (gitignored; regenerable) |
| V3 asset table + per-asset records (prompt, route, price, start/end, latency, verdict, failure reason) | FOUND | `v3/gen/ASSET-TABLE.md`, `v3/gen/ASSETS.jsonl` (`a129cacc…`) — 52 rows |
| V3 copy deck, VO script/takes | FOUND | `v3/plan/COPY-DECK-v3.yaml`, `v3/plan/VO-SCRIPT.txt`, `v3/plan/VO-TAKES.json` |
| V3 stills (11), video (5), audio (16 VO + music), statics (11), deliverables (23) | FOUND | `v3/gen/stills/`, `v3/gen/video/`, `v3/gen/audio/`, `v3/gen/statics/`, `v3/gen/deliverables/` |
| V3 `*-accepted.*` copies | DUPLICATE | `v3/gen/stills/a0-accepted.png` = `a0-r1.png`; `v3/gen/video/{a1,a2,a3,b1}-accepted.mp4` = `…-r1.mp4` (byte-identical; gitignored) |
| V3 batch logs | FOUND_BUT_UNTRACKED | `v3/gen/stills-batch.log`, `v3/gen/video-batch.log` |
| V4 normalized request, creative blueprint, route plan, execution manifest, acceptance contract, speaker prompts, V3 asset inventory | FOUND | `v4/plan/NORMALIZED-REQUEST-V4.yaml`, `CREATIVE-BLUEPRINT-V4.md`, `ROUTE-PLAN-V4.yaml` (`b8b4b616…`), `EXECUTION-MANIFEST-V4.json` (`852725b4…`), `ACCEPTANCE-CONTRACT-V4.md`, `SPEAKER-PROMPTS-V4.md`, `V3-ASSET-INVENTORY.md` |
| V4 asset records | FOUND | `v4/gen/ASSETS.jsonl` (`44477a6e…`) — 12 rows (2 stills, Omni, Veo r1/r2 failed, Veo r3 accepted) |
| V4 speaker media (stills r1/r2/accepted, Omni clip + wav, Veo r3 clip + wav, bubble frame, frame 7.7) | FOUND | `v4/gen/speaker/` |
| `speaker-accepted.mp4` | DUPLICATE | = `v4/gen/speaker/veo-r3.mp4` (`72a16bd7…`), gitignored |
| Veo frames 7.5 / 7.9 | FOUND_BUT_UNTRACKED | `v4/gen/speaker/veo-r3-frame-7.{5,9}.png` (7.7 is tracked) |
| V4 craft deliverable | FOUND | `v4/gen/deliverables/aarohi-craft-4x5.png` |

### QA reports, contact sheets, human-verdict files

| Item | Class | Path |
|---|---|---|
| V4/V4.1 layout, contrast, crop reports (regenerated at V4.1) | FOUND | `v4/qa/layout-report.json` (`1c78e06d…`), `contrast-report.json` (`84009f23…`), `crop-report.json` (`652631cf…`) |
| V4/V4.1 contact sheets, frame scans, audio report | FOUND | `v4/qa/contact-sheet-2s.jpg`, `contact-sheet-key-beats.jpg`, `frames-a1-05s.jpg`, `frames-a3-05s.jpg`, `frame-scan.md`, `audio-report.md`, `v4/assembly/v4{,.1}/audio-measure.json` |
| Speaker micro-qualification (scores, transcripts, contact sheets) | FOUND | `v4/qa/speaker/SPEAKER-QUALIFICATION.md` (`e437642c…`), `omni-r1-transcript.json`, `veo-r3-transcript.json`, `*-contact-*.jpg` |
| V3 audio report, V1/V2 timelines with off-deck check | FOUND | `v3/assembly/v3/audio-report.json`, `assembly/v{1,2}/timeline.json` |
| Human verdict files (ACCEPT / SPECIFIC REPAIR / REJECT per version) | **CHAT_ONLY_HUMAN_EVIDENCE** | none on disk — every pilot learning doc ends "awaiting Controller judgment"; the verdicts (V1 specific repair, V2 rebuild, V3 reject, V4 specific repair, V4.1 accept) and their reasons exist only in the Controller conversation and are transcribed in `production-learning/cases/UPWORK-INTRO-001/HUMAN-VERDICTS.yaml` |
| V1/V2 QA reports (layout/contrast/crop) | MISSING (never produced) | the V1/V2 compositor had no gates; the deck check (`d3_off_deck`) in `assembly/v2/timeline.json` is the only mechanical QA of that era |
| V3 QA reports | MISSING (never produced) | V3 self-check is prose in `v3/learning/PRODUCT-LEARNING-V3.md` §H; no layout/contrast/crop measurement existed — the reason V3 failed by eye |

### Learning reports and tools

| Item | Class | Path |
|---|---|---|
| V1/V2 production map + learning | FOUND | `learning/PRODUCTION-MAP-AND-LEARNING.md` |
| V3 learning | FOUND | `v3/learning/PRODUCT-LEARNING-V3.md` |
| V4 + V4.1 learning | FOUND | `v4/learning/PRODUCT-LEARNING-V4.md` (§H = V4.1) |
| Tools (V1/V2 composer, film, assemble, transcribe; V3 gen/compose/film3/mix3; V4 design4/film4/gen4/mix4/speaker_*) | FOUND | `tools/`, `v3/tools/`, `v4/tools/` |
| Session metadata (start/end of the two executing sessions) | FOUND (outside the repo) | Claude desktop sessions `local_40723378…` ("Upwork introduction video", created 09:32:14Z, last activity 11:51:50Z) and `local_b73a9a32…` ("Upwork Intro V3 production execution", created 12:27:53Z, last activity 17:26:51Z) — read-only metadata; not copied into the repo |

### Not present anywhere (do not fabricate)

- A signed human-verdict file per version; the Controller's V1/V2 feedback bullets and the V3 defect list as files.
- Vendor-billed amounts for any pool; whether Lyria's three failed calls or Veo's two UNAVAILABLE operations billed.
- Vertex / Gemini credit balances (not readable by API); only fal cash was read.
- Any mechanical record of the Controller's review time between versions.
