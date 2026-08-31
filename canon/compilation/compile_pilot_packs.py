#!/usr/bin/env python3
"""Compile the two pilot doctrine packs: product_appearance and composition_and_attention.

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

Fresh code (REP-05). Nothing here is copied from commit 8115400. House rules inherited from
canon/experiments/v1/value-gate/build_oracle_contexts.py:
  1. render source text by id, never paraphrase by hand;
  2. fail closed on an id that does not resolve in canon/knowledge/current/;
  3. fail closed on a source whose Audit Gate record is not `complete`.

What is authored vs. rendered:
  AUTHORED (committed below, Canon judgment per the REP-05 brief): the per-decision question /
  default / check text, conflict resolution rules, closure waiver reasons, and limit lines.
  RENDERED (mechanical, by id): concept labels, ontology term definitions, confidence markers
  (via canon/compilation/assign_markers.py + the aggregation rule in
  canon/compilation/COMPILED-DOCTRINE-SPEC-v0.md), closure verification, origin counts
  (via canon/validation/validate_audit_gate_v02.independent_origins_ok), and the corpus digest
  (recomputed against canon/knowledge/CANON-CORPUS-INDEX.yaml accepted entries).

Fail-closed conditions (each a hard SystemExit, never a warning):
  unresolved id; id colliding with canon/candidates/; audit record not complete; stale corpus
  index (any listed file's bytes differ from its recorded sha256); closure hole not covered by
  citation, conflict entry, or waiver; terse rendering over budget.

Outputs (byte-stable: sorted keys, no timestamps, LF, UTF-8):
    canon/compilation/PACK-product_appearance-v0.yaml
    canon/compilation/PACK-composition_and_attention-v0.yaml

Usage:
    python3 canon/compilation/compile_pilot_packs.py           # write both packs
    python3 canon/compilation/compile_pilot_packs.py --check   # regenerate, fail on drift
"""
from __future__ import annotations

import hashlib
import importlib.util
import io
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from canon.compilation import assign_markers  # noqa: E402  (committed marker assigner, REP-04)

KNOWLEDGE = REPO_ROOT / "canon/knowledge/current"
CANDIDATES = REPO_ROOT / "canon/candidates"
RECORDS = REPO_ROOT / "canon/audit/records"
INDEX = REPO_ROOT / "canon/knowledge/CANON-CORPUS-INDEX.yaml"
ANNEX = REPO_ROOT / "canon/planning/PROPOSED-claim-dating-annex-v1.yaml"
AUDIT_GATE = REPO_ROOT / "canon/validation/validate_audit_gate_v02.py"
LEDGER = REPO_ROOT / "canon/candidates/ontology-join/cross-source-candidates-v0.yaml"

OUT_PA = REPO_ROOT / "canon/compilation/PACK-product_appearance-v0.yaml"
OUT_CA = REPO_ROOT / "canon/compilation/PACK-composition_and_attention-v0.yaml"

STATUS_LINE = (
    "PROPOSED — Canon-stream worker output; no Controller decision adopts it; "
    "coordination/CONTROL-STATE.md governs."
)

TERSE_MAX_TOKENS = 2500          # per pack; tokens = ceil(chars / 4)
GRADE_ORDER = ["ASSERTED", "REASONED", "MEASURED"]
FLAG_ORDER = list(assign_markers.FLAG_ORDER) + ["MEDIUM-UNTESTED"]

# ── verbatim limit lines (exact strings; the validator greps for them) ───────

DEVANAGARI_LIMIT = (
    "Devanagari correctness criteria do not exist in Canon — never generate Devanagari "
    "glyphs; composite text deterministically."
)
LSM_LATER_CHAPTERS_CAVEAT = (
    "Coverage caveat (GAP-16): light-science-magic ch3 is the only admitted chapter of its "
    "source; the source's later chapters are HOLD (not admitted) and are recorded as "
    "qualifying and in places reversing ch3 guidance. This pack cites that caveat's "
    "existence only and consumes no HOLD content."
)
PA_D9_PACKSHOT_LIMIT = (
    "Packshot convention absent from Canon (A13 application_unbound): hero-angle, "
    "label-legibility and scale-cue conventions are not in the corpus; this default is one "
    "1949 cinema-era claim — do not overgeneralize."
)
CA_D6_ASPECT_LIMIT = (
    "No accepted source treats fixed 9:16 feed frames (A01/G2): every aspect and "
    "orientation claim here predates vertical-feed formats; transfer is untested."
)
PA_COVERAGE_DELTA_LIMIT = (
    "Coverage delta (declared, not compiled): CANON-V1-LIVE24-COVERAGE.yaml lists "
    "dwyer-patel-cinema-india, jain-gods-in-the-bazaar and freeman-photographers-eye-graphic-guide "
    "as contributors to this pack's domains; none is compiled here — their doctrine "
    "(frontality/darshan staging, iconographic correctness, props-as-vocabulary) is absent, "
    "not arbitrated."
)
PA_CATEGORY_SURFACE_LIMIT = (
    "Category-surface gap: no accepted claim covers watch conventions (hand positions) or "
    "anisotropic brushed/sunburst surfaces — the diffuse/direct/glare contrast set (PA-D1) "
    "does not model radial anisotropic glow; state the gap rather than force one of the "
    "three types."
)
CA_COVERAGE_DELTA_LIMIT = (
    "Coverage delta (declared, not compiled): CANON-V1-LIVE24-COVERAGE.yaml lists "
    "dwyer-patel-cinema-india, jain-gods-in-the-bazaar, samara-making-breaking-grid-ch1 "
    "(term t_sam_c003_0018 only, CF-16) and alton-painting-with-light-ch2 for this pack's "
    "domains; no claim of theirs is compiled — their doctrine (frontality/darshan attention "
    "order, symmetry-as-authority, grid structure) is absent, not arbitrated."
)

# ── authored decision tables ─────────────────────────────────────────────────
# Every id below must resolve in canon/knowledge/current/ (the compiler fails closed).
# Text is terse, imperative, answer-shaped: a weak model edits a made decision,
# it never composes from principle (see canon/compilation/INJECTION-CONTRACT-v0.md).

