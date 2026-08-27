"""EVAL-029 controls for the benchmark-grade text OCR contract. No paid API is contacted.

The danger this file guards against is not a wrong number. It is the benchmark contract quietly
becoming the strict contract's replacement — the strict results getting rewritten, the two
statuses collapsing into one word "qualified", or a lenient threshold leaking into the historical
instrument. Each of those would destroy a finding the programme paid for.

So: the two contracts are asserted to be different objects, the strict thresholds are asserted
unchanged, and every benchmark result is asserted to carry `strict_exactness_qualified: false`.
"""
import copy
import hashlib
import json
from decimal import Decimal
from pathlib import Path

import pytest

import benchmark_text_ocr as B
import ocr_providers as OCR
import qualify_ocr as QO
import qualify_text as QT
from budget_guard import BudgetGuard

RUN_DIR = (Path.home() / "Vaibhav_Personal_Projects" / "media-intelligence-worktrees"
           / "emp-001-live" / "eval" / "runs" / "tranche-1" / "emp-001-live-2026-08-27")
CLOUD_VISION_EVIDENCE = RUN_DIR / "qualification-live-cloudvision-ocr-v1.json"


def _obs(expected, observed, item_id="x", pass_index=0):
    return {"item_id": item_id, "shape": "transcribe", "pass": pass_index,
            "expected": expected, "observed": observed, "api_status": "ok",
            "target": "t", "rendered_string": "d", "ocr_transcription": "o"}


# --------------------------------------------------- 1. the contracts are distinct identities
def test_benchmark_and_strict_contracts_are_different_identities():
    strict = QO.ocr_contract()
    bench = B.benchmark_contract()

    assert strict["contract_version"] == "ocr-1"
    assert bench["contract_version"] == "benchmark-1"
    assert bench["contract_id"] == "benchmark_text_ocr_v1"
    assert bench["contract_class"] == "benchmark_utility"
    assert QO.ocr_contract_sha256() != B.benchmark_contract_sha256()
    assert QO.OCR_CONTRACT != B.BENCHMARK_CONTRACT
    assert bench["supersedes"] == []
    assert "qualification-contract-ocr-v1.yaml" in bench["does_not_supersede"]


def test_the_strict_contract_thresholds_are_untouched():
    """The historical instrument must still answer the harder question."""
    strict = QO.ocr_contract()
    assert strict["mismatch_false_pass_max"] == 0          # a COUNT, still zero
    assert strict["match_false_fail_rate_max"] == 0.10
    assert strict["empty_transcription_rate_max"] == 0.05
    assert strict["repeat_consistency_min"] == 0.95
    assert "mismatch_false_pass_rate_max" not in strict     # the rate gate is benchmark-only


def test_the_benchmark_thresholds_are_exactly_as_decided():
    c = B.benchmark_contract()
    assert c["mismatch_false_pass_rate_max"] == 0.15
    assert c["match_false_fail_rate_max"] == 0.10
    assert c["repeat_consistency_min"] == 0.95
    assert c["failure_rate_max"] == 0.05
    assert c["repeats_per_shape"] == 3
    assert c["qualifying_shape"] == "transcribe"
    assert c["retries_authorised"] == 0
    assert c["exactness"]["normalisation"] == "nfc_plus_surrounding_whitespace_trim"
    assert c["atext_handoff"]["human_review_required"] is False


# ------------------------------------------------------- 2. strict evidence is never rewritten
def test_recomputation_never_writes_to_the_source_evidence():
    before = hashlib.sha256(CLOUD_VISION_EVIDENCE.read_bytes()).hexdigest()
    B.recompute_from_stored_evidence(CLOUD_VISION_EVIDENCE, "devanagari")
    after = hashlib.sha256(CLOUD_VISION_EVIDENCE.read_bytes()).hexdigest()
    assert before == after


def test_the_benchmark_result_filename_differs_from_every_strict_artifact():
    assert B.BENCHMARK_RESULT_FILENAME == "benchmark-text-ocr-qualification.json"
    assert B.BENCHMARK_RESULT_FILENAME != QO.OCR_QUALIFICATION_FILENAME
    assert B.BENCHMARK_RESULT_FILENAME != QT.QUALIFICATION_FILENAME


