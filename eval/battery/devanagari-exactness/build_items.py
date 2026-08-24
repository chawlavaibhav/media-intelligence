#!/usr/bin/env python3
"""
Build the Devanagari exactness battery: deterministic, balanced, visibly-valid items.

THE QUESTION THE BATTERY ASKS
    Not "can this model read Hindi?" but:
    **"Does this evaluator report a match when the visible text differs from the requested
    target?"** That silent yes — the false pass — is the failure that reaches a customer with a
    passing grade attached.

GROUND TRUTH BY CONSTRUCTION
    Every image is rendered locally from a string we chose, with a pinned font FILE that is also
    the font the validity screen shaped. What the image says is therefore known without any
    annotation, any reader, and any dataset label.

DIRECTION MATTERS MORE THAN IT LOOKS
      corrupt_image  render(perturbed), ask about the ORIGINAL word.
                     The model sees malformed text and is handed a plausible real word. Every
                     pull of its language prior says "yes, that's the word." This is where silent
                     autocorrection actually happens, so it is the primary stratum.

      corrupt_target render(original), ask about the PERTURBED string.
                     Clean text, odd target. Much easier. A control: a checker that fails here is
                     failing basic comparison, not resisting autocorrection.

ONE HARD OPPORTUNITY PER BASE WORD  (Controller review fix 5)
    An earlier version let one base word back up to four mismatch items and then quoted a
    binomial zero-failure upper bound over the resulting count. That is not honest: four
    deterministic perturbations of the same word are not four independent chances to catch a
    checker out. The bound was being computed over correlated trials.

    The rule is now structural rather than a caveat: **every mismatch item uses a distinct base
    word**, so the number of hard opportunities equals the number of distinct hard base words by
    construction, and the invariant is asserted in the test suite. Class coverage is preserved by
    solving the allocation deterministically (a maximum bipartite matching between failure
    classes and base words) instead of by relaxing the independence rule.

    Even so, the resulting figure is a **binomial/opportunity-model bound conditional on this
    battery's construction**. The words and operators are not a probability sample of all future
    generated Hindi, so it is not an estimate of any checker's universal true error rate.

NO ITEM SHIPS UNVERIFIED
    Every mismatch passes devtext.is_valid_mismatch(): the strings must differ after NFC *and*
    the FINAL RASTER OUTPUT must differ. Rejections are written to the manifest with their
    reason, not silently dropped.

No network. No model. No spend. Rendering is local.
"""
from __future__ import annotations

import argparse
import collections
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import perturb  # noqa: E402
from checker_input import write_checker_inputs  # noqa: E402
from devtext import (RenderSpec, canonical_equal, environment_provenance,  # noqa: E402
                     has_devanagari, is_valid_mismatch, nfc, raster_sha256, render,
                     sha256_file, shape, shapes_with_dotted_circle, strip_outer_whitespace)

# Fraction of mismatch items built in the hard direction (see module docstring).
CORRUPT_IMAGE_SHARE = 0.7
# Structural, not tunable: one mismatch item per distinct base word, so a zero-failure bound is
# computed over distinct opportunities rather than over correlated perturbations of one word.
MAX_MISMATCH_ITEMS_PER_BASE = 1
# No single failure class may exceed this share of the mismatch stratum.
MAX_CLASS_SHARE = 0.12
# Share of the mismatch stratum reserved for visibly-broken clusters. Deliberately small: they
# are a useful floor (a checker that misses these is unusable) but they do not test resistance to
# autocorrection, so they are excluded from the hard stratum entirely.
IMPLAUSIBLE_SHARE = 0.15


# --------------------------------------------------------------------------------------------
# Statistics
# --------------------------------------------------------------------------------------------
def zero_failure_upper_bound(n: int, confidence: float = 0.95) -> float:
    """One-sided Clopper-Pearson upper bound on the failure rate when 0 failures are seen in n.

    Plain English: if a checker gets n independent chances to wave a broken image through and
    never does, this is the highest true failure rate still consistent with that result at the
    stated confidence. It is a *ceiling on our ignorance*, not a measurement of accuracy.
    """
    if n <= 0:
        return 1.0
    return 1.0 - (1.0 - confidence) ** (1.0 / n)


