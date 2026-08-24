#!/usr/bin/env python3
"""
Build the Devanagari exactness battery: deterministic, balanced, visibly-valid items.

THE QUESTION THE BATTERY ASKS
    Not "can this model read Hindi?" but:
    **"Does this evaluator report a match when the visible text differs from the requested
    target?"** That silent yes — the false pass — is the failure that reaches a customer with a
    passing grade attached.

GROUND TRUTH BY CONSTRUCTION
    Every image is rendered locally from a string we chose. What the image says is therefore known
    without any annotation, any reader, and any dataset label. This is the property EVAL-003's
    photographed pack could not have.

DIRECTION MATTERS MORE THAN IT LOOKS
    A mismatch can be built two ways, and they do not measure the same thing:

      corrupt_image  render(perturbed), ask about the ORIGINAL word.
                     The model sees malformed text and is handed a plausible real word. Every
                     pull of its language prior says "yes, that's the word." This is where silent
                     autocorrection actually happens, so it is the primary stratum.

      corrupt_target render(original), ask about the PERTURBED string.
                     The model sees clean text and is handed an odd string. Much easier. Retained
                     as a control: a checker that fails here is failing basic comparison, not
                     resisting autocorrection.

    Both are generated and reported separately. Collapsing them would let a good score on the easy
    direction hide blindness on the hard one.

NO ITEM SHIPS UNVERIFIED
    Every mismatch passes devtext.is_valid_mismatch(): the strings must differ after NFC *and*
    the shaped glyphs must differ. Rejections are written to the manifest with their reason, not
    silently dropped.

No network. No model. No spend. Rendering is local.
"""
from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import perturb  # noqa: E402
from devtext import (RenderSpec, has_devanagari, is_valid_mismatch, nfc, render,  # noqa: E402
                     sha256_file, shape)

# Fraction of mismatch items built in the hard direction (see module docstring).
CORRUPT_IMAGE_SHARE = 0.7
# No single base word may back more than this many items, so one word cannot dominate.
MAX_ITEMS_PER_BASE = 4
# No single failure class may exceed this share of the mismatch stratum.
MAX_CLASS_SHARE = 0.12
# Share of the mismatch stratum reserved for visibly-broken clusters. Deliberately small: they
# are a useful floor (a checker that misses these is unusable) but they do not test resistance to
# autocorrection, so they must not dilute the hard stratum.
IMPLAUSIBLE_SHARE = 0.15


def load_base_strings(path: Path | None, eval003_manifest: Path | None) -> list[dict]:
    """Base words, with provenance recorded per string."""
    if path and path.exists():
        raw = json.loads(path.read_text(encoding="utf-8"))
        return [{"text": nfc(r["text"] if isinstance(r, dict) else r),
                 "provenance": (r.get("provenance") if isinstance(r, dict) else None)
                               or f"base-list:{path.name}"}
                for r in raw]
    if eval003_manifest and eval003_manifest.exists():
        seen, out = set(), []
        for line in eval003_manifest.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            t = nfc(r.get("source_provided_transcription", ""))
            if t and has_devanagari(t) and t not in seen:
                seen.add(t)
                out.append({
                    "text": t,
                    # Reused as a LEXICAL ITEM only. EVAL-003 established these annotations are
                    # unsafe as ground truth about what a photograph shows — irrelevant here,
                    # because we render the string ourselves. What still needs confirming is that
                    # each string is a real, well-formed Hindi word: see NATIVE-VALIDATION.md.
                    "provenance": "eval003_hindi_pack_transcription:lexical_reuse_only",
                })
        return sorted(out, key=lambda r: r["text"])
    raise SystemExit("no base strings: pass --base-strings or ensure the EVAL-003 manifest exists")


