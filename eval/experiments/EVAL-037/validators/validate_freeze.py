#!/usr/bin/env python3
"""EVAL-037 — validate the frozen common substrate. Fails closed.

    python3 eval/experiments/EVAL-037/validators/validate_freeze.py
"""
import hashlib
import json
import os
import pathlib
import subprocess
import sys

import yaml

HERE = pathlib.Path(__file__).resolve().parent
PKG = HERE.parent
REPO = PKG.parents[2]
sys.path.insert(0, str(PKG / "tools"))
from jsonschema_mini import validate            # noqa: E402
import freeze_fingerprint as FF                 # noqa: E402

CANON_BASE = "c6f8d910f7a3cdaaeafa2280313abfb9b898cddd"
FULL_FP = "cbd321aa3be7464e785a0d42de1764cdccc8bdd33bc023a376740f8f196bde60"
QA_FP = "1313c0babe2194a7bc71c1628f9fbec5fa4f35ca5ff5edc7f594662101dc62bd"
BRIEFS = ["B01", "B02", "B03", "B04", "B05", "B06"]
WEB_BRIEFS = ["B01", "B02"]
NOWEB_BRIEFS = ["B03", "B04", "B05", "B06"]
LANES = ["sol-no-canon", "sol-full-canon", "sonnet-no-canon", "sonnet-full-canon",
         "haiku-no-canon", "haiku-full-canon", "gemma-no-canon", "gemma-full-canon"]
MODELS = {"sol": ("OpenAI", "gpt-5.6-sol"), "sonnet": ("Anthropic", "claude-sonnet-5"),
          "haiku": ("Anthropic", "claude-haiku-4-5-20251001"),
          "gemma": ("Google Gemini API", "gemma-4-31b-it")}
SECTIONS = ["DELIVERABLE", "OBJECTIVE_INTERPRETATION", "CORE_CREATIVE_IDEA",
            "MESSAGE_AND_INFORMATION_HIERARCHY", "VISUAL_SYSTEM", "PRODUCTION_RECIPE",
            "GENERATION_PROMPTS", "DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS",
            "AUDIO_AND_EDIT", "FAILURE_PREVENTION", "HARD_CONSTRAINT_CHECK",
            "KNOWLEDGE_AND_WEBSITE_USE"]
TRANSIENT = ["timeout", "connection_error", "rate_limit_429", "server_error_5xx"]
FAILURES = []


GATES = {"n": 0}


def gate(name, ok, detail=""):
    GATES["n"] += 1
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""))
    if not ok:
        FAILURES.append(name)
    return ok


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def order_key(t):
    return hashlib.sha256(("EVAL-037|" + t).encode()).hexdigest()


def canon_fps():
    import glob
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
        rows = [(p, sha(REPO / p)) for p in sorted(paths)]
        return hashlib.sha256("".join(f"{p}:{h}\n" for p, h in rows).encode()).hexdigest()

    return (fp(collect("canon/knowledge/current") + collect("canon/candidates/canon-014")),
            fp(sorted(str(pathlib.Path(p).relative_to(REPO))
                      for p in glob.glob(str(REPO / "canon/qa/canon-014/*-qa-bank.yaml")))))


