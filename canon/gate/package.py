"""FINAL_PRODUCTION_PACKAGE parser for schema v1 and v2 (CANON-GATE-001 plan §B package.py).

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

v1 (the 18 Sonnet baselines): bare ALL_CAPS headings, 12 sections. v2 (the haiku/gemma runs
and the production shape per Ruling 3): `##` headings, the four typed VISUAL_SYSTEM subfields
(surface_finish_per_key_object, implied_light_source, placement_zone, attention_order),
optionally DOCTRINE_DEVIATIONS (retired in production, CANON-SHAPE-v1 §5). The section
regex is identical to eval/experiments/EVAL-038/tools/strip_blind.py::SECTION_RE so the gate
and the blinding tool cut a package at the same lines.

Prompt extraction (plan §B): double-quoted runs >= 120 chars under GENERATION_PROMPTS, and
`>` blockquote runs with `**` removed — the same rules EVAL-038's EXTRACTION-RECORD.json
records for the four dispatched prompts. A section whose straight quotes admit no single
pairing raises UnbalancedQuotes (Ruling 7, L-01): the gate reports the error rather than
guessing a closer. Shot extraction: table rows `| n |`, `Shot n`
headings, or numbered items in PRODUCTION_RECIPE / GENERATION_PROMPTS. The plan names the
union of the two sections; a literal union double-counts a package that carries both a shot
table and per-block prompt headings (Sonnet B01: 11 + 4), so the shot list is the single
section yielding the most entries, PRODUCTION_RECIPE first on a tie.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from canon.gate import vocab

SECTION_RE = re.compile(r"^(?:#{1,4}\s+)?(?:\*\*)?([A-Z][A-Z_]{3,})(?:\*\*)?:?$")
TYPED_SUBFIELDS = ("surface_finish_per_key_object", "implied_light_source", "placement_zone",
                   "attention_order")
SUBFIELD_RE = re.compile(
    r"^\s*(?:\*\*)?(" + "|".join(TYPED_SUBFIELDS) + r")(?:\*\*)?\s*:?\s*(?:\*\*)?\s*(.*)$")
PROMPT_MIN_CHARS = 120
SHOT_SECTIONS = ("PRODUCTION_RECIPE", "GENERATION_PROMPTS")
SHOT_TABLE_ROW = re.compile(r"^\|\s*(\d+)\s*\|")
SHOT_HEADING = re.compile(r"^#{0,4}\s*(?:\*\*)?Shot\s+(\d+)")
SHOT_NUMBERED = re.compile(r"^\s*(\d+)[.)]\s")
DURATION_PATTERN = re.compile(
    r"(\d+(?:\.\d+)?)(?:\s*[–-]\s*(\d+(?:\.\d+)?))?\s*(?:s\b|sec\b|secs\b|seconds?\b)")
ASPECT_RATIO = re.compile(r"\b(\d{1,2}):(\d{1,2})\b")
DIMENSIONS = re.compile(r"(\d{3,5})\s*[×x*]\s*(\d{3,5})")
MINIMUM_WORDS = re.compile(r"\b(?:minimum|min|at least)\b", re.I)
# `.` and `;` split at whitespace; `!` and `?` split only when the next character is not a
# lowercase letter, so "a visible #REF! error" stays one clause (F-14).
SENTENCE_SPLIT = re.compile(r"[.;]\s+|[!?]\s+(?=[^a-z])|\n")
WORD = re.compile(r"[A-Za-z']+")


@dataclass
class Package:
    sections: dict          # SECTION_NAME -> text (headings removed)
    subfields: dict         # typed VISUAL_SYSTEM subfield -> text ("" when present but empty)
    schema: str             # 'v1' | 'v2'
    text: str = ""


@dataclass(frozen=True)
class Prompt:
    index: int              # 1-based, in package order
    text: str
    origin: str             # 'quoted' | 'blockquote' | 'file'


@dataclass(frozen=True)
class Shot:
    label: str
    duration_s_min: float | None
    duration_s_max: float | None
    text: str
    section: str


@dataclass
class Scope:
    text: str
    sources: list = field(default_factory=list)          # section / subfield names used
    empty_subfields: list = field(default_factory=list)  # typed subfields present but empty
    parts: list = field(default_factory=list)            # (source, text) in scope order

    def add(self, source: str, body: str) -> None:
        if source not in self.sources:
            self.sources.append(source)
            self.parts.append((source, body))
            self.text = "\n".join(t for _, t in self.parts)


def split_sentences(text: str) -> list:
    return [s.strip() for s in SENTENCE_SPLIT.split(text) if s and s.strip()]


# ── sections and subfields ───────────────────────────────────────────────────

def parse_package(text: str) -> Package:
    sections: dict = {}
    current = None
    for line in text.splitlines():
        m = SECTION_RE.match(line.strip())
        if m:
            current = m.group(1)
            sections.setdefault(current, [])
            continue
        if current is not None:
            sections[current].append(line)
    joined = {name: "\n".join(lines).strip("\n") for name, lines in sections.items()}
    subfields = _split_subfields(joined.get("VISUAL_SYSTEM", ""))
    # Schema is decided by the v2 contract's fields, not by heading style: Sonnet B01 (v1)
    # already uses `##` headings, Sonnet B06 bare ones.
    schema = "v2" if subfields or "DOCTRINE_DEVIATIONS" in joined else "v1"
    return Package(sections=joined, subfields=subfields, schema=schema, text=text)


def _split_subfields(visual_system: str) -> dict:
    out: dict = {}
    current = None
    for line in visual_system.splitlines():
        m = SUBFIELD_RE.match(line)
        if m:
            current = m.group(1)
            out[current] = [m.group(2)] if m.group(2).strip() else []
            continue
        if current is not None:
            out[current].append(line)
    return {name: "\n".join(lines).strip() for name, lines in out.items()}


def scope_text(pkg: Package, feeds_sections) -> Scope:
    """Resolve a decision's committed feeds_sections over this package (Ruling 3): a typed
    subfield is read first when present; present-but-empty is recorded as a declaration gap
    and does not fall back; an absent subfield falls back to the parent section's prose."""
    scope = Scope(text="")
    for name in feeds_sections:
        if "." in name:
            section, sub = name.split(".", 1)
            if sub in pkg.subfields:
                if pkg.subfields[sub].strip():
                    scope.add(name, pkg.subfields[sub])
                else:
                    scope.empty_subfields.append(name)
                continue
            if section in pkg.sections:
                scope.add(section, pkg.sections[section])
            continue
        if name in pkg.sections:
            scope.add(name, pkg.sections[name])
    return scope


