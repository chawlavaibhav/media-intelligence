#!/usr/bin/env python3
"""
Tests for deterministic item construction, checker-input blinding, and rendering provenance.

These are not decoration. Several of them encode defects that were actually present in the code
they now guard:

  * `test_invisible_difference_is_rejected` — precomposed क़ (U+0958) and क + nukta shape to
    byte-identical glyphs. An item built from that pair would score a checker wrong for
    correctly reporting what it saw.

  * `test_raster_identical_is_rejected_even_when_glyphs_differ` — `सु‌बह` (with a zero-width
    non-joiner) and `सुबह` shape to DIFFERENT glyph sequences and render to IDENTICAL pixels.
    The earlier glyph-only gate would have admitted it. This is why the gate is now the final
    raster.

  * `test_plausibility_allows_matra_after_nukta` — an early plausibility rule flagged तोड़ा (an
    ordinary Hindi word) as malformed. It would have thrown away valid hard items.

  * `test_shaper_catches_clusters_the_string_rule_missed` — deleting the first consonant of
    इंग्लीश leaves इं्लीश, whose virama hangs off an anusvara. The string rule passed it; the
    shaper draws it with a dotted circle. It had reached the hard stratum.

  * `test_transcribe_payload_never_exposes_the_target` — the checker contract described shape 1
    as blind while also handing every checker the target. The two shapes measure different
    things and shape 1 is only meaningful if it really is blind.

Run:  python3 test_devanagari_exactness.py
No network, no model, no spend.
"""
from __future__ import annotations

import json
import math
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import checker_input  # noqa: E402
import devtext  # noqa: E402
import perturb  # noqa: E402
from build_items import (CORRUPT_IMAGE_SHARE, opportunities_required,  # noqa: E402
                         zero_failure_upper_bound)
from checker_input import (GROUND_TRUTH_FIELDS, project_transcribe,  # noqa: E402
                           project_verdict, scoring_record, verify_blind)
from devtext import (FontMissing, NUKTA, RenderSpec, VIRAMA,  # noqa: E402
                     canonical_equal, environment_provenance, glyphs_differ,
                     has_devanagari, is_valid_mismatch, nfc, raster_sha256, render,
                     shape, shapes_with_dotted_circle, sha256_file, strip_outer_whitespace)

# The nukta pair, built from explicit codepoints. Written as ordinary source literals the two
# forms are visually identical and an editor may normalise one into the other, which would turn
# the invisible-difference test into a tautology that always passes.
PRECOMPOSED_QA = "\u0958"              # क़  as a single precomposed codepoint
DECOMPOSED_QA = "\u0915\u093C"         # क + nukta

FAILURES: list[str] = []
_BUILD_CACHE: dict[int, tuple] = {}


def check(name: str, cond: bool, detail: str = "") -> None:
    status = "PASS" if cond else "FAIL"
    print(f"  {status}  {name}" + (f"  — {detail}" if detail and not cond else ""))
    if not cond:
        FAILURES.append(name)


def build_battery(total: int = 40) -> tuple[list[dict], dict, Path]:
    """Build once per size and reuse; rendering is the slow part of this suite."""
    if total not in _BUILD_CACHE:
        d = Path(tempfile.mkdtemp(prefix=f"devx-test-{total}-"))
        r = subprocess.run(
            [sys.executable, str(HERE / "build_items.py"), "--total", str(total),
             "--out-dir", str(d)],
            capture_output=True, text=True,
        )
        if r.returncode != 0:
            raise RuntimeError(f"build failed: {r.stderr.strip()[:400]}")
        items = [json.loads(l) for l in (d / "items.jsonl").read_text().splitlines() if l.strip()]
        summary = json.loads((d / "build-summary.json").read_text())
        _BUILD_CACHE[total] = (items, summary, d)
    return _BUILD_CACHE[total]


