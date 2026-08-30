#!/usr/bin/env python3
"""EVAL-037 — behavioural tests. Zero network, zero spend, zero experimental calls.

Mostly NEGATIVE tests: each breaks exactly one rule and asserts the substrate rejects
it. A validator that only accepts is not a validator.

    python3 validators/test_substrate.py
"""
import copy
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

import yaml

HERE = pathlib.Path(__file__).resolve().parent
PKG = HERE.parent
REPO = PKG.parents[2]
sys.path.insert(0, str(PKG / "tools"))

from jsonschema_mini import validate                                  # noqa: E402
import canon_tools                                                    # noqa: E402
from canon_tools import Canon, CanonStatusError, ACCEPTED, HOLD       # noqa: E402
import website_tools as WT                                            # noqa: E402
import providers as P                                                 # noqa: E402
import runner as R                                                    # noqa: E402

RESULT_SCHEMA = json.loads((PKG / "schemas/result.schema.json").read_text())
LEDGER_SCHEMA = json.loads((PKG / "schemas/attempt-ledger.schema.json").read_text())
PASSED, FAILED = [], []


def check(name, ok, detail=""):
    (PASSED if ok else FAILED).append(name)
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""))


def run_lane(lane, scenario, target=None):
    out = pathlib.Path(tempfile.mkdtemp())
    cmd = [sys.executable, str(PKG / "tools/runner.py"), "--lane", str(PKG / "lanes" / lane),
           "--fake", scenario, "--out", str(out)]
    if target:
        cmd += ["--fake-target", target]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO)
    if p.returncode != 0:
        raise AssertionError(f"runner failed: {p.stderr[-900:]}")
    return (json.loads((out / "result.json").read_text()),
            json.loads((out / "attempt-ledger.json").read_text()), out)


def order_key(t):
    return hashlib.sha256(("EVAL-037|" + t).encode()).hexdigest()


# ========================================================================== #
def t_clean():
    r, l, out = run_lane("sonnet-no-canon.yaml", "clean")
    check("T01 clean run produces exactly 18 trials",
          r["trial_count"] == 18 and len(r["trials"]) == 18)
    check("T02 clean run: every trial complete on the first attempt",
          all(t["status"] == "complete" and t["attempts_used"] == 1 for t in r["trials"]))
    check("T03 clean result validates", not validate(r, RESULT_SCHEMA),
          "; ".join(validate(r, RESULT_SCHEMA)[:2]))
    check("T04 clean ledger validates", not validate(l, LEDGER_SCHEMA),
          "; ".join(validate(l, LEDGER_SCHEMA)[:2]))
    shutil.rmtree(out, ignore_errors=True)


def t_trial_order():
    """Correction 6 — the order must RECOMPUTE, not merely run 1..18."""
    for lid in ("sonnet-full-canon", "gemma-no-canon"):
        L = yaml.safe_load((PKG / f"lanes/{lid}.yaml").read_text())
        ids = [t["trial_id"] for t in L["execution"]["trials_plan"]]
        expected = sorted(
            [f"E037-{lid}-{b}-R{r}" for r in (1, 2, 3)
             for b in ["B01", "B02", "B03", "B04", "B05", "B06"]], key=order_key)
        check(f"T05 {lid}: frozen order recomputes from sha256('EVAL-037|'+id)",
              ids == expected)
    L = yaml.safe_load((PKG / "lanes/sonnet-full-canon.yaml").read_text())
    first6 = [t["brief_id"] for t in L["execution"]["trials_plan"][:6]]
    check("T06 the order is a real shuffle, not repetition-major",
          first6 != ["B01", "B02", "B03", "B04", "B05", "B06"], f"{first6}")
    # a plain 1..18 check would pass for ANY ordering — prove the validator is stronger
    shuffled = copy.deepcopy(L)
    tp = shuffled["execution"]["trials_plan"]
    tp[0], tp[1] = tp[1], tp[0]
    for i, t in enumerate(tp, 1):
        t["order_index"] = i
    tmp = pathlib.Path(tempfile.mkdtemp()) / "bad.yaml"
    tmp.write_text(yaml.safe_dump(shuffled, sort_keys=False))
    p = subprocess.run([sys.executable, str(PKG / "tools/runner.py"), "--lane", str(tmp),
                        "--fake", "clean", "--preflight-only"],
                       capture_output=True, text=True, cwd=REPO)
    check("T07 a reordered plan with tidy order_index 1..18 is still REJECTED",
          p.returncode != 0 and "SHA-256" in (p.stderr + p.stdout).replace(
              "frozen SHA-256 ordering", "SHA-256"))
    shutil.rmtree(tmp.parent, ignore_errors=True)


