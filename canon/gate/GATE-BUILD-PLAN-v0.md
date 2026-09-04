# CANON-GATE-001 — Gate build plan v0 (planner output; contract between maker and checker)

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
`coordination/CONTROL-STATE.md` governs.

**Authority:** `coordination/decisions/CONTROLLER-CANON-GATE-001-BUILD-AUTHORISATION-2026-09-03.md`
(all seven boundary conditions bind every line below). **Shape:** `canon/CANON-SHAPE-v1.md` §4.
**Doctrine:** `canon/compilation/PACK-product_appearance-v0.yaml` (PA-D1..PA-D10) and
`canon/compilation/PACK-composition_and_attention-v0.yaml` (CA-D1..CA-D11). **Evidence:**
`eval/experiments/EVAL-038/` (read-only). **Spend:** USD 0; zero provider calls; the paid text
detector is wired and never invoked.

This plan writes no code. The maker executes it test-first; the checker verifies against it and
against the packs. Where the plan says NOT MECHANISED, the maker does not attempt it.

## 0. Findings from the evidence that shape the plan

1. **The doctrine's check lines are mostly semantic.** They were authored as yes/no questions for
   the *model* to answer over its own output (`COMPILED-DOCTRINE-SPEC-v0` §1). Of 21 lines, none
   mechanises in full; 10 mechanise partially at pre-dispatch (a literal clause, usually a
   presence-of-declaration clause); 11 do not mechanise at all. Post-draw, without pixel decoding,
   only the artifact's dimensions/aspect/duration and (with a detector) baked text are checkable.
2. **Where the gate would have caught real defects.** Direct inspection of the committed artifacts
   (`judging/media/B01-video/V01-frame-2.jpg`, `V02-frame-1.jpg`,
   `media/E038-media-B06-sonnet-replay2.jpg`) confirms: V01 bakes garbled "Whatsapp" chips with
   nonsense numbers; V02 bakes "Rent reminurders" bubbles and a "99" badge; the B06 replay bakes
   "ASTER / MERIDIAN 38 / MECHANICAL" on the dial. M01 (haiku, accepted) and M02 carry no dial text.
3. **Package or draw?** For B01, **the packages were the defect.** Both dispatched prompts asked the
   generator for text-bearing content: Sonnet's shot-1 prompt requests "a smartphone screen filling
   with ... chat bubbles and a notification counter climbing past 99", "spreadsheet with a visible
   #REF! error", "laminated rent-rate chart"; Haiku's shot-1 prompt requests "smartphone screens
   showing overlapping WhatsApp conversations (green chat bubbles), email notifications (red
   badges)". Both packages' own DETERMINISTIC sections say screens/UI must be real assets — the
   prompts contradict their own plan. Sonnet's "no text overlays baked into video" clause forbids
   overlays only, not diegetic text. A pre-dispatch text guard catches both. For the B06 replay,
   **the draw was the defect** (prompt: "no text, no logos, no watermark"); only a post-draw scan
   catches it. The fixtures in §7 encode exactly this.
4. **Declared vs delivered.** The Sonnet B06 DELIVERABLE declares "1600×2000 px minimum"; every
   committed B06 artifact is 928×1152 (JPEG SOF, stdlib-parsed). The Haiku B01 shot durations sum
   to 16.5 s against a declared 30 s (reviewer-2 caught this by hand); the Sonnet B01
   HARD_CONSTRAINT_CHECK claims its shot list "≈ 30s" but it sums to 26 s. These are mechanisable
   consistency facts but they derive from no pack `check_id` — see §8 Q1.
5. **Receipts are retired.** `CANON-SHAPE-v1` §5 retires the per-check FAILURE_PREVENTION lines
   and DOCTRINE_DEVIATIONS as a production mechanism. The gate must therefore handle both a v1
   package (the 18 Sonnet baselines: 12 bare-heading sections) and a v2 package (the haiku/gemma
   runs: `##` headings, typed VISUAL_SYSTEM subfields, DOCTRINE_DEVIATIONS). Checks that need a v2
   field report NOT_RUN on v1, never PASS.
6. **Stdlib header parsing works on the committed artifacts.** JPEG SOF gives 928×1152; MP4
   `moov/trak/mdia/minf/stbl/stsd` gives `avc1` 720×1280 and `mvhd` gives 8.0 s. (`tkhd`
   width/height are 16.16 fixed-point at offset +76 for version 0 / +88 for version 1 — a quick
   probe with the wrong offsets returned garbage; the maker must unit-test against the committed
   MP4s.) PIL and numpy are absent (verified); PyYAML is present and is already the repo's
   validator/test convention for reading the packs.

## A. Check derivation table — one row per committed check line

Legend. **PRE** = pre-dispatch (over package text + generation prompts + dispatch descriptor).
**POST** = post-draw (over artifact bytes + dispatch descriptor + optional detector). **PARTIAL**
= the code tests the quoted literal clause as a *necessary* condition only; a PASS on a partial
check is printed as `PASS [partial: <clause>]` and never claims the whole line. **NOT MECH** =
not mechanised; reported as such with the reason; never counted as satisfied. Scan scope for a
partial check = the package sections named in that decision's committed `feeds_sections` (rendered
by id from the pack) plus GENERATION_PROMPTS. Every check text below is quoted verbatim from the
pack and must be *loaded from the pack at runtime*, never hard-coded.

