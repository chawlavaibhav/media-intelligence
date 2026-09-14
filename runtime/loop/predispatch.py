"""Pre-dispatch gate for the loop: canon.gate.predispatch over the rendered package, plus one
runtime row the gate does not own.

DISPATCH DESCRIPTOR. The gate compares the package's declared aspect against the request the
provider would receive, read in the committed `request.json` shapes (canon/gate/run_gate.py):
  image: {"generationConfig": {"imageConfig": {"aspectRatio": "W:H"}}}
  video: {"parameters": {"aspectRatio": "W:H", "durationSeconds": N}}
`dispatch_descriptor(spec)` builds those from PRODUCTION-SPEC-v1 fields — deliverable.aspect and,
for motion, deliverable.motion.seconds. The spec carries a resolution CLASS (social_still,
social_video), not a pixel resolution, so no `resolution` key is written; the gate does not read
one. Lane F's manifest carries the real request body; when the driver has an attempt it passes
that attempt's descriptor instead if one is present (see driver.descriptor_for).

MODALITY comes from runtime/canon/KIND-NR-BINDING-v0.yaml via runtime.canon.normalize.KindBinding
(a row per deliverable kind); nothing here names a kind.

PACKS. The spec's canon.packs_selected rows that say compiled: true are handed to the gate as its
pack set. A spec that names no compiled pack (the committed fixtures) hands selection to the gate's
own trigger table (packs=None) — the runtime never switches LIMIT-TEXT off by passing an empty
override, because an empty override makes the limit NOT-APPLICABLE.

RUNTIME-PLATE-NO-LETTERING-INSTRUCTION. Under deterministic code composition the plate must carry an
explicit no-lettering instruction (the Stage-A blueprints' `no-in-image-text` check; the spec's
baked_text_scan). The gate's LIMIT-TEXT already reports whether such a clause is present, in its
PASS detail, but does not fail on its absence — so this row does, using the gate's own
NO_TEXT_CLAUSE vocabulary over the same extracted prompt. No words are added to the prompt.
"""
from __future__ import annotations

from canon.gate import doctrine, package as gate_pkg, textscan
from canon.gate import predispatch as gate_pre
from canon.gate.findings import Status
from runtime.canon.normalize import KindBinding
from runtime.errors import Refusal
from runtime.loop import outcome, package, refusals

PLATE_ROW = "RUNTIME-PLATE-NO-LETTERING-INSTRUCTION"
_REGISTRY = None
_BINDING = None


def registry():
    global _REGISTRY
    if _REGISTRY is None:
        _REGISTRY = doctrine.load_registry()
    return _REGISTRY


def modality_of(spec: dict) -> str:
    global _BINDING
    if _BINDING is None:
        _BINDING = KindBinding()
    kind = (spec.get("deliverable") or {}).get("kind")
    try:
        return str(_BINDING.row(kind)["modality"])
    except Refusal as exc:
        raise Refusal(refusals.MODALITY_BINDING_MISSING, exc.message, **exc.context) from None


def compiled_packs(spec: dict):
    rows = (spec.get("canon") or {}).get("packs_selected") or []
    ids = [str(r["pack_id"]) for r in rows if isinstance(r, dict) and r.get("compiled") is True]
    return ids or None


def dispatch_descriptor(spec: dict) -> dict:
    deliverable = spec["deliverable"]
    aspect = str(deliverable["aspect"])
    if modality_of(spec) in ("video", "image_sequence"):
        params = {"aspectRatio": aspect}
        seconds = (deliverable.get("motion") or {}).get("seconds")
        if seconds is not None:
            params["durationSeconds"] = int(seconds)
        return {"parameters": params}
    return {"generationConfig": {"imageConfig": {"aspectRatio": aspect}}}


def plate_row(spec: dict, package_text: str) -> dict:
    if package.text_mechanism(spec) != "deterministic_text_composition":
        return outcome.runtime_row(PLATE_ROW, Status.NOT_APPLICABLE.value,
                                  "the exact-text mechanism is not deterministic code composition; "
                                  "there is no textless plate to check", blocking=True)
    try:
        prompts = gate_pkg.extract_prompts(gate_pkg.parse_package(package_text))
    except gate_pkg.ExtractionError as exc:
        return outcome.runtime_row(PLATE_ROW, Status.ERROR.value,
                                  f"the plate prompt could not be extracted: {exc}")
    if not prompts:
        return outcome.runtime_row(PLATE_ROW, Status.ERROR.value, "no plate prompt in the package")
    m = textscan.NO_TEXT_CLAUSE.search(prompts[0].text)
    if m:
        return outcome.runtime_row(PLATE_ROW, Status.PASS.value,
                                  f"the plate prompt carries an explicit no-lettering instruction "
                                  f"('{m.group(0)}') — gate vocabulary NO_TEXT_CLAUSE")
    return outcome.runtime_row(PLATE_ROW, Status.FAIL.value,
                              "the textless plate prompt carries no explicit no-lettering instruction "
                              "(gate vocabulary NO_TEXT_CLAUSE matched nothing); under deterministic "
                              "code composition lettering on the plate is a reject, so the plate is "
                              "not dispatched. The runtime adds no words to a prompt; the planner "
                              "must supply the instruction", blocking=True)


def run(spec: dict, package_text: str, dispatch_descriptor: dict, *, product_entity: bool,
        registry_=None) -> dict:
    reg = registry_ or registry()
    report = gate_pre.run_predispatch(
        package_text, None, dispatch_descriptor, modality_of(spec), bool(product_entity), reg,
        label=str(spec.get("spec_id") or "package"), packs=compiled_packs(spec))
    return outcome.from_report(report, extra_rows=[plate_row(spec, package_text)])