def t_website_tool():
    """Correction 1 — reachable in BOTH conditions for B01/B02 only."""
    rn, ln, on = run_lane("sonnet-no-canon.yaml", "website_user")
    rf, lf, of = run_lane("sonnet-full-canon.yaml", "website_user")
    for tag, r in (("NO_CANON", rn), ("FULL_CANON", rf)):
        web = [t for t in r["trials"] if t["brief_id"] in ("B01", "B02")]
        noweb = [t for t in r["trials"] if t["brief_id"] not in ("B01", "B02")]
        check(f"T08 {tag}: B01/B02 reach the website tool",
              all(t["website_tool_exposed"] and t["website_snapshot_used"]
                  and t["website_tool_calls"] == 1 for t in web), f"{len(web)} trials")
        check(f"T09 {tag}: B03–B06 cannot access any website",
              all(not t["website_tool_exposed"] and not t["website_snapshot_used"]
                  and t["website_tool_calls"] == 0 for t in noweb))
    dn = {t["brief_id"]: t["website_snapshot_digests"] for t in rn["trials"]
          if t["website_snapshot_digests"]}
    df = {t["brief_id"]: t["website_snapshot_digests"] for t in rf["trials"]
          if t["website_snapshot_digests"]}
    check("T10 website BYTES are identical across conditions", dn == df and bool(dn), f"{dn}")
    calls = [tc for at in ln["attempts"] for tc in (at.get("tool_calls") or [])
             if tc.get("tool_family") == "website"]
    check("T11 every website call records name, arguments and the exact snapshot digest",
          bool(calls) and all(tc["name"] == "website_read" and isinstance(tc["arguments"], dict)
                              and len(tc["snapshot_sha256"]) == 64 for tc in calls))
    check("T12 website_snapshot_used is derived, never hardcoded false",
          any(t["website_snapshot_used"] for t in rn["trials"])
          and "website_snapshot_used\": False" not in (PKG / "tools/runner.py").read_text()
          and '"website_snapshot_used": False' not in (PKG / "tools/runner.py").read_text())
    try:
        WT.Website(PKG, "B04"); reach = True
    except WT.WebsiteAccessError:
        reach = False
    check("T13 a no-website brief cannot construct the tool at all", not reach)
    try:
        WT.Website(PKG, "B01").website_read(url="https://evil.example"); leak = True
    except WT.WebsiteAccessError:
        leak = False
    check("T14 another domain is refused, not fetched", not leak)
    out = WT.Website(PKG, "B01").website_read()
    man = yaml.safe_load((PKG / "common/websites/WEBSITE-SNAPSHOT-MANIFEST.yaml").read_text())
    sealed = {s["files"]["page.txt"]["sha256"] for s in man["sites"]}
    check("T15 website_read returns the sealed bytes, the digest and the source URL",
          out["snapshot_sha256"] in sealed and out["source_url"] == "https://rentok.com"
          and out["live_browsing"] is False and out["content_chars"] > 1000)
    for o in (on, of, ln, lf):
        pass
    shutil.rmtree(on, ignore_errors=True); shutil.rmtree(of, ignore_errors=True)


def t_website_drift():
    """A snapshot that no longer matches its sealed digest must not be served."""
    tmp = pathlib.Path(tempfile.mkdtemp())
    shutil.copytree(PKG / "common", tmp / "common")
    p = tmp / "common/websites/rentok.com/page.txt"
    p.write_text(p.read_text() + "\ntampered\n")
    try:
        WT.Website(tmp, "B01").website_read(); served = True
    except WT.WebsiteAccessError:
        served = False
    check("T16 altered snapshot bytes are REFUSED rather than served", not served)
    shutil.rmtree(tmp, ignore_errors=True)


def t_format_repair():
    """Correction 2 — the repair must carry the original answer."""
    T = "E037-sonnet-no-canon-B05-R1"
    r, l, out = run_lane("sonnet-no-canon.yaml", "malformed", T)
    t = next(x for x in r["trials"] if x["trial_id"] == T)
    atts = sorted((a for a in l["attempts"] if a["trial_id"] == T),
                  key=lambda x: x["attempt_index"])
    check("T17 a malformed answer triggers exactly one format repair",
          t["status"] == "format_repaired" and t["format_repairs_used"] == 1
          and len(atts) == 2 and atts[1]["attempt_kind"] == "format_repair")
    req = json.loads((out / atts[1]["request_path"]).read_text())
    body = req["messages"][0]["content"]
    brief = (PKG / "common/briefs/B05.txt").read_text()
    check("T18 the repair request contains the ORIGINAL BRIEF", brief.strip() in body)
    check("T19 the repair request contains the ORIGINAL MODEL ANSWER",
          "Here are three concepts you could consider" in body
          and "BEGIN YOUR PREVIOUS RESPONSE" in body)
    check("T20 the repair request contains exactly the frozen format-only instruction",
          "Do not add, remove, improve or reconsider any creative content" in body
          and "unchanged in substance" in body)
    check("T21 the repair exposes no other trial and no new creative guidance",
          "E037-" not in body and "concept" not in
          R.FORMAT_REPAIR_TEMPLATE.replace("{previous_response}", ""))
    check("T22 repair_source_response_digest matches the answer being repaired",
          atts[1]["repair_source_response_digest"] == atts[0]["response_digest"]
          and t["repair_source_response_digest"] == atts[0]["response_digest"])
    check("T23 the malformed output is retained, not discarded",
          atts[0]["outcome"] == "format_invalid" and (out / atts[0]["raw_response_path"]).exists())
    shutil.rmtree(out, ignore_errors=True)


def t_failed_format():
    T = "E037-sonnet-no-canon-B05-R1"
    r, l, out = run_lane("sonnet-no-canon.yaml", "always_malformed", T)
    t = next(x for x in r["trials"] if x["trial_id"] == T)
    check("T24 a still-invalid repair becomes failed_format, NOT format_repaired",
          t["status"] == "failed_format")
    check("T25 failed_format retains its output but is not eligible",
          t["package_path"] is not None and (out / t["package_path"]).exists()
          and t["eligible_for_media_generation"] is False)
    check("T26 failed_format uses exactly one repair and does not resample",
          t["format_repairs_used"] == 1 and t["attempts_used"] == 2)
    bad = copy.deepcopy(r)
    bt = next(x for x in bad["trials"] if x["trial_id"] == T)
    bt["status"] = "format_repaired"
    check("T27 the schema REJECTS calling an ineligible repair 'format_repaired'",
          bool(validate(bad, RESULT_SCHEMA)))
    shutil.rmtree(out, ignore_errors=True)