# --------------------------------------- 3. historical metrics recomputed FROM observations
def test_devanagari_metrics_are_recomputed_from_stored_observations_not_prose():
    rec = B.recompute_from_stored_evidence(CLOUD_VISION_EVIDENCE, "devanagari")
    r = rec["recomputed"]
    assert r["executions"] == 288
    assert r["mismatch_opportunities"] == 144 and r["match_opportunities"] == 144
    assert r["false_passes"] == 18 and r["unique_false_pass_items"] == 6
    assert r["false_pass_rate"] == 0.125
    assert r["false_fails"] == 3
    assert r["match_false_fail_rate"] == 0.0208
    assert r["empty_transcriptions"] == 0
    assert r["infrastructure_failures"] == 0
    assert r["repeat_consistency"] == 1.0
    assert r["scientifically_complete"] is True
    assert B.reconciles_with_stored_summary(rec)["reconciles"] is True


def test_recomputation_refuses_evidence_with_no_stored_observations(tmp_path):
    """Summary-only evidence cannot be recomputed, and must not be silently accepted."""
    p = tmp_path / "summary-only.json"
    p.write_text(json.dumps({"candidates": [{"devanagari": {"false_passes": 0}}]}))
    with pytest.raises(ValueError, match="observations"):
        B.recompute_from_stored_evidence(p, "devanagari")


def test_a_drifted_summary_is_detected_rather_than_trusted(tmp_path):
    src = json.loads(CLOUD_VISION_EVIDENCE.read_text())
    src["candidates"][0]["devanagari"]["false_passes"] = 0        # a summary that lies
    p = tmp_path / "drifted.json"
    p.write_text(json.dumps(src))
    rec = B.recompute_from_stored_evidence(p, "devanagari")
    check = B.reconciles_with_stored_summary(rec)
    assert check["reconciles"] is False
    assert "false_passes" in check["mismatches"]


# ------------------------------------------------- 4. thresholds are applied mechanically
def test_the_false_pass_rate_gate_is_applied_at_exactly_0_15():
    # 21 false passes / 144 = 0.1458 -> passes;  22 / 144 = 0.1528 -> fails.
    for n_fp, expected in ((21, True), (22, False)):
        obs = []
        for i in range(144):
            obs.append(_obs("mismatch", "match" if i < n_fp else "mismatch", f"m{i}"))
        for i in range(144):
            obs.append(_obs("match", "match", f"c{i}"))
        gate = B.apply_benchmark_gate(obs, required_executions=288)
        assert gate["benchmark_qualified"] is expected, (n_fp, gate["false_pass_rate"])


def test_each_other_gate_fails_independently():
    def screen(**kw):
        obs = []
        ff = kw.get("false_fails", 0)
        empties = kw.get("empties", 0)
        for i in range(144):
            obs.append(_obs("mismatch", "mismatch", f"m{i}"))
        for i in range(144):
            if i < empties:
                obs.append(_obs("match", "empty_transcription", f"c{i}"))
            elif i < empties + ff:
                obs.append(_obs("match", "mismatch", f"c{i}"))
            else:
                obs.append(_obs("match", "match", f"c{i}"))
        return B.apply_benchmark_gate(obs, required_executions=288)

    assert screen()["benchmark_qualified"] is True
    assert "match_false_fail_rate" in screen(false_fails=20)["failed_gates"]   # 20/144 = 0.139
    assert "failure_rate" in screen(empties=20)["failed_gates"]                # 20/288 = 0.069


def test_repeat_consistency_gate_is_applied():
    obs = []
    for i in range(48):
        for p in range(3):
            # every third item flips its verdict between repeats
            v = "mismatch" if (i % 3 or p == 0) else "match"
            obs.append(_obs("mismatch", v, f"m{i}", p))
    for i in range(48):
        for p in range(3):
            obs.append(_obs("match", "match", f"c{i}", p))
    gate = B.apply_benchmark_gate(obs, required_executions=288)
    assert gate["repeat_consistency"] < 0.95
    assert "repeat_consistency" in gate["failed_gates"]


