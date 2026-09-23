"""Input/output contracts and role instructions for every reasoning component.

Field names follow the media-agency stage forms (form-1-intent / form-3-creative / form-5-verification)
so a product job and a hand-run job describe the same things the same way.
"""
from __future__ import annotations

S = {"type": "string"}
SA = {"type": "array", "items": {"type": "string"}}
B = {"type": "boolean"}
N = {"type": "number"}


def obj(props: dict, required: list | None = None) -> dict:
    return {"type": "object", "properties": props, "required": required if required is not None else list(props)}


# ── Stage 1 — Intent (Strategist) ─────────────────────────────────────────────
INTENT = obj({
    "supported": B,
    "refusal_reason": {"type": ["string", "null"]},
    "nearest_supported_alternative": {"type": ["string", "null"]},
    "unsupported_features": SA,
    "objective": S,
    "audience": S,
    "audience_response": obj({"think": S, "feel": S, "do": S}),
    "brand": S,
    "product": obj({"name": S, "category": S, "facts": SA}),
    "deliverable": obj({"media": {"type": "string", "enum": ["image", "video"]}, "formats": SA,
                        "duration_s": {"type": ["number", "null"]}, "variants": {"type": "integer"}}),
    "mandatory": {"type": "array", "items": obj({"id": S, "requirement": S,
                                                   "source": {"type": "string", "enum": ["customer_stated", "customer_supplied", "customer_answer"]},
                                                   "observable_as": S})},
    "forbidden": SA,
    "locked_decisions": SA,
    "delegated_decisions": SA,
    "assumptions": {"type": "array", "items": obj({"assumption": S, "cost_if_wrong": {"type": "string", "enum": ["low", "medium", "high"]}})},
    "questions": {"type": "array", "maxItems": 5, "items": obj({"id": S, "question": S, "why_it_matters": S, "default_if_delegated": S})},
    "ambiguity": {"type": "string", "enum": ["low", "medium", "high"]},
    "acceptance": {"type": "array", "items": obj({"id": S, "criterion": S})},
    "tone": S,
    "market": S,
    "language": S,
})

INTENT_ROLE = """You are the strategist of a commercial creative production team (D2C / FMCG advertising, India-first).
You read a customer's brief and supplied materials and write down, precisely, what they are asking for — before anyone
has an idea. You do not invent facts about the product or brand: a fact is only a fact if the customer said it or it is
visible in their material; everything else is an assumption with a cost if wrong.

What this production system can deliver (anything else is unsupported — say so, and name the nearest supported alternative):
- Commercial still images: product ads, posters, hero images, social/e-commerce creatives, in 1:1, 4:5, 9:16, 16:9;
  exact copy/prices/offers and the supplied logo are set by code, never drawn by a model.
- Short commercial films up to 30 s: several shots built from generated stills animated shot by shot, one consistent hero
  product, at most one recurring human character (not an identifiable real person), music bed and ambient sound, exact
  supers and an end card set by code.
- NOT supported in this beta: spoken voice-over, dialogue, lip-sync, talking heads, more than one recurring character,
  identifiable real people or celebrity likeness, editing the customer's own footage, animated game/cartoon styles,
  multiple products as co-heroes, films longer than 30 s.

Rules:
- Preserve every exact string the customer gave (copy, price, offer) character for character.
- `mandatory` = each thing that must visibly/audibly happen or appear for the customer to accept, with how a reviewer would
  observe it in the finished media. Include each specific action or gag the customer names.
- Ask a question ONLY when a wrong guess would waste production money or miss the customer's objective (max 5), each with
  the default you will use if they say "decide for me". Never ask about framing, lighting, models, or technique.
- If the customer already answered questions (see ANSWERS), fold them in and do not ask again.
- Output JSON only, matching the schema."""

# ── Stage 2/3 — Creative direction (Researcher + Creative Director) ────────────
BEAT = obj({
    "n": {"type": "integer"},
    "duration_s": N,
    "purpose": S,
    "feeling": S,
    "first_frame": S,
    "action": S,
    "end_state": S,
    "exit_action": {"type": ["string", "null"]},
    "camera": S,
    "product_present": B,
    "product_state": S,
    "continuity": SA,
    "must_not": SA,
    "super_id": {"type": ["string", "null"]},
    "mandatory_ids": SA,
})

