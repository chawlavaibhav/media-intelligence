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

## Runner and dry run (2026-09-26 11:07 IST)
- run.py written (arms A/B/C + A_MAI, ledger with per-step and total caps, B5 code checks, studio finishing from worktree origin/claude/kitchen-v3 @ 11bfc5f at ~/Vaibhav_Personal_Projects/bakeoff-media/studio, venv at ~/Vaibhav_Personal_Projects/bakeoff-media/.venv). Media under ~/Vaibhav_Personal_Projects/bakeoff-media/run-2026-09-26 (outside git).
- Simulated dry run: all 16 briefs, all arms: 49 arm runs OK, 0 failures; make_pairs → 45 pairs (4 repeats). Bugs found and fixed in the dry run: video checks ran ffmpeg at error log level (black/freeze/loudness never reported — now proven on a black clip); freeze to end of clip not counted; long copy line overflowed the studio compositor (now retried wrapped at word breaks, same words and order).
- Implementation choices (not in TEST-FLOWS; decided now, before any output): A films = Veo text-to-video per scene, brief photos as Veo reference images on Veo standard (if Veo refuses refs with HTTP 400, US$0, resent without and logged); A stills aspect = the first ratio written in the brief, else 1:1; B/C aspect = B1's; A/B/C films 9:16; C reuses B's B1 output; writers never see the photos (the approved prompts give only the count), the picker sees a contact sheet; B5 stills that fail checks are left out of the pick (no extra draws); B5 film failure takes the one retake slot before the riskiest scene; MAI with photos uses its edits endpoint (all photos attached); finishing = studio still_ad / super_overlay (last 3.5 s of a scene with on-screen copy) / 2.5-s end_card only when there is exact copy or a logo; Lyria bed at 18% under native audio, loudnorm -16 LUFS; failed media calls are booked at their reserved price (conservative).
- Veo 3.1 reference-image request shape accepted by both Veo models (probe, US$0). MAI edits (multipart) smoke OK: 1 image.

## Practice (live)
- T1 done: B and C OK, US$0.27 each (4 Nano Banana draws + Vision OCR). Lint flagged both writers (124/135-word still prompts; negative phrasing) and one fix call cleared it.
- TUNING (practice only): lint's brand-name rule flagged "thali"/"dhaba" because they were capitalised in the offer line. Now brand names = exact-copy lines + web addresses/handles and their name part (mokobara.com → mokobara, @mousi.kitchen → mousi). Takes effect from the exam; T2–T4 have no brand copy.
- Observation (not a verdict): with a busy picture, the studio lockup shrinks the picture and extends the background to make a copy band (its designed behaviour), which leaves soft picture edges. Kept as-is (studio reuse).
- T2 done: B and C OK, US$2.41 each (2 Veo Fast 8-s takes). Projected practice total ≈ US$13.7 > the US$12 practice cap I derived from the founder's US$165. Stopped the run during T3's writer calls (no T3 media spent; in-flight Claude calls were subscription, US$0) and re-split within US$165: practice 14, stills 23 (estimate ≈ 20), films 128. Total unchanged.
- 11:27–12:51 IST: the Mac went to idle sleep; the T3 run stalled mid-call (a Nano Banana call and a Claude call hung ~84 min). Stopped; relaunching every process under `caffeinate -i`. T3 restarted from scratch (its 2 first-frame stills, ~US$0.13, stay in the ledger).
- 2026-09-26 12:55 IST — founder: "continue" / "you muse run mutliple agents for parallel work" — the steps now run as parallel processes: practice T3–T4, stills E01–E07, films E08–E10, films E11–E12. Consequences, stated honestly: (1) the exam starts before practice T3/T4 finish, so T3/T4 can no longer tune anything; the only practice tuning is the lint brand-name rule (from T1); (2) the ledger file is now shared under a cross-process file lock (each reserve re-reads it, so step and total caps hold across processes); results are written per brief and collected. Parallel simulated test: 4 processes, 622 ledger rows, 0 unsettled.

## Exam (live, parallel)
- E08 done: A US$3.60, B US$3.81, C US$3.81.
- E08 C: Lyria refused the writer's music line ("Minimal cool downtempo lo-fi bed, mostly texture — kept low so the ice-clink and pour sounds stay foregrounded.") with HTTP 400 "Request blocked for an unspecified policy reason". The runner shipped C's film without a music bed (by design: music failure never blocks). Not fixed mid-run (freeze). Known confound for E08 C vs B: B has a Lyria bed, C does not, for a provider refusal rather than a method difference. Booked at US$0.06 (conservative; a refused request is probably not billed).
