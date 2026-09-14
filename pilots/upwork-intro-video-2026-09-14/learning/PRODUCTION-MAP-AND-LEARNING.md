# Production map + media-intelligence learning — pilot `upwork-intro-video-2026-09-14`

Status: FIRST PASS ASSEMBLED, awaiting Controller judgment (ACCEPT / SPECIFIC REPAIR / REJECT).
Master: `assembly/v1/upwork-intro-first-pass.mp4` — 1920x1080, 24 fps, H.264 + AAC, 56.3 s, 22.8 MB,
−16.6 LUFS integrated, −1.0 dBTP. Spend: **USD 3.76 = ₹359** of the ₹3,000 cap (`gen/LEDGER-SUMMARY.md`).

## 1. Production map

| t | Scene | Purpose | Route / surface | Attempts | USD | Repair |
|---|---|---|---|---|---|---|
| 0.0–8.0 | T1 presenter (J-cut: finished ad up while the first sentence is spoken) | hook; service named inside 5 s; disclosure once | Veo 3.1 fast i2v + `generateAudio`, 1080p, Vertex credits, from NB2 still `gen/p0-presenter/p0-r2.png` | 1 | 0.96 | none |
| — | Presenter still | one identity for three takes | Nano Banana 2, Gemini API | 3 draws, r2 chosen | 0.20 | — |
| 8.0–11.0 | "Your brief." card | the input is one photo + one line | code | — | 0 | — |
| 11.0–17.0 | The ad builds itself (Ledge) | demonstrate a designed ad, exact text | NB2 4:5 textless plate `gen/a0-plate/a0-r1.png` + code (hb-view + Pillow) | 2 draws, r1 chosen | 0.13 | — |
| 17.0–20.0 | Four sizes | one layout → 4:5 / 1:1 / 9:16 / WhatsApp | code | — | 0 | — |
| 20.0–24.0 | Six hooks, Hindi flip | variants of an approved concept; Hindi once | code (Kohinoor Devanagari via hb-view) | — | 0 | — |
| 24.0–27.0 | The check (₹1,229 → ₹1,299) | reliability shown, legible to every buyer | code | — | 0 | — |
| 27.0–30.2 | Phone 1: Aarohi text-in-motion | the sold video deliverable, same brand | NB2 9:16 plate → MiniMax H3 Max i2v (fal cash) → code text per frame | 1 + 1 | 0.07 + 0.48 | — |
| 30.2–33.2 | Phone 2: Diwali sweets, code-set Devanagari | Hindi in motion, exact | **sealed** EVAL-040 topo3-video arm C composite r1 | 0 | 0 | — |
| 33.2–36.2 | Phone 3: juice macro + code-set offer | premium product clip with exact text | **sealed** EVAL-040 VID-T2V-04 Omni r1 + code overlay | 0 | 0 | — |
| 36.2–42.8 | T2 presenter (trimmed to 6.6 s) | process + the named human | Veo 3.1 fast i2v + audio, same still | 1 | 0.96 | none |
| 42.8–50.8 | T3 presenter | offer structure + CTA (window qualifier on frame) | same | 1 | 0.96 | none |
| 50.8–56.3 | End card | end on the package; CTA boss; brand once | code | — | 0 | — |
| bed | Music | inert, ducked under T2/T3 | **sealed** Lyria MUS-02 r1 looped with a 3 s crossfade | 0 | 0 | — |
| sfx | 14 snaps / tone / tick | sound events on frame 1 and each build step | synthesised (numpy) | — | 0 | — |

Every on-screen string comes from `plan/COPY-DECK.yaml` v4 (D3 check: 0 off-deck strings). Presenter words verified
verbatim against the script by transcript (triage tier) for each take and for the assembled film.