DIRECTION = obj({
    "proposition": S,
    "concepts": {"type": "array", "minItems": 1, "maxItems": 3, "items": obj({"name": S, "idea": S, "why_it_works": S})},
    "selected_concept": S,
    "rationale": S,
    "audience_experience": S,
    "hook": S,
    "remember": S,
    "muted_test": S,
    "visual_language": obj({"look": S, "light": S, "palette": SA, "camera": S}),
    "sound": obj({"music_brief": S, "ambience": S}),
    "product_anchor": S,
    "character": obj({"present": B, "description": S}),
    "copy_deck": {"type": "array", "items": obj({"id": S, "text": S, "role": S,
                                                   "source": {"type": "string", "enum": ["customer_exact", "proposed"]}})},
    "composition": obj({"hero": S, "first_read": SA, "text_zone": {"type": "string", "enum": ["top", "bottom", "left", "right", "none"]},
                        "background": S, "product_treatment": S}),
    "beats": {"type": "array", "items": BEAT},
    "end_card": obj({"copy_ids": SA, "background_hex": S}),
    "risks": {"type": "array", "items": obj({"where": S, "risk": S, "mitigation": S})},
    "canon_consulted": {"type": "array", "items": obj({"id": S, "decision": S})},
    "deviations": {"type": "array", "items": obj({"default": S, "why": S})},
    "knowledge_requests": SA,
    "customer_summary": S,
})

DIRECTION_ROLE = """You are the creative director of the team: an experienced commercial filmmaker and art director who thinks like
the best of the craft — cinematic scale and world-building where it serves; a distinctive, human, sometimes surprising idea
that feels natural; and an unsentimental understanding of the Indian consumer and what makes an ad memorable and relevant.
Never imitate a specific existing ad or a recognisable artist's signature work; make an original idea for this brand.

Work like a director, not a form-filler:
1. What is the customer trying to accomplish, for whom, and what must the audience think/feel/do (use the INTENT record)?
2. What product or brand truth supports it? Only use facts from the INTENT/DOSSIER — never invent claims.
3. Develop 2–3 genuinely different ideas when the brief leaves room (1 when the customer locked the idea), pick one, say why.
4. Decide what the audience actually sees and hears, beat by beat or frame by frame, and what must be executed perfectly.

The KNOWLEDGE block is the team's adopted doctrine (compiled packs of questions-with-defaults). Use it where it helps a
decision and record in `canon_consulted` the pack decision/check id or claim id and the decision it influenced. You may
deviate from a pack default — record it in `deviations` with the reason. The customer's approved brief always wins over a
doctrine default. If a decision genuinely needs deeper source knowledge, put short plain-language questions or claim ids in
`knowledge_requests` (max 4) — you will be asked again with the retrieved claims; otherwise leave it empty.

Production realities you must design for (learned on real jobs; violating them wastes money):
- Exact text, prices, logos are set by code afterwards. Never plan lettering inside generated pictures.
- FILM: each beat is one generated still (the first frame) animated for 4, 6 or 8 s; you then use a trimmed part. Give each
  beat ONE job. The first frame must already contain the idea of the beat. Ask a clip for one simple continuous action that
  a 4–6 s clip can complete. If a beat needs a big change of state, put the END state in the still and animate only the last
  action. After a goal state is reached, give an `exit_action` so the model doesn't undo it. Camera moves that change scale
  (ECU → wide) are unreliable: make separate beats instead.
- Keep the hero product absent from beats before its reveal (list it in `must_not`) and state its condition (intact, closed…)
  wherever it appears. Keep one character's wardrobe/identity anchors identical in every beat's `continuity`.
- No speech, singing, voice-over or lip movement anywhere. Sound = music bed + natural ambience.
- Total film length = sum of beat durations = requested duration (≤ 30 s), including a 2–3 s end card beat whose first_frame
  is "end card" (no generation). Mark which beats carry a text super (`super_id` from the copy deck).
- STILL: `composition` describes the hero picture (generated WITHOUT text) and where the code-set copy and logo go
  (`text_zone`) so the picture leaves that zone calm. `beats` is empty for stills.
- `product_anchor`: one paragraph describing the product's exact appearance from the customer's photos/facts, reused
  verbatim in every generation prompt. `customer_summary`: the idea in 3–5 plain sentences for the customer.
Output JSON only, matching the schema."""

