#!/usr/bin/env python3
"""Deterministic temporal perturbations - the transformations that CREATE truth.

THE IDEA IN ONE PARAGRAPH
-------------------------
Normally you learn whether a video has a defect by asking a person to watch it
and say so. That is slow, expensive and itself uncertain. Here we do the
opposite: we take a clean clip and BREAK IT ON PURPOSE, in a known way, at a
known time. Because we performed the break, we already know the answer. There
is nothing to annotate. The instrument under test is then asked whether it can
find the break we know is there - and, separately, whether it wrongly reports a
break in the untouched clip.

Every function below therefore returns two things: the perturbed clip, and the
exact truth record describing what was done and where.

RULES OBSERVED HERE
-------------------
* Deterministic. No wall clock, no unseeded randomness. Any randomness is seeded
  from a hash of the source clip and the parameters, so a rebuild reproduces the
  same bytes.
* A perturbation that does not change the pixels is NOT a defect. It raises
  NullPerturbationError rather than being silently written into the pack as a
  fixture whose "truth" is undetectable.
* Truth is the transformation itself. No function here consults a label, a
  model, a network or a human.
* These functions do not decide whether an instrument passes. They only build
  material. Gate arithmetic lives in qualify_temporal.py.
"""
from __future__ import annotations

import hashlib
import json

from clipseq import ClipError, ClipSequence


class NullPerturbationError(ClipError):
    """A declared perturbation left the pixels unchanged.

    This is treated as a build failure, not a curiosity. A fixture whose
    injected defect is invisible would score every instrument as a miss and
    would silently corrupt the recall figure.
    """


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def _seed(source_hash: str, ptype: str, params: dict) -> int:
    blob = f"{source_hash}|{ptype}|{json.dumps(params, sort_keys=True)}".encode()
    return int.from_bytes(hashlib.sha256(blob).digest()[:8], "big")


def _check_interval(clip: ClipSequence, start: int, end: int, what: str) -> None:
    if not isinstance(start, int) or not isinstance(end, int):
        raise ClipError(f"{what}: interval bounds must be integers")
    if not (0 <= start < end <= clip.n_frames):
        raise ClipError(f"{what}: interval [{start},{end}) outside clip of "
                        f"{clip.n_frames} frames")


def _check_bbox(clip: ClipSequence, bbox) -> tuple:
    try:
        x, y, w, h = (int(v) for v in bbox)
    except (TypeError, ValueError) as exc:
        raise ClipError(f"bbox must be 4 integers (x,y,w,h), got {bbox!r}") from exc
    if w <= 0 or h <= 0 or x < 0 or y < 0 or x + w > clip.width or y + h > clip.height:
        raise ClipError(f"bbox {bbox!r} outside frame {clip.width}x{clip.height}")
    return x, y, w, h


# How many independent samples an evaluator must land INSIDE the affected
# interval before the defect is even in principle observable.
#
# 1  - the perturbed content differs from its surroundings, so a single sample
#      inside the window can already disagree with the rest of the clip.
# 2  - the evidence IS the relationship between two samples (two consecutive
#      frames being identical, or a jump between them). One sample cannot show it.
#
# This is a derivation from what each defect physically is. It is NOT a
# qualification threshold and sets no pass mark.
_MIN_SAMPLES_INSIDE = {
    "frame_freeze": 2,
    "frame_duplication": 2,
    "frame_drop": 2,
    "frame_reversal": 2,
    "segment_reordering": 2,
    "shot_horizontal_flip": 1,
    "midclip_horizontal_flip": 1,
    "identity_splice": 1,
    "product_region_substitution": 1,
    "text_region_mutation": 1,
    "text_glyph_substitution": 1,
    "framing_discontinuity": 1,
    "technical_corruption": 1,
}