| check_id | Committed `check` (verbatim) | PRE | POST | What the code tests / why not |
|---|---|---|---|---|
| PA-D1-check | "Every key object has exactly one declared finish; two surfaces of the same tone still read differently by finish; no surface reads as both matte and mirror-glossy in one shot." | PARTIAL | NOT MECH | PRE clause 1 (necessary): at least one FINISH term (§B vocab) occurs in scope. Object-to-finish binding and "exactly one" need the key-object list (the brief) — not available; clause 3 contradiction needs pixels or reliable noun-phrase binding — not attempted. POST: pixel + material judgment. |
| PA-D2-check | "Highlight positions agree with the single implied source; highlight brightness does not fall off with implied source distance; a large soft source reads as a large reflection, never a hard point." | NOT MECH | NOT MECH | Highlight geometry needs decoded pixels and scene understanding. "Single implied source" is not "one light instrument" (PA-D4 default allows added lights); counting light words would false-fail the accepted B06 packages (key + fill + kicker + background light). |
| PA-D3-check | "Shadow edge quality and highlight size agree — a soft shadow with a pinpoint specular, or the reverse, is a lighting contradiction." | NOT MECH | NOT MECH | Needs shadow/specular measurement in pixels; a prompt-vocabulary contradiction test false-fails legitimate kicker/rim requests. |
| PA-D4-check | "One nameable fictional source; key direction agrees with it; no shadow in frame contradicts the declared direction." | PARTIAL | NOT MECH | PRE clause 1 (necessary): some sentence in scope contains a LIGHT term and a DIRECTION term together (§B). Agreement and shadow contradiction need pixels. |
| PA-D5-check | "Product-to-ground tonal contrast survives a grayscale check; where depth planes are staged, nearer planes are darker than farther ones." | NOT MECH | NOT MECH | Grayscale check needs decoded pixels and product/ground segmentation; the artifacts are JPEG (no stdlib decoder). No literal pre-dispatch clause exists. |
| PA-D6-check | "Mood is attributable to light character — direction, hardness, contrast — not to a brightness slider; the key level is declared and consistent across shots." | NOT MECH | NOT MECH | "Key level declared" has no stable vocabulary in real packages (B06 Sonnet declares mood, not key level) — a strict test false-fails; cross-shot consistency needs pixels. |
| PA-D7-check | "State in one line what the hero image sells at a glance; if that line needs the body copy, the image fails." | NOT MECH | NOT MECH | The retro-test's decisive check is a semantic judgment ("needs the body copy"). Presence of a hierarchy line is not the check. Remains a human / blueprint-model check. |
| PA-D8-check | "Every specular on glass, dark or glossy surfaces is declared wanted or removed; none is accidental." | PARTIAL | NOT MECH | PRE (conditional, necessary): if a GLOSSY-SURFACE term occurs in scope, a SPECULAR-DECLARATION term must also occur (either polarity: "controlled reflection" or "no reflections"). If no glossy-surface term occurs → NOT_RUN "condition not detected", not PASS. POST: pixels. |
| PA-D9-check | "Count visible faces of the product; if a candidate angle shows more surfaces without breaking PA-D2 or PA-D5, prefer it." | NOT MECH | NOT MECH | Face counting needs object understanding in pixels; candidate comparison needs alternatives that do not exist at gate time. (An "angle is named" test is not a clause of this check and would be invented doctrine.) |
| PA-D10-check | "Every deviation from PA-D1..PA-D9 is listed in DOCTRINE_DEVIATIONS with its forcing brief clause; none is silent." | PARTIAL | NOT MECH | PRE (v2 only): DOCTRINE_DEVIATIONS present → every entry names a decision id `(PA\|CA)-D\d+` and carries a forcing clause (the word `because`, or `brief`, or a quoted string); the literal `none` is valid. Section absent → NOT_RUN "no DOCTRINE_DEVIATIONS section (schema v1 / receipts retired, CANON-SHAPE-v1 §5)". "None is silent" (undeclared deviations) is undetectable. |
| CA-D1-check | "Name the 1st/2nd/3rd read; each carried by exactly one dominant cue; no two cues compete for one beat." | PARTIAL | NOT MECH | PRE clause 1 (necessary): an ordered enumeration of ≥3 reads exists in scope — numbered list `1.`/`2.`/`3.`, or `1st/2nd/3rd read`, or `Primary/Secondary/Tertiary`. "One dominant cue" is semantic. |
| CA-D2-check | "Placement is stated as a zone plus the reason for it; no placement is justified by a named ratio or grid line." | clause 2 FULL; clause 1 PARTIAL | NOT MECH | Clause 2: FAIL if a NAMED-RATIO/GRID term (§B) occurs in scope outside a negation window. Clause 1 (necessary): a PLACEMENT term occurs in scope. "Reason for it" is semantic. |
| CA-D3-check | "The edge treatment is one of the three, named; no accidental near-tangency between a subject edge and a frame edge." | NOT MECH | NOT MECH | Real accepted packages describe edges in free prose ("generous clean negative space in the top 15 percent") that no closed vocabulary of Freeman's three treatments matches without false failures; tangency needs pixels. |
| CA-D4-check | "A framing element used is darker or thinner than the subject it frames." | NOT MECH | NOT MECH | Conditional on a frame-within-frame being used, then a tonal/width comparison in pixels. |
| CA-D5-check | "Declared balanced or deliberately restless; if balanced, a grayscale check shows tonal weight agreeing with size weight." | PARTIAL | NOT MECH | PRE clause 1: a BALANCE-DECLARATION term (§B: balanced, balance, restless, unbalanced, off-balance) occurs in scope. Grayscale weight needs pixels. Note: this partial FAILS the Sonnet B06 package (no declaration) — a true doctrine gap in a non-doctrine package; see §8 Q2. |
| CA-D6-check | "The stated aspect is justified by a named shape in the scene, not by the platform alone." | PARTIAL | PARTIAL | PRE (necessary): an aspect is stated in DELIVERABLE ∪ VISUAL_SYSTEM ∪ prompts (`\b\d{1,2}:\d{1,2}\b` or square/portrait/landscape/vertical/horizontal). POST (necessary): the artifact's w/h equals the stated/dispatched aspect within tolerance (§E) — an artifact that is not the stated aspect makes the check unanswerable. "Justified by a named shape" is semantic; and when the brief fixes the aspect, INJECTION-CONTRACT §3.1 makes justification moot (the gate does not read the brief). |
| CA-D7-check | "Per cut, name the new information and motivation; per beat, state the one device: cut, camera move, or blocking." | PARTIAL | NOT MECH | Video/image_sequence only. PRE (necessary): PRODUCTION_RECIPE ∪ GENERATION_PROMPTS contains ≥2 shot entries (table rows `\| *\d+ *\|`, `Shot \d+`, or numbered items) — without per-shot structure there is nothing to name a cut against. Content of "new information/motivation/device" is semantic. |
| CA-D8-check | "An imperfect cut names the bottom criteria sacrificed; never sacrifice emotion for eye-trace, planarity or 3D continuity." | NOT MECH | NOT MECH | Edit-room judgment; no detectable trigger for "imperfect cut". |
| CA-D9-check | "Screen direction and side-of-frame persist across consecutive shots, or something on screen shows the change (gos_0007), or the crossing is declared in DOCTRINE_DEVIATIONS." | NOT MECH | NOT MECH | Needs per-shot spatial understanding (pre) or frame analysis (post). |
| CA-D10-check | "No shot outlasts its describable content; the stated pace names the prevailing norm it assumes." | PARTIAL | NOT MECH | Video only. PRE clause 2 (necessary): a pace is stated — shot durations present (`\d+(\.\d+)?\s*(s\|sec\|seconds)` or `\d+–\d+ seconds`) in PRODUCTION_RECIPE ∪ AUDIO_AND_EDIT ∪ GENERATION_PROMPTS. "Outlasts describable content" is semantic. |
| CA-D11-check | "Each camera move names its motivation; unmotivated moves are replaced by stillness or a cut." | NOT MECH | NOT MECH | Motivation is stated at plan level, not sentence-locally ("fast whip-pans" are motivated by the chaos grade in VISUAL_SYSTEM); any sentence-local test false-fails. |

