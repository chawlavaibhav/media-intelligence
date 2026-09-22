# Addendum D — Independent checker output (verbatim)

Checker: a separate Claude Sonnet session, fresh context, one tool call (reading `02-checker-input.md`), no access to the audit, the job records, the mapping, or the producer's working. Run 2026-09-20; 114,693 tokens; 11.5 minutes. Plans were labelled X/Y per `random.seed(20260920)`; the mapping was sealed until this file was written.

**Mapping (unsealed):** B1 X = existing, Y = five-stage · B2 X = existing, Y = five-stage · **B3 X = five-stage, Y = existing** · B4 X = existing, Y = five-stage · **B5 X = five-stage, Y = existing**.

---

## B1 — Plan X

A1: 1 — Correctly captures the chopstick-lesson/fail/happy-ending structure from the brief, but adds an unstated framing ("a spec film that makes Cumin Co.'s founders see...") not present in the customer's brief.
A2: 1 — Resolves most creative choices but asks the customer to confirm "spend cap" even though the permitted facts already fix it at USD 8, and raises an unexplained "pool balance attestation."
A3: 2 — Beats are timed to the tenth of a second (e.g. "2 (3.0–6.5)") with fixed voice-line windows, formats, and order of work.
A4: 0 — More than one issue found: the unsupported "founders" framing, the undefined "pool balance attestation," and asking about a spend cap already given as a permitted fact.

B1: YES — The mint bowl is in frame at beat 1 (0.0–3.0s) and the rosé bowl (with chopsticks in its notch) closes beat 5.
B2: NO — On-screen brand text "Cumin Co." appears only in beat 5 (13.0–18.0s) and is never spoken in any of the five voice lines.
B3: NO — The plan states explicitly "no CTA in-frame (brand line closes the film)."
B4: YES — Beat 5 closes on the rim-notch bowl with "Ramen night at home. / Cumin Co." text.
B5: NO — Beat 1 is explicitly labelled "two-shot, table height, wide," not a close-up or mid-action opening.
B6: YES — Beat 4 (10.0–13.0s) specifies "the tips cross; the noodle escapes back into the broth."
B7: NO — The plan's only claim is "'the bowl on a noodle night' sells at a glance," with no numbered frame named, which the rubric explicitly disqualifies.
B8: NO — Beat timings are fixed in the plan text itself and voice lines are generated only after the clips, not measured first.
B9: YES — "provider decided by the customer's ear at micro-qualification (one line each on two providers)" happens before clips are made.
B10: NO — 4:5 and 1:1 are stated to be "declared crops of the 9:16 master," not composed separately.
B11: NO — Beat 2 text "The bottom stick stays still." does not match voice line 2 "The bottom one just rests. It never moves."
B12: YES — "plate for her hand and the first grip clip tested first (the brief's hardest requirement)" names and front-loads the highest-risk hand shot.

C1: Meaning of "pool balance attestation" is never defined; "ending spoon vs fist-grip" is left to the customer unresolved; which of the two voice providers is used is undecided.
C2: The "spec film that makes Cumin Co.'s founders see..." framing is not stated anywhere in the brief; "pool balance attestation" and the specific "Reels UI band" placement rule are not grounded in the permitted facts.

## B1 — Plan Y

A1: 2 — Mirrors the brief's structure closely and explicitly flags its own additions (objective, proposition line) for customer confirmation rather than asserting them silently.
A2: 2 — Lists concrete open questions ("objective default OK; embossed mark allowed; proposition veto; add product name + URL to the deck; spoon ending") before production.
A3: 2 — Names specific frames (F1–F6), spoken/super lines per frame, and a derivation rule for timing ("beat durations equal voice duration plus a hold").
A4: 1 — One issue found: the URL "cuminco.com" is introduced without being present in the permitted facts.