# Which frozen capability each perturbation supplies known truth for.
# Sourced from eval/v1/instruments/FAMILY-4-TEMPORAL-VIDEO.md and the frozen
# EVALUATOR-QUALIFICATION-MAP. No capability is invented here.
_CAPABILITY_TARGETS = {
    "frame_freeze":                ["motion_action_quality", "technical_visual_integrity"],
    "frame_duplication":           ["motion_action_quality", "technical_visual_integrity"],
    "frame_drop":                  ["motion_action_quality", "technical_visual_integrity"],
    "frame_reversal":              ["motion_action_quality", "action_adherence"],
    "segment_reordering":          ["sequence_state_continuity", "action_adherence"],
    "shot_horizontal_flip":        ["multi_shot_spatial_continuity"],
    "midclip_horizontal_flip":     ["multi_shot_spatial_continuity", "technical_visual_integrity"],
    "identity_splice":             ["person_stability_in_clip"],
    "product_region_substitution": ["product_stability_in_clip"],
    "text_region_mutation":        ["text_logo_stability_in_clip"],
    "text_glyph_substitution":     ["text_logo_stability_in_clip"],
    "framing_discontinuity":       ["camera_framing_fidelity"],
    "technical_corruption":        ["technical_visual_integrity"],
}


def _finalise(source: ClipSequence, out_frames: list, ptype: str, params: dict,
              out_start: int, out_end: int, src_start: int, src_end: int,
              region=None, region_source=None, extra=None) -> tuple:
    """Build the perturbed clip and its truth record, rejecting no-ops."""
    if ptype not in _MIN_SAMPLES_INSIDE:
        raise ClipError(f"unknown perturbation type {ptype!r}")
    out = ClipSequence(f"{source.clip_id}__{ptype}", source.width, source.height,
                       source.fps, out_frames, dict(source.provenance))
    if out.content_hash() == source.content_hash():
        raise NullPerturbationError(
            f"{ptype} on {source.clip_id} produced pixel-identical output; "
            "an injected defect that changes nothing is not a defect")

    interval_s = round((out_end - out_start) / source.fps, 6)
    min_samples = _MIN_SAMPLES_INSIDE[ptype]
    truth = {
        "perturbation_type": ptype,
        "params": params,
        "deterministic_seed": _seed(source.content_hash(), ptype, params),
        "source_clip_id": source.clip_id,
        "source_content_hash": source.content_hash(),
        "source_n_frames": source.n_frames,
        "source_motion_load": source.motion_load(),
        "output_content_hash": out.content_hash(),
        "output_n_frames": out.n_frames,
        "output_motion_load": out.motion_load(),
        "fps": source.fps,
        # Where the defect is, in the OUTPUT clip an instrument will be shown.
        "affected_output_frames": [out_start, out_end],
        "affected_output_time_s": [round(out_start / source.fps, 6),
                                   round(out_end / source.fps, 6)],
        # Where it came from in the SOURCE, which differs whenever frames were
        # inserted or removed.
        "affected_source_frames": [src_start, src_end],
        "affected_region_xywh": list(region) if region else None,
        "affected_region_source": region_source,
        "defect_present": True,
        "targets_capabilities": list(_CAPABILITY_TARGETS[ptype]),
        # Sampling arithmetic - the frozen family-4 caveat made explicit.
        "min_samples_inside_interval": min_samples,
        "affected_interval_s": interval_s,
        "min_uniform_sample_fps_for_visibility": (
            None if interval_s <= 0 else round(min_samples / interval_s, 6)),
    }
    if extra:
        truth.update(extra)
    return out, truth


# --------------------------------------------------------------------------
# temporal-structure perturbations
# --------------------------------------------------------------------------
def frame_freeze(clip: ClipSequence, start: int, length: int) -> tuple:
    """Hold one frame still for `length` frames - a stall. Clip length unchanged."""
    end = start + length
    _check_interval(clip, start, end, "frame_freeze")
    if length < 2:
        raise ClipError("frame_freeze: a freeze shorter than 2 frames is not a stall")
    frames = [bytearray(f) for f in clip.frames]
    held = bytearray(clip.frames[start])
    for i in range(start, end):
        frames[i] = bytearray(held)
    return _finalise(clip, frames, "frame_freeze",
                     {"start": start, "length": length}, start, end, start, end)


