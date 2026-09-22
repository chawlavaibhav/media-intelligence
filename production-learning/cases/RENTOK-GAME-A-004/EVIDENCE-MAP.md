# EVIDENCE MAP — case RENTOK-GAME-A-004

Raw media is **not** duplicated here. Every claim points at a file on the job branch
`work/agency-job-rentok-game-lane-a-001` at its immutable HEAD `7dab37a` (full sha
`7dab37a70b004881a1ef9dea465b8aac41e6a979`), directory `agency/jobs/AGY-2026-09-20-RENTOK-GAME-LANE-A-001/`,
identified by path, commit and full sha256. Paths are relative to that directory. The branch name is provenance only; the
commit is what the validator reads.

Validate: `JOB_COMMIT=$(git rev-parse origin/work/agency-job-rentok-game-lane-a-001)` then
`python3 production-learning/tools/check_case.py --case production-learning/cases/RENTOK-GAME-A-004 --source-ref "$JOB_COMMIT"
--source-dir agency/jobs/AGY-2026-09-20-RENTOK-GAME-LANE-A-001` (fetch the branch first if the ref does not resolve).

## The delivered film and its superseded versions

| Claim | path @ commit | sha256 |
|---|---|---|
| the accepted film (final_asset; Video Y in the blind packet) | `gen/final/rentok-game-lane-a-9x16-30s.mp4` @ `7dab37a` | `9d50c4c5729f32d198fbaafc642fd78eccc0ee11dee2131cb637270584b5e24a` |
| repair-round-1 file (D-11: black end card) — superseded | `gen/final/v2/rentok-game-lane-a-9x16-30s.mp4` @ `7dab37a` | `5769ffa7232e6bb1427ce1f0db7396fedd12e9af58dc7feb5d61f140d20b0ab9` |
| first checker-reviewed file (D-1 two elst atoms) — superseded | `gen/final/v1/rentok-game-lane-a-9x16-30s.mp4` @ `7dab37a` | `6d418c10163e8af033cb3158173a5960d41a2ba4db061e3bdeb8dff039118168` |
| producer contact sheet of the delivered file | `gen/final/CONTACT-SHEET.png` @ `7dab37a` | `f210e4b25b78ec85aa81d4dcdec3e5e6037c8d7748d15e1c750a4ed744f4481f` |
| producer keyframes of the delivered file | `gen/final/KEYFRAMES.png` @ `7dab37a` | `6df0519f339eb4b3d15f1d791a7ed236a2d4d09ee96d1e7779f038d9d5db1374` |

The blind-packet copy the customer watched (`video-Y.mp4`, container metadata stripped) hashes differently
(`fb43de10…`, on the experiment branch below); its source sha256 in the sealed mapping is the accepted film's.

## Records, stages, ledgers, tools

