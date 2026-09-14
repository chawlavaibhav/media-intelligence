# CANON-BRIEF — Upwork intro film (60 s, fully AI-generated presenter + work)

Canon researcher output, 14 Sep 2026. Read-only research; nothing here is a Controller finding. Every line carries a knowledge id from `canon/knowledge/current/<source>/source-knowledge.yaml` or a compiled decision id (`CA-D*`, `PA-D*`). Paraphrase throughout; "our_reading" marks an inference Canon does not itself make.

## 1. How this project applies Canon

- **Accepted Canon only, fail-closed on HOLD** (`canon/knowledge/CANON-CORPUS-INDEX.yaml` `retrieval_note`; `canon/CANON-SHAPE-v1.md` §5). All 37 sources cited are accepted (`canon/audit/AUDIT-GATE-v0.2.md`). Two carry scoping markers: `google-abcd-video-ads` = `platform_contingent` (one platform, dated, publisher interest); `sontag-on-photography` = `critique_context` (never production advice) (`canon/planning/CANON-V1-LIVE37-COVERAGE.md`).
- **Cite by id; "render by id, never paraphrase"** (`canon/HANDOFF.md`; `CANON-SHAPE-v1.md` §5). Ids: `sk_whip_0053`; compiled decisions: `CA-D1`. Each object carries a confidence marker (MEASURED / REASONED / ASSERTED + CONTESTED, QUALIFIED, DATED, CULTURE-BOUND, MEDIUM-UNTESTED — `runtime/canon/INJECTION-PREFIX-v1.md`). Nearly everything relevant here is ASSERTED-hedged, SINGLE-ORIGIN, DATED, MEDIUM-UNTESTED. Prefix rule: a weak marker is "a reason for care, not silence".
- **Injection.** Normalized Request → table lookup (`canon/packs/pack-triggers-v0.yaml`) → packs as a cached system prefix, no receipts (`runtime/canon/packs.py`, `INJECTION-PREFIX-v1.md`; ruling C-10, `coordination/CONTROL-STATE.md`). A `video/generate` job would call four base packs plus typography, indian_indic and commercial_communication conditionals — but **only two packs exist** (`PACK-composition_and_attention-v0.yaml` CA-D1..D11; `PACK-product_appearance-v0.yaml` PA-D1..D10) and C-10 forbids compiling more. For this pilot Canon reaches the film through this brief's ids and the two packs' check lines.
- **Gate.** CANON-GATE-001 (`canon/gate/`): 21 check lines as code; blocking set = baked-text guard, delivered-vs-declared, named-ratio, integrity, extraction errors. Guard T1: any Devanagari codepoint in a prompt → FAIL. Both packs carry verbatim: **"Devanagari correctness criteria do not exist in Canon — never generate Devanagari glyphs; composite text deterministically."** A PASS "is structure, never quality".
- **What Canon cannot judge.** Whether Canon works (Controller-reserved, CONTROL-STATE); model capability (`CANON-SHAPE-v1.md` §1); audio (zero sources); Devanagari typography (A14 **absent**), animated type (B12), colour grading (B13); short-form grammar (B11), hooks (C09), Indian context (C13) **limited** (`CANON-V1-LIVE37-COVERAGE.md`). **No source covers Upwork profile videos, marketplace buyers, or AI-disclosed presenters.** Everything below transfers from print, TV and cinema and carries that discount.

## 2. Doctrine for the first 5 seconds

