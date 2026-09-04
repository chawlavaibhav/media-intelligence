# -*- coding: utf-8 -*-
"""Emit the EVAL-039A Stage A freeze package. USD 0; no network; reads only committed repo files."""
import copy, hashlib, os, re, sys, yaml, datetime
sys.path.insert(0, os.path.dirname(__file__))
from routes import R, EVAL_PRICES, USD_INR_REF
from common import NOTICE, FAMILIES
from cases_img import IMG
from cases_vid import VID
from cases_aud import AUD

HERE = os.path.dirname(os.path.abspath(__file__))
# runs from eval/empirical-planning/STAGE-A-FREEZE-2026-09/tools/ (committed copy); REPO is four levels up
REPO = os.environ.get("MI_REPO") or os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
OUT = os.environ.get("MI_OUT") or os.path.join(REPO, "eval/empirical-planning/STAGE-A-FREEZE-2026-09")
BASE_SHA = "cb92f1e"
import subprocess
def git(*a):
    try: return subprocess.run(["git", "-C", REPO] + list(a), capture_output=True, text=True).stdout.strip()
    except Exception: return "unavailable"
TODAY = "2026-09-05"

# ---------------------------------------------------------------- packs (read-only)
PA = yaml.safe_load(open(f"{REPO}/canon/compilation/PACK-product_appearance-v0.yaml", encoding="utf-8"))
CA = yaml.safe_load(open(f"{REPO}/canon/compilation/PACK-composition_and_attention-v0.yaml", encoding="utf-8"))
TRIG = yaml.safe_load(open(f"{REPO}/canon/packs/pack-triggers-v0.yaml", encoding="utf-8"))
assert TRIG["coverage_gap_notice"].strip() == NOTICE, "notice drift"
DEC = {}
for pack in (PA, CA):
    for d in pack["decisions"]:
        DEC[d["decision_id"]] = dict(question=d["question"], default=d["default"], check=d["check"], check_id=d["check_id"], limits=d.get("limits") or [], pack=pack["pack_id"])
PACK_LIMITS = {"product_appearance": PA["pack_limits"], "composition_and_attention": CA["pack_limits"]}
CORPUS = PA["corpus_digest"][:12]

PLAN = open(f"{REPO}/coordination/plans/2026-09-05-CAPABILITY-LAB-CAMPAIGN-v1.md", encoding="utf-8").read()
E_LINES = [l for l in PLAN.splitlines() if re.match(r"^- E[1-5] — ", l)]
assert len(E_LINES) == 5

ROSTER_PATH = f"{REPO}/eval/empirical-planning/ROSTER-REFRESH-2026-09.yaml"
ROSTER = yaml.safe_load(open(ROSTER_PATH, encoding="utf-8")) if os.path.exists(ROSTER_PATH) else None
assert ROSTER is not None, "roster expected present (it was read at build time); rerun with the unpinned branch otherwise"
RREC = {r["route_key"]: r for r in ROSTER["routes"]}
ROSTER_SHA256 = hashlib.sha256(open(ROSTER_PATH, "rb").read()).hexdigest()
PRICED_AGAINST = dict(file="eval/empirical-planning/ROSTER-REFRESH-2026-09.yaml", sha256=ROSTER_SHA256,
                      roster_last_commit=git("log", "-1", "--format=%h %s", "--", "eval/empirical-planning/ROSTER-REFRESH-2026-09.yaml"),
                      branch_head_at_build=git("log", "-1", "--format=%h", "HEAD"), working_tree_matches_head=(git("diff", "HEAD", "--stat", "--", "eval/empirical-planning/ROSTER-REFRESH-2026-09.yaml") == ""),
                      rule="the spend record must name this sha256; if the roster changes, rebuild with tools/build.py rather than editing numbers by hand")
def roster_price(R0):
    rec = RREC.get(R0["roster_key"])
    if rec is None: return ("absent", None, None)
    if R0["roster_variant"] == "fallback":
        fb = rec.get("fallback") or {}; return (fb.get("route_status"), (fb.get("regular_price") or {}).get("value"), fb.get("pin_ref"))
    if R0["roster_variant"]:
        for v in rec.get("variants") or []:
            if v.get("variant") == R0["roster_variant"]:
                return (v.get("route_status"), (v.get("regular_price") or {}).get("value"), v.get("pin_ref"))
        return ("variant_absent", None, None)
    return (rec.get("route_status"), (rec.get("regular_price") or {}).get("value"), rec.get("pin_ref"))
XCHECK = []
for k, R0 in R.items():
    st, val, pin = roster_price(R0)
    if R0["price_status"] == "pinned":
        base = R0["roster_base_price"] if R0["roster_base_price"] is not None else R0["unit_price"]
        assert st in ("pinned", "needs_controller_enablement", "no_access") and val is not None and abs(float(val) - float(base)) < 1e-9, (k, st, val, base)
        assert pin and R0["price_ref"].endswith(pin.split("price-pins-2026-09/")[-1]), (k, pin, R0["price_ref"])
    XCHECK.append(dict(route_key=k, roster_key=R0["roster_key"], roster_variant=R0["roster_variant"], roster_status=st, roster_price=val, package_price=R0["unit_price"], package_price_status=R0["price_status"], **({"addon": R0["addon"]} if R0["addon"] else {})))
print("roster cross-check ok:", len(XCHECK), "routes")

# ---------------------------------------------------------------- assemble cases
CASES = IMG + VID + AUD
BY = {c["case_id"]: c for c in CASES}
for c in CASES:
    for f in ("nr", "acceptance_contract", "bp"):
        if isinstance(c[f], str) and c[f].startswith("same_as:"):
            src = BY[c[f].split(":")[1]]
            c[f] = copy.deepcopy(src[f]); c.setdefault("same_as", {})[f] = src["case_id"]

ORDER = ["IMG-CORE-01", "IMG-CORE-02", "IMG-CORE-03", "IMG-CORE-04", "IMG-TEXT-01", "IMG-TEXT-02", "IMG-EDIT-01", "IMG-EDIT-02", "IMG-EXT-01", "IMG-COMP-01", "IMG-REF-01", "IMG-REF-02",
         "VID-T2V-01", "VID-T2V-02", "VID-T2V-03", "VID-T2V-04", "VID-2SPK-01", "VID-KNEE-01", "VID-TOPO3-01", "VID-I2V-01", "VID-I2V-02", "VID-I2V-03", "VID-I2V-04", "VID-REF-01", "VID-REF-02", "VID-MS-01", "VID-MS-02",
         "AUD-TTS-01", "AUD-TTS-02", "AUD-TTS-03", "AUD-LIP-01", "AUD-LIP-02", "AUD-LIP-03", "MUS-01", "MUS-02"]
assert sorted(ORDER) == sorted(BY) and len(ORDER) == 35, (set(ORDER) ^ set(BY))
CASES = [BY[k] for k in ORDER]

# ---------------------------------------------------------------- pack selection (deterministic, from NR)
BASE = {"static_image": ["composition_and_attention", "colour_and_visual_register"],
        "video": ["composition_and_attention", "colour_and_visual_register", "camera_and_spatial_grammar", "editing_pacing_and_short_form"],
        "audio": []}
COMPILED = {"composition_and_attention", "product_appearance"}

def packs_for(c):
    nr = c["nr"]; rows = []
    for p in TRIG["universal_packs"]:
        rows.append((p, "universal"))
    for p in BASE[nr["modality"]]:
        rows.append((p, f"base:{nr['modality']} (R05)"))
    if nr.get("text_requirements"):
        rows.append(("typography_and_copy", "text_requirements_nonempty (R08)"))
    if nr.get("product_or_packshot_present"):
        rows.append(("product_appearance", "product_or_packshot_entity_present (R06)"))
    rows.append(("indian_indic_context", "language_topology_present_or_market_IN (R10; market IN for every case)"))
    if c["bp"].get("advertising"):
        rows.append(("commercial_communication", "advertising_acceptance_intent (R18)"))
    out = []
    for p, why in rows:
        out.append(dict(pack=p, status="compiled — injected by id" if p in COMPILED else "selected_uncompiled — listed only; no doctrine drawn", trigger=why))
    return out

