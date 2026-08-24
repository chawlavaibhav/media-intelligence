#!/usr/bin/env python3
"""
Devanagari shaping + rendering primitives for the exactness battery.

WHY THIS EXISTS
    The battery needs ground truth that does not depend on anyone's annotation of a photograph.
    We get it by *constructing* the image: render a known string with a known font, and the image
    provably contains that string. No reader, no dataset label, no ambiguity about what is on the
    page.

ONE FONT ASSET, USED FOR BOTH SHAPING AND RENDERING  (Controller review fix 2)
    An earlier version of this module shaped with `hb-shape --font-file=<exact file>` but
    rasterised with `pango-view --font="<family name>"`. Those are two different lookups. The
    validity screen could therefore approve a difference measured in one font while the committed
    PNG was drawn through whatever face fontconfig happened to resolve. Measured on this machine
    before the fix:

        render() with a VALID   font_file  -> faffe232d6430ce4...
        render() with a BOGUS   font_file  -> faffe232d6430ce4...   (identical: the file was ignored)
        pango-view with a family name that does not exist -> rendered anyway, no error

    Both tools now take the SAME font FILE and the SAME face index:

        hb-shape  --font-file=<file> --face-index=<n>     -> glyph sequence (diagnostic)
        hb-view   <file>            --face-index=<n>      -> PNG            (authoritative pixels)

    `hb-view` is HarfBuzz's own rasteriser, so the shaping behind the pixels is the shaping we
    measured. It accepts a font file, never a family, so fontconfig fallback cannot occur. A
    missing font file raises `FontMissing` — the run stops loudly instead of drawing through
    another face.

THE TRAP THIS MODULE EXISTS TO PREVENT
    Two different Unicode strings can render to *identical pixels*. Measured on this machine:

        क़  (U+0958, precomposed)      -> [uni0915093C=0+770]
        क + nukta (U+0915 U+093C)      -> [uni0915093C=0+770]

    If we built a "mismatch" item from that pair, we would be asking a checker to report a
    difference that is not visible, and scoring it wrong for looking at the picture correctly.

    Every mismatch item must therefore satisfy BOTH:
      1. the NFC-canonical strings differ  (it is a real textual difference), and
      2. the FINAL RASTER OUTPUT differs   (the difference is actually drawn)

    Condition 2 is checked on the actual PNG bytes, not on the glyph sequence. Differing glyph
    sequences are useful evidence but are not logically the same claim as differing pixels; the
    glyph comparison is retained as a *diagnostic* only.  (Controller review fix 3)

EXTERNAL TOOLS (all local, no network, no model, no spend)
    hb-shape     HarfBuzz shaping -> glyph sequence.  Diagnostic.
    hb-view      HarfBuzz rasteriser -> deterministic PNG.  Authoritative.
"""
from __future__ import annotations

import atexit
import functools
import hashlib
import shutil
import subprocess
import tempfile
import unicodedata
from dataclasses import dataclass
from pathlib import Path

# --- Devanagari block constants used across the battery -------------------------------------
DEV_START, DEV_END = 0x0900, 0x097F
VIRAMA       = "्"   # halant — forms conjuncts / half forms
NUKTA        = "़"
ANUSVARA     = "ं"
CHANDRABINDU = "ँ"
VISARGA      = "ः"
ZWJ, ZWNJ    = "‍", "‌"
RA           = "र"
DANDA        = "।"

# Dependent vowel signs (matras). Order matters only for readability.
MATRAS = ["ा", "ि", "ी", "ु", "ू", "ृ",
          "े", "ै", "ो", "ौ"]
# Independent vowels
INDEP_VOWELS = ["अ", "आ", "इ", "ई", "उ", "ऊ",
                "ए", "ऐ", "ओ", "औ"]
# Consonants (base set, excluding precomposed-nukta forms U+0958..U+095F)
CONSONANTS = [chr(c) for c in range(0x0915, 0x093A)]

