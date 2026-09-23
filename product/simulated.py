"""Deterministic, no-network stand-ins for the reasoning roles — for dry end-to-end runs and tests only.

They follow the same contracts as the live models, so the whole product path (states, ledger, graph,
verification, gateway, revision) is exercised at USD 0. They are labelled `simulated` everywhere, and
the verification layer never counts a simulated review as independent verification.
"""
from __future__ import annotations

import json
import re

UNSUPPORTED = [
    (r"\bvoice[- ]?over\b|\bvo\b|narrat", "spoken voice-over"),
    (r"dialog|dialogue|\bspeaks?\b|\btalking head", "dialogue or talking heads"),
    (r"lip[- ]?sync", "lip-sync"),
    (r"celebrity|shah ?rukh|virat|deepika", "identifiable real person / celebrity likeness"),
    (r"our (own )?footage|edit (our|my) video", "editing customer footage"),
    (r"\b(4[5-9]|[5-9]\d|1\d\d)[- ]?(s|sec|second)", "films longer than 30 seconds"),
]


def _ctx(context, key):
    v = context.get(key)
    if isinstance(v, str):
        try:
            return json.loads(v)
        except ValueError:
            return v
    return v


class SimulatedReasoning:
    def respond(self, role: str, context: dict, media) -> dict:
        return getattr(self, role)(context, media)

    # Stage 1
    def strategist(self, context, media):
        brief = _ctx(context, "BRIEF") or {}
        answers = _ctx(context, "ANSWERS")
        answers = answers if isinstance(answers, dict) else {}
        text = (brief.get("text") or "")
        low = text.lower()
        media_kind = brief.get("media", "image")
        unsupported = [label for pat, label in UNSUPPORTED if re.search(pat, low)]
        strings = [s for s in brief.get("exact_strings", []) if s]
        product = brief.get("product") or {}
        mandatory = [{"id": f"M{i+1}", "requirement": f'the exact text "{s}" appears, character for character',
                      "source": "customer_stated", "observable_as": "rendered text matches the string"} for i, s in enumerate(strings)]
        mandatory.append({"id": f"M{len(mandatory)+1}", "requirement": "the customer's product is the hero and matches the supplied photos",
                          "source": "customer_supplied", "observable_as": "product shape, colour and label match the reference"})
        for m in re.findall(r"must (?:show|have|include) ([^.;]+)", low):
            mandatory.append({"id": f"M{len(mandatory)+1}", "requirement": m.strip(), "source": "customer_stated",
                              "observable_as": f"'{m.strip()}' is visible in the finished media"})
        questions = []
        if len(text.split()) < 12 and not answers:
            questions.append({"id": "Q1", "question": "Who is this for, and what should they do after seeing it?",
                              "why_it_matters": "the idea and the call to action depend on it",
                              "default_if_delegated": "urban 22–40 online shoppers; visit the brand's store"})
        return {
            "supported": not unsupported,
            "refusal_reason": ("This beta cannot produce: " + ", ".join(unsupported)) if unsupported else None,
            "nearest_supported_alternative": ("A film with music, ambience and on-screen text supers instead of speech"
                                              if unsupported else None),
            "unsupported_features": unsupported,
            "objective": f"Make people want {product.get('name') or 'the product'}",
            "audience": (answers.get("Q1") if isinstance(answers, dict) and answers.get("Q1") else "urban 22–40 online shoppers"),
            "audience_response": {"think": "this is made for me", "feel": "curious and reassured", "do": "look it up"},
            "brand": product.get("brand") or "the brand",
            "product": {"name": product.get("name") or "the product", "category": product.get("category") or "product",
                        "facts": [f for f in [product.get("description")] if f]},
            "deliverable": {"media": media_kind, "formats": brief.get("formats") or (["9:16"] if media_kind == "video" else ["1:1"]),
                            "duration_s": brief.get("duration_s") if media_kind == "video" else None, "variants": 1},
            "mandatory": mandatory,
            "forbidden": ["model-drawn lettering or logos", "speech or singing"],
            "locked_decisions": [f'copy: "{s}"' for s in strings],
            "delegated_decisions": ["concept", "framing", "light", "music"],
            "assumptions": [{"assumption": "the product photos show the current packaging", "cost_if_wrong": "high"}],
            "questions": questions,
            "ambiguity": "medium" if questions else "low",
            "acceptance": [{"id": "A1", "criterion": "every mandatory item is visible and the product is faithful"}],
            "tone": "warm, confident",
            "market": brief.get("market") or "IN",
            "language": brief.get("language") or "en",
        }

    # Stage 2/3
    def creative_director(self, context, media):
        intent = _ctx(context, "INTENT") or {}
        brief = _ctx(context, "BRIEF") or {}
        media_kind = (intent.get("deliverable") or {}).get("media", "image")
        strings = brief.get("exact_strings", [])
        copy = [{"id": f"c{i+1}", "text": s, "role": "headline" if i == 0 else "line", "source": "customer_exact"}
                for i, s in enumerate(strings)]
        name = (intent.get("product") or {}).get("name") or "the product"
        beats = []
        if media_kind == "video":
            total = float((intent.get("deliverable") or {}).get("duration_s") or 15)
            card = 3.0
            n = max(2, min(6, round((total - card) / 4.5)))
            each = round((total - card) / n, 2)
            story = [("the problem, felt", "a cluttered, ordinary moment before the product", False),
                     ("the reveal", f"{name} enters the frame, clean and intact", True),
                     ("the product at work", f"{name} in use, doing its one job", True),
                     ("the payoff", "the person relaxes, the moment resolved", True),
                     ("the product, remembered", f"{name} alone, hero light", True),
                     ("the smile", "a small human reaction", True)]
            for i in range(n):
                purpose, frame, present = story[i % len(story)]
                beats.append({"n": i + 1, "duration_s": each, "purpose": purpose, "feeling": "warm", "first_frame": frame,
                              "action": "a slow push-in; one small natural movement", "end_state": "the moment holds",
                              "exit_action": None, "camera": "35mm, eye level", "product_present": present,
                              "product_state": "intact, clean" if present else "absent",
                              "continuity": ["same person, same clothes in every beat"],
                              "must_not": [] if present else [name], "super_id": "c1" if (i == 1 and copy) else None,
                              "mandatory_ids": []})
            beats.append({"n": n + 1, "duration_s": card, "purpose": "sign-off", "feeling": "resolved", "first_frame": "end card",
                          "action": "none", "end_state": "logo and line", "exit_action": None, "camera": "n/a",
                          "product_present": False, "product_state": "n/a", "continuity": [], "must_not": [],
                          "super_id": None, "mandatory_ids": [m["id"] for m in intent.get("mandatory", [])[:len(copy)]]})
        return {
            "proposition": f"{name}: the small thing that makes the day easier",
            "concepts": [{"name": "The quiet fix", "idea": f"an ordinary frustration, resolved by {name}", "why_it_works": "product as hero"},
                         {"name": "Hero still life", "idea": f"{name} as the only object that matters", "why_it_works": "clarity"}],
            "selected_concept": "The quiet fix",
            "rationale": "simplest route from the audience's moment to the product truth",
            "audience_experience": "recognition, then relief",
            "hook": "a moment the viewer knows", "remember": name, "muted_test": "yes",
            "visual_language": {"look": "natural, premium", "light": "one soft window light", "palette": ["#1f2a44", "#f4efe6"],
                                "camera": "35mm, shallow depth"},
            "sound": {"music_brief": "warm, understated, gentle build", "ambience": "room tone"},
            "product_anchor": f"{name} exactly as in the customer's reference photos, clean and intact",
            "character": {"present": media_kind == "video", "description": "a woman in her late twenties, plain navy kurta"},
            "copy_deck": copy,
            "composition": {"hero": f"{name} centre-left, three-quarter view", "first_read": [name, "headline", "logo"],
                            "text_zone": "top" if media_kind == "image" else "none", "background": "calm warm wall",
                            "product_treatment": "soft key light, gentle shadow"},
            "beats": beats,
            "end_card": {"copy_ids": [c["id"] for c in copy], "background_hex": "#1f2a44"},
            "risks": [{"where": "beat 3", "risk": "product identity drift", "mitigation": "reference photo in every still"}] if beats else [],
            "canon_consulted": [{"id": "CC-D4", "decision": "product as hero in every product beat"}],
            "deviations": [],
            "knowledge_requests": [],
            "customer_summary": f"We open on a familiar moment and let {name} quietly resolve it, ending on your line and logo.",
        }

    def direction_reviewer(self, context, media):
        intent = _ctx(context, "INTENT") or {}
        return {"verdict": "approve",
                "mandatory_coverage": [{"mandatory_id": m["id"], "covered": True, "where": "copy deck / beats"} for m in intent.get("mandatory", [])],
                "issues": [], "feasibility_risks": []}

    def inspector(self, context, media):
        return {"usable": True, "required_action_occurred": "cannot_determine", "end_state_reached": "cannot_determine",
                "product_identity_ok": "cannot_determine", "character_consistent": "cannot_determine",
                "prohibited_present": [], "unrequested_elements": [], "lettering_present": "cannot_determine",
                "best_segment": {"in_s": 0.0, "out_s": 0.0}, "notes": "simulated inspection: nothing was looked at"}

    def reviewer(self, context, media):
        intent = _ctx(context, "INTENT") or {}
        return {"verdict": "pass", "modalities_evaluated": ["simulated"],
                "mandatory": [{"mandatory_id": m["id"], "visible": "cannot_determine", "evidence": "simulated"} for m in intent.get("mandatory", [])],
                "defects": [], "product_fidelity": {"verdict": "cannot_determine", "evidence": "simulated"},
                "continuity": {"verdict": "cannot_determine", "evidence": "simulated"},
                "model_lettering": {"present": "cannot_determine", "evidence": "simulated"},
                "subject_obstructed": {"present": "cannot_determine", "evidence": "simulated"},
                "commercial_read": "not evaluated (simulated)",
                "audio": {"speech_or_singing": "cannot_determine", "notes": "simulated"},
                "summary_for_customer": "Simulated review — no one has looked at this media."}

    def revision_router(self, context, media):
        fb = _ctx(context, "FEEDBACK") or {}
        text = (fb.get("text") or "").lower() if isinstance(fb, dict) else str(fb).lower()
        target = fb.get("target") if isinstance(fb, dict) else None
        m = re.search(r'(?:copy|text|headline|line)\s*(?:to|should read|:)\s*"([^"]+)"', fb.get("text", "") if isinstance(fb, dict) else "")
        if m:
            cid = (target or "c1").split(":")[-1]
            return {"class": "targeted_change", "targets": [{"kind": "copy", "ref": cid, "change": "new text"}], "preserve": ["all pictures"],
                    "copy_changes": [{"id": cid, "text": m.group(1)}], "explanation_for_customer": "We'll reset that line exactly as written."}
        if "whole idea" in text or "different concept" in text or "start over" in text:
            return {"class": "concept_change", "targets": [], "preserve": [], "copy_changes": [],
                    "explanation_for_customer": "This changes the idea, so we'll come back with a new direction and quote."}
        if target and target.startswith("beat:"):
            return {"class": "targeted_change", "targets": [{"kind": "beat", "ref": target.split(":")[1], "change": fb.get("text", "")}],
                    "preserve": ["every other beat", "music", "copy"], "copy_changes": [],
                    "explanation_for_customer": f"We'll remake only beat {target.split(':')[1]}."}
        return {"class": "targeted_change", "targets": [{"kind": "still", "ref": "hero", "change": fb.get("text", "") if isinstance(fb, dict) else text}],
                "preserve": ["copy", "logo"], "copy_changes": [], "explanation_for_customer": "We'll remake the picture with that change."}
