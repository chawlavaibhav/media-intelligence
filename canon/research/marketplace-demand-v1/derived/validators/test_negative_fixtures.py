#!/usr/bin/env python3
"""CANON-011 - negative controls for validate_marketplace_bank.py.

WHY THIS FILE EXISTS. This project has already paid for the lesson: a validator tested
only on correct input proves nothing, and negative-control fixtures immediately exposed
three real defects in an earlier harness, none of which was visible from reading the
code. The same lesson supplies the second rule applied here - an empty check is not a
passing check - so this file fails if any gate turns out to be unreachable.

WHAT IT DOES. For each gate it takes the real committed bank, breaks exactly one thing,
runs the validator against the broken copy, and requires it to FAIL with that gate named.
It then runs the unmodified bank and requires a PASS, so a validator that simply rejects
everything cannot pass this suite either.

Run from the repository root:

    python3 canon/research/marketplace-demand-v1/derived/validators/test_negative_fixtures.py
"""
import copy
import io
import pathlib
import sys
import tempfile
from contextlib import redirect_stdout

import yaml

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import validate_marketplace_bank as V  # noqa: E402

BANK = yaml.safe_load(V.BANK_PATH.read_text())


def run_on(bank_doc, prompt_path=None):
    """Write bank_doc to a temp file, validate it, return (exit_code, output)."""
    with tempfile.TemporaryDirectory() as td:
        p = pathlib.Path(td) / "bank.yaml"
        p.write_text(yaml.safe_dump(bank_doc, sort_keys=False, allow_unicode=True))
        argv = ["--bank", str(p), "--quiet"]
        if prompt_path is not None:
            argv += ["--prompt-bank", str(prompt_path)]
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = V.main(argv)
        return code, buf.getvalue()


def mutate(fn):
    b = copy.deepcopy(BANK)
    fn(b)
    return b


# --- each entry: (gate label, description, mutation) -------------------------------

def _drop_source_facts(b):
    b["cases"][0].pop("source_facts_used")


def _bad_provenance(b):
    b["cases"][0]["normalized_request"]["R05_modality"]["provenance"] = "probably"


def _fiverr_as_buyer_brief(b):
    b["cases"][0]["source_marketplace"] = "fiverr"


def _fiverr_convention_claims_customer(b):
    b["fiverr_convention_inputs"]["conventions"][0]["provenance"] = "customer_stated"


def _route_leak_into_brief(b):
    b["cases"][0]["route_neutral_generation_brief"] += "\nUse Veo 3 for the product shots."


def _route_leak_into_envelope(b):
    b["cases"][0]["prompt_ready_envelope"]["visual_tone"] = "cinematic, via img2img"


def _runnable_with_blocking_fixture(b):
    c = next(x for x in b["cases"] if x["runnable_now"] is True)
    c["fixture_requirements"][0]["blocks_runnable"] = True
    c["fixture_requirements"][0]["blocks_runnable_reason"] = "test fixture"


def _duplicate_case_id(b):
    b["cases"][1]["case_id"] = b["cases"][0]["case_id"]


def _duplicate_fixture_id(b):
    a = next(x for x in b["cases"] if x.get("fixture_requirements"))
    other = next(x for x in b["cases"][1:] if x.get("fixture_requirements") and x is not a)
    other["fixture_requirements"][0]["fixture_id"] = a["fixture_requirements"][0]["fixture_id"]


def _missing_source_file(b):
    b["cases"][0]["source_file"] = "canon/research/marketplace-demand-v1/sources/does-not-exist.md"


def _fixture_without_declaration(b):
    c = next(x for x in b["cases"] if x.get("fixture_requirements"))
    c["fixture_requirements"] = []
    c["runnable_now"] = True


def _fixture_relabelled_as_customer_stated(b):
    """The exact lie gate 8 exists to catch: a benchmark-supplied value claimed as the
    customer's, with the fixture declaration deleted so nothing contradicts it."""
    c = b["cases"][0]
    c["normalized_request"]["R15_delivery"]["provenance"] = "customer_stated"
    c["normalized_request"]["R15_delivery"].pop("sub_field_provenance", None)
    c["fixture_requirements"] = []


def _untraceable_verbatim(b):
    b["cases"][0]["source_facts_used"][0]["verbatim"] = "the buyer asked for a 90 second ad"


def _production_route_as_operation(b):
    b["cases"][0]["normalized_request"]["R01_requested_operation"]["value"] = "inpaint"


def _system_derived_operation(b):
    b["cases"][0]["normalized_request"]["R01_requested_operation"]["provenance"] = "system_derived"


def _system_derived_text_requirement(b):
    b["cases"][0]["normalized_request"]["R08_text_requirements"]["provenance"] = "system_derived"


def _edit_without_subject_of_operation(b):
    c = next(x for x in b["cases"]
             if x["normalized_request"]["R01_requested_operation"]["value"] == "edit")
    for a in c["normalized_request"]["R02_supplied_assets"]["value"]:
        if a.get("role") == "subject_of_operation":
            a["role"] = "identity_reference"


def _variants_without_a_set(b):
    c = next(x for x in b["cases"]
             if x["normalized_request"]["R01_requested_operation"]["value"] == "variants")
    c["normalized_request"]["R04_deliverable_set"]["value"]["cardinality"] = 1


def _enumerated_implicit_preservation(b):
    c = next(x for x in b["cases"]
             if isinstance(x["normalized_request"]["R03_mutation_intents"].get("value"), dict))
    c["normalized_request"]["R03_mutation_intents"]["value"]["intents"] += [
        {"target": "the room", "intent": "preserve", "detail": "unchanged"},
        {"target": "the lighting", "intent": "preserve", "detail": "unchanged"},
        {"target": "the people", "intent": "preserve", "detail": "unchanged"},
    ]