| id | principle | implication for this film |
|---|---|---|
| sk_ogx_0040 | First frame is the gate — "open with the fire"; one burr of singularity; many short scenes score below average | Frame 1 = the most striking finished ad or the presenter's sharpest line; no logo, no fade-in, no montage. |
| sk_abcd_0006, sk_abcd_0007 | Jump in: tight framing, open mid-action or on a close-up | Open tight and in progress; no establishing wide. |
| sk_abcd_0005 | Hook *and* sustain, audio with visual | A sound event synchronous with frame 1. |
| sk_abcd_0010, sk_abcd_0011, sk_ogx_0039 | Brand early and throughout; name within ten seconds; end on the package; attribution fails by default | Seller mark in the opening beat and the last frame. |
| sk_sb_c003_0015, sk_sb_c003_0014 | Grunt test: offer, benefit, next step within five seconds | By 0:05 a muted viewer can say "Meta ad creatives, fast." |
| sk_hea_mts_0010, sk_hea_mts_0011 | Surprise wins attention; a curiosity gap holds it | One category-expectation break (cf. sk_whip_0030), then a gap the work closes. |
| sk_hop_sa_0031, sk_hop_sa_0032, sk_ogx_0007 | The headline selects the reader; blind/clever openers attract the wrong ones; name the audience | First words flag "DTC / Meta ads"; ambiguity is a cost. |
| sk_whip_0001, sk_whip_0060 | The fuse must resolve inside the medium's dwell; two-second show-and-remove test | Test the first 2 s on a stranger; re-cut if they cannot say what it is for. |
| sk_god_0022 | Surface selects the audience before content | Grade, type and framing must read "premium agency", not "AI showreel", before a word lands. |
| sk_dpci_0090, sk_fre_c003_0020 | A face engages regardless of recognition; eyes pull hardest | Presenter face, eyes to lens, is a valid frame-1 candidate. |
| sk_jgb_0010 | Frontal gaze as a functional requirement | Into lens on first and last lines; never downcast on a claim. |
| sk_conv_c003_0017, sk_mla_0010 | Withholding fixates; undisclosed reward beats described | Do not list deliverables in the open; promise, then show. |
| sk_nse_0027 | First impression colours later evidence (halo) | Nothing rough before 0:05. |

## 3. Doctrine for the sales sequence and credibility

- **Definite figures.** A specific claim is believed because it could be caught being false; a number implies tests (sk_hop_sa_0051, sk_hop_sa_0052); superlatives are discounted and discredit the rest (sk_hop_sa_0050, sk_mla_0029, sk_ogx_0009). → "24 hours. Express, 4." "Four sizes. English and Hindi." Never "fast", "stunning", "best".
- **Result, not construction.** State the buyer's outcome, not the method (sk_mla_0009); the promise must matter to the buyer and be quantified (sk_ogx_0046, sk_ogx_0060); offer service, keep the seller's gain out of sight (sk_mla_0011, sk_hop_sa_0017). → "creatives you can test this week."
- **Customer hero, seller guide** (sk_sb_c003_0008, sk_whip_0015); name the want (sk_sb_c003_0009); a plan that removes risk (sk_sb_c003_0010); state the resolved state (sk_sb_c003_0013); dose stakes like salt (sk_sb_c003_0012). → Never "we are the best"; instead "you send the link; you get a straight price."
- **Demonstration over assertion** (sk_whip_0047, sk_mla_0004, sk_ogx_0035) — §4. "Yeah, right" is fixed by provable specifics, "so what" by relevance (sk_whip_0040).
- **Price.** Omitting price loses the reader (sk_ogx_0022); cheapness is not an appeal, a bargain is (sk_hop_sa_0039); price signals quality (sk_hop_sa_0040, sk_ogx_0067, sk_god_0029); economy appeals offend (sk_mla_0060). → Show the structure plainly; Express as paid add-on is a premium signal.
- **Risk transfer.** A guarantee impresses in proportion to visible risk accepted (sk_hop_sa_0041, sk_mla_0013). → State revision/refund terms once.
- **Named person.** A named individual outsells an impersonal offer (sk_hop_sa_0048, sk_mla_0018). → Name Vaibhav as the human who checks every file.
- **Positive framing.** Never attack a rival; show the condition desired (sk_sa8_0042); brand-insistence and boasting are the standard failures (sk_mla_0012). → No "unlike other AI creators".
- **Category.** Rational, high-consideration purchases favour activation specifics (sk_eic_0006); premium is built emotionally (sk_eic_0012); a specialist reader needs no decoration (sk_ogx_0047). → Specifics carry the sale; restraint carries the premium.

