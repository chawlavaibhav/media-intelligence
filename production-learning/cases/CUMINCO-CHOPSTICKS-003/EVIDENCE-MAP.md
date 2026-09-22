# EVIDENCE MAP — case CUMINCO-CHOPSTICKS-003

Raw evidence lives on the archival job branch `work/agency-job-cuminco-chopsticks-001` at commit `de1f9783046d19f1c6dc5b92532c39f0bc008399` (directory `agency/jobs/AGY-2026-09-15-CUMINCO-CHOPSTICKS-001/`), never merged. Every row: path @ commit | sha256 of the blob at that commit.
Validate: `python3 production-learning/tools/check_case.py --case production-learning/cases/CUMINCO-CHOPSTICKS-003 --source-ref de1f9783046d19f1c6dc5b92532c39f0bc008399 --source-dir agency/jobs/AGY-2026-09-15-CUMINCO-CHOPSTICKS-001`.

| Claim | path @ commit | sha256 |
|---|---|---|
| the job record (brief verbatim, intake, NR, blueprint, plan, spend, QA rows, verdicts) | `JOB.yaml` @ `de1f9783046d` | `c9e6da63907972d197bb651b4d1b1f718f4ebb05bbd12ccd19f7b324914fa2ae` |
| the learning packet | `LEARNING-PACKET.yaml` @ `de1f9783046d` | `9cbc7fd4b964cfeda5f3159d5b8a43f416d981eeac79e76c35b3cd6c7b4cf0ed` |
| PRODUCTION-JOB-v1 brief (NR source) | `brief.job.json` @ `de1f9783046d` | `dc4ca7eec86e647100083c17e8870afadbfd708864e00a32065b554f17677fc3` |
| append-only ledger (reserve/settle lines) | `gen/LEDGER.jsonl` @ `de1f9783046d` | `08e141f0f9418554e0ecbf0de5da2a0f265e28817c7610e5f0929f5a46c46e15` |
| attempt records (one per paid call) | `gen/ATTEMPTS.jsonl` @ `de1f9783046d` | `34ca6f40472f995f38cfd92f90c7876ae27f7883f9460660729d8ee8e68dcea6` |
| every prompt as sent | `prompts/PROMPTS.yaml` @ `de1f9783046d` | `4eee8c10140e3db17305ccd2bfedbccd7e4f458c201c68f92b933833bae79748` |
| V1 9:16 (rejected) | `gen/final/cuminco-chopsticks-9x16.mp4` @ `de1f9783046d` | `097e428e5929f1bd10d71bc68479dcbe6e011803629b198b616858e17b205d9d` |
| V2 9:16 (rejected) | `gen/final/v2/cuminco-chopsticks-9x16.mp4` @ `de1f9783046d` | `adaeaa37e4c647a9ac24e986d8124ca6f86265172d23194019333db437693f8a` |
| V3 9:16 (rejected — 'voices overlapping') | `gen/final/v3/cuminco-chopsticks-9x16.mp4` @ `de1f9783046d` | `85d7410e8bc52717b4630944a5c3664cddf54ba776d43a689cfa9e9e766e67ae` |
| V3 QA report (gates on the actual file) | `gen/final/v3/cuminco-chopsticks-9x16.qa.json` @ `de1f9783046d` | `9a134a78bb47dd9cc4a99671a64e730bb25afc8d25d9095a2801cbbbd9a6fc07` |
| accepted plate H1 (r2) | `gen/plates/plate-H1-accepted.png` @ `de1f9783046d` | `dcd267915401d9e384051c1ad3a6fe6e108f08cdca76f26a049e94725427edf1` |
| accepted plate A (r2) | `gen/plates/plate-A-accepted.png` @ `de1f9783046d` | `9f4d17c39753d2d2efbdab0bc4c16c9576743f0cdf50848db2e1b2110790536e` |
| rejected plate A r1 (garbled mark) | `gen/plates/plate-A-r1.png` @ `de1f9783046d` | `4f1bfc20c16c94f4f1d348b6ca343cf79f10e8fa945e712196ff06456e32f025` |
| accepted clip-2 | `gen/clips/clip-2-accepted.mp4` @ `de1f9783046d` | `706aa3cf445ac44c005da79673a4347fe4027567a7eba33e2a6e6cbe22a90ff5` |
| clip-1 r2 (closed-mouth regen) | `gen/clips/clip-1-r2.mp4` @ `de1f9783046d` | `6ebc713d7fbc5add33f2a914d56452b52e3c03437b081d80858835e546bb41f7` |
| clip-5 r2 | `gen/clips/clip-5-r2.mp4` @ `de1f9783046d` | `bb85d928a0c35959527106710dbd860282b063ce376b24fc7950459989b67ce2` |
| chosen voice reference (Leda bubbly) | `gen/vo/r5-leda-v2-bubbly.wav` @ `de1f9783046d` | `e514ee17627c97cc6168d9c6b50c7e9c52a37e10e82ea26445d31042fc6a1d5c` |
| VO line b1 (5.32 s after trim — the overlap) | `gen/vo/final-b1.wav` @ `de1f9783046d` | `6f0b7f56ffd435582b5a512fddfee019033d819e3c031334fed9d5083ac5c488` |
| spoken close b6 (overran the film) | `gen/vo/final-b6.wav` @ `de1f9783046d` | `2b3f06009084300f386ceb45f25dad14356d4160f30238b0e01a1512193b7549` |
| music bed | `gen/music/bed-r1.wav` @ `de1f9783046d` | `d76e85ebde91e24a9e432cc79eb0b49f9953e93225ad9d517459a2113a6f809a` |
| job dispatch tool (ledger + cap + classifier) | `tools/dispatch.py` @ `de1f9783046d` | `84d691ef69325619748bc9a96094166f1dfdcdcca47af98d4caf0d118755a7c3` |
| job composition tool (gates, obstruction, audio chain) | `tools/compose.py` @ `de1f9783046d` | `00e7385fa1ac10c6addfddc088a3fc5a8b6b704d2d00421f579ed346bcc65a26` |
| V3 contact sheet | `qa/final-9x16-v3-contact.png` @ `de1f9783046d` | `8bcff1a3049887735891ae6d58cb244545694b36af296f55a425d2c7cc806139` |
| V1 contact sheet | `qa/final-9x16-contact.png` @ `de1f9783046d` | `2b822d27e66897a6586c0fadfff84d269db5e26815bb651b26b2b8e390df361a` |

## What is not on disk
- the user's verdicts (chat only; transcribed in HUMAN-VERDICTS.yaml)
- the user's listening of the voice takes (chat only)
- vendor statements (unreconciled; ledger figures are upper bounds)
- the prior cloud session's unpushed branch (Downloads/HANDOFF.md; its concept was superseded by the user's re-brief)
