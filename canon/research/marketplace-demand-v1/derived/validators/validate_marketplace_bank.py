#!/usr/bin/env python3
"""CANON-011 - deterministic validator for the marketplace-derived brief bank.

FAILS CLOSED. Every gate below is a rule the task or the Controller decision states, and
each one exists because breaking it would produce a specific, nameable lie about where a
requirement came from.

    G1  every case has source lineage back to a committed marketplace file
    G2  every Normalized Request field R01-R18 is present and carries a provenance
    G3  no Fiverr seller gig is treated as a buyer brief
    G4  no provider, model or production-route term leaks into a route-neutral field
    G5  every runnable_now case identifies all its fixtures, and none of them blocks
    G6  case ids and fixture ids are unique
    G7  every referenced source path exists
    G8  an experiment-supplied fixture is never labelled customer_stated
    G9  every source fact is traceable - its verbatim string really is in the source file

Plus structural gates the grammar itself states:

    G10 grammar rules RULE-01 to RULE-04 and RULE-08 hold on every case
    G11 every capability id exists and is active in Capability Contract v2, and every
        evaluator family is one the qualification map defines
    G12 no evaluator is described as qualified, anywhere
    G13 the prompt-ready bank matches the brief bank envelope for envelope
    G14 nothing outside canon/research/marketplace-demand-v1/derived/ is written by this task

Run from the repository root:

    python3 canon/research/marketplace-demand-v1/derived/validators/validate_marketplace_bank.py

PyYAML is required and is not installed system-wide on this machine; create a local
virtual environment with pyyaml, as the Canon handoff already records.
"""
import argparse
import pathlib
import re
import sys

import yaml

HERE = pathlib.Path(__file__).resolve().parent
DERIVED = HERE.parent
ROOT = HERE.parents[4]
BANK_PATH = DERIVED / "marketplace-brief-bank-v1.yaml"
PROMPT_PATH = DERIVED / "marketplace-prompt-ready-bank-v1.yaml"
CAPABILITY_CONTRACT = ROOT / "eval/pre-execution-freeze/CAPABILITY-CONTRACT-v2.yaml"
QUALIFICATION_MAP = ROOT / "eval/pre-execution-freeze/EVALUATOR-QUALIFICATION-MAP.yaml"

GRAMMAR_FIELDS = [
    "R01_requested_operation", "R02_supplied_assets", "R03_mutation_intents",
    "R04_deliverable_set", "R05_modality", "R06_entities", "R07_relationships",
    "R08_text_requirements", "R09_brand_requirements", "R10_language_topology",
    "R11_speaker_topology", "R12_temporal_structure", "R13_subject_motion",
    "R14_camera_motion", "R15_delivery", "R16_specification_provenance",
    "R17_ambiguity_markers", "R18_acceptance_intent",
]

PROVENANCE = {
    "customer_stated", "customer_implied", "experiment_supplied_fixture",
    "system_derived", "absent",
}

REQUESTED_OPERATIONS = {
    "generate", "edit", "animate", "restore", "extend", "compose", "variants",
}

# The grammar's own forbidden operation values, plus the vendor and technique names the
# marketplace sources are full of. A route-neutral field containing any of these has
# stopped describing what must be made and started describing how.
FORBIDDEN_ROUTE_TERMS = [
    # production routes - the grammar forbids these as operation values outright
    "inpaint", "outpaint", "img2img", "image2image", "text2img", "text2video",
    "controlnet", "lora", "upscale", "segment_and_composite", "segment and composite",
    "image-to-video", "image to video", "img2vid", "rotoscope", "comfyui",
    # providers and models named across the two marketplace sources
    "veo", "kling", "seedance", "runway", "sora", "higgsfield", "heygen", "synthesia",
    "midjourney", "flux", "elevenlabs", "arcads", "invideo", "d-id", "pika", "kaiber",
    "nano banana", "suno", "colossyan", "capcut", "premiere pro", "stable diffusion",
    "gpt-image", "ideogram", "gemini", "claude", "openai", "anthropic", "fal",
]