B1: YES — F1 opens on "the mint bowl with steam" and F6 end card is the packshot with product name/brand.
B2: YES — "wordmark small top-left from frame 0" and "persistent wordmark from frame 0; the bowl in every frame."
B3: YES — "'cuminco.com' on the end card and spoken."
B4: YES — F6 end card carries product name, brand and URL.
B5: YES — Opening is "a macro of the mint bowl with steam, his crossed chopsticks..." with the plan stating explicitly "no wide two-shot."
B6: YES — F4 specifies "his hand, tips cross, the noodle falls."
B7: YES — "Hero frame: frame 5, a macro of his chopsticks parked in the rim notch while a spoon lifts broth, held at least 3 seconds."
B8: YES — "voice-over recorded and measured first; beat durations equal voice duration plus a hold; film length derived... not fixed in advance."
B9: YES — "three candidates auditioned on the longest line at final pace before any plate is made."
B10: YES — "4:5 and 1:1 plates are drawn, not cropped; an obstruction check with a subject box runs before delivery."
B11: YES — F2–F4 state "super and voice" carry identical wording, e.g. "The bottom stick stays still."
B12: YES — "Highest-risk shot: frame 4, the miss (crossing sticks, falling noodle, hands) — tested first."

C1: Objective default, embossed-mark permission, the proposition line, the product-name/URL addition, and spoon-vs-alternative ending are all explicitly left for the customer to confirm.
C2: "cuminco.com" is stated as an ask/addition without being present in the permitted facts.

B1: Plan X A=4/8 B=5/12 · Plan Y A=7/8 B=12/12

## B2 — Plan X

A1: 1 — Delivers the required formats and content but includes "RERA registered. T&Cs apply." on the card, an unverifiable regulatory claim on an invented brand, and Attempt 1's single extended clip does not clearly realize the "three-shot" structure the brief and facts require.
A2: 0 — The plan states outright: "No written plan existed before the first paid call; this is the plan as executed."
A3: 2 — Gives specific technical parameters (Veo 3.1 Fast, 8-s + 7-s extend, cut points 8.0–9.1s) and assembly timings ("exterior 0–8 s... interior 8–15 s... offer card slides up at 11.5 s").
A4: 1 — One found: "RERA registered. T&Cs apply." is stated despite permitted facts requiring regulatory claims on the invented brand to be "verifiable or omitted."

B1: YES — Attempt 2 opens on the exterior (the home) and closes with the offer card describing the home.
B2: NO — No visual brand mark is described, and no timing is given confirming the spoken brand name falls within the first 3–5 seconds.
B3: YES — Voice line 2 says "Book a site visit this weekend," and the card carries "BOOK A SITE VISIT."
B4: YES — Assembly ends with the offer card.
B5: NO — No shot framing (close-up/mid-action vs wide) is described for either attempt.
B6: NO — "Per-clip continuity checks" are mentioned generically after generation, with no specific frame identified showing the same people together.
B7: NO — No numbered shot is named as selling the product alone.
B8: NO — Timings ("11.5 s") are stated as fixed cut points, with no mention of measuring voice duration first.
B9: NO — No voice casting/audition process is described.
B10: NO — Statics in Attempt 1 are explicitly "cut from the 720p video frames," i.e. cropped.
B11: NO — Card copy (e.g. "FROM ₹1.2 CR") paraphrases rather than matches voice line 2 ("Prices from one point two crore...") verbatim.
B12: NO — No generative-risk assessment or test-first order is mentioned.

C1: Since no plan existed before the paid call, brand name, copy, and technical choices were all invented live; which voice line maps to which clip in Attempt 2 is unclear; whether attempt 1's single-clip structure satisfies the "three-shot" requirement is unresolved.
C2: "RERA registered. T&Cs apply." is an unverifiable regulatory claim on an invented brand, contradicting the explicit permitted-fact constraint.

## B2 — Plan Y

A1: 2 — Mandatory list ("exterior shot, interior shot, offer card, same people... one Indian-English voice") matches the brief exactly, and the RERA-type claim is proactively handled ("flagged as an unverifiable regulatory claim... replaced... or omitted").
A2: 2 — Defines acceptance criteria and a same-people check "before any motion" ahead of paid generation, resolving risk before spend.
A3: 2 — Specifies shot content, spoken card copy verbatim, hold minimums ("each shot holds at least 4 s"), and quantified acceptance thresholds (e.g. "no silence longer than 0.8 s").
A4: 2 — No unsupported facts or unnecessary complexity found; invented copy is explicitly permitted for this fictional brand.

