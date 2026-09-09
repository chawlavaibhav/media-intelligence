#!/usr/bin/env python3
"""registry_rows: the first Capability Registry rows, re-evaluated from SEALED run records under the FROZEN criteria.

    python3 eval/harness-v2/registry_rows.py --run OUT:RUN_ID [--run OUT:RUN_ID ...]            # dry: print, write nothing
    python3 eval/harness-v2/registry_rows.py --run ... --write [--registry eval/registry/registry-v1.jsonl]

WHAT IT DOES (EVAL-041 part 1; Controller freeze of 2026-09-09, MD-C1)

    1. loads every named run: the committed PLAN.yaml (only if it still hashes to PLAN.sha256), every attempt
       (a recovered attempt is preferred, via store.load_attempt), the sealed media and the battery spend ledger;
    2. classifies every planned trial: COUNTED (a provider outcome - an artifact, a refusal, a provider error) or
       EXCLUDED (a local infrastructure fault: network_failure / poll_network_failure with no request id, a
       pre-dispatch refusal, a harness error, an unresolved ambiguous dispatch, or a trial that never ran);
       excluded trials never enter `trials` and are listed on every row under `excluded_trials`;
    3. groups counted trials into CELLS: (question = case family, route_key, surface, arm, prompt basis, frozen
       condition set) - see CELL_CONDITION_PATHS for which frozen levels split a family into several rows;
    4. re-runs the frozen deterministic instruments over the sealed bytes inside a BatteryHarness:
         format_probe        -> delivery_format_compliance, reliability_pass_at_k   (per artifact)
         ledger_metrics      -> latency_errors_refusals, cost_and_cpao              (per trial, refusals included)
         repeat_consistency  -> reproducibility                                      (per repeat pair, unseeded)
    5. builds each row ONLY through BatteryHarness.registry_row_for (the registry gate, then the frozen
       Harness.write_registry_row, then the SCHEMA-v1 uncertainty block) and serialises it with the schema's
       remaining fields (instrument / cost / reliability / freshness blocks, run ids, plan sha256, criteria sha256,
       evidence_tier: deterministic). A capability outside EVALUATOR-PLAN's eight is refused by the gate.
    6. in `--write` mode appends the rows to the registry jsonl (refusing synthetic rows and duplicate entry ids);
       the default mode prints them and writes nothing.

COUNTING RULES (schema v1)
    n_items          distinct base items (cases) in the balanced cell - never trials, never repeats
    repeats_per_item 2 for artifact and trial cells; 1 for reproducibility (one repeat PAIR is one observation)
    trials           counted attempts that carry a scoreable verdict; an item that cannot contribute exactly
                     repeats_per_item scoreable trials is dropped from the row and listed under `items_excluded`
                     (the frozen writer refuses unbalanced cells; a refusal is still counted in the ledger rows)
    uncertainty      computed, clopper_pearson_95 over base items, independence NOT ESTABLISHED (the core cases
                     share one author and one blueprint style), is_reference_calculation_only true
    absence_reason   set only where a whole cell could not be computed (then no row is written; the reason is
                     printed and reported); CpAO is always absent / not_applicable inside a cost row

HOW A TRIAL BECOMES A HARNESS ASSET
    An artifact trial is registered with its sealed bytes. A trial WITHOUT an artifact (a refusal or a provider
    error) is registered with its sealed attempt record as the asset (media_kind other), so that ledger_metrics -
    whose observation unit is the trial and which reads instrument_inputs.attempt - can score it as a fail
    inside a balanced cell. Format and repeat instruments are never run on such an asset.

Nothing here opens a socket or reads a key; git is consulted only to load the freeze package at the plan's
commit when the working tree no longer matches the plan's TEST-CASES sha256.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import tempfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

import yaml

import hv2_paths
import battery_harness as BH
import casebook as CB
import harness as H
import run_live as RL
import store as S
from instruments import common as C
from instruments import format_probe as FP
from instruments import ledger_metrics as LM
from instruments import registry_gate as RG
from instruments import repeat_consistency as RC

REGISTRY_PATH = hv2_paths.EVAL_ROOT / "registry" / "registry-v1.jsonl"
SCHEMA_REF = "eval/registry/SCHEMA-v1-draft.yaml"
CONTRACT_REF = "eval/v1/capability-contract.yaml"
FREEZE_DECISION_REF = "coordination/decisions/CONTROLLER-INSTRUMENT-THRESHOLDS-FROZEN-2026-09-09.md"
EVIDENCE_TIER = "deterministic"
REPEATS_PER_ITEM = 2
UNSEEDED = "unset"

# capability -> how it is measured and where it sits on the contract's ladder
CAPABILITIES = {
    "delivery_format_compliance": {"instrument": "format_probe", "difficulty_level": 3, "contract_id": "delivery_format_compliance",
                                   "routing_use": "hard_constraint", "observation_unit": "artifact",
                                   "ladder": "level 3: resolution class and aspect together (the case declares both)"},
    "reliability_pass_at_k": {"instrument": "format_probe", "difficulty_level": 2, "contract_id": "reliability_pass_at_k",
                              "routing_use": "hard_constraint", "observation_unit": "artifact",
                              "ladder": "level 2: pass-at-2; the deterministic pass criterion is format compliance"},
    "latency_errors_refusals": {"instrument": "ledger_metrics", "difficulty_level": 3, "contract_id": "latency_errors_refusals",
                                "routing_use": "hard_constraint", "observation_unit": "trial",
                                "ladder": "level 3: error rate by error class (p50 / p95 latency and the refusal rate are carried too)"},
    "cost_and_cpao": {"instrument": "ledger_metrics", "difficulty_level": 1, "contract_id": "cost_and_cpao",
                      "routing_use": "hard_constraint", "observation_unit": "trial",
                      "ladder": "level 1: settled cost per call (trial cost); CpAO absent / not_applicable"},
    "reproducibility": {"instrument": "repeat_consistency", "difficulty_level": 3, "contract_id": "reproducibility_repairability",
                        "routing_use": "descriptive_only", "observation_unit": "repeat_pair",
                        "ladder": "level 3: repeat agreement with no seed control (SEED-POLICY unset)"},
}
FORMAT_CAPS = ("delivery_format_compliance", "reliability_pass_at_k")
LEDGER_CAPS = ("latency_errors_refusals", "cost_and_cpao")
PAIR_CAPS = ("reproducibility",)

# Frozen condition levels that DEFINE a cell: cases of one family that differ on any of these go to different rows.
# COND-LANGUAGE.language is the EVALUATOR-PLAN hard rule ("never pooled across en/hi/hg - applies to every case").
# The declared aspect ratio / resolution are NOT cell keys: the frozen format_probe criterion compares each artifact
# with its OWN declaration, so they are recorded per item under conditions.declared_per_item (assumption A1 in the
# EVAL-041 report; a re-cut is a change to this tuple and a new set of rows).
CELL_CONDITION_PATHS = (
    ("COND-LANGUAGE", "language"),
    ("COND-DELIVERY", "duration_s"),
    ("COND-DELIVERY", "fps"),
    ("COND-DELIVERY", "delivery_size_declared"),
    ("COND-REFERENCE", "reference_type"),
    ("COND-INPUT", "input_source_class"),
    ("COND-OPERATION",),
)
ITEM_DECLARED_PATHS = (
    ("COND-DELIVERY", "aspect_ratio"), ("COND-DELIVERY", "resolution"), ("COND-DELIVERY", "platform_target"),
    ("COND-LOAD", "scene_complexity_class"), ("COND-LOAD", "n_people"), ("COND-CONSTRAINT", "exact_string_count"),
    ("COND-LANGUAGE", "script_system"),
)
RETEST_TRIGGERS = ["provider_version_change", "instrument_version_change", "scheduled_interval_elapsed",
                   "production_failure_spike", "vendor_capability_announcement"]
REGISTRY_WRITE_RULE = ("row built by BatteryHarness.registry_row_for: the registry gate (eight deterministic capabilities, deterministic "
                       "instrument, no synthetic measurement) then the frozen eval/v1/harness Harness.write_registry_row; appended by "
                       "eval/harness-v2/registry_rows.py --write; never edited by hand")


class RegistryRowsError(RuntimeError):
    """A run could not be read as sealed evidence, or a row could not be written honestly."""


def _sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _sha256_text(s: str) -> str:
    return _sha256_bytes(s.encode("utf-8"))


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _dig(d, path):
    cur = d
    for k in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(k)
    return cur


def _dec(v):
    try:
        return Decimal(str(v))
    except (InvalidOperation, TypeError, ValueError):
        return None


# ==================================================================================== runs
class Run:
    """One sealed run directory: plan (hash-checked), attempts (recovered preferred), ledger rows, classified trials."""

    def __init__(self, out: Path | str, run_id: str):
        self.out = Path(out)
        self.run_id = run_id
        self.plan = RL.load_plan(self.out, run_id)
        self.plan_sha256 = self.plan["_sha256"]
        self.header = self.plan["header"]
        self.store = S.SealedStore(self.out / RL.ARTIFACTS_DIR)
        self.ledger_path = self.out / RL.LEDGER_DIR / run_id / "spend-ledger.jsonl"
        self.ledger_rows = ([json.loads(l) for l in self.ledger_path.read_text(encoding="utf-8").splitlines() if l.strip()]
                            if self.ledger_path.exists() else [])
        self.trials: list[dict] = []
        for t in self.plan["trials"]:
            attempt = self.store.load_attempt(t["trial_id"])
            status, reason, has_art = classify_trial(self.out, t, attempt)
            rec = {"run_id": run_id, "trial_id": t["trial_id"], "plan": t, "attempt": attempt, "status": status, "reason": reason,
                   "has_artifact": has_art, "artifact_path": None, "attempt_bytes": None, "recovered": False}
            if attempt is not None:
                rp = self.store.recovered_attempt_path(t["trial_id"])
                src = rp if rp.exists() else self.store.attempt_path(t["trial_id"])
                rec["recovered"] = rp.exists()
                rec["attempt_bytes"] = src.read_bytes()
                if has_art:
                    rec["artifact_path"] = self.store.root / attempt["artifact"]["relative_path"]
                    if not self.store.verify(attempt["artifact"]):
                        raise RegistryRowsError(f"{run_id}/{t['trial_id']}: sealed artifact does not hash to its record; nothing built on it")
            self.trials.append(rec)

    @classmethod
    def from_spec(cls, spec: str) -> "Run":
        if ":" not in spec:
            raise RegistryRowsError(f"--run takes OUT:RUN_ID, got {spec!r}")
        out, run_id = spec.rsplit(":", 1)
        return cls(out, run_id)

    @property
    def ref(self) -> str:
        try:
            return str(self.out.resolve().relative_to(hv2_paths.REPO_ROOT.resolve()))
        except ValueError:
            return str(self.out)


def classify_trial(out: Path, plan_trial: dict, attempt: dict | None) -> tuple:
    """(status, reason, has_artifact). COUNTED = a provider outcome. EXCLUDED = a local fault or a trial that never ran."""
    tid = plan_trial["trial_id"]
    if attempt is None:
        for kind in ("pre_dispatch_refusal", "harness_error"):
            rp = Path(out) / RL.TRIALS_DIR / f"{S.safe_id(tid)}.{kind}.json"
            if rp.exists():
                try:
                    reason = str(json.loads(rp.read_text(encoding="utf-8")).get("reason", ""))[:200]
                except Exception:  # noqa: BLE001
                    reason = "unreadable record"
                return "excluded", f"{kind}: {reason}", False
        return "excluded", "not_dispatched: no attempt record and no trial record", False
    status = attempt.get("status")
    if status == "ok" and attempt.get("artifact"):
        return "counted", "ok", True
    ec = attempt.get("error_class") or ""
    if ec in RL.INFRA_ERROR_CLASSES and not attempt.get("provider_request_id"):
        return "excluded", f"infrastructure_fault: {ec}", False
    if attempt.get("ambiguous_dispatch") and attempt.get("outcome_resolved") is False:
        return "excluded", f"ambiguous_dispatch_unresolved: {ec}", False
    return "counted", f"provider_outcome: {status} ({ec or 'no error class'})", False


def resolve_book(header: dict, book: CB.CaseBook | None = None) -> CB.CaseBook:
    """The freeze package the plan was built from: the working tree if its TEST-CASES sha256 matches, else the plan's commit."""
    if book is not None:
        return book
    b = CB.CaseBook.from_paths()
    if b.source.get("test_cases_sha256") == header.get("test_cases_sha256"):
        return b
    commit = header.get("commit")
    if not commit:
        raise RegistryRowsError("the plan names no commit and the working tree's TEST-CASES.yaml differs from the plan's")
    return CB.CaseBook.from_git(commit)


