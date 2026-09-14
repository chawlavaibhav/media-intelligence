"""Render a FINAL_PRODUCTION_PACKAGE (schema v2) from a PRODUCTION-SPEC-v1 and its blueprint.

WHY A RENDERER. The Canon gate (canon/gate) reads one text shape — the package the Lab's planning
models wrote — and its parser is deliberately strict (Rulings 7-12: straight quotes only, a
120-character prompt floor, a closed set of section headings, nothing unknown after the prompts).
The runtime has a spec and a blueprint, not a package, so this module writes the package FROM those
two objects, and the gate then judges it exactly as it judges a Lab package. Nothing here judges
anything: the doctrine rows come from `canon.gate`.

WHAT THE PARSER BIT, AND HOW EACH RULE IS OBEYED (canon/gate/package.py):
- SECTION_RE reads ANY bare ALL-CAPS line of four or more letters as a heading. So every spec value
  is rendered inside a bullet ("- ...") or after a lower-case label, never alone on a line; a
  constraint that reads "IMPORTANT" cannot open a section. After rendering, the heading list is
  compared with the intended order and any surprise is a refusal (PACKAGE_STRAY_HEADING).
- Headings after GENERATION_PROMPTS must be in KNOWN_HEADINGS_AFTER_PROMPTS and appear once. The
  order used is the one every committed EVAL-038 v2 package carries: ... GENERATION_PROMPTS,
  DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS, FAILURE_PREVENTION, HARD_CONSTRAINT_CHECK.
- Prompts are straight-double-quoted runs. A curly quote is an extraction error at the gate, so it
  is a refusal here (PACKAGE_CURLY_QUOTE). A run under PROMPT_MIN_CHARS is an extraction error at
  the gate, so it is a refusal here (PACKAGE_PROMPT_BELOW_FLOOR) — never padded.
- A line beginning "1. " inside PRODUCTION_RECIPE or GENERATION_PROMPTS is a shot. Static packages
  therefore carry no numbered lines; the motion package carries exactly one ("1. Shot 1 — N s").
- The declared aspect is read from DELIVERABLE as "W:H aspect ratio"; the declared duration as
  "N seconds"; neither section mentions a minimum W×H, so DISPATCH-DIMENSIONS reports NOT_RUN
  (the spec carries a resolution_class, not pixel minima — reported, not invented).

WHICH PROMPT GOES IN (C-6c). The exact-text mechanism decides the route identity, so it decides
the prompt set: under `deterministic_text_composition` only the textless plate is in the package
(it is the one dispatched; the in-scene "main" prompt belongs to mechanism A and is left out, not
quoted); under `model_draws_text` the main prompt; under `not_applicable` the main prompt, or the
motion prompt when the deliverable is the motion version. No words are added to any prompt.

TYPED SUBFIELDS. The four VISUAL_SYSTEM subfields are filled, in this precedence, from (1) the
same-named key in spec.composition / spec.materials_and_light, (2) the blueprint's case_values for
the decisions whose `feeds_sections` (read from the compiled packs) name that subfield, (3) the
literal phrase NOT_STATED. The gate then reports what it finds; a subfield reading "not stated by
the plan" earns a non-blocking declaration FAIL, which is the truth.
"""
from __future__ import annotations

import functools
import re

from canon.gate import doctrine
from canon.gate import package as gate_pkg
from runtime.errors import Refusal
from runtime.loop import refusals

NOT_STATED = "not stated by the plan"
SECTION_ORDER_STATIC = (
    "FINAL_PRODUCTION_PACKAGE", "DELIVERABLE", "OBJECTIVE_INTERPRETATION", "CORE_CREATIVE_IDEA",
    "MESSAGE_AND_INFORMATION_HIERARCHY", "VISUAL_SYSTEM", "PRODUCTION_RECIPE", "GENERATION_PROMPTS",
    "DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS", "FAILURE_PREVENTION", "HARD_CONSTRAINT_CHECK",
)
SECTION_ORDER_MOTION = SECTION_ORDER_STATIC
TEXT_MECHANISMS = ("deterministic_text_composition", "model_draws_text", "not_applicable")
# The committed route fixtures predate lane E's `text_mechanism` key and carry only `strategy`;
# this is the fallback reading, documented in WAVE2-INTERFACES §1 vocabulary.
STRATEGY_TO_MECHANISM = {
    "code_set_on_textless_plate": "deterministic_text_composition",
    "generated_in_scene": "model_draws_text",
    "none_required": "not_applicable",
    "no_exact_text": "not_applicable",
}
CURLY = re.compile("[“”‘’]")


