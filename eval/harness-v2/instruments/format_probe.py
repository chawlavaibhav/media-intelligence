"""format_probe -> delivery_format_compliance, reliability_pass_at_k: is the file what the case asked for?

    ffprobe -print_format json -show_format -show_streams -> container, width x height, aspect, duration,
    fps, audio-stream presence; compared with the case's COND-DELIVERY and the route row's params.
A file ffprobe cannot parse is absent / parse_failure. Proposed tolerances: PASS-CRITERIA-v0.yaml#format_probe.
"""
from __future__ import annotations

import re
from pathlib import Path

from . import common as C
from . import imageio as IO

INSTRUMENT_ID = "format_probe"
VERSION = "0.1.0"
CAPABILITIES = ("delivery_format_compliance", "reliability_pass_at_k")
_ASPECT = re.compile(r"^\s*(\d+)\s*:\s*(\d+)\s*$")


def declared_aspect(case_row: dict) -> str | None:
    for cand in ((case_row.get("params") or {}).get("aspect"),
                 ((case_row.get("conditions") or {}).get("COND-DELIVERY") or {}).get("aspect_ratio")):
        if isinstance(cand, str) and _ASPECT.match(cand):
            return cand.strip()
        if isinstance(cand, list):
            for c in cand:
                if isinstance(c, str) and _ASPECT.match(c):
                    return c.strip()
    return None


def declared_duration(case_row: dict) -> float | None:
    for cand in ((case_row.get("params") or {}).get("duration_s"),
                 ((case_row.get("conditions") or {}).get("COND-DELIVERY") or {}).get("duration_s")):
        if isinstance(cand, bool):
            continue
        if isinstance(cand, (int, float)):
            return float(cand)
        if isinstance(cand, str) and cand.strip().replace(".", "", 1).isdigit():
            return float(cand)
    return None


def declared_audio(case_row: dict) -> bool | None:
    a = str((case_row.get("params") or {}).get("audio", "")).strip().lower()
    if a.startswith("on"):
        return True
    if a.startswith("off"):
        return False
    return None


def resolution_class_ok(declared: str | None, width, height) -> tuple:
    """(ok | None, note). Classes: 'NNNp' -> short side == NNN; '1024-class' -> long side 960..1100;
    'N MP' -> pixel count within +-25 % of N million. Unparseable -> None (not checked)."""
    if not declared or not width or not height:
        return None, "no declared resolution class"
    d = str(declared).lower()
    short, long_ = min(width, height), max(width, height)
    m = re.search(r"(\d{2,4})\s*p\b", d)
    if m:
        target = int(m.group(1))
        return short == target, f"{target}p class: short side {short}"
    if "1024-class" in d or "1k" in d:
        return 960 <= long_ <= 1100, f"1024-class: long side {long_}"
    m = re.search(r"(\d+(?:\.\d+)?)\s*mp\b", d)
    if m:
        mp = float(m.group(1))
        px = width * height / 1e6
        return abs(px - mp) <= 0.25 * mp, f"{mp} MP class: {px:.3f} MP"
    return None, f"resolution class {declared!r} not parseable"


def measure(path: Path | str, case_row: dict, thresholds: dict | None = None) -> dict:
    t = thresholds or {}
    probe = IO.ffprobe(path)
    checks: dict = {}
    notes: dict = {}
    da = declared_aspect(case_row)
    if da and probe["aspect_float"]:
        n, d = (int(v) for v in da.split(":"))
        checks["aspect_ok"] = abs(probe["aspect_float"] / (n / d) - 1.0) <= float(t.get("aspect_ratio_tolerance_fraction", 0.01))
        notes["aspect"] = f"declared {da}, observed {probe['aspect']} ({probe['width']}x{probe['height']})"
    else:
        checks["aspect_ok"] = None
        notes["aspect"] = "no declared aspect or no picture"
    dd = declared_duration(case_row)
    if dd is not None:
        checks["duration_ok"] = probe["duration_s"] is not None and abs(probe["duration_s"] - dd) <= float(t.get("duration_tolerance_s", 0.5))
        notes["duration"] = f"declared {dd} s, observed {probe['duration_s']}"
    else:
        checks["duration_ok"] = True
        notes["duration"] = "not applicable (no declared duration)"
    au = declared_audio(case_row)
    if au is not None and t.get("audio_present_iff_audio_on", True):
        checks["audio_ok"] = probe["has_audio"] == au
        notes["audio"] = f"declared audio {'on' if au else 'off'}, stream {'present' if probe['has_audio'] else 'absent'}"
    else:
        checks["audio_ok"] = True
        notes["audio"] = "not applicable"
    ok, note = resolution_class_ok((case_row.get("params") or {}).get("resolution"), probe["width"], probe["height"])
    checks["resolution_class_ok"] = ok if t.get("resolution_class_must_match_declared", True) else None
    notes["resolution"] = note
    checks["decodable"] = True
    return {"probe": probe, "checks": checks, "notes": notes, "declared": {"aspect": da, "duration_s": dd, "audio": au,
            "resolution": (case_row.get("params") or {}).get("resolution")}, "artifact_sha256": C.sha256_file(path)}


def evaluate(path, case_row: dict, criteria_path: Path | str | None = None) -> dict:
    crit = C.criterion(INSTRUMENT_ID, criteria_path)
    try:
        m = measure(path, case_row, crit.thresholds)
    except IO.ToolUnavailable as exc:
        return C.unavailable(str(exc))
    except (IO.ProbeError, OSError, ValueError) as exc:
        return C.parse_failure(str(exc))
    defects = [{"term": f"{k.replace('_ok', '')} mismatch: {m['notes'].get(k.replace('_ok', ''), '')}"}
               for k, v in m["checks"].items() if v is False]
    return C.gate(crit, not defects, m, defects)


def instrument(criteria_path: Path | str | None = None):
    def fn(path, item, capability):
        return evaluate(path, C.inputs_of(item).get("case_row") or item, criteria_path)
    return C.build_instrument(INSTRUMENT_ID, VERSION, CAPABILITIES, fn, criteria_path)
