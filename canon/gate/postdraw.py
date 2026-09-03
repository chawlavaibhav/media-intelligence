"""Post-draw gate: baked-text scan first, then the artifact's header facts against the
dispatch descriptor and the package (CANON-GATE-001 plan §D post-draw, §E, Rulings 1–2).

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

Without pixel decoding only the artifact's dimensions / aspect / duration and — with a
detector — baked text are checkable, so every doctrine line but CA-D6 reports NOT_MECHANISED
here with its reason. The text scan runs over the artifact (image) or over supplied frames
(video; stdlib cannot decode H.264, so no frames means NOT_RUN, never PASS). A `no_text`
result is a detector's answer about one output, never a certification (EVAL-029).
"""
from __future__ import annotations

import hashlib

from canon.gate import artifact as probes
from canon.gate import package
from canon.gate.findings import TOLERANCES, CheckResult, Report, Status
from canon.gate.predispatch import (DISPATCH_SOURCE, dispatched_aspect, limit_source_tail,
                                    not_selected_reason)

GATE = "post_draw"
INFRA_SOURCE = "plan §E INFRA rows — container, video track, record sha256; not doctrine"

# Plan §A POST column, for the lines that do not mechanise over artifact bytes.
NOT_MECHANISED_POST = {
    "PA-D1-check": "finish per object is a pixel + material judgment",
    "PA-D2-check": "highlight geometry needs decoded pixels and scene understanding",
    "PA-D3-check": "needs shadow/specular measurement in pixels",
    "PA-D4-check": "key/shadow agreement with the declared direction needs pixels",
    "PA-D5-check": "grayscale check needs decoded pixels and product/ground segmentation; the "
                   "production route emits JPEG (no stdlib decoder)",
    "PA-D6-check": "light character and cross-shot key consistency need pixels",
    "PA-D7-check": "semantic judgment ('needs the body copy') — human / blueprint-model check",
    "PA-D8-check": "specular inspection on glass/dark/glossy surfaces needs pixels",
    "PA-D9-check": "face counting needs object understanding in pixels",
    "PA-D10-check": "deviation completeness is a package property; the artifact carries no "
                    "deviation record",
    "CA-D1-check": "read order and 'one dominant cue' need pixels and attention modelling",
    "CA-D2-check": "placement zone and its reason need scene understanding in pixels",
    "CA-D3-check": "edge treatment and tangency need pixels",
    "CA-D4-check": "framing-element tone/width comparison needs pixels",
    "CA-D5-check": "grayscale tonal weight needs pixels",
    "CA-D7-check": "per-cut content is semantic; frame analysis is not available in stdlib",
    "CA-D8-check": "edit-room judgment; no detectable trigger for 'imperfect cut'",
    "CA-D9-check": "screen direction needs frame analysis",
    "CA-D10-check": "'outlasts describable content' is semantic; per-shot timing needs decoded "
                    "frames",
    "CA-D11-check": "camera motion and its motivation need decoded frames",
}
CA_D6_CLAUSE = "The stated aspect is justified by a named shape in the scene"


def _doctrine(line, status, clause, detail, *, blocking=False):
    return CheckResult(check_id=line.check_id, family="doctrine", gate=GATE, status=status,
                       coverage="partial" if clause else "none", clause=clause,
                       source_text=line.text, detail=detail, evidence=(), blocking=blocking)


def _row(check_id, family, status, detail, *, blocking=False, source=INFRA_SOURCE, evidence=()):
    return CheckResult(check_id=check_id, family=family, gate=GATE, status=status,
                       coverage="full", clause="", source_text=source, detail=detail,
                       evidence=tuple(evidence), blocking=blocking)


# ── LIMIT-TEXT over the artifact / frames ────────────────────────────────────

def _not_run_detector(detection, registry_tail):
    if detection.detector_id == "none":
        return ("no text detector configured; the qualified detector (Cloud Vision "
                "TEXT_DETECTION) needs a separate spend authorisation" + registry_tail)
    return (f"{detection.detector_id} unavailable: {detection.raw.get('note', '')}"
            + registry_tail)


