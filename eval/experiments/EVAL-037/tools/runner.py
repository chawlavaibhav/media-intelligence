#!/usr/bin/env python3
"""EVAL-037 — the common lane runner.

One lane = one model x one condition x 18 trials, in one isolated execution session.

    python3 tools/runner.py --lane lanes/sonnet-full-canon.yaml
    python3 tools/runner.py --lane lanes/sonnet-full-canon.yaml --fake clean --out /tmp/x

WHAT THIS FILE ENFORCES

  * exactly 18 trials, in the lane's frozen (SHA-256 derived) order
  * a fresh stateless request per attempt; no state crosses a trial boundary
  * the substrate is identified by its FREEZE FINGERPRINT, not by a commit SHA. The
    Canon base commit is recorded separately, as Canon provenance.
  * retries only for TRANSIENT provider failures (max 2). Deterministic failures -
    bad request, context overflow, tool-loop guard, refusal, truncation - are recorded
    as execution failures and never resampled.
  * exactly one format repair, and the repair request CONTAINS the original answer
  * a transient failure during a repair retries THAT REPAIR, never a fresh generation
  * an invalid repair is `failed_format`, never `format_repaired`
  * every provider turn's usage/cost evidence retained, and summed to trial totals
  * the exact serialised request retained for every invocation, not only a digest
  * the complete tool transcript retained, with real arguments and per-item identity
  * every output retained; no creative judging; no media
"""
import argparse
import datetime as dt
import hashlib
import json
import pathlib
import subprocess
import sys
import time

import yaml

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = ROOT.parents[2]
sys.path.insert(0, str(HERE))

SECTIONS = ["DELIVERABLE", "OBJECTIVE_INTERPRETATION", "CORE_CREATIVE_IDEA",
            "MESSAGE_AND_INFORMATION_HIERARCHY", "VISUAL_SYSTEM", "PRODUCTION_RECIPE",
            "GENERATION_PROMPTS", "DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS",
            "AUDIO_AND_EDIT", "FAILURE_PREVENTION", "HARD_CONSTRAINT_CHECK",
            "KNOWLEDGE_AND_WEBSITE_USE"]

MAX_TRANSIENT_RETRIES = 2      # per phase (creative, then repair)
MAX_FORMAT_REPAIRS = 1

# Frozen. The repair carries the model's OWN prior answer back to it and asks only for
# the same substance in the required shape. It adds no creative guidance whatsoever.
FORMAT_REPAIR_TEMPLATE = (
    "Your previous response to the request above did not use the required output "
    "structure.\n\n"
    "--- BEGIN YOUR PREVIOUS RESPONSE ---\n"
    "{previous_response}\n"
    "--- END YOUR PREVIOUS RESPONSE ---\n\n"
    "Return that same answer again, unchanged in substance, using exactly the required "
    "FINAL_PRODUCTION_PACKAGE section headings. Do not add, remove, improve or "
    "reconsider any creative content. Change only the formatting."
)


def sha256_text(s):
    return hashlib.sha256(str(s).encode("utf-8")).hexdigest()


