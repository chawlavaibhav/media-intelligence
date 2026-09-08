"""brand_colour -> packaging_brand_colour_fidelity: how far is the pack's colour from the brand's?

    mean sRGB inside the pack/product mask -> linear (IEC 61966-2-1) -> XYZ (D65) -> CIELAB; dE*ab
    (CIE76) against the fixture-recorded sRGB reference converted the same way.
Proposed threshold: PASS-CRITERIA-v0.yaml#brand_colour (frozen: false -> absent / criterion_not_frozen).
"""
from __future__ import annotations

import math
from pathlib import Path

from . import common as C
from . import imageio as IO

INSTRUMENT_ID = "brand_colour"
VERSION = "0.1.0"
CAPABILITIES = ("packaging_brand_colour_fidelity",)
D65 = (0.95047, 1.0, 1.08883)


def _lin(c: float) -> float:
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def srgb_to_xyz(rgb) -> tuple:
    r, g, b = (_lin(v) for v in rgb)
    return (0.4124564 * r + 0.3575761 * g + 0.1804375 * b,
            0.2126729 * r + 0.7151522 * g + 0.0721750 * b,
            0.0193339 * r + 0.1191920 * g + 0.9503041 * b)


def _f(t: float) -> float:
    return t ** (1.0 / 3.0) if t > (6.0 / 29.0) ** 3 else t / (3 * (6.0 / 29.0) ** 2) + 4.0 / 29.0


def srgb_to_lab(rgb) -> tuple:
    x, y, z = srgb_to_xyz(rgb)
    fx, fy, fz = _f(x / D65[0]), _f(y / D65[1]), _f(z / D65[2])
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def delta_e76(lab_a, lab_b) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(lab_a, lab_b)))


def measure(image_path: Path | str, mask_path: Path | str, reference_srgb) -> dict:
    img = C.read_image(image_path).to_rgb()
    mask = C.read_image(mask_path).to_grey()
    if (mask.width, mask.height) != (img.width, img.height):
        raise IO.ProbeError(f"mask is {mask.width}x{mask.height}, image is {img.width}x{img.height}; a mask must match the image exactly")
    ref = tuple(int(v) for v in reference_srgb)
    if len(ref) != 3 or any(not 0 <= v <= 255 for v in ref):
        raise IO.ProbeError(f"reference sRGB {reference_srgb!r} is not three 0-255 values")
    sums = [0, 0, 0]
    n = 0
    d, md = img.data, mask.data
    for i in range(img.width * img.height):
        if md[i] >= 128:
            n += 1
            sums[0] += d[3 * i]
            sums[1] += d[3 * i + 1]
            sums[2] += d[3 * i + 2]
    if n == 0:
        raise IO.ProbeError("the mask selects no pixels; a colour cannot be measured over an empty region")
    mean = [s / n for s in sums]
    lab = srgb_to_lab(mean)
    ref_lab = srgb_to_lab(ref)
    return {
        "mean_srgb_in_mask": [int(round(v)) for v in mean], "mean_srgb_in_mask_exact": mean,
        "mean_lab_in_mask": list(lab), "reference_srgb": list(ref), "reference_lab": list(ref_lab),
        "delta_e_ab": delta_e76(lab, ref_lab), "delta_e_formula": "CIE76", "colour_space": "CIELAB D65 via sRGB->linear->XYZ",
        "pixels_in_mask": n, "mask_sha256": C.sha256_file(mask_path), "image_sha256": C.sha256_file(image_path),
    }


def evaluate(image_path, mask_path, reference_srgb, criteria_path: Path | str | None = None) -> dict:
    crit = C.criterion(INSTRUMENT_ID, criteria_path)
    try:
        m = measure(image_path, mask_path, reference_srgb)
    except IO.ToolUnavailable as exc:
        return C.unavailable(str(exc))
    except (IO.ProbeError, OSError, ValueError, TypeError) as exc:
        return C.parse_failure(str(exc))
    limit = float(crit.thresholds.get("delta_e_ab_max", 5.0))
    ok = m["delta_e_ab"] <= limit
    return C.gate(crit, ok, m, [] if ok else [{"term": f"dE*ab {m['delta_e_ab']:.2f} > {limit}"}])


def instrument(criteria_path: Path | str | None = None):
    def fn(path, item, capability):
        ins = C.inputs_of(item)
        if not ins.get("mask_path") or ins.get("reference_srgb") is None:
            return C.parse_failure("packaging_brand_colour_fidelity needs instrument_inputs.mask_path and .reference_srgb on the item")
        return evaluate(path, ins["mask_path"], ins["reference_srgb"], criteria_path)
    return C.build_instrument(INSTRUMENT_ID, VERSION, CAPABILITIES, fn, criteria_path)
