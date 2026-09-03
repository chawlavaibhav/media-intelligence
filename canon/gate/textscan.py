"""Baked-text scan: prompt guard, detector protocol, offline detectors, and the wired-but-
refusing Cloud Vision adapter (CANON-GATE-001 plan §D and §B textscan.py).

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

Source of the check: the verbatim pack limit line ("… never generate Devanagari glyphs;
composite text deterministically"), rendered by the registry — Ruling 1. The gate inspects
draws, never final composites.

Pre-dispatch (over each generation prompt, sentence-split on `[.;!?]\\s+|\\n`):
  T1 Devanagari codepoints (U+0900–U+097F, U+A8E0–U+A8FF) — full;
  T2 requested rendered text — a quoted string (>= 2 word characters) with a TEXT_VERB, or a
     TEXT_REQUEST term — unless a NEGATOR sits within 4 tokens before the term or the
     sentence carries a DEFERRAL term;
  T3 a TEXT_SURFACE term with no ILLEGIBILITY/DEFERRAL term in the same sentence.

Post-draw: a TextDetector over the artifact (or supplied video frames). `NoDetector` is the
default and yields `unavailable` (NOT_RUN). `CloudVisionTextDetection` mirrors the request and
response handling of eval/empirical-tranche-1/ocr_providers.py (cited, not imported) and its
default transport raises SpendNotAuthorised before any socket: USD 0, zero provider calls;
invoking it is a separate Controller spend authorisation, not a flag.
"""
from __future__ import annotations

import base64
import hashlib
import re
from dataclasses import dataclass, field
from typing import Protocol

from canon.gate import vocab
from canon.gate.package import split_sentences

DEVANAGARI = re.compile(r"[ऀ-ॿ꣠-ꣿ]+")
QUOTED = re.compile(r"(?<!\w)([\"'“‘])(.+?)([\"'”’])(?!\w)")
TOKEN = re.compile(r"[A-Za-z']+")
NEGATION_WINDOW = 4


def compile_terms(terms) -> list:
    """(label, regex) per term: case-insensitive, bounded by non-word characters."""
    return [(t, re.compile(r"(?<!\w)(?:" + t + r")(?!\w)", re.I)) for t in terms]


TEXT_VERBS = compile_terms(vocab.TEXT_VERBS)
TEXT_REQUEST_TERMS = compile_terms(vocab.TEXT_REQUEST_TERMS)
DEFERRAL_TERMS = compile_terms(vocab.DEFERRAL_TERMS)
TEXT_SURFACE_TERMS = compile_terms(vocab.TEXT_SURFACE_TERMS)
ILLEGIBILITY_TERMS = compile_terms(vocab.ILLEGIBILITY_TERMS)
NO_TEXT_CLAUSE = re.compile(vocab.NO_TEXT_CLAUSE, re.I)


@dataclass(frozen=True)
class TextHit:
    subcheck: str          # T1 | T2 | T3
    sentence_index: int    # 1-based within the prompt
    sentence: str
    terms: tuple           # the matched strings, lowercased


@dataclass
class PromptScan:
    sentences: list
    hits: list = field(default_factory=list)
    no_text_clause: bool = False


def devanagari_spans(text: str) -> list:
    return DEVANAGARI.findall(text)


def negated(sentence: str, start: int) -> bool:
    """A NEGATOR within NEGATION_WINDOW tokens before position `start`."""
    tokens = [t.lower().strip("'") for t in TOKEN.findall(sentence[:start])][-NEGATION_WINDOW:]
    if any(t in vocab.NEGATORS for t in tokens):
        return True
    joined = " ".join(tokens)
    return any(p in joined for p in vocab.NEGATOR_PHRASES)


def _matches(compiled, sentence: str, *, skip_negated: bool) -> list:
    found = []
    for _, rx in compiled:
        for m in rx.finditer(sentence):
            if skip_negated and negated(sentence, m.start()):
                continue
            found.append(m.group(0).lower())
    return found


def _quoted_strings(sentence: str) -> list:
    return [m.group(2) for m in QUOTED.finditer(sentence)
            if len(re.findall(r"\w", m.group(2))) >= 2]


def scan_prompt(text: str) -> PromptScan:
    sentences = split_sentences(text)
    scan = PromptScan(sentences=sentences, no_text_clause=bool(NO_TEXT_CLAUSE.search(text)))
    for i, sentence in enumerate(sentences, 1):
        spans = devanagari_spans(sentence)
        if spans:
            scan.hits.append(TextHit("T1", i, sentence, tuple(spans)))
        deferred = bool(_matches(DEFERRAL_TERMS, sentence, skip_negated=False))
        if not deferred:
            terms = []
            quoted = _quoted_strings(sentence)
            if quoted:
                verbs = _matches(TEXT_VERBS, sentence, skip_negated=True)
                if verbs:
                    terms += verbs + [f"'{q}'" for q in quoted]
            terms += _matches(TEXT_REQUEST_TERMS, sentence, skip_negated=True)
            if terms:
                scan.hits.append(TextHit("T2", i, sentence, tuple(dict.fromkeys(terms))))
        surfaces = _matches(TEXT_SURFACE_TERMS, sentence, skip_negated=False)
        if surfaces and not _matches(ILLEGIBILITY_TERMS, sentence, skip_negated=False):
            scan.hits.append(TextHit("T3", i, sentence, tuple(dict.fromkeys(surfaces))))
    return scan