**The presenter is admittedly AI — is candour an asset?** No source covers this; the following is our_reading. Candour is believed because the speaker is seen to report negatives as readily as positives (sk_ctg_0004). Reassurance signals ("made with real cheese", stock handshakes) read as evidence *against* the claim; authenticity is scarce (sk_whip_0035). Unpolished, defensive testimony beats solicited praise; a polished performance is taken for a paid actor (sk_ogx_0034). Visible craft and apparent selling create resistance (sk_hop_sa_0011, sk_mla_0006). An idea must carry its own credentials — a way for the audience to test it (sk_hea_mts_0013). Photographic authority depends on the viewer believing a causal trace (sk_snt_0003); an AI presenter forfeits it, so pretending to it is the reassurance failure. Say "candour", not "honesty" — no accusation (sk_cat_c003_0002). **Implication:** disclose once, early, flatly, as fact; hand the credential to the work; name the accountable human; never repeat the disclosure. Counter-pull: a memorable face displaces the product (sk_ogx_0021, sk_ppm_0031) — keep presenter time small.

## 4. Doctrine for show-don't-tell and visual demonstration

- Showing beats telling; a demonstration needs no clever headline (sk_whip_0047); demonstrations persuade above average — never name a competitor in one (sk_ogx_0035). Show the product in use and its end result; close-ups pay when the product is hero (sk_ogx_0041, sk_ogx_0013). Pictures pay when they depict the condition the buyer covets (sk_sa8_0006) and must earn their space (sk_hop_sa_0026). → A finished ad, the four sizes fanning from it, the Hindi flip, the 10–15 s video ad — each an end result a media buyer covets.
- Craft minutiae produce identification (sk_conv_c003_0018); past a point, detail makes spectators (sk_murch_c003_0016). → One process beat (text locking into place); no tooling.
- **One boss per frame** (sk_whip_0053); every element added reduces every other (sk_whip_0003); two points make none (sk_whip_0004); only one clever element (sk_whip_0043); the removal test (sk_whip_0002). CA-D1: name the 1st/2nd/3rd read, one dominant cue each; competing cues confuse (sk_ms_c003_0019). Power by contrast, not "impact" (sk_vig_c003_0009).
- **See-say.** A visual repeating the headline is a rookie failure (sk_whip_0032); yet supers must match speech *exactly* (sk_ogx_0042, sk_abcd_0008). → Any super under the presenter is word-identical to the line; work sections carry text without voice.
- **Density.** Doing too much is a fault in itself (sk_abcd_0017); processing cost makes people tune out (sk_sb_c003_0003); a shot lasts as long as silently describing it takes (sk_gote_c003_0053, CA-D10).
- **Legibility numbers.** Text ≥ 4.5:1 against its background; large text (≥ 18 pt, or ≥ 14 pt bold) may drop to 3:1 (sk_wcag_0001, sk_wcag_0002, sk_wcag_0021); thin/unfamiliar letterforms suffer at low contrast (sk_wcag_0022, sk_wcag_0031); graphics 3:1 (sk_wcag_0006); colour never the only carrier (sk_wcag_0007); 4.499 fails (sk_wcag_0033). WCAG gives no mobile pixel minimum — our_reading: apply 14/18 pt at the phone's rendered scale and verify on a device. Text over image needs value contrast (sk_sam_c003_0021). All-caps retard reading (sk_alb_c003_0005, sk_ogx_0028); reverse type and headlines over the picture are named failures; approve at 20 inches, not 15 feet (sk_ogx_0028). Few can judge value across hues — grayscale check (sk_alb_c003_0018, CA-D5). Bright, high-contrast for small screens (sk_abcd_0009, platform_contingent).
- Peripheral details carry the judgement of a service the buyer cannot assess (sk_sut_alc_0020). → The exact price line, legal line and Devanagari line *are* the proof of care; make them the close-ups.

## 5. Doctrine for editing rhythm and shot grammar (60 s)

