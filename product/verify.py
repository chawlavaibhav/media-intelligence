"""Verification: one entry point for every production pathway, results bound to exact asset versions,
and the presentation gateway.

No renderer, script or model marks anything verified. Producers write media; this module writes check
rows (PASS / FAIL / NOT_VERIFIED / FLAG) against the asset's sha256; the gateway decides. A check that
applies and has no row on that exact version is NOT_VERIFIED and blocks, unless a named person waived it.
A simulated review can never PASS an independent-review obligation.
"""
from __future__ import annotations

import functools
import json
from decimal import Decimal
from pathlib import Path

import yaml

from product import media
from product.store import Store, dec

CONTROLS_FILE = Path(__file__).parent / "data" / "FAILURE-CONTROLS-v1.yaml"


@functools.lru_cache(maxsize=1)
def controls() -> dict:
    reg = yaml.safe_load(CONTROLS_FILE.read_text())
    return {c["id"]: c for c in reg["controls"]}


def required_checks(media_kind: str, *, mandatory_ids: list, has_copy: bool, has_logo: bool, super_ids: list = (),
                    has_character: bool = True) -> dict:
    """check_id -> control id, for the final asset of a job. Everything here must PASS (or be waived)."""
    req = {"ledger_integrity": "ATTEMPT_ID_UNIQUE_AND_RESERVE_MINTED",
           "exact_copy_match": "EXACT_COPY_MATCH",
           "not_previously_rejected": "REJECTED_DESIGN_REUSE",
           "independent_review": "QA_COVERAGE_ENFORCEMENT",
           "product_fidelity": "PRODUCT_INTACT_AND_FAITHFUL",
           "no_model_lettering": "VIDEO_FRAME_TEXT_HYGIENE",
           "ad_structure": "AD_STRUCTURE_MINIMUM"}
    for m in mandatory_ids:
        req[f"mandatory:{m}"] = "MANDATORY_EVENT_VISIBILITY_LJ_LINE"
    req.update(PROCESS_CONTROLS)
    req["process:direction_truth"] = "PRODUCT_AND_WORLD_TRUTH_BEFORE_SPEND"
    req["subject_unobstructed"] = "SUBJECT_OBSTRUCTION"
    if media_kind == "image":
        req["format_revalidated"] = "FORMAT_SPECIFIC_REVALIDATION"
        req["disjoint"] = "ELEMENT_DISJOINTNESS"
        req["hero_visible"] = "HERO_VISIBLE"
        if has_logo:
            req["bounds:logo"] = "TEXT_BOUNDS_GATE"
    else:
        req.update({"container_edit_lists": "CONTAINER_EDIT_LIST_CHECK", "loudness_true_peak": "CODEC_TRUE_PEAK_MARGIN",
                    "audio_joins": "AUDIO_LEVEL_CONTINUITY_AT_CUTS", "audio_reviewed": "AUDIO_REVIEWED_BY_EAR",
                    "source_resolution": "SOURCE_RESOLUTION_STATED", "delivery_conformance": "DELIVERY_CONFORMANCE",
                    "no_black_frames": "NO_BLACK_OR_DROPPED_PICTURE",
                    "end_card:disjoint": "ELEMENT_DISJOINTNESS", "end_card:brand_colour:end_card": "BRAND_COLOUR_ON_RENDERED_FRAME",
                    "clips:no_in_model_cut": "IN_MODEL_HARD_CUT"})
        for s in super_ids:
            req[f"super:{s}:contrast:super"] = "CONTRAST_GATE"
        if has_character:
            req["character_continuity"] = "CHARACTER_CONTINUITY"
        req.update(PROCESS_CONTROLS_VIDEO)
        req["product_across_shots"] = "PRODUCT_CONTINUITY_ACROSS_SHOTS"
        req["audio_heard_by_person"] = "AUDIO_REVIEWED_BY_EAR"
    return req


# Obligations only a person can discharge, by doing the thing — never by a waiver. The atlas's most repeated mechanism
# (no_human_ear_on_the_delivered_audio: six jobs) recurred because "nobody could listen" was always waivable in effect.
NON_WAIVABLE = {"audio_heard_by_person"}
ATTESTABLE = {"audio_heard_by_person": "Listened to the whole film with sound on: no speech, no singing, no clicks or holes at the cuts, "
                                       "music suits the story",
              "independent_review": "Watched the whole piece at phone size: a demanding customer would accept it as is",
              "product_fidelity": "The product is the customer's product — shape, colour, parts, openings — intact, not torn or warped",
              "product_across_shots": "The product is the same product in every shot",
              "character_continuity": "The person is the same person in every shot (face, hair, clothes, accessories)",
              "no_model_lettering": "No lettering, logo or wordmark was drawn by the model; only code-set text and the supplied logo",
              "subject_unobstructed": "The product/subject is never covered, cut off or blocked by text, graphics or objects",
              "small_taster_confirmed": "I looked at every picture and clip the small taster passed in this cut: the customer's "
                                        "product, the same hands/person, the same room and light, nothing warped"}