def t_repair_transient():
    T = "E037-sonnet-no-canon-B05-R1"
    r, l, out = run_lane("sonnet-no-canon.yaml", "repair_flaky", T)
    t = next(x for x in r["trials"] if x["trial_id"] == T)
    atts = sorted((a for a in l["attempts"] if a["trial_id"] == T),
                  key=lambda x: x["attempt_index"])
    kinds = [a["attempt_kind"] for a in atts]
    check("T28 a transient failure during a repair retries THAT repair",
          kinds == ["initial", "format_repair", "format_repair_technical_retry"])
    reqs = {a["attempt_index"]: json.loads((out / a["request_path"]).read_text())
            for a in atts}
    check("T29 the repair retry never falls back to a fresh creative generation",
          "BEGIN YOUR PREVIOUS RESPONSE" in reqs[2]["messages"][0]["content"]
          and reqs[1]["messages"][0]["content"] == reqs[2]["messages"][0]["content"])
    check("T30 the repaired trial still uses only ONE format repair",
          t["format_repairs_used"] == 1 and t["status"] == "format_repaired")
    shutil.rmtree(out, ignore_errors=True)


def t_failure_classification():
    """Corrections 8 and 9."""
    T = "E037-sonnet-no-canon-B01-R1"
    cases = [("flaky", "complete", 2, 1), ("hard_fail", "failed_technical", 3, 2),
             ("deterministic_fail", "failed_execution", 1, 0),
             ("context_overflow", "failed_execution", 1, 0),
             ("loop_guard", "failed_execution", 1, 0),
             ("truncated", "failed_execution", 1, 0)]
    for scen, status, attempts, retries in cases:
        r, l, out = run_lane("sonnet-no-canon.yaml", scen, T)
        t = next(x for x in r["trials"] if x["trial_id"] == T)
        check(f"T31 {scen}: status={status}, attempts={attempts}, retries={retries}",
              t["status"] == status and t["attempts_used"] == attempts
              and t["transient_retries_used"] == retries,
              f"got {t['status']}/{t['attempts_used']}/{t['transient_retries_used']}")
        shutil.rmtree(out, ignore_errors=True)

    check("T32 context overflow is deterministic, never a transient retry class",
          "context_overflow" in P.DETERMINISTIC_CLASSES
          and not P.is_transient("context_overflow"))
    check("T33 tool-loop exhaustion is deterministic, never a transient retry class",
          "tool_loop_guard_exhausted" in P.DETERMINISTIC_CLASSES
          and not P.is_transient("tool_loop_guard_exhausted"))
    check("T34 the transient set is exactly timeout/connection/429/5xx",
          P.TRANSIENT_CLASSES == {"timeout", "connection_error", "rate_limit_429",
                                  "server_error_5xx"})

    class E(Exception):
        pass
    for status, want in ((429, "rate_limit_429"), (503, "server_error_5xx"),
                         (400, "invalid_request_4xx"), (401, "auth_error")):
        e = E("x"); e.status_code = status
        check(f"T35 HTTP {status} classifies as {want}", P.classify_exception(e) == want)
    e = E("prompt is too long for the context window"); e.status_code = 400
    check("T36 a 400 naming the context window is context_overflow, not a retry",
          P.classify_exception(e) == "context_overflow"
          and not P.is_transient(P.classify_exception(e)))
    check("T37 an unrecognised error defaults to DETERMINISTIC (no free resample)",
          not P.is_transient(P.classify_exception(E("something odd"))))
    check("T38 truncation is detected from the provider stop reason",
          P.check_stop_reason({"stop_reason": "max_tokens"}) == "truncated_response"
          and P.check_stop_reason({"stop_reason": "refusal"}) == "model_refusal"
          and P.check_stop_reason({"stop_reason": "end_turn"}) is None)
    check("T39 the tool-loop guard is 100 turns and is not a retrieval budget",
          P.MAX_TOOL_TURNS == 100
          and "NOT a retrieval budget" in (PKG / "tools/providers.py").read_text())


def t_usage():
    """Correction 3 — usage summed over EVERY provider turn."""
    r, l, out = run_lane("sonnet-full-canon.yaml", "tool_user")
    by = {}
    for at in l["attempts"]:
        by.setdefault(at["trial_id"], []).append(at)
    ok = True
    for t in r["trials"]:
        turns = [tn for at in by[t["trial_id"]] for tn in (at.get("provider_turns") or [])]
        ok &= t["usage_totals"]["provider_turns"] == len(turns)
        for f in ("input_tokens", "output_tokens", "reasoning_tokens", "cached_input_tokens"):
            vals = [tn[f] for tn in turns if tn.get(f) is not None]
            ok &= t["usage_totals"][f] == (sum(vals) if vals else None)
    check("T40 trial usage totals equal the sum over ALL provider turns", ok)
    canon = [t for t in r["trials"] if t["canon_tool_calls"] > 0]
    check("T41 Canon retrieval turns are counted, not just the final response",
          all(t["usage_totals"]["provider_turns"] > 1 for t in canon), f"{len(canon)} trials")
    b01 = next(t for t in r["trials"] if t["brief_id"] == "B01")
    b03 = next(t for t in r["trials"] if t["brief_id"] == "B03")
    check("T42 a trial with an extra website turn records more turns than one without",
          b01["usage_totals"]["provider_turns"] > b03["usage_totals"]["provider_turns"],
          f"{b01['usage_totals']['provider_turns']} vs {b03['usage_totals']['provider_turns']}")
    turn = l["attempts"][0]["provider_turns"][0]
    for f in ("provider_model_version", "provider_request_id", "input_tokens",
              "cached_input_tokens", "output_tokens", "reasoning_tokens",
              "stop_reason", "latency_ms", "provider_reported_usage"):
        check(f"T43 every provider turn records {f}", f in turn)
    check("T44 lane totals aggregate every attempt's turns",
          r["lane_usage_totals"]["provider_turns"]
          == sum(len(at.get("provider_turns") or []) for at in l["attempts"]))
    check("T45 cost is computed from the frozen price snapshot",
          r["lane_cost_basis"] == "computed" and r["lane_calculated_cost_usd"] > 0
          and r["price_snapshot"] == "eval-037-price-snapshot-v1")
    prices = R.load_prices()
    c, basis = R.cost_for(prices, "gpt-5.6-sol", 1000, 500)
    check("T46 an unpriced model yields a NULL cost with a stated reason, not a guess",
          c is None and "not established" in basis)
    c2, b2 = R.cost_for(prices, "claude-sonnet-5", None, 500)
    check("T47 a missing token count yields a NULL cost, never an invented one",
          c2 is None and "did not report" in b2)
    shutil.rmtree(out, ignore_errors=True)


