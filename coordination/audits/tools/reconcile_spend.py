#!/usr/bin/env python3
"""reconcile_spend: one spend table per EVAL-040 run, from the sealed ledgers alone.

    python3 coordination/audits/tools/reconcile_spend.py [--json OUT.json]

Read-only. No network, no provider call, no cloud call. Standard library only.

WHY THIS EXISTS (audit 2026-09-10, findings F-2 / F-3 / F-09)
    The project has been quoting one number for "spend". There are four different numbers and they
    are not equal:

      1. LEDGER CONSUMED      - what the cap actually counted (a reservation settled at the estimate).
      2. DELIVERED            - the part of it that produced a sealed artifact.
      3. NO-ARTIFACT          - the part that did not; some of it was never billed by the vendor
                                (the six Wan 2 HTTP 422 draws are recorded in the Controller's own
                                spend record as "nothing generated, nothing charged").
      4. VENDOR BILLED        - unknown to this repository. It can only come from the fal / Google /
                                Sarvam / ElevenLabs statements. This script leaves that column empty
                                on purpose rather than guessing.

    A cap is enforced over column 1 (see eval/harness-v2/adapters/base.py, which settles the
    reservation once a request may have been sent, whatever comes back). Cash actually leaving the
    account is column 4. Reporting column 1 as money spent overstates it.
"""
import argparse, json, os, sys
from collections import OrderedDict
from decimal import Decimal

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
RUNS = os.path.join(ROOT, "eval", "experiments", "EVAL-040", "runs")


