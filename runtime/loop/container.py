"""Delivered-container hygiene — MP4 edit lists (production-learning RENTOK-GAME-A-004, defect D-1).

WHY. Lane A of the RentOK two-lane job wrote "no edit lists" into its own platform spec row (YouTube:
"No Edit Lists (or the video might not get processed correctly)"; Meta: "should not contain edit
lists"), and its deterministic suite passed the container on geometry, codec, size and moov-first — but
never looked for an `elst` box. ffmpeg writes two by default (the B-frame delay on video, the AAC
priming on audio), so the first deliverable carried exactly what the spec forbade. The independent
checker found it by walking the box tree; the fix was a USD-0 re-mux. The rule promoted here: a
container claim is verified by reading the container's own box tree, not by trusting the encoder's
defaults or a byte grep (media payload can contain any four letters).

This is a pure function over bytes: no ffprobe, no network. The agency QA path calls it on the
delivered file; a caller with no bytes gets NOT-RUN, never PASS-by-omission (as frame_hygiene does
for frames).
"""
from __future__ import annotations

from runtime.loop import outcome

CHECK_ID = "RUNTIME-VIDEO-CONTAINER-EDIT-LIST"
CONTAINER_BOXES = frozenset((b"moov", b"trak", b"edts", b"mdia", b"minf", b"stbl"))


def _boxes(data: bytes, start: int, end: int):
    """Yield (fourcc, header_size, box_start, box_end) for the boxes laid end to end in data[start:end]."""
    pos = start
    while pos + 8 <= end:
        size = int.from_bytes(data[pos:pos + 4], "big")
        fourcc = data[pos + 4:pos + 8]
        header = 8
        if size == 1:                                           # 64-bit largesize
            if pos + 16 > end:
                return
            size = int.from_bytes(data[pos + 8:pos + 16], "big")
            header = 16
        elif size == 0:                                         # box extends to the end of the file
            size = end - pos
        if size < header:                                       # malformed; stop rather than loop
            return
        yield fourcc, header, pos, min(pos + size, end)
        pos += size


def count_boxes(data: bytes, fourcc: bytes) -> int:
    """Count boxes of one type by walking the MP4 box tree (moov → trak → edts …), never by byte grep."""
    def walk(start: int, end: int) -> int:
        n = 0
        for typ, header, b0, b1 in _boxes(data, start, end):
            if typ == fourcc:
                n += 1
            if typ in CONTAINER_BOXES:
                n += walk(b0 + header, b1)
        return n
    return walk(0, len(data))


def top_level_boxes(data: bytes) -> list:
    return [typ.decode("latin-1") for typ, _h, _a, _b in _boxes(data, 0, len(data))]


def assess_edit_lists(data: bytes | None) -> dict:
    """One runtime row. NOT-RUN (blocking) when there are no bytes or no `moov` at the top level (not a
    readable MP4 — nothing was verified); FAIL (blocking) when any `elst` box exists in the tree; PASS
    with the count of tracks walked otherwise."""
    if not data:
        return outcome.runtime_row(CHECK_ID, "NOT-RUN",
                                   "no container bytes supplied; edit lists were not checked")
    top = top_level_boxes(data)
    if "moov" not in top:
        return outcome.runtime_row(CHECK_ID, "NOT-RUN",
                                   f"no moov box at the top level (found {top or 'nothing'}); not a readable MP4, "
                                   "so edit lists were not checked")
    n_elst = count_boxes(data, b"elst")
    n_trak = count_boxes(data, b"trak")
    if n_elst:
        return outcome.runtime_row(CHECK_ID, "FAIL",
                                   f"{n_elst} elst box(es) in the box tree across {n_trak} track(s); the platforms' "
                                   "own specs say none — re-mux without edit lists (ffmpeg -use_editlist 0)")
    return outcome.runtime_row(CHECK_ID, "PASS",
                               f"0 elst boxes across {n_trak} track(s), by walking the moov/trak/edts tree")
