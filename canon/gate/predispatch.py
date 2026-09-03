"""Pre-dispatch gate: the packs' check lines run over the package text, the generation
prompts and the dispatch descriptor (CANON-GATE-001 plan §A, §B predispatch.py, Rulings 1–3).

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

One function per mechanised id, each returning exactly one CheckResult; the runner appends a
NOT_MECHANISED / NOT_APPLICABLE row for every registry id it did not run, so every report
lists all 21 doctrine ids. A partial check tests the quoted literal clause as a necessary
condition only and prints that clause. Scan scope = the decision's committed feeds_sections
(typed subfield first, prose fallback — Ruling 3) plus GENERATION_PROMPTS. Blocking rows
(Ruling 2): LIMIT-TEXT, DISPATCH-*, CA-D2 clause 2, and any ERROR.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass

from canon.gate import package, textscan, vocab
from canon.gate.findings import TOLERANCES, CheckResult, Report, Status

GATE = "pre_dispatch"

# Plan §A "what the code tests / why not" for the lines that do not mechanise pre-dispatch.
NOT_MECHANISED_PRE = {
    "PA-D2-check": "highlight geometry needs decoded pixels and scene understanding; 'single "
                   "implied source' is not one light instrument (PA-D4 default allows added "
                   "lights) — counting light words would false-fail accepted packages",
    "PA-D3-check": "needs shadow/specular measurement in pixels; a prompt-vocabulary "
                   "contradiction test false-fails legitimate kicker/rim requests",
    "PA-D5-check": "grayscale check needs decoded pixels and product/ground segmentation; no "
                   "literal pre-dispatch clause exists",
    "PA-D6-check": "'key level declared' has no stable vocabulary in real packages — a strict "
                   "test false-fails; cross-shot consistency needs pixels",
    "PA-D7-check": "the decisive check is a semantic judgment ('needs the body copy'); presence "
                   "of a hierarchy line is not the check — remains a human / blueprint-model "
                   "check",
    "PA-D9-check": "face counting needs object understanding in pixels; candidate comparison "
                   "needs alternatives that do not exist at gate time",
    "CA-D3-check": "accepted packages describe edges in free prose that no closed vocabulary of "
                   "the three treatments matches without false failures; tangency needs pixels",
    "CA-D4-check": "conditional on a frame-within-frame being used, then a tonal/width "
                   "comparison in pixels",
    "CA-D8-check": "edit-room judgment; no detectable trigger for 'imperfect cut'",
    "CA-D9-check": "needs per-shot spatial understanding (pre) or frame analysis (post)",
    "CA-D11-check": "motivation is stated at plan level, not sentence-locally; any "
                    "sentence-local test false-fails",
}

FINISH = textscan.compile_terms(vocab.FINISH_TERMS)
LIGHT = textscan.compile_terms(vocab.LIGHT_TERMS)
DIRECTION = textscan.compile_terms(vocab.DIRECTION_TERMS)
GLOSSY = textscan.compile_terms(vocab.GLOSSY_SURFACE_TERMS)
SPECULAR = textscan.compile_terms(vocab.SPECULAR_DECLARATION_TERMS)
NAMED_RATIO = textscan.compile_terms(vocab.NAMED_RATIO_GRID_TERMS)
PLACEMENT = textscan.compile_terms(vocab.PLACEMENT_TERMS)
BALANCE = textscan.compile_terms(vocab.BALANCE_TERMS)
ASPECT_WORDS = textscan.compile_terms(vocab.ASPECT_WORDS)
DEVIATION_ID = re.compile(vocab.DEVIATION_ID)
DEVIATION_CLAUSE = textscan.compile_terms(vocab.DEVIATION_CLAUSE_WORDS)
READ_ORDER_FAMILIES = (
    ("numbered list", vocab.READ_ORDER_NUMBERED, ("1", "2", "3"), re.M),
    ("1st/2nd/3rd read", vocab.READ_ORDER_ORDINAL, ("1st", "2nd", "3rd"), re.I),
    ("Primary/Secondary/Tertiary", vocab.READ_ORDER_RANK, ("Primary", "Secondary", "Tertiary"), 0),
)
TABLE_SEPARATOR = re.compile(r"^\|[\s\-:|]+\|?$")


@dataclass
class Ctx:
    pkg: package.Package
    prompts: list          # prompt texts
    modality: str
    registry: object


def _found(compiled, text: str) -> list:
    """Distinct matched strings, lowercased, in order of first appearance."""
    hits = []
    for _, rx in compiled:
        for m in rx.finditer(text):
            hits.append((m.start(), m.group(0).lower()))
    return list(dict.fromkeys(t for _, t in sorted(hits)))


def _scope(ctx: Ctx, line) -> package.Scope:
    scope = package.scope_text(ctx.pkg, line.feeds_sections)
    if "GENERATION_PROMPTS" not in scope.sources and ctx.prompts:
        scope.add("GENERATION_PROMPTS", "\n".join(ctx.prompts))
    return scope


def _doctrine(line, status, clause, detail, *, evidence=(), blocking=False):
    return CheckResult(check_id=line.check_id, family="doctrine", gate=GATE, status=status,
                       coverage="partial", clause=clause, source_text=line.text, detail=detail,
                       evidence=tuple(evidence), blocking=blocking)


def _empty_gap(line, clause, scope):
    return _doctrine(line, Status.FAIL, clause,
                     f"typed subfield {', '.join(scope.empty_subfields)} present but empty — "
                     "declaration gap (Ruling 3)")


def _where(scope) -> str:
    return ", ".join(scope.sources) if scope.sources else "no section in scope"


# ── LIMIT-TEXT ───────────────────────────────────────────────────────────────

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


# ── the mechanised partials, in the plan's build order ───────────────────────

def check_ca_d2(ctx: Ctx, line) -> CheckResult:
    """Clause 2 (full, blocking): no named ratio / grid line outside a negation window.
    Clause 1 (partial): a placement term occurs in scope."""
    clause = "Placement is stated as a zone; no placement is justified by a named ratio or grid line"
    scope = _scope(ctx, line)
    for source, body in scope.parts:
        for sentence in package.split_sentences(body):
            for _, rx in NAMED_RATIO:
                for m in rx.finditer(sentence):
                    if not textscan.negated(sentence, m.start()):
                        return _doctrine(
                            line, Status.FAIL, clause,
                            f"placement justified by a named ratio or grid line "
                            f"('{m.group(0)}') in {source}", evidence=(sentence[:200],),
                            blocking=True)
    if scope.empty_subfields:
        return _empty_gap(line, clause, scope)
    terms = _found(PLACEMENT, scope.text)
    if not terms:
        return _doctrine(line, Status.FAIL, clause,
                         f"no placement term in {_where(scope)}; no named ratio or grid line")
    return _doctrine(line, Status.PASS, clause,
                     f"placement term(s) ({', '.join(terms[:4])}) in {_where(scope)}; no named "
                     "ratio or grid line")


def check_pa_d4(ctx: Ctx, line) -> CheckResult:
    clause = "One nameable fictional source"
    scope = _scope(ctx, line)
    if scope.empty_subfields:
        return _empty_gap(line, clause, scope)
    for source, body in scope.parts:
        for sentence in package.split_sentences(body):
            lights = _found(LIGHT, sentence)
            directions = _found(DIRECTION, sentence)
            if lights and directions:
                return _doctrine(line, Status.PASS, clause,
                                 f"light term ({lights[0]}) with direction ({directions[0]}) in "
                                 f"{source}: \"{sentence[:120]}\"", evidence=(sentence[:200],))
    return _doctrine(line, Status.FAIL, clause,
                     f"no sentence in {_where(scope)} names a light source together with a "
                     "direction")


def check_pa_d1(ctx: Ctx, line) -> CheckResult:
    clause = "Every key object has exactly one declared finish"
    scope = _scope(ctx, line)
    if scope.empty_subfields:
        return _empty_gap(line, clause, scope)
    terms = _found(FINISH, scope.text)
    if not terms:
        return _doctrine(line, Status.FAIL, clause, f"no finish term in {_where(scope)}")
    return _doctrine(line, Status.PASS, clause,
                     f"finish term(s) ({', '.join(terms[:6])}) in {_where(scope)}")


def check_ca_d1(ctx: Ctx, line) -> CheckResult:
    clause = "Name the 1st/2nd/3rd read"
    scope = _scope(ctx, line)
    if scope.empty_subfields:
        return _empty_gap(line, clause, scope)
    for source, body in scope.parts:
        for name, pattern, ranks, flags in READ_ORDER_FAMILIES:
            counts = [len(re.findall(pattern.format(n=n), body, flags)) for n in ranks]
            if all(counts):
                items = len(re.findall(pattern.format(n=r"\d+"), body, flags)) if name == \
                    "numbered list" else sum(counts)
                return _doctrine(line, Status.PASS, clause,
                                 f"ordered reads ({name}) in {source} ({items} items)")
    return _doctrine(line, Status.FAIL, clause,
                     f"no ordered enumeration of three reads in {_where(scope)}")


def check_ca_d5(ctx: Ctx, line) -> CheckResult:
    clause = "Declared balanced or deliberately restless"
    scope = _scope(ctx, line)
    terms = _found(BALANCE, scope.text)
    if not terms:
        return _doctrine(line, Status.FAIL, clause,
                         f"no balance/restless declaration in {_where(scope)}")
    return _doctrine(line, Status.PASS, clause,
                     f"declaration term(s) ({', '.join(terms[:4])}) in {_where(scope)}")


def check_pa_d8(ctx: Ctx, line) -> CheckResult:
    clause = "Every specular on glass, dark or glossy surfaces is declared wanted or removed"
    scope = _scope(ctx, line)
    glossy = _found(GLOSSY, scope.text)
    if not glossy:
        return _doctrine(line, Status.NOT_RUN, clause,
                         f"condition not detected: no glass/dark/glossy-surface term in "
                         f"{_where(scope)}")
    for _, rx in SPECULAR:
        m = re.search(r"(?:\S+\s+){0,2}" + rx.pattern, scope.text, re.I)
        if m:
            return _doctrine(line, Status.PASS, clause,
                             f"glossy-surface term(s) ({', '.join(glossy[:4])}) with a specular "
                             f"declaration ('{m.group(0)}') in {_where(scope)}")
    return _doctrine(line, Status.FAIL, clause,
                     f"glossy-surface term(s) ({', '.join(glossy[:4])}) in {_where(scope)} with "
                     "no specular declaration (either polarity)")


def _deviation_entries(section: str) -> tuple:
    """(entries, none_literal): non-blank lines minus table header/separator rows, headings,
    rules and the literal `none`."""
    lines = section.splitlines()
    entries, none_literal = [], False
    for i, raw in enumerate(lines):
        line = raw.strip()
        if not line or line.startswith("#") or re.fullmatch(r"-{3,}|\*{3,}", line):
            continue
        if TABLE_SEPARATOR.match(line):
            continue
        if i + 1 < len(lines) and TABLE_SEPARATOR.match(lines[i + 1].strip()):
            continue  # a table header row
        bare = re.sub(r"[*_`|.\s]", "", line).lower()
        if bare == "none":
            none_literal = True
            continue
        entries.append(line)
    return entries, none_literal


def check_pa_d10(ctx: Ctx, line) -> CheckResult:
    clause = ("Every deviation from PA-D1..PA-D9 is listed in DOCTRINE_DEVIATIONS with its "
              "forcing brief clause")
    section = ctx.pkg.sections.get("DOCTRINE_DEVIATIONS")
    if section is None:
        return _doctrine(line, Status.NOT_RUN, clause,
                         "no DOCTRINE_DEVIATIONS section (schema v1 / receipts retired, "
                         "CANON-SHAPE-v1 §5)")
    entries, none_literal = _deviation_entries(section)
    if not entries:
        if none_literal:
            return _doctrine(line, Status.PASS, clause, "literal `none` — no deviation declared")
        return _doctrine(line, Status.FAIL, clause,
                         "DOCTRINE_DEVIATIONS present but carries neither an entry nor the "
                         "literal `none`")
    bad = []
    for entry in entries:
        has_id = bool(DEVIATION_ID.search(entry))
        has_clause = bool(_found(DEVIATION_CLAUSE, entry)) or bool(textscan._quoted_strings(entry))
        if not (has_id and has_clause):
            bad.append(f"{'no decision id' if not has_id else 'no forcing clause'}: "
                       f"\"{entry[:100]}\"")
    if bad:
        return _doctrine(line, Status.FAIL, clause,
                         f"{len(bad)} of {len(entries)} entries defective — " + "; ".join(bad[:3]),
                         evidence=tuple(bad))
    return _doctrine(line, Status.PASS, clause,
                     f"{len(entries)} entries, each naming a decision id and a forcing clause")


def check_ca_d6(ctx: Ctx, line) -> CheckResult:
    clause = "The stated aspect is justified by a named shape in the scene"
    parts = [(n, ctx.pkg.sections[n]) for n in ("DELIVERABLE", "VISUAL_SYSTEM")
             if n in ctx.pkg.sections]
    if ctx.prompts:
        parts.append(("GENERATION_PROMPTS", "\n".join(ctx.prompts)))
    for source, body in parts:
        m = package.ASPECT_RATIO.search(body)
        if m:
            return _doctrine(line, Status.PASS, clause,
                             f"aspect stated: {int(m.group(1))}:{int(m.group(2))} ({source})")
        words = _found(ASPECT_WORDS, body)
        if words:
            return _doctrine(line, Status.PASS, clause, f"aspect stated: {words[0]} ({source})")
    return _doctrine(line, Status.FAIL, clause,
                     "no aspect stated in DELIVERABLE, VISUAL_SYSTEM or the generation prompts")


def check_ca_d7(ctx: Ctx, line) -> CheckResult:
    clause = "Per cut, name the new information and motivation"
    shots = package.extract_shots(ctx.pkg)
    if len(shots) < 2:
        return _doctrine(line, Status.FAIL, clause,
                         f"{len(shots)} shot entry in PRODUCTION_RECIPE / GENERATION_PROMPTS — "
                         "no per-shot structure to name a cut against")
    return _doctrine(line, Status.PASS, clause,
                     f"{len(shots)} shot entries in {shots[0].section}")


def check_ca_d10(ctx: Ctx, line) -> CheckResult:
    clause = "the stated pace names the prevailing norm it assumes"
    for name in ("PRODUCTION_RECIPE", "AUDIO_AND_EDIT", "GENERATION_PROMPTS"):
        m = package.DURATION_PATTERN.search(ctx.pkg.sections.get(name, ""))
        if m:
            return _doctrine(line, Status.PASS, clause,
                             f"shot durations stated in {name} ('{m.group(0)}')")
    return _doctrine(line, Status.FAIL, clause,
                     "no shot duration stated in PRODUCTION_RECIPE, AUDIO_AND_EDIT or "
                     "GENERATION_PROMPTS")


CHECKS = {
    "CA-D2-check": check_ca_d2, "PA-D4-check": check_pa_d4, "PA-D1-check": check_pa_d1,
    "CA-D1-check": check_ca_d1, "CA-D5-check": check_ca_d5, "PA-D8-check": check_pa_d8,
    "PA-D10-check": check_pa_d10, "CA-D6-check": check_ca_d6, "CA-D7-check": check_ca_d7,
    "CA-D10-check": check_ca_d10,
}
DISPATCH_SOURCE = ("CANON-SHAPE-v1 §4 'brief-fixed parameters honoured'; INJECTION-CONTRACT-v0 "
                   "§3.1 — not a pack check_id")


# ── DISPATCH family (Ruling 1: separately labelled, never counted as doctrine) ────────────

def dispatched_aspect(dispatch: dict):
    if not isinstance(dispatch, dict):
        return None
    params = dispatch.get("parameters") or {}
    image = ((dispatch.get("generationConfig") or {}).get("imageConfig") or {})
    return params.get("aspectRatio") or image.get("aspectRatio")


def _dispatch_row(check_id, status, detail):
    return CheckResult(check_id=check_id, family="dispatch", gate=GATE, status=status,
                       coverage="full", clause="", source_text=DISPATCH_SOURCE, detail=detail,
                       evidence=(), blocking=True)


def check_dispatch_aspect(ctx: Ctx, dispatch) -> CheckResult:
    declared = package.declared_aspect(ctx.pkg)
    if dispatch is None:
        return _dispatch_row("DISPATCH-ASPECT", Status.NOT_RUN, "no dispatch descriptor supplied")
    sent = dispatched_aspect(dispatch)
    if not sent:
        return _dispatch_row("DISPATCH-ASPECT", Status.NOT_RUN, "dispatch carries no aspectRatio")
    if declared is None:
        return _dispatch_row("DISPATCH-ASPECT", Status.NOT_RUN,
                             f"package declares no a:b aspect; dispatch carries {sent}")
    if declared.replace(" ", "") != str(sent).replace(" ", ""):
        return _dispatch_row("DISPATCH-ASPECT", Status.FAIL,
                             f"package declares {declared}, dispatch carries {sent}")
    return _dispatch_row("DISPATCH-ASPECT", Status.PASS,
                         f"package declares {declared} = dispatched {sent}")


def check_dispatch_shot_sum(ctx: Ctx) -> CheckResult:
    shots = [s for s in package.extract_shots(ctx.pkg) if s.duration_s_max is not None]
    declared = package.declared_duration_s(ctx.pkg)
    if not shots:
        return _dispatch_row("DISPATCH-SHOT-SUM", Status.NOT_RUN,
                             "no shot entry carries a duration")
    if declared is None:
        return _dispatch_row("DISPATCH-SHOT-SUM", Status.NOT_RUN,
                             "package declares no total duration")
    total = package.shot_sum_s(shots)
    tol = TOLERANCES["shot_sum_rel"]
    detail = (f"{len(shots)} shot durations sum to {total:g} s (max of ranges) against declared "
              f"{declared:g} s (tolerance ±{int(tol * 100)} %)")
    if abs(total - declared) <= tol * declared:
        return _dispatch_row("DISPATCH-SHOT-SUM", Status.PASS, detail)
    return _dispatch_row("DISPATCH-SHOT-SUM", Status.FAIL, detail)


# ── runner ───────────────────────────────────────────────────────────────────

def not_selected_reason(pack_id: str, modality: str) -> str:
    if pack_id == "product_appearance":
        return f"{pack_id} not selected (trigger table: no product/packshot entity)"
    return f"{pack_id} not selected (trigger table: {modality} selects no pack)"


def run_predispatch(package_text: str, prompts, dispatch, modality: str, product_entity: bool,
                    registry, label: str = "package") -> Report:
    pkg = package.parse_package(package_text)
    sha = hashlib.sha256(package_text.encode("utf-8")).hexdigest()
    packs = registry.select_packs(modality, product_entity)
    if prompts is None:
        prompts = [p.text for p in package.extract_prompts(pkg)]
    ctx = Ctx(pkg=pkg, prompts=list(prompts), modality=modality, registry=registry)
    results = []

    if packs:
        results.append(check_limit_text(ctx.prompts, registry))
    else:
        results.append(CheckResult(
            check_id="LIMIT-TEXT", family="limit", gate=GATE, status=Status.NOT_APPLICABLE,
            coverage="full", clause="", source_text=registry.limit_text,
            detail=f"no pack selected for {modality} (trigger table) — the limit line belongs "
                   "to the selected packs", evidence=(), blocking=True))

    for check_id, line in registry.checks.items():
        if line.pack_id not in packs:
            results.append(_doctrine(line, Status.NOT_APPLICABLE, "",
                                     not_selected_reason(line.pack_id, modality)))
        elif not registry.applicable(check_id, modality):
            results.append(_doctrine(line, Status.NOT_APPLICABLE, "",
                                     registry.applicability_reason(check_id, modality)))
        elif check_id in CHECKS:
            results.append(CHECKS[check_id](ctx, line))
        else:
            results.append(_doctrine(line, Status.NOT_MECHANISED, "",
                                     NOT_MECHANISED_PRE[check_id]))

    if packs:
        results.append(check_dispatch_aspect(ctx, dispatch))
        if modality in ("video", "image_sequence"):
            results.append(check_dispatch_shot_sum(ctx))

    return Report(gate=GATE, inputs={label: sha}, packs_selected=packs, results=results,
                  label=f"package {label} (sha256 {sha[:12]})")
