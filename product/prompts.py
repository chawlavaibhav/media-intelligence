"""Deterministic prompt builder: board + product dossier -> generation prompts. A prompt is never typed
by hand and never written by a model directly; the director's decisions are rendered into the prompt
shapes that worked on Mokobara/V2 (verbatim product block, one light line, one dominant cue, the
no-lettering clause, explicit absence before the reveal, exit action after a goal state)."""
from __future__ import annotations

import re

NO_LETTERING = ("No text, no lettering, no captions, no logos, no signage, no labels with readable words, "
                "no watermark anywhere in the picture.")
NO_SPEECH = "No one speaks, sings or moves their lips; natural ambient sound only."
BASE_NEGATIVE = ["text", "letters", "captions", "watermark", "logo", "signage", "talking", "speech", "singing",
                 "lip movement", "extra fingers", "warped product", "duplicate product"]


def _strip(text: str, words: list) -> str:
    for w in sorted({w for w in words if w and len(w) > 1}, key=len, reverse=True):
        text = re.sub(r"\b" + re.escape(w) + r"\b", "the", text, flags=re.I)
    return re.sub(r"\bthe the\b", "the", text)


def guard_for(intent: dict, direction: dict, brief: dict) -> dict:
    """What the dispatcher must refuse in any prompt of this job."""
    exact = [c["text"] for c in direction.get("copy_deck", [])] + list(brief.get("exact_strings") or [])
    brand = (intent.get("brand") or "").strip()
    forbidden = [brand] if brand and brand.lower() not in ("the brand", "") else []
    forbidden += list(brief.get("forbidden_words") or [])
    return {"exact_strings": exact, "forbidden_words": forbidden}


def _anchor(direction: dict, guard: dict) -> str:
    return _strip(direction.get("product_anchor", ""), guard["forbidden_words"])


def _look(direction: dict) -> str:
    v = direction.get("visual_language") or {}
    pal = ", ".join(v.get("palette") or [])
    return f"Look: {v.get('look', '')}. Light: {v.get('light', '')}. Palette: {pal}. Camera: {v.get('camera', '')}."


def still_prompt(direction: dict, guard: dict, *, beat: dict | None = None, aspect: str, with_product_ref: bool,
                 with_character_ref: bool) -> str:
    lines = []
    if beat is None:          # the hero picture of a still ad
        c = direction.get("composition") or {}
        lines.append(f"A commercial product photograph. {c.get('hero', '')}. Background: {c.get('background', '')}. "
                     f"Product treatment: {c.get('product_treatment', '')}.")
        zone = c.get("text_zone", "none")
        if zone != "none":
            lines.append(f"Keep the {zone} {'third' if zone in ('top', 'bottom') else 'side'} of the frame calm and uncluttered "
                         f"(plain background there, nothing important in it).")
        lines.append(f"The product: {_anchor(direction, guard)} It is brand new, completely intact, clean, exactly as in the "
                     f"reference photo{'s' if with_product_ref else ''}.")
    else:
        lines.append(f"A cinematic film still, the first frame of a shot. {beat.get('first_frame', '')}.")
        if beat.get("product_present"):
            lines.append(f"The product: {_anchor(direction, guard)} State: {beat.get('product_state') or 'intact'}; "
                         f"brand new, completely intact, exactly as in the reference photo.")
        else:
            lines.append("The product does not appear anywhere in this picture; no bag, box, bottle or package of any kind.")
        ch = direction.get("character") or {}
        if ch.get("present"):
            lines.append(f"The person: {ch.get('description', '')}" + (" — the same person as in the character reference image."
                                                                       if with_character_ref else "."))
        if beat.get("continuity"):
            lines.append("Continuity: " + "; ".join(beat["continuity"]) + ".")
        if beat.get("must_not"):
            lines.append("Must not appear: " + ", ".join(_strip(m, guard["forbidden_words"]) for m in beat["must_not"]) + ".")
        lines.append(f"Camera: {beat.get('camera', '')}.")
    lines.append(_look(direction))
    lines.append(f"Aspect ratio {aspect}. Photorealistic.")
    lines.append(NO_LETTERING)
    return _strip(" ".join(lines), guard["forbidden_words"])


def clip_prompt(direction: dict, guard: dict, beat: dict) -> str:
    parts = [f"Animate this exact first frame. {beat.get('action', '')}.",
             f"By the end of the shot: {beat.get('end_state', '')}."]
    if beat.get("exit_action"):
        parts.append(f"After that: {beat['exit_action']}. The goal state is never undone.")
    if beat.get("product_present"):
        parts.append("The product stays exactly as in the first frame: same shape, colour and details, intact, never deforming.")
    else:
        parts.append("The product never appears in this shot.")
    parts.append(f"Camera: {beat.get('camera', '')}. One continuous shot, no cuts, no scene change.")
    parts.append(NO_SPEECH)
    parts.append("No text or lettering appears.")
    return _strip(" ".join(parts), guard["forbidden_words"])


def clip_negative(direction: dict, guard: dict, beat: dict, product_words: list) -> str:
    neg = list(BASE_NEGATIVE)
    if not beat.get("product_present"):
        neg += product_words
    neg += ["scene cut", "camera cut", "morphing"]
    return _strip(", ".join(dict.fromkeys(n for n in neg if n)), guard["forbidden_words"])


def character_prompt(direction: dict, guard: dict, aspect: str) -> str:
    ch = direction.get("character") or {}
    return _strip(f"Character reference photograph: {ch.get('description', '')}. Full body and clear face, standing, neutral "
                  f"expression, plain light-grey studio background, even soft light. {_look(direction)} Aspect ratio {aspect}. "
                  f"{NO_LETTERING}", guard["forbidden_words"])


def music_prompt(direction: dict, guard: dict) -> tuple:
    s = direction.get("sound") or {}
    p = _strip(f"Instrumental music bed for a short commercial film: {s.get('music_brief', '')}. Instrumental only, no vocals, "
               f"no singing, no spoken words.", guard["forbidden_words"])
    return p, "vocals, singing, voice, speech, lyrics"


def product_words(intent: dict) -> list:
    p = intent.get("product") or {}
    words = [p.get("category") or ""] + re.findall(r"[A-Za-z]{4,}", p.get("category") or "")
    return [w for w in dict.fromkeys(words) if w]
