# EVIDENCE MAP — case RENTOK-GAME-V2-006

Raw media is **not** duplicated here. Every claim points at a file on the job branch
`work/agency-job-rentok-game-v2-001` at its immutable HEAD `b06deaf` (full sha
`b06deaf7907de9c64d574a5f042a014c2e519ce6`), directory `agency/jobs/AGY-2026-09-21-RENTOK-GAME-V2-001/`,
identified by path, commit and full sha256. Paths are relative to that directory. The branch name is provenance only; the
commit is what the validator reads. **At sync time the job branch existed only in the local repository** (not on
`origin`); a push is attempted in step 7 of the sync and the PR body says whether it succeeded.

Validate: `python3 production-learning/tools/check_case.py --case production-learning/cases/RENTOK-GAME-V2-006
--source-ref b06deaf7907de9c64d574a5f042a014c2e519ce6 --source-dir agency/jobs/AGY-2026-09-21-RENTOK-GAME-V2-001`
(fetch `work/agency-job-rentok-game-v2-001` first if the ref does not resolve).

## The delivered film and its superseded version

| Claim | path @ commit | sha256 |
|---|---|---|
| the accepted film (final_asset) | `gen/final/rentok-game-v2-9x16-30s.mp4` @ `b06deaf` | `0e76b7b1872317728cfbb08dc948e4c678452ef7d84a0eafd6ece0f89013d122` |
| final-v1 before repair round 1 (R-1 framing, R-2 true peak) — never presented | `gen/final/v1/rentok-game-v2-9x16-30s.mp4` @ `b06deaf` | `1cc8c13d79aa6dd92136ff58dd478cce19583706227eb1d498f6184457c51ca9` |
| producer contact sheet of the delivered file (61 frames + 16 keyframes; D1 eye pass) | `gen/final/CONTACT-SHEET.png` @ `b06deaf` | `de2887bb01a7b975dc96ba7d91016cb3cc910c5a935d29576762780eaafa5326` |
| producer keyframes incl. hero frame 651 | `gen/final/KEYFRAMES.png` @ `b06deaf` | `54f48b50c7adfed0b67097f8de40e17346f25f4f93f702dc6b63af7ce86844b8` |
| the three hashes above as the producer wrote them | `gen/final/SHA256SUMS.txt` @ `b06deaf` | `f022fc3d8394e1123748e2bd02f99e0a2dd1af218de0d7f37d85aeaa53a98de3` |
| USD-0 animatic v2 (stand-ins; 26 gates PASS before the paid call) | `gen/animatic-v2.mp4` @ `b06deaf` | `1af2cb5cddb8156d851e79e0012cd0c7f87fad5e41b646e5b043641090e87dda` |
| USD-0 animatic v1 (A-1..A-5 found on it) | `gen/animatic-v1.mp4` @ `b06deaf` | `ee41f86c6f7f92afa7a42b40718a8eb6af3994d6fde36a382066d0e5ad7b29c4` |

## Records, stages, ledgers