def opportunities_required(target_bound: float, confidence: float = 0.95) -> int:
    """Smallest number of zero-failure opportunities whose upper bound is <= target_bound."""
    return int(math.ceil(math.log(1.0 - confidence) / math.log(1.0 - target_bound)))


# --------------------------------------------------------------------------------------------
# Base strings
# --------------------------------------------------------------------------------------------
def load_base_strings(path: Path | None, eval003_manifest: Path | None) -> list[dict]:
    """Base words, with provenance recorded per string.

    `strip_outer_whitespace` is applied here and named here: a trailing tab or newline in a
    tab-separated annotation file belongs to the file format, not to the word. It is an INGEST
    rule and is deliberately not part of the comparison predicate — see devtext.
    """
    def clean(s: str) -> str:
        return nfc(strip_outer_whitespace(s))

    if path and path.exists():
        raw = json.loads(path.read_text(encoding="utf-8"))
        return [{"text": clean(r["text"] if isinstance(r, dict) else r),
                 "provenance": (r.get("provenance") if isinstance(r, dict) else None)
                               or f"base-list:{path.name}"}
                for r in raw]
    if eval003_manifest and eval003_manifest.exists():
        seen, out = set(), []
        for line in eval003_manifest.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            t = clean(r.get("source_provided_transcription", ""))
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


# --------------------------------------------------------------------------------------------
# Deterministic allocation: one mismatch item per base word, class coverage preserved
# --------------------------------------------------------------------------------------------
def _max_matching(classes: list[str], adjacency: dict[str, list[str]]) -> dict[str, str]:
    """Kuhn's algorithm. Deterministic: inputs are sorted, so the matching is reproducible.

    Left = failure classes, right = base words. Maximising this matching is what lets the battery
    keep broad class coverage *and* the one-item-per-base rule at the same time — the two only
    appear to conflict if the allocation is done greedily.
    """
    match_base_to_class: dict[str, str] = {}

    def try_assign(cls: str, seen: set[str]) -> bool:
        for base in adjacency.get(cls, []):
            if base in seen:
                continue
            seen.add(base)
            holder = match_base_to_class.get(base)
            if holder is None or try_assign(holder, seen):
                match_base_to_class[base] = cls
                return True
        return False

    for cls in classes:
        try_assign(cls, set())
    return {cls: base for base, cls in match_base_to_class.items()}


def select_mismatches(valid: list[dict], n_mismatch: int,
                      max_per_class: int, max_implausible: int) -> list[dict]:
    """Choose `n_mismatch` records, each on a DISTINCT base word.

    Phase 1 — coverage. One base per failure class, by maximum bipartite matching over classes
    that have at least one *plausible* candidate. Scarce classes are not crowded out by common
    ones, which a greedy pass would do.

    Phase 2 — coverage of the remainder. Classes still uncovered are offered implausible-only
    candidates, under the implausible quota.

    Phase 3 — fill. Remaining base words are handed out round-robin across classes, respecting
    the per-class cap and preferring plausible candidates.
    """
    # best[(base, cls)] -> record. Plausible first, then deterministic order.
    by_key: dict[tuple[str, str], dict] = {}
    for r in sorted(valid, key=lambda r: (r["base"], r["failure_class"],
                                          r["plausibility"] != "plausible",
                                          r["position"], r["perturbed"])):
        by_key.setdefault((r["base"], r["failure_class"]), r)

    classes = sorted({k[1] for k in by_key})
    plaus_adj = {c: sorted(b for (b, cc) in by_key
                           if cc == c and by_key[(b, cc)]["plausibility"] == "plausible")
                 for c in classes}
    any_adj = {c: sorted(b for (b, cc) in by_key if cc == c) for c in classes}

    used_bases: set[str] = set()
    per_class = collections.Counter()
    n_implausible = 0
    chosen: list[dict] = []

    def take(base: str, cls: str) -> bool:
        nonlocal n_implausible
        rec = by_key.get((base, cls))
        if rec is None or base in used_bases or per_class[cls] >= max_per_class:
            return False
        if rec["plausibility"] != "plausible":
            if n_implausible >= max_implausible:
                return False
            n_implausible += 1
        chosen.append(rec)
        used_bases.add(base)
        per_class[cls] += 1
        return True

    # Phase 1 — plausible coverage.
    for cls, base in sorted(_max_matching(classes, plaus_adj).items()):
        if len(chosen) >= n_mismatch:
            break
        take(base, cls)

    # Phase 2 — classes still uncovered, implausible allowed under quota.
    for cls in classes:
        if len(chosen) >= n_mismatch:
            break
        if per_class[cls]:
            continue
        for base in any_adj[cls]:
            if take(base, cls):
                break

    # Phase 3 — fill remaining bases round-robin across classes.
    cursor = {c: 0 for c in classes}
    while len(chosen) < n_mismatch:
        progressed = False
        for cls in classes:
            if len(chosen) >= n_mismatch:
                break
            if per_class[cls] >= max_per_class:
                continue
            adj = any_adj[cls]
            while cursor[cls] < len(adj):
                base = adj[cursor[cls]]
                cursor[cls] += 1
                if take(base, cls):
                    progressed = True
                    break
        if not progressed:
            break
    return chosen


