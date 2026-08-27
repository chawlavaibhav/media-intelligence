"""EVAL-030 controls. No paid API is contacted; no image is generated.

The two failures that would matter most here are silent ones: scoring a file that is not the
sealed artifact (which would attribute a measurement to the wrong generator), and letting a
"benchmark" number be read as a certification. Both are asserted against directly.
"""
import copy
import hashlib
import json
from decimal import Decimal
from pathlib import Path

import pytest

import ocr_providers as OCR
import qualify_text as QT
import score_atex_benchmark as S
from budget_guard import BudgetGuard


def _manifest():
    return S.sealed_manifest()


class FakeVisionHttp:
    """Stands where the Cloud Vision socket would be. Returns a scripted transcription."""

    def __init__(self, text_for=None, default="", error_for=None):
        self.calls = []
        self.text_for = text_for or {}
        self.default = default
        self.error_for = error_for or set()

    def __call__(self, url, headers, body, timeout_s):
        import base64
        payload = json.loads(body.decode("utf-8"))
        raw = base64.b64decode(payload["requests"][0]["image"]["content"])
        sha = hashlib.sha256(raw).hexdigest()
        self.calls.append({"sha256": sha, "body": payload, "url": url})
        if sha in self.error_for:
            return copy.deepcopy(OCR.CLOUD_VISION_TOP_LEVEL_ERROR_FIXTURE)
        text = self.text_for.get(sha, self.default)
        if not text:
            return {"responseId": "cv-x", "responses": [{"textAnnotations": []}]}
        return {"responseId": "cv-x", "responses": [{"fullTextAnnotation": {"text": text}}]}


def _perfect_http():
    """Every artifact transcribes to its own target — a synthetic 16/16."""
    m = _manifest()
    items = {i["item_id"]: i["target_string"] for i in m["frozen_items"]}
    mapping = {}
    for e in m["artifacts"]:
        data = (S.SEALED_ROOT / e["relative_path"]).read_bytes()
        mapping[hashlib.sha256(data).hexdigest()] = items[e["item_id"]]
    return FakeVisionHttp(text_for=mapping)


# ------------------------------------------------------------------ sealed inputs are intact
def test_all_sixteen_sealed_artifacts_exist_and_match_their_hashes():
    m = _manifest()
    assert len(m["artifacts"]) == 16
    assert m["missing_coordinates"] == []
    for e in m["artifacts"]:
        data = S.verify_artifact(e)
        assert hashlib.sha256(data).hexdigest() == e["sha256"]
        assert len(data) == e["bytes"]


def test_the_manifest_covers_both_routes_and_all_four_items():
    m = _manifest()
    assert sorted(r["route"] for r in m["routes"].values()) == [
        "fal-ai/ideogram/v3", "openai/gpt-image-2"]
    assert sorted(i["item_id"] for i in m["frozen_items"]) == [
        "ATEXT-01", "ATEXT-02", "ATEXT-03", "ATEXT-04"]
    slots = {}
    for e in m["artifacts"]:
        slots.setdefault(e["slot"], []).append(e["item_id"])
    assert {k: len(v) for k, v in slots.items()} == {"IMG-01": 8, "IMG-02": 8}


# ------------------------------------------------------------- verification precedes dispatch
def test_a_missing_artifact_is_refused_and_never_substituted(tmp_path):
    e = dict(_manifest()["artifacts"][0])
    with pytest.raises(S.ArtifactRefused, match="missing"):
        S.verify_artifact(e, root=tmp_path)


def test_a_hash_mismatch_is_refused(tmp_path):
    m = _manifest()
    e = dict(m["artifacts"][0])
    target = tmp_path / e["relative_path"]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(b"not the sealed artifact")
    with pytest.raises(S.ArtifactRefused, match="sha256 mismatch"):
        S.verify_artifact(e, root=tmp_path)