# ============================================================================================
# 1-3 · Checker-input blinding  (Controller review fix 1)
# ============================================================================================
def test_transcribe_payload_never_exposes_the_target():
    items, _, _ = build_battery()
    payloads = [project_transcribe(i) for i in items]
    check("transcribe payload has no target_string field",
          all("target_string" not in p for p in payloads))
    leaked = [p["item_id"] for p in payloads
              if any(isinstance(v, str) and has_devanagari(v) for v in p.values())]
    check("no Devanagari appears anywhere in a transcribe payload", not leaked, str(leaked[:3]))
    check("transcribe prompt is the frozen transcription-only prompt",
          all(p["prompt"] == checker_input.PROMPT_TRANSCRIBE for p in payloads))
    check("verify_blind passes on the transcribe projection",
          verify_blind(payloads, "transcribe") == [])


def test_verdict_payload_does_expose_the_target():
    items, _, _ = build_battery()
    payloads = [project_verdict(i) for i in items]
    check("every verdict payload carries target_string",
          all(p.get("target_string") for p in payloads))
    check("every verdict prompt actually contains the target",
          all(p["target_string"] in p["prompt"] for p in payloads))
    check("verify_blind passes on the verdict projection",
          verify_blind(payloads, "verdict") == [])


def test_no_ground_truth_metadata_reaches_either_checker():
    items, _, _ = build_battery()
    for shape_name, project in (("transcribe", project_transcribe), ("verdict", project_verdict)):
        payloads = [project(i) for i in items]
        leaked = sorted({k for p in payloads for k in p if k in GROUND_TRUTH_FIELDS})
        check(f"no ground-truth field in {shape_name} payloads", not leaked, str(leaked))


def test_leak_is_detected_when_a_target_is_injected():
    """Regression: verify_blind must FAIL when the defect it exists to catch is reintroduced."""
    items, _, _ = build_battery()
    bad = project_transcribe(items[0])
    bad["target_string"] = items[0]["target_string"]
    v = verify_blind([bad], "transcribe")
    check("injected target into a transcribe payload is caught", len(v) > 0)
    check("the violation names the target field",
          any("target_string" in x for x in v), str(v))

    sneaky = project_transcribe(items[0])
    sneaky["prompt"] = sneaky["prompt"] + "\nExpected: " + items[0]["target_string"]
    v2 = verify_blind([sneaky], "transcribe")
    check("target smuggled into the transcribe prompt is caught by the Devanagari sweep",
          len(v2) > 0, str(v2))


def test_scoring_record_retains_the_target():
    items, _, _ = build_battery()
    recs = [scoring_record(i) for i in items]
    check("evaluator-side scoring record keeps the target",
          all(r["target_string"] for r in recs))
    check("evaluator-side scoring record keeps the constructed verdict",
          all(r["expected_verdict"] in ("match", "mismatch") for r in recs))
    check("shape 1 is scorable: canonical_equal(target, rendered) reproduces every verdict",
          all((canonical_equal(r["rendered_string"], r["target_string"]))
              == (r["expected_verdict"] == "match") for r in recs))