def _one_line(value) -> str:
    """Collapse whitespace so no spec value can span lines (a bare line could read as a heading)."""
    return " ".join(str(value).split())


def text_mechanism(spec: dict) -> str:
    et = spec.get("exact_text") or {}
    mech = et.get("text_mechanism")
    if mech is None:
        mech = STRATEGY_TO_MECHANISM.get(et.get("strategy"))
    if mech not in TEXT_MECHANISMS:
        raise Refusal(refusals.PACKAGE_TEXT_MECHANISM_UNKNOWN,
                      "the spec's exact_text.text_mechanism is not one the renderer knows; the "
                      "mechanism decides which prompt is dispatched (C-6c), so it is never guessed",
                      got=et.get("text_mechanism", et.get("strategy")), known=list(TEXT_MECHANISMS))
    return mech


def is_motion(spec: dict) -> bool:
    return bool((spec.get("deliverable") or {}).get("motion"))


def dispatched_prompt_slot(spec: dict) -> str:
    """Which blueprint prompt is the one sent: motion | textless_plate | main."""
    if is_motion(spec):
        return "motion"
    if text_mechanism(spec) == "deterministic_text_composition":
        return "textless_plate"
    return "main"


def _check_prompt(slot: str, value) -> str:
    if not isinstance(value, str) or not value.strip():
        raise Refusal(refusals.PACKAGE_PROMPT_MISSING,
                      f"the blueprint carries no {slot!r} prompt and the spec's mechanism dispatches "
                      f"that slot; the renderer never writes a prompt of its own", slot=slot)
    if CURLY.search(value):
        raise Refusal(refusals.PACKAGE_CURLY_QUOTE,
                      f"the {slot!r} prompt carries a curly quote; the gate reads only straight "
                      f"quotes as prompt delimiters (Ruling 10) and the renderer does not rewrite "
                      f"prompts", slot=slot)
    if len(value) < gate_pkg.PROMPT_MIN_CHARS:
        raise Refusal(refusals.PACKAGE_PROMPT_BELOW_FLOOR,
                      f"the {slot!r} prompt is {len(value)} chars, under the gate's "
                      f"{gate_pkg.PROMPT_MIN_CHARS}-char floor (Ruling 9); a short prompt is refused, "
                      f"never padded", slot=slot, length=len(value), floor=gate_pkg.PROMPT_MIN_CHARS)
    return value


@functools.lru_cache(maxsize=1)
def _subfield_feeders() -> dict:
    """subfield -> [check_id, ...] whose pack line names VISUAL_SYSTEM.<subfield> in feeds_sections,
    in registry order. Read from the compiled packs, not hand-typed."""
    registry = doctrine.load_registry()
    out = {name: [] for name in gate_pkg.TYPED_SUBFIELDS}
    for check_id, line in registry.checks.items():
        for feed in line.feeds_sections:
            if feed.startswith("VISUAL_SYSTEM."):
                sub = feed.split(".", 1)[1]
                if sub in out:
                    out[sub].append(check_id)
    return out


def subfield_values(spec: dict, blueprint: dict) -> dict:
    composition = spec.get("composition") or {}
    materials = spec.get("materials_and_light") or {}
    case_values = (blueprint or {}).get("case_values") or {}
    feeders = _subfield_feeders()
    out = {}
    for name in gate_pkg.TYPED_SUBFIELDS:
        value = composition.get(name) or materials.get(name)
        if value:
            out[name] = _one_line(value)
            continue
        parts = [_one_line(case_values[cid]) for cid in feeders[name] if case_values.get(cid)]
        out[name] = " ".join(parts) if parts else NOT_STATED
    return out