# ── generation prompts ───────────────────────────────────────────────────────

CLOSER_TAIL = re.compile(r"[ \t]*[.)\],;:!?]*[ \t]*(?:\n|$)")


class UnbalancedQuotes(ValueError):
    """The straight quotes of a GENERATION_PROMPTS section admit no single pairing (Ruling 7,
    L-01): a run never closes, or a quote after an undecided inch mark could equally open a
    new run or close the current one. The gate never guesses a closer."""


def _excerpt(text: str, i: int) -> str:
    return " ".join(text[i:i + 28].split())


def _straight_runs(text: str) -> list:
    """(start, body) between paired straight quotes; raises UnbalancedQuotes when the text
    admits no single pairing. A quote opens a run when nothing alphanumeric (and no quote)
    precedes it; it closes the open run when nothing alphanumeric follows it. Whitespace just
    inside either quote is accepted (K-02). Outside a run a digit-preceded quote can never
    open one, so `the 5" screen` between prompts is skipped instead of shifting every later
    pair (F-12).

    Inside a run a quote immediately preceded by a digit is an inch mark — `6" OLED panel`,
    `is 6". It shows` (K-05) — unless a bracket or separator follows it or the rest of its
    line is blank/punctuation, where it definitely closes (`… past 99"` at end of line,
    `"Aspect ratio: 9:16")`). A digit-preceded quote followed by prose on the same line
    (`₹9" (massive …)`, `99" then …`) is undecidable: the inch mark and the closer look the
    same. The safer default is to leave the run open and mark it in doubt, not to close it:
    closing would cut every K-05 prompt at its inch mark and hand the remainder — the
    text-bearing half — to a run opened by the prompt's own closing quote, which then never
    closes; leaving it open keeps the prompt whole when a definite closer follows and
    otherwise reaches an error, never a silent drop. While in doubt only a definite closer,
    or a quote that could not open a run (alphanumeric before it), may close the run. A
    quote that could open a new run — `"VIDEO`, `"` before the next prompt — means two
    pairings exist (the inch mark was the closer and this opens; or it was not and this is
    nested), so the gate raises instead of choosing. A run still open at the end of the text
    raises too (Ruling 7 condition 1). A wrong guess either drops a prompt or manufactures
    one from unrelated prose, and LIMIT-TEXT then reports PASS over text it never scanned
    (L-01, the committed Gemma B02-R1 package)."""
    runs = []
    open_at = None
    doubt = None    # offset of the digit-preceded quote that left the open run undecided
    for m in re.finditer(r'"', text):
        i = m.start()
        prev = text[i - 1] if i else ""
        nxt = text[i + 1] if i + 1 < len(text) else ""
        could_open = not (prev.isalnum() or prev == '"')
        if open_at is None:
            if could_open:
                open_at, doubt = i, None
            continue
        if nxt.isalnum() and not could_open:
            continue   # inside a word (5"x7) or a doubled quote: neither opens nor closes
        definite = nxt in ")],;:" or CLOSER_TAIL.match(text, i + 1) is not None
        if prev.isdigit() and not definite:
            doubt = i   # inch mark or closer — undecided; the run stays open
            continue
        if nxt.isalnum():
            if doubt is not None:
                raise UnbalancedQuotes(
                    f"the quote at offset {i} ({_excerpt(text, i)!r}) could open a new run or "
                    f"close the one opened at offset {open_at} — the digit-preceded quote at "
                    f"offset {doubt} ({_excerpt(text, doubt)!r}) is an inch mark under one "
                    f"pairing and a closer under the other")
            continue   # a nested opener; the run continues
        if doubt is not None and could_open and not definite:
            raise UnbalancedQuotes(
                f"the quote at offset {i} ({_excerpt(text, i)!r}) could open a new run or "
                f"close the one opened at offset {open_at} — the digit-preceded quote at "
                f"offset {doubt} ({_excerpt(text, doubt)!r}) is an inch mark under one "
                f"pairing and a closer under the other")
        runs.append((open_at, text[open_at + 1:i]))
        open_at, doubt = None, None
    if open_at is not None:
        raise UnbalancedQuotes(
            f"the run opened at offset {open_at} ({_excerpt(text, open_at)!r}) never closes")
    return runs