# ============================================================================================
# 4-5 · One pinned font asset for shaping AND rendering  (Controller review fix 2)
# ============================================================================================
def test_shaping_and_rendering_use_the_same_pinned_font_asset():
    spec = RenderSpec()
    seen: list[list[str]] = []
    real_run = subprocess.run

    def spy(cmd, *a, **k):
        if isinstance(cmd, list):
            seen.append(cmd)
        return real_run(cmd, *a, **k)

    devtext.subprocess.run = spy
    try:
        with tempfile.TemporaryDirectory() as t:
            # bypass the caches so the underlying commands are actually issued
            devtext._shape_cached.cache_clear()
            devtext._raster_sha256_cached.cache_clear()
            shape("सुबह", spec)
            render("सुबह", Path(t) / "x.png", spec)
    finally:
        devtext.subprocess.run = real_run

    shaper = [c for c in seen if c and c[0] == "hb-shape"]
    renderer = [c for c in seen if c and c[0] == "hb-view"]
    check("shaping invoked hb-shape", len(shaper) == 1, str(seen))
    check("rendering invoked hb-view", len(renderer) == 1, str(seen))
    if shaper and renderer:
        check("shaper is given the pinned font FILE",
              f"--font-file={spec.font_file}" in shaper[0], str(shaper[0]))
        check("renderer is given the same pinned font FILE",
              spec.font_file in renderer[0], str(renderer[0]))
        check("both pin the same face index",
              f"--face-index={spec.face_index}" in shaper[0]
              and f"--face-index={spec.face_index}" in renderer[0])
    check("RenderSpec no longer carries a font FAMILY name",
          not hasattr(spec, "font_desc"))
    joined = " ".join(" ".join(c) for c in seen)
    check("no family-name renderer (pango-view) is used at all", "pango-view" not in joined)


def test_font_fallback_cannot_silently_occur():
    bogus = RenderSpec(font_file="/nonexistent/NoSuchFont.ttf")
    with tempfile.TemporaryDirectory() as t:
        out = Path(t) / "x.png"
        try:
            render("सुबह", out, bogus)
            check("render with a missing font raises instead of falling back", False,
                  "render() succeeded with a nonexistent font file")
        except FontMissing:
            check("render with a missing font raises FontMissing", True)
        except Exception as e:                                     # pragma: no cover
            check("render with a missing font raises FontMissing", False, repr(e))
        check("no image was produced by the failed render", not out.exists())
    try:
        shape("सुबह", bogus)
        check("shape with a missing font raises instead of falling back", False)
    except FontMissing:
        check("shape with a missing font raises FontMissing", True)


def test_environment_provenance_is_recorded():
    p = environment_provenance(RenderSpec())
    for k in ("font_file", "font_sha256", "face_index", "shaper", "renderer",
              "point_size", "margin"):
        check(f"provenance records {k}", bool(p.get(k) is not None and p.get(k) != ""))
    check("provenance font sha256 is a real digest", re.fullmatch(r"[0-9a-f]{64}", p["font_sha256"]) is not None)
    check("provenance records that shaping and rendering share one asset",
          p["same_asset_for_shaping_and_rendering"] is True)
    check("provenance records that the font is NOT committed to the repo",
          p["font_committed_to_repo"] is False)


def test_font_asset_is_not_committed():
    r = subprocess.run(["git", "ls-files"], cwd=HERE, capture_output=True, text=True)
    fonts = [f for f in r.stdout.splitlines()
             if f.lower().endswith((".ttf", ".otf", ".ttc", ".woff", ".woff2"))]
    check("no font binary is committed in this battery", not fonts, str(fonts))


# ============================================================================================
# 6-8 · Visibility screening on FINAL PIXELS  (Controller review fix 3)
# ============================================================================================
def test_invisible_difference_is_rejected():
    """Canonically equivalent nukta encodings: same word, same pixels, must never be an item."""
    precomposed, decomposed = PRECOMPOSED_QA, DECOMPOSED_QA
    check("the nukta pair is canonically equal", canonical_equal(precomposed, decomposed))
    check("the nukta pair shapes identically", not glyphs_differ(precomposed, decomposed))
    check("the nukta pair renders to identical pixels",
          raster_sha256(precomposed) == raster_sha256(decomposed))
    v = is_valid_mismatch(precomposed, decomposed)
    check("the nukta pair is rejected as an item", not v.valid, f"reason={v.reason}")
    check("rejected for the right reason", v.reason == "canonical_equal", v.reason)