def attestable(check_id: str) -> str | None:
    if check_id in ATTESTABLE:
        return ATTESTABLE[check_id]
    if check_id.startswith("mandatory:"):
        return f"The mandatory item {check_id[10:]} visibly happens on screen (I can name the moment)"
    return None


def attest(store: Store, job_id: str, asset_id: str, check_id: str, *, founder, note: str, outcome: str = "PASS"):
    """The founder performed the check on this exact file and recorded what they found (spec §6.4: an unqualified judge's
    "yes" counts only once the founder confirms). `founder` is a FounderProof from authority.founder_proof(); the
    confirmation is stored as an override row, and the door guard counts the result only when that row exists."""
    statement = attestable(check_id)
    if statement is None:
        raise ValueError(f"{check_id} is not a person-performed check")
    if len(note.strip()) < 15:
        raise ValueError("say what you heard/saw (at least a sentence)")
    store.add_override(job_id, kind="confirm", target=f"{asset_id}:{check_id}", founder=founder, reason=note.strip(),
                       data={"outcome": outcome, "statement": statement})
    store.record_check(job_id, asset_id, check_id=check_id, status="PASS" if outcome == "PASS" else "FAIL", blocking=True,
                       runner=f"founder:{founder.email}", detail=note.strip()[:1000],
                       evidence={"by": founder.actor, "statement": statement},
                       control_ids=[_CONTROL_OF.get(check_id, "MANDATORY_EVENT_VISIBILITY_LJ_LINE")])


def waive(store: Store, job_id: str, asset_id: str, check_id: str, *, founder, reason: str):
    """The founder overrides a door-guard block on this exact file, with a written reason (spec §6.4)."""
    if check_id in NON_WAIVABLE:
        raise ValueError("this check cannot be waived — a person has to perform it and record what they found")
    store.add_override(job_id, kind="check_waiver", target=f"{asset_id}:{check_id}", founder=founder, reason=reason)
    store.waive(job_id, asset_id, check_id, founder.user_id, reason.strip())


_CONTROL_OF = {"audio_heard_by_person": "AUDIO_REVIEWED_BY_EAR", "independent_review": "QA_COVERAGE_ENFORCEMENT",
               "product_fidelity": "PRODUCT_INTACT_AND_FAITHFUL", "product_across_shots": "PRODUCT_CONTINUITY_ACROSS_SHOTS",
               "character_continuity": "CHARACTER_CONTINUITY", "no_model_lettering": "VIDEO_FRAME_TEXT_HYGIENE",
               "subject_unobstructed": "SUBJECT_OBSTRUCTION", "small_taster_confirmed": "QA_COVERAGE_ENFORCEMENT"}


def record_rows(store: Store, job_id: str, asset_id: str, rows: list, *, runner: str, prefix: str = ""):
    for r in rows:
        store.record_check(job_id, asset_id, check_id=prefix + r["check_id"], status=r["status"],
                           blocking=r.get("blocking", True), runner=runner, detail=r.get("detail", ""),
                           evidence=r.get("evidence"), control_ids=[r.get("control", "")])


# ── deterministic checks ───────────────────────────────────────────────────────────────────────
def ledger_integrity(store: Store, job_id: str) -> dict:
    rows = store.attempts(job_id)
    ids = [r["id"] for r in rows]
    seqs = [r["seq"] for r in rows]
    problems = []
    if len(set(ids)) != len(ids) or len(set(seqs)) != len(seqs):
        problems.append("duplicate attempt id")
    if seqs != sorted(seqs) or (seqs and seqs != list(range(1, len(seqs) + 1))):
        problems.append("attempt sequence has gaps")
    held = [r["id"] for r in rows if r["status"] == "reserved"]
    if held:
        problems.append(f"unsettled reservations: {held}")
    committed = store.committed_usd(job_id)
    budget = dec(store.job(job_id)["budget_usd"])
    if committed > budget:
        problems.append(f"committed USD {committed} exceeds the budget USD {budget}")
    return {"check_id": "ledger_integrity", "control": "ATTEMPT_ID_UNIQUE_AND_RESERVE_MINTED",
            "status": "FAIL" if problems else "PASS",
            "detail": "; ".join(problems) or f"{len(rows)} attempts, ids unique, all settled, USD {committed} of {budget}"}


