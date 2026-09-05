"""repeat_consistency -> reproducibility: how alike are repeat 1 and repeat 2 of the same (case, route)?

    dHash (9x8 greyscale, 64-bit) Hamming distance and global SSIM between the two artifacts; a video is
    compared on its first / middle / last frames (ffmpeg) and reported per frame and as the maximum.
    `unseeded` (SEED-POLICY unset) and `held_seed` (held) groups are separate measurements that are
    never pooled: unseeded pass = both repeats produced a valid artifact of the same probed format
    (structural reproducibility; distances are observation only); held_seed pass = Hamming <= N.
Today every route is `unset` (SEED-POLICY.yaml), so only the unseeded rule can apply.
"""
from __future__ import annotations

from pathlib import Path

from . import common as C
from . import imageio as IO
from . import metrics as MX

INSTRUMENT_ID = "repeat_consistency"
VERSION = "0.1.0"
CAPABILITIES = ("reproducibility",)
GROUP_BY_POLICY = {"unset": "unseeded", "held": "held_seed"}
IMAGE_CONTAINERS = ("png_pipe", "image2", "jpeg_pipe", "webp_pipe", "gif", "bmp_pipe", "tiff_pipe")
FRAMES = ("first", "middle", "last")

dhash = MX.dhash


def _load(path: Path | str) -> tuple:
    """(kind, signature, [Image...]) - PNG via stdlib; other files via ffprobe/ffmpeg."""
    p = Path(path)
    if not p.exists() or p.stat().st_size == 0:
        raise IO.ProbeError(f"{p} does not exist or is empty")
    data = p.read_bytes()
    if data[:8] == IO.PNG_SIG:
        img = IO.decode_png(data)
        return "image", {"kind": "image", "container": "png", "width": img.width, "height": img.height, "has_audio": False}, [img]
    info = IO.ffprobe(p)
    cont = str(info["container"] or "")
    if any(c in cont for c in IMAGE_CONTAINERS) or (not info["has_video"] and not info["has_audio"]):
        img = IO.decode_image_ffmpeg(p)
        return "image", {"kind": "image", "container": cont, "width": img.width, "height": img.height, "has_audio": False}, [img]
    if info["has_video"]:
        frames = IO.decode_video_frames(p, FRAMES)
        return "video", {"kind": "video", "container": cont, "width": info["width"], "height": info["height"], "has_audio": info["has_audio"]}, frames
    raise IO.ProbeError(f"{p.name} is audio-only; repeat consistency compares pictures")


def measure(repeat1: Path | str, repeat2: Path | str, seed_policy: str) -> dict:
    if seed_policy not in GROUP_BY_POLICY:
        raise ValueError(f"seed_policy {seed_policy!r} is not one of {sorted(GROUP_BY_POLICY)}; groups are never pooled")
    kind1, sig1, imgs1 = _load(repeat1)
    kind2, sig2, imgs2 = _load(repeat2)
    per_frame = []
    labels = FRAMES if kind1 == "video" else ("image",)
    for i, (a, b) in enumerate(zip(imgs1, imgs2)):
        ha, hb = MX.dhash(a), MX.dhash(b)
        if (a.width, a.height) != (b.width, b.height):
            b = IO.resize_nearest(b, a.width, a.height)
        ssim = MX.ssim_grey(a, b)["ssim"]
        per_frame.append({"frame": labels[i] if i < len(labels) else str(i), "dhash_hamming": MX.hamming(ha, hb),
                          "dhash_1": f"{ha:016x}", "dhash_2": f"{hb:016x}", "ssim": ssim})
    same_format = (sig1["kind"] == sig2["kind"] and (sig1["width"], sig1["height"]) == (sig2["width"], sig2["height"])
                   and sig1["has_audio"] == sig2["has_audio"])
    return {
        "group": GROUP_BY_POLICY[seed_policy], "seed_policy": seed_policy, "kind": kind1,
        "frames_compared": list(labels) if kind1 == "video" else ["image"], "per_frame": per_frame,
        "dhash_hamming_max": max(f["dhash_hamming"] for f in per_frame),
        "ssim_min": min((f["ssim"] for f in per_frame if f["ssim"] is not None), default=None),
        "same_probed_format": same_format, "format_1": sig1, "format_2": sig2,
        "repeat1_sha256": C.sha256_file(repeat1), "repeat2_sha256": C.sha256_file(repeat2),
    }


def evaluate(repeat1, repeat2, seed_policy: str, criteria_path: Path | str | None = None) -> dict:
    crit = C.criterion(INSTRUMENT_ID, criteria_path)
    try:
        m = measure(repeat1, repeat2, seed_policy)
    except IO.ToolUnavailable as exc:
        return C.unavailable(str(exc))
    except (IO.ProbeError, OSError) as exc:
        return C.parse_failure(str(exc))
    t = crit.thresholds
    if m["group"] == "unseeded":
        ok = bool(m["same_probed_format"])
        defects = [] if ok else [{"term": f"repeats differ in probed format: {m['format_1']} vs {m['format_2']}"}]
    else:
        limit = int((t.get("held_seed") or {}).get("dhash_hamming_max", 4))
        ok = m["dhash_hamming_max"] <= limit and bool(m["same_probed_format"])
        defects = [] if ok else [{"term": f"held-seed repeats differ: max Hamming {m['dhash_hamming_max']} > {limit} or format differs"}]
    return C.gate(crit, ok, m, defects)


def instrument(criteria_path: Path | str | None = None):
    def fn(path, item, capability):
        ins = C.inputs_of(item)
        if not ins.get("other_repeat_path"):
            return C.parse_failure("reproducibility needs instrument_inputs.other_repeat_path (the other repeat of the same case x route)")
        return evaluate(path, ins["other_repeat_path"], ins.get("seed_policy", "unset"), criteria_path)
    return C.build_instrument(INSTRUMENT_ID, VERSION, CAPABILITIES, fn, criteria_path)