def test_raster_identical_is_rejected_even_when_glyphs_differ():
    """The case the old glyph-only gate would have admitted.

    `सु‌बह` carries a zero-width non-joiner. It is a genuinely different string after NFC, and it
    shapes to a DIFFERENT glyph sequence — an extra zero-advance glyph. The final PNGs are
    byte-identical. Asking a checker to report that difference would score it wrong for
    correctly describing the picture.
    """
    clean, zwnj = "सुबह", "सु‌बह"
    check("the ZWNJ pair is NOT canonically equal", not canonical_equal(clean, zwnj))
    check("the ZWNJ pair DOES shape to different glyph sequences", glyphs_differ(clean, zwnj))
    check("the ZWNJ pair renders to IDENTICAL pixels",
          raster_sha256(clean) == raster_sha256(zwnj))
    v = is_valid_mismatch(zwnj, clean)
    check("the ZWNJ pair is rejected as an item", not v.valid)
    check("rejected as raster_identical, not as a glyph question",
          v.reason == "raster_identical", v.reason)
    check("the rejection record still notes that glyphs differed", v.glyphs_differ)


def test_visible_difference_is_accepted():
    v = is_valid_mismatch("सुवह", "सुबह")
    check("visible ब/व difference is accepted", v.valid, v.reason)
    check("accepted pair really has different final pixels",
          v.rendered_raster_sha256 != v.target_raster_sha256)
    check("accepted pair also has different glyphs (diagnostic agrees)", v.glyphs_differ)


def test_identical_strings_are_not_a_mismatch():
    v = is_valid_mismatch("सुबह", "सुबह")
    check("identical strings rejected as mismatch",
          not v.valid and v.reason == "canonical_equal", v.reason)


def test_rejection_reasons_are_the_documented_set():
    documented = {"canonical_equal", "raster_identical", "rendering_error", "ok"}
    seen = {is_valid_mismatch(a, b).reason for a, b in
            [("क़", "क़"), ("सु‌बह", "सुबह"), ("सुवह", "सुबह")]}
    check("only documented rejection reasons are produced", seen <= documented, str(seen))


# ============================================================================================
# 9 · Canonicalisation semantics say exactly what the code does  (Controller review fix 4)
# ============================================================================================
def test_nfc_is_nfc_and_nothing_else():
    check("nfc does not strip leading whitespace", nfc("  सुबह") == "  सुबह")
    check("nfc does not strip trailing whitespace", nfc("सुबह\n") == "सुबह\n")
    check("nfc does compose the precomposed nukta pair",
          nfc(PRECOMPOSED_QA) == nfc(DECOMPOSED_QA))
    check("nfc is idempotent", nfc(nfc(PRECOMPOSED_QA)) == nfc(PRECOMPOSED_QA))


def test_whitespace_is_a_separate_named_rule():
    check("strip_outer_whitespace removes outer whitespace",
          strip_outer_whitespace("  सुबह \n") == "सुबह")
    check("strip_outer_whitespace leaves INTERNAL whitespace alone",
          strip_outer_whitespace(" सुबह की ") == "सुबह की")
    check("the comparison predicate does NOT strip",
          not canonical_equal("सुबह", "सुबह "))
    check("internal whitespace is a real difference",
          not canonical_equal("सुबह की", "सुबहकी"))


def test_comparison_predicate_is_canonical_not_codepoint_identity():
    a, b = PRECOMPOSED_QA, DECOMPOSED_QA
    check("the two nukta encodings are NOT codepoint-identical", a != b)
    check("but they ARE canonically equal, which is what the battery compares",
          canonical_equal(a, b))
    check("and they render identically, so canonical equality agrees with the pixels",
          raster_sha256(a) == raster_sha256(b))


