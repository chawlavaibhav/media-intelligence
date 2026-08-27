#!/usr/bin/env python3
"""Rasterise the Latin pack locally and decide perceptibility on DECODED PIXELS.

WHY PIXELS, AND NOTHING ELSE

    A 'mismatch' that cannot be seen is not a hard item. It is a way to mark a judge WRONG for
    correctly reporting what was actually drawn. The Devanagari battery established the rule the
    hard way and it carries over unchanged:

        a mismatch must differ after NFC  *and*  differ in its decoded RGBA8 raster.

    Neither test alone is sound. Unicode difference is too weak (a zero-width space draws nothing).
    Encoded PNG bytes are too strong (one picture written three ways gives three file hashes).

WHAT THIS FILE DOES AND DOES NOT CLAIM

    It performs the MECHANICAL half of the perceptibility sanity pass, at zero spend, with no
    network call: it renders both strings of every mismatch item with a pinned font FILE and
    compares their pixel fingerprints.

    It does NOT perform the HUMAN half — 'would a person reading a real commercial surface notice,
    and is this a usable surface at all?'. That needs a person. This worker cannot honestly do it,
    so the sheet is emitted UNFILLED and the record marks the review outstanding. EVAL-012 is
    explicit that fabricating it is worse than declaring it missing.

WHERE THE IMAGES GO

    `build/` beside this file, gitignored, exactly as the Devanagari battery treats its own
    images: fully reproducible from committed code plus a pinned font, so committing the bytes
    would add weight without adding truth. The committed artifacts are the manifest, its
    fingerprint, and this record.

    The renderer refuses to write anywhere inside the frozen Devanagari battery.

READ-ONLY REUSE OF THE BATTERY'S RENDERING CODE

    `devtext.render` and `pngraster.pixel_fingerprint` are imported read-only from
    `eval/battery/devanagari-exactness/`. They are the project's existing, tested answer to
    'is this difference actually on the page', and the cross-branch validation script already
    explains why a second copy of somebody else's contract is worse than a read-only reference:
    the copy drifts, and then you are proving compliance against a stale snapshot.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKAGE_ROOT = HERE.parent
REPO_ROOT = PACKAGE_ROOT.parent.parent
BATTERY = REPO_ROOT / "eval" / "battery" / "devanagari-exactness"

# Read-only import of the battery's rendering + raster-comparison code. Nothing is written there.
sys.path.insert(0, str(BATTERY))
from devtext import RenderSpec, render  # noqa: E402
from pngraster import pixel_fingerprint  # noqa: E402

PACK = HERE / "latin-pack-v1.jsonl"
FINGERPRINT = HERE / "latin-pack-v1.sha256"
DEFAULT_BUILD_DIR = HERE / "build"
MECHANICAL_RECORD = HERE / "perceptibility-mechanical.json"
HUMAN_SHEET = HERE / "perceptibility-review.csv"

# Pinned by FILE, not by family name, so there is no silent fallback face. The sha256 of the
# actual bytes is recorded with every run; a different font asset is detectable, not arguable.
DEFAULT_FONT_FILE = "/System/Library/Fonts/Supplemental/Arial.ttf"
DEFAULT_POINT_SIZE = 64


class ForbiddenOutputPath(RuntimeError):
    """The requested output directory is inside a protected frozen artifact."""


def _reject_protected_path(path: Path) -> None:
    path = path.resolve()
    battery = BATTERY.resolve()
    if path == battery or battery in path.parents:
        raise ForbiddenOutputPath(
            f"refusing to write {path} — it resolves inside the frozen Devanagari battery at "
            f"{battery}. EMP-001 reads that battery and never writes to it.")


def spec_for(font_file: str = DEFAULT_FONT_FILE, point_size: int = DEFAULT_POINT_SIZE) -> RenderSpec:
    return RenderSpec(font_file=font_file, face_index=0, point_size=point_size)


def is_visibly_different(a: str, b: str, work_dir: Path,
                         spec: RenderSpec | None = None) -> bool:
    """True iff the two strings draw DIFFERENT pictures with the pinned font.

    This is the whole perceptibility gate. It renders and compares decoded RGBA8 rasters — not
    codepoints, not glyph ids, not encoded PNG bytes.
    """
    spec = spec or spec_for()
    work_dir = Path(work_dir)
    _reject_protected_path(work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)

    fps = []
    for label, text in (("a", a), ("b", b)):
        # Name by content hash so two calls with the same string reuse one deterministic file.
        name = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
        fps.append(pixel_fingerprint(render(text, work_dir / f"{name}.png", spec)))
    return fps[0] != fps[1]


def _font_provenance(spec: RenderSpec) -> dict:
    font = Path(spec.font_file)
    return {
        "tool": "hb-view",
        "font_file": str(font),
        "font_sha256": hashlib.sha256(font.read_bytes()).hexdigest(),
        "face_index": spec.face_index,
        "point_size": spec.point_size,
        "note": ("Pinned by FILE, not family name: there is no fallback face. The images are a "
                 "reproducible build product; the committed artifacts are the manifest, its "
                 "fingerprint and this record."),
    }


def load_pack() -> list[dict]:
    return [json.loads(x) for x in PACK.read_text(encoding="utf-8").splitlines() if x.strip()]


def render_pack(out_dir: Path | str = DEFAULT_BUILD_DIR,
                font_file: str = DEFAULT_FONT_FILE,
                point_size: int = DEFAULT_POINT_SIZE,
                write_records: bool = True) -> dict:
    """Render every item, run the pixel gate over every mismatch, write both records."""
    out_dir = Path(out_dir)
    _reject_protected_path(out_dir)
    spec = spec_for(font_file, point_size)
    images = out_dir / "images"
    images.mkdir(parents=True, exist_ok=True)

    rows = load_pack()
    by_id = {}
    for row in rows:
        path = render(row["rendered_string"], images / f"{row['item_id']}.png", spec)
        by_id[row["item_id"]] = {
            "path": path,
            "file_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "pixel_fingerprint": pixel_fingerprint(path),
        }

    # The match item on the same base string is what the mismatch is compared against: it is the
    # picture of the CORRECT text, rendered by the same pinned font at the same size.
    match_fp = {r["base_id"]: by_id[r["item_id"]]["pixel_fingerprint"]
                for r in rows if r["expected"] == "match"}

    items = []
    for row in rows:
        if row["expected"] != "mismatch":
            continue
        mine = by_id[row["item_id"]]
        items.append({
            "item_id": row["item_id"],
            "base_id": row["base_id"],
            "failure_class": row["failure_class"],
            "edit_detail": row["edit_detail"],
            "differs_after_nfc": (unicodedata.normalize("NFC", row["rendered_string"])
                                  != unicodedata.normalize("NFC", row["target_string"])),
            "visible_in_decoded_pixels": mine["pixel_fingerprint"] != match_fp[row["base_id"]],
            "target_pixel_fingerprint": match_fp[row["base_id"]],
            "rendered_pixel_fingerprint": mine["pixel_fingerprint"],
            "rendered_image_file_sha256": mine["file_sha256"],
        })
    items.sort(key=lambda i: i["item_id"])

    invisible = [i["item_id"] for i in items if not i["visible_in_decoded_pixels"]]

    record = {
        "record": "latin-pack-v1-perceptibility",
        "pack_sha256": FINGERPRINT.read_text(encoding="utf-8").split()[0],
        "mechanical_gate": {
            "rule": "a mismatch must differ after NFC AND in its decoded RGBA8 raster",
            "decided_on": "decoded_pixels",
            "why_not_encoded_png_bytes": ("one picture written three ways has three file hashes "
                                          "and one appearance"),
            "why_not_codepoints_alone": ("a zero-width space differs in codepoints and draws "
                                         "nothing"),
        },
        "render_provenance": _font_provenance(spec),
        "items": items,
        "mismatches_checked": len(items),
        "mismatches_visible": len(items) - len(invisible),
        "mismatches_invisible": invisible,
        "human_perceptibility_review": {
            "status": "OUTSTANDING_ZERO_SPEND_HUMAN_PREREQUISITE",
            "performed_by_this_worker": False,
            "sheet": str(HUMAN_SHEET.relative_to(REPO_ROOT)),
            "what_it_must_answer": [
                "visible_difference — would a person reading this surface notice the corruption?",
                "usable_surface — is this a plausible commercial surface to test a judge on?",
            ],
            "why_not_done_here": ("EVAL-012 forbids fabricating a human review. The mechanical "
                                 "pixel gate above proves a difference is ON THE PAGE; it cannot "
                                 "prove a person would notice it, and the two are not the same "
                                 "claim."),
            "if_any_item_is_rejected": ("correct the base list in build_latin_pack.py and rebuild "
                                        "the WHOLE manifest before re-freezing the fingerprint. "
                                        "Never patch a single reviewed row in place."),
        },
        "external_calls": 0,
        "spend_usd": "0",
    }

    if write_records:
        MECHANICAL_RECORD.write_text(
            json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8")
        _write_human_sheet(rows)

    return record


def _write_human_sheet(rows: list[dict]) -> Path:
    """Emit the review sheet UNFILLED. Every verdict column is blank, by design."""
    with HUMAN_SHEET.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["item_id", "visible_difference", "usable_surface", "reviewer_note"])
        for r in sorted(rows, key=lambda x: x["item_id"]):
            w.writerow([r["item_id"], "", "", ""])
    return HUMAN_SHEET


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Render the Latin pack and run the pixel gate.")
    ap.add_argument("--out-dir", default=str(DEFAULT_BUILD_DIR))
    ap.add_argument("--font-file", default=DEFAULT_FONT_FILE)
    ap.add_argument("--point-size", type=int, default=DEFAULT_POINT_SIZE)
    a = ap.parse_args(argv)
    rec = render_pack(Path(a.out_dir), a.font_file, a.point_size)
    print(json.dumps({k: v for k, v in rec.items() if k != "items"},
                     ensure_ascii=False, indent=2, sort_keys=True))
    return 1 if rec["mismatches_invisible"] else 0


if __name__ == "__main__":
    sys.exit(main())
