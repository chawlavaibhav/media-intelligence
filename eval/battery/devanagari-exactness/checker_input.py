#!/usr/bin/env python3
"""
Checker-facing input projection, and the pre-run leak check that proves it is safe.

WHY THIS FILE EXISTS  (Controller review fix 1)
    The two checker shapes are different experiments, and an earlier version of the contract
    quietly broke one of them. It said "the checker receives an image and a target string" while
    also describing shape 1 as an *indirect* test in which the model commits to what it sees and
    OUR code does the comparison. Both cannot be true. If the model is shown the target, it is no
    longer transcribing without knowing the expected answer — which is precisely the pressure the
    indirect shape exists to remove.

        SHAPE 1  transcribe   image + a frozen transcription-only prompt.
                              The target is EVALUATOR-SIDE ONLY. The model never sees it.
                              verdict = canonical_equal(transcription, target), computed by us.

        SHAPE 2  verdict      image + target + a frozen exact-match prompt.
                              The model returns match / mismatch / refused / error.
                              Deliberately exposed: this is the production-like wiring, and the
                              plausible answer is visible in the prompt.

    Comparing the two measures how much of a checker's false-pass behaviour is caused by *showing
    it the answer we hope for*. That comparison is only meaningful if shape 1 really is blind.

    Everything here is mechanical rather than prose: a projection function per shape, an explicit
    allow-list, and `verify_blind()`, which must be run and must return no violations before any
    checker call is made.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from devtext import has_devanagari

# --------------------------------------------------------------------------------------------
# Frozen prompts
# --------------------------------------------------------------------------------------------
# Frozen before any run. Changing either after seeing results and reporting it as the same run is
# an EXPERIMENT MUTATION stop under shared/AUTONOMY-POLICY.md. The sha256 of each is recorded
# with the run so a changed prompt is detectable rather than arguable.

PROMPT_TRANSCRIBE = (
    "Transcribe the text visible in this image, exactly as it appears.\n"
    "Output only the transcription and nothing else.\n"
    "Do NOT correct spelling. Do NOT guess what it was meant to say. "
    "If a character looks wrong or unusual, transcribe what is actually drawn."
)

PROMPT_VERDICT = (
    "Does the text visible in this image match the following target string exactly, "
    "character for character?\n"
    "TARGET: {target}\n"
    "Answer with exactly one word: MATCH or MISMATCH.\n"
    "Do NOT correct spelling. Do NOT allow for a plausible intended reading. "
    "Judge only what is actually drawn against the target as given."
)


def prompt_sha256(p: str) -> str:
    return hashlib.sha256(p.encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------------------------
# Field allow-lists
# --------------------------------------------------------------------------------------------
# An allow-list, not a deny-list. A deny-list silently ships any field added later; an allow-list
# fails closed.

TRANSCRIBE_FIELDS = ("item_id", "image_file", "image_file_sha256", "checker_shape", "prompt")
VERDICT_FIELDS = ("item_id", "image_file", "image_file_sha256", "checker_shape", "target_string",
                  "prompt")

# Fields in the build manifest that reveal, or help infer, the expected answer. None of these may
# appear in either checker payload.
GROUND_TRUTH_FIELDS = frozenset({
    "rendered_string", "expected_verdict", "failure_class", "failure_group", "direction",
    "plausibility", "edit_detail", "base_word", "base_provenance", "rendered_shape",
    "target_shape", "rendered_pixel_sha256", "target_pixel_sha256", "hard_opportunity",
    "items_sharing_this_image", "render_spec", "glyphs_differ",
})

# `target_string` is ground truth *for shape 1* and legitimate input *for shape 2*. It is
# therefore handled by shape rather than by this set.
TARGET_FIELD = "target_string"


# --------------------------------------------------------------------------------------------
# Projections
# --------------------------------------------------------------------------------------------
def project_transcribe(item: dict) -> dict:
    """Checker-facing payload for shape 1. Contains no target and no answer-revealing metadata."""
    return {
        "item_id": item["item_id"],
        "image_file": item["image_file"],
        "image_file_sha256": item["image_file_sha256"],
        "checker_shape": "transcribe",
        "prompt": PROMPT_TRANSCRIBE,
    }


def project_verdict(item: dict) -> dict:
    """Checker-facing payload for shape 2. Contains the target, by design."""
    return {
        "item_id": item["item_id"],
        "image_file": item["image_file"],
        "image_file_sha256": item["image_file_sha256"],
        "checker_shape": "verdict",
        "target_string": item["target_string"],
        "prompt": PROMPT_VERDICT.format(target=item["target_string"]),
    }


def scoring_record(item: dict) -> dict:
    """Evaluator-side record. Retains the target and the constructed answer.

    Written to a separate file that is never handed to a checker. Shape 1 cannot be scored
    without it, which is exactly why it must live apart from the checker input.
    """
    return {
        "item_id": item["item_id"],
        "target_string": item["target_string"],
        "rendered_string": item["rendered_string"],
        "expected_verdict": item["expected_verdict"],
        "direction": item.get("direction"),
        "plausibility": item.get("plausibility"),
        "failure_class": item.get("failure_class"),
        "failure_group": item.get("failure_group"),
        "base_word": item.get("base_word"),
        "hard_opportunity": item.get("hard_opportunity", False),
    }


# --------------------------------------------------------------------------------------------
# Pre-run leak check
# --------------------------------------------------------------------------------------------
def verify_blind(payloads: list[dict], shape: str) -> list[str]:
    """Return a list of violations. **An empty list is the only acceptable result before a run.**

    Checks, per payload:
      * only allow-listed keys are present;
      * no ground-truth metadata field appears;
      * for `transcribe`: no target field, and — the check that would catch a leak arriving by
        some field we did not anticipate — **no Devanagari character anywhere in the payload**.
        The battery's targets are Devanagari, so their presence in a blind payload is decisive
        regardless of what the field is called.
      * for `verdict`: the target IS present, and the prompt actually carries it.
    """
    allowed = set(TRANSCRIBE_FIELDS if shape == "transcribe" else VERDICT_FIELDS)
    violations: list[str] = []
    for p in payloads:
        iid = p.get("item_id", "<no id>")
        extra = set(p) - allowed
        if extra:
            violations.append(f"{iid}: unexpected field(s) in {shape} payload: {sorted(extra)}")
        leaked = set(p) & GROUND_TRUTH_FIELDS
        if leaked:
            violations.append(f"{iid}: ground-truth field(s) leaked: {sorted(leaked)}")
        if p.get("checker_shape") != shape:
            violations.append(f"{iid}: checker_shape is {p.get('checker_shape')!r}, expected {shape!r}")

        if shape == "transcribe":
            if TARGET_FIELD in p:
                violations.append(f"{iid}: transcribe payload contains {TARGET_FIELD}")
            for k, v in p.items():
                if isinstance(v, str) and has_devanagari(v):
                    violations.append(
                        f"{iid}: transcribe payload field {k!r} contains Devanagari text — "
                        f"the target must never be visible in this shape")
        else:
            if not p.get(TARGET_FIELD):
                violations.append(f"{iid}: verdict payload is missing {TARGET_FIELD}")
            elif p.get(TARGET_FIELD) not in p.get("prompt", ""):
                violations.append(f"{iid}: verdict prompt does not carry the target string")
    return violations


def write_checker_inputs(items: list[dict], out_dir: Path) -> dict:
    """Write both checker-facing files plus the evaluator-side scoring key.

    Raises if either projection fails its blind check, so a leaking file cannot be written and
    then used by mistake.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    transcribe = [project_transcribe(i) for i in items]
    verdict = [project_verdict(i) for i in items]

    for payloads, shape in ((transcribe, "transcribe"), (verdict, "verdict")):
        v = verify_blind(payloads, shape)
        if v:
            raise RuntimeError(f"{shape} projection failed its blind check:\n  " + "\n  ".join(v))

    paths = {}
    for name, rows in (("checker-input-transcribe.jsonl", transcribe),
                       ("checker-input-verdict.jsonl", verdict),
                       ("scoring-key.jsonl", [scoring_record(i) for i in items])):
        p = out_dir / name
        p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows),
                     encoding="utf-8")
        paths[name] = p
    return paths