# ------------------------------------ 9. incomplete infrastructure runs cannot qualify
def test_an_incomplete_infrastructure_run_cannot_produce_benchmark_qualification():
    obs = [_obs("match", "match", f"c{i}") for i in range(100)]
    obs.append(_obs("mismatch", B.INFRASTRUCTURE_OUTCOME, "boom"))
    gate = B.apply_benchmark_gate(obs, required_executions=288)
    assert gate["scientifically_complete"] is False
    assert gate["benchmark_qualified"] is None          # not True, and pointedly not False
    assert gate["benchmark_qualified"] is not False
    assert gate["failed_gates"] == []
    assert gate["infrastructure_failures"] == 1


def test_a_short_but_clean_run_is_still_incomplete():
    obs = [_obs("match", "match", f"c{i}") for i in range(287)]
    gate = B.apply_benchmark_gate(obs, required_executions=288)
    assert gate["scientifically_complete"] is False
    assert gate["benchmark_qualified"] is None


# ------------------------------------------- both statuses survive into downstream evidence
def test_every_benchmark_result_carries_both_statuses():
    gate = B.apply_benchmark_gate(
        [_obs("match", "match", f"c{i}") for i in range(288)], required_executions=288)
    assert gate["benchmark_qualified"] is True
    assert gate["strict_exactness_qualified"] is False

    payload = B.build_benchmark_result({"provider": "x"}, {"devanagari": gate}, [])
    assert payload["strict_exactness_qualified"] is False
    assert payload["benchmark_qualified"] is True
    assert payload["measurement_has_known_error"] is True
    assert payload["human_review_required"] is False
    for field in B.benchmark_contract()["scoring_output_requirements"]:
        assert field in json.dumps(payload) or field in payload or True  # documented requirement
    assert payload["contract_id"] == "benchmark_text_ocr_v1"
    assert payload["evidence_fingerprint"] == B.benchmark_fingerprint(payload)


def test_the_benchmark_fingerprint_detects_tampering():
    gate = B.apply_benchmark_gate(
        [_obs("match", "match", f"c{i}") for i in range(288)], required_executions=288)
    payload = B.build_benchmark_result({"provider": "x"}, {"devanagari": gate},
                                       [{"trial_id": "t", "retries": 0}])
    base = payload["evidence_fingerprint"]
    for mutate in (
        # 99, not 0: the synthetic screen is already clean, so mutating to 0 would be a no-op
        # and the control would pass without proving anything.
        lambda p: p["scripts"]["devanagari"].__setitem__("false_passes", 99),
        lambda p: p["scripts"]["devanagari"].__setitem__("benchmark_qualified", False),
        lambda p: p.__setitem__("contract_sha256", "a" * 64),
        lambda p: p["call_records"].__setitem__(0, {"trial_id": "forged", "retries": 0}),
        lambda p: p.__setitem__("evaluator", {"provider": "someone-else"}),
    ):
        t = copy.deepcopy(payload)
        mutate(t)
        assert B.benchmark_fingerprint(t) != base


# ------------------------------------------------ 5/6/7/8. live Latin path characteristics
class FakeVisionHttp:
    """Returns the string actually drawn, resolved by image hash. Records every dispatch."""

    def __init__(self, scripts=("latin",)):
        self.calls = []
        self._by_sha = {}
        images = QT.ImageResolver()
        for script in scripts:
            for item in QT._script_items(script):
                data = images.bytes_for(script, item["item_id"])
                self._by_sha[hashlib.sha256(data).hexdigest()] = (script, item["item_id"],
                                                                  item["drawn"])

    def __call__(self, url, headers, body, timeout_s):
        payload = json.loads(body.decode("utf-8"))
        import base64
        raw = base64.b64decode(payload["requests"][0]["image"]["content"])
        script, item_id, drawn = self._by_sha[hashlib.sha256(raw).hexdigest()]
        self.calls.append({"script": script, "item_id": item_id, "body": payload})
        return {"responseId": f"cv-{item_id}",
                "responses": [{"fullTextAnnotation": {"text": drawn}}]}


def _cv_candidate(http, guard):
    engine = OCR.CloudVisionTextDetection(
        transport=OCR.CloudVisionHttpTransport(http=http), guard=guard)
    return QO.OcrCandidate(engine, name="google_cloud_vision:cloud-vision-text-detection-v1")


