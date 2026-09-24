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
    if kind == "frame":
        return f"Scene {spec.get('shot')} of {total_shots} is set up."
    if kind == "shot":
        return f"Shot {spec.get('shot')} of {total_shots} is made."
    if kind == "plate":
        return f"Your {spec.get('aspect')} picture is made."
    if kind == "music":
        return "The music is ready."
    if kind in ("assemble", "compose_still"):
        return "Putting it all together."
    return None


def tell(store, job_id: str, text: str):
    """One line on the customer's progress (never repeated back to back)."""
    last = store.events(job_id, ("customer_update",))
    if last and json.loads(last[-1]["data_json"]).get("text") == text:
        return
    store.event(job_id, "waiter", "customer_update", {"text": text})


def progress(store, job_id: str, limit: int = 40) -> list:
    """The customer's progress line: state changes in plain words plus what the kitchen finished, oldest first."""
    job = store.job(job_id)
    out, last = [{"utc": job["created"], "text": STATE_WORDS["submitted"]}], STATE_WORDS["submitted"]
    for e in store.events(job_id, ("state", "customer_update")):
        d = json.loads(e["data_json"])
        text = STATE_WORDS.get(d.get("to")) if e["kind"] == "state" else d.get("text")
        if text and text != last:
            out.append({"utc": e["utc"], "text": text})
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


# ── the chat (founder 2026-09-24): the customer types a prompt, and the job is one conversation ──────────────────────
LIST_WORDS = {
    "needs_answers": "Waiting for your reply", "awaiting_customer_input": "Waiting for your reply", "awaiting_approval": "Your plan is ready",
    "awaiting_master_approval": "The look is ready to see", "awaiting_taste": "A first shot is ready to see",
    "ready_for_review": "Ready for you", "needs_customer_decision": "Needs your decision", "needs_retry_decision": "Needs your decision",
    "paused_budget": "Needs your OK to continue", "accepted": "Delivered", "rejected": "Closed", "abandoned": "Closed",
    "refused": "We couldn't make this one", "paused_operator": "Our team is on it", "paused_for_founder": "Our team is on it",
    "failed": "Our team is on it", "operator_hold": "Final look",
}


def list_words(state: str) -> str:
    """A job's state on the customer's list of ads, in a few plain words."""
    return LIST_WORDS.get(state, "We're working on it")


WORKING = {"submitted": "Reading your brief…", "understanding": "Reading your brief…",
           "feasibility": "Checking we can make everything you asked for…", "directing": "Sketching your plan…",
           "planning": "Setting up the shoot…", "checking": "Giving it a final look…", "revising": "Making your changes…",
           "paused_provider": "One of our tools is slow today — we'll carry on shortly…", "operator_hold": "Giving it a final look…"}


def working_line(store, job_id: str) -> str | None:
    """What we are doing right now, in the present tense ("Shooting scene 3 of 6…"); None when it is not our turn."""
    job = store.job(job_id)
    s = job["state"]
    if s == "producing":
        nodes = [n for n in store.nodes(job_id) if n["status"] != "retired"]
        if job["media"] != "video":
            return "Making your pictures…"
        master = next((n for n in nodes if n["kind"] == "master"), None)
        if master and master["status"] != "done":
            return "Setting the look of your film…"
        shots = [n for n in nodes if n["kind"] == "shot"]
        done = sum(1 for n in shots if n["status"] == "done")
        if shots and done < len(shots):
            return f"Shooting scene {done + 1} of {len(shots)}…"
        return "Putting your film together…"
    return WORKING.get(s)


def order_line(brief: dict) -> str:
    """What is being made, in a few words: "Instagram Reel · 20 seconds" / "Image · square and portrait"."""
    f = brief.get("formats") or []
    if brief.get("media") == "video":
        kind = "Instagram Reel" if f[:1] == ["9:16"] else "Short film, landscape" if f[:1] == ["16:9"] else "Short film"
        return f"{kind} · {int(float(brief.get('duration_s') or 15))} seconds"
    names = {"1:1": "square", "4:5": "portrait", "9:16": "story", "16:9": "landscape"}
    sizes = [names.get(x, x) for x in f or ["1:1"]]
    return ("Image · " if len(sizes) == 1 else "Images · ") + " and ".join([", ".join(sizes[:-1]), sizes[-1]] if len(sizes) > 1 else sizes)