# ---------------------------------------------------------------- blueprint rendering
SK_RE = re.compile(r"\s*\((?:closure waiver |scs_|sk_)[^)]*\)")

def render_blueprint(c):
    cid = c["case_id"]; bp = c["bp"]; nr = c["nr"]
    packs = packs_for(c)
    selected_compiled = {p["pack"] for p in packs if p["pack"] in COMPILED}
    lines = []
    L = lines.append
    L(f"# Production blueprint — {cid}")
    L("")
    L("```yaml")
    L(f"case_id: {cid}")
    L("author: executor_agent")
    L("blueprint_author: executor_agent")
    L("held_constant_across_routes: true")
    L(f"frozen: {TODAY}")
    L(f"gate_pre: not_available_on_base — canon/gate/run_gate.py is absent from base {BASE_SHA} (CANON-GATE-001 unmerged); run `pre` on this file when it lands")
    L(f"packs_source: canon/compilation/PACK-*-v0.yaml (corpus {CORPUS}); triggers canon/packs/pack-triggers-v0.yaml; DEFAULT/CHECK text rendered by id, never paraphrased; no HOLD material")
    if c.get("same_as", {}).get("bp"):
        L(f"production_spec_identical_to: {c['same_as']['bp']} (the cost-knee case runs the same request on other tiers; only this header differs)")
    L("```")
    L("")
    L("## 1. packs_selected (deterministic lookup from the Normalized Request; `compiled` = injected by id, `uncompiled` = listed only, no doctrine drawn)")
    L("")
    for p in packs:
        L(f"- `{p['pack']}` — {'compiled' if p['pack'] in COMPILED else 'uncompiled'} — {p['trigger']}")
    L("")
    if nr["modality"] == "audio":
        L("### Coverage-gap notice (verbatim, `canon/packs/pack-triggers-v0.yaml` → `coverage_gap_notice`, mandatory in every audio cell)")
        L("")
        L("> " + NOTICE)
        L("")
        L("**Attribution:** no decision in this blueprint is attributed to Canon. Section 2 is empty by design; section 2a lists the production parameters taken from the brief alone.")
        L("")
    elif bp.get("audio_half"):
        L("### Coverage-gap notice for the audio half of this cell (verbatim, `canon/packs/pack-triggers-v0.yaml` → `coverage_gap_notice`)")
        L("")
        L("> " + NOTICE)
        L("")
        L("**Attribution:** the speech-to-mouth transform and every audio parameter below come from the brief alone and are not attributed to Canon. Only the three composition decisions in section 2, which concern the untouched video plate, cite compiled doctrine.")
        L("")
    # decisions
    L("## 2. decisions (by id; DEFAULT = the pack's text; CASE VALUE = this case's filled value)")
    L("")
    outside = []
    used_ids = []
    for did, val in bp.get("decisions", []):
        d = DEC[did]
        if d["pack"] not in selected_compiled:
            outside.append((did, val)); continue
        used_ids.append(did)
        L(f"### {did} — {d['question']}")
        L("")
        L(f"- **DEFAULT ({d['pack']}):** {d['default']}")
        for lim in d["limits"]:
            L(f"- **LIMIT (pack text):** {lim}")
        L(f"- **CASE VALUE:** {val}")
        L("")
    if not bp.get("decisions"):
        L("_No Canon decision applies to this cell (audio: zero packs, zero accepted sources — see the notice above)._")
        L("")
    devs = [f"{did}: {val}" for did, val in bp.get("decisions", []) if did in used_ids and re.search(r"[Dd]eviation|exception \(CF-06\)|declared as the energetic exception", val)]
    L("### DOCTRINE_DEVIATIONS")
    L("")
    if devs:
        for d in devs: L(f"- {d}")
    else:
        L("- none — every applicable default is accepted as written.")
    L("")
    if outside:
        L("### 2a. Production parameters outside the triggered packs (brief-only; not Canon)")
        L("")
        L("The `product_appearance` pack is not triggered for this Normalized Request (no product or packshot entity), so its lighting doctrine is not injected. The parameters below are the Executor's production choices on the brief alone and are attributed to nothing in Canon.")
        L("")
        for did, val in outside:
            L(f"- light/mood: {SK_RE.sub('', val)}")
        L("")
    if bp.get("brief_parameters"):
        L("### 2a. Production parameters from the brief alone (not Canon)" if nr["modality"] == "audio" or bp.get("audio_half") else "### 2b. Brief parameters")
        L("")
        for b in bp["brief_parameters"]: L(f"- {b}")
        L("")
    # text handling
    L("## 3. text_handling")
    L("")
    th = bp["text_handling"]
    if isinstance(th, str):
        L(f"- mode: `{th}`")
    else:
        L(f"- mode: {th['mode']}")
        for s in th["strings"]:
            ex = s.get("exactness", "exact")
            L(f"- string `{s['id']}` ({s['script']}, {s['role']}, {ex}): **{s['content']}**")
        cs = th["composite_spec"]
        L(f"- composite arm: font {cs['font']}; positions: {cs['positions']}; colour: {cs['colour']}; rule: {cs['rule']}")
    L("")
    # dispatch
    L("## 4. dispatch_parameters (identical for every route; route mapping only in `TEST-CASES.yaml` → `routes[].params`)")
    L("")
    for k, v in bp["dispatch"].items(): L(f"- {k}: {v}")
    L("")
    # checks
    L("## 5. pre_dispatch_checks (the packs' CHECK lines, by id, run over the prompt before any call)")
    L("")
    for did in used_ids:
        d = DEC[did]; L(f"- `{d['check_id']}`: {d['check']}")
    if nr["modality"] == "audio":
        L("- no pack CHECK applies (audio cell — see the coverage-gap notice); brief-only pre-dispatch checks, attributed to nothing in Canon: the request payload's script is byte-identical to `speaker_topology.script`; ≤ 250 characters; one voice; no music bed.")
    elif isinstance(th, str) and th.startswith("none"):
        L("- `no-in-image-text`: the generation prompt includes an explicit no-lettering instruction and names no string; any lettering in the output is a reject (E5), never an exclusion.")
    elif not isinstance(th, str):
        L("- `no-in-image-text (composite arm / plate)`: the textless-plate prompt includes an explicit no-lettering instruction; lettering on a plate is a reject; the overlay step is code at USD 0.")
        L("- `exact-string-carry (generated arms)`: every required string appears in the generation prompt byte-identical to `text_requirements[].content` (checked by substring).")
    for p in packs:
        if p["pack"] in selected_compiled:
            for lim in PACK_LIMITS[p["pack"]][:1]:
                L(f"- pack limit (`{p['pack']}`): {lim}")
    L("")
    # prompt
    L("## 6. generation_prompt (byte-identical across every route listed for this case)")
    L("")
    L("```text")
    L(bp["prompt"])
    L("```")
    for name, txt in (bp.get("prompt_variants") or {}).items():
        L("")
        L(f"### {name}")
        L("")
        L("```text")
        L(txt)
        L("```")
    L("")
    return "\n".join(lines)

# ---------------------------------------------------------------- routes → records
def route_record(r, case):
    R0 = R[r["route_key"]]
    rec = dict(route_key=r["route_key"], route_id=R0["route_id"], surface=R0["surface"], billing_pool=R0["billing_pool"],
               route_status=R0["route_status"], arm=r["arm"], params=dict(r["params"]), repeats=r["repeats"], tranche=r["tranche"],
               item_id=r.get("item_id", case["case_id"]), quantity=r["quantity"], quantity_unit=r.get("quantity_unit", "images"))
    rec["params"]["seed"] = "unset"
    if R0["conditional"]: rec["conditional"] = "listed, not in the cap"
    if r.get("repeats_exception"): rec["repeats_note"] = r["repeats_exception"]
    rec["price_status"] = R0["price_status"]
    return rec

