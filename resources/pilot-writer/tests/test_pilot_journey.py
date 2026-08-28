#!/usr/bin/env python3
"""RES-007 tests: prove the outcome writer can persist a realistic PILOT-001-shaped
production journey that the FROZEN validators accept, without a single provider call.

    python3 resources/pilot-writer/tests/test_pilot_journey.py

Everything is synthetic: fictional provider (dummy-vendor), test currency XTS, fixed
timestamps, deterministic pseudo-random BINARY fixture bytes (deliberately not valid
UTF-8, because production media is not text). No provider was called, no media was
generated, no money was spent.

The acceptance authority for produced records is the frozen pair
validate_topology_v3.py / recompute_cpao_v3.py - the tests run both as subprocesses
exactly as a human would, and also re-run the existing R4-C/R4-D control suites to
prove nothing regressed.

The synthetic journey (one accepted branded video):

    JOB-PW1 -> OUT-PW1 (video_asset)
      SET-SEQ ordered video_sequence:  U-SHOT-A(0), U-SHOT-B(1)
      SET-AUX unordered:               U-LOGO, U-ASSEMBLY
    steps:
      ST-GEN-A  provider_generation  ATT-A-REFUSED(refusal, 2.0) -> ATT-A-RETRY(ok, 10.0) -> shot-a.bin
      ST-GEN-B  provider_generation  ATT-B-TIMEOUT(timeout, 1.0) -> ATT-B-RETRY(ok, 10.0) -> shot-b.bin
      ST-GEN-LOGO provider_generation ATT-LOGO(ok, 3.0)                                   -> logo.bin
      ST-CONCAT local ffmpeg concat  cut.bin      = shot-a + shot-b   (ordered parents 0,1)
      ST-BRAND  local ffmpeg overlay final.bin    = cut + logo        (source 0, overlay 1)
                 both local steps share ONE ledger entry (0.5) - counted once
      ST-REVIEW human_review, required cost 15.0
      ST-SPOTCHECK human_review, human_optional 5.0 (recorded, excluded from both views;
                 HED-1 stays a Controller decision - both classes are representable)
    acceptance: OUT-PW1 accepted, final artifact final.bin

Hand-computed cost expectation (independent of the engine):
    api_tool       = 2 + 10 + 1 + 10 + 3 + 0.5(evaluator) = 26.50 XTS
    local_compute  = 0.50 (shared entry counted ONCE)
    human_required = 15.00
    human_optional = 5.00 excluded from both views
    fully-loaded   = 42.00 ; accepted outcomes = 1
    API/tool CpAO 26.50 ; fully-loaded CpAO 42.00 ; distinct entries 9
"""

import hashlib
import os
import shutil
import subprocess
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "resources", "pilot-writer"))

from outcome_writer import OutcomeWriter, WriterError  # noqa: E402

VALIDATE = os.path.join(ROOT, "resources", "pre-execution-freeze", "validators",
                        "validate_topology_v3.py")
RECOMPUTE = os.path.join(ROOT, "resources", "pre-execution-freeze", "validators",
                         "recompute_cpao_v3.py")
OUT_DIR = os.path.join(ROOT, "resources", "pilot-writer", "synthetic-journey")
ART_DIR = os.path.join(OUT_DIR, "artifacts")
NC_DIR = os.path.join(OUT_DIR, "negative-controls")

T = "2026-08-28T{:02d}:00:00Z".format  # fixed synthetic timestamps, deterministic

EXPECTED_CPAO = {
    "api_tool_cost": 26.5,
    "local_compute_cost": 0.5,
    "human_required_cost": 15.0,
    "fully_loaded_cost": 42.0,
    "accepted_outcomes": 1,
    "api_tool_cpao": 26.5,
    "fully_loaded_cpao": 42.0,
    "currency": "XTS",
    "distinct_cost_entries_counted": 9,
}

RESULTS = []


def check(name, fn):
    try:
        fn()
        RESULTS.append((name, True, ""))
        print(f"[PASS] {name}")
    except Exception as x:  # noqa: BLE001 - a test harness reports, it does not crash
        RESULTS.append((name, False, str(x)))
        print(f"[FAIL] {name}: {x}")


def synthetic_bytes(seed, n):
    """Deterministic binary bytes that are NOT valid UTF-8 - the shape of real media."""
    out = bytearray(b"\x00\xff\xfe")           # guarantee non-UTF-8, embedded NULs
    block = seed.encode()
    while len(out) < n:
        block = hashlib.sha256(block).digest()
        out.extend(block)
    return bytes(out[:n])


# A genuine SHA-256 for test attempts (Review 2: placeholder pseudo-hashes such as
# "ppp..." are no longer accepted anywhere, including by the writer itself).
PH = hashlib.sha256(b"unit-test-prompt").hexdigest()