- **Murch's six:** emotion 51 > story 23 > rhythm 10 > eye-trace 7 > planarity 5 > 3-D space 4 (sk_murch_c003_0019–0025); sacrifice from the bottom up (sk_murch_c003_0027); a satisfied higher criterion hides lower failures (sk_murch_c003_0028); CA-D8. → An AI clip with imperfect continuity but a landed beat stays.
- The editor's material is the order and rate of information release (sk_murch_c003_0013); deciding not to cut is the larger part (sk_murch_c003_0017); over-cutting is the tour guide who cannot stop pointing (sk_murch_c003_0018); most with least (sk_murch_c003_0015).
- **Per cut:** new information (sk_gote_c003_0004) and a motivation to leave, usually movement or sound (sk_gote_c003_0006); CA-D7: name both, one device per beat. Compositions differ at the cut (sk_gote_c003_0026), >30° on the same subject (sk_gote_c003_0012, sk_gos_c003_0014); a noticed cut ejects the viewer (sk_gote_c003_0013) and degrades what follows (sk_gote_c003_0059); the best edit is unnoticed (sk_gote_c003_0058).
- **Shot count.** Many short scenes test below average (sk_ogx_0040); the three-second norm is called alarming (sk_gote_c003_0052); a self-sufficient shot is not cut apart (sk_gote_c003_0050). Our_reading: three presenter takes of 6–8 s plus 8–10 work shots of 3–5 s ≈ 12–14 shots, not 30.
- **Presenter grammar.** A monologue is broken by reaction shots of the listener (sk_gote_c003_0051) — here the listener is the work: cut to the ad the line refers to. A still frontal tableau supports direct address (sk_dpci_0010, sk_jgb_0010); one person, not crowds (sk_ogx_0015); head height reads neutral — right for trust beats, weak for a hook (sk_crl_0027); each face has a lens and distance at which it is most itself — test first (sk_conv_c003_0025); cutting closer amplifies a small gesture (sk_conv_c003_0016). **Canon gives no presenter shot size** — §9.
- **Camera.** Every move motivated, stillness chosen (sk_ms_c003_0002, CA-D11); a constant-pace push toward one face reads as inevitability (sk_ms_c003_0015); attention can move within a shot instead of cutting (sk_ms_c003_0010); the technique goes unnoticed (sk_ms_c003_0018). Screen direction persists (sk_gos_c003_0007, sk_gos_c003_0010, CA-D9). Wide→tight tradition (sk_gos_c003_0017) conflicts with the tight open (sk_abcd_0007): favour the hook, widen once, tighten again.
- **Sound.** Voice-over holds less than an actor on camera (sk_ogx_0042); sound builds reality faster than picture (sk_gote_c003_0048); sound bridges and L-cuts motivate transitions (sk_gote_c003_0007, sk_gote_c003_0022); music is inert, effects help, jingles below average (sk_ogx_0042); source music dodges the manipulation defence (sk_conv_c003_0009); opening music must not promise a film that does not follow (sk_conv_c003_0023).
- **Transitions.** Cuts by default; dissolves read languid and mean time manipulation (sk_gote_c003_0029–0031) — only for the morning→noon jump; a fade marks a boundary (sk_gote_c003_0037) — only at the end.
- **Pacing curve and ending.** Set context, then ask; direction grows more direct as the ad proceeds (sk_abcd_0025, sk_abcd_0026); the climax converts interest to an act before attention lapses (sk_mla_0063); end by moving the viewer (sk_whip_0059); on-screen CTA paired with spoken CTA (sk_abcd_0021); end on the package (sk_ogx_0039); tagline last, only if it survives alone with the mark (sk_whip_0057).

## 6. Doctrine for light, colour, premium feel

