"""Shared fixtures for the lane-G loop tests. Holds no tests of its own.

Everything is offline: spec fixtures from runtime/route/fixtures, hand-made blueprints and
human verdicts from runtime/fixtures/synthetic, the compiled packs from canon/compilation.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import yaml  # noqa: E402

from runtime import paths  # noqa: E402
from runtime.route.profile import load_profile  # noqa: E402

FIXTURES = ROOT / "runtime" / "route" / "fixtures"
SYNTHETIC = ROOT / "runtime" / "fixtures" / "synthetic"
SPEC_OVERLAY = FIXTURES / "SPEC-static-ad-devanagari-overlay.yaml"
SPEC_IN_SCENE = FIXTURES / "SPEC-static-ad-devanagari-in-scene.yaml"
SPEC_MOTION = FIXTURES / "SPEC-motion-6s-silent.yaml"


def load_spec_dict(path: Path, **overrides) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    data.setdefault("policy_profile", "alpha_human_release")
    # the fixtures write job_sha256 as an unquoted run of zeros, which YAML reads as the integer 0;
    # the intent is a 64-character placeholder digest, restored here (reported upward as a fixture quirk)
    if isinstance(data.get("job_sha256"), int):
        data["job_sha256"] = f"{data['job_sha256']:064x}"
    # lane E's v1 keys (WAVE2-INTERFACES §1); the committed fixtures predate them
    strategy = (data.get("exact_text") or {}).get("strategy")
    data["exact_text"].setdefault("text_mechanism", {
        "code_set_on_textless_plate": "deterministic_text_composition",
        "generated_in_scene": "model_draws_text",
    }.get(strategy, "not_applicable"))
    for k, v in overrides.items():
        data[k] = v
    return data


def load_json(name: str) -> dict:
    return json.loads((SYNTHETIC / name).read_text(encoding="utf-8"))


def blueprint_overlay() -> dict:
    return load_json("blueprint-img-text-01.json")


def blueprint_clean() -> dict:
    """Runtime-authored plate prompt that the gate passes (see the fixture's _note)."""
    return load_json("blueprint-plate-clean.json")


def blueprint_motion() -> dict:
    return load_json("blueprint-motion-6s.json")


def profile(name: str = "alpha_human_release"):
    return load_profile(name, paths.POLICY_PROFILES)


def with_aspect(spec: dict, aspect: str) -> dict:
    out = copy.deepcopy(spec)
    out["deliverable"]["aspect"] = aspect
    return out