def exact_copy_match(exact_strings: list, direction: dict, rendered: list | None, logo_present: bool = False) -> dict:
    """Every customer string must be in the copy deck verbatim AND have been drawn, by code, on this exact file
    (the renderer refuses any string its font cannot draw, so a rendered string is a glyph-complete one)."""
    deck = {c["text"] for c in direction.get("copy_deck", [])}
    if rendered is None:
        return {"check_id": "exact_copy_match", "control": "EXACT_COPY_MATCH", "status": "NOT_VERIFIED",
                "detail": "no render record for this file: which strings it carries is unknown"}
    drawn = set(rendered)
    not_in_deck = [s for s in exact_strings if s and s not in deck]
    not_drawn = [s for s in exact_strings if s and s not in drawn]
    # atlas approved_copy_line_not_carried_into_the_cut (UPW1-25): every approved deck line is placed somewhere
    from product.compose import is_logo_line
    logo_lines = {c["text"] for c in direction.get("copy_deck", []) if logo_present and is_logo_line(c)}
    drawn |= logo_lines                     # delivered by the supplied logo file, not by type
    dropped = [t for t in deck if t and t not in drawn and t not in exact_strings]
    problems = ([f"altered or missing in the copy deck: {not_in_deck}"] if not_in_deck else []) + \
               ([f"not drawn on this file: {not_drawn}"] if not_drawn else []) + \
               ([f"approved copy lines not carried into the cut: {dropped}"] if dropped else [])
    return {"check_id": "exact_copy_match", "control": "EXACT_COPY_MATCH", "status": "FAIL" if problems else "PASS",
            "detail": "; ".join(problems) or f"{len(exact_strings)} customer strings drawn verbatim on this file",
            "evidence": {"rendered": sorted(drawn), "required": list(exact_strings)}}


def not_previously_rejected(store: Store, job_id: str, asset_id: str) -> dict:
    sha = store.asset(asset_id)["sha256"]
    rejected = {store.asset(f["asset_id"])["sha256"] for f in store.feedback(job_id) if f["asset_id"] and f["kind"] in ("revision", "reject")}
    hit = sha in rejected
    return {"check_id": "not_previously_rejected", "control": "REJECTED_DESIGN_REUSE", "status": "FAIL" if hit else "PASS",
            "detail": "this exact file was already rejected or sent back by the customer" if hit else "new version"}


def ad_structure(direction: dict, media_kind: str, has_logo: bool) -> dict:
    problems = []
    if not has_logo and not any(c.get("role") in ("brand", "headline", "product_line") for c in direction.get("copy_deck", [])):
        problems.append("no brand mark and no brand line")
    if media_kind == "video" and not any(b.get("product_present") for b in direction.get("beats", [])):
        problems.append("the product appears in no beat")
    return {"check_id": "ad_structure", "control": "AD_STRUCTURE_MINIMUM", "status": "FAIL" if problems else "PASS",
            "detail": "; ".join(problems) or "brand placed; product present"}


