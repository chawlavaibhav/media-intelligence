"""gate_wrapper: the compiled-doctrine gate's post-draw check, run as an OBSERVATION only.

    python3 canon/gate/run_gate.py post --artifact <file> --dispatch <request.json> --modality <m> [--frames DIR] --json <out>

`canon/gate/run_gate.py` exists on branch work/canon-gate-001 (read-only) and NOT on this branch, so on
this base `run_post()` returns {status: not_available_on_base, base: <sha>}. The instrument is registered
`provisional`: it may never write a Registry row; its report is stored as an observation.
This is one of the two local-subprocess sites outside transports.py (the other is imageio's ffmpeg).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import hv2_paths
from . import common as C

INSTRUMENT_ID = "gate_wrapper"
VERSION = "0.1.0"
GATE_REL = "canon/gate/run_gate.py"
MODALITIES = ("static_image", "video", "image_sequence", "audio")


def base_sha(repo_root: Path = hv2_paths.REPO_ROOT) -> str | None:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo_root, capture_output=True, text=True, check=True).stdout.strip()
    except Exception:  # noqa: BLE001
        return None


def run_post(artifact: Path | str, request_json: Path | str, modality: str, frames_dir: Path | str | None = None,
             gate_script: Path | str | None = None, json_out: Path | str | None = None, timeout_s: float = 300.0) -> dict:
    script = Path(gate_script) if gate_script else hv2_paths.REPO_ROOT / GATE_REL
    if modality not in MODALITIES:
        return {"status": "invalid_modality", "modality": modality, "allowed": list(MODALITIES)}
    if not script.exists():
        return {"status": "not_available_on_base", "base": base_sha(), "gate_path": str(script),
                "note": "canon/gate/run_gate.py lives on work/canon-gate-001; EVALUATOR-PLAN gate_post: not_available_on_base today"}
    out = Path(json_out) if json_out else Path(str(artifact) + ".gate.json")
    argv = [sys.executable, str(script), "post", "--artifact", str(artifact), "--dispatch", str(request_json),
            "--modality", modality, "--json", str(out)]
    if frames_dir:
        argv += ["--frames", str(frames_dir)]
    try:
        r = subprocess.run(argv, capture_output=True, text=True, timeout=timeout_s, cwd=script.parent.parent.parent)
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "argv": argv[1:]}
    report = None
    if out.exists():
        try:
            report = json.loads(out.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            report = {"$unparseable": True}
    return {"status": "ran", "exit_code": r.returncode, "report": report, "stdout": (r.stdout or "")[:2000],
            "stderr": (r.stderr or "")[:2000], "argv": argv[1:], "json_path": str(out)}


def instrument(criteria_path: Path | str | None = None):
    def fn(path, item, capability):
        ins = C.inputs_of(item)
        obs = run_post(path, ins.get("request_json") or (str(path) + ".request.json"), ins.get("modality", "static_image"),
                       ins.get("frames_dir"), ins.get("gate_script"))
        if obs["status"] != "ran":
            return C.result("absent", "instrument_unavailable", f"gate {obs['status']}", observation=obs)
        return C.result("absent", "other", "observation_only: the gate is provisional and never yields a verdict here", observation=obs)
    return C.build_instrument(INSTRUMENT_ID, VERSION, (), fn, criteria_path, qualification_status="provisional")