def main():
    print("EVAL-037 freeze validation\n")
    lanes = {}
    for lid in LANES:
        p = PKG / "lanes" / f"{lid}.yaml"
        if p.exists():
            lanes[lid] = yaml.safe_load(p.read_text(encoding="utf-8"))

    # ---- F1  substrate identity is bytes, not a commit --------------------
    full, rows = FF.compute()
    common, crows = FF.compute_common()
    rec_full = FF._recorded("freeze_fingerprint")
    rec_common = FF._recorded("common_substrate_digest")
    gate("F1a freeze fingerprint recomputes and matches FREEZE-FINGERPRINT.yaml",
         rec_full == full, f"{full[:16]}… over {len(rows)} files")
    gate("F1b common substrate digest recomputes (lanes excluded, so non-circular)",
         rec_common == common, f"{common[:16]}… over {len(crows)} files")
    gate("F1c every lane embeds the common substrate digest",
         all(L["substrate"]["common_substrate_digest"] == common for L in lanes.values()))

    # Neither digest may appear inside the scope it covers — that is what makes both
    # of them verifiable rather than self-invalidating.
    inside = [rel for rel, _h in rows
              if full in (PKG / rel).read_text(encoding="utf-8", errors="ignore")]
    gate("F1d the freeze fingerprint appears in no file it covers (no self-reference)",
         not inside, f"found in {inside}" if inside else "")
    cinside = [rel for rel, _h in crows
               if common in (PKG / rel).read_text(encoding="utf-8", errors="ignore")]
    gate("F1e the common digest appears in no file it covers (lanes are outside it, "
         "so only lanes may embed it)", not cinside,
         f"found in {cinside}" if cinside else "")
    doc = (PKG / "EXECUTION-CONTRACT.md").read_text()
    gate("F1f EXECUTION-CONTRACT.md prints neither digest, and says why",
         full not in doc and common not in doc
         and "does not print either digest" in doc)

    # ---- F2  the canon base commit does NOT contain EVAL-037 --------------
    listed = subprocess.run(["git", "ls-tree", "-r", "--name-only", CANON_BASE,
                             "eval/experiments/"], cwd=REPO,
                            capture_output=True, text=True).stdout.strip()
    anc = subprocess.run(["git", "merge-base", "--is-ancestor", CANON_BASE, "HEAD"],
                         cwd=REPO, capture_output=True).returncode == 0
    gate("F2a canon_base_commit is an ancestor of HEAD (Canon provenance holds)", anc,
         CANON_BASE[:12])
    gate("F2b canon_base_commit does NOT contain EVAL-037, and nothing claims it does",
         listed == "", f"unexpectedly contains: {listed[:120]}" if listed else
         "verified empty at that commit")
    bad = []
    for lid, L in lanes.items():
        sub = L["substrate"]
        if "base_commit" in L or sub.get("canon_base_commit") != CANON_BASE:
            bad.append(lid)
        role = (sub.get("canon_base_commit_role") or "").lower()
        if "does not contain eval-037" not in role.replace("not contain eval-037",
                                                           "does not contain eval-037"):
            if "provenance" not in role:
                bad.append(lid)
    gate("F2c no lane calls it the execution starting commit; each states its real role",
         not bad, f"{sorted(set(bad))}" if bad else "")

    # ---- F3  Canon fingerprints -------------------------------------------
    f, q = canon_fps()
    gate("F3  Canon fingerprints recompute exactly", f == FULL_FP and q == QA_FP,
         f"full={f[:16]}… qa={q[:16]}…")

    # ---- F4  briefs, F5 prompt --------------------------------------------
    ok = True
    for b in BRIEFS:
        raw = (PKG / "common/briefs" / f"{b}.txt").read_bytes()
        ok &= raw.count(b"\n") == 1 and raw.endswith(b"\n") and len(raw) > 300
    gate("F4  six briefs present, single-line, byte-exact", ok)
    sp = (PKG / "common/system-prompt.txt").read_text(encoding="utf-8")
    gate("F5  common prompt carries all 12 package sections",
         all(s in sp for s in SECTIONS) and "FINAL_PRODUCTION_PACKAGE" in sp)

    # ---- F6  website snapshots + tool --------------------------------------
    man = yaml.safe_load((PKG / "common/websites/WEBSITE-SNAPSHOT-MANIFEST.yaml").read_text())
    hosts = {s["host"] for s in man["sites"]}
    dirs = {d.name for d in (PKG / "common/websites").iterdir() if d.is_dir()}
    dig_ok = all(sha(PKG / s["path"] / "index.html") == s["files"]["index.html"]["sha256"]
                 and sha(PKG / s["path"] / "page.txt") == s["files"]["page.txt"]["sha256"]
                 for s in man["sites"])
    gate("F6a exactly the two permitted snapshots, digests intact",
         hosts == {"rentok.com", "getaight.ai"} and dirs == hosts and dig_ok
         and man["live_browsing_permitted_during_trials"] is False)

    sys.path.insert(0, str(PKG / "tools"))
    import website_tools as WT
    gate("F6b website tool exposed for B01/B02 only",
         all(WT.schema_for(b) for b in WEB_BRIEFS)
         and all(WT.schema_for(b) is None for b in NOWEB_BRIEFS))
    same = WT.schema_for("B01")["input_schema"] == WT.TOOL_SCHEMA["input_schema"]
    gate("F6c the website tool has one schema, so it cannot differ by condition", same)
    ok = True
    for lid, L in lanes.items():
        w = L["website_tool"]
        ok &= (w["name"] == "website_read" and w["exposed_for_briefs"] == WEB_BRIEFS
               and w["not_exposed_for_briefs"] == NOWEB_BRIEFS
               and w["identical_across_conditions"] is True
               and w["live_browsing"] == "forbidden"
               and w["model_decides_whether_to_call"] is True)
    gate("F6d every lane declares the website tool identically, in both conditions", ok)
    try:
        WT.Website(PKG, "B03"); reach = True
    except WT.WebsiteAccessError:
        reach = False
    gate("F6e a no-website brief cannot construct the website tool at all", not reach)
    try:
        WT.Website(PKG, "B01").website_read(url="https://example.com"); leak = True
    except WT.WebsiteAccessError:
        leak = False
    gate("F6f any other domain is refused, not fetched", not leak)
    gate("F6g no fetch path exists in the website tool",
         not any(x in (PKG / "tools/website_tools.py").read_text()
                 for x in ("requests", "urllib", "httpx", "socket", "curl", "urlopen")))

    # ---- F7  lanes ---------------------------------------------------------
    gate("F7  all eight lane configs present and parse", len(lanes) == 8)

    all_ids = []
    for lid, L in lanes.items():
        plan = L["execution"]["trials_plan"]
        ids = [t["trial_id"] for t in plan]
        expected = sorted(
            [f"E037-{lid}-{b}-R{r}" for r in (1, 2, 3) for b in BRIEFS], key=order_key)
        per = all(sum(1 for t in plan if t["brief_id"] == b) == 3 for b in BRIEFS)
        gate(f"F8  {lid}: 18 trials in the recomputed SHA-256 order",
             len(ids) == 18 and len(set(ids)) == 18 and ids == expected and per
             and [t["order_index"] for t in plan] == list(range(1, 19)))
        all_ids += ids
    gate("F9  144 trials in total, every id globally unique",
         len(all_ids) == 144 and len(set(all_ids)) == 144, f"{len(all_ids)} trials")

    # the ordering must not be the old repetition-major one
    lid0 = "sonnet-full-canon"
    if lid0 in lanes:
        first6 = [t["brief_id"] for t in lanes[lid0]["execution"]["trials_plan"][:6]]
        gate("F10 the frozen order is the SHA-256 shuffle, not repetition-major",
             first6 != BRIEFS, f"first six briefs: {first6}")

    # ---- F11 condition isolation ------------------------------------------
    for lid, L in lanes.items():
        if L["condition"] != "NO_CANON":
            continue
        blob = (PKG / "lanes" / f"{lid}.yaml").read_text()
        leaks = [x for x in ("canon/knowledge/", "canon/candidates/", "canon/qa/",
                             FULL_FP, QA_FP) if x in blob]
        cd = L["condition_detail"]
        gate(f"F11 {lid}: no Canon content and no addendum",
             not leaks and cd["addendum_path"] is None and cd["canon_tools_exposed"] == []
             and cd["canon_instruction"] == "absent")

    for lid, L in lanes.items():
        if L["condition"] != "FULL_CANON":
            continue
        cd = L["condition_detail"]; f_ = cd["fingerprints"]
        gate(f"F12 {lid}: both fingerprints + three read-only Canon tools",
             f_["full_knowledge"]["combined_digest"] == FULL_FP
             and f_["qa"]["combined_digest"] == QA_FP
             and cd["canon_tools_exposed"] == ["canon_catalog", "canon_search", "canon_read"]
             and cd["mandatory_canon_use"] is False and cd["no_aggregate_top_k"] is True
             and f_["on_mismatch"] == "stop")

    # ---- F13 models, no aliases, no capability gate -------------------------
    ok = True
    for lid, L in lanes.items():
        m = L["model"]; prov, mid = MODELS[m["key"]]
        ok &= (m["provider"] == prov and m["model_id"] == mid
               and m["moving_alias"] is False
               and not any(a in mid for a in ("latest", "-preview", "@latest")))
    gate("F13 model roster exact, no moving aliases", ok)
    blob = (PKG / "tools/preflight.py").read_text() + \
           "".join((PKG / "lanes" / f"{lid}.yaml").read_text() for lid in lanes) + \
           (PKG / "EXECUTION-CONTRACT.md").read_text()
    claim = [x for x in ("historically not supported function calling",
                         "has historically not supported",
                         "cannot support function calling") if x in blob]
    gate("F14 the withdrawn Gemma capability claim/gate is gone everywhere", not claim,
         f"{claim}" if claim else "")
    gate("F15 preflight returns only 0 or 2 (no model-specific gate exit)",
         "return 3" not in (PKG / "tools/preflight.py").read_text())

    # ---- F16 retry policy ---------------------------------------------------
    ok = True
    for lid, L in lanes.items():
        r = L["retry_policy"]
        t, d, fr = r["transient_failure"], r["deterministic_failure"], r["format_repair"]
        ok &= (t["initial_attempt"] == 1 and t["max_technical_retries"] == 2
               and t["classes"] == TRANSIENT and d["retries"] == 0
               and d["status"] == "failed_execution"
               and "context_overflow" in d["classes"]
               and "tool_loop_guard_exhausted" in d["classes"]
               and fr["max"] == 1 and fr["scope"] == "format only"
               and "the original model answer, verbatim" in fr["request_contains"]
               and fr["records"] == "repair_source_response_digest"
               and fr["if_repair_still_invalid"]["status"] == "failed_format"
               and fr["if_repair_still_invalid"]["eligible_for_media_generation"] is False
               and any("creatively weak" in x for x in r["forbidden_retry_reasons"]))
    gate("F16 retry policy: transient-only retries, deterministic never resampled, "
         "one format repair carrying the original answer", ok)

    ok = all(L["tool_loop_guard"]["max_provider_turns"] == 100
             and L["tool_loop_guard"]["is_a_retrieval_budget"] is False
             for L in lanes.values())
    import providers as P
    gate("F17 tool-loop guard is 100 turns and is declared NOT a retrieval budget",
         ok and P.MAX_TOOL_TURNS == 100)
    gate("F18 transient/deterministic class split matches the lanes",
         sorted(P.TRANSIENT_CLASSES) == sorted(TRANSIENT)
         and "context_overflow" in P.DETERMINISTIC_CLASSES
         and "tool_loop_guard_exhausted" in P.DETERMINISTIC_CLASSES
         and "truncated_response" in P.DETERMINISTIC_CLASSES)

    # ---- F19 canon_search is ranked lexical retrieval, not regex ------------
    ct = (PKG / "tools/canon_tools.py").read_text()
    gate("F19 canon_search is deterministic BM25 over a real tokenizer, not regex",
         "BM25_K1" in ct and "def tokenize" in ct and "re.compile(query" not in ct
         and "_bm25_index" in ct)
    import canon_tools as CT
    kinds = set()
    c = CT.Canon(REPO, condition="FULL_CANON")
    for e in c._flatten():
        kinds.add(e["kind"])
    gate("F20 every item class is indexed, visual evidence included",
         kinds == {"knowledge", "concept_system", "binding", "ontology_term",
                   "ontology_concept", "qa", "visual_evidence"}, f"{sorted(kinds)}")

    # ---- F21 price snapshot -------------------------------------------------
    pr = yaml.safe_load((PKG / "common/price-snapshot.yaml").read_text())
    priced = {k: v for k, v in pr["models"].items() if v["input"] is not None}
    unpriced = [k for k, v in pr["models"].items() if v["input"] is None]
    gate("F21 price snapshot exists; unknown prices are null, never invented",
         set(pr["models"]) == {m[1] for m in MODELS.values()}
         and all(v.get("source") for v in priced.values())
         and all(pr["models"][k].get("source") is None for k in unpriced),
         f"priced={sorted(priced)} unpriced={sorted(unpriced)}")

    # ---- F22 schemas --------------------------------------------------------
    res_s = json.loads((PKG / "schemas/result.schema.json").read_text())
    good = _good_result()
    bad = json.loads(json.dumps(good)); bad["trials"] = bad["trials"][:17]
    gate("F22 schemas accept a good run and reject a 17-trial run",
         not validate(good, res_s) and validate(bad, res_s),
         "; ".join(validate(good, res_s)[:2]))

    # ---- F23 lane self-containment ------------------------------------------
    ok = True
    for lid in lanes:
        blob = (PKG / "lanes" / f"{lid}.yaml").read_text()
        others = [o for o in LANES if o != lid and (f"lanes/{o}" in blob or f"{o}.yaml" in blob)]
        if others:
            ok = False
            print(f"        {lid} names sibling lanes: {others}")
    gate("F23 every lane is self-contained (names no sibling lane)", ok)

    print()
    if FAILURES:
        print(f"FREEZE VALIDATION FAILED — {len(FAILURES)} gate(s): {', '.join(FAILURES)}")
        return 1
    print(f"FREEZE VALIDATION PASSED — all {GATES['n']} gates green")
    return 0