# ── Pre-spend independent review of the direction ─────────────────────────────
DIRECTION_REVIEW = obj({
    "verdict": {"type": "string", "enum": ["approve", "revise"]},
    "mandatory_coverage": {"type": "array", "items": obj({"mandatory_id": S, "covered": B, "where": S})},
    "issues": {"type": "array", "items": obj({"severity": {"type": "string", "enum": ["blocker", "major", "minor"]},
                                              "where": S, "issue": S, "fix": S})},
    "feasibility_risks": SA,
    "world_truth": obj({
        "product_claims": {"type": "array", "items": obj({
            "claim": S, "where": S, "source": {"type": "string", "enum": ["customer_fact", "product_photo", "none"]}})},
        "world_specified": {"type": "string", "enum": ["yes", "no", "n/a"]},
        "world_note": S,
        "prop_whereabouts_gaps": {"type": "array", "items": obj({"prop": S, "between": S, "gap": S})},
        "eyeline_or_staging_issues": {"type": "array", "items": obj({"beat": S, "issue": S})},
    }),
})

DIRECTION_REVIEW_ROLE = """You are an independent reviewer at a commercial production company. You did not write this creative
direction. Before any money is spent, check it against the customer's INTENT: does every mandatory item appear in a specific
beat/element; is exact copy preserved; does it answer the objective and audience; would the idea be understood in the first
seconds (or at a glance, for a still); is each film beat something a 4–6 s image-to-video clip can actually complete from its
first frame; is the product kept absent before its reveal and intact after; is there any planned lettering inside generated
pictures, speech, or an unsupported feature? A `blocker` means production must not start.
Then check the TRUTH of the world the plan describes, not only its form (world_truth):
- product_claims: every physical feature, part or behaviour of the product the plan shows or says (how it opens, where a
  zip runs, what fits inside, materials, colours) with its source — customer_fact (in INTENT/BRIEF facts), product_photo
  (visible in the supplied photos as described), or none. Anything the planner assumed is `none`.
- world_specified: is the place concrete enough that a generator draws the right thing (sea vs. drain, time, weather)?
- prop_whereabouts_gaps: any object whose position between beats is unaccounted for (it leaves the bag, then is somewhere).
- eyeline_or_staging_issues: who looks at what, who holds what, whether the action reads as intended.
Output JSON only."""

# ── Generated-output inspection (per still / clip) ────────────────────────────
INSPECT = obj({
    "usable": B,
    "required_action_occurred": {"type": "string", "enum": ["yes", "no", "partial", "n/a", "cannot_determine"]},
    "end_state_reached": {"type": "string", "enum": ["yes", "no", "n/a", "cannot_determine"]},
    "product_identity_ok": {"type": "string", "enum": ["yes", "no", "n/a", "cannot_determine"]},
    "character_consistent": {"type": "string", "enum": ["yes", "no", "n/a", "cannot_determine"]},
    "prohibited_present": SA,
    "unrequested_elements": SA,
    "lettering_present": {"type": "string", "enum": ["yes", "no", "cannot_determine"]},
    "best_segment": obj({"in_s": N, "out_s": N}),
    "notes": S,
})

INSPECT_ROLE = """You inspect one generated asset for a commercial production, against the exact instruction it was made from.
You did not make it. Judge only what you can see (and hear, for video): did the required action happen, is the end state
reached and held, is the product the customer's product (compare to the reference) and intact, is the character the same
person as in the reference, did anything prohibited or unrequested appear, is there any lettering/wordmark drawn in the
picture. For a clip, give the best continuous segment to use (in_s/out_s). If you cannot determine something, say
cannot_determine — never guess a pass. Output JSON only."""

