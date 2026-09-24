"""Deterministic prompt builder: board + product dossier -> generation prompts. A prompt is never typed
by hand and never written by a model directly; the director's decisions are rendered into the prompt
shapes that worked on Mokobara/V2 (verbatim product block, one light line, one dominant cue, the
no-lettering clause, explicit absence before the reveal, exit action after a goal state)."""
from __future__ import annotations

import re

# The product's own small marks are part of the product; everything else is lettering the model must not add.
# Live 2026-09-23: a blanket "no logos anywhere" contradicted "preserve the brand details exactly" and the inspector
# rejected faithful bags for carrying their real badge.
NO_LETTERING = ("No text, no lettering, no captions, no signage, no watermark and no logos added anywhere in the scene; "
                "the only marks allowed are the product's own small brand marks exactly as they appear on the reference photos.")
NO_SPEECH = "No one speaks, sings or moves their lips; natural ambient sound only."
BASE_NEGATIVE = ["text", "letters", "captions", "watermark", "logo", "signage", "talking", "speech", "singing",
                 "lip movement", "extra fingers", "warped product", "duplicate product"]


def _strip(text: str, words: list) -> str:
    for w in sorted({w for w in words if w and len(w) > 1}, key=len, reverse=True):
        # (?<!\w)/(?!\w) rather than \b, so a string that starts or ends in punctuation ("Pack less. Go further.") is scrubbed too
        text = re.sub(r"(?<!\w)" + re.escape(w) + r"(?!\w)", "the", text, flags=re.I)
    return re.sub(r"\bthe the\b", "the", text)


_OVERLAY = re.compile(r"\b(logo|logos|wordmark|code-set|code set|composit\w*|overlay\w*|supers?|headline|tagline|copy deck|"
                      r"text layer|end card|typeset|caption\w*|website|url|on[- ]screen|words? (appear|fade|rise|sit)\w*)\b", re.I)


def _visual(text: str) -> str:
    """Only what the camera sees. The director's notes about code-set layers (logo, headline, supers, end card) never reach
    a generator — live 2026-09-23: 'a small supplied logo occupies the upper-left margin as a code-set layer' came back as a
    drawn 'SUPPLIED' label. The word 'supplied' is dropped for the same reason."""
    keep = [s for s in re.split(r"(?<=[.;!?])\s+", text or "") if s and not _OVERLAY.search(s)]
    return re.sub(r"\bsupplied\s+", "", " ".join(keep), flags=re.I).strip()


def guard_for(intent: dict, direction: dict, brief: dict) -> dict:
    """What the dispatcher must refuse in any prompt of this job."""
    exact = [c["text"] for c in direction.get("copy_deck", [])] + list(brief.get("exact_strings") or [])
    brand = (intent.get("brand") or "").strip()
    forbidden = [brand] if brand and brand.lower() not in ("the brand", "") else []
    forbidden += list(brief.get("forbidden_words") or [])
    # every exact string the dispatcher refuses (dispatch.prompt_guard: longer than 3 characters) is scrubbed from the
    # prompts like the brand — live 2026-09-24: a recipe naming "iPhone Duo" in its product anchor could never produce
    forbidden += [s for s in exact if s and len(s) > 3 and s not in forbidden]
    return {"exact_strings": exact, "forbidden_words": forbidden}


def _anchor(direction: dict, guard: dict) -> str:
    return _strip(_visual(direction.get("product_anchor", "")), guard["forbidden_words"])


def _look(direction: dict) -> str:
    v = direction.get("visual_language") or {}
    pal = ", ".join(v.get("palette") or [])
    return f"Look: {v.get('look', '')}. Light: {v.get('light', '')}. Palette: {pal}. Camera: {v.get('camera', '')}."