def full_provenance(**overrides):
    """The inherited v2.1 call provenance the corrected contract requires on every
    attempt (all synthetic). Overrides let a call vary model, completion, etc."""
    p = dict(provider="dummy-vendor", model_id="dummy-video-1",
             model_version="unpinnable", endpoint="dummy://generate",
             workflow="single_call",
             config_hash=hashlib.sha256(b"synthetic-config").hexdigest(),
             config_location="dummy://config/pilot",
             reference_asset_hashes=[], requested_at=T(9), completed_at=T(9))
    p.update(overrides)
    return p


def run(cmd, expect_exit):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != expect_exit:
        raise AssertionError(
            f"{' '.join(os.path.basename(c) for c in cmd)} exited {p.returncode}, "
            f"expected {expect_exit}\n{p.stdout}\n{p.stderr}")
    return p.stdout


# ---------------------------------------------------------------------------------
def build_journey():
    """Build the full synthetic journey; returns (writer, {artifact files})."""
    if os.path.isdir(ART_DIR):
        shutil.rmtree(ART_DIR)
    os.makedirs(ART_DIR)

    # Provider outputs: pseudo-random binary. Local outputs: DETERMINISTIC byte
    # transforms of their parents (a genuine concat and a genuine composite), so the
    # lineage recorded is the lineage that actually produced the bytes.
    shot_a = synthetic_bytes("res007-shot-a", 2048)
    shot_b = synthetic_bytes("res007-shot-b", 2048)
    logo = synthetic_bytes("res007-logo", 512)
    cut = shot_a + shot_b                       # concat: order is meaning, A then B
    final = cut + logo                          # overlay composite (synthetic stand-in)
    files = {"shot-a.bin": shot_a, "shot-b.bin": shot_b, "logo.bin": logo,
             "cut.bin": cut, "final.bin": final}
    for name, data in files.items():
        with open(os.path.join(ART_DIR, name), "wb") as f:
            f.write(data)

    w = OutcomeWriter()

    # Cost ledger first (references must resolve at record time). All synthetic, XTS.
    def led(id_, amount, cc, hour):
        w.add_ledger_entry(id_, amount, "XTS", cc, T(hour), "synthetic_test",
                           synthetic=True)
    led("LED-A-REFUSED", 2.0, "api_tool", 9)
    led("LED-A-RETRY", 10.0, "api_tool", 9)
    led("LED-B-TIMEOUT", 1.0, "api_tool", 9)
    led("LED-B-RETRY", 10.0, "api_tool", 9)
    led("LED-LOGO", 3.0, "api_tool", 9)
    led("LED-LOCAL-FFMPEG", 0.5, "local_compute", 10)   # SHARED by two local steps
    led("LED-REVIEW", 15.0, "human_required", 11)
    led("LED-SPOTCHECK", 5.0, "human_optional", 11)     # recorded, excluded; HED-1 open
    led("LED-EVAL", 0.5, "api_tool", 11)

    w.add_job("JOB-PW1", T(8), "BRIEF-PW1", "req_lin_synthetic_pilot_test")
    w.add_outcome("OUT-PW1", "JOB-PW1", "video_asset", T(8),
                  reproducibility_status="full")
    w.add_set("SET-SEQ", "OUT-PW1", "ordered", "video_sequence")
    w.add_set("SET-AUX", "OUT-PW1", "unordered", "multi_format_set")
    w.add_unit("U-SHOT-A", "SET-SEQ", "shot", position=0)
    w.add_unit("U-SHOT-B", "SET-SEQ", "shot", position=1)
    w.add_unit("U-LOGO", "SET-AUX", "overlay")
    w.add_unit("U-ASSEMBLY", "SET-AUX", "layer")

    # --- provider generation, with the failure paths kept as individual attempts ---
    # Full inherited v2.1 call provenance on EVERY attempt (G12, corrected contract).
    # No eval_item_id anywhere: these are production attempts serving BRIEF-PW1 via
    # step -> unit -> set -> outcome -> job.
    w.add_provider_step("ST-GEN-A", "U-SHOT-A", "provider_generation", 0, T(9))
    w.record_attempt("ATT-A-REFUSED", "ST-GEN-A", "refusal", "general_video",
                     "LED-A-REFUSED",
                     error_detail="synthetic provider moderation refusal, verbatim",
                     prompt_hash=hashlib.sha256(b"prompt-shot-a").hexdigest(),
                     **full_provenance())
    w.record_attempt("ATT-A-RETRY", "ST-GEN-A", "ok", "general_video", "LED-A-RETRY",
                     retry_of_attempt_id="ATT-A-REFUSED",
                     retry_reason="prior attempt refused",
                     prompt_hash=hashlib.sha256(b"prompt-shot-a-rephrased").hexdigest(),
                     **full_provenance())
    w.add_provider_step("ST-GEN-B", "U-SHOT-B", "provider_generation", 0, T(9))
    # A timeout is the one case where completed_at is legitimately None: the call
    # never completed. The v2.1 nullable semantics are preserved, not reinvented.
    w.record_attempt("ATT-B-TIMEOUT", "ST-GEN-B", "timeout", "general_video",
                     "LED-B-TIMEOUT",
                     error_detail="synthetic 504 upstream timeout, verbatim",
                     prompt_hash=hashlib.sha256(b"prompt-shot-b").hexdigest(),
                     **full_provenance(completed_at=None))
    w.record_attempt("ATT-B-RETRY", "ST-GEN-B", "ok", "general_video", "LED-B-RETRY",
                     retry_of_attempt_id="ATT-B-TIMEOUT",
                     retry_reason="prior attempt timed out",
                     prompt_hash=hashlib.sha256(b"prompt-shot-b").hexdigest(),
                     **full_provenance())
    w.add_provider_step("ST-GEN-LOGO", "U-LOGO", "provider_generation", 0, T(9))
    w.record_attempt("ATT-LOGO", "ST-GEN-LOGO", "ok", "image", "LED-LOGO",
                     prompt_hash=hashlib.sha256(b"prompt-logo").hexdigest(),
                     **full_provenance(model_id="dummy-image-1"))

    w.record_artifact("art-shot-a", "ST-GEN-A", "video",
                      path=os.path.join(ART_DIR, "shot-a.bin"),
                      output_location="resources/pilot-writer/synthetic-journey/artifacts/shot-a.bin",
                      attempt_id="ATT-A-RETRY")
    w.record_artifact("art-shot-b", "ST-GEN-B", "video",
                      path=os.path.join(ART_DIR, "shot-b.bin"),
                      output_location="resources/pilot-writer/synthetic-journey/artifacts/shot-b.bin",
                      attempt_id="ATT-B-RETRY")
    w.record_artifact("art-logo", "ST-GEN-LOGO", "image",
                      path=os.path.join(ART_DIR, "logo.bin"),
                      output_location="resources/pilot-writer/synthetic-journey/artifacts/logo.bin",
                      attempt_id="ATT-LOGO")

    # --- local deterministic assembly: real bytes, NO attempt, NO trial -------------
    w.add_transform_recipe("TR-CONCAT", "ffmpeg", "7.0.1-synthetic", "concat",
                           params="-f concat -safe 0 -i list.txt -c copy cut.bin",
                           params_location="resources/pilot-writer/synthetic-journey/recipes.md")
    w.add_transform_recipe("TR-OVERLAY", "ffmpeg", "7.0.1-synthetic", "overlay",
                           params="-i cut.bin -i logo.bin -filter_complex overlay=10:10 final.bin",
                           params_location="resources/pilot-writer/synthetic-journey/recipes.md")
    w.add_local_step("ST-CONCAT", "U-ASSEMBLY", "assembly", 0, T(10), "TR-CONCAT",
                     cost_ref="LED-LOCAL-FFMPEG")
    w.add_local_step("ST-BRAND", "U-ASSEMBLY", "composition", 1, T(10), "TR-OVERLAY",
                     cost_ref="LED-LOCAL-FFMPEG")     # same ledger entry, counted once
    w.record_artifact("art-cut", "ST-CONCAT", "video",
                      path=os.path.join(ART_DIR, "cut.bin"),
                      output_location="resources/pilot-writer/synthetic-journey/artifacts/cut.bin",
                      parents=[("art-shot-a", "source", 0),
                               ("art-shot-b", "source", 1)])
    w.record_artifact("art-final", "ST-BRAND", "video",
                      path=os.path.join(ART_DIR, "final.bin"),
                      output_location="resources/pilot-writer/synthetic-journey/artifacts/final.bin",
                      parents=[("art-cut", "source", 0),
                               ("art-logo", "overlay", 1)])

    # --- human review: a step, never an attempt; cost class is data, not a decision -
    w.add_human_step("ST-REVIEW", "U-ASSEMBLY", "human_review", 2, T(11),
                     operator_ref="ROLE-PILOT-REVIEWER", cost_ref="LED-REVIEW")
    w.add_human_step("ST-SPOTCHECK", "U-ASSEMBLY", "human_review", 3, T(11),
                     operator_ref="ROLE-SECOND-REVIEWER", cost_ref="LED-SPOTCHECK")

    # --- an already-supplied measurement reference, stored verbatim -----------------
    w.record_measurement("M-PW1", "art-final", "motion_action_quality", "whole_asset",
                         result={"synthetic": True}, evaluator_cost_ref="LED-EVAL")

    w.set_final_artifact("OUT-PW1", "art-final")
    w.record_outcome_acceptance("ACC-PW1", "OUT-PW1", True,
                                "dummy-customer-proxy", T(12), "BRIEF-PW1")
    return w, files