def _bullets(items) -> list:
    return [f"- {_one_line(i)}" for i in items] or ["- none stated by the plan"]


def render_package(spec: dict, blueprint: dict) -> str:
    mech = text_mechanism(spec)
    motion = is_motion(spec)
    deliverable = spec.get("deliverable") or {}
    aspect = _one_line(deliverable.get("aspect") or "")
    if not re.fullmatch(r"\d{1,2}:\d{1,2}", aspect):
        raise Refusal(refusals.PACKAGE_STRAY_HEADING.replace("STRAY_HEADING", "ASPECT_UNREADABLE"),
                      "deliverable.aspect must be W:H so the gate can read the declared aspect",
                      got=aspect)
    prompts = (blueprint or {}).get("generation_prompts") or {}
    slot = dispatched_prompt_slot(spec)
    dispatched = _check_prompt(slot, prompts.get(slot))
    strings = (spec.get("exact_text") or {}).get("strings") or []
    source_ref = _one_line((blueprint or {}).get("source_ref") or "not stated by the plan")
    planner = _one_line((blueprint or {}).get("planner") or "not stated by the plan")
    subs = subfield_values(spec, blueprint)

    L = ["# FINAL_PRODUCTION_PACKAGE", ""]

    # DELIVERABLE — the gate reads the aspect and, for motion, the duration from here.
    L += ["## DELIVERABLE", ""]
    line = (f"One {_one_line(deliverable.get('kind'))} deliverable, {aspect} aspect ratio"
            f", resolution class {_one_line(deliverable.get('resolution_class') or 'not stated by the plan')}.")
    L.append(line)
    if motion:
        m = deliverable["motion"]
        L.append(f"Duration {int(m.get('seconds'))} seconds; shot count 1; audio: "
                 f"{'present' if m.get('audio') else 'none (silent)'}; derived from "
                 f"{_one_line(m.get('from') or 'not stated by the plan')} "
                 f"({_one_line(m.get('depends_on') or 'no dependency named')}).")
    L.append("")

    L += ["## OBJECTIVE_INTERPRETATION", "",
          f"The plan's objective, verbatim: {_one_line(spec.get('objective') or NOT_STATED)}",
          "Interpretation beyond the plan's words: none added by the runtime.", ""]

    L += ["## CORE_CREATIVE_IDEA", "",
          f"As the planner's blueprint states it (planner {planner}; source {source_ref}). The "
          f"dispatched prompt under the prompts section is the idea in full; the runtime adds no "
          f"creative content."]
    focal = (spec.get("composition") or {}).get("focal_intent")
    if focal:
        L.append(f"Focal intent, the plan's words: {_one_line(focal)}")
    L.append("")

    L += ["## MESSAGE_AND_INFORMATION_HIERARCHY", ""]
    L.append(f"- Primary message, the plan's objective: {_one_line(spec.get('objective') or NOT_STATED)}")
    if strings:
        how = {"deterministic_text_composition": "composited by code onto the textless plate, never drawn by the model",
               "model_draws_text": "drawn by the model in scene (mechanism A)",
               "not_applicable": "not applicable"}[mech]
        L.append(f"- Exact copy ({how}): " + "; ".join(_one_line(s.get("value")) for s in strings))
    else:
        L.append("- Exact copy: none in this plan.")
    L.append("- Read order: see the attention_order subfield below.")
    L.append("")

    L += ["## VISUAL_SYSTEM", ""]
    for name in gate_pkg.TYPED_SUBFIELDS:
        L.append(f"{name}: {subs[name]}")
    L.append("")

    L += ["## PRODUCTION_RECIPE", ""]
    L.append(f"- Exact-text mechanism: {mech} (route identity per C-6c).")
    L.append(f"- Dispatched prompt: the {slot} prompt below; no other prompt is sent.")
    if mech == "deterministic_text_composition" and prompts.get("main"):
        L.append("- The blueprint's in-scene main prompt is not dispatched under this mechanism and "
                 "is omitted from this package (it belongs to a different route identity).")
    if motion:
        m = deliverable["motion"]
        L.append(f"1. Shot 1 — {int(m.get('seconds'))} seconds: the accepted still, moving; the frame "
                 f"holds; audio {'present' if m.get('audio') else 'none'}.")
    for key, val in (spec.get("composition") or {}).items():
        if key not in gate_pkg.TYPED_SUBFIELDS and key != "focal_intent":
            L.append(f"- composition.{key}: {_one_line(val)}")
    for key, val in (spec.get("materials_and_light") or {}).items():
        if key not in gate_pkg.TYPED_SUBFIELDS:
            L.append(f"- materials_and_light.{key}: {_one_line(val)}")
    L.append("")

    L += ["## GENERATION_PROMPTS", ""]
    label = {"textless_plate": "Dispatched prompt, the textless plate (the text mechanism is deterministic "
                               "code composition, so this is the only prompt sent):",
             "main": "Dispatched prompt (main):",
             "motion": "Dispatched prompt (motion, from the accepted still):"}[slot]
    L += [label, f'"{dispatched}"', ""]

    L += ["## DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS", ""]
    if mech == "deterministic_text_composition":
        L.append("Code composes these exact strings onto the textless plate after the draw; the model "
                 "never renders this copy (C-6c):")
        for i, s in enumerate(strings, 1):
            L.append(f"- string {i} (script {_one_line(s.get('script') or 'not stated')}, placement "
                     f"{_one_line(s.get('placement') or 'not stated')}, may_reflow "
                     f"{str(bool(s.get('may_reflow'))).lower()}): {_one_line(s.get('value'))}")
    elif mech == "model_draws_text":
        L.append("No code-composed elements: the exact strings are drawn by the model in scene "
                 "(mechanism A) and verified against the draw:")
        for i, s in enumerate(strings, 1):
            L.append(f"- string {i}: {_one_line(s.get('value'))}")
    else:
        L.append("- none: the plan carries no exact text to compose.")
    L.append("Deterministic checks run by code, never shown to the approver: "
             + ", ".join(_one_line(c) for c in spec.get("deterministic_checks") or []) + ".")
    L.append("")

    L += ["## FAILURE_PREVENTION", ""]
    L.append("Gate requirements the spec names:")
    L += _bullets(spec.get("gate_requirements") or [])
    excl = spec.get("route_exclusions") or []
    if excl:
        L.append("Routes the spec excludes, with the plan's reason:")
        L += [f"- {_one_line(e.get('route_key'))}: {_one_line(e.get('reason'))}" for e in excl]
    L.append("")

    L += ["## HARD_CONSTRAINT_CHECK", ""]
    L.append("The plan's hard constraints, verbatim:")
    L += _bullets(spec.get("hard_constraints") or [])
    L.append("")

    text = "\n".join(L)
    _verify(text)
    return text