# ============================================================================================
# 10 · Hard opportunities use distinct base words  (Controller review fix 5)
# ============================================================================================
def test_hard_opportunities_use_distinct_base_words():
    items, summary, _ = build_battery()
    hard = [i for i in items if i.get("hard_opportunity")]
    bases = [i["base_word"] for i in hard]
    check("every hard opportunity sits on a distinct base word",
          len(bases) == len(set(bases)), f"{len(bases)} items, {len(set(bases))} words")
    om = summary["opportunity_model"]
    check("summary reports hard item count and distinct hard base words as equal",
          om["hard_items"] == om["distinct_hard_base_words"],
          f"{om['hard_items']} vs {om['distinct_hard_base_words']}")
    check("summary reports both numbers explicitly, not only one",
          {"hard_items", "distinct_hard_base_words"} <= set(om))


def test_every_mismatch_uses_a_distinct_base_word():
    items, summary, _ = build_battery()
    mis = [i["base_word"] for i in items if i["expected_verdict"] == "mismatch"]
    check("no base word backs two mismatch items", len(mis) == len(set(mis)),
          f"{len(mis)} items, {len(set(mis))} words")
    om = summary["opportunity_model"]
    check("summary reports mismatch items == distinct mismatch base words",
          om["mismatch_items"] == om["distinct_mismatch_base_words"])


def test_hard_stratum_contains_no_implausible_items():
    items, _, _ = build_battery()
    hard = [i for i in items if i.get("hard_opportunity")]
    check("no hard item is a visibly-broken cluster",
          all(i["plausibility"] == "plausible" for i in hard))
    check("no hard item's IMAGE contains a dotted circle",
          all("uni25CC" not in i["rendered_shape"] for i in hard))


def test_bound_is_computed_from_the_opportunity_count():
    items, summary, _ = build_battery()
    om = summary["opportunity_model"]
    expected = round(zero_failure_upper_bound(om["distinct_hard_base_words"]), 4)
    check("the quoted hard bound is derived from distinct base-word opportunities",
          abs(om["hard_bound_if_zero_false_passes_95pct"] - expected) < 1e-9,
          f"{om['hard_bound_if_zero_false_passes_95pct']} vs {expected}")
    check("a 5% bound needs 59 zero-failure opportunities",
          opportunities_required(0.05) == 59, str(opportunities_required(0.05)))
    need = om["hard_opportunities_required_for_5pct"]
    check("the required word count follows from the hard-direction share, not a stored guess",
          om["validated_base_words_required_for_5pct"] == math.ceil(need / CORRUPT_IMAGE_SHARE),
          f"{om['validated_base_words_required_for_5pct']} vs "
          f"{math.ceil(need / CORRUPT_IMAGE_SHARE)}")


def test_epistemic_limit_is_recorded_with_the_bound():
    _, summary, _ = build_battery()
    text = " ".join(summary["opportunity_model"]["epistemic_limit"].lower().split())
    check("the bound ships with its epistemic limit",
          "not a probability sample" in text, text[:140])
    check("the limit says it is not a universal true error rate",
          "true error rate" in text, text[:140])


# ============================================================================================
# 11-14 · Battery invariants
# ============================================================================================
def test_build_is_deterministic():
    hashes = []
    for _ in range(2):
        with tempfile.TemporaryDirectory() as t:
            subprocess.run([sys.executable, str(HERE / "build_items.py"),
                            "--total", "30", "--out-dir", t],
                           capture_output=True, text=True)
            hashes.append(sha256_file(Path(t) / "items.jsonl"))
    check("two builds produce byte-identical manifests", hashes[0] == hashes[1])


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


