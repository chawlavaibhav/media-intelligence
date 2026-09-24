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


# Founder 2026-09-24, later the same day: "Let the user enter a prompt. The form was an internal instrument the waiter fills
# for the kitchen." An order may be only a prompt (Service.submit_prompt). The waiter then fills the order slip itself from
# the customer's words — film or picture, sizes, length, exact text — and records it as an `order_change` (the customer's
# words stay as written). Code reads the words first: a film or a picture is decided only when the customer's words (or
# their answer) say so, never by default; when they don't, the waiter asks in the thread and the reply is the answer.
PROMPT_MEDIA_Q = "Should this be a Reel / short film, or a poster / image?"
PROMPT_NOTE = ("The customer only typed a prompt (a chat message); nothing was chosen on a form. The ORDER_SLIP's media, formats, "
               "length and exact strings were filled in by the waiter from their words. Put in `deliverable` the sizes and length "
               "their words ask for. If it is unclear which words must appear exactly and that matters, ask.")
PROMPT_NOTE_UNDECIDED = (" Their words do not say whether they want a film or a picture: the ORDER_SLIP's media is a placeholder "
                         "and we are asking them.")
IMAGE_SAID = re.compile(r"\b(posters?|stills?|static|banners?|carousels?|flyers?|thumbnails?|print ads?|(?:image|picture|photo) ads?|"
                        r"(?:an?|one|single|two|three|\d) (?:images?|pictures?)|(?:instagram|insta|feed|social|linkedin|facebook) posts?)\b", re.I)
SHORT_IMAGE = re.compile(r"\b(image|picture|poster|still)\b", re.I)          # a short answer: "image please"
SECONDS = re.compile(r"\b(\d{1,3})\s*-?\s*(?:s|secs?|seconds?)\b", re.I)
QUOTED = re.compile(r'["“”]([^"“”\n]{2,160})["“”]|‘([^‘’\n]{2,160})’')
# A quote is exact on-screen text only when the words just before it say so ("the words", "headline", "end on", "text
# cards"…). Live check 2026-09-24: a concept name in quotes (Concept, "One key":) was taken as required on-screen text.
ON_SCREEN = re.compile(r"\b(text|texts|words?|lines?|says?|reads?|appears?|headline|tagline|slogan|caption|copy|title|"
                       r"overlay|on[- ]screen|end (?:on|card|with)|written|write|spell\w*|cta|url|website|label)\b", re.I)


def on_screen_quotes(text: str) -> list:
    out = []
    for m in QUOTED.finditer(text or ""):
        q = (m.group(1) or m.group(2) or "").strip()
        before = text[max(0, m.start() - 60):m.start()]
        between_quotes = bool(out) and re.fullmatch(r"[\s,/;&and]*", text[prev_end:m.start()] or "") is not None
        if q and (ON_SCREEN.search(before) or between_quotes):
            out.append(q)
            prev_end = m.end()
        elif q:
            prev_end = m.end()
    return out
VERTICAL = re.compile(r"\b(reels?|stor(?:y|ies)|shorts|vertical|9:16)\b", re.I)
LANDSCAPE = re.compile(r"\b(youtube|landscape|horizontal|widescreen|16:9)\b", re.I)
IMAGE_SIZES = [("1:1", re.compile(r"\b(square|1:1)\b", re.I)), ("4:5", re.compile(r"\b(4:5|portrait)\b", re.I)),
               ("9:16", re.compile(r"\b(stor(?:y|ies)|9:16|vertical)\b", re.I)), ("16:9", re.compile(r"\b(16:9|landscape|youtube|banner)\b", re.I))]


def is_prompt_order(k, job_id) -> bool:
    return not k.store.original_brief(job_id).get("media")


def media_in(text: str) -> str | None:
    """What these words ask for: "video", "image", "both" or None (they don't say)."""
    film, image = bool(FILM_WORDS.search(text)), bool(IMAGE_SAID.search(text))
    if not (film or image) and len(text.split()) <= 6 and SHORT_IMAGE.search(text):
        image = True
    return "both" if film and image else "video" if film else "image" if image else None