# ---------------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------------
WRITER, FILES = None, None
ARCHIVE_PATH = os.path.join(OUT_DIR, "pilot-journey-synthetic.yaml")


def t01_build_and_write():
    global WRITER, FILES
    WRITER, FILES = build_journey()
    WRITER.write_archive(ARCHIVE_PATH, expected_cpao=EXPECTED_CPAO)
    assert os.path.isfile(ARCHIVE_PATH)


def t02_binary_artifacts_are_binary_and_faithful():
    """The fixture bytes are genuinely binary (not UTF-8), and the archive's hash and
    byte length match the ACTUAL committed bytes, recomputed independently here."""
    d = yaml.safe_load(open(ARCHIVE_PATH))
    arts = {a["artifact_id"]: a for a in d["artifacts"]}
    for name, data in FILES.items():
        try:
            data.decode("utf-8")
            raise AssertionError(f"{name}: fixture bytes decoded as UTF-8; the test "
                                 f"must use genuinely binary media-shaped bytes")
        except UnicodeDecodeError:
            pass
    for aid, fname in [("art-shot-a", "shot-a.bin"), ("art-shot-b", "shot-b.bin"),
                       ("art-logo", "logo.bin"), ("art-cut", "cut.bin"),
                       ("art-final", "final.bin")]:
        on_disk = open(os.path.join(ART_DIR, fname), "rb").read()
        assert arts[aid]["output_hash"] == hashlib.sha256(on_disk).hexdigest(), \
            f"{aid}: archive hash does not match bytes on disk"
        assert arts[aid]["output_bytes"] == len(on_disk), \
            f"{aid}: archive byte length does not match bytes on disk"


