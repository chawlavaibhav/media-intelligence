#!/usr/bin/env python3
"""EVAL-038 reasoning-lane runner — weak model + compiled packs, unconditional injection.

Authority: DN-07 (canon/candidates/canon-014/REP-07-DECISION-NOTES.md):
USD 10.00 hard cap across ALL EVAL-038 paid calls (reasoning + media), 0 retries,
execution-time route/price verification before every paid call.

Spend discipline (EMP-001 lineage, simplified for this tranche):
- append-only JSONL ledger shared by every EVAL-038 paid call, committed as bytes;
- worst-case reservation BEFORE each dispatch (estimated input + max_tokens output at
  the pinned price); dispatch refused if committed + reservation would exceed the cap;
- settlement at provider-reported usage; a failure after send settles conservatively
  at the reservation (AMBIGUOUS counts against the cap, never released);
- 0 retries of any class — a failed trial is a recorded result.

Reuses the committed EVAL-037 provider adapters (eval/experiments/EVAL-037/tools/
providers.py) with no tools exposed: injection is unconditional, retrieval does not
exist here.
"""
import argparse
import datetime
import hashlib
import json
import os
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[4]
E37_TOOLS = ROOT / "eval/experiments/EVAL-037/tools"
E38 = ROOT / "eval/experiments/EVAL-038"
sys.path.insert(0, str(E37_TOOLS))

import providers  # noqa: E402  (EVAL-037 committed adapters)

# DN-07: 0 retries of any kind. The Anthropic SDK's client-level default is 2 HTTP
# retries; force 0 without editing the frozen EVAL-037 adapter bytes.
import anthropic as _anthropic_mod  # noqa: E402
_ORIG_ANTHROPIC = _anthropic_mod.Anthropic
_anthropic_mod.Anthropic = lambda **kw: _ORIG_ANTHROPIC(max_retries=0, **kw)

HARD_CAP_USD = 10.00
LEDGER = E38 / "runs/spend-ledger.jsonl"

LANES = {
    "haiku-packs": {"model_id": "claude-haiku-4-5-20251001", "adapter": "anthropic",
                    "model_key": "haiku", "price_key": "claude-haiku-4-5-20251001"},
    "gemma-packs": {"model_id": "gemma-4-31b-it", "adapter": "gemini",
                    "model_key": "gemma", "price_key": "gemma-4-31b-it"},
}

BRIEFS = ["B01", "B02", "B03", "B04", "B05", "B06"]


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha256(b):
    if isinstance(b, str):
        b = b.encode()
    return hashlib.sha256(b).hexdigest()


def load_prices(lane):
    snap = yaml.safe_load((E38 / "common/price-snapshot-038.yaml").read_text())
    p = snap["models"][lane["price_key"]]
    if p["input"] is None or p["output"] is None:
        sys.exit(f"STOP — PRICE_NOT_ESTABLISHED for {lane['price_key']}: the snapshot "
                 "holds null; pin the official price first (DN-07 requires price "
                 "verification before every paid call).")
    return float(p["input"]), float(p["output"])


def ledger_totals():
    committed = 0.0
    if LEDGER.exists():
        for line in LEDGER.read_text().splitlines():
            rec = json.loads(line)
            if rec["entry"] in ("settle", "settle_ambiguous"):
                committed += rec["usd"]
    return committed


def ledger_append(rec):
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a") as f:
        f.write(json.dumps(rec, sort_keys=True) + "\n")


def verify_route(lane):
    """Execution-time route verification: the exact model id must exist upstream."""
    if lane["adapter"] == "anthropic":
        import anthropic
        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        m = client.models.retrieve(lane["model_id"])
        return {"verified_model_id": m.id, "display_name": m.display_name,
                "verified_at": now()}
    else:
        from google import genai
        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        m = client.models.get(model=lane["model_id"])
        return {"verified_model_id": getattr(m, "name", lane["model_id"]),
                "verified_at": now()}