- Decide the fictional source first, then place the key to agree (sk_alt_c003_0011); one consistent direction — audiences read light untrained (sk_alt_c003_0026); PA-D4: one nameable source, no contradicting shadow. Mood is light character, not exposure (sk_alt_c003_0025, PA-D6); lighting follows the dramatic line (sk_alt_c003_0022). → Morning-to-noon is a per-shot lighting decision.
- One interior source photographs flat; fill, kicker, backlight restore roundness (sk_alt_c003_0009). Depth = tonal separation of figure from ground (sk_alt_c003_0015, PA-D5); distance dark→light (sk_alt_c003_0017); cold grounds separate warm faces (sk_alt_c003_0003).
- **Presenter skin.** Soft light flatters, hard exposes (sk_crl_0018); skin's small direct reflection must not be killed, and a larger source — not exposure — renders darker skin (sk_lsmx_0051); hard shadows buy depth but spend attention (sk_lsmx_0018).
- **Ads as objects.** Source sets light type, surface sets reflection type (sk_lsm_c003_0007); a shiny surface reports source size (sk_lsm_c003_0012); diffuse carries colour, direct carries material (sk_lsmx_0004); a reflected object proves gloss (sk_lsmx_0014). PA-D1..D3, PA-D8: one declared finish per object, highlight size agreeing with shadow softness, every specular wanted or removed. Shiny props are wanted (sk_alt_c003_0004).
- **Colour.** Never seen alone; one colour reads as two on different grounds (sk_alb_c003_0006, sk_alb_c003_0012); precision, not pleasantness (sk_alb_c003_0017); a colour set early identifies a figure later (sk_ms_c003_0016). Saturation is a public shout (sk_jgb_0020) — the opposite of understated. Colour pays where appearance is the appeal (sk_sa8_0008): the ads, not the presenter's world.
- **Restraint = premium.** Power by contrast of scale and weight (sk_vig_c003_0009); elegance and timelessness against lavishness (sk_vig_c003_0010–0012); spend visibly off the merit lessens effect (sk_sa8_0044); visible craft creates resistance (sk_mla_0006) — yet a cheap look rubs off on the product (sk_ogx_0008). Resolve by subtraction: negative space as a shape of equal weight (sk_sam_c003_0004), structure partly unrevealed (sk_sam_c003_0070), symmetry = authority or asymmetry = modern, held throughout (sk_sam_c003_0068), off-centre by default (sk_fre_c003_0018, CA-D2).

## 7. The Indian / Hindi dimension

- Show Hindi by **script and setting together**, unstyled (sk_nnn_0019). Text is a cultural barrier across languages; Indian posters go text-minimal (sk_dpci_0130) — *one* Hindi line, perfectly set.
- **Origination, not translation** (sk_nnn_0052): "written in Hindi, not translated" is a definite, checkable claim (sk_hop_sa_0051).
- Copy is regulated (banned words, ASCI: sk_nnn_0011, sk_nnn_0012). → "Legal text exactly right" is a real service; close-up on a correct legal line.
- A spoken word set as the picture itself (sk_nnn_0022) is a legitimate motion-text device for the Hindi flip.
- Avoid cliché: Hindi is not India — regional codes differ (sk_jgb_0040); saturation is the bazaar register (sk_jgb_0020); bazaar totems introduced *unfamiliar* products (sk_nnn_0043), and this buyer is not unfamiliar with ads. Difference is content on a universal template, not costume (sk_jgb_0050, sk_jgb_0150); hybrid "this as well as that" (sk_rbwl_0120); define your India (sk_rbwl_0170).
- Shared quality pool plus local nuance (sk_ppm_0030); respect, understood context, delight not intimidation (sk_ppm_0001).
- Frontal gaze and darshan (sk_jgb_0010, sk_dpci_0010) justify direct address without any Indian styling.
- **Hard limit:** never generate Devanagari glyphs; composite deterministically (pack limit; gate T1). Canon cannot check Devanagari (A14 absent) — Vaibhav must.

## 8. Anti-patterns AI showreels commit

