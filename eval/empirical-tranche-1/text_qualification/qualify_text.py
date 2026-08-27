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
import time
import unicodedata
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKAGE_ROOT = HERE.parent
REPO_ROOT = PACKAGE_ROOT.parent.parent

sys.path.insert(0, str(PACKAGE_ROOT))
from budget_guard import BudgetExceeded, BudgetGuard, NotAuthorised, open_guard  # noqa: E402
import providers as P  # noqa: E402
import human_review as HR  # noqa: E402

import yaml  # noqa: E402

CONTRACT = HERE / "qualification-contract-v2.yaml"
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
                 "expected": v["expected_verdict"], "drawn": v["rendered_string"],
                 "failure_class": v.get("failure_class"),
                 "failure_group": v.get("failure_group"),
                 "edit_detail": v.get("edit_detail")}
                for v in load_devanagari_items()]
    return [{"item_id": v["item_id"], "target": v["target_string"],
             "expected": v["expected"], "drawn": v["rendered_string"],
             "failure_class": v.get("failure_class"),
             "failure_group": v.get("failure_group"),
             "edit_detail": v.get("edit_detail")}
            for v in load_latin_items()]


# --------------------------------------------------------------------------------- images
LATIN_IMAGES = HERE / "build" / "images"
DEVANAGARI_CHECKER_INPUT = DEVANAGARI_VIEW / "checker-input-transcribe.jsonl"


class ImageIntegrityError(RuntimeError):
    """The bytes on disk are not the bytes the manifest says they are."""


class ImageResolver:
    """Resolve an item id to the exact image bytes a judge should be shown.

    The checker contract is explicit: resolve the path, read the file, and CONFIRM THE HASH before
    sending anything. A judge scored against different bytes than we believe we sent is not a weak
    measurement, it is not a measurement — and the failure is silent, which is the worst kind.

    Devanagari images carry an authoritative `image_file_sha256` in the committed checker-input
    projection, so they are verified strictly. Latin images are a local render of a committed
    string; their hash is computed and recorded, and verified against the perceptibility record
    wherever that record pins one.
    """

    def __init__(self):
        self._cache: dict[tuple[str, str], bytes] = {}
        self._expected: dict[tuple[str, str], str] = {}
        self._paths: dict[tuple[str, str], Path] = {}
        self._load_devanagari()
        self._load_latin()

    def _load_devanagari(self) -> None:
        if not DEVANAGARI_CHECKER_INPUT.exists():
            return
        base = DEVANAGARI_CHECKER_INPUT.parent
        for line in DEVANAGARI_CHECKER_INPUT.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            key = ("devanagari", row["item_id"])
            self._paths[key] = (base / row["image_file"]).resolve()
            self._expected[key] = row["image_file_sha256"]

    def _load_latin(self) -> None:
        record = HERE / "perceptibility-mechanical.json"
        pinned = {}
        if record.exists():
            for row in json.loads(record.read_text(encoding="utf-8"))["items"]:
                pinned[row["item_id"]] = row["rendered_image_file_sha256"]
        for path in sorted(LATIN_IMAGES.glob("lx-*.png")):
            key = ("latin", path.stem)
            self._paths[key] = path
            if path.stem in pinned:
                self._expected[key] = pinned[path.stem]

    def _key(self, script: str, item_id: str) -> tuple[str, str]:
        key = (script, item_id)
        if key not in self._paths:
            raise FileNotFoundError(
                f"no rendered image for {script} item {item_id}. Both image sets are reproducible "
                f"build products; rebuild them with the commands in "
                f"eval/empirical-tranche-1/README.md.")
        return key

    def bytes_for(self, script: str, item_id: str) -> bytes:
        key = self._key(script, item_id)
        if key not in self._cache:
            data = self._paths[key].read_bytes()
            self.verify_bytes(script, item_id, data)
            self._cache[key] = data
        return self._cache[key]

    def verify_bytes(self, script: str, item_id: str, data: bytes) -> str:
        """Return the sha256, raising if it contradicts a pinned expectation."""
        key = self._key(script, item_id)
        digest = hashlib.sha256(data).hexdigest()
        expected = self._expected.get(key)
        if expected and digest != expected:
            raise ImageIntegrityError(
                f"{script} item {item_id}: image on disk hashes {digest[:16]}… but the manifest "
                f"pins {expected[:16]}…. Refusing to send bytes we cannot identify.")
        return digest

    def verified(self, script: str, item_id: str) -> bool:
        """True when this item's bytes were checked against a pinned hash, not merely read."""
        key = self._key(script, item_id)
        if key not in self._expected:
            return False
        self.bytes_for(script, item_id)
        return True

    def sha256_for(self, script: str, item_id: str) -> str:
        return hashlib.sha256(self.bytes_for(script, item_id)).hexdigest()


