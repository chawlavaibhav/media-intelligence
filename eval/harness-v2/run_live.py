#!/usr/bin/env python3
"""EVAL-040 live runner: plan, smoke-test, execute (resumable) and status for one authorised battery run.

    python3 eval/harness-v2/run_live.py plan    --run-id <id> --cases IMG-CORE-01,... [--routes k1,k2] [--tranche 1a] --out <dir>
    python3 eval/harness-v2/run_live.py smoke   --run-id <id> --case <case_id> --route <route_key> --out <dir>   (ONE dispatch, repeat 1)
    python3 eval/harness-v2/run_live.py execute --run-id <id> --out <dir> [--max-dispatches N]                 (runs the committed plan)
    python3 eval/harness-v2/run_live.py status  --run-id <id> --out <dir>

WHAT IT DOES, IN PLAIN ENGLISH

    `plan` writes down, before any money moves, exactly which calls will be made and in which order: the rows
    of the dry-run manifest (the same request builder a live call uses) restricted to the requested cases,
    routes and tranche, minus every row that could not dispatch (conditional, no adapter, unverified shape,
    unpinned price, needs_controller_enablement). The order is repeat-major: every case's repeat 1 (cases in the
    requested order, routes in catalogue order) is dispatched before any repeat 2, so the two unseeded draws of a
    (case, route) are separated by the whole lane, never by seconds.
    `PLAN.yaml` + `PLAN.sha256` are the commitment; `execute` refuses if the plan is absent or its bytes changed.

    `execute` opens the Controller's authorisation (refuses if absent or not permitted), opens or creates the
    battery ledger under `<out>/ledger/<run-id>/`, builds each adapter with the REAL transport and
    `allow_default_token_source=True` (this module is the only place that flag is set), and dispatches the
    plan one trial at a time with 0 retries. Every outcome is persisted by the adapter through the sealed store
    and the ledger. A cap breach (`BudgetExceeded`, raised by the ledger BEFORE anything is sent) stops the run
    cleanly; a refusal our own code raises before any send is recorded under `<out>/trials/` and the run
    continues; any other exception on one trial is recorded the same way and the run continues. A trial that
    already has an attempt, a pre-dispatch refusal or a harness error record is skipped on resume (its request
    is sealed; a re-run is a new trial id under a new run id, never a retry).

    After every artifact: format_probe, the compiled-doctrine gate's post check (observation only) and, after
    repeat 2, repeat_consistency against repeat 1 - written under `<out>/instruments/<trial_id>.json`. The
    instruments never block the run: their failures are recorded on that file.

    Everything is written under `<out>`. No key value is ever written: keys are read by NAME at dispatch
    inside the adapters and scrubbed from every record (adapters/base.py).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import traceback
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import yaml

import hv2_paths
import casebook as CB
import dry_run as DR
import ledger as L
import pricing as PR
import store as S
import surfaces
from adapters import adapter_for as _adapter_for
from adapters import base as B
from budget_guard import BudgetExceeded, NotAuthorised
from providers import DispatchRefused, PreDispatchRefusal

adapter_for = _adapter_for            # module attribute so a test can wrap it; the runner takes an override too

PLAN_FILE = "PLAN.yaml"
PLAN_SHA_FILE = "PLAN.sha256"
STATE_FILE = "RUN-STATE.json"
LOG_FILE = "RUN-LOG.jsonl"
TRIALS_DIR = "trials"
INSTRUMENTS_DIR = "instruments"
ARTIFACTS_DIR = "artifacts"
LEDGER_DIR = "ledger"
MODALITY_BY_MEDIA_KIND = {"image": "static_image", "video": "video", "audio": "audio"}
FREEZE_FILES = ("TEST-CASES.yaml", "COST-TABLE.yaml")
PLAN_STATEMENT = ("This plan is the ordered list of the calls run_live.py will make under the named authorisation and nothing else. "
                  "Every trial's body sha256 is the dry-run body of the same builder a live dispatch sends; execute refuses a trial whose "
                  "rendered body differs. The plan authorises nothing by itself: the ledger re-reads the authorisation file at every open.")


class PlanRefused(RuntimeError):
    """The plan cannot be drawn or executed as asked. Nothing was sent."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _require_permitted(auth: L.BatteryAuthorisation, what: str) -> None:
    if auth.refusals:
        raise NotAuthorised(f"{what}: EVAL-040 paid execution is not authorised ({auth.source_path}):\n  - " + "\n  - ".join(auth.refusals))


