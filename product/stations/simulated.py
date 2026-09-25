"""Deterministic, no-network stand-ins for the seven AI workers — for dry runs and tests only (USD 0).

They follow the same forms as the live models, so every station, send-back and gate is exercised. Everything they write
is labelled simulated, and the door guard never counts a simulated judge's "yes" as verification.

Simulated vision: a test photo may carry a PNG text chunk `mi-sim-shows` saying what the picture shows (tests use it to
stand in for what a vision model would see, e.g. "people for scale" behind a caption that says "product"). Without it,
the simulation only knows the customer's caption.
Tests change a worker's behaviour by replacing a method on this object (e.g. `sim.head_cook__ingredient_check`).
"""
from __future__ import annotations

import re
import struct
import zlib

from product import library


# ── simulated photos ────────────────────────────────────────────────────────────────────────────────────────────
def with_shows(png: bytes, shows: str) -> bytes:
    """Insert a tEXt chunk after IHDR: what a vision model would see in this picture (test fixtures only)."""
    data = b"mi-sim-shows\x00" + shows.encode("latin-1", "replace")
    chunk = struct.pack(">I", len(data)) + b"tEXt" + data + struct.pack(">I", zlib.crc32(b"tEXt" + data) & 0xffffffff)
    return png[:33] + chunk + png[33:]


def shows_of(blob: bytes) -> str | None:
    i = blob.find(b"tEXtmi-sim-shows\x00")
    if i < 0:
        return None
    n = struct.unpack(">I", blob[i - 4:i])[0]
    return blob[i + 4 + len("mi-sim-shows\x00"):i + 4 + n].decode("latin-1")


ROLE_WORDS = [("logo", r"\blogo|wordmark"), ("lifestyle", r"\bpeople|person|model wearing|lifestyle|for scale|traveller|man |woman "),
              ("infographic", r"infographic|label(s|led)|annotat|callout|text labels|diagram"),
              ("product_detail", r"\bopen\b|inside|interior|detail|close[- ]?up|pocket|compartment|lining"),
              ("product_view", r"front|back|side|closed|product|bag|bottle|tin|pack")]


def role_of(text: str | None) -> str:
    for role, pat in ROLE_WORDS:
        if text and re.search(pat, text, re.I):
            return role
    return "other"


PART_WORDS = r"(?:pocket|compartment|flap|lining|lid|bucket|zip(?:per)?s?|sleeve|pouch|cap|seal|box|tin|bottle)"
STATE_WORDS = r"(?:open(?:ed)?|closed|shut|zipped shut|unzipped|visible|inside|packed|empty|full)"
_TRUTH = [re.compile(rf"\b((?:\w+[ -]){{0,3}}{PART_WORDS})\s+(?:is\s+|being\s+|to\s+be\s+)?({STATE_WORDS})\b", re.I),
          re.compile(rf"\b({STATE_WORDS})\s+((?:\w+[ -]){{0,3}}{PART_WORDS})\b", re.I),
          re.compile(rf"\b(the\s+(?:bag|product|box|pack))\s+(?:is\s+)?(?:being\s+)?({STATE_WORDS})\b", re.I)]
_STOPWORDS = {"a", "an", "the", "our", "its", "their", "and", "into", "in", "goes", "slides", "must", "show", "shows", "of", "then", "with", "see"}


def truths_in(text: str) -> list:
    out = []
    for i, rx in enumerate(_TRUTH):
        for m in rx.finditer(text):
            a, b = (m.group(1), m.group(2)) if i != 1 else (m.group(2), m.group(1))
            part = " ".join(w for w in a.lower().split() if w not in _STOPWORDS).strip()
            state = b.lower()
            if part:
                out.append(f"{part} {state}")
    return list(dict.fromkeys(out))