**Tally:** pre-dispatch — 10 partial (one clause fully mechanised: CA-D2 clause 2), 11 not
mechanised; post-draw — 1 partial (CA-D6), 20 not mechanised. Every one of the 21 ids appears in
every gate report, in every status.

### A.1 Two check families with a committed source other than a `check_id` (Controller ruling required — §8 Q1)

| id | Committed source (verbatim) | PRE | POST | What the code tests |
|---|---|---|---|---|
| LIMIT-TEXT | Both packs, `pack_limits`, exact-string validated by `validate_compiled_pack.py` check (8): "Devanagari correctness criteria do not exist in Canon — never generate Devanagari glyphs; composite text deterministically." Also named first in `CANON-SHAPE-v1` §4 and in the authorisation ("baked-text scan first"). | FULL (§D T1–T3) | FULL when a detector is configured; NOT_RUN otherwise | PRE: the prompt must not ask the generator to render glyphs (Devanagari codepoints; requested text; text-bearing surfaces). POST: the draw must contain no text (detector). |
| DISPATCH-* | `CANON-SHAPE-v1` §4 ("brief-fixed parameters honoured") and `INJECTION-CONTRACT-v0` §3.1 ("a deliverable parameter fixed by the brief ... takes precedence"). **Not a pack check_id.** | FULL | FULL | Package-stated aspect = dispatched aspect; sum of shot durations ≈ declared duration; artifact aspect/dimensions/duration = dispatched/declared. Printed under a separate `dispatch` heading, never counted as a doctrine check. Build only if the Controller rules it admissible; otherwise omit and keep CA-D6's aspect clause only. |

## B. Module layout — `canon/gate/`

All modules: Python 3 stdlib + PyYAML (to read the packs; existing repo convention). No network,
no `os.environ` reads anywhere under `canon/gate/` (test-enforced), no writes under `canon/`.

