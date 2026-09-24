"""Station 2 — the waiter (spec §3, §4.2, §4.9, §5). Cheap AI. Writes Understanding; takes change requests.
The change-taker of v1 is merged in here (spec §4.9)."""
from __future__ import annotations

import json
import re

from product.store import sha256_bytes

# Founder 2026-09-24 (a beta customer's 20-s Reel was ordered with the form left on "Image 1:1" and the waiter REFUSED the
# job): a mix-up or an unsupported ask is a question to the customer, never a dead end. Asked once; refused only if the
# answer still cannot be made.
MEDIA_Q, ALT_Q = "Q-MEDIA", "Q-ALTERNATIVE"
FILM_WORDS = re.compile(r"\b(reels?|videos?|films?|clips?|animat\w*|motion|footage|\d{1,2}\s*-?\s*(?:s|sec|secs|seconds?)\b)", re.I)
IMAGE_WORDS = re.compile(r"\b(posters?|still images?|static|banners?|carousels?|flyers?|thumbnails?)\b", re.I)


def media_mismatch(slip: dict, words: str) -> str | None:
    """What the customer's words describe, when it contradicts the media they picked on the order form."""
    if slip["media"] == "image" and FILM_WORDS.search(words):
        return "video"
    if slip["media"] == "video" and IMAGE_WORDS.search(words) and not FILM_WORDS.search(words):
        return "image"
    return None


def _apply_media_answer(k, job_id, slip, answers) -> dict:
    a = str(answers.get(MEDIA_Q) or "").lower()
    if not a:
        return slip
    media = "video" if re.search(r"video|film|reel|clip", a) else "image" if re.search(r"image|poster|still|picture", a) else None
    if not media or media == slip["media"]:
        return slip
    fmts = [f for f in ("9:16", "16:9", "1:1", "4:5") if f in a] or (["9:16"] if media == "video" else ["1:1"])
    secs = re.search(r"(\d{1,2})\s*(?:s|sec|second)", a)
    dur = float(min(30, max(6, int(secs.group(1))))) if media == "video" and secs else (20.0 if media == "video" else None)
    k.store.put_artifact(job_id, "order_change", {"media": media, "formats": fmts[:1] if media == "video" else fmts,
                                                  "duration_s": dur, "from_answer": a[:300]}, "customer")
    k.store.set_job(job_id, media=media)
    return k.order_slip(job_id)


def understand(k, job_id: str):
    job = k.store.job(job_id)
    if job["state"] == "submitted":
        k.store.transition(job_id, "submitted", "understanding", actor="system")
    slip = k.order_slip(job_id)
    words = k.exact_words(job_id)
    answers = k.store.artifact(job_id, "answers") or {}
    slip = _apply_media_answer(k, job_id, slip, answers)
    cinput = k.store.artifact(job_id, "customer_input") or {}
    ctx = {"ORDER_SLIP": {kk: v for kk, v in slip.items() if kk not in ("customer_exact_words",) and not kk.startswith("_")},
           "ANSWERS": answers or "none yet", "CUSTOMER_INPUT": cinput or "none",
           "SHELF": k.shelf.summary(job["account_id"])}
    with k.store.timed(job_id, "understanding"):
        form = k.workers.call(job_id, "waiter", "understanding", ctx, exact_words=words, media=k.photo_media(job_id))
    _floor(k, job_id, form, slip, words)
    wants = None if answers else media_mismatch(slip, words)
    if not answers and (wants or not form["supported"]):
        qs = list(form.get("questions") or [])
        if wants:
            picked = "an image (" + ", ".join(slip["formats"] or ["1:1"]) + ")" if slip["media"] == "image" else "a short film"
            qs.insert(0, {"id": MEDIA_Q, "question": f"Your brief describes {'a film / Reel' if wants == 'video' else 'an image'}, but the order "
                          f"form says {picked}. Which should we make? Answer 'video' (and 9:16 or 16:9, and the length in seconds) or 'image'.",
                          "why_it_matters": "a film and an image are planned and priced differently",
                          "default_if_delegated": "video 9:16" if wants == "video" else "image 1:1"})
        if not form["supported"] and not wants:
            qs.insert(0, {"id": ALT_Q, "question": f"We can't make this exactly as asked: {form.get('refusal_reason') or ''} "
                          f"We can make: {form.get('nearest_supported_alternative') or 'a close alternative'}. Go ahead with that? (yes / no)",
                          "why_it_matters": "without it we cannot start", "default_if_delegated": "no"})
        form.update(questions=qs[:5], supported=True)
    k.put_form(job_id, "understanding", form)
    if not form["supported"]:
        k.store.transition(job_id, "understanding", "refused", actor="system",
                           data={"reason": form.get("refusal_reason"), "alternative": form.get("nearest_supported_alternative")},
                           closed_at=_now(), outcome="refused")
        return
    if form.get("questions") and not answers:
        from product import flow
        flow.send_back(k.store, job_id, "SB-WAITER-QUESTIONS", why=f"{len(form['questions'])} questions")
        k.store.transition(job_id, "understanding", "needs_answers", actor="system")
        k.store.timing_start(job_id, "customer_wait", "answers")
        return
    k.store.transition(job_id, "understanding", "feasibility", actor="system")