def frame_duplication(clip: ClipSequence, start: int, run: int, repeats: int) -> tuple:
    """Re-insert a run of frames `repeats` extra times. The clip gets LONGER.

    Distinct from a freeze: a freeze repeats ONE frame in place, duplication
    replays a moving run, so the motion stutters backwards and forwards rather
    than stopping.
    """
    end = start + run
    _check_interval(clip, start, end, "frame_duplication")
    if run < 1 or repeats < 1:
        raise ClipError("frame_duplication: run and repeats must both be >= 1")
    block = [bytearray(f) for f in clip.frames[start:end]]
    frames = [bytearray(f) for f in clip.frames[:end]]
    for _ in range(repeats):
        frames += [bytearray(f) for f in block]
    frames += [bytearray(f) for f in clip.frames[end:]]
    return _finalise(clip, frames, "frame_duplication",
                     {"start": start, "run": run, "repeats": repeats},
                     start, end + run * repeats, start, end)


def frame_drop(clip: ClipSequence, start: int, length: int) -> tuple:
    """Remove a known run of frames - a temporal jump. The clip gets SHORTER."""
    end = start + length
    _check_interval(clip, start, end, "frame_drop")
    if clip.n_frames - length < 2:
        raise ClipError("frame_drop: would leave fewer than 2 frames")
    frames = [bytearray(f) for f in clip.frames[:start]] + \
             [bytearray(f) for f in clip.frames[end:]]
    # The discontinuity in the output sits at the seam: the pair of frames that
    # are now adjacent but were not adjacent in the source.
    seam_lo = max(0, start - 1)
    seam_hi = min(len(frames), start + 1)
    return _finalise(clip, frames, "frame_drop",
                     {"start": start, "length": length}, seam_lo, seam_hi, start, end)


def frame_reversal(clip: ClipSequence, start: int, length: int) -> tuple:
    """Play a known run backwards - motion reverses direction and returns."""
    end = start + length
    _check_interval(clip, start, end, "frame_reversal")
    if length < 3:
        raise ClipError("frame_reversal: a run shorter than 3 frames is not a reversal")
    frames = [bytearray(f) for f in clip.frames]
    frames[start:end] = [bytearray(f) for f in reversed(clip.frames[start:end])]
    return _finalise(clip, frames, "frame_reversal",
                     {"start": start, "length": length}, start, end, start, end)


def segment_reordering(clip: ClipSequence, start: int, length: int, insert_at: int) -> tuple:
    """Move a run of frames to an earlier or later position.

    Anything whose visible state advances over time (a filling progress bar, a
    box being opened, a counter) is then provably out of order. That gives
    sequence_state_continuity a known-truth defect WITHOUT anyone labelling
    what the state is: the order is wrong because we reordered it.
    """
    end = start + length
    _check_interval(clip, start, end, "segment_reordering")
    if length < 2:
        raise ClipError("segment_reordering: run must be >= 2 frames")
    rest = [bytearray(f) for f in clip.frames[:start]] + \
           [bytearray(f) for f in clip.frames[end:]]
    if not (0 <= insert_at <= len(rest)):
        raise ClipError("segment_reordering: insert_at outside the remaining clip")
    if insert_at == start:
        raise ClipError("segment_reordering: insert_at equals start - that is a no-op")
    block = [bytearray(f) for f in clip.frames[start:end]]
    frames = rest[:insert_at] + block + rest[insert_at:]
    return _finalise(clip, frames, "segment_reordering",
                     {"start": start, "length": length, "insert_at": insert_at},
                     insert_at, insert_at + length, start, end)


# --------------------------------------------------------------------------
# orientation perturbations
# --------------------------------------------------------------------------
def _flip_frame(frame: bytearray, width: int, height: int) -> bytearray:
    out = bytearray(len(frame))
    stride = width * 3
    for y in range(height):
        row = frame[y * stride:(y + 1) * stride]
        flipped = bytearray(stride)
        for x in range(width):
            src = x * 3
            dst = (width - 1 - x) * 3
            flipped[dst:dst + 3] = row[src:src + 3]
        out[y * stride:(y + 1) * stride] = flipped
    return out