# cut order (task §C, copied verbatim into IRREDUCIBILITY.md): item number → (cases touched, scope)
CUT_ITEMS = {1: (["VID-MS-01"], "route line: Seedance 2.5 15 s"), 2: (["VID-REF-01", "VID-REF-02"], "route line: Seedance 2.5 ref2v"),
             3: (["VID-I2V-01", "VID-I2V-02", "VID-I2V-03", "VID-I2V-04"], "route line: Wan 3.0 i2v"), 4: (["VID-MS-02"], "whole case"),
             5: (["VID-REF-02"], "route line: Kling v3 elements (conditional arm)"), 6: (["VID-I2V-02", "VID-I2V-03"], "route line: Seedance 2.5 i2v"),
             7: (["VID-2SPK-01"], "arm: the chain (plate, i2v, TTS drives, lipsync)"), 8: (["MUS-02"], "whole case"),
             9: (["VID-KNEE-01"], "route line: Veo 3.1 full tier"), 10: (["VID-T2V-01", "VID-T2V-02", "VID-T2V-03", "VID-T2V-04"], "route line: Wan 3.0 t2v")}
def cut_fields(c):
    items = [i for i, (ids, _) in CUT_ITEMS.items() if c["case_id"] in ids]
    if items:
        return dict(cut_order_rank=min(items), cut_order_items=[dict(item=i, scope=CUT_ITEMS[i][1]) for i in items])
    lang = c["customer_request"]["language"]
    why = []
    if c["case_id"].split("-")[1] in ("CORE", "T2V", "I2V") or c["lane"] == "AUD": why.append("core item")
    if lang in ("hi", "hg"): why.append("Hindi/Hinglish item")
    if c["case_id"] in ("IMG-TEXT-01", "IMG-TEXT-02", "VID-TOPO3-01"): why.append("TOPO-02/03 arms A and C")
    if not why: why.append("not named by any cut item")
    return dict(cut_order_rank="never_cut", cut_order_items=[], never_cut_reason=", ".join(why))

def catalogue():
    out = {}
    for k, R0 in R.items():
        out[k] = dict(route_id=R0["route_id"], surface=R0["surface"], billing_pool=R0["billing_pool"], route_status=R0["route_status"], arm_class=R0["arm"],
                      unit=R0["unit"], unit_price=R0["unit_price"], price_status=R0["price_status"], price_ref=R0["price_ref"],
                      roster_route_key=R0["roster_key"] + (f" / variant {R0['roster_variant']}" if R0["roster_variant"] else ""),
                      seed_support=R0["seed_support"], conditional=R0["conditional"], plan_ref=R0["plan_ref"])
        for f in ("priced_surface", "roster_base_price", "addon", "note", "credit_alternative", "quantity_rule"):
            if R0[f]: out[k][f] = R0[f]
    return out

# ---------------------------------------------------------------- evaluator plan
DET8 = ["delivery_format_compliance", "edit_preservation", "packaging_brand_colour_fidelity", "audio_video_synchronisation", "reliability_pass_at_k", "cost_and_cpao", "latency_errors_refusals", "reproducibility"]

def eval_plan(c):
    nr = c["nr"]; ex = set(c["capabilities"]["exercised"]); mod = nr["modality"]
    th = c["bp"]["text_handling"]; no_text = isinstance(th, str) and th.startswith("none")
    has_text = bool(nr.get("text_requirements"))
    speech = bool(nr.get("speaker_topology")) and nr["speaker_topology"].get("script_exactness") == "exact"
    tdet = ["COMMON_T_DET (see common_T_DET at the top of this file)"]
    if "edit_preservation" in ex: tdet.append("masked-diff preservation against the supplied input (mask = the named changed region) → edit_preservation")
    if "packaging_brand_colour_fidelity" in ex: tdet.append("brand-colour distance in the pack/product mask against the fixture-recorded sRGB → packaging_brand_colour_fidelity")
    if "audio_video_synchronisation" in ex: tdet.append("A/V offset between the supplied drive and the output audio/mouth-onset → audio_video_synchronisation (we supply both inputs)")
    if no_text and mod != "audio": tdet.append("baked-text scan (Cloud Vision TEXT_DETECTION on the image / on 3 sampled frames): any detection → reject under E5; the detector's known error rate is carried")
    tbench = []
    if has_text: tbench.append("Cloud Vision TEXT_DETECTION vs text_requirements (Devanagari NFC / Latin normalised) on every artifact" + (" and on 3 sampled frames per clip" if mod == "video" else "") + " → exact_text_* (benchmark-grade, never Registry)")
    if speech: tbench.append("ASR vs the known script on the output audio → spoken_script_correctness (benchmark-grade; ASR model unnamed → price unpinned)")
    thuman = ["COMMON_T_HUMAN (blind Controller acceptance, see common_T_HUMAN)"]
    if "pronunciation_intelligibility" in ex: thuman.append("pronunciation of Hindi / brand names by a first-language listener (Q5, human only)")
    tscreen = ["COMMON_T_SCREEN (see common_T_SCREEN)"]
    regs = [k for k in DET8 if k in ex]
    return dict(case_id=c["case_id"], T_DET=tdet, T_BENCH=tbench or ["none for this case"], T_HUMAN=thuman, T_SCREEN=tscreen,
                registry_eligible_capabilities=regs, non_registry_capabilities=sorted(ex - set(DET8)))

# ---------------------------------------------------------------- cost table
def cost_rows(c):
    rows = []
    for r in c["routes"]:
        R0 = R[r["route_key"]]; q = r["quantity"]; calls = r["repeats"]; price = R0["unit_price"]
        line = None; inr = None
        if price is not None:
            if R0["unit"] in ("per_image", "per_clip"): line = price * calls
            elif R0["unit"] in ("per_second", "per_minute"): line = price * q * calls
            elif R0["unit"] == "per_1k_chars": line = price * q / 1000 * calls
            elif R0["unit"] == "per_1M_chars": line = price * q / 1e6 * calls
            elif R0["unit"] == "per_1k_chars_inr": inr = price * q / 1000 * calls; line = inr / USD_INR_REF
            else: raise ValueError(R0["unit"])
        rows.append(dict(case_id=c["case_id"], item_id=r.get("item_id", c["case_id"]), route_key=r["route_key"], arm=r["arm"],
                         surface=R0["surface"], billing_pool=R0["billing_pool"], tranche=r["tranche"], items=1, repeats=calls, calls=calls,
                         quantity_per_call=round(q, 4) if isinstance(q, float) else q, quantity_unit=r.get("quantity_unit", "images"),
                         unit_price=price, price_status=R0["price_status"],
                         line_usd=(round(line, 4) if line is not None else None), line_inr=(round(inr, 4) if inr is not None else None),
                         conditional=R0["conditional"], route_status=R0["route_status"],
                         counted_in_cap=(line is not None and not R0["conditional"] and R0["in_cap"] and R0["route_status"] != "no_access")))
    return rows

# ---------------------------------------------------------------- emit
os.makedirs(f"{OUT}/test-cases", exist_ok=True); os.makedirs(f"{OUT}/BLUEPRINTS", exist_ok=True)
records, plans, allrows, bp_sha = [], [], [], {}
for c in CASES:
    cid = c["case_id"]
    text = render_blueprint(c)
    path = f"{OUT}/BLUEPRINTS/{cid}.blueprint.md"
    open(path, "w", encoding="utf-8").write(text)
    sha = hashlib.sha256(text.encode("utf-8")).hexdigest(); bp_sha[cid] = sha
    rec = dict(case_id=cid, item_id=cid, lane=c["lane"], question_served=c["question_served"], customer_request=c["customer_request"], source=c["source"],
               nr=c["nr"], capabilities=c["capabilities"], conditions=c["conditions"], reference_assets=c["reference_assets"],
               acceptance_contract=c["acceptance_contract"], blueprint_ref=f"BLUEPRINTS/{cid}.blueprint.md", blueprint_author="executor_agent", blueprint_sha256=sha,
               routes=[route_record(r, c) for r in c["routes"]], downstream_reuse=c["downstream_reuse"], **cut_fields(c), irreducibility_ref=c["irreducibility_ref"])
    if c.get("same_as"): rec["same_as"] = c["same_as"]
    if c.get("pool_note"): rec["billing_note"] = c["pool_note"]
    records.append(rec); plans.append(eval_plan(c)); allrows += cost_rows(c)