def t_canon_transcript():
    """Correction 4 — real arguments and per-item identity, not just hashes."""
    r, l, out = run_lane("sonnet-full-canon.yaml", "canon_user")
    calls = [tc for at in l["attempts"] for tc in (at.get("tool_calls") or [])
             if tc.get("tool_family") == "canon"]
    check("T48 Canon calls are recorded", len(calls) == 36, f"{len(calls)} calls")
    check("T49 each call retains its ACTUAL arguments, not only a hash",
          all(isinstance(tc["arguments"], dict) for tc in calls)
          and any(tc["arguments"].get("query") for tc in calls))
    refs = [ref for tc in calls for ref in tc.get("retrieved_refs", [])]
    check("T50 each retrieved item retains id, source id, status, kind and Q&A flag",
          bool(refs) and all(
              set(("item_id", "source_id", "source_dir", "source_status", "kind",
                   "is_qa")) <= set(ref) for ref in refs))
    check("T51 every retained ref carries a real source_status",
          all(ref["source_status"] in ("ACCEPTED", "HOLD") for ref in refs))
    resolvable = True
    for at in l["attempts"]:
        for tc in (at.get("tool_calls") or []):
            path, _, line = tc["transcript_ref"].partition("#")
            rows = (out / path).read_text().splitlines()
            d = json.loads(rows[int(line)])
            resolvable &= d["full_result"] is not None and d["call"]["name"] == tc["name"]
    check("T52 every transcript_ref resolves to the FULL retained tool result", resolvable)
    check("T53 the exact serialised request is retained for every attempt",
          all((out / at["request_path"]).exists() for at in l["attempts"])
          and all(json.loads((out / at["request_path"]).read_text()).get("messages")
                  for at in l["attempts"]))
    shutil.rmtree(out, ignore_errors=True)


def t_canon_search():
    """Correction 7 — BM25 ranked retrieval, all item classes, status preserved."""
    c = Canon(REPO, condition="FULL_CANON")
    r = c.canon_search("colour contrast typography")
    check("T54 canon_search is BM25-ranked with scores and ranks",
          "BM25" in r["ranking"] and all("score" in x and "rank" in x for x in r["results"])
          and [x["rank"] for x in r["results"][:5]] == [1, 2, 3, 4, 5])
    check("T55 results are ordered by descending score",
          all(r["results"][i]["score"] >= r["results"][i + 1]["score"]
              for i in range(min(50, len(r["results"]) - 1))))
    r2 = c.canon_search("colour contrast typography")
    check("T56 search is deterministic",
          [x["item_id"] for x in r["results"]] == [x["item_id"] for x in r2["results"]])
    kinds = {e["kind"] for e in c._flatten()}
    check("T57 every item class is retrievable, visual evidence included",
          kinds == {"knowledge", "concept_system", "binding", "ontology_term",
                    "ontology_concept", "qa", "visual_evidence"}, f"{sorted(kinds)}")
    check("T58 no aggregate top-K is imposed by the harness",
          r["limit_applied"] is None and r["returned"] == r["total_matches"]
          and r["limit_source"] == "none (unbounded)", f"{r['total_matches']} results")
    lim = c.canon_search("colour contrast typography", limit=7)
    check("T59 a limit applies only when the CALLER asks for one",
          lim["returned"] == 7 and lim["limit_source"] == "caller"
          and lim["total_matches"] == r["total_matches"])
    check("T60 status is preserved on every ranked result",
          all(x["source_status"] in (ACCEPTED, HOLD) for x in r["results"]))
    qa = [x for x in r["results"] if x["kind"] == "qa"]
    check("T61 Q&A epistemic metadata survives ranking",
          bool(qa) and all(x["not_benchmark_ground_truth"] is True
                           and x["independent_corroboration"] is False for x in qa))
    ct = (PKG / "tools/canon_tools.py").read_text()
    ct_code = "\n".join(l for l in ct.splitlines() if not l.lstrip().startswith("#"))
    ct_code = ct_code.split('"""', 2)[-1]          # drop the module docstring
    check("T62 no embedding or model call in the retrieval path",
          not any(x in ct_code for x in ("import openai", "import anthropic",
                                         "from google", "requests.", "embed(",
                                         "embedding", "httpx", "urllib")))
    check("T63 tokenization is deterministic and documented",
          canon_tools.tokenize("Colour-Contrast, 2026!") == ["colour", "contrast", "2026"])