def still_prompt(direction: dict, guard: dict, *, beat: dict | None = None, aspect: str, with_product_ref: bool,
                 with_character_ref: bool) -> str:
    lines = []
    if beat is None:          # the hero picture of a still ad
        c = direction.get("composition") or {}
        lines.append(f"A commercial product photograph. {_visual(c.get('hero', ''))} Background: {_visual(c.get('background', ''))} "
                     f"Product treatment: {_visual(c.get('product_treatment', ''))}")
        zone = c.get("text_zone", "none")
        if zone != "none":
            lines.append(f"Keep the {zone} {'third' if zone in ('top', 'bottom') else 'side'} of the frame calm and uncluttered "
                         f"(plain background there, nothing important in it).")
        lines.append(f"The product: {_anchor(direction, guard)} It is brand new, completely intact, clean, exactly as in the "
                     f"reference photo{'s' if with_product_ref else ''}.")
    else:
        lines.append(f"A cinematic film still, the first frame of a shot. {_visual(beat.get('first_frame', ''))}")
        if beat.get("description"):     # recipe v2: the chef's full plain-English paragraph for this shot
            lines.append(f"The shot: {_visual(beat['description'])}")
        anchors = direction.get("identity_anchors") or {}
        if anchors.get("world"):
            lines.append(f"The place: {_visual(anchors['world'])}")
        if beat.get("product_present"):
            lines.append(f"The product: {_anchor(direction, guard)} State: {_visual(beat.get('product_state') or 'intact')}; "
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
        lines.append(f"Camera: {_visual(beat.get('camera', ''))}")
    lines.append(_look(direction))
    lines.append(f"Aspect ratio {aspect}. Photorealistic.")
    lines.append(NO_LETTERING)
    return _strip(" ".join(lines), guard["forbidden_words"])


def clip_prompt(direction: dict, guard: dict, beat: dict) -> str:
    parts = [f"Animate this exact first frame. {_visual(beat.get('action', ''))}"]
    if beat.get("description"):         # recipe v2: what the camera sees, moment by moment, and what the viewer feels
        parts.append(f"The shot: {_visual(beat['description'])}")
    parts.append(f"By the end of the shot: {_visual(beat.get('end_state', ''))}")
    if beat.get("exit_action"):
        parts.append(f"After that: {_visual(beat['exit_action'])} The goal state is never undone.")
    if beat.get("product_present"):
        parts.append("The product stays exactly as in the first frame: same shape, colour and details, intact, never deforming.")
    else:
        parts.append("The product never appears in this shot.")
    parts.append(f"Camera: {_visual(beat.get('camera', ''))} One continuous shot, no cuts, no scene change.")
    parts.append(NO_SPEECH)
    parts.append("No text or lettering appears.")
    return _strip(" ".join(parts), guard["forbidden_words"])


def clip_negative(direction: dict, guard: dict, beat: dict, product_words: list) -> str:
    neg = list(BASE_NEGATIVE)
    if not beat.get("product_present"):
        neg += product_words
    neg += ["scene cut", "camera cut", "morphing"]
    return _strip(", ".join(dict.fromkeys(n for n in neg if n)), guard["forbidden_words"])


_HANDS_ONLY = re.compile(r"\b(no face|never (a|the) face|only (by )?(the |two )?(same )?(\w+ )?hands|hands only|hands and (lower )?forearms only)\b", re.I)


def character_prompt(direction: dict, guard: dict, aspect: str) -> str:
    """The reference image frames the character the way the film will: a hands-only film gets a hands reference
    (live 2026-09-23: 'full body and clear face' contradicted a hands-only plan and both draws were rightly rejected)."""
    ch = direction.get("character") or {}
    desc = ch.get("description", "")
    if _HANDS_ONLY.search(desc):
        framing = ("Close-up reference photograph of the two hands and lower forearms only, palms down then relaxed, cuffs "
                   "visible; no face, head, torso or other body part anywhere in the frame")
    else:
        framing = "Full body and clear face, standing, neutral expression"
    return _strip(f"Character reference photograph: {_visual(desc)} {framing}, plain light-grey studio background, even soft "
                  f"light. {_look(direction)} Aspect ratio {aspect}. {NO_LETTERING}", guard["forbidden_words"])


def music_prompt(direction: dict, guard: dict) -> tuple:
    s = direction.get("sound") or {}
    p = _strip(f"Instrumental music bed for a short commercial film: {s.get('music_brief', '')}. Instrumental only, no vocals, "
               f"no singing, no spoken words.", guard["forbidden_words"])
    return p, "vocals, singing, voice, speech, lyrics"


def product_words(intent: dict) -> list:
    p = intent.get("product") or {}
    words = [p.get("category") or ""] + re.findall(r"[A-Za-z]{4,}", p.get("category") or "")
    return [w for w in dict.fromkeys(words) if w]


# ── v2: one master plate, every shot chained from it (spec §5 head cook, §6.1) ──────────────────────────────────────────
def master_plate_prompt(recipe: dict, guard: dict, *, aspect: str, with_product_ref: bool) -> str:
    """The master plate: the film's one world — room, light, product — at rest. Every shot is built from it."""
    mp = recipe.get("master_plate") or {}
    lines = [f"A cinematic film still that establishes the whole film's world. {_visual(mp.get('description', ''))}",
             f"The product: {_anchor(recipe, guard)} State: {_visual(mp.get('product_state') or 'intact')}; brand new, completely intact, "
             f"exactly as in the reference photo{'s' if with_product_ref else ''}."]
    ch = recipe.get("character") or {}
    if ch.get("present"):
        lines.append(f"The person: {_visual(ch.get('description', ''))}")
    lines += [_look(recipe), f"Aspect ratio {aspect}. Photorealistic.", NO_LETTERING]
    return _strip(" ".join(lines), guard["forbidden_words"])


CHAIN_CLAUSE = ("Continuity: the same room, light, product (shape, colour, every opening) and the same hands/person and wardrobe "
                "as the MASTER PLATE reference image{prev}. Nothing about the product changes.")


def shot_frame_prompt(recipe: dict, guard: dict, shot: dict, *, aspect: str, has_previous: bool, correction: str = "") -> str:
    base = still_prompt(recipe, guard, beat=shot, aspect=aspect, with_product_ref=True, with_character_ref=False)
    chain = CHAIN_CLAUSE.format(prev="; it continues directly from the PREVIOUS SHOT reference image" if has_previous else "")
    corr = f" Correct this from the last attempt: {_visual(correction)}." if correction else ""
    return _strip(base.replace(NO_LETTERING, chain + corr + " " + NO_LETTERING), guard["forbidden_words"])