# counts
def calls(pred): return sum(r["calls"] for r in allrows if pred(r))
n1a = calls(lambda r: r["tranche"] == "1a" and not r["conditional"]); n1b = calls(lambda r: r["tranche"] == "1b" and not r["conditional"]); ncond = calls(lambda r: r["conditional"])
langs = {"en": 0, "hi": 0, "hg": 0}; lane_lang = {}
for c in CASES:
    l = c["customer_request"]["language"]; langs[l] += 1; lane_lang.setdefault(c["lane"], {"en": 0, "hi": 0, "hg": 0})[l] += 1
fixtures = [c["case_id"] for c in CASES if c["source"]["pool"] == "fixture"]
counts = dict(cases=len(CASES), blueprints=len(CASES), calls_1a=n1a, calls_1b=n1b, calls_total=n1a + n1b, calls_conditional=ncond, language_mix=langs, language_mix_by_lane=lane_lang, fixtures=fixtures)
print("COUNTS", counts)

yd = lambda o: yaml.safe_dump(o, allow_unicode=True, sort_keys=False, width=2000, default_flow_style=None)
HEAD = f"# EVAL-039A — Stage A freeze package. Prices/pins by route key from EVAL-039B's ROSTER-REFRESH-2026-09.yaml (present at build time; read-only).\n# STATUS: FROZEN PROPOSAL, USD 0, awaits the Controller's acceptance (task file §F, morning decisions in README.md).\n# Generated {TODAY} by the Executor agent from the committed packs, grammar and source pools; base {BASE_SHA}. No provider, evaluator, OCR or LLM call was made.\n"
open(f"{OUT}/TEST-CASES.yaml", "w", encoding="utf-8").write(HEAD + yd(dict(package="STAGE-A-FREEZE-2026-09", task="EVAL-039A", status="FROZEN_PROPOSAL_PENDING_CONTROLLER_ACCEPTANCE", base=BASE_SHA, counts=counts,
    cut_order_rule="cut_order_rank = the lowest-numbered task-§C cut item that touches the case (cut_order_items[] lists each item and whether it removes a route line, an arm, or the whole case), or never_cut with never_cut_reason (core item / Hindi-Hinglish item / TOPO-02/03 arms A and C); the cut order itself is in IRREDUCIBILITY.md",
    route_catalogue=catalogue(),
    interlock_eval_039b=dict(item_id="= case_id (route-level item_id where a case carries several billed items, e.g. VID-2SPK-01 TTS lines)", quantity="routes[].quantity with routes[].quantity_unit ∈ {images, seconds, chars, minutes, clips}", regenerate="python3 eval/empirical-planning/project_costs.py --test-cases eval/empirical-planning/STAGE-A-FREEZE-2026-09/TEST-CASES.yaml (EVAL-039B)", price_pins="ROSTER-REFRESH-2026-09.yaml present at build time; every route record names its roster_route_key and price_status; the COST-TABLE carries a roster_cross_check block"),
    cases=records)))

open(f"{OUT}/EVALUATOR-PLAN.yaml", "w", encoding="utf-8").write(HEAD + yd(dict(package="STAGE-A-FREEZE-2026-09", rule="only the 8 yes_deterministic capabilities of EVALUATOR-QUALIFICATION-MAP.yaml may write Registry rows (T-DET); T-BENCH (Cloud Vision, ASR) carries error rates and never enters the Registry; T-HUMAN is blind Controller acceptance; T-SCREEN is screened_not_qualified triage; an unqualified evaluator never blocks generation",
    deterministic_capabilities=DET8, language_pooling="never pooled across en/hi/hg (COND-LANGUAGE hard rule) — applies to every case",
    common_T_DET=["format probe (container, aspect, resolution, duration, audio-track presence) → delivery_format_compliance",
                  "ledger-derived latency, error class, refusal → latency_errors_refusals",
                  "trial cost from the ledger → cost_and_cpao (trial cost only; CpAO absence_reason: not_applicable)",
                  "unseeded repeat hash + SSIM between the two repeats → reproducibility (inherent variance, seed_policy unset)",
                  "reliability_pass_at_k where a deterministic pass criterion exists (format probe pass)",
                  "run_gate.py post — structure-only, observation, when CANON-GATE-001 lands (gate_post: not_available_on_base today)"],
    common_T_HUMAN="Controller blind acceptance against ACCEPTANCE-CONTRACTS.md (EVAL-038 pattern: stripped, blinded, committed, keys off-repo); one accept/reject per artifact; identity items judged as line-ups with decoys",
    common_T_SCREEN="VLM failure-mode tagging (Gemini / Claude vision), labelled screened_not_qualified; never a Registry input; agreement with T-HUMAN recorded as Q4 qualification evidence",
    gate_post="canon/gate/run_gate.py post on every artifact, structure only, observation — not_available_on_base " + BASE_SHA,
    evaluator_call_estimate=dict(cloud_vision_calls="≈ one per image artifact (baked-text scan or exactness) + 3 frames per video clip (baked-text) + 3 frames per TOPO-03 clip (exactness); see COST-TABLE.yaml evaluator rows", asr_calls="one per speech artifact (TTS 20, T2V-01 12, 2SPK native 8 + chain 4, lipsync 12)", vlm_triage_calls="one per artifact"),
    per_case=plans)))

seed_rows = []
for k, R0 in R.items():
    seed_rows.append(dict(route_key=k, route_id=R0["route_id"], surface=R0["surface"], seed_support=R0["seed_support"],
                          seed_support_evidence=("EVAL-010 WORKFLOW-CONTROL-MATRIX.yaml reproducibility_summary" if R0["seed_support"] in ("exposed", "absent_in_api") else "undocumented — route unpinned; EVAL-039B records it"),
                          seed_policy="unset", seed_value=None, reason="inherent variance by default (A-TEXT precedent); repeats under `unset` are never pooled with `held` repeats"))
open(f"{OUT}/SEED-POLICY.yaml", "w", encoding="utf-8").write(HEAD + yd(dict(package="STAGE-A-FREEZE-2026-09", default_policy="unset", held_routes=[], never_pooled=True,
    rule="declared before any repeat group is run (STAGED-EXECUTION-PLAN stage A); `held` only where the Executor records a reason — none recorded; seed_support from EVAL-010 where that evidence names the route, else undocumented", routes=seed_rows)))

# cost totals
def tot(rows):
    d = {}
    for r in rows:
        key = (r["tranche"], r["billing_pool"]); e = d.setdefault(key, dict(calls=0, usd_nominal=0.0, inr_nominal=0.0, unpinned_calls=0, priced_calls=0))
        e["calls"] += r["calls"]
        if r["line_usd"] is None: e["unpinned_calls"] += r["calls"]
        else: e["priced_calls"] += r["calls"]; e["usd_nominal"] += r["line_usd"]; e["inr_nominal"] += (r["line_inr"] or 0)
    return [dict(tranche=k[0], billing_pool=k[1], **{kk: (round(v, 2) if isinstance(v, float) else v) for kk, v in e.items()}) for k, e in sorted(d.items())]