# ======================================================================================= plan
def _filtered_book(book: CB.CaseBook, cases: list[str]) -> CB.CaseBook:
    picked = []
    for c in cases:
        try:
            picked.append(book.case(c))
        except KeyError:
            raise PlanRefused(f"case {c!r} is not in TEST-CASES.yaml at {book.source.get('rev') or book.source.get('kind')}") from None
    return CB.CaseBook({**book.data, "cases": picked}, book._bp, book.source, cost_table={"route_catalogue": book.catalogue})


def _freeze_matches(git_rev: str, item_basis_commit: str) -> bool:
    for name in FREEZE_FILES:
        rel = f"{CB.FREEZE_REL}/{name}"
        try:
            if CB.git_show(git_rev, rel) != CB.git_show(item_basis_commit, rel):
                return False
        except Exception as exc:  # noqa: BLE001
            raise PlanRefused(f"cannot compare {rel} at {git_rev} with the item basis commit {item_basis_commit}: {exc}") from exc
    return True


def build_plan(out: Path | str, run_id: str, cases: list[str], routes: list[str] | None, tranche: str | None,
               auth_path: Path | str, git_rev: str = "HEAD", mode: str = "lane", repeats: tuple | None = None) -> dict:
    """Write `<out>/PLAN.yaml` + `PLAN.sha256` before any dispatch. Refuses an empty plan and never overwrites."""
    out = Path(out)
    if (out / PLAN_FILE).exists():
        raise PlanRefused(f"{out / PLAN_FILE} already exists; a plan is written once. Use a new run id for a new plan.")
    if not cases:
        raise PlanRefused("no cases requested")
    auth = L.load_battery_authorisation(auth_path)
    _require_permitted(auth, "build_plan")
    registry = surfaces.REGISTRY
    for r in routes or []:
        if r not in registry.keys():
            raise PlanRefused(f"route {r!r} is not in the SurfaceRegistry")

    book = CB.CaseBook.from_git(git_rev)
    commit = book.source["commit"]
    freeze_ok = _freeze_matches(git_rev, auth.item_basis_commit)
    if not freeze_ok:
        raise PlanRefused(f"the freeze package at {git_rev} ({commit[:12]}) differs from the authorisation's item basis commit "
                          f"{auth.item_basis_commit}; a change means a rebuild and a new record")
    fbook = _filtered_book(book, cases)
    pricing = PR.Pricing()
    cost_table = PR.CostTable()
    manifest = DR.build_manifest(fbook, registry, pricing, cost_table, git_commit=commit)

    trials, excluded = [], []
    by_case: dict[str, list] = {c: [] for c in cases}
    for row in manifest["rows"]:
        reason = None
        if routes and row["route_key"] not in routes:
            continue                                     # not requested: neither planned nor listed
        if not row["would_dispatch"]:
            reason = row["refusal_reason"] or "would_dispatch: false"
        elif tranche and row["tranche"] != tranche:
            reason = f"tranche {row['tranche']} not requested ({tranche})"
        elif repeats and row["repeat_index"] not in repeats:
            reason = f"repeat {row['repeat_index']} not requested ({list(repeats)})"
        if reason:
            excluded.append({"case_id": row["case_id"], "route_key": row["route_key"], "arm": row["arm"], "repeat_index": row["repeat_index"],
                             "tranche": row["tranche"], "reason": reason})
            continue
        by_case[row["case_id"]].append(row)
    if routes:
        planned_routes = {r["route_key"] for rows in by_case.values() for r in rows}
        missing = [r for r in routes if r not in planned_routes]
        if missing:
            raise PlanRefused(f"requested routes {missing} have no dispatchable row for cases {cases} in tranche {tranche!r}: "
                              + "; ".join(f"{e['route_key']}: {e['reason']}" for e in excluded if e["route_key"] in missing) or "not listed on these cases")
    seq = 0
    # Repeat-major: EVERY case's repeat 1 (cases in the requested order, routes in catalogue order) is
    # dispatched before ANY repeat 2. Repeats are unseeded inherent-variance draws (SEED-POLICY); sending
    # the identical body to a provider seconds apart invites request-level caching or shared sampler state,
    # which would understate variance. Separating the two blocks by the whole lane is the cheapest guard.
    all_reps = sorted({r["repeat_index"] for rows in by_case.values() for r in rows})
    for rep in all_reps:
        for case_id in cases:
            rows = by_case[case_id]
            for r in rows:
                if r["repeat_index"] != rep:
                    continue
                seq += 1
                entry = registry.get(r["route_key"])
                trials.append({
                    "seq": seq, "trial_id": B.make_trial_id(r), "case_id": r["case_id"], "item_id": r["item_id"],
                    "route_key": r["route_key"], "arm": r["arm"], "repeat_index": r["repeat_index"], "tranche": r["tranche"],
                    "surface": entry.surface, "adapter": entry.adapter, "surface_model_id": entry.surface_model_id, "endpoint": r["url"],
                    "billing_pool": entry.billing_pool, "currency": r["currency"],
                    "estimated_amount_native": r["computed_amount"], "estimated_usd_equiv": r["amount_usd_equiv"],
                    "unit_price": r["unit_price"], "quantity": r["quantity"], "quantity_unit": r["quantity_unit"], "price_pin_ref": r["price_pin_ref"],
                    "body_sha256": r["body_sha256"], "api_calls_per_trial": r["api_calls_per_trial"],
                    "key_name": entry.key_name, "credential_file_name": entry.credential_file_name, "seed_policy": r["seed_policy"],
                })
    if not trials:
        raise PlanRefused(f"the plan is empty for cases {cases}, routes {routes}, tranche {tranche!r}: "
                          + "; ".join(f"{e['case_id']}/{e['route_key']}: {e['reason']}" for e in excluded[:12]))
    by_pool: dict[str, dict] = {}
    for t in trials:
        slot = by_pool.setdefault(t["billing_pool"], {"calls": 0, "currency": t["currency"], "native": Decimal("0"), "usd_equiv": Decimal("0")})
        slot["calls"] += 1
        slot["native"] += Decimal(t["estimated_amount_native"])
        slot["usd_equiv"] += Decimal(t["estimated_usd_equiv"])
    header = {
        "plan": "EVAL-040-RUN-PLAN", "run_id": run_id, "mode": mode, "generated_utc": _now(), "statement": PLAN_STATEMENT,
        "git_rev": git_rev, "commit": commit, "item_basis_commit": auth.item_basis_commit, "freeze_matches_item_basis": freeze_ok,
        "tranche_id": auth.tranche_id, "authorisation_path": auth.source_path, "authorisation_sha256": auth.sha256,
        "roster_sha256": pricing.roster.sha256, "test_cases_sha256": book.source["test_cases_sha256"], "cost_table_sha256": book.source["cost_table_sha256"],
        "cases": list(cases), "routes": list(routes) if routes else None, "tranche": tranche, "repeats": list(repeats) if repeats else None,
        "ordering": "repeat-major; every case's repeat 1 (cases in requested order, routes in catalogue order) before any repeat 2",
        "counts": {"trials": len(trials), "excluded": len(excluded)},
        "estimated_by_pool": {k: {"calls": v["calls"], "currency": v["currency"], "native": str(v["native"]), "usd_equiv": str(v["usd_equiv"])} for k, v in by_pool.items()},
        "estimated_total_usd_equiv": str(sum((v["usd_equiv"] for v in by_pool.values()), Decimal("0"))),
        "retries_authorised": L.RETRIES_AUTHORISED,
    }
    plan = {"header": header, "trials": trials, "excluded": excluded}
    out.mkdir(parents=True, exist_ok=True)
    text = ("# EVAL-040 RUN PLAN - the ordered list of calls run_live.py will make; written BEFORE any dispatch; execute refuses if these bytes change.\n"
            + yaml.safe_dump(plan, sort_keys=False, allow_unicode=True, width=160))
    (out / PLAN_FILE).write_text(text, encoding="utf-8")
    (out / PLAN_SHA_FILE).write_text(f"{_sha256_file(out / PLAN_FILE)}  {PLAN_FILE}\n", encoding="utf-8")
    return plan