| File | Responsibility | Public signatures |
|---|---|---|
| `__init__.py` | package marker; module docstring carries the STATUS line and the "PASS establishes structure, never quality" sentence | — |
| `doctrine.py` | render-by-id registry of the 21 check lines from the two committed packs; per-decision `feeds_sections`; pack applicability by request; cheap fail-closed HOLD scan at load (id-shaped tokens in the pack files against `canon/candidates/**/source-knowledge.yaml` and `source-concept-systems.yaml`, same regex as `validate_compiled_pack.py`); refuses a pack whose `check_id != decision_id + "-check"` or whose decision count is not 10/11 | `load_registry(pack_paths=PACK_PATHS) -> Registry`; `Registry.checks: dict[str, CheckLine(check_id, decision_id, pack_id, text, feeds_sections, question)]`; `select_packs(modality: str, product_entity: bool) -> list[str]` (mirrors `pack-triggers-v0.yaml`: composition_and_attention for static_image/video/image_sequence; product_appearance iff product entity; audio → none); `applicable(check_id, modality) -> bool` (CA-D7/8/9 video+image_sequence; CA-D10/11 video only) |
| `package.py` | FINAL_PRODUCTION_PACKAGE parser for v1 and v2; section regex identical to `eval/experiments/EVAL-038/tools/strip_blind.py::SECTION_RE`; v2 subfield split; generation-prompt extraction; shot-list and duration extraction | `parse_package(text) -> Package(sections: dict[str,str], subfields: dict[str,str], schema: 'v1'\|'v2')`; `extract_prompts(pkg) -> list[Prompt(index, text, origin)]` (double-quoted runs ≥120 chars under GENERATION_PROMPTS, and `>` blockquote runs with `**` removed — **amended by Ruling 9, `CONTROLLER-CANON-GATE-001-FIFTH-CHECK-DISPOSITION-2026-09-05.md`: a quoted run under the 120-char floor is an extraction ERROR, never silently ignored**); `extract_shots(pkg) -> list[Shot(label, duration_s_min, duration_s_max, text)]`; `declared_aspect(pkg) -> str\|None`; `declared_duration_s(pkg) -> float\|None`; `declared_min_dimensions(pkg) -> tuple\|None` |
| `vocab.py` | every recogniser vocabulary as a frozen constant annotated with the check_id it serves and the pack words it extends; a module-level CHANGELOG list (tuning is Controller-visible) | constants only (see §B.1) |
| `findings.py` | result model, verdict, renderers | `Status` enum {PASS, FAIL, NOT_MECHANISED, NOT_APPLICABLE, NOT_RUN, ERROR}; `CheckResult(check_id, family: 'doctrine'\|'limit'\|'dispatch'\|'infra', gate: 'pre_dispatch'\|'post_draw', status, coverage: 'full'\|'partial'\|'none', clause: str, source_text: str, detail: str, evidence: tuple[str,...])`; `Report(gate, inputs: dict[str,str] (path→sha256), packs_selected, results: list[CheckResult])`; `Report.verdict() -> 'PASS'\|'FAIL'`; `Report.render_text() -> str`; `Report.to_json() -> dict` |
| `predispatch.py` | the pre-dispatch checks, one function per mechanised id, each returning exactly one `CheckResult`; the runner appends NOT_MECHANISED / NOT_APPLICABLE rows for every registry id it did not run | `run_predispatch(package_text: str, prompts: list[str]\|None, dispatch: dict\|None, modality: str, product_entity: bool, registry: Registry) -> Report` |
| `artifact.py` | stdlib container probes | `probe(data: bytes) -> ArtifactInfo(kind: 'image'\|'video'\|'unknown', container: 'png'\|'jpeg'\|'mp4'\|..., width, height, duration_s, has_video_track, has_audio_track, codec, notes)`; `probe_png`, `probe_jpeg`, `probe_mp4`; raises `ProbeError` on truncated/malformed input (→ ERROR, gate fails closed) |
| `textscan.py` | Devanagari codepoint scan; detector protocol; offline detectors; the wired-but-refusing Cloud Vision adapter | `devanagari_spans(text) -> list[str]`; `class TextDetector(Protocol): detector_id: str; def detect(self, image_bytes) -> TextDetection(status: 'text'\|'no_text'\|'unavailable', transcript: str, detector_id: str, raw: dict)`; `NoDetector` (always `unavailable`); `ScriptedDetector(results: dict[sha256, TextDetection])` (unknown digest → `unavailable`); `CloudVisionTextDetection(transport=RefusingTransport())` with `build_request(image_bytes) -> dict` (shape identical to `eval/empirical-tranche-1/ocr_providers.py`: `TEXT_DETECTION`, no `languageHints`, `maxResults: 1`), `parse(raw) -> TextDetection`, `detect()`; `RefusingTransport.__call__` raises `SpendNotAuthorised("CANON-GATE-001 authorises zero provider calls; invoking Cloud Vision TEXT_DETECTION needs a separate spend authorisation")` before any socket |
| `postdraw.py` | post-draw runner | `run_postdraw(artifact_bytes: bytes, dispatch: dict, package_text: str\|None, detector: TextDetector, frames: list[bytes]\|None, modality: str, product_entity: bool, registry: Registry) -> Report` |
| `run_gate.py` | CLI, invoked from the repo root like `canon/validation/validate_*.py`; exit 0 on PASS, 1 otherwise; `--json PATH` writes the report | `main(argv=None) -> int`. `python3 canon/gate/run_gate.py pre --package P.txt [--prompt-file F ...] [--dispatch request.json] --modality {static_image,video,image_sequence,audio} [--product] [--packs a,b] [--validate-packs]`; `python3 canon/gate/run_gate.py post --artifact A --dispatch request.json [--package P.txt] [--frames DIR] [--detector none\|scripted:FILE.json] --modality ... [--product]` |

Dispatch descriptor = the committed `*.request.json` shape: `parameters.aspectRatio` /
`parameters.durationSeconds` / `parameters.resolution` (video) or
`generationConfig.imageConfig.aspectRatio` (image). `--validate-packs` runs
`validate_compiled_pack.validate_pack` on both packs (≈15 s; not the default). The cheap HOLD scan
in `doctrine.py` always runs.

### B.1 Recogniser vocabularies (v0; implementation, not doctrine; each constant cites its check_id)