def t_canon_status():
    c = Canon(REPO, condition="FULL_CANON")
    cat = c.canon_catalog()
    check("T64 catalog exposes every source with a real status",
          cat["total"] == 42 and cat["accepted"] == 24 and cat["hold"] == 18)
    check("T65 every HOLD source carries an explicit caution",
          all("caution" in s for s in cat["sources"] if s["source_status"] == HOLD))
    check("T66 filtering by HOLD returns only HOLD",
          all(s["source_status"] == HOLD
              for s in c.canon_catalog(source_status=HOLD)["sources"]))
    hold_src = next(s["source_dir"] for s in cat["sources"] if s["source_status"] == HOLD)
    rd = c.canon_read(source_dir=hold_src, artifact="source-knowledge.yaml")
    check("T67 canon_read stamps HOLD on the artifact AND every item",
          rd["source_status"] == HOLD
          and all(i["source_status"] == HOLD and "caution" in i for i in rd["items"]))
    for bad, label in (({"source_status": "accepted"}, "lowercase"), ({}, "absent")):
        try:
            canon_tools._assert_status(bad); ok = False
        except CanonStatusError:
            ok = True
        check(f"T68 a {label} status is REFUSED, not coerced", ok)
    try:
        Canon(REPO, condition="NO_CANON"); ok = False
    except PermissionError:
        ok = True
    check("T69 constructing Canon under NO_CANON raises", ok)
    try:
        canon_tools.dispatch(c, "canon_write", {}); ok = False
    except ValueError:
        ok = True
    check("T70 only the three named Canon tools are dispatchable", ok)
    src = (PKG / "tools/canon_tools.py").read_text()
    check("T71 the Canon module opens nothing for writing",
          '"w"' not in src and "'w'" not in src)


def t_no_canon_isolation():
    r, l, out = run_lane("sonnet-no-canon.yaml", "tool_user")
    check("T72 NO_CANON makes zero Canon calls even when the model tries",
          all(t["canon_tool_calls"] == 0 and t["canon_used"] is None for t in r["trials"]))
    check("T73 NO_CANON records no Canon fingerprints", "canon_fingerprints" not in r)
    lane = yaml.safe_load((PKG / "lanes/sonnet-no-canon.yaml").read_text())
    check("T74 the NO_CANON prompt is the common prompt verbatim",
          R.system_prompt_for(lane) == (PKG / "common/system-prompt.txt").read_text())
    schemas, _ = R.build_tools(lane, "B03")
    check("T75 NO_CANON + no-website brief exposes NO tools at all", schemas == [])
    schemas, _ = R.build_tools(lane, "B01")
    check("T76 NO_CANON + B01 exposes ONLY the website tool",
          [s["name"] for s in schemas] == ["website_read"])
    blob = (PKG / "lanes/sonnet-no-canon.yaml").read_text()
    leaks = [x for x in ("canon/knowledge/", "canon/candidates/", "canon/qa/") if x in blob]
    check("T77 the NO_CANON lane names no Canon corpus path", not leaks)
    shutil.rmtree(out, ignore_errors=True)

    # The strongest form of the claim: a NO_CANON worker must not even IMPORT the
    # Canon module, nor open any file under canon/. Prove it by making both fatal.
    guard = pathlib.Path(tempfile.mkdtemp()) / "guard.py"
    guard.write_text(
        "import builtins, runpy, sys, os\n"
        "class Block:\n"
        "    def find_spec(self, name, path=None, target=None):\n"
        "        if name.split('.')[0] == 'canon_tools':\n"
        "            raise AssertionError('NO_CANON imported canon_tools')\n"
        "        return None\n"
        "sys.meta_path.insert(0, Block())\n"
        "_open = builtins.open\n"
        "def guarded(f, *a, **k):\n"
        "    p = str(f)\n"
        "    if '/canon/knowledge/' in p or '/canon/candidates/' in p or '/canon/qa/' in p:\n"
        "        raise AssertionError('NO_CANON opened a Canon file: ' + p)\n"
        "    return _open(f, *a, **k)\n"
        "builtins.open = guarded\n"
        "sys.argv = sys.argv[1:]\n"
        "runpy.run_path(sys.argv[0], run_name='__main__')\n")
    o2 = pathlib.Path(tempfile.mkdtemp())
    p2 = subprocess.run(
        [sys.executable, str(guard), str(PKG / "tools/runner.py"),
         "--lane", str(PKG / "lanes/sonnet-no-canon.yaml"), "--fake", "tool_user",
         "--out", str(o2)], capture_output=True, text=True, cwd=REPO)
    check("T77b a NO_CANON worker never imports canon_tools and never opens a Canon "
          "file (enforced fatally)",
          p2.returncode == 0 and "AssertionError" not in p2.stderr,
          p2.stderr.strip().splitlines()[-1] if p2.returncode else "18 trials, no Canon touch")
    # and the same guard must FIRE on a FULL_CANON lane, proving the guard works
    o3 = pathlib.Path(tempfile.mkdtemp())
    p3 = subprocess.run(
        [sys.executable, str(guard), str(PKG / "tools/runner.py"),
         "--lane", str(PKG / "lanes/sonnet-full-canon.yaml"), "--fake", "clean",
         "--out", str(o3)], capture_output=True, text=True, cwd=REPO)
    check("T77c the same guard FIRES on a FULL_CANON lane (so T77b is not vacuous)",
          p3.returncode != 0 and "canon_tools" in p3.stderr)
    shutil.rmtree(guard.parent, ignore_errors=True)
    shutil.rmtree(o2, ignore_errors=True); shutil.rmtree(o3, ignore_errors=True)