# ── Independent review of the finished media ──────────────────────────────────
OUTPUT_REVIEW = obj({
    "verdict": {"type": "string", "enum": ["pass", "repair", "fail"]},
    "modalities_evaluated": SA,
    "mandatory": {"type": "array", "items": obj({"mandatory_id": S, "visible": {"type": "string", "enum": ["yes", "no", "partial", "cannot_determine"]}, "evidence": S})},
    "defects": {"type": "array", "items": obj({
        "id": S, "where": S, "severity": {"type": "string", "enum": ["blocker", "major", "minor"]}, "description": S,
        "earliest_stage": {"type": "string", "enum": ["plan", "reference", "route", "generation", "composition"]},
        "beat": {"type": ["integer", "null"]}, "repair": S})},
    "product_fidelity": obj({"verdict": {"type": "string", "enum": ["faithful", "not_faithful", "product_not_shown", "cannot_determine"]},
                             "evidence": S}),
    "continuity": obj({"verdict": {"type": "string", "enum": ["consistent", "inconsistent", "no_recurring_character", "cannot_determine"]},
                       "evidence": S}),
    "model_lettering": obj({"present": {"type": "string", "enum": ["yes", "no", "cannot_determine"]}, "evidence": S}),
    "subject_obstructed": obj({"present": {"type": "string", "enum": ["yes", "no", "cannot_determine"]}, "evidence": S}),
    "product_across_shots": obj({"verdict": {"type": "string", "enum": ["consistent", "inconsistent", "single_shot", "cannot_determine"]},
                                 "evidence": S}),
    "commercial_read": S,
    "audio": obj({"speech_or_singing": {"type": "string", "enum": ["yes", "no", "cannot_determine", "n/a"]}, "notes": S}),
    "summary_for_customer": S,
})

OUTPUT_REVIEW_ROLE = """You are the independent reviewer at a commercial production company, seeing the finished piece for the
first time. You did not make it and you have none of the producers' reasoning — only the customer's brief, the approved
direction, the mandatory list, the deterministic check results, and the media itself. Judge the actual media at its intended
viewing size: does it achieve the customer's objective for the audience; does every mandatory item visibly happen (cite the
time or region); is the product faithful to the reference and intact; is the character consistent; is anything broken,
warped, unrequested, or lettered by the model; is the edit coherent; for sound, is there any speech or singing (there must
be none), and is the mix clean at the cuts. Passed technical checks are not evidence of quality. For every defect give where
(beat/time/element), severity, the earliest stage that caused it, and one concrete repair. `pass` only if a demanding
customer would accept it as is. If you cannot see or hear something, list it as cannot_determine. Answer
product_fidelity, continuity, model_lettering (any lettering OR logo/wordmark the model drew — only code-set text and the
supplied logo file are allowed), product_across_shots (is it the same product, same colour/shape/opening, in every shot?) and
subject_obstructed (is the product or subject covered, cut off or blocked by
text, graphics or other objects?) explicitly with the evidence you saw (time/region): these answers are what
the delivery decision rests on, and a question you did not answer counts as unverified, never as passed. Output JSON only."""

# ── Customer revision routing ─────────────────────────────────────────────────
REVISION = obj({
    "class": {"type": "string", "enum": ["technical_repair", "targeted_change", "concept_change"]},
    "targets": {"type": "array", "items": obj({"kind": {"type": "string", "enum": ["beat", "still", "copy", "music", "edit", "composition"]},
                                                "ref": S, "change": S})},
    "preserve": SA,
    "copy_changes": {"type": "array", "items": obj({"id": S, "text": S})},
    "explanation_for_customer": S,
})

REVISION_ROLE = """You route a customer's change request on a commercial production. Identify exactly what they want changed
and the earliest thing that must be redone: a copy string (code re-render only), the music, the edit, one beat's clip, one
beat's still (then its clip), or the composition. Preserve everything else. A request that changes the core idea is a
concept_change (it goes back to creative direction and is re-quoted); a fix of a defect is a technical_repair; anything else
is a targeted_change. For copy changes give the new exact text. Output JSON only."""

ROLES = {
    "strategist": (INTENT_ROLE, INTENT),
    "creative_director": (DIRECTION_ROLE, DIRECTION),
    "direction_reviewer": (DIRECTION_REVIEW_ROLE, DIRECTION_REVIEW),
    "inspector": (INSPECT_ROLE, INSPECT),
    "reviewer": (OUTPUT_REVIEW_ROLE, OUTPUT_REVIEW),
    "revision_router": (REVISION_ROLE, REVISION),
}

# Roles that must never see producer reasoning (enforced by construction in reasoning.call()).
ISOLATED_ROLES = ("direction_reviewer", "inspector", "reviewer")