# ------------------------------------------------------------------------------ live candidate
class LiveCandidate:
    """A real `TextJudge` participating in the qualification protocol.

    This is the class EVAL-012 was missing. `--live` opened a valid authorisation guard and then
    raised unconditionally, so the real judges never took part and only `FakeCandidate` was ever
    scored. Everything downstream — the progressive stop, the gates, the persistence shape — was
    therefore only ever proved against a fake.

    The judge owns the budget guard and performs its own reserve/record around each dispatch, so
    `manages_own_budget` is True and the scorer must not double-count. `synthetic` is False:
    evidence produced here is real evidence about whatever the transport actually talked to.
    """

    synthetic = False
    manages_own_budget = True

    def __init__(self, judge: "P.TextJudge", images: ImageResolver, name: str | None = None,
                 min_dispatch_interval_seconds: float = 0.0, clock=None, sleeper=None):
        self.judge = judge
        self.images = images
        self.name = name or f"{judge.provider}:{judge.resolved_version}"
        self.calls = 0
        self.retries = 0
        self.calls_by_script = {s: 0 for s in SCRIPTS}
        self.min_dispatch_interval_seconds = max(0.0, float(min_dispatch_interval_seconds))
        self._clock = clock or time.monotonic
        self._sleeper = sleeper or time.sleep
        self._last_dispatch_at = None

    def _pace(self) -> None:
        if self.min_dispatch_interval_seconds <= 0:
            return
        now = self._clock()
        if self._last_dispatch_at is not None:
            remaining = self.min_dispatch_interval_seconds - (now - self._last_dispatch_at)
            if remaining > 0:
                self._sleeper(remaining)
        self._last_dispatch_at = self._clock()

    def estimate_usd(self) -> Decimal:
        return self.judge._estimate()

    def _run(self):
        budget = getattr(self.judge.guard, "budget", None)
        return getattr(budget, "run", None)

    def run_id(self) -> str:
        """The EMP-001 run this candidate's spend belongs to, if it has a persistent budget."""
        return getattr(self._run(), "run_id", "no-run")

    def evidence_mode(self) -> str:
        """`live` or `fake_live`, taken from the RUN record.

        Never hard-coded. A-TEXT refuses to be handed fake-live evidence, so this label is load
        bearing: if it lied, a rehearsal could open a paid stage.
        """
        return getattr(self._run(), "mode", "live")

    def trial_id(self, script: str, item: dict, shape: str, pass_index: int) -> str:
        """Durable, unique and DETERMINISTIC.

        Derived from the run, the exact model version and the experimental coordinates rather
        than from a counter, so the same call in a resumed process gets the same id and a
        duplicate is visible as a duplicate instead of appearing to be a new trial.
        """
        return (f"{self.run_id()}:{self.judge.provider}:{self.judge.resolved_version}"
                f":{script}:{item['item_id']}:{shape}:p{pass_index}")

    def call(self, script: str, item: dict, shape: str, pass_index: int) -> dict:
        """One call. One trial. No loop, no retry — a refusal returns a record and we move on."""
        self.calls += 1
        self.calls_by_script[script] += 1

        trial_id = self.trial_id(script, item, shape, pass_index)
        # One provider call is one trial, and for a root call the trial IS the attempt
        # (eval/v1/harness/models.py). Both are carried so the record stays topology-compatible.
        self.judge.call_context = {
            "trial_id": trial_id,
            "attempt_id": trial_id,
            "script": script,
            "item_id": item["item_id"],
            "shape": shape,
            "pass_index": pass_index,
            "stage": "qualification",
        }

        image_bytes = self.images.bytes_for(script, item["item_id"])
        self._pace()
        if shape == "transcribe":
            # The target is passed for the BLIND CHECK only. It is never placed in the payload;
            # it is what the payload is proved not to contain.
            response = self.judge.transcribe(image_bytes, blind_check_target=item["target"])
        else:
            response = self.judge.verdict(image_bytes, item["target"])

        record = self.judge.call_record(response, shape=shape)
        record.update({
            "image_sha256": hashlib.sha256(image_bytes).hexdigest(),
            "synthetic": False,
            "evidence_mode": self.evidence_mode(),
        })
        return {
            "api_status": response.api_status,
            "text": response.text,
            "cost": response.billed_usd if response.billed_usd is not None else Decimal("0"),
            "call_record": record,
            "ambiguous_dispatch": response.ambiguous_dispatch,
        }