def _verify(text: str) -> None:
    headings = gate_pkg.section_headings(text)
    if headings != list(SECTION_ORDER_STATIC):
        raise Refusal(refusals.PACKAGE_STRAY_HEADING,
                      "a rendered line reads as a section heading the renderer did not intend; the "
                      "gate would cut the package there, so the package is refused",
                      got=headings, expected=list(SECTION_ORDER_STATIC))
    try:
        found = gate_pkg.extract_prompts(gate_pkg.parse_package(text))
    except gate_pkg.CurlyQuotes as exc:
        raise Refusal(refusals.PACKAGE_CURLY_QUOTE, str(exc)) from None
    except gate_pkg.PromptBelowFloor as exc:
        raise Refusal(refusals.PACKAGE_PROMPT_BELOW_FLOOR, str(exc), floor=gate_pkg.PROMPT_MIN_CHARS) from None
    except gate_pkg.ExtractionError as exc:
        raise Refusal(refusals.PACKAGE_PROMPT_UNEXTRACTABLE,
                      f"the gate cannot extract the prompt from the rendered package: {exc}") from None
    if len(found) != 1:
        raise Refusal(refusals.PACKAGE_PROMPT_UNEXTRACTABLE,
                      "the rendered package must yield exactly the one dispatched prompt",
                      extracted=len(found))