- Thumbnail walls / montage: many short scenes below average (sk_ogx_0040); crowds don't pull (sk_ogx_0015); musical vignettes impotent (sk_ogx_0038); each element dilutes the rest (sk_whip_0003); doing too much (sk_abcd_0017); tour-guide editing (sk_murch_c003_0018).
- Generic epic/drone imagery: photogenic subjects yield substitutes (sk_crl_0028); irrelevant lures (sk_ogx_0047); stock imagery reeks (sk_whip_0035); learn the category's worn images (sk_whip_0030); the maker's interest is not the audience's (sk_ogx_0016).
- Claims without proof / superlatives: sk_hop_sa_0050, sk_mla_0029, sk_ogx_0009, sk_whip_0040; brand insistence and boasting (sk_mla_0012).
- All-caps, reverse type, headline over picture, approved at fifteen feet: sk_alb_c003_0005, sk_ogx_0028; exclamation marks read as desperation (sk_whip_0033).
- Four bold lines / no hierarchy: sk_whip_0053, sk_whip_0004, sk_whip_0043, CA-D1.
- Puns and clever openers: no persuasive value (sk_whip_0029, sk_ogx_0011, sk_hop_sa_0032).
- Fake social proof / invented characters (sk_whip_0034); the crowd-trend device needs a real trend (sk_mla_0027).
- AI persona as celebrity — remembered, product forgotten (sk_ogx_0021, sk_ppm_0031); brand as hero (sk_sb_c003_0008).
- Naming or attacking competitors: sk_ogx_0035, sk_sa8_0042.
- Unmotivated moves, wobble-as-realism: sk_ms_c003_0002; dissolves everywhere: sk_gote_c003_0031, sk_gote_c003_0034; supers that paraphrase the voice: sk_ogx_0042; jingles: sk_ogx_0042.
- Reassurance tells — "real", asterisked prices, repeated disclaimers: sk_whip_0035.
- Baked or generated Devanagari: pack limit, gate T1.

## 9. What Canon is silent on (record as learning)

Upwork profile video conventions and thumbnail/first-frame behaviour; muted autoplay (Canon's only sound claim is platform-contingent sound-on YouTube, sk_abcd_0014); AI-disclosed presenters and lip-sync tolerance; presenter shot size and eye-line-to-lens for trust; Devanagari typography (A14), animated type/motion design (B12), colour grading (B13), audio (no source); 60-s pacing curves; vertical vs horizontal for a profile; B2B freelance-buyer psychology (Hopkins scopes himself to mass-market goods, sk_mla_0002; Binet's data is brand campaigns, sk_eic_0024); how a global buyer reads an Indian seller; whether delivery-time claims (24 h / 4 h) are believed; captions for sound-off viewing.

## 10. Top-12 rules for the Creative Director

1. **sk_ogx_0040** — First frame is the gate; open with the fire; one singular image; few scenes.
2. **sk_whip_0047 + sk_mla_0004** — Demonstration outperforms assertion; hand the credential to the work.
3. **sk_hop_sa_0051 / sk_hop_sa_0052 + sk_mla_0029** — Definite figures are credited at par; superlatives discount everything.
4. **sk_whip_0053 + CA-D1** — One boss per frame; name the 1st/2nd/3rd read.
5. **sk_ogx_0042** — On-camera speech holds better than voice-over; supers word-identical to speech; music inert, effects help.
6. **sk_sb_c003_0008 + sk_whip_0015 + sk_sb_c003_0015** — Customer hero, seller guide; grunt test at five seconds.
7. **sk_murch_c003_0020 / sk_murch_c003_0027** — Emotion first; sacrifice continuity before emotion when AI clips are imperfect.
8. **sk_gote_c003_0004 / sk_gote_c003_0006 / sk_gote_c003_0053** — New information and motivation per cut; shot length = describable content.
9. **sk_whip_0035 + sk_ogx_0034** — Reassurance signals are read against the claim; unpolished candour is credible. Disclose once, flatly.
10. **sk_alt_c003_0011 / sk_alt_c003_0026 / sk_alt_c003_0025 + PA-D4/PA-D6** — One fictional light source, consistent direction; mood by light character.
11. **sk_wcag_0001 / sk_wcag_0021 + sk_ogx_0028 + sk_alb_c003_0005** — 4.5:1 (3:1 for ≥18 pt / 14 pt bold); no caps, no reverse type on picture; approve at reading distance.
12. **Pack limit (Devanagari) + sk_nnn_0052 + sk_nnn_0019** — Never generate Devanagari; composite exactly; claim origination not translation; script and setting together.

Reserve: sk_ogx_0039 (name early, end on package), sk_god_0022 (surface selects the audience), sk_vig_c003_0009 (contrast, not impact).
