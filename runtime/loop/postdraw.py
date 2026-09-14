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
from runtime.loop import outcome
from runtime.loop.predispatch import compiled_packs, modality_of, registry

DRY_DETAIL = ("no artifact; dry attempt — the attempt was rendered and priced, nothing was sent, no "
              "bytes came back; the post-draw gate cannot run and does not pass")
DRY_ROWS = ("LIMIT-TEXT", "DISPATCH-ASPECT", "INFRA-CONTAINER")


def run(spec: dict, artifact_bytes, dispatch_descriptor: dict, package_text: str, *,
        product_entity: bool, detector=None, frames=None, record=None, registry_=None) -> dict:
    if artifact_bytes is None:
        return outcome.not_run(gate_post.GATE, DRY_ROWS, DRY_DETAIL)
    reg = registry_ or registry()
    report = gate_post.run_postdraw(
        bytes(artifact_bytes), dispatch_descriptor, package_text,
        detector if detector is not None else textscan.NoDetector(), frames, modality_of(spec),
        bool(product_entity), reg, label=str(spec.get("spec_id") or "artifact"), record=record,
        packs=compiled_packs(spec))
    return outcome.from_report(report)
