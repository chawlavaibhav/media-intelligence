"""Shared scaffolding. Every test runs offline, against a throwaway job store."""
from __future__ import annotations

import copy
import json
import tempfile
from pathlib import Path

from runtime import paths
from runtime.intake import Intake, JobStore
from runtime.policy import PolicyProfiles
from runtime.spec.compile import SpecCompiler

TEST_PROFILES = paths.FIXTURES / "policy" / "POLICY-PROFILES-test.yaml"


def brief(name: str) -> dict:
    with open(paths.BRIEF_FIXTURES / f"{name}.json", "r", encoding="utf-8") as fh:
        return json.load(fh)


def fresh_store() -> JobStore:
    return JobStore(tempfile.mkdtemp(prefix="runtime-test-"))


def intake(profiles: PolicyProfiles | None = None) -> Intake:
    return Intake(store=fresh_store(), profiles=profiles)


def test_profiles() -> PolicyProfiles:
    return PolicyProfiles(profiles_path=TEST_PROFILES)


def submit(name: str, **overrides) -> dict:
    raw = copy.deepcopy(brief(name))
    raw.update(overrides)
    return intake().submit(raw).job


def compiler(**kwargs) -> SpecCompiler:
    return SpecCompiler(**kwargs)