def _clauses(text: str) -> list:
    parts = re.split(r"(?<=[.;!?])\s+|,\s+(?:and\s+)?|\s+—\s+|\s+and\s+(?=the\s|a\s|then\s)", text)
    return [p.strip(" .") for p in parts if p and len(p.strip()) > 3]


class SimulatedWorkers:
    def respond(self, worker: str, form: str, blocks: dict, media: list, **kw) -> dict:
        return getattr(self, f"{worker}__{form}")(blocks, media, **kw)

    # ── waiter ─────────────────────────────────────────────────────────────────────────────────────────────
    # kitchen v3: a voice-over is offered when the customer asks; dialogue and lip-sync are not
    UNSUPPORTED = [(r"\bdialogue\b(?!,? ?no)|\btalking head|\bspeaks?\b", "dialogue or talking heads"),
                   (r"lip[- ]?sync", "lip-sync"), (r"celebrity|shah ?rukh|virat|deepika", "identifiable real person / celebrity likeness"),
                   (r"\b(4[5-9]|[5-9]\d|1\d\d)[- ]?(s|sec|second)", "films longer than 30 seconds")]

    def waiter__understanding(self, b, media):
        words = b["CUSTOMER_EXACT_WORDS"]
        order = b.get("ORDER_SLIP") or {}
        answers = b.get("ANSWERS") if isinstance(b.get("ANSWERS"), dict) else {}
        cinput = b.get("CUSTOMER_INPUT") if isinstance(b.get("CUSTOMER_INPUT"), dict) else {}
        low = words.lower()
        low_neg = re.sub(r"\bno (dialogue|voice[- ]?over|dialog)[^.;]*", "", low)
        unsupported = [lab for pat, lab in self.UNSUPPORTED if re.search(pat, low_neg)]
        product = order.get("product") or {}
        strings = [s for s in order.get("exact_strings", []) if s]
        mandatory = [{"id": f"M{i + 1}", "requirement": f'the exact text "{s}" appears, character for character',
                      "source": "customer_stated", "observable_as": "rendered text matches the string"} for i, s in enumerate(strings)]
        mandatory.append({"id": f"M{len(mandatory) + 1}", "requirement": "the customer's product is the hero and matches the supplied photos",
                          "source": "customer_supplied", "observable_as": "product shape, colour and parts match the photos"})
        for m in re.findall(r"must (?:show|have|include) ([^.;]+)", low):
            for part in re.split(r"\s+and\s+(?=the\s)", m):
                mandatory.append({"id": f"M{len(mandatory) + 1}", "requirement": part.strip(), "source": "customer_stated",
                                  "observable_as": f"'{part.strip()}' is visible in the finished media"})
        # photo roles from what the (simulated) vision sees, compared with the customer's caption and note
        photos, mismatches = [], []
        note = order.get("references_note") or ""
        blobs = [bl for m, bl in media if m.startswith("image/")]
        for i, p in enumerate(order.get("photos", [])):
            seen = shows_of(blobs[i]) if i < len(blobs) else None
            caption = p.get("customer_label")
            m = re.search(rf"photo\s*{p['photo']}\b([^.;]*)", note, re.I)
            said = " ".join(x for x in (caption, m.group(1) if m else None) if x) or None
            role = role_of(seen or said or p.get("filename"))
            photos.append({"photo": p["photo"], "asset_id": p["asset_id"], "role": role, "shows": seen or said or "a product photo",
                           "customer_label": caption})
            if seen and said and role_of(said) not in (role, "other") and not (role_of(said) == "product_view" and role == "product_detail"):
                mismatches.append({"what": f"photo {p['photo']} is described as '{said.strip()}' but shows {seen}",
                                   "where": f"photo {p['photo']}", "why_it_matters": "the kitchen would plan from the wrong picture"})
        questions = []
        if len(words.split()) < 12 and not answers:
            questions.append({"id": "Q1", "question": "Who is this for, and what should they do after seeing it?",
                              "why_it_matters": "the idea and the call to action depend on it",
                              "default_if_delegated": "urban 22–40 online shoppers; visit the brand's store"})
        media_kind = order.get("media", "image")
        return {
            "customer_exact_words": words, "supported": not unsupported,
            "refusal_reason": ("This beta cannot produce: " + ", ".join(unsupported)) if unsupported else None,
            "nearest_supported_alternative": "A film with music, ambience and on-screen text instead of speech" if unsupported else None,
            "unsupported_features": unsupported,
            "objective": f"Make people want {product.get('name') or 'the product'}",
            "audience": answers.get("Q1") or "urban 22–40 online shoppers",
            "audience_response": {"think": "this is made for me", "feel": "curious and reassured", "do": "look it up"},
            "brand": product.get("brand") or "the brand",
            "product": {"name": product.get("name") or "the product", "category": product.get("category") or "product",
                        "facts": [f for f in [product.get("description")] if f]},
            "deliverable": {"media": media_kind, "formats": order.get("formats") or (["9:16"] if media_kind == "video" else ["1:1"]),
                            "duration_s": order.get("duration_s") if media_kind == "video" else None},
            "mandatory": mandatory, "forbidden": ["model-drawn lettering or logos", "speech or singing"],
            "photo_roles": photos, "mismatches": mismatches,
            "assumptions": [{"assumption": "the product photos show the current product", "cost_if_wrong": "high"}],
            "questions": questions, "ambiguity": "medium" if questions else "low",
            "accepted_alternatives": list(cinput.get("accepted_alternatives") or []),
            "tone": "warm, confident", "market": "IN", "language": "en"}

    def waiter__change_request(self, b, media):
        fb = b.get("FEEDBACK") or {}
        text = fb.get("text", "") if isinstance(fb, dict) else str(fb)
        target = fb.get("target") if isinstance(fb, dict) else None
        m = re.search(r'(?:copy|text|headline|line)\s*(?:to|should read|:)\s*"([^"]+)"', text)
        if m:
            cid = (target or "c1").split(":")[-1]
            return {"class": "targeted_change", "targets": [{"kind": "copy", "ref": cid, "change": "new text"}], "preserve": ["all pictures"],
                    "copy_changes": [{"id": cid, "text": m.group(1)}], "explanation_for_customer": "We'll reset that line exactly as written."}
        if re.search(r"whole idea|different concept|start over", text, re.I):
            return {"class": "concept_change", "targets": [], "preserve": [], "copy_changes": [],
                    "explanation_for_customer": "This changes the idea, so we'll come back with a new plan and quote."}
        if target and target.startswith(("shot:", "beat:")):
            n = target.split(":")[1]
            return {"class": "targeted_change", "targets": [{"kind": "shot", "ref": n, "change": text}],
                    "preserve": ["every other shot", "music", "copy", "master plate"], "copy_changes": [],
                    "explanation_for_customer": f"We'll remake only shot {n}."}
        if target == "music" or re.search(r"\bmusic\b", text, re.I):
            return {"class": "targeted_change", "targets": [{"kind": "music", "ref": "music", "change": text}], "preserve": ["pictures", "copy"],
                    "copy_changes": [], "explanation_for_customer": "We'll change the music only."}
        return {"class": "targeted_change", "targets": [{"kind": "composition", "ref": "hero", "change": text}], "preserve": ["copy", "logo"],
                "copy_changes": [], "explanation_for_customer": "We'll rework the picture with that change."}

    # ── pantry and oven checker (the vision half; verdicts are code) ─────────────────────────────────────────────
    # ── chef ───────────────────────────────────────────────────────────────────────────────────────────────
    def chef__recipe(self, b, media):
        """Kitchen v3 recipe: the story, the anchors, a board where each shot names its tool and carries full prompts."""
        u = b.get("UNDERSTANDING") or {}
        order = b.get("ORDER_SLIP") or {}
        media_kind = (u.get("deliverable") or {}).get("media", "image")
        name = (u.get("product") or {}).get("name") or "the product"
        words = b.get("CUSTOMER_EXACT_WORDS", "")
        strings = order.get("exact_strings") or []
        copy = [{"id": f"c{i + 1}", "text": s, "role": "headline" if i == 0 else "line", "source": "customer_exact"} for i, s in enumerate(strings)]
        tray_ids = [i["id"] for i in (b.get("TRAY") or [])][:6]
        hands_only = bool(re.search(r"\bonly hands|hands only|\bhands\b", words, re.I))
        person = ("the same two hands and lower forearms, off-white cuffs, no rings" if hands_only
                  else "a woman of about 60 in a sage cotton kurta, silver hair in a low bun, thin reading glasses")
        world = "a warm Indian living room at evening, a teak side table, one cup of chai, a warm lamp"
        look = (f"A cinematic photograph, vertical: {person}, in {world}, holding {name} exactly as in the product photos; "
                f"soft lamp light from the left; warm natural colour; calm upper third.")
        shots = []
        if media_kind == "video":
            total = float((u.get("deliverable") or {}).get("duration_s") or 15)
            each = round((total - 3.0) / 3, 2)
            board = [("The moment", "recognition", "video"), ("The product", "admiration", "photo"), ("The feeling", "warmth", "still")]
            for i, (title, feeling, tool) in enumerate(board, 1):
                shots.append({"n": i, "duration_s": each, "title": title, "feeling": feeling,
                              "framing": f"medium close shot, eye level, {title.lower()}", "impact": f"{feeling} lands",
                              "description": f"A 50mm eye-level shot in {world}: {person}; {title.lower()} with {name}. The viewer "
                                             f"feels {feeling}.",
                              "tool": tool, "picture_prompt": "" if tool == "photo" else f"{look} Shot {i}: {title.lower()}.",
                              "motion_prompt": ("She looks down at the product and a slow smile arrives; the camera drifts in a "
                                                "little. Nothing else moves." if tool == "video" else "a slow push-in"),
                              "photo_index": 1 if tool == "photo" else None, "product_present": True,
                              "super_id": "c1" if (i == 2 and copy) else None,
                              "must_survive": f"{title.lower()}: {feeling}, with the same person", "may_change": "angle, lens, length",
                              "not_instead": "a product photo in place of the moment"})
            shots.append({"n": 4, "duration_s": 3.0, "title": "End card", "feeling": "the idea, remembered", "framing": "the end card",
                          "impact": "the name and the line", "description": "The end card, set by code.", "tool": "end_card",
                          "picture_prompt": "", "motion_prompt": "", "photo_index": None, "product_present": False, "super_id": None,
                          "must_survive": "", "may_change": "", "not_instead": ""})
        wants_voice = bool(re.search(r"\bvoice[- ]?over\b|\bnarrat|\bvo\b", words, re.I)) and \
            not re.search(r"\bno voice|without (a )?voice|no vo\b", words, re.I)
        voice = {"wanted": wants_voice and media_kind == "video", "language": "hi-IN",
                 "direction": "a warm woman in her fifties, unhurried, smiling in the voice, soft Hindi-English, small pauses",
                 "lines": [{"shot": 1, "text": f"{name}. Aaram se."}] if wants_voice and media_kind == "video" else []}
        return {
            "selected_concept": "The quiet evening", "remember": name, "audience_person": "a 60-year-old at home in the evening",
            "story": (f"An ordinary evening in a warm home. Someone the viewer could be picks up {name}, and a small moment of "
                      f"comfort follows; the film ends on their smile and the product at rest in the soft lamp light."),
            "identity_anchors": {"person": person, "product": f"{name} exactly as the customer's photos show it", "world": world,
                                 "grade": "natural, warm, premium"},
            "look": {"picture_prompt": look, "text_zone": "top", "product_present": True},
            "sound": {"music_prompt": "warm, understated piano with a gentle build; instrumental", "ambience": "room tone, a cup set down"},
            "voice_over": voice, "copy_deck": copy, "shots": shots,
            "end_card": {"copy_ids": [c["id"] for c in copy], "background_hex": "#1f2a44"},
            "reference_photos": [1] if b.get("PHOTOS") not in (None, "no photos supplied") else [],
            # chef v9: three directions through the three offered lenses; recent dishes read
            "audience_truth": "They want to feel looked after without being sold to.",
            "directions": [{"lens": x["id"], "idea": f"{name}, seen as {x['name']}", "form": "three moments and an end card",
                            "on_screen": "the person and the product"} for x in ((b.get("LENSES") or {}).get("offered") or
                                                                                   [{"id": "observer", "name": "o"}, {"id": "street_comic", "name": "c"},
                                                                                    {"id": "demonstrator", "name": "d"}])][:3],
            "chosen_direction": "the first direction, because its idea fits this order best",
            "lens": ((b.get("LENSES") or {}).get("offered") or [{"id": "observer"}])[0]["id"],
            "shape": "three moments and an end card",
            "habits_refused": "none repeated" if b.get("RECENT_DISHES") in (None, "none yet") else "changed the setting and the music from the recent dishes",
            "library_used": tray_ids,
            "customer_summary": f"One warm evening with {name}: a real moment, the product exactly as it is, and your words at the end."}

    # ── tasters ───────────────────────────────────────────────────────────────────────────────────────────
    def head_cook__ingredient_check(self, b, media, **kw):
        return {"usable": True, "unsure": False, "must_survive_kept": "cannot_determine", "required_action_occurred": "cannot_determine", "end_state_reached": "cannot_determine",
                "product_identity_ok": "cannot_determine", "character_consistent": "cannot_determine",
                "matches_master_plate": "cannot_determine", "matches_previous_plate": "cannot_determine", "differences": [],
                "prohibited_present": [], "unrequested_elements": [], "lettering_present": "cannot_determine",
                "best_segment": {"in_s": 0.0, "out_s": 0.0}, "notes": "simulated inspection: nothing was looked at",
                "repair": "keep", "better_prompt": ""}

    def head_cook__voice_cast(self, b, media, **kw):
        vo = b.get("VOICE_OVER") or {}
        return {"provider": "sarvam", "voice": "priya", "language_code": vo.get("language") or "hi-IN",
                "settings": {"pace": 0.95, "pitch": 0, "style": "warm", "style_prompt": vo.get("direction", "")},
                "lines": [{"shot": ln["shot"], "text": ln["text"], "ssml": ""} for ln in vo.get("lines", [])],
                "why": "simulated cast: Sarvam carries Hinglish best on the evidence so far"}

    def gatekeeper__final_review(self, b, media, **kw):
        mand = b.get("MANDATORY") or []
        return {"verdict": "pass", "modalities_evaluated": ["simulated"],
                "mandatory": [{"mandatory_id": m["id"], "visible": "cannot_determine", "evidence": "simulated"} for m in mand],
                "defects": [], "product_fidelity": {"verdict": "cannot_determine", "evidence": "simulated"},
                "continuity": {"verdict": "cannot_determine", "evidence": "simulated"},
                "model_lettering": {"present": "cannot_determine", "evidence": "simulated"},
                "subject_obstructed": {"present": "cannot_determine", "evidence": "simulated"},
                "product_across_shots": {"verdict": "cannot_determine", "evidence": "simulated"},
                "commercial_read": "not evaluated (simulated)", "audio": {"speech_or_singing": "cannot_determine", "notes": "simulated"},
                "summary_for_customer": "Simulated review — no one has looked at this media."}

    # ── diary writer ──────────────────────────────────────────────────────────────────────────────────────
    def diary_writer__lessons(self, b, media):
        jf = b.get("JOB_FILE") or {}
        outcome = jf.get("outcome") or "abandoned"
        recipe = jf.get("recipe") or {}
        per = []
        routes = sorted({s["route"] for s in recipe.get("shots", []) if s.get("route") not in (None, "END-CARD")}) or (["IMG"] if jf.get("media") == "image" else [])
        classes = sorted({s["action_class"] for s in recipe.get("shots", []) if s.get("action_class") not in (None, "none")})
        per.append({"worker": "chef", "what_went_right": "the recipe used only allowed routes" if recipe else "no recipe was written",
                    "what_went_wrong": "" if outcome == "accepted" else f"the customer's verdict was {outcome}",
                    "evidence_refs": [f"recipe v{jf.get('recipe_version', 0)}"],
                    "proposed_change": {"target": "recipe_library", "why": "every recipe is kept with its outcome",
                                        "diff": {"summary": (recipe.get("customer_summary") or jf.get("title") or "job")[:400], "outcome": outcome,
                                                 "customer_words": (jf.get("verdict_words") or "")[:300], "action_classes": classes,
                                                 "routes": routes, "product_category": jf.get("product_category"), "media": jf.get("media"),
                                                 "recipe": {k: recipe.get(k) for k in ("proposition", "selected_concept", "shots")}}}} if recipe else
                   {"worker": "chef", "what_went_right": "", "what_went_wrong": "no recipe was written", "evidence_refs": [], "proposed_change": None})
        for node, n in sorted((jf.get("taster_rejections") or {}).items()):
            cls = (jf.get("node_classes") or {}).get(node)
            if n >= 2 and cls:
                per.append({"worker": "head_cook", "what_went_right": f"rejected {n} takes of {node} before they reached the film",
                            "what_went_wrong": f"{cls} failed repeatedly on its route",
                            "evidence_refs": [f"events take_rejected node={node}"],
                            "proposed_change": {"target": "equipment_sheet", "why": f"{n} rejected takes of {cls}",
                                                "diff": {"action_class": cls, "verdict": "cannot", "routes": [(jf.get("node_routes") or {}).get(node, "FILM-C")],
                                                         "sample_count": n, "evidence_refs": [f"{jf.get('job_id')} {node}"],
                                                         "note": f"rejected {n} of {n} takes on {jf.get('job_id')}"}}})
        for d in jf.get("defects") or []:
            per.append({"worker": "gatekeeper", "what_went_right": f"found {d.get('id')}", "what_went_wrong": d.get("description", "")[:200],
                        "evidence_refs": [f"final_review {d.get('id')}"],
                        "proposed_change": {"target": "failure_diary", "why": "a defect found on a finished cut",
                                            "diff": {"text": d.get("description", "")[:600], "failure_mode": d.get("earliest_stage") or "unknown",
                                                     "action_classes": classes, "routes": routes, "media": jf.get("media")}}})
        sent = [x for x in jf.get("send_backs") or [] if x.get("rule") == "SB-RECIPE"]
        if sent:
            per.append({"worker": "chef", "what_went_right": "", "what_went_wrong": f"the recipe was sent back {len(sent)} times",
                        "evidence_refs": [f"send_back SB-RECIPE round {x.get('round')}" for x in sent],
                        "proposed_change": {"target": "rulebook_card", "why": f"{len(sent)} recipe send-backs: {sent[-1].get('why', '')[:200]}",
                                            "diff": {"worker": "chef", "changes": {"kra_add": "Before planning any hand action, read its "
                                                     "equipment-sheet row; plan a still of the state for anything marked cannot."}}}})
        for w in ("waiter", "pantry_checker", "recipe_checker"):
            per.append({"worker": w, "what_went_right": "form complete", "what_went_wrong": "", "evidence_refs": [f"{w} form"], "proposed_change": None})
        return {"outcome": outcome, "what_the_customer_said": jf.get("verdict_words") or "(no words recorded)", "per_worker": per}