def film_checks(path: Path, *, cuts: list, source_sizes: list, delivered: tuple, planned_s: float | None = None,
                card_in_s: float | None = None) -> list:
    rows = []
    if not media.have_ffmpeg():
        for cid, ctl in [("container_edit_lists", "CONTAINER_EDIT_LIST_CHECK"), ("loudness_true_peak", "CODEC_TRUE_PEAK_MARGIN"),
                         ("audio_joins", "AUDIO_LEVEL_CONTINUITY_AT_CUTS"), ("delivery_conformance", "DELIVERY_CONFORMANCE"),
                         ("no_black_frames", "NO_BLACK_OR_DROPPED_PICTURE")]:
            rows.append({"check_id": cid, "control": ctl, "status": "NOT_VERIFIED", "detail": "ffmpeg is not installed on this host"})
        return rows
    from runtime.loop.container import assess_edit_lists
    el = assess_edit_lists(Path(path).read_bytes())
    st = {"PASS": "PASS", "FAIL": "FAIL"}.get(str(el.get("status")), "NOT_VERIFIED")
    rows.append({"check_id": "container_edit_lists", "control": "CONTAINER_EDIT_LIST_CHECK", "status": st,
                 "detail": str(el.get("detail", el))[:300]})
    # what the file IS, against what was ordered
    p = media.probe(path)
    bad = []
    if (p["width"], p["height"]) != tuple(delivered):
        bad.append(f"frame {p['width']}x{p['height']} ≠ ordered {delivered[0]}x{delivered[1]}")
    if p["video_codec"] != "h264" or p["pix_fmt"] != "yuv420p":
        bad.append(f"video {p['video_codec']}/{p['pix_fmt']} (needs h264/yuv420p to play everywhere)")
    if not p["has_audio"] or p["audio_codec"] != "aac":
        bad.append(f"audio {p['audio_codec'] or 'missing'} (needs AAC)")
    fr = media.frame_rates(path)
    if fr and fr["r"] != fr["avg"]:
        bad.append(f"uneven frame timing: nominal {fr['r']} vs average {fr['avg']}")
    if planned_s is not None and abs(p["duration_s"] - planned_s) > 0.25:
        bad.append(f"duration {p['duration_s']:.2f}s ≠ planned {planned_s:.2f}s")
    rows.append({"check_id": "delivery_conformance", "control": "DELIVERY_CONFORMANCE", "status": "FAIL" if bad else "PASS",
                 "detail": "; ".join(bad) or f"{p['width']}x{p['height']} {p['video_codec']}/{p['pix_fmt']} + {p['audio_codec']}, "
                                              f"{p['duration_s']:.2f}s (planned {planned_s})", "evidence": p})
    # picture actually present: no black span anywhere (the fade to the card is a crossfade, never black)
    blacks = media.black_spans(path)
    rows.append({"check_id": "no_black_frames", "control": "NO_BLACK_OR_DROPPED_PICTURE", "status": "FAIL" if blacks else "PASS",
                 "detail": ("black picture at " + ", ".join(f"{a:.2f}–{b:.2f}s" for a, b in blacks)) if blacks
                 else "no black span ≥ 0.2 s in the delivered picture", "evidence": {"black_spans": blacks}})
    # frozen picture inside the filmed part (the end card is meant to be still); a flag for the human, not a verdict
    frozen = [(a, b) for a, b in media.frozen_spans(path, min_s=1.5) if card_in_s is None or a < card_in_s - 0.5]
    if frozen:
        rows.append({"check_id": "frozen_picture", "control": "NO_BLACK_OR_DROPPED_PICTURE", "status": "FLAG", "blocking": False,
                     "detail": "picture frozen at " + ", ".join(f"{a:.2f}–{b:.2f}s" for a, b in frozen)})
    ld = media.loudness(path)
    tp, il = ld["true_peak_dbtp"], ld["integrated_lufs"]
    if tp is None or il is None:
        rows.append({"check_id": "loudness_true_peak", "control": "CODEC_TRUE_PEAK_MARGIN", "status": "NOT_VERIFIED",
                     "detail": "loudness could not be measured", "evidence": ld})
    else:
        ok = tp <= -1.0 and abs(il + 14) <= 2
        rows.append({"check_id": "loudness_true_peak", "control": "CODEC_TRUE_PEAK_MARGIN", "status": "PASS" if ok else "FAIL",
                     "detail": f"integrated {il} LUFS, true peak {tp} dBTP (limits -14±2, ≤ -1.0)", "evidence": ld})
    # A join "hole" is a dip that recovers: the 30 ms after the cut against BOTH the 100 ms before it and the 150–300 ms
    # after it (a cut to a quieter scene is a level change, not a hole). Calibrated on real media, MOKOBARA-ODYSSEY-007
    # DF-10: v1's recorded holes at 3.5 s / 7.5 s measure 10.6 / 8.8 dB; the crossfaded v2 measures ≤ 0.9 dB at all six
    # cuts, and its 7.5 s cut to a quieter shot (−7.3 dB level change) measures −1.3. Limit 6 dB.
    worst, bad, unmeasured, ev = -99.0, [], [], []
    for t in cuts:
        before, after, later = media.rms_db(path, t - 0.10, 0.10), media.rms_db(path, t + 0.005, 0.03), media.rms_db(path, t + 0.15, 0.15)
        if None in (before, after, later):
            unmeasured.append(t)
            continue
        hole = min(before, later) - after
        ev.append({"t": t, "before_db": before, "after_db": after, "later_db": later, "hole_db": round(hole, 1)})
        worst = max(worst, hole)
        if hole > 6.0:
            bad.append(f"{t:.2f}s hole {hole:.1f} dB")
    status = "FAIL" if bad else ("NOT_VERIFIED" if unmeasured or not cuts else "PASS")
    rows.append({"check_id": "audio_joins", "control": "AUDIO_LEVEL_CONTINUITY_AT_CUTS", "status": status, "evidence": {"cuts": ev},
                 "detail": "; ".join(bad) or (f"could not measure the level at {unmeasured}" if unmeasured else
                                              ("no cut positions were supplied" if not cuts else
                                               f"{len(cuts)} cuts, worst dip {worst:.1f} dB (limit 6)"))})
    # disclosure, with a flag when a source is stretched more than 1.5× to reach the delivered frame
    scale = max((max(delivered[0] / w, delivered[1] / h) for w, h in source_sizes if w and h), default=None)
    rows.append({"check_id": "source_resolution", "control": "SOURCE_RESOLUTION_STATED",
                 "status": "NOT_VERIFIED" if scale is None else ("PASS" if scale <= 1.5 else "FLAG"),
                 "blocking": scale is None,
                 "detail": (f"generated sources {sorted(set(map(tuple, source_sizes)))} delivered {delivered[0]}x{delivered[1]} "
                            f"(upscale ×{scale:.2f})") if scale else "source clip sizes unknown",
                 "evidence": {"sources": source_sizes, "delivered": list(delivered), "upscale": scale}})
    return rows