def decide_order(k, job_id, answers: dict, form: dict | None = None) -> dict:
    """A prompt order's slip, filled from the customer's words and their answer to "film or picture?" — plus, where their
    words don't say, the waiter's reading (`form`: sizes, length, product). Recorded as a new `order_change` when it
    changes; `provisional` while nobody has said film or picture (the waiter then asks)."""
    words = k.exact_words(job_id)
    said = str(answers.get(MEDIA_Q) or "")
    media = media_in(said) if said else None
    media = media if media in ("image", "video") else None
    if media is None and said:                                  # answered, but not with a kind: the stated default
        media = "image" if not media_in(words) in ("image", "video") else media_in(words)
    if media is None:
        media = media_in(words) if media_in(words) in ("image", "video") else None
    provisional = media is None
    media = media or "image"
    texts = [words, said]
    d = (form or {}).get("deliverable") or {}
    if media == "video":
        secs = next((int(m[-1]) for t in reversed(texts) if (m := SECONDS.findall(t))), None) or d.get("duration_s") or 15
        dur = float(min(30, max(6, int(float(secs)))))
        fmts = ["16:9"] if any(LANDSCAPE.search(t) for t in texts) else ["9:16"] if any(VERTICAL.search(t) for t in texts) else \
            [f for f in (d.get("formats") or []) if f in ("9:16", "16:9")][:1] or ["9:16"]
    else:
        dur = None
        fmts = [f for f, rx in IMAGE_SIZES if any(rx.search(t) for t in texts)] or \
            [f for f in (d.get("formats") or []) if f in ("1:1", "4:5", "9:16", "16:9")] or ["1:1"]
    in_answer = [(a or b).strip() for a, b in QUOTED.findall(said or "") if (a or b).strip()]   # replying to our text question
    exact = list(dict.fromkeys(on_screen_quotes(words) + in_answer))[:8]
    prev = k.store.artifact(job_id, "order_change") or {}
    product = dict(prev.get("product") or {})
    if form and form.get("product"):
        p = form["product"]
        product = {"name": str(p.get("name") or "")[:300], "brand": str(form.get("brand") or "")[:300],
                   "category": str(p.get("category") or "")[:300], "description": "; ".join(p.get("facts") or [])[:300]}
    change = {"media": media, "formats": fmts, "duration_s": dur, "exact_strings": exact, "product": product,
              "provisional": provisional, "decided_by": "waiter", "from": "the customer's prompt" + (" and answer" if said else "")}
    if {x: prev.get(x) for x in change} != change:
        k.store.put_artifact(job_id, "order_change", change, "waiter")
    if k.store.job(job_id)["media"] != media:
        k.store.set_job(job_id, media=media)
    return change


def understand(k, job_id: str):
    job = k.store.job(job_id)
    if job["state"] == "submitted":
        k.store.transition(job_id, "submitted", "understanding", actor="system")
    words = k.exact_words(job_id)
    answers = k.store.artifact(job_id, "answers") or {}
    prompt = is_prompt_order(k, job_id)
    if prompt:
        decide_order(k, job_id, answers)                       # the slip needs a media before anyone reads it
    slip = k.order_slip(job_id)
    if not prompt:
        slip = _apply_media_answer(k, job_id, slip, answers)
    cinput = k.store.artifact(job_id, "customer_input") or {}
    ctx = {"ORDER_SLIP": {kk: v for kk, v in slip.items() if kk not in ("customer_exact_words",) and not kk.startswith("_")},
           "ANSWERS": answers or "none yet", "CUSTOMER_INPUT": cinput or "none",
           "SHELF": k.shelf.summary(job["account_id"])}
    if prompt:
        ctx["HOW_ORDERED"] = PROMPT_NOTE + (PROMPT_NOTE_UNDECIDED if (k.store.artifact(job_id, "order_change") or {}).get("provisional") else "")
    with k.store.timed(job_id, "understanding"):
        form = k.workers.call(job_id, "waiter", "understanding", ctx, exact_words=words, media=k.photo_media(job_id))
    ask_media = False
    if prompt:
        ask_media = decide_order(k, job_id, answers, form).get("provisional", False) and not answers
        slip = k.order_slip(job_id)
    _floor(k, job_id, form, slip, words)
    wants = None if (answers or prompt) else media_mismatch(slip, words)
    if not answers and (wants or ask_media or not form["supported"]):
        qs = list(form.get("questions") or [])
        if ask_media:
            qs = [q for q in qs if not re.search(r"\b(reel|film|video|poster|image|picture)\b", q.get("question", ""), re.I)]
            qs.insert(0, {"id": MEDIA_Q, "question": PROMPT_MEDIA_Q, "why_it_matters": "a film and a picture are planned and priced differently",
                          "default_if_delegated": "a poster / image"})
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
    k.store.transition(job_id, "understanding", "directing", actor="system")      # kitchen v3: straight to the chef


def hand_to_chef(k, job_id: str):
    """A job left in the retired `feasibility` step (kitchen v3 removed the pantry checker) goes straight to the chef."""
    k.store.transition(job_id, "feasibility", "directing", actor="system", data={"reason": "kitchen v3: no pantry checker"})


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
