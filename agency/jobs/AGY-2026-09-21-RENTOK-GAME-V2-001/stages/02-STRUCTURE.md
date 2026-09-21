# Stage 2 — Structure and facts (carried over from AGY-2026-09-20-RENTOK-GAME-LANE-A-001 @ 7dab37a, re-verified)

Job `AGY-2026-09-21-RENTOK-GAME-V2-001`. The full record is `source/lane-a/02-STRUCTURE.lane-a.md` (byte-identical copy, sha256 in `PROVENANCE.md`); its evidence files are copied into this job: `source/platform/*` (with `SHA256SUMS.txt`), `source/rentok-brand/*` (with `SHA256SUMS.txt`), and the Controller's frozen snapshot `source/rentok-snapshot/*`.

## Re-verified in this job (OBSERVED 2026-09-21, by re-reading this job's own copies)

| Item | Lane A value | Re-check | Result |
|---|---|---|---|
| Snapshot integrity | `source/rentok-snapshot/SHA256SUMS.txt` | `shasum -a 256 home.html` = `17019dcf…` = the listed value | matches |
| Brand spelling (flag F5) | `RentOk` in the raster wordmark; typed strings in capitals (`RENTOK`, spelling-neutral) | `grep -c RentOk home.txt` = 3; `grep -o RentOK *.txt` = 0; `home.txt:1` = "RentOk \| PG/Hostel/Flat Management App" | **kept**: wordmark raster `RentOk`, capitals elsewhere |
| Safe zones | IG/FB 14 % top / 35 % bottom / 6 % sides; YouTube figure 288 / 672 / 48 / 192; intersection **(65,288)–(888,1248)** | `ig-reels-ads-guide.txt` contains "14% of the top, 35% of the bottom, and 6% on each side"; `yt-vertical-safe-area-figure.svg` contains 288, 672, 192 (48 present as the left margin) | **kept**: critical text/logo boxes inside (65,288)–(888,1248); the WORLD fills the full 1080×1920 (the CQ-001 lesson: the box bounds critical elements, not the art) |
| Permitted claims used by the copy deck | `DIGITAL KYC` ← home.txt:99 · `AUTOPAY` ← home.txt:19–20, autopay.txt:4–5 · `DUES TRACKED LIVE` ← autopay.txt:104–107, 136; home.txt:104 · `ONE DASHBOARD` ← autopay.txt:95 · `COMPLAINT TICKETS` ← complaint-management.txt:10 | each line re-read at the cited line number in this job's `.txt` extracts (`sed -n`) | all five lines say what the deck claims; **kept** |
| Forbidden claims (A11) | guarantee(d), 100%, never, no more (promise), zero+problem, prevent, recover(y), eliminate, all/every problem, always, any %, numerals attached to outcomes; Nintendo/Mario/Luigi/Mushroom Kingdom | list copied into `tools/qa_checks.py FORBIDDEN` (unchanged) | **kept** |
| IP do/don't table (2c) | original owner (no cap/overalls/moustache-signature), phone power-up (no mushroom/star/flower), problem-shaped obstacles, PG street world (no ? blocks, pipes, castle), plain pole + blue tick flag, original type/music/SFX, words "Mario/Nintendo" never on screen or in a prompt | applied again to every asset this job reuses or draws (Stage 4 §4.2 consistency card) and to the C renderer's generic "?" (on the document wall = the unknown tenant; not a block) and the "hearts"-free health bar (▮▯ segments) | **kept**; the new-sheet prompt is grepped by `dispatch.py _prompt_guard` for the IP words |
| Publishing spec 2.1 | 1080×1920, MP4 moov-first, no edit lists, H.264 High 4:2:0 30 fps ≈ 9 Mbps, AAC-LC 48 kHz 192 kbps stereo, 30.0 s | encode flags in `tools/render_v2.py` / `tools/assemble.py` are Lane A's (`-use_editlist 0`, `+faststart+negative_cts_offsets`) | **kept** |
| Audio 2.6 | muted-first yes; original Lyria bed; code SFX; −14 LUFS / TP ≤ −1 dBTP | same targets; the bed is now processed per beat (Stage 3) — still original audio | **kept** |
| 2.7 one geometry | one 9:16 master serves the three placements | unchanged | **kept** |

Nothing in the snapshot, the platform pages or the brand file was re-fetched (no need: the frozen files are the evidence, and their hashes match). No new fact is asserted from memory.

Not a verdict. Written by the producer session.