PA_DECISIONS = [
    {
        "decision_id": "PA-D1",
        "question": "What reflection type dominates each key product surface — diffuse (matte), direct (glossy), or glare?",
        "default": "Declare a finish per named object before any prompt is written and light for the declared finish; the three reflection types are a contrast set (scs_lsm_c003_001) — finish is a property of the surface, not of the light.",
        "check": "Every key object has exactly one declared finish; two surfaces of the same tone still read differently by finish; no surface reads as both matte and mirror-glossy in one shot.",
        "ids": ["sk_lsm_c003_0001", "sk_lsm_c003_0002", "sk_lsm_c003_0003", "sk_lsm_c003_0004",
                "sk_lsm_c003_0010", "sk_lsm_c003_0008", "sk_lsm_c003_0015", "sk_lsm_c003_0020",
                "scs_lsm_c003_001"],
        "feeds": ["VISUAL_SYSTEM.surface_finish_per_key_object", "GENERATION_PROMPTS",
                  "FAILURE_PREVENTION"],
        "limits": [],
    },
    {
        "decision_id": "PA-D2",
        "question": "Where may the highlight sit on each glossy surface?",
        "default": "One highlight per surface, consistent with one implied source placed inside or outside the family of angles by intent (scs_lsm_c003_002); the reflection reports the source's size.",
        "check": "Highlight positions agree with the single implied source; highlight brightness does not fall off with implied source distance; a large soft source reads as a large reflection, never a hard point.",
        "ids": ["sk_lsm_c003_0013", "sk_lsm_c003_0014", "sk_lsm_c003_0011", "sk_lsm_c003_0012",
                "sk_lsm_c003_0006", "sk_lsm_c003_0008", "sk_lsm_c003_0020", "scs_lsm_c003_002"],
        "feeds": ["VISUAL_SYSTEM.implied_light_source", "PRODUCTION_RECIPE", "GENERATION_PROMPTS",
                  "FAILURE_PREVENTION"],
        "limits": [],
    },
    {
        "decision_id": "PA-D3",
        "question": "Hard or soft source?",
        "default": "Large/soft relative to subject for product surfaces unless the brief forces drama; choose the instrument for the shadow edge it must produce (sk_alt_c003_0006); for direct reflection the source's size sets the highlight's size (sk_lsm_c003_0014).",
        "check": "Shadow edge quality and highlight size agree — a soft shadow with a pinpoint specular, or the reverse, is a lighting contradiction.",
        "ids": ["sk_lsm_c003_0006", "sk_lsm_c003_0007", "sk_alt_c003_0006", "sk_lsm_c003_0014"],
        "feeds": ["PRODUCTION_RECIPE", "GENERATION_PROMPTS", "FAILURE_PREVENTION"],
        "limits": [],
    },
    {
        "decision_id": "PA-D4",
        "question": "What is the fictional light source, and does everything agree with it?",
        "default": "Name the fictional source first, then place the key to agree with it (sk_alt_c003_0011); build in the working order of scs_alt_c003_002 — one source photographs flat, added lights restore roundness (sk_alt_c003_0009), interiors imitate daylight's structure (0008); keep one consistent direction because audiences read light without being taught (0026).",
        "check": "One nameable fictional source; key direction agrees with it; no shadow in frame contradicts the declared direction.",
        "ids": ["sk_alt_c003_0008", "sk_alt_c003_0009", "sk_alt_c003_0011", "sk_alt_c003_0026",
                "sk_alt_c003_0018", "scs_alt_c003_002"],
        "feeds": ["VISUAL_SYSTEM.implied_light_source", "PRODUCTION_RECIPE", "GENERATION_PROMPTS",
                  "FAILURE_PREVENTION"],
        "limits": [],
    },
    {
        "decision_id": "PA-D5",
        "question": "How does the product separate from its ground?",
        "default": "By tonal separation, either direction (sk_alt_c003_0015). Scope rule: 0015 governs subject-against-ground; the dark-to-light progression (0017) governs only staged depth planes. Cold, plain grounds separate warm subjects (0003); a deliberately shiny prop (0004) trades off against a quiet ground — decide per object, never both on one surface.",
        "check": "Product-to-ground tonal contrast survives a grayscale check; where depth planes are staged, nearer planes are darker than farther ones.",
        "ids": ["sk_alt_c003_0015", "sk_alt_c003_0017", "sk_alt_c003_0003", "sk_alt_c003_0004"],
        "feeds": ["VISUAL_SYSTEM.placement_zone", "GENERATION_PROMPTS", "FAILURE_PREVENTION"],
        "limits": [],
    },
    {
        "decision_id": "PA-D6",
        "question": "What key level does the mood require?",
        "default": "Set the key by genre and mood before lighting anything (sk_alt_c003_0018); let level follow the dramatic line (0022); make mood with the character of the light, not exposure (0025); the fictional source still governs (0011).",
        "check": "Mood is attributable to light character — direction, hardness, contrast — not to a brightness slider; the key level is declared and consistent across shots.",
        "ids": ["sk_alt_c003_0018", "sk_alt_c003_0022", "sk_alt_c003_0025", "sk_alt_c003_0011"],
        "feeds": ["VISUAL_SYSTEM", "PRODUCTION_RECIPE", "FAILURE_PREVENTION"],
        "limits": [],
    },
    {
        "decision_id": "PA-D7",
        "question": "Does the imagery earn its space commercially?",
        "default": "Treat the picture as a salesman that must earn its space (sk_hop_sa_0026); assume the viewer decides from a glance at headline or picture (0035); size imagery by importance to the sale, never decoration.",
        "check": "State in one line what the hero image sells at a glance; if that line needs the body copy, the image fails.",
        "ids": ["sk_hop_sa_0026", "sk_hop_sa_0035", "scs_hop_sa_003"],
        "feeds": ["MESSAGE_AND_INFORMATION_HIERARCHY", "CORE_CREATIVE_IDEA", "FAILURE_PREVENTION"],
        "limits": [],
    },
    {
        "decision_id": "PA-D8",
        "question": "Glass, dark or mirror-glossy object in frame — special handling?",
        "default": "Dark subjects reveal direct reflection because they produce less diffuse reflection (sk_lsm_c003_0017); use the diagnostic guidelines to identify polarized reflection (0018); polarizing the source makes a reflection manageable (0019); polarized direct reflection is dimmer than ordinary direct reflection (0015).",
        "check": "Every specular on glass, dark or glossy surfaces is declared wanted or removed; none is accidental.",
        "ids": ["sk_lsm_c003_0015", "sk_lsm_c003_0017", "sk_lsm_c003_0018", "sk_lsm_c003_0019"],
        "feeds": ["PRODUCTION_RECIPE", "GENERATION_PROMPTS", "FAILURE_PREVENTION"],
        "limits": [],
    },
    {
        "decision_id": "PA-D9",
        "question": "Which angle is the hero angle?",
        "default": "The angle showing the most surfaces of the product (sk_alt_c003_0010) — Canon's only committed angle-choice criterion.",
        "check": "Count visible faces of the product; if a candidate angle shows more surfaces without breaking PA-D2 or PA-D5, prefer it.",
        "ids": ["sk_alt_c003_0010"],
        "feeds": ["PRODUCTION_RECIPE", "GENERATION_PROMPTS", "FAILURE_PREVENTION"],
        "limits": [PA_D9_PACKSHOT_LIMIT],
    },
    {
        "decision_id": "PA-D10",
        "question": "When may any of the above be overridden?",
        "default": "Technique serves a creative decision it does not make (sk_lsm_c003_0020): any default in this pack yields to an explicit creative decision recorded in DOCTRINE_DEVIATIONS with the brief clause that forces it.",
        "check": "Every deviation from PA-D1..PA-D9 is listed in DOCTRINE_DEVIATIONS with its forcing brief clause; none is silent.",
        "ids": ["sk_lsm_c003_0020"],
        "feeds": ["DOCTRINE_DEVIATIONS", "HARD_CONSTRAINT_CHECK"],
        "limits": [],
    },
]