main_rows = [r for r in allrows if not r["conditional"]]; cond_rows = [r for r in allrows if r["conditional"]]
n_img_art = sum(r["calls"] for r in main_rows if r["quantity_unit"] == "images"); n_vid_art = sum(r["calls"] for r in main_rows if r["quantity_unit"] == "seconds")
n_text_vid = sum(r["calls"] for r in main_rows if r["case_id"] == "VID-TOPO3-01")
cv_calls = n_img_art + 4 + 3 * n_vid_art  # +4 composited finals (2 text cases × 2 base draws)
asr_calls = 20 + 12 + 8 + 4 + 12
vlm_calls = n1a + n1b
eval_rows = [dict(instrument="cloud-vision-text-detection", calls=cv_calls, unit_price=EVAL_PRICES["cloud-vision-text-detection"]["price"], line_usd=round(cv_calls * 0.0015, 2), price_status="plan_indicative", price_ref=EVAL_PRICES["cloud-vision-text-detection"]["ref"], billing_pool="credits (GCP) — unverified", tranche="1a+1b", basis=f"{n_img_art} image artifacts + 4 composited finals + 3 frames × {n_vid_art} clips"),
             dict(instrument="asr-vs-script", calls=asr_calls, unit_price=None, line_usd=None, price_status="unpinned", price_ref=EVAL_PRICES["asr-vs-script"]["ref"], billing_pool="unknown", tranche="1a+1b", basis="TTS 20 + T2V-01 12 + 2SPK native 8 + chain lipsync 4 + lipsync 12"),
             dict(instrument="vlm-triage", calls=vlm_calls, unit_price=0.01, line_usd=round(vlm_calls * 0.01, 2), price_status="plan_indicative", price_ref=EVAL_PRICES["vlm-triage"]["ref"], billing_pool="cash (Anthropic/Gemini key)", tranche="1a+1b", basis="one call per artifact"),
             dict(instrument="controller_blind_judging", calls=n1a + n1b + 4, unit_price="≈ 20 s per artifact (plan §E)", line_usd=None, price_status="human_time", price_ref="plan §E", billing_pool="Controller time", tranche="1a+1b", minutes=round((n1a + n1b + 4) * 20 / 60), basis="every artifact + 4 composited finals; identity items take longer (decoy line-ups)")]
totals = dict(by_tranche_and_pool=tot(main_rows), conditional_by_pool=tot(cond_rows),
              nominal_usd_in_cap=round(sum(r["line_usd"] for r in main_rows if r["counted_in_cap"]), 2),
              nominal_usd_cash=round(sum(r["line_usd"] for r in main_rows if r["line_usd"] is not None and r["billing_pool"] == "cash"), 2),
              nominal_usd_credits=round(sum(r["line_usd"] for r in main_rows if r["line_usd"] is not None and r["billing_pool"] == "credits"), 2),
              nominal_inr_sarvam=round(sum(r["line_inr"] or 0 for r in main_rows), 2),
              unpinned_calls_excluded_from_cap=sum(r["calls"] for r in main_rows if r["line_usd"] is None),
              unpinned_routes_excluded=sorted({r["route_key"] for r in main_rows if r["line_usd"] is None}),
              no_access_calls_excluded_from_cap=sum(r["calls"] for r in main_rows if r["route_status"] == "no_access"),
              no_access_routes_excluded=sorted({r["route_key"] for r in main_rows if r["route_status"] == "no_access"}),
              no_access_nominal_inr=round(sum(r["line_inr"] or 0 for r in main_rows if r["route_status"] == "no_access"), 2),
              conditional_nominal_usd=round(sum(r["line_usd"] for r in cond_rows if r["line_usd"] is not None), 2),
              evaluator_nominal_usd=round(sum(r["line_usd"] for r in eval_rows if isinstance(r["line_usd"], float)), 2),
              calls=dict(tranche_1a=n1a, tranche_1b=n1b, total=n1a + n1b, conditional=ncond, task_fixed=dict(tranche_1a=186, tranche_1b=112, total=298, conditional=32)))
tr1a = round(sum(r["line_usd"] for r in main_rows if r["counted_in_cap"] and r["tranche"] == "1a"), 2)
tr1b = round(sum(r["line_usd"] for r in main_rows if r["counted_in_cap"] and r["tranche"] == "1b"), 2)
totals["nominal_usd_1a"] = tr1a; totals["nominal_usd_1b"] = tr1b
open(f"{OUT}/COST-TABLE.yaml", "w", encoding="utf-8").write(HEAD + yd(dict(package="STAGE-A-FREEZE-2026-09", priced_against_roster=PRICED_AGAINST,
    rules=["rows = route × case × arm; calls = items × repeats", "regular prices only; promotions (H3 Max 0.02/s until 7 Sep) recorded in the roster, never used",
           "price_status pinned = the unit price and pin path are taken from EVAL-039B's ROSTER-REFRESH-2026-09.yaml record named in roster_route_key (bytes + sha256 in price-pins-2026-09/PIN-INDEX.yaml) and cross-checked at build time; unpinned = no projectable price in the roster → line_usd null, summed under unpinned_calls_excluded_from_cap",
           "route_status no_access (Sarvam: key present by name, value empty per the roster; the Controller session says present — morning decision 2 / MD-10) → lines shown in INR, excluded from the cap under no_access_calls_excluded_from_cap",
           "pools: Google → Vertex credits; gpt-image-2 / FLUX.2 Pro → Azure credits only if the Controller deploys them, else fal cash (recorded as cash here); Sora 2 / MAI → credits, conditional, excluded; SD3.5 → Bedrock credits, conditional, excluded; fal-only → cash; Sarvam → Sarvam credits (INR); ElevenLabs → cash",
           "i2v / ref2v / 15-s / extend seconds use the roster's pinned variant price for that path (no cross-path assumption remains except Omni Flash's ≤ 15-s ceiling, priced at the pinned 10-s rate × 15 s, and Veo Lite i2v, which has no pinned variant and is unpinned)",
           "quantity rules from the pinned bytes: Kling lipsync bills input seconds rolled up to 5-s increments (6-s or 8-s plate → 10 s); ElevenLabs music bills per output minute rounded up (30-s clip → 1 minute); sync-lipsync bills per output second",
           f"INR→USD display rate {USD_INR_REF} from the August file; Sarvam invoices in INR",
           "the proposed cap covers only counted_in_cap rows; conditional rows and unpinned rows are outside it"],
    totals=totals, evaluator_rows=eval_rows, route_catalogue=catalogue(), roster_cross_check=XCHECK, rows=allrows)))

# ---------------------------------------------------------------- markdown package files
def md_case(c, rec):
    cr = c["customer_request"]; nr = c["nr"]
    L = []
    L.append(f"# {c['case_id']} — {c['lane']} lane, {cr['language']} ({cr['register']})\n")
    L.append("## The request, as the customer sent it\n")
    L.append(f"**Channel:** {cr['channel']} · **Language:** {cr['language']} · **Attachments named:** {', '.join(cr['attachments_named']) or 'none'}\n")
    L.append("> " + cr["text"].replace("\n", "\n> ") + "\n")
    src = c["source"]
    L.append(f"**Source:** pool `{src['pool']}`, id `{src['id']}`" + (f"; secondary `{src['secondary_source']['pool']}:{src['secondary_source']['id']}`" if src.get("secondary_source") else "") + "\n")
    L.append("**Adaptations:**\n")
    for a in src["adaptation"]: L.append(f"- {a}")
    L.append("")
    L.append("## Normalized Request (CANON-010 grammar)\n")
    L.append("| field | value | provenance |\n|---|---|---|")
    pv = nr["provenance"]
    def pfor(name):
        v = pv.get(name) or pv.get(name.split(".")[0]) or "—"
        return v if isinstance(v, str) else f"system_derived — {v['rationale']}"
    def cell(v):
        s = yaml.safe_dump(v, allow_unicode=True, default_flow_style=True, width=10000).strip() if not isinstance(v, str) else v
        return s.replace("|", "\\|").replace("\n", " ")
    for f in ["requested_operation", "modality", "supplied_assets", "mutation_intents", "deliverable_set", "entities", "relationships", "text_requirements", "brand_requirements", "language_topology", "speaker_topology", "temporal_structure", "subject_motion", "camera_motion", "delivery", "ambiguity_markers", "acceptance_intent"]:
        v = nr.get(f)
        if v in (None, [], {}): L.append(f"| {f} | — (absent) | absent |"); continue
        L.append(f"| {f} | {cell(v)} | {pfor(f)} |")
    L.append(f"\n`product_or_packshot_present`: {nr['product_or_packshot_present']} · primary capability `{c['capabilities']['primary']}`\n")
    L.append("## Acceptance contract (judged blind, from the artifact alone)\n")
    for s in c["acceptance_contract"]: L.append(f"- {s}")
    L.append("- Deterministic pre-checks that count as rejects (E5): format probe (container/aspect/resolution/duration/audio-track); baked-text scan on no-text items; duration or aspect mismatch against `delivery`.")
    L.append("")
    L.append("## Routes\n")
    L.append("Routes, arms, tranches and billing quantities are in `TEST-CASES.yaml` → this case's `routes[]` (route facts in `route_catalogue`): " + ", ".join(sorted({r['route_key'] for r in rec['routes']})) + ".\n")
    L.append(f"**Blueprint:** `{rec['blueprint_ref']}` (sha256 `{rec['blueprint_sha256'][:16]}…`, author executor_agent)\n")
    L.append("## Why this shape is real demand\n")
    L.append(c["why_real"] if c.get("why_real") else WHY[c["case_id"]])
    L.append("")
    return "\n".join(L)