B1: YES — Shot 1 opens on the exterior (the home) and Shot 3's card slides up over the interior, home-adjacent throughout.
B2: YES — "NIVAAS HOMES mark small from frame 0" with "one continuous voice" persisting.
B3: YES — "BOOK A SITE VISIT" is on the card and spoken.
B4: YES — Shot 3 is the closing offer card.
B5: NO — Shot 1 is described only as "exterior at golden hour" with no stated close-up/mid-action framing.
B6: YES — "Shot 2: interior, the same couple at a window" plus "Highest-risk shot: the interior with two people (identity across shots) — generated and checked first."
B7: NO — No specific shot is named as selling the product without copy.
B8: YES — "shot durations derived from the measured voice; the card enters after line 2 ends."
B9: YES — "one TTS narrator cast by ear on line 1 at final pace before the stills are made."
B10: NO — No statement addresses keeping text off hands/faces/product.
B11: YES — "voice line 2 is the card copy spoken verbatim."
B12: YES — "Highest-risk shot: the interior with two people (identity across shots) — generated and checked first."

C1: Exact camera framing (close-up vs wide) for shots 1 and 2 is unspecified; the owner's copy-approval step required by the permitted facts is not listed in the verification/production order.
C2: None found.

B2: Plan X A=3/8 B=3/12 · Plan Y A=8/8 B=9/12

## B3 — Plan X

A1: 2 — The intent contract lists every mandatory item from the brief accurately and explicitly flags the brief-vs-owner-instruction-vs-permitted-fact contradiction over a presenter rather than resolving it unilaterally.
A2: 2 — "This contradiction blocks the creative stage until the customer answers; two variants are prepared," with explicit asks for presenter yes/no, hosting/aspect, and spend cap.
A3: 2 — Gives a ten-beat board (F1–F10), a timing process ("script locked → voice recorded and measured → timings from the voice"), and minimum hold durations ("no card shorter than 2.5 s").
A4: 1 — One found: "TTS: not Sarvam for a 48-s read" references a specific vendor constraint not established anywhere in this brief's permitted facts.

B1: NO — The finished ad opens the film (F1) but the last frame (F10) is a generic "end card, spoken close," not the finished ad work itself.
B2: NO — The plan states "wordmark on the end card only," explicitly not present throughout.
B3: YES — "'Send your product link and offer. Get a straight price for the first test pack.' on the card and spoken."
B4: YES — F10 is the end card with the spoken close.
B5: YES — Opening is "a finished ad full-frame within 3 s... not a presenter, not a clock, not a logo."
B6: YES — "QA moment: a Devanagari glyph flagged and corrected on screen, 3 s" (board F7).
B7: NO — No numbered shot is claimed to sell the product alone without copy.
B8: YES — "voice recorded and measured → timings from the voice."
B9: YES — Casting "on the longest paragraph at final pace before any picture" (TTS) or "one take qualified by ear and transcript before anything depends on it" (presenter).
B10: NO — No statement addresses text placement relative to hands/faces, and only one aspect ratio (16:9) is discussed.
B11: YES — "Cards carry the spoken words verbatim."
B12: YES — "Highest-risk shot: the presenter take (face, speech, identity) — made and judged first."

C1: Whether a presenter is used at all is unresolved pending the customer; hosting platform/aspect ratio default is pending confirmation; the spend cap is an open question.
C2: The reference to "Sarvam" as a TTS provider is not grounded in any permitted fact given for this brief.

## B3 — Plan Y

A1: 1 — Correctly incorporates the Upwork-rule permitted fact, but its recommended concept puts a specific real, recurring, lip-synced presenter ("Vaibhav") on screen across multiple beats, conflicting with the brief's explicit "no presenter, no lip-synced person, no recurring character," presented as the lead concept rather than gated behind customer confirmation.
A2: 2 — "Paid generation waits for the frozen script, which waits for the presenter ruling," gating spend behind the unresolved question appropriately.
A3: 2 — Gives an explicit second-by-second beat sheet (0–2s, 2–4s, 4–8s, etc.) with exact spoken lines.
A4: 1 — One found: the name "Vaibhav" is introduced as the real presenter without being established anywhere in this file's brief or permitted facts.

