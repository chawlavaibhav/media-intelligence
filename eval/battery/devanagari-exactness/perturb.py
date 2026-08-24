#!/usr/bin/env python3
"""
The failure taxonomy, as deterministic string operators.

WHAT THESE ARE FOR
    The battery asks a checker: "here is an image, here is a target string — do they match
    exactly?" To measure whether it *silently autocorrects*, we need mismatches that look like
    the mistakes a generator actually makes: a wrong vowel sign, a broken conjunct, a swapped
    letter — plausible enough that a model reading toward the nearest real word will wave them
    through.

    Each operator takes a base string and returns every candidate perturbation of its class,
    with enough metadata to explain later exactly what was changed and where.

WHAT THEY DELIBERATELY DO NOT COVER
    Anything that is not expressible as a different Unicode string — malformed glyph topology,
    fused or broken characters, ambiguous strokes. Those are real generator failures but they
    cannot be produced by rendering a different string, because the renderer always draws
    well-formed glyphs. They belong to the generated-image stress layer and are specified
    separately in GENERATED-GLYPH-STRESS-LAYER.md. Pretending a Unicode substitution covers
    them would overstate what this battery tests.

EVERY candidate is a *candidate only*. It becomes an item solely after
devtext.is_valid_mismatch() confirms the difference is both textual and visible.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

from devtext import (ANUSVARA, CHANDRABINDU, CONSONANTS, DEPENDENT_VOWEL_SIGNS, DEV_END,
                     DEV_START, INDEP_VOWELS, MATRAS, NUKTA, RA, VIRAMA, VISARGA,
                     canonical_equal)

# Visually confusable consonant pairs. Chosen because they differ by a small stroke and a
# reader (human or model) resolving toward the plausible word can slide between them.
# ब/व and य/थ are not theoretical: both are in our own recorded generator failures.
CONFUSABLE_CONSONANTS = [
    ("ब", "व"), ("भ", "म"), ("घ", "ध"), ("ङ", "ड"), ("थ", "य"),
    ("ट", "ठ"), ("प", "ष"), ("ख", "रव"), ("ऋ", "ॠ"), ("द", "ढ"),
]
# Visually confusable matra pairs — differ by one stroke or by stroke count.
CONFUSABLE_MATRAS = [
    ("ि", "ी"), ("ु", "ू"), ("े", "ै"), ("ो", "ौ"), ("ा", "ो"),
]


# Marks that may never begin a Devanagari orthographic cluster. A string starting with one is
# not a plausible misspelling — it is visibly broken, and a checker will reject it trivially.
LEADING_ILLEGAL = (set(MATRAS) | set(DEPENDENT_VOWEL_SIGNS) |
                   {VIRAMA, NUKTA, ANUSVARA, CHANDRABINDU, VISARGA})


def cluster_plausibility(s: str) -> str:
    """
    Is this string a *plausible* alternative spelling, or visibly malformed?

    This matters for what the battery measures. Silent autocorrection happens when the corrupted
    text still looks like it could be a word — that is when a language prior can paper over it.
    A string that opens with a vowel sign, or ends on a bare virama, is obviously broken; a
    checker that rejects it has demonstrated nothing about resisting autocorrection.

    Both kinds are kept, because trivially-detectable mismatches are a useful floor, but they are
    tagged so results can be reported separately and the hard stratum is not diluted.
    """
    if not s:
        return "implausible_cluster"
    if s[0] in LEADING_ILLEGAL:
        return "implausible_cluster"
    if s.endswith(VIRAMA):
        return "implausible_cluster"
    # A vowel sign is fine after a consonant OR after a nukta (ड़ा is ordinary Hindi); it is
    # wrong only at string start, or stacked on another vowel sign, or after a bare virama.
    matra_bad_prev = set(MATRAS) | set(DEPENDENT_VOWEL_SIGNS) | {VIRAMA}
    for i, ch in enumerate(s):
        if ch == VIRAMA:
            # A virama must sit BETWEEN two consonants (a nukta may intervene before it).
            # Checking only the following character missed `इं्लीश` — deleting the
            # first consonant of `इंग्लीश` leaves a virama hanging off an anusvara, which
            # the shaper draws with a dotted circle. Controller review fix.
            prev_ok = i > 0 and (s[i-1] in CONSONANTS or
                                 (s[i-1] == NUKTA and i > 1 and s[i-2] in CONSONANTS))
            if not prev_ok or i + 1 >= len(s) or s[i+1] not in CONSONANTS:
                return "implausible_cluster"
        if ch == NUKTA and (i == 0 or s[i-1] not in CONSONANTS):
            return "implausible_cluster"
        if ch in DEPENDENT_VOWEL_SIGNS and (i == 0 or s[i-1] in matra_bad_prev):
            return "implausible_cluster"
    return "plausible"


@dataclass(frozen=True)
class Candidate:
    text: str            # the perturbed string
    failure_class: str   # taxonomy id
    position: int        # index in the base string where the change was applied
    detail: str          # human-readable description of the edit

    @property
    def plausibility(self) -> str:
        return cluster_plausibility(self.text)


def _is_dev(c: str) -> bool:
    return DEV_START <= ord(c) <= DEV_END


def _pairs_both_ways(pairs):
    for a, b in pairs:
        yield a, b
        yield b, a


# --------------------------------------------------------------------------------------------
# Matra operators
# --------------------------------------------------------------------------------------------
def matra_substitute(s: str) -> list[Candidate]:
    """Replace a vowel sign with a visually similar one — the classic 'wrong matra'."""
    out = []
    for i, ch in enumerate(s):
        for a, b in _pairs_both_ways(CONFUSABLE_MATRAS):
            if ch == a:
                out.append(Candidate(s[:i] + b + s[i+1:], "MATRA_SUBSTITUTE", i,
                                     f"matra {a!r}->{b!r} at {i}"))
    return out


def matra_delete(s: str) -> list[Candidate]:
    """Drop a vowel sign entirely — the word keeps its consonants but changes sound."""
    return [Candidate(s[:i] + s[i+1:], "MATRA_DELETE", i, f"deleted matra {ch!r} at {i}")
            for i, ch in enumerate(s) if ch in MATRAS]


def matra_insert(s: str) -> list[Candidate]:
    """Add a vowel sign after a bare consonant."""
    out = []
    for i, ch in enumerate(s):
        nxt = s[i+1] if i + 1 < len(s) else ""
        if ch in CONSONANTS and nxt not in MATRAS and nxt != VIRAMA:
            for m in ("ा", "ी", "ु"):
                out.append(Candidate(s[:i+1] + m + s[i+1:], "MATRA_INSERT", i,
                                     f"inserted matra {m!r} after {ch!r} at {i}"))
    return out


def matra_reposition(s: str) -> list[Candidate]:
    """Move a vowel sign to a different consonant — same characters, different word."""
    out = []
    idxs = [i for i, c in enumerate(s) if c in MATRAS]
    cons = [i for i, c in enumerate(s) if c in CONSONANTS]
    for i in idxs:
        m = s[i]
        stripped = s[:i] + s[i+1:]
        for j in cons:
            if j in (i - 1, i):
                continue
            k = j if j < i else j - 1
            cand = stripped[:k+1] + m + stripped[k+1:]
            if not canonical_equal(cand, s):
                out.append(Candidate(cand, "MATRA_REPOSITION", i,
                                     f"moved matra {m!r} from {i} to after index {k}"))
    return out


# --------------------------------------------------------------------------------------------
# Consonant / character operators
# --------------------------------------------------------------------------------------------
def consonant_substitute(s: str) -> list[Candidate]:
    """Swap a consonant for a visually confusable one."""
    out = []
    for i, ch in enumerate(s):
        for a, b in _pairs_both_ways(CONFUSABLE_CONSONANTS):
            if ch == a:
                out.append(Candidate(s[:i] + b + s[i+1:], "CONSONANT_SUBSTITUTE", i,
                                     f"consonant {a!r}->{b!r} at {i}"))
    return out


def char_delete(s: str) -> list[Candidate]:
    """Drop a base consonant — a missing letter."""
    return [Candidate(s[:i] + s[i+1:], "CHAR_DELETE", i, f"deleted {ch!r} at {i}")
            for i, ch in enumerate(s) if ch in CONSONANTS]


def char_insert(s: str) -> list[Candidate]:
    """Insert a duplicate of an adjacent consonant — a doubled letter."""
    return [Candidate(s[:i+1] + ch + s[i+1:], "CHAR_INSERT", i, f"duplicated {ch!r} at {i}")
            for i, ch in enumerate(s) if ch in CONSONANTS]


def char_transpose(s: str) -> list[Candidate]:
    """Swap two adjacent characters — order error, same inventory."""
    out = []
    for i in range(len(s) - 1):
        a, b = s[i], s[i+1]
        if not (_is_dev(a) and _is_dev(b)):
            continue
        # Swapping a base with its own combining mark is a different phenomenon (and often
        # produces an invalid cluster the shaper will normalise); MATRA_REPOSITION covers that.
        if b in MATRAS or b == VIRAMA or b in (NUKTA, ANUSVARA, CHANDRABINDU, VISARGA):
            continue
        out.append(Candidate(s[:i] + b + a + s[i+2:], "CHAR_TRANSPOSE", i,
                             f"transposed {a!r} and {b!r} at {i}"))
    return out


# --------------------------------------------------------------------------------------------
# Conjunct / half-form operators
# --------------------------------------------------------------------------------------------
def conjunct_split(s: str) -> list[Candidate]:
    """Remove a virama so a conjunct ligature becomes two separate letters.

    Visually large: क्ष is a single fused glyph, कष is two. This is exactly the
    'conjunct vs half-form' class, and it is the kind of error a generator makes when it fails
    to form a ligature."""
    return [Candidate(s[:i] + s[i+1:], "CONJUNCT_SPLIT", i, f"removed virama at {i}")
            for i, ch in enumerate(s) if ch == VIRAMA]


def conjunct_form(s: str) -> list[Candidate]:
    """Insert a virama between two consonants, fusing them into a conjunct."""
    out = []
    for i in range(len(s) - 1):
        if s[i] in CONSONANTS and s[i+1] in CONSONANTS:
            out.append(Candidate(s[:i+1] + VIRAMA + s[i+1:], "CONJUNCT_FORM", i,
                                 f"inserted virama after {s[i]!r} at {i}"))
    return out


# --------------------------------------------------------------------------------------------
# Diacritic operators
# --------------------------------------------------------------------------------------------
def nukta_add(s: str) -> list[Candidate]:
    """Add a nukta dot beneath a consonant that does not have one."""
    return [Candidate(s[:i+1] + NUKTA + s[i+1:], "NUKTA_ADD", i, f"added nukta after {ch!r} at {i}")
            for i, ch in enumerate(s)
            if ch in CONSONANTS and (i + 1 >= len(s) or s[i+1] != NUKTA)]


def nukta_remove(s: str) -> list[Candidate]:
    return [Candidate(s[:i] + s[i+1:], "NUKTA_REMOVE", i, f"removed nukta at {i}")
            for i, ch in enumerate(s) if ch == NUKTA]


def nasal_substitute(s: str) -> list[Candidate]:
    """Anusvara <-> chandrabindu — a dot versus a dot-with-crescent above the line."""
    out = []
    for i, ch in enumerate(s):
        if ch == ANUSVARA:
            out.append(Candidate(s[:i] + CHANDRABINDU + s[i+1:], "NASAL_SUBSTITUTE", i,
                                 "anusvara->chandrabindu"))
        elif ch == CHANDRABINDU:
            out.append(Candidate(s[:i] + ANUSVARA + s[i+1:], "NASAL_SUBSTITUTE", i,
                                 "chandrabindu->anusvara"))
    return out


def nasal_delete(s: str) -> list[Candidate]:
    return [Candidate(s[:i] + s[i+1:], "NASAL_DELETE", i, f"removed nasal mark {ch!r} at {i}")
            for i, ch in enumerate(s) if ch in (ANUSVARA, CHANDRABINDU)]


def nasal_insert(s: str) -> list[Candidate]:
    out = []
    for i, ch in enumerate(s):
        if ch in CONSONANTS or ch in MATRAS:
            nxt = s[i+1] if i + 1 < len(s) else ""
            if nxt not in (ANUSVARA, CHANDRABINDU) and nxt not in MATRAS and nxt != VIRAMA:
                out.append(Candidate(s[:i+1] + ANUSVARA + s[i+1:], "NASAL_INSERT", i,
                                     f"inserted anusvara after {ch!r} at {i}"))
    return out


def visarga_add(s: str) -> list[Candidate]:
    return [Candidate(s + VISARGA, "VISARGA_ADD", len(s) - 1, "appended visarga")] if s else []


def visarga_remove(s: str) -> list[Candidate]:
    return [Candidate(s[:i] + s[i+1:], "VISARGA_REMOVE", i, f"removed visarga at {i}")
            for i, ch in enumerate(s) if ch == VISARGA]


# --------------------------------------------------------------------------------------------
# Reph / rakar operators — the two positional forms of र
# --------------------------------------------------------------------------------------------
def reph_to_full(s: str) -> list[Candidate]:
    """A reph (र + virama, drawn as a hook above the following letter) becomes a full र."""
    out = []
    for i in range(len(s) - 1):
        if s[i] == RA and s[i+1] == VIRAMA:
            out.append(Candidate(s[:i+1] + s[i+2:], "REPH_TO_FULL_RA", i,
                                 "reph र् -> full र"))
    return out


def rakar_to_full(s: str) -> list[Candidate]:
    """A rakar (virama + र, drawn as a subscript stroke) becomes a full र."""
    out = []
    for i in range(len(s) - 1):
        if s[i] == VIRAMA and s[i+1] == RA:
            out.append(Candidate(s[:i] + s[i+1:], "RAKAR_TO_FULL_RA", i,
                                 "rakar ्र -> full र"))
    return out


def full_ra_to_reph(s: str) -> list[Candidate]:
    """Turn a full र followed by a consonant into a reph."""
    out = []
    for i in range(len(s) - 1):
        if s[i] == RA and s[i+1] in CONSONANTS:
            out.append(Candidate(s[:i+1] + VIRAMA + s[i+1:], "FULL_RA_TO_REPH", i,
                                 "full र -> reph र्"))
    return out


def independent_to_dependent_vowel(s: str) -> list[Candidate]:
    """Swap an independent vowel letter for a different one — a whole-letter vowel error."""
    out = []
    for i, ch in enumerate(s):
        if ch in INDEP_VOWELS:
            for other in INDEP_VOWELS:
                if other != ch:
                    out.append(Candidate(s[:i] + other + s[i+1:], "INDEP_VOWEL_SUBSTITUTE", i,
                                         f"independent vowel {ch!r}->{other!r} at {i}"))
    return out


# --------------------------------------------------------------------------------------------
OPERATORS: dict[str, Callable[[str], list[Candidate]]] = {
    "MATRA_SUBSTITUTE": matra_substitute,
    "MATRA_DELETE": matra_delete,
    "MATRA_INSERT": matra_insert,
    "MATRA_REPOSITION": matra_reposition,
    "CONSONANT_SUBSTITUTE": consonant_substitute,
    "CHAR_DELETE": char_delete,
    "CHAR_INSERT": char_insert,
    "CHAR_TRANSPOSE": char_transpose,
    "CONJUNCT_SPLIT": conjunct_split,
    "CONJUNCT_FORM": conjunct_form,
    "NUKTA_ADD": nukta_add,
    "NUKTA_REMOVE": nukta_remove,
    "NASAL_SUBSTITUTE": nasal_substitute,
    "NASAL_DELETE": nasal_delete,
    "NASAL_INSERT": nasal_insert,
    "VISARGA_ADD": visarga_add,
    "VISARGA_REMOVE": visarga_remove,
    "REPH_TO_FULL_RA": reph_to_full,
    "RAKAR_TO_FULL_RA": rakar_to_full,
    "FULL_RA_TO_REPH": full_ra_to_reph,
    "INDEP_VOWEL_SUBSTITUTE": independent_to_dependent_vowel,
}

# Classes grouped by the aspect of the writing system they stress. Used for reporting so a
# checker that is blind to one whole aspect is visible rather than averaged away.
CLASS_GROUPS = {
    "vowel_signs":  ["MATRA_SUBSTITUTE", "MATRA_DELETE", "MATRA_INSERT", "MATRA_REPOSITION",
                     "INDEP_VOWEL_SUBSTITUTE"],
    "letters":      ["CONSONANT_SUBSTITUTE", "CHAR_DELETE", "CHAR_INSERT", "CHAR_TRANSPOSE"],
    "conjuncts":    ["CONJUNCT_SPLIT", "CONJUNCT_FORM"],
    "dots_marks":   ["NUKTA_ADD", "NUKTA_REMOVE", "NASAL_SUBSTITUTE", "NASAL_DELETE",
                     "NASAL_INSERT", "VISARGA_ADD", "VISARGA_REMOVE"],
    "ra_forms":     ["REPH_TO_FULL_RA", "RAKAR_TO_FULL_RA", "FULL_RA_TO_REPH"],
}
CLASS_TO_GROUP = {c: g for g, cs in CLASS_GROUPS.items() for c in cs}


def all_candidates(s: str, classes: Iterable[str] | None = None) -> list[Candidate]:
    """Every candidate perturbation of `s`, deterministically ordered."""
    names = list(classes) if classes else list(OPERATORS)
    out: list[Candidate] = []
    for name in names:
        out.extend(OPERATORS[name](s))
    # Stable order independent of dict iteration or operator internals.
    out.sort(key=lambda c: (c.failure_class, c.position, c.text))
    return out
