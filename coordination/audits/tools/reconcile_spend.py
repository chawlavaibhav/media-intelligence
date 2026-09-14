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

CONTROLLER RULING C-2 (14 September 2026) - which number governs a cap
    "Future dispatch caps are enforced against conservative ledger consumption at dispatch time. Vendor-
    billed cost is a separate reconciliation field used for actual CpAO. Do not wait for bills before
    enforcing a cap." The ledger (column 1) governs every cap, at dispatch. Vendor billing (column 4) is
    a RECONCILIATION field: read once from the statements and written beside the ledger figure, so the
    real cost per accepted outcome can be computed. Lack of statements blocks nothing: with no statements
    file the column prints "not reconciled (no statement filed)" and this tool exits 0.
    Record: coordination/decisions/CONTROLLER-AUDIT-CLOSEOUT-CAP-CROSSINGS-AND-CALL-LIMIT-2026-09-14.md

THE VENDOR STATEMENTS FILE (optional; nobody has filed one yet, so it does not exist)
    Path: coordination/audits/vendor-statements/VENDOR-BILLED-2026-09.yaml   (override: --vendor-statements PATH)
    Shape:
        statements:
          - provider: fal                          # fal | google_cloud | sarvam | elevenlabs (free text, named)
            statement_period: 2026-09-08/2026-09-10
            statement_ref: "fal usage export, Sep 2026"   # how to find the statement again. NO account numbers,
                                                          # invoice ids that embed them, or any credential.
            billed_native: "77.52"                 # what the statement says, in the vendor's own currency
            currency: USD                          # or INR / credits
            billed_usd_equiv: "77.52"              # the same amount in USD-equivalent (state the rate in statement_ref if converted)
            covers_run_ids: [vid-wan2, vid-wan2-smoke]   # the sealed runs this statement line covers; every id must exist
            reconciled_by: "<name>"
            reconciled_utc: "2026-09-14T10:00:00Z"
    Every field is required; unknown fields, unknown run ids, non-numeric amounts and a statement_ref that
    looks like an account number (8+ consecutive digits) are refused with exit code 2 - the tool never
    guesses a bill. A run covered by a statement prints `stmt:<provider>` in the vendor-billed column and the
    VENDOR STATEMENTS section compares the billed figure with the ledger figure over the covered runs.
    Nothing here is written back to any ledger; this tool stays read-only over eval/experiments/**.
"""
import argparse, json, os, re, sys
from collections import OrderedDict
from decimal import Decimal, InvalidOperation

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
RUNS = os.path.join(ROOT, "eval", "experiments", "EVAL-040", "runs")
DEFAULT_STATEMENTS = os.path.join(ROOT, "coordination", "audits", "vendor-statements", "VENDOR-BILLED-2026-09.yaml")
NOT_RECONCILED = "not reconciled (no statement filed)"
STATEMENT_FIELDS = ("provider", "statement_period", "statement_ref", "billed_native", "currency", "billed_usd_equiv",
                    "covers_run_ids", "reconciled_by", "reconciled_utc")


class StatementRefused(ValueError):
    """The statements file exists but cannot be trusted as written. Refusing beats guessing a bill."""


def load_statements(path, known_run_ids):
    """The filed vendor statements, or None when no file exists (C-2: absence blocks nothing)."""
    if not os.path.exists(path):
        return None
    try:
        import yaml
    except ImportError as exc:                   # a filed statement that cannot be read must not be silently ignored
        raise StatementRefused(f"{path} exists but PyYAML is not installed to read it") from exc
    with open(path, encoding="utf-8") as fh:
        doc = yaml.safe_load(fh)
    if not isinstance(doc, dict) or not isinstance(doc.get("statements"), list) or not doc["statements"]:
        raise StatementRefused(f"{path}: expected a mapping with a non-empty `statements` list")
    out = []
    for n, st in enumerate(doc["statements"], start=1):
        where = f"{path} statement #{n}"
        if not isinstance(st, dict):
            raise StatementRefused(f"{where} is not a mapping")
        missing = [f for f in STATEMENT_FIELDS if f not in st]
        unknown = [f for f in st if f not in STATEMENT_FIELDS]
        if missing or unknown:
            raise StatementRefused(f"{where}: missing {missing}, unknown {unknown}; the schema is in this tool's docstring")
        for f in ("provider", "statement_period", "statement_ref", "currency", "reconciled_by", "reconciled_utc"):
            if not isinstance(st[f], str) or not st[f].strip():
                raise StatementRefused(f"{where}: {f} must be a non-empty string")
        if re.search(r"\d{8,}", st["statement_ref"]):
            raise StatementRefused(f"{where}: statement_ref contains 8+ consecutive digits; that looks like an account or "
                                   f"invoice number, which must not be recorded here")
        amounts = {}
        for f in ("billed_native", "billed_usd_equiv"):
            try:
                amounts[f] = Decimal(str(st[f]))
            except (InvalidOperation, ValueError, TypeError) as exc:
                raise StatementRefused(f"{where}: {f} {st[f]!r} is not a decimal amount") from exc
            if amounts[f] < 0:
                raise StatementRefused(f"{where}: {f} is negative")
        runs = st["covers_run_ids"]
        if not isinstance(runs, list) or not runs or any(not isinstance(r, str) for r in runs):
            raise StatementRefused(f"{where}: covers_run_ids must be a non-empty list of run ids")
        bad = [r for r in runs if r not in known_run_ids]
        if bad:
            raise StatementRefused(f"{where}: covers_run_ids names runs with no sealed ledger: {bad}")
        out.append({**st, "billed_native": amounts["billed_native"], "billed_usd_equiv": amounts["billed_usd_equiv"], "covers_run_ids": list(runs)})
    return out


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


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=None, help="also write the table as JSON to this path")
    ap.add_argument("--vendor-statements", default=DEFAULT_STATEMENTS,
                    help="the filed vendor statements (C-2 reconciliation input); absent = every run 'not reconciled', exit 0")
    args = ap.parse_args(argv)

    rows = [r for r in (load_run(x) for x in sorted(os.listdir(RUNS))) if r]
    try:
        statements = load_statements(args.vendor_statements, {r["run_id"] for r in rows})
    except StatementRefused as exc:
        print(f"REFUSED: the vendor statements file cannot be used as written - {exc}")
        print("Nothing was reconciled and no ledger figure changed. Fix the file or remove it; the ledger table is unaffected.")
        return 2
    covered = {}                                                  # run_id -> provider named by the statement that covers it
    for st in statements or []:
        for rid in st["covers_run_ids"]:
            covered[rid] = st["provider"]
    for r in rows:
        r["vendor_billed"] = f"stmt:{covered[r['run_id']]}" if r["run_id"] in covered else NOT_RECONCILED

    print("C-2: the ledger governs the cap at dispatch time; vendor billing is a separate reconciliation field.")
    print(f"{'run':24} {'authorisation':38} {'cap':>7} {'calls':>5} {'consumed':>10} "
          f"{'delivered':>10} {'no-artifact':>11}  vendor billed")
    for r in rows:
        print(f"{r['run_id']:24} {r['authorisation']:38} {str(r['recorded_ceiling_usd']):>7} "
              f"{r['paid_calls']:>5} {r['ledger_consumed_usd_equiv']:>10} "
              f"{r['delivered_usd_equiv']:>10} {r['no_artifact_usd_equiv']:>11}  {r['vendor_billed']}")

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
    if statements is None:
        print(f"  vendor billed: {NOT_RECONCILED}. No file at {os.path.relpath(args.vendor_statements, ROOT)}.")
        print("  Read the fal, Google Cloud, Sarvam and ElevenLabs statements once and file them there (schema in this")
        print("  tool's docstring). Until then the project has an upper bound on its costs, not a cost (C-2); caps are")
        print("  unaffected - they are enforced against the ledger, never against a bill.")
    else:
        print("VENDOR STATEMENTS (C-2 reconciliation; billed minus ledger is negative where the ledger over-counted):")
        by_run = {r["run_id"]: r for r in rows}
        print(f"{'provider':14} {'period':24} {'ledger consumed':>15} {'billed usd-eq':>13} {'billed - ledger':>15}  covers")
        for st in statements:
            ledgered = sum(by_run[rid]["ledger_consumed_usd_equiv"] for rid in st["covers_run_ids"])
            print(f"{st['provider']:14} {st['statement_period']:24} {ledgered:>15} {st['billed_usd_equiv']:>13} "
                  f"{st['billed_usd_equiv'] - ledgered:>15}  {','.join(st['covers_run_ids'])}")
            print(f"{'':14} ref: {st['statement_ref']} ({st['billed_native']} {st['currency']}); reconciled by {st['reconciled_by']} at {st['reconciled_utc']}")
        uncovered = [r["run_id"] for r in rows if r["run_id"] not in covered]
        if uncovered:
            print(f"  {len(uncovered)} run(s) still {NOT_RECONCILED}: {','.join(uncovered)}")

    if args.json:
        out = json.loads(json.dumps(rows, default=str))
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(out, fh, indent=1, sort_keys=True)
        print(f"\nwrote {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
