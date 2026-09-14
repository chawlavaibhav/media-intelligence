"""The reasoning pass for a Stage-A-derived brief IS its frozen blueprint, parsed — never a model call.

Lead's design decision (14 Sep 2026): at USD 0 the planner seam runs from recorded material only.
For a brief derived from a frozen Stage-A case (runtime/tools/brief_from_stage_a_case.py) the
recorded plan is that case's blueprint under
eval/empirical-planning/STAGE-A-FREEZE-2026-09/BLUEPRINTS/<case>.blueprint.md (read-only), and this
module turns it into the planner response shape deterministically:

  objective               a fixed template over the job's kind and aspect plus the FIRST SENTENCE of
                          the customer's own request, verbatim. No fact is invented.
  hard_constraints        the case's Normalized Request `acceptance_intent.hard_constraints`
                          (TEST-CASES.yaml) — the freeze's own reading of the customer's statements.
  acceptance_statements   the case's `acceptance_contract` lines, untouched. They are guarded by the
                          compiler's StyleGuard like any other statement; a line that fails is a
                          refusal naming the line, never an edit.
  composition             CA-D1 / CA-D2 / CA-D3 (and CA-D5 / CA-D6 when present) CASE VALUE text.
  materials_and_light     PA-D1 / PA-D2 / PA-D4 / PA-D5 / PA-D6 CASE VALUE text, or the blueprint's
                          §2a brief-only light/mood lines when no product-appearance decision exists.
  resolution_class        §4 dispatch_parameters `resolution`, as written.
  generation_prompts      the ```text blocks, extracted by eval/harness-v2/casebook.py's own
                          `extract_prompt` (imported, so the two never diverge in parsing).
  planner / source_ref    "stage_a_blueprint_fixture" and the blueprint's path + sha256.

What is deliberately NOT read from the blueprint: §1 packs_selected. The spec's canon.packs_selected
is computed by CanonCorpus from the job; a test checks that the two agree for the cases in use, and
a disagreement is reported, not papered over. `parse_blueprint()` exposes §1 for that test.

Everything here is offline and reads only frozen files.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

from .. import paths
from ..errors import Refusal
from ..util import load_yaml
from .planner_seam import PLANNER_STAGE_A_BLUEPRINT, PlannerPrompt, validate_response

STAGE_A_POOL = "stage_a_case"

_HEADER = re.compile(r"^```yaml\n(.*?)\n```", re.S | re.M)
_PACK_ROW = re.compile(r"^- `([a-z_]+)` — (compiled|uncompiled) — (.+?)\s*$", re.M)
_DECISION = re.compile(r"^### ([A-Z]{2}-D\d+) — (.+?)\n(.*?)(?=^### |^## |\Z)", re.S | re.M)
_CASE_VALUE = re.compile(r"^- \*\*CASE VALUE:\*\* (.+?)\s*$", re.M)
_SECTION = re.compile(r"^## (\d+)\. ([a-z_]+)[^\n]*\n(.*?)(?=^## |\Z)", re.S | re.M)
_SUBSECTION_2A = re.compile(r"^### 2a\.[^\n]*\n(.*?)(?=^### |^## |\Z)", re.S | re.M)
_PARAM = re.compile(r"^- ([a-z_/]+): (.+?)\s*$", re.M)
_SENTENCE_END = re.compile(r"(?<=[.!?।])\s+")

# The blueprint block each prompt slot is read from, in casebook.py's own arm vocabulary. The main
# prompt is `## 6. generation_prompt`; the textless plate is the composite arm's block (or the
# TOPO3 9:16 plate block); the motion prompt is the image-to-video arms' shared block.
_TEXTLESS_ARMS = ("C_composite_textless", "C_plate_9x16")
_MOTION_ARMS = ("A_cheap_still_to_cheap_i2v",)


def _casebook():
    """Import eval/harness-v2/casebook.py the way runtime/route/price.py imports the harness: put the
    harness directory on sys.path, import hv2_paths (path insertions only), then the module."""
    hv2 = Path(paths.HARNESS_V2)
    if not hv2.is_dir():
        raise Refusal(Refusal.BLUEPRINT_UNPARSEABLE, f"{hv2} is not in this checkout", harness=str(hv2))
    if str(hv2) not in sys.path:
        sys.path.insert(0, str(hv2))
    import hv2_paths  # noqa: F401
    import casebook

    return casebook


def parse_blueprint(text: str) -> dict:
    """The blueprint's structure, read mechanically. Raises BLUEPRINT_UNPARSEABLE on a missing part."""
    header = _HEADER.search(text)
    if not header:
        raise Refusal(Refusal.BLUEPRINT_UNPARSEABLE, "blueprint has no leading ```yaml header block")
    import yaml

    head = yaml.safe_load(header.group(1)) or {}
    sections = {name: body for _, name, body in _SECTION.findall(text)}
    for needed in ("packs_selected", "decisions", "dispatch_parameters", "generation_prompt"):
        if needed not in sections:
            raise Refusal(Refusal.BLUEPRINT_UNPARSEABLE, f"blueprint has no '## N. {needed}' section", section=needed)

    packs = [{"pack_id": p, "compiled": status == "compiled", "trigger": trig}
             for p, status, trig in _PACK_ROW.findall(sections["packs_selected"])]
    if not packs:
        raise Refusal(Refusal.BLUEPRINT_UNPARSEABLE, "blueprint §1 lists no packs")

    case_values, questions = {}, {}
    for check_id, question, body in _DECISION.findall(sections["decisions"]):
        found = _CASE_VALUE.search(body)
        if found:
            case_values[check_id] = " ".join(found.group(1).split())
            questions[check_id] = question.strip()

    brief_only: dict = {}
    sub = _SUBSECTION_2A.search(sections["decisions"])
    if sub:
        for key, value in _PARAM.findall(sub.group(1)):
            brief_only.setdefault(key, []).append(" ".join(value.split()))

    dispatch = {key: " ".join(value.split()) for key, value in _PARAM.findall(sections["dispatch_parameters"])}
    text_handling = [" ".join(line[2:].split()) for line in sections.get("text_handling", "").splitlines()
                     if line.startswith("- ")]

    casebook = _casebook()
    main = casebook.extract_prompt(text)
    textless = _first_block(casebook, text, _TEXTLESS_ARMS)
    motion = _first_block(casebook, text, _MOTION_ARMS)
    if motion is None and str(head.get("case_id") or "").startswith(("VID-I2V", "VID-T2V", "VID-MS", "VID-REF", "VID-KNEE", "VID-2SPK")):
        # A video case whose blueprint carries only the single §6 generation_prompt: that prompt IS
        # the motion prompt (the blueprint says it is "byte-identical across every route listed for
        # this case"). Recorded at integration (lead, 14 Sep 2026; dry battery run B05) - the renderer
        # dispatches the `motion` slot for a motion deliverable and never guesses another slot.
        motion = main

    return {
        "case_id": head.get("case_id"),
        "header": head,
        "packs_selected": packs,
        "case_values": case_values,
        "decision_questions": questions,
        "brief_only_parameters": brief_only,
        "dispatch_parameters": dispatch,
        "text_handling": text_handling,
        "generation_prompts": {"main": main, "textless_plate": textless, "motion": motion},
    }


