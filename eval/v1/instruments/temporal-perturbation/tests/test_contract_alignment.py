"""This package must not drift away from the frozen contracts.

These tests read the frozen files directly. If someone renames a capability,
adds one, or quietly points a perturbation at something outside the temporal
family, the tests fail rather than the drift being discovered months later in a
report.

Parsed with a small line scanner rather than PyYAML so the checks run in a bare
interpreter, exactly like the rest of this package.
"""
import pathlib
import re

import perturbations as P

REPO = pathlib.Path(__file__).resolve().parents[5]
FROZEN_MAP = REPO / "eval/pre-execution-freeze/EVALUATOR-QUALIFICATION-MAP.yaml"
CONTRACT = REPO / "eval/v1/instruments/temporal-perturbation/perturbation-contract.yaml"
FAMILY_SPEC = REPO / "eval/v1/instruments/FAMILY-4-TEMPORAL-VIDEO.md"


def frozen_temporal_capabilities() -> set:
    caps, current = set(), None
    for line in FROZEN_MAP.read_text().splitlines():
        m = re.match(r"- capability: (\S+)", line.strip())
        if m:
            current = m.group(1)
        elif current and line.strip() == "evaluator_family: temporal_video":
            caps.add(current)
    return caps


def test_the_frozen_map_still_lists_nine_temporal_capabilities():
    caps = frozen_temporal_capabilities()
    assert len(caps) == 9, f"expected 9 temporal_video capabilities, found {sorted(caps)}"


def test_no_perturbation_names_a_capability_outside_the_frozen_family():
    frozen = frozen_temporal_capabilities()
    named = {c for v in P.CAPABILITY_TARGETS.values() for c in v}
    assert named <= frozen, f"invented or misfiled capabilities: {sorted(named - frozen)}"


def test_every_frozen_temporal_capability_has_at_least_one_perturbation():
    frozen = frozen_temporal_capabilities()
    named = {c for v in P.CAPABILITY_TARGETS.values() for c in v}
    assert frozen <= named, f"no injected truth for: {sorted(frozen - named)}"


def test_contract_file_covers_every_implemented_perturbation():
    text = CONTRACT.read_text()
    ids = set(re.findall(r"^  - id: (\S+)$", text, re.M))
    for ptype in P.PERTURBATIONS:
        assert ptype in ids, f"{ptype} is implemented but absent from the contract"


def test_contract_declares_truth_completeness_for_every_perturbation():
    """A perturbation that cannot establish the whole judgement must say so."""
    text = CONTRACT.read_text()
    blocks = re.split(r"\n  - id: ", text)
    seen = 0
    for b in blocks[1:]:
        pid = b.split("\n", 1)[0].strip()
        if pid not in P.PERTURBATIONS:
            continue
        seen += 1
        assert "truth_completeness" in b, f"{pid} does not declare truth_completeness"
    assert seen == len(P.PERTURBATIONS)


def test_contract_sets_no_numeric_pass_mark():
    text = CONTRACT.read_text()
    assert "DOES_NOT_EXIST" in text
    assert "numeric_pass_mark" in text
    assert re.search(r"(recall|false_positive)[^\n]*[<>]=?\s*0?\.\d", text) is None, \
        "a numeric gate appeared in the contract; none exists in the frozen family-4 spec"


def test_min_samples_table_covers_every_perturbation():
    assert set(P.MIN_SAMPLES_INSIDE) == set(P.CAPABILITY_TARGETS) == set(P.PERTURBATIONS)


def test_family_spec_still_describes_a_recall_gate_with_a_sampling_caveat():
    text = FAMILY_SPEC.read_text()
    assert "Detection recall" in text
    assert "False-positive rate" in text
    assert "Localisation accuracy" in text
    assert "sample rate is part of the measurement" in text