def _quoted_runs(text: str) -> list:
    """(start, body) for every quoted run >= PROMPT_MIN_CHARS. Straight quotes pair by
    `_straight_runs`; curly quotes pair each “ with the next ”."""
    runs = [(start, body) for start, body in _straight_runs(text)
            if len(body) >= PROMPT_MIN_CHARS]
    for m in re.finditer(r"“([^“”]*)”", text, re.S):
        if len(m.group(1)) >= PROMPT_MIN_CHARS:
            runs.append((m.start(), m.group(1)))
    return runs


def _blockquote_runs(text: str) -> list:
    runs = []
    pos = 0
    block: list = []
    start = None
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith(">"):
            if start is None:
                start = pos
            block.append(re.sub(r"^\s*>\s?", "", line.rstrip("\n")).replace("**", ""))
        elif block:
            runs.append((start, "\n".join(block).strip()))
            block, start = [], None
        pos += len(line)
    if block:
        runs.append((start, "\n".join(block).strip()))
    return [(s, b) for s, b in runs if b]


def extract_prompts(pkg: Package) -> list:
    """Prompts in package order; raises UnbalancedQuotes when the section's straight quotes
    admit no single pairing (Ruling 7) — callers report the error, never a partial list."""
    section = pkg.sections.get("GENERATION_PROMPTS")
    if section is None:
        return []
    try:
        found = [(s, b, "quoted") for s, b in _quoted_runs(section)]
    except UnbalancedQuotes as exc:
        raise UnbalancedQuotes(f"unbalanced quotes in GENERATION_PROMPTS — {exc}") from None
    found += [(s, b, "blockquote") for s, b in _blockquote_runs(section)]
    found.sort(key=lambda t: t[0])
    return [Prompt(index=i + 1, text=b.strip(), origin=o) for i, (_, b, o) in enumerate(found)]


