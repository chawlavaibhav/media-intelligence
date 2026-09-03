"""Pre-dispatch gate: the packs' check lines run over the package text, the generation
prompts and the dispatch descriptor (CANON-GATE-001 plan §A, §B predispatch.py, Rulings 1–3).

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

One function per mechanised id, each returning exactly one CheckResult; the runner appends a
NOT_MECHANISED / NOT_APPLICABLE row for every registry id it did not run, so every report
lists all 21 doctrine ids. A partial check tests the quoted literal clause as a necessary
condition only and prints that clause. Blocking rows (Ruling 2): LIMIT-TEXT, DISPATCH-*,
CA-D2 clause 2, and any ERROR.
"""
from __future__ import annotations

from canon.gate import textscan
from canon.gate.findings import CheckResult, Status

GATE = "pre_dispatch"


def limit_source_tail(limit_text: str) -> str:
    tail = limit_text.rsplit(";", 1)[-1].strip()
    return f'pack_limits "… {tail}"'


def _describe_hit(prompt_index: int, hit: textscan.TextHit) -> str:
    terms = ", ".join(f"'{t}'" for t in hit.terms[:4])
    where = f"prompt {prompt_index}, sentence {hit.sentence_index}"
    if hit.subcheck == "T1":
        return f"{where} contains Devanagari glyphs ({terms})"
    if hit.subcheck == "T2":
        return f"{where} requests rendered text ({terms}) with no negation/deferral"
    return f"{where} requests text-bearing surfaces ({terms}) with no illegibility/deferral term"


def check_limit_text(prompts: list, registry) -> CheckResult:
    """LIMIT-TEXT pre-dispatch (§D T1–T3) over every extracted generation prompt."""
    base = dict(check_id="LIMIT-TEXT", family="limit", gate=GATE, coverage="full",
                clause="", source_text=registry.limit_text, blocking=True)
    if not prompts:
        return CheckResult(status=Status.ERROR, evidence=(),
                           detail="no generation prompt could be extracted from "
                                  "GENERATION_PROMPTS (or supplied) — fails closed", **base)
    source = f" — source: {limit_source_tail(registry.limit_text)}"
    descriptions, evidence, clause_in = [], [], []
    for i, text in enumerate(prompts, 1):
        scan = textscan.scan_prompt(text)
        if scan.no_text_clause:
            clause_in.append(str(i))
        for hit in scan.hits:
            descriptions.append(_describe_hit(i, hit))
            evidence.append(f"prompt {i}, sentence {hit.sentence_index} [{hit.subcheck}]: "
                            f"{hit.sentence[:200]}")
    if descriptions:
        more = f"; +{len(descriptions) - 1} more hit(s)" if len(descriptions) > 1 else ""
        return CheckResult(status=Status.FAIL, detail=descriptions[0] + more + source,
                           evidence=tuple(evidence), **base)
    clause_note = (f"explicit no-text clause present (prompt {', '.join(clause_in)})"
                   if clause_in else "no explicit no-text clause in any prompt")
    return CheckResult(status=Status.PASS, evidence=(),
                       detail=f"no Devanagari, requested text or text-bearing surface in "
                              f"{len(prompts)} prompt(s); {clause_note}{source}", **base)