def _floor(k, job_id, form, slip, words):
    """Deterministic floor under the waiter's reading (each correction is recorded as an event):
    the exact words byte-equal to the order slip; the media, formats and duration the customer chose; every exact string
    a must-have; every photo labelled."""
    notes = []
    if form.get("customer_exact_words") != words:
        notes.append("customer_exact_words differed from the order slip; replaced with the order slip's bytes")
        form["customer_exact_words"] = words
    d = form["deliverable"]
    d["media"] = slip["media"]
    d["formats"] = slip["formats"] or d.get("formats")
    if slip["media"] == "video" and slip.get("duration_s"):
        d["duration_s"] = float(slip["duration_s"])
    have = " ".join(m["requirement"] for m in form.get("mandatory", []))
    for s in slip.get("exact_strings", []):
        if s and s not in have:
            form["mandatory"].append({"id": f"M{len(form['mandatory']) + 1}", "requirement": f'the exact text "{s}" appears, character for character',
                                      "source": "customer_stated", "observable_as": "rendered text equals the string"})
            notes.append(f"added the exact string {s!r} as a must-have")
    labelled = {r["photo"] for r in form.get("photo_roles", [])}
    for p in slip.get("photos", []):
        if p["photo"] not in labelled:
            form["photo_roles"].append({"photo": p["photo"], "asset_id": p["asset_id"], "role": "other", "shows": "not labelled by the waiter",
                                        "customer_label": p.get("customer_label")})
            notes.append(f"photo {p['photo']} was not labelled; marked 'other' for the pantry checker")
    if notes:
        k.store.event(job_id, "system", "waiter_floor", {"notes": notes, "exact_words_sha256": sha256_bytes(words.encode())})


def change_request(k, job_id: str, feedback: dict) -> dict:
    """One change request → one Change request form (the waiter classifies; flow sends it to the affected station)."""
    recipe = k.store.artifact(job_id, "recipe") or {}
    u = k.store.artifact(job_id, "understanding") or {}
    ctx = {"FEEDBACK": {"target": feedback.get("target"), "text": feedback.get("text")},
           "RECIPE_SHOTS": [{kk: s.get(kk) for kk in ("n", "purpose", "action", "route")} for s in recipe.get("shots", [])],
           "COPY_DECK": recipe.get("copy_deck", []), "MANDATORY": u.get("mandatory", [])}
    form = k.workers.call(job_id, "waiter", "change_request", ctx, exact_words=k.exact_words(job_id))
    k.put_form(job_id, "change_request", form)
    return form


def _now():
    from product.store import utc_now
    return utc_now()


def slip_json(slip: dict) -> str:
    return json.dumps(slip, ensure_ascii=False, sort_keys=True)