def t03_provider_local_human_steps_distinct():
    d = yaml.safe_load(open(ARCHIVE_PATH))
    steps = {s["step_id"]: s for s in d["steps"]}
    arts = {a["artifact_id"]: a for a in d["artifacts"]}
    # Local and human steps: no attempts. Provider steps: every attempt present.
    for sid in ("ST-CONCAT", "ST-BRAND", "ST-REVIEW", "ST-SPOTCHECK"):
        assert steps[sid]["attempt_ids"] == [], f"{sid} must carry no attempts"
    assert steps["ST-GEN-A"]["attempt_ids"] == ["ATT-A-REFUSED", "ATT-A-RETRY"]
    # Local artifacts genuinely have no attempt and no trial.
    for aid in ("art-cut", "art-final"):
        assert arts[aid]["attempt_id"] is None and arts[aid]["trial_id"] is None
    # 5 attempts -> 5 distinct trials (one call = one trial, failures included).
    trials = {a["trial_id"] for a in d["attempts"]}
    assert len(d["attempts"]) == 5 and len(trials) == 5


def t04_failed_attempts_persist_without_artifacts():
    d = yaml.safe_load(open(ARCHIVE_PATH))
    failed = {a["attempt_id"]: a for a in d["attempts"]
              if a["status"] in ("refusal", "timeout")}
    assert set(failed) == {"ATT-A-REFUSED", "ATT-B-TIMEOUT"}
    for a in failed.values():
        assert a["error_detail"], "a failure must keep its verbatim reason"
    claimed = {a["attempt_id"] for a in d["artifacts"] if a["attempt_id"]}
    assert not claimed & set(failed), "a failed attempt must not have an artifact"


def t05_ordered_multi_parent_lineage():
    d = yaml.safe_load(open(ARCHIVE_PATH))
    arts = {a["artifact_id"]: a for a in d["artifacts"]}
    cut = {(p["parent_artifact_id"], p["position"]) for p in arts["art-cut"]["parents"]}
    assert cut == {("art-shot-a", 0), ("art-shot-b", 1)}, \
        "concat order A-then-B must be reconstructible"
    final = {(p["parent_artifact_id"], p["role"], p["position"])
             for p in arts["art-final"]["parents"]}
    assert final == {("art-cut", "source", 0), ("art-logo", "overlay", 1)}


def t06_frozen_topology_validator_passes():
    out = run(["python3", VALIDATE, ARCHIVE_PATH], expect_exit=0)
    assert "[PASS] G1" in out and "[PASS] G11" in out and "[PASS] G12" in out
    assert "failed/refused:    2" in out, "both failed attempts must be visible"
    assert "'production': 5" in out, "all 5 attempts must be declared production kind"


def t07_frozen_cpao_engine_matches_hand_computed_total():
    out = run(["python3", RECOMPUTE, ARCHIVE_PATH], expect_exit=0)
    assert "recomputed totals match the archive's hand-computed expectation" in out
    assert "(EXCLUDED from both views)" in out, \
        "the human_optional entry must be visibly excluded, not silently dropped"


def t08_writer_refuses_attempt_on_local_step():
    w, _ = build_journey()
    try:
        w.record_attempt("ATT-EVIL", "ST-CONCAT", "ok", "general_video", "LED-EVAL",
                         prompt_hash=PH, **full_provenance())
        raise AssertionError("writer accepted a provider attempt on a local step")
    except WriterError:
        pass


