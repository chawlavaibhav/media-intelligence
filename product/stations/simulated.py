"""Deterministic, no-network stand-ins for the seven AI workers — for dry runs and tests only (USD 0).

They follow the same forms as the live models, so every station, send-back and gate is exercised. Everything they write
is labelled simulated, and the door guard never counts a simulated judge's "yes" as verification.

Simulated vision: a test photo may carry a PNG text chunk `mi-sim-shows` saying what the picture shows (tests use it to
stand in for what a vision model would see, e.g. "people for scale" behind a caption that says "product"). Without it,
the simulation only knows the customer's caption.
Tests change a worker's behaviour by replacing a method on this object (e.g. `sim.small_taster__ingredient_check`).
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
    UNSUPPORTED = [(r"\bvoice[- ]?over\b(?! ?(?:is|are)? ?not)|\bnarrat", "spoken voice-over"),
                   (r"\bdialogue\b(?!,? ?no)|\btalking head|\bspeaks?\b", "dialogue or talking heads"),
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
    def pantry_checker__feasibility(self, b, media):
        words = b["CUSTOMER_EXACT_WORDS"]
        u = b.get("UNDERSTANDING") or {}
        roles = u.get("photo_roles") or []
        media_kind = (u.get("deliverable") or {}).get("media", "image")
        need = truths_in(words)
        for m in u.get("mandatory", []):
            need += truths_in(m["requirement"])
        truths = []
        for t in dict.fromkeys(need):
            key = [w for w in t.split() if len(w) > 3 and w not in ("open", "opened", "closed", "visible", "shut", "zipped")]
            state = t.split()[-1]
            hit = next((r for r in roles if r["role"] in ("product_view", "product_detail", "infographic")
                        and all(k.rstrip("s") in r["shows"].lower() for k in key[-1:])
                        and (state in ("closed", "shut", "visible", "packed") or state.rstrip("ed") in r["shows"].lower())), None)
            truths.append({"part_state": t, "covered_by_photo": "yes" if hit else "no", "photo_ref": hit["photo"] if hit else None,
                           "source": "photo" if hit else "none"})
        accepted = {a["instead_of"].lower(): a["use"] for a in u.get("accepted_alternatives") or []}
        actions = []
        for c in _clauses(words):
            if re.search(r"\b(no|never|not)\b.*\b(dialogue|voice|face)", c, re.I):
                continue
            cls = library.classify(c)
            if not cls or cls[0] in ("product_state_still",):
                continue
            if any(k in c.lower() or c.lower() in k for k in accepted):
                continue
            actions.append({"id": f"A{len(actions) + 1}", "action": c, "action_class": cls[0], "required_by_customer": True})
        for inst, use in accepted.items():
            actions.append({"id": f"A{len(actions) + 1}", "action": use, "action_class": "product_state_still", "required_by_customer": True})
        if media_kind == "video" and not any(a["action_class"] == "camera_move_static_product" for a in actions):
            actions.insert(0, {"id": "A0", "action": "the camera moves gently around the product at rest",
                               "action_class": "camera_move_static_product", "required_by_customer": False})
        if media_kind == "image":
            infographic = any(r["role"] == "infographic" for r in roles) and not any(r["role"] == "product_view" for r in roles)
            actions = [{"id": "A1", "action": "the product pictured from the customer's photo",
                        "action_class": "product_still_from_infographic_photo" if infographic else "product_still_from_clean_photo",
                        "required_by_customer": True}]
        return {"product_truth": truths, "actions_needed": actions}

    # ── chef ───────────────────────────────────────────────────────────────────────────────────────────────
    def chef__recipe(self, b, media):
        u, f = b.get("UNDERSTANDING") or {}, b.get("FEASIBILITY") or {}
        order = b.get("ORDER_SLIP") or {}
        media_kind = (u.get("deliverable") or {}).get("media", "image")
        name = (u.get("product") or {}).get("name") or "the product"
        strings = order.get("exact_strings") or []
        copy = [{"id": f"c{i + 1}", "text": s, "role": "headline" if i == 0 else "line", "source": "customer_exact"} for i, s in enumerate(strings)]
        tray_ids = [i["id"] for i in (b.get("TRAY") or [])][:4]
        verdicts = {}
        for v in f.get("route_verdicts", []):
            verdicts.setdefault(v["action_id"], []).append(v)
        shots, risks = [], []
        if media_kind == "video":
            total = float((u.get("deliverable") or {}).get("duration_s") or 15)
            usable = []
            for a in f.get("actions_needed", []):
                ok = [v for v in verdicts.get(a["id"], []) if v["verdict"] in ("reliable", "risky")]
                if ok:
                    best = min(ok, key=lambda v: (library.RANK[v["verdict"]], v["route"]))
                    usable.append((a, best))
            usable = usable[:5] or []
            each = round((total - 3.0) / max(1, len(usable)), 2)
            mand = [m["id"] for m in u.get("mandatory", []) if not m["requirement"].startswith("the exact text")]
            for i, (a, v) in enumerate(usable):
                risky = v["verdict"] == "risky"
                shots.append({"n": i + 1, "duration_s": each, "purpose": "show it", "first_frame": f"{name} in the master-plate room; {a['action']}",
                              "action": a["action"], "end_state": "the moment holds", "camera": "35mm, eye level", "route": v["route"],
                              "action_class": a["action_class"], "starts_from": "master_plate" if (i == 0 or risky) else "previous_shot_end",
                              "feasibility_refs": [a["id"]], "product_present": True, "product_state": "intact",
                              "continuity": ["same room, light and product as the master plate"], "must_not": [],
                              "super_id": "c1" if (i == 1 and copy) else None, "mandatory_ids": mand if i == 0 else []})
                if risky:
                    risks.append({"shot": i + 1, "action_id": a["id"], "risk": f"{a['action_class']} is risky on {v['route']}",
                                  "limit": "produced first from the master plate; one simple action; code motion fallback"})
            shots.append({"n": len(shots) + 1, "duration_s": 3.0, "purpose": "sign-off", "first_frame": "end card", "action": "none",
                          "end_state": "logo and line", "camera": "n/a", "route": "END-CARD", "action_class": "none", "starts_from": "still_only",
                          "feasibility_refs": [], "product_present": False, "product_state": "n/a", "continuity": [], "must_not": [],
                          "super_id": None, "mandatory_ids": [m["id"] for m in u.get("mandatory", []) if m["requirement"].startswith("the exact text")]})
        return {
            "proposition": f"{name}: the small thing that makes the day easier",
            "concepts": [{"name": "The quiet fix", "idea": f"an ordinary moment, resolved by {name}", "why_it_works": "product as hero"}],
            "selected_concept": "The quiet fix", "rationale": "simplest route from the audience's moment to the product truth",
            "audience_experience": "recognition, then relief", "hook": "a moment the viewer knows", "remember": name,
            "visual_language": {"look": "natural, premium", "light": "one soft window light", "palette": ["#1f2a44", "#f4efe6"],
                                "camera": "35mm, shallow depth"},
            "sound": {"music_brief": "warm, understated, gentle build", "ambience": "room tone"},
            "product_anchor": f"{name} exactly as the customer's photos show it, clean and intact",
            "master_plate": {"description": f"{name} at rest on a warm oak table by a window, soft morning light", "product_state": "closed, intact"},
            "character": {"present": False, "description": ""},
            "copy_deck": copy,
            "composition": {"hero": f"{name} centre-left, three-quarter view", "text_zone": "top" if media_kind == "image" else "none",
                            "background": "calm warm wall", "product_treatment": "soft key light, gentle shadow"},
            "shots": shots, "end_card": {"copy_ids": [c["id"] for c in copy], "background_hex": "#1f2a44"},
            "risks": risks, "library_used": tray_ids, "reuse_shelf_items": [s["id"] for s in (b.get("SHELF") or {}).get("master_plates", [])[:1]]
            + [s["id"] for s in (b.get("SHELF") or {}).get("characters", [])[:1]],
            "customer_summary": f"We open on {name} in one calm room and let the story unfold shot by shot, ending on your line and logo."}

    # ── recipe checker (the model half; code rules decide too) ───────────────────────────────────────────────
    def recipe_checker__recipe_check(self, b, media):
        r = b.get("RECIPE") or {}
        u = b.get("UNDERSTANDING") or {}
        planned = {s.get("action_class") for s in r.get("shots", [])}
        matched = [i["id"] for i in (b.get("TRAY") or []) if i["section"] == "failure_diary"
                   and any(c in i["text"] for c in planned if c not in ("none",))][:5]
        covered = {m for s in r.get("shots", []) for m in s.get("mandatory_ids", [])}
        return {"verdict": "approve", "predicted_acceptance": "uncertain",
                "acceptance_reason": "simulated recipe check — nobody judged the idea",
                "mandatory_coverage": [{"mandatory_id": m["id"], "covered": m["id"] in covered or not r.get("shots"),
                                        "where": "shots" if m["id"] in covered else "composition"} for m in u.get("mandatory", [])],
                "issues": [], "add_steps": [], "past_failures_matched": matched}

    # ── tasters ───────────────────────────────────────────────────────────────────────────────────────────
    def small_taster__ingredient_check(self, b, media, **kw):
        return {"usable": True, "unsure": False, "required_action_occurred": "cannot_determine", "end_state_reached": "cannot_determine",
                "product_identity_ok": "cannot_determine", "character_consistent": "cannot_determine",
                "matches_master_plate": "cannot_determine", "matches_previous_plate": "cannot_determine", "differences": [],
                "prohibited_present": [], "unrequested_elements": [], "lettering_present": "cannot_determine",
                "best_segment": {"in_s": 0.0, "out_s": 0.0}, "notes": "simulated inspection: nothing was looked at"}

    def big_taster__final_review(self, b, media, **kw):
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
                per.append({"worker": "small_taster", "what_went_right": f"rejected {n} takes of {node} before they reached the film",
                            "what_went_wrong": f"{cls} failed repeatedly on its route",
                            "evidence_refs": [f"events take_rejected node={node}"],
                            "proposed_change": {"target": "equipment_sheet", "why": f"{n} rejected takes of {cls}",
                                                "diff": {"action_class": cls, "verdict": "cannot", "routes": [(jf.get("node_routes") or {}).get(node, "FILM-C")],
                                                         "sample_count": n, "evidence_refs": [f"{jf.get('job_id')} {node}"],
                                                         "note": f"rejected {n} of {n} takes on {jf.get('job_id')}"}}})
        for d in jf.get("defects") or []:
            per.append({"worker": "big_taster", "what_went_right": f"found {d.get('id')}", "what_went_wrong": d.get("description", "")[:200],
                        "evidence_refs": [f"final_review {d.get('id')}"],
                        "proposed_change": {"target": "failure_diary", "why": "a defect found on a finished cut",
                                            "diff": {"text": d.get("description", "")[:600], "failure_mode": d.get("earliest_stage") or "unknown",
                                                     "action_classes": classes, "routes": routes, "media": jf.get("media")}}})
        for w in ("waiter", "pantry_checker", "recipe_checker"):
            per.append({"worker": w, "what_went_right": "form complete", "what_went_wrong": "", "evidence_refs": [f"{w} form"], "proposed_change": None})
        return {"outcome": outcome, "what_the_customer_said": jf.get("verdict_words") or "(no words recorded)", "per_worker": per}