# EVERY dependent vowel sign in the block, including the ones MATRAS omits (ॅ ॉ ॆ ॊ ॄ and the
# rare U+094E/U+094F, U+0955..U+0957). MATRAS drives the perturbation operators and stays limited
# to the common Hindi set; this wider set is what "may this character begin a cluster" must be
# checked against. `बॉम्बे` uses U+0949, which MATRAS does not contain — so a rule built only on
# MATRAS called the broken string `ॉम्बे` plausible.
# U+093C NUKTA and U+093D AVAGRAHA sit inside the same numeric run but are NOT vowel signs, and
# excluding them matters: `तोड़ा` is an ordinary Hindi word whose `ा` follows a nukta.
DEPENDENT_VOWEL_SIGNS = ([chr(c) for c in range(0x093A, 0x094D)
                          if c not in (0x093C, 0x093D)] +
                         [chr(c) for c in range(0x094E, 0x0950)] +
                         [chr(c) for c in range(0x0955, 0x0958)])

# Default rendering font. An explicit FILE and an explicit FACE INDEX, never a family name, so
# the run cannot silently change because fontconfig resolved a different face. The file is a
# system font and is deliberately NOT committed to the repository; provenance is recorded
# instead (see `environment_provenance`).
DEFAULT_FONT_FILE = "/System/Library/Fonts/Kohinoor.ttc"
DEFAULT_FACE_INDEX = 0


class ToolMissing(RuntimeError):
    """Raised when a required local tool is unavailable, so callers fail loudly."""


class FontMissing(RuntimeError):
    """Raised when the pinned font file is absent.

    This is deliberately fatal. Silently substituting another face would invalidate every
    visibility decision the battery has made, and would do so invisibly.
    """


def require_tools(*names: str) -> None:
    missing = [n for n in names if shutil.which(n) is None]
    if missing:
        raise ToolMissing(
            f"required local tool(s) not found: {', '.join(missing)}. "
            f"This battery renders text locally; it makes no network or model calls."
        )


def require_font(font_file: str) -> Path:
    p = Path(font_file)
    if not p.exists():
        raise FontMissing(
            f"pinned font file not found: {font_file}. "
            f"This battery pins one font FILE for both shaping and rendering; there is no "
            f"fallback face, by design. Supply the same font asset (sha256 recorded in the "
            f"build summary) or rebuild the battery and record the new provenance."
        )
    return p


# --------------------------------------------------------------------------------------------
# Text canonicalisation — three separate, separately-named rules  (Controller review fix 4)
# --------------------------------------------------------------------------------------------
# An earlier version had a function called `nfc()` that also called `.strip()`. The contract said
# "NFC and nothing else", which was not what the code did. Whitespace handling is a real decision
# and it now lives in its own named rule, with its own rationale and its own tests, rather than
# hiding inside a function named after a Unicode normalisation form.

def nfc(s: str) -> str:
    """Unicode NFC normalisation. **Nothing else.** No stripping, no case folding, no filtering.

    NFC matters here beyond tidiness: it maps the precomposed nukta letters (U+0958..U+095F) onto
    their decomposed equivalents, which is also what the renderer draws. Comparing in NFC
    therefore agrees with the pixels instead of disagreeing with them.
    """
    return unicodedata.normalize("NFC", s)


def strip_outer_whitespace(s: str) -> str:
    """Remove leading/trailing whitespace. A **transport** rule, not a comparison rule.

    Applied in exactly two places, both of them boundaries where whitespace is an artefact of the
    carrier rather than part of the string:

      * INGEST — base words read out of tab-separated annotation files, where a trailing tab or
        newline belongs to the file format, not to the word.
      * RESPONSE PARSING — a checker's raw reply, where a leading newline or a trailing space
        belongs to the chat transport, not to what the model claims it saw.

    It is deliberately NOT part of the comparison predicate. **Internal** whitespace is never
    touched: `"सुबह की"` and `"सुबहकी"` are different strings and must compare unequal.
    """
    return s.strip()


def canonical_equal(a: str, b: str) -> bool:
    """The battery's comparison predicate: **NFC equality, nothing looser.**

    This is *canonical* exactness, not raw-codepoint identity. Two encodings of the same nukta
    letter are canonically equal and render to the same pixels, so calling them different would
    penalise a checker for correctly reporting what it saw. Everything beyond that — a dropped
    vowel sign, a swapped letter, a missing dot — compares unequal.
    """
    return nfc(a) == nfc(b)


def has_devanagari(s: str) -> bool:
    return any(DEV_START <= ord(c) <= DEV_END for c in s)