def review_rows(review: dict, *, mandatory_ids: list, media_kind: str, asset_sha256: str | None = None,
                qualified: bool = True) -> list:
    """Turn an independent review into check rows for ONE file. Simulated reviews never PASS; a review that was not
    shown this exact file proves nothing about it; an unanswered question is NOT_VERIFIED, never a pass by silence."""
    simulated = bool(review.get("_simulated")) or "simulated" in (review.get("modalities_evaluated") or [])
    iso = (review.get("_call") or {}).get("isolated", False)
    shown = review.get("_reviewed_sha256")
    unseen = asset_sha256 is not None and shown is not None and asset_sha256 not in shown
    rows = []

    def nv(cid, ctl, why):
        rows.append({"check_id": cid, "control": ctl, "status": "NOT_VERIFIED", "detail": why})

    def row(cid, ctl, answer, ok_values, fail_values, detail):
        if simulated:
            return nv(cid, ctl, "simulated reviewer — nobody looked: " + detail)
        if unseen:
            return nv(cid, ctl, "the reviewer was not shown this exact file")
        if answer in ok_values and not qualified:
            rows.append({"check_id": cid, "control": ctl, "status": "NOT_VERIFIED",
                         "detail": f"the model reviewer says fine, but it is not qualified to pass this — a person confirms: {detail}"})
        elif answer in ok_values:
            rows.append({"check_id": cid, "control": ctl, "status": "PASS", "detail": detail})
        elif answer in fail_values:
            rows.append({"check_id": cid, "control": ctl, "status": "FAIL", "detail": detail})
        else:
            nv(cid, ctl, f"not established by the reviewer ({answer or 'no answer'}): {detail}")

    blockers = [d for d in review.get("defects", []) if d.get("severity") in ("blocker", "major")]
    verdict_ok = "pass" if (iso and review.get("verdict") == "pass" and not blockers) else ("fail" if review.get("verdict") else None)
    row("independent_review", "QA_COVERAGE_ENFORCEMENT", verdict_ok, ("pass",), ("fail",),
        f"verdict {review.get('verdict')}; {len(review.get('defects', []))} defects ({len(blockers)} blocker/major); isolated={iso}")
    vis = {m.get("mandatory_id"): m for m in review.get("mandatory", [])}
    for mid in mandatory_ids:
        m = vis.get(mid) or {}
        row(f"mandatory:{mid}", "MANDATORY_EVENT_VISIBILITY_LJ_LINE", m.get("visible"), ("yes",), ("no", "partial"),
            f"{m.get('visible')}: {m.get('evidence')}" if m else "the reviewer did not address it")
    pf = review.get("product_fidelity") if isinstance(review.get("product_fidelity"), dict) else {}
    pf_ans = "not_faithful" if any(d.get("id", "").startswith("PF") for d in blockers) else pf.get("verdict")
    row("product_fidelity", "PRODUCT_INTACT_AND_FAITHFUL", pf_ans, ("faithful",), ("not_faithful", "product_not_shown"),
        f"{pf.get('verdict')}: {pf.get('evidence', '')}")
    ml = review.get("model_lettering") if isinstance(review.get("model_lettering"), dict) else {}
    row("no_model_lettering", "VIDEO_FRAME_TEXT_HYGIENE", ml.get("present"), ("no",), ("yes",), f"{ml.get('present')}: {ml.get('evidence', '')}")
    so = review.get("subject_obstructed") if isinstance(review.get("subject_obstructed"), dict) else {}
    row("subject_unobstructed", "SUBJECT_OBSTRUCTION", so.get("present"), ("no",), ("yes",), f"{so.get('present')}: {so.get('evidence', '')}")
    if media_kind == "video":
        mods = [m.lower() for m in review.get("modalities_evaluated", [])]
        sp = (review.get("audio") or {}).get("speech_or_singing")
        if not simulated and "audio" not in mods:
            rows.append({"check_id": "audio_reviewed", "control": "AUDIO_REVIEWED_BY_EAR", "status": "NOT_VERIFIED", "blocking": False,
                         "detail": "the model reviewer did not listen; the person's listen (audio_heard_by_person) decides"})
        else:
            row("audio_reviewed", "AUDIO_REVIEWED_BY_EAR", sp, ("no",), ("yes",), f"speech/singing: {sp}; {(review.get('audio') or {}).get('notes', '')}")
        pa = review.get("product_across_shots") if isinstance(review.get("product_across_shots"), dict) else {}
        row("product_across_shots", "PRODUCT_CONTINUITY_ACROSS_SHOTS", pa.get("verdict"), ("consistent", "single_shot"), ("inconsistent",),
            f"{pa.get('verdict')}: {pa.get('evidence', '')}")
        ct = review.get("continuity") if isinstance(review.get("continuity"), dict) else {}
        row("character_continuity", "CHARACTER_CONTINUITY", ct.get("verdict"), ("consistent",), ("inconsistent",),
            f"{ct.get('verdict')}: {ct.get('evidence', '')}")
    return rows