# ------------------------------------------------------------------------------ fake candidate
class FakeCandidate:
    """A deterministic stand-in for a judge. Makes no network call, ever.

    It counts its calls per script so the progressive stop can be proved by measurement rather
    than by inspection, and it exposes `retries`, which must stay 0.
    """

    COST_PER_CALL = Decimal("0.0021")
    synthetic = True
    manages_own_budget = False      # the scorer reserves and records on its behalf

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

    def estimate_usd(self) -> Decimal:
        return self.COST_PER_CALL

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


def _metrics(observations: list[dict]) -> dict:
    """Compute one metric set over an explicitly selected observation slice."""
    mismatches = [o for o in observations if o["expected"] == "mismatch"]
    matches = [o for o in observations if o["expected"] == "match"]
    refusals = [o for o in observations if o["observed"] == "refusal"]
    scoreable = [o for o in observations if o["observed"] in ("match", "mismatch")]

    false_passes = sum(1 for o in mismatches if o["observed"] == "match")
    false_fails = sum(1 for o in matches if o["observed"] == "mismatch")

    scored_matches = [o for o in matches if o["observed"] != "refusal"]
    false_fail_rate = false_fails / len(scored_matches) if scored_matches else 0.0
    refusal_rate = len(refusals) / len(observations) if observations else 0.0

    by_cell: dict[tuple[str, str], set] = {}
    for o in scoreable:
        by_cell.setdefault((o["item_id"], o["shape"]), set()).add(o["observed"])
    consistency = (sum(1 for values in by_cell.values() if len(values) == 1) / len(by_cell)
                   if by_cell else 0.0)

    return {
        "calls": len(observations),
        "match_opportunities": len(matches),
        "mismatch_opportunities": len(mismatches),
        "false_passes": false_passes,
        "false_pass_rate": round(false_passes / len(mismatches), 4) if mismatches else 0.0,
        "false_fails": false_fails,
        "match_false_fail_rate": round(false_fail_rate, 4),
        "refusals": len(refusals),
        "refusal_rate": round(refusal_rate, 4),
        "repeat_consistency": round(consistency, 4),
        "unique_false_pass_items": len({
            o["item_id"] for o in mismatches if o["observed"] == "match"
        }),
    }