def t09_writer_refuses_artifact_for_failed_attempt():
    w, _ = build_journey()
    try:
        w.record_artifact("art-evil", "ST-GEN-A", "video", data=b"\x00\xffx",
                          output_location="dummy://x", attempt_id="ATT-A-REFUSED")
        raise AssertionError("writer accepted an artifact for a refused attempt")
    except WriterError:
        pass


def t10_writer_refuses_local_artifact_claiming_attempt():
    w, _ = build_journey()
    try:
        w.record_artifact("art-evil", "ST-CONCAT", "video", data=b"\x00\xffx",
                          output_location="dummy://x", attempt_id="ATT-A-RETRY")
        raise AssertionError("writer accepted an attempt claim on a local artifact")
    except WriterError:
        pass


def t11_writer_refuses_ambiguous_order():
    w, _ = build_journey()
    try:
        w.record_artifact("art-evil", "ST-CONCAT", "video", data=b"\x00\xffx",
                          output_location="dummy://x",
                          parents=[("art-shot-a", "source", 0),
                                   ("art-shot-b", "source", 0)])
        raise AssertionError("writer accepted duplicate parent positions")
    except WriterError:
        pass
    try:
        w.add_unit("U-EVIL", "SET-SEQ", "shot")   # ordered set, no position
        raise AssertionError("writer accepted an unpositioned unit in an ordered set")
    except WriterError:
        pass


def t12_writer_refuses_duplicate_trial_and_silent_failure():
    w, _ = build_journey()
    try:
        w.record_attempt("ATT-EVIL", "ST-GEN-A", "ok", "general_video", "LED-EVAL",
                         trial_id="ATT-A-RETRY", prompt_hash=PH,
                         **full_provenance())
        raise AssertionError("writer accepted two attempts sharing one trial")
    except WriterError:
        pass
    try:
        w.record_attempt("ATT-EVIL2", "ST-GEN-A", "refusal", "general_video",
                         "LED-EVAL", prompt_hash=PH,
                         **full_provenance())      # no error_detail
        raise AssertionError("writer accepted a failure with no recorded reason")
    except WriterError:
        pass


def t13_writer_refuses_acceptance_without_final_artifact_or_by_resources():
    w, _ = build_journey()
    w2 = OutcomeWriter()
    w2.add_job("J", T(8), "B", "req_lin_x")
    w2.add_outcome("O", "J", "video_asset", T(8))
    try:
        w2.record_outcome_acceptance("A", "O", True, "customer", T(9), "B")
        raise AssertionError("writer accepted an outcome with no final artifact")
    except WriterError:
        pass
    try:
        w.record_outcome_acceptance("ACC-EVIL", "OUT-PW1", True,
                                    "resources-worker", T(12), "BRIEF-PW1")
        raise AssertionError("writer let Resources decide customer acceptance")
    except WriterError:
        pass


def t14_negative_control_mutable_cost_refused_by_engine():
    """A deliberately invalid journey - one ledger entry recorded as mutable. The
    writer represents it (refusing would silently rewrite evidence); the FROZEN CpAO
    engine must refuse to produce a number. Preserved as a committed negative control."""
    os.makedirs(NC_DIR, exist_ok=True)
    w, _ = build_journey()
    w.add_ledger_entry("LED-MUTABLE", 1.0, "XTS", "api_tool", T(9),
                       "synthetic_test", synthetic=True, immutable=False)
    a = w.to_archive(expected_cpao=EXPECTED_CPAO)
    for att in a["attempts"]:
        if att["attempt_id"] == "ATT-LOGO":
            att["cost_ref"] = "LED-MUTABLE"
    p = os.path.join(NC_DIR, "nc-mutable-cost-ref.yaml")
    yaml.safe_dump(a, open(p, "w"), sort_keys=False)
    out = run(["python3", RECOMPUTE, p, "--expect-refusal"], expect_exit=3)
    assert "immutable is not true" in out