def assign_directions(chosen: list[dict]) -> int:
    """Assign `corrupt_image` / `corrupt_target` deterministically.

    Implausible corruptions are never placed in the hard direction: a string that opens with a
    vowel sign is trivially rejectable, so counting it as an autocorrection opportunity would
    inflate the hard stratum with items that do not test autocorrection at all.

    Returns the number of hard opportunities. Because every mismatch sits on a distinct base word,
    that number is also the number of distinct hard base words.
    """
    chosen.sort(key=lambda r: (r["plausibility"] != "plausible", r["failure_class"], r["base"]))
    plausible = [r for r in chosen if r["plausibility"] == "plausible"]
    n_hard = min(round(len(chosen) * CORRUPT_IMAGE_SHARE), len(plausible))
    hard = set(id(r) for r in plausible[:n_hard])
    for r in chosen:
        is_hard = id(r) in hard
        r["direction"] = "corrupt_image" if is_hard else "corrupt_target"
        r["hard_opportunity"] = is_hard
    return n_hard


# --------------------------------------------------------------------------------------------
def build(base_strings, spec: RenderSpec, target_total: int, seed: int, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    img_dir = out_dir / "images"
    img_dir.mkdir(exist_ok=True)

    # ---- enumerate and screen every candidate --------------------------------------------
    valid: list[dict] = []
    rejected: list[dict] = []
    for b in base_strings:
        base = b["text"]
        for c in perturb.all_candidates(base):
            v = is_valid_mismatch(base, c.text, spec)
            # Plausibility is decided by the SHAPER as well as by the string rule. A string the
            # shaper draws with a dotted circle (U+25CC) is visibly malformed, however legal it
            # looked to a hand-written cluster grammar, and must not sit in the hard stratum.
            plaus = c.plausibility
            reason = "string_rule" if plaus != "plausible" else None
            if plaus == "plausible" and shapes_with_dotted_circle(c.text, spec):
                plaus, reason = "implausible_cluster", "shaper_dotted_circle"
            rec = {
                "base": base, "perturbed": c.text, "failure_class": c.failure_class,
                "group": perturb.CLASS_TO_GROUP.get(c.failure_class, "other"),
                "position": c.position, "detail": c.detail,
                "plausibility": plaus, "implausible_reason": reason,
            }
            if v.valid:
                valid.append(rec)
            else:
                rejected.append({**rec, "rejection_reason": v.reason,
                                 "glyph_sequences_differed": v.glyphs_differ})

    # Every match item must be a DISTINCT rendered word, and every mismatch item must sit on a
    # DISTINCT base word. The battery therefore caps at the number of usable base words and
    # reports the cap rather than padding to a requested size.
    usable_bases = sorted({r["base"] for r in valid})
    n_mismatch = min(target_total // 2, len(usable_bases))
    n_match = n_mismatch
    capped = n_mismatch < target_total // 2
    max_per_class = max(1, int(n_mismatch * MAX_CLASS_SHARE))
    max_implausible = max(1, int(n_mismatch * IMPLAUSIBLE_SHARE))

    # `seed` rotates the deterministic candidate order so a different-but-still-reproducible
    # sample can be drawn if the Controller wants one. It is not an RNG.
    if seed:
        rot = seed % max(1, len(valid))
        valid = valid[rot:] + valid[:rot]

    chosen = select_mismatches(valid, n_mismatch, max_per_class, max_implausible)
    n_hard = assign_directions(chosen)

    # ---- match items, drawn from the SAME base words ---------------------------------------
    # Deliberate: a base word that appears as a mismatch also appears as a match, so word
    # identity carries no signal about the expected answer.
    mismatch_bases = [r["base"] for r in chosen]
    ordered_bases = mismatch_bases + [b for b in usable_bases if b not in set(mismatch_bases)]
    match_bases = ordered_bases[:n_match]

    prov = {b["text"]: b["provenance"] for b in base_strings}
    items = []
    # One rendered string -> one image file. A clean word is deliberately reused across a match
    # item and a corrupt_target mismatch item: same pixels, two different targets, opposite
    # expected answers. That pairing isolates the target as the only variable.
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
            # Authoritative visibility evidence: the final rasters, compared as bytes.
            "rendered_raster_sha256": raster_sha256(rendered, spec),
            "target_raster_sha256": raster_sha256(target, spec),
            # Diagnostic only — a different glyph sequence is evidence of, not proof of, a
            # different picture.
            "rendered_shape": shape(rendered, spec),
            "target_shape": shape(target, spec),
            "base_word": meta.get("base"),
            "base_provenance": prov.get(meta.get("base")),
            "failure_class": meta.get("failure_class"),
            "failure_group": meta.get("group"),
            "plausibility": meta.get("plausibility", "plausible"),
            "direction": meta.get("direction"),
            "hard_opportunity": bool(meta.get("hard_opportunity", False)),
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
                 {"base": b, "failure_class": None, "group": None, "hard_opportunity": False,
                  "direction": "clean_control", "detail": "exact match; ground truth by construction"})
        i += 1

    items.sort(key=lambda r: r["item_id"])
    shares = collections.Counter(r["image_file"] for r in items)
    for r in items:
        r["items_sharing_this_image"] = shares[r["image_file"]]
    return items, chosen, rejected, valid, {
        "capped": capped,
        "usable_base_words_available": len(usable_bases),
        "requested_total": target_total,
        "n_hard_opportunities": n_hard,
    }


def summarise(items, chosen, rejected, valid, cap, spec, seed) -> dict:
    mismatches = [r for r in items if r["expected_verdict"] == "mismatch"]
    hard = [r for r in mismatches if r["hard_opportunity"]]
    hard_bases = {r["base_word"] for r in hard}
    all_mismatch_bases = {r["base_word"] for r in mismatches}

    hard_n = len(hard)
    need_5 = opportunities_required(0.05)
    # Hard opportunities are CORRUPT_IMAGE_SHARE of the mismatch stratum, and one mismatch item
    # per base word, so the base-word requirement follows directly.
    words_for_5 = int(math.ceil(need_5 / CORRUPT_IMAGE_SHARE))

    return {
        "battery": "devanagari-exactness-v0",
        "generated_by": "eval/battery/devanagari-exactness/build_items.py",
        "ground_truth": "by construction — every image is rendered locally from a known string "
                        "with a pinned font file; no annotation, reader or dataset label is "
                        "relied upon",
        "seed": seed,
        "render_spec": spec.as_dict(),
        "environment_provenance": environment_provenance(spec),
        "totals": {
            "items": len(items),
            "match": sum(1 for r in items if r["expected_verdict"] == "match"),
            "mismatch": len(mismatches),
        },
        "opportunity_model": {
            "rule": "every mismatch item uses a distinct base word, so item count and distinct "
                    "opportunity count are equal by construction",
            "mismatch_items": len(mismatches),
            "distinct_mismatch_base_words": len(all_mismatch_bases),
            "hard_items": hard_n,
            "distinct_hard_base_words": len(hard_bases),
            "hard_bound_if_zero_false_passes_95pct": round(zero_failure_upper_bound(hard_n), 4),
            "all_mismatch_bound_if_zero_false_passes_95pct":
                round(zero_failure_upper_bound(len(mismatches)), 4),
            "hard_opportunities_required_for_5pct": need_5,
            "validated_base_words_required_for_5pct": words_for_5,
            "epistemic_limit":
                "This is a binomial upper bound over the opportunities this battery constructs, "
                "conditional on its word list, its operators and its font. The words and "
                "operators are NOT a probability sample of future generated Hindi, so it is not "
                "an estimate of any checker's universal true error rate. It bounds what this "
                "battery could have failed to detect, nothing wider.",
        },
        "mismatch_by_direction": dict(collections.Counter(r["direction"] for r in mismatches)),
        "mismatch_by_class": dict(collections.Counter(r["failure_class"] for r in mismatches)),
        "mismatch_by_group": dict(collections.Counter(r["failure_group"] for r in mismatches)),
        "mismatch_by_plausibility": dict(collections.Counter(r["plausibility"] for r in mismatches)),
        "hard_by_group": dict(collections.Counter(r["failure_group"] for r in hard)),
        "size_cap": {**cap, "note":
            "Match items must be distinct words and every mismatch item must sit on a distinct "
            "base word, so the battery cannot exceed the number of usable base words. For a "
            "larger battery, supply more validated base words rather than padding."},
        "distinct_base_words_used": len({r["base_word"] for r in items}),
        "candidate_screening": {
            "valid": len(valid),
            "rejected": dict(collections.Counter(r["rejection_reason"] for r in rejected)),
            "rejected_despite_differing_glyphs": sum(
                1 for r in rejected
                if r["rejection_reason"] == "raster_identical" and r["glyph_sequences_differed"]),
            "rule": "a mismatch ships only if NFC-canonical strings differ AND the final PNG "
                    "bytes differ; the glyph-sequence comparison is a diagnostic, not the gate",
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
    ap.add_argument("--seed", type=int, default=0,
                    help="rotates the deterministic candidate order; 0 = canonical order")
    ap.add_argument("--font-file", default=RenderSpec().font_file)
    ap.add_argument("--face-index", type=int, default=RenderSpec().face_index)
    ap.add_argument("--point-size", type=int, default=RenderSpec().point_size)
    ap.add_argument("--dry-run", action="store_true",
                    help="enumerate and screen candidates, report coverage, write nothing")
    a = ap.parse_args()

    spec = RenderSpec(font_file=a.font_file, face_index=a.face_index, point_size=a.point_size)
    bases = load_base_strings(a.base_strings, a.eval003_manifest)
    print(f"base strings: {len(bases)}")

    if a.dry_run:
        valid, rejected = [], collections.Counter()
        cls = collections.Counter()
        for b in bases:
            for c in perturb.all_candidates(b["text"]):
                v = is_valid_mismatch(b["text"], c.text, spec)
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

    summary = summarise(items, chosen, rejected, valid, cap, spec, a.seed)
    (out / "build-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2),
                                            encoding="utf-8")

    # Checker-facing projections + the evaluator-side scoring key. Written through the blind
    # check, so a leaking file cannot be produced and then used by mistake.
    write_checker_inputs(items, out)

    print(json.dumps(summary["totals"], indent=2))
    print("opportunity model:", json.dumps(
        {k: summary["opportunity_model"][k] for k in
         ("mismatch_items", "distinct_mismatch_base_words", "hard_items",
          "distinct_hard_base_words", "hard_bound_if_zero_false_passes_95pct",
          "hard_opportunities_required_for_5pct", "validated_base_words_required_for_5pct")},
        indent=2))
    print("by direction:", summary["mismatch_by_direction"])
    print("by group    :", summary["mismatch_by_group"])
    print(f"classes     : {len(summary['mismatch_by_class'])}")
    print(f"rejected    : {summary['candidate_screening']['rejected']}")
    print(f"wrote -> {out}")


if __name__ == "__main__":
    main()