def _flip_interval(clip: ClipSequence, start: int, end: int, ptype: str,
                   params: dict, extra=None) -> tuple:
    _check_interval(clip, start, end, ptype)
    frames = [bytearray(f) for f in clip.frames]
    for i in range(start, end):
        frames[i] = _flip_frame(clip.frames[i], clip.width, clip.height)
    return _finalise(clip, frames, ptype, params, start, end, start, end, extra=extra)


def shot_horizontal_flip(clip: ClipSequence, shot_index: int, shots: list) -> tuple:
    """Mirror exactly one shot of a multi-shot clip.

    A subject walking left-to-right in shot 1 now walks right-to-left in shot 2
    with no cue that they turned round. That is the classic screen-direction
    violation, and it is invisible in any single frame - which is precisely why
    frame-level checkers cannot substitute for this family.
    """
    if not shots:
        raise ClipError("shot_horizontal_flip: clip declares no shot boundaries")
    if not (0 <= shot_index < len(shots)):
        raise ClipError(f"shot_horizontal_flip: no shot {shot_index}")
    if len(shots) < 2:
        raise ClipError("shot_horizontal_flip: needs a clip with at least 2 shots")
    start, end = shots[shot_index]
    return _flip_interval(clip, start, end, "shot_horizontal_flip",
                          {"shot_index": shot_index, "shots": [list(s) for s in shots]},
                          extra={"n_shots": len(shots)})


def midclip_horizontal_flip(clip: ClipSequence, start: int, end: int) -> tuple:
    """Mirror a run inside a single continuous shot - an orientation break with
    no cut to excuse it."""
    return _flip_interval(clip, start, end, "midclip_horizontal_flip",
                          {"start": start, "end": end})


# --------------------------------------------------------------------------
# identity / content perturbations
# --------------------------------------------------------------------------
def identity_splice(clip: ClipSequence, donor: ClipSequence, start: int, length: int) -> tuple:
    """Swap in frames from a DIFFERENT clip - a different person, mid-shot.

    Fails closed if the donor's geometry or frame rate differs: silently
    rescaling would introduce a second, undeclared defect and destroy the
    one-defect-per-fixture property the recall figure depends on.
    """
    end = start + length
    _check_interval(clip, start, end, "identity_splice")
    if (donor.width, donor.height, donor.fps) != (clip.width, clip.height, clip.fps):
        raise ClipError("identity_splice: donor geometry/fps differs from the base clip")
    if donor.content_hash() == clip.content_hash():
        raise ClipError("identity_splice: donor is the same material as the base clip")
    if donor.n_frames < length:
        raise ClipError("identity_splice: donor is shorter than the spliced run")
    frames = [bytearray(f) for f in clip.frames]
    for k, i in enumerate(range(start, end)):
        frames[i] = bytearray(donor.frames[k])
    return _finalise(clip, frames, "identity_splice",
                     {"start": start, "length": length,
                      "donor_clip_id": donor.clip_id,
                      "donor_content_hash": donor.content_hash()},
                     start, end, start, end,
                     extra={"donor_clip_id": donor.clip_id,
                            "donor_content_hash": donor.content_hash()})


def _region_map(clip: ClipSequence, bbox, start: int, end: int, ptype: str,
                params: dict, transform, region_source: str, extra=None) -> tuple:
    x, y, w, h = _check_bbox(clip, bbox)
    _check_interval(clip, start, end, ptype)
    frames = [bytearray(f) for f in clip.frames]
    for i in range(start, end):
        f = frames[i]
        for yy in range(y, y + h):
            base = (yy * clip.width + x) * 3
            for xx in range(w):
                o = base + xx * 3
                f[o], f[o + 1], f[o + 2] = transform(
                    f[o], f[o + 1], f[o + 2], xx, yy - y, i)
    return _finalise(clip, frames, ptype, params, start, end, start, end,
                     region=(x, y, w, h), region_source=region_source, extra=extra)