WHY = {
 "IMG-CORE-01": "BR-F02-EN is the brief bank's purest packshot: a Mumbai cold-pressed juice brand asking for one clean bottle shot on a light ground for a launch. Its notes say it directly exercises the reflection physics that make glass read as glass — the shape every D2C beverage brand asks for first. The only change is that the label copy goes on in post, which is how launch shots are actually briefed when the label artwork is still with the designer.",
 "IMG-CORE-02": "BR-F03-HG is a Gurugram fintech asking for a young professional with a phone, trustworthy 'like a bank' yet fun for Gen Z — the register tension the bank planted deliberately. Dropping the headline and the app screenshot ('design team baad mein add karegi') is the ordinary way an Indian marketing team briefs a base creative before copy is signed off.",
 "IMG-CORE-03": "BR-F04-HG is a Hyderabad cloud kitchen that wants to look like the top Zomato brands without copying them, at a budget price point, and — like most small Indian food businesses — has no usable photography (the honest condition the bank records under BR-F01-EN). A generated top-view biryani spread with the price and logo added later is exactly what such a kitchen sends its designer.",
 "IMG-CORE-04": "No source pool holds this shape, so it is a labelled fixture: a Hindi children's-story app wanting a picture-book illustration of a sad child at a rainy window. It is the exact scene shape on which the Media Factory prior records a Veo refusal (emotional, stylised, child-like), and Indian kids' content apps commission this shape constantly. The image core needs one item that can trigger a policy refusal, and the market-scene slot is folded into it.",
 "IMG-TEXT-01": "BR-F01-HI is a Jaipur sweet shop's Diwali poster with three exact Devanagari strings, including the conjunct in मिष्ठान, and two real contradictions (offer most important but name biggest; traditional but modern). Festival offer posters are the single most common request small Indian retailers make, and they write them exactly like this.",
 "IMG-TEXT-02": "BR-F01-EN is an Indiranagar gym's New Year offer with three exact Latin strings and brand colours, no people because there are no good photos — the bank's clean baseline for typography-led creatives. Leaving a corner for the logo is how gyms and cafes brief when the logo file lives with someone else.",
 "IMG-EDIT-01": "RX-01 is a Bengaluru furniture retailer asking to remove a staff member from a showroom photo before it goes on the product page tomorrow — the defining single-removal edit where the customer names nothing to keep because everything is implicitly preserved. Retailers send this to designers daily.",
 "IMG-EDIT-02": "RX-02 is an Indore spice brand asking for a white background for an Amazon listing while the printed Devanagari on the pack stays byte-exact. Marketplace listings require white backgrounds, and a damaged matra on a food pack is a real compliance and trust failure — the extension file explains why an English version would not test the same thing.",
 "IMG-EXT-01": "RX-07 is a Kochi travel agency that needs its landscape banner as a 9:16 Story without cropping the boat or the headline. Reformatting one asset for every placement is the most common 'small job' Indian agencies receive, and the customer asked to extend, not to crop.",
 "IMG-COMP-01": "RX-08 is a Delhi cosmetics brand sending a model portrait and a lipstick packshot to be combined, with the face and the signature shade held exactly and a Devanagari headline on top — two identity references and a new relationship in one creative, written in Hinglish with Devanagari copy, which is how such brands actually write.",
 "IMG-REF-01": "BR-F02-HI is a Kanpur mustard-oil brand that wants a clean, trustworthy photo of its yellow 1-litre tin; here the customer sends three phone photos of the tin, which is how a regional FMCG owner actually briefs — 'यही टिन दिखे, कुछ बदले नहीं'. Product identity from the owner's own photographs is the bulk of Indian e-commerce imagery work.",
 "IMG-REF-02": "MKT-009 is an Upwork buyer with a recurring female character who 'must be maintained across all output' — the posting drew 50+ proposals, the strongest demand signal in the marketplace bank. Localised to a Bengaluru content studio with a real recurring host, the still is the first asset such a studio orders.",
 "VID-T2V-01": "BR-F07-HI is a Nashik agri-inputs dealer wanting a farmer speaking one Hindi line to camera with the product in hand — 'simple aur bharosemand'. Testimonial-style talking clips in Hindi are the dominant rural-marketing format; the source flags the efficacy claim and so does this case.",
 "VID-T2V-02": "BR-F06-EN is a Delhi running-shoe brand wanting a real, non-glossy runner with the shoes visible and no dialogue. Compressed to the single sprint beat, it is the high-motion clip every sportswear D2C brand asks for, with the end card and music added by their own editor.",
 "VID-T2V-03": "A labelled fixture: a Hindi kids' story channel wanting an illustrated rain scene where a child is comforted — the Media Factory Veo refusal shape as a text-to-video request. Indian children's-content channels commission emotional illustrated shorts in this exact register; no pool item holds it, so the fixture is declared.",
 "VID-T2V-04": "MKT-012 is an Upwork buyer paying USD 80 fixed for a short cinematic product ad; the product is the same juice bottle as IMG-CORE-01 (BR-F02-EN), so the buyer is the same Mumbai brand following up its still with a 6-second Reels ad. 'Cinematic product ad' is the most-posted paid video shape in the marketplace research.",
 "VID-2SPK-01": "BR-F08-HI is a Jaipur paint brand's husband-and-wife exchange — 'यह रंग कैसा लगेगा?' / 'घर जैसा' — with the pun preserved and the paint can visible. Two-person emotional dialogue is the Indian TV-ad idiom carried into Reels; the customer's own words ('जो बोल रहा है उसी के होंठ हिलें') name the turn-assignment requirement.",
 "VID-KNEE-01": "The same request as VID-T2V-04, run on the cheap and premium tiers so the Controller can see the price ladder on one real buyer's brief rather than on a benchmark prompt.",
 "VID-TOPO3-01": "The same Jaipur sweet shop (BR-F01-HI) asking for its Diwali poster as a 6-second WhatsApp status with the three Devanagari lines held perfectly still and readable — the request that turns a poster into a moving status is asked of every small designer each festival season, and it is the Controller's headline cheap-text topology.",
 "VID-I2V-01": "RX-05 is a premium bottle brand asking for a slow camera move around its packshot with the bottle itself untouched — the cleanest camera-versus-subject separation in the extension. Here it is the juice brand animating its own accepted still for the website hero, which is how the Media Factory plate topology was actually used.",
 "VID-I2V-02": "RX-06 is a Lucknow tea brand asking for a still to become a short clip with a static camera and a slight smile, written in Devanagari. Transposed to the fintech's Hindi page animating its own accepted still, it is the near-static talking-shot plate that every lip-sync job starts from.",
 "VID-I2V-03": "BR-F06-HG is a Mumbai quick-commerce app wanting a fast, snappy clip of a young man reacting and moving — three beats in ten seconds, the tightest compression in the bank. Compressed to one celebration beat on the customer's own accepted still, it is the 'make my photo move, but energetically' request Hinglish-speaking growth teams send.",
 "VID-I2V-04": "A labelled fixture: the kids' story app animating its own accepted illustration of the girl at the rainy window — the exact workflow mode (i2v of an emotional stylised child scene) on which the Media Factory prior records Veo's refusal. Story apps animate their illustrations routinely.",
 "VID-REF-01": "MKT-014 is an Upwork buyer paying USD 10 fixed for 'an AI video ad, produced from images' — the marketplace's clearest statement that buyers expect product video to come from their own photos. Localised to a Jaipur D2C brand sending three photos of its pack, with the tin reference pack shared with IMG-REF-01.",
 "VID-REF-02": "MKT-009 again: the recurring host must be her in every video, 50+ proposals' worth of demand. The Bengaluru studio asks for its host walking into a cafe, camera free — identity from references without a starting frame, which is what distinguishes reference-to-video from i2v.",
 "VID-MS-01": "BR-F10-HG is a Mumbai budget airline's 15-second multi-shot Reel — two friends planning, running through the airport, arriving — written in Hinglish. With VO and end card handled by the customer's editor and the livery constraint dropped (no asset), it is the §C.3d 15-second item on a real buyer's brief.",
 "VID-MS-02": "BR-F10-EN is a Bengaluru mattress brand's problem-then-relief sequence with a dark-to-light lighting arc and the same person in shots one and three. Cut to 10 seconds and three shots, it is the one-person multi-shot control that the 15-second item needs.",
 "AUD-TTS-01": "BR-F05-HI is an Indore detergent brand's ten-second demo whose voice-over line is 'एक धुलाई में दाग गायब'; here the buyer asks for that VO alone, as brands do when the video is cut in-house. A one-line Hindi efficacy VO is the commonest TTS job in regional FMCG.",
 "AUD-TTS-02": "BR-F07-HG is a Noida upskilling platform's Hinglish instructor line with a Devanagari verb inside a Latin sentence — 'Aaj hi enroll करो' — and the bank's energetic-yet-calm tension. Code-mixed VO with a brand name is what edtech brands send to voice studios; the brand name is a labelled fixture.",
 "AUD-TTS-03": "BR-F05-EN is a Chennai electric-scooter brand's three-sentence VO 'Zero petrol. Zero noise. All city.' in a calm male voice; asking for an Indian-English accent is how such brands reject the default Western voice.",
 "AUD-LIP-01": "A labelled fixture consuming two real-demand items: the detergent brand (BR-F05-HI) supplies its VO and a 6-second clip of its presenter (the VID-I2V-02 accepted clip) and asks for the voice to be lip-synced — the Media Factory LatentSync route, which the prior calls the 'best ₹20 shot', and TOPO-01's arm B.",
 "AUD-LIP-02": "A labelled fixture: the Noida platform (BR-F07-HG) sends its instructor clip and Hinglish VO for lip-sync, asking that 'mouth shapes sahi lagni chahiye' on a code-mixed line — the request an edtech brand makes when it has a presenter clip but records the voice separately.",
 "AUD-LIP-03": "A labelled fixture: the scooter brand (BR-F05-EN) sends a presenter clip and its English VO for lip-sync with closed lips in the pauses — the English control for the lip-sync lane.",
 "MUS-01": "BR-F06-HI is an Ahmedabad pressure-cooker brand's demo that wants 'sirf background music aur kitchen ki awaaz'; here the buyer asks for the 30-second bed alone with a light Indian touch, as brands do when the edit is in-house. Music beds for kitchen and home demos are a routine regional ask.",
 "MUS-02": "BR-F06-EN's runner film wants 'just music and ambient sound', real not glossy; here the brand asks for the 30-second bed alone — a minimal building beat that sits under street sound.",
}
for c, rec in zip(CASES, records):
    open(f"{OUT}/test-cases/{c['case_id']}.md", "w", encoding="utf-8").write(md_case(c, rec))