| Claim | path @ commit | sha256 |
|---|---|---|
| the job record: brief verbatim, plan, spend, qa, versions[0] verdict verbatim, ttao stamps | `JOB.yaml` @ `7dab37a` | `bbec62cc628264df8bd86405873790b45551e12ac98d336929529ba9c3087135` |
| the producer's learning packet (observed facts, F-01..F-10, candidates) | `LEARNING-PACKET.yaml` @ `7dab37a` | `da3f6cf39b1969f1f13a799f72a3d3080f5f9a5c6a9328ab2d2428f9d6c1a33f` |
| append-only ledger: 8 reserved + 8 ok lines, USD 0.529 | `gen/LEDGER.jsonl` @ `7dab37a` | `671344251ecf676c187ac3b6b981623e3d83962cb40a0b0172e8d2e9d57d9fe5` |
| attempt mirror: 8 rows, latencies, artifact sha256s | `gen/ATTEMPTS.jsonl` @ `7dab37a` | `406e38c96bfc00b38546e0a04ad859364e5a262169325ced756d9a9f1aaa97a7` |
| independent checker: Stage-5 verdict D-1..D-10, re-verification R1–R4 (D-11) | `stages/CHECK-STAGE-5.md` @ `7dab37a` | `26be1eb3f0521deab53a2f04715740055e646055e14505ccce48221108c75f84` |
| independent checker: gate verdicts 1–4 before spend | `stages/CHECK-GATES-1-4.md` @ `7dab37a` | `92e83eb09415f94f9be1dbffb25b92137b39fc5c6801d453dc892990e7d309c9` |
| producer execution record incl. §9 repair statements and §9b honest note on D-11 | `stages/05-EXECUTION-AND-VERIFICATION.md` @ `7dab37a` | `25b580ed6164ee0a52727c6f08dead61f9921b1cd5f0370d0e4845bac423de2d` |
| production plan: code-rendered game, risk order, QA map, spend estimate | `stages/04-PRODUCTION-PLAN.md` @ `7dab37a` | `ed295b5de6cbe8f3b47eec3bc78a9fed1a5e5dbcb9c156e844dfe7b209939f99` |
| creative package: Canon claims by id, storyboard, copy deck, check lines | `stages/03-CREATIVE.md` @ `7dab37a` | `9c68ad6538f4064df95376e8c817586695b58259ed7bbb7fafced419e5f74ec6` |
| platform spec + safe-zone intersection ('no edit lists' row), permitted claims, brand colours measured | `stages/02-STRUCTURE.md` @ `7dab37a` | `4c881143aef80439c8c2e8e401b23d6f0e638dc81e56e5e3f7b3265b53b8525b` |
| intent contract M1–M11, flags, assumptions D1–D7 | `stages/01-INTENT.md` @ `7dab37a` | `5dd4e613bb6d818bcac8f08a6be25e16e6b83fa482a1692daa22a5ce7ecdb409` |
| the repaired board the delivered film was rendered from (beat times in ACCEPTED-TEMPLATE.yaml) | `board.json` @ `7dab37a` | `9be5c7671cccdd00242d455577b88e995c1afccbc3cec054a5067bf758932986` |
| the frozen 26-string copy deck | `copy-deck.json` @ `7dab37a` | `de0c25365554a67ca340a7f56b233a369bef935e2e1fcb207e7f7868ffd9d07b` |
| DET suite on the delivered file: 23 checks, 0 FAIL, D1 NOT_RUN | `qa/final-v6-audio/DET-RESULTS.json` @ `7dab37a` | `dc71d0a90a471f5437ff39d78587cf70bd9ff43196ee4dd813eb8a2962530ce2` |
| the USD-0 animatic gates that found R2a/R2b | `qa/animatic-v1/DET-RESULTS.json` @ `7dab37a` | `ea04ef6031429ff10b2e5114dda6ee3b88fa0b78538d9ab5fc0537640b5ac8e7` |
| the producer's DET suite incl. the post-D-1 elst box walk (count_atoms) | `tools/qa_checks.py` @ `7dab37a` | `094d5dfa7e8a3db8686ec04c45768502adf66b928a5e4c3a2041accbedda41fc` |
| the renderer (D-11 fix: hard-coded card colour) | `tools/render_game.py` @ `7dab37a` | `f9a819f081778289caf574d28951356b8489b8330c05d978f762a2c9dc4584f9` |
| the micro-qualified sprite sheet (att-001) | `gen/raw/A1_owner_sheet_att001.png` @ `7dab37a` | `f17060521a91db5699f957864c8b68bf831529ae698c7f4e5c00a2c9d4b4dcf9` |
| the Lyria bed (att-008) | `gen/raw/A10_music_att-008.wav` @ `7dab37a` | `8be3e70e5f368fd18f53eb965db48bcdd2514ef2311c5648f838b5be3a35ed4a` |
| the frozen customer brief (identical bytes on both lanes and the experiment branch) | `input/01-CUSTOMER-BRIEF-FROZEN.md` @ `7dab37a` | `65382cffe1d5632c354b2f1601c0e2b7c7d44539dbfaf350562e07b772cf5cc0` |
| the acceptance contract A1–A11 (identical on both lanes) | `input/03-ACCEPTANCE-CONTRACT.md` @ `7dab37a` | `43be9e133fe644790c2609ef34242535c0c77cdc30730a009232f719b42d3454` |
## Experiment context (not under the job directory; cited in prose, not as validator rows)

