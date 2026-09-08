"""masked_diff -> edit_preservation: did the edit leave everything OUTSIDE the named region alone?

    measure(input, output, mask)  output resized to the input's size (nearest-neighbour); MAE per channel
                                  (sRGB 0-255) over pixels outside the mask; SSIM (BT.601 grey, 8x8
                                  windows) over windows entirely outside the mask.
    mask                          a PNG the size of the input; grey >= 128 marks the CHANGED region;
                                  its sha256 and path are recorded (mask provenance).
Proposed thresholds live in PASS-CRITERIA-v0.yaml#masked_diff (frozen: false -> absent / criterion_not_frozen).
"""
from __future__ import annotations

from pathlib import Path

from . import common as C
from . import imageio as IO
from . import metrics as MX

INSTRUMENT_ID = "masked_diff"
VERSION = "0.1.0"
CAPABILITIES = ("edit_preservation",)


def load_mask(mask_path: Path | str, width: int, height: int) -> tuple[list, str]:
    """True = OUTSIDE the changed region (the pixels that must be preserved)."""
    p = Path(mask_path)
    img = C.read_image(p).to_grey()
    if (img.width, img.height) != (width, height):
        raise IO.ProbeError(f"mask {p.name} is {img.width}x{img.height}, input is {width}x{height}; a mask must match the input exactly")
    return [v < 128 for v in img.data], C.sha256_file(p)


def measure(input_path: Path | str, output_path: Path | str, mask_path: Path | str) -> dict:
    inp = C.read_image(input_path).to_rgb()
    out_img = C.read_image(output_path)
    original = [out_img.width, out_img.height]
    out = IO.resize_nearest(out_img.to_rgb(), inp.width, inp.height)
    outside, mask_sha = load_mask(mask_path, inp.width, inp.height)
    if not any(outside):
        raise IO.ProbeError("the mask covers the whole image; nothing is outside it to preserve")
    mae = MX.mae_rgb(inp, out, outside)
    ssim = MX.ssim_grey(inp, out, outside)
    return {
        "mae_outside_mask": mae["mean"], "mae_per_channel": mae["per_channel"],
        "ssim_outside_mask": ssim["ssim"], "ssim_windows_used": ssim["windows"],
        "pixels_outside_mask": mae["pixels"], "pixels_inside_mask": inp.width * inp.height - mae["pixels"],
        "input_size": [inp.width, inp.height], "output_original_size": original, "resized_output_to": [inp.width, inp.height],
        "resample": "nearest_neighbour", "colour_space": "sRGB 8-bit (MAE); BT.601 luma (SSIM)",
        "mask_sha256": mask_sha, "mask_provenance": {"path": str(mask_path), "sha256": mask_sha, "rule": "grey >= 128 marks the changed region"},
        "input_sha256": C.sha256_file(input_path), "output_sha256": C.sha256_file(output_path),
    }


def evaluate(input_path, output_path, mask_path, criteria_path: Path | str | None = None) -> dict:
    crit = C.criterion(INSTRUMENT_ID, criteria_path)
    try:
        m = measure(input_path, output_path, mask_path)
    except IO.ToolUnavailable as exc:
        return C.unavailable(str(exc))
    except (IO.ProbeError, OSError, ValueError) as exc:
        return C.parse_failure(str(exc))
    t = crit.thresholds
    defects = []
    if m["mae_outside_mask"] is None or m["mae_outside_mask"] > float(t.get("mae_max_per_channel_8bit", 8)):
        defects.append({"term": f"outside-mask MAE {m['mae_outside_mask']} > {t.get('mae_max_per_channel_8bit')}"})
    if m["ssim_outside_mask"] is None:
        defects.append({"term": "no 8x8 window lies entirely outside the mask; SSIM not computable"})
    elif m["ssim_outside_mask"] < float(t.get("ssim_min_outside_mask", 0.9)):
        defects.append({"term": f"outside-mask SSIM {m['ssim_outside_mask']:.4f} < {t.get('ssim_min_outside_mask')}"})
    return C.gate(crit, not defects, m, defects)


def instrument(criteria_path: Path | str | None = None):
    def fn(path, item, capability):
        ins = C.inputs_of(item)
        if not ins.get("input_path") or not ins.get("mask_path"):
            return C.parse_failure("edit_preservation needs instrument_inputs.input_path and .mask_path on the item")
        return evaluate(ins["input_path"], path, ins["mask_path"], criteria_path)
    return C.build_instrument(INSTRUMENT_ID, VERSION, CAPABILITIES, fn, criteria_path)