def t_full_canon_prompt():
    lane = yaml.safe_load((PKG / "lanes/sonnet-full-canon.yaml").read_text())
    sp = R.system_prompt_for(lane)
    base = (PKG / "common/system-prompt.txt").read_text()
    add = yaml.safe_load((PKG / "conditions/full-canon.yaml").read_text())["addendum"]
    check("T78 FULL_CANON prompt = common prompt + addendum, in that order",
          sp.startswith(base.rstrip("\n")) and add.rstrip("\n") in sp)
    check("T79 the addendum lives only in conditions/full-canon.yaml",
          "ACCEPTED means the source passed" not in base
          and all("ACCEPTED means the source passed" not in p.read_text()
                  for p in (PKG / "lanes").glob("*.yaml")))
    schemas, _ = R.build_tools(lane, "B01")
    check("T80 FULL_CANON + B01 exposes the three Canon tools AND the website tool",
          sorted(s["name"] for s in schemas)
          == ["canon_catalog", "canon_read", "canon_search", "website_read"])
    schemas, _ = R.build_tools(lane, "B03")
    check("T81 FULL_CANON + B03 exposes the Canon tools but NO website tool",
          sorted(s["name"] for s in schemas)
          == ["canon_catalog", "canon_read", "canon_search"])


def t_substrate_identity():
    """Correction 5."""
    out = subprocess.run(["git", "ls-tree", "-r", "--name-only",
                          "c6f8d910f7a3cdaaeafa2280313abfb9b898cddd",
                          "eval/experiments/"], cwd=REPO,
                         capture_output=True, text=True).stdout.strip()
    check("T82 the Canon base commit provably does NOT contain EVAL-037", out == "")
    for lid in ("sol-no-canon", "gemma-full-canon"):
        L = yaml.safe_load((PKG / f"lanes/{lid}.yaml").read_text())
        s = L["substrate"]
        check(f"T83 {lid}: no base_commit start-commit claim; role stated as provenance",
              "base_commit" not in L and "provenance" in s["canon_base_commit_role"].lower()
              and "does not contain eval-037" in s["canon_base_commit_role"].lower())
        check(f"T84 {lid}: dispatch is gated on the substrate fingerprint",
              len(s["common_substrate_digest"]) == 64
              and s["freeze_fingerprint_file"] == "FREEZE-FINGERPRINT.yaml")
    import freeze_fingerprint as FF
    full, rows = FF.compute()
    check("T85 the freeze fingerprint is in no file it covers (not self-referential)",
          not [r for r, _ in rows
               if full in (PKG / r).read_text(encoding="utf-8", errors="ignore")])
    # a drifted substrate must be rejected at preflight
    tmp = pathlib.Path(tempfile.mkdtemp()) / "lane.yaml"
    L = yaml.safe_load((PKG / "lanes/sonnet-no-canon.yaml").read_text())
    L["substrate"]["common_substrate_digest"] = "0" * 64
    tmp.write_text(yaml.safe_dump(L, sort_keys=False))
    p = subprocess.run([sys.executable, str(PKG / "tools/runner.py"), "--lane", str(tmp),
                        "--fake", "clean", "--preflight-only"],
                       capture_output=True, text=True, cwd=REPO)
    check("T86 a substrate whose bytes differ is REJECTED before any call",
          p.returncode != 0 and "common substrate digest mismatch" in p.stderr)
    shutil.rmtree(tmp.parent, ignore_errors=True)


def t_gemma():
    """Correction 10."""
    blob = ((PKG / "tools/preflight.py").read_text()
            + (PKG / "EXECUTION-CONTRACT.md").read_text()
            + (PKG / "experiment.yaml").read_text()
            + "".join(p.read_text() for p in (PKG / "lanes").glob("*.yaml")))
    check("T87 the withdrawn Gemma capability claim is gone everywhere",
          not any(x in blob for x in ("historically not supported",
                                      "cannot support function calling")))
    check("T88 no model-specific preflight gate remains",
          "return 3" not in (PKG / "tools/preflight.py").read_text())
    for lid in ("gemma-full-canon", "gemma-no-canon"):
        L = yaml.safe_load((PKG / f"lanes/{lid}.yaml").read_text())
        check(f"T89 {lid}: normal exact-model preflight, no substitution",
              L["model"]["model_id"] == "gemma-4-31b-it"
              and L["model"]["moving_alias"] is False
              and "STOP" in L["model"]["alias_policy"])
    L = yaml.safe_load((PKG / "lanes/gemma-full-canon.yaml").read_text())
    check("T90 gemma FULL_CANON exposes the same three Canon tools as every other lane",
          L["condition_detail"]["canon_tools_exposed"]
          == ["canon_catalog", "canon_search", "canon_read"])
    r, l, out = run_lane("gemma-full-canon.yaml", "tool_user")
    check("T91 gemma FULL_CANON runs 18 trials with tools declared",
          len(r["trials"]) == 18 and all(t["canon_tool_calls"] > 0 for t in r["trials"]))
    shutil.rmtree(out, ignore_errors=True)


