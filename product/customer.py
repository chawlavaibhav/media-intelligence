"""What the customer sees and hears (founder, 2026-09-23): "we don't show them the kitchen, but we keep them engaged".

The customer never sees the kitchen — no worker names, routes, check ids, retries, models or costs per call. They see:
  - their order, as the waiter wrote it down;
  - a progress line that keeps moving while the kitchen works (the 15–20 minutes of a film are never silent);
  - the plan in plain words, a first look, and a taste of the hardest shot before the rest is made;
  - the finished work with a short, friendly list of what was checked;
  - a message whenever it is their turn (on the page, and by email when a mail server is configured).
"""
from __future__ import annotations

import json
import os
import re
import smtplib
from email.message import EmailMessage

from product.flow import CUSTOMER_STATES

# ── progress ────────────────────────────────────────────────────────────────────────────────────────────────────────
STATE_WORDS = {
    "submitted": "We've received your order.",
    "understanding": "We're reading your brief and looking at your photos.",
    "needs_answers": "We have a few quick questions for you.",
    "feasibility": "We're checking we can make everything you asked for.",
    "awaiting_customer_input": "We need one thing from you before we start.",
    "directing": "Our creative team is writing your plan.",
    "awaiting_approval": "Your plan and a first look are ready for you.",
    "planning": "Thank you! We're setting up production.",
    "producing": "We're making it now.",
    "awaiting_master_approval": "The look of your film is ready — have a look.",
    "awaiting_taste": "A first moving shot is ready for you to taste.",
    "checking": "Giving everything a final check.",
    "ready_for_review": "It's ready for you.",
    "revising": "We're making your changes.",
    "needs_customer_decision": "We need your decision on one thing.",
    "needs_retry_decision": "Something went wrong on our side. You can ask us to try again, or stop here.",
    "paused_budget": "We've paused: this needs a little more budget.",
    "paused_provider": "One of our production services is slow; we'll carry on shortly.",
    "paused_operator": "Our team is taking a look; we'll carry on shortly.",
    "paused_for_founder": "Our team is taking a look; we'll carry on shortly.",
    "failed": "Something went wrong on our side; our team has been told.",
    "accepted": "Delivered. Thank you!",
    "rejected": "Closed.",
    "abandoned": "Closed.",
    "refused": "We can't make this one yet.",
}


def node_words(kind: str, spec: dict, total_shots: int) -> str | None:
    if kind == "master":
        return "The look of your film is ready."
    if kind == "character":
        return "The people in your film are ready."
    if kind in ("frame", "photo"):
        return f"Scene {spec.get('shot')} of {total_shots} is set up — here is how it looks."
    if kind == "voice":
        return "The voice-over is recorded."
    if kind == "shot":
        return f"Shot {spec.get('shot')} of {total_shots} is made."
    if kind == "plate":
        return f"Your {spec.get('aspect')} picture is made."
    if kind == "music":
        return "The music is ready."
    if kind in ("assemble", "compose_still"):
        return "Putting it all together."
    return None


def tell(store, job_id: str, text: str, asset: str | None = None):
    """One line on the customer's progress (never repeated back to back). `asset`: a still the head cook kept, shown with
    the line (founder 2026-09-25: keep showing the customer the stills as they are made)."""
    last = store.events(job_id, ("customer_update",))
    if last and json.loads(last[-1]["data_json"]).get("text") == text and not asset:
        return
    store.event(job_id, "waiter", "customer_update", {"text": text, **({"asset": asset} if asset else {})})


def progress(store, job_id: str, limit: int = 40) -> list:
    """The customer's progress line: state changes in plain words plus what the kitchen finished, oldest first."""
    job = store.job(job_id)
    out, last = [{"utc": job["created"], "text": STATE_WORDS["submitted"]}], STATE_WORDS["submitted"]
    for e in store.events(job_id, ("state", "customer_update")):
        d = json.loads(e["data_json"])
        text = STATE_WORDS.get(d.get("to")) if e["kind"] == "state" else d.get("text")
        if text and (text != last or d.get("asset")):
            out.append({"utc": e["utc"], "text": text, "asset": d.get("asset")})
            last = text
    return out[-limit:]


# ── words from the kitchen never reach the customer ───────────────────────────────────────────────────────────────
_KITCHEN_TOKENS = [(re.compile(r"\s*\((?:FILM-[ABC]|IMG)[^)]*\)"), ""), (re.compile(r"\b(?:FILM-[ABC]|EQ-\w+)\b,?\s*"), ""),
                   (re.compile(r"\s{2,}"), " ")]


def plain(text) -> str:
    """Strip route codes and equipment ids from text a worker wrote, before a customer reads it."""
    out = str(text or "")
    for pat, sub in _KITCHEN_TOKENS:
        out = pat.sub(sub, out)
    return out.strip()