def _good_result():
    lid = "sonnet-full-canon"
    ids = sorted([f"E037-{lid}-{b}-R{r}" for r in (1, 2, 3) for b in BRIEFS], key=order_key)
    trials = []
    for i, tid in enumerate(ids, 1):
        b = tid.split("-")[-2]
        web = b in WEB_BRIEFS
        trials.append({
            "trial_id": tid, "brief_id": b, "brief_digest": "0" * 64,
            "repetition": int(tid.split("-R")[-1]), "order_index": i,
            "status": "complete", "attempts_used": 1, "transient_retries_used": 0,
            "format_repairs_used": 0, "repair_source_response_digest": None,
            "fresh_context": True, "package_path": f"packages/{tid}.txt",
            "package_digest": "0" * 64, "sections_present": SECTIONS,
            "eligible_for_media_generation": True, "canon_used": True,
            "canon_tool_calls": 2,
            "canon_items_returned": {"accepted": 3, "hold": 1, "qa": 0},
            "website_tool_exposed": web, "website_tool_calls": 1 if web else 0,
            "website_snapshot_used": web,
            "website_snapshot_digests": ["a" * 64] if web else [],
            "usage_totals": {"input_tokens": 10, "output_tokens": 5,
                             "provider_turns": 2, "latency_ms": 3},
            "price_snapshot": "eval-037-price-snapshot-v1",
            "calculated_cost_usd": 0.0001, "cost_basis": "computed",
            "wall_clock_ms": 10})
    return {"experiment": "EVAL-037", "lane_id": lid,
            "branch": f"work/eval-037-{lid}",
            "substrate": {"freeze_fingerprint": "b" * 64, "canon_base_commit": CANON_BASE,
                          "execution_commit": "c" * 40},
            "runner_commit": "d" * 40, "provider": "Anthropic", "model": "claude-sonnet-5",
            "condition": "FULL_CANON",
            "canon_fingerprints": {"full_knowledge": FULL_FP, "qa": QA_FP},
            "price_snapshot": "eval-037-price-snapshot-v1",
            "lane_usage_totals": {"input_tokens": 180, "output_tokens": 90,
                                  "provider_turns": 36, "latency_ms": 54},
            "lane_calculated_cost_usd": 0.002, "lane_cost_basis": "computed",
            "trial_count": 18, "trials": trials}


if __name__ == "__main__":
    sys.exit(main())
