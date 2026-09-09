# Video piece 1 — text into motion (VID-TOPO3-01): observations before the Controller's verdicts (2026-09-09)

Recorded by the Writer Controller from extracted frames (0.5 s, 3 s, 5.5 s) of the sealed clips. Product evidence;
the Controller's blind verdicts (judging-video/) decide acceptance. Spend: smoke USD 0.48 + lane USD 9.74.

| Arm | Route | What the frames show |
|---|---|---|
| A — cheap still (Qwen 9:16 plate, draw 2) → cheap image-to-video | MiniMax H3 Max (768×1344, 6.6 s) | The plate's lettering stays crisp and stable through the whole clip; the diya flames animate. The plate's own spelling errors ("कली", "मिंष्टान") carry over unchanged. |
| A | Wan 3.0 Prime (720×1280, 6 s) | Same: lettering preserved and stable; gentle motion. |
| B — premium video model writes the Hindi itself | Veo 3.1 full (720×1280, 6 s) | Fluent-looking but entirely fabricated Devanagari ("यास्बी यादन प्रुोलो…"); stable across frames; the "20%" survives. Not readable as Hindi. |
| B | Kling v3 Pro (1080×1920, 6 s) | Pseudo-Devanagari with Latin fragments ("शोRAW रो…"); stable; unreadable. |
| C — textless plate (FLUX 9:16) → cheap i2v → exact strings by code on every frame | H3 Max + composite.py --video | All three strings exact and crisp on every frame; the animation of the textless plate itself put flame-like tips on the sweets (a motion artefact of the plate, not of the text). |

What this already says, pending verdicts: exact Devanagari through motion comes from **carrying a correct still into a
cheap animator** (arm A) or **setting the type by code on an animated plate** (arm C); the premium native route (arm B)
cannot write Hindi at all in this test. The remaining defect on arm A is upstream: the cheapest text route (Qwen) misspelled
both 9:16 plates, where Nano Banana 2 spelled the square poster correctly twice in round one.