def _score_script(candidate, script: str, guard: BudgetGuard, repeats: int) -> dict:
    """Run every item x shape x pass. Only the contract's primary shape decides qualification."""
    items = _script_items(script)
    observations: list[dict] = []
    stopped_reason = None

    # Budget accounting belongs to exactly ONE layer. A live judge reserves and records around
    # its own dispatch, so the scorer must not do it again — double-counting would exhaust the
    # ceiling at half the calls and look like a budget stop rather than a bug.
    owns_budget = getattr(candidate, "manages_own_budget", False)
    call_records: list[dict] = []

    for pass_index in range(repeats):
        for shape in SHAPES:
            for item in items:
                try:
                    if not owns_budget:
                        guard.reserve(candidate.estimate_usd())
                    reply = candidate.call(script, item, shape, pass_index)
                    if not owns_budget:
                        guard.record(reply["cost"])
                except BudgetExceeded:
                    # Raised either here or inside the judge, before anything was dispatched.
                    stopped_reason = "budget_exhausted"
                    break
                if reply.get("call_record"):
                    call_records.append(reply["call_record"])
                observations.append({
                    "item_id": item["item_id"],
                    "shape": shape,
                    "pass": pass_index,
                    "expected": item["expected"],
                    "observed": _observed_verdict(shape, item, reply),
                    "api_status": reply.get("api_status"),
                    "target": item["target"],
                    "rendered_string": item["drawn"],
                    "failure_class": item.get("failure_class"),
                    "failure_group": item.get("failure_group"),
                    "edit_detail": item.get("edit_detail"),
                    "evaluator_response": reply.get("text", ""),
                })

                if reply.get("ambiguous_dispatch"):
                    # The provider may have received and billed that call, and we have no usable
                    # answer. The trial above is persisted with its cost; the run STOPS rather
                    # than carrying on as though nothing happened. Retries remain 0, so there is
                    # no second attempt to make — the only choices were stop or pretend.
                    stopped_reason = "ambiguous_dispatch"
                    break
            if stopped_reason:
                break
        if stopped_reason:
            break

    c = contract()
    primary_shape = c["primary_generated_output_shape"]
    metrics_by_shape = {
        shape: _metrics([o for o in observations if o["shape"] == shape])
        for shape in SHAPES
    }
    primary = metrics_by_shape[primary_shape]
    pooled = _metrics(observations)

    failed_gates = []
    if primary["false_passes"] > c["mismatch_false_pass_max"]:
        failed_gates.append("mismatch_false_pass")
    if primary["match_false_fail_rate"] > c["match_false_fail_rate_max"]:
        failed_gates.append("match_false_fail_rate")
    if primary["refusal_rate"] > c["refusal_rate_max"]:
        failed_gates.append("refusal_rate")
    if primary["repeat_consistency"] < c["repeat_consistency_min"]:
        failed_gates.append("repeat_consistency")

    return {
        "script": script,
        "calls": primary["calls"],
        "total_dispatches": len(observations),
        "primary_shape": primary_shape,
        # Top-level gate metrics are intentionally the PRIMARY blind-shape metrics.
        "false_passes": primary["false_passes"],
        "false_pass_rate": primary["false_pass_rate"],
        "false_fails": primary["false_fails"],
        "match_false_fail_rate": primary["match_false_fail_rate"],
        "refusals": primary["refusals"],
        "refusal_rate": primary["refusal_rate"],
        "repeat_consistency": primary["repeat_consistency"],
        "unique_false_pass_items": primary["unique_false_pass_items"],
        "metrics_by_shape": metrics_by_shape,
        "pooled_diagnostic_metrics": pooled,
        "failed_gates": failed_gates,
        "passed": not failed_gates and stopped_reason is None,
        "stopped_reason": stopped_reason,
        "observations": observations,
        "call_records": call_records,
    }


def qualify_candidate(candidate, guard: BudgetGuard, perceptibility_path: Path | str | None = None) -> dict:
    """Devanagari first. Latin only for survivors and only after the human review is valid."""
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
        # From the CANDIDATE, never a constant. Mislabelling real evidence as synthetic would
        # discard it; mislabelling synthetic evidence as real would promote it.
        "synthetic": getattr(candidate, "synthetic", True),
        "may_populate_registry": False,
        "contract_status": c["status"],
        "qualified_scope_excludes": c["qualified_scope_excludes"],
    }
    if not dev["passed"]:
        return result

    human = HR.review_status(perceptibility_path)
    result["latin_human_review"] = human
    if not human["ok"]:
        result["stopped_reason"] = "latin_human_perceptibility_unresolved"
        return result

    lat = _score_script(candidate, "latin", guard, repeats)
    result["latin"] = lat
    result["stopped_after"] = "latin"
    result["stopped_reason"] = lat["stopped_reason"]
    if lat["passed"]:
        result["qualified_scope"] = ["devanagari", "latin"]
    return result


# ------------------------------------------------------------------- persisted qualification
QUALIFICATION_FILENAME = "qualification-result.json"

# Fields the fingerprint is computed over. Everything that decides whether A-TEXT may open.
FINGERPRINTED_FIELDS = ("run_id", "tranche_id", "mode", "synthetic", "qualified", "candidates", "call_records", "contract_sha256")