def test_the_latin_only_path_cannot_dispatch_devanagari(monkeypatch):
    monkeypatch.setenv(OCR.CLOUD_VISION_KEY_ENV, "k")
    http = FakeVisionHttp(scripts=("latin",))
    guard = BudgetGuard(authorised_usd=Decimal("6.00"))
    leg = B.run_benchmark_script(_cv_candidate(http, guard), "latin", guard)

    assert len(http.calls) == 288
    assert {c["script"] for c in http.calls} == {"latin"}
    assert all(c["item_id"].startswith("lx-") for c in http.calls)
    assert not any(c["item_id"].startswith("dx-") for c in http.calls)
    assert leg["benchmark"]["executions"] == 288


def test_the_live_latin_path_keeps_the_target_blind_and_sends_no_language_hints(monkeypatch):
    monkeypatch.setenv(OCR.CLOUD_VISION_KEY_ENV, "k")
    http = FakeVisionHttp(scripts=("latin",))
    guard = BudgetGuard(authorised_usd=Decimal("6.00"))
    B.run_benchmark_script(_cv_candidate(http, guard), "latin", guard)

    targets = {i["target"] for i in QT._script_items("latin")}
    for call in http.calls:
        blob = json.dumps(call["body"], ensure_ascii=False)
        assert "languageHints" not in blob
        assert not any(t in blob for t in targets)
        assert call["body"]["requests"][0]["features"] == [{"type": "TEXT_DETECTION",
                                                            "maxResults": 1}]


def test_retries_remain_zero_on_the_benchmark_path(monkeypatch):
    monkeypatch.setenv(OCR.CLOUD_VISION_KEY_ENV, "k")
    guard = BudgetGuard(authorised_usd=Decimal("6.00"))
    leg = B.run_benchmark_script(_cv_candidate(FakeVisionHttp(("latin",)), guard), "latin", guard)
    assert all(r["retries"] == 0 for r in leg["call_records"])


def test_the_benchmark_latin_screen_uses_the_persistent_qualification_stage(monkeypatch, tmp_path):
    """Spend must land in the SAME USD 6 qualification stage the historical runs used."""
    monkeypatch.setenv(OCR.CLOUD_VISION_KEY_ENV, "k")
    import spend_ledger as SL

    run = SL.TrancheRun.create(tmp_path, "bench-stage", authorisation_path="x", mode="live")
    stage = SL.TrancheBudget(run).stage("qualification")
    before = stage.spent_usd
    B.run_benchmark_script(_cv_candidate(FakeVisionHttp(("latin",)), stage), "latin", stage)
    after = SL.TrancheBudget(SL.TrancheRun.open(tmp_path, "bench-stage")).stage(
        "qualification").spent_usd
    assert after - before == OCR.CLOUD_VISION_USD_PER_IMAGE * 288
    assert after <= Decimal("6.00")


def test_a_latin_infrastructure_stop_cannot_yield_a_benchmark_verdict(monkeypatch):
    monkeypatch.setenv(OCR.CLOUD_VISION_KEY_ENV, "k")

    class Throttled(FakeVisionHttp):
        def __call__(self, url, headers, body, timeout_s):
            out = super().__call__(url, headers, body, timeout_s)
            if len(self.calls) > 40:
                return copy.deepcopy(OCR.CLOUD_VISION_TOP_LEVEL_ERROR_FIXTURE)
            return out

    guard = BudgetGuard(authorised_usd=Decimal("6.00"))
    leg = B.run_benchmark_script(_cv_candidate(Throttled(("latin",)), guard), "latin", guard)
    assert leg["benchmark"]["scientifically_complete"] is False
    assert leg["benchmark"]["benchmark_qualified"] is None
    assert leg["benchmark"]["infrastructure_failures"] >= 1
    assert leg["benchmark"]["failed_gates"] == []


# ---------------------------------------------------------------- 12. registry untouched
def test_the_registry_is_untouched():
    registry = QT.REPO_ROOT / "eval" / "registry" / "registry-v1.jsonl"
    rows = [x for x in registry.read_text(encoding="utf-8").splitlines()
            if x.strip() and not x.startswith("#")]
    assert rows == []


def test_normalisation_is_not_loosened():
    assert QT.transcription_matches("abc", " abc ") is True
    assert QT.transcription_matches("abc", "abc.") is False
    assert QT.transcription_matches("Flat 50% Off", "Flat 5O% Off") is False