PA_CONFLICTS = [
    {"conflict_id": "CF-01", "decision_ref": "PA-D5", "kind": "contradicts",
     "between": ["sk_alt_c003_0015", "sk_alt_c003_0017"],
     "nature": "symmetrical tonal separation against a preferred direction for distance; both stated in the source",
     "resolution_rule": "0015 governs subject-against-ground (either direction); 0017 governs progression across three or more staged depth planes (near dark, far light). Apply by which structure the frame has."},
    {"conflict_id": "CF-02", "decision_ref": "PA-D5", "kind": "trades_off_with",
     "between": ["sk_alt_c003_0003", "sk_alt_c003_0004"],
     "nature": "cold, quiet grounds against deliberately shiny props — speculars wanted on one, banned on the other",
     "resolution_rule": "Decide per object: a glossy prop keeps its declared speculars; the ground behind it stays cold and quiet. Never both treatments on the same surface."},
    {"conflict_id": "CF-03", "decision_ref": "PA-D6", "kind": "contradicts",
     "between": ["sk_alt_c003_0018", "sk_alt_c003_0011"],
     "nature": "musical comedy is exempted from the requirement that lighting agree with an established source",
     "resolution_rule": "Product and commercial imagery is not the exempt genre: follow 0011 (source agreement) unless the brief names a theatrical pastiche, and record that as a deviation."},
    {"conflict_id": "CF-04", "decision_ref": "PA-D1", "kind": "contradicts",
     "between": ["sk_lsm_c003_0004", "sk_lsm_c003_0010"],
     "nature": "diffuse reflection is angle-independent; direct reflection is a mirror image visible at one determined angle",
     "resolution_rule": "Scope by declared finish (PA-D1): 0004 governs matte/diffuse surfaces, 0010 governs glossy/direct surfaces. Both hold at once on different surfaces."},
    {"conflict_id": "CF-05", "decision_ref": "PA-D3", "kind": "contradicts",
     "between": ["sk_lsm_c003_0006", "sk_lsm_c003_0014"],
     "nature": "source size does not change a diffuse reflection; for direct reflection source size and placement change everything",
     "resolution_rule": "Scope by reflection type: 0006 governs diffuse surfaces; 0014 governs whether and how large the mirror image appears on direct surfaces."},
    {"conflict_id": "CF-06", "decision_ref": "PA-D2", "kind": "contradicts",
     "between": ["sk_lsm_c003_0008", "sk_lsm_c003_0012"],
     "nature": "diffuse brightness falls with distance by the inverse square law; a shiny surface reports the source's size, not its distance",
     "resolution_rule": "Scope by reflection type: apply falloff reasoning to diffuse surfaces only; on shiny surfaces reason about apparent source size."},
    {"conflict_id": "CF-07", "decision_ref": "PA-D2", "kind": "contradicts",
     "between": ["sk_lsm_c003_0011", "sk_lsm_c003_0008"],
     "nature": "the two reflection types respond oppositely to source distance",
     "resolution_rule": "Scope by reflection type: direct-reflection brightness is distance-independent (0011); diffuse follows the inverse square law (0008). Never apply one surface's rule to the other."},
    {"conflict_id": "CF-08", "decision_ref": "PA-D8", "kind": "cross_source_tension",
     "between": ["t_alt_c003_0021", "t_lsm_c003_0008"],
     "tension_ref": "T5", "ledger_record": "xj_0023",
     "ledger_file": "canon/candidates/ontology-join/cross-source-candidates-v0.yaml — candidate ledger cross-reference — unadopted, informational only (status: proposed; no candidates-lane content is consumed)",
     "nature": "Alton dresses sets with highly reflective objects so specular highlights give the image life, contingent on antihalo film stock (t_alt_c003_0021); LSM names a mirror image of the source appearing where the photographer does not want it the unwanted direct reflection (t_lsm_c003_0008)",
     "resolution_rule": "Apply PA-D8's check: every specular is declared wanted — a deliberately shiny prop keeps its highlights (sk_alt_c003_0004) — or identified and removed (sk_lsm_c003_0018, sk_lsm_c003_0019); technique serves the creative decision (sk_lsm_c003_0020). Alton's term is contingent on antihalo film stock (DATED)."},
]

PA_WAIVERS = [
    {"ref": "sk_alt_c003_0006", "relation": "depends_on", "partner": "sk_alt_c003_0007",
     "reason": "vocabulary dependency: 0007 is the studio's naming of light functions (keylight, crosslight, ...); the decision consumes only the shadow-quality criterion, which stands without the vocabulary."},
    {"ref": "sk_hop_sa_0026", "relation": "depends_on", "partner": "sk_hop_sa_0021",
     "reason": "evidential-basis dependency: 0021 states the mail-order school grounding Hopkins' authority; it is reflected in this decision's DATED and CULTURE-BOUND caution, not compiled as doctrine."},
    {"ref": "sk_hop_sa_0035", "relation": "depends_on", "partner": "sk_hop_sa_0031",
     "reason": "the headline-selection rule belongs to commercial_communication / typography_and_copy pack scope; this pack consumes only the glance test for imagery. Named here so the omission is visible."},
    {"ref": "sk_lsm_c003_0018", "relation": "depends_on", "partner": "sk_lsm_c003_0016",
     "reason": "mechanism explainer (the jump-rope/picket-fence polarization model); the diagnostic stands on the observed behaviour, and the analogy adds tokens without changing any check."},
    {"ref": "sk_lsm_c003_0019", "relation": "depends_on", "partner": "sk_lsm_c003_0016",
     "reason": "same mechanism explainer as above; the polarizer default stands on the behaviour, not the analogy."},
]

