# Portfolio samples 2026-09-15 — raw evidence index (archival branch `work/upwork-portfolio-samples-2026-09-15`)

This branch preserves, unrewritten, everything the lab produced for the Upwork portfolio tiles on 15 Sep 2026 after the
V4.1 film was accepted: paid generations (`gen/portfolio/`), the ledger lines (`gen/LEDGER.jsonl`, asset ids `pf-*`),
the per-asset records and verdict lines (`gen/ASSETS.jsonl`), the copy (`plan/COPY-PF.yaml`), the tools
(`tools/export_tiles.py`, `compose_v4.py`, `compose_pf.py`, `ad_9x16.py`, `portfolio_gen.py`, `nivaas_gen.py`, `nivaas_build.py`,
`nivaas2_gen.py`, `nivaas2_motion.py`, `nivaas2_build.py`, `speaker_check.py`) and the delivered export folder as handed to the
profile session (`portfolio-export/`, a byte copy of `~/Vaibhav_Personal_Projects/upwork-portfolio-media/` minus one duplicate
film file). The Controller's verdicts on the tiles were given in chat only; they are transcribed in the learning case, not here.

## Paid generations (from gen/ASSETS.jsonl, mechanical timestamps, UTC)

| asset_id | model | start | end | latency s | status | est USD | file | verdict lines |
|---|---|---|---|---|---|---|---|---|
| pf-ironleaf-packshot-r1 | openai/gpt-image-2 | 02:35:49 | 02:36:30 | 40.5 | ok | 0.053 | gen/portfolio/ironleaf-packshot-r1.png | accept (02:40:08Z) |
| pf-gyaan-plate-r1 | gemini-3.1-flash-image | 02:36:30 | 02:36:41 | 11.1 | ok | 0.067 | gen/portfolio/gyaan-plate-r1.png | accept (02:40:08Z) |
| pf-gyaan-motion-r1 | gemini-omni-1.1-flash-preview | 02:40:08 | 02:40:46 | 37.7 | ok | 1.0136 | gen/portfolio/gyaan-motion-r1.mp4 | accept (02:41:50Z) |
| pf-nivaas-story-r1 | veo-3.1-fast-generate-001 | 02:58:10 | 03:00:58 | 167.8 | ok | 1.5 | gen/portfolio/nivaas-story-r1.mp4 | accept (03:09:13Z); reject (03:14:25Z) |
| pf-nivaas2-ext-r1 | openai/gpt-image-2 | 03:16:09 | 03:16:50 | 40.3 | ok | 0.053 | gen/portfolio/nivaas2-ext-r1.png | accept (03:19:00Z) |
| pf-nivaas2-int-r1 | openai/gpt-image-2 | 03:16:50 | 03:17:29 | 39.8 | ok | 0.053 | gen/portfolio/nivaas2-int-r1.png | accept (03:19:00Z) |
| pf-nivaas2-ext-motion-r1 | veo-3.1-fast-generate-001 | 03:19:00 | 03:21:30 | 150.1 | ok | 0.96 | gen/portfolio/nivaas2-ext-motion-r1.mp4 | accept (03:25:36Z) |
| pf-nivaas2-int-motion-r1 | veo-3.1-fast-generate-001 | 03:21:30 | 03:24:11 | 161.3 | ok | 0.96 | gen/portfolio/nivaas2-int-motion-r1.mp4 | accept (03:25:36Z) |
