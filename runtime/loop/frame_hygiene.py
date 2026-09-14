"""Video-frame text hygiene — the runtime row RUNTIME-VIDEO-FRAME-TEXT (production-learning UPWORK-INTRO-001, SD-06).

WHY. On the Upwork intro pilot a Kling image-to-video clip grew letter-shaped shop signage in its last
second although the source still had passed the text scan; the post-draw scan had looked at the still,
never at the clip. The executor caught it by eye. The rule promoted here: a generated video's text verdict
comes ONLY from frames sampled from that video after generation. A text-clean source still is recorded
but transfers nothing. No sampled frames → NOT-RUN, never PASS.

The row is appended by runtime/loop/postdraw.run for video modality next to the canon gate's own
LIMIT-TEXT (which already scans caller-supplied frames); it exists so that the verdict of a video with no
frames is NOT_RUN at the gate level rather than PASS-by-omission, and so the report says in words that
the still did not stand in for the clip.
"""
from __future__ import annotations

from runtime.loop import outcome

CHECK_ID = "RUNTIME-VIDEO-FRAME-TEXT"


def _still_clause(source_still_clean) -> str:
    if source_still_clean is True:
        return "; the source still was text-clean — that does not transfer to the video"
    if source_still_clean is False:
        return "; the source still itself carried text"
    return ""


def assess(frame_detections, *, source_still_clean=None) -> dict:
    """One runtime row from the detector's answers over the sampled frames (in order).

    FAIL (blocking) if any frame reports `text`; NOT-RUN (blocking) if no frames were sampled or any
    frame was `unavailable` to the detector (an unscanned frame is not a clean frame); PASS otherwise."""
    frames = list(frame_detections or [])
    if not frames:
        return outcome.runtime_row(CHECK_ID, "NOT-RUN",
                                   "no frames were sampled from the generated video; a video's text verdict comes "
                                   "only from its sampled frames" + _still_clause(source_still_clean))
    texts = [(i, d) for i, d in enumerate(frames, 1) if d.status == "text"]
    if texts:
        i, d = texts[0]
        more = f"; +{len(texts) - 1} more frame(s)" if len(texts) > 1 else ""
        return outcome.runtime_row(CHECK_ID, "FAIL",
                                   f"frame {i} of {len(frames)}: text detected ('{d.transcript[:80]}') per {d.detector_id}"
                                   f"{more}" + _still_clause(source_still_clean))
    unavailable = [i for i, d in enumerate(frames, 1) if d.status != "no_text"]
    if unavailable:
        return outcome.runtime_row(CHECK_ID, "NOT-RUN",
                                   f"{len(unavailable)} of {len(frames)} sampled frames unavailable to the detector — "
                                   "not counted as text-free" + _still_clause(source_still_clean))
    return outcome.runtime_row(CHECK_ID, "PASS",
                               f"no text in {len(frames)} sampled frames per {frames[0].detector_id}"
                               + _still_clause(source_still_clean))