def qualification_fingerprint(payload: dict) -> str:
    """SHA-256 over the claim AND the evidence that produced it.

    This is what stops a hand-edited `qualified_scope` from opening a paid stage. The claim is not
    trusted on its own: it is bound to the call records behind it, so widening the claim without
    also producing the calls changes the fingerprint and the handoff refuses.
    """
    material = {k: payload.get(k) for k in FINGERPRINTED_FIELDS}
    canonical = json.dumps(material, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                           default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def build_qualification_result(run, results: list[dict], candidates: list) -> dict:
    """Assemble the persistable qualification record for one EMP-001 run."""
    call_records = []
    for r in results:
        call_records.extend(r["devanagari"]["call_records"])
        if r["latin"]:
            call_records.extend(r["latin"]["call_records"])

    qualified = []
    for result, candidate in zip(results, candidates):
        if not result["qualified_scope"]:
            continue
        qualified.append({
            "candidate": result["candidate"],
            "provider": candidate.judge.provider,
            "model_alias": candidate.judge.model_alias,
            "resolved_version": candidate.judge.resolved_version,
            "qualified_scope": sorted(result["qualified_scope"]),
        })

    payload = {
        "record": "EMP-001-qualification-result",
        "run_id": run.run_id,
        "tranche_id": "EMP-001",
        "mode": run.mode,
        "synthetic": run.mode not in ("live",),
        "qualified": qualified,
        "candidates": results,
        "call_records": call_records,
        "contract_status": contract()["status"],
        "contract_version": contract().get("contract_version"),
        "contract_sha256": hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
        "qualified_scope_excludes": contract()["qualified_scope_excludes"],
        "note": ("Qualification running is not promotion. A qualified judge may MEASURE the "
                 "A-TEXT screen; it does not by itself put a row in the Capability Registry."),
    }
    payload["evidence_fingerprint"] = qualification_fingerprint(payload)
    return payload


def persist_qualification(run, payload: dict) -> Path:
    """Write the qualification result into the run's evidence directory."""
    path = run.evidence_dir / QUALIFICATION_FILENAME
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True,
                               default=str) + "\n", encoding="utf-8")
    return path


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
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True,
                              default=str) + "\n", encoding="utf-8")
    return result


def build_live_candidates(guard: BudgetGuard, http=None, images: ImageResolver | None = None,
                          resolved_versions: dict | None = None,
                          only_provider: str | None = None,
                          min_dispatch_interval_seconds: float = 0.0) -> list[LiveCandidate]:
    """Construct the two frozen judge candidates behind whatever transport is supplied.

    `http` is the injected HTTP layer. Passing None means the real socket, which is why nothing in
    this branch ever calls it that way — every exercise here injects a recorder.

    Versions must be pinned by the caller at execution. The aliases in config.yaml are NOT
    versions, and a judge refuses to exist without a resolved one.
    """
    import yaml as _yaml

    cfg = _yaml.safe_load((PACKAGE_ROOT / "config.yaml").read_text(encoding="utf-8"))
    images = images or ImageResolver()
    resolved_versions = resolved_versions or {}

    candidates = []
    for spec in cfg["qualification"]["judge_candidates"]:
        provider, alias = spec["provider"], spec["model_alias"]
        if only_provider is not None and provider != only_provider:
            continue
        version = resolved_versions.get(provider)
        if not version:
            raise NotAuthorised(
                f"no resolved version pinned for {provider} ({alias}). The exact model snapshot "
                f"must be pinned at execution; an alias is not a version.")
        judge_cls = {
            "anthropic": P.AnthropicTextJudge,
            "google": P.GeminiTextJudge,
            "openai": P.OpenAITextJudge,
        }.get(provider)
        if judge_cls is None:
            raise NotAuthorised(f"unsupported judge provider {provider!r}")
        candidates.append(LiveCandidate(
            judge=judge_cls(model_alias=alias, resolved_version=version,
                            transport=P.transport_for(provider, version, http=http),
                            guard=guard),
            images=images,
            min_dispatch_interval_seconds=min_dispatch_interval_seconds))
    return candidates


