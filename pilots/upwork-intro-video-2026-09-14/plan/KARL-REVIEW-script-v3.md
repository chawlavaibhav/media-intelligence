# Karl review — SCRIPT v3 (before any spend)

Checked against COMMERCIAL-BRIEF §5/§7/§9, CANON-BRIEF §2/§3/§8/§10 and the EVAL-040 ledgers for the three sealed clips (frames viewed).

## 1. Hook "I'm not real. The ads are." — WEAKEN
Strongest attack: the first legible words, beside a face that is not the profile photo, are "I'm not real." On mute that is a deepfake caption, not candour; the pivot lands only when the Aarohi insert appears at 2.5 s. The service is named by 5 s only if eight words are read in 2.5 s over a phone-frame insert. Gimmick risk is bounded: Canon supports disclosing once, flatly, and it is never repeated. Fix: make the service line the first legible super and let the disclosure follow inside the same take (T1-alt, order reversed). Also "brands" names one of three buyer types; media buyers and agencies (§3) go unnamed.

## 2. Claims vs matrix — REJECT as written (fixable)
- **"Express: four." at 43.5–51.5 has no window on that frame.** The header promises "only with the IST window on the same card"; the timeline puts the window on the end card six seconds later. Brief rule: 4 hours never without the window. Fix: window line on the T3 super, or use T3-alt.
- End card prints Express before Standard; the owner's order is Standard first.
- No "demonstration / invented brand" label anywhere; §8 requires one.
- Nothing banned on screen; no service price, no metric. "Adwisely" on the end card silently settles open question 3, unruled.
- Header says 63 spoken words; the lines total 56–58.

## 3. "Vaibhav — the human — checks every file" — WEAKEN
An AI announcing that a human exists is Canon's "made with real cheese" reassurance tell (sk_whip_0035); dashed on a super it reads as a wink. The name is fine; the profile is "Vaibhav C.". Fix: "Vaibhav checks every file before it reaches you."

## 4. Structure and pacing — WEAKEN
Fourteen pieces in 57 s; the work section is eight consecutive 3–4 s shots, the montage Canon §8 names first. It is the overview's bullet list in order; it proves differentiators 2 and 4 and only asserts differentiator 1: the v2 brief's central instruction, "dramatise the clock, not the technology", has no clock anywhere. Defensible without real timestamps, but speed then rests on two spoken numbers. The check beat corrects a Devanagari glyph the US/UK buyer cannot read, in 3 s, in a small player: evidence value nil for most buyers. Fix: check the English price or date line. Cut first: the phone triptych (27–36 s), see item 5; that returns 9 s to the build and check.

## 5. Sealed lab clips — REJECT the triptych as evidence
Ledger facts. (a) The "Hindi text-in-motion sweets ad" is `topo3-nb-video`, arm `A2_nb_still_to_cheap_i2v`, `composited: false`: Nano Banana generated the Devanagari, its sister plate was rejected for two "श्री", and the i2v prompt says "any lettering stays perfectly still". Neither text-in-motion nor code-set; it breaks Canon rule 12 and the exact-text promise on the beat right after the check. The composited variant (`topo3-video`, arm C, "no mistakes") is the only usable one. (b) The Kling couple story has no product, text or brand in any shot: a people-led lifestyle spot, while "product, text and scene ads only" is live copy. (c) The juice macro: blank label, no offer, a model demo. Four visual worlds with one designed anatomy reads as a stock reel, and Upwork tells buyers to check portfolio authenticity. Fix: one clip, code-set text, Aarohi anatomy.

## 6. Production-risk honesty — WEAKEN
The 6/6 native-speech result is text-to-video (VID-T2V-01 farmer). No image-to-video take with native speech from an anchored still has been run; `recipes/README.md` marks Kling `generate_audio` on i2v UNTESTED. The presenter route is unproven, and the buyer sees what the profile's own lab scored 0/5: a synthetic person talking. Most likely slop: three separate generations, three slightly different voices and mouths, plus the banned sales lift. Acceptance checks: STT-transcribe each take and diff against the script (one changed word breaks the super rule); pitch/formant comparison across T1–T3; two-second muted stranger test, "same woman?"; frame-1 mouth closed ("mid-breath" invites an open-mouth poster); no rising pitch at line ends; light from the left in every take. Also: the Ledge ad at 2.5 s does not exist yet; the layout engine lacks its panel primitive.

## 7. What the plan is not seeing
- **Poster frame.** Frame 1 is a stranger's face beside Vaibhav's real photo. The "video of you" risk strikes at the thumbnail, before any disclosure plays. No poster-frame decision exists.
- **Legibility at player size.** 9:16 ads in phone frames inside 16:9 occupy about a third of frame height; at profile-player size the price and legal line, the second promise, will not be readable. Approve every text frame at actual player dimensions.
- **Hosting.** If Upwork still requires a YouTube link, suggested videos overlay the end card and YouTube picks the poster. Confirm first.
- **End card.** Its boss is "Adwisely"; the buyer's next action is to message Vaibhav C. The window line, the only load-bearing text in the film, is the smallest type on it.

## Verdict
Not ready for spend. Two REJECTs (express without window; the triptych), both fixable in a day at USD 0. Fix those, drop "the human", and the film survives to a v4.