## 2. Self-check against `plan/ACCEPTANCE-CONTRACT.md` (Controller judges B, C1–C3 by eye and ear)
- A1–A7: pass by construction (supers word-identical; 24 h before 4 h; window on the T3 frame and the end card; no prices/metrics/clients/banned words; Adwisely once; Vaibhav named once).
- B1 one light direction: presenter still and both plates prompted "window light from the LEFT"; cards one type system; cuts only, one fade. B5: no thumbnail wall, no drone, no caps, no exclamation.
- C1 identity: frame checks at 0/1.5/3/4.5/6/7.8 s on all three takes — same face, hair, top, wall (CD's eye; Controller to confirm). C2 speech: transcripts match verbatim; cadence "natural", no defects flagged. C4 lettering: none seen in presenter frames or plates; the juice clip carries a generated "250 ml" label (accepted in the Lab; noted). C5: the insert ad at 0:00 is the ad the build finishes at 0:17 (same composer, same deck).
- D1–D6: 1920x1080 H.264/AAC 56.3 s 22.8 MB; −16.6 LUFS / −1.0 dBTP; music ducked to 0.28× under T2/T3 and silent after 55.8 s; D3 deck check clean; contrast: ink #17201C on cream #F5F1EA ≈ 15:1, cream on #1F4B3F ≈ 8:1 (computed from the hex values); no watermark; vertical ads shown whole inside phone frames.
- E1–E3: every ad is pipeline output (new for this film or sealed EVAL-040), "Demonstration · invented brands" on every work frame; the presenter says "I'm not real" and never claims to be the owner.

Known limits carried into judgment: speed is stated, not demonstrated (no real order timestamps exist yet);
Upwork's "video of you" rule is knowingly not met (Controller ruling 14 Sep); the profile overview still says
presenters are "not on the menu" while the film shows one (Nadia should reconcile the copy or the film should be
described as the studio's own showcase, not a sellable deliverable).

## 3. Concepts considered and rejected (Creative Director stage, USD 0)
- Two-hander with the owner's phone footage (recommended for the Upwork rule) — overruled: fully AI.
- Environment transforming around the presenter — rejected: identity through transformations is the weakest evidence; ambition moved into the ads ladder.
- Pure voice-over demo — rejected: weakest differentiation; ignores the owner's instinct for a face; VO voice ≠ presenter voice.
- AI likeness of the owner — rejected: reference-person 0/2, and it edges "should not mislead about who you are".
- Karl's REJECTs on v3 (Express without window; library triptych not evidence) fixed before spend; his WEAKENs (hook order, appositive, English check, poster frame, CTA as boss, demo label) adopted.

## 4. Canon knowledge that materially changed decisions
sk_ogx_0040 (open on the fire; few scenes → 12 shots not 30), sk_sb_c003_0015 (grunt test → service named first),
sk_whip_0035 + sk_ogx_0034 (disclose once, flatly; never repeat), sk_hop_sa_0048 (named person → "Vaibhav checks"),
sk_hop_sa_0051 (definite figures; no superlatives anywhere), sk_ogx_0042 (on-camera speech over VO; supers word-identical;
music inert, effects help → snaps on every build step, bed at 0.16×), sk_whip_0053 + CA-D1 (one boss per frame), sk_ogx_0028 +
sk_alb_c003_0005 (no caps, no reverse type over picture → supers on cream tabs, text on panels), sk_gote_c003_0029/0037
(cuts only; one fade at the end), sk_alt_c003_0011 (one light direction across presenter and plates), sk_sut_alc_0020 (the
price line as the close-up proof of care), pack limit + sk_nnn_0052 (Devanagari composited, Hindi copy originated not
translated), sk_ogx_0039 (end on the package). Full brief: `preprod/CANON-BRIEF.md`.

## 5. Proposed learnings (NOT Registry mutations; single commercial run)
**What the system got right.** Every route the shot map named worked first time: NB2 stills 5/5 usable, Veo 3.1 fast
i2v + native audio 3/3 (words verbatim, identity held within takes, lips in sync per transcript check), H3 Max plate
animation 1/1, code-set text exact everywhere. Cost per accepted film if accepted: **USD 3.76 (₹359)** — 12% of cap.

**What required human creative judgment.** Concept selection; script; the decision to reuse sealed clips and which
ones (Karl caught that the first picks were off-menu or generated-text); layout tuning by eye (four iterations on the
work segments); choosing the still and the plate; the ad anatomy itself (Jonah's Ledge doc).

**Capability evidence that was missing.** (a) i2v + native speech from an anchored still — UNTESTED before today; now 3/3
DIRECTIONAL on Veo 3.1 fast (proposed cell VID-I2V-SPEECH/veo-3.1-fast). (b) cross-take identity from a shared first
frame — 3 takes, held (proposed). (c) speech-transcript verification as a deterministic-ish gate — Gemini audio
understanding matched 4/4 (triage). (d) whether a 16:9 presenter cut with 9:16 ads in phone frames reads well on the
Upwork player — untested until uploaded.

**Canon knowledge missing.** Upwork/marketplace profile video conventions; AI-disclosed presenters; presenter shot size
and eye-line; muted-autoplay behaviour; captions for sound-off; 60 s pacing curves; motion typography (B12); audio (no
source at all — the music/effects decisions came from one Ogilvy line).

**Runtime features missing.** A `speaking-presenter` job family (Alpha-1 excludes it by C-7 — correctly; this pilot did
not widen it); per-frame code-set text on video as a runtime template (exists only as harness `composite.py` + this
pilot's `overlay_clip.py`); a deck-driven super/caption composer with word-identical enforcement; an assembly stage
(concat, bed, duck, loudness); a transcript gate for native speech; a library index of sealed accepted media with
"what it depicts" so reuse is a query, not a contact sheet.

## 6. Tools written for this pilot (all USD 0, deterministic)
`tools/adcomp.py` (Ledge composer, hb-view text, 4 formats, Hindi), `tools/film.py` (segments, supers, J-cut, deck
check), `tools/build_work.py`, `tools/overlay_clip.py` (RR-6 per-frame text on clips), `tools/assemble.py` (timeline,
bed, sfx, two-pass loudness), `tools/transcribe.py` + `tools/sentence_times.py` (triage transcript checks).