def run_live(guard: BudgetGuard, http=None, resolved_versions: dict | None = None,
             mode: str = "live", only_provider: str | None = None, run=None,
             min_dispatch_interval_seconds: float = 0.0) -> dict:
    """The real orchestration. Devanagari first; Latin only for survivors; one shared ceiling.

    The guard is shared across BOTH candidates and BOTH scripts, exactly as frozen: the ceiling is
    a property of the tranche, not of each candidate, so a first candidate that spends most of it
    correctly starves the second rather than quietly doubling the budget.
    """
    images = ImageResolver()
    candidates = build_live_candidates(
        guard, http=http, images=images,
        resolved_versions=resolved_versions,
        only_provider=only_provider,
        min_dispatch_interval_seconds=min_dispatch_interval_seconds)

    results = []
    for candidate in candidates:
        results.append(qualify_candidate(candidate, guard=guard))

    dispatches = sum(c.calls for c in candidates)
    if run is not None:
        qualification_payload = build_qualification_result(run, results, candidates)
        persist_qualification(run, qualification_payload)
    return {
        "record": "EMP-001-text-qualification",
        "mode": mode,
        "dry_run": False,
        "synthetic": False,
        "may_populate_registry": False,
        "registry_rows_written": 0,
        "candidates": results,
        "dispatches": dispatches,
        "calls_per_candidate_per_script": CALLS_PER_SCRIPT,
        "maximum_evaluator_calls_if_all_survive": MAX_EVALUATOR_CALLS,
        "spend_recorded_usd": str(guard.spent_usd),
        "authorised_ceiling_usd": str(guard.authorised_usd),
        "materials": {
            "devanagari": verify_devanagari_identity(),
            "latin_pack_sha256": hashlib.sha256(LATIN_PACK.read_bytes()).hexdigest(),
        },
        "qualified_candidates": [r["candidate"] for r in results if r["qualified_scope"]],
        "note": ("Qualification running is not promotion. A qualified judge may measure the "
                 "A-TEXT screen; it does not by itself put a row in the Capability Registry."),
    }


