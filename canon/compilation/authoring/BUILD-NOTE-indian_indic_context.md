# Build note — indian_indic_context (IN)

STATUS: PROPOSED — builder output for `coordination/decisions/CONTROLLER-CANON-COMPLETION-2026-09-22.md`; adoption is the Controller's step. USD 0; no model or provider call.

Files: `PACK-indian_indic_context.authoring.yaml` (authored), `canon/compilation/PACK-indian_indic_context-v0.yaml` (compiled). Loop: compiler `--only` green; `canon_done --pack` missing 0 (exit 2, PROPOSED); validator PASS; `--check` byte-stable across all 9 packs.

The corpus here is thin (LIVE37 `critical_limited`: one domain C13, five contributors, none of them a product-advertising manual). Six decisions, not eight: the contributors honestly support six producer questions, and the terse budget forced one merge and one cut (below). Every decision carries the contributors' own hedges in the DEFAULT text (one artist, undated, no counts, insider account, author's own likelihood, "not universally recognized"); no hedge was hardened.

## 1. Decisions

- **IN-D1** Language and script per surface — originate, never translate (nnn_0052); Hindi word + Devanagari beside the Latin logotype on one plate (nnn_0019); text as a cultural barrier across a multilingual territory (dpci_0130); Pandey's credo (ppm_0001) and local-team structure (ppm_0030).
- **IN-D2** Which India, and what transfers — name the target India from variables, not a stratum (rbwl_0170); regional codes are the main pre-press rejection ground and are learnable (jgb_0040); the analogy trap (rbwl_0090); hybrid adoption, "this as well as that" (rbwl_0120); star recognition is culture-bound (dpci_0090).
- **IN-D3** Visual register — sari grammar and colour code (dpci_0070); character types (dpci_0120); prop vocabulary (dpci_0040); melodramatic exteriority (dpci_0030); unstyled small-town setting (nnn_0019); the Diwali clay-lamp case (rbwl_0120); and the source's own expiry notice on all three cinema codes (dpci_0190) — period codes, never the current default.
- **IN-D4** Gaze — the calendar trade's frontal-gaze constraint (jgb_0010) on its precondition (jgb_0130); frontality/tableau as a reading category (dpci_0020); darshan at Dwyer's bounded strength (dpci_0010). The default is "decide per shot", not "be frontal": no contributor says a product ad should be frontal.
- **IN-D5** Celebrity — all three memorable (ppm_0031); star-as-character once use is universal (nnn_0041); the pre-test instrument effect (nnn_0040); the 2002 aura study with its caveats (nnn_0042); celebrity as the new bazaar totem, the author's own likelihood (nnn_0043); CC-D7 cross-referenced as another market and era.
- **IN-D6** Claims and clearance — ASCI as an institution and the 2007 cable sanction (nnn_0012); Animal Welfare Board route before approving an animal script, censor certificate for cinema shorts (nnn_0013); gori→nikhri recorded as history, not endorsed (nnn_0011). Everything else: "check outside Canon".

## 2. Seed coverage — 5 of 5