CA_DECISIONS = [
    {
        "decision_id": "CA-D1",
        "question": "What reads first, second, third?",
        "default": "One dominant element by contrast — visual power is achieved by contrast, not 'impact' (vig_0009); eyes attract more strongly than probably any other subject (fre_0020); competing cues confuse rather than direct (repeated focus-shifting is the type case, ms_0019); complete control of attention is self-defeating (murch_0018); misdirection (murch_0033) is the scoped exception, only to set up a reveal.",
        "check": "Name the 1st/2nd/3rd read; each carried by exactly one dominant cue; no two cues compete for one beat.",
        "ids": ["sk_fre_c003_0020", "sk_vig_c003_0009", "sk_murch_c003_0018", "sk_ms_c003_0019",
                "sk_murch_c003_0033"],
        "feeds": ["VISUAL_SYSTEM.attention_order", "MESSAGE_AND_INFORMATION_HIERARCHY",
                  "FAILURE_PREVENTION"],
        "limits": [],
    },
    {
        "decision_id": "CA-D2",
        "question": "Where does the subject sit in frame?",
        "default": "Off-centre within one of three approximate zones (fre_001; fre_0017, 0018); centre only when the scene points inward (0019); extreme placement needs a visible reason (0021). The source rejects coordinate rules (0016, vs its nod to classical proportion, 0028): zones are regions, never grids or named ratios.",
        "check": "Placement is stated as a zone plus the reason for it; no placement is justified by a named ratio or grid line.",
        "ids": ["sk_fre_c003_0015", "sk_fre_c003_0016", "sk_fre_c003_0017", "sk_fre_c003_0018",
                "sk_fre_c003_0019", "sk_fre_c003_0021", "sk_fre_c003_0028", "sk_fre_c003_0029",
                "scs_fre_c003_001"],
        "feeds": ["VISUAL_SYSTEM.placement_zone", "GENERATION_PROMPTS", "FAILURE_PREVENTION"],
        "limits": [],
    },
    {
        "decision_id": "CA-D3",
        "question": "How does the frame hold the subject at its edges?",
        "default": "One edge treatment per shot (fre_002): tight fit with a slight deliberate gap (fre_0006); busy scene, edges stop mattering (0005); deliberate halving of a symmetrical subject (0007). Straight subject edges near frame edges read magnetic (0003); thin any bright framing element (0004).",
        "check": "The edge treatment is one of the three, named; no accidental near-tangency between a subject edge and a frame edge.",
        "ids": ["sk_fre_c003_0002", "sk_fre_c003_0005", "sk_fre_c003_0006", "sk_fre_c003_0007",
                "sk_fre_c003_0003", "sk_fre_c003_0004", "sk_fre_c003_0030", "scs_fre_c003_002"],
        "feeds": ["VISUAL_SYSTEM", "GENERATION_PROMPTS", "FAILURE_PREVENTION"],
        "limits": [],
    },
    {
        "decision_id": "CA-D4",
        "question": "Use a frame within the frame?",
        "default": "No compulsion (fre_0022); when a subject passes behind an opening, the near-universal reaction is to shoot the moment it sits cleanly inside, breaking no edges; thin a bright framing element or it takes over (0004).",
        "check": "A framing element used is darker or thinner than the subject it frames.",
        "ids": ["sk_fre_c003_0022", "sk_fre_c003_0004"],
        "feeds": ["VISUAL_SYSTEM", "GENERATION_PROMPTS"],
        "limits": [],
    },
    {
        "decision_id": "CA-D5",
        "question": "Balance the frame, or refuse the eye rest?",
        "default": "Classical balance is the default; it weighs size AND tone together (fre_0028, 0029; fre_005); refusing the eye a resting place (0032) is the declared energetic exception. Symmetry imposes order on a subject that has none (0030); diagonals need strict horizontals and verticals to divide against (0033, 0034 per CF-07).",
        "check": "Declared balanced or deliberately restless; if balanced, a grayscale check shows tonal weight agreeing with size weight.",
        "ids": ["sk_fre_c003_0028", "sk_fre_c003_0029", "sk_fre_c003_0030", "sk_fre_c003_0032",
                "sk_fre_c003_0033", "sk_fre_c003_0034", "sk_fre_c003_0007", "sk_fre_c003_0016",
                "scs_fre_c003_005"],
        "feeds": ["VISUAL_SYSTEM", "GENERATION_PROMPTS", "FAILURE_PREVENTION"],
        "limits": [],
    },
    {
        "decision_id": "CA-D6",
        "question": "Which orientation and aspect?",
        "default": "Choose by the scene's shapes (fre_003): a vertical frame is not itself tallness (fre_0008); a square reads strict and draws the eye inward (0009, 0010); a wide frame needs shapes that call for it (0011).",
        "check": "The stated aspect is justified by a named shape in the scene, not by the platform alone.",
        "ids": ["sk_fre_c003_0008", "sk_fre_c003_0009", "sk_fre_c003_0010", "sk_fre_c003_0011",
                "scs_fre_c003_003"],
        "feeds": ["VISUAL_SYSTEM", "DELIVERABLE", "FAILURE_PREVENTION"],
        "limits": [CA_D6_ASPECT_LIMIT],
    },
    {
        "decision_id": "CA-D7",
        "question": "How does attention travel across cuts (video)?",
        "default": "Every new shot carries new information (gote_0004) and every departure is motivated (0006); drive eye-trace by alternating frame placement (0010), keeping difficulty near the optimum (0011); composition must differ at the cut (0026) — the wipe waives it (0035). Alternatives: move attention inside one continuous shot (ms_0010; ms_002), or block with a static wide (0017). One device per beat.",
        "check": "Per cut, name the new information and motivation; per beat, state the one device: cut, camera move, or blocking.",
        "ids": ["sk_gote_c003_0004", "sk_gote_c003_0006", "sk_gote_c003_0010", "sk_gote_c003_0011",
                "sk_gote_c003_0026", "sk_ms_c003_0010", "sk_ms_c003_0017", "sk_gote_c003_0035",
                "sk_ms_c003_0001", "sk_ms_c003_0004", "scs_ms_c003_002"],
        "feeds": ["AUDIO_AND_EDIT", "GENERATION_PROMPTS", "FAILURE_PREVENTION"],
        "limits": [],
    },
    {
        "decision_id": "CA-D8",
        "question": "When cut criteria conflict, what is sacrificed first?",
        "default": "Murch's Rule of Six (murch_001; murch_0019): emotion 51 (0020) > story 23 (0021) > rhythm 10 (0022) > eye-trace 7 (0023) > planarity 5 (0024) > 3D space 4 (0025). Aim to satisfy all six (0031); else sacrifice upward from the bottom (0027) — higher criteria obscure failures of lower ones, never the reverse (0028). Weights hedged, intervals the point (0029); top three bind tightly (0030); 'bad' is film-relative (0011); the list serves occupying the audience's position (0032).",
        "check": "An imperfect cut names the bottom criteria sacrificed; never sacrifice emotion for eye-trace, planarity or 3D continuity.",
        "ids": ["sk_murch_c003_0019", "sk_murch_c003_0020", "sk_murch_c003_0021",
                "sk_murch_c003_0022", "sk_murch_c003_0023", "sk_murch_c003_0024",
                "sk_murch_c003_0025",
                "sk_murch_c003_0027", "sk_murch_c003_0028", "sk_murch_c003_0011",
                "sk_murch_c003_0029", "sk_murch_c003_0030", "sk_murch_c003_0031",
                "sk_murch_c003_0032", "scs_murch_c003_001"],
        "feeds": ["AUDIO_AND_EDIT", "FAILURE_PREVENTION"],
        "limits": [],
    },
    {
        "decision_id": "CA-D9",
        "question": "Screen direction and the line?",
        "default": "Frame edges are the audience's directional reference (gos_0005); keep setups within one 180-degree arc (0010; gos_001); movement and position persist across cuts (gote_0017, 0018; gos_0011); reciprocal coverage obeys the line (gote_0056). A far-side setup is good in itself — the reversal shows only at the cut (gos_0012, contradicting 0007/0010); crossing needs a declared creative reason (0013).",
        "check": "Screen direction and side-of-frame persist across consecutive shots, or something on screen shows the change (gos_0007), or the crossing is declared in DOCTRINE_DEVIATIONS.",
        "ids": ["sk_gos_c003_0005", "sk_gos_c003_0008", "sk_gos_c003_0011", "sk_gos_c003_0012",
                "sk_gote_c003_0017", "sk_gote_c003_0018", "sk_gote_c003_0056", "sk_gos_c003_0007",
                "sk_gos_c003_0010", "sk_gos_c003_0013", "sk_gote_c003_0008", "scs_gos_c003_001"],
        "feeds": ["GENERATION_PROMPTS", "AUDIO_AND_EDIT", "FAILURE_PREVENTION"],
        "limits": [],
    },
    {
        "decision_id": "CA-D10",
        "question": "How long may a shot hold?",
        "default": "Set length by silently describing the shot's contents; the description's time is the shot's (gote_0053). The fast-cutting norm — which the source calls alarming — is the ambient pace (0052).",
        "check": "No shot outlasts its describable content; the stated pace names the prevailing norm it assumes.",
        "ids": ["sk_gote_c003_0053", "sk_gote_c003_0052"],
        "feeds": ["AUDIO_AND_EDIT", "GENERATION_PROMPTS"],
        "limits": [],
    },
    {
        "decision_id": "CA-D11",
        "question": "Does the camera move, and why?",
        "default": "Every move is motivated and stillness is chosen (ms_0002); an object in transit licenses a move across a location (0011); do the most with the least (murch_0015); shared success criterion: the technique goes unnoticed (ms_0018; ms_003).",
        "check": "Each camera move names its motivation; unmotivated moves are replaced by stillness or a cut.",
        "ids": ["sk_ms_c003_0002", "sk_ms_c003_0011", "sk_murch_c003_0015", "sk_ms_c003_0018",
                "scs_ms_c003_003"],
        "feeds": ["GENERATION_PROMPTS", "AUDIO_AND_EDIT", "FAILURE_PREVENTION"],
        "limits": [],
    },
]