def _fake_live(guard, out: Path, run=None, only_provider: str | None = None) -> dict:
    """The real orchestration with an injected recorder standing where the socket would be.

    Proves the positive path end to end at zero spend. Its results are labelled `fake_live` and
    are no more promotable than a dry run: a perfect reader is not a real one.
    """
    import os

    from fake_live import FakeJudgeHttp, image_index_for

    os.environ.setdefault("ANTHROPIC_API_KEY", "fake-live-anthropic-key")
    os.environ.setdefault("GOOGLE_API_KEY", "fake-live-google-key")

    index = image_index_for("both")
    http_by_provider = {
        "anthropic": FakeJudgeHttp(P.AnthropicTextJudge, index),
        "google": FakeJudgeHttp(P.GeminiTextJudge, index),
    }

    images = ImageResolver()
    all_candidates = {
        "anthropic": LiveCandidate(judge=P.AnthropicTextJudge(
            model_alias="claude-sonnet-5", resolved_version="claude-sonnet-5",
            transport=P.AnthropicHttpTransport("claude-sonnet-5",
                                               http=http_by_provider["anthropic"]),
            guard=guard), images=images),
        "google": LiveCandidate(judge=P.GeminiTextJudge(
            model_alias="gemini-3.5-flash-lite", resolved_version="FAKE-LIVE-google-snapshot",
            transport=P.GeminiHttpTransport("FAKE-LIVE-google-snapshot",
                                            http=http_by_provider["google"]),
            guard=guard), images=images),
    }
    selected = [only_provider] if only_provider else ["anthropic", "google"]
    candidates = [all_candidates[p] for p in selected]

    results = [qualify_candidate(c, guard=guard) for c in candidates]

    # Persist the qualification into the run so a LATER, SEPARATE process can consume it.
    # This is the whole point of the handoff: the next stage reads evidence off disk, not out of
    # a variable that died with the process that made it.
    if run is not None:
        payload = build_qualification_result(run, results, candidates)
        persist_qualification(run, payload)

    payload = {
        "record": "EMP-001-text-qualification",
        "mode": "fake_live",
        "dry_run": False,
        "synthetic": False,
        "may_populate_registry": False,
        "registry_rows_written": 0,
        "external_calls": 0,
        "spend_usd": "0",
        "candidates": results,
        "dispatches": sum(len(http_by_provider[p].calls) for p in selected),
        "simulated_spend_usd": str(guard.spent_usd),
        "calls_per_candidate_per_script": CALLS_PER_SCRIPT,
        "selected_providers": selected,
        "maximum_evaluator_calls_if_all_survive": CALLS_PER_SCRIPT * 2 * len(candidates),
        "materials": {
            "devanagari": verify_devanagari_identity(),
            "latin_pack_sha256": hashlib.sha256(LATIN_PACK.read_bytes()).hexdigest(),
        },
        "note": ("The real orchestration, the real judges, the real transports and the real "
                 "scorer, with an injected recorder standing where the socket would be. It "
                 "proves the positive path executes. It is NOT evidence about any model: a "
                 "perfect reader is not a real one, and nothing here may reach the Registry."),
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True,
                              default=str) + "\n", encoding="utf-8")
    return payload


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="EMP-001 progressive text-judge qualification.")
    ap.add_argument("--dry-run", action="store_true",
                    help="synthetic protocol simulation; no judge, no transport")
    ap.add_argument("--fake-live", action="store_true",
                    help="the real orchestration with an injected recorder; zero network")
    ap.add_argument("--live", action="store_true",
                    help="real paid execution; requires explicit authorisation and pinned versions")
    ap.add_argument("--authorisation", default=None)
    ap.add_argument("--run-root", default=None,
                    help="persistent EMP-001 run root; enables the durable tranche ledger")
    ap.add_argument("--run-id", default=None)
    ap.add_argument("--anthropic-version", default=None)
    ap.add_argument("--gemini-version", default=None)
    ap.add_argument("--only-provider", choices=["anthropic", "google"], default=None,
                    help="bounded continuation: run only one configured judge provider")
    ap.add_argument("--min-dispatch-interval-seconds", type=float, default=0.0,
                    help="minimum spacing between evaluator dispatch starts; operational only")
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    a = ap.parse_args(argv)

    if a.live or a.fake_live:
        # Fails closed for BOTH: the fake-live path deliberately walks the same authorisation
        # gate, so exercising it also exercises the gate a paid run must pass.
        authorisation = open_guard(a.authorisation) if a.authorisation else open_guard()

        run = None
        guard = authorisation
        if a.run_root and a.run_id:
            import spend_ledger as SL

            root = Path(a.run_root)
            mode = "fake_live" if a.fake_live else "live"
            try:
                run = SL.TrancheRun.open(root, a.run_id)
            except SL.LedgerCorrupt:
                run = SL.TrancheRun.create(root, a.run_id,
                                           authorisation_path=a.authorisation or "", mode=mode)
            # The stage cap lives here, not in the authorisation file: USD 6 for qualification
            # even when the authorisation names the full USD 10.
            guard = SL.TrancheBudget(run).stage("qualification")

        if a.fake_live:
            result = _fake_live(guard, Path(a.out), run=run, only_provider=a.only_provider)
            print(f"fake-live: {result['dispatches']} recorded dispatches, 0 network calls")
            for c in result["candidates"]:
                latin = c["latin"]["calls"] if c["latin"] else 0
                print(f"  {c['candidate']:34} devanagari={c['devanagari']['calls']:4} "
                      f"latin={latin:4} scope={c['qualified_scope'] or 'none'}")
            print(f"external calls: {result['external_calls']}   spend USD: {result['spend_usd']}")
            print(f"written: {a.out}")
            return 0

        versions = {"anthropic": a.anthropic_version, "google": a.gemini_version}
        required = [a.only_provider] if a.only_provider else ["anthropic", "google"]
        missing = [p for p in required if not versions.get(p)]
        if missing:
            raise NotAuthorised(
                f"--live is missing exact model ID(s) for: {missing}. A run that cannot name "
                "what it called cannot be reproduced.")

        result = run_live(
            guard, http=None, resolved_versions=versions,
            only_provider=a.only_provider, run=run,
            min_dispatch_interval_seconds=a.min_dispatch_interval_seconds)
        out = Path(a.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True,
                                  default=str) + "\n", encoding="utf-8")
        print(f"live: {result['dispatches']} dispatches, "
              f"spend USD {result['spend_recorded_usd']}")
        print(f"written: {out}")
        return 0

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
