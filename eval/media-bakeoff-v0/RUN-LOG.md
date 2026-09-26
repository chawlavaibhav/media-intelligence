# Bake-off v1 run log

## Founder overrides
- 2026-09-26 10:29 IST — founder: "claude models come from the claude subscription" — changes: every Claude call (A1/A3 writer, B2/B6 writer, C0 librarian, C2/C2b writer) goes through the `claude` CLI on the founder's subscription (headless: own system prompt, no tools/MCP/hooks/memory, empty cwd), not ANTHROPIC_API_KEY. Cash cost of those calls is recorded as US$0; tokens are still logged.

## Pre-flight (2026-09-26 10:29 IST)
- preflight.py: READY only when ~/.mi-keys is sourced in-command (session was not started with it). GOOGLE_API_KEY yes, Vertex SA yes, no Azure keys in ~/.mi-keys.
- prompts/: all 16 re-rendered byte-identical (T1–T4, E01–E12).
- Google models listed for the key: veo-3.1-generate-preview, veo-3.1-fast-generate-preview, gemini-3.1-flash-image, lyria-3-clip-preview, gemini-3-flash-preview. Both Veo endpoints accept auth (deliberately invalid request → HTTP 400 validation, US$0).
- Nano Banana 2 live smoke: 1 image OK (~US$0.067).
- ANTHROPIC_API_KEY in ~/.mi-keys: HTTP 401 "API key is invalid" (now moot: subscription override).
- Claude CLI subscription: `claude auth status` → loggedIn false; headless call → "OAuth session expired". Needs the founder to log in.
- Azure aight-studio-ai (getaight sub, ~/.mi-studio-keys): gpt-5.6-luna OK (13 tokens). Deployments: gpt-5.6-sol/terra/luna, Kimi-K2.6. MAI-Image-2.6 NOT deployed.
- Photos: all on origin/work/agency-job-mokobara-odyssey-001; E01's Private_Island_3 file is named with dashes (The-Transit-Backpack-30L_Private-Island-3_…jpg) — mapped, same photo.
- Finishing: studio compose (origin/claude/kitchen-v3) needs Pillow+raqm; venv made at ~/Vaibhav_Personal_Projects/bakeoff-media/.venv (Pillow 12.3, raqm yes); Devanagari font Kohinoor.ttc present.
- Runner: none exists on the branch yet (HANDOFF step 1). To build, then dry-run T1–T4 simulated.
- Pre-flight spend so far: ~US$0.07.
- 2026-09-26 10:35 IST — founder: "MAI was hosted for llm gateway. if not there, you host the mAI model" — MAI not found on any aight-* Foundry/OpenAI account (gateway included). MAI-Image-2.6 is offered in eastus only; founder ran the create/deploy himself (my attempt was blocked by Claude Code's classifier). New: AIServices account aight-bakeoff-mai-eus (RG aight-studio, eastus, getaight sub), deployment MAI-Image-2.6 (2026-07-31, GlobalStandard cap 1). Key read via `az ... keys list` inside the command only.
- MAI-Image-2.6 smoke: 1 image OK via POST /mai/v1/images/generations (1024x1024, 39 s).
- 2026-09-26 10:52 IST — founder: "i am already logged in claude" / ran `claude auth login` — CLI now logged in as the subscription account; Sonnet 5 headless call OK (model claude-sonnet-5).
- 2026-09-26 10:52 IST — founder: "Apple duo photos to be picked from interent" — E09 now attaches 3 of Apple's official photos from apple.com/in (downloaded 24 Sep for the iPhone Duo job, ~/Vaibhav_Personal_Projects/iphone-duo-ad/apple/): hero (open, in hands), design_hero (folded + open), display (folded). BRIEFS.yaml E09 assets + asset_dir set; prompts/E09.md re-rendered (photo count 0 → 3). Same photos to every arm.
- 2026-09-26 10:52 IST — founder: "Go for 165 dollars" — total cap US$165 (was 115); practice film T3 on Veo 3.1 Fast (was standard). Per-step caps: practice $12, stills-type exam $25, films $128. Read as GO for the run once the simulated dry run passes.
- render_prompts.py refactored into build() (used by run.py); all 16 re-rendered byte-identical before the E09 change.