def test_battery_is_balanced_and_trivial_strategies_fail():
    items, summary, _ = build_battery()
    n_match = sum(1 for i in items if i["expected_verdict"] == "match")
    n_mis = sum(1 for i in items if i["expected_verdict"] == "mismatch")
    check("battery is balanced 50/50", n_match == n_mis, f"{n_match} vs {n_mis}")
    check("'always match' scores exactly 50%", n_match / len(items) == 0.5)
    check("'always mismatch' scores exactly 50%", n_mis / len(items) == 0.5)

    mb = {i["base_word"] for i in items if i["expected_verdict"] == "match"}
    xb = {i["base_word"] for i in items if i["expected_verdict"] == "mismatch"}
    check("base words appear in both strata, so word identity is not a cue",
          len(mb & xb) > 0, f"overlap={len(mb & xb)}")

    by_img: dict[str, list] = {}
    for i in items:
        by_img.setdefault(i["image_file"], []).append(i)
    pairs = [v for v in by_img.values() if len(v) > 1]
    check("paired items exist (same pixels, opposite verdict)", len(pairs) > 0)
    check("every paired image carries opposite expected verdicts",
          all(len({x["expected_verdict"] for x in v}) > 1 for v in pairs))
    check("no duplicate image bytes across distinct files",
          summary["distinct_image_files"] == summary["distinct_image_hashes"])


def test_battery_content_invariants():
    items, summary, _ = build_battery()
    mismatches = [i for i in items if i["expected_verdict"] == "mismatch"]
    check("no mismatch item is invisible on the page",
          all(i["rendered_raster_sha256"] != i["target_raster_sha256"] for i in mismatches))
    check("every match item is truly canonically identical",
          all(canonical_equal(i["rendered_string"], i["target_string"])
              for i in items if i["expected_verdict"] == "match"))
    check("ground truth is recorded as constructed, not annotated",
          "by construction" in summary["ground_truth"])
    check("every item records the render spec it was built with",
          all(i["render_spec"]["font_file"] for i in items))


def test_class_and_group_coverage_is_reported():
    _, summary, _ = build_battery()
    check("failure classes are reported", len(summary["mismatch_by_class"]) >= 15,
          str(len(summary["mismatch_by_class"])))
    check("all five failure groups are represented",
          set(summary["mismatch_by_group"]) ==
          {"vowel_signs", "letters", "conjuncts", "dots_marks", "ra_forms"},
          str(sorted(summary["mismatch_by_group"])))
    check("the hard stratum's group split is reported separately",
          bool(summary.get("hard_by_group")))
    check("direction split is reported", set(summary["mismatch_by_direction"]) ==
          {"corrupt_image", "corrupt_target"}, str(summary["mismatch_by_direction"]))


# ============================================================================================
# 15 · No network, no model call
# ============================================================================================
def test_no_module_can_make_a_network_or_model_call():
    # Assembled from fragments so this scanner does not match its own pattern literal.
    clients = "|".join(["req" + "uests", "url" + "lib", "htt" + "px", "aioh" + "ttp",
                        "soc" + "ket", "htt" + "p\\.client"])
    keys = "|".join(["OPEN" + "AI", "ANTHRO" + "PIC", "OPENRO" + "UTER", "API" + "_KEY"])
    banned = re.compile(rf"\b({clients})\b|htt" + r"ps?://|" + keys, re.IGNORECASE)
    offenders = []
    for f in sorted(HERE.glob("*.py")):
        for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if line.lstrip().startswith("#"):
                continue
            if banned.search(line):
                offenders.append(f"{f.name}:{n}: {line.strip()[:80]}")
    check("no battery module references a network client, URL or API key", not offenders,
          "; ".join(offenders[:3]))


def test_build_writes_no_committed_temporary_images():
    _, _, d = build_battery()
    strays = [p.name for p in d.iterdir()
              if p.is_file() and p.suffix == ".png"]
    check("no loose PNG is written beside the manifests", not strays, str(strays[:5]))
    check("screening scratch directory is outside the build output",
          not str(devtext._SCRATCH).startswith(str(d)))


# ============================================================================================
# Plausibility rule
# ============================================================================================
def test_plausibility_allows_matra_after_nukta():
    """Regression: तोड़ा is a real word; a vowel sign after a nukta is ordinary Hindi."""
    check("तोड़ा is plausible", perturb.cluster_plausibility("तोड़ा") == "plausible")
    check("तोड़ना is plausible", perturb.cluster_plausibility("तोड़ना") == "plausible")