# ==================================================================================== cells
def family_of(case_id: str) -> str:
    return case_id.rsplit("-", 1)[0] if "-" in case_id else case_id


def workflow_mode_for(conditions: dict, arm: str | None, default: str) -> str:
    modes = _dig(conditions, ("COND-WORKFLOW", "workflow_mode_per_route_arm"))
    if not isinstance(modes, dict) or not modes:
        return default
    composite = bool(arm and arm.startswith(CB.COMPOSITE_ARM_PREFIX))
    for k, v in modes.items():
        if ("arm c" in k.lower()) == composite:
            return str(v)
    return str(next(iter(modes.values())))


def prompt_basis(book: CB.CaseBook, case_id: str, arm: str | None, attempt: dict) -> str:
    """Which blueprint prompt the sealed request carried: the main prompt, the textless plate, or neither."""
    ph = attempt.get("prompt_hash")
    if not ph:
        return "unknown:no_prompt_hash"
    try:
        if _sha256_text(book.prompt_for(case_id)) == ph:
            return "blueprint_main"
    except Exception:  # noqa: BLE001
        pass
    if arm and arm.startswith(CB.COMPOSITE_ARM_PREFIX):
        try:
            if _sha256_text(book.prompt_for(case_id, arm)) == ph:
                return "blueprint_textless_plate"
        except Exception:  # noqa: BLE001
            pass
    return f"unknown:{ph[:12]}"