def check_limit_text_post(artifact_bytes: bytes, frames, modality: str, detector, registry):
    base = dict(check_id="LIMIT-TEXT", family="limit", gate=GATE, coverage="full", clause="",
                source_text=registry.limit_text, blocking=True)
    tail = f" — source: {limit_source_tail(registry.limit_text)}"
    if modality in ("video", "image_sequence"):
        if not frames:
            return CheckResult(status=Status.NOT_RUN, evidence=(), **base,
                               detail="frame extraction not available in stdlib; supply "
                                      "--frames DIR of JPEG/PNG frames to scan" + tail)
        unavailable, texts = [], []
        for i, frame in enumerate(frames, 1):
            d = detector.detect(frame)
            if d.status == "text":
                texts.append((i, d))
            elif d.status != "no_text":
                unavailable.append(i)
        if texts:
            i, d = texts[0]
            return CheckResult(
                status=Status.FAIL, **base,
                detail=f"frame {i}: text detected ('{d.transcript[:80]}') per {d.detector_id}"
                       + (f"; +{len(texts) - 1} more frame(s)" if len(texts) > 1 else "") + tail,
                evidence=tuple(f"frame {i}: {d.transcript[:200]}" for i, d in texts))
        if unavailable:
            return CheckResult(status=Status.NOT_RUN, evidence=(), **base,
                               detail=f"{len(unavailable)} of {len(frames)} frames unavailable "
                                      f"to {detector.detector_id} — not counted as text-free"
                                      + tail)
        return CheckResult(status=Status.PASS, evidence=(), **base,
                           detail=f"no text detected in {len(frames)} frames per "
                                  f"{detector.detector_id}; benchmark qualification never "
                                  "certifies an individual output (EVAL-029)" + tail)
    d = detector.detect(artifact_bytes)
    if d.status == "text":
        return CheckResult(status=Status.FAIL, evidence=(d.transcript[:200],), **base,
                           detail=f"text detected ('{d.transcript[:80]}') per {d.detector_id}"
                                  + tail)
    if d.status == "no_text":
        return CheckResult(status=Status.PASS, evidence=(), **base,
                           detail=f"no text detected per {d.detector_id}; benchmark "
                                  "qualification never certifies an individual output "
                                  "(EVAL-029)" + tail)
    return CheckResult(status=Status.NOT_RUN, evidence=(), **base,
                       detail=_not_run_detector(d, tail))


# ── geometry ─────────────────────────────────────────────────────────────────

def _aspect_outcome(info, aspect):
    """(ok, detail) or (None, reason) when the comparison cannot run."""
    if info is None or info.width is None:
        return None, "artifact dimensions unavailable"
    if not aspect:
        return None, "no dispatched or declared aspect to compare against"
    try:
        ok, ratio, target = probes.aspect_matches(info.width, info.height, aspect)
    except ValueError as exc:
        return None, str(exc)
    tol = TOLERANCES["aspect_ratio_abs"]
    if ok:
        return True, (f"artifact {info.width}×{info.height} (ratio {ratio:.4f}) matches {aspect} "
                      f"({target:.4f}) within ±{tol}")
    return False, (f"artifact {info.width}×{info.height} (ratio {ratio:.4f}) is not {aspect} "
                   f"({target:.4f}; Δ{abs(ratio - target):.4f} > {tol})")


def check_ca_d6_post(line, info, aspect):
    ok, detail = _aspect_outcome(info, aspect)
    if ok is None:
        return _doctrine(line, Status.NOT_RUN, CA_D6_CLAUSE, detail)
    if ok:
        return _doctrine(line, Status.PASS, CA_D6_CLAUSE, detail)
    return _doctrine(line, Status.FAIL, CA_D6_CLAUSE,
                     detail + " — the check is unanswerable on this artifact")


def check_dispatch_aspect_post(info, aspect):
    ok, detail = _aspect_outcome(info, aspect)
    status = Status.NOT_RUN if ok is None else (Status.PASS if ok else Status.FAIL)
    return _row("DISPATCH-ASPECT", "dispatch", status, detail, blocking=True,
                source=DISPATCH_SOURCE)


def check_dispatch_dimensions(info, pkg):
    if pkg is None:
        return _row("DISPATCH-DIMENSIONS", "dispatch", Status.NOT_RUN,
                    "no package supplied — declared minimum unknown", blocking=True,
                    source=DISPATCH_SOURCE)
    declared = package.declared_min_dimensions(pkg)
    if declared is None:
        return _row("DISPATCH-DIMENSIONS", "dispatch", Status.NOT_RUN,
                    "package declares no minimum dimensions", blocking=True,
                    source=DISPATCH_SOURCE)
    if info is None or info.width is None:
        return _row("DISPATCH-DIMENSIONS", "dispatch", Status.NOT_RUN,
                    "artifact dimensions unavailable", blocking=True, source=DISPATCH_SOURCE)
    w, h = declared
    detail = f"artifact {info.width}×{info.height} against declared minimum {w}×{h}"
    if info.width >= w and info.height >= h:
        return _row("DISPATCH-DIMENSIONS", "dispatch", Status.PASS, detail, blocking=True,
                    source=DISPATCH_SOURCE)
    return _row("DISPATCH-DIMENSIONS", "dispatch", Status.FAIL, detail + " — below the minimum",
                blocking=True, source=DISPATCH_SOURCE)


def check_dispatch_duration(info, declared):
    if info is None or info.duration_s is None:
        note = "; ".join(n for n in (info.notes if info else ()) if "duration" in n)
        return _row("DISPATCH-DURATION", "dispatch", Status.NOT_RUN,
                    "artifact duration unavailable" + (f" ({note})" if note else ""),
                    blocking=True, source=DISPATCH_SOURCE)
    tol = TOLERANCES["duration_s_abs"]
    detail = (f"artifact {info.duration_s:.2f} s against dispatched {declared:g} s "
              f"(tolerance ±{tol} s)")
    ok = abs(info.duration_s - float(declared)) <= tol
    return _row("DISPATCH-DURATION", "dispatch", Status.PASS if ok else Status.FAIL, detail,
                blocking=True, source=DISPATCH_SOURCE)


