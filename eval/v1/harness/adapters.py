"""Dummy generators and evaluator adapters. SYNTHETIC ONLY.

Nothing here calls a network, a model or a paid API. Every output is fabricated
locally and deterministically so the harness's plumbing can be exercised without
spending anything and without producing anything that could be mistaken for
evidence.

Every measurement these produce is flagged synthetic=True, and the harness
refuses to promote a synthetic measurement into a Registry row.
"""
from __future__ import annotations


# ------------------------------------------------------------------ generators
def dummy_generator(item, cfg):
    """Fabricate an artifact. The payload encodes what the item asked for so the
    dummy evaluators have something deterministic to 'read'."""
    defects = cfg.get("inject_defects", [])
    payload = (f"SYNTHETIC_ASSET item={item['item_id']} "
               f"modality={item.get('modality','image')} "
               f"model={cfg.get('model','dummy')} "
               f"defects={','.join(defects) if defects else 'none'}")
    return {"api_status": "ok", "payload": payload,
            "cost_generation": cfg.get("unit_price", 0.10)}


def refusing_generator(item, cfg):
    """A refusal that STILL COSTS MONEY.

    EI-C6: a refused call consumed latency and may well have been billed. These
    adapters previously hardcoded cost 0.0, which meant the self-test could not
    detect a cost calculation that dropped failed attempts - the bug and the
    test were blind in the same place.
    """
    return {"api_status": "refused", "error_class": "moderation_block",
            "cost_generation": cfg.get("unit_price", 0.0)}


def erroring_generator(item, cfg):
    """An error that STILL COSTS MONEY. See refusing_generator."""
    return {"api_status": "error", "error_class": "timeout",
            "cost_generation": cfg.get("unit_price", 0.0)}


def timeout_generator(item, cfg):
    return {"api_status": "timeout", "error_class": "deadline_exceeded",
            "cost_generation": cfg.get("unit_price", 0.0)}


# ------------------------------------------------------------------ evaluators
def _defects_in(payload):
    for part in payload.split():
        if part.startswith("defects="):
            v = part.split("=", 1)[1]
            return [] if v == "none" else v.split(",")
    return []


def make_evaluator(name, owns_defect_terms):
    """Build a deterministic evaluator that fails only on ITS OWN defect terms.

    Deliberately narrow: an evaluator that sees a defect belonging to another
    capability must NOT report it. That is what keeps capabilities separable and
    lets failure co-occurrence mean something.
    """
    def fn(payload, item, capability):
        present = _defects_in(payload)
        mine = [d for d in present if d in owns_defect_terms]
        if mine:
            return {"verdict": "fail",
                    "defects": [{"term": d, "observed_by": "instrument"} for d in mine],
                    "latency_s": 0.01}
        return {"verdict": "pass", "defects": [], "latency_s": 0.01}
    fn.__name__ = f"eval_{name}"
    return fn


def not_applicable_evaluator(payload, item, capability):
    """Correctly reports that it cannot judge this asset - with a REASON."""
    return {"verdict": "absent", "absence_reason": "not_applicable"}


def badly_behaved_evaluator(payload, item, capability):
    """NEGATIVE CONTROL: returns 'absent' with no reason.

    The harness must reject this. Without the reason, 'could not measure' is
    indistinguishable from 'measured and it was fine'.
    """
    return {"verdict": "absent"}


def bogus_verdict_evaluator(payload, item, capability):
    """NEGATIVE CONTROL: returns a verdict outside the permitted vocabulary."""
    return {"verdict": "probably_fine"}
