"""Negative controls for the corrected Canon V1 value gate (CANON-V1-CORRECTION-PASS).

These tests exist because every one of them corresponds to a way the gate could quietly produce a
wrong answer. They assert on the scorer's real output, run against synthetic fixtures — never
against a model output or a human verdict, neither of which exists.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
GATE = ROOT / "canon/experiments/v1/value-gate"
SCORER = GATE / "score_value_gate.py"
DRY = GATE / "dry-run"


def score(fixture: str):
    r = subprocess.run([sys.executable, str(SCORER), str(DRY / fixture)],
                       capture_output=True, text=True, cwd=ROOT)
    return r.returncode, (json.loads(r.stdout) if r.stdout.strip() else {})


# ── C-C5 · exactly two independent reviewers ────────────────────────────────────

def test_single_reviewer_fails_closed():
    code, out = score("single-reviewer.json")
    assert code == 1
    assert out["status"] == "INCOMPLETE"
    assert any("independent reviewers are required" in e for e in out["errors"])


def test_same_reviewer_twice_is_not_two_reviewers():
    code, out = score("duplicate-reviewer.json")
    assert code == 1
    assert out["status"] == "INCOMPLETE"
    assert any("duplicate reviewer_id" in e for e in out["errors"])


def test_reviewer_disagreement_is_not_a_clear_win():
    """One clear win plus one non-win must not count, and must be reported as disagreement."""
    code, out = score("reviewer-disagreement.json")
    assert code == 0
    assert out["coverage_probes"]["unanimous_canon_clear_wins"] == 4
    assert out["coverage_probes"]["band"] == "mixed"
    assert len(out["reviewer_disagreement_pairs"]) == 1


def test_reviewer_judgements_are_not_averaged():
    _, out = score("coverage-5of7-continue.json")
    assert "no_averaging" in out["clear_win_rule"]
    for pair in out["per_pair"]:
        assert len(pair["reviewers"]) == 2          # each reviewer preserved separately
        for judgement in pair["reviewers"].values():
            assert isinstance(judgement["canon_clear_win"], bool)


# ── C-C6 · only coverage probes vote on continuation ────────────────────────────

@pytest.mark.parametrize("fixture,wins,band", [
    ("coverage-5of7-continue.json", 5, "continue"),
    ("coverage-4of7-mixed.json", 4, "mixed"),
    ("coverage-3of7-stop.json", 3, "stop"),
])
def test_frozen_coverage_bands(fixture, wins, band):
    code, out = score(fixture)
    assert code == 0
    assert out["coverage_probes"]["total"] == 7
    assert out["coverage_probes"]["unanimous_canon_clear_wins"] == wins
    assert out["coverage_probes"]["band"] == band
    assert out["headline"] == band


def test_gap_probe_wins_do_not_rescue_a_failing_band():
    """All five gap probes winning must not turn a 3/7 coverage result into continue."""
    code, out = score("gap-probes-do-not-rescue.json")
    assert code == 0
    assert out["gap_probes"]["unanimous_canon_clear_wins"] == 5
    assert out["coverage_probes"]["unanimous_canon_clear_wins"] == 3
    assert out["headline"] == "stop"
    assert out["gap_probes"]["counted_toward_continuation"] is False


def test_gap_probe_losses_do_not_sink_a_passing_band():
    """Losing every gap probe must not stop expansion — the knowledge is known to be absent."""
    code, out = score("gap-probes-do-not-sink.json")
    assert code == 0
    assert out["gap_probes"]["unanimous_canon_clear_wins"] == 0
    assert out["headline"] == "continue"


def test_probe_split_matches_the_manifest():
    _, out = score("coverage-5of7-continue.json")
    assert out["coverage_probes"]["total"] == 7
    assert out["gap_probes"]["total"] == 5


# ── Intent safety is global ─────────────────────────────────────────────────────

def test_intent_regression_on_a_gap_probe_still_blocks_continuation():
    """Intent safety is not confined to the pairs that vote."""
    code, out = score("intent-regression-overrides.json")
    assert code == 0
    assert out["coverage_probes"]["unanimous_canon_clear_wins"] == 5   # would otherwise continue
    assert out["headline"] == "intent_regression"
    assert out["intent_safety"]["blocks_automatic_continuation"] is True
    assert out["intent_safety"]["canon_intent_regression_pairs"]


# ── Fail closed on incomplete input ─────────────────────────────────────────────

@pytest.mark.parametrize("fixture,marker", [
    ("missing-pair.json", "missing verdict is not a tie"),
    ("missing-dimension.json", "not judged"),
])
def test_incomplete_input_fails_closed(fixture, marker):
    code, out = score(fixture)
    assert code == 1
    assert out["status"] == "INCOMPLETE"
    assert any(marker in e for e in out["errors"])


def test_no_verdicts_refuses_to_infer_a_result():
    r = subprocess.run([sys.executable, str(SCORER), str(DRY / "does-not-exist.json")],
                       capture_output=True, text=True, cwd=ROOT)
    out = json.loads(r.stdout)
    assert out["status"] == "NO_VERDICTS"
    assert "headline" not in out and "coverage_probes" not in out


def test_position_bias_alone_cannot_reach_continue():
    """A reviewer who always picks whichever plan is shown first must not reach `continue`.

    Overall 6/6 balance is NOT sufficient and this test proved it: the first corrected build was a
    tidy 6/6 across 12 pairs while showing Canon first on 5 of the 7 coverage probes — the only ones
    that vote — so pure position bias scored 5/7 and reached `continue`. Blinding is now balanced
    within each stratum, with any odd leftover going to the control arm.
    """
    code, out = score("position-bias-always-A.json")
    assert code == 0
    assert out["headline"] != "continue"


def test_blinding_is_balanced_within_the_voting_stratum():
    manifest = json.loads((GATE / "run-manifest.json").read_text())
    by_role = manifest["blinding"]["canon_first_by_role"]
    assert manifest["blinding"]["stratified_by"] == "gate_role"
    # Canon may never be shown first on more than half the pairs of any stratum.
    assert by_role["coverage_probe"] <= 7 // 2
    assert by_role["gap_probe"] <= 5 // 2


def test_synthetic_input_is_never_reported_as_a_result():
    _, out = score("coverage-5of7-continue.json")
    assert out["status"] == "DUMMY_DRY_RUN_NOT_A_RESULT"
    assert "not evidence about Canon" in out["warning"]


def test_no_statistical_claim_is_emitted():
    """No rate or interval may be reported. The disclaimer naming those terms is not a claim, so it
    is excluded from the scan — otherwise the test fails on the very text that prevents the error."""
    _, out = score("coverage-5of7-continue.json")
    assert "NOT a population estimate" in out["statistical_note"]
    scanned = {k: v for k, v in out.items() if k not in ("statistical_note", "warning")}
    blob = json.dumps(scanned)
    for forbidden in ("confidence_interval", "p_value", "confidence interval", "margin of error"):
        assert forbidden not in blob


# ── C-C4 · blinding is actually sealed ──────────────────────────────────────────

def test_real_run_preparation_refuses_contaminated_controls():
    r = subprocess.run([sys.executable, str(GATE / "prepare_real_run.py"),
                        "--key-out", "/tmp/canon-key-test.json"],
                       capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 1
    out = json.loads(r.stdout)
    assert out["status"] == "REFUSED"
    assert any("generic-contexts-real" in e for e in out["errors"])


def test_real_run_key_may_not_be_written_inside_the_repository():
    real = GATE / "generic-contexts-real"
    created = not real.exists()
    if created:
        real.mkdir()
    try:
        r = subprocess.run([sys.executable, str(GATE / "prepare_real_run.py"),
                            "--key-out", str(GATE / "key.json")],
                           capture_output=True, text=True, cwd=ROOT)
        assert r.returncode == 1
        out = json.loads(r.stdout)
        assert any("inside the repository" in e for e in out["errors"])
    finally:
        if created:
            real.rmdir()


def test_no_committed_real_run_artifact_reveals_the_mapping():
    """Negative control: nothing committed for a real run may disclose which arm is A."""
    for name in ("real-run-manifest.json", "real-reviewer-packet.json"):
        f = GATE / name
        if not f.exists():
            continue
        blob = f.read_text()
        assert "oracle_canon" not in blob or '"A"' not in blob, \
            f"{name} appears to disclose the arm mapping"
        doc = json.loads(blob)
        if name == "real-run-manifest.json":
            assert "mapping" not in json.dumps(doc.get("blinding", {}))
            assert doc["blinding"]["sealed"] is True


def test_reviewer_packet_template_never_names_an_arm():
    packet = json.loads((GATE / "reviewer-packet-template.json").read_text())
    blob = json.dumps(packet)
    for arm in ("oracle_canon", "generic-contexts", "oracle-contexts"):
        assert arm not in blob, f"reviewer packet leaks arm identity via {arm!r}"


def test_committed_dry_run_key_is_marked_invalid_for_real_use():
    key = json.loads((GATE / "blinding-key.json").read_text())
    assert key["status"] == "DRY_RUN_ONLY_INVALIDATED_FOR_REAL_USE"


# ── C-C3 · the control-authoring packet leaks no Canon ──────────────────────────

def test_control_authoring_packet_is_free_of_canon():
    packet = json.loads((GATE / "control-authoring-input.json").read_text())
    blob = json.dumps(packet, ensure_ascii=False)
    assert "authoritative_intent" not in blob
    for src in sorted((ROOT / "canon/knowledge/current").iterdir()):
        assert src.name not in blob, f"packet names accepted source {src.name}"
    for oracle in sorted((GATE / "oracle-contexts").glob("*.md")):
        for line in oracle.read_text().splitlines():
            line = line.strip()
            if len(line) > 60:
                assert line not in blob, f"packet reproduces oracle text from {oracle.name}"


def test_control_packet_builder_detects_injected_canon():
    """The leakage check must actually fire — a check that never fails proves nothing."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("bcp", GATE / "build_control_packet.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    terms = mod.leakage_terms()
    assert "murch-blink-p1-25" in terms
    assert "ondaatje" in terms
    assert "context" not in terms      # generic English words must not trip the check
    assert len(terms) > 20


def test_contaminated_controls_are_marked_and_not_referenced_as_real():
    d = GATE / "generic-contexts-DRYRUN-CONTAMINATED"
    assert d.is_dir()
    assert not (GATE / "generic-contexts").exists(), "the ambiguous original directory must be gone"
    for f in d.glob("BR-*.md"):
        assert "CONTAMINATED FOR THE REAL GATE" in f.read_text()