def _unknown_capability(b):
    b["cases"][0]["capability_mappings"]["atomic"].append("vibe_fidelity")


def _unknown_evaluator_family(b):
    b["cases"][0]["evaluator_dependencies"][0]["family"] = "gut_feel"


def _evaluator_claimed_qualified(b):
    b["cases"][0]["evaluator_dependencies"][0]["qualified"] = True


def _subjective_claimed_objective(b):
    c = next(x for x in b["cases"] if x["acceptance_contract"].get("subjective_creative"))
    c["acceptance_contract"]["subjective_creative"][0]["no_deterministic_ground_truth"] = False


def _model_specific_fields_present(b):
    b["cases"][0]["prompt_ready_envelope"]["model_specific_fields"] = {"provider": "some-vendor"}


def _envelope_drift(b):
    """Hand-edit an envelope in the brief bank so it no longer matches the generated
    prompt-ready bank. The two must never drift apart silently."""
    b["cases"][0]["prompt_ready_envelope"]["objective"] = "something else entirely"


def _empty_bank(b):
    b["cases"] = []


def _too_few_cases(b):
    b["cases"] = b["cases"][:5]


def _too_few_runnable(b):
    for c in b["cases"]:
        if c["runnable_now"] is True:
            c["runnable_now"] = False
            c.setdefault("fixture_requirements", [{}])
            c["fixture_requirements"][0]["blocks_runnable"] = True
            c["fixture_requirements"][0]["blocks_runnable_reason"] = "test"


CASES = [
    ("G1", "a case with no source facts is rejected", _drop_source_facts),
    ("G2", "a provenance outside the vocabulary is rejected", _bad_provenance),
    ("G3", "a Fiverr gig presented as a buyer brief is rejected", _fiverr_as_buyer_brief),
    ("G3", "a Fiverr convention claiming customer provenance is rejected", _fiverr_convention_claims_customer),
    ("G4", "a provider name in the route-neutral brief is rejected", _route_leak_into_brief),
    ("G4", "a production-route term in the envelope is rejected", _route_leak_into_envelope),
    ("G4", "model-specific fields in the envelope are rejected", _model_specific_fields_present),
    ("G5", "runnable_now with a blocking fixture is rejected", _runnable_with_blocking_fixture),
    ("G5", "a fixture-labelled field with no declared fixture is rejected", _fixture_without_declaration),
    ("G6", "a duplicate case id is rejected", _duplicate_case_id),
    ("G6", "a duplicate fixture id is rejected", _duplicate_fixture_id),
    ("G7", "a source path that does not resolve is rejected", _missing_source_file),
    ("G8", "a fixture relabelled as customer_stated is rejected", _fixture_relabelled_as_customer_stated),
    ("G9", "a verbatim string not present in the source is rejected", _untraceable_verbatim),
    ("G10", "a production route used as a requested operation is rejected", _production_route_as_operation),
    ("G10", "a system-derived requested operation is rejected", _system_derived_operation),
    ("G10", "a system-derived text requirement is rejected", _system_derived_text_requirement),
    ("G10", "an edit with no subject_of_operation asset is rejected", _edit_without_subject_of_operation),
    ("G10", "variants with a single deliverable is rejected", _variants_without_a_set),
    ("G10", "enumerated implicit preservation is rejected", _enumerated_implicit_preservation),
    ("G11", "a capability id not in the contract is rejected", _unknown_capability),
    ("G11", "an evaluator family the map does not define is rejected", _unknown_evaluator_family),
    ("G11", "an evaluator declared qualified is rejected", _evaluator_claimed_qualified),
    ("G2", "a subjective requirement claimed as objective is rejected", _subjective_claimed_objective),
    ("G13", "an envelope that drifts from the prompt-ready bank is rejected", _envelope_drift),
    ("STRUCT", "an empty bank fails rather than passing", _empty_bank),
    ("SCOPE", "fewer than 12 cases is rejected", _too_few_cases),
    ("SCOPE", "fewer than 8 runnable cases is rejected", _too_few_runnable),
]


def main():
    print("=" * 74)
    print("CANON-011 negative controls for validate_marketplace_bank.py")
    print("=" * 74)

    failures = []

    # Control: the real bank must PASS. Without this, a validator that rejected every
    # input would score a perfect run on the negative suite.
    code, out = run_on(BANK)
    if code != 0:
        failures.append(f"CONTROL: the unmodified bank failed validation:\n{out}")
        print("  FAIL  CONTROL   the unmodified bank should pass and did not")
    else:
        print("  ok    CONTROL   the unmodified committed bank passes")

    for gate, desc, fn in CASES:
        code, out = run_on(mutate(fn))
        if code == 0:
            failures.append(f"{gate}: {desc} - validator PASSED a bank it should have rejected")
            print(f"  FAIL  {gate:<7}  {desc}")
        elif gate not in ("STRUCT", "SCOPE") and gate not in out:
            failures.append(
                f"{gate}: {desc} - validator failed, but not on {gate}. Output:\n{out}"
            )
            print(f"  FAIL  {gate:<7}  {desc} (failed on the wrong gate)")
        else:
            print(f"  ok    {gate:<7}  {desc}")

    print("-" * 74)
    if failures:
        print(f"{len(failures)} negative control(s) did not behave as required:\n")
        for f in failures:
            print(f"  {f}\n")
        print("RESULT: FAIL")
        return 1
    print(f"RESULT: PASS - {len(CASES)} negative controls all rejected, and the real bank passes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