B1: NO — The film opens on the AI presenter ("I'm not real"), not the finished ad; it closes on a brand end card, not the finished ad work.
B2: NO — The plan itself states "Brand name once (end card)," i.e. not within 3–5s and not throughout.
B3: YES — "Send your product link"... "You'll get a straight price for a first test pack."
B4: YES — Ends on the "Adwisely mark" end card with the standard line.
B5: NO — The opening is a presenter speaking to camera in a "warm minimal studio," not a product/action shot.
B6: YES — "26–30 s the check: a wrong Devanagari glyph flagged, corrected."
B7: NO — No beat is named as selling the product alone without copy.
B8: NO — Beat timings are fixed upfront in the beat sheet with no stated process of measuring voice first.
B9: NO — No casting/audition process is described for either speaker.
B10: NO — No statement addresses on-screen text placement relative to hands/faces.
B11: NO — Card text (e.g. "Your brief. One photo. One line.") does not match the concurrent spoken lines quoted.
B12: NO — No specific highest-risk shot is named and tested first; risk is discussed only generally in the fallback comparisons.

C1: The presenter ruling from the owner is unresolved and blocks the whole production path; the final choice among the three fallback concepts is undecided.
C2: The name "Vaibhav" is not sourced in the given brief or permitted facts; the statistic "reference-person route 0/2 in the lab" is not supported by any fact given in this file.

B3: Plan X A=7/8 B=8/12 · Plan Y A=6/8 B=3/12

## B4 — Plan X

A1: 1 — Captures the chaos-to-resolution narrative well but consistently misspells the brand "RentOK" against the permitted fact "The spelling on the site is 'RentOk'," and adds a Hindi-English mixed-language register not requested in the brief.
A2: 0 — No open questions to the customer are raised anywhere in the plan; it proceeds straight to a full locked deliverable.
A3: 2 — An 11-shot list with per-shot durations, a timed hierarchy (0–3s hook, 3–14s escalation, etc.), and distinct generation prompts per block.
A4: 0 — More than one issue found: the brand is misspelled "RentOK" throughout, and specific invented signage ("Sharma PG for Boys") is presented without being grounded in permitted facts.

B1: NO — The first shot is WhatsApp chat chaos, not the product; only the last shot (11) shows the RentOK logo.
B2: NO — No brand mark or spoken name appears until shot 7 (~11.5s in), well past 3–5s.
B3: NO — Shot 11 carries only a tagline/CTA text ("Apni property, apne control mein") with no explicit action verb or URL.
B4: YES — Shot 11 ends on the "RentOK logo... tagline + CTA text, trust stat overlay."
B5: YES — Shot 1 is "phone screen flooding with WhatsApp chats, badge climbing 99+," a close, mid-action opening.
B6: YES — Shots 6–7 specify the owner "exhales, sets phone down" then "taps the RentOK icon, whip-pan, lighting shifts."
B7: NO — No shot is named as selling the product alone without copy.
B8: NO — No voice-over script or measurement process is described at all.
B9: NO — No voice casting process is described.
B10: NO — No statement addresses keeping text off hands/faces/product.
B11: NO — No spoken voice-over lines are given to compare against the captions.
B12: NO — No generative-risk assessment or test-first order is described.

C1: The exact voice-over script/lines are never written; access to real brand assets/app screenshots (flagged as needed) is not confirmed; the final CTA link or action beyond a tagline is unspecified.
C2: The brand name is consistently spelled "RentOK," contradicting the permitted fact that the site spelling is "RentOk."

## B4 — Plan Y

A1: 2 — Mandatory list matches the brief precisely, and the plan uses the correct site spelling ("he taps RentOk and says the name").
A2: 2 — Explicitly asks the customer which CTA action, whether real screenshots/logo are available, and whether Hinglish is wanted, before production.
A3: 2 — Board F1–F9 specifies shot content with timing anchors ("RentOk named by 5 s," "turn no later than 12 s") and explicit production rules (Q1–Q9).
A4: 1 — One found: the question list phrase "Download the RentOK app" uses the incorrect capitalization inconsistent with the "RentOk" spelling used elsewhere in the same plan.

B1: YES — F1 carries "wordmark corner" from the first frame and F9 shows "phone with the app and wordmark."
B2: YES — "the wordmark from t = 0... not only at the close" plus spoken "RentOk" at the turn.
B3: YES — "'See how it works – rentok.com'... on the card and spoken."
B4: YES — F9 ends on the phone with the app and wordmark.
B5: YES — "open mid-action — the owner's thumb typing a rent reminder at 11 pm."
B6: YES — "F5 he taps RentOk and says the name" is the specified turn frame.
B7: NO — No shot is named as selling the product alone without copy.
B8: NO — No statement ties shot timings to a measured voice-over duration.
B9: YES — "if a voice-over, cast by ear on the longest line before pictures."
B10: NO — No statement addresses text placement relative to hands/faces.
B11: YES — "Q6 supers equal speech: Hinglish pain labels are spoken as well as shown."
B12: YES — "Highest-risk shot: the phone-screen shots with legible UI in motion... test one first."