def cell_conditions(case_row: dict, arm: str | None, attempt: dict) -> tuple:
    """(cell-defining levels, declared-per-item levels) from the case's frozen conditions."""
    conds = case_row.get("conditions") or {}
    levels = {".".join(p): _dig(conds, p) for p in CELL_CONDITION_PATHS}
    levels["workflow_mode"] = workflow_mode_for(conds, arm, attempt.get("workflow") or "")
    levels["seed_policy"] = attempt.get("seed_policy") or case_row.get("params", {}).get("seed") or UNSEEDED
    levels["lane"] = attempt.get("lane") or "image"
    levels["audio"] = (case_row.get("params") or {}).get("audio")
    declared = {".".join(p): _dig(conds, p) for p in ITEM_DECLARED_PATHS}
    declared["params.aspect"] = (case_row.get("params") or {}).get("aspect")
    declared["params.resolution"] = (case_row.get("params") or {}).get("resolution")
    return levels, declared


def build_cells(runs: list[Run], book: CB.CaseBook | None = None) -> dict:
    """Group COUNTED trials into cells; return {cell_id: cell}. Excluded trials are attached to the cell they belonged to."""
    cells: dict = {}
    for run in runs:
        b = resolve_book(run.header, book)
        for rec in run.trials:
            t = rec["plan"]
            case_id, route, arm, rep = t["case_id"], t["route_key"], t.get("arm"), int(t.get("repeat_index") or 1)
            try:
                case_row = b.row(case_id, route, arm, rep)
            except KeyError:
                case_row = b.row(case_id, route, arm, 1)
            attempt = rec["attempt"] or {}
            basis = prompt_basis(b, case_id, arm, attempt) if attempt else "unknown:not_dispatched"
            levels, declared = cell_conditions(case_row, arm, attempt)
            family = family_of(case_id)
            surface = t.get("surface") or attempt.get("surface") or ""
            provenance = {
                "provider": attempt.get("provider") or surface, "model": attempt.get("model_id") or t.get("surface_model_id") or route,
                "version": attempt.get("model_version") or t.get("surface_model_id") or "unpinnable",
                "endpoint": attempt.get("endpoint") or t.get("endpoint") or "", "workflow": attempt.get("workflow") or levels["workflow_mode"],
                "lane": levels["lane"],
            }
            if rec["status"] == "excluded":
                # attach to whichever cell of this (family, route, arm) exists or will exist; provenance may be plan-only
                basis_key = "any"
                key_material = {"family": family, "route_key": route, "surface": surface, "arm": arm, "levels": levels}
            else:
                basis_key = basis
                key_material = {"family": family, "route_key": route, "surface": surface, "arm": arm, "prompt_basis": basis, "levels": levels,
                                "provenance": provenance}
            cond_id = _sha256_text(json.dumps({"levels": levels, "arm": arm}, sort_keys=True, default=str))[:12]
            cid = f"{family}__{route}__{arm or 'core'}__{basis_key}__{cond_id}"
            if rec["status"] == "excluded":
                # find the counted cell for this family/route/arm/cond_id (any prompt basis); else park under a shadow cell
                targets = [c for c in cells.values() if c["family"] == family and c["route_key"] == route and c["arm"] == arm and c["cond_id"] == cond_id]
                if targets:
                    for c in targets:
                        c["excluded"].append(_excluded_note(rec))
                else:
                    cells.setdefault(cid, _new_cell(cid, family, route, surface, arm, "any", cond_id, levels, provenance, key_material))
                    cells[cid]["excluded"].append(_excluded_note(rec))
                continue
            cell = cells.setdefault(cid, _new_cell(cid, family, route, surface, arm, basis, cond_id, levels, provenance, key_material))
            if cell["provenance"] != provenance:
                raise RegistryRowsError(f"cell {cid}: trials disagree on provenance {cell['provenance']} vs {provenance}; one row is one model+endpoint")
            cell["declared_per_item"].setdefault(case_id, declared)
            cell["items"][case_id].append({**rec, "case_row": case_row, "run": run})
            cell["runs"][run.run_id] = run
    # shadow cells (only excluded trials) are merged into the counted cell of the same family/route/arm/cond if one exists
    for cid in [c for c in cells if cells[c]["prompt_basis"] == "any"]:
        shadow = cells[cid]
        targets = [c for c in cells.values() if c["cell_id"] != cid and c["family"] == shadow["family"] and c["route_key"] == shadow["route_key"]
                   and c["arm"] == shadow["arm"] and c["cond_id"] == shadow["cond_id"]]
        if targets:
            for c in targets:
                c["excluded"].extend(shadow["excluded"])
            del cells[cid]
    for c in cells.values():
        for case_id in c["items"]:
            c["items"][case_id].sort(key=lambda r: int(r["plan"].get("repeat_index") or 1))
    return cells