def sha256_file(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sections_present(text):
    """Mechanical presence check. Presence only — never a quality opinion."""
    return [s for s in SECTIONS if s in (text or "")]


def is_well_formed(text):
    return ("FINAL_PRODUCTION_PACKAGE" in (text or "")
            and len(sections_present(text)) == len(SECTIONS))


# --------------------------------------------------------------------------
def substrate_digests():
    import freeze_fingerprint as FF
    return {"freeze_fingerprint": FF.compute()[0],
            "common_substrate_digest": FF.compute_common()[0],
            "recorded_freeze_fingerprint": FF._recorded("freeze_fingerprint")}


def canon_fingerprints():
    """Recompute both corpus digests. Reads bytes only; never interprets content."""
    import glob
    import os
    arts = ["source-knowledge.yaml", "source-concept-systems.yaml",
            "operational-bindings.yaml", "ontology-mappings.yaml",
            "visual-evidence-ledger.yaml"]

    def collect(rel):
        out, base = [], REPO / rel
        for d in sorted(os.listdir(base)):
            if (base / d).is_dir():
                out += [f"{rel}/{d}/{a}" for a in arts if (base / d / a).is_file()]
        return out

    def fp(paths):
        rows = [(p, sha256_file(REPO / p)) for p in sorted(paths)]
        return hashlib.sha256("".join(f"{p}:{h}\n" for p, h in rows).encode()).hexdigest()

    return {"full_knowledge": fp(collect("canon/knowledge/current")
                                + collect("canon/candidates/canon-014")),
            "qa": fp(sorted(str(pathlib.Path(p).relative_to(REPO))
                            for p in glob.glob(str(REPO / "canon/qa/canon-014/*-qa-bank.yaml"))))}


def expected_trial_order(lane_id, trial_id_prefix=None):
    """Recompute the frozen order: sort trial ids by sha256('EVAL-037|' + trial_id).

    The ORDERING METHOD is unchanged and is the only thing frozen here. A lane may
    declare its own `trial_id_prefix` so a supplemental treatment can occupy a separate
    trial-id namespace; the ids then differ, so the resulting permutation differs, but
    it is derived by the identical rule. Absent a declared prefix this is bit-identical
    to the original `E037-<lane_id>` behaviour for every existing lane.
    """
    prefix = trial_id_prefix or f"E037-{lane_id}"
    ids = [f"{prefix}-{b}-R{r}"
           for r in (1, 2, 3) for b in ["B01", "B02", "B03", "B04", "B05", "B06"]]
    return sorted(ids, key=lambda t: sha256_text("EVAL-037|" + t))


def preflight(lane, fake=None):
    """Verify the substrate before the first call. Fails closed."""
    problems, notes = [], []

    # -- substrate identity: the BYTES are the authority, not a commit SHA --
    d = substrate_digests()
    want = lane["substrate"]["common_substrate_digest"]
    if d["common_substrate_digest"] != want:
        problems.append(f"common substrate digest mismatch — this checkout is not the "
                        f"approved frozen substrate.\n     lane expects {want}"
                        f"\n     computed     {d['common_substrate_digest']}")
    if d["recorded_freeze_fingerprint"] != d["freeze_fingerprint"]:
        problems.append(f"freeze fingerprint drift — FREEZE-FINGERPRINT.yaml records "
                        f"{d['recorded_freeze_fingerprint']} but the tree computes "
                        f"{d['freeze_fingerprint']}")
    notes.append(f"common substrate computed {d['common_substrate_digest'][:16]}… / "
                 f"lane expects {want[:16]}…")
    notes.append(f"freeze fingerprint {d['freeze_fingerprint'][:16]}… matches "
                 f"FREEZE-FINGERPRINT.yaml (controller-approved dispatch gate)")

    # -- Canon provenance: a separate fact, recorded separately -------------
    cbc = lane["substrate"]["canon_base_commit"]
    anc = subprocess.run(["git", "merge-base", "--is-ancestor", cbc, "HEAD"],
                         cwd=REPO, capture_output=True)
    if anc.returncode != 0:
        problems.append(f"canon_base_commit {cbc[:12]} is not an ancestor of HEAD; this "
                        f"checkout does not contain the Canon corpus the fingerprints "
                        f"were computed against")
    notes.append(f"canon base commit {cbc[:12]} is an ancestor of HEAD (Canon provenance)")

    got = sha256_file(ROOT / lane["prompt"]["system_prompt_path"])
    if got != lane["prompt"]["system_prompt_sha256"]:
        problems.append(f"system prompt digest mismatch: {got}")

    for bid, b in lane["briefs"].items():
        got = sha256_file(ROOT / b["path"])
        if got != b["sha256"]:
            problems.append(f"brief {bid} digest mismatch: {got}")
        site = b.get("website")
        if site:
            for k, dk in (("snapshot_html", "snapshot_html_sha256"),
                          ("snapshot_text", "snapshot_text_sha256")):
                got = sha256_file(ROOT / site[k])
                if got != site[dk]:
                    problems.append(f"{bid} {k} digest mismatch: {got}")

    if lane["condition"] == "FULL_CANON":
        fps = lane["condition_detail"]["fingerprints"]
        live = canon_fingerprints()
        if live["full_knowledge"] != fps["full_knowledge"]["combined_digest"]:
            problems.append(f"full-knowledge fingerprint mismatch: {live['full_knowledge']}")
        if live["qa"] != fps["qa"]["combined_digest"]:
            problems.append(f"Q&A fingerprint mismatch: {live['qa']}")
        notes.append(f"canon full_knowledge={live['full_knowledge'][:16]}… "
                     f"qa={live['qa'][:16]}…")

    plan = lane["execution"]["trials_plan"]
    ids = [t["trial_id"] for t in plan]
    if len(ids) != 18 or len(set(ids)) != 18:
        problems.append(f"trials_plan has {len(ids)} entries ({len(set(ids))} unique), "
                        f"expected 18 unique")
    expected = expected_trial_order(lane["lane_id"],
                                    lane["execution"].get("trial_id_prefix"))
    if ids != expected:
        problems.append("trial order does not match the frozen SHA-256 ordering")
    notes.append("trial order recomputed from sha256('EVAL-037|'+trial_id) and matches")

    if fake is None:
        dirty = subprocess.run(
            ["git", "status", "--porcelain", "--", str(HERE.relative_to(REPO))],
            cwd=REPO, capture_output=True, text=True).stdout.strip()
        if dirty:
            problems.append("runner tree is dirty: freeze and COMMIT the runner before "
                            f"the first experimental call.\n{dirty}")
        notes.append("model preflight is the worker's responsibility: confirm the EXACT "
                     "model id resolves before trial 1, and STOP rather than substitute.")
    else:
        notes.append(f"FAKE PROVIDER ({fake}) — no network, no spend, no experimental call")
    return problems, notes


# --------------------------------------------------------------------------
def load_prices():
    return yaml.safe_load((ROOT / "common/price-snapshot.yaml").read_text(encoding="utf-8"))


def cost_for(prices, model_id, inp, out):
    """Cost from the frozen price snapshot, or null with a stated reason. Never guessed."""
    m = (prices.get("models") or {}).get(model_id)
    if m is None:
        return None, f"no price entry for {model_id} in {prices['snapshot_id']}"
    if m.get("input") is None or m.get("output") is None:
        return None, f"price not established for {model_id} at freeze time"
    if inp is None or out is None:
        return None, "provider did not report both input and output token counts"
    return round(inp / 1e6 * m["input"] + out / 1e6 * m["output"], 8), "computed"


def sum_usage(turns):
    """Sum across EVERY provider turn, including intermediate tool turns.

    A field no turn reported stays null. A field some turns reported is summed over
    exactly those turns, and `*_turns_reporting` says how many that was, so a partial
    sum can never be mistaken for a complete one.
    """
    out = {}
    for f in ("input_tokens", "cached_input_tokens", "output_tokens", "reasoning_tokens"):
        vals = [t[f] for t in turns if t.get(f) is not None]
        out[f] = sum(vals) if vals else None
        out[f + "_turns_reporting"] = len(vals)
    out["provider_turns"] = len(turns)
    out["latency_ms"] = sum(t.get("latency_ms") or 0 for t in turns)
    return out


# --------------------------------------------------------------------------
def build_tools(lane, brief_id):
    """Tools for this trial. Website access depends on the BRIEF, Canon on the CONDITION."""
    import website_tools
    schemas, canon, site = [], None, None

    if lane["condition"] == "FULL_CANON":
        import canon_tools
        canon = canon_tools.Canon(REPO, condition="FULL_CANON")
        schemas += canon_tools.TOOL_SCHEMAS

    ws = website_tools.schema_for(brief_id)
    if ws:
        site = website_tools.Website(ROOT, brief_id)
        schemas.append(ws)

    def dispatch(name, args):
        if name == website_tools.TOOL_NAME:
            return website_tools.dispatch(site, name, args)
        if canon is None:
            raise ValueError(f"tool {name!r} is not exposed in this condition")
        import canon_tools as CT
        return CT.dispatch(canon, name, args)

    return schemas, dispatch if schemas else None


def system_prompt_for(lane):
    text = (ROOT / lane["prompt"]["system_prompt_path"]).read_text(encoding="utf-8")
    if lane["condition"] == "FULL_CANON":
        cond = yaml.safe_load(
            (ROOT / lane["condition_detail"]["addendum_path"]).read_text(encoding="utf-8"))
        text = (text.rstrip("\n") + "\n\n"
                + cond[lane["condition_detail"]["addendum_key"]].rstrip("\n") + "\n")
    return text


def make_adapter(lane, schemas, fake, fake_target):
    mk, mid = lane["model"]["key"], lane["model"]["model_id"]
    if fake:
        from fake_provider import FakeAdapter
        return FakeAdapter(mid, schemas, scenario=fake, target_trial=fake_target,
                           model_key=mk, provider=lane["model"]["provider"])
    from providers import ADAPTERS
    return ADAPTERS[mk](mid, schemas)


# --------------------------------------------------------------------------
def run_trial(trial, lane, system_prompt, outdir, fake, fake_target, prices):
    """One trial: creative phase, then at most one format-repair phase."""
    import providers as P

    brief_path = ROOT / trial["brief_path"]
    brief = brief_path.read_text(encoding="utf-8")
    schemas, dispatch = build_tools(lane, trial["brief_id"])
    adapter = make_adapter(lane, schemas, fake, fake_target)

    attempts, all_turns, all_tools = [], [], []
    transient_retries = {"creative": 0, "repair": 0}
    repairs = 0
    status = package = package_path = None
    repair_source_digest = None
    last_text = None
    t0 = time.time()
    idx = 0
    phase = "creative"

    while True:
        if phase == "creative":
            # The brief, and only the brief. Nothing else is ever added here.
            user = brief
            kind = "initial" if idx == 0 else "technical_retry"
        else:
            # The repair request carries the ORIGINAL brief and the model's OWN prior
            # answer, plus exactly the frozen format-only instruction. No other trial
            # and no new creative guidance ever appears here.
            user = brief + "\n\n" + FORMAT_REPAIR_TEMPLATE.format(previous_response=last_text)
            already = any(a["attempt_kind"].startswith("format_repair") for a in attempts)
            kind = "format_repair_technical_retry" if already else "format_repair"

        request = adapter.build_request(system_prompt, user)
        req_path = outdir / "requests" / f"{trial['trial_id']}-a{idx}.request.json"
        req_path.parent.mkdir(parents=True, exist_ok=True)
        req_path.write_text(json.dumps(request, indent=2, default=str), encoding="utf-8")

        row = {"trial_id": trial["trial_id"], "brief_id": trial["brief_id"],
               "repetition": trial["repetition"], "attempt_index": idx,
               "attempt_kind": kind, "phase": phase, "started_at": now(),
               "fresh_context": True,
               "request_digest": adapter.request_digest(request),
               "request_path": str(req_path.relative_to(outdir))}
        if phase == "repair":
            row["repair_source_response_digest"] = repair_source_digest

        try:
            kw = {"dispatch": dispatch}
            if fake:
                kw.update(trial_id=trial["trial_id"], attempt=idx, phase=phase)
            resp = adapter.call(request, **kw)
        except Exception as e:  # noqa: BLE001 — classified, never blanket-retried
            fc = getattr(e, "failure_class", None) or P.classify_exception(e)
            turns = (getattr(e, "detail", {}) or {}).get("turns", [])
            all_turns += turns
            row.update(ended_at=now(),
                       outcome="transient_failure" if P.is_transient(fc)
                       else "deterministic_failure",
                       failure_class=fc, failure_is_transient=P.is_transient(fc),
                       error=str(e)[:600], provider_turns=turns,
                       usage=sum_usage(turns) if turns else None)
            attempts.append(row)
            if P.is_transient(fc) and transient_retries[phase] < MAX_TRANSIENT_RETRIES:
                transient_retries[phase] += 1
                idx += 1
                continue                       # retries THIS phase's request, unchanged
            # Either the transient budget is exhausted, or this is a deterministic
            # failure that must never be resampled.
            status = ("failed_technical" if P.is_transient(fc) else "failed_execution")
            break

        text = resp["text"]
        turns = resp.get("turns", [])
        all_turns += turns
        tools = resp.get("tool_calls", [])

        # Full tool transcript: real arguments, per-item identity, full result.
        tref = None
        if tools:
            tpath = outdir / "transcripts" / f"{trial['trial_id']}-a{idx}.jsonl"
            tpath.parent.mkdir(parents=True, exist_ok=True)
            with open(tpath, "w", encoding="utf-8") as fh:
                for n, tc in enumerate(tools):
                    full = tc.pop("_full_result", None)
                    tc["transcript_ref"] = f"{tpath.relative_to(outdir)}#{n}"
                    fh.write(json.dumps({"line": n, "call": tc, "full_result": full},
                                        default=str) + "\n")
            tref = str(tpath.relative_to(outdir))
        all_tools += tools

        resp_path = outdir / "raw" / f"{trial['trial_id']}-a{idx}.response.json"
        resp_path.parent.mkdir(parents=True, exist_ok=True)
        resp_path.write_text(json.dumps(resp["raw"], indent=2, default=str), encoding="utf-8")

        usage = sum_usage(turns)
        cost, basis = cost_for(prices, lane["model"]["model_id"],
                               usage["input_tokens"], usage["output_tokens"])
        row.update(ended_at=now(), response_digest=sha256_text(text),
                   raw_response_path=str(resp_path.relative_to(outdir)),
                   transcript_path=tref, provider_turns=turns, usage=usage,
                   price_snapshot=prices["snapshot_id"],
                   calculated_cost_usd=cost, cost_basis=basis,
                   tool_calls=[{k: v for k, v in tc.items() if k != "_full_result"}
                               for tc in tools],
                   website_reads=[tc["snapshot_sha256"] for tc in tools
                                  if tc.get("tool_family") == "website"])

        if is_well_formed(text):
            row["outcome"] = "ok"
            attempts.append(row)
            package = text
            status = "format_repaired" if repairs else "complete"
            break

        row["outcome"] = "format_invalid"
        row["note"] = "required section structure absent — mechanical check only"
        attempts.append(row)
        last_text = text

        if repairs < MAX_FORMAT_REPAIRS:
            repairs += 1
            repair_source_digest = sha256_text(text)
            phase = "repair"
            idx += 1
            continue

        # The one permitted repair already ran and the answer is STILL invalid.
        # Retain it, mark failed_format, and do not call it repaired.
        package = text
        status = "failed_format"
        break

    if package is not None:
        package_path = outdir / "packages" / f"{trial['trial_id']}.txt"
        package_path.parent.mkdir(parents=True, exist_ok=True)
        package_path.write_text(package, encoding="utf-8")

    totals = sum_usage(all_turns)
    tcost, tbasis = cost_for(prices, lane["model"]["model_id"],
                             totals["input_tokens"], totals["output_tokens"])
    canon_calls = [t for t in all_tools if t.get("tool_family") == "canon"]
    web_calls = [t for t in all_tools if t.get("tool_family") == "website"]

    # -- REQUIRED_CANON treatment gate -------------------------------------
    # Mechanical, and evaluated ONLY from evidence already collected. It issues no
    # further provider call: a trial that ignored the mandatory instruction keeps its
    # output and is recorded as `failed_required_canon_use`. It is never quality-
    # retried and never resampled — that would select on behaviour and destroy the
    # comparison. `canon_catalog` alone is deliberately NOT Canon use: the treatment
    # requires a search the model composed and an object the model chose to read.
    n_search = sum(1 for t in canon_calls if t.get("name") == "canon_search")
    n_read = sum(1 for t in canon_calls if t.get("name") == "canon_read")
    n_catalog = sum(1 for t in canon_calls if t.get("name") == "canon_catalog")
    treatment = (lane.get("treatment") or {}).get("id")
    required_canon = treatment == "REQUIRED_CANON"
    canon_satisfied = n_search >= 1 and n_read >= 1
    format_outcome = status
    if required_canon and not canon_satisfied:
        status = "failed_required_canon_use"

    eligible = package is not None and status in ("complete", "format_repaired")

    result = {
        "trial_id": trial["trial_id"], "brief_id": trial["brief_id"],
        "brief_digest": sha256_file(brief_path), "repetition": trial["repetition"],
        "order_index": trial["order_index"], "status": status,
        "attempts_used": len(attempts),
        "transient_retries_used": transient_retries["creative"] + transient_retries["repair"],
        "format_repairs_used": repairs,
        "repair_source_response_digest": repair_source_digest,
        "fresh_context": True,
        "package_path": str(package_path.relative_to(outdir)) if package_path else None,
        "package_digest": sha256_text(package) if package else None,
        "sections_present": sections_present(package) if package else [],
        "eligible_for_media_generation": eligible,
        "treatment": treatment,
        "format_outcome": format_outcome,
        "required_canon_use_satisfied": (canon_satisfied if required_canon else None),
        "canon_used": (bool(canon_calls) if lane["condition"] == "FULL_CANON" else None),
        "canon_tool_calls": len(canon_calls),
        "canon_search_calls": n_search,
        "canon_read_calls": n_read,
        "canon_catalog_calls": n_catalog,
        "canon_items_returned": {
            "accepted": sum(t.get("accepted_items", 0) for t in canon_calls),
            "hold": sum(t.get("hold_items", 0) for t in canon_calls),
            "qa": sum(t.get("qa_items", 0) for t in canon_calls)},
        "website_tool_exposed": any(s["name"] == "website_read" for s in schemas),
        "website_tool_calls": len(web_calls),
        "website_snapshot_used": bool(web_calls),
        "website_snapshot_digests": sorted({t["snapshot_sha256"] for t in web_calls}),
        "usage_totals": totals,
        "price_snapshot": prices["snapshot_id"],
        "calculated_cost_usd": tcost,
        "cost_basis": tbasis,
        "wall_clock_ms": int((time.time() - t0) * 1000),
    }
    return result, attempts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--fake", default=None,
                    help="run against the fake provider (no network, no spend)")
    ap.add_argument("--fake-target", default=None)
    ap.add_argument("--preflight-only", action="store_true")
    a = ap.parse_args()

    lane = yaml.safe_load(pathlib.Path(a.lane).read_text(encoding="utf-8"))
    problems, notes = preflight(lane, fake=a.fake)
    for n in notes:
        print(f"  note: {n}")
    if problems:
        for p in problems:
            print(f"  PREFLIGHT FAIL: {p}", file=sys.stderr)
        print("STOPPING. Do not substitute anything. Escalate.", file=sys.stderr)
        return 2
    print("preflight OK")
    if a.preflight_only:
        return 0

    outdir = pathlib.Path(a.out) if a.out else (REPO / lane["evidence"]["root"])
    outdir.mkdir(parents=True, exist_ok=True)
    system_prompt = system_prompt_for(lane)
    prices = load_prices()
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                          capture_output=True, text=True).stdout.strip()

    trials, all_attempts = [], []
    for trial in lane["execution"]["trials_plan"]:
        res, atts = run_trial(trial, lane, system_prompt, outdir, a.fake, a.fake_target, prices)
        trials.append(res); all_attempts += atts
        print(f"  [{res['order_index']:2d}/18] {res['trial_id']}  {res['status']}  "
              f"attempts={res['attempts_used']}  turns={res['usage_totals']['provider_turns']}"
              f"  web={res['website_tool_calls']}  canon={res['canon_tool_calls']}"
              f" (search={res['canon_search_calls']} read={res['canon_read_calls']})")

    # Substrate identity recorded into the evidence: the freeze fingerprint is
    # COMPUTED from the tree that actually ran (preflight already proved it matches
    # the approved record), the canon base commit is provenance, and the execution
    # commit is simply where this lane ran. None of the three is the "starting commit".
    identity = {"freeze_fingerprint": substrate_digests()["freeze_fingerprint"],
                "canon_base_commit": lane["substrate"]["canon_base_commit"],
                "execution_commit": head}
    treatment_id = (lane.get("treatment") or {}).get("id")
    ledger = {"experiment": "EVAL-037", "lane_id": lane["lane_id"], "branch": lane["branch"],
              "substrate": identity, "runner_commit": head,
              "model": lane["model"]["model_id"], "condition": lane["condition"],
              "treatment": treatment_id,
              "attempts": all_attempts}

    lane_turns = [t for a_ in all_attempts for t in (a_.get("provider_turns") or [])]
    lane_totals = sum_usage(lane_turns)
    lcost, lbasis = cost_for(prices, lane["model"]["model_id"],
                             lane_totals["input_tokens"], lane_totals["output_tokens"])
    result = {"experiment": "EVAL-037", "lane_id": lane["lane_id"], "branch": lane["branch"],
              "substrate": identity, "runner_commit": head,
              "provider": lane["model"]["provider"], "model": lane["model"]["model_id"],
              "condition": lane["condition"], "treatment": treatment_id,
              "trial_count": len(trials),
              "price_snapshot": prices["snapshot_id"],
              "lane_usage_totals": lane_totals,
              "lane_calculated_cost_usd": lcost, "lane_cost_basis": lbasis,
              "trials": trials}
    if lane["condition"] == "FULL_CANON":
        fps = lane["condition_detail"]["fingerprints"]
        result["canon_fingerprints"] = {
            "full_knowledge": fps["full_knowledge"]["combined_digest"],
            "qa": fps["qa"]["combined_digest"]}

    (outdir / "attempt-ledger.json").write_text(json.dumps(ledger, indent=2, default=str))
    (outdir / "result.json").write_text(json.dumps(result, indent=2, default=str))
    print(f"wrote {outdir}/attempt-ledger.json and {outdir}/result.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