| seed | carried by |
|---|---|
| sk_dpci_0040 (props vocabulary) | IN-D3 |
| sk_dpci_0070 (clothing grammar) | IN-D3 |
| sk_dpci_0120 (character types) | IN-D3 |
| sk_nnn_0052 (Hindi origination) | IN-D1 (also CC-D9, CV-D9 — cross-referenced, not duplicated in substance) |
| sk_ppm_0001 (Pandey's credo) | IN-D1 (also CC-D9) |

## 3. Closure holes and resolutions

The seed packet prints stored-direction guards only; the compiler's undirected union surfaced three reversed `qualifies` edges (dpci_0190 → 0040/0070/0120; jgb_0180 → jgb_0010). Resolved:

- **sk_dpci_0040 / 0070 / 0120 qualified_by sk_dpci_0190** — CITED (IN-D3). This is the source's own expiry notice ("filmi style is a thing of the past" by 2002) and it changes the default: the codes are compiled as deliberate period codes, never the current default. A waiver here would have been exactly the hardening the independent checks caught elsewhere.
- **sk_jgb_0010 depends_on sk_jgb_0130** — CITED (IN-D4).
- **sk_dpci_0010 depends_on sk_dpci_0020** — CITED (IN-D4).
- **sk_jgb_0040 depends_on sk_jgb_0130** — CITED (IN-D4; pack-level closure).
- **sk_rbwl_0090 qualified_by sk_rbwl_0120** — CITED (IN-D2, IN-D3).
- **sk_dpci_0130 depends_on sk_dpci_0120**; **sk_dpci_0120 depends_on sk_dpci_0070** — CITED.
- **sk_jgb_0010 qualified_by sk_jgb_0180** — WAIVED: Jain's evidential bound types the interview evidence; IN-D4 already consumes 0010 typed that way (one artist, partly discursive). Same waiver CV-D9 carries for jgb_0090.
- **sk_rbwl_0170 depends_on sk_rbwl_0040, sk_rbwl_0060** — WAIVED: market-sizing argument and the value-orientation segmentation model; IN-D2 consumes only "name the target India from variables". Citing 0040 would have pulled its own chain (0050, 0030: survey-data and boom-cycle claims) into a creative pack.
- **sk_dpci_0010 qualified_by sk_dpci_0110** — WAIVED: overpainting, a craft the source closes by the 1990s; its "secular darshan" is weaker than the bound IN-D4 already applies.
- **sk_dpci_0120 depends_on sk_dpci_0100** — WAIVED: the star-portrait carrier of the type code; IN-D3 consumes the clothing carrier (0070, cited) and the code's non-universality. Introduced when IN-D5 (picture-vs-text) was cut (§5).
- **CF-01 sk_nnn_0041 contradicts sk_nnn_0042** — CONFLICT, not a stored guard: the source's own caveat says the two pull in different directions and are reconciled nowhere. Rule: 0042 speaks to which star, 0041 to how the star appears; neither is measured.

## 4. Limit lines and why

- Decision limits: IN-D1 (only Hindi origination attested; CC-D9 shares two ids; CC-D1/D7 own the line); IN-D2 (jgb_0040's codes are deity attributes for prints, not products or people).
- Pack limits: (a) coverage delta naming each contributor's era and object — market strategy to 2009, Hindi cinema/posters to 2002, calendar trade 1994–2001, one credo 2015, one insider survey 2016; nothing on 9:16, phones, sound-off, post-2016 India, and no contributor measures whether any of it sells. (b) Uncovered list — Hinglish/code-mixing, every non-Hindi language and script, English-vs-regional per surface, voice-over language, festival calendar/colour, family/gender/body norms, menswear, regional dress, modern home, food, jewellery, religious-imagery restraint, humour by region; A14 has no contributor. (c) Regulation — **ASCI is in the corpus only as an institution and its 2007 cable sanction (nnn_0012); the ASCI Code's rules, fairness/celebrity/influencer guidelines, celebrity due diligence, CCPA, MRP display and platform policies are not in Canon.** (The task brief said ASCI is not in the corpus; the precise state is: the body is, its rules are not.) The Devanagari line is added by the compiler.

## 5. Deliberately not compiled

- **IN-D5 "How much does the picture carry against the text, and on which recognisable figures?"** — drafted, then cut for budget (2,712 tokens with it after three tightening passes). It rested on dpci_0130/0120/0100/0080/0090: pre-1990 film-poster star doctrine, SINGLE-ORIGIN, and not on the producer-question list. Its two transferable points survive: text-as-cultural-barrier moved into IN-D1 (dpci_0130), the type code into IN-D3 (dpci_0120). Dropped with it: dpci_0100 (Bachchan's fixed features), dpci_0080 (persona persistence) and a CF-02 scoping 0080 against nnn_0041 by medium and era — named in the regulation limit line so the boundary is visible.
- An earlier IN-D3 "what transfers from a non-Indian source" was merged into IN-D2 (same ids, same question family) before the cut.
- Bijapurkar's consumer claims (rbwl_0020 demand structure, 0060 segmentation, 0150 stripped-down offers, 0160 unit of purchase, 0140 youth sampling) — strategy and pricing, not creative decisions.
- nnn_0055 social-cause platforms — recorded without outcome, no question a producer must answer.
- nnn_0050/0051 infant and star shooting-day hazards — production scheduling, not doctrine for the board.
- jgb_0020/0090/0130/0040 as colour and saturation doctrine — already in CV-D9; here 0040 and 0130 are cited only for regional-code checking and the frontal-gaze precondition.
- ppm_0010/0011 (research procedure), ppm_0020/0021 (client process) — agency practice, not an artifact decision.

No hedge was hardened: "seems", "almost invariably", "author's own likelihood", "no sample", "one artist", "partly discursive", "contested" are carried into the DEFAULT text.

## 6. Terse tokens

2,463 of 2,500 (9,852 chars); 27 cited sk objects, 19,498 cited claim bytes; 1 conflict, 5 waivers.

## 7. Session tokens

Roughly 150k tokens for this build (seed packet once, four claim batches by id, five compile iterations).
