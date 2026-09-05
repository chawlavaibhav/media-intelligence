"""audio_track_offset_vs_drive -> audio_video_synchronisation (PARTIAL claim, MD-C6).

What it measures: the offset between the drive audio we supplied and the audio track the provider
returned inside the artifact. It does NOT measure mouth onset against sound - that is not deterministic.
The instrument is therefore registered as `audio_track_offset_vs_drive`, and whether that partial
measurement may stand in for the capability is a Controller decision (MD-C6).

    both signals -> 16 kHz mono PCM (ffmpeg) -> 10-ms RMS envelopes -> mean-removed -> normalised
    cross-correlation over lags -1000..+1000 ms -> lag_ms at the peak (positive = the artifact's audio
    LAGS the drive) and the peak correlation. A peak below min_peak_correlation means no alignment was
    found and the result is absent (never pass).
"""
from __future__ import annotations

import math
from pathlib import Path

from . import common as C
from . import imageio as IO

INSTRUMENT_ID = "av_offset"
REGISTERED_AS = "audio_track_offset_vs_drive"
VERSION = "0.1.0"
CAPABILITIES = ("audio_video_synchronisation",)
RATE = 16000
STEP_MS = 10
MAX_LAG_MS = 1000


def envelope(samples: list, rate: int = RATE, step_ms: int = STEP_MS) -> list:
    step = rate * step_ms // 1000
    out = []
    for i in range(0, len(samples) - step + 1, step):
        seg = samples[i:i + step]
        out.append(math.sqrt(sum(s * s for s in seg) / step))
    return out


def cross_correlate(drive: list, art: list, max_lag_steps: int) -> tuple:
    """(best_lag_steps, peak_corr). corr(lag) aligns art[i+lag] with drive[i]: positive lag = artifact later."""
    md = sum(drive) / len(drive) if drive else 0.0
    ma = sum(art) / len(art) if art else 0.0
    d = [v - md for v in drive]
    a = [v - ma for v in art]
    best_lag, best = 0, -2.0
    for lag in range(-max_lag_steps, max_lag_steps + 1):
        num = dd = aa = 0.0
        for i in range(len(d)):
            j = i + lag
            if 0 <= j < len(a):
                num += d[i] * a[j]
                dd += d[i] * d[i]
                aa += a[j] * a[j]
        corr = num / math.sqrt(dd * aa) if dd > 0 and aa > 0 else 0.0
        # strictly better wins; an EXACT tie keeps the smaller |lag| (a periodic drive has no unique lag,
        # and the tie rule is recorded so the choice is visible, not silent)
        if corr > best + 1e-12 or (abs(corr - best) <= 1e-12 and abs(lag) < abs(best_lag)):
            best, best_lag = corr, lag
    return best_lag, best


def measure(drive_path: Path | str, artifact_path: Path | str, rate: int = RATE, step_ms: int = STEP_MS,
            max_lag_ms: int = MAX_LAG_MS) -> dict:
    drive = IO.decode_audio_pcm(drive_path, rate)
    art = IO.decode_audio_pcm(artifact_path, rate)
    ed, ea = envelope(drive.samples, rate, step_ms), envelope(art.samples, rate, step_ms)
    if len(ed) < 2 or len(ea) < 2:
        raise IO.ProbeError("an audio input is shorter than two envelope steps; nothing to align")
    lag_steps, peak = cross_correlate(ed, ea, max_lag_ms // step_ms)
    return {
        "lag_ms": lag_steps * step_ms, "peak_correlation": peak, "rate_hz": rate, "envelope_step_ms": step_ms,
        "max_lag_ms": max_lag_ms, "sign_convention": "positive = the artifact's audio lags the drive",
        "tie_rule": "exact correlation ties resolve to the smaller |lag|",
        "drive_seconds": len(drive.samples) / rate, "artifact_audio_seconds": len(art.samples) / rate,
        "drive_sha256": C.sha256_file(drive_path), "artifact_sha256": C.sha256_file(artifact_path),
        "claim": f"partial: {REGISTERED_AS}",
    }


def evaluate(drive_path, artifact_path, criteria_path: Path | str | None = None) -> dict:
    crit = C.criterion(INSTRUMENT_ID, criteria_path)
    try:
        m = measure(drive_path, artifact_path)
    except IO.ToolUnavailable as exc:
        return C.unavailable(str(exc))
    except (IO.ProbeError, OSError, ValueError) as exc:
        return C.parse_failure(str(exc))
    t = crit.thresholds
    min_corr = float(t.get("min_peak_correlation", 0.5))
    if m["peak_correlation"] < min_corr:
        return C.result("absent", "other", f"no alignment found: peak correlation {m['peak_correlation']:.3f} < {min_corr}",
                        m, claim=m["claim"], criterion={"id": crit.id, "ref": crit.ref, "frozen": crit.frozen})
    limit = float(t.get("abs_lag_ms_max", 80))
    ok = abs(m["lag_ms"]) <= limit
    r = C.gate(crit, ok, m, [] if ok else [{"term": f"audio track offset {m['lag_ms']} ms exceeds +-{limit:g} ms"}])
    r["claim"] = m["claim"]
    return r


def instrument(criteria_path: Path | str | None = None):
    def fn(path, item, capability):
        ins = C.inputs_of(item)
        if not ins.get("drive_audio_path"):
            return C.parse_failure("audio_video_synchronisation needs instrument_inputs.drive_audio_path on the item")
        return evaluate(ins["drive_audio_path"], path, criteria_path)
    return C.build_instrument(INSTRUMENT_ID, VERSION, CAPABILITIES, fn, criteria_path, instrument_id=REGISTERED_AS,
                              extra_config={"claim": "partial: audio track offset vs the supplied drive; mouth onset is not measured (MD-C6)"})