| Claim | path @ commit | sha256 |
|---|---|---|
| the job record: brief verbatim, intake, plan, spend, qa, versions[0] verdict verbatim ('its already good' / 'not required'), ttao stamps (job_start 11:25:07Z, qa_complete 12:16:20Z, human_decision 16:34:35Z), kpis ttao_hms 5:09:28 | `JOB.yaml` @ `b06deaf` | `5db2187fbcda9db3abde0fd65c8024bfb2dc371b8d8fb165375c9c1a2019aabf` |
| the producer's learning packet + the Controller's appended human_verdict_final (ttao_note: 0:51:13 / 5:09:28; 'USD 0.66 every drawing'; 'six recorded defects left unrepaired') | `LEARNING-PACKET.yaml` @ `b06deaf` | `35dd35eb6e2377b9b05c3a914b368b46029a3995e4f3481895d9e457900b60ab` |
| append-only ledger: 1 reserved + 1 ok line, USD 0.067 of cap 3.00, reserve stamp before the call | `gen/LEDGER.jsonl` @ `b06deaf` | `b0e5996db7b9f1cd38a888836f891ae00b1cfddc0d14cde6087dd8899bb1c029` |
| attempt mirror: 1 row, the full prompt, latency 53.6 s, artifact sha256, verdict_note with the lookback miss | `gen/ATTEMPTS.jsonl` @ `b06deaf` | `0e26ede5ad169bff5bb141f3b171259afe9fc5ba34f2ecdbeaae20ca9307e540` |
| provenance of the 61 reused files: Lane A @ 7dab37a and Treatment C @ 41d97c6, each blob-verified | `PROVENANCE.md` @ `b06deaf` | `9d52c7fd6e5261a2145eccbb55f53261bdf833f56ca79187d8d6ab463e0cda88` |
| independent checker: DET re-measurement, A1–A11, claims vs site, defects N1–N9 + P1, creative scores, verdict DELIVERABLE WITH DEFECTS | `stages/CHECK-STAGE-5.md` @ `b06deaf` | `69d722c3399a88ea45b4bf398305d17ee8d96d7997f85c3e8d8713e627022168` |
| producer execution record: order of work with UTC, DET table 28/28, the paid draw inspected, repairs A-1..A-5 / R-1..R-2, LJ items, §5.6 what the renderer cannot do | `stages/05-EXECUTION-AND-VERIFICATION.md` @ `b06deaf` | `78c8d1c6496d4b6a8d904afeddbeffa94ae067d548ec449654f2f69f7582a6c9` |
| production plan: reuse records with accepted_in_context, the one new draw N1, ceiling 0.201 of 3.00, consistency card | `stages/04-PRODUCTION-PLAN.md` @ `b06deaf` | `2779f8ab094fcabf7836d16778c9aa89954fb8ec162225fe3c929dbc0c51823d` |
| creative package 'the Video-4 way': BOARD-v2 fields, per-beat feeling table, GAP block (animation principles), Part E animatic judgement | `stages/03-CREATIVE.md` @ `b06deaf` | `f0735c18ab4a04f59cf11b1bc5284656771bd94417c1ab4cc365d6a7d78a1576` |
| structure carried over from Lane A and re-verified | `stages/02-STRUCTURE.md` @ `b06deaf` | `cb7ec7cea50f345f6c58b168ba619949483e0a0ce3977159692ed1b0c3619fa0` |
| intent carried over from Lane A and re-verified; V2-D1..D4 assumptions | `stages/01-INTENT.md` @ `b06deaf` | `249f28e7be92abd253f83349a371d0e4499aff6b3ec3f35d274f458f66419cb2` |
| the frozen customer brief (identical to Lane A's) | `input/01-CUSTOMER-BRIEF-FROZEN.md` @ `b06deaf` | `65382cffe1d5632c354b2f1601c0e2b7c7d44539dbfaf350562e07b772cf5cc0` |
| acceptance contract (A1–A11, 2.6 loudness) | `input/03-ACCEPTANCE-CONTRACT.md` @ `b06deaf` | `43be9e133fe644790c2609ef34242535c0c77cdc30730a009232f719b42d3454` |
| CQ-001 diagnosis as frozen into the job (why this job exists; §6 the smallest consequential change) | `input/05-CQ-001-DIAGNOSIS-AND-ROUTE.md` @ `b06deaf` | `bf672a35bdaaa5c9d26ceafefa8f888e4afd35eb185d598021a65a91e04c9d93` |
| Treatment C record as frozen into the job | `input/06-CQ-001-TREATMENT-C.md` @ `b06deaf` | `9ff9d6dfaedbadf454372a9e3ac345fc8c0f882803861f539721c8a06db220c6` |
| spend authorisation: 'USD 3 (Recommended)', credits only, 2026-09-21T11:21:39Z | `input/SPEND-AUTHORISATION.md` @ `b06deaf` | `55beb47b7c8aaa3cd3587671fc54964fce88f2b0524bccfbba936f7a35121f52` |

## The board, the deck, the renderer, the gates

| Claim | path @ commit | sha256 |
|---|---|---|
| BOARD-v2: fifteen beats with feeling / framing (owner_frac_target per pose, focus_t, camera keyframes) / impact (25 primitive names); hero_frame 651; principles_note | `board.json` @ `b06deaf` | `702028771872b7c2aec0dc3c6aa8aaa1c2cc1fff5bfe2cdfd22393814c3c8f41` |
| copy deck, 27 strings byte-identical to Lane A's | `copy-deck.json` @ `b06deaf` | `77f6b06cbf6f3ae60129d5f16586fc2e46193c3d4c6a75af38f8bc5f292b48df` |
| brief.job.json (Lane A's, unchanged; Canon prefix) | `brief.job.json` @ `b06deaf` | `149193ced1df59aea84ccfcfbe3b8ac8a7271bbabcfb2aa358eb0fa3c6b06c03` |
| the board-driven renderer (reads camera / hit-stop / shake / pose / audio from the board) | `tools/render_v2.py` @ `b06deaf` | `8566efa9d8f9653998c09290cfc0938682a6c7a509a39ce1746eb0cd454e1e32` |
| the board authored as data | `tools/make_board.py` @ `b06deaf` | `dad12b75fc43016fa8508199b712b2a4593cfca0d247dd7cda18e16aea112b54` |
| the DET suite incl. C5b (sprite states burst/leaving excluded), FRAMING at focus_t, 'world fills the frame (camera >= 1.0)', HERO frame | `tools/qa_checks.py` @ `b06deaf` | `8effc837ed6cfb30818c601df3c795d7e56ee85d0f7724f6df844b7b41fe54cf` |
| sheet inspection: cells, standing_cell_h, keyability, keys/book pixel counts, merged-cell split | `tools/inspect_sheet.py` @ `b06deaf` | `f3da66bd4e3155fe5d3e00eab07714441a0d4e20fdb91e9816874a73ec6a73b0` |
| SFX from the board's 53 cues | `tools/sfx_v2.py` @ `b06deaf` | `5d7fa1ba199ac7b4a04168366fc23b02b80a1b2f28cdf08b07ead6eec72f06c9` |
| assembly with per-beat bed processing, loudnorm + limiter | `tools/assemble_v2.py` @ `b06deaf` | `580333d184aafd1d66df88058bb5c50242170b008ae92a88b88877aece9ba976` |
| layout log of the delivered file: 900 rows, camera scale 1.0–1.6, owner_frac per frame, sprite screen boxes with states — the source of every box in `runtime/tests/test_k_rentok_game_v2_006.py` (FLAG ∩ OWNER on frames 796–821; PHONE over the head band at frame 546; OWNER x0 = −52 at frame 113; owner_frac 0.156 at 8.40 s vs 0.216 at 8.55 s) | `gen/final-v3-audio-layout.jsonl` @ `b06deaf` | `1823adcbd2ae322cba38ddc04227a95a05cbbbdf350ed913ca0f5b07f98ece2b` |
| event log of the delivered file (hits, install 17.4, bursts, flag 26.6) | `gen/final-v3-audio-events.json` @ `b06deaf` | `3d1de698b86a4556ad8bd38af5a0339ee45685fcc481ccb0cf308c5f564b4af9` |
| DET results on the delivered file: 28 PASS / 0 FAIL / 1 NOT_RUN | `qa/final-v3-audio/DET-RESULTS.json` @ `b06deaf` | `967080a566759f594c072741cf237a4a233a633558c0169708a5713449d31d57` |
| DET on animatic v1 (the 4 FAIL that became A-1..A-4) | `qa/animatic-v1/DET-RESULTS.json` @ `b06deaf` | `ce185fa94e5a511241869def41aa0b40a08be2c941482b52fcdc065904774589` |
| DET on animatic v2 (26 PASS / 0 FAIL / 3 NOT_RUN, before the paid call) | `qa/animatic-v2/DET-RESULTS.json` @ `b06deaf` | `228663a1020505258b282b048e9f9aae41f5a5ea4db8013eef1f540852146670` |

## The one paid draw and the sheet densities

| Claim | path @ commit | sha256 |
|---|---|---|
| att-001 raw sheet (frozen by sha256; = ATTEMPTS.jsonl artifact_sha256) | `gen/raw/V2-S1_pose_sheet_att-001.png` @ `b06deaf` | `ad4dab13c768e69dee32ddcf2c1b7daf6888dbdb2bf053d025da5cb5a0b32e9f` |
| the prompt sent (no lettering clause; no deck string; no IP word) | `gen/prompts/V2-S1_pose_sheet.txt` @ `b06deaf` | `02c38c70c3b36c3cbaa31b9b43b575080bdc94f9a62c06a4d38c13830836400d` |
| Canon pre-gate PASS on the prompt | `gen/prompts/V2-S1_pose_sheet.gate.json` @ `b06deaf` | `b34d603536576c2db03d3d8bb47d85c4b0164618e6ae34599868dfbd2efb528d` |
| consistency card: the eight cells beside the accepted Lane A idle and C brace | `qa/V2-S1-consistency-card.png` @ `b06deaf` | `bfa10152d988168353c2e976a058bc0d42d75307db3bc11e9ecf085404c9c37e` |
| V2 sheet cut-out record: 8 cells, standing_cell_h 342, keyable 0.9995, book 5/8, keys 8/8, merged cell split | `gen/assets/v2_cutout.json` @ `b06deaf` | `6e3446628ac6a7f51731d9f77dbc5e04f6c7f5b69a041cd1d3ad43a34f8ccb1c` |
| Treatment C sheet cut-out record: brace/windup/fire 344 px (density comparison, N5) | `gen/assets/c_cutout.json` @ `b06deaf` | `bb32392ee3d1ac0d6d91223f558fa0c3caf6c0ea1230639a45347936b94fb5ac` |
| Lane A base sheet cut-out record: idle 561 px (density comparison, N5) | `gen/assets/owner_cutout.json` @ `b06deaf` | `12d572ca96e06e950e0d56bb5ee388e3257a6c8c6dd4797b78173e49f1e0e7c6` |

## The checker's own frames (the unrepaired defects, as seen)

| Claim | path @ commit | sha256 |
|---|---|---|
| checker's 61 frames at 2 fps | `qa/checker/CONTACT-SHEET.png` @ `b06deaf` | `987ebf0d1459bfa2a3e71f8ec74bb36e348910a3a6cb1966b25b4b079c138486` |
| eight frames at 360 px wide (phone-size readability; A8; the small projectile) | `qa/checker/PHONE-360.png` @ `b06deaf` | `0f2441e71879ccb359f9476a3d5b389170cf680b00d42053a9f7aa249600dec7` |
| N1 — the flag rising through the owner (26.6 / 26.9 / 27.2 s) | `qa/checker/lj/14-f798-f825-flag-rises-through-owner.png` @ `b06deaf` | `39255073332a873982bdd4356097099baa054a30670c896911be5dfdde59c295` |
| N2 — the phone over the face at the wind-up | `qa/checker/lj/09-f546-f556-windup-face-occluded.png` @ `b06deaf` | `a6f89da018d4a52bca6015e2be605807194df0c7ac28358102844ff154b9ed2b` |
| N3 — kneel → catch in one frame; the two white flash frames | `qa/checker/lj/08-f519-f528-kneel-to-catch-flash.png` @ `b06deaf` | `61adabf1fac1b17082e5d00e806dfc04a072a1036109b4cff6faea09571178fb` |
| N4 — the dazed owner clipped at the left edge | `qa/checker/lj/02-edge-clip-t4.0-t6.8-t14.2.png` @ `b06deaf` | `a92ee55ab940eef24a5046fa24e7b20133ffb4e75736e838efeec7001e72dacf` |
| N5 — pose swaps, native vs phone size | `qa/checker/lj/03-pose-swaps-native-vs-phone.png` @ `b06deaf` | `d317e5ac4188788bff09d2b59f87ef23003597874e0fd0f3b78df07fb680423c` |
| N6 — key fringe at 4x zoom | `qa/checker/lj/15-f258-key-fringe-zoom.png` @ `b06deaf` | `2a0e5afd81b590258d16fb8cf5ff024c1d4102eb01e205685a4ffef739472325` |
| P1 — the 'lookback' that faces forward (8.2 s) | `qa/checker/lj/05-f246-t8.20-lookback.png` @ `b06deaf` | `318b889187dc594faeab649c491106fde16d384dd202d5c305dc788488a815d8` |
| weak payoff — the tenant tag (22.9 s) | `qa/checker/lj/12-f687-t22.90-tenant-tag.png` @ `b06deaf` | `acde8a4be516d8a0711ee88d0c1d4e46154ce1a3b1441bf57a347d358e72297a` |
| weak payoff — the swarm colour flip (25.3 s) | `qa/checker/lj/13-f759-t25.30-swarm-flip.png` @ `b06deaf` | `ba5cc3f447b5db6c843c84ad878d4482694a815e16b923d4baa0b4e9fb0b19cd` |

## Context on other branches (cited, not validated by this case's `--source-ref`)

| Claim | where |
|---|---|
| Lane A's accepted film and its ledger (USD 0.529; the assets reused here) | branch work/agency-job-rentok-game-lane-a-001 at commit 7dab37a — case RENTOK-GAME-A-004 |
| CQ-001: blind rank D > C > B > A; prompt translation refuted; §6 the smallest consequential change; Treatment C's animatic and draw (USD 0.067) | branch work/experiment-rentok-creative-quality-001 at commit 41d97c694324b2cd22e119ad43b12fbbb4715efa — experiments/RENTOK-CREATIVE-QUALITY-001/07-DIAGNOSIS-AND-ROUTE.md and treatments/C-creative-direction/TREATMENT-C.md (local branch; worktree ../media-intelligence-rentok-cq) |
| Cumin B's animatic catch (ANIMATIC_BEFORE_SPEND count) | branch work/agency-job-cumin-exp-b-fivestage at commit 5c33173 — agency/jobs/AGY-2026-09-20-CUMIN-EXP-B-FIVESTAGE-001/LEARNING-PACKET.yaml (a rejected job, local branch, pending its own sync) |

## Not on disk (chat only)

- the customer's three messages ('Also, this is finally one amazinh outcome' / 'not required' / 'its already good') — transcribed by the Controller into `JOB.yaml` and `LEARNING-PACKET.yaml`;
- the list of the "six" defects the Controller put to the customer for the declined repair round;
- the Controller's instruction that "the video 4 way" = Treatment C (recorded as Controller-resolved in `JOB.yaml nr.ambiguity_markers`).
