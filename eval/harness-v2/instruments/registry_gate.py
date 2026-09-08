"""registry_gate: the only path from a measurement to a Registry row, and the uncertainty it must carry.

    deterministic_capabilities()        the 8 ids in EVALUATOR-PLAN.yaml -> deterministic_capabilities
    assert_registry_eligible(cap, inst) refuses any other capability, any instrument that is not
                                        deterministic / qualified, and an instrument not specified for cap
    assert_measurements_real(ms)        refuses a synthetic measurement (the frozen harness also refuses)
    measurements_to_cell(ms)            n_items, repeats_per_item, trials, passes, absence_reason, from measurements
    clopper_pearson(k, n)               exact binomial interval by bisection (stdlib)
    attach_uncertainty(row)             SCHEMA-v1 `uncertainty`: computed, clopper_pearson_95, over base_items,
                                        independence NOT ESTABLISHED, is_reference_calculation_only true
This task writes no Registry row and no data row under eval/registry/.
"""
from __future__ import annotations

import math
from collections import Counter
from pathlib import Path

import yaml

import hv2_paths
from models import REGISTRY_WRITABLE


class RegistryGateRefused(RuntimeError):
    """Nothing about this measurement may become a Registry row."""


def deterministic_capabilities(path: Path | str = hv2_paths.EVALUATOR_PLAN) -> set:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    caps = data.get("deterministic_capabilities") or []
    if not isinstance(caps, list) or not caps:
        raise RegistryGateRefused(f"{path} names no deterministic_capabilities")
    return set(caps)


def assert_registry_eligible(capability: str, instrument, plan_path: Path | str = hv2_paths.EVALUATOR_PLAN) -> None:
    allowed = deterministic_capabilities(plan_path)
    if capability not in allowed:
        raise RegistryGateRefused(f"capability {capability!r} is not one of EVALUATOR-PLAN's deterministic capabilities {sorted(allowed)}; "
                                  f"no deterministic instrument may write it")
    status = getattr(instrument, "qualification_status", None)
    if status not in REGISTRY_WRITABLE:
        raise RegistryGateRefused(f"instrument {getattr(instrument, 'id', instrument)!r} has qualification status {status!r}; only {REGISTRY_WRITABLE} may write")
    if capability not in getattr(instrument, "capabilities", set()):
        raise RegistryGateRefused(f"instrument {instrument.id!r} is not specified for capability {capability!r}; qualification never generalises")


def assert_measurements_real(measurements) -> None:
    bad = [m for m in measurements if getattr(m, "synthetic", True)]
    if bad:
        raise RegistryGateRefused(f"{len(bad)} measurement(s) are synthetic; a synthetic measurement never becomes a Registry row")


def measurements_to_cell(measurements) -> dict:
    items = {m.item_id for m in measurements}
    verdicts = Counter(m.verdict for m in measurements)
    reasons = Counter(m.absence_reason for m in measurements if m.verdict == "absent" and m.absence_reason)
    n_items = len(items)
    trials = len(measurements)
    per_item = Counter(m.item_id for m in measurements)
    balanced = n_items > 0 and len(set(per_item.values())) == 1
    return {
        "n_items": n_items, "trials": trials, "repeats_per_item": (trials // n_items if balanced else None),
        "balanced": balanced, "passes": verdicts.get("pass", 0), "fails": verdicts.get("fail", 0), "absent": verdicts.get("absent", 0),
        "absence_reasons": dict(reasons), "absence_reason": (reasons.most_common(1)[0][0] if reasons else None),
    }


def _binom_cdf(k: int, n: int, p: float) -> float:
    if p <= 0:
        return 1.0
    if p >= 1:
        return 1.0 if k >= n else 0.0
    return sum(math.comb(n, i) * (p ** i) * ((1 - p) ** (n - i)) for i in range(0, k + 1))


def _bisect(fn, target: float, lo: float = 0.0, hi: float = 1.0, iters: int = 200) -> float:
    """fn is monotone decreasing in p; find p with fn(p) == target."""
    for _ in range(iters):
        mid = (lo + hi) / 2
        if fn(mid) > target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def clopper_pearson(k: int, n: int, level: float = 0.95) -> tuple:
    if n <= 0 or k < 0 or k > n:
        raise ValueError(f"need 0 <= k <= n with n > 0, got k={k}, n={n}")
    alpha = 1 - level
    # lower: P(X >= k | p_lo) = alpha/2  <=>  P(X <= k-1 | p_lo) = 1 - alpha/2   (the CDF is decreasing in p)
    lo = 0.0 if k == 0 else _bisect(lambda p: _binom_cdf(k - 1, n, p), 1 - alpha / 2)
    # upper: P(X <= k | p_hi) = alpha/2
    hi = 1.0 if k == n else _bisect(lambda p: _binom_cdf(k, n, p), alpha / 2)
    return lo, hi


def attach_uncertainty(row, level: float = 0.95) -> dict:
    """Fill SCHEMA-v1 `uncertainty` on a row (dict or RegistryRow) from n_items / repeats_per_item / passes."""
    get = (lambda k: row.get(k)) if isinstance(row, dict) else (lambda k: getattr(row, k, None))
    n_items, reps, passes, trials = get("n_items"), get("repeats_per_item") or 1, get("passes") or 0, get("trials")
    if not n_items:
        raise ValueError("row has no n_items")
    k_items = passes / reps
    k = int(round(k_items))
    lo, hi = clopper_pearson(k, n_items, level)
    u = {
        "status": "computed", "method": f"clopper_pearson_{int(level * 100)}",
        "interval_low": round(lo, 6), "interval_high": round(hi, 6), "interval_level": level,
        "computed_over": "base_items", "n_used": n_items,
        "assumptions": [
            "exact binomial (Clopper-Pearson) under an iid Bernoulli model the battery does not establish",
            f"item-level successes taken as passes / repeats_per_item = {passes} / {reps} = {k_items:g}, rounded to {k}; a trial-balanced cell",
            "repeats of one item are one item, never extra independent observations",
            "one generator and one blueprint per case: errors may be correlated across items",
        ],
        "independence_status": "NOT ESTABLISHED", "is_reference_calculation_only": True,
        "note": "a sizing reference under SCHEMA-v1; never the instrument's or the model's real-world error rate",
    }
    if isinstance(row, dict):
        row["uncertainty"] = u
    else:
        row.uncertainty = u
    return {"uncertainty": u, "trials": trials}