def t15_negative_control_no_accepted_outcome_refused():
    """Failure-path journey: the provider refused/timed out, nothing was accepted.
    The failed attempts REMAIN recorded (topology valid), no artifact is faked, and
    CpAO is UNDEFINED - the engine refuses rather than reporting zero."""
    w = OutcomeWriter()
    w.add_ledger_entry("LED-1", 2.0, "XTS", "api_tool", T(9), "synthetic_test",
                       synthetic=True)
    w.add_job("JOB-FAIL", T(8), "BRIEF-F", "req_lin_synthetic_pilot_test")
    w.add_outcome("OUT-FAIL", "JOB-FAIL", "video_asset", T(8))
    w.add_set("SET-F", "OUT-FAIL", "ordered", "video_sequence")
    w.add_unit("U-F", "SET-F", "shot", position=0)
    w.add_provider_step("ST-F", "U-F", "provider_generation", 0, T(9))
    w.record_attempt("ATT-F", "ST-F", "refusal", "general_video", "LED-1",
                     error_detail="synthetic refusal, verbatim",
                     prompt_hash=hashlib.sha256(b"prompt-fail").hexdigest(),
                     **full_provenance())
    p = os.path.join(NC_DIR, "nc-only-failed-attempts.yaml")
    w.write_archive(p)
    run(["python3", VALIDATE, p], expect_exit=0)         # the failure IS valid evidence
    out = run(["python3", RECOMPUTE, p, "--expect-refusal"], expect_exit=3)
    assert "no accepted outcome" in out
    d = yaml.safe_load(open(p))
    assert d["attempts"][0]["status"] == "refusal" and d["artifacts"] == []


def t16_frozen_validator_catches_post_writer_tampering():
    """If someone edits the archive AFTER the writer (faking an attempt on the local
    concat step), the frozen validator still rejects it - the writer's guards are a
    convenience, not the line of defence."""
    a = yaml.safe_load(open(ARCHIVE_PATH))
    for s in a["steps"]:
        if s["step_id"] == "ST-CONCAT":
            s["attempt_ids"] = ["ATT-A-RETRY"]
    p = os.path.join(NC_DIR, "nc-tampered-local-step-attempt.yaml")
    yaml.safe_dump(a, open(p, "w"), sort_keys=False)
    out = run(["python3", VALIDATE, p, "--expect-fail"], expect_exit=0)
    assert "[FAIL:G2]" in out


def t17_existing_control_suites_still_pass():
    out = run(["bash", os.path.join(ROOT, "resources", "pre-execution-freeze",
                                    "validators", "run_lineage_controls.sh")],
              expect_exit=0)
    assert "41/41" in out, ("2 positives + 39 negatives: the ten first-correction G12 "
                            "controls plus the thirteen Review-2 invariant controls")
    out = run(["bash", os.path.join(ROOT, "resources", "pre-execution-freeze",
                                    "validators", "run_cpao_controls_v3.sh")],
              expect_exit=0)
    assert "13/13" in out


def t18_deterministic_output():
    """Re-building the journey byte-for-byte reproduces the archive."""
    before = open(ARCHIVE_PATH, "rb").read()
    w, _ = build_journey()
    w.write_archive(ARCHIVE_PATH, expected_cpao=EXPECTED_CPAO)
    assert open(ARCHIVE_PATH, "rb").read() == before


def t19_repair_step_journey():
    """A repair path: a provider-generated shot is repaired by a local deterministic
    step (step_kind=repair, repair_of_step_id set). The repair creates a new artifact
    with the defective one as parent; no attempt is manufactured for it."""
    w = OutcomeWriter()
    w.add_ledger_entry("LED-GEN", 5.0, "XTS", "api_tool", T(9), "synthetic_test",
                       synthetic=True)
    w.add_ledger_entry("LED-REPAIR", 0.5, "XTS", "local_compute", T(10),
                       "synthetic_test", synthetic=True)
    w.add_job("JOB-R", T(8), "BRIEF-R", "req_lin_synthetic_pilot_test")
    w.add_outcome("OUT-R", "JOB-R", "video_asset", T(8))
    w.add_set("SET-R", "OUT-R", "ordered", "video_sequence")
    w.add_unit("U-R", "SET-R", "shot", position=0)
    w.add_provider_step("ST-GEN", "U-R", "provider_generation", 0, T(9))
    w.record_attempt("ATT-R", "ST-GEN", "ok", "general_video", "LED-GEN",
                     prompt_hash=hashlib.sha256(b"prompt-repair").hexdigest(),
                     **full_provenance())
    w.record_artifact("art-raw", "ST-GEN", "video", data=synthetic_bytes("r-raw", 512),
                      output_location="dummy://r/raw", attempt_id="ATT-R")
    w.add_transform_recipe("TR-FIX", "ffmpeg", "7.0.1-synthetic", "encode",
                           params="-i raw -vf eq=brightness=0.05 fixed",
                           params_location="dummy://params/fix")
    w.add_local_step("ST-FIX", "U-R", "repair", 1, T(10), "TR-FIX",
                     cost_ref="LED-REPAIR", repair_of_step_id="ST-GEN")
    w.record_artifact("art-fixed", "ST-FIX", "video",
                      data=synthetic_bytes("r-fixed", 512),
                      output_location="dummy://r/fixed",
                      parents=[("art-raw", "source", 0)])
    w.set_final_artifact("OUT-R", "art-fixed")
    w.record_outcome_acceptance("ACC-R", "OUT-R", True, "dummy-customer-proxy",
                                T(11), "BRIEF-R")
    p = os.path.join(NC_DIR, "..", "repair-journey.yaml")
    w.write_archive(p, expected_cpao={
        "api_tool_cost": 5.0, "local_compute_cost": 0.5, "human_required_cost": 0.0,
        "fully_loaded_cost": 5.5, "accepted_outcomes": 1, "api_tool_cpao": 5.0,
        "fully_loaded_cpao": 5.5, "currency": "XTS",
        "distinct_cost_entries_counted": 2})
    run(["python3", VALIDATE, p], expect_exit=0)
    run(["python3", RECOMPUTE, p], expect_exit=0)
    d = yaml.safe_load(open(p))
    fix = next(s for s in d["steps"] if s["step_id"] == "ST-FIX")
    assert fix["step_kind"] == "repair" and fix["repair_of_step_id"] == "ST-GEN"
    assert fix["attempt_ids"] == []