def _new_cell(cid, family, route, surface, arm, basis, cond_id, levels, provenance, key_material) -> dict:
    return {"cell_id": cid, "family": family, "route_key": route, "surface": surface, "arm": arm, "prompt_basis": basis, "cond_id": cond_id,
            "levels": levels, "provenance": provenance, "key_material": key_material, "items": defaultdict(list), "declared_per_item": {},
            "excluded": [], "runs": {}}


def _excluded_note(rec: dict) -> dict:
    a = rec.get("attempt") or {}
    return {"run_id": rec["run_id"], "trial_id": rec["trial_id"], "case_id": rec["plan"]["case_id"], "repeat_index": rec["plan"].get("repeat_index"),
            "reason": rec["reason"], "status": a.get("status"), "error_class": a.get("error_class"), "reservation_id": a.get("reservation_id")}


# ==================================================================================== instruments + harness
RECORD_ASSET_CONTENT_TYPE = "application/json"


class RegistryHarness(BH.BatteryHarness):
    """BatteryHarness with one storage detail fixed for record-assets: a sealed attempt record standing in for a trial
    without an artifact is stored as `<asset_id>.json`. BatteryHarness maps every unknown content type to `.bin`, which
    is the extension of the frozen harness's own pointer file for the same asset, so the two would collide.
    write_registry_row and registry_row_for are inherited untouched (a test proves it)."""

    def generate(self, item, provider_cfg, generator, **kw):
        saved = S.EXT_BY_CONTENT_TYPE.get(RECORD_ASSET_CONTENT_TYPE)
        S.EXT_BY_CONTENT_TYPE[RECORD_ASSET_CONTENT_TYPE] = ".json"
        try:
            return super().generate(item, provider_cfg, generator, **kw)
        finally:
            if saved is None:
                S.EXT_BY_CONTENT_TYPE.pop(RECORD_ASSET_CONTENT_TYPE, None)
            else:
                S.EXT_BY_CONTENT_TYPE[RECORD_ASSET_CONTENT_TYPE] = saved


def frozen_instruments(criteria_path: Path | str | None = None) -> dict:
    """The three deterministic instruments built from the committed (frozen) criteria; refuses an unfrozen file.
    Each instrument's fn is wrapped so its full result (the measurement the frozen Measurement does not keep) is
    retained on `inst.results[(path, capability)]`; the wrapper changes neither config nor config_hash."""
    insts = {i.id: i for i in (FP.instrument(criteria_path), LM.instrument(criteria_path), RC.instrument(criteria_path))}
    for iid in ("format_probe", "ledger_metrics", "repeat_consistency"):
        crit = C.criterion(iid, criteria_path)
        if not crit.frozen:
            raise RegistryRowsError(f"{crit.ref} is not frozen; no Registry row may be built on an unapproved threshold (MD-C1)")
    for inst in insts.values():
        inst.results = {}
        inst.fn = _recording(inst.fn, inst.results)
    return insts


def _recording(fn, results: dict):
    def wrapped(path, item, capability):
        r = fn(path, item, capability)
        results[(str(path), capability)] = r
        return r
    return wrapped


def criteria_sha256(criteria_path: Path | str | None = None) -> str:
    return C.load_criteria(criteria_path)["_sha256"]


def _evidence_clock(cell: dict):
    stamps = [r["attempt"].get("completed_at") or r["attempt"].get("requested_at") for rs in cell["items"].values() for r in rs if r.get("attempt")]
    stamps = [s for s in stamps if s]
    fixed = max(stamps) if stamps else _now()
    return lambda: fixed


def _settled(attempt: dict, ledger_rows: list):
    row = LM.settled_row(attempt, ledger_rows)
    return _dec(row.get("amount_usd_equiv", row.get("amount_usd"))) if row else None


def populate_harness(cell: dict, root: Path, instruments: dict) -> tuple:
    """Register every counted trial of the cell as a harness asset and measure it. Returns (harness, measurements-by-cap, asset index)."""
    hz = RegistryHarness(root, clock=_evidence_clock(cell))
    for inst in instruments.values():
        hz.register_instrument(inst)
    by_cap: dict = defaultdict(list)
    index: dict = {}          # (run_id, trial_id) -> {"asset_id", "prov", "rec"}
    prov_base = cell["provenance"]
    for case_id, recs in cell["items"].items():
        first_attempt_id = None
        for rec in recs:
            attempt, t = rec["attempt"], rec["plan"]
            rep = int(t.get("repeat_index") or 1)
            settled = _settled(attempt, rec["run"].ledger_rows)
            cfg = {**prov_base, "currency": attempt.get("currency") or "USD", "seed_policy": attempt.get("seed_policy") or UNSEEDED,
                   "media_kind": (attempt.get("artifact") or {}).get("media_kind", "image") if rec["has_artifact"] else "other",
                   "route_key": cell["route_key"], "arm": cell["arm"] or "", "config_path": attempt.get("config_location") or ""}
            item = {"item_id": case_id, "prompt_spec": attempt.get("prompt_hash") or "", "measurement_fanout": list(CAPABILITIES)}
            if rec["has_artifact"]:
                data, ct = rec["artifact_path"].read_bytes(), (attempt["artifact"].get("content_type") or "application/octet-stream")
            else:
                data, ct = rec["attempt_bytes"], RECORD_ASSET_CONTENT_TYPE

            def gen(it, cfg_, data=data, ct=ct, settled=settled):
                return {"api_status": "ok", "payload_bytes": data, "content_type": ct, "synthetic": False,
                        "cost_generation": (float(settled) if settled is not None else None)}
            kw = {}
            if rep > 1 and first_attempt_id:
                kw = {"repeat_of": first_attempt_id, "repeat_index": rep}
            prov = hz.generate(item, cfg, gen, **kw)
            if rep == 1 or first_attempt_id is None:
                first_attempt_id = prov.attempt_id
            index[(rec["run_id"], rec["trial_id"])] = {"asset_id": prov.asset_id, "prov": prov, "rec": rec, "case_id": case_id, "repeat_index": rep}
    # measurements
    for key, ent in index.items():
        rec, asset = ent["rec"], ent["asset_id"]
        attempt, case_row = rec["attempt"], rec["case_row"]
        base_item = {"item_id": ent["case_id"], "measurement_fanout": list(CAPABILITIES)}
        if rec["has_artifact"]:
            for cap in FORMAT_CAPS:
                m = hz.measure(asset, cap, "format_probe", {**base_item, "instrument_inputs": {"case_row": case_row}}, observation_unit="artifact")
                by_cap[cap].append((m, ent))
        for cap in LEDGER_CAPS:
            m = hz.measure(asset, cap, "ledger_metrics", {**base_item, "instrument_inputs": {"attempt": attempt, "ledger_rows": rec["run"].ledger_rows}},
                           observation_unit="trial")
            by_cap[cap].append((m, ent))
        if rec["has_artifact"] and ent["repeat_index"] > 1:
            first = next((e for e in index.values() if e["case_id"] == ent["case_id"] and e["repeat_index"] == 1), None)
            if first and first["rec"]["has_artifact"]:
                inputs = {"other_repeat_path": str(first["rec"]["artifact_path"]), "seed_policy": attempt.get("seed_policy") or UNSEEDED}
                m = hz.measure(asset, "reproducibility", "repeat_consistency", {**base_item, "instrument_inputs": inputs}, observation_unit="repeat_pair")
                by_cap["reproducibility"].append((m, ent, first))
    return hz, by_cap, index


