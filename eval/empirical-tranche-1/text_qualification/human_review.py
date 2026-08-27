"""Canonical validator for the EMP-001 Latin human perceptibility review.

The human review is evidence, not a generated build artifact.  A renderer may create an empty
sheet before review, but once a real reviewer has answered it no rebuild may silently erase those
answers.

Acceptance is the frozen Task-2 rule:
- every one of the 96 items must have usable_surface=yes;
- every mismatch item must have visible_difference=yes;
- match items do not have a corruption, so visible_difference may be blank (or n/a).

The reviewer note also binds the answers to the exact frozen Latin-pack fingerprint.  If the pack
changes, the old review becomes stale and the gate closes.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACK = HERE / "latin-pack-v1.jsonl"
PACK_FINGERPRINT = HERE / "latin-pack-v1.sha256"
HUMAN_SHEET = HERE / "perceptibility-review.csv"


def pack_sha256() -> str:
    return PACK_FINGERPRINT.read_text(encoding="utf-8").split()[0]


def load_pack() -> list[dict]:
    return [json.loads(x) for x in PACK.read_text(encoding="utf-8").splitlines() if x.strip()]


def review_status(path: Path | str | None = None) -> dict:
    path = Path(path) if path else HUMAN_SHEET
    pack = load_pack()
    expected_ids = [r["item_id"] for r in sorted(pack, key=lambda x: x["item_id"])]
    mismatch_ids = {r["item_id"] for r in pack if r["expected"] == "mismatch"}
    expected_sha = pack_sha256()

    base = {
        "path": str(path),
        "pack_sha256": expected_sha,
        "items_expected": len(expected_ids),
        "mismatches_expected": len(mismatch_ids),
    }
    if not path.exists():
        return {**base, "ok": False, "status": "MISSING_HUMAN_REVIEW",
                "reason": "review sheet does not exist"}

    try:
        with path.open(encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
    except Exception as exc:
        return {**base, "ok": False, "status": "INVALID_HUMAN_REVIEW",
                "reason": f"cannot read review sheet: {exc}"}

    required = {"item_id", "visible_difference", "usable_surface", "reviewer_note"}
    if not rows:
        return {**base, "ok": False, "status": "OUTSTANDING_HUMAN_REVIEW",
                "reason": "review sheet has no rows"}
    if not required.issubset(rows[0].keys()):
        return {**base, "ok": False, "status": "INVALID_HUMAN_REVIEW",
                "reason": "review sheet is missing required columns"}

    ids = [r.get("item_id", "").strip() for r in rows]
    if len(ids) != len(set(ids)) or sorted(ids) != expected_ids:
        return {**base, "ok": False, "status": "STALE_OR_INVALID_HUMAN_REVIEW",
                "reason": "review item ids do not exactly match the frozen Latin pack"}

    usable_yes = sum((r.get("usable_surface") or "").strip().lower() == "yes" for r in rows)
    mismatch_visible_yes = sum(
        (r.get("visible_difference") or "").strip().lower() == "yes"
        for r in rows if r["item_id"] in mismatch_ids
    )
    rejected = [
        r["item_id"] for r in rows
        if (r.get("usable_surface") or "").strip().lower() == "no"
        or (r["item_id"] in mismatch_ids
            and (r.get("visible_difference") or "").strip().lower() == "no")
    ]

    # Bind the human answers to the exact pack reviewed.  The note is free-form, but every row in
    # the durable reviewed sheet carries this machine-checkable token.
    binding = f"pack_sha256={expected_sha}"
    bound_rows = sum(binding in (r.get("reviewer_note") or "") for r in rows)

    ok = (usable_yes == len(expected_ids)
          and mismatch_visible_yes == len(mismatch_ids)
          and bound_rows == len(expected_ids)
          and not rejected)

    if ok:
        status = "COMPLETE_HUMAN_REVIEW"
        reason = None
    elif usable_yes == 0 and mismatch_visible_yes == 0:
        status = "OUTSTANDING_HUMAN_REVIEW"
        reason = "human verdicts are not filled"
    else:
        status = "STALE_OR_INVALID_HUMAN_REVIEW"
        reason = "review is incomplete, rejected, or not bound to the current pack fingerprint"

    return {
        **base,
        "ok": ok,
        "status": status,
        "reason": reason,
        "items_reviewed": len(rows),
        "usable_yes": usable_yes,
        "mismatch_visible_yes": mismatch_visible_yes,
        "bound_rows": bound_rows,
        "rejected_items": rejected,
    }


def resolved(path: Path | str | None = None) -> bool:
    return bool(review_status(path)["ok"])