- `FINISH_TERMS` (PA-D1; pack words: diffuse, matte, direct, glossy, glare) + {gloss, polished, brushed, satin, mirror, sheen, specular, reflective, frosted, lacquer, metallic}.
- `LIGHT_TERMS` (PA-D4): {key light, key, light source, softbox, soft box, window light, daylight, sunlight, tube-light, tubelight, lamp, practical, backlight, rim light, kicker, fill, spotlight, overhead light, "lit from", "light from"}.
- `DIRECTION_TERMS` (PA-D4): {upper-left, upper left, top-left, top left, upper-right, upper right, top-right, from the left, from the right, from above, from behind, from the side, camera-left, camera-right, overhead, behind, side, front, `\d+\s*°`, `\d+\s*degrees`, window}.
- `GLOSSY_SURFACE_TERMS` (PA-D8): {glass, crystal, sapphire, bottle, mirror, chrome, polished, glossy, lacquer, black, dark surface, dark background}. `SPECULAR_DECLARATION_TERMS` (PA-D8): {reflection, reflections, specular, speculars, highlight, highlights, glint, glare}.
- `READ_ORDER_PATTERNS` (CA-D1): `^\s*(?:[-*]\s*)?(?:\*\*)?(?:1|2|3)[.)]`, `\b(?:1st|2nd|3rd)\s+read`, `\b(?:Primary|Secondary|Tertiary)\b`.
- `NAMED_RATIO_GRID_TERMS` (CA-D2 clause 2): {rule of thirds, rule-of-thirds, thirds grid, golden ratio, golden section, golden mean, golden spiral, divine proportion, fibonacci, phi grid, grid line, gridline, "intersection of the thirds", "power point", "power points"}. Deliberately excludes bare "third"/"lower third"/"upper-middle third" (zone descriptions in the accepted B06 package). `NEGATORS` = {no, not, never, without, avoid, "rather than", "never a", zero} within 4 tokens before the term → not a hit.
- `PLACEMENT_TERMS` (CA-D2 clause 1): {centre, center, off-centre, off-center, left of centre, left of center, right of centre, right of center, upper, lower, zone, positioned, placed, placement}.
- `BALANCE_TERMS` (CA-D5): {balanced, balance, restless, unbalanced, off-balance, "refuse the eye"}. Deliberately excludes "symmetrical" ("clean symmetrical dial layout" describes the dial, not the frame).
- `ASPECT_PATTERN` (CA-D6): `\b\d{1,2}:\d{1,2}\b` plus {square, portrait, landscape, vertical, horizontal}.
- `SHOT_PATTERNS` (CA-D7): table rows `^\|\s*\d+\s*\|`, `^#{0,4}\s*(?:\*\*)?Shot\s+\d+`, `^\s*\d+[.)]\s`. `DURATION_PATTERN` (CA-D10, DISPATCH): `(\d+(?:\.\d+)?)(?:\s*[–-]\s*(\d+(?:\.\d+)?))?\s*(?:s\b|sec\b|secs\b|seconds?\b)`.
- Text guard vocabularies: §D.

## C. Result model, verdict, and what the gate prints

