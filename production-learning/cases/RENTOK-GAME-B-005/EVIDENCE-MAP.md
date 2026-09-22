# EVIDENCE MAP — case RENTOK-GAME-B-005

Raw media is **not** duplicated here. Every claim points at a file on the job branch
`work/agency-job-rentok-game-lane-b-001` at its immutable HEAD `d0a0583` (full sha
`d0a0583d3372c6f7c49fdeee18643d4cb860cd67`), directory `agency/jobs/AGY-2026-09-20-RENTOK-GAME-LANE-B-001/`,
identified by path, commit and full sha256. Paths are relative to that directory. The branch name is provenance only; the
commit is what the validator reads.

Validate: `JOB_COMMIT=$(git rev-parse origin/work/agency-job-rentok-game-lane-b-001)` then
`python3 production-learning/tools/check_case.py --case production-learning/cases/RENTOK-GAME-B-005 --source-ref "$JOB_COMMIT"
--source-dir agency/jobs/AGY-2026-09-20-RENTOK-GAME-LANE-B-001`.

## The delivered film and its superseded version

| Claim | path @ commit | sha256 |
|---|---|---|
| the accepted film (final_asset; Video X in the blind packet) | `gen/final/rentok-game-lane-b-9x16-30s.mp4` @ `d0a0583` | `40cf2f40bf50c88d04afebb98ea91f6896a83aac8ad4fbdc010b0e289eb42c78` |
| the file the checker reviewed (D-1..D-8) — superseded by repair round 1 | `gen/final/v1/rentok-game-lane-b-9x16-30s.mp4` @ `d0a0583` | `d9d437d3a83411d6b1e0776f83edd974d6e807bb55953184c72f09f5a6b89df1` |
| producer contact sheet of the delivered file | `gen/final/CONTACT-SHEET.png` @ `d0a0583` | `0f932205e00322a0668ab31c7266df0ceefc31e841b0bc54bf64c320ab5e2884` |

The blind-packet copy the customer watched (`video-X.mp4`, container metadata stripped) hashes differently
(`233e1818…`, on the experiment branch below); its source sha256 in the sealed mapping is the accepted film's.

## Records, stages, ledgers, tools, audio

