#!/usr/bin/env python3
"""Progressive Devanagari-first text-judge qualification for EMP-001.

THE EXPENSIVE MISTAKE THIS AVOIDS

    A candidate that has already false-passed on Devanagari does not go on to demonstrate that it
    also fails English. That is another 576 paid calls for no new information. The stop is
    mechanical and it is tested by COUNTING CALLS, not by reading this docstring and believing it.

WHO DECIDES EXACTNESS

    We do. Not the judge.

    In the `transcribe` shape the judge never sees the target; it commits to what it believes is
    drawn, and `transcription_matches` compares that to the target in code, after exactly one
    frozen normalisation rule (NFC, plus trimming surrounding whitespace) and nothing else. No
    case folding, no de-accenting, no "close enough". Letting a judge decide string equality after
    transcribing is how the blind shape stops being blind.

    The `verdict` shape does see the target. It is diagnostic. Comparing the two shapes measures
    how much of a checker's false-pass behaviour is caused by showing it the answer we hope for —
    and a verdict may never override a primary transcription mismatch.

WHAT A DRY RUN IS AND IS NOT

    `--dry-run` simulates the complete protocol against deterministic fake candidates. It makes
    zero network calls, spends zero money, and every result it produces is marked
    `synthetic: true` / `may_populate_registry: false`. Synthetic evidence may never reach the
    Capability Registry, and nothing here writes to it.

    A dry run tells you the harness works. It tells you NOTHING about any real model.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import unicodedata
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKAGE_ROOT = HERE.parent
REPO_ROOT = PACKAGE_ROOT.parent.parent

sys.path.insert(0, str(PACKAGE_ROOT))
from budget_guard import BudgetExceeded, BudgetGuard, NotAuthorised, open_guard  # noqa: E402

import yaml  # noqa: E402

CONTRACT = HERE / "qualification-contract-v1.yaml"
LATIN_PACK = HERE / "latin-pack-v1.jsonl"
DEVANAGARI_VIEW = HERE / "build" / "devanagari" / "validated"
DEVANAGARI_BUILD = HERE / "build" / "devanagari"
HUMAN_VALIDATION_RECORD = (REPO_ROOT / "eval/battery/devanagari-exactness/human-validation"
                           / "human-validation-v1.json")
DEFAULT_OUT = HERE / "qualification-dryrun.json"

SHAPES = ("transcribe", "verdict")
SCRIPTS = ("devanagari", "latin")

# Per candidate, per script: 96 items x 2 shapes x 3 passes.
CALLS_PER_SCRIPT = 96 * len(SHAPES) * 3
MAX_EVALUATOR_CALLS = CALLS_PER_SCRIPT * len(SCRIPTS) * 2  # both candidates, both scripts


def contract() -> dict:
    return yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))


# ------------------------------------------------------------------------------- the scorer
def normalise(s: str) -> str:
    """The ONE frozen normalisation rule: NFC, plus trimming surrounding whitespace.

    Named and tested separately from the comparison so that "we normalised" can never quietly
    grow to mean "we also case-folded and dropped the accents".
    """
    return unicodedata.normalize("NFC", s).strip()


def transcription_matches(target: str, transcription: str) -> bool:
    """Code-level exactness. The judge does not get a vote."""
    return normalise(target) == normalise(transcription)


def parse_verdict_reply(reply: str) -> str:
    """MATCH / MISMATCH, or `unparseable`. A parse failure is recorded, never guessed."""
    token = reply.strip().upper()
    if token == "MATCH":
        return "match"
    if token == "MISMATCH":
        return "mismatch"
    return "unparseable"


# ---------------------------------------------------------------------------------- materials
def load_latin_items() -> list[dict]:
    return [json.loads(x) for x in LATIN_PACK.read_text(encoding="utf-8").splitlines() if x.strip()]


def load_devanagari_items() -> list[dict]:
    """The 96-item HUMAN-VALIDATED view, materialised outside the frozen battery."""
    path = DEVANAGARI_VIEW / "scoring-key.jsonl"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} does not exist. Materialise the validated view first — it is a reproducible "
            f"build product, deliberately not committed:\n"
            f"  cd eval/battery/devanagari-exactness\n"
            f"  python3 build_items.py --total 120 --out-dir <OUT>\n"
            f"  python3 apply_human_validation.py --from-build <OUT> --out-dir <OUT>/validated\n"
            f"Use an --out-dir OUTSIDE the battery: EMP-001 reads that battery and never writes "
            f"to it.")
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def verify_devanagari_identity() -> dict:
    """Fail closed unless the materialised build IS the one the human reviewer validated."""
    record = json.loads(HUMAN_VALIDATION_RECORD.read_text(encoding="utf-8"))
    expected = record["battery_identity"]["items_jsonl_sha256"]
    built = DEVANAGARI_BUILD / "items.jsonl"

    if not built.exists():
        return {"ok": False, "reason": f"no materialised build at {built}",
                "expected_items_jsonl_sha256": expected, "actual_items_jsonl_sha256": None}

    actual = hashlib.sha256(built.read_bytes()).hexdigest()
    expected_state = record["expected_validated_state"]
    view = load_devanagari_items() if (DEVANAGARI_VIEW / "scoring-key.jsonl").exists() else []

    return {
        "ok": (actual == expected
               and len(view) == expected_state["items"]
               and sum(v["expected_verdict"] == "match" for v in view) == expected_state["match"]
               and sum(v["expected_verdict"] == "mismatch" for v in view)
               == expected_state["mismatch"]),
        "expected_items_jsonl_sha256": expected,
        "actual_items_jsonl_sha256": actual,
        "validated_items": len(view),
        "expected_validated_state": expected_state["items"],
        "note": ("The 106-item build is the material the reviewer saw; the 96-item validated view "
                 "is what a checker run uses."),
    }


def _script_items(script: str) -> list[dict]:
    if script == "devanagari":
        return [{"item_id": v["item_id"], "target": v["target_string"],
                 "expected": v["expected_verdict"], "drawn": v["rendered_string"]}
                for v in load_devanagari_items()]
    return [{"item_id": v["item_id"], "target": v["target_string"],
             "expected": v["expected"], "drawn": v["rendered_string"]}
            for v in load_latin_items()]


# ------------------------------------------------------------------------------ fake candidate
class FakeCandidate:
    """A deterministic stand-in for a judge. Makes no network call, ever.

    It counts its calls per script so the progressive stop can be proved by measurement rather
    than by inspection, and it exposes `retries`, which must stay 0.
    """

    COST_PER_CALL = Decimal("0.0021")

    def __init__(self, name: str, false_pass_on_first_mismatch: bool = False,
                 false_fail_rate: float = 0.0, refusal_rate: float = 0.0,
                 inconsistent: bool = False):
        self.name = name
        self.false_pass_on_first_mismatch = false_pass_on_first_mismatch
        self.false_fail_rate = false_fail_rate
        self.refusal_rate = refusal_rate
        self.inconsistent = inconsistent
        self.calls = 0
        self.retries = 0
        self.calls_by_script = {s: 0 for s in SCRIPTS}
        self._mismatch_seen = 0

    def call(self, script: str, item: dict, shape: str, pass_index: int) -> dict:
        """One call. One trial. No loop anywhere in this method."""
        self.calls += 1
        self.calls_by_script[script] += 1
        n = self.calls

        if self.refusal_rate and (n % max(1, int(1 / self.refusal_rate)) == 0):
            return {"api_status": "refusal", "text": "", "cost": self.COST_PER_CALL}

        if item["expected"] == "mismatch":
            self._mismatch_seen += 1
            if self.false_pass_on_first_mismatch and self._mismatch_seen == 1:
                # The dangerous error: report the target as drawn when it was not.
                text = item["target"] if shape == "transcribe" else "MATCH"
                return {"api_status": "ok", "text": text, "cost": self.COST_PER_CALL}

        if self.false_fail_rate and (n % max(1, int(1 / self.false_fail_rate)) == 0) \
                and item["expected"] == "match":
            text = item["drawn"] + "x" if shape == "transcribe" else "MISMATCH"
            return {"api_status": "ok", "text": text, "cost": self.COST_PER_CALL}

        if self.inconsistent and pass_index == 2 and item["expected"] == "match":
            text = item["drawn"] + "?" if shape == "transcribe" else "MISMATCH"
            return {"api_status": "ok", "text": text, "cost": self.COST_PER_CALL}

        if shape == "transcribe":
            return {"api_status": "ok", "text": item["drawn"], "cost": self.COST_PER_CALL}
        return {"api_status": "ok",
                "text": "MATCH" if item["expected"] == "match" else "MISMATCH",
                "cost": self.COST_PER_CALL}


# ----------------------------------------------------------------------------------- scoring
def _observed_verdict(shape: str, item: dict, reply: dict) -> str:
    """What the judge effectively said about this item. `refusal` and `unparseable` stay apart."""
    if reply["api_status"] != "ok":
        return "refusal"
    if shape == "transcribe":
        return "match" if transcription_matches(item["target"], reply["text"]) else "mismatch"
    return parse_verdict_reply(reply["text"])


def _score_script(candidate, script: str, guard: BudgetGuard, repeats: int) -> dict:
    """Run every item x shape x pass, scoring as we go. Stops on a budget refusal."""
    items = _script_items(script)
    observations: list[dict] = []
    stopped_reason = None

    for pass_index in range(repeats):
        for shape in SHAPES:
            for item in items:
                try:
                    guard.reserve(FakeCandidate.COST_PER_CALL)
                except BudgetExceeded:
                    stopped_reason = "budget_exhausted"
                    break
                reply = candidate.call(script, item, shape, pass_index)
                guard.record(reply["cost"])
                observations.append({
                    "item_id": item["item_id"], "shape": shape, "pass": pass_index,
                    "expected": item["expected"],
                    "observed": _observed_verdict(shape, item, reply),
                })
            if stopped_reason:
                break
        if stopped_reason:
            break

    c = contract()
    mismatches = [o for o in observations if o["expected"] == "mismatch"]
    matches = [o for o in observations if o["expected"] == "match"]
    refusals = [o for o in observations if o["observed"] == "refusal"]
    scoreable = [o for o in observations if o["observed"] in ("match", "mismatch")]

    false_passes = sum(1 for o in mismatches if o["observed"] == "match")
    false_fails = sum(1 for o in matches if o["observed"] == "mismatch")

    false_fail_rate = (false_fails / len([o for o in matches if o["observed"] != "refusal"])
                       if any(o["observed"] != "refusal" for o in matches) else 0.0)
    refusal_rate = len(refusals) / len(observations) if observations else 0.0

    # Repeat consistency: for each (item, shape), did every pass agree?
    by_cell: dict[tuple, set] = {}
    for o in scoreable:
        by_cell.setdefault((o["item_id"], o["shape"]), set()).add(o["observed"])
    complete = {k: v for k, v in by_cell.items() if len(v) >= 1}
    consistency = (sum(1 for v in complete.values() if len(v) == 1) / len(complete)
                   if complete else 0.0)

    failed_gates = []
    if false_passes > c["mismatch_false_pass_max"]:
        failed_gates.append("mismatch_false_pass")
    if false_fail_rate > c["match_false_fail_rate_max"]:
        failed_gates.append("match_false_fail_rate")
    if refusal_rate > c["refusal_rate_max"]:
        failed_gates.append("refusal_rate")
    if consistency < c["repeat_consistency_min"]:
        failed_gates.append("repeat_consistency")

    return {
        "script": script,
        "calls": len(observations),
        "false_passes": false_passes,
        "false_fails": false_fails,
        "match_false_fail_rate": round(false_fail_rate, 4),
        "refusals": len(refusals),
        "refusal_rate": round(refusal_rate, 4),
        "repeat_consistency": round(consistency, 4),
        "failed_gates": failed_gates,
        "passed": not failed_gates and stopped_reason is None,
        "stopped_reason": stopped_reason,
    }


def qualify_candidate(candidate, guard: BudgetGuard) -> dict:
    """Devanagari first. Latin only for survivors. Stop the moment either gate or the budget says so."""
    c = contract()
    repeats = c["repeats_per_shape"]

    dev = _score_script(candidate, "devanagari", guard, repeats)
    result = {
        "candidate": candidate.name,
        "devanagari": dev,
        "latin": None,
        "qualified_scope": [],
        "stopped_after": "devanagari",
        "stopped_reason": dev["stopped_reason"],
        "synthetic": True,
        "may_populate_registry": False,
        "contract_status": c["status"],
        "qualified_scope_excludes": c["qualified_scope_excludes"],
    }
    if not dev["passed"]:
        return result

    lat = _score_script(candidate, "latin", guard, repeats)
    result["latin"] = lat
    result["stopped_after"] = "latin"
    result["stopped_reason"] = lat["stopped_reason"]
    if lat["passed"]:
        result["qualified_scope"] = ["devanagari", "latin"]
    return result


# --------------------------------------------------------------------------------------- run
def _dry_run(out: Path) -> dict:
    guard = BudgetGuard(authorised_usd=Decimal("6.00"))
    candidates = [
        qualify_candidate(FakeCandidate(name="fake-openai-candidate"), guard),
        qualify_candidate(FakeCandidate(name="fake-google-candidate",
                                        false_pass_on_first_mismatch=True), guard),
    ]
    result = {
        "record": "EMP-001-text-qualification",
        "dry_run": True,
        "synthetic": True,
        "may_populate_registry": False,
        "registry_rows_written": 0,
        "external_calls": 0,
        "spend_usd": "0",
        "simulated_spend_usd": str(guard.spent_usd),
        "candidates": candidates,
        "calls_per_candidate_per_script": CALLS_PER_SCRIPT,
        "maximum_evaluator_calls_if_all_survive": MAX_EVALUATOR_CALLS,
        "materials": {
            "devanagari": verify_devanagari_identity(),
            "latin_pack_sha256": hashlib.sha256(LATIN_PACK.read_bytes()).hexdigest(),
        },
        "note": ("Every candidate above is a deterministic local fake. This run proves the "
                 "protocol executes and stops where it should. It says NOTHING about any real "
                 "model, and no result here may reach the Capability Registry."),
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    return result


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="EMP-001 progressive text-judge qualification.")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--live", action="store_true",
                    help="requires an explicit authorisation file; refuses without one")
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    a = ap.parse_args(argv)

    if a.live:
        open_guard()  # raises NotAuthorised, which is the whole point
        raise NotAuthorised(
            "EMP-001 live qualification is not implemented in the zero-spend branch. Paid "
            "execution is Task 9 of the implementation plan and requires explicit user approval.")

    result = _dry_run(Path(a.out))
    print(f"dry run: {len(result['candidates'])} synthetic candidates")
    for c in result["candidates"]:
        latin = c["latin"]["calls"] if c["latin"] else 0
        print(f"  {c['candidate']:26} devanagari={c['devanagari']['calls']:4} latin={latin:4} "
              f"scope={c['qualified_scope'] or 'none'}")
    print(f"external calls: {result['external_calls']}   spend USD: {result['spend_usd']}")
    print(f"written: {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
