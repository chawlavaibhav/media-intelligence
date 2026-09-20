"""VO schedule gate ported verbatim from PR #103 (1de2b37:runtime/compositor/gates.py) for experiment job B; not on main."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[4]))  # repo root
try:
    from runtime.errors import Refusal
except Exception:  # fallback keeps the gate importable outside the repo
    class Refusal(Exception):
        def __init__(self, code, message='', **kw): super().__init__(message); self.code=code; self.info=kw

class LayoutRefused(Refusal):
    TEXT_OUT_OF_CANVAS = "TEXT_OUT_OF_CANVAS"
    TEXT_OUT_OF_CONTAINER = "TEXT_OUT_OF_CONTAINER"
    CONTRAST_BELOW_THRESHOLD = "CONTRAST_BELOW_THRESHOLD"
    UNDECLARED_COVER_CROP = "UNDECLARED_COVER_CROP"
    GEOMETRY_OFF_TOKEN = "GEOMETRY_OFF_TOKEN"
    CRITICAL_REGIONS_OVERLAP = "CRITICAL_REGIONS_OVERLAP"
    TOKEN_SOURCE_MISSING = "TOKEN_SOURCE_MISSING"
    VO_LINES_OVERLAP = "VO_LINES_OVERLAP"
    VO_OVERRUNS_END = "VO_OVERRUNS_END"


# ── geometry helpers ─────────────────────────────────────────────────────────


def check_vo_schedule(lines, *, film_end_s: float, min_gap_s: float = 0.0) -> dict:
    """Voice-over lines are placed from their MEASURED durations, never from a plan: two lines may not
    overlap (nor sit closer than `min_gap_s`), and no line may run past the end of the film. Case 003:
    six lines were placed at hand-set start times from an 18-s plan; measured afterwards, line 1 overlapped
    line 2 by 0.92 s and the closing line overran the film by 0.94 s — the human heard "voices overlapping".
    Text overflow already failed closed (check_text_bounds); audio overflow did not. Each line is
    {"id", "start_s", "duration_s"}; durations are what the trimmed file actually measures."""
    rows = []
    for ln in lines:
        start, dur = float(ln["start_s"]), float(ln["duration_s"])
        if dur <= 0:
            raise ValueError(f"vo line {ln.get('id')!r}: duration must be measured and positive")
        rows.append((start, start + dur, str(ln.get("id"))))
    rows.sort()
    end = float(film_end_s)
    for i in range(1, len(rows)):
        prev, cur = rows[i - 1], rows[i]
        if cur[0] < prev[1] + float(min_gap_s):
            raise LayoutRefused(LayoutRefused.VO_LINES_OVERLAP,
                                f"vo line {cur[2]} starts at {cur[0]:.2f}s but {prev[2]} ends at {prev[1]:.2f}s"
                                + (f" (gap < {min_gap_s}s)" if min_gap_s else ""),
                                pair=(prev[2], cur[2]), overlap_s=round(prev[1] + float(min_gap_s) - cur[0], 3))
    for start, stop, lid in rows:
        if stop > end + 1e-6:
            raise LayoutRefused(LayoutRefused.VO_OVERRUNS_END,
                                f"vo line {lid} ends at {stop:.2f}s, after the film ends at {end:.2f}s",
                                id=lid, overrun_s=round(stop - end, 3))
    return {"status": "PASS", "lines": [r[2] for r in rows], "film_end_s": end, "min_gap_s": float(min_gap_s),
            "last_line_ends_s": round(rows[-1][1], 3) if rows else None}