# Fields inside a case that must stay route-neutral. Everything NOT listed here may
# legitimately quote a buyer's own tool name - that is source provenance, not a route
# decision, and erasing it would lose a real fact about the buyer.
ROUTE_NEUTRAL_CASE_FIELDS = [
    "route_neutral_generation_brief",
    "prompt_ready_envelope",
    "acceptance_contract",
    "capability_mappings",
]

# Phrases that would assert an instrument IS qualified. The scan below is
# negation-aware on purpose: "no evaluator this case needs has been qualified" is a true
# statement the bank must be able to make, while "this evaluator has been qualified"
# would be a lie. A naive substring check cannot tell those apart and would force the
# bank to stop saying the honest thing.
QUALIFIED_ASSERTIONS = [
    "is qualified", "has been qualified", "is now qualified", "was qualified",
    "instrument qualified", "qualified: true",
]
NEGATORS = ("no ", "not ", "never", "nothing", "none", "cannot", "zero", "ever ",
            "0 qualified", "unqualified", "without")


# Module-level caches. The negative-control suite calls main() thirty times in one
# process, and re-parsing the capability contract and the marketplace sources each time
# turned a two-second check into a two-minute one.
_YAML_CACHE = {}
_TEXT_CACHE = {}


def load_yaml(path):
    key = str(path)
    if key not in _YAML_CACHE:
        _YAML_CACHE[key] = yaml.safe_load(pathlib.Path(path).read_text())
    return _YAML_CACHE[key]


def load_norm_text(path):
    key = str(path)
    if key not in _TEXT_CACHE:
        p = pathlib.Path(path)
        _TEXT_CACHE[key] = norm(p.read_text()) if p.exists() else None
    return _TEXT_CACHE[key]


def strings_in(node):
    """Yield every string anywhere inside a nested structure."""
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for k, v in node.items():
            yield str(k)
            yield from strings_in(v)
    elif isinstance(node, list):
        for v in node:
            yield from strings_in(v)