def t_schema_negatives():
    good = _good_result()
    cases = [
        ("T92 a 17-trial result is rejected", lambda d: d["trials"].pop()),
        ("T93 a 3rd transient retry is rejected",
         lambda d: d["trials"][0].update(transient_retries_used=5)),
        ("T94 a 2nd format repair is rejected",
         lambda d: d["trials"][0].update(format_repairs_used=2)),
        ("T95 failed_technical claiming a package is rejected",
         lambda d: d["trials"][0].update(status="failed_technical")),
        ("T96 failed_execution claiming eligibility is rejected",
         lambda d: d["trials"][0].update(status="failed_execution")),
        ("T97 a moving-alias model id is rejected",
         lambda d: d.update(model="claude-sonnet-latest")),
        ("T98 fresh_context: false is rejected",
         lambda d: d["trials"][0].update(fresh_context=False)),
        ("T99 an unknown extra field is rejected",
         lambda d: d["trials"][0].update(creative_score=7)),
        ("T100 a B03 trial claiming website access is rejected",
         lambda d: [t.update(website_tool_exposed=True, website_tool_calls=1,
                             website_snapshot_used=True)
                    for t in d["trials"] if t["brief_id"] == "B03"]),
        ("T101 a B01 trial claiming NO website tool is rejected",
         lambda d: [t.update(website_tool_exposed=False)
                    for t in d["trials"] if t["brief_id"] == "B01"]),
        ("T102 format_repaired with no repair-source digest is rejected",
         lambda d: d["trials"][0].update(status="format_repaired",
                                         format_repairs_used=1,
                                         repair_source_response_digest=None)),
        ("T103 a wrong canon_base_commit is rejected",
         lambda d: d["substrate"].update(canon_base_commit="0" * 40)),
    ]
    for name, mutate in cases:
        d = copy.deepcopy(good); mutate(d)
        check(name, bool(validate(d, RESULT_SCHEMA)))
    check("T104 the unmutated good result still validates", not validate(good, RESULT_SCHEMA),
          "; ".join(validate(good, RESULT_SCHEMA)[:2]))

    led = _good_ledger()
    check("T105 the good ledger validates", not validate(led, LEDGER_SCHEMA),
          "; ".join(validate(led, LEDGER_SCHEMA)[:2]))
    for name, mut in [
        ("T106 a transient outcome with a deterministic class is rejected",
         lambda d: d["attempts"][0].update(outcome="transient_failure",
                                           failure_class="context_overflow",
                                           failure_is_transient=True)),
        ("T107 a deterministic outcome marked transient is rejected",
         lambda d: d["attempts"][0].update(outcome="deterministic_failure",
                                           failure_class="context_overflow",
                                           failure_is_transient=True)),
        ("T108 a repair attempt with no repair-source digest is rejected",
         lambda d: d["attempts"][0].update(phase="repair", attempt_kind="format_repair")),
        ("T109 a technical_retry in the repair phase is rejected",
         lambda d: d["attempts"][0].update(attempt_kind="technical_retry", phase="repair",
                                           attempt_index=1)),
        ("T110 an attempt with no retained request path is rejected",
         lambda d: d["attempts"][0].pop("request_path")),
    ]:
        d = copy.deepcopy(led); mut(d)
        check(name, bool(validate(d, LEDGER_SCHEMA)))


def t_lane_run_validator_negatives():
    r, l, out = run_lane("sonnet-full-canon.yaml", "tool_user")

    def run_validator(mr=None, ml=None, extra=None, rm=None):
        tmp = pathlib.Path(tempfile.mkdtemp())
        shutil.copytree(out, tmp / "run")
        rr = json.loads((tmp / "run/result.json").read_text())
        ll = json.loads((tmp / "run/attempt-ledger.json").read_text())
        if mr:
            mr(rr)
        if ml:
            ml(ll)
        (tmp / "run/result.json").write_text(json.dumps(rr))
        (tmp / "run/attempt-ledger.json").write_text(json.dumps(ll))
        if extra:
            (tmp / "run" / extra).write_bytes(b"\x89PNG\r\n")
        if rm:
            for p in (tmp / "run").rglob(rm):
                p.unlink()
        p = subprocess.run(
            [sys.executable, str(PKG / "validators/validate_lane_run.py"),
             "--lane", str(PKG / "lanes/sonnet-full-canon.yaml"), "--run", str(tmp / "run")],
            capture_output=True, text=True, cwd=REPO)
        shutil.rmtree(tmp, ignore_errors=True)
        return p.returncode

    check("T111 the validator PASSES the untouched run", run_validator() == 0)
    check("T112 REJECTS a dropped trial",
          run_validator(mr=lambda d: d["trials"].pop()) != 0)
    check("T113 REJECTS reordered trials",
          run_validator(mr=lambda d: d["trials"].reverse()) != 0)
    check("T114 REJECTS a media artefact in the run directory",
          run_validator(extra="frame.png") != 0)
    check("T115 REJECTS a retry with no transient failure before it",
          run_validator(ml=lambda d: d["attempts"].append(
              {**d["attempts"][0], "attempt_index": 1,
               "attempt_kind": "technical_retry"})) != 0)
    check("T116 REJECTS an attempt after a deterministic failure",
          run_validator(ml=lambda d: (
              d["attempts"][0].update(outcome="deterministic_failure",
                                      failure_class="context_overflow",
                                      failure_is_transient=False),
              d["attempts"].insert(1, {**d["attempts"][0], "attempt_index": 1,
                                       "attempt_kind": "technical_retry",
                                       "outcome": "ok"}))) != 0)
    check("T117 REJECTS stripped Canon retrieval refs",
          run_validator(ml=lambda d: [tc.pop("retrieved_refs", None)
                                      for at in d["attempts"]
                                      for tc in (at.get("tool_calls") or [])]) != 0)
    check("T118 REJECTS a missing tool transcript file",
          run_validator(rm="*.jsonl") != 0)
    check("T119 REJECTS a missing retained request",
          run_validator(rm="*.request.json") != 0)
    check("T120 REJECTS understated usage totals",
          run_validator(mr=lambda d: d["trials"][0]["usage_totals"].update(
              provider_turns=1)) != 0)
    check("T121 REJECTS a B03 trial claiming a website call",
          run_validator(mr=lambda d: [t.update(website_tool_calls=1,
                                               website_snapshot_used=True)
                                      for t in d["trials"] if t["brief_id"] == "B03"]) != 0)
    check("T122 REJECTS a website digest that is not the sealed snapshot",
          run_validator(mr=lambda d: [t.update(website_snapshot_digests=["f" * 64])
                                      for t in d["trials"]
                                      if t["website_snapshot_digests"]]) != 0)
    shutil.rmtree(out, ignore_errors=True)


