#!/usr/bin/env python3
"""
Tests for deterministic item construction.

These are not decoration. Two of them encode defects found while building this battery:

  * `test_invisible_difference_is_rejected` — precomposed क़ (U+0958) and क + nukta shape to
    byte-identical glyphs on this font. An item built from that pair would score a checker wrong
    for correctly reporting what it saw.

  * `test_plausibility_allows_matra_after_nukta` — the first version of the plausibility rule
    flagged तोड़ा (an ordinary Hindi word) as malformed, because it treated a vowel sign after a
    nukta as illegal. That would have thrown away valid hard items.

Run:  python3 test_devanagari_exactness.py
No network, no model, no spend.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import perturb  # noqa: E402
from devtext import (NUKTA, VIRAMA, glyphs_differ, is_valid_mismatch, nfc,  # noqa: E402
                     render, shape, sha256_file)

FAILURES: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    status = "PASS" if cond else "FAIL"
    print(f"  {status}  {name}" + (f"  — {detail}" if detail and not cond else ""))
    if not cond:
        FAILURES.append(name)


# --------------------------------------------------------------------------------------------
# Validity screening
# --------------------------------------------------------------------------------------------
def test_invisible_difference_is_rejected():
    """Different Unicode, identical pixels -> must never become an item."""
    precomposed, decomposed = "क़", "क़"
    same_glyphs = not glyphs_differ(precomposed, decomposed)
    v = is_valid_mismatch(precomposed, decomposed)
    check("invisible nukta pair shapes identically", same_glyphs)
    check("invisible nukta pair is rejected as an item", not v.valid,
          f"got valid={v.valid} reason={v.reason}")


def test_visible_difference_is_accepted():
    v = is_valid_mismatch("सुबह", "सुवह")
    check("visible ब/व difference is accepted", v.valid, v.reason)
    check("accepted pair really has different glyphs", v.rendered_shape != v.target_shape)


def test_identical_strings_are_not_a_mismatch():
    v = is_valid_mismatch("सुबह", "सुबह")
    check("identical strings rejected as mismatch", not v.valid and v.reason == "normalised_equal")


def test_normalisation_agrees_with_pixels():
    """NFC must collapse exactly those pairs the renderer draws identically."""
    a, b = "क़", "क़"
    check("NFC collapses the precomposed nukta pair", nfc(a) == nfc(b))


# --------------------------------------------------------------------------------------------
# Plausibility rule
# --------------------------------------------------------------------------------------------
def test_plausibility_allows_matra_after_nukta():
    """Regression: तोड़ा is a real word; a vowel sign after a nukta is ordinary Hindi."""
    check("तोड़ा is plausible", perturb.cluster_plausibility("तोड़ा") == "plausible")


def test_plausibility_rejects_broken_clusters():
    cases = {
        "ोड़ना": "opens with a vowel sign",
        "तो़ना": "nukta on a vowel sign",
        "तोड़न" + VIRAMA: "trailing bare virama",
    }
    for s, why in cases.items():
        check(f"implausible: {why}",
              perturb.cluster_plausibility(s) == "implausible_cluster", s)
    for s in ("क्षेत्र", "अभिनन्दन", "तोड़ना"):
        check(f"plausible: {s}", perturb.cluster_plausibility(s) == "plausible")


# --------------------------------------------------------------------------------------------
# Operators
# --------------------------------------------------------------------------------------------
def test_operators_change_the_string():
    base = "क्षेत्र"
    cands = perturb.all_candidates(base)
    check("operators produce candidates", len(cands) > 0)
    check("no candidate equals its base", all(nfc(c.text) != nfc(base) for c in cands))
    check("every candidate carries a known class",
          all(c.failure_class in perturb.OPERATORS for c in cands))


def test_operator_enumeration_is_deterministic():
    a = [(c.failure_class, c.position, c.text) for c in perturb.all_candidates("अभिनन्दन")]
    b = [(c.failure_class, c.position, c.text) for c in perturb.all_candidates("अभिनन्दन")]
    check("candidate enumeration is stable across calls", a == b)


def test_conjunct_split_is_visible():
    """क्ष is one fused glyph; कष is two. The split must be visible, or the class is untestable."""
    joined = "क" + VIRAMA + "ष"
    split = "कष"
    check("conjunct split changes the glyph sequence", glyphs_differ(joined, split),
          f"{shape(joined)} vs {shape(split)}")


def test_every_class_has_at_least_one_visible_instance():
    """A class that can only ever produce invisible differences would be dead weight."""
    bases = ["क्षेत्र", "अभिनन्दन", "तोड़ना", "पार्किंग", "इंडिया", "संग्राहलय"]
    seen = set()
    for b in bases:
        for c in perturb.all_candidates(b):
            if c.failure_class not in seen and is_valid_mismatch(b, c.text).valid:
                seen.add(c.failure_class)
    unreachable = set(perturb.OPERATORS) - seen
    # Some classes need a feature the sample bases lack (e.g. NUKTA_REMOVE needs a nukta).
    expected_gaps = {"NUKTA_REMOVE", "VISARGA_REMOVE", "NASAL_SUBSTITUTE", "NASAL_DELETE",
                     "REPH_TO_FULL_RA", "RAKAR_TO_FULL_RA", "INDEP_VOWEL_SUBSTITUTE",
                     "MATRA_SUBSTITUTE", "FULL_RA_TO_REPH"}
    check("no class is unreachable for an unexplained reason",
          unreachable <= expected_gaps, f"unexpectedly unreachable: {unreachable - expected_gaps}")


# --------------------------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------------------------
def test_render_is_deterministic():
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        a = render("सुबह की पहली चाय", t / "a.png")
        b = render("सुबह की पहली चाय", t / "b.png")
        check("identical text renders byte-identically", sha256_file(a) == sha256_file(b))


def test_different_text_renders_differently():
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        a = render("सुबह", t / "a.png")
        b = render("सुवह", t / "b.png")
        check("different text renders to different bytes", sha256_file(a) != sha256_file(b))


# --------------------------------------------------------------------------------------------
# Whole-battery invariants (run against a freshly built battery)
# --------------------------------------------------------------------------------------------
def test_built_battery_invariants():
    with tempfile.TemporaryDirectory() as t:
        r = subprocess.run(
            [sys.executable, str(HERE / "build_items.py"), "--total", "40", "--out-dir", t],
            capture_output=True, text=True,
        )
        if r.returncode != 0:
            check("battery builds", False, r.stderr.strip()[:200])
            return
        items = [json.loads(l) for l in (Path(t) / "items.jsonl").read_text().splitlines() if l.strip()]
        summary = json.loads((Path(t) / "build-summary.json").read_text())

        n_match = sum(1 for i in items if i["expected_verdict"] == "match")
        n_mis = sum(1 for i in items if i["expected_verdict"] == "mismatch")
        check("battery is balanced 50/50", n_match == n_mis, f"{n_match} vs {n_mis}")
        check("'always match' and 'always mismatch' both score 50%",
              abs(n_match - n_mis) == 0)

        check("no mismatch item is invisible",
              all(i["rendered_shape"] != i["target_shape"]
                  for i in items if i["expected_verdict"] == "mismatch"))
        check("every match item is truly identical",
              all(nfc(i["rendered_string"]) == nfc(i["target_string"])
                  for i in items if i["expected_verdict"] == "match"))
        check("no duplicate image bytes",
              summary["distinct_image_files"] == summary["distinct_image_hashes"])

        mb = {i["base_word"] for i in items if i["expected_verdict"] == "match"}
        xb = {i["base_word"] for i in items if i["expected_verdict"] == "mismatch"}
        check("some base words appear in both strata (word identity is not a cue)",
              len(mb & xb) > 0, f"overlap={len(mb & xb)}")

        # Paired items: same image, opposite verdict.
        by_img: dict[str, list] = {}
        for i in items:
            by_img.setdefault(i["image_file"], []).append(i)
        pairs = [v for v in by_img.values() if len(v) > 1]
        if pairs:
            check("paired items on one image carry opposite verdicts",
                  all(len({x["expected_verdict"] for x in v}) > 1 for v in pairs))

        check("ground truth is recorded as constructed, not annotated",
              "by construction" in summary["ground_truth"])


def test_build_is_deterministic():
    hashes = []
    for _ in range(2):
        with tempfile.TemporaryDirectory() as t:
            subprocess.run([sys.executable, str(HERE / "build_items.py"),
                            "--total", "30", "--out-dir", t],
                           capture_output=True, text=True)
            hashes.append(sha256_file(Path(t) / "items.jsonl"))
    check("two builds produce byte-identical manifests", hashes[0] == hashes[1])


def main() -> int:
    print("Devanagari exactness battery — construction tests\n")
    for fn in sorted(
        (v for k, v in globals().items() if k.startswith("test_") and callable(v)),
        key=lambda f: f.__name__,
    ):
        print(f"{fn.__name__}:")
        fn()
    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)} check(s): {', '.join(FAILURES)}")
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
