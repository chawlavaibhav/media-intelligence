"""Post-draw gate for the loop: canon.gate.postdraw over the returned artifact.

`artifact_bytes is None` is the dry case — the attempt was rendered and priced, nothing was sent,
nothing came back. The verdict is NOT_RUN with every row saying "no artifact; dry attempt". It is
never PASS: a gate that passed nothing has established nothing.

Detector: whatever the caller supplies (in this tranche canon.gate.textscan.ScriptedDetector from a
JSON fixture keyed on the synthetic artifact's sha256); none means canon.gate.textscan.NoDetector,
whose answer is always `unavailable`, so LIMIT-TEXT reports NOT-RUN. No paid detector is ever
constructed here.
"""
from __future__ import annotations

from canon.gate import postdraw as gate_post
from canon.gate import textscan
from runtime.loop import frame_hygiene, outcome
from runtime.loop.predispatch import compiled_packs, modality_of, registry

DRY_DETAIL = ("no artifact; dry attempt — the attempt was rendered and priced, nothing was sent, no "
              "bytes came back; the post-draw gate cannot run and does not pass")
DRY_ROWS = ("LIMIT-TEXT", "DISPATCH-ASPECT", "INFRA-CONTAINER")


VIDEO_MODALITIES = ("video", "image_sequence")


def run(spec: dict, artifact_bytes, dispatch_descriptor: dict, package_text: str, *,
        product_entity: bool, detector=None, frames=None, record=None, registry_=None,
        source_still_clean=None) -> dict:
    """`frames`: bytes of frames the CALLER sampled from the returned video (the runtime decodes no
    video). For video modality the gate appends RUNTIME-VIDEO-FRAME-TEXT (runtime/loop/frame_hygiene):
    the verdict is FAIL when a sampled frame carries text, and NOT_RUN — not PASS — when no frames were
    sampled, whatever the source still's own scan said (`source_still_clean` is recorded only)."""
    if artifact_bytes is None:
        return outcome.not_run(gate_post.GATE, DRY_ROWS, DRY_DETAIL)
    reg = registry_ or registry()
    det = detector if detector is not None else textscan.NoDetector()
    modality = modality_of(spec)
    frames = list(frames or [])
    report = gate_post.run_postdraw(
        bytes(artifact_bytes), dispatch_descriptor, package_text, det, frames, modality,
        bool(product_entity), reg, label=str(spec.get("spec_id") or "artifact"), record=record,
        packs=compiled_packs(spec))
    if modality not in VIDEO_MODALITIES:
        return outcome.from_report(report)
    detections = [det.detect(f) for f in frames]
    row = frame_hygiene.assess(detections, source_still_clean=source_still_clean)
    out = outcome.from_report(report, extra_rows=[row])
    if row["status"] == "NOT-RUN" and out["verdict"] == outcome.PASS:
        out["verdict"] = outcome.NOT_RUN      # a video nobody sampled has established nothing
    return out