def _first_block(casebook, text: str, arms: tuple) -> str | None:
    for arm in arms:
        try:
            return casebook.extract_prompt(text, arm)
        except ValueError:
            continue
    return None


def first_sentence(text: str) -> str:
    text = " ".join(str(text).split())
    parts = _SENTENCE_END.split(text, maxsplit=1)
    return parts[0] if parts and parts[0] else text


class BlueprintPlanner:
    """Answers `plan(prompt, *, job, nr)` from the frozen blueprint the job's provenance names."""

    def __init__(self, freeze_root: str | Path | None = None, *, provenance: dict):
        self.freeze_root = Path(freeze_root or paths.STAGE_A_FREEZE)
        self.provenance = dict(provenance or {})
        if self.provenance.get("source_pool") != STAGE_A_POOL:
            raise Refusal(
                Refusal.PLANNER_FIXTURE_MISSING,
                f"BlueprintPlanner serves provenance source_pool {STAGE_A_POOL!r} only",
                got=self.provenance.get("source_pool"),
            )
        self.case_id = str(self.provenance.get("case_id") or "")
        if not self.case_id:
            raise Refusal(Refusal.PLANNER_FIXTURE_MISSING, "provenance names no case_id")

    # ------------------------------------------------------------------ inputs
    def case(self) -> dict:
        doc = load_yaml(self.freeze_root / "TEST-CASES.yaml") or {}
        for row in doc.get("cases", []):
            if row.get("case_id") == self.case_id:
                return row
        raise Refusal(
            Refusal.PLANNER_FIXTURE_MISSING,
            f"no Stage-A case {self.case_id!r} in the frozen package; the lane will not call a model",
            case_id=self.case_id,
            test_cases=str(self.freeze_root / "TEST-CASES.yaml"),
        )

    def blueprint_path(self, case: dict) -> Path:
        ref = str(self.provenance.get("blueprint_ref") or case.get("blueprint_ref") or "")
        path = (self.freeze_root / ref).resolve()
        if not ref or self.freeze_root.resolve() not in path.parents or not path.is_file():
            raise Refusal(
                Refusal.PLANNER_FIXTURE_MISSING,
                f"blueprint {ref!r} for case {self.case_id!r} is not a file inside the frozen package",
                case_id=self.case_id,
                blueprint_ref=ref,
            )
        return path

    def read(self, case: dict) -> tuple[Path, bytes, str]:
        path = self.blueprint_path(case)
        data = path.read_bytes()
        sha = hashlib.sha256(data).hexdigest()
        expected = self.provenance.get("blueprint_sha256")
        if expected and expected != sha:
            raise Refusal(
                Refusal.BLUEPRINT_UNPARSEABLE,
                "the brief was derived from a blueprint with different bytes than the one on disk; the "
                "reasoning pass is served from frozen bytes only, so this is a refusal, not a re-plan",
                case_id=self.case_id,
                expected_sha256=expected,
                actual_sha256=sha,
                path=str(path),
            )
        return path, data, sha

    # ------------------------------------------------------------------ the plan
    def plan(self, prompt: PlannerPrompt, *, job: dict, nr=None) -> dict:
        case = self.case()
        path, data, sha = self.read(case)
        parsed = parse_blueprint(data.decode("utf-8"))
        if parsed["case_id"] != self.case_id:
            raise Refusal(
                Refusal.BLUEPRINT_UNPARSEABLE,
                f"blueprint header names case {parsed['case_id']!r}, the brief names {self.case_id!r}",
                path=str(path),
            )
        values = parsed["case_values"]
        request = job["deliverable_request"]
        customer_text = ((case.get("customer_request") or {}).get("text")) or job["brief"]["text"]

        composition = _pick(values, {
            "attention_order": "CA-D1",
            "placement_zone": "CA-D2",
            "edge_treatment": "CA-D3",
            "balance": "CA-D5",
            "aspect_justification": "CA-D6",
        })
        materials = _pick(values, {
            "surface_finish_per_key_object": "PA-D1",
            "highlight_placement": "PA-D2",
            "implied_light_source": "PA-D4",
            "separation": "PA-D5",
            "key_level": "PA-D6",
        })
        light_lines = parsed["brief_only_parameters"].get("light/mood") or []
        if "implied_light_source" not in materials and light_lines:
            materials["implied_light_source"] = " ".join(light_lines)

        intent = (case.get("nr") or {}).get("acceptance_intent") or {}
        hard = [" ".join(str(c).split()) for c in (intent.get("hard_constraints") or [])]
        statements = [" ".join(str(s).split()) for s in (case.get("acceptance_contract") or [])]

        response = {
            "objective": (
                f"Produce one {request['kind']} at {request['aspect']} that answers the customer's "
                f"request: \"{first_sentence(customer_text)}\""
            ),
            "hard_constraints": hard,
            "acceptance_statements": statements,
            "composition": composition,
            "materials_and_light": materials,
            "resolution_class": parsed["dispatch_parameters"].get("resolution") or None,
            "planner": PLANNER_STAGE_A_BLUEPRINT,
            "source_ref": f"{_rel(path)} sha256:{sha}",
            "generation_prompts": parsed["generation_prompts"],
            "case_values": values,
            "production_parameters": {
                "dispatch_parameters": parsed["dispatch_parameters"],
                "brief_only_parameters": parsed["brief_only_parameters"],
                "text_handling": parsed["text_handling"],
                "decision_questions": parsed["decision_questions"],
                "blueprint_header": {k: str(v) for k, v in parsed["header"].items()},
            },
        }
        return validate_response(response, source=str(path))


def _pick(values: dict, mapping: dict) -> dict:
    return {field: values[check_id] for field, check_id in mapping.items() if check_id in values}


def _rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(paths.ROOT))
    except ValueError:
        return str(path)