# ==================================================================================== rows
def balanced_items(pairs: list, repeats: int) -> tuple:
    """Split measurement tuples into (kept, items_excluded) so every kept item has exactly `repeats` scoreable measurements."""
    per_item: dict = defaultdict(list)
    for tup in pairs:
        per_item[tup[1]["case_id"]].append(tup)
    kept, excluded = [], []
    for case_id, tups in per_item.items():
        scoreable = [tp for tp in tups if tp[0].verdict in ("pass", "fail")]
        absent = [tp for tp in tups if tp[0].verdict == "absent"]
        if len(scoreable) == repeats and not absent:
            kept.extend(scoreable)
        else:
            excluded.append({"item_id": case_id, "scoreable": len(scoreable), "required": repeats,
                             "absent": [{"trial_id": tp[1]["rec"]["trial_id"], "absence_reason": tp[0].absence_reason} for tp in absent]})
    return kept, excluded


def write_cell_rows(cell: dict, instruments: dict, root: Path, crit_sha: str, capabilities=tuple(CAPABILITIES)) -> tuple:
    """Every row of one cell through BatteryHarness.registry_row_for. Returns (records, unwritten)."""
    for cap in capabilities:
        if cap not in CAPABILITIES:
            # the gate is the authority; ask it directly so the refusal names EVALUATOR-PLAN's list
            RG.assert_registry_eligible(cap, instruments.get("format_probe"))
            raise RegistryRowsError(f"capability {cap!r} has no deterministic measurement plan in registry_rows.py")
    hz, by_cap, index = populate_harness(cell, root, instruments)
    ledger_attempts = [e["rec"]["attempt"] for e in index.values()]
    ledger_rows_all = [r for run in cell["runs"].values() for r in run.ledger_rows]
    cell_metrics = LM.cell_metrics(ledger_attempts, ledger_rows_all) if ledger_attempts else None
    records, unwritten = [], []
    conditions = {**cell["levels"], "arm": cell["arm"], "prompt_basis": cell["prompt_basis"], "declared_per_item": cell["declared_per_item"]}
    for cap in capabilities:
        spec = CAPABILITIES[cap]
        inst = instruments[spec["instrument"]]
        repeats = 1 if cap in PAIR_CAPS else REPEATS_PER_ITEM
        pairs = by_cap.get(cap, [])
        kept, items_excluded = balanced_items(pairs, repeats)
        no_artifact = [{"item_id": e["case_id"], "trial_id": e["rec"]["trial_id"], "run_id": e["rec"]["run_id"], "status": e["rec"]["attempt"].get("status"),
                        "error_class": e["rec"]["attempt"].get("error_class")} for e in index.values() if not e["rec"]["has_artifact"]]
        if cap in FORMAT_CAPS + PAIR_CAPS:
            for na in no_artifact:
                if na["item_id"] not in {x["item_id"] for x in items_excluded} and na["item_id"] not in {tp[1]["case_id"] for tp in kept}:
                    items_excluded.append({"item_id": na["item_id"], "scoreable": 0, "required": repeats, "absent": [], "no_artifact": [na]})
            for x in items_excluded:
                x.setdefault("no_artifact", [na for na in no_artifact if na["item_id"] == x["item_id"]])
        if not kept:
            unwritten.append({"cell_id": cell["cell_id"], "capability": cap, "absence_reason": _absence_for(items_excluded, no_artifact),
                              "items_excluded": items_excluded, "note": "no item contributes a balanced set of scoreable measurements"})
            continue
        ms = [tp[0] for tp in kept]
        try:
            row = hz.registry_row_for(cap, inst.id, ms, conditions, spec["difficulty_level"], repeats)
        except (H.HarnessError, RG.RegistryGateRefused) as exc:
            unwritten.append({"cell_id": cell["cell_id"], "capability": cap, "absence_reason": "other", "items_excluded": items_excluded,
                              "note": f"writer refused: {exc}"})
            continue
        records.append(to_record(row, cell, cap, kept, items_excluded, no_artifact, cell_metrics, index, crit_sha, inst, by_cap))
    return records, unwritten


def _absence_for(items_excluded: list, no_artifact: list) -> str:
    if any(na.get("status") == "refusal" for na in no_artifact):
        return "refused"
    if no_artifact:
        return "generation_failed"
    if any(x.get("absent") for x in items_excluded):
        return "not_measured"
    return "not_applicable"


def _entry_id(cell: dict, cap: str, inst) -> str:
    return "cap-" + _sha256_text(json.dumps({"cell": cell["key_material"], "runs": sorted(cell["runs"]), "capability": cap,
                                             "instrument_config_hash": inst.config_hash}, sort_keys=True, default=str))[:16]