def t20_writer_requires_full_inherited_provenance():
    """The corrected contract: no production attempt row is accepted with missing or
    null inherited call provenance, and no unknown field bag is accepted."""
    from outcome_writer import ATTEMPT_REQUIRED_NON_NULL
    for field in ATTEMPT_REQUIRED_NON_NULL:
        w, _ = build_journey()
        kwargs = dict(prompt_hash=PH, **full_provenance())
        kwargs[field] = None
        try:
            w.record_attempt("ATT-X", "ST-GEN-A", "ok", "general_video", "LED-EVAL",
                             **kwargs)
            raise AssertionError(f"writer accepted null required field {field}")
        except WriterError:
            pass
    w, _ = build_journey()
    try:
        w.record_attempt("ATT-X", "ST-GEN-A", "ok", "general_video", "LED-EVAL",
                         prompt_hash=PH,
                         **full_provenance(reference_asset_hashes=None))
        raise AssertionError("writer accepted null reference_asset_hashes")
    except WriterError:
        pass
    try:
        kwargs = dict(prompt_hash=PH, **full_provenance())
        del kwargs["completed_at"]
        w.record_attempt("ATT-X", "ST-GEN-A", "ok", "general_video", "LED-EVAL",
                         **kwargs)
        raise AssertionError("writer accepted an omitted completed_at")
    except WriterError:
        pass
    try:
        w.record_attempt("ATT-X", "ST-GEN-A", "ok", "general_video", "LED-EVAL",
                         prompt_hash=PH, mystery_field="x",
                         **full_provenance())
        raise AssertionError("writer accepted an unknown extra field")
    except WriterError:
        pass


def t21_eval_item_id_conditional_override():
    """Production attempts must NOT carry eval_item_id; benchmark/eval attempts must.
    A benchmark-kind journey passes the corrected frozen validator end to end."""
    w, _ = build_journey()
    try:
        w.record_attempt("ATT-X", "ST-GEN-A", "ok", "general_video", "LED-EVAL",
                         prompt_hash=PH, eval_item_id="ITEM-001",
                         **full_provenance())
        raise AssertionError("writer accepted eval_item_id on a production attempt")
    except WriterError:
        pass
    try:
        w.record_attempt("ATT-Y", "ST-GEN-A", "ok", "general_video", "LED-EVAL",
                         prompt_hash=PH, attempt_kind="benchmark_eval",
                         **full_provenance())
        raise AssertionError("writer accepted a benchmark attempt without eval_item_id")
    except WriterError:
        pass
    # A valid benchmark_eval attempt round-trips through the frozen validator.
    w2 = OutcomeWriter()
    w2.add_ledger_entry("LED-1", 1.0, "XTS", "api_tool", T(9), "synthetic_test",
                        synthetic=True)
    w2.add_job("JOB-BM", T(8), "BRIEF-BM", "req_lin_synthetic_pilot_test")
    w2.add_outcome("OUT-BM", "JOB-BM", "static_asset", T(8))
    w2.add_set("SET-BM", "OUT-BM", "unordered", "variant_set")
    w2.add_unit("U-BM", "SET-BM", "static")
    w2.add_provider_step("ST-BM", "U-BM", "provider_generation", 0, T(9))
    w2.record_attempt("ATT-BM", "ST-BM", "ok", "image", "LED-1",
                      prompt_hash=hashlib.sha256(b"bench-prompt").hexdigest(),
                      attempt_kind="benchmark_eval", eval_item_id="ITEM-SYN-001",
                      **full_provenance(model_id="dummy-image-1"))
    w2.record_artifact("art-bm", "ST-BM", "image", data=synthetic_bytes("bm", 256),
                       output_location="dummy://bm/1", attempt_id="ATT-BM")
    w2.set_final_artifact("OUT-BM", "art-bm")
    w2.record_outcome_acceptance("ACC-BM", "OUT-BM", True, "dummy-customer-proxy",
                                 T(10), "BRIEF-BM")
    p = os.path.join(NC_DIR, "..", "benchmark-attempt-journey.yaml")
    w2.write_archive(p)
    out = run(["python3", VALIDATE, p], expect_exit=0)
    assert "'benchmark_eval': 1" in out
    d = yaml.safe_load(open(p))
    assert d["attempts"][0]["eval_item_id"] == "ITEM-SYN-001"