# ACCEPTANCE-CONTRACTS.md
L = ["# Acceptance contracts — Stage A freeze (judged blind, from the artifact alone)\n",
     "Each contract is 3–6 statements a first-language Indian judge can decide from the artifact with no prompt, route name, arm or Canon reference. Phrased `ACCEPT only if …` / `REJECT if …`; no rubric scores, no adjectives without an observable. Every contract ends with the deterministic pre-checks that count as rejects (E5): a format probe (container, aspect, resolution, duration, audio-track presence against `delivery`), the baked-text scan on no-text items, and any duration or aspect mismatch. A refusal, error or blank artifact is a reject counted under E1, never an exclusion.\n",
     "Judging mechanics follow `eval/experiments/EVAL-038/JUDGING-PROTOCOL.md`: stripped artifacts under blinded names, a salted commitment of the key committed before judging, the key off-repo, revealed only after every verdict is committed. Identity contracts are judged as line-ups: the artifact beside the references and the same-category decoys; the judge must pick the referenced identity.\n",
     "Language is never pooled: en, hi and hg verdicts are tallied separately.\n"]
for c in CASES:
    L.append(f"## {c['case_id']} ({c['customer_request']['language']})\n")
    for s in c["acceptance_contract"]: L.append(f"- {s}")
    L.append("- Pre-checks counted as rejects (E5): format probe; " + ("baked-text scan; " if isinstance(c["bp"]["text_handling"], str) and c["bp"]["text_handling"].startswith("none") and c["nr"]["modality"] != "audio" else "") + "duration/aspect mismatch against `delivery`.")
    L.append("")
open(f"{OUT}/ACCEPTANCE-CONTRACTS.md", "w", encoding="utf-8").write("\n".join(L))

# IRREDUCIBILITY.md
CUT = ["Seedance 2.5 on VID-MS-01 (15 s premium)", "Seedance 2.5 on VID-REF-01/02", "Wan 3.0 on VID-I2V-*", "VID-MS-02", "VID-REF-02 Kling-elements arm", "Seedance 2.5 on i2v items", "VID-2SPK-01 chain arm", "MUS-02", "VID-KNEE-01 Veo full tier", "Wan 3.0 on VID-T2V-*"]
L = ["# Irreducibility and cut order — Stage A freeze\n", "One paragraph per case: which routing question (plan §C.1) would go unanswered if it were dropped, and why it cannot merge with its nearest neighbour.\n"]
for c in CASES:
    L.append(f"## {c['irreducibility_ref']} — {c['case_id']}\n"); L.append(c["irreducibility"] + "\n")
L.append("## Cut order if money is short (fixed here, copied verbatim from the task file §C)\n")
for i, s in enumerate(CUT, 1): L.append(f"{i}. {s}")
L.append("\n**Never cut:** repeats, any core item, any Hindi item, TOPO-02/03 arms A and C.\n")
L.append("In `TEST-CASES.yaml` every case carries `cut_order_rank`: an integer = the lowest-numbered cut item that touches the case, with `cut_order_items[]` listing every item and its scope (items 1, 2, 3, 5, 6, 9, 10 remove one route line; 7 removes an arm; 4 and 8 remove the whole case); or `never_cut` with the reason (core item, Hindi/Hinglish item, TOPO-02/03 arms A and C). Cases and ranks: " + "; ".join(f"item {i} → {', '.join(ids)}" for i, (ids, _) in CUT_ITEMS.items()) + ".\n")
open(f"{OUT}/IRREDUCIBILITY.md", "w", encoding="utf-8").write("\n".join(L))

# ELIMINATION-RULES.md
L = ["# Elimination rules — pre-registered before any call (Stage A)\n", "E1–E5 are copied byte-for-byte from `coordination/plans/2026-09-05-CAPABILITY-LAB-CAMPAIGN-v1.md` §C.4:\n"]
L += E_LINES
L += ["", "**Survivor cap:** at most 3 routes per question advance to Stage B (E3).", "",
      "**Proportional rule for routes with fewer core trials (stated before any call):** Seedance 2.5 runs 2 core items × 2 repeats = 4 core trials instead of 8. It is eliminated on the same *proportions*: E1 refusal/hard error on ≥ 3/8 → ≥ 37.5 % (so ≥ 2 of 4); E2 blind acceptance ≤ 2/8 → ≤ 25 % (so ≤ 1 of 4). No threshold is rounded in Seedance's favour.", "",
      "**E5 in this package:** the deterministic pre-checks named at the end of every acceptance contract (format probe, baked-text scan on no-text items, duration/aspect mismatch) are rejects, never exclusions. A refusal or error is counted under E1 and is also a reject for E2's denominator.", "",
      "Elimination is per (route, question) (E4); a route dropped on one question can advance on another. Nothing here is changed mid-run; a change is a new task."]
open(f"{OUT}/ELIMINATION-RULES.md", "w", encoding="utf-8").write("\n".join(L) + "\n")