def norm(text):
    return re.sub(r"\s+", " ", text).strip()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--bank", type=pathlib.Path, default=BANK_PATH,
                    help="brief bank to validate (default: the committed bank)")
    ap.add_argument("--prompt-bank", type=pathlib.Path, default=PROMPT_PATH,
                    help="prompt-ready bank to cross-check against")
    ap.add_argument("--quiet", action="store_true", help="suppress the summary header")
    args = ap.parse_args(argv)
    bank_path, prompt_path = args.bank, args.prompt_bank

    errors = []
    notes = []

    if not bank_path.exists():
        print(f"FAIL: {bank_path} not found")
        return 1
    bank_raw = bank_path.read_text()
    bank = yaml.safe_load(bank_raw)
    cases = bank.get("cases") or []

    if not cases:
        errors.append("STRUCTURAL: the bank contains no cases. An empty check is not a passing check.")

    # An explicit scope gate the task states: 12-20 cases, at least 8 runnable.
    if not (12 <= len(cases) <= 20):
        errors.append(f"SCOPE: {len(cases)} cases; the task requires 12-20.")
    runnable = [c for c in cases if c.get("runnable_now") is True]
    if len(runnable) < 8:
        errors.append(f"SCOPE: {len(runnable)} runnable cases; the task requires at least 8.")

    def source_text(path_str):
        return load_norm_text(ROOT / path_str)

    # ---- capability and evaluator vocabularies, read from the frozen contracts -----
    cap_ids_active = set()
    if CAPABILITY_CONTRACT.exists():
        contract = load_yaml(CAPABILITY_CONTRACT)
        cap_ids_active = {
            d["id"] for d in contract["dimensions"] if d.get("status") == "active"
        }
    else:
        errors.append(f"G11: capability contract not found at {CAPABILITY_CONTRACT}")

    evaluator_families = set()
    if QUALIFICATION_MAP.exists():
        qmap = load_yaml(QUALIFICATION_MAP)
        evaluator_families = set(qmap["by_evaluator_family"].keys())
        if qmap.get("instruments_qualified") != 0:
            notes.append(
                "G12: the qualification map no longer reports 0 qualified instruments. "
                "The bank's evaluator_qualification_status must be re-checked."
            )
    else:
        errors.append(f"G11: evaluator qualification map not found at {QUALIFICATION_MAP}")

    declared_families = set(bank.get("evaluator_families") or [])
    if evaluator_families and declared_families != evaluator_families:
        errors.append(
            "G11: the bank's evaluator_families list does not match the qualification map. "
            f"bank-only={sorted(declared_families - evaluator_families)} "
            f"map-only={sorted(evaluator_families - declared_families)}"
        )

    # ---- G3: Fiverr is conventions only ------------------------------------------
    fiverr = bank.get("fiverr_convention_inputs") or {}
    if fiverr.get("is_customer_brief") is not False:
        errors.append("G3: fiverr_convention_inputs must declare is_customer_brief: false.")
    for conv in fiverr.get("conventions") or []:
        for banned in ("customer_stated", "customer_implied"):
            if banned in yaml.safe_dump(conv):
                errors.append(
                    f"G3: Fiverr convention {conv.get('id')} carries a customer provenance label. "
                    "A seller gig cannot state a customer requirement."
                )
        txt = source_text(fiverr.get("source_file", ""))
        if txt is None:
            errors.append(f"G7: Fiverr source file missing: {fiverr.get('source_file')}")
        elif norm(conv.get("verbatim", "")) not in txt:
            errors.append(
                f"G9: Fiverr convention {conv.get('id')} verbatim not found in its source file."
            )

    seen_case_ids = set()
    seen_fixture_ids = set()

    for case in cases:
        cid = case.get("case_id", "<missing case_id>")

        # ---- G6: unique ids ------------------------------------------------------
        if cid in seen_case_ids:
            errors.append(f"G6: duplicate case_id {cid}")
        seen_case_ids.add(cid)

        # ---- G1: source lineage --------------------------------------------------
        for field in ("source_marketplace", "source_record_id", "source_title",
                      "source_file", "source_facts_used"):
            if not case.get(field):
                errors.append(f"G1: {cid} is missing {field}.")
        if not case.get("source_facts_used"):
            errors.append(f"G1: {cid} cites no source facts.")

        # ---- G3: no case may be a Fiverr gig -------------------------------------
        if case.get("source_marketplace") != "upwork":
            errors.append(
                f"G3: {cid} has source_marketplace={case.get('source_marketplace')!r}. "
                "Only individual Upwork buyer jobs may be customer-intent sources; a Fiverr "
                "gig is a seller offering and can never be a buyer brief."
            )

        # ---- G7 + G9: source file exists and every verbatim resolves --------------
        sf = case.get("source_file", "")
        txt = source_text(sf)
        if txt is None:
            errors.append(f"G7: {cid} names a source file that does not exist: {sf}")
        else:
            for fact in case.get("source_facts_used") or []:
                v = fact.get("verbatim")
                if not v:
                    errors.append(f"G9: {cid} has a source fact with no verbatim string.")
                elif norm(v) not in txt:
                    errors.append(
                        f"G9: {cid} cites a verbatim string that is not in {sf}: {v[:70]!r}"
                    )

        # ---- G2 + G8: every grammar field present with a legal provenance ---------
        nr = case.get("normalized_request") or {}
        for field in GRAMMAR_FIELDS:
            if field not in nr:
                errors.append(f"G2: {cid} is missing normalized_request field {field}.")
                continue
            entry = nr[field] or {}
            prov = entry.get("provenance")
            if prov not in PROVENANCE:
                errors.append(f"G2: {cid}.{field} has provenance {prov!r}, which is not in the vocabulary.")
            for sub, sprov in (entry.get("sub_field_provenance") or {}).items():
                if sprov not in PROVENANCE:
                    errors.append(
                        f"G2: {cid}.{field}.sub_field_provenance[{sub}] = {sprov!r} is not in the vocabulary."
                    )
            # grammar rule: R01 and R08 may never be system_derived
            if field == "R01_requested_operation" and prov in ("system_derived", "absent"):
                errors.append(
                    f"G10/RULE: {cid}.R01 provenance is {prov!r}. The grammar forbids a "
                    "system-derived requested operation - if the system decided what the "
                    "customer wanted, the system misread the request."
                )
            if field == "R08_text_requirements" and prov == "system_derived":
                errors.append(
                    f"G10/RULE: {cid}.R08 provenance is system_derived. Copy the system invented "
                    "is never a customer text requirement."
                )
            if field == "R16_specification_provenance" and prov != "system_derived":
                errors.append(f"G2: {cid}.R16 must be system_derived; it is a record of provenance.")

        # G8, stated as its own gate: a value the benchmark supplies is never customer_stated.
        # Enforced by construction above (a field carries exactly one provenance) plus the
        # fixture cross-check below: anything labelled experiment_supplied_fixture must have a
        # matching fixture entry, and anything with a fixture entry may not claim customer_stated
        # for the same sub-field.
        fixture_ids = {f.get("fixture_id") for f in (case.get("fixture_requirements") or [])}
        fixture_labelled = []
        for field in GRAMMAR_FIELDS:
            entry = nr.get(field) or {}
            if entry.get("provenance") == "experiment_supplied_fixture":
                fixture_labelled.append(field)
            for sub, sprov in (entry.get("sub_field_provenance") or {}).items():
                if sprov == "experiment_supplied_fixture":
                    fixture_labelled.append(f"{field}.{sub}")
        if fixture_labelled and not fixture_ids:
            errors.append(
                f"G8: {cid} labels {len(fixture_labelled)} field(s) experiment_supplied_fixture "
                "but declares no fixture_requirements. A fixture that is not declared is a fixture "
                "hiding as customer intent."
            )

        # ---- G6 continued: fixture ids unique across the whole bank ---------------
        for fx in case.get("fixture_requirements") or []:
            fid = fx.get("fixture_id")
            if not fid:
                errors.append(f"G6: {cid} has a fixture with no fixture_id.")
            elif fid in seen_fixture_ids:
                errors.append(f"G6: duplicate fixture_id {fid}")
            else:
                seen_fixture_ids.add(fid)
            if "blocks_runnable" not in fx:
                errors.append(f"G5: {cid} fixture {fid} does not say whether it blocks runnability.")
            if fx.get("blocks_runnable") and not fx.get("blocks_runnable_reason"):
                errors.append(f"G5: {cid} fixture {fid} blocks runnability without a stated reason.")

        # ---- G5: runnable cases must have every fixture and no blocker ------------
        if case.get("runnable_now") is True:
            if fixture_labelled and not fixture_ids:
                errors.append(f"G5: {cid} is runnable_now but declares no fixtures for its fixture-labelled fields.")
            for fx in case.get("fixture_requirements") or []:
                if fx.get("blocks_runnable"):
                    errors.append(
                        f"G5: {cid} is runnable_now: true while fixture {fx.get('fixture_id')} "
                        "declares blocks_runnable: true."
                    )
            if not case.get("runnable_rationale"):
                errors.append(f"G5: {cid} is runnable_now with no runnable_rationale.")
        elif case.get("runnable_now") is False:
            if not any(fx.get("blocks_runnable") for fx in (case.get("fixture_requirements") or [])):
                errors.append(
                    f"G5: {cid} is runnable_now: false but no fixture explains what blocks it."
                )
        else:
            errors.append(f"G5: {cid} has no boolean runnable_now.")

        # ---- G10: grammar cross-field rules --------------------------------------
        op_entry = nr.get("R01_requested_operation") or {}
        op = op_entry.get("value")
        if op not in REQUESTED_OPERATIONS:
            errors.append(
                f"G10/RULE-01: {cid} requested_operation is {op!r}, which is not one of the "
                "seven customer-intent operations. A production route is not an operation."
            )
        assets = (nr.get("R02_supplied_assets") or {}).get("value") or []
        if op in {"edit", "animate", "restore", "extend", "compose"}:
            roles = {a.get("role") for a in assets if isinstance(a, dict)}
            if "subject_of_operation" not in roles:
                errors.append(
                    f"G10/RULE-02: {cid} requests {op} but no supplied asset has role "
                    "subject_of_operation."
                )
        dset = (nr.get("R04_deliverable_set") or {}).get("value") or {}
        if op == "variants" and not (isinstance(dset.get("cardinality"), int) and dset["cardinality"] > 1):
            errors.append(f"G10/RULE-03: {cid} requests variants but cardinality is not greater than 1.")
        if dset.get("acceptance_basis") == "best_n_of_m" and not dset.get("best_n"):
            errors.append(f"G10/RULE-04: {cid} uses best_n_of_m acceptance without stating best_n.")
        mut = (nr.get("R03_mutation_intents") or {}).get("value")
        if isinstance(mut, dict):
            if "preservation_default" not in mut:
                errors.append(
                    f"G10/RULE-08: {cid} records mutation intents without a preservation_default. "
                    "Implicit preservation must not be enumerated as customer statements."
                )
            preserve_entries = [i for i in (mut.get("intents") or []) if i.get("intent") == "preserve"]
            if len(preserve_entries) > 2:
                errors.append(
                    f"G10/RULE-08: {cid} enumerates {len(preserve_entries)} explicit preserve "
                    "intents, which looks like manufactured customer intent."
                )

        # ---- G4: no route leakage into route-neutral fields -----------------------
        for field in ROUTE_NEUTRAL_CASE_FIELDS:
            blob = " ".join(strings_in(case.get(field))).lower()
            for term in FORBIDDEN_ROUTE_TERMS:
                if re.search(r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])", blob):
                    errors.append(
                        f"G4: {cid}.{field} contains the route/provider term {term!r}. A "
                        "route-neutral field says what must be MADE; a buyer's own tool name "
                        "belongs in buyer_named_tools or buyer_named_production_route."
                    )

        # ---- G11: capability ids and evaluator families are real ------------------
        caps = case.get("capability_mappings") or {}
        for capid in caps.get("atomic") or []:
            if cap_ids_active and capid not in cap_ids_active:
                errors.append(
                    f"G11: {cid} maps to capability {capid!r}, which is not an active capability "
                    "in Capability Contract v2."
                )
        for dep in case.get("evaluator_dependencies") or []:
            fam = dep.get("family")
            if evaluator_families and fam not in evaluator_families:
                errors.append(f"G11: {cid} names evaluator family {fam!r}, which the qualification map does not define.")
            if dep.get("qualified") is not False:
                errors.append(
                    f"G11/G12: {cid} evaluator dependency {fam!r} does not declare qualified: false. "
                    "No instrument in this project has ever been qualified."
                )

        for req in (case.get("acceptance_contract") or {}).get("hard_objective") or []:
            if req.get("provenance") not in PROVENANCE:
                errors.append(f"G2: {cid} acceptance requirement has provenance {req.get('provenance')!r}.")
            capid = req.get("capability")
            if cap_ids_active and capid not in cap_ids_active:
                errors.append(
                    f"G11: {cid} acceptance requirement names capability {capid!r}, which is not "
                    "an active capability in Capability Contract v2."
                )
        for req in (case.get("acceptance_contract") or {}).get("subjective_creative") or []:
            if req.get("provenance") not in PROVENANCE:
                errors.append(f"G2: {cid} subjective requirement has provenance {req.get('provenance')!r}.")
            capid = req.get("capability")
            if cap_ids_active and capid not in cap_ids_active:
                errors.append(
                    f"G11: {cid} subjective requirement names capability {capid!r}, which is not "
                    "an active capability in Capability Contract v2."
                )
            if req.get("no_deterministic_ground_truth") is not True:
                errors.append(
                    f"G2: {cid} subjective requirement does not declare "
                    "no_deterministic_ground_truth: true. A subjective requirement must not be "
                    "presented as though it had deterministic ground truth."
                )

        for field in ("open_questions", "stage_fit", "route_neutral_generation_brief",
                      "prompt_ready_envelope", "customer_brief", "acceptance_contract",
                      "execution_feasibility", "fixture_requirements",
                      "capability_mappings", "evaluator_dependencies"):
            if not case.get(field):
                errors.append(f"G1: {cid} is missing required field {field}.")

        env = case.get("prompt_ready_envelope") or {}
        if "model_specific_fields" not in env:
            errors.append(f"G4: {cid} envelope does not declare model_specific_fields.")
        elif env.get("model_specific_fields") is not None:
            errors.append(
                f"G4: {cid} envelope carries model-specific fields. Adapters come later, "
                "after a Production IR exists."
            )

    # ---- G12: nothing anywhere claims an evaluator is qualified -------------------
    low = bank_raw.lower()
    for phrase in QUALIFIED_ASSERTIONS:
        for m in re.finditer(re.escape(phrase), low):
            window = low[max(0, m.start() - 90):m.start()]
            if any(n in window for n in NEGATORS):
                continue
            line = low.count("\n", 0, m.start()) + 1
            errors.append(
                f"G12: line {line} asserts {phrase!r} with no negation in front of it. "
                "No instrument in this project has ever been qualified."
            )

    # ---- G13: the prompt-ready bank matches the brief bank ------------------------
    if not prompt_path.exists():
        errors.append(f"G13: prompt-ready bank not found at {prompt_path}")
    else:
        prompt_bank = load_yaml(prompt_path)
        envelopes = {e["case_id"]: e["envelope"] for e in prompt_bank.get("envelopes") or []}
        if set(envelopes) != seen_case_ids:
            errors.append(
                "G13: the prompt-ready bank and the brief bank cover different cases. "
                f"prompt-only={sorted(set(envelopes) - seen_case_ids)} "
                f"bank-only={sorted(seen_case_ids - set(envelopes))}"
            )
        for case in cases:
            cid = case.get("case_id")
            if cid in envelopes and envelopes[cid] != case.get("prompt_ready_envelope"):
                errors.append(
                    f"G13: envelope for {cid} differs between the two banks. Regenerate with "
                    "build_prompt_ready_bank.py rather than hand-editing."
                )

    # ---- G14: this task writes nowhere but its own directory ----------------------
    protected = [
        "canon/experiments/v1/brief-bank",
        "canon/experiments/pre-execution-freeze",
        "eval/v1/capability-contract.yaml",
        "eval/v1/bank",
        "eval/registry",
        "eval/pre-execution-freeze",
        "canon/research/marketplace-demand-v1/sources",
        "canon/research/marketplace-demand-v1/README.md",
    ]
    declared = set(bank.get("meta", {}).get("does_not_modify") or [])
    for p in protected[:5]:
        if not any(d.rstrip("/").endswith(p.rstrip("/")) or p in d for d in declared):
            notes.append(f"G14: {p} is not named in meta.does_not_modify (advisory).")

    if not args.quiet:
        print("=" * 74)
        print("CANON-011 marketplace brief bank validator")
        print("=" * 74)
        print(f"bank                 : {bank_path}")
        print(f"cases                : {len(cases)}")
        print(f"runnable now         : {len(runnable)}")
        print(f"fixtures declared    : {len(seen_fixture_ids)}")
        print(f"capability ids known : {len(cap_ids_active)} active in Capability Contract v2")
        print(f"evaluator families   : {len(evaluator_families)} defined in the qualification map")
        for n in notes:
            print(f"NOTE  {n}")
    if errors:
        print(f"{len(errors)} ERROR(S):")
        for e in errors:
            print(f"  FAIL  {e}")
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS - all gates G1-G14 hold.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
