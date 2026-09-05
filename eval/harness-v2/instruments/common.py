"""Shared plumbing for the deterministic instruments: the PASS-CRITERIA loader, the frozen-gate rule,
result shapes and the harness.Instrument factory.

THE FROZEN-GATE RULE (Controller between-role note 4; task §3)

    While PASS-CRITERIA-v0.yaml says `frozen: false` for an instrument, `gate()` returns
        verdict: absent, absence_reason: other, note: criterion_not_frozen
    and keeps the full measurement plus `would_verdict` (what the proposed threshold WOULD have said)
    as an observation. Only a `frozen: true` entry - a Controller ruling, MD-C1 - yields pass / fail.
    The threshold values and the frozen flag are part of the Instrument config, so they are covered
    by config_hash: freezing or changing a value makes a different instrument, as the Registry
    schema requires.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

import yaml

import hv2_paths  # noqa: F401
import harness as H                    # read-only import of the frozen v1 harness
from models import ABSENCE_REASONS, VERDICTS
from . import imageio as IO

HERE = Path(__file__).resolve().parent
CRITERIA_PATH = HERE / "PASS-CRITERIA-v0.yaml"
CRITERIA_REF = "eval/harness-v2/instruments/PASS-CRITERIA-v0.yaml"
CRITERION_NOT_FROZEN = "criterion_not_frozen"


class CriteriaError(RuntimeError):
    """PASS-CRITERIA-v0.yaml cannot be read as declared, or names no entry for this instrument."""


@dataclass(frozen=True)
class Criterion:
    id: str
    frozen: bool
    status: str
    thresholds: dict
    metric: str
    colour_space: str
    source: str
    verified: bool
    controller_ref: str
    capabilities: tuple
    registered_as: str
    path: str
    sha256: str

    @property
    def ref(self) -> str:
        return f"{CRITERIA_REF}#{self.id}"


def load_criteria(path: Path | str | None = None) -> dict:
    p = Path(path) if path else CRITERIA_PATH
    raw = p.read_bytes()
    data = yaml.safe_load(raw.decode("utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("criteria"), dict):
        raise CriteriaError(f"{p}: no criteria mapping")
    data["_sha256"] = hashlib.sha256(raw).hexdigest()
    data["_path"] = str(p)
    return data


def criterion(instrument_id: str, path: Path | str | None = None) -> Criterion:
    data = load_criteria(path)
    c = data["criteria"].get(instrument_id)
    if not isinstance(c, dict):
        raise CriteriaError(f"no PASS-CRITERIA entry for instrument {instrument_id!r}; an instrument without an entry may not run")
    return Criterion(
        id=instrument_id, frozen=(c.get("frozen") is True), status=str(c.get("status")),
        thresholds=dict(c.get("thresholds") or {}), metric=str(c.get("metric") or ""),
        colour_space=str(c.get("colour_space") or ""), source=str(c.get("source") or ""),
        verified=(c.get("verified") is True), controller_ref=str(c.get("controller_ref") or ""),
        capabilities=tuple(c.get("capabilities") or ()), registered_as=str(c.get("registered_as") or instrument_id),
        path=data["_path"], sha256=data["_sha256"])


# ------------------------------------------------------------------------------ results
def result(verdict: str, absence_reason: str | None = None, note: str = "", measurement: dict | None = None,
           defects=(), **extra) -> dict:
    if verdict not in VERDICTS:
        raise ValueError(f"verdict {verdict!r} not in {VERDICTS}")
    if verdict == "absent" and absence_reason not in ABSENCE_REASONS:
        raise ValueError(f"absent needs a reason from {ABSENCE_REASONS}, got {absence_reason!r}")
    if verdict != "absent" and absence_reason is not None:
        raise ValueError("a pass/fail verdict must not carry an absence reason")
    out = {"verdict": verdict, "absence_reason": absence_reason, "note": note,
           "measurement": dict(measurement or {}),
           "defects": [({"term": d, "observed_by": "instrument"} if isinstance(d, str) else {"observed_by": "instrument", **d}) for d in defects]}
    out.update(extra)
    return out


def parse_failure(reason: str, measurement: dict | None = None) -> dict:
    return result("absent", "parse_failure", f"fail closed: {reason}", measurement)


def unavailable(reason: str) -> dict:
    return result("absent", "instrument_unavailable", reason)


def gate(crit: Criterion, passed: bool, measurement: dict, defects=(), note: str = "") -> dict:
    """The one place a verdict is decided. Unfrozen criterion -> absent / criterion_not_frozen."""
    if passed is None:
        raise ValueError("gate() needs a boolean; an uncomputable result is a parse_failure, not a verdict")
    crit_info = {"id": crit.id, "ref": crit.ref, "frozen": crit.frozen, "status": crit.status,
                 "controller_ref": crit.controller_ref, "criteria_file_sha256": crit.sha256}
    if not crit.frozen:
        return result("absent", "other", CRITERION_NOT_FROZEN, measurement, defects=(),
                      would_verdict=("pass" if passed else "fail"),
                      would_defects=[({"term": d, "observed_by": "instrument"} if isinstance(d, str) else {"observed_by": "instrument", **d}) for d in defects],
                      criterion=crit_info)
    return result("pass" if passed else "fail", None, note, measurement, defects=(() if passed else defects), criterion=crit_info)


# ------------------------------------------------------------------------------ instruments
def tool_versions() -> dict:
    t = IO.tools()
    return {k: (v.get("version") if v.get("available") else None) for k, v in t.items()}


def build_instrument(criterion_id: str, version: str, capabilities, fn, criteria_path: Path | str | None = None,
                     extra_config: dict | None = None, qualification_status: str = "deterministic",
                     observation_unit: str = "artifact", instrument_id: str | None = None) -> H.Instrument:
    """A harness.Instrument whose config (and so config_hash) covers thresholds, frozen flag, colour space,
    the criteria file's sha256 and the local tool versions."""
    c = criterion(criterion_id, criteria_path)
    config = {"instrument": instrument_id or c.registered_as, "criterion_id": c.id, "version": version,
              "criteria_ref": c.ref, "criteria_file_sha256": c.sha256, "frozen": c.frozen, "status": c.status,
              "thresholds": c.thresholds, "metric": c.metric, "colour_space": c.colour_space,
              "tool_versions": tool_versions(), **(extra_config or {})}
    return H.Instrument(instrument_id or c.registered_as, version, config, qualification_status=qualification_status,
                        calibration_ref=c.ref, capabilities=tuple(capabilities), observation_unit=observation_unit, fn=fn)


# ------------------------------------------------------------------------------ media helpers
def sha256_file(path: Path | str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_image(path: Path | str) -> IO.Image:
    """PNG through the stdlib decoder; anything else through ffmpeg. Raises ProbeError / ToolUnavailable."""
    p = Path(path)
    if not p.exists() or p.stat().st_size == 0:
        raise IO.ProbeError(f"{p} does not exist or is empty")
    data = p.read_bytes()
    if data[:8] == IO.PNG_SIG:
        return IO.decode_png(data)
    return IO.decode_image_ffmpeg(p)


def inputs_of(item: dict) -> dict:
    """Extra inputs an instrument needs (mask, reference, drive audio, the other repeat) travel on the item."""
    return dict(item.get("instrument_inputs") or {})