def run_trial(lane, lane_id, brief_id, rep, price_in, price_out, outdir, manifest):
    trial_id = f"E038-{lane_id}-{brief_id}-R{rep}"
    system = (E38 / f"payloads/{brief_id}.system.txt").read_text()
    user = (E38 / f"payloads/{brief_id}.user.txt").read_text()
    mrec = manifest["briefs"][brief_id]
    assert sha256(system) == mrec["system_sha256"], f"payload drift: {brief_id} system"
    assert sha256(user) == mrec["user_sha256"], f"payload drift: {brief_id} user"

    if lane["adapter"] == "anthropic":
        adapter = providers.AnthropicMessagesAdapter(
            lane["model_id"], tool_schemas=None, model_key=lane["model_key"])
    else:
        adapter = providers.GeminiAdapter(lane["model_id"], tool_schemas=None)
    request = adapter.build_request(system, user)

    max_out = providers.MAX_TOKENS[lane["model_key"]]
    est_in = mrec["input_tokens_estimate"]
    reservation = (est_in / 1e6) * price_in + (max_out / 1e6) * price_out
    committed = ledger_totals()
    if committed + reservation > HARD_CAP_USD:
        ledger_append({"entry": "refuse", "trial_id": trial_id, "at": now(),
                       "reason": f"cap: committed {committed:.6f} + reservation "
                                 f"{reservation:.6f} > {HARD_CAP_USD}"})
        return "REFUSED_CAP", 0.0
    ledger_append({"entry": "reserve", "trial_id": trial_id, "usd": round(reservation, 6),
                   "at": now(), "committed_before": round(committed, 6)})

    raw_dir = outdir / "raw"
    pkg_dir = outdir / "packages"
    raw_dir.mkdir(parents=True, exist_ok=True)
    pkg_dir.mkdir(parents=True, exist_ok=True)
    (raw_dir / f"{trial_id}.request.json").write_text(
        json.dumps(request, indent=1, sort_keys=True, default=str))

    status, text, turns, failure = "ok", None, [], None
    try:
        result = adapter.call(request, dispatch=None)
        text, turns = result["text"], result["turns"]
    except providers.ProviderError as e:
        status, failure = "failed", e.failure_class
        detail = getattr(e, "detail", None) or {}
        (raw_dir / f"{trial_id}.failure.json").write_text(json.dumps(
            {"failure_class": e.failure_class, "message": str(e)[:2000],
             "turns": detail.get("turns", []), "at": now()},
            indent=1, sort_keys=True, default=str))

    if status == "ok":
        usage = {}
        for f in ("input_tokens", "cached_input_tokens", "output_tokens",
                  "reasoning_tokens"):
            vals = [t[f] for t in turns if t.get(f) is not None]
            usage[f] = sum(vals) if vals else None
            usage[f + "_turns_reporting"] = len(vals)
        usage["provider_turns"] = len(turns)
        (raw_dir / f"{trial_id}.response.json").write_text(
            json.dumps({"usage": usage, "turns": turns}, indent=1,
                       sort_keys=True, default=str))
        (pkg_dir / f"{trial_id}.txt").write_text(text or "")
        in_tok = usage.get("input_tokens") or 0
        out_tok = usage.get("output_tokens") or 0
        cost = (in_tok / 1e6) * price_in + (out_tok / 1e6) * price_out
        ledger_append({"entry": "settle", "trial_id": trial_id, "usd": round(cost, 6),
                       "at": now(), "input_tokens": in_tok, "output_tokens": out_tok,
                       "payload_system_sha256": mrec["system_sha256"],
                       "payload_user_sha256": mrec["user_sha256"],
                       "package_sha256": sha256(text or "")})
        return status, cost
    else:
        # anything after the send began is AMBIGUOUS: settle at the reservation.
        ledger_append({"entry": "settle_ambiguous", "trial_id": trial_id,
                       "usd": round(reservation, 6), "at": now(),
                       "failure_class": failure})
        return status, reservation


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True, choices=sorted(LANES))
    ap.add_argument("--reps", type=int, default=2)
    args = ap.parse_args()
    lane = LANES[args.lane]

    price_in, price_out = load_prices(lane)
    route = verify_route(lane)
    print(f"route verified: {route}")
    print(f"price pinned: in {price_in}/MTok out {price_out}/MTok")

    manifest = yaml.safe_load((E38 / "payloads/PAYLOAD-MANIFEST.yaml").read_text())
    outdir = E38 / f"runs/{args.lane}"
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "route-verification.json").write_text(
        json.dumps({**route, "price_input_per_mtok": price_in,
                    "price_output_per_mtok": price_out}, indent=1, sort_keys=True))

    results = {}
    for brief_id in BRIEFS:
        for rep in range(1, args.reps + 1):
            trial_id = f"E038-{args.lane}-{brief_id}-R{rep}"
            if (outdir / f"packages/{trial_id}.txt").exists():
                print(f"{trial_id}: already done, skipping (no regeneration)")
                continue
            status, cost = run_trial(lane, args.lane, brief_id, rep,
                                     price_in, price_out, outdir, manifest)
            results[trial_id] = (status, round(cost, 6))
            print(f"{trial_id}: {status} usd={cost:.6f} "
                  f"total_committed={ledger_totals():.6f}")
            if status == "REFUSED_CAP":
                print("HARD STOP: cap reached")
                sys.exit(2)
    total = ledger_totals()
    print(f"lane {args.lane} complete; EVAL-038 committed spend USD {total:.6f} "
          f"of {HARD_CAP_USD:.2f}")


if __name__ == "__main__":
    main()
