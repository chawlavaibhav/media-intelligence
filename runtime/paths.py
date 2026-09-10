"""Every path the runtime reads, resolved from the package location, never from cwd."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RUNTIME = ROOT / "runtime"
CONTRACTS = RUNTIME / "contracts"

JOB_CONTRACT = CONTRACTS / "PRODUCTION-JOB-v0.yaml"
SPEC_CONTRACT = CONTRACTS / "PRODUCTION-SPEC-v0.yaml"
DELIVERABLE_KINDS = CONTRACTS / "DELIVERABLE-KINDS.yaml"
POLICY_PROFILES = CONTRACTS / "POLICY-PROFILES.yaml"

# Read-only Canon and Lab assets. The runtime never writes under these trees.
CANON_TRIGGERS = ROOT / "canon" / "packs" / "pack-triggers-v0.yaml"
CANON_COMPILATION = ROOT / "canon" / "compilation"
CANON_INJECTION_CONTRACT = CANON_COMPILATION / "INJECTION-CONTRACT-v0.md"
CANON_CORPUS_INDEX = ROOT / "canon" / "knowledge" / "CANON-CORPUS-INDEX.yaml"
EVIDENCE_MAP = ROOT / "eval" / "capability-map" / "ROUTING-EVIDENCE-MAP-v0.yaml"

# Runtime-owned data (rows, not code). Editing a row must never require editing code.
REQUIRED_LIMITS = RUNTIME / "policy" / "REQUIRED-LIMITS-v0.yaml"
KIND_NR_BINDING = RUNTIME / "canon" / "KIND-NR-BINDING-v0.yaml"
RULE_INTERPRETATION = RUNTIME / "evidence" / "RULE-INTERPRETATION-v0.yaml"
ACCEPTANCE_STYLE = RUNTIME / "spec" / "ACCEPTANCE-STYLE-v0.yaml"
FACET_CAPABILITIES = RUNTIME / "spec" / "FACET-CAPABILITIES-v0.yaml"

FIXTURES = RUNTIME / "fixtures"
PLANNER_FIXTURES = FIXTURES / "planner"
BRIEF_FIXTURES = FIXTURES / "briefs"

DEFAULT_STORE = RUNTIME / "store"