def to_record(row, cell: dict, cap: str, kept: list, items_excluded: list, no_artifact: list, cell_metrics, index: dict, crit_sha: str, inst, by_cap) -> dict:
    spec = CAPABILITIES[cap]
    rec = row.to_dict()
    runs = cell["runs"]
    trial_ids = sorted({tp[1]["rec"]["trial_id"] for tp in kept})
    settled = [(_settled(e["rec"]["attempt"], e["rec"]["run"].ledger_rows)) for e in index.values()]
    settled_known = [s for s in settled if s is not None]
    settled_total = sum(settled_known, Decimal("0")) if settled_known else None
    price_pins = sorted({e["rec"]["plan"].get("price_pin_ref") or "" for e in index.values()} - {""})
    unit_prices = sorted({str(e["rec"]["plan"].get("unit_price")) for e in index.values()})
    billing_pools = sorted({str(e["rec"]["plan"].get("billing_pool")) for e in index.values()})
    crit = C.criterion(spec["instrument"])
    raw_crit = (yaml.safe_load(Path(crit.path).read_text(encoding="utf-8")) or {}).get("criteria", {}).get(spec["instrument"], {})
    results = getattr(inst, "results", {})
    trial_verdicts = [{"run_id": tp[1]["rec"]["run_id"], "trial_id": tp[1]["rec"]["trial_id"], "item_id": tp[1]["case_id"], "repeat_index": tp[1]["repeat_index"],
                       "verdict": tp[0].verdict, "defects": tp[0].defects, "recovered_attempt": tp[1]["rec"]["recovered"],
                       "artifact_sha256": (tp[1]["rec"]["attempt"].get("artifact") or {}).get("sha256"),
                       "status": tp[1]["rec"]["attempt"].get("status"), "error_class": tp[1]["rec"]["attempt"].get("error_class"),
                       "measurement_notes": _measurement_notes(results.get((tp[1]["prov"].output_path, cap)))} for tp in kept]
    recovered = sorted(e["rec"]["trial_id"] for e in index.values() if e["rec"]["recovered"])
    defect_terms = Counter(d.get("term") for tv in trial_verdicts for d in tv["defects"])
    cooccur = Counter(tuple(sorted(d.get("term") for d in tv["defects"])) for tv in trial_verdicts if len(tv["defects"]) > 1)
    latencies = {e["rec"]["trial_id"]: LM.latency_s(e["rec"]["attempt"]) for e in index.values()}
    rec.update({
        "entry_id": _entry_id(cell, cap, inst), "harness_entry_id": row.entry_id,
        "schema_version": "v1-draft", "schema_ref": SCHEMA_REF, "contract_version": "v1-draft", "contract_ref": CONTRACT_REF,
        "contract_dimension_id": spec["contract_id"], "routing_use": spec["routing_use"], "difficulty_level_basis": spec["ladder"],
        "lane": cell["levels"].get("lane"), "question": cell["family"], "route_key": cell["route_key"], "surface": cell["surface"], "arm": cell["arm"],
        "prompt_basis": cell["prompt_basis"], "bank_item_ids": sorted({tp[1]["case_id"] for tp in kept}), "cell_item_ids": sorted(cell["items"]), "battery_version": "EVAL-040-TRANCHE-1 / STAGE-A-FREEZE-2026-09",
        "run_ids": sorted(runs), "runs": [{"run_id": r.run_id, "run_ref": r.ref, "plan_sha256": r.plan_sha256, "commit": r.header.get("commit"),
                                          "authorisation_sha256": r.header.get("authorisation_sha256")} for r in runs.values()],
        "run_ref": "; ".join(sorted(r.ref for r in runs.values())), "raw_outputs_ref": sorted(f"{r.ref}/{RL.ARTIFACTS_DIR}" for r in runs.values()),
        "artifact_manifest_ref": sorted(f"{r.ref}/{RL.ARTIFACTS_DIR}/manifest.jsonl" for r in runs.values()),
        "trial_ids": trial_ids, "criteria_ref": C.CRITERIA_REF, "criteria_sha256": crit_sha, "pass_criterion_ref": crit.ref,
        "evidence_tier": EVIDENCE_TIER, "tested_date": row.tested_date, "written_utc": _now(), "sample_source": "lab", "synthetic": False,
        "absence_reason": None, "registry_write_rule": REGISTRY_WRITE_RULE,
        "instrument": {"id": inst.id, "version": inst.version, "config_hash": inst.config_hash, "role": "gate",
                       "deterministic_component": crit.metric.strip(), "calibration_ref": inst.calibration_ref,
                       "calibration_date": str(raw_crit.get("frozen_at") or ""), "calibration_status": "deterministic",
                       "qualification_record_ref": FREEZE_DECISION_REF, "thresholds": crit.thresholds, "frozen": crit.frozen},
        "cost": {"currency": "USD", "price_source": price_pins, "price_read_date": "2026-09 (price-pins-2026-09)", "unit_price_pinned": unit_prices,
                 "billing_pool": billing_pools, "generation_total": row.cost_generation_total, "transform_total": 0.0,
                 "evaluator_total": row.cost_evaluator_total, "human_verification_total": 0.0, "repair_total": None,
                 "usd_per_pass": row.usd_per_pass, "usd_per_pass_lower_bound": row.usd_per_pass_lower_bound,
                 "settled_total_usd_equiv_all_counted_trials": (str(settled_total.quantize(Decimal("0.000001"))) if settled_total is not None else None),
                 "per_trial_usd_mean": (str((settled_total / len(settled_known)).quantize(Decimal("0.000001"))) if settled_known else None),
                 "n_settled": len(settled_known), "basis": "settled spend rows of the battery ledger (pinned price x quantity); never an estimate"},
        "latency_s": ({"p50": cell_metrics["latency_s"]["p50"], "p95": cell_metrics["latency_s"]["p95"], "n": cell_metrics["latency_s"]["n"],
                       "method": "nearest_rank", "by_trial": latencies, "recovered_trials": recovered,
                       "caveat": ("completed_at of a RECOVERED attempt is the recovery time, so its latency includes the outage / misread gap, "
                                  "not the provider's time alone" if recovered else None)} if cell_metrics else {"p50": None, "p95": None}),
        "reliability": {"api_error_rate": cell_metrics["error_rate"] if cell_metrics else None,
                        "error_classes": [{"class": k, "n": v} for k, v in sorted((cell_metrics or {}).get("error_class_counts", {}).items())],
                        "moderation_block_rate": ((cell_metrics or {}).get("error_class_counts", {}).get("moderation_block", 0) / cell_metrics["n_attempts"]) if cell_metrics else None,
                        "refusal_rate": cell_metrics["refusal_rate"] if cell_metrics else None,
                        "status_counts": (cell_metrics or {}).get("status_counts"), "n_counted_trials": (cell_metrics or {}).get("n_attempts"),
                        "reproducibility": {"seed_supported": None, "seed_honoured": None, "seed_policy": cell["levels"].get("seed_policy"),
                                            "repeat_agreement": _repeat_agreement(by_cap.get("reproducibility", []))}},
        "freshness": {"status": "current", "model_version_at_test": row.version, "tested_date": row.tested_date, "retest_triggers": RETEST_TRIGGERS,
                      "note": "assigned by trigger, not by formula (SCHEMA-v1)"},
        "failure_type_counts": dict(defect_terms), "failure_cooccurrence": [{"terms": list(k), "n": v} for k, v in cooccur.items()],
        "trial_verdicts": trial_verdicts, "items_excluded": items_excluded, "trials_without_artifact": no_artifact,
        "excluded_trials": cell["excluded"], "conditions": row.conditions,
    })
    if cap == "cost_and_cpao":
        rec["cpao"] = {"verdict": "absent", "absence_reason": "not_applicable", "note": "no accepted-outcome chain at Stage A; trial cost only"}
    if cap == "reliability_pass_at_k":
        rec["pass_at_k"] = _pass_at_k(by_cap.get("delivery_format_compliance", []), index, REPEATS_PER_ITEM)
    if cap == "reproducibility":
        rec["repeat_variance"] = _repeat_variance(kept, inst)
        rec["variance_uncertainty"] = {"status": "not_computed", "not_computed_reason": "descriptive_only_result",
                                       "not_computed_note": "unseeded dHash / SSIM distances are a variance measurement with no pass/fail and no error bar; "
                                                            "the row's passes count the frozen structural rule (both repeats valid, same probed format)"}
        rec["observation_unit"] = "repeat_pair"
        rec["repeats_per_item_note"] = "one repeat PAIR (repeat 1 vs repeat 2 of the same case x route) is one observation; trials = pairs"
    if row.uncertainty.get("assumptions") is not None:
        row.uncertainty["assumptions"] = list(row.uncertainty["assumptions"]) + [
            "the four core items and the two text items were written by one author from one brief bank; correlated difficulty across items is likely",
            "one route, one endpoint, one frozen prompt per item: repeats are draws of the same request, never new items"]
        rec["uncertainty"] = row.uncertainty
    return rec