# ── what we checked, in the customer's words ───────────────────────────────────────────────────────────────────────
FRIENDLY = [
    (r"^exact_copy_match$", "Your exact words appear exactly as you wrote them."),
    (r"^ad_structure$", "It has everything an ad needs: your product, your message and a clear ending."),
    (r"^format_revalidated$", "Each size was laid out on its own, not cropped from another."),
    (r"(^|:)(bounds:logo|disjoint)$", "Your logo and text sit cleanly and don't cover each other."),
    (r"^hero_visible$", "Your product is clearly visible."),
    (r"^product_colour_match$", "Your product's colours match your photos."),
    (r"^(loudness_true_peak|audio_joins)$", "The sound is at the right level and smooth between shots."),
    (r"^(delivery_conformance|container_edit_lists|source_resolution)$", "The file plays correctly on phones and social apps."),
    (r"^no_black_frames$", "No black or frozen moments."),
    (r"^end_card:", "The ending card is clean and on-brand."),
    (r"^super:", "The words on screen are easy to read."),
    (r"^clips:no_in_model_cut$", "No sudden jumps inside a shot."),
    (r"^brand_colour", "Your brand colours are used."),
]


def friendly(check_id: str) -> str | None:
    for pat, words in FRIENDLY:
        if re.search(pat, check_id):
            return words
    return None


def checked_list(gateway_results: list) -> list:
    """The passed checks the customer would care about, in plain words, once each."""
    out = []
    for g in gateway_results:
        for row in g["table"]:
            w = friendly(row["check_id"]) if row["status"] == "PASS" else None
            if w and w not in out:
                out.append(w)
    return out


def problem_words(check_id: str, detail: str = "") -> str:
    """A failed measurement in plain words (never the check's internal name)."""
    w = friendly(check_id)
    if w:
        return "This did not hold: " + w[0].lower() + w[1:]
    return "One of our automatic measurements on the finished file did not pass."


# ── "it's your turn" ───────────────────────────────────────────────────────────────────────────────────────────────
TURN_WORDS = {
    "needs_answers": "We have a few quick questions about your order",
    "awaiting_customer_input": "We need one thing from you before we start",
    "awaiting_approval": "Your plan and a first look are ready",
    "awaiting_master_approval": "The look of your film is ready for your OK",
    "awaiting_taste": "A first shot of your film is ready to taste",
    "ready_for_review": "Your work is ready",
    "needs_customer_decision": "We need your decision",
    "needs_retry_decision": "Something went wrong on our side — try again or stop?",
    "paused_budget": "Your job needs a little more budget",
}


def notify_turn(k, job_id: str, state: str):
    """Tell the customer it is their turn: always on the page (an event), and by email when a mail server is set up
    (MI_SMTP_HOST, MI_SMTP_PORT, MI_SMTP_USER, MI_SMTP_PASSWORD, MI_MAIL_FROM). Never raises."""
    if state not in CUSTOMER_STATES or state not in TURN_WORDS:
        return
    job = dict(k.store.job(job_id))
    who = job.get("created_by") or ""
    user = k.store.user(who) or k.store.user_by_email(who) if who else None
    user = dict(user) if user else None
    subject = f"{TURN_WORDS[state]} — {job['title']}"
    body = (f"Hello{(' ' + user['name']) if user and user.get('name') else ''},\n\n{TURN_WORDS[state]}.\n"
            f"Open your order: {k.s.base_url.rstrip('/')}/jobs/{job_id}\n\nThank you,\nMedia Intelligence")
    sent, why = False, "no mail server configured (MI_SMTP_HOST); shown on the customer's page"
    host = os.environ.get("MI_SMTP_HOST")
    if host and user and user.get("email"):
        try:
            msg = EmailMessage()
            msg["Subject"], msg["From"], msg["To"] = subject, os.environ.get("MI_MAIL_FROM", "no-reply@localhost"), user["email"]
            msg.set_content(body)
            with smtplib.SMTP(host, int(os.environ.get("MI_SMTP_PORT", "587")), timeout=20) as s:
                s.starttls()
                if os.environ.get("MI_SMTP_USER"):
                    s.login(os.environ["MI_SMTP_USER"], os.environ.get("MI_SMTP_PASSWORD", ""))
                s.send_message(msg)
            sent, why = True, "emailed"
        except Exception as e:  # noqa: BLE001 — a mail failure must never stop the kitchen
            from product.config import scrub
            why = f"email failed: {scrub(str(e))[:160]}"
    k.store.event(job_id, "waiter", "customer_notified", {"state": state, "subject": subject, "emailed": sent, "note": why})