def product_region_substitution(clip: ClipSequence, bbox, start: int, end: int,
                                region_source: str = "declared") -> tuple:
    """Replace the product's pixels with a deterministically different product
    from a known frame onward - the object morphs mid-clip."""
    def swap(r, g, b, xx, yy, _i):
        # A fixed, reversible-looking but visibly different appearance: channel
        # rotation plus a coarse stripe, so the object is clearly a DIFFERENT
        # object rather than the same one under different light.
        stripe = 40 if ((xx + yy) // 3) % 2 else 0
        return (min(255, b + stripe), min(255, r), min(255, g))
    return _region_map(clip, bbox, start, end, "product_region_substitution",
                       {"bbox": list(bbox), "start": start, "end": end},
                       swap, region_source)


def text_region_mutation(clip: ClipSequence, bbox, start: int, end: int,
                         shift_px: int = 3, region_source: str = "declared") -> tuple:
    """Alter the rendered text inside its region from a known frame onward.

    Works on ANY clip, including real footage, because it changes pixels rather
    than characters. The known truth is 'the text surface changed at frame k',
    which is exactly the failure text_logo_stability_in_clip names: a string
    that is right at the start of a clip and wrong later on.
    """
    if shift_px == 0:
        raise ClipError("text_region_mutation: shift_px of 0 would change nothing")
    x, y, w, h = _check_bbox(clip, bbox)
    _check_interval(clip, start, end, "text_region_mutation")
    frames = [bytearray(f) for f in clip.frames]
    for i in range(start, end):
        f = frames[i]
        for yy in range(y, y + h):
            row_base = (yy * clip.width + x) * 3
            row = bytes(f[row_base:row_base + w * 3])
            shifted = bytearray(w * 3)
            for xx in range(w):
                src = (xx - shift_px) % w
                shifted[xx * 3:xx * 3 + 3] = row[src * 3:src * 3 + 3]
            f[row_base:row_base + w * 3] = shifted
    return _finalise(clip, frames, "text_region_mutation",
                     {"bbox": list(bbox), "start": start, "end": end,
                      "shift_px": shift_px},
                     start, end, start, end,
                     region=(x, y, w, h), region_source=region_source)


def text_glyph_substitution(clip: ClipSequence, bbox, start: int, end: int,
                            renderer, before: str, after: str,
                            region_source: str = "declared") -> tuple:
    """Re-render the text region with a DIFFERENT string from frame k onward.

    Only available where we control the rendering - i.e. constructed clips.
    Real supplied footage cannot use this, because we do not own its glyphs;
    it uses text_region_mutation instead. Both give known truth; only this one
    also records the exact before/after strings.
    """
    if before == after:
        raise ClipError("text_glyph_substitution: before and after strings are identical")
    x, y, w, h = _check_bbox(clip, bbox)
    _check_interval(clip, start, end, "text_glyph_substitution")
    frames = [bytearray(f) for f in clip.frames]
    for i in range(start, end):
        renderer(frames[i], clip.width, (x, y, w, h), after)
    return _finalise(clip, frames, "text_glyph_substitution",
                     {"bbox": list(bbox), "start": start, "end": end,
                      "text_before": before, "text_after": after},
                     start, end, start, end,
                     region=(x, y, w, h), region_source=region_source,
                     extra={"text_before": before, "text_after": after})


# --------------------------------------------------------------------------
# framing and technical perturbations
# --------------------------------------------------------------------------
def framing_discontinuity(clip: ClipSequence, start: int, end: int,
                          crop_num: int = 3, crop_den: int = 4,
                          anchor_x_num: int = 1, anchor_y_num: int = 1,
                          anchor_den: int = 8) -> tuple:
    """Crop and rescale from a known frame onward - the framing jumps.

    Integer nearest-neighbour scaling only, so the result is bit-exact on every
    machine. The subject is unchanged and the motion is unchanged; only the
    OBSERVER's framing breaks, which is the distinction the frozen contract
    draws between camera_framing_fidelity and action_adherence.
    """
    _check_interval(clip, start, end, "framing_discontinuity")
    if not (0 < crop_num < crop_den):
        raise ClipError("framing_discontinuity: crop fraction must be a proper fraction")
    cw = max(2, clip.width * crop_num // crop_den)
    ch = max(2, clip.height * crop_num // crop_den)
    ox = min(clip.width - cw, clip.width * anchor_x_num // anchor_den)
    oy = min(clip.height - ch, clip.height * anchor_y_num // anchor_den)
    frames = [bytearray(f) for f in clip.frames]
    for i in range(start, end):
        src = clip.frames[i]
        out = bytearray(len(src))
        for yy in range(clip.height):
            sy = oy + (yy * ch) // clip.height
            srow = sy * clip.width * 3
            drow = yy * clip.width * 3
            for xx in range(clip.width):
                sx = ox + (xx * cw) // clip.width
                s = srow + sx * 3
                d = drow + xx * 3
                out[d:d + 3] = src[s:s + 3]
        frames[i] = out
    return _finalise(clip, frames, "framing_discontinuity",
                     {"start": start, "end": end, "crop_num": crop_num,
                      "crop_den": crop_den, "anchor_x_num": anchor_x_num,
                      "anchor_y_num": anchor_y_num, "anchor_den": anchor_den},
                     start, end, start, end,
                     extra={"crop_box_xywh": [ox, oy, cw, ch]})


def technical_corruption(clip: ClipSequence, start: int, end: int,
                         block: int = 8, severity: int = 96) -> tuple:
    """Inject block-level corruption in a known interval.

    Stands in for the compression breakup, flicker and transient garbage that
    technical_visual_integrity exists to catch - the class of defect that every
    other capability can pass while a customer rejects the asset on sight.

    The block pattern is seeded from the source clip hash and the parameters, so
    it is different per fixture but identical on every rebuild.
    """
    _check_interval(clip, start, end, "technical_corruption")
    if not (1 <= severity <= 255):
        raise ClipError("technical_corruption: severity must be 1..255")
    if block < 2:
        raise ClipError("technical_corruption: block must be >= 2 pixels")
    params = {"start": start, "end": end, "block": block, "severity": severity}
    state = _seed(clip.content_hash(), "technical_corruption", params)
    frames = [bytearray(f) for f in clip.frames]
    blocks_hit = 0
    for i in range(start, end):
        f = frames[i]
        for by in range(0, clip.height, block):
            for bx in range(0, clip.width, block):
                # xorshift64* - deterministic, stdlib-free of `random`.
                state ^= (state << 13) & 0xFFFFFFFFFFFFFFFF
                state ^= state >> 7
                state ^= (state << 17) & 0xFFFFFFFFFFFFFFFF
                if state % 3:
                    continue
                blocks_hit += 1
                dr = (state >> 3) % severity
                dg = (state >> 11) % severity
                db = (state >> 19) % severity
                for yy in range(by, min(by + block, clip.height)):
                    o = (yy * clip.width + bx) * 3
                    for xx in range(min(block, clip.width - bx)):
                        p = o + xx * 3
                        f[p] = (f[p] + dr) & 0xFF
                        f[p + 1] = (f[p + 1] + dg) & 0xFF
                        f[p + 2] = (f[p + 2] + db) & 0xFF
    if blocks_hit == 0:
        raise NullPerturbationError("technical_corruption: no block was corrupted")
    return _finalise(clip, frames, "technical_corruption", params,
                     start, end, start, end,
                     extra={"blocks_corrupted": blocks_hit})


def null_perturbation(clip: ClipSequence) -> tuple:
    """A deliberately inert transformation.

    It exists ONLY so the build and the tests can prove that the pack builder
    refuses it. Rule 6 of the frozen qualification master spec: test the
    machinery with deliberately broken inputs, and never let an empty check
    report success.
    """
    return _finalise(clip, [bytearray(f) for f in clip.frames], "frame_freeze",
                     {"start": 0, "length": 0}, 0, 0, 0, 0)


PERTURBATIONS = tuple(sorted(_CAPABILITY_TARGETS))
CAPABILITY_TARGETS = dict(_CAPABILITY_TARGETS)
MIN_SAMPLES_INSIDE = dict(_MIN_SAMPLES_INSIDE)