def test_plausibility_rejects_broken_clusters():
    cases = {
        "ोड़ना": "opens with a vowel sign",
        "तो़ना": "nukta on a vowel sign",
        "ॉम्बे": "opens with U+0949, a vowel sign MATRAS does not list",
        "तोड़न" + VIRAMA: "trailing bare virama",
        "इं्लीश": "virama hanging off an anusvara",
    }
    for s, why in cases.items():
        check(f"implausible: {why}",
              perturb.cluster_plausibility(s) == "implausible_cluster", s)
    for s in ("क्षेत्र", "अभिनन्दन", "तोड़ना", "बॉम्बे", "पार्किंग"):
        check(f"plausible: {s}", perturb.cluster_plausibility(s) == "plausible")


def test_shaper_catches_clusters_the_string_rule_missed():
    """The shaper's dotted circle is the authoritative 'this cluster is invalid' signal."""
    check("इं्लीश shapes with a dotted circle", shapes_with_dotted_circle("इं्लीश"))
    check("ॉम्बे shapes with a dotted circle", shapes_with_dotted_circle("ॉम्बे"))
    for good in ("इंग्लीश", "बॉम्बे", "तोड़ा", "क्षेत्र"):
        check(f"{good} shapes cleanly", not shapes_with_dotted_circle(good))


# ============================================================================================
# Operators
# ============================================================================================
def test_operators_change_the_string():
    base = "क्षेत्र"
    cands = perturb.all_candidates(base)
    check("operators produce candidates", len(cands) > 0)
    check("no candidate equals its base", all(not canonical_equal(c.text, base) for c in cands))
    check("every candidate carries a known class",
          all(c.failure_class in perturb.OPERATORS for c in cands))


def test_operator_enumeration_is_deterministic():
    a = [(c.failure_class, c.position, c.text) for c in perturb.all_candidates("अभिनन्दन")]
    b = [(c.failure_class, c.position, c.text) for c in perturb.all_candidates("अभिनन्दन")]
    check("candidate enumeration is stable across calls", a == b)


def test_conjunct_split_is_visible():
    """क्ष is one fused glyph; कष is two. The split must be visible, or the class is untestable."""
    joined, split = "क" + VIRAMA + "ष", "कष"
    check("conjunct split changes the glyph sequence", glyphs_differ(joined, split))
    check("conjunct split changes the final pixels",
          raster_sha256(joined) != raster_sha256(split))


def test_every_class_has_at_least_one_visible_instance():
    bases = ["क्षेत्र", "अभिनन्दन", "तोड़ना", "पार्किंग", "इंडिया", "संग्राहलय"]
    seen = set()
    for b in bases:
        for c in perturb.all_candidates(b):
            if c.failure_class not in seen and is_valid_mismatch(b, c.text).valid:
                seen.add(c.failure_class)
    unreachable = set(perturb.OPERATORS) - seen
    expected_gaps = {"NUKTA_REMOVE", "VISARGA_REMOVE", "NASAL_SUBSTITUTE", "NASAL_DELETE",
                     "REPH_TO_FULL_RA", "RAKAR_TO_FULL_RA", "INDEP_VOWEL_SUBSTITUTE",
                     "MATRA_SUBSTITUTE", "FULL_RA_TO_REPH"}
    check("no class is unreachable for an unexplained reason",
          unreachable <= expected_gaps, f"unexpectedly unreachable: {unreachable - expected_gaps}")


def main() -> int:
    print("Devanagari exactness battery — construction, blinding and provenance tests\n")
    for fn in sorted(
        (v for k, v in list(globals().items()) if k.startswith("test_") and callable(v)),
        key=lambda f: f.__name__,
    ):
        print(f"{fn.__name__}:")
        try:
            fn()
        except Exception as e:                                     # pragma: no cover
            check(f"{fn.__name__} raised", False, repr(e))
    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)} check(s):")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