def format_revalidated(store: Store, asset_id: str, fmt: str) -> dict:
    """Each format is its own composition, gated on its own canvas (never a crop of another format's master)."""
    a = store.asset(asset_id)
    lay = (json.loads(a["meta_json"]).get("layout") or {})
    gates = [r for r in store.checks(asset_id) if r["runner"] == "compositor_gates"]
    want = list(media.FORMAT_PX.get(fmt, (0, 0)))
    ok = lay.get("canvas") == want and len(gates) >= 3
    return {"check_id": "format_revalidated", "control": "FORMAT_SPECIFIC_REVALIDATION", "status": "PASS" if ok else "FAIL",
            "detail": f"{fmt}: composed on {lay.get('canvas')} (ordered {want}); {len(gates)} compositor gates on this file"}


# ── world / product truth of the direction (decided by code from the reviewer's structured answers) ──
def truth_blockers(review) -> list:
    """World/product-truth failures, decided by code from the reviewer's structured answers (not by its severity words)."""
    wt = review.get("world_truth") or {}
    out = [f"unsourced product claim: {c.get('claim')} ({c.get('where')})" for c in wt.get("product_claims", []) if c.get("source") == "none"]
    if wt.get("world_specified") == "no":
        out.append(f"the world is not specified: {wt.get('world_note', '')}")
    out += [f"{g.get('prop')} unaccounted for {g.get('between')}: {g.get('gap')}" for g in wt.get("prop_whereabouts_gaps", [])]
    return out



# ── process controls: proven from the ledger, graph and event log of this job ─────────────────
PROCESS_CONTROLS = {"process:paid_preflight": "PAID_PRODUCTION_PREFLIGHT",
                    "process:failures_classified": "TRANSIENT_ERROR_CLASSIFICATION",
                    "process:provider_pool": "PROVIDER_POOL_AVAILABILITY"}
PROCESS_CONTROLS_VIDEO = {"process:take_selection": "TAKE_SELECTION_BEFORE_RETAKE",
                          "process:continuity_chain": "PRODUCT_CONTINUITY_ACROSS_SHOTS",
                          "process:riskiest_first": "RISKIEST_ACTION_QUALIFIED_FIRST",
                          "clips:required_action": "END_STATE_STILL_PLUS_LAST_ACTION_I2V",
                          "clips:end_state": "END_STATE_STILL_PLUS_LAST_ACTION_I2V"}


