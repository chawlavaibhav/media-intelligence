# EVIDENCE MAP — case MOKOBARA-ODYSSEY-007

Every claim in this case resolves to a path on the job branch at the **immutable commit
`130be42caae351a5bf8dc8d062b6fbf51e32b353`** (`work/agency-job-mokobara-odyssey-001`, on origin), under
`agency/jobs/AGY-2026-09-21-MOKOBARA-ODYSSEY-001/`. Rows are `path` @ `commit` with the blob's sha256 in the third column (the hash at that
commit, computed by this sync with `git cat-file blob … | shasum -a 256`). The validator resolves every row and re-hashes
every hashed row; the accepted asset is byte-verified against `OUTCOME.final_asset.sha256`. No media was copied into
this case; the film is read from the commit.

## The accepted asset and its predecessor

| Claim | Evidence (`path` @ `commit`) | sha256 of the blob |
|---|---|---|
| The accepted film (v2), 33,188,717 bytes, 30.021 s, 1080x1920 | `gen/final/mokobara-odyssey-9x16-30s.mp4` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `71850d1cf7969ed1ecf8dc3252586e557c05093377e2e202326283ba93a8faff` |
| The producer's own hash of v2 | `gen/final/SHA256SUMS.txt` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `341d2671966375b632dd693577918e81a19c68f029f5db7c44276e159529c0f7` |
| v1 (judged SPECIFIC REPAIR; the checker's file) | `gen/final/v1/mokobara-odyssey-9x16-30s.mp4` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `75d1fc8b2d59368b7358017c342aaca183e1943e8cc27f6aec43e9bc572cf6a2` |
| v1's hash record | `gen/final/v1/SHA256SUMS.txt` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `134c99944c55d3651dc29571d449063f8798de2d019352d0a09f35b53e6b8b24` |
| The v2 edit list (which take, how many seconds, per beat) | `gen/edl-v2.json` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `f1ad8da142ce7aa98f2248dccd0b8f14115675c7ca7ef0e03d88d73ac6e2b839` |
| Assembly report (segments, 0.6-s xfade, 60-ms audio joins, loudnorm passes) | `gen/assemble-report.json` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `39e43e61a720bc0374e4d889a8698ccc039402c2ef161aa6c719b36c82a3a4fa` |

## Verdicts, status, packet, clocks

| Claim | Evidence (`path` @ `commit`) | sha256 of the blob |
|---|---|---|
| Both customer verdicts verbatim; the Controller's INFERRED item mapping; the v2 open items | `HUMAN-VERDICT-V1.md` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `1e692067e6d4c29db633ff651b033d950bdca6fa0b3398064d0ca9123b238de6` |
| `class: spec_work`, `production_status: accepted`, `learning_status: pending_sync`, every attempt row, `qa.defects` DF-1..DF-10, `versions[]` (incl. the stale duplicate v2 entry), `ttao.*` stamps, `kpis.ttao_hms 10:23:37`, the ledger note on att-020 | `JOB.yaml` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `6d8b64a8ce186850cee6470c2b855e6a29354e1cf3d52197af24350ab3356613` |
| The learning packet (what worked / did not; numbers with the discrepancies this case records; candidate promotions) | `LEARNING-PACKET.yaml` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `ab2022f389ce19172cf5e44b2d36abf1beb9c463d509f7f1af8728ca4fd4578b` |
| `job_start_utc 2026-09-21T17:22:48Z` (the TTAO clock's start) | `TTAO-START.yaml` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `6f182c15e475141f973353ad41e8032a462933fb81e9a4f9083ee5c107ccc4fd` |
| `dispatch_start 2026-09-21T17:38:37Z` | `gen/DISPATCH-START-UTC.txt` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `e02f05fa9188b67e3a108d86aa7fd6b8f8582408d6e3b2178888b8b7d1332aef` |
| Commit times used as anchors: 0d4adf2 / 9a0a1bb (stages), 7bacd79 (stage 5), 2e69cd7 (v1 verdict), 12f43f5 (checker), 8bc9f33 (repair round), 5e64662 (v2 verdict), 130be42 (TTAO fields) | `git log --format='%h %ci %s' 130be42` on the fetched branch | — |

## Brief, authorisation, stages

| Claim | Evidence (`path` @ `commit`) | sha256 of the blob |
|---|---|---|
| The frozen brief, verbatim, with the five execution instructions and the Controller's reading of "arms" and "odysey" | `input/00-CUSTOMER-BRIEF-FROZEN.md` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `17ffc7defffe657f46449bc24a5abebf288a3cbb28389acfc380c852c556a36a` |
| Cap USD 12.00, credits only, no fal, 0 hidden retries, every failed call counted | `input/SPEND-AUTHORISATION.md` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `e7622c7e56b7503565c96b43856c29b2079c82e1d47a93e716ff4766ea33f52c` |
| Mandatory items M1–M7 and the decisions taken without asking (9:16, ~30 s, no dialogue, the Transit Backpack in Private Island, no price) | `stages/01-INTENT.md` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `17e3dcb850084a685febb9ca2bf9870ede71dd73e36ddf72e815aaf2928edfcf` |
| Publishing spec carried from case 004 (safe box, loudness, no edit lists); brand facts quote-exact from fetched files; "font not verified"; permitted and forbidden strings; the IP list | `stages/02-STRUCTURE.md` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `2baccbd48000838fa1deb922c6f1850601a2d488b8feef9d4835034d05382de2` |
| Canon consulted by id (incl. the Ogilvy/Hopkins humour tension resolved from existing claims); the 21 compiled checks applied; the declared gaps; the board table; the copy deck; audio direction | `stages/03-CREATIVE.md` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `02afead8c8f43228ed703a3662ee7ec11262c8807b1a17ddc353f7078a902a8c` |
| Deterministic pack lookup: 2 injected, 8 uncompiled, prefix sha 4d7a5b27…, 21 check ids | `stages/evidence/canon-lookup.txt` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `b5d24f87dfccb22300902133f33fd5b868b04dc4ed10c1c15561ecfb293dd70a` |
| The board: seven beats with feeling / framing / impact / canon, identity anchors, hero frame, audio plan | `board.json` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `d74a6f72f9040532750cb2403d3f88b2ee3663863e15195a0f8586ac36672e0c` |
| The three byte-exact strings | `copy-deck.json` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `691b9673649dcd11f963243373fdee2d159cee201060be1a2fd00606bf8d182e` |
| Route candidates, the topology decision, why i2v over t2v/ref2v, the riskiest capability, the micro-qualification plan, expected spend 3.53 | `stages/04-PRODUCTION-SELECTION.md` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `0d9b7d19a42841b9fb57a25a8820594a9f92fd672b66398d3720d2111218b8be` |
| What happened in order on v1; the 18-attempt spend table (5.389); DET results; the LJ list (incl. LJ-3's overstatement and LJ-8); "not realised" | `stages/05-PRODUCTION.md` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `947d4aeae743c92fe3ffdcf9422bd97e9622b04ec9a1dec76f0bb4daf2da48d6` |
| Repair round 1: the merged item → layer → fix → attempts/USD → frame → result table (A–E + 4, 5); the ledger collision note; items not addressed and why; the v2 edit list; DET v2 | `stages/06-REPAIR-ROUND-1.md` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `c59d8f5ee6054116d65101b633be2be9402c5fa15d1ed0807ba17e3628c4fe38` |
| The independent checker on v1: every re-measurement, the ledger re-add (5.389, 17/17 hashes), the IP grep (0 hits), R1–R8, brand/product fidelity, D1–D9, the creative scores, the cross-reference with the customer's verdict | `stages/CHECK-STAGE-5.md` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `fa642b28c929aac15f3c0c1c5fc430f09d912c67d1ac6dde7b3e88a0b1e41d0b` |

## Money and attempts

| Claim | Evidence (`path` @ `commit`) | sha256 of the blob |
|---|---|---|
| 27 reserve lines = USD 7.857 (11 x 0.067 + 70 s x 0.10 + 2 x 0.06); 26 ok, 1 http_500; cumulative re-adds; att-020b `note_id`; att-020 reserved 18:22:16Z / settled 18:23:28Z around att-020b at 18:23:00Z | `gen/LEDGER.jsonl` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `5c865015d105d56136d06a2e989c6bad21e413b2793792e12215ad318089d635` |
| 27 attempt records: prompt sent, params, reference image sha256s, latency (Veo 48.3–73.5 s; NB2 11.5–35.4 s; sum 1071.2 s), artifact sha256, verdict, is_repair | `gen/ATTEMPTS.jsonl` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `e6b939af60b0e9b8a8e0a9a68763467df7a4dc8b9f820d18cfd3a5299ba7ca1a` |
| One recorded change per re-take (first pass and repair round) | `gen/RETAKES.md` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `5e96803a4f21d5e68e4031b7660426de2211a7310a4dbc2686be91571c187d8f` |
| `next_attempt_id()` counts lines of ATTEMPTS.jsonl (the settle-time file) — the LG-1 root cause; the prompt guard; reserve before every request | `tools/dispatch.py` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `40bff22ca71e96b3df3de1e0a7c2a7999dea92381eeee875dd120ba5c8a2d6c9` |
| The dispatch kit's lineage (copied from CQ-001 @ 41d97c6 ← Cumin B @ 5c33173; qa_checks from case 006's job @ ffefe44b; loudness/mux flags from its assemble_v2.py) | `tools/PROVENANCE.md` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `0d41a7128873bc31c598892984490c42857f443999761559f5de271d62ab1b37` |
| Micro-qualification card: PASS with note (arm not to the shoulder; no second arm) | `qa/b4/MICRO-QUAL.md` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `5c6235f0de57bd358c78fbde2eeac17051b27b27c9f72792e5083c03e79b307e` |
| Beat-4 take 1 (straight paddle; the take in the accepted film) and take 2 (warped blade; used in v1) | `gen/clips/b4.mp4` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `3fc93d6619501033e1b874b75e4ac7c0126dba73da8c67f1d7e4ebcda7dd0cef` |
| (same claim, second file) | `gen/clips/b4-take2.mp4` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `60e20943fd18955c77032c1b34585964f323321a66fa7a8b6b30b627119edeb3` |
| The Lyria wording that got HTTP 500 and the neutral wording that succeeded | `gen/prompts/music.txt` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `6453396372d648e1975f0c19ebfdbff400192fa0ba0301a0e32d2036945e2ee1` |
| (same claim, second file) | `gen/prompts/music-v2.txt` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `4863421998993b7fad4935fe4d515e58887d228c9598d77e56b6470a028ad5fb` |
| The exit-action prompt (beat 5 take 4) and the negative prompt naming the product (beat 1 take 2) | `gen/prompts/b5-clip-take4.txt` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `18fe8324b717d013b1fad7399e3ad3693dc494fadeb1dda94b40e8cdc94e7ad1` |
| (same claim, second file) | `gen/prompts/negative-b1.txt` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `da4b3d4129b65db07d26f116bb8955eb49ddca5c007b3191a9efd8a5a29c029d` |

## Composition, QA, brand assets

| Claim | Evidence (`path` @ `commit`) | sha256 of the blob |
|---|---|---|
| `tools/render_text.py` imports `check_text_bounds`, `check_contrast`, `check_disjoint` from `runtime.compositor.gates`; the super's 10-frame luminance samples | `tools/render_text.py` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `93da9497f497f73db0d6b70a753a09f9becf6af15aad277ac7223c913b3fec0f` |
| The 10 compositor gates at render (bounds x5, contrast x4 — super on pixels 6.583, three on navy 14.457 — disjoint x1), the font record (Helvetica Neue; site faces seen), boxes, logo/wordmark sha256s | `gen/overlays/layout.json` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `36331092ba0fa7286258bf308d1af0b85353e168f7f6511596e2bed12cd5e06e` |
| DET on v2: 18 PASS / 1 FLAG / 1 NOT_RUN (duration 30.021, geometry, moov first, 0 elst, AAC, -13.4 LUFS / -4.0 dBTP, copy byte-exact, wordmark and logo by hash, gates, safe box) | `qa/final/qa-results.json` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `e7a77f9dfa8b93d6c854aff4068a9169c4c40f08bb54099b7c68e14ff158e05c` |
| DET on v1 (the checker's file) | `qa/final-v1/qa-results.json` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `3808a631c6262dfa8d125e72956b7a75f14c9b932ca327873a754c3acbe4285c` |
| 60-ms acrossfade joins (v2 assembler) | `tools/assemble.py` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `24c15a696a663dbacc8a82d751445e2f68b140bbd95e94ea50b9e83df97cf3c9` |
| The job-local DET suite (container walk, loudness, copy deck, hash checks, OCR flag, keyframes) | `tools/qa_checks.py` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `1f600f738a1bee1c923d3d1a5f5f617be3d64a70a77acc89f685a8afaf4affed` |
| The site's own wordmark SVG and black logo PNG, unmodified | `source/mokobara/wordmark-white.svg` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `c443658f13bed93aa1adbb6bcbc5fcbb06fc4d9abdafd0f59f5da593c67356eb` |
| (same claim, second file) | `source/mokobara/logo-png.png` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `b3aefbd50a7edfa9b3a251373a7ed4a039e1540609a4d8c65c323581d776da07` |
| The 13 fetched brand files hashed at fetch time | `source/mokobara/SHA256SUMS.txt` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` | `e604c7c851339cf6f04f579df4b7b0e136c7be068491a8ca5394ae0969c9a13b` |
| Frames cited by the checker (11 + the product comparison sheet), the repair-round sheets and frames, the v2 contact sheet and keyframes | `qa/checker`, `qa/repair-1`, `qa/final` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` (directories; individual frames listed by `git ls-tree`) | — |

## What is NOT on the branch (stated, not invented)

- No independent check of v2 (no `stages/CHECK-STAGE-6.md`); the customer's "pass" is the only judgment on the accepted file.
- No ear check of the native audio by a human, on either version.
- No file records which "minor issues" the customer meant on v2.
- No session-token counts; no vendor statement; no machine-readable credits balance.
- The Mokobara dossier (`coordination/commercial/d2c-prospecting/dossiers/mokobara.md`) lives on the base sha `c88c0d5`, not under the job directory; it is cited by Stage 1 and not re-read by this sync.