CA_CONFLICTS = [
    {"conflict_id": "CF-01", "decision_ref": "CA-D3", "kind": "contradicts",
     "between": ["sk_fre_c003_0002", "sk_fre_c003_0005"],
     "nature": "exact edge-proportioned framing against loose framing whose edges stop mattering",
     "resolution_rule": "Curve-proportioned cut in a sparse frame (0002); in a busy scene edges stop mattering (0005). Declare the case."},
    {"conflict_id": "CF-02", "decision_ref": "CA-D3", "kind": "contradicts",
     "between": ["sk_fre_c003_0005", "sk_fre_c003_0006"],
     "nature": "busy-scene edge indifference against fragile tight fit",
     "resolution_rule": "Tight fit (0006) is a sparse-frame device, unavailable in a busy scene (0005); one treatment per shot, named."},
    {"conflict_id": "CF-03", "decision_ref": "CA-D3", "kind": "contradicts",
     "between": ["sk_fre_c003_0006", "sk_fre_c003_0007"],
     "nature": "the source presents deliberate frame break (halving) as the opposite of frame fit",
     "resolution_rule": "Halving (0007) needs a symmetrical subject and a stated reason; else fit-with-gap (0006)."},
    {"conflict_id": "CF-04", "decision_ref": "CA-D3", "kind": "contradicts",
     "between": ["sk_fre_c003_0007", "sk_fre_c003_0030"],
     "nature": "halving pulls the eye apart; centred symmetry draws it inward",
     "resolution_rule": "Centred symmetry (0030) imposes order on a disordered subject; halving (0007) creates tension on an ordered one. State the intent."},
    {"conflict_id": "CF-05", "decision_ref": "CA-D2", "kind": "contradicts",
     "between": ["sk_fre_c003_0016", "sk_fre_c003_0028"],
     "nature": "the source rejects placement rules outright yet elsewhere endorses classical proportion as innately satisfying",
     "resolution_rule": "Balance is a disposition judged by eye with tone weighed (0028, 0029), never a coordinate rule (0016); no named ratio justifies a placement."},
    {"conflict_id": "CF-06", "decision_ref": "CA-D5", "kind": "contradicts",
     "between": ["sk_fre_c003_0028", "sk_fre_c003_0032"],
     "nature": "satisfying the eye against deliberately refusing it rest",
     "resolution_rule": "Balance is the default; restless is a declared, brief-driven exception (DOCTRINE_DEVIATIONS)."},
    {"conflict_id": "CF-07", "decision_ref": "CA-D5", "kind": "contradicts",
     "between": ["sk_fre_c003_0033", "sk_fre_c003_0034"],
     "nature": "the source's two adjacent cases take opposite positions on rectilinear treatment",
     "resolution_rule": "Diagonals divide against strict rectilinears (0033); echo the subject's rectilinearity only when it matches its spirit (0034)."},
    {"conflict_id": "CF-08", "decision_ref": "CA-D2", "kind": "trades_off_with",
     "between": ["sk_fre_c003_0018", "sk_fre_c003_0019"],
     "nature": "background as setting versus subject as sole statement",
     "resolution_rule": "Off-centre shows subject and setting (0018); centre when the scene points inward and the subject is the sole statement (0019)."},
    {"conflict_id": "CF-09", "decision_ref": "CA-D2", "kind": "trades_off_with",
     "between": ["sk_fre_c003_0018", "sk_fre_c003_0021"],
     "nature": "off-centre placement against background dominance at the extreme",
     "resolution_rule": "Extreme placement only with a visible reason (0021); otherwise stay inside the three zones."},
    {"conflict_id": "CF-10", "decision_ref": "CA-D9", "kind": "contradicts",
     "between": ["sk_gos_c003_0007", "sk_gos_c003_0012"],
     "nature": "jumping the line is the failure of the screen-direction rule — yet the far-side shot is good in itself, the mistake appearing only once the shots are edited together",
     "resolution_rule": "The far-side setup is not itself the error (0012): the mistake appears only at the cut (0007). Crossing needs a declared creative reason (0013)."},
    {"conflict_id": "CF-11", "decision_ref": "CA-D9", "kind": "contradicts",
     "between": ["sk_gos_c003_0010", "sk_gos_c003_0012"],
     "nature": "the 180-degree arc rule against the far-side setup whose error appears only at the edit",
     "resolution_rule": "As CF-10: the arc rule (0010) binds setups that will be cut together; the far-side error appears at the edit (0012); deliberate exceptions per 0013."},
    {"conflict_id": "CF-12", "decision_ref": "CA-D7", "kind": "contradicts",
     "between": ["sk_gote_c003_0035", "sk_gote_c003_0026"],
     "nature": "the wipe suspends the composition-difference requirement at the cut",
     "resolution_rule": "Composition must differ at every straight cut (0026); the wipe (0035) is the exception — the wiping element supplies the visual event."},
    {"conflict_id": "CF-13", "decision_ref": "CA-D7", "kind": "contradicts",
     "between": ["sk_gote_c003_0035", "sk_gote_c003_0012"],
     "nature": "the wipe also waives the camera-angle (thirty-degree) requirement; the partner claim is not compiled into this pack",
     "resolution_rule": "The thirty-degree rule (0012) is camera_and_spatial_grammar scope, named so the wipe's waiver is visible; at a straight cut it stands."},
    {"conflict_id": "CF-14", "decision_ref": "CA-D7", "kind": "contradicts",
     "between": ["sk_ms_c003_0017", "sk_ms_c003_0010"],
     "nature": "blocking with a static wide solves the attention problem without a camera move, accepting a cut as fallback",
     "resolution_rule": "One attention device per beat — cut, move, or blocking; the pack does not rank them."},
    {"conflict_id": "CF-15", "decision_ref": "CA-D1", "kind": "contradicts",
     "between": ["sk_murch_c003_0033", "sk_murch_c003_0018"],
     "nature": "the editor misdirects attention as a magician does, against the warning that complete control of attention is self-defeating",
     "resolution_rule": "0018 is the default; misdirection (0033) only in service of a declared reveal, never ambient control."},
    {"conflict_id": "CF-16", "decision_ref": "CA-D1", "kind": "cross_source_tension",
     "between": ["t_hop_sa_0009", "t_sam_c003_0018"],
     "tension_ref": "T4", "ledger_record": "xj_0022",
     "ledger_file": "canon/candidates/ontology-join/cross-source-candidates-v0.yaml — candidate ledger cross-reference — unadopted, informational only (status: proposed; no candidates-lane content is consumed)",
     "nature": "Hopkins defines unoccupied_space as space paid for and not used to sell — borders, margins, enlarged type, half-page copy (t_hop_sa_0009); Samara defines negative_space as white space seen as shapes of equal importance to the positive elements (t_sam_c003_0018)",
     "resolution_rule": "Each term binds in its origin frame — Hopkins: paid direct-response space; Samara: grid-organised design. Name the artifact's frame before applying either; neither is compiled as a default."},
    {"conflict_id": "CF-17", "decision_ref": "CA-D8", "kind": "contradicts",
     "between": ["sk_murch_c003_0025", "sk_murch_c003_0026"],
     "nature": "the source ranks three-dimensional continuity last, deliberately and against the film-school tradition it reports (spatial continuity first)",
     "resolution_rule": "3D space ranks last (0025); 0026 is the tradition the source argues against — named for closure, not doctrine."},
]

