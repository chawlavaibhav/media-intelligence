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


def required_checks(media_kind: str, *, mandatory_ids: list, has_copy: bool, has_logo: bool, super_ids: list = ()) -> dict:
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
    if media_kind == "image":
        req["disjoint"] = "ELEMENT_DISJOINTNESS"
        req["hero_visible"] = "HERO_VISIBLE"
        if has_logo:
            req["bounds:logo"] = "TEXT_BOUNDS_GATE"
    else:
        req.update({"container_edit_lists": "CONTAINER_EDIT_LIST_CHECK", "loudness_true_peak": "CODEC_TRUE_PEAK_MARGIN",
                    "audio_joins": "AUDIO_LEVEL_CONTINUITY_AT_CUTS", "audio_reviewed": "AUDIO_REVIEWED_BY_EAR",
                    "source_resolution": "SOURCE_RESOLUTION_STATED", "character_continuity": "CHARACTER_CONTINUITY",
                    "end_card:disjoint": "ELEMENT_DISJOINTNESS", "end_card:brand_colour:end_card": "BRAND_COLOUR_ON_RENDERED_FRAME",
                    "clips:no_in_model_cut": "IN_MODEL_HARD_CUT"})
        for s in super_ids:
            req[f"super:{s}:contrast:super"] = "CONTRAST_GATE"
    return req


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


def exact_copy_match(exact_strings: list, direction: dict) -> dict:
    deck = {c["text"] for c in direction.get("copy_deck", [])}
    missing = [s for s in exact_strings if s and s not in deck]
    return {"check_id": "exact_copy_match", "control": "EXACT_COPY_MATCH", "status": "FAIL" if missing else "PASS",
            "detail": (f"missing or altered: {missing}" if missing else f"{len(exact_strings)} customer strings set verbatim")}


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


def film_checks(path: Path, *, cuts: list, source_sizes: list, delivered: tuple) -> list:
    rows = []
    if not media.have_ffmpeg():
        for cid, ctl in [("container_edit_lists", "CONTAINER_EDIT_LIST_CHECK"), ("loudness_true_peak", "CODEC_TRUE_PEAK_MARGIN"),
                         ("audio_joins", "AUDIO_LEVEL_CONTINUITY_AT_CUTS")]:
            rows.append({"check_id": cid, "control": ctl, "status": "NOT_VERIFIED", "detail": "ffmpeg is not installed on this host"})
    else:
        from runtime.loop.container import assess_edit_lists
        el = assess_edit_lists(Path(path).read_bytes())
        st = {"PASS": "PASS", "FAIL": "FAIL"}.get(str(el.get("status")), "NOT_VERIFIED")
        rows.append({"check_id": "container_edit_lists", "control": "CONTAINER_EDIT_LIST_CHECK", "status": st,
                     "detail": str(el.get("detail", el))[:300]})
        ld = media.loudness(path)
        tp, il = ld["true_peak_dbtp"], ld["integrated_lufs"]
        ok = tp is not None and il is not None and tp <= -1.0 and abs(il + 14) <= 2
        rows.append({"check_id": "loudness_true_peak", "control": "CODEC_TRUE_PEAK_MARGIN", "status": "PASS" if ok else "FAIL",
                     "detail": f"integrated {il} LUFS, true peak {tp} dBTP (limits -14±2, ≤ -1.0)", "evidence": ld})
        worst, bad = 0.0, []
        for t in cuts:
            before, after = media.rms_db(path, t - 0.05, 0.05), media.rms_db(path, t, 0.05)
            if before is None or after is None:
                continue
            drop = before - after
            worst = max(worst, drop)
            if drop > 12.0:
                bad.append(f"{t:.2f}s drop {drop:.1f} dB")
        rows.append({"check_id": "audio_joins", "control": "AUDIO_LEVEL_CONTINUITY_AT_CUTS", "status": "FAIL" if bad else "PASS",
                     "detail": "; ".join(bad) or f"{len(cuts)} cuts, worst level drop {worst:.1f} dB (limit 12)"})
    rows.append({"check_id": "source_resolution", "control": "SOURCE_RESOLUTION_STATED", "status": "PASS",
                 "detail": f"generated sources {sorted(set(map(tuple, source_sizes)))} delivered {delivered[0]}x{delivered[1]}",
                 "evidence": {"sources": source_sizes, "delivered": list(delivered)}})
    return rows