These files are on branch `work/experiment-rentok-two-lane-2026-09-20` (commit `594e7c9`, full
`594e7c9e041a2cb39c74058df4b17341ddec8762`). They are outside `--source-dir`, so they are listed with "at commit" wording
and their sha256 in a separate column; the validator does not resolve them.

| Claim | location | hash |
|---|---|---|
| experiment contract (design, isolation, §8 blindness limitation) | `experiments/RENTOK-TWO-LANE-2026-09-20/00-EXPERIMENT-CONTRACT.md` at commit 594e7c9 on `work/experiment-rentok-two-lane-2026-09-20` | sha256 `0c92a90daeaae8e88d76f81ca496b6e7daf0d491d057d417a91add80db09ff66` |
| USD 10 per lane, credits only, pool attested — the human's answers verbatim | `experiments/RENTOK-TWO-LANE-2026-09-20/SPEND-AUTHORISATION.md` at commit 594e7c9 on `work/experiment-rentok-two-lane-2026-09-20` | sha256 `38ea5134941124b715b120089523a242d6f944c98ffe83a8fdbb00df3964829d` |
| the customer's verdict transcribed verbatim before the mapping was opened | `experiments/RENTOK-TWO-LANE-2026-09-20/05-BLIND-PACKET/VERDICTS.md` at commit 594e7c9 on `work/experiment-rentok-two-lane-2026-09-20` | sha256 `0495f024e02c2666076f4faa3807a2d3cc3d07dfe32813c519dbef831aa1bc81` |
| sealed mapping X=B, Y=A with source sha256s (sealed 19:55:59Z) | `experiments/RENTOK-TWO-LANE-2026-09-20/05-BLIND-PACKET-SEALED/MAPPING.json` at commit 594e7c9 on `work/experiment-rentok-two-lane-2026-09-20` | sha256 `39365d6242e8f0a76c3ed48dbdf371f4135198c0ad117ff8afb40458b9cf935d` |
| packet file hashes (video-X 233e1818…, video-Y fb43de10…) | `experiments/RENTOK-TWO-LANE-2026-09-20/05-BLIND-PACKET/SHA256SUMS.txt` at commit 594e7c9 on `work/experiment-rentok-two-lane-2026-09-20` | sha256 `1ff04927903bee3a6be591311fc4df379171f2a0f7b4d5c206cd178aeb8f3044` |
| the Controller's comparison after the verdicts | `experiments/RENTOK-TWO-LANE-2026-09-20/06-CONTROLLER-COMPARISON.md` at commit 594e7c9 on `work/experiment-rentok-two-lane-2026-09-20` | sha256 `6ed94282ea78cbb908a5051e15b4fe7b18ed7859745ccf0da47a89c2f553721b` |
| the acceptance contract (same bytes as both lanes' input/03) | `experiments/RENTOK-TWO-LANE-2026-09-20/03-ACCEPTANCE-CONTRACT.md` at commit 594e7c9 on `work/experiment-rentok-two-lane-2026-09-20` | sha256 `43be9e133fe644790c2609ef34242535c0c77cdc30730a009232f719b42d3454` |
## Sampled frames and checker evidence

The job branch carries 891 PNG files (sampled frames under `qa/*/frames/`, the checker's `qa/checker/` frames and crops,
sprite cut-outs). They are not hashed individually here; the checker's cited frames are named by timecode in
`stages/CHECK-STAGE-5.md`, and the DET results that summarise the sampled frames are hashed above.

## What is not on disk

- The customer's chat message itself (only the Controller's verbatim transcription in `VERDICTS.md` and `JOB.yaml versions[0]`).
- The human Controller's chat authorisation of repair round 1 / round 1b (JOB.yaml says "Controller-authorised"; the words are not on disk).
- Any vendor statement (Google credits are not machine-readable; spend is the ledger's upper bound).
- A paid text-detector run over the sampled frames (D1 recorded NOT_RUN; producer and checker eyes only).
- A human ear on the music before the customer's (the checker could not listen).