def _measurement_notes(result):
    """The instrument's own reading of the artifact (format_probe notes / probe size; ledger status), for a human reader of the row."""
    if not result:
        return None
    m = result.get("measurement") or {}
    if "probe" in m:
        p = m["probe"]
        return {"observed": f"{p.get('width')}x{p.get('height')} {p.get('container')} audio={'yes' if p.get('has_audio') else 'no'}", "notes": m.get("notes"),
                "checks": m.get("checks")}
    if "status" in m:
        return {"status": m.get("status"), "error_class": m.get("error_class"), "latency_s": m.get("latency_s"), "billing_state": m.get("billing_state")}
    if "settled_usd_equiv" in m:
        return {"settled_usd_equiv": m.get("settled_usd_equiv"), "reserved_usd_equiv": m.get("reserved_usd_equiv")}
    if "dhash_hamming_max" in m:
        return {"dhash_hamming_max": m.get("dhash_hamming_max"), "ssim_min": m.get("ssim_min"), "same_probed_format": m.get("same_probed_format")}
    return None


def _repeat_agreement(pairs: list):
    vals = []
    for tp in pairs:
        m = tp[0]
        if m.verdict in ("pass", "fail"):
            vals.append(1.0 if m.verdict == "pass" else 0.0)
    return (sum(vals) / len(vals)) if vals else None


def _pass_at_k(format_pairs: list, index: dict, k: int) -> dict:
    per_item: dict = defaultdict(lambda: {"pass": 0, "fail": 0, "absent": 0, "no_artifact": 0})
    for tp in format_pairs:
        per_item[tp[1]["case_id"]][tp[0].verdict if tp[0].verdict in ("pass", "fail") else "absent"] += 1
    for e in index.values():
        if not e["rec"]["has_artifact"]:
            per_item[e["case_id"]]["no_artifact"] += 1
    items = dict(per_item)
    return {"k": k, "criterion": "format_probe pass (delivery_format_compliance)", "n_items": len(items),
            "items_with_at_least_one_pass": sum(1 for v in items.values() if v["pass"] >= 1),
            "items_with_all_passes": sum(1 for v in items.values() if v["pass"] == k),
            "per_item": items, "note": "a refusal or error counts as a non-pass at that draw; this block covers every counted trial, "
                                       "the row's n_items / trials cover only the balanced artifact set"}


def _repeat_variance(kept: list, inst) -> dict:
    """The distances the repeat_consistency instrument measured (read back from its recorded results, never re-measured)."""
    pairs = []
    for tp in kept:
        m, ent, first = tp[0], tp[1], (tp[2] if len(tp) > 2 else None)
        res = (getattr(inst, "results", {}).get((ent["prov"].output_path, "reproducibility")) or {}).get("measurement") if first else None
        pairs.append({"item_id": ent["case_id"], "trial_ids": [first["rec"]["trial_id"] if first else None, ent["rec"]["trial_id"]],
                      "dhash_hamming_max": res["dhash_hamming_max"] if res else None, "ssim_min": res["ssim_min"] if res else None,
                      "same_probed_format": res["same_probed_format"] if res else None, "group": res["group"] if res else None,
                      "structural_verdict": m.verdict})
    ham = [p["dhash_hamming_max"] for p in pairs if p["dhash_hamming_max"] is not None]
    ssim = [p["ssim_min"] for p in pairs if p["ssim_min"] is not None]
    return {"group": "unseeded", "seed_policy": UNSEEDED, "pairs": pairs, "n_pairs": len(pairs),
            "dhash_hamming": {"mean": (sum(ham) / len(ham)) if ham else None, "max": max(ham) if ham else None, "min": min(ham) if ham else None},
            "ssim": {"mean": (sum(ssim) / len(ssim)) if ssim else None, "min": min(ssim) if ssim else None, "max": max(ssim) if ssim else None},
            "reading": "64-bit dHash Hamming distance (0 = identical structure, 32 = unrelated) and global SSIM between the two draws; observation only"}