def load_run(run):
    d = os.path.join(RUNS, run)
    led = os.path.join(d, "ledger", run, "spend-ledger.jsonl")
    meta = os.path.join(d, "ledger", run, "run.json")
    if not os.path.exists(led) or not os.path.exists(meta):
        return None
    rec = json.load(open(meta, encoding="utf-8"))
    arts = os.path.join(d, "artifacts")
    row = {
        "run_id": run,
        "authorisation": os.path.basename(rec.get("authorisation_path", "")),
        "authorisation_sha256": rec.get("authorisation_sha256"),
        "recorded_ceiling_usd": rec.get("total_ceiling_usd"),
        "mode": rec.get("mode"),
        "retries_authorised": rec.get("retries_authorised"),
        "roster_sha256_8": (rec.get("price_basis_roster_sha256") or "")[:8],
        "item_basis_commit": rec.get("item_basis_commit"),
        "paid_calls": 0,
        "reservations": 0,
        "releases": 0,
        "ledger_consumed_usd_equiv": Decimal(0),
        "delivered_usd_equiv": Decimal(0),
        "no_artifact_usd_equiv": Decimal(0),
        "no_artifact_trials": [],
        "by_pool_usd_equiv": OrderedDict(),
        "by_pool_native": OrderedDict(),
        "first_at": None,
        "last_at": None,
    }
    for line in open(led, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        e = json.loads(line)
        t = e.get("type")
        if t == "reservation":
            row["reservations"] += 1
        elif t == "release":
            row["releases"] += 1
        elif t == "spend":
            amt = Decimal(e.get("amount_usd_equiv", "0"))
            nat = Decimal(e.get("amount_native", "0"))
            pool = e.get("billing_pool", "?")
            row["paid_calls"] += 1
            row["ledger_consumed_usd_equiv"] += amt
            row["by_pool_usd_equiv"][pool] = row["by_pool_usd_equiv"].get(pool, Decimal(0)) + amt
            row["by_pool_native"][pool] = row["by_pool_native"].get(pool, Decimal(0)) + nat
            trial = e.get("trial_id") or e.get("attempt_id")
            sealed = any(
                os.path.exists(os.path.join(arts, f"{trial}{suffix}.record.json"))
                for suffix in ("", ".composite", ".composite-v2")
            )
            if sealed:
                row["delivered_usd_equiv"] += amt
            else:
                row["no_artifact_usd_equiv"] += amt
                row["no_artifact_trials"].append({"trial_id": trial, "usd_equiv": str(amt)})
            at = e.get("at")
            if at:
                row["first_at"] = min(row["first_at"] or at, at)
                row["last_at"] = max(row["last_at"] or at, at)
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=None, help="also write the table as JSON to this path")
    args = ap.parse_args()

    rows = [r for r in (load_run(x) for x in sorted(os.listdir(RUNS))) if r]

    print(f"{'run':24} {'authorisation':38} {'cap':>7} {'calls':>5} {'consumed':>10} "
          f"{'delivered':>10} {'no-artifact':>11} {'vendor billed':>13}")
    for r in rows:
        print(f"{r['run_id']:24} {r['authorisation']:38} {str(r['recorded_ceiling_usd']):>7} "
              f"{r['paid_calls']:>5} {r['ledger_consumed_usd_equiv']:>10} "
              f"{r['delivered_usd_equiv']:>10} {r['no_artifact_usd_equiv']:>11} {'unknown':>13}")

    # per authorisation (this is the level a signed cap is written at)
    print()
    print("PER AUTHORISATION FILE - the level the Controller signs a cap at:")
    per = OrderedDict()
    for r in rows:
        k = r["authorisation"]
        p = per.setdefault(k, {"runs": [], "consumed": Decimal(0), "delivered": Decimal(0),
                               "no_artifact": Decimal(0), "calls": 0, "caps": set()})
        p["runs"].append(r["run_id"])
        p["consumed"] += r["ledger_consumed_usd_equiv"]
        p["delivered"] += r["delivered_usd_equiv"]
        p["no_artifact"] += r["no_artifact_usd_equiv"]
        p["calls"] += r["paid_calls"]
        p["caps"].add(str(r["recorded_ceiling_usd"]))
    print(f"{'authorisation':38} {'caps seen':>16} {'consumed':>10} {'delivered':>10} {'calls':>6}  runs")
    for k, p in per.items():
        caps = "/".join(sorted(p["caps"]))
        highest = max(Decimal(c) for c in p["caps"])
        flag = "  <<< CONSUMED ABOVE HIGHEST CAP" if p["consumed"] > highest else ""
        print(f"{k:38} {caps:>16} {p['consumed']:>10} {p['delivered']:>10} {p['calls']:>6}  "
              f"{','.join(p['runs'])}{flag}")

    # pools
    print()
    pools = OrderedDict()
    for r in rows:
        for pool, amt in r["by_pool_usd_equiv"].items():
            pools.setdefault(pool, [Decimal(0), Decimal(0)])
            pools[pool][0] += amt
            pools[pool][1] += r["by_pool_native"][pool]
    print("TOTALS BY BILLING POOL (usd-equivalent, native):")
    for pool, (u, n) in pools.items():
        print(f"  {pool:20} {u:>12} {n:>12}")
    tot = sum(r["ledger_consumed_usd_equiv"] for r in rows)
    deliv = sum(r["delivered_usd_equiv"] for r in rows)
    noart = sum(r["no_artifact_usd_equiv"] for r in rows)
    print()
    print(f"  ledger consumed across all runs : USD {tot}")
    print(f"    of which produced an artifact : USD {deliv}")
    print(f"    of which produced nothing     : USD {noart}   <- upper bound on money never billed")
    print(f"  vision-judge run (own cap, no run ledger): USD 3.156153 "
          f"(eval/experiments/EVAL-040/QUALIFICATION-REPORT-2026-09-09.yaml)")
    print(f"  grand total counted against caps: USD {tot + Decimal('3.156153')}")
    print()
    print("  vendor billed: NOT IN THIS REPOSITORY. Read it off the fal, Google Cloud, Sarvam and")
    print("  ElevenLabs statements and record it beside these numbers once.")

    if args.json:
        out = json.loads(json.dumps(rows, default=str))
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(out, fh, indent=1, sort_keys=True)
        print(f"\nwrote {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