# ── detectors ────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class TextDetection:
    status: str            # text | no_text | unavailable
    transcript: str
    detector_id: str
    raw: dict


class TextDetector(Protocol):
    detector_id: str

    def detect(self, image_bytes: bytes) -> TextDetection: ...


class NoDetector:
    """Always `unavailable`: the post-draw text scan reports NOT_RUN, never PASS."""
    detector_id = "none"

    def detect(self, image_bytes: bytes) -> TextDetection:
        return TextDetection("unavailable", "", self.detector_id,
                             {"note": "no text detector configured"})


class ScriptedDetector:
    """Human-observed truth keyed by artifact sha256 — proves plumbing, measures nothing."""
    detector_id = "scripted"

    def __init__(self, results: dict):
        self.results = dict(results)

    @classmethod
    def from_json(cls, doc: dict) -> "ScriptedDetector":
        return cls({digest: TextDetection(str(v.get("status")), str(v.get("transcript") or ""),
                                          cls.detector_id, dict(v))
                    for digest, v in doc.items()})

    def detect(self, image_bytes: bytes) -> TextDetection:
        digest = hashlib.sha256(image_bytes).hexdigest()
        if digest in self.results:
            return self.results[digest]
        return TextDetection("unavailable", "", self.detector_id,
                             {"note": f"no scripted result for sha256 {digest[:12]}"})


class SpendNotAuthorised(Exception):
    """Raised before any network activity: CANON-GATE-001 authorises zero provider calls."""


class RefusingTransport:
    """The default Cloud Vision transport. `calls` counts dispatches past the refusal — always 0."""

    def __init__(self):
        self.calls = 0

    def __call__(self, request: dict) -> dict:
        raise SpendNotAuthorised(
            "CANON-GATE-001 authorises zero provider calls; invoking Cloud Vision TEXT_DETECTION "
            "needs a separate spend authorisation")


CLOUD_VISION_ENDPOINT = "https://vision.googleapis.com/v1/images:annotate"  # cited; never dialled


class CloudVisionTextDetection:
    """Wired, never invoked. Request shape identical to EMP-001's ocr_providers.py
    (`TEXT_DETECTION`, no `languageHints`, `maxResults: 1`); response parsing over the
    documented shapes only — anything undocumented is `unavailable` (fails closed)."""
    detector_id = "cloud-vision-text-detection-v1"
    feature = "TEXT_DETECTION"

    def __init__(self, transport=None):
        self.transport = transport if transport is not None else RefusingTransport()

    def build_request(self, image_bytes: bytes) -> dict:
        return {
            "requests": [{
                "image": {"content": base64.b64encode(image_bytes).decode("ascii")},
                "features": [{"type": self.feature, "maxResults": 1}],
            }]
        }

    def parse(self, raw: dict) -> TextDetection:
        def unavailable(note):
            return TextDetection("unavailable", "", self.detector_id, {"note": note, "raw": raw})

        if not isinstance(raw, dict):
            return unavailable("reply is not an object")
        if raw.get("error"):
            return unavailable(f"top-level error: {str(raw['error'])[:200]}")
        responses = raw.get("responses")
        if not isinstance(responses, list) or not responses:
            return unavailable("no `responses` array")
        r0 = responses[0]
        if not isinstance(r0, dict):
            return unavailable("`responses[0]` is not an object")
        if r0.get("error"):
            return unavailable(f"per-response error: {str(r0['error'])[:200]}")
        if "textAnnotations" in r0:
            anns = r0.get("textAnnotations") or []
            text = str((anns[0] if anns else {}).get("description") or "")
        elif "fullTextAnnotation" in r0:
            text = str((r0.get("fullTextAnnotation") or {}).get("text") or "")
        elif not r0:
            # Cloud Vision answers an image with no detectable text with an empty response
            # object; recorded as no_text with the shape named, not as a detector measurement.
            text = ""
        else:
            return unavailable("undocumented response shape (no textAnnotations / "
                               "fullTextAnnotation / error)")
        if text.strip():
            return TextDetection("text", text, self.detector_id, {"raw": raw})
        return TextDetection("no_text", "", self.detector_id, {"raw": raw})

    def detect(self, image_bytes: bytes) -> TextDetection:
        return self.parse(self.transport(self.build_request(image_bytes)))