def review_rows(review: dict, *, mandatory_ids: list, media_kind: str) -> list:
    """Turn an independent review into check rows. Simulated reviews never PASS."""
    simulated = bool(review.get("_simulated")) or "simulated" in (review.get("modalities_evaluated") or [])
    iso = (review.get("_call") or {}).get("isolated", False)
    rows = []

    def row(cid, ctl, ok, detail, flag=False):
        if simulated:
            rows.append({"check_id": cid, "control": ctl, "status": "NOT_VERIFIED", "detail": "simulated reviewer — nobody looked: " + detail})
        else:
            rows.append({"check_id": cid, "control": ctl, "status": ("PASS" if ok else ("FLAG" if flag else "FAIL")), "detail": detail})

    blockers = [d for d in review.get("defects", []) if d.get("severity") in ("blocker", "major")]
    row("independent_review", "QA_COVERAGE_ENFORCEMENT", iso and review.get("verdict") == "pass" and not blockers,
        f"verdict {review.get('verdict')}; {len(review.get('defects', []))} defects ({len(blockers)} blocker/major); isolated={iso}")
    vis = {m.get("mandatory_id"): m for m in review.get("mandatory", [])}
    for mid in mandatory_ids:
        m = vis.get(mid)
        if m is None or m.get("visible") == "cannot_determine":
            rows.append({"check_id": f"mandatory:{mid}", "control": "MANDATORY_EVENT_VISIBILITY_LJ_LINE", "status": "NOT_VERIFIED",
                         "detail": "the reviewer did not establish it" if m is None else f"cannot determine: {m.get('evidence')}"})
        else:
            row(f"mandatory:{mid}", "MANDATORY_EVENT_VISIBILITY_LJ_LINE", m.get("visible") == "yes", f"{m.get('visible')}: {m.get('evidence')}")
    pf = (review.get("product_fidelity") or "").lower()
    row("product_fidelity", "PRODUCT_INTACT_AND_FAITHFUL", not any(d.get("id", "").startswith("PF") for d in blockers)
        and not any(w in pf for w in ("not faithful", "wrong", "deform", "warp", "different product")), review.get("product_fidelity", ""))
    lettering = [d for d in review.get("defects", []) if "letter" in (d.get("description", "") + d.get("id", "")).lower()]
    row("no_model_lettering", "VIDEO_FRAME_TEXT_HYGIENE", not lettering, "no model-drawn lettering reported" if not lettering else lettering[0]["description"])
    if media_kind == "video":
        mods = [m.lower() for m in review.get("modalities_evaluated", [])]
        sp = (review.get("audio") or {}).get("speech_or_singing")
        if "audio" not in mods or sp in (None, "cannot_determine", "n/a"):
            rows.append({"check_id": "audio_reviewed", "control": "AUDIO_REVIEWED_BY_EAR", "status": "NOT_VERIFIED",
                         "detail": "the reviewer did not listen to the audio; a human listen is required"})
        else:
            row("audio_reviewed", "AUDIO_REVIEWED_BY_EAR", sp == "no", f"speech/singing: {sp}; {(review.get('audio') or {}).get('notes', '')}")
        cont = (review.get("continuity") or "").lower()
        row("character_continuity", "CHARACTER_CONTINUITY", not any(w in cont for w in ("drift", "inconsistent", "different person", "changes")),
            review.get("continuity", ""))
    return rows


# ── the gateway ────────────────────────────────────────────────────────────────────────────────
def gateway(store: Store, job_id: str, asset_id: str, required: dict) -> dict:
    rows = {r["check_id"]: r for r in store.checks(asset_id)}
    waived = {w["check_id"]: w for w in store.waivers(asset_id)}
    sha = store.asset(asset_id)["sha256"]
    blocking, table = [], []
    for cid in sorted(set(required) | set(rows)):
        r = rows.get(cid)
        status = r["status"] if r else "NOT_VERIFIED"
        if r is not None and r["asset_sha256"] != sha:
            status = "NOT_VERIFIED"           # a result for another version of the file proves nothing about this one
        is_blocking = (r["blocking"] if r else True) and status in ("FAIL", "NOT_VERIFIED")
        w = waived.get(cid)
        entry = {"check_id": cid, "control": required.get(cid) or (r["control_ids"] if r else ""), "status": status,
                 "detail": r["detail"] if r else "no result recorded for this exact file", "runner": r["runner"] if r else None,
                 "waived_by": w["by_user"] if w else None, "waiver_reason": w["reason"] if w else None}
        table.append(entry)
        if is_blocking and not w:
            blocking.append(entry)
    return {"asset_id": asset_id, "sha256": sha, "ready": not blocking, "blocking": blocking, "table": table,
            "waived": [e for e in table if e["waived_by"]]}