def process_controls(store: Store, job_id: str, media_kind: str, *, clip_asset_ids: list = ()) -> list:
    job = store.job(job_id)
    atts = store.attempts(job_id)
    prov = [a for a in atts if a["category"] == "provider"]
    rows = []

    def add(cid, ok, detail, evidence=None, nv=False):
        rows.append({"check_id": cid, "control": {**PROCESS_CONTROLS, **PROCESS_CONTROLS_VIDEO}[cid],
                     "status": "NOT_VERIFIED" if nv else ("PASS" if ok else "FAIL"), "detail": detail, "evidence": evidence or {}})

    # 1. no production spend before the customer authorised a budget (preview frames ride the planning allowance)
    # the FIRST authorisation of production spend (the approval), not the latest raise — a later budget increase must not
    # make earlier, properly authorised spend look unauthorised (live film job, 2026-09-23)
    auth_at = job["approved_at"] or job["budget_authorised_at"]
    early = [a["seq"] for a in prov if a["node_id"] != "preview" and (not auth_at or a["reserved_at"] < auth_at)]
    unpriced = [a["seq"] for a in prov if dec(a["reserved_usd"]) <= 0]
    add("process:paid_preflight", bool(job["budget_authorised_by"]) and not early and not unpriced,
        f"{len(prov)} provider attempts; budget authorised by {job['budget_authorised_by'] or 'nobody'} at {auth_at}; "
        f"before authorisation: {early or 'none'}; unpriced: {unpriced or 'none'}")
    # 2. every failure carries a class
    failed = [a for a in atts if a["status"] == "failed"]
    unclassified = [a["seq"] for a in failed if not a["failure_class"]]
    add("process:failures_classified", not unclassified,
        f"{len(failed)} failed attempts, unclassified: {unclassified or 'none'}")
    # 3. no reservation left hanging; a run of ≥3 transient failures on one node must have paused the job
    held = [a["seq"] for a in atts if a["status"] == "reserved"]
    streaks, run = [], {}
    for a in prov:
        k = a["node_id"]
        run[k] = run.get(k, 0) + 1 if (a["status"] == "failed" and a["failure_class"] == "infrastructure_transient") else 0
        if run[k] >= 3:
            streaks.append(k)
    paused = any(json.loads(e["data_json"]).get("to") == "paused_provider" for e in store.events(job_id, ("state",)))
    add("process:provider_pool", not held and (not streaks or paused),
        f"unsettled reservations: {held or 'none'}; transient runs ≥3: {sorted(set(streaks)) or 'none'}"
        + ("; job paused for the provider" if streaks else ""))
    # 4. the recipe that was paid for passed the recipe checker (or the founder overrode it, named and reasoned)
    rc = store.artifact(job_id, "recipe_check") or {}
    over = store.overrides(job_id, "recipe_send_back")
    confirmed = store.overrides(job_id, "confirm_recipe")
    sim_rc = bool((rc.get("written_by") or {}).get("simulated"))
    if not rc:
        rows.append({"check_id": "process:direction_truth", "control": "PRODUCT_AND_WORLD_TRUTH_BEFORE_SPEND", "status": "NOT_VERIFIED",
                     "detail": "no recipe check on record"})
    elif rc.get("verdict_after_code") != "approve" and over:
        rows.append({"check_id": "process:direction_truth", "control": "PRODUCT_AND_WORLD_TRUTH_BEFORE_SPEND", "status": "FLAG",
                     "blocking": False, "detail": f"recipe send-back overridden by {over[-1]['founder_email']}: {over[-1]['reason'][:200]}"})
    elif rc.get("verdict_after_code") != "approve":
        rows.append({"check_id": "process:direction_truth", "control": "PRODUCT_AND_WORLD_TRUTH_BEFORE_SPEND", "status": "FAIL",
                     "detail": "the recipe checker sent the recipe back"})
    elif sim_rc and not confirmed:
        rows.append({"check_id": "process:direction_truth", "control": "PRODUCT_AND_WORLD_TRUTH_BEFORE_SPEND", "status": "NOT_VERIFIED",
                     "detail": "simulated recipe check — nobody judged the recipe"})
    else:
        rows.append({"check_id": "process:direction_truth", "control": "PRODUCT_AND_WORLD_TRUTH_BEFORE_SPEND", "status": "PASS",
                     "detail": f"recipe checker approved; code rules clean ({len(rc.get('code_findings', []))} findings)"
                               + (f"; confirmed by {confirmed[-1]['founder_email']}" if confirmed else "")})
    if media_kind != "video":
        return rows
    shot_nodes = [n for n in store.nodes(job_id) if n["kind"] in ("shot", "frame") and n["status"] != "retired"]
    # 5. a new attempt only after the previous one was tasted and rejected
    rejected = {}
    for e in store.events(job_id, ("take_rejected",)):
        n = json.loads(e["data_json"]).get("node"); rejected[n] = rejected.get(n, 0) + 1
    over = []
    for n in shot_nodes:
        draws = [a for a in prov if a["node_id"] == n["node_id"] and a["status"] == "ok"]
        if max(0, len(draws) - 1) > rejected.get(n["node_id"], 0):
            over.append(n["node_id"])
    add("process:take_selection", not over, f"outputs redrawn without a rejected attempt: {over or 'none'}")
    # 6. risky shots were produced and tasted before any other shot was paid for
    risky = [n["node_id"] for n in shot_nodes if n["kind"] == "shot" and json.loads(n["spec_json"]).get("risky")]
    shot_atts = [a for a in prov if (a["node_id"] or "").startswith(("shot_", "frame_")) and not a["is_repair"]]
    if not risky:
        add("process:riskiest_first", True, "no risky shot in this recipe (every shot reliable on its route)")
    else:
        risky_nodes = set(risky) | {r.replace("shot_", "frame_") for r in risky}
        last_risky = max((a["seq"] for a in shot_atts if a["node_id"] in risky_nodes), default=None)
        early = [a["node_id"] for a in shot_atts if a["node_id"] not in risky_nodes and last_risky and a["seq"] < last_risky]
        add("process:riskiest_first", last_risky is not None and not early,
            f"risky shots {risky}; other shots paid for before the risky ones were done: {sorted(set(early)) or 'none'}")
    # 7. continuity: every shot starts from the master plate or the previous shot's end frame (the production log)
    log = store.artifact(job_id, "production_log") or {"entries": []}
    frames = [e for e in log["entries"] if e["node"].startswith("frame_")]
    broken = [e["node"] for e in frames if e["source_kind"] not in ("master_plate", "previous_shot_end")]
    add("process:continuity_chain", bool(frames) and not broken,
        f"{len(frames)} shots; built from the master plate or the previous end frame; broken: {broken or 'none'}")
    # 8. the small taster saw each selected (generated) clip reach its action and end state
    for cid, key in (("clips:required_action", "required_action_occurred"), ("clips:end_state", "end_state_reached")):
        ans = {}
        for aid in clip_asset_ids:
            m = json.loads(store.asset(aid)["meta_json"])
            if m.get("code_motion"):
                continue
            ans[aid] = (m.get("inspection") or {}).get(key)
        vals = set(ans.values())
        if "no" in vals:
            add(cid, False, f"the small taster reported NO on {[k for k, v in ans.items() if v == 'no']}", ans)
        elif vals <= {"yes"}:
            add(cid, True, f"{len(ans)} generated clips: yes" if ans else "no generated clip in this cut (code motion only)", ans)
        else:
            add(cid, False, f"not established on {[k for k, v in ans.items() if v != 'yes']} ({sorted(map(str, vals))})", ans, nv=True)
    return rows