def t22_production_archive_has_no_eval_item_id_and_full_provenance():
    """The corrected synthetic pilot archive: every attempt declares production kind,
    carries every inherited provenance field, and has no eval_item_id anywhere."""
    d = yaml.safe_load(open(ARCHIVE_PATH))
    required = ("attempt_kind", "provider", "model_id", "model_version", "endpoint",
                "workflow", "prompt_hash", "config_hash", "config_location",
                "reference_asset_hashes", "requested_at", "completed_at",
                "repeat_index", "repeat_of_attempt_id", "retry_of_attempt_id",
                "status", "lane", "cost_ref", "storage_class")
    for a in d["attempts"]:
        assert a["attempt_kind"] == "production"
        assert "eval_item_id" not in a, "no fabricated benchmark id on production rows"
        for k in required:
            assert k in a, f"attempt {a['attempt_id']}: missing {k}"
    timeout = next(a for a in d["attempts"] if a["status"] == "timeout")
    assert timeout["completed_at"] is None, \
        "a timed-out call never completed; completed_at must be recorded null"


def t23_writer_enforces_review2_invariants():
    """Review-2 invariants refused at record time: malformed repeat_index values,
    placeholder pseudo-hashes, junk reference-asset hashes, malformed timestamps."""
    cases = [
        dict(repeat_index=-1), dict(repeat_index="0"), dict(repeat_index=True),
        dict(repeat_index=None),
        dict(prompt_hash="p" * 64),
        dict(prompt_hash=PH.upper()),   # valid hex but uppercase: the project records
                                        # hashlib hexdigest (lowercase) - convention kept
        dict(config_hash="not-a-hash"),
        dict(reference_asset_hashes=["junk"]),
        dict(requested_at="yesterday morning"),
        dict(requested_at="2026-02-01 09:00:00"),
        dict(completed_at="2026-13-99T99:99:99Z"),
    ]
    for override in cases:
        w, _ = build_journey()
        kwargs = dict(prompt_hash=PH, **full_provenance())
        kwargs.update(override)
        try:
            w.record_attempt("ATT-X", "ST-GEN-A", "ok", "general_video", "LED-EVAL",
                             **kwargs)
            raise AssertionError(f"writer accepted invalid provenance {override}")
        except WriterError:
            pass


def t24_validator_rejects_review2_violations_on_durable_archive():
    """The durable archive is independently protected: seed each Review-2 violation
    into an otherwise valid written archive and prove the frozen validator rejects it
    with a G12 message naming that invariant (writer checks alone are not the line of
    defence)."""
    cases = [
        ({"lane": None}, "lane"), ({"lane": "video"}, "lane"),
        ({"storage_class": "B_cache"}, "storage_class"),
        ({"repeat_index": -1}, "repeat_index"),
        ({"repeat_index": "0"}, "repeat_index"),
        ({"repeat_index": True}, "repeat_index"),
        ({"prompt_hash": "p" * 64}, "prompt_hash"),
        ({"config_hash": "zz"}, "config_hash"),
        ({"reference_asset_hashes": ["junk"]}, "reference_asset_hashes"),
        ({"repeat_of_attempt_id": "ATT-GHOST"}, "repeat_of_attempt_id"),
        ({"retry_of_attempt_id": "ATT-GHOST", "retry_reason": "x"},
         "retry_of_attempt_id"),
        ({"requested_at": "yesterday"}, "requested_at"),
        ({"completed_at": "2026-02-01 09:15:00"}, "completed_at"),
    ]
    os.makedirs(NC_DIR, exist_ok=True)
    for i, (mutation, token) in enumerate(cases):
        a = yaml.safe_load(open(ARCHIVE_PATH))
        target = next(x for x in a["attempts"] if x["attempt_id"] == "ATT-LOGO")
        target.update(mutation)
        p = os.path.join(NC_DIR, "tmp-review2-seeded.yaml")
        yaml.safe_dump(a, open(p, "w"), sort_keys=False)
        out = run(["python3", VALIDATE, p, "--expect-fail"], expect_exit=0)
        first = next(l for l in out.splitlines() if l.startswith("[FAIL:"))
        assert first.startswith("[FAIL:G12]") and token in first, \
            f"case {i} {mutation}: expected G12/{token}, got: {first}"
    os.remove(p)


def main():
    tests = [(k, v) for k, v in sorted(globals().items()) if k.startswith("t")
             and callable(v)]
    for name, fn in tests:
        check(name, fn)
    failed = [r for r in RESULTS if not r[1]]
    print(f"\n{len(RESULTS) - len(failed)}/{len(RESULTS)} RES-007 writer tests passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