def test_a_tampered_artifact_stops_the_run_before_any_evaluator_call(monkeypatch):
    monkeypatch.setenv(OCR.CLOUD_VISION_KEY_ENV, "k")
    http = _perfect_http()
    real = S.verify_artifact

    def poisoned(entry, root=S.SEALED_ROOT):
        if entry["coordinate_id"].endswith("ATEXT-02:r0"):
            raise S.ArtifactRefused("sha256 mismatch (simulated)")
        return real(entry, root)

    monkeypatch.setattr(S, "verify_artifact", poisoned)
    with pytest.raises(S.ArtifactRefused):
        S.score_sealed_atex(http=http, guard=BudgetGuard(authorised_usd=Decimal("1")))
    # It refused partway; the refusal happened instead of a dispatch, not after one.
    assert len(http.calls) < 16


# ------------------------------------------------------------------------- no generation
def test_the_scorer_module_cannot_generate():
    import ast
    tree = ast.parse(Path(S.__file__).read_text(encoding="utf-8"))
    # Strip docstrings: the module explains at length what it refuses to do, and that prose
    # naturally names the very things the executable code must not contain.
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if (node.body and isinstance(node.body[0], ast.Expr)
                    and isinstance(node.body[0].value, ast.Constant)
                    and isinstance(node.body[0].value.value, str)):
                node.body.pop(0)
    code = ast.unparse(tree)
    for forbidden in ("generate_atex", "FAL_KEY", "fal.run", "fal-ai/ideogram",
                      "openai/gpt-image", "num_images"):
        assert forbidden not in code, forbidden
    # Check THIS module's own import statements, not the shared process sys.modules: pytest runs
    # every test file in one interpreter, so a sibling test importing the generator would make a
    # global check fail while saying nothing about this module.
    imported = set()
    for node in ast.walk(ast.parse(Path(S.__file__).read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            imported.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
    assert not any("generate" in m or "fal" in m.lower() for m in imported), sorted(imported)


def test_scoring_invokes_no_generator_and_touches_no_fal_route(monkeypatch):
    monkeypatch.setenv(OCR.CLOUD_VISION_KEY_ENV, "k")
    monkeypatch.delenv("FAL_KEY", raising=False)

    import providers as P
    if hasattr(P, "FalImageGenerator"):
        def explode(*a, **k):
            raise AssertionError("a generator was constructed during EVAL-030")
        monkeypatch.setattr(P, "FalImageGenerator", explode)

    payload = S.score_sealed_atex(http=_perfect_http(),
                                  guard=BudgetGuard(authorised_usd=Decimal("1")))
    assert payload["generation"]["regenerated_anything"] is False
    assert payload["generation"]["generator_invoked"] is False


def test_artifact_bytes_on_disk_are_unchanged_by_scoring(monkeypatch):
    monkeypatch.setenv(OCR.CLOUD_VISION_KEY_ENV, "k")
    m = _manifest()
    before = {e["relative_path"]: hashlib.sha256(
        (S.SEALED_ROOT / e["relative_path"]).read_bytes()).hexdigest() for e in m["artifacts"]}
    S.score_sealed_atex(http=_perfect_http(), guard=BudgetGuard(authorised_usd=Decimal("1")))
    after = {e["relative_path"]: hashlib.sha256(
        (S.SEALED_ROOT / e["relative_path"]).read_bytes()).hexdigest() for e in m["artifacts"]}
    assert before == after


# ------------------------------------------------------------------- evaluator discipline
def test_the_target_is_never_sent_and_no_language_hints_are_used(monkeypatch):
    monkeypatch.setenv(OCR.CLOUD_VISION_KEY_ENV, "k")
    http = _perfect_http()
    S.score_sealed_atex(http=http, guard=BudgetGuard(authorised_usd=Decimal("1")))
    targets = {i["target_string"] for i in _manifest()["frozen_items"]}
    assert len(http.calls) == 16
    for call in http.calls:
        blob = json.dumps(call["body"], ensure_ascii=False)
        assert "languageHints" not in blob
        for t in targets:
            assert t not in blob
        assert call["body"]["requests"][0]["features"] == [
            {"type": "TEXT_DETECTION", "maxResults": 1}]


def test_each_artifact_is_scored_exactly_once(monkeypatch):
    monkeypatch.setenv(OCR.CLOUD_VISION_KEY_ENV, "k")
    http = _perfect_http()
    payload = S.score_sealed_atex(http=http, guard=BudgetGuard(authorised_usd=Decimal("1")))
    assert len(http.calls) == 16
    assert len({c["sha256"] for c in http.calls}) == 16
    assert len({r["coordinate_id"] for r in payload["rows"]}) == 16


def test_retries_remain_zero(monkeypatch):
    monkeypatch.setenv(OCR.CLOUD_VISION_KEY_ENV, "k")
    payload = S.score_sealed_atex(http=_perfect_http(),
                                  guard=BudgetGuard(authorised_usd=Decimal("1")))
    assert all(r["retries"] == 0 for r in payload["rows"])


def test_evaluator_spend_cannot_exceed_the_authorised_maximum(monkeypatch):
    monkeypatch.setenv(OCR.CLOUD_VISION_KEY_ENV, "k")
    guard = BudgetGuard(authorised_usd=S.MAX_EVALUATOR_SPEND)
    payload = S.score_sealed_atex(http=_perfect_http(), guard=guard)
    assert S.MAX_EVALUATOR_SPEND == Decimal("0.0240")
    assert Decimal(payload["spend"]["evaluator_usd"]) <= S.MAX_EVALUATOR_SPEND
    assert guard.spent_usd <= guard.authorised_usd


# ---------------------------------------------------------------------------- comparison
def test_exact_match_uses_the_frozen_normalisation(monkeypatch):
    monkeypatch.setenv(OCR.CLOUD_VISION_KEY_ENV, "k")
    m = _manifest()
    items = {i["item_id"]: i["target_string"] for i in m["frozen_items"]}
    mapping = {}
    for e in m["artifacts"]:
        sha = hashlib.sha256((S.SEALED_ROOT / e["relative_path"]).read_bytes()).hexdigest()
        t = items[e["item_id"]]
        # outer whitespace must still match; a trailing period must not
        mapping[sha] = f"  {t}  " if e["slot"] == "IMG-01" else f"{t}."
    payload = S.score_sealed_atex(http=FakeVisionHttp(text_for=mapping),
                                  guard=BudgetGuard(authorised_usd=Decimal("1")))
    by_slot = {}
    for r in payload["rows"]:
        by_slot.setdefault(r["slot"], []).append(r["exact_match"])
    assert all(by_slot["IMG-01"]), "outer whitespace must be trimmed"
    assert not any(by_slot["IMG-02"]), "a trailing period is not an exact match"


def test_an_empty_transcription_is_not_an_exact_match(monkeypatch):
    monkeypatch.setenv(OCR.CLOUD_VISION_KEY_ENV, "k")
    payload = S.score_sealed_atex(http=FakeVisionHttp(default=""),
                                  guard=BudgetGuard(authorised_usd=Decimal("1")))
    assert all(r["exact_match"] is False for r in payload["rows"])
    assert payload["scoring"]["exact_matches"] == 0


# ------------------------------------------------------------------- fail-closed on ambiguity
def test_an_ambiguous_evaluator_failure_stops_and_is_still_costed(monkeypatch):
    monkeypatch.setenv(OCR.CLOUD_VISION_KEY_ENV, "k")
    m = _manifest()
    third = m["artifacts"][2]
    sha = hashlib.sha256((S.SEALED_ROOT / third["relative_path"]).read_bytes()).hexdigest()
    base = _perfect_http()

    class Malformed(FakeVisionHttp):
        def __call__(self, url, headers, body, timeout_s):
            out = super().__call__(url, headers, body, timeout_s)
            if self.calls[-1]["sha256"] == sha:
                return copy.deepcopy(OCR.CLOUD_VISION_MALFORMED_FIXTURE)
            return out

    http = Malformed(text_for=base.text_for)
    guard = BudgetGuard(authorised_usd=Decimal("1"))
    payload = S.score_sealed_atex(http=http, guard=guard)

    assert payload["scoring"]["complete"] is False
    assert payload["scoring"]["stopped_reason"] == "ambiguous_dispatch"
    failed = [r for r in payload["rows"] if r["evaluator_failed"]]
    assert len(failed) == 1
    assert failed[0]["ambiguous_dispatch"] is True
    assert failed[0]["retries"] == 0
    assert Decimal(failed[0]["evaluator_billed_usd"]) > 0      # persisted AND costed
    assert failed[0]["counts_toward_generator_score"] is False  # not a generator miss
    assert payload["scoring"]["unmeasured_evaluator_failures"] == 1
    assert guard.spent_usd > 0


# ---------------------------------------------------------------- evidence carries uncertainty
def test_every_row_carries_the_evaluator_error_rates_and_both_statuses(monkeypatch):
    monkeypatch.setenv(OCR.CLOUD_VISION_KEY_ENV, "k")
    payload = S.score_sealed_atex(http=_perfect_http(),
                                  guard=BudgetGuard(authorised_usd=Decimal("1")))
    for r in payload["rows"]:
        for field in ("slot", "generator_route", "item_id", "script", "target_string",
                      "repeat_index", "artifact_sha256", "evaluator_identity",
                      "evaluator_contract_id", "evaluator_contract_sha256", "ocr_transcription",
                      "exact_match", "evaluator_cost_ref", "evaluator_false_pass_rate",
                      "evaluator_false_fail_rate"):
            assert field in r, field
        assert r["benchmark_qualified"] is True
        assert r["strict_exactness_qualified"] is False
        assert r["measurement_has_known_error"] is True
        expected = 0.125 if r["script"] == "devanagari" else 0.1042
        assert r["evaluator_false_pass_rate"] == expected
    assert payload["strict_exactness_qualified"] is False
    assert payload["may_populate_registry"] is False


def test_the_raw_rate_is_not_adjusted_for_evaluator_error(monkeypatch):
    monkeypatch.setenv(OCR.CLOUD_VISION_KEY_ENV, "k")
    payload = S.score_sealed_atex(http=_perfect_http(),
                                  guard=BudgetGuard(authorised_usd=Decimal("1")))
    s = payload["scoring"]
    assert s["exact_matches"] == 16
    assert s["unmeasured_evaluator_failures"] == 0
    # raw count / raw attempts, with no correction factor applied anywhere
    assert s["observed_exact_match_rate"] == round(16 / 16, 4) == 1.0
    assert "corrected" not in json.dumps(payload).lower().replace("uncorrected", "")


def test_the_scoring_fingerprint_detects_tampering(monkeypatch):
    monkeypatch.setenv(OCR.CLOUD_VISION_KEY_ENV, "k")
    payload = S.score_sealed_atex(http=_perfect_http(),
                                  guard=BudgetGuard(authorised_usd=Decimal("1")))
    base = payload["evidence_fingerprint"]
    for mutate in (
        lambda p: p["rows"][0].__setitem__("exact_match", not p["rows"][0]["exact_match"]),
        lambda p: p["rows"][0].__setitem__("ocr_transcription", "forged"),
        lambda p: p["rows"][0].__setitem__("artifact_sha256", "a" * 64),
        lambda p: p["scoring"].__setitem__("exact_matches", 99),
        lambda p: p["by_generator_route"].__setitem__("openai/gpt-image-2", {"exact": 99}),
    ):
        t = copy.deepcopy(payload)
        mutate(t)
        assert S.scoring_fingerprint(t) != base


def test_aggregates_split_by_route_script_and_item(monkeypatch):
    monkeypatch.setenv(OCR.CLOUD_VISION_KEY_ENV, "k")
    payload = S.score_sealed_atex(http=_perfect_http(),
                                  guard=BudgetGuard(authorised_usd=Decimal("1")))
    assert set(payload["by_generator_route"]) == {"openai/gpt-image-2", "fal-ai/ideogram/v3"}
    for v in payload["by_generator_route"].values():
        assert v["attempts"] == 8
    assert set(payload["by_script"]) == {"devanagari", "latin_hinglish", "latin_commercial_claim"}
    assert payload["by_script"]["devanagari"]["attempts"] == 8      # 2 items x 2 routes x 2 repeats
    assert set(payload["by_item"]) == {"ATEXT-01", "ATEXT-02", "ATEXT-03", "ATEXT-04"}


def test_registry_remains_empty():
    registry = QT.REPO_ROOT / "eval" / "registry" / "registry-v1.jsonl"
    rows = [x for x in registry.read_text(encoding="utf-8").splitlines()
            if x.strip() and not x.startswith("#")]
    assert rows == []