# What the customer's button presses look like in the thread (their own typed words are shown as they wrote them).
PRESSED = {"awaiting_approval": "Approved — go ahead.", "awaiting_master_approval": "The look is right — make the film.",
           "awaiting_taste": "Looks good — make the rest.", "ready_for_review": "Accepted.", "needs_retry_decision": "Try again.",
           "needs_customer_decision": "One more attempt, please.", "paused_budget": "Yes, continue."}
DELEGATED = "decide for me (use your default)"


def _near(a: str, b: str, seconds: float = 5) -> bool:
    from datetime import datetime
    f = "%Y-%m-%dT%H:%M:%S.%fZ"
    try:
        return abs((datetime.strptime(a, f) - datetime.strptime(b, f)).total_seconds()) <= seconds
    except ValueError:
        return False


def thread(store, job_id: str, customer_email: str) -> list:
    """The job as a conversation, oldest first: the customer's prompt (with their photos), our progress lines, and what
    the customer said or pressed since. Each item: {who: customer|studio, text, utc, kind: said|progress, photos}."""
    job = store.job(job_id)
    brief = store.original_brief(job_id)
    first = [a["id"] for a in store.assets(job_id, source="customer") if _near(a["created"], job["created"], 60)]
    out = [{"who": "customer", "text": brief["text"], "utc": job["created"], "kind": "said", "photos": first}]
    for p in progress(store, job_id)[1:]:
        out.append({"who": "studio", "text": p["text"], "utc": p["utc"], "kind": "progress"})
    arts = {k: store.q("SELECT data_json, created FROM artifacts WHERE job_id=? AND kind=? ORDER BY version", (job_id, k))
            for k in ("answers", "customer_input")}
    fb = store.feedback(job_id)
    for e in store.events(job_id, ("state",)):
        if e["actor"] != customer_email:
            continue
        d = json.loads(e["data_json"])
        frm, to, text, photos = d.get("from"), d.get("to"), None, []
        if frm == "needs_answers":
            a = next((json.loads(r["data_json"]) for r in reversed(arts["answers"]) if r["created"] <= e["utc"]), {})
            said = list(dict.fromkeys(str(v) for v in a.values() if str(v) != DELEGATED))
            text = "\n".join(said) or "Decide for me."
        elif frm == "awaiting_customer_input":
            ci = next((json.loads(r["data_json"]) for r in reversed(arts["customer_input"]) if r["created"] <= e["utc"]), {})
            bits = ([f for f in ci.get("facts", []) if f][-1:] + [ci.get("note")]) if ci else []
            text = "\n".join(b for b in bits if b) or "Yes, go ahead with your suggestions."
            photos = [a["id"] for a in store.assets(job_id, source="customer") if a["id"] not in first and _near(a["created"], e["utc"], 10)]
        elif d.get("change") or d.get("taste_change"):
            text = d.get("change") or d.get("taste_change")
        elif frm == "ready_for_review" and to in ("revising", "rejected"):
            text = "\n".join(f["text"] for f in fb if f["by_user"] == customer_email and _near(f["created"], e["utc"])) or None
        elif to in ("abandoned", "rejected"):
            text = "Stop here." if frm in ("needs_retry_decision", "needs_customer_decision") else "Close this ad."
        else:
            text = PRESSED.get(frm)
        if text:
            out.append({"who": "customer", "text": text, "utc": e["utc"], "kind": "said", "photos": photos})
    out.sort(key=lambda x: (x["utc"], x["who"] != "customer"))                # what they pressed, then our answer
    # our progress lines between two of their messages fold into one quiet line (the latest), the rest on a tap
    folded = []
    for m in out:
        if m["kind"] == "progress" and folded and folded[-1]["kind"] == "steps":
            folded[-1]["earlier"].append(folded[-1]["text"])
            folded[-1].update(text=m["text"], utc=m["utc"])
        elif m["kind"] == "progress":
            folded.append({**m, "kind": "steps", "earlier": []})
        else:
            folded.append(m)
    return folded
