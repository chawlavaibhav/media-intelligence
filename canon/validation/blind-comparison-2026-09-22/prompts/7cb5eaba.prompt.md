You are the creative director on a media-agency job. Produce the Stage 3 creative board for the brief below, as ONE JSON object written to the output path given at the end. No other files. Do not read any repository file, and do not search for anything: everything you may use is in this prompt.

The board must have exactly these fields (this is the shape the agency's gate validates):
- "proposition": one sentence.
- "board": {"kind": "film", "duration_s": <number>, "style_line": <fixed opening line of every prompt>, "negative_line": <fixed closing line: no text, no logos…>, "identity_anchors": {<name>: <verbatim description restated in every prompt>, …}, "hero_frame": {"beat": <n>, "description": <the one frame that sells the product without copy — a frame, never a claim>}, "audio": {"native_audio": <bool>, "music_bed": <string>, "voice_over": <string or "none">}, "beats": [ {"n": 1, "t_in": 0, "t_out": …, "clip_s": …, "title": …, "feeling": <what the viewer feels>, "framing": <what is in the frame, where, what moves>, "first_frame": <what the STILL shows at t_in, before anything moves>, "impact": <how the beat lands: camera, hold, sound, performance>, "canon": [<ids of any supplied knowledge you applied here, or empty>], "mandatory_ids": [<which brief requirements this beat carries, as M1, M2… of your own numbering>]}, … ] } — beats contiguous, t_out of the last = duration_s; the last beat may be a code-composed brand close (clip_s 0).
- "copy_deck": {"strings": {<id>: <exact on-screen text>}, "sources": {<id>: <where each string comes from>}, "placements": {<name>: {"t_in":…, "t_out":…, "contents": [<string ids>], "why": …}}}.
- "mandatory": [{"id": "M1", "customer_words": <the brief's own words>, "realisation": <how the film carries it>}, …] — every requirement in the brief.
- "brand_timeline": {"first_mark_s": …, "in_context": …, "spoken": …}, "ask": {"string_id": …, "surface": "card"|"super", "at_s": …}, "last_frame": …, "muted_test": "yes"|"no".
- "deviations": [{"from": <a supplied default you overrode>, "brief_clause": <the customer clause that forces it>}] — may be empty.
- "knowledge_used": [{"id": <id>, "used_for": <beat or decision>}] — every supplied knowledge item you actually applied; empty if none supplied or none used. Never invent an id.

Constraints that always apply: everything is produced by generative models (a still per beat, then image-to-video per beat, stitched by code; exact text composed by code, never generated); no dialogue or voice-over; no named film, actor, character or copyrighted work; the product must be a recognisable likeness of the real one; 9:16, 15–30 s.

Write the best board you can. Quality is judged by a non-author on: whether the hero frame sells without copy; how specific and producible each beat's feeling / framing / first_frame / impact are; whether every brief requirement lands on a beat; brand timing; and honesty (a deviation is declared, not hidden).

## THE BRIEF (verbatim job record)
{
 "brief": {
  "language": "en",
  "market": "IN",
  "text": "I want to make a video for RentOK. The video has a Mario game. The player is basically a PG owner. The obstacles in the game are basically the problems that owner faces — tenant verification, collecting rent, tenants leaving without paying rent, no place to do reconciliation, solving complaints and so on. The game also introduces a cheat code — install RentOK app. Once it is done, Mario gets a gun sort of power/immunity. It runs and kills all the obstacles and gets the flag. Platforms: Instagram Reels / Facebook and YouTube Shorts. Duration: 30 seconds. Game identity: An original Mario-inspired game, rather than an exact reproduction of Nintendo's character, artwork, music or game assets. Visual treatment: Delegated to the creative system. Power-up design: Delegated to the creative system, while preserving the requested game-style power/immunity mechanic. Brand and product source: Official RentOK website, https://rentok.com."
 },
 "customer_ref": "acct-rentok",
 "deliverable_request": {
  "aspect": "9:16",
  "count": 1,
  "kind": "multi_shot_story",
  "modality": "video",
  "motion": {
   "audio": true,
   "from": "generated",
   "seconds": 30
  },
  "operation": "generate",
  "subject": {
   "entity": "logo",
   "entity_id": "rentok_wordmark",
   "identity_invariants": [
    "Rent in white",
    "Ok in cyan #03FFF1",
    "blue #0038FF ground"
   ]
  },
  "ambiguity_markers": [
   "kind_nearest_match: 30 s game-style advertising film, longer than the registered multi_shot_story band",
   "customer says 'Mario game' but confirmed 'original Mario-inspired'"
  ]
 },
 "exact_text_strings": [
  {
   "may_reflow": false,
   "placement": "overlay",
   "script": "latin",
   "value": "INSTALL"
  },
  {
   "may_reflow": false,
   "placement": "overlay",
   "script": "latin",
   "value": "RENTOK APP"
  },
  {
   "may_reflow": false,
   "placement": "overlay",
   "script": "latin",
   "value": "TENANT VERIFICATION"
  },
  {
   "may_reflow": false,
   "placement": "overlay",
   "script": "latin",
   "value": "COLLECTING RENT"
  },
  {
   "may_reflow": false,
   "placement": "overlay",
   "script": "latin",
   "value": "LEFT WITHOUT PAYING"
  },
  {
   "may_reflow": false,
   "placement": "overlay",
   "script": "latin",
   "value": "NO RECONCILIATION"
  },
  {
   "may_reflow": false,
   "placement": "overlay",
   "script": "latin",
   "value": "COMPLAINTS"
  },
  {
   "may_reflow": false,
   "placement": "overlay",
   "script": "latin",
   "value": "✓ DIGITAL KYC"
  },
  {
   "may_reflow": false,
   "placement": "overlay",
   "script": "latin",
   "value": "✓ AUTOPAY"
  },
  {
   "may_reflow": false,
   "placement": "overlay",
   "script": "latin",
   "value": "✓ DUES TRACKED LIVE"
  },
  {
   "may_reflow": false,
   "placement": "overlay",
   "script": "latin",
   "value": "✓ ONE DASHBOARD"
  },
  {
   "may_reflow": false,
   "placement": "overlay",
   "script": "latin",
   "value": "✓ COMPLAINT TICKETS"
  },
  {
   "may_reflow": false,
   "placement": "overlay",
   "script": "latin",
   "value": "INSTALL"
  },
  {
   "may_reflow": false,
   "placement": "overlay",
   "script": "latin",
   "value": "RENTOK APP"
  },
  {
   "may_reflow": false,
   "placement": "overlay",
   "script": "latin",
   "value": "RENTOK.COM"
  }
 ],
 "reference_assets": [
  {
   "asset_id": "rentok_wordmark",
   "content_type": "image/webp",
   "depicts_identifiable_person": false,
   "provenance": "customer_site",
   "role": "logo",
   "sha256": "1ff7dcf58689684d8ddae150d384f4aa30c246c314b0bf4e4a389a06e8f66f80",
   "path": "source/rentok-brand/rentok-new-logo.webp",
   "fetched": "https://rentok.com home page img src, 2026-09-20T18:19:29Z"
  }
 ],
 "job_id": "AGY-2026-09-20-RENTOK-GAME-LANE-A-001",
 "policy_profile": "dry",
 "retention": {
  "policy_ref": "alpha-1-default"
 },
 "submitted_by": "producer-lane-a"
}
## SUPPLIED KNOWLEDGE — ten compiled doctrine packs (apply what fits; cite check ids like CA-D1 in `canon` / `knowledge_used`)
CANON_DOCTRINE packs are compiled production decisions from an audited corpus. Each
DEFAULT is a decision already made: accept it, or override it — legal only when a specific
brief clause forces it. Never re-arbitrate a PRE-ARBITRATED CONFLICT: the stated rule
decides. A conflict rule inherits the confidence marker and override path of its
decision_ref. Write the plan only: every CHECK is verified mechanically by a code gate after
the plan is written, so no compliance receipt, deviation list or pass/fix line is asked for.

Marker legend. MEASURED = the source compares or measures. REASONED = a mechanism is given.
ASSERTED = stated without either. CONTESTED = contradicted within its source. QUALIFIED =
narrowed by an in-source exception. DATED = tied to its era's technology. CULTURE-BOUND = tied
to its culture. FIGURE-UNVERIFIED = cites an uninspected figure. MEDIUM-UNTESTED = transfer to
short feed video untested — assume it neither way. -hedged = extractor-added caveat.
-our_reading = our interpretation, not the source's words. SINGLE-ORIGIN / MULTI-ORIGIN(n) =
independent sources behind the decision, never claim-level agreement. Markers label evidence
character, never rank sources. A weak marker is a reason for care, not silence: follow the
default unless a brief clause forces otherwise.


CANON DOCTRINE PACK concept_and_distinctiveness v0 (accepted corpus 3f7e3fadb3fb). 10 decisions. Each DEFAULT is a decision already made: accept it, or override it in DOCTRINE_DEVIATIONS citing the brief clause that forces the override. Answer every CHECK in FAILURE_PREVENTION as pass or fix, by decision id. Id legend: ids drop the sk_/scs_ prefix and _c003 infix (fre_0020 = sk_fre_c003_0020; 3-digit = scs_ system); bare NNNN continues the last-named source.

CD-D1 [ASSERTED-hedged|CONTESTED|QUALIFIED|DATED|FIGURE-UNVERIFIED|MULTI-ORIGIN(4)]
Q: The one proposition; is the product load-bearing in it?
DEFAULT: One promise of a benefit, unique as well as persuasive — one a rival could make fails (ogx_0060). Core by exclusion; proverb, not sound bite (hea_mts_0009, 0008). One adjective per brand; if taken, a polar opposite or a flank (whip_0015; one point per execution, 0004). Big-idea test: gasp, wish I'd thought of it, unique, fits strategy, thirty years, one personality (ogl_0012, 0013, 0007). Unretellable without the benefit; spread without the sponsor is worthless (ctg_0053, 0052). Product as hero of the picture (ogl_0014): in use, end result, close-up, one device repeated for years (ogx_0041).
CHECK: Promise in one sentence, adjective in one word; no rival's name swaps in; unretellable without the product; product in use.

CD-D2 [ASSERTED-hedged|CONTESTED|QUALIFIED|DATED|CULTURE-BOUND|FIGURE-UNVERIFIED|MULTI-ORIGIN(3)]
Q: What makes the idea distinctive, not generic?
DEFAULT: Remarkable = worth remarking: break an expectation the audience holds about the category, or leave a question open (ctg_0013). Learn the category's worn images, then refuse them (whip_0030). Shared logic gives rivals the same answer; advantage is in what nobody tests (sut_alc_0017, 0004; overreach, not reason, 0032). Invert category norms only in full opposition — a little wrong is no good (whip_0065); relevance is the one rule never released (0067).
CHECK: Board names the expectation broken or question opened, the clichés avoided, why it matters to this buyer.

CD-D3 [ASSERTED-hedged|QUALIFIED|DATED|CULTURE-BOUND|FIGURE-UNVERIFIED|MULTI-ORIGIN(6)]
Q: Which borrowed forms and codes may the idea use?
DEFAULT: Borrow a fixed-meaning image only re-angled to the product advantage; unmodified beside the logo it is cliché (whip_0046, 0030). Award work is pattern-bound: a template is a form, never the idea (hea_mts_0025). No analogies: readers do not complete them; the vehicle displaces the product (ogx_0020). Audience codes hold only for their audience and date: Hindi-cinema types, dress and props are a pre-1990s style the book calls past (dpci_0120, 0070, 0040, 0190); a colour identifies a figure only if established earlier (ms_0016). Keep an established mark: retouch, never replace (vig_0013, 0011).
CHECK: Each borrowed image names its re-angle; cinema codes dated and scoped; logo = supplied mark; no analogy carries the claim.

CD-D4 [ASSERTED-hedged|CONTESTED|DATED|FIGURE-UNVERIFIED|MULTI-ORIGIN(3)]
Q: If the idea is a story: hero, opposing force, stakes?
DEFAULT: Customer hero, brand guide; a brand playing hero competes with the customer (sb_0008, whip_0015). Cross the brand's truest thing — a customer truth, not a product fact — with the conflicts it causes (whip_0012, 0041). No conflict, no story; life-after-purchase cuts to the end of the movie (0011); absence of the product is usually more interesting than presence (0013). Stakes named, dosed like salt (sb_0012); want, obstacle, life either way always answerable (0014). Story pre-orders the message (0004) and rehearses action (hea_mts_0018).
CHECK: Hero, guide, truth, conflict, stakes one line each; no opening after the problem is solved; brand not the hero.

CD-D5 [ASSERTED-hedged|DATED|CULTURE-BOUND|MEDIUM-UNTESTED|MULTI-ORIGIN(3)]
Q: Surprise, curiosity, or order of release?
DEFAULT: Violate an expectation to get attention (hea_mts_0010): a visual surprise in frame one, one singular burr; a parade of short scenes is below average (ogx_0040). Surprise decays; to hold, open a gap in what the viewer knows, then fill it (hea_mts_0011). The material is when and in what order information is released (murch_0013). Name within ten seconds, end on the pack (ogx_0039).
CHECK: Board states the expectation violated, the gap and its close, the release order, the burr image.

CD-D6 [ASSERTED-hedged|QUALIFIED|DATED|CULTURE-BOUND|MULTI-ORIGIN(3)]
Q: How concrete and credible is the idea?
DEFAULT: Human actions and sensory detail — the only way an idea means the same to everyone (hea_mts_0012); feeling attaches to an individual, not a category (0016); the proverb makes the abstract concrete (0008). Specifics — a figure, a time, a sum — beat generalities; superlatives convince nobody (ogx_0009). Flag the buyer or the place by name (0007). Exclamation marks read as desperation (whip_0033).
CHECK: One named person, one specific figure or sensory fact; no superlative, no exclamation mark; hailing word opens.

CD-D7 [ASSERTED-hedged|DATED|CULTURE-BOUND|MULTI-ORIGIN(5)]
Q: What should the audience feel; which register; humour?
DEFAULT: Feeling first: what they remember is how they felt (murch_0020); to care is to feel (hea_mts_0015); the effective emotion is often not the obvious one (0017). Emotion sells as well as reason, most where nothing is unique — add a rational excuse (ogx_0036). Register = product × audience: interesting first, funny an accent, no slapstick on a hospital (whip_0058); humour can now sell but only the very few write funny — else don't (ogx_0032); celebrity, cartoon-for-adults, vignette parade below average (0038), a celebrity never the only memorable thing (ppm_0031). Respect; delight, never intimidate (ppm_0001).
CHECK: One target feeling and its rational excuse; register fits product and audience; humour only under a brief clause.

CD-D8 [ASSERTED-hedged|QUALIFIED|DATED|FIGURE-UNVERIFIED|SINGLE-ORIGIN]
Q: Too obvious or too weird — how long is the fuse?
DEFAULT: Sit where clear and clever overlap; 'seen it before' and 'don't get it' mark the edges (whip_0005). Write it flat, then spin (0006). Wit makes the viewer travel 5–40%; the completion is what sticks (0007), but the quick get outranks creativity (0001) and dwell time sets the fuse: two seconds, then ask what it said (0060). Exaggeration is everyone's first reach — use it knowingly, only on a truth (0031); puns and rhymes arrive first; throw them away (0029).
CHECK: A stranger gets it in one viewing; flat statement beside the spun one; exaggeration names its truth; no pun, no rhyme.

CD-D9 [ASSERTED-our_reading-hedged|CONTESTED|QUALIFIED|FIGURE-UNVERIFIED|MEDIUM-UNTESTED|MULTI-ORIGIN(5)]
Q: What is left out; how does the idea survive 15–30 s?
DEFAULT: Grunt test: offer, benefit, action in five seconds (sb_0015). Each added element weakens the rest; remove each, keep only the load-bearing (whip_0003, 0002). Most with the least; past a point, detail makes spectators (murch_0015, 0016). Keep all six cut criteria where possible (0031); else give up from the bottom — never emotion before story, story before rhythm (0027, 0019; emotion outweighs the rest, weights hedged, 0029). Every device motivated, stillness chosen, method unnoticed (ms_0002, 0018); staging alone can direct attention (0017); combine techniques, never two competing cues (0008, 0019); strength by contrast, not impact (vig_0009).
CHECK: Every element passes the removal test; one cue per beat; grunt answers in five seconds; emotion and story survive the cut.

CD-D10 [ASSERTED-hedged|QUALIFIED|MEDIUM-UNTESTED|MULTI-ORIGIN(2)]
Q: What does sound do for the idea?
DEFAULT: Music seems to work best channelling an emotion the film has already made, not supplying one (conv_0007); music from inside the scene reads as accident, not commentary (0009), and wears out with overuse (0011). Opening music promising a register the film does not keep is a fault however good (0023). Withdraw dialogue and sound reads as speech (0019). Actors on camera over voice-over; supers = spoken words; music no measurable good, effects can help, jingles below average (ogx_0042).
CHECK: Emotion made before music enters; opening sound matches the register; supers = speech; no jingle carries the message.

PRE-ARBITRATED CONFLICTS (the rule already decides; do not re-arbitrate):
CF-01 ogx_0040 vs ogx_0039: Surprise in frame one (0040); name within ten seconds, end on the pack (0039).
CF-02 whip_0005 vs whip_0001: Say it straight first; keep the spin only while a stranger gets it in one viewing (0001; bound by medium, 0060).
CF-03 whip_0007 vs whip_0001: Travel of 5–40% only inside the medium's dwell time (0060); a scroll before the get = fuse too long.
CF-04 whip_0013 vs sa8_0042: The conflict is the product's absence (0013), never the buyer's own defect or a named rival (0042).
CF-05 ctg_0013 vs ctg_0021: Remarkability buys attention and immediate talk (0013), not action; for a behaviour objective tie the idea to a cue at the buying moment (0021).

PACK LIMITS:
- Devanagari correctness criteria do not exist in Canon — never generate Devanagari glyphs; composite text deterministically.
- Coverage delta: ogx_* = 1983 US 30 s TV; ogl_*/sa8_* = 1920s–80s print; murch/conv/ms = feature-film craft; ctg/hea/sut = word-of-mouth/communication research. Nothing treats 9:16 feeds, sound-off autoplay or sub-10 s ads: CD-D9's short-form rules are untested transfers; CD-D5, D9, D10 need a timeline (D10 sound) — for a static image nothing here replaces them.
- India: only Dwyer/Patel (Hindi cinema to 2002, posters mainly pre-1990) and Pandey (2015) are Indian; category conventions, festival ideas, regional-language humour, Hinglish, the Indian buyer's emotional target, ASCI: uncovered — check ASCI outside Canon.
- Uncovered: intellectual property (trademark, copyright, parody of a rival, a real person's likeness — whip_0046 is about meaning, not rights); metaphor choice beyond ogx_0020; Berger's triggers.


CANON DOCTRINE PACK critique_and_effectiveness v0 (accepted corpus 3f7e3fadb3fb). 10 decisions. Each DEFAULT is a decision already made: accept it, or override it in DOCTRINE_DEVIATIONS citing the brief clause that forces the override. Answer every CHECK in FAILURE_PREVENTION as pass or fix, by decision id. Id legend: ids drop the sk_/scs_ prefix and _c003 infix (fre_0020 = sk_fre_c003_0020; 3-digit = scs_ system); bare NNNN continues the last-named source.

CE-D1 [ASSERTED-hedged|QUALIFIED|DATED|FIGURE-UNVERIFIED|MEDIUM-UNTESTED|MULTI-ORIGIN(4)]
Q: One core; every element earning its place?
DEFAULT: Grunt test: offer, benefit, action in five seconds, no context (sb_0015). Core by exclusion — proverb, not sound bite (hea_mts_0009, 0008). One adjective, one point (whip_0015, 0004); each added element weakens the rest — keep only the load-bearing (0003). A picture earns its space, sized by importance to the sale (hop_sa_0026).
CHECK: Three grunt answers in 5 s; core in one sentence; nothing the sale would not miss.

CE-D2 [ASSERTED-hedged|CONTESTED|QUALIFIED|DATED|CULTURE-BOUND|MEDIUM-UNTESTED|MULTI-ORIGIN(2)]
Q: Sell or merely entertain; product the hero?
DEFAULT: Measure = brand-preference change; recall appears uncorrelated with purchase (ogx_0031). Liked and selling are seldom one ad (ogl_0021). Product the hero — no dull products, only dull writers (0014); in use, end result, food in motion, close-ups (ogx_0041). Amusement draws the uninterested; money is serious — no amusing, boasting, showing off; one typical buyer (mla_0064, hop_sa_0014). Celebrity, adult cartoons, vignette parades: below average (ogx_0038).
CHECK: One line says what it sells; product performs; memorable thing = product, not celebrity or gag.

CE-D3 [ASSERTED-hedged|QUALIFIED|CULTURE-BOUND|MULTI-ORIGIN(3)]
Q: Claim credible and concrete?
DEFAULT: Specifics — figure, time, sum — over generalities; superlatives convince nobody (ogx_0009). Actions and sensory detail, the only way an idea means the same to all (hea_mts_0012); feeling attaches to an individual, not a category (0016). Flag the buyer or name the place (ogx_0007). Exaggeration is the first reach — knowingly, only on a truth (whip_0031). Exclamation marks read as desperate (0033); puns and rhymes have no persuasive value (0029).
CHECK: One specific fact; a named person or place; no superlative, exclamation, pun, rhyme; exaggeration on a truth.

CE-D4 [ASSERTED-hedged|QUALIFIED|DATED|CULTURE-BOUND|FIGURE-UNVERIFIED|MEDIUM-UNTESTED|MULTI-ORIGIN(5)]
Q: Attention earned, held, credited to the brand?
DEFAULT: First frame is the gate: open with the fire — a visual surprise, one burr; scene parades are below average (ogx_0040). Surprise decays — open a gap, then fill it (hea_mts_0011); the material is the release order (murch_0013). Still reveal: attention to one place, then a second findable element; too small or dim, the viewer leaves (fre_0025); a scale figure's size floor is set by print size (0024). Attribution fails by default: name by 10 s, end on the pack (ogx_0039); one visual device for years (0041); an established mark: retouch, never replace (vig_0013).
CHECK: Frame one surprises; gap opened and closed; late elements visible at delivery size; name by 10 s; pack last; supplied mark.

CE-D5 [ASSERTED-hedged|CONTESTED|DATED|FIGURE-UNVERIFIED|MULTI-ORIGIN(3)]
Q: Story: hero, conflict, stakes answerable at every moment?
DEFAULT: Customer hero, brand guide — a brand playing hero competes with the customer (sb_0008, whip_0015). No conflict, no story; a brief opening after purchase cuts to the end of the movie (whip_0011). Stakes named, dosed like salt (sb_0012). Always answerable: what the hero wants, what opposes, life either way (0014). Story pre-orders the message (0004), rehearses action (hea_mts_0018).
CHECK: Hero, guide, conflict, stakes one line each; no opening after the problem is solved; brand not hero.

CE-D6 [ASSERTED-hedged|QUALIFIED|MEDIUM-UNTESTED|MULTI-ORIGIN(3)]
Q: What does audio add; do picture and sound agree?
DEFAULT: Supers = spoken words verbatim; on-camera speech holds better than voice-over; background music no measurable good; effects can help; jingles below average, aired only when unscripted listeners decipher them (ogx_0042). Sound creates reality faster than picture; ear helps eye (gote_0048). Music seems to work best channelling an emotion already made (conv_0007); opening music promising a register the piece never keeps is a fault however good (0023); withdrawn dialogue makes sound heard as speech (0019).
CHECK: Supers = speech; emotion before music; opening sound fits the register; ear gets what the eye lacks.

CE-D7 [ASSERTED-hedged|QUALIFIED|DATED|CULTURE-BOUND|FIGURE-UNVERIFIED|MULTI-ORIGIN(5)]
Q: Register: feeling, humour, clear/clever, respect, language?
DEFAULT: Interesting first; funny is an accent, maybe the wrong one; register = product × audience, no slapstick on a hospital (whip_0058). Clear/clever overlap: 'don't get it' and 'seen it before' mark the edges (0005); a 1979 study found every commercial misread by 19–40 %: be crystal clear (ogx_0043). Humour can now sell, but very few write funny, else don't (0032; vs mla_0064, CF-03). What they remember is how they felt (murch_0020). Respect, an understood context, delight not intimidation (ppm_0001). Indian-language lines originated, not translated (nnn_0052).
CHECK: One target feeling; a stranger gets it in one viewing; humour only on a brief clause; vernacular originated.

CE-D8 [ASSERTED-hedged|CONTESTED|QUALIFIED|DATED|CULTURE-BOUND|FIGURE-UNVERIFIED|MEDIUM-UNTESTED|MULTI-ORIGIN(2)]
Q: Does every cut earn itself; does the space hold?
DEFAULT: Each shot cut to carries new information (gote_0004); each departure motivated by movement or sound in the outgoing shot (0006). Length = time to describe the contents silently (0053), against a fast-cut norm calling three seconds long; action pace is not love-scene pace (0052). Dissolves are said to read languid (0031); fades bound an act, audio up first (0037). The camera is the audience's eye; too much movement covers up (alt_0014). The film world keeps constant direction and distance (gos_0006); screen direction holds until a change is shown: exit left, enter right (0007); a contradicting shot needs a break shot (gote_0017).
CHECK: Per cut: new thing, reason to leave; shot no shorter than its contents read; transitions and moves motivated; no unshown reversal.

CE-D9 [ASSERTED-hedged|CONTESTED|QUALIFIED|DATED|FIGURE-UNVERIFIED|MULTI-ORIGIN(5)]
Q: Any colour, tone, text or frame judged alone?
DEFAULT: A colour is almost never seen alone — judge each against its neighbours, the most relative medium (alb_0006, 0011). Few judge value across hues by eye (0018). Depth by tonal separation of subject and ground, either way (alt_0015); genre sets the key before a scene is lit (0018), level follows the dramatic line (0022). Text over image needs enough value contrast and follows the structure (sam_0021); differentiated letters read easier, all-caps hardest (alb_0005). Strength is contrast, scale or bold vs light, never impact (vig_0009). Placement: one of three zones, not a coordinate (fre_0017); a vertical frame alone gives no tallness; oppose elements at the long-axis ends (0008).
CHECK: Grayscale: subject/ground, text/image separate; one key, level follows the emotional line; no all-caps; strength = contrast; zone not ratio.

CE-D10 [ASSERTED-hedged|CONTESTED|QUALIFIED|FIGURE-UNVERIFIED|MEDIUM-UNTESTED|MULTI-ORIGIN(3)]
Q: How is the verdict stated, and what gives first?
DEFAULT: A verdict is analysis against the brief's objectives, not reaction or redesign (disc_0005); each finding names element, objective, and why it does or does not serve it (0006). A good note: what is wrong, missing or unclear; early, specific, no demand; a fix only illustrates (cat_0015). The visible fault is usually a symptom, target the cause (0011); a right alarm with a wrong diagnosis still helps (0017). When a cut cannot meet all six criteria, give up from the bottom, never emotion before story nor story before rhythm (murch_0019, 0027); emotion first (0020).
CHECK: Finding = element + objective + why; no change list; fixes only illustrate; competing criteria take the sacrifice order.

PRE-ARBITRATED CONFLICTS (the rule already decides; do not re-arbitrate):
CF-01 ogx_0040 vs ogx_0039: Surprise in frame one; name by ten seconds; end on the pack.
CF-02 whip_0005 vs whip_0001: Spin only while a stranger gets it in one viewing.
CF-03 mla_0064 vs ogx_0032: No humour unless the brief asks and the writer is one of the few; record it.
CF-04 alt_0018 vs alt_0011: Not the exempt genre: one nameable source unless the brief names a pastiche.
CF-05 gos_0007 vs gos_0012: Crossed line = fault unless a shown change or a break shot restores direction.
CF-06 alt_0015 vs alt_0017: 0015: subject vs ground, either way; 0017: only three or more staged depth planes.
CF-07 ogl_0014 vs ogl_0021: Hero is the form, selling the criterion: a hero shot that does not sell fails.
CF-08 ogx_0031 vs ogx_0006: Film/video: brand-preference change; recall figures are print claims.

PACK LIMITS:
- Devanagari correctness criteria do not exist in Canon — never generate Devanagari glyphs; composite text deterministically.
- Coverage: ogx = 1983 US 30 s TV on brand preference; hop/mla = 1920s print; gote/gos/murch/conv/alt = film/TV craft; disc/cat = design reviews. None treats 9:16 feeds, sound-off autoplay, sub-10 s ads or thumb-stop metrics, nor whether a piece must work with audio removed — CE-D6 governs the audio present.
- India: only Pandey (2015) and Parameswaran; ASCI, category/festival codes, regional register uncovered — ASCI outside Canon.
- Uncovered: liking, views, engagement as predictors (0031 rejects recall, TV only); emotion's effect unquantified (0036); pre-testing; checker independence; 'enough' contrast (sam_0021). Still/carousel: CE-D4, D6, D8 are timeline craft; nothing replaces them.


CANON DOCTRINE PACK composition_and_attention v0 (accepted corpus 3f7e3fadb3fb). 11 decisions. Each DEFAULT is a decision already made: accept it, or override it in DOCTRINE_DEVIATIONS citing the brief clause that forces the override. Answer every CHECK in FAILURE_PREVENTION as pass or fix, by decision id. Id legend: ids drop the sk_/scs_ prefix and _c003 infix (fre_0020 = sk_fre_c003_0020; 3-digit = scs_ system); bare NNNN continues the last-named source.

CA-D1 [ASSERTED-hedged|CONTESTED|QUALIFIED|DATED|CULTURE-BOUND|FIGURE-UNVERIFIED|MEDIUM-UNTESTED|MULTI-ORIGIN(5)]
Q: What reads first, second, third?
DEFAULT: One dominant element by contrast — power is contrast, not 'impact' (vig_0009); eyes attract more than probably anything (fre_0020); competing cues confuse (ms_0019); total control is self-defeating (murch_0018; misdirection 0033 per CF-15). A late-found second element stays findable — too small or dim and the viewer leaves (fre_0025); a scale figure registers only above a size the delivered size sets (0024). Coded figures, dress and props read as the code the audience holds (dpci_0120, 0070, 0040; a style dated as ended, 0190): state the meaning, period code only.
CHECK: Three reads, one dominant cue each; second reads visible at delivered size; coded elements dated.

CA-D2 [ASSERTED-hedged|CONTESTED|QUALIFIED|DATED|FIGURE-UNVERIFIED|MULTI-ORIGIN(3)]
Q: Where do subject, text and mark sit?
DEFAULT: Off-centre in one of three approximate zones (fre_001; fre_0017, 0018); centre only when the scene points inward (0019); extreme placement needs a visible reason (0021); no coordinate rules (0016 vs 0028; CF-05) — zones, never grids or ratios. Text over the image: value contrast to read, playing off the image, following the structure beneath (sam_0021); the supplied mark is placed, never redrawn: an established logo is equity, identity the system, never change for its own sake (vig_0013; timeless, 0011).
CHECK: Zone plus reason, no ratio or grid; text reads by value contrast on the structure; mark unaltered.

CA-D3 [ASSERTED-hedged|CONTESTED|QUALIFIED|FIGURE-UNVERIFIED|SINGLE-ORIGIN]
Q: How do the edges hold the subject?
DEFAULT: One edge treatment per shot (fre_002): tight fit, slight deliberate gap (fre_0006); busy scene, edges stop mattering (0005); deliberate halving of a symmetrical subject (0007); straight edges near the frame read magnetic (0003); thin a bright framing element (0004).
CHECK: One named treatment; no accidental near-tangency at the frame edge.

CA-D4 [ASSERTED-hedged|QUALIFIED|FIGURE-UNVERIFIED|SINGLE-ORIGIN]
Q: Use a frame within the frame?
DEFAULT: No compulsion (fre_0022); a subject passing behind an opening is shot as it sits cleanly inside, breaking no edges; thin a bright framing element, else it takes over (0004).
CHECK: A framing element is darker or thinner than what it frames.

CA-D5 [ASSERTED-hedged|CONTESTED|QUALIFIED|DATED|FIGURE-UNVERIFIED|MULTI-ORIGIN(2)]
Q: Balance or restless; depth and key in tone?
DEFAULT: Classical balance by default, weighing size AND tone (fre_0028, 0029; fre_005); refusing the eye rest (0032) is the declared energetic exception; symmetry orders a subject that has none (0030); diagonals divide against strict rectilinears (0033, 0034 per CF-07). Depth: foreground against background in tone, either direction (alt_0015; 0017 per CF-18). Key: set for the whole piece by its category before any scene (0018) — comedy high, low key spoils it; drama follows the dramatic line: bright gaiety, lower sadness, deep blacks and glaring whites for tragedy (0022).
CHECK: Declared balanced or restless; in grayscale size and tonal weight agree, subject separates from ground; key set for the whole, level on the dramatic line.

CA-D6 [ASSERTED-hedged|QUALIFIED|DATED|CULTURE-BOUND|FIGURE-UNVERIFIED|SINGLE-ORIGIN]
Q: Which orientation and aspect?
DEFAULT: By the scene's shapes (fre_003): a vertical frame is not itself tallness (fre_0008); a square reads strict, eye inward (0009, 0010); a wide frame needs shapes calling for it (0011).
CHECK: Aspect justified by a named shape, not the platform alone.
LIMIT: No accepted source treats fixed 9:16 feed frames (A01/G2): every aspect and orientation claim here predates vertical-feed formats; transfer is untested.

CA-D7 [ASSERTED-our_reading-hedged|CONTESTED|QUALIFIED|FIGURE-UNVERIFIED|MEDIUM-UNTESTED|MULTI-ORIGIN(3)]
Q: How does attention travel across cuts?
DEFAULT: The edit is when and in what order information is released (murch_0013): every new shot carries new information (gote_0004), every departure is motivated (0006); alternate placement to drive eye-trace (0010), difficulty near optimum (0011); composition differs at the cut (0026), wipe excepted (0035). Or in one shot: a hidden move (ms_0010; ms_002), a blocked static wide (0017), or a colour tied to the figure in an earlier closer shot finds it blurred (0016); one device per beat.
CHECK: Per cut: new information and motivation; per beat: one device.

CA-D8 [ASSERTED-hedged|CONTESTED|QUALIFIED|DATED|MEDIUM-UNTESTED|SINGLE-ORIGIN]
Q: Cut criteria conflict — what goes first?
DEFAULT: Rule of Six (murch_001; 0019): emotion 51 (0020) > story 23 (0021) > rhythm 10 (0022) > eye-trace 7 (0023) > planarity 5 (0024) > 3D 4 (0025). Aim for all six (0031), else sacrifice upward from the bottom (0027) — higher criteria hide lower failures, never the reverse (0028). Weights hedged, intervals the point (0029); top three bind tightly (0030); 'bad' is film-relative (0011); the list serves the audience's position (0032).
CHECK: An imperfect cut names the bottom criteria sacrificed, never emotion.

CA-D9 [ASSERTED-hedged|CONTESTED|QUALIFIED|FIGURE-UNVERIFIED|MEDIUM-UNTESTED|SINGLE-ORIGIN]
Q: Screen direction and the line?
DEFAULT: The off-frame world keeps constant rules of direction and distance (gos_0006); frame edges are the audience's reference (0005); setups inside one 180° arc (0010; gos_001); movement and position persist across cuts (gote_0017, 0018; gos_0011); reciprocal coverage obeys the line (gote_0056); far side: CF-10/11 (gos_0012, 0013).
CHECK: Direction and side persist, or the change is shown (gos_0007), or declared in DOCTRINE_DEVIATIONS.

CA-D10 [ASSERTED-hedged|QUALIFIED|DATED|CULTURE-BOUND|FIGURE-UNVERIFIED|MEDIUM-UNTESTED|SINGLE-ORIGIN]
Q: How long may a shot hold; what joins shots?
DEFAULT: Silently describe the shot's contents; that time is its length (gote_0053); the fast-cutting norm (alarming, says the source) is the ambient pace (0052). A dissolve reads by duration — frames a jump cut, seconds a superimposition — lasting as its purpose needs, never the software default (0028); said to read languid, sombre (romantic or sad passages, 0031). A fade bounds an act, scene or programme or a time/place change; audio first (0037). Sound creates reality faster than picture; stimulate the ear to help the eye (0048).
CHECK: No shot outlasts its describable content; dissolves name purpose and duration; fades bound, audio first.

CA-D11 [ASSERTED-our_reading-hedged|QUALIFIED|DATED|MEDIUM-UNTESTED|MULTI-ORIGIN(3)]
Q: Does the camera move, and why?
DEFAULT: Every move motivated, stillness chosen (ms_0002); an object in transit licenses a move across a location (0011); the most with the least (murch_0015); the camera is the audience's eye — too much movement covers up, as bad as none (alt_0014); success: technique unnoticed (ms_0018; ms_003).
CHECK: Each move names its motivation; else stillness or a cut.

PRE-ARBITRATED CONFLICTS (the rule already decides; do not re-arbitrate):
CF-01 fre_0002 vs fre_0005: Curve-proportioned cut in a sparse frame (0002); busy scene, edges stop mattering (0005); declare the case.
CF-02 fre_0005 vs fre_0006: Tight fit (0006) is a sparse-frame device, unavailable in a busy scene (0005); one named treatment.
CF-03 fre_0006 vs fre_0007: Halving (0007) needs a symmetrical subject and a stated reason; else fit-with-gap (0006).
CF-04 fre_0007 vs fre_0030: Centred symmetry (0030) orders a disordered subject; halving (0007) tenses an ordered one; state the intent.
CF-05 fre_0016 vs fre_0028: Balance judged by eye, tone weighed (0028, 0029), never a coordinate rule (0016); no ratio justifies placement.
CF-06 fre_0028 vs fre_0032: Balance default; restless is a declared, brief-driven exception (DOCTRINE_DEVIATIONS).
CF-07 fre_0033 vs fre_0034: Diagonals divide against strict rectilinears (0033); echo the subject's rectilinearity only when it fits its spirit (0034).
CF-08 fre_0018 vs fre_0019: Off-centre: subject and setting (0018); centre: scene points inward, subject the sole statement (0019).
CF-09 fre_0018 vs fre_0021: Extreme placement only with a visible reason (0021); else the three zones.
CF-10 gos_0007 vs gos_0012: The far-side setup is not the error (0012), the cut is (0007); cross only for a declared creative reason (0013).
CF-11 gos_0010 vs gos_0012: As CF-10: the arc rule (0010) binds setups cut together; exceptions per 0013.
CF-12 gote_0035 vs gote_0026: Composition differs at every straight cut (0026); the wipe (0035) excepts: its wiping element is the visual event.
CF-14 ms_0017 vs ms_0010: One attention device per beat — cut, move or blocking; unranked.
CF-15 murch_0033 vs murch_0018: 0018 default; misdirection (0033) only for a declared reveal, never ambient control.
CF-16 t_hop_sa_0009 vs t_sam_0018: Each term binds in its origin frame (Hopkins: paid direct-response space; Samara: grid design); name the frame first; neither is a default.
CF-18 alt_0015 vs alt_0017: 0015: subject-against-ground, either direction; 0017: three-plus staged depth planes, near dark, far light; by the frame's structure.

PACK LIMITS:
- Devanagari correctness criteria do not exist in Canon — never generate Devanagari glyphs; composite text deterministically.
- Uncompiled contributors (absent, not arbitrated): jain-gods-in-the-bazaar (darshan order, symmetry-as-authority; CV-D9, IN-D2), samara's grid (t_sam_0018 only, CF-16), carroll-read-this-photographs.


CANON DOCTRINE PACK colour_and_visual_register v0 (accepted corpus 3f7e3fadb3fb). 10 decisions. Each DEFAULT is a decision already made: accept it, or override it in DOCTRINE_DEVIATIONS citing the brief clause that forces the override. Answer every CHECK in FAILURE_PREVENTION as pass or fix, by decision id. Id legend: ids drop the sk_/scs_ prefix and _c003 infix (fre_0020 = sk_fre_c003_0020; 3-digit = scs_ system); bare NNNN continues the last-named source.

CV-D1 [ASSERTED-hedged|CONTESTED|DATED|MEDIUM-UNTESTED|MULTI-ORIGIN(3)]
Q: What is the palette; which one element is saturated?
DEFAULT: One saturated element on a graded-down ground, and it is the product — the hero wherever possible (ogl_0014). A contrasting colour finds the product even blurred and distant if one hue is nearly the only colour in frame and the link was made in an earlier, closer shot (ms_0016); two competing cues confuse (0019). Strength is contrast, never impact — usually vulgarity (vig_0009); primary shapes and colours, message over titillation (0011).
CHECK: Board names the one saturated element and the graded-down ground; nothing else competes; in video the colour is tied to the product in a closer shot first.

CV-D2 [ASSERTED-our_reading-hedged|CONTESTED|QUALIFIED|DATED|FIGURE-UNVERIFIED|MEDIUM-UNTESTED|MULTI-ORIGIN(2)]
Q: Which one cue moves attention in a moving frame?
DEFAULT: One cue per beat. Colour directs attention as well as any camera move (ms_0016); a static wide, dominant subject facing camera, needs no move (0017); a wanted move hides behind an action (0010). Never rack focus between planes — cut to a close-up (0019). Every move and every hold has a reason (0002); the camera is the audience's eye, too much movement covers up (alt_0014); the audience registers the product, not the method (ms_0018).
CHECK: Each beat names its one cue; no focus racking; each move or hold has a reason.

CV-D3 [ASSERTED-hedged|QUALIFIED|SINGLE-ORIGIN]
Q: How is any colour judged — alone or against its neighbours?
DEFAULT: Never alone: a colour is almost never seen unrelated to others (alb_0006); colour is the most relative medium (0011). One colour on two grounds reads as two (0012); influence runs on lightness and hue at once (0014), some colours influence, others accept (0013), strongest for a small piece on a large ground (0015); meaning is in the relations (0007). Very few judge lightness across hues by eye (0018): measure.
CHECK: Colour judged on a composite of the real frame, never a swatch; lightness differences measured as luminance.

CV-D4 [ASSERTED-hedged|QUALIFIED|DATED|FIGURE-UNVERIFIED|MULTI-ORIGIN(4)]
Q: How is the brand colour specified and verified?
DEFAULT: By value, on pixels. A colour name yields as many colours as listeners (alb_0001); colour memory is poor (0002); names are inadequate (0003). Supply the exact value; verify it on delivered pixels against the real ground, which shifts it (0012, 0006); a miss is a fix. Supplied mark untouched — an established logo is equity, identity is the system (vig_0013, 0011); the same image year after year (ogl_0007). Logotype text escapes contrast only under a brand mandate (wcag_0004), never by choice — use the higher-contrast variant (0034).
CHECK: No brand colour by name alone; delivered brand pixels in context match the value or are corrected; mark is the supplied file; logotype under 3:1 is the brand's own variant.

CV-D5 [ASSERTED-hedged|CONTESTED|QUALIFIED|DATED|FIGURE-UNVERIFIED|MULTI-ORIGIN(3)]
Q: How does the product separate from its ground, hue aside?
DEFAULT: By tone, either direction (alt_0015); the dark-to-light progression (0017) governs only staged depth planes. Cold grounds separate warm subjects; warm blends into warm (0003, monochrome film). Colour is never the only means of a distinction (wcag_0007); a ≥ 3:1 lightness difference is itself the second means unless the hue must be identified (0038). Few judge lightness across hues (alb_0018): measure the product edge.
CHECK: Separation survives grayscale; product edge ≥ 3:1 luminance, or a second non-colour cue (edge, shadow, finish) named; depth planes near-dark to far-light.

CV-D6 [ASSERTED-hedged|QUALIFIED|DATED|FIGURE-UNVERIFIED|SINGLE-ORIGIN]
Q: What makes the mood — level, or light character and grade?
DEFAULT: Character. Mood comes from the quality of light — direction, diffusion, shadows — never from exposure level (alt_0025); quantity is exposure, quality is orientation, mood, beauty, depth (0013). One consistent direction — audiences read light untaught (0026); aim at the viewer's mental image, not literal nature (0027). Level follows the dramatic line: bright for gaiety, lower for sadness, deep blacks and glaring whites for tragedy (0022).
CHECK: Mood attributable to named light character and grade, not a brightness slider; one light direction per shot; a level change between beats has a reason.

CV-D7 [ASSERTED-hedged|CONTESTED|DATED|SINGLE-ORIGIN]
Q: Which key does the genre set; when does the brief override it?
DEFAULT: Decide the key of the whole piece from its category before any scene is lit (alt_0018): comedy high and bright — low key spoils it; drama for mood with its ups and downs (0022); mystery its own. The key still appears to come from one nameable fictional source, found first (0011). Override only on a brief clause.
CHECK: Board states the key (high / low / mixed) with its genre reason; key agrees with a named fictional source; any exemption cites the brief clause.

CV-D8 [ASSERTED-hedged|QUALIFIED|DATED|CULTURE-BOUND|FIGURE-UNVERIFIED|MULTI-ORIGIN(3)]
Q: What contrast must the palette leave for anything readable?
DEFAULT: Grade so text measures. Text over an image needs value contrast and follows the structure beneath it (sam_0021). Text ≥ 4.5:1 (wcag_0001) by luminance ratio (0014); large text — ≥ 18 pt or 14 pt bold (0021) — ≥ 3:1 (0002), wider strokes reading at lower contrast (0031), never a thin or unfamiliar face (0022); unrounded; a thin face passes nominally yet fails — thicken or exceed (0033). Narrow outline is letter, wide halo is ground (0018). Exempt only decoration, swappable words (0027), or incidental text like a street sign in a photo (0003, 0035). All-caps is the hardest read (alb_0005); measure (0018).
CHECK: Each text zone reports its ratio at darkest and lightest point: ≥ 4.5:1, or ≥ 3:1 with size and weight; no all-caps running line; no thin face.

CV-D9 [ASSERTED-our_reading-hedged|QUALIFIED|DATED|CULTURE-BOUND|FIGURE-UNVERIFIED|MEDIUM-UNTESTED|MULTI-ORIGIN(2)]
Q: Indian audience — saturation, regional codes, vernacular register?
DEFAULT: Saturation as a claim on attention is a documented convention, not a rule: Sivakasi presses retouched for maximum saturation on a practitioner theory of attention, a practice that outlived its cause, called gaudy by its own makers (jgb_0020). Never pick saturation by an imagined audience class — 'the masses' is producers' rhetoric, not a taste line (0090). Regional iconographic codes are the main ground of pre-press rejection (0040) and the condition on which a devotional image works (0130); in a fixed subject only colour, dress, ornament vary (0070). Bazaar imagery introduced unfamiliar products (nnn_0043); vernacular register by script plus an unstyled, unaspirational small-town setting (0019); one flat brand ground held across hundreds of pieces (0021); Hindi originated, not translated (0052).
CHECK: Saturation named with its attention job, not an audience class; a regional or devotional subject lists its codes; Hindi originated; vernacular setting deliberate.

CV-D10 [ASSERTED-hedged|CONTESTED|QUALIFIED|DATED|MULTI-ORIGIN(2)]
Q: What overall register — quality or loud?
DEFAULT: Quality. Most products get an image of quality, above all those 'worn' in public; cheap-looking advertising rubs off (ogl_0008); every execution projects the same brand image (0007). Strength is contrast and intellectual elegance, never impact for its own sake (vig_0009); against fashion: economy, message over titillation (0011). The product is the hero (ogl_0014); the ad admired for style and the ad that sells are seldom the same (0021).
CHECK: Register named in one line with its product-and-audience reason; nothing loud without a job; palette matches prior work.

PRE-ARBITRATED CONFLICTS (the rule already decides; do not re-arbitrate):
CF-01 alt_0015 vs alt_0017: 0015 governs subject against ground, either direction; 0017 only three or more staged depth planes (near dark, far light).
CF-02 alt_0018 vs alt_0011: A product ad is not the exempt genre: key agrees with the fictional source (0011) unless the brief names a theatrical pastiche — a deviation on CV-D7.
CF-03 ms_0017 vs ms_0010: Two people in continuous movement: 0017 (static wide); a shift between places: 0010 (move hidden behind an action); either with its reason.
CF-04 ogl_0014 vs ogl_0021: A style-led register that displaces the product loses (0014); the criterion is selling (0021); style needs a brief clause.

PACK LIMITS:
- Devanagari correctness criteria do not exist in Canon — never generate Devanagari glyphs; composite text deterministically.
- Coverage delta: alb_* = 1963 colour teaching; alt_* = 1949 monochrome film; ms_* = narrative directing (ms_0016 read onto a product); jgb_* = Sivakasi calendar trade 1994–2001, not ads; nnn_0019/0021 = one plate each; wcag_* = web thresholds (CV-D5's 3:1 is a UI colour-coding rule transferred here). None treats grading, 9:16 feeds, phones, platform recompression or 'vivid' display modes; CV-D8 thresholds are Latin-only: every default transfers untested.
- No source names a palette size, hue, saturation or colour temperature for a product ad; CV-D1 is this pack's reading of ms_0016 and vig_0009. Harmony, warm/cool psychology, category codes, festival palettes, skin tones, Indian daylight: uncovered — assume neither way. Restraint vs saturation is unarbitrated: vig_0011/ogl_0008 prescribe quality; jgb_0020 documents, does not recommend.


CANON DOCTRINE PACK camera_and_spatial_grammar v0 (accepted corpus 3f7e3fadb3fb). 8 decisions. Each DEFAULT is a decision already made: accept it, or override it in DOCTRINE_DEVIATIONS citing the brief clause that forces the override. Answer every CHECK in FAILURE_PREVENTION as pass or fix, by decision id. Id legend: ids drop the sk_/scs_ prefix and _c003 infix (fre_0020 = sk_fre_c003_0020; 3-digit = scs_ system); bare NNNN continues the last-named source.

CG-D1 [ASSERTED-hedged|CONTESTED|DATED|CULTURE-BOUND|MEDIUM-UNTESTED|MULTI-ORIGIN(4)]
Q: How is each beat planned — shot size, lens, key?
DEFAULT: Plan outside-in: wider shots establish, tighter shots reach detail as the action develops (gos_0017). Cover every angle and framing the edit needs (0001) so the most revealing angle is chosen per beat (murch_0009; conv_0027). The director owns the lens — a random lens is a random shot (ms_0003); each face has the lens and distance that renders it most itself, found by test (conv_0025). Decide the key of the whole picture before scene work (alt_0018); in drama the level follows the dramatic line and the long shot's job is mood as well as geography (0022).
CHECK: Each beat names size, lens and level with a reason; wider to tighter or a recorded deviation; key named once.
LIMIT: No product focal length or size ladder in Canon; lens claims are about faces; Alton's key categories are 1949 genres — the order transfers, not the table.

CG-D2 [ASSERTED-hedged|CONTESTED|QUALIFIED|FIGURE-UNVERIFIED|MEDIUM-UNTESTED|SINGLE-ORIGIN]
Q: Where is the line of action, and how do direction and side of frame hold across cuts?
DEFAULT: The film world keeps constant rules of direction; the frame edges are the viewer's reference (gos_0006; 0005). Trace the line along the sight line or the movement (0009; gote_0054); keep every setup inside one 180° arc on its one side (gos_0010). A far-side shot reverses left and right — fine alone, wrong in the cut (0012; gote_0055). Exit frame left, enter frame right (gos_0007); a continued movement keeps its direction (gote_0017); a subject keeps its side unless seen to move (0018); bridge a contradiction with an insert (0016). Cross the line only for a recorded creative reason (gos_0013).
CHECK: Line on the board; every setup on one side; direction and side of frame hold across every cut, or a bridge or on-screen change exists.

CG-D3 [ASSERTED-hedged|QUALIFIED|MEDIUM-UNTESTED|SINGLE-ORIGIN]
Q: Where do eye-lines go, and how is two-person coverage matched?
DEFAULT: A look creates a sight line as movement does; the viewer builds the space from them (gos_0008). A look off-frame obliges a payoff from a direction, angle and height near the looker's (0016). A single from a two-shot keeps its side and direction of attention (0011); both singles from one side of the line, or both read as looking at an unseen third (gote_0056). Reciprocal coverage matches size, height, lens and angle from the mirrored arc position (gos_0015).
CHECK: Every off-frame look paid off from a matching vantage; singles keep sides and looks; reciprocal singles match size, height, lens.

CG-D4 [ASSERTED-hedged|CONTESTED|QUALIFIED|DATED|FIGURE-UNVERIFIED|MULTI-ORIGIN(2)]
Q: What angle and height on the product, and how is it staged in depth?
DEFAULT: Default the camera to a neutral hat: the most revealing angle, the viewer thinking about the action (conv_0015); make it a presence only by decision. The most revealing angle on a solid shows the most surfaces — move to one side and raise until none is gained (alt_0010). Depth is tonal separation of foreground from background, either direction (0015); a complete picture: that angle, each surface a different brightness, a ground of another tone (0015; 0010). Where distance must read, the most distant part is lightest, a full black-to-white scale (0017). A flat monotone wall is broken by cast shadow (0016).
CHECK: Each angle names the surfaces it shows; subject-to-ground separation survives grayscale; distance, where it must read, lightens toward the far; no flat monotone ground without shadow or reason.

CG-D5 [ASSERTED-our_reading-hedged|CONTESTED|QUALIFIED|DATED|CULTURE-BOUND|FIGURE-UNVERIFIED|MEDIUM-UNTESTED|MULTI-ORIGIN(2)]
Q: Does the camera move in this shot, and why?
DEFAULT: Every move has a reason and so does every held camera — moving because you can, or sitting still from laziness, is one error (ms_0002). The camera is the audience's eye; too much movement is as bad as none (alt_0014). To move attention without a cut, hide the move behind an action (ms_0010) or hold a static wide, dominant subject blocked to face camera (0017); colour set on the subject in an earlier closer shot directs attention like a move (0016). Never rack focus back and forth; cut to a close-up (0019). A long-to-close move carries two lightings — the slower setup (alt_0021).
CHECK: Each shot states move or static with a reason; a push-in declares lighting at both ends; no repeated focus shifts.

CG-D6 [ASSERTED-hedged|QUALIFIED|DATED|CULTURE-BOUND|FIGURE-UNVERIFIED|MEDIUM-UNTESTED|MULTI-ORIGIN(2)]
Q: What joins the shots, how far apart, how long does each hold?
DEFAULT: The edit is the order and rate of release of information (murch_0013). Every shot cut TO gives information the viewer lacks (gote_0004); every departure is motivated by a movement or sound in the outgoing shot (0006). Cut by default — continuous action, change of impact, of information or locale (0027); consecutive shots of one subject sit at least 30° apart on the arc or change focal length, else they jump (gos_0014). A dissolve reads by its duration (gote_0028); its register is languid and sombre — effective in romantic or sad passages (0031). A fade bounds a programme or act, or a change of time or locale; audio up under black first (0037). A readable shot holds its describe-aloud duration, a busier frame longer (0053); fast cutting belongs to an action passage (0052).
CHECK: Per cut: new information in and motivation out named; consecutive shots of one subject at least 30° apart; each dissolve or fade names its condition; readable shots hold their describe-aloud time.

CG-D7 [ASSERTED-hedged|QUALIFIED|MEDIUM-UNTESTED|MULTI-ORIGIN(2)]
Q: When a cut cannot keep everything, what gives first?
DEFAULT: Aim for all six at once — emotion, story, rhythm, eye-trace, planarity, 3-D continuity; it usually can be done (murch_0019; 0031). Emotion outweighs the other five together (0020). Otherwise sacrifice from the bottom: space, then planarity, eye-trace, rhythm, story, never emotion (0027); a met higher criterion seems to hide a failed lower one (0028). The Grammar's rules yield to a creative reason, crossing the line included (gos_0013); record the deviation with it.
CHECK: A cut breaking the line, side of frame or 30° names the higher criterion it keeps, in DOCTRINE_DEVIATIONS.
LIMIT: Murch's six are scoped 'for me' and to narrative film; product-film transfer untested.

CG-D8 [ASSERTED-hedged|QUALIFIED|FIGURE-UNVERIFIED|MEDIUM-UNTESTED|MULTI-ORIGIN(2)]
Q: What does the soundtrack do for the space the camera shows?
DEFAULT: Sound creates reality faster than picture; stimulate the ear to help the eye (gote_0048). Shots sharing time and place share sound across the cut, level following distance (0019). Music channels an emotion the film has already created, seldom supplies one — a tendency, not a rule (conv_0007); music with a visible origin in the scene takes a different route (0009). Opening music that sets an expectation the film does not meet is a fault however good (0023). Withdraw dialogue and the audience hears the rest of the track as speech (0019).
CHECK: Sound continues across every same-place cut, level by shot size; the opening cue matches what follows; each cue names its emotion or visible source.

PRE-ARBITRATED CONFLICTS (the rule already decides; do not re-arbitrate):
CF-01 gos_0007 vs gos_0012: 0007 governs every cut continuing a movement or look; a far-side shot (0012) is cut in only under 0013's creative reason, recorded.
CF-02 gos_0010 vs gos_0012: Setups stay inside the arc (0010); a far-side setup (0012) needs 0013's reason on the board and a bridge (gote_0016) where the cut reverses direction.
CF-03 ms_0017 vs ms_0010: Two people in continuous movement: 0017 (static wide, dominant subject faces camera); a shift between places: 0010 (move hidden behind an action); either with its reason (0002).
CF-04 alt_0015 vs alt_0017: 0015 governs subject against ground, either direction; 0017 governs the reading of distance itself: the most distant part lightest, a full black-to-white scale (near dark, far light).
CF-05 gote_0053 vs gote_0052: 0053 governs any shot that must be read; 0052 licenses faster cutting only in an action passage; a readable shot cut shorter is a deviation.
CF-06 gote_0019 vs gote_0021: 0019 governs by default; removing or contradicting the expected sound (0021, not compiled here) is a device only when declared — a deviation on CG-D8.
CF-07 alt_0018 vs alt_0011: A product film is not the exempt genre: the key agrees with the fictional source (0011, not compiled here) unless the brief names a theatrical pastiche, recorded as a deviation on CG-D1.

PACK LIMITS:
- Devanagari correctness criteria do not exist in Canon — never generate Devanagari glyphs; composite text deterministically.
- Coverage delta: every contributor (Alton 1949; Grammar of the Shot/Edit, Kenworthy 2009; Murch) assumes a cinema or TV frame; none treats 9:16 feeds, 15–30 s or sound-off autoplay — arc, 30°, hold and sound defaults transfer untested.
- No contributor is Indian or treats frontality, darshan or an Indian viewer's reading of the camera; no packshot convention in Canon; assume neither way.
- Line, eye-line, reciprocal and move/hold rules are stated for talent; none motivates a move or cut on a product-only beat (a turntable shot) — no default. static_image: CG-D1 and D4 only; the rest need a timeline, CG-D8 an audio track.


CANON DOCTRINE PACK editing_pacing_and_short_form v0 (accepted corpus 3f7e3fadb3fb). 10 decisions. Each DEFAULT is a decision already made: accept it, or override it in DOCTRINE_DEVIATIONS citing the brief clause that forces the override. Answer every CHECK in FAILURE_PREVENTION as pass or fix, by decision id. Id legend: ids drop the sk_/scs_ prefix and _c003 infix (fre_0020 = sk_fre_c003_0020; 3-digit = scs_ system); bare NNNN continues the last-named source.

EP-D1 [ASSERTED-hedged|DATED|MULTI-ORIGIN(2)]
Q: How does the film open?
DEFAULT: Open mid-action or on a close-up, with bold imagery (sk_abcd_0007); reach the heart of the story faster — engaging pacing, tight framing (0006); hook, then sustain, audio and visuals together (0005). The opening sets how the whole is read (sk_conv_c003_0024); opening music that sets an expectation the film fails to meet is a fault however good (0023).
CHECK: First shot is mid-action or a close-up; hook and what sustains it are named; opening music matches what follows.

EP-D2 [ASSERTED-hedged|QUALIFIED|MULTI-ORIGIN(2)]
Q: What must every cut carry, and what lets us leave the shot?
DEFAULT: Every shot cut TO gives information the viewer lacks, visual or aural (sk_gote_c003_0004); every departure FROM a shot is motivated by a movement or sound in it at that moment (0006). Cut where action is continuous, impact must change, or information or locale changes (0027). The edit is the order and rate at which information is released, not the material (sk_murch_c003_0013).
CHECK: Per cut: the incoming shot's new information and the outgoing shot's motivating movement or sound are named; a cut with neither goes.

EP-D3 [ASSERTED-hedged|QUALIFIED|MEDIUM-UNTESTED|SINGLE-ORIGIN]
Q: When candidate cuts compete, which wins?
DEFAULT: Rank: true to the emotion of the moment, advances story, rhythmically right, eye-trace, planarity, 3-D continuity (sk_murch_c003_0019); emotion outweighs the other five combined (0020). Aim for all six; it usually can be done (0031). Only when it cannot, sacrifice bottom-up: never emotion before story, story before rhythm, rhythm before eye-trace, eye-trace before planarity, planarity before space (0027).
CHECK: A cut that breaks space or planarity names the higher criterion it keeps; none trades emotion or story for continuity.
LIMIT: Murch's list is scoped 'for me' and to narrative film; transfer to a product film is untested.

EP-D4 [ASSERTED-hedged|CONTESTED|QUALIFIED|DATED|CULTURE-BOUND|MEDIUM-UNTESTED|MULTI-ORIGIN(2)]
Q: How long does each shot hold?
DEFAULT: A shot that must be read (product, pack, super, establishing) holds as long as silently describing its contents takes; a busier frame earns longer (sk_gote_c003_0053). Beat-driven cuts go by felt beat, not frame count (0009). The sub-three-second norm is no rule: the source gives quick cuts their place but separates what an action passage bears from a love scene (0052). Shots changed too often read as a guide who cannot stop pointing (sk_murch_c003_0018).
CHECK: Every shot that must be read holds at least its describe-aloud duration; every shorter shot sits in a declared action passage.

EP-D5 [ASSERTED-hedged|QUALIFIED|FIGURE-UNVERIFIED|MEDIUM-UNTESTED|SINGLE-ORIGIN]
Q: How do movement and screen direction hold across cuts?
DEFAULT: Keep screen direction across every cut that continues a movement (sk_gote_c003_0017): shoot from one side of the action line unless the line is seen to change on screen (0054); crossing it reverses left-right (0055). A subject keeps its side of frame across a scene unless it moved on screen (0018). Where a shot contradicts established direction, insert a narrative-continuing shot that breaks attention on the direction of travel (0017).
CHECK: Each movement continued across a cut travels the same way; a contradiction is bridged by an inserted shot, never cut directly.

EP-D6 [ASSERTED-our_reading-hedged|CONTESTED|QUALIFIED|FIGURE-UNVERIFIED|MEDIUM-UNTESTED|SINGLE-ORIGIN]
Q: Move the camera, hold it, or cut — and how is attention moved?
DEFAULT: Every move has a reason and so does every held camera — never move just because you can, never sit still from laziness (sk_ms_c003_0002). Where it fits, move attention inside one shot (cutting is fine, less flowing): hide the move behind an action (0010); hold a static wide, block so the dominant subject faces camera (0017); tie a colour to the subject in an earlier closer shot so it reads in a beat when small or blurred (0016). Never rack focus back and forth between planes — it confuses; after a shock, cut to a close-up (0019).
CHECK: Each shot states move or static, with reason; none relies on repeated focus shifts; a figure that must register small or blurred had its colour set earlier and closer.

EP-D7 [ASSERTED-hedged|CULTURE-BOUND|FIGURE-UNVERIFIED|MEDIUM-UNTESTED|SINGLE-ORIGIN]
Q: Cut, dissolve or fade — which, and what does it say?
DEFAULT: The cut is the working default (sk_gote_c003_0027). A dissolve carries a languid, somber, thoughtful register — the 'tear jerker', for romantic or sad passages (0031) — and reads by duration: a few frames imitates a jump cut, several seconds a superimposition; last as long as its purpose needs, never the one-second software default by reflex (0028). A fade marks the start or end of a programme, act, scene or sequence (0037); fade audio up under black before picture fades in.
CHECK: A dissolve sits on an emotional or slowed passage with a chosen duration; a fade only at a boundary; no fade-in over silence.

EP-D8 [ASSERTED-hedged|QUALIFIED|MEDIUM-UNTESTED|MULTI-ORIGIN(2)]
Q: What does sound do that picture cannot, and how does music enter?
DEFAULT: Sound establishes reality faster than picture (sk_gote_c003_0048); a sound begun under the outgoing shot and explained by the incoming one motivates a cut across place or subject (0007). Score channels an emotion the picture has already created, seldom supplies one, a tendency not a rule (sk_conv_c003_0007); music with a visible origin in the scene takes a different route — the scene explains it, so it is not read as manipulation (0009). Where voice withdraws, the audience searches the remaining sound for meaning and hears it as speech (0019).
CHECK: Each music cue names the emotion already built, or its visible source; each cut across place or subject has a sound bridge or a reason for none; passages without voice carry designed sound.

EP-D9 [ASSERTED-hedged|QUALIFIED|DATED|SINGLE-ORIGIN]
Q: Where and how does the brand appear across the film?
DEFAULT: Introduce the brand or product from the start and keep it present to the end — an early appearance that lapses does not satisfy (sk_abcd_0011). Brand early, often, richly — richly means variety of asset, not repetition (0010): product shots, pack shots, in-situ branding, graphics, voice-over, music, fit to message and objective (0013). Core rule first, then tailor emphasis to the marketing objective; nothing dropped (0022). Full-funnel: start with a mix of branding elements, finish on the product (0026).
CHECK: Brand or product present in every shot, no lapse; more than one asset type carries it; a full-funnel film closes on the product.

EP-D10 [ASSERTED-hedged|QUALIFIED|DATED|SINGLE-ORIGIN]
Q: How is the ask made, and how are audio and on-screen channels paired?
DEFAULT: Ask for action with a clear, concise instruction carried by a written CTA, graphics, audio, or a scene from the story (sk_abcd_0019); choose the CTA against one specific objective and say plainly what to do (0020). Pair the on-screen CTA with a voice-over saying the same (0021) and on-screen branding with an audio brand mention (0012); audio and supers reinforce key points, never compete (0008); these pairings rest on sound-on viewing, stated for YouTube only (0014). Full-funnel: CTAs throughout, more direct as the film proceeds (0026).
CHECK: One named objective, one CTA tied to it; on-screen CTA and brand each have a matching audio line at the same moment; text, audio and picture agree.
LIMIT: Audio pairings assume sound is heard (YouTube only); on a sound-off feed the on-screen channel carries ask and brand alone — the corpus does not say how.

PRE-ARBITRATED CONFLICTS (the rule already decides; do not re-arbitrate):
CF-01 gote_0053 vs gote_0052: 0053 governs any shot whose job is to be read: it holds its describe-aloud duration. 0052 licenses faster cutting only in an action passage, not a love scene; cutting a shot that must be read shorter is a deviation.
CF-02 ms_0017 vs ms_0010: By scene: continuous movement between two people takes 0017 (static wide, dominant actor faces camera, hands-and-feet coverage as cut fallback); a shift between locations or points of interest takes 0010 (hide the move behind an action). Either needs its reason (0002).
CF-03 murch_0018 vs murch_0033: 0018 governs cut frequency: never so many shot changes that the viewer never chooses where to look. 0033 (not compiled here; named so the boundary is visible) governs where attention is sent inside the shots made.

PACK LIMITS:
- Devanagari correctness criteria do not exist in Canon — never generate Devanagari glyphs; composite text deterministically.
- No contributor treats 9:16 feed frames or sound-off autoplay (the film sources predate feed video; ABCD is YouTube-only): transfer of every hold, transition and audio-pairing default to vertical short-form is untested.
- No source sets a target duration for hook, brand entry or hold ('early', 'faster', 'often' are unquantified); attach no seconds.
- B12 motion design / animated type has no contributor (no default for animated supers or kinetic type). B09 dialogue is thin (sk_conv_c003_0019, sk_ms_c003_0017): no shot/reverse-shot or reaction-cut default.
- Uncovered: caption timing for sound-off autoplay, the loop point of a looping clip, cutdown versioning — no default; state the gap.
- image_sequence: EP-D7 durations and the sound decisions (EP-D8, EP-D10) need a timeline and an audio track.


CANON DOCTRINE PACK typography_and_copy v0 (accepted corpus 3f7e3fadb3fb). 11 decisions. Each DEFAULT is a decision already made: accept it, or override it in DOCTRINE_DEVIATIONS citing the brief clause that forces the override. Answer every CHECK in FAILURE_PREVENTION as pass or fix, by decision id. Id legend: ids drop the sk_/scs_ prefix and _c003 infix (fre_0020 = sk_fre_c003_0020; 3-digit = scs_ system); bare NNNN continues the last-named source.

TC-D1 [ASSERTED-hedged|QUALIFIED|DATED|MEDIUM-UNTESTED|SINGLE-ORIGIN]
Q: What must the words do?
DEFAULT: Grunt test: a stranger reads what you offer, how it helps, what to do — in five seconds (sb_0015); a clearer offer beats a better product (0018). Readers keep only what helps them thrive — company history and scale are filtered out (0002); effortful words lose them (0003); story pre-orders the message (0004). At any moment the copy says what the hero wants, what opposes them, life either way (0014).
CHECK: Offer, benefit, action present as words; a stranger answers the three questions from the key frame.

TC-D2 [ASSERTED-hedged|QUALIFIED|DATED|FIGURE-UNVERIFIED|MULTI-ORIGIN(2)]
Q: Whose story do the lines tell; how many things do they say?
DEFAULT: Customer as hero, brand as guide (sb_0008) — the archetype that grants the power, never the hero (whip_0015). One point per execution; three things to say is three ads (0004): each element added lowers every other (0003). One adjective per brand; every line sits under it (0015).
CHECK: Lines address the customer's want, not the brand's greatness; board names the one point and one adjective.

TC-D3 [REASONED-hedged|CONTESTED|DATED|MULTI-ORIGIN(2)]
Q: What conflict and stakes do the lines carry?
DEFAULT: Give the copy an opposing force; 'Area Bank Not Robbed' goes unread — nothing changed (whip_0011). Prefer life without the product to life with it (0013). Name what the customer loses by not acting, dosed like salt (sb_0012).
CHECK: Headline or opening line states a problem or absence, not the solved state; one stake named.

TC-D4 [REASONED-hedged|QUALIFIED|DATED|FIGURE-UNVERIFIED|SINGLE-ORIGIN]
Q: How clever may the line be; how fast must it get?
DEFAULT: Write the flat statement, then spin it (whip_0006); the line lives where clear and clever overlap — 'I don't get it' and 'I've seen that before' are the edges (0005). The quick get outranks creativity (0001); wit leaves the viewer 5–40% of the way to travel (0007). Dwell sets the fuse: a passing screen takes about seven words, logo extra; two-second test — show, remove, ask what it said (0060). Cut any element the idea survives without (0002).
CHECK: Flat statement on the board beside the final line; a stranger states its meaning after two seconds; nothing unneeded survives.

TC-D5 [ASSERTED-hedged|DATED|CULTURE-BOUND|FIGURE-UNVERIFIED|SINGLE-ORIGIN]
Q: What register; what is never written?
DEFAULT: Interesting first; funny is an accent, set by product and audience — no slapstick on a hospital (whip_0058). No puns, no rhyming headline (0029). No exclamation mark — it reads as desperation (0033). Exaggeration only on a truth, knowingly (0031). No 'real', no asterisked price, no stock handshake — reassurance reads as the lie it covers (0035). No invented person or model number (0034).
CHECK: Copy has zero '!', no pun or rhyme, no 'real/genuine', no asterisk, no fictional name or SKU; register named with its product-and-audience reason.

TC-D6 [ASSERTED-hedged|QUALIFIED|FIGURE-UNVERIFIED|MULTI-ORIGIN(2)]
Q: Which element is the boss, how much copy, how is the rest ranked?
DEFAULT: Postcard (one visual, little copy) or letter (copy-led, complex message) — decide first; something dominates either way (whip_0045). One entry point, with a reason (0053). One clever element only: clever visual, quiet headline, or the reverse (0043); never show what you say (0032) — word–image polarity sets the shift (0048). Rank the rest by scale and weight: bold against light is strength, mere impact is vulgarity (vig_0009); type beyond trend (0011). A headline that needs explaining has failed; lead with the strongest point (whip_0037). Tagline only if it finishes the argument and stands alone with the logo (0057).
CHECK: Board states postcard/letter, entry element and reason; one clever element; visual does not restate the headline; at most three type sizes, each a rank; tagline stands with logo alone or goes.

TC-D7 [ASSERTED-hedged|QUALIFIED|DATED|FIGURE-UNVERIFIED|MULTI-ORIGIN(2)]
Q: Where does the text sit; how small may a secondary line be?
DEFAULT: Place by zone — centre, off-centre, edge — not coordinate (fre_0017). In a vertical frame, oppose line and product at the two ends of the long axis; the tall format alone conveys nothing (0008). Text over an image follows the structure underneath and plays off its values (sam_0021). A small element registers only above a size set by the delivered size (fre_0024); a line to be found second must stay findable or the viewer moves on (0025).
CHECK: Every text block in a named zone with a reason; text aligned to the image's structure; secondary text checked on a phone at delivery size.
LIMIT: fre_0008, 0024, 0025 are landscape-still claims on pictorial elements; transfer to composed copy is this pack's reading.

TC-D8 [ASSERTED-hedged|QUALIFIED|DATED|CULTURE-BOUND|FIGURE-UNVERIFIED|MULTI-ORIGIN(3)]
Q: What contrast must composed text hold against its ground?
DEFAULT: Measure, never eyeball: few can judge lightness across hues (alb_0018); no colour is seen alone (0006, 0011). Text ≥ 4.5:1 to its ground (wcag_0001) by luminance ratio (0014); large text — ≥ 18 pt or 14 pt bold (0021) — may drop to 3:1 (0002) since wider strokes read at lower contrast (0031), never with a thin or unusual face (0022). Unrounded: 4.499 fails; thin faces pass nominally, fail in practice — thicken or exceed (0033). Narrow outline is letter, wide halo is ground (0018). Exempt only decoration (words swappable) or text incidental in a picture (0003). Over an image, measure the pixels under the letters (sam_0021).
CHECK: Each text block reports its ratio at the darkest and lightest point of its ground: ≥ 4.5:1, or ≥ 3:1 with size and weight stated; no exemption on a message word.
LIMIT: wcag_* are web-conformance thresholds; applying them to a composited frame is this pack's reading, not the source's; single-frame only — no default over a moving video ground.

TC-D9 [ASSERTED-hedged|QUALIFIED|DATED|FIGURE-UNVERIFIED|MULTI-ORIGIN(2)]
Q: Which letterforms and case; may colour alone carry a distinction?
DEFAULT: Reading goes by word picture, not letter (alb_0004): mixed case for any running line; all-capitals is the hardest read (0005). No extraordinarily thin or unfamiliar letterforms, above all at low contrast (wcag_0022). Colour is never the only means of a distinction (0007); a ≥ 3:1 lightness difference is a second means unless the hue itself must be identified (0038).
CHECK: No running line in all-caps; stroke not thin at delivered size; every colour-coded difference also differs in lightness, weight or shape.

TC-D10 [ASSERTED-hedged|QUALIFIED|DATED|FIGURE-UNVERIFIED|MULTI-ORIGIN(2)]
Q: How is the brand mark handled?
DEFAULT: Place the supplied mark; never redraw, restyle or regenerate it — an established logo is equity, identity is the system not the logo, change for its own sake is the wrong motive (vig_0013, 0011). Logotype text is exempt from the contrast threshold (wcag_0004) only under a brand mandate; author-chosen low contrast is not — use the brand's higher-contrast variant (0034).
CHECK: Mark is the supplied file, untouched; on a ground under 3:1 the brand's own higher-contrast variant, never a recolour.

TC-D11 [ASSERTED-hedged|QUALIFIED|DATED|SINGLE-ORIGIN]
Q: Which text is generated and which is composed?
DEFAULT: None generated. Every word meant to be read is real composed text, not an image of text (wcag_0008); text rendered into pixels for a look is an image of text (0025). Letterforms inside a generated picture are allowed only as incidental — a sign that happens to be in a photo, no message (0035) — or pure decoration, words swappable without loss (0027). Prompts name no legible words.
CHECK: No message word exists only as generated pixels; prompts quote no text to render; every legible string traces to the text layer.

PRE-ARBITRATED CONFLICTS (the rule already decides; do not re-arbitrate):
CF-01 whip_0005 vs whip_0001: Say it straight first; keep the spin only while a stranger gets the line in two seconds (0060).
CF-02 whip_0007 vs whip_0001: Leave 5–40% for the viewer, never more; if the two-second test fails, shorten the distance.
CF-03 whip_0048 vs whip_0001: Polarity above zero (no see-say, 0032), below where the idea fails to resolve in the medium's dwell (0060).
CF-04 sb_0012 vs sb_0017: Stakes always named, never over-dosed — 0012 governs the dose; 0017's rules-cannot-be-broken framing is not compiled.
CF-05 sb_0002 vs sb_0003: Both cuts apply: drop what is not about the customer's thriving (0002), then what still costs effort (0003); one does not excuse the other.

PACK LIMITS:
- Devanagari correctness criteria do not exist in Canon — never generate Devanagari glyphs; composite text deterministically.
- Coverage delta: whip_* = 2016 US print/outdoor/TV craft (seven words is a poster figure); sb_* = US web copy; wcag_* = web conformance; sam_* = editorial print/web; alb_* = 1963 colour teaching; fre_* = landscape stills. None treats composed text in 9:16 feeds, platform UI safe zones (Reels/Shorts overlays) or animated type — placement, size and contrast transfer untested; no type size, line count or hold given.
- A14 (Devanagari & Indic typography) has no contributor: no default for Devanagari letterforms, matra legibility, mixed Hindi–English lines or script pairing; Hindi copy origination (nnn_0052) is in CC-D9.
- Grids (A07): Samara's column/module doctrine is not compiled beyond sam_0021; no column, gutter or baseline default.


CANON DOCTRINE PACK product_appearance v0 (accepted corpus 3f7e3fadb3fb). 12 decisions. Each DEFAULT is a decision already made: accept it, or override it in DOCTRINE_DEVIATIONS citing the brief clause that forces the override. Answer every CHECK in FAILURE_PREVENTION as pass or fix, by decision id. Id legend: ids drop the sk_/scs_ prefix and _c003 infix (fre_0020 = sk_fre_c003_0020; 3-digit = scs_ system); bare NNNN continues the last-named source.

PA-D1 [ASSERTED-hedged|CONTESTED|QUALIFIED|SINGLE-ORIGIN]
Q: Which reflection type dominates each key surface — diffuse (matte), direct (glossy) or glare?
DEFAULT: Declare a finish per named object before any prompt and light for it; the three types are a contrast set (lsm_001) — finish belongs to the surface, not the light.
CHECK: One declared finish per key object; same-tone surfaces still differ by finish; none reads both matte and mirror-glossy.

PA-D2 [ASSERTED-hedged|CONTESTED|QUALIFIED|SINGLE-ORIGIN]
Q: Where may the highlight sit on each glossy surface?
DEFAULT: One highlight per surface, from one implied source placed inside or outside the family of angles by intent (lsm_002); the reflection reports the source's size.
CHECK: Highlights agree with the one implied source, not dimming with its distance; a large soft source reads large, never hard.

PA-D3 [ASSERTED-hedged|CONTESTED|QUALIFIED|DATED|FIGURE-UNVERIFIED|MULTI-ORIGIN(2)]
Q: Hard or soft source?
DEFAULT: Large/soft relative to subject unless the brief forces drama; pick the instrument by the shadow edge it must produce (alt_0006); for direct reflection, source size sets highlight size (lsm_0014).
CHECK: Shadow edge and highlight size agree — a soft shadow with a pinpoint specular, or the reverse, contradicts.

PA-D4 [ASSERTED-hedged|CONTESTED|DATED|FIGURE-UNVERIFIED|SINGLE-ORIGIN]
Q: What is the fictional light source; does everything agree with it?
DEFAULT: Name the fictional source first, then place the key to agree (alt_0011); build in alt_002's order — one source photographs flat, added lights restore roundness (0009), interiors imitate daylight's structure (0008); one consistent direction, since audiences read light untaught (0026).
CHECK: One nameable fictional source; key direction agrees; no shadow in frame contradicts it.

PA-D5 [ASSERTED-hedged|CONTESTED|QUALIFIED|DATED|SINGLE-ORIGIN]
Q: How does the product separate from its ground?
DEFAULT: By tonal separation, either direction (alt_0015); the dark-to-light progression (0017) only for staged depth planes. Cold, plain grounds separate warm subjects (0003); a deliberately shiny prop (0004) trades off against a quiet ground (CF-02).
CHECK: Product-to-ground contrast survives grayscale; staged depth planes run dark near, light far.

PA-D6 [ASSERTED-hedged|CONTESTED|DATED|SINGLE-ORIGIN]
Q: What key level does the mood require?
DEFAULT: Set the key by genre and mood before lighting (alt_0018); level follows the dramatic line (0022); mood from the character of the light, not exposure (0025); the fictional source still governs (0011).
CHECK: Mood traces to light character — direction, hardness, contrast — not brightness; key level declared and held across shots.

PA-D7 [REASONED-hedged|DATED|CULTURE-BOUND|MEDIUM-UNTESTED|SINGLE-ORIGIN]
Q: Does the imagery earn its space commercially?
DEFAULT: The picture is a salesman that must earn its space (hop_sa_0026); assume the viewer decides from a glance at headline or picture (0035); size imagery by importance to the sale, never decoration; plan for one imagined typical buyer and do what a salesman would face to face — never amuse, boast or show off (0014).
CHECK: One line: what the hero image sells at a glance, to which typical buyer; if it needs the body copy, the image fails.

PA-D8 [ASSERTED-hedged|CONTESTED|QUALIFIED|DATED|FIGURE-UNVERIFIED|SINGLE-ORIGIN]
Q: Glass, dark or mirror-glossy object — special handling?
DEFAULT: Dark subjects reveal direct reflection, producing less diffuse (lsm_0017); black-on-black: light black as if metal — find and fill the family (lsmx_0057). Identify polarized reflection by its diagnostics (lsm_0018); a polarized source makes it manageable (0019) but sits late in the ladder on cost: darker background, source toward camera, camera height first (lsmx_0023); cross-polarizing source and lens buys freedom from geometry at large cost (0009). Polarized direct reflection is dimmer than ordinary (lsm_0015).
CHECK: Every specular on glass, dark or glossy surfaces is declared wanted or removed; none accidental.

PA-D9 [ASSERTED-hedged|DATED|FIGURE-UNVERIFIED|SINGLE-ORIGIN]
Q: Which angle is the hero angle?
DEFAULT: The angle showing the most surfaces (alt_0010) — Canon's only committed angle-choice criterion.
CHECK: Count visible faces; prefer the angle showing more unless it breaks PA-D2 or PA-D5.
LIMIT: Packshot convention absent from Canon (A13 application_unbound): hero-angle, label-legibility and scale-cue conventions are not in the corpus; this default is one 1949 cinema-era claim — do not overgeneralize.

PA-D10 [ASSERTED-hedged|SINGLE-ORIGIN]
Q: When may any of the above be overridden?
DEFAULT: Technique serves a creative decision it does not make (lsm_0020): any default here yields to an explicit creative decision, recorded in DOCTRINE_DEVIATIONS with its forcing brief clause.
CHECK: Every deviation from a PA decision sits in DOCTRINE_DEVIATIONS with its forcing brief clause; none silent.

PA-D11 [ASSERTED-hedged|QUALIFIED|DATED|FIGURE-UNVERIFIED|MULTI-ORIGIN(2)]
Q: Where does the product sit, and how do height, scale and a second read register?
DEFAULT: Place by zone — around the centre, near an edge or corner, or off-centre — never a coordinate (fre_0017). A vertical frame is not itself tallness: oppose two elements at the ends of the long axis (0008). With nothing of familiar size in frame, size does not read; a small figure supplies it, as small as possible yet still seen at the delivered size (0024). A late-found second element must stay findable — too small or dim and the viewer leaves (0025). The camera is the audience's eye; too much movement covers up, as bad as none (alt_0014).
CHECK: Zone and reason named; scale cue and second read visible at delivered size; each move names what it concentrates on.

PA-D12 [ASSERTED-hedged|QUALIFIED|DATED|CULTURE-BOUND|FIGURE-UNVERIFIED|SINGLE-ORIGIN]
Q: What do props, dress and figures staged with the product signal?
DEFAULT: Each is a code the audience already holds — props for period, class and modernity (dpci_0040), dress for occasion, formality and colour (0070), a figure for its type (0120): Hindi-cinema codes to 2002, a style the source dates as ended (0190). Use as deliberate, dated period codes, never the current default (tables: IN-D3).
CHECK: Each prop, garment and figure has a stated meaning and date range; filmi-era codes marked 'period, deliberate'.

PRE-ARBITRATED CONFLICTS (the rule already decides; do not re-arbitrate):
CF-01 alt_0015 vs alt_0017: 0015: subject-against-ground, either direction; 0017: three or more staged depth planes, near dark, far light. Apply by the frame's structure.
CF-02 alt_0003 vs alt_0004: Per object: a glossy prop keeps its declared speculars; the ground behind stays cold and quiet; never both on one surface.
CF-03 alt_0018 vs alt_0011: Commercial imagery is not the exempt genre: follow 0011 unless the brief names a theatrical pastiche, recorded as a deviation.
CF-04 lsm_0004 vs lsm_0010: By declared finish (PA-D1): 0004 governs matte/diffuse, 0010 glossy/direct; both hold on different surfaces.
CF-05 lsm_0006 vs lsm_0014: By reflection type: 0006 diffuse; 0014 whether and how large the mirror image appears on direct surfaces.
CF-06 lsm_0008 vs lsm_0012: By reflection type: falloff reasoning on diffuse only; on shiny surfaces reason about apparent source size.
CF-07 lsm_0011 vs lsm_0008: Direct-reflection brightness is distance-independent (0011); diffuse follows the inverse square law (0008); never swap the rules.
CF-08 t_alt_0021 vs t_lsm_0008: Every specular is declared wanted — a shiny prop keeps its highlights (alt_0004) — or identified and removed (lsm_0018, 0019); technique serves the decision (0020); Alton's term is antihalo-stock contingent (DATED).
CF-09 lsmx_0023 vs lsmx_0035: Material decides: a glossy dielectric box works the suppression ladder (0023); a polished metal box embraces direct reflection — the surroundings become the source (0035, uncompiled).
CF-10 lsmx_0057 vs lsmx_0036: Light black as if metal (0057); the metal SUPPORT arrangements (0036, uncompiled) carry across only for actual metal — withdrawn where polarization behaviour differs.
CF-11 lsmx_0009 vs lsmx_0038: Cross-polarization (0009) is a dielectric-glare last resort; never on metal, whose edges the direct reflection constitutes (0038, uncompiled).

PACK LIMITS:
- Devanagari correctness criteria do not exist in Canon — never generate Devanagari glyphs; composite text deterministically.
- Coverage note (GAP-16 resolved by the DN-06 admission): the source's later chapters are accepted as light-science-magic-beyond-ch3, a scoped extension of ch3. Its three self-qualification claims are compiled where they bite (PA-D8: sk_lsmx_0009, sk_lsmx_0023, sk_lsmx_0057 — polarizer demoted on cost grounds; glossy-box remedy ladder ordered cheapest-first; black-on-black lit as if metal). The remainder of the extension awaits the full live-37 pack compile.
- Coverage delta: jain-gods-in-the-bazaar (frontality/darshan staging, iconographic codes; CV-D9, IN-D2), carroll-read-this-photographs, hopkins ch8-21: nothing compiled here — absent, not arbitrated.
- Category gap: no claim covers watch conventions (hand positions) or brushed/sunburst anisotropic surfaces; PA-D1's types do not model radial glow — state the gap, never force a type.
- Transfer untested: fre_0008/0024 landscape, 0017 a 3:2 still, alt_0014 narrative film, dpci codes one audience to 2002 — packshots, 9:16 and other audiences assume neither way.


CANON DOCTRINE PACK indian_indic_context v0 (accepted corpus 3f7e3fadb3fb). 6 decisions. Each DEFAULT is a decision already made: accept it, or override it in DOCTRINE_DEVIATIONS citing the brief clause that forces the override. Answer every CHECK in FAILURE_PREVENTION as pass or fix, by decision id. Id legend: ids drop the sk_/scs_ prefix and _c003 infix (fre_0020 = sk_fre_c003_0020; 3-digit = scs_ system); bare NNNN continues the last-named source.

IN-D1 [ASSERTED-our_reading-hedged|DATED|CULTURE-BOUND|FIGURE-UNVERIFIED|MULTI-ORIGIN(3)]
Q: Which language and script does the copy originate in, per surface — originated or translated?
DEFAULT: Originate copy in the delivered language: the source's line is origination versus translation — a translating Language Department separates language from idea (nnn_0052; Hindi, metro agencies 1970s–2000s). One inspected plate carries the vernacular by the Hindi word AND its Devanagari script beside the Latin logotype (nnn_0019). Across a multilingual territory, Indian film posters 'rarely use text' — text is seen as a cultural barrier; from the 1980s only the title and three names, in English (dpci_0130, dated). Say it in a context the audience understands, with respect, to delight not intimidate (ppm_0001, a credo). Locations within India differ as countries do: shared quality pool plus a local team (ppm_0030, asserted).
CHECK: Language and script named per surface, each 'originated', never 'translated from English'; a local-nuance reader named for any market outside the writer's own; text a non-reader needs is never the only carrier; Devanagari composited.
LIMIT: Only Hindi origination is attested; CC-D9 shares nnn_0052 and ppm_0001; CC-D1/D7 govern the line.

IN-D2 [REASONED-hedged|QUALIFIED|DATED|CULTURE-BOUND|FIGURE-UNVERIFIED|MULTI-ORIGIN(3)]
Q: Which India is the audience, and what transfers from another market or a non-Indian source?
DEFAULT: Define the target India from named variables (consumer class, urban/rural, state, age cohort), never 'India', 'the masses' or a town-size stratum, held 'no longer wise' (rbwl_0170, a reframing, undated cases). Regional iconographic codes are the main ground for sending a design back before press, and learnable, not membership (jgb_0040, calendar trade 1994–2001, informant-reported). Nothing transfers by analogy: 'Indian consumers today are like American consumers twenty years ago' is called deeply flawed — consumers exist in real time with their own history and dense home-grown options (rbwl_0090, 1991–2009, over-prediction cases only); expect 'this as well as that', the new beside the old, not replacing it (rbwl_0120; keep the unbundling mechanism, drop the 'DNA of Indian society' framing). Recognising a star is bounded to viewers inside the culture (dpci_0090, no measurement).
CHECK: Target India named by two or more variables; each non-Indian-source default applied is listed with why it holds here or marked culture-untested; the product does not replace a tradition unless a brief clause says so.
LIMIT: jgb_0040 codes are deity attributes for prints; no contributor gives regional codes for products or people.

IN-D3 [ASSERTED-our_reading-hedged|QUALIFIED|DATED|CULTURE-BOUND|FIGURE-UNVERIFIED|MULTI-ORIGIN(3)]
Q: Which visual register do Indian viewers read — dress, props, setting, festival?
DEFAULT: State each code's meaning on the board. Sari grammar by occasion, season, formality, with a colour code — red, green, yellow festive; white or pale for widows; black largely Western — and its cinematic use: sari as chastity, sober saris on mothers, Western clothes on the unmarried heroine with no negative charge by the 1990s (dpci_0070, Hindi cinema to 2002, 'almost invariably', no counts). Character types — good/bad, rich/poor, traditional/modern — are a code the audience holds, 'not universally recognized', unmarked by clothing after about 1990 (dpci_0120). Props carry period and class — tonga rural/historical, train modernity, bicycle youth, car wealth, auto and taxi the middle and working city — two entries dated by decade: period-bound description, not a rule (dpci_0040). In the melodramatic mode, setting and costume externalise feeling — 'glamorous realism' (dpci_0030; not all Hindi cinema). Attested vernacular setting: an unstyled, unaspirationally lit small-town street (nnn_0019). Festival: chocolate entered the Diwali sweets exchange only when packed in the traditional clay lamps, not via Indian motifs in ads (rbwl_0120, undated). The source's expiry notice governs the three cinema codes: their 'filmi' style is 'a thing of the past' by 2002 (dpci_0190) — deliberate period codes, never the current default.
CHECK: Each garment, prop and setting has its stated code and date range; filmi-era codes marked 'period, deliberate'; a festival execution names the practice joined, not just the motif.

IN-D4 [REASONED-hedged|QUALIFIED|DATED|CULTURE-BOUND|FIGURE-UNVERIFIED|MULTI-ORIGIN(2)]
Q: Does the figure look out at the viewer — frontal address or gaze-follows-action?
DEFAULT: Where an image is bought for a two-way look, the calendar trade's constraint is that the figure looks out at the viewer whatever the action — a woman putting on a slipper, washing clothes, 'she has to look at you'; eyes painted last; the reason given is devotional, from one artist, marked by Jain as partly discursive (jgb_0010, calendar art 1994–2001), resting on iconographic correctness as the condition on which an image works at all (jgb_0130, trade belief, no consumer study). Frontality and the tableau are a reading category built on early and 1950s film, not a production instruction (dpci_0020); darshan is accepted by Dwyer only inside the film, to produce the star (dpci_0010, contested). Decide address per shot; do not default a product ad to frontal on this corpus.
CHECK: Per hero figure: frontal-to-viewer or gaze-follows-action, with the reason; a devotional or calendar-register execution is frontal with eyes finished.

IN-D5 [ASSERTED-hedged|DATED|CULTURE-BOUND|MULTI-ORIGIN(2)]
Q: Celebrity — cast one, and if so how?
DEFAULT: If a celebrity is cast, the viewer must find celebrity, script and idea all memorable, not the celebrity alone (ppm_0031, stated, untested). Once celebrity use became near-universal a star declaring use ceased to differentiate; the reported move is the star cast as a character in a story (nnn_0041, author-selected examples, 2000s). Instrument effect: celebrities raise pre-test scores and the pre-test is the gate — a reason to cast independent of whether the ad works (nnn_0040; silent on whether celebrities work). A 2002 agency-owned study says 'aura' dominates fit; youth brands take current heartthrobs, serious categories maturity (nnn_0042; no sample, method or effect size). Author's own likelihood: celebrity now does the bazaar totem's job — imagery borrowed to introduce products the buyer had no frame for (nnn_0043, second-hand). CC-D7 (Ogilvy, US 1983) rates the celebrity below average — other market, other era.
CHECK: If a celebrity appears: script and idea memorable without them; the star plays a named character, not 'I use X', unless a brief clause asks; a pre-test motive is recorded.

IN-D6 [ASSERTED-hedged|DATED|CULTURE-BOUND|SINGLE-ORIGIN]
Q: Which claim and clearance norms bind an Indian ad?
DEFAULT: The corpus records institutions, not rules: ASCI (1985, UK model) hears complaints through its CCC and orders modification; since a 2007 Cable TV Network Rules amendment an ad it finds objectionable cannot air on any cable network (nnn_0012, insider account). The Animal Welfare Board regulates real animals on shoots — settle that route before approving an animal script; cinema shorts need a censor certificate (nnn_0013). The gori→nikhri substitution is history — the ban changed the word, not the proposition — not endorsed (nnn_0011). Plan every claim for an ASCI check outside Canon.
CHECK: HARD_CONSTRAINT_CHECK lists 'ASCI Code check: outside Canon' against every claim; a real animal names its AWBI route; no euphemism carries a banned meaning.

PRE-ARBITRATED CONFLICTS (the rule already decides; do not re-arbitrate):
CF-01 nnn_0041 vs nnn_0042: Which star and how the star appears are separate: 0042 speaks only to which (aura, with its category conditions); 0041 to how (as a character). Neither is measured; apply 0041 to the script whichever star 0042 picks.

PACK LIMITS:
- Devanagari correctness criteria do not exist in Canon — never generate Devanagari glyphs; composite text deterministically.
- Coverage delta: LIVE37 critical_limited — five contributors, none a product-advertising manual: rbwl_* = market strategy to 2009 (short shelf life by the author's own word); dpci_* = Hindi cinema and film posters to 2002; jgb_* = Sivakasi calendar trade 1994–2001; ppm_* = one practitioner's credo, 2015; nnn_* = an insider's survey of Indian ad history, 2016. None treats 9:16 feeds, phones, sound-off or a post-2016 India; none measures whether any of it sells — every default transfers untested.
- Uncovered, assume neither way: Hinglish and code-mixing; every non-Hindi language or script; English-versus-regional per surface; voice-over language; festival calendar or colour by festival; family, gender and body norms; menswear, regional dress, a modern home, food, jewellery; religious-imagery restraint for brands; humour by region. A14 (Devanagari & Indic typography) has no contributor; national-symbol depiction rules (flag, emblem, currency, map) and skin-tone / colourism casting guidance.
- Regulation: ASCI appears only as an institution and its 2007 cable sanction (nnn_0012); the ASCI Code's rules, fairness, celebrity and influencer guidelines, celebrity due diligence, CCPA, MRP display and platform policies are not in Canon — check every claim outside Canon. Bijapurkar's consumer claims, film-poster star doctrine (dpci_0100, 0080) and social-cause platforms (nnn_0055) are not compiled.


CANON DOCTRINE PACK commercial_communication v0 (accepted corpus 3f7e3fadb3fb). 10 decisions. Each DEFAULT is a decision already made: accept it, or override it in DOCTRINE_DEVIATIONS citing the brief clause that forces the override. Answer every CHECK in FAILURE_PREVENTION as pass or fix, by decision id. Id legend: ids drop the sk_/scs_ prefix and _c003 infix (fre_0020 = sk_fre_c003_0020; 3-digit = scs_ system); bare NNNN continues the last-named source.

CC-D1 [ASSERTED-hedged|QUALIFIED|DATED|CULTURE-BOUND|MULTI-ORIGIN(4)]
Q: What is the one thing this ad says?
DEFAULT: One point per execution; three things to say = three ads (whip_0004). Find the core by exclusion; the standard is the proverb, not the sound bite (hea_mts_0009, 0008). Keep message and language focused (abcd_0017); engagement devices sit inside that point (0018). In five seconds a stranger grunts what you offer, how it helps, what to do (sb_0015); people buy what they grasp fastest (0018).
CHECK: The single point is one sentence on the board; every scene and line serves it; the three grunt answers sit in the key frame.

CC-D2 [ASSERTED-hedged|QUALIFIED|DATED|SINGLE-ORIGIN]
Q: What is the CTA, and against which objective?
DEFAULT: Core principles, then weight them to the brief's one objective (abcd_0022). One CTA against that objective, saying plainly what to do (0020); direction clear, concise, easy — written CTA, graphic, audio or story scene (0019); voice the on-screen CTA in the same words (0021; premise 0014, audio heard). Full-funnel: CTAs throughout, more direct as the ad runs (0026).
CHECK: CTA names one action and its objective; spoken and on-screen CTA words match; no generic unattached ask.

CC-D3 [ASSERTED-hedged|QUALIFIED|DATED|MULTI-ORIGIN(2)]
Q: When does the brand appear, how often, through which assets?
DEFAULT: Brand or product from the start, never lapsing (abcd_0011). Early, often, richly — vary the asset (product shot, pack shot, in-situ branding, graphics, voice-over, music) to fit message and objective (0010, 0013, 0022); say the name as well as show it (0012, 0014). Attribution fails by default: name within ten seconds, end on the pack (ogx_0039). Full-funnel: open on mixed branding elements, end on the product (abcd_0026).
CHECK: Brand or product seen or spoken from the opening, never lapsing; name shown and spoken; final frame is the pack.

CC-D4 [ASSERTED-hedged|CONTESTED|DATED|FIGURE-UNVERIFIED|MEDIUM-UNTESTED|MULTI-ORIGIN(4)]
Q: Who is the hero — product or customer?
DEFAULT: Both. Picture: the product is the hero — in use, with its end-result, in close-up, simply (ogl_0014, ogx_0041); a picture is a salesman earning its space, sized by importance to the sale (hop_sa_0026). Story: the customer is the hero, the brand the guide/archetype granting the power; a brand playing hero competes with the customer (sb_0008, whip_0015); one adjective per brand (0015). Judge by selling, not style (ogl_0021).
CHECK: Board names the story's hero (customer) and the picture's hero (product); product shown in use; no shot merely decorates.

CC-D5 [ASSERTED-hedged|CONTESTED|DATED|MULTI-ORIGIN(3)]
Q: What conflict does the story run on, and what is at stake?
DEFAULT: Give the story an opposing force; a brief about life after purchase cuts to the end of the movie (whip_0011); life without the product usually beats life with it (0013). Name what the customer loses by not acting, dosed like salt (sb_0012). At any moment the viewer can say what the hero wants, what opposes them, and life either way (0014). Story pre-orders the message (0004) and rehearses the audience to act (hea_mts_0018).
CHECK: Want, obstacle, stakes each one line on the board; the ad does not open after the problem is solved.

CC-D6 [ASSERTED-hedged|DATED|CULTURE-BOUND|MEDIUM-UNTESTED|MULTI-ORIGIN(4)]
Q: What happens in the first frame and first seconds?
DEFAULT: Open with the fire: a visual surprise in frame one (ogx_0040). Jump in — reach the heart of the story sooner, with pacing and tight framing (abcd_0006); start mid-action or on a close-up (0007); hook and sustain with audio and visuals (0005). Surprise decays: open a gap in what the viewer knows, then fill it (hea_mts_0011); curiosity activates most (mla_0010). One visual burr that sticks; a parade of short scenes is below average (ogx_0040).
CHECK: Frame one holds a nameable surprise, not a logo or establishing shot; a gap opens early, closes before the CTA; one image is the burr.

CC-D7 [ASSERTED-hedged|QUALIFIED|DATED|FIGURE-UNVERIFIED|MEDIUM-UNTESTED|MULTI-ORIGIN(4)]
Q: How are the claim and the lines made credible?
DEFAULT: Specifics — percentage, time, money saved — never superlatives (ogx_0009); no boasting (hop_sa_0014); among good rivals say what is good about yours, not that it is better (ogl_0016). Human actions and sensory detail (hea_mts_0012); one individual, not an abstraction (0016). Testimonial: a real unpolished user defending under challenge (ogx_0034), not a celebrity — below average, remembered instead of the product (0038). Exaggeration rests on a truth (whip_0031). The line sits where clear and clever overlap: say it straight, then great (0005); wit leaves the viewer part of the way (0007). No puns, rhymes (0029) or exclamation marks (0033).
CHECK: Every claim specific and traceable to a product fact; no 'best'; endorser a user unless a brief clause names a celebrity; no exclamation mark, pun or rhyme; stranger gets the line in one read.

CC-D8 [ASSERTED-hedged|DATED|CULTURE-BOUND|MEDIUM-UNTESTED|MULTI-ORIGIN(4)]
Q: Is humour allowed, and what register does the ad take?
DEFAULT: Set out to be interesting, not funny; funny is an accent, and register follows product and audience — no slapstick on a hospital (whip_0058). Hopkins bans amusement — money is serious, amusement attracts the uninterested (mla_0064, hop_sa_0014). Ogilvy's dated reversal: humour can now sell, but only the very few write funny; otherwise do not try (ogx_0032). ABCD's humour, surprise, intrigue are braked by focus (abcd_0018, 0017). Cartoons sell to children, not adults; musical vignettes entertain, don't sell (ogx_0038).
CHECK: Register justified by product and audience; if humour, name the brief clause and the point it carries; no cartoon for adults, no vignette parade.

CC-D9 [ASSERTED-hedged|QUALIFIED|DATED|CULTURE-BOUND|MEDIUM-UNTESTED|MULTI-ORIGIN(4)]
Q: Whom does the ad address, in which language?
DEFAULT: Write to one typical buyer likely to want the thing, then do what a salesman would face to face (hop_sa_0014, 0008). The headline hails only the people you can interest (0031): put the word that flags them, or the city, in it (ogx_0007); an offer limited to a class beats a general one (hop_sa_0043). Originate copy in the audience's language — translating an English idea separates language from idea (nnn_0052); say it with respect, in a context the audience understands, to delight not intimidate (ppm_0001).
CHECK: One buyer named; the headline or opening line carries the word that hails them; copy written in its delivered language, not translated; nothing condescends.

CC-D10 [ASSERTED-hedged|QUALIFIED|DATED|MULTI-ORIGIN(2)]
Q: What does the audio layer carry?
DEFAULT: Actors on camera hold better than voice-over; supers say exactly the spoken words (ogx_0042); the CTA super is voiced in the same words (abcd_0021); the brand name spoken as well as shown (0012). Background music: no measurable good or harm; effects can help; jingles are below average at changing brand preference (ogx_0042). Full-funnel: hook attention with audio (abcd_0026). Premise: audio is heard (0014).
CHECK: Supers match voice-over word for word; brand name in audio; no jingle carries the message alone; on-camera speech over voice-over.

PRE-ARBITRATED CONFLICTS (the rule already decides; do not re-arbitrate):
CF-01 ogx_0040 vs ogx_0039: Frame one carries the surprise (0040); the name arrives within ten seconds, the ad ends on the pack (0039): surprise first, name never past ten seconds.
CF-02 mla_0064 vs mla_0010: Attract by curiosity about the thing sold (0010), never by amusement drawing the uninterested (0064).
CF-03 mla_0064 vs ogx_0032: Default no humour; only when a brief clause asks, register fits product and audience (whip_0058) and the joke carries the selling point — record the deviation on CC-D8.
CF-04 abcd_0017 vs abcd_0018: An engagement device lives inside the one message (0017); one needing a second message is cut (0018 yields).
CF-05 ogl_0014 vs ogl_0021: A style-admired treatment that displaces the product loses (0014); the criterion is selling (0021); style-led deviation needs a brief clause.
CF-06 sb_0012 vs sb_0017: Stakes always named, never over-dosed (0012 governs the dose); 0017's rules-cannot-be-broken framing is not compiled.
CF-07 ogx_0038 vs ogx_0034: A testimonial casts a real loyal user defending under challenge (0034); a celebrity is the below-average end (0038) and needs a brief clause.
CF-08 whip_0005 vs whip_0001: The quick get wins: say it straight first; keep cleverness only while a stranger gets it in one read (0001, uncompiled).

PACK LIMITS:
- Devanagari correctness criteria do not exist in Canon — never generate Devanagari glyphs; composite text deterministically.
- Coverage delta: ogx_* = 1983 US 30 s TV; hop_sa_*/mla_* = 1920s print and mail order; abcd_* = YouTube 2022, sound on. Nothing treats 9:16 feeds, sound-off viewing or ads under 10 s — assume neither way. CC-D3, D6, D10 are video-only; audio-only ads uncovered.
- India: only Hindi origination (nnn_0052) and Pandey's credo (ppm_0001) are compiled; other Indian languages, Hinglish, regional markets, Bijapurkar's consumer claims and Parameswaran's celebrity/ASCI claims are not — check ASCI outside Canon.
- Objective mix: Binet & Field's brand/activation findings are not compiled; no budget split or reach is set. Uncovered: Indian price/offer display (MRP, EMI) and platform-native CTAs (WhatsApp order, swipe-up); state the gap.

## OUTPUT
Write the JSON object to /tmp/blind/7cb5eaba.json (create the directory). Then reply with one line: the path and the number of beats.