# ── runner ───────────────────────────────────────────────────────────────────

def run_postdraw(artifact_bytes: bytes, dispatch: dict, package_text, detector, frames,
                 modality: str, product_entity: bool, registry, label: str = "artifact",
                 record=None) -> Report:
    sha = hashlib.sha256(artifact_bytes).hexdigest()
    inputs = {label: sha}
    pkg = None
    if package_text:
        inputs["package"] = hashlib.sha256(package_text.encode("utf-8")).hexdigest()
        pkg = package.parse_package(package_text)
    packs = registry.select_packs(modality, product_entity)
    results = []

    try:
        info = probes.probe(artifact_bytes)
        probe_error = None
    except probes.ProbeError as exc:
        info, probe_error = None, str(exc)

    # 1. baked text first
    if packs:
        results.append(check_limit_text_post(artifact_bytes, frames, modality, detector,
                                             registry))
    else:
        results.append(CheckResult(
            check_id="LIMIT-TEXT", family="limit", gate=GATE, status=Status.NOT_APPLICABLE,
            coverage="full", clause="", source_text=registry.limit_text,
            detail=f"no pack selected for {modality} (trigger table) — the limit line belongs "
                   "to the selected packs", evidence=(), blocking=True))

    # 2. the 21 doctrine lines
    aspect = dispatched_aspect(dispatch) or (package.declared_aspect(pkg) if pkg else None)
    for check_id, line in registry.checks.items():
        if line.pack_id not in packs:
            results.append(_doctrine(line, Status.NOT_APPLICABLE, "",
                                     not_selected_reason(line.pack_id, modality)))
        elif not registry.applicable(check_id, modality):
            results.append(_doctrine(line, Status.NOT_APPLICABLE, "",
                                     registry.applicability_reason(check_id, modality)))
        elif check_id == "CA-D6-check":
            results.append(check_ca_d6_post(line, info, aspect))
        else:
            results.append(_doctrine(line, Status.NOT_MECHANISED, "",
                                     NOT_MECHANISED_POST[check_id]))

    # 3. dispatch family
    video_dispatch = modality in ("video", "image_sequence")
    declared_duration = (dispatch.get("parameters") or {}).get("durationSeconds") \
        if isinstance(dispatch, dict) else None
    if packs:
        results.append(check_dispatch_aspect_post(info, aspect))
        results.append(check_dispatch_dimensions(info, pkg))
        if declared_duration is not None:
            results.append(check_dispatch_duration(info, declared_duration))

    # 4. infra rows
    if probe_error:
        results.append(_row("INFRA-CONTAINER", "infra", Status.ERROR,
                            f"artifact unparsable: {probe_error} — fails closed"))
    elif info.kind == "unknown":
        results.append(_row("INFRA-CONTAINER", "infra", Status.NOT_RUN, "; ".join(info.notes)))
    else:
        geometry = f"{info.width}×{info.height}"
        if info.duration_s is not None:
            geometry += f", {info.duration_s:.2f} s, {info.codec}"
        results.append(_row("INFRA-CONTAINER", "infra", Status.PASS,
                            f"{info.container} {info.kind} {geometry}"
                            + (f" ({'; '.join(info.notes)})" if info.notes else "")))
    if video_dispatch or declared_duration is not None:
        if info is None:
            results.append(_row("INFRA-VIDEO-TRACK", "infra", Status.NOT_RUN,
                                "artifact unparsable"))
        elif info.has_video_track:
            results.append(_row("INFRA-VIDEO-TRACK", "infra", Status.PASS,
                                f"video track present ({info.codec})"
                                + (", audio track present" if info.has_audio_track else
                                   ", no audio track")))
        else:
            results.append(_row("INFRA-VIDEO-TRACK", "infra", Status.FAIL,
                                f"no video track in a {info.container} {info.kind} for a video "
                                "dispatch"))
    if record is None:
        results.append(_row("INFRA-RECORD-SHA", "infra", Status.NOT_RUN,
                            "no record.json supplied"))
    else:
        recorded = str(record.get("sha256") or "")
        if recorded == sha:
            results.append(_row("INFRA-RECORD-SHA", "infra", Status.PASS,
                                f"artifact sha256 {sha[:12]}… equals record.json"))
        else:
            results.append(_row("INFRA-RECORD-SHA", "infra", Status.FAIL,
                                f"artifact sha256 {sha[:12]}… != record.json sha256 "
                                f"{recorded[:12] or '(missing)'}…"))

    return Report(gate=GATE, inputs=inputs, packs_selected=packs, results=results,
                  label=f"artifact {label} (sha256 {sha[:12]})")