CA_WAIVERS = [
    {"ref": "sk_gote_c003_0017", "relation": "depends_on", "partner": "sk_gote_c003_0054",
     "reason": "definitional dependency: 0054 defines the action line; the same geometry is compiled in this decision via scs_gos_c003_001 and sk_gos_c003_0010."},
    {"ref": "sk_gote_c003_0056", "relation": "depends_on", "partner": "sk_gote_c003_0055",
     "reason": "consequence explainer: 0055 states the left-right reversal that crossing the line produces; the decision's check tests that reversal outcome directly. Named so the mechanism's location is visible."},
    {"ref": "sk_murch_c003_0011", "relation": "qualified_by", "partner": "sk_murch_c003_0012",
     "reason": "the qualification (removal constrained by the structure of what remains) governs physical footage removal in an edit room; the decision consumes 0011 only for what-counts-as-bad being film-relative."},
    {"ref": "sk_vig_c003_0009", "relation": "depends_on", "partner": "sk_vig_c003_0011",
     "reason": "philosophy dependency: 0011 is the source's timelessness commitment; the contrast rule stands without adopting the philosophy."},
]

PACKS = [
    {
        "pack_id": "product_appearance",
        "out": OUT_PA,
        "applicability": ["static_image", "video", "image_sequence"],
        "decisions": PA_DECISIONS,
        "conflicts": PA_CONFLICTS,
        "waivers": PA_WAIVERS,
        "pack_limits": [DEVANAGARI_LIMIT, LSM_LATER_CHAPTERS_CAVEAT,
                        PA_COVERAGE_DELTA_LIMIT, PA_CATEGORY_SURFACE_LIMIT],
    },
    {
        "pack_id": "composition_and_attention",
        "out": OUT_CA,
        "applicability": ["static_image", "video", "image_sequence"],
        "decisions": CA_DECISIONS,
        "conflicts": CA_CONFLICTS,
        "waivers": CA_WAIVERS,
        "pack_limits": [DEVANAGARI_LIMIT, CA_COVERAGE_DELTA_LIMIT],
    },
]


# ── corpus loading (fail-closed) ─────────────────────────────────────────────