# --------------------------------------------------------------------------------------------
# Render specification
# --------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class RenderSpec:
    """Everything that affects the pixels. Recorded per item so a run is reproducible.

    `font_file` + `face_index` are used by BOTH `shape()` and `render()`. There is no separate
    family-name field any more: having one was the defect this dataclass now prevents.
    """
    font_file: str = DEFAULT_FONT_FILE
    face_index: int = DEFAULT_FACE_INDEX
    point_size: int = 40
    margin: int = 24
    background: str = "FFFFFF"   # hb-view colour syntax: rrggbb
    foreground: str = "000000"

    def as_dict(self) -> dict:
        return {
            "font_file": self.font_file, "face_index": self.face_index,
            "point_size": self.point_size, "margin": self.margin,
            "background": self.background, "foreground": self.foreground,
        }


def _tool_version(name: str) -> str:
    try:
        r = subprocess.run([name, "--version"], capture_output=True, text=True)
        return (r.stdout or r.stderr).strip().splitlines()[0]
    except Exception:                                    # pragma: no cover - environment probe
        return "unavailable"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def environment_provenance(spec: RenderSpec) -> dict:
    """Everything needed to judge whether a future run is the same experiment.

    The font itself is a proprietary system asset and is **not** committed. Its SHA-256 is, so a
    future run can prove it used the same bytes — or discover that it did not.
    """
    font = require_font(spec.font_file)
    return {
        "font_file": str(font),
        "font_sha256": sha256_file(font),
        "font_bytes": font.stat().st_size,
        "face_index": spec.face_index,
        "font_committed_to_repo": False,
        "font_note": "proprietary system font; not redistributed. Identity is pinned by sha256.",
        "shaper": _tool_version("hb-shape"),
        "renderer": _tool_version("hb-view"),
        "renderer_identity": "hb-view (HarfBuzz own rasteriser); takes a font FILE, never a "
                             "family name, so fontconfig fallback cannot occur",
        "same_asset_for_shaping_and_rendering": True,
        "point_size": spec.point_size,
        "margin": spec.margin,
        "background": spec.background,
        "foreground": spec.foreground,
    }


# --------------------------------------------------------------------------------------------
# Shaping — diagnostic
# --------------------------------------------------------------------------------------------
def _unicodes_arg(text: str) -> str:
    """Pass text as explicit codepoints, so no shell/locale encoding step can alter it."""
    return ",".join(f"U+{ord(c):04X}" for c in text)