def t_zero_calls():
    src = (PKG / "tools/fake_provider.py").read_text()
    check("T123 fake_provider imports no SDK and opens no socket",
          not any(x in src for x in ("import openai", "import anthropic", "from google",
                                     "import requests", "import socket", "urllib", "httpx")))
    code = "\n".join(l for l in src.splitlines() if not l.lstrip().startswith("#"))
    code = code.split('"""', 2)[-1]
    check("T124 fake_provider is deterministic (no clock, no randomness)",
          not any(x in code for x in ("import random", "random.", "time.time(",
                                      "datetime.now(", "uuid.", "os.urandom")))
    for m in ("openai", "anthropic", "google.genai"):
        p = subprocess.run([sys.executable, "-c", f"import {m}"], capture_output=True)
        check(f"T125 provider SDK {m!r} is not installed, so no call is even possible",
              p.returncode != 0)
    r, l, out = run_lane("sonnet-full-canon.yaml", "tool_user")
    raws = list((out / "raw").glob("*.json"))
    check("T126 every raw response in a fake run is marked fake",
          bool(raws) and all(json.loads(p.read_text()).get("fake") is True for p in raws),
          f"{len(raws)} responses")
    shutil.rmtree(out, ignore_errors=True)


# ========================================================================== #
SECTIONS = ["DELIVERABLE", "OBJECTIVE_INTERPRETATION", "CORE_CREATIVE_IDEA",
            "MESSAGE_AND_INFORMATION_HIERARCHY", "VISUAL_SYSTEM", "PRODUCTION_RECIPE",
            "GENERATION_PROMPTS", "DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS",
            "AUDIO_AND_EDIT", "FAILURE_PREVENTION", "HARD_CONSTRAINT_CHECK",
            "KNOWLEDGE_AND_WEBSITE_USE"]


def _good_result():
    lid = "sonnet-full-canon"
    ids = sorted([f"E037-{lid}-{b}-R{r}" for r in (1, 2, 3)
                  for b in ["B01", "B02", "B03", "B04", "B05", "B06"]], key=order_key)
    trials = []
    for i, tid in enumerate(ids, 1):
        b = tid.split("-")[-2]
        web = b in ("B01", "B02")
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
            "calculated_cost_usd": 0.0001, "cost_basis": "computed", "wall_clock_ms": 5})
    return {"experiment": "EVAL-037", "lane_id": lid, "branch": f"work/eval-037-{lid}",
            "substrate": {"freeze_fingerprint": "b" * 64,
                          "canon_base_commit": "c6f8d910f7a3cdaaeafa2280313abfb9b898cddd",
                          "execution_commit": "c" * 40},
            "runner_commit": "d" * 40, "provider": "Anthropic", "model": "claude-sonnet-5",
            "condition": "FULL_CANON",
            "canon_fingerprints": {
                "full_knowledge": "cbd321aa3be7464e785a0d42de1764cdccc8bdd33bc023a376740f8f196bde60",
                "qa": "1313c0babe2194a7bc71c1628f9fbec5fa4f35ca5ff5edc7f594662101dc62bd"},
            "price_snapshot": "eval-037-price-snapshot-v1",
            "lane_usage_totals": {"input_tokens": 180, "output_tokens": 90,
                                  "provider_turns": 36, "latency_ms": 54},
            "lane_calculated_cost_usd": 0.002, "lane_cost_basis": "computed",
            "trial_count": 18, "trials": trials}


def _good_ledger():
    return {"experiment": "EVAL-037", "lane_id": "sol-no-canon",
            "branch": "work/eval-037-sol-no-canon",
            "substrate": {"freeze_fingerprint": "a" * 64,
                          "canon_base_commit": "c6f8d910f7a3cdaaeafa2280313abfb9b898cddd",
                          "execution_commit": "b" * 40},
            "runner_commit": "b" * 40, "model": "gpt-5.6-sol", "condition": "NO_CANON",
            "attempts": [{"trial_id": "E037-sol-no-canon-B01-R1", "brief_id": "B01",
                          "repetition": 1, "attempt_index": 0, "attempt_kind": "initial",
                          "phase": "creative", "started_at": "2026-08-30T12:00:00+00:00",
                          "ended_at": "2026-08-30T12:00:10+00:00", "outcome": "ok",
                          "fresh_context": True, "request_digest": "c" * 64,
                          "request_path": "requests/x-a0.request.json",
                          "response_digest": "d" * 64}]}


def main():
    print("EVAL-037 substrate tests — fake provider only, no network, no spend\n")
    for fn in (t_clean, t_trial_order, t_website_tool, t_website_drift, t_format_repair,
               t_failed_format, t_repair_transient, t_failure_classification, t_usage,
               t_canon_transcript, t_canon_search, t_canon_status, t_no_canon_isolation,
               t_full_canon_prompt, t_substrate_identity, t_gemma, t_schema_negatives,
               t_lane_run_validator_negatives, t_zero_calls):
        fn()
    print(f"\n{len(PASSED)} passed, {len(FAILED)} failed")
    if FAILED:
        print("FAILED: " + "\n         ".join(FAILED))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
