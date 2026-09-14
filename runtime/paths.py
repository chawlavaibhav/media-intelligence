"""Every path the runtime reads, resolved from the package location, never from cwd."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RUNTIME = ROOT / "runtime"
CONTRACTS = RUNTIME / "contracts"

# 14 Sep 2026 (lane E): both bound to v1. They were bound to the v0 files, so intake keyed consent
# on role == 'person' (the hole CHANGES-v0-to-v1.md says v1 closed) and the compiler emitted a spec
# the router (runtime/route/spec.py, built against v1) refused. The v0 files stay beside these as
# the record; nothing reads them.
JOB_CONTRACT = CONTRACTS / "PRODUCTION-JOB-v1.yaml"
SPEC_CONTRACT = CONTRACTS / "PRODUCTION-SPEC-v1.yaml"
DELIVERABLE_KINDS = CONTRACTS / "DELIVERABLE-KINDS.yaml"
POLICY_PROFILES = CONTRACTS / "POLICY-PROFILES.yaml"

# Read-only Canon and Lab assets. The runtime never writes under these trees.
CANON_TRIGGERS = ROOT / "canon" / "packs" / "pack-triggers-v0.yaml"
CANON_COMPILATION = ROOT / "canon" / "compilation"
CANON_INJECTION_CONTRACT = CANON_COMPILATION / "INJECTION-CONTRACT-v0.md"
CANON_CORPUS_INDEX = ROOT / "canon" / "knowledge" / "CANON-CORPUS-INDEX.yaml"
EVIDENCE_MAP = ROOT / "eval" / "capability-map" / "ROUTING-EVIDENCE-MAP-v0.yaml"
# The frozen Stage-A package: the recorded reasoning pass for a Stage-A-derived brief IS its blueprint
# (lead's design decision, 14 Sep 2026), parsed deterministically by runtime/spec/blueprint_planner.py.
STAGE_A_FREEZE = ROOT / "eval" / "empirical-planning" / "STAGE-A-FREEZE-2026-09"
STAGE_A_TEST_CASES = STAGE_A_FREEZE / "TEST-CASES.yaml"
STAGE_A_BLUEPRINTS = STAGE_A_FREEZE / "BLUEPRINTS"
HARNESS_V2 = ROOT / "eval" / "harness-v2"
MARKETPLACE_BRIEF_BANK = ROOT / "canon" / "research" / "marketplace-demand-v1" / "derived" / "marketplace-brief-bank-v1.yaml"

# Runtime-owned data (rows, not code). Editing a row must never require editing code.
REQUIRED_LIMITS = RUNTIME / "policy" / "REQUIRED-LIMITS-v0.yaml"
KIND_NR_BINDING = RUNTIME / "canon" / "KIND-NR-BINDING-v0.yaml"
RULE_INTERPRETATION = RUNTIME / "evidence" / "RULE-INTERPRETATION-v0.yaml"
ACCEPTANCE_STYLE = RUNTIME / "spec" / "ACCEPTANCE-STYLE-v0.yaml"
FACET_CAPABILITIES = RUNTIME / "spec" / "FACET-CAPABILITIES-v0.yaml"

FIXTURES = RUNTIME / "fixtures"
PLANNER_FIXTURES = FIXTURES / "planner"
BRIEF_FIXTURES = FIXTURES / "briefs"
# Briefs derived from the frozen Stage-A cases by runtime/tools/brief_from_stage_a_case.py (and one
# marketplace case by brief_from_marketplace_case.py). Generated, committed, regenerable byte for byte.
ALPHA_BRIEFS = FIXTURES / "alpha-briefs"

DEFAULT_STORE = RUNTIME / "store"
