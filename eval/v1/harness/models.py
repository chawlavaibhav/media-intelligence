"""Core records for the generate-once evaluation harness.

TERMINOLOGY, because these words carry the whole design:

  ITEM      a frozen benchmark item from the E4 bank. A specification, not media.
  ATTEMPT   one call to a provider. Every call is a new attempt, always.
  ASSET     one artifact produced by one attempt. THE TRIAL.
  MEASUREMENT  one evaluator's verdict about one asset.

  REPEAT    a DELIBERATE re-run of the same item+config to estimate how
            reproducible a workflow is. It is part of the experiment design and
            is decided BEFORE the run.
  RETRY     a later attempt caused by a PREVIOUS attempt failing or being
            rejected. It is part of a production/repair chain and is decided
            AFTER seeing a result.

  THESE ARE NOT THE SAME THING (correction E-C4). Conflating them corrupts two
  different numbers in opposite directions:
    - counting a repeat as a retry inflates the apparent failure rate and makes
      a reliable workflow look like it needed rescuing;
    - counting a retry as a repeat hides real production cost, because only
      retries belong in the retry chain that Cost per Accepted Outcome divides
      by. CpAO would then be computed over too few attempts and read too cheap.

The rule the whole system exists to enforce:

    ONE ASSET IS ONE TRIAL, however many evaluators inspect it.

Twelve measurements of one asset are twelve measurements of ONE trial - not
twelve trials. Frames sampled from a clip carry their parent's trial id and add
no trials at all. Repeats measure reliability and are never base items.
Getting this wrong silently multiplies apparent confidence, which is the
single most expensive statistical error available to this project.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any
import hashlib
import json

# -----------------------------------------------------------------------------
# Result absence is NOT one thing. Collapsing these would let "we could not
# measure it" read as "it passed" or "it failed" - which is exactly the
# distinction a router must be able to make.
# -----------------------------------------------------------------------------
ABSENCE_REASONS = (
    "not_applicable",        # capability does not apply to this asset at all
    "not_measured",          # applicable, simply not run this time
    "instrument_unqualified",# an instrument exists but may not be trusted
    "generation_failed",     # no asset to measure
    "refused",               # provider declined to produce it
)

VERDICTS = ("pass", "fail", "absent")

QUALIFICATION_STATUSES = (
    "qualified",              # may write Registry rows
    "provisional",            # may NOT
    "screened_not_qualified", # may NOT
    "disqualified",           # may NOT
    "unmeasurable",           # may NOT
    "deterministic",          # may write - needs no calibration (e.g. file probe)
)
REGISTRY_WRITABLE = ("qualified", "deterministic")


def sha256_str(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def config_hash(cfg: dict) -> str:
    """Stable hash over the exact request configuration.

    Covers prompt, parameters, seed policy and reference hashes. Changing ANY of
    these makes a DIFFERENT experiment - this is Autonomy Policy stop condition 8
    ("changing an evaluator prompt and reporting the rerun as the original")
    made durable in the data rather than left to discipline.
    """
    return sha256_str(json.dumps(cfg, sort_keys=True, separators=(",", ":")))


@dataclass
class GenerationProvenance:
    """Everything needed to say what produced an asset, and to find it again.

    EXACTLY ONE of these exists per asset. That is invariant 1.
    """
    attempt_id: str
    asset_id: str
    item_id: str
    provider: str
    model: str
    version: str
    endpoint: str
    workflow: str
    lane: str
    config_hash: str
    config_path: str                       # recoverable, not just hashed
    input_hashes: list[str] = field(default_factory=list)
    reference_hashes: list[str] = field(default_factory=list)
    seed: Any = None
    seed_policy: str = "unsupported"
    requested_at: str = ""
    completed_at: str = ""
    api_status: str = "ok"                 # ok | error | refused | timeout
    error_class: str | None = None
    output_path: str | None = None
    output_sha256: str | None = None
    # Cost components stay SEPARATE. Folding evaluator cost into generation cost
    # hides a third or more of the true cost of an observation.
    cost_generation: float | None = None
    cost_transform: float | None = None
    currency: str = "USD"
    parent_asset_id: str | None = None     # set for frames/derived assets
    derivation: str | None = None          # e.g. "frame_sample@t=1.5s"

    # --- EXPERIMENTAL REPEAT (design-time) -----------------------------------
    # Deliberate re-run of the same item+config to estimate reproducibility.
    # repeat_index 0 is the first attempt of a repeat set, not a repeat itself.
    repeat_index: int = 0
    repeat_of_attempt_id: str | None = None

    # --- PRODUCTION RETRY (result-time) --------------------------------------
    # Caused by a prior attempt failing or being rejected. Belongs to the
    # accepted-outcome retry chain; a repeat NEVER does.
    retry_of_attempt_id: str | None = None
    retry_reason: str | None = None

    def is_experimental_repeat(self) -> bool:
        return self.repeat_of_attempt_id is not None

    def is_production_retry(self) -> bool:
        return self.retry_of_attempt_id is not None

    def to_dict(self):
        return asdict(self)


@dataclass
class Measurement:
    """One evaluator's verdict about one asset, for one capability."""
    measurement_id: str
    asset_id: str                 # the trial this measures
    trial_asset_id: str           # parent trial - equals asset_id unless derived
    item_id: str
    capability: str
    verdict: str                  # pass | fail | absent
    absence_reason: str | None = None
    instrument_id: str = ""
    instrument_version: str = ""
    instrument_config_hash: str = ""
    instrument_qualification_status: str = ""
    instrument_calibration_ref: str | None = None
    observation_unit: str = ""
    sampled_frames: int | None = None
    defects: list[dict] = field(default_factory=list)   # MULTIPLE per output
    cost_evaluator: float | None = None
    latency_s: float | None = None
    measured_at: str = ""
    synthetic: bool = False       # dummy-fixture provenance, never promotable

    def to_dict(self):
        return asdict(self)


@dataclass
class RegistryRow:
    """An empirical capability measurement. NONE MAY EXIST YET.

    A row may only be written by an instrument whose qualification status is in
    REGISTRY_WRITABLE, and never from synthetic measurements.
    """
    entry_id: str
    provider: str
    model: str
    version: str
    endpoint: str
    workflow: str
    capability: str
    difficulty_level: int
    observation_unit: str
    conditions: dict
    n_items: int                 # INDEPENDENT base items
    repeats_per_item: int
    trials: int                  # n_items x repeats_per_item
    passes: int
    pass_rate: float | None
    failed_trials: list[dict] = field(default_factory=list)
    instrument_id: str = ""
    instrument_version: str = ""
    instrument_config_hash: str = ""
    instrument_qualification_status: str = ""
    instrument_calibration_ref: str | None = None
    cost_generation_total: float | None = None
    cost_evaluator_total: float | None = None
    cost_human_total: float | None = None
    usd_per_pass: float | None = None
    usd_per_pass_lower_bound: float | None = None
    battery_version: str = ""
    # E-C8: uncertainty provenance. `status` is mandatory; a row carries either
    # an interval WITH its method and assumptions, or an explicit reason it was
    # not computed. Never a bare point estimate presented as exact.
    uncertainty: dict = field(default_factory=lambda: {
        "status": "not_computed",
        "not_computed_reason": "instrument_unqualified",
        "not_computed_note": (
            "No instrument is qualified, so no interval could be attached to "
            "any number. This is the honest state, not a gap."),
    })
    run_ref: str = ""
    tested_date: str = ""
    sample_source: str = "lab"
    synthetic: bool = False

    def to_dict(self):
        return asdict(self)