@functools.lru_cache(maxsize=8192)
def _shape_cached(text: str, font_file: str, face_index: int) -> str:
    require_tools("hb-shape")
    require_font(font_file)
    if not text:
        return ""
    r = subprocess.run(
        ["hb-shape", f"--font-file={font_file}", f"--face-index={face_index}",
         f"--unicodes={_unicodes_arg(text)}"],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        raise RuntimeError(f"hb-shape failed for {text!r}: {r.stderr.strip()[:200]}")
    return r.stdout.strip()


def shape(text: str, spec: RenderSpec = RenderSpec()) -> str:
    """HarfBuzz's shaped glyph sequence for `text`, as a stable string.

    **Diagnostic only.** A different glyph sequence is strong evidence that two strings look
    different, but it is not the same claim as "the final PNGs differ" — which is what the
    battery actually asserts. `raster_sha256` settles that question.
    """
    return _shape_cached(text, spec.font_file, spec.face_index)


def glyphs_differ(a: str, b: str, spec: RenderSpec = RenderSpec()) -> bool:
    """True when the two strings shape to different glyph sequences. Diagnostic."""
    return shape(a, spec) != shape(b, spec)


# U+25CC DOTTED CIRCLE is the glyph a shaper substitutes when a combining mark has nothing legal
# to attach to. It is the writing system's own "this cluster is invalid" marker, and it is
# unmistakable on the page.
DOTTED_CIRCLE_GLYPH = "uni25CC"


def shapes_with_dotted_circle(text: str, spec: RenderSpec = RenderSpec()) -> bool:
    """True when shaping `text` produces a dotted circle — i.e. the string is visibly malformed.

    This matters for what the battery measures. Silent autocorrection happens when corrupted text
    still looks like it could be a word. A string the shaper marks with a dotted circle does not:
    any checker will reject it on sight, so counting it as an autocorrection opportunity would
    inflate the hard stratum with items that test nothing.

    It is also a far better test than a hand-written cluster grammar, because it asks the shaper
    what it actually drew rather than asking us what we think is legal. Deleting the first
    consonant of `इंग्लीश` leaves `इं्लीश`, whose virama has no consonant to sit on; the string
    rule missed it and the shaper did not.
    """
    return DOTTED_CIRCLE_GLYPH in shape(text, spec)


# --------------------------------------------------------------------------------------------
# Rendering — authoritative
# --------------------------------------------------------------------------------------------
def render(text: str, out_path: Path, spec: RenderSpec = RenderSpec()) -> Path:
    """Rasterise `text` to a PNG with the pinned font file.

    Deterministic: identical inputs give byte-identical output. No family-name lookup, so no
    silent fallback; a missing font file raises `FontMissing`.
    """
    require_tools("hb-view")
    require_font(spec.font_file)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(
        ["hb-view", spec.font_file,
         f"--face-index={spec.face_index}",
         f"--unicodes={_unicodes_arg(text)}",
         f"--font-size={spec.point_size}",
         f"--margin={spec.margin}",
         f"--background={spec.background}",
         f"--foreground={spec.foreground}",
         "-O", "png", "-o", str(out_path)],
        capture_output=True, text=True,
    )
    if r.returncode != 0 or not out_path.exists():
        raise RuntimeError(f"hb-view failed for {text!r}: {r.stderr.strip()[:200]}")
    return out_path


# A process-lifetime scratch directory for the visibility screen. Thousands of candidate pairs
# are rendered and compared while building; only their hashes are kept, and the directory is
# removed on exit, so no temporary image ever reaches the repository.
_SCRATCH = tempfile.mkdtemp(prefix="devx-screen-")
atexit.register(lambda: shutil.rmtree(_SCRATCH, ignore_errors=True))


@functools.lru_cache(maxsize=8192)
def _raster_sha256_cached(text: str, spec_key: tuple) -> str:
    spec = RenderSpec(*spec_key)
    out = Path(_SCRATCH) / (hashlib.sha256(text.encode("utf-8")).hexdigest()[:24] + ".png")
    render(text, out, spec)
    digest = sha256_file(out)
    out.unlink(missing_ok=True)
    return digest


def raster_sha256(text: str, spec: RenderSpec = RenderSpec()) -> str:
    """SHA-256 of the FINAL PNG for `text`. The authoritative 'what is on the page' value."""
    return _raster_sha256_cached(text, (spec.font_file, spec.face_index, spec.point_size,
                                        spec.margin, spec.background, spec.foreground))


# --------------------------------------------------------------------------------------------
# Validity screen
# --------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class MismatchValidity:
    valid: bool
    reason: str
    rendered_shape: str
    target_shape: str
    glyphs_differ: bool          # diagnostic only
    rendered_raster_sha256: str  # "" when not reached
    target_raster_sha256: str


def is_valid_mismatch(rendered: str, target: str,
                      spec: RenderSpec = RenderSpec()) -> MismatchValidity:
    """
    A mismatch item is fair only if the difference is BOTH textual and actually drawn.

    Gates, in order:
      1. `canonical_equal`  — the strings are the same after NFC, so there is no textual
                              difference at all.
      2. `rendering_error`  — shaping or rasterising failed; the pair cannot be judged.
      3. `raster_identical` — the FINAL PNGs are byte-identical. Asking a checker to report a
                              difference that is not on the page would penalise correct
                              observation. This is decided on pixels, not on glyph ids.

    The glyph-sequence comparison is recorded as a diagnostic. It is not the gate, because
    "different glyph sequence" and "different pixels" are different claims.
    """
    try:
        rs, ts = shape(rendered, spec), shape(target, spec)
    except (RuntimeError, ToolMissing, FontMissing) as e:
        return MismatchValidity(False, "rendering_error", "", "", False, "", "")

    if canonical_equal(rendered, target):
        return MismatchValidity(False, "canonical_equal", rs, ts, rs != ts, "", "")

    try:
        rr, tr = raster_sha256(rendered, spec), raster_sha256(target, spec)
    except (RuntimeError, ToolMissing, FontMissing):
        return MismatchValidity(False, "rendering_error", rs, ts, rs != ts, "", "")

    if rr == tr:
        return MismatchValidity(False, "raster_identical", rs, ts, rs != ts, rr, tr)
    return MismatchValidity(True, "ok", rs, ts, rs != ts, rr, tr)