# ── the gateway ────────────────────────────────────────────────────────────────────────────────
def gateway(store: Store, job_id: str, asset_id: str, required: dict) -> dict:
    """The door guard. Nothing leaves with a failed or missing check; only the founder can override, with a reason.
    A waiver or a person-performed result counts only when a founder override row backs it (authority.py)."""
    from product.authority import is_founder_user
    ovs = store.overrides(job_id)
    backed = {(o["kind"], o["target"]): o for o in ovs if is_founder_user(store, o["founder_user_id"])}
    rows = {r["check_id"]: r for r in store.checks(asset_id)}
    waived, ignored = {}, []
    for w in store.waivers(asset_id):
        o = backed.get(("check_waiver", f"{asset_id}:{w['check_id']}"))
        if o and o["founder_user_id"] == w["by_user"]:
            waived[w["check_id"]] = {"by_user": o["founder_email"], "reason": o["reason"]}
        else:
            ignored.append({"check_id": w["check_id"], "by": w["by_user"], "why": "not made by the signed-in founder — ignored"})
    sha = store.asset(asset_id)["sha256"]
    blocking, table = [], []
    for cid in sorted(set(required) | set(rows)):
        r = rows.get(cid)
        status = r["status"] if r else "NOT_VERIFIED"
        detail = r["detail"] if r else "no result recorded for this exact file"
        if r is not None and r["asset_sha256"] != sha:
            status = "NOT_VERIFIED"           # a result for another version of the file proves nothing about this one
        if r is not None and (r["runner"].startswith("person:") or r["runner"].startswith("founder:")) \
                and ("confirm", f"{asset_id}:{cid}") not in backed:
            status, detail = "NOT_VERIFIED", f"a person-recorded result not confirmed by the founder is ignored ({r['runner']})"
        is_blocking = (r["blocking"] if r else True) and status in ("FAIL", "NOT_VERIFIED")
        w = waived.get(cid) if cid not in NON_WAIVABLE else None
        entry = {"check_id": cid, "control": required.get(cid) or (r["control_ids"] if r else ""), "status": status,
                 "detail": detail, "runner": r["runner"] if r else None,
                 "waived_by": w["by_user"] if w else None, "waiver_reason": w["reason"] if w else None}
        table.append(entry)
        if is_blocking and not w:
            blocking.append(entry)
    shown = [{"kind": o["kind"], "target": o["target"], "by": o["founder_email"], "reason": o["reason"], "utc": o["created"]}
             for o in ovs if is_founder_user(store, o["founder_user_id"])]
    return {"asset_id": asset_id, "sha256": sha, "ready": not blocking, "blocking": blocking, "table": table,
            "waived": [e for e in table if e["waived_by"]], "ignored_waivers": ignored, "founder_overrides": shown}