def load_plan(out: Path | str, run_id: str) -> dict:
    """The committed plan, only if its bytes still hash to PLAN.sha256 and it names this run id."""
    out = Path(out)
    p, s = out / PLAN_FILE, out / PLAN_SHA_FILE
    if not p.exists() or not s.exists():
        raise PlanRefused(f"no committed plan at {p} (+ {PLAN_SHA_FILE}); run `plan` first. Nothing was sent.")
    recorded = s.read_text(encoding="utf-8").split()[0]
    actual = _sha256_file(p)
    if recorded != actual:
        raise PlanRefused(f"{p} hashes to {actual[:12]}... but {PLAN_SHA_FILE} records {recorded[:12]}...; the plan changed after it was committed. Nothing was sent.")
    plan = yaml.safe_load(p.read_text(encoding="utf-8"))
    if not isinstance(plan, dict) or plan.get("header", {}).get("run_id") != run_id:
        raise PlanRefused(f"{p} is not the plan of run {run_id!r}")
    state = out / STATE_FILE
    if state.exists():
        rec = json.loads(state.read_text(encoding="utf-8"))
        if rec.get("plan_sha256") and rec["plan_sha256"] != actual:
            raise PlanRefused(f"{state} was written against plan {rec['plan_sha256'][:12]}..., not {actual[:12]}...; a run never changes its plan")
    plan["_sha256"] = actual
    return plan