| Claim | path @ commit | sha256 |
|---|---|---|
| the job record: brief verbatim, plan, spend (25 attempts, pool_label_discrepancy), qa, versions[0] verdict verbatim, ttao stamps | `JOB.yaml` @ `d0a0583` | `329a2210b402e84d64f530971c56463c333a116a8eab4aeecad1b20224df1712` |
| the producer's learning packet | `LEARNING-PACKET.yaml` @ `d0a0583` | `a89eabca0124188dd8582f7edc1e4e48e1602aef9f98a185d7643d94e895902a` |
| append-only ledger: 25 reserved + 25 settle lines, USD 0.58675, 3 failures kept | `gen/LEDGER.jsonl` @ `d0a0583` | `d489d4b517d25ab47dfbe3c4ae0f8d097d9d91643709a7627b5d6fa1da25ecd2` |
| attempt mirror: 25 rows incl. att-006 (HTTP 401 quota), att-013 (PROHIBITED_CONTENT), att-016 (local_fault) | `gen/ATTEMPTS.jsonl` @ `d0a0583` | `1f9747c900be455c4b931ec9891ae4cfd7a000ffe77a61b2b36a2771091d1329` |
| independent checker: Stage-5 verdict D-1..D-8, re-verification (D-9, N-1..N-3) | `stages/CHECK-STAGE-5.md` @ `d0a0583` | `ee2f6f329edc73f1d2bf21c1bb7afd3652b393c19e36e05469f8b8e938ecb05a` |
| independent checker: gate verdicts 1–4 (REOPEN 1 nameplate, REOPEN 2 pool labels) | `stages/CHECK-GATES-1-4.md` @ `d0a0583` | `400bf6e0629782597927c494f63a4fc64daa8b9ba350b94ca0110231d5d8f890` |
| producer execution record incl. repair round 1 | `stages/05-EXECUTION-AND-VERIFICATION.md` @ `d0a0583` | `4fd700257d8bf04985474eeceba693e4eda0977edd574823708d1eee078044d7` |
| production plan: stills → code, no video model, voice audition plan | `stages/04-PRODUCTION-PLAN.md` @ `d0a0583` | `306e7becf5ed1e1e9a6c78502b5a78c9fc1a6306342eec88109187fba2a47a67` |
| creative package incl. CHANGES-FROM-SUPPLIED-DIRECTION (10 changes), storyboard F1–F17, copy deck | `stages/03-CREATIVE.md` @ `d0a0583` | `f0e29bdc7f4f6cbccd000afb8ed5d4f2ca587c54b7680328d2e1d368fb033ddb` |
| platform specs, safe zones, permitted claims, brand colours | `stages/02-STRUCTURE.md` @ `d0a0583` | `118e7341aafa11fad67b7342fee870c2fa88ad6a6bceb404c96fbe953567e055` |
| intent contract | `stages/01-INTENT.md` @ `d0a0583` | `f8e87b245650e09fb3b97429bd1904f2897e82c5e5e7e7b7f4fd9428cec4552c` |
| beat times and measured VO starts/durations (V2 at 15.9 s after D-3) | `gen/render/TIMELINE.json` @ `d0a0583` | `5ee8fb123e52133cc88cc2ef7d2d9311f763b4c972c34cbb883068a597444caf` |
| per-frame layout log incl. G-* graphic boxes (the D-1/D-9 disjoint extension) | `gen/render/LAYOUT.json` @ `d0a0583` | `8df7ef17fb533a7fd8f0a6e7b472613aca63206af07e0d1aeb7c6651cf1e78fd` |
| mix report with the VO schedule gate result | `gen/audio/MIX_REPORT.json` @ `d0a0583` | `c721ff99d90a157bd8a1163556ed5cd0efbb240d24b3d5c2f022de1dfc6ad0d4` |
| the producer's QA report on the delivered file | `qa/QA-REPORT.json` @ `d0a0583` | `0c8999fd7009862ac1a0868760f4fbac8226b27199cc992b778a962527e89aad` |
| micro-qualification card (item 1 corrected after D-4) | `qa/A1-microqual-card.md` @ `d0a0583` | `7e488602db8b93fc22526e7eeab519289ba5f46f3c005c9a0236acc1fc9fbc6a` |
| the producer's DET suite incl. graphics in the disjoint set | `tools/qa_checks.py` @ `d0a0583` | `c8f2e16cc459c041d3e71809de6c7ce7edc69d0331058b6533ec681c1fc6388a` |
| the dispatcher (T1 fix: input checked before reserving) | `tools/dispatch.py` @ `d0a0583` | `749998c391d2a11c024fdb62707c4572e489cdf3ef9dd6da9cc6aa414110465b` |
| VO overlap/overrun gate ported from PR #103 (does not check text alignment — D-3) | `tools/vo_schedule_gate.py` @ `d0a0583` | `1b7ef2e1cf6725566345846fd8c9385966c442db73539ed83f25d5fedcc7625e` |
| the mixer (loads A_sarvam_*.wav only — one voice source, checker-verified) | `tools/mix_audio.py` @ `d0a0583` | `0adb6f73daf736b7a1f77a213ebdaf76faee581dcec5bffedef887a582c20f60` |
| selected announcer line 1 (att-001) | `gen/voice/A_sarvam_V1.wav` @ `d0a0583` | `96dae055199d36922116a27e4bb0df9ec9cdc540a49c27d01fea5ab6e2758c6e` |
| selected announcer line 2 (att-002) | `gen/voice/A_sarvam_V2.wav` @ `d0a0583` | `fc9340e8e9cb70bb7c157deb3f050e0a6eb9cfd076d4ee8bf7381f863b9cec2f` |
| selected announcer line 3 (att-003) | `gen/voice/A_sarvam_V3.wav` @ `d0a0583` | `d041cabecf3d7d15b6fdf04882f7fe3315cc1b803035dbb306f950f558263e0d` |
| the Lyria bed (att-025) | `gen/audio/A6_lyria_v1.wav` @ `d0a0583` | `dba70af68d56b05667681c1c0a6f3ddec949ac40eeaadcb53496ff34380fbbbe` |
| the frozen customer brief | `input/01-CUSTOMER-BRIEF-FROZEN.md` @ `d0a0583` | `65382cffe1d5632c354b2f1601c0e2b7c7d44539dbfaf350562e07b772cf5cc0` |
| the ChatGPT direction (lane B only; a proposal to verify, not a contract) | `input/02-CHATGPT-DIRECTION-LANE-B-ONLY.md` @ `d0a0583` | `d8ea48c57646137748e6fca216077c471948099359380c2d4d41ebc49cd833d5` |
| the acceptance contract A1–A11 | `input/03-ACCEPTANCE-CONTRACT.md` @ `d0a0583` | `43be9e133fe644790c2609ef34242535c0c77cdc30730a009232f719b42d3454` |
## Experiment context (not under the job directory; cited in prose, not as validator rows)