def build(base_strings, spec: RenderSpec, target_total: int, seed: int, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    img_dir = out_dir / "images"
    img_dir.mkdir(exist_ok=True)

    # Every match item must be a DISTINCT rendered word: repeating a word produces byte-identical
    # images, wastes budget, and hands a checker a repetition cue. The battery therefore caps at
    # the number of distinct base words and reports the cap rather than padding to a requested size.
    distinct_bases = len({b["text"] for b in base_strings})
    n_match = min(target_total // 2, distinct_bases)
    n_mismatch = n_match                      # held at 50/50 so "always fail" scores 50%
    capped = n_match < target_total // 2
    max_per_class = max(1, int(n_mismatch * MAX_CLASS_SHARE))
    max_implausible = max(1, int(n_mismatch * IMPLAUSIBLE_SHARE))

    # ---- enumerate and screen every candidate --------------------------------------------
    valid: list[dict] = []
    rejected: list[dict] = []
    for b in base_strings:
        base = b["text"]
        for c in perturb.all_candidates(base):
            v = is_valid_mismatch(base, c.text, spec.font_file)
            rec = {
                "base": base, "perturbed": c.text, "failure_class": c.failure_class,
                "group": perturb.CLASS_TO_GROUP.get(c.failure_class, "other"),
                "position": c.position, "detail": c.detail,
                "plausibility": c.plausibility,
            }
            if v.valid:
                valid.append(rec)
            else:
                rejected.append({**rec, "rejection_reason": v.reason})

    # ---- deterministic balanced selection -------------------------------------------------
    # Ordering is a stable sort, not an RNG: the same repository state and seed always produce
    # the same battery. `seed` only rotates the deterministic order so a different-but-still-
    # reproducible sample can be drawn if the Controller wants one.
    # Plausible corruptions sort first within each class: they are the ones that actually test
    # whether a checker autocorrects. Implausible ones remain reachable, under a quota.
    valid.sort(key=lambda r: (r["failure_class"], r["plausibility"] != "plausible",
                              r["base"], r["position"], r["perturbed"]))
    by_class: dict[str, list[dict]] = collections.defaultdict(list)
    for r in valid:
        by_class[r["failure_class"]].append(r)
    for cls in by_class:
        rot = seed % max(1, len(by_class[cls]))
        by_class[cls] = by_class[cls][rot:] + by_class[cls][:rot]

    per_base = collections.Counter()
    per_class = collections.Counter()
    n_implausible = 0
    chosen: list[dict] = []
    # Round-robin across classes so coverage is broad before it is deep.
    classes = sorted(by_class)
    idx = {c: 0 for c in classes}
    while len(chosen) < n_mismatch:
        progressed = False
        for cls in classes:
            if len(chosen) >= n_mismatch:
                break
            if per_class[cls] >= max_per_class:
                continue
            lst = by_class[cls]
            while idx[cls] < len(lst):
                cand = lst[idx[cls]]; idx[cls] += 1
                if per_base[cand["base"]] >= MAX_ITEMS_PER_BASE:
                    continue
                if cand["plausibility"] != "plausible":
                    if n_implausible >= max_implausible:
                        continue
                    n_implausible += 1
                chosen.append(cand); per_base[cand["base"]] += 1; per_class[cls] += 1
                progressed = True
                break
        if not progressed:
            break

    # ---- assign direction deterministically ------------------------------------------------
    n_hard = round(len(chosen) * CORRUPT_IMAGE_SHARE)
    for i, r in enumerate(chosen):
        r["direction"] = "corrupt_image" if i < n_hard else "corrupt_target"

    # ---- match items, drawn from the SAME base words ---------------------------------------
    # Deliberate: a base word that appears as a mismatch also appears as a match, so word
    # identity carries no signal about the expected answer and "recognise the word, answer from
    # the lexicon" is not a viable shortcut.
    mismatch_bases = [r["base"] for r in chosen]
    ordered_bases = list(dict.fromkeys(mismatch_bases)) + \
                    [b["text"] for b in base_strings if b["text"] not in set(mismatch_bases)]
    match_bases = ordered_bases[:n_match]      # distinct words only; never cycled

    prov = {b["text"]: b["provenance"] for b in base_strings}
    items = []
    # One rendered string -> one image file. A clean word is deliberately reused across a match
    # item and a corrupt_target mismatch item: same pixels, two different targets, opposite
    # expected answers. That pairing is a feature — it isolates the target as the only variable,
    # so a checker cannot be right by judging the image alone. Sharing the file makes the pairing
    # explicit instead of hiding it behind duplicate bytes.
    rendered_to_file: dict[str, Path] = {}

    def add_item(idx_: int, rendered: str, target: str, expected: str, meta: dict):
        stem = f"dx-{idx_:04d}"
        if rendered in rendered_to_file:
            png = rendered_to_file[rendered]
        else:
            png = img_dir / f"img-{len(rendered_to_file):04d}.png"
            render(rendered, png, spec)
            rendered_to_file[rendered] = png
        items.append({
            "item_id": stem,
            "rendered_string": rendered,      # what the image provably contains
            "target_string": target,          # what the checker is asked about
            "expected_verdict": expected,     # match | mismatch — known by construction
            "image_file": f"images/{png.name}",
            "image_sha256": sha256_file(png),
            "rendered_shape": shape(rendered, spec.font_file),
            "target_shape": shape(target, spec.font_file),
            "base_word": meta.get("base"),
            "base_provenance": prov.get(meta.get("base")),
            "failure_class": meta.get("failure_class"),
            "failure_group": meta.get("group"),
            "plausibility": meta.get("plausibility", "plausible"),
            "direction": meta.get("direction"),
            "edit_detail": meta.get("detail"),
            "render_spec": spec.as_dict(),
        })

    i = 0
    for r in chosen:
        if r["direction"] == "corrupt_image":
            add_item(i, r["perturbed"], r["base"], "mismatch", r)
        else:
            add_item(i, r["base"], r["perturbed"], "mismatch", r)
        i += 1
    for b in match_bases:
        add_item(i, b, b, "match",
                 {"base": b, "failure_class": None, "group": None,
                  "direction": "clean_control", "detail": "exact match; ground truth by construction"})
        i += 1

    # Stable id order independent of construction order.
    items.sort(key=lambda r: r["item_id"])
    # Annotate how many items share each image, so the paired design is visible in the manifest.
    shares = collections.Counter(r["image_file"] for r in items)
    for r in items:
        r["items_sharing_this_image"] = shares[r["image_file"]]
    return items, chosen, rejected, valid, {"capped": capped,
                                            "distinct_base_words_available": distinct_bases,
                                            "requested_total": target_total}


def main():
    here = Path(__file__).resolve().parent
    repo = here.parents[2]
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base-strings", type=Path, default=None)
    ap.add_argument("--eval003-manifest", type=Path,
                    default=repo / "eval/calibration/devanagari-v0/candidate-manifest.jsonl")
    ap.add_argument("--out-dir", type=Path, default=here / "build")
    ap.add_argument("--total", type=int, default=120, help="total items; half match, half mismatch")
    ap.add_argument("--seed", type=int, default=20260825)
    ap.add_argument("--font-file", default=RenderSpec().font_file)
    ap.add_argument("--point-size", type=int, default=RenderSpec().point_size)
    ap.add_argument("--dry-run", action="store_true",
                    help="enumerate and screen candidates, report coverage, render nothing")
    a = ap.parse_args()

    spec = RenderSpec(font_file=a.font_file, point_size=a.point_size)
    bases = load_base_strings(a.base_strings, a.eval003_manifest)
    print(f"base strings: {len(bases)}")

    if a.dry_run:
        valid, rejected = [], collections.Counter()
        cls = collections.Counter()
        for b in bases:
            for c in perturb.all_candidates(b["text"]):
                v = is_valid_mismatch(b["text"], c.text, spec.font_file)
                if v.valid:
                    valid.append(c); cls[c.failure_class] += 1
                else:
                    rejected[v.reason] += 1
        print(f"valid candidates: {len(valid)}   rejected: {dict(rejected)}")
        for k, v in sorted(cls.items()):
            print(f"  {k:26} {v}")
        return

    items, chosen, rejected, valid, cap = build(bases, spec, a.total, a.seed, a.out_dir)
    out = Path(a.out_dir)
    (out / "items.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in items), encoding="utf-8")
    (out / "rejected-candidates.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rejected), encoding="utf-8")

    summary = {
        "battery": "devanagari-exactness-v0",
        "generated_by": "eval/battery/devanagari-exactness/build_items.py",
        "ground_truth": "by construction — every image is rendered locally from a known string; "
                        "no annotation, reader or dataset label is relied upon",
        "seed": a.seed,
        "render_spec": spec.as_dict(),
        "totals": {
            "items": len(items),
            "match": sum(1 for r in items if r["expected_verdict"] == "match"),
            "mismatch": sum(1 for r in items if r["expected_verdict"] == "mismatch"),
        },
        "mismatch_by_direction": dict(collections.Counter(
            r["direction"] for r in items if r["expected_verdict"] == "mismatch")),
        "mismatch_by_class": dict(collections.Counter(
            r["failure_class"] for r in items if r["expected_verdict"] == "mismatch")),
        "mismatch_by_group": dict(collections.Counter(
            r["failure_group"] for r in items if r["expected_verdict"] == "mismatch")),
        "mismatch_by_plausibility": dict(collections.Counter(
            r["plausibility"] for r in items if r["expected_verdict"] == "mismatch")),
        "size_cap": {**cap, "note":
            "Match items must be distinct words, so the battery cannot exceed the number of "
            "available base words without repeating an image. For a larger battery, supply more "
            "validated base words rather than padding."},
        "distinct_base_words_used": len({r["base_word"] for r in items}),
        "candidate_screening": {
            "valid": len(valid),
            "rejected": dict(collections.Counter(r["rejection_reason"] for r in rejected)),
            "rule": "a mismatch ships only if NFC strings differ AND shaped glyphs differ",
        },
        "distinct_image_hashes": len({r["image_sha256"] for r in items}),
        "distinct_image_files": len({r["image_file"] for r in items}),
        "paired_items": {
            "count": sum(1 for r in items if r["items_sharing_this_image"] > 1),
            "note": "Items sharing one image are a deliberate pair: identical pixels, different "
                    "target, opposite expected verdict. A checker cannot score well on both by "
                    "looking only at the image, and cannot score well on both by ignoring it.",
        },
    }
    (out / "build-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2),
                                            encoding="utf-8")
    print(json.dumps(summary["totals"], indent=2))
    print("by direction:", summary["mismatch_by_direction"])
    print("by group    :", summary["mismatch_by_group"])
    print(f"rejected    : {summary['candidate_screening']['rejected']}")
    print(f"wrote -> {out}")


if __name__ == "__main__":
    main()