# ==================================================================================== runner
def live_transport_factory(entry, trial):
    """The REAL urllib transports (transports.py is the only module that opens a socket). Used by main() only."""
    import transports as T
    fam = {"fal": T.FalQueueTransport, "vertex": T.VertexTransport, "sarvam_direct": T.SarvamTransport}.get(entry.surface)
    if fam is None:
        raise DispatchRefused(f"{entry.route_key}: no live transport for surface {entry.surface}; nothing was sent")
    return fam()


class LiveRunner:
    """Executes a committed plan against the ledger, the sealed store and injected transports."""

    def __init__(self, out: Path | str, run_id: str, auth_path: Path | str, transport_factory, adapter_kwargs: dict | None = None,
                 gate_script: Path | str | None = None, adapter_for=None, book: CB.CaseBook | None = None):
        self.out = Path(out)
        self.run_id = run_id
        self.auth_path = Path(auth_path)
        self.transport_factory = transport_factory
        self.adapter_kwargs = dict(adapter_kwargs or {})
        self.gate_script = gate_script
        self.adapter_for = adapter_for or globals()["adapter_for"]
        self._book = book
        self.registry = surfaces.REGISTRY
        self.store = S.SealedStore(self.out / ARTIFACTS_DIR)
        self.plan: dict | None = None
        self.budget: L.BatteryBudget | None = None
        self.pricing: PR.Pricing | None = None

    # -- paths / records ------------------------------------------------------------------------
    def _trial_record_path(self, trial_id: str, kind: str) -> Path:
        return self.out / TRIALS_DIR / f"{S.safe_id(trial_id)}.{kind}.json"

    def is_terminal(self, trial_id: str) -> bool:
        return (self.store.attempt_path(trial_id).exists() or self._trial_record_path(trial_id, "pre_dispatch_refusal").exists()
                or self._trial_record_path(trial_id, "harness_error").exists())

    def _log(self, event: str, **fields) -> None:
        self.out.mkdir(parents=True, exist_ok=True)
        with (self.out / LOG_FILE).open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({"at": _now(), "event": event, "run_id": self.run_id, **fields}, sort_keys=True, ensure_ascii=False, default=str) + "\n")

    def _write_state(self, **fields) -> None:
        path = self.out / STATE_FILE
        rec = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"run_id": self.run_id, "started_at": _now()}
        rec.update(fields, updated_at=_now())
        path.write_text(json.dumps(rec, indent=1, sort_keys=True, default=str) + "\n", encoding="utf-8")

    def _write_trial_record(self, trial: dict, kind: str, **fields) -> Path:
        path = self._trial_record_path(trial["trial_id"], kind)
        path.parent.mkdir(parents=True, exist_ok=True)
        n = 1
        while path.exists():
            n += 1
            path = self._trial_record_path(trial["trial_id"], f"{kind}.{n}")
        rec = {"trial_id": trial["trial_id"], "kind": kind, "at": _now(), "case_id": trial["case_id"], "route_key": trial["route_key"],
               "repeat_index": trial["repeat_index"], "seq": trial["seq"], **fields}
        path.write_text(json.dumps(rec, indent=1, sort_keys=True, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
        return path

    @property
    def book(self) -> CB.CaseBook:
        if self._book is None:
            self._book = CB.CaseBook.from_git(self.plan["header"]["commit"])
        return self._book

    # -- opening ---------------------------------------------------------------------------------
    def open(self) -> L.BatteryAuthorisation:
        """Plan first (nothing to execute without it), then the authorisation, then the ledger. Sends nothing."""
        self.plan = load_plan(self.out, self.run_id)
        auth = L.load_battery_authorisation(self.auth_path)
        _require_permitted(auth, "execute")
        root = self.out / LEDGER_DIR
        if (root / self.run_id / "run.json").exists():
            run = L.BatteryRun.open(root, self.run_id, auth)
        else:
            run = L.BatteryRun.create(root, self.run_id, auth, mode="live")
        self.budget = L.BatteryBudget(run)
        self.pricing = PR.Pricing()
        return auth

    # -- one trial ---------------------------------------------------------------------------------
    def _dispatch(self, trial: dict) -> dict:
        row = self.book.row(trial["case_id"], trial["route_key"], trial["arm"], trial["repeat_index"])
        entry = self.registry.get(trial["route_key"])
        transport = self.transport_factory(entry, trial)
        adapter = self.adapter_for(entry, pricing=self.pricing, transport=transport, budget=self.budget, store=self.store,
                                   allow_default_token_source=True, **self.adapter_kwargs)
        request = adapter.build_request(row)                      # renders only; refuses bad params before any money moves
        if request.body_sha256 != trial["body_sha256"]:
            raise PreDispatchRefusal(f"{trial['trial_id']}: the rendered body sha256 {request.body_sha256[:12]}... differs from the plan's "
                                     f"{trial['body_sha256'][:12]}...; the plan is executed verbatim or not at all. Nothing was sent.")
        return adapter.dispatch(row, call_context={"trial_id": trial["trial_id"]})

    def _instruments(self, trial: dict, attempt: dict) -> None:
        """format_probe + gate post + (repeat 2) repeat_consistency. Observation only; never raises."""
        res = {"trial_id": trial["trial_id"], "run_id": self.run_id, "at": _now(), "format_probe": None, "gate_post": None,
               "repeat_consistency": None, "errors": []}
        try:
            art = attempt.get("artifact") if attempt.get("status") == "ok" else None
            if not art:
                res["errors"].append(f"no artifact to instrument (status {attempt.get('status')})")
            else:
                path = self.store.root / art["relative_path"]
                row = self.book.row(trial["case_id"], trial["route_key"], trial["arm"], trial["repeat_index"])
                try:
                    from instruments import format_probe as FP
                    res["format_probe"] = FP.evaluate(path, row)
                except Exception as exc:  # noqa: BLE001
                    res["errors"].append(f"format_probe: {type(exc).__name__}: {exc}")
                try:
                    from instruments import gate_wrapper as GW
                    inst_dir = self.out / INSTRUMENTS_DIR
                    inst_dir.mkdir(parents=True, exist_ok=True)
                    res["gate_post"] = GW.run_post(path, self.store.request_path(trial["trial_id"]), MODALITY_BY_MEDIA_KIND.get(art.get("media_kind"), "static_image"),
                                                   gate_script=self.gate_script, json_out=inst_dir / f"{S.safe_id(trial['trial_id'])}.gate.json")
                except Exception as exc:  # noqa: BLE001
                    res["errors"].append(f"gate_post: {type(exc).__name__}: {exc}")
                if trial["repeat_index"] >= 2:
                    try:
                        from instruments import repeat_consistency as RC
                        first = next((t for t in self.plan["trials"] if t["case_id"] == trial["case_id"] and t["route_key"] == trial["route_key"]
                                      and t["arm"] == trial["arm"] and t["repeat_index"] == 1), None)
                        a1 = json.loads(self.store.attempt_path(first["trial_id"]).read_text(encoding="utf-8")) if first and self.store.attempt_path(first["trial_id"]).exists() else None
                        if a1 and a1.get("status") == "ok" and a1.get("artifact"):
                            res["repeat_consistency"] = RC.evaluate(self.store.root / a1["artifact"]["relative_path"], path, attempt.get("seed_policy") or "unset")
                            res["repeat_consistency"]["other_repeat_trial_id"] = first["trial_id"]
                        else:
                            res["errors"].append("repeat_consistency: repeat 1 has no artifact to compare against")
                    except Exception as exc:  # noqa: BLE001
                        res["errors"].append(f"repeat_consistency: {type(exc).__name__}: {exc}")
        except Exception as exc:  # noqa: BLE001
            res["errors"].append(f"instruments: {type(exc).__name__}: {exc}")
        try:
            inst_dir = self.out / INSTRUMENTS_DIR
            inst_dir.mkdir(parents=True, exist_ok=True)
            p = inst_dir / f"{S.safe_id(trial['trial_id'])}.json"
            n = 1
            while p.exists():
                n += 1
                p = inst_dir / f"{S.safe_id(trial['trial_id'])}.{n}.json"
            p.write_text(json.dumps(res, indent=1, sort_keys=True, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
        except Exception as exc:  # noqa: BLE001
            self._log("instrument_write_failed", trial_id=trial["trial_id"], error=f"{type(exc).__name__}: {exc}")

    # -- the run ------------------------------------------------------------------------------------
    def execute(self, max_dispatches: int | None = None) -> dict:
        auth = self.open()
        trials = self.plan["trials"]
        self._write_state(status="running", plan_sha256=self.plan["_sha256"], authorisation_sha256=auth.sha256, mode=self.plan["header"]["mode"])
        self._log("run_started", n_trials=len(trials), max_dispatches=max_dispatches, authorisation_sha256=auth.sha256,
                  ceiling_usd_equiv=str(auth.max_consumed_usd_equivalent))
        summary = {"run_id": self.run_id, "status": "running", "dispatched": 0, "skipped": 0, "errors": [], "trial_order": [], "stop_reason": None}
        for trial in trials:
            tid = trial["trial_id"]
            if self.is_terminal(tid):
                summary["skipped"] += 1
                continue
            if max_dispatches is not None and summary["dispatched"] >= max_dispatches:
                summary["status"], summary["stop_reason"] = "paused_max_dispatches", f"max_dispatches {max_dispatches} reached"
                break
            self._log("dispatching", trial_id=tid, seq=trial["seq"], estimated_usd_equiv=trial["estimated_usd_equiv"], billing_pool=trial["billing_pool"])
            try:
                attempt = self._dispatch(trial)
            except (BudgetExceeded, NotAuthorised) as exc:
                reason = f"{type(exc).__name__}: {exc}"
                summary["status"], summary["stop_reason"] = ("stopped_cap_reached" if isinstance(exc, BudgetExceeded) else "stopped_not_authorised"), reason
                self._log("stopped", trial_id=tid, reason=reason)
                break
            except (PreDispatchRefusal, DispatchRefused) as exc:
                reason = f"{type(exc).__name__}: {exc}"
                self._write_trial_record(trial, "pre_dispatch_refusal", reason=reason, sent=False)
                summary["errors"].append({"trial_id": tid, "kind": "pre_dispatch_refusal", "note": reason[:300]})
                self._log("pre_dispatch_refusal", trial_id=tid, reason=reason)
                continue
            except Exception as exc:  # noqa: BLE001 - one trial's failure never ends the run
                reason = f"{type(exc).__name__}: {exc}"
                self._write_trial_record(trial, "harness_error", error=reason, traceback=traceback.format_exc()[-4000:])
                summary["errors"].append({"trial_id": tid, "kind": "harness_error", "note": reason[:300]})
                self._log("harness_error", trial_id=tid, error=reason)
                continue
            summary["dispatched"] += 1
            summary["trial_order"].append(tid)
            art = attempt.get("artifact") or {}
            self._log("dispatched", trial_id=tid, status=attempt.get("status"), error_class=attempt.get("error_class"),
                      billing_state=attempt.get("billing_state"), cost_ref=attempt.get("cost_ref"), artifact_sha256=art.get("sha256"),
                      artifact_bytes=art.get("bytes"), provider_request_id=attempt.get("provider_request_id"))
            if attempt.get("status") != "ok":
                summary["errors"].append({"trial_id": tid, "kind": "attempt", "status": attempt.get("status"), "error_class": attempt.get("error_class"),
                                          "note": (attempt.get("raw_status_note") or "")[:300]})
            self._instruments(trial, attempt)
        if summary["status"] == "running":
            summary["status"] = "completed" if all(self.is_terminal(t["trial_id"]) for t in trials) else "incomplete"
        remaining = sum(1 for t in trials if not self.is_terminal(t["trial_id"]))
        self._write_state(status=summary["status"], stop_reason=summary["stop_reason"], n_dispatched_last_session=summary["dispatched"],
                          n_remaining=remaining, n_errors=len(summary["errors"]))
        self._log("run_finished", status=summary["status"], n_dispatched=summary["dispatched"], n_skipped=summary["skipped"], n_remaining=remaining,
                  stop_reason=summary["stop_reason"])
        summary["remaining"] = remaining
        return summary


def smoke(out: Path | str, run_id: str, case_id: str, route_key: str, auth_path: Path | str, transport_factory, adapter_kwargs: dict | None = None,
          gate_script: Path | str | None = None, git_rev: str = "HEAD", adapter_for=None) -> dict:
    """ONE dispatch: a one-trial plan (repeat 1 only) executed with max_dispatches=1."""
    plan = build_plan(out, run_id, cases=[case_id], routes=[route_key], tranche=None, auth_path=auth_path, git_rev=git_rev, mode="smoke", repeats=(1,))
    if len(plan["trials"]) != 1:
        raise PlanRefused(f"a smoke plan must hold exactly one trial; got {len(plan['trials'])}")
    runner = LiveRunner(out, run_id, auth_path, transport_factory, adapter_kwargs, gate_script, adapter_for=adapter_for)
    return runner.execute(max_dispatches=1)


# ==================================================================================== status
def status(out: Path | str, run_id: str, auth_path: Path | str = L.AUTH_LOCAL_PATH) -> dict:
    out = Path(out)
    plan = load_plan(out, run_id)
    store = S.SealedStore(out / ARTIFACTS_DIR)
    done, remaining, errors = 0, 0, []
    for t in plan["trials"]:
        tid = t["trial_id"]
        ap = store.attempt_path(tid)
        pre = out / TRIALS_DIR / f"{S.safe_id(tid)}.pre_dispatch_refusal.json"
        herr = out / TRIALS_DIR / f"{S.safe_id(tid)}.harness_error.json"
        if ap.exists():
            done += 1
            a = json.loads(ap.read_text(encoding="utf-8"))
            if a.get("status") != "ok":
                errors.append({"trial_id": tid, "kind": "attempt", "status": a.get("status"), "error_class": a.get("error_class"),
                               "billing_state": a.get("billing_state"), "note": (a.get("raw_status_note") or "")[:200]})
        elif pre.exists():
            done += 1
            errors.append({"trial_id": tid, "kind": "pre_dispatch_refusal", "note": json.loads(pre.read_text(encoding="utf-8")).get("reason", "")[:200]})
        elif herr.exists():
            done += 1
            errors.append({"trial_id": tid, "kind": "harness_error", "note": json.loads(herr.read_text(encoding="utf-8")).get("error", "")[:200]})
        else:
            remaining += 1
    auth = L.load_battery_authorisation(auth_path)
    root = out / LEDGER_DIR
    by_pool: dict[str, dict] = {}
    headroom, headroom_basis, spent = None, None, Decimal("0")
    if (root / run_id / "run.json").exists():
        if auth.permitted:
            budget = L.BatteryBudget(L.BatteryRun.open(root, run_id, auth))
            for pool, v in budget.totals_by_pool().items():
                by_pool[pool] = {"currency": v["currency"], "native": str(v["native"].quantize(Decimal("0.000001"))), "usd_equiv": str(v["usd_equiv"].quantize(Decimal("0.000001")))}
            spent = budget.spent_usd()
            headroom, headroom_basis = budget.remaining_usd(), "authorisation file (re-validated)"
        else:
            rows = [json.loads(l) for l in (root / run_id / "spend-ledger.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
            settled = {r.get("reservation_id") for r in rows if r["type"] in ("spend", "release")}
            for r in rows:
                if r["type"] in ("spend", "correction") or (r["type"] == "reservation" and r.get("reservation_id") not in settled):
                    slot = by_pool.setdefault(r.get("billing_pool", "unknown"), {"currency": r.get("currency", "USD"), "native": Decimal("0"), "usd_equiv": Decimal("0")})
                    slot["native"] += Decimal(str(r.get("amount_native", r.get("amount_usd"))))
                    slot["usd_equiv"] += Decimal(str(r.get("amount_usd_equiv", r.get("amount_usd"))))
                    spent += Decimal(str(r.get("amount_usd_equiv", r.get("amount_usd"))))
            by_pool = {k: {"currency": v["currency"], "native": str(v["native"]), "usd_equiv": str(v["usd_equiv"])} for k, v in by_pool.items()}
            rec = json.loads((root / run_id / "run.json").read_text(encoding="utf-8"))
            headroom, headroom_basis = Decimal(str(rec.get("total_ceiling_usd", "0"))) - spent, "run.json recorded ceiling (authorisation NOT permitted now; display only)"
    state = json.loads((out / STATE_FILE).read_text(encoding="utf-8")) if (out / STATE_FILE).exists() else {}
    st = {"run_id": run_id, "mode": plan["header"]["mode"], "planned": len(plan["trials"]), "done": done, "remaining": remaining,
          "estimated_total_usd_equiv": plan["header"]["estimated_total_usd_equiv"], "settled_by_pool": by_pool, "spent_usd_equiv": str(spent),
          "remaining_headroom_usd_equiv": (str(headroom) if headroom is not None else None), "headroom_basis": headroom_basis,
          "authorisation_permitted": auth.permitted, "authorisation_refusals": list(auth.refusals), "state": state.get("status"), "stop_reason": state.get("stop_reason"),
          "errors": errors}
    return st


def print_status(st: dict) -> None:
    print(f"run {st['run_id']} ({st['mode']}): {st['done']} done / {st['remaining']} remaining of {st['planned']} planned; state {st['state']}"
          + (f" ({st['stop_reason']})" if st.get("stop_reason") else ""))
    for pool, v in sorted(st["settled_by_pool"].items()):
        print(f"  {pool:15s} {v['currency']} {v['native']}  (USD-equiv {v['usd_equiv']})")
    print(f"  spent USD-equiv {st['spent_usd_equiv']} of estimated {st['estimated_total_usd_equiv']}; headroom {st['remaining_headroom_usd_equiv']} [{st['headroom_basis']}]")
    if not st["authorisation_permitted"]:
        print("  authorisation NOT permitted: " + "; ".join(st["authorisation_refusals"]))
    for e in st["errors"]:
        print(f"  ! {e['trial_id']}: {e['kind']} {e.get('status') or ''} {e.get('error_class') or ''} {e.get('note') or ''}".rstrip())


# ==================================================================================== cli
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        p.add_argument("--run-id", required=True)
        p.add_argument("--out", required=True, help="the run directory, e.g. eval/experiments/EVAL-040/runs/<run-id>/")
        p.add_argument("--auth", default=str(L.AUTH_LOCAL_PATH), help="authorisation file (default: eval/harness-v2/authorization.local.yaml)")

    p = sub.add_parser("plan"); common(p)
    p.add_argument("--cases", required=True, help="comma-separated case ids, in the order they will run")
    p.add_argument("--routes", default=None, help="comma-separated route keys (default: every dispatchable route on those cases)")
    p.add_argument("--tranche", default="1a")
    p.add_argument("--git-rev", default="HEAD")
    p = sub.add_parser("smoke"); common(p)
    p.add_argument("--case", required=True)
    p.add_argument("--route", required=True)
    p.add_argument("--git-rev", default="HEAD")
    p = sub.add_parser("execute"); common(p)
    p.add_argument("--max-dispatches", type=int, default=None)
    p = sub.add_parser("status"); common(p)
    a = ap.parse_args(argv)

    try:
        if a.cmd == "plan":
            plan = build_plan(a.out, a.run_id, cases=[c.strip() for c in a.cases.split(",") if c.strip()],
                              routes=([r.strip() for r in a.routes.split(",") if r.strip()] if a.routes else None),
                              tranche=a.tranche, auth_path=a.auth, git_rev=a.git_rev)
            h = plan["header"]
            print(json.dumps({"run_id": h["run_id"], "trials": h["counts"]["trials"], "excluded": h["counts"]["excluded"],
                              "estimated_by_pool": h["estimated_by_pool"], "estimated_total_usd_equiv": h["estimated_total_usd_equiv"],
                              "commit": h["commit"], "plan": str(Path(a.out) / PLAN_FILE)}, indent=1))
            return 0
        if a.cmd in ("smoke", "execute"):
            print(f"LIVE: paid calls under {a.auth}; run {a.run_id}; out {a.out}", file=sys.stderr)
            live_kwargs = {"sleep": time.sleep}
            if a.cmd == "smoke":
                summary = smoke(a.out, a.run_id, a.case, a.route, a.auth, live_transport_factory, live_kwargs, git_rev=a.git_rev)
            else:
                summary = LiveRunner(a.out, a.run_id, a.auth, live_transport_factory, live_kwargs).execute(max_dispatches=a.max_dispatches)
            print(json.dumps({k: v for k, v in summary.items() if k != "trial_order"}, indent=1, default=str))
            print_status(status(a.out, a.run_id, a.auth))
            return 0
        if a.cmd == "status":
            print_status(status(a.out, a.run_id, a.auth))
            return 0
    except (PlanRefused, NotAuthorised, DispatchRefused) as exc:
        print(f"REFUSED ({type(exc).__name__}): {exc}", file=sys.stderr)
        return 2
    return 1


if __name__ == "__main__":
    sys.exit(main())