Statuses: **PASS** (the tested clause holds), **FAIL** (it does not), **NOT_MECHANISED** (the
line cannot be tested by code; reason mandatory), **NOT_APPLICABLE** (pack not selected for this
request, or modality excludes the check; reason quotes the trigger rule or the check's own words),
**NOT_RUN** (mechanisable but an input is missing: no DOCTRINE_DEVIATIONS section, no detector,
no frames, no declared dimensions), **ERROR** (input unparsable — fails closed).

Verdict: `FAIL` if any result is FAIL or ERROR; else `PASS`. Nothing else influences it. There is
no severity tier and no "pass with gaps" (that would convert unrun checks into passes).

Invariants (test-enforced): every report carries exactly one row per registry id (21) plus the
LIMIT-TEXT row and any DISPATCH rows; every NOT_MECHANISED / NOT_APPLICABLE / NOT_RUN row has a
non-empty reason; every doctrine row carries `source_text` equal to the pack's `check` string.

Text rendering, mirroring `validate_compiled_pack.py`:

```
CANON GATE v0 — pre-dispatch — package E037-sonnet-no-canon-B01-R1.txt (sha256 …) — packs: composition_and_attention
FAIL            LIMIT-TEXT      prompt 1, sentence 2 requests text-bearing surfaces ('chat bubbles', 'notification counter') with no illegibility/deferral term — source: pack_limits "… composite text deterministically."
PASS            CA-D1-check     [partial: "Name the 1st/2nd/3rd read"] ordered reads in MESSAGE_AND_INFORMATION_HIERARCHY (5 items)
FAIL            CA-D5-check     [partial: "Declared balanced or deliberately restless"] no balance/restless declaration in VISUAL_SYSTEM, GENERATION_PROMPTS, FAILURE_PREVENTION
NOT-MECHANISED  PA-D2-check     highlight geometry needs decoded pixels and scene understanding — not counted as satisfied
NOT-APPLICABLE  PA-D1-check     product_appearance not selected (trigger table: no product/packshot entity)
NOT-RUN         PA-D10-check    no DOCTRINE_DEVIATIONS section (schema v1 / receipts retired, CANON-SHAPE-v1 §5)
…
GATE FAIL (2 failing checks). 7 checks mechanised (all partial) over 21 doctrine check lines; 14 lines NOT mechanised, not applicable or not run — never counted as satisfied.
```

and on success the final line is exactly:

```
GATE PASS: <n> mechanised checks hold over the submitted bytes; <m> doctrine check lines NOT mechanised, <k> not applicable, <j> not run — none counted as satisfied. This establishes structure over the prompt/artifact bytes — not doctrine satisfaction, quality, outcomes, or adoption.
```

A partial PASS always prints its clause in brackets; the words "doctrine satisfied" never appear.

## D. The baked-text scan (first, both gates)

Source: the verbatim pack limit line (§A.1). Scope: the gate inspects **draws**, never final
composites — composited text is the deterministic path the limit line prescribes. v0 carries no
"text deliverable" exemption: no route is exactness-qualified (`CONTROL-STATE.md`: Registry 0,
strict exactness disqualified), so a text deliverable still generates a text-free plate and
composites its text.

**Pre-dispatch text guard (`LIMIT-TEXT`, over each extracted generation prompt, sentence-split on
`[.;!?]\s+|\n`):**

- **T1 Devanagari** — any codepoint in U+0900–U+097F or U+A8E0–U+A8FF → FAIL (literal: "never generate Devanagari glyphs"). Full.
- **T2 Requested rendered text** → FAIL when a sentence contains (a) a quoted string of ≥2 word characters (straight or curly quotes) together with a TEXT_VERB {reading, reads, says, saying, labeled, labelled, titled, text, caption, headline, tagline, subheading, wordmark, lettering, "with the words", displays, displaying, showing, shows}, or (b) a TEXT_REQUEST term {caption(s), subtitle(s), headline, tagline, title card, typography, lettering, wordmark, logo, on-screen text, text overlay, watermark, "text reading", "label reading"} — unless a NEGATOR sits within 4 tokens before the term, or the sentence contains a DEFERRAL term {added in post, in post, post-production, composited, composite, deterministic, overlay later, reserved for, space reserved, to be added}. Known limitation (accepted, conservative): sentence-level deferral exempts Sonnet's shot-11 "RentOK logo animates … CTA text to be added in post" sentence; the other B01 prompts still fail.
- **T3 Text-bearing surfaces** → FAIL when a sentence contains a TEXT_SURFACE term {chat bubble(s), chat thread, chat(s), conversation(s), message(s), notification(s), badge(s), counter, spreadsheet, excel, #REF, ledger, notebook, handwritten, sign, signage, chart, poster, receipt, invoice, price tag, menu, newspaper, dashboard, app icon, app screen, home screen, UI, interface, button, banner, phone screen, smartphone screen, laptop screen, screen showing, screen shows, screen filling, screens showing} and no ILLEGIBILITY/DEFERRAL term in the same sentence {illegible, unreadable, blurred, out of focus, blank, dark screen, switched off, screen replacement, replaced in post, green screen, greenscreen, placeholder, no legible, no readable, added in post, composited}. This is the subcheck that catches both B01 prompts.
- **Detail line** (no status effect): whether the prompt carries any explicit no-text clause.

**Post-draw scan (`LIMIT-TEXT`, artifact):** `detector.detect(bytes)`: `text` → FAIL quoting the
transcript; `no_text` → PASS with the detail "per <detector_id>; benchmark qualification never
certifies an individual output (EVAL-029)"; `unavailable` or `NoDetector` → NOT_RUN "no text
detector configured; the qualified detector (Cloud Vision TEXT_DETECTION) needs a separate spend
authorisation". Video: frames must be supplied (`--frames DIR` of JPEG/PNG; stdlib cannot decode
H.264); none → NOT_RUN "frame extraction not available in stdlib"; any frame `text` → FAIL.

**Detector interface and adapters:** as in §B `textscan.py`. `CloudVisionTextDetection` mirrors the
request/response handling of `eval/empirical-tranche-1/ocr_providers.py` (cited, not imported —
that module reads keys at dispatch and depends on the EMP-001 budget guard). Its default transport
refuses before any socket; no key, endpoint call, or `os.environ` read exists under `canon/gate/`.
Invoking it is a separate Controller spend authorisation, not a flag.

## E. Artifact inspection without PIL/numpy

Checkable from headers (stdlib `struct`):

- **PNG**: signature `89 50 4E 47 0D 0A 1A 0A`; IHDR at offset 8 → width, height (big-endian u32), bit depth, colour type.
- **JPEG**: `FF D8`; walk markers; standalone markers `D0–D7`, `D8`, `01` have no length; SOF markers {C0,C1,C2,C3,C5,C6,C7,C9,CA,CB,CD,CE,CF} → precision(1) height(2) width(2) components(1); stop at `DA` without SOF → ProbeError. EXIF orientation is not applied (documented limitation).
- **MP4/ISO-BMFF**: box walk with 32-bit size, `size==1` largesize, `size==0` to-EOF; `ftyp` required; `moov` may follow `mdat`; `mvhd` v0/v1 → timescale, duration; per `trak`: `mdia/hdlr` handler (`vide`/`soun`); for the video track `mdia/minf/stbl/stsd` first sample entry (`avc1`, `hvc1`, `hev1`, `mp4v`, `vp09`, `av01`) → width/height at entry offset +32/+34 (u16); `tkhd` matrix for 90°/270° rotation (swap w/h if rotated); `mdhd` as duration cross-check. Fragmented MP4 (`moof`, mvhd duration 0) → duration NOT_RUN.
- Other containers (WEBP, GIF, HEIC, MOV variants without `moov`) → NOT_RUN "unsupported container".

Checks built on the probe: **CA-D6 (post, partial)** artifact `w/h` vs dispatched aspect `a:b`,
absolute tolerance 0.01 on the ratio (928/1152 = 0.8056 vs 0.8 → Δ0.0056 PASS; 720/1280 = 0.5625
exact); **DISPATCH-DIMENSIONS** artifact ≥ declared minimum pixels when the package declares
one (`(\d{3,5})\s*[×x*]\s*(\d{3,5})` near "minimum|min|at least"), else NOT_RUN — the committed
B06 Sonnet package declares 1600×2000 and every B06 artifact is 928×1152 → FAIL (true gap);
**DISPATCH-DURATION** mvhd duration vs `durationSeconds` ±0.5 s; **INFRA** rows: container
recognised, video track present for a video dispatch, artifact sha256 equals `record.json` sha256
when a record is supplied.

**NOT checkable and not to be attempted:** anything requiring pixel values — text (without a
detector), grayscale contrast (PA-D5, CA-D5), highlight position/size (PA-D2/D3/D8), shadow
direction (PA-D4), tangency (CA-D3), framing-element tone (CA-D4), face counting (PA-D9), screen
direction and motion (CA-D9/D10/D11), colour or mood. (PNG pixel decoding via `zlib` is feasible in
stdlib but the production route emits JPEG; not built in v0.)

## F. Test strategy (maker works test-first; stdlib `unittest`, `python3 -m unittest tests.test_gate_*`)

Fixtures are the committed EVAL-038 files read in place (never copied or modified) plus in-memory
mutations and in-test synthetic bytes. Scripted detector results are a dict `sha256 → TextDetection`
in the test module, commented as encoding human-observed truth (reviewer notes in
`judging/verdicts/`, `RESULTS.md` replay note, and direct inspection), not a detector measurement.

| Test file | What it proves | Positive fixture(s) | Negative fixture(s) |
|---|---|---|---|
| `tests/test_gate_doctrine.py` | registry has exactly 21 ids; each `text` equals the pack `check`; `feeds_sections` rendered by id; every report lists all 21; every non-PASS row has a reason; no id-shaped token under `canon/gate/*.py` resolves outside accepted Canon (reuse the `validate_compiled_pack` regex); pack applicability per modality/product | the two committed packs | a pack copy with one `check_id` renamed or a HOLD id inserted (in a tempdir) is refused |
| `tests/test_gate_package.py` | v1 and v2 parsing (bare, `##`, `**bold**` headings); subfield split; prompt extraction reproduces the four committed `media/prompts/*.txt` after whitespace normalisation (`" ".join(split())`), consistent with `EXTRACTION-RECORD.json`; shot/duration extraction: Sonnet B01 → 11 shots summing to 26.0 s; Haiku B01 → 6 shots summing to 16.5 s (max of ranges) | `baseline/sonnet-no-canon/E037-sonnet-no-canon-B06-R1.txt`, `…-B01-R1.txt`, `runs/haiku-packs/packages/E038-haiku-packs-B06-R1.txt`, `…-B01-R1.txt` | a package missing GENERATION_PROMPTS → `extract_prompts` returns [] and the gate reports ERROR |
| `tests/test_gate_textscan.py` | T1 on a Devanagari string; T2/T3 on the four real prompts with expected sentence hits; negation and deferral windows; `NoDetector` → NOT_RUN; `ScriptedDetector`; Cloud Vision `build_request` equals the EMP-001 shape byte-for-byte for a fixed image; `parse` over the documented response shapes (`textAnnotations`, `fullTextAnnotation`, per-response `error`, top-level `error`, empty); default transport raises `SpendNotAuthorised` and `transport.calls == 0`; `grep`-style test that no file under `canon/gate/` contains `environ`, `urlopen`, or `vision.googleapis` outside the adapter's endpoint constant | B06 Sonnet prompt ("no text, no logos, no watermark" → PASS); B06 Haiku prompt (no request, no clause → PASS with note) | B01 Sonnet prompts 1 and 3 (T3, T2 → FAIL); B01 Haiku shots 1, 2, 6 (T3, T2, T2 → FAIL); B06 Sonnet prompt with "no " deleted before "text" → FAIL; B01 Sonnet sentence 2 rewritten with "screens dark and illegible" → clears |
| `tests/test_gate_predispatch.py` | per-check expected statuses on the four real packages (table below); mutations flip exactly the intended row | see table | insert "rule of thirds" into VISUAL_SYSTEM → CA-D2 FAIL; insert "not the rule of thirds" → still PASS; delete all finish words from B06 Sonnet prompt → PA-D1 FAIL; delete "from upper left" → PA-D4 FAIL; DOCTRINE_DEVIATIONS entry without id/because → PA-D10 FAIL |
| `tests/test_gate_artifact.py` | real JPEGs → 928×1152; real MP4s → 720×1280, 8.0 s, `avc1`, audio present; synthetic PNG/JPEG/MP4 bytes built in-test (tkhd v0 and v1, largesize box, `moov` after `mdat`, rotated matrix); aspect tolerance boundary | `media/E038-media-B06-*.jpg`, `media/E038-media-B01-*.mp4` | truncated JPEG (no SOF) → ProbeError → ERROR; GIF bytes → NOT_RUN; synthetic 1000×1000 PNG vs 4:5 → CA-D6 FAIL |
| `tests/test_gate_postdraw.py` | end-to-end over the six artifacts with dispatch = committed `*.request.json` and scripted detector | M01 (haiku) no_text → text PASS, aspect PASS, dims NOT_RUN (haiku declares no pixels) → GATE PASS; M02 no_text → text PASS, aspect PASS, DISPATCH-DIMENSIONS FAIL vs 1600×2000 (true gap; PASS if the DISPATCH family is not built) | replay image `text` ("ASTER MERIDIAN 38 MECHANICAL") → FAIL; V01/V02 with the committed `judging/media/B01-video/V0?-frame-?.jpg` frames scripted `text` → FAIL; V01 with no frames → text NOT_RUN, aspect/duration PASS |
| `tests/test_gate_cli.py` | `main([...])` exit codes; final-line idiom present verbatim on PASS; `--json` round-trips every row | pre on Haiku B06 → 0 | pre on Sonnet B01 → 1 |

Expected pre-dispatch statuses on the real packages (the fixture table the maker encodes; all
other doctrine rows are NOT_MECHANISED / NOT_APPLICABLE / NOT_RUN as per §A):

| Row | Haiku B06 (image, product, v2) | Sonnet B06 (image, product, v1) | Haiku B01 (video, no product, v2) | Sonnet B01 (video, no product, v1) |
|---|---|---|---|---|
| LIMIT-TEXT | PASS (note: no explicit no-text clause) | PASS | FAIL (shots 1, 2, 6) | FAIL (prompts 1, 3) |
| PA-D1 | PASS (brushed, matte) | PASS (brushed, polished) | N/A | N/A |
| PA-D4 | PASS ("key light from upper-left at 45°") | PASS ("key light from upper left") | N/A | N/A |
| PA-D8 | PASS (crystal → "no internal reflections", speculars) | PASS (crystal → "controlled reflection") | N/A | N/A |
| PA-D10 | PASS (2 entries, ids + clauses) | NOT_RUN | N/A | N/A |
| CA-D1 | PASS (1st/2nd/3rd read) | PASS (1–4 Primary…) | PASS | PASS (1–5) |
| CA-D2 | PASS / PASS | PASS / PASS | PASS / PASS | PASS / PASS |
| CA-D5 | PASS ("balanced") | **FAIL** (no declaration — true gap) | PASS ("deliberately unbalanced and restless") | **FAIL** (no declaration) |
| CA-D6 (pre) | PASS (4:5) | PASS (4:5) | PASS (9:16) | PASS (9:16) |
| CA-D7 | N/A (static) | N/A | PASS (6 shots) | PASS (11 rows) |
| CA-D10 | N/A | N/A | PASS | PASS |
| DISPATCH-SHOT-SUM (if built) | N/A | N/A | FAIL (16.5 vs 30, tol ±20%) | PASS (26 vs 30; detail prints 26) |
| **Verdict** | **PASS** | **FAIL** (CA-D5) | **FAIL** | **FAIL** |

The two FAIL verdicts on B01 match the human outcome (both videos rejected for baked text); the
PASS on Haiku B06 matches the accepted image; the Sonnet B06 FAIL is a declaration gap the
Controller must rule on (§8 Q2) — the test records it as expected so the maker cannot tune it
away silently.

Build order (each step: tests first, then code, then run `python3 -m unittest tests.test_gate_*`):
1 `findings.py` + `doctrine.py`; 2 `package.py`; 3 `textscan.py` + LIMIT-TEXT in `predispatch.py`;
4 remaining pre-dispatch checks in the order CA-D2, PA-D4, PA-D1, CA-D1, CA-D5, PA-D8, PA-D10,
CA-D6, CA-D7, CA-D10 (+ DISPATCH if ruled admissible); 5 `artifact.py`; 6 `postdraw.py`; 7
`run_gate.py` + CLI tests. The maker reports every check it could not build exactly as this plan's
NOT MECHANISED rows and must not add checks absent from §A / §A.1.

Registration: a `compiled_doctrine_gate` row may be added to `verify/VALIDATOR-INDEX.yaml` with
validator `python3 -m unittest tests.test_gate_predispatch tests.test_gate_postdraw` and
`establishes: [gate_verdicts_on_committed_eval038_fixtures]` — only if the Controller wants the
index to carry a non-evidence family (its header says evidence families only).

## G. Risks and open questions for the Controller

1. **Boundary 2 (render by id) vs the two non-`check_id` families.** LIMIT-TEXT derives from a
   committed, exact-string-validated pack limit line, not a `check_id`; the DISPATCH family derives
   from `CANON-SHAPE-v1` §4 / `INJECTION-CONTRACT` §3.1. Both are the evidence's highest-value
   mechanisable checks (baked text caught 3/5 artifacts; declared-vs-delivered gaps exist on 4/6).
   **Ruling needed:** admit LIMIT-TEXT (recommended: yes); admit DISPATCH as a separately-labelled
   non-doctrine family (recommended: yes) or drop it.
2. **Declaration-presence partials block non-doctrine packages.** CA-D5 (and, on other inputs,
   CA-D1/PA-D1/PA-D4) will FAIL a strong-model package written without the packs, on a literal
   clause. In the production shape every blueprint is written under the packs, so this is by
   design — but the Controller may prefer these to be dropped from the blocking set. The plan keeps
   the verdict binary; the fixture records the Sonnet B06 FAIL openly.
3. **The shape document is optimistic.** Of its pre-dispatch list — "declared finish per object,
   one light source, no in-image text, attention order named, brief-fixed parameters honoured" —
   only "no in-image text" and "brief-fixed parameters" mechanise fully; "declared finish" and
   "attention order named" only as presence checks; "one light source" cannot be mechanised without
   false failures. Post-draw, the "artifact checks" reduce to aspect/dimensions/duration plus a paid
   text scan; every artifact-content check line (PA-D2/3/5/8/9, CA-D3/4/5-grayscale, CA-D9) is
   not mechanisable in stdlib. The redraw loop in §4 therefore currently has one real trigger
   (text) plus geometry.
4. **Vocabularies are implementation and will need tuning.** Each constant is annotated with its
   check_id and carries a CHANGELOG; tuning outside a Controller-visible change is forbidden by
   this plan. False-failure risk is highest in T3 (text-bearing surfaces) and lowest in T1/T2.
5. **Receipt retirement leaves PA-D10 and v2-dependent checks NOT_RUN in production.** The
   Controller should say which package schema the production blueprint carries; keeping the four
   typed VISUAL_SYSTEM subfields (a plan, not a receipt) would make PA-D1/PA-D4/CA-D1/CA-D2 partials
   materially more reliable.
6. **Post-draw text scan is NOT_RUN until spend is authorised**; the scripted detector proves
   plumbing only; video additionally needs frame extraction outside stdlib (ffmpeg).
7. **Tolerances are uncalibrated**: aspect Δ0.01, duration ±0.5 s, shot-sum ±20 % (Sonnet B01's
   26 s vs "≈30 s" passes; Haiku's 16.5 s fails). Constants live in one place with the rationale.
8. **PyYAML** is the one non-stdlib import (reading the packs; existing validator/test convention).
   Confirm this satisfies boundary 7.
9. **The pack validator costs ≈15 s**; the gate performs a cheap HOLD scan at load and offers
   `--validate-packs`; this is a weaker fail-closed guarantee than re-validating on every run.
10. **The gate never reads the brief.** "Brief-fixed parameters honoured" is checked against the
    dispatch descriptor and the package's DELIVERABLE, not the customer brief; a package that
    mis-transcribes the brief's aspect passes the gate.