# ── shots, durations, declarations ───────────────────────────────────────────

def parse_duration(text: str):
    m = DURATION_PATTERN.search(text)
    if not m:
        return None
    lo = float(m.group(1))
    hi = float(m.group(2)) if m.group(2) else lo
    return (min(lo, hi), max(lo, hi))


def _shots_in(section_name: str, body: str) -> list:
    entries = []  # (label, [lines])
    for line in body.splitlines():
        m = SHOT_TABLE_ROW.match(line) or SHOT_HEADING.match(line) or SHOT_NUMBERED.match(line)
        if m:
            entries.append((m.group(1), [line]))
        elif entries:
            entries[-1][1].append(line)
    shots = []
    for label, lines in entries:
        d = parse_duration(lines[0])
        shots.append(Shot(label=label, duration_s_min=d[0] if d else None,
                          duration_s_max=d[1] if d else None,
                          text="\n".join(lines).strip(), section=section_name))
    return shots


def extract_shots(pkg: Package) -> list:
    best: list = []
    for name in SHOT_SECTIONS:
        if name in pkg.sections:
            shots = _shots_in(name, pkg.sections[name])
            if len(shots) > len(best):
                best = shots
    return best


def shot_sum_s(shots) -> float:
    return float(sum(s.duration_s_max for s in shots if s.duration_s_max is not None))


def find_aspect(text: str):
    """The first `a:b` in `text` that reads as an aspect, normalised ("4:5"), else None. A
    pair with an ASPECT_CONTEXT word within three tokens on either side is an aspect; failing
    that, a pair with a zero numerator, a leading-zero denominator, a TIME_CONTEXT word within
    three tokens before it or a time suffix within two after it is a clock time and is
    skipped (F-04: "Hands set to 10:10 as convention.", "the last 0:03")."""
    for m in ASPECT_RATIO.finditer(text):
        a, b = m.group(1), m.group(2)
        # context windows stop at a sentence boundary so "… 10:10 as convention. 4:5 aspect"
        # does not lend the next sentence's "aspect" to the clock time
        head = re.split(r"[.;!?\n]", text[max(0, m.start() - 60):m.start()])[-1]
        tail = re.split(r"[.;!?\n]", text[m.end():m.end() + 40])[0]
        before = [t.lower() for t in WORD.findall(head)][-3:]
        after = [t.lower() for t in WORD.findall(tail)][:3]
        if any(t in vocab.ASPECT_CONTEXT_WORDS for t in before + after):
            return f"{int(a)}:{int(b)}"
        if a == "0" or (len(b) == 2 and b[0] == "0"):
            continue
        if any(t in vocab.TIME_CONTEXT_BEFORE for t in before) \
                or any(t in vocab.TIME_CONTEXT_AFTER for t in after[:2]):
            continue
        return f"{int(a)}:{int(b)}"
    return None


def declared_aspect(pkg: Package):
    for name in ("DELIVERABLE", "VISUAL_SYSTEM"):
        found = find_aspect(pkg.sections.get(name, ""))
        if found:
            return found
    try:
        prompts = extract_prompts(pkg)
    except UnbalancedQuotes:
        return None   # the prompts are unreadable; LIMIT-TEXT reports the error
    for p in prompts:
        found = find_aspect(p.text)
        if found:
            return found
    return None


def declared_duration_s(pkg: Package):
    for name in ("DELIVERABLE", "PRODUCTION_RECIPE", "AUDIO_AND_EDIT"):
        d = parse_duration(pkg.sections.get(name, ""))
        if d:
            return d[1]
    return None


def declared_min_dimensions(pkg: Package):
    for name in ("DELIVERABLE", "VISUAL_SYSTEM", "PRODUCTION_RECIPE", "GENERATION_PROMPTS"):
        for sentence in split_sentences(pkg.sections.get(name, "")):
            m = DIMENSIONS.search(sentence)
            if m and MINIMUM_WORDS.search(sentence):
                return (int(m.group(1)), int(m.group(2)))
    return None
