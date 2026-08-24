#!/usr/bin/env python3
"""
Devanagari shaping + rendering primitives for the exactness battery.

WHY THIS EXISTS
    The battery's clean-control stratum needs ground truth that does not depend on anyone's
    annotation of a photograph. We get it by *constructing* the image: render a known string with
    a known font, and the image provably contains that string. No reader, no dataset label, no
    ambiguity about what is on the page.

THE TRAP THIS MODULE EXISTS TO PREVENT
    Two different Unicode strings can render to *identical pixels*. Measured on this machine:

        क़  (U+0958, precomposed)      -> [uni0915093C=0+770]
        क + nukta (U+0915 U+093C)      -> [uni0915093C=0+770]

    If we built a "mismatch" item from that pair, we would be asking a checker to report a
    difference that is not visible, and scoring it wrong for looking at the picture correctly.
    That measures Unicode pedantry, not visual faithfulness.

    Every mismatch item must therefore satisfy BOTH:
      1. the normalised target strings differ  (it is a real textual difference), and
      2. the shaped glyph sequences differ     (the difference is actually on the page).

    `is_valid_mismatch()` enforces both. Items failing either are rejected, with the reason
    recorded rather than silently dropped.

EXTERNAL TOOLS (all local, no network, no model, no spend)
    hb-shape     HarfBuzz shaping -> glyph sequence. Ground truth for "does this look different".
    pango-view   HarfBuzz-backed rasteriser -> deterministic PNG.
Both are invoked with an explicit font file so results do not depend on font fallback.
"""
from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
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

# Default rendering font. An explicit file, never a family name, so the run cannot silently
# change because fontconfig resolved a different face.
DEFAULT_FONT_FILE = "/System/Library/Fonts/Kohinoor.ttc"
DEFAULT_FONT_DESC = "Kohinoor Devanagari"


class ToolMissing(RuntimeError):
    """Raised when a required local tool is unavailable, so callers fail loudly."""


def require_tools(*names: str) -> None:
    missing = [n for n in names if shutil.which(n) is None]
    if missing:
        raise ToolMissing(
            f"required local tool(s) not found: {', '.join(missing)}. "
            f"This battery renders text locally; it makes no network or model calls."
        )


def nfc(s: str) -> str:
    """Canonical form used for every textual comparison in this battery.

    NFC matters here beyond tidiness: it maps the precomposed nukta letters (U+0958..U+095F) onto
    their decomposed equivalents, which is also what the renderer draws. Comparing in NFC
    therefore agrees with the pixels instead of disagreeing with them.
    """
    return unicodedata.normalize("NFC", s).strip()


def has_devanagari(s: str) -> bool:
    return any(DEV_START <= ord(c) <= DEV_END for c in s)


# --------------------------------------------------------------------------------------------
# Shaping
# --------------------------------------------------------------------------------------------
def shape(text: str, font_file: str = DEFAULT_FONT_FILE) -> str:
    """Return HarfBuzz's shaped glyph sequence for `text` as a stable string.

    This is the mechanical answer to "would these two strings look different on the page".
    Glyph ids and cluster/advance values are included, so a pure reordering that produces the
    same glyphs in a different arrangement is still distinguishable.
    """
    require_tools("hb-shape")
    if not Path(font_file).exists():
        raise ToolMissing(f"font file not found: {font_file}")
    codes = ",".join(f"U+{ord(c):04X}" for c in text)
    if not codes:
        return ""
    r = subprocess.run(
        ["hb-shape", f"--font-file={font_file}", f"--unicodes={codes}"],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        raise RuntimeError(f"hb-shape failed for {codes!r}: {r.stderr.strip()[:200]}")
    return r.stdout.strip()


def glyphs_differ(a: str, b: str, font_file: str = DEFAULT_FONT_FILE) -> bool:
    """True when the two strings shape to different glyph sequences — i.e. look different."""
    return shape(a, font_file) != shape(b, font_file)


@dataclass(frozen=True)
class MismatchValidity:
    valid: bool
    reason: str
    rendered_shape: str
    target_shape: str


def is_valid_mismatch(rendered: str, target: str,
                      font_file: str = DEFAULT_FONT_FILE) -> MismatchValidity:
    """
    A mismatch item is fair only if the difference is BOTH textual and visible.

    Rejects, with the reason recorded:
      * `normalised_equal`  — not a textual difference at all after NFC.
      * `glyphs_identical`  — a textual difference the renderer does not draw. Asking a checker
                              to report it would penalise correct observation.
    """
    rs, ts = shape(rendered, font_file), shape(target, font_file)
    if nfc(rendered) == nfc(target):
        return MismatchValidity(False, "normalised_equal", rs, ts)
    if rs == ts:
        return MismatchValidity(False, "glyphs_identical", rs, ts)
    return MismatchValidity(True, "ok", rs, ts)


# --------------------------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class RenderSpec:
    """Everything that affects the pixels. Recorded per item so a run is reproducible."""
    font_file: str = DEFAULT_FONT_FILE
    font_desc: str = DEFAULT_FONT_DESC
    point_size: int = 40
    margin: int = 24
    background: str = "white"
    foreground: str = "black"

    def as_dict(self) -> dict:
        return {
            "font_file": self.font_file, "font_desc": self.font_desc,
            "point_size": self.point_size, "margin": self.margin,
            "background": self.background, "foreground": self.foreground,
        }


def render(text: str, out_path: Path, spec: RenderSpec = RenderSpec()) -> Path:
    """Rasterise `text` to a PNG. Deterministic: identical inputs give byte-identical output."""
    require_tools("pango-view")
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, LC_ALL="en_US.UTF-8", LANG="en_US.UTF-8")
    r = subprocess.run(
        ["pango-view", "-q",
         f"--font={spec.font_desc} {spec.point_size}",
         f"--text={text}",
         f"--background={spec.background}", f"--foreground={spec.foreground}",
         f"--margin={spec.margin}",
         "-o", str(out_path)],
        capture_output=True, text=True, env=env,
    )
    if r.returncode != 0 or not out_path.exists():
        raise RuntimeError(f"pango-view failed for {text!r}: {r.stderr.strip()[:200]}")
    return out_path


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()