Branch `work/experiment-rentok-two-lane-2026-09-20`, commit `594e7c9` (full `594e7c9e041a2cb39c74058df4b17341ddec8762`).
Outside `--source-dir`, so listed with "at commit" wording and the sha256 in a separate column; the validator does not
resolve them.

| Claim | location | hash |
|---|---|---|
| experiment contract (design, isolation, §8 blindness limitation) | `experiments/RENTOK-TWO-LANE-2026-09-20/00-EXPERIMENT-CONTRACT.md` at commit 594e7c9 on `work/experiment-rentok-two-lane-2026-09-20` | sha256 `0c92a90daeaae8e88d76f81ca496b6e7daf0d491d057d417a91add80db09ff66` |
| USD 10 per lane, credits only, pool attested — the human's answers verbatim | `experiments/RENTOK-TWO-LANE-2026-09-20/SPEND-AUTHORISATION.md` at commit 594e7c9 on `work/experiment-rentok-two-lane-2026-09-20` | sha256 `38ea5134941124b715b120089523a242d6f944c98ffe83a8fdbb00df3964829d` |
| the customer's verdict transcribed verbatim before the mapping was opened | `experiments/RENTOK-TWO-LANE-2026-09-20/05-BLIND-PACKET/VERDICTS.md` at commit 594e7c9 on `work/experiment-rentok-two-lane-2026-09-20` | sha256 `0495f024e02c2666076f4faa3807a2d3cc3d07dfe32813c519dbef831aa1bc81` |
| sealed mapping X=B, Y=A with source sha256s (sealed 19:55:59Z) | `experiments/RENTOK-TWO-LANE-2026-09-20/05-BLIND-PACKET-SEALED/MAPPING.json` at commit 594e7c9 on `work/experiment-rentok-two-lane-2026-09-20` | sha256 `39365d6242e8f0a76c3ed48dbdf371f4135198c0ad117ff8afb40458b9cf935d` |
| packet file hashes (video-X 233e1818…, video-Y fb43de10…) | `experiments/RENTOK-TWO-LANE-2026-09-20/05-BLIND-PACKET/SHA256SUMS.txt` at commit 594e7c9 on `work/experiment-rentok-two-lane-2026-09-20` | sha256 `1ff04927903bee3a6be591311fc4df379171f2a0f7b4d5c206cd178aeb8f3044` |
| the Controller's comparison after the verdicts | `experiments/RENTOK-TWO-LANE-2026-09-20/06-CONTROLLER-COMPARISON.md` at commit 594e7c9 on `work/experiment-rentok-two-lane-2026-09-20` | sha256 `6ed94282ea78cbb908a5051e15b4fe7b18ed7859745ccf0da47a89c2f553721b` |
| the acceptance contract (same bytes as both lanes' input/03) | `experiments/RENTOK-TWO-LANE-2026-09-20/03-ACCEPTANCE-CONTRACT.md` at commit 594e7c9 on `work/experiment-rentok-two-lane-2026-09-20` | sha256 `43be9e133fe644790c2609ef34242535c0c77cdc30730a009232f719b42d3454` |
## Roster and routing-map labels (the PD-02 discrepancy), verified in this checkout at `origin/main @ 4d919c9`

- `eval/empirical-planning/ROSTER-REFRESH-2026-09.yaml`: `sarvam-bulbul-v3` and `elevenlabs-v3` carry `billing_pool: cash`.
- `eval/capability-map/ROUTING-EVIDENCE-MAP-v0.yaml`: pools listed as `sarvam_credits` and `elevenlabs_credits`.
- Neither file is edited by this branch; the reconciliation is a proposal in `PROMOTION-QUEUE.yaml`.

## Sampled frames, stills and checker evidence

The job branch carries 69 PNG files (the seven stills, sprite slices, the checker's `qa/checker/` frames and crops, the
producer's sampled frames). They are not hashed individually here; the stills' hashes are on the attempt rows in
`gen/ATTEMPTS.jsonl` (checker: all 22 artefact hashes re-hash to the files on disk).

## What is not on disk

- The customer's chat message itself (only the Controller's verbatim transcription).
- Any human ear on the voice audition or the music before the customer's.
- A run of the pre-dispatch prompt gate (`A1: NOT_RUN`, recorded by the producer).
- Any vendor statement (only the Gemini routes report usage).
- The human Controller's chat authorisation of repair round 1 (JOB.yaml records the round; the words are not on disk).