# COVERAGE-MATRIX.md
c1_rows = ["best commercial still without text", "best product-reference still / best person-reference still", "best supplied-image edit / preservation route", "best exact-text route; when text should be deterministic", "best image-to-video route", "best text-to-video route", "best reference-conditioned video route", "best multi-shot route", "best high-motion / action route", "best native dialogue / audio route", "best Hindi / Hinglish route (COND-LANGUAGE)", "best TTS route", "best lip-sync route", "cheapest acceptable production plate; premium when cheap fails", "model-policy / refusal fallback", "behaviour under reference / constraint / language / motion / delivery load"]
def cases_for_row(row):
    return [c["case_id"] for c in CASES if any(r.startswith(row.split(" (")[0]) for r in c["question_served"]["plan_c1_rows"])]
L = ["# Coverage matrix — Stage A freeze\n", f"35 cases, {n1a + n1b} calls (1a {n1a} / 1b {n1b}) + {ncond} conditional. **4K recorded as a Stage B COND-DELIVERY level only; round one runs 720p.**\n",
     "## 1. Plan §C.1 routing questions → cases\n", "| routing question (plan §C.1) | cases |\n|---|---|"]
for row in c1_rows:
    ids = cases_for_row(row)
    if row.startswith("behaviour under"): ids = ["Stage B sweeps (survivors only); Stage A records every family on every row"]
    L.append(f"| {row} | {', '.join(ids)} |")
L.append("| VID-04 edit existing footage (Runway Aleph) | deferred_no_account — Controller decision 5 |")
L += ["", "## 2. Roster questions (SCIENTIFIC-WAVE1-MODEL-ROSTER) → cases\n", "| question | cases |\n|---|---|"]
for q in ["IMG-01", "IMG-02", "IMG-03", "IMG-04", "VID-01", "VID-02", "VID-03", "VID-04", "VID-05", "AUD-01", "AUD-02", "AUD-03"]:
    ids = [c["case_id"] for c in CASES if any(r.startswith(q) for r in c["question_served"]["roster_questions"])]
    L.append(f"| {q} | {', '.join(ids) if ids else 'deferred_no_account (Runway)'} |")
L += ["", "## 3. §C.3d additions\n",
      "- one 15-second item: **VID-MS-01** (Kling v3 15 s, Seedance 2.5 15 s, Omni Flash 1.1 longest ≤ 15 s, Veo 3.1 fast + extend; 4 routes × 2 = 8 calls)",
      "- one two-speaker Hindi dialogue item: **VID-2SPK-01** — native arm (Veo 3.1 fast, Kling v3, Omni Flash 1.1, Seedance 2.5; 8 calls) and chain arm (plate 2 + i2v 2 + TTS 8 [counted under TTS] + lipsync 4 = 8 chain calls + 8 TTS)",
      "- music lane: **MUS-01**, **MUS-02** × 2 routes (Lyria on Vertex, ElevenLabs music on fal) × 2 repeats = 8 calls",
      "- 4K: **not a case.** 4K recorded as a Stage B COND-DELIVERY level only; round one runs 720p.", "",
      "## 4. Core counts and per-core requirements\n", "| core | count | cases | Hindi/Hinglish | policy-edge | high-motion |\n|---|---|---|---|---|---|",
      "| image | 4 | IMG-CORE-01..04 | IMG-CORE-02 (hg), IMG-CORE-04 (hi) | IMG-CORE-04 | n/a |",
      "| text-to-video | 4 | VID-T2V-01..04 | VID-T2V-01 (hi), VID-T2V-03 (hg) | VID-T2V-03 | VID-T2V-02 |",
      "| image-to-video | 4 | VID-I2V-01..04 | VID-I2V-02 (hi), VID-I2V-04 (hi), VID-I2V-03 (hg) | VID-I2V-04 | VID-I2V-03 |",
      "| TTS | 3 | AUD-TTS-01..03 | AUD-TTS-01 (hi), AUD-TTS-02 (hg) | waived — a TTS policy-edge has no source shape and no prior; stated | n/a |",
      "| lipsync | 3 | AUD-LIP-01..03 | AUD-LIP-01 (hi), AUD-LIP-02 (hg) | waived — as TTS; stated | n/a |", "",
      "## 5. TOPO-02 / TOPO-03 arms\n", "| topology | arm A | arm B | arm C |\n|---|---|---|---|",
      "| TOPO-02 IMG-TEXT-01 (hi) | NB2, Qwen Image 3, GPT Image 2 — 3 × 2 = 6 | NB Pro, Seedream 5 Pro, Recraft V4 — 3 × 2 = 6 | FLUX.2 Pro textless base × 2 + overlay by code (USD 0) |",
      "| TOPO-02 IMG-TEXT-02 (en) | same routes, 6 | same routes, 6 | same, 2 + overlay |",
      "| TOPO-03 VID-TOPO3-01 (hi) | IMG-TEXT-01 arm-A accepted still → H3 Max, Wan 3.0, Veo 3.1 lite i2v — 3 × 2 = 6 (1b) | Veo 3.1 full, Kling v3 native t2v — 2 × 2 = 4 (1a) | IMG-TEXT-01 arm-C base → Veo 3.1 lite i2v × 2 (1b) + tracked/static overlay by code |", "",
      "## 6. Media Factory freshness items → cases\n", "| prior item | cases |\n|---|---|",
      "| 1 Veo policy behaviour on the emotional stylised child scene | VID-I2V-04, VID-T2V-03 (and IMG-CORE-04 as the still) |",
      "| 2 Seedance 2.x cost/quality position | every Seedance 2.5 line: VID-T2V-01/02, VID-I2V-02/03, VID-REF-01/02, VID-MS-01 |",
      "| 3 in-scene text through motion (composite-always for video) | VID-TOPO3-01 |",
      "| 4 multi-turn dialogue and voice consistency | VID-2SPK-01 |",
      "| 5 LatentSync-class mouth repaint vs native lip-sync | AUD-LIP-01/02/03 (+ VID-2SPK-01 chain arm) |", "",
      "## 7. `requested_operation` coverage\n", "| operation | cases | note |\n|---|---|---|",
      "| generate | IMG-CORE-*, IMG-TEXT-*, IMG-REF-*, VID-T2V-*, VID-2SPK-01, VID-KNEE-01, VID-TOPO3-01, VID-REF-*, VID-MS-*, AUD-TTS-*, MUS-* | |",
      "| edit | IMG-EDIT-01, IMG-EDIT-02 | |", "| animate | VID-I2V-01..04 | |", "| extend | IMG-EXT-01 | |", "| compose | IMG-COMP-01, AUD-LIP-01..03 | |",
      "| restore | — | **omitted with reason:** no restore route in the plan §C.3 slate (RX-04's 1961 photograph shape has no screened route) |",
      "| variants | — | **omitted with reason:** variant-set acceptance is outcome-level (COND-SCALE note) → Stage C; RX-09's Tamil/Bengali scripts have no benchmark-grade instrument |", "",
      "## 8. Language mix (counts by lane)\n", "| lane | en | hi | hg | total |\n|---|---|---|---|---|"]
for lane, d in lane_lang.items(): L.append(f"| {lane} | {d['en']} | {d['hi']} | {d['hg']} | {sum(d.values())} |")
L.append(f"| **all** | {langs['en']} | {langs['hi']} | {langs['hg']} | 35 |")
L.append(f"\nHindi + Hinglish = {langs['hi'] + langs['hg']}/35 = {round(100 * (langs['hi'] + langs['hg']) / 35)} % (target ≥ 40 %).\n")
L += ["## 9. Benchmark vocabulary\n", "No `customer_request.text` contains `probe`, `capability`, `benchmark`, `isolated`, `level 1` or `condition` (checked by grep in the Executor's self-check; the Tester re-runs it)."]
open(f"{OUT}/COVERAGE-MATRIX.md", "w", encoding="utf-8").write("\n".join(L) + "\n")

# README.md
from readme import README
open(f"{OUT}/README.md", "w", encoding="utf-8").write(README(counts, totals, tr1a, tr1b, ROSTER is not None, fixtures, langs, lane_lang))
print("DONE", OUT)