def load_audit_gate():
    spec = importlib.util.spec_from_file_location("audit_gate_v02", AUDIT_GATE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_environment():
    """Everything the compiler reads, loaded once. Every load is fail-closed."""
    objs, src_of = assign_markers.load_corpus()

    systems, terms, owner, source_id_of = {}, {}, {}, {}
    for d in sorted(p.name for p in KNOWLEDGE.iterdir() if p.is_dir()):
        scs = yaml.safe_load((KNOWLEDGE / d / "source-concept-systems.yaml").read_text()) or {}
        ont = yaml.safe_load((KNOWLEDGE / d / "ontology-mappings.yaml").read_text()) or {}
        for s in scs.get("source_concept_systems") or []:
            systems[s["scs_id"]] = s
            owner[s["scs_id"]] = d
            source_id_of[s["scs_id"]] = scs.get("source_id")
        for t in ont.get("terms") or []:
            terms[t["term_id"]] = t
            owner[t["term_id"]] = d
    for sk, o in objs.items():
        owner[sk] = src_of[sk]
        source_id_of[sk] = o.get("source_id")

    audited, records = {}, {}
    for p in sorted(RECORDS.glob("*.audit.yaml")):
        r = yaml.safe_load(p.read_text()) or {}
        records[p.name] = r
        name = str(r.get("knowledge_dir", "")).rstrip("/").split("/")[-1]
        audited[name] = r.get("audit_status")

    candidate_ids = set()
    for p in CANDIDATES.rglob("source-knowledge.yaml"):
        for o in (yaml.safe_load(p.read_text()) or {}).get("source_knowledge") or []:
            candidate_ids.add(o.get("sk_id"))
    for p in CANDIDATES.rglob("source-concept-systems.yaml"):
        for s in (yaml.safe_load(p.read_text()) or {}).get("source_concept_systems") or []:
            candidate_ids.add(s.get("scs_id"))

    annex = yaml.safe_load(ANNEX.read_text())
    dating_by_id = {}
    for row in annex["technology_dating"]["rows"]:
        dating_by_id.setdefault(row["sk_id"], set()).add(row["class"])
    medium_untested = {row["sk_id"] for row in annex["medium_transfer_untested"]["rows"]}

    return {
        "objs": objs, "src_of": src_of, "systems": systems, "terms": terms,
        "owner": owner, "source_id_of": source_id_of,
        "audited": audited, "records": records, "candidate_ids": candidate_ids,
        "dating_by_id": dating_by_id, "medium_untested": medium_untested,
        "markers": assign_markers.compute_markers(objs),
        "audit_gate": load_audit_gate(),
    }


def corpus_digest() -> str:
    """Recompute the accepted-corpus digest and cross-check the index. Fail closed on drift."""
    acc = yaml.safe_load(INDEX.read_text())["fingerprints"]["accepted_canon"]
    for row in acc["files"]:
        actual = hashlib.sha256((REPO_ROOT / row["path"]).read_bytes()).hexdigest()
        if actual != row["sha256"]:
            raise SystemExit(f"corpus index stale: {row['path']} bytes differ from the recorded sha256")
    canonical = "".join(
        f"{r['path']}:{r['sha256']}\n" for r in sorted(acc["files"], key=lambda x: x["path"])
    )
    combined = hashlib.sha256(canonical.encode()).hexdigest()
    if combined != acc["combined_digest"]:
        raise SystemExit("corpus index inconsistent: recombined digest differs from combined_digest")
    return combined


# ── id resolution and closure (fail-closed) ──────────────────────────────────

def resolve(ref: str, env: dict) -> None:
    if ref in env["candidate_ids"]:
        raise SystemExit(f"{ref}: collides with canon/candidates/ (HOLD lane) — fail closed")
    if ref not in env["owner"]:
        raise SystemExit(f"{ref}: does not resolve in canon/knowledge/current/")
    src = env["owner"][ref]
    if env["audited"].get(src) != "complete":
        raise SystemExit(f"{ref}: Audit Gate status for {src} is not 'complete'")


def guard_partners(env: dict) -> dict:
    """Direction-normalized guard partner map over the accepted corpus.

    contradicts symmetric; qualifies reversed into qualified_by; trades_off_with symmetric;
    depends_on directed (outgoing only). Stored direction is extractor choice (GAP-11)."""
    part: dict = {}

    def add(a, rel, b):
        part.setdefault(a, {}).setdefault(rel, set()).add(b)

    for s, o in env["objs"].items():
        for r in o.get("intra_source_relations") or []:
            rel, t = r.get("relation"), r.get("target")
            if t not in env["objs"]:
                continue
            if rel == "contradicts":
                add(s, "contradicts", t)
                add(t, "contradicts", s)
            elif rel == "qualifies":
                add(t, "qualified_by", s)
            elif rel == "qualified_by":
                add(s, "qualified_by", t)
            elif rel == "trades_off_with":
                add(s, "trades_off_with", t)
                add(t, "trades_off_with", s)
            elif rel == "depends_on":
                add(s, "depends_on", t)
    return part


def verify_closure(pack: dict, env: dict) -> None:
    part = guard_partners(env)
    cited = {ref for d in pack["decisions"] for ref in d["ids"]}
    conflict_named = {ref for c in pack["conflicts"] for ref in c["between"]}
    waived = {(w["ref"], w["relation"], w["partner"]) for w in pack["waivers"]}
    for sk in sorted(cited):
        if sk not in env["objs"]:
            continue  # scs/t ids carry no guard relations
        for rel in ("contradicts", "qualified_by", "trades_off_with", "depends_on"):
            for partner in sorted(part.get(sk, {}).get(rel, ())):
                if partner in cited or partner in conflict_named:
                    continue
                if (sk, rel, partner) in waived:
                    continue
                raise SystemExit(
                    f"{pack['pack_id']}: closure hole — {sk} {rel} {partner} is neither cited, "
                    "named in a conflicts entry, nor waived (GAP-11)")


# ── decision-level confidence marker (aggregation rule; see the spec §4) ─────

def decision_marker(ids: list, env: dict) -> str:
    sk_ids = [i for i in ids if i in env["objs"]]
    if not sk_ids:
        raise SystemExit(f"decision cites no sk objects: {ids}")
    ms = [env["markers"][i] for i in sk_ids]

    base = GRADE_ORDER[min(GRADE_ORDER.index(m["base"]) for m in ms)]
    if len(sk_ids) == 1:
        base = GRADE_ORDER[max(0, GRADE_ORDER.index(base) - 1)]  # single-claim demotion

    suffixes = [s for s in assign_markers.SUFFIX_ORDER if any(s in m["suffixes"] for m in ms)]
    flags = {f for m in ms for f in m["flags"]}
    for i in sk_ids:
        src = env["owner"][i]
        record = next((r for r in env["records"].values()
                       if str(r.get("knowledge_dir", "")).rstrip("/").endswith(src)), {})
        applicable = (record.get("technology_contingency") or {}).get("applicable")
        if applicable and "durable_mechanism" not in env["dating_by_id"].get(i, set()):
            flags.add("DATED")
    if any(i in env["medium_untested"] for i in sk_ids):
        flags.add("MEDIUM-UNTESTED")

    sources = sorted({env["source_id_of"][i] for i in ids if env["source_id_of"].get(i)})
    n = independent_origin_count(sources, env)
    origin = "SINGLE-ORIGIN" if n == 1 else f"MULTI-ORIGIN({n})"

    parts = [base + "".join(suffixes)]
    parts += [f for f in FLAG_ORDER if f in flags]
    parts.append(origin)
    return "[" + "|".join(parts) + "]"


def independent_origin_count(source_ids: list, env: dict) -> int:
    """Exhaustive maximum mutually-independent subset (sets here are tiny, <= 5)."""
    n = len(source_ids)
    if n <= 1:
        return n
    ok = {}
    for i, a in enumerate(source_ids):
        for b in source_ids[i + 1:]:
            good, _ = env["audit_gate"].independent_origins_ok(a, b, env["records"])
            ok[(a, b)] = ok[(b, a)] = good
    best = 1
    for mask in range(1, 1 << n):
        members = [source_ids[i] for i in range(n) if mask >> i & 1]
        if all(ok[(x, y)] for i, x in enumerate(members) for y in members[i + 1:]):
            best = max(best, len(members))
    return best


# ── rendering ────────────────────────────────────────────────────────────────

def compiled_from(ids: list, env: dict) -> list:
    rows = []
    for ref in ids:
        resolve(ref, env)
        if ref in env["objs"]:
            kind, label = "source_knowledge", env["objs"][ref].get("concept_label")
        elif ref in env["systems"]:
            kind, label = "concept_system", env["systems"][ref].get("label")
        else:
            kind, label = "ontology_term", env["terms"][ref].get("term")
        m = env["markers"].get(ref)
        rows.append({
            "ref": ref,
            "kind": kind,
            "source_dir": env["owner"][ref],
            "concept_label": label,
            "marker": assign_markers.render_marker(m["base"], m["flags"], m["suffixes"]) if m else None,
        })
    return rows


def tension_members(conflict: dict, env: dict) -> list:
    """Render cross-source tension member terms by id from accepted ontology mappings."""
    rows = []
    for ref in conflict["between"]:
        resolve(ref, env)
        t = env["terms"][ref]
        rows.append({
            "ref": ref,
            "source_dir": env["owner"][ref],
            "term": t.get("term"),
            "definition_in_origin_frame": " ".join(str(t.get("definition_in_origin_frame") or "").split()),
        })
    return rows


def render_terse(pack: dict, decisions_out: list, digest: str) -> str:
    lines = [
        f"CANON DOCTRINE PACK {pack['pack_id']} v0 (accepted corpus {digest[:12]}). "
        f"{len(decisions_out)} decisions. Each DEFAULT is a decision already made: accept it, "
        "or override it in DOCTRINE_DEVIATIONS citing the brief clause that forces the "
        "override. Answer every CHECK in FAILURE_PREVENTION as pass or fix, by decision id. "
        "Id legend: ids drop the sk_/scs_ prefix and _c003 infix (fre_0020 = sk_fre_c003_0020; "
        "3-digit = scs_ system); bare NNNN continues the last-named source.",
        "",
    ]
    for d in decisions_out:
        lines.append(f"{d['decision_id']} {d['confidence_marker']}")
        lines.append(f"Q: {d['question']}")
        lines.append(f"DEFAULT: {d['default']}")
        lines.append(f"CHECK: {d['check']}")
        for lim in d["limits"]:
            lines.append(f"LIMIT: {lim}")
        lines.append("")
    lines.append("PRE-ARBITRATED CONFLICTS (the rule already decides; do not re-arbitrate):")

    def short(ref: str) -> str:
        return ref.replace("sk_", "").replace("scs_", "").replace("_c003", "")

    for c in pack["conflicts"]:
        a, b = c["between"]
        lines.append(f"{c['conflict_id']} {short(a)} vs {short(b)}: {c['resolution_rule']}")
    lines.append("")
    lines.append("PACK LIMITS:")
    for lim in pack["pack_limits"]:
        lines.append(f"- {lim}")
    return "\n".join(lines) + "\n"


def tokens(text: str) -> int:
    return (len(text) + 3) // 4


def build_pack(pack: dict, env: dict, digest: str) -> str:
    verify_closure(pack, env)

    decisions_out = []
    for d in pack["decisions"]:
        decisions_out.append({
            "decision_id": d["decision_id"],
            "question": d["question"],
            "default": d["default"],
            "check": d["check"],
            "check_id": f"{d['decision_id']}-check",
            "confidence_marker": decision_marker(d["ids"], env),
            "compiled_from": compiled_from(d["ids"], env),
            "feeds_sections": d["feeds"],
            "limits": d["limits"],
        })

    conflicts_out = []
    for c in pack["conflicts"]:
        row = {k: c[k] for k in ("conflict_id", "decision_ref", "kind", "between",
                                 "nature", "resolution_rule")}
        if c["kind"] == "cross_source_tension":
            row["tension_ref"] = c["tension_ref"]
            row["ledger_record"] = c["ledger_record"]
            row["ledger_file"] = c["ledger_file"]
            row["members"] = tension_members(c, env)
        else:
            for ref in c["between"]:
                resolve(ref, env)
        conflicts_out.append(row)

    terse = render_terse(pack, decisions_out, digest)
    terse_tokens = tokens(terse)
    if terse_tokens > TERSE_MAX_TOKENS:
        raise SystemExit(
            f"{pack['pack_id']}: terse rendering {terse_tokens} tokens exceeds the "
            f"{TERSE_MAX_TOKENS}-token budget — a pack that cannot fit is a compilation "
            "failure to report, never a budget to raise silently")

    cited_sk = sorted({r for d in pack["decisions"] for r in d["ids"] if r in env["objs"]})
    claim_bytes = sum(len(env["objs"][r].get("claim") or "") for r in cited_sk)

    doc = {
        "artifact": f"PACK-{pack['pack_id']}-v0",
        "status": STATUS_LINE,
        "stream": "canon",
        "task": "REP-05",
        "addresses_gaps": ["GAP-02", "GAP-04", "GAP-05", "GAP-09", "GAP-11", "GAP-14", "GAP-16"],
        "spec": "canon/compilation/COMPILED-DOCTRINE-SPEC-v0.md",
        "generated_by": "canon/compilation/compile_pilot_packs.py (deterministic; rerun to verify)",
        "pack_id": pack["pack_id"],
        "pack_version": "v0",
        "applicability": {"modalities": pack["applicability"]},
        "corpus_digest": digest,
        "corpus_digest_source": (
            "canon/knowledge/CANON-CORPUS-INDEX.yaml fingerprints.accepted_canon "
            "(recomputed from per-file sha256 entries and cross-checked against disk)"),
        "budget": {
            "terse_max_tokens": TERSE_MAX_TOKENS,
            "token_rule": "tokens = ceil(chars / 4); the enforced quantity is bytes of the terse rendering",
        },
        "counts": {
            "decisions": len(decisions_out),
            "cited_sk_objects": len(cited_sk),
            "cited_claim_bytes": claim_bytes,
            "conflicts": len(conflicts_out),
            "closure_waivers": len(pack["waivers"]),
            "terse_chars": len(terse),
            "terse_tokens": terse_tokens,
        },
        "decisions": decisions_out,
        "conflicts": conflicts_out,
        "closure_waivers": pack["waivers"],
        "pack_limits": pack["pack_limits"],
        "consumption": {
            "contract": "canon/compilation/INJECTION-CONTRACT-v0.md",
            "trigger_table": "canon/packs/pack-triggers-v0.yaml",
            "target_schema": "FINAL_PRODUCTION_PACKAGE v2 (12 EVAL-037 sections + DOCTRINE_DEVIATIONS)",
        },
        "terse_injection_text": terse,
        "what_a_pass_does_not_establish": (
            "Relevance to any brief, doctrine quality, medium fit, outcome improvement, or "
            "adoption. A validator PASS is a structural fact about committed bytes; adoption "
            "is a Controller decision."),
    }

    buf = io.StringIO()
    for line in (
        f"{pack['out'].name} — GENERATED by canon/compilation/compile_pilot_packs.py; do not hand-edit.",
        f"STATUS: {STATUS_LINE}",
        "Compiled doctrine pack: questions-with-defaults over accepted Canon only.",
        "Validate: python3 canon/validation/validate_compiled_pack.py",
    ):
        buf.write(f"# {line}\n")
    buf.write(yaml.safe_dump(doc, sort_keys=True, allow_unicode=True, width=100))
    return buf.getvalue()


def generate() -> dict:
    env = load_environment()
    digest = corpus_digest()
    return {pack["out"]: build_pack(pack, env, digest) for pack in PACKS}


def main(argv) -> int:
    outputs = generate()
    if "--check" in argv:
        second = generate()
        drift = []
        for path, text in outputs.items():
            if second[path] != text:
                drift.append(f"{path}: two in-process compiles differ (non-determinism)")
            if not path.exists():
                drift.append(f"{path}: missing on disk")
            elif path.read_text() != text:
                drift.append(f"{path}: committed bytes differ from recompilation")
        if drift:
            print("DRIFT:", *drift, sep="\n  ")
            return 1
        print("check OK: both packs recompile byte-identically")
        return 0
    for path, text in outputs.items():
        path.write_text(text)
        doc = yaml.safe_load(text)
        print(f"wrote {path.relative_to(REPO_ROOT)} "
              f"({doc['counts']['decisions']} decisions, "
              f"{doc['counts']['cited_sk_objects']} sk objects, "
              f"{doc['counts']['terse_tokens']} terse tokens, {len(text)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