C1: Which CTA action (app download vs. website) is unresolved pending the customer; whether Hinglish is wanted is unresolved; access to real screenshots/logo is unconfirmed.
C2: "Download the RentOK app" uses a capitalization inconsistent with the permitted-fact spelling "RentOk" used elsewhere in the same plan.

B4: Plan X A=3/8 B=3/12 · Plan Y A=7/8 B=9/12

## B5 — Plan X

A1: 2 — Intent contract matches the brief precisely: one woman, natural demo, exactly one purchase reason, creator feel, no website (soft "link in bio" instead).
A2: 2 — Flags the purchase reason for customer veto and resolves the native-speech-vs-VO question through an explicit test rather than an unstated assumption.
A3: 2 — Board F1–F5 with specific lines, exact demo action/timing, and clear distinction of deterministic vs. generated elements.
A4: 2 — No unsupported claims or added complexity found; forbidden-claim language is explicitly scanned for.

B1: YES — F1 is "mid-action hook, bottle in hand" and F5 closes with "bottle to camera."
B2: YES — "the label readable in her hand at 0–3 s" satisfies the mark-in-first-seconds requirement, with the bottle recurring across frames.
B3: YES — "'link in bio' spoken at the end plus small text."
B4: YES — F5 ends on the bottle to camera.
B5: YES — "she opens mid-action, serum already on two fingers."
B6: YES — "two drops, pat, ten seconds later she touches her cheek and it is dry."
B7: NO — No shot is named as selling the product alone without copy.
B8: NO — No statement ties shot timings to a measured voice/line duration.
B9: NO — The plan tests native-vs-VO for identity risk but does not describe auditioning multiple voice candidates by ear.
B10: NO — No statement addresses caption placement relative to hands/faces beyond the bottle label itself.
B11: YES — "captions equal the spoken words, burned in."
B12: YES — "shot 1 (face + speech + bottle in hand) tested first as the riskiest."

C1: The brand name is left as a placeholder ("[brand]") in F5; whether delivery is native speech or a single voice-over is "decided after one native take is tested"; the purchase reason is subject to customer veto.
C2: None found.

## B5 — Plan Y

A1: 1 — Core elements are present, but the "single purchase reason" is actually a bundle of three attributes (fragrance-free + lightweight + non-sticky), diluting the brief's explicit "one clear purchase reason."
A2: 0 — No open questions to the customer are raised anywhere; the plan proceeds directly to a full locked production recipe.
A3: 2 — Five shots each with exact second ranges (0–3s, 3–9s, 9–16s, 16–22s, 22–25s) and exact dialogue.
A4: 1 — One found: the "one purchase reason" is presented as three combined benefits rather than a single reason.

B1: YES — Shot 1 has "she holds the bottle near her collarbone" and Shot 5 is a "close-up of the bottle held to camera."
B2: NO — Label legibility/brand naming is not established until Shot 5 ("It's called Rooh Clarity Serum"), not within 3–5s.
B3: YES — Shot 5 overlay "Link in bio."
B4: YES — Shot 5 ends on the bottle close-up with overlay.
B5: YES — Shot 1 is "selfie framing," a close framing rather than wide/logo.
B6: YES — Shot 3 specifies "two drops from the dropper onto a fingertip, patted onto cheek and jawline."
B7: NO — No shot is named as selling the product alone without copy.
B8: NO — Shot durations are fixed upfront in the recipe with no stated voice-measurement step.
B9: NO — No casting/audition process is described.
B10: NO — No statement addresses caption placement relative to hands/faces.
B11: YES — "word-synced captions" ties on-screen text to the spoken lines.
B12: NO — No generative-risk assessment or shot-tested-first order is described anywhere in the plan.

C1: Approval of the invented brand name with the customer is not addressed; whether production is AI-generated or traditionally filmed is never specified; the casting process for the actress is not described.
C2: None found.

B5: Plan X A=8/8 B=8/12 · Plan Y A=4/8 B=6/12