# ==================================================================================== registry file
def existing_entry_ids(path: Path) -> set:
    if not Path(path).exists():
        return set()
    ids = set()
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.lstrip().startswith("#"):
            ids.add(json.loads(line).get("entry_id"))
    return ids


def append_records(path: Path | str, records: list) -> int:
    """Append rows to the registry jsonl. Refuses a synthetic row, a row without entry_id, or a duplicate entry id."""
    path = Path(path)
    seen = existing_entry_ids(path)
    for r in records:
        if r.get("synthetic") is not False:
            raise RegistryRowsError(f"row {r.get('entry_id')} is not marked synthetic: false; refused")
        if not r.get("entry_id"):
            raise RegistryRowsError("row without entry_id; refused")
        if r["entry_id"] in seen:
            raise RegistryRowsError(f"entry_id {r['entry_id']} already in {path}; a row is written once")
        seen.add(r["entry_id"])
        if r.get("evidence_tier") != EVIDENCE_TIER:
            raise RegistryRowsError(f"row {r['entry_id']} carries evidence_tier {r.get('evidence_tier')!r}; only deterministic rows are registry rows")
    with path.open("a", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, sort_keys=True, ensure_ascii=False, default=str) + "\n")
    return len(records)


# ==================================================================================== driver
def build_rows(run_specs: list, book: CB.CaseBook | None = None, harness_root: Path | str | None = None, criteria_path: Path | str | None = None,
               capabilities=tuple(CAPABILITIES)) -> dict:
    runs = [Run.from_spec(s) if isinstance(s, str) else s for s in run_specs]
    instruments = frozen_instruments(criteria_path)
    crit_sha = criteria_sha256(criteria_path)
    cells = build_cells(runs, book)
    root = Path(harness_root) if harness_root else Path(tempfile.mkdtemp(prefix="hv2-registry-"))
    records, unwritten = [], []
    for cid, cell in sorted(cells.items()):
        if not cell["items"]:
            unwritten.append({"cell_id": cid, "capability": None, "absence_reason": "not_measured", "items_excluded": [],
                              "note": "every planned trial of this cell was excluded (infrastructure fault / never dispatched)", "excluded_trials": cell["excluded"]})
            continue
        recs, unw = write_cell_rows(cell, instruments, root / S.safe_id(cid), crit_sha, capabilities)
        records.extend(recs)
        unwritten.extend(unw)
    return {"records": records, "unwritten": unwritten, "cells": cells, "runs": runs, "criteria_sha256": crit_sha, "harness_root": root,
            "instruments": {k: {"version": v.version, "config_hash": v.config_hash} for k, v in instruments.items()}}


def summary_table(result: dict) -> str:
    lines = [f"{'cell':<70} {'capability':<28} {'n':>3} {'rep':>3} {'trials':>6} {'pass':>5} {'lo':>6} {'hi':>6}  entry_id"]
    for r in result["records"]:
        u = r["uncertainty"]
        lines.append(f"{r['question'] + '/' + r['route_key'] + '/' + str(r['arm']) + '/' + r['conditions'].get('COND-LANGUAGE.language', '?'):<70} "
                     f"{r['capability']:<28} {r['n_items']:>3} {r['repeats_per_item']:>3} {r['trials']:>6} {r['passes']:>5} "
                     f"{u.get('interval_low', 0):>6.3f} {u.get('interval_high', 0):>6.3f}  {r['entry_id']}")
    for u in result["unwritten"]:
        lines.append(f"UNWRITTEN {u['cell_id']} {u.get('capability')}: {u.get('absence_reason')} - {u.get('note')}")
    by_cap = Counter(r["capability"] for r in result["records"])
    by_route = Counter(r["route_key"] for r in result["records"])
    lines.append(f"rows: {len(result['records'])}  by capability: {dict(sorted(by_cap.items()))}  by route: {dict(sorted(by_route.items()))}")
    lines.append(f"criteria_sha256: {result['criteria_sha256']}")
    return "\n".join(lines)


def main(argv=None, book: CB.CaseBook | None = None) -> int:
    """CLI. `book` is a test-only injection of the freeze package (the CLI resolves it from the plan)."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--run", action="append", required=True, help="OUT_DIR:RUN_ID (repeatable)")
    ap.add_argument("--write", action="store_true", help="append the rows to the registry (default: dry, print only)")
    ap.add_argument("--registry", default=str(REGISTRY_PATH))
    ap.add_argument("--json", default=None, help="also dump the records (dry or written) to this file")
    ap.add_argument("--harness-root", default=None, help="where the per-cell harness state goes (default: a temp dir, deleted afterwards)")
    ap.add_argument("--keep-harness", action="store_true")
    ap.add_argument("--capability", action="append", default=None, help="restrict to these capabilities (default: all five)")
    a = ap.parse_args(argv)
    caps = tuple(a.capability) if a.capability else tuple(CAPABILITIES)
    result = build_rows(a.run, book=book, harness_root=a.harness_root, capabilities=caps)
    try:
        print(summary_table(result))
        if a.json:
            Path(a.json).write_text("\n".join(json.dumps(r, sort_keys=True, ensure_ascii=False, default=str) for r in result["records"]) + "\n", encoding="utf-8")
            print(f"records dumped to {a.json}")
        if a.write:
            n = append_records(a.registry, result["records"])
            print(f"WROTE {n} row(s) to {a.registry}")
        else:
            print(f"DRY RUN: {len(result['records'])} row(s) built, nothing written (pass --write to append to {a.registry})")
    finally:
        if not a.keep_harness and a.harness_root is None:
            shutil.rmtree(result["harness_root"], ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
