"""Stdlib container probes — what an artifact's headers say without decoding a pixel
(CANON-GATE-001 plan §E, §B artifact.py).

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

PNG: signature + IHDR. JPEG: marker walk to the first SOF (C0–C3, C5–C7, C9–CB, CD–CF);
standalone markers D0–D7, D8, 01 and fill bytes carry no length; SOS before SOF is a
ProbeError. EXIF orientation is not applied (documented limitation). MP4 / ISO-BMFF: box walk
(32-bit size, size==1 largesize, size==0 to-EOF); `ftyp` required; `moov` may follow `mdat`;
mvhd v0/v1 -> timescale, duration; per trak: hdlr handler (vide/soun), stsd first sample
entry -> codec and width/height at entry offset +32/+34, tkhd matrix for a 90°/270°
rotation (dimensions swapped), mdhd as a duration cross-check. Fragmented input (`moof`,
mvhd duration 0) yields no duration. GIF / WEBP / HEIC are recognised and reported as
unsupported; unrecognised or truncated bytes raise ProbeError so the gate fails closed.
No pixel value is ever read: text, contrast, highlights, shadows, tangency, faces, motion
and colour are out of reach here by design.
"""
from __future__ import annotations

import struct
from dataclasses import dataclass

from canon.gate.findings import TOLERANCES

SOF_MARKERS = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
STANDALONE_MARKERS = set(range(0xD0, 0xD8)) | {0xD8, 0x01}
VIDEO_CODECS = {"avc1", "hvc1", "hev1", "mp4v", "vp09", "av01", "avc3", "dvh1"}
HEIC_BRANDS = {b"heic", b"heix", b"hevc", b"hevx", b"mif1", b"msf1", b"avif"}


class ProbeError(Exception):
    """Truncated or malformed input — the gate reports ERROR and fails closed."""


@dataclass
class ArtifactInfo:
    kind: str                      # image | video | unknown
    container: str                 # png | jpeg | mp4 | mov | gif | webp | heic
    width: int | None = None
    height: int | None = None
    duration_s: float | None = None
    has_video_track: bool = False
    has_audio_track: bool = False
    codec: str | None = None
    notes: tuple = ()


# ── dispatcher ───────────────────────────────────────────────────────────────

def probe(data: bytes) -> ArtifactInfo:
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return probe_png(data)
    if data[:2] == b"\xff\xd8":
        return probe_jpeg(data)
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return ArtifactInfo("unknown", "gif", notes=("unsupported container: gif",))
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return ArtifactInfo("unknown", "webp", notes=("unsupported container: webp",))
    if len(data) >= 12 and data[4:8] == b"ftyp":
        if data[8:12] in HEIC_BRANDS:
            return ArtifactInfo("unknown", "heic", notes=("unsupported container: heic",))
        return probe_mp4(data)
    raise ProbeError("unrecognised container (not PNG, JPEG, ISO-BMFF, GIF or WEBP)")


# ── PNG ──────────────────────────────────────────────────────────────────────

def probe_png(data: bytes) -> ArtifactInfo:
    if len(data) < 33 or data[12:16] != b"IHDR":
        raise ProbeError("PNG: truncated or IHDR not the first chunk")
    width, height = struct.unpack(">II", data[16:24])
    if not width or not height:
        raise ProbeError("PNG: zero dimension in IHDR")
    return ArtifactInfo("image", "png", width, height,
                        notes=(f"bit depth {data[24]}, colour type {data[25]}",))


# ── JPEG ─────────────────────────────────────────────────────────────────────

def probe_jpeg(data: bytes) -> ArtifactInfo:
    pos = 2
    n = len(data)
    while True:
        if pos + 2 > n:
            raise ProbeError("JPEG: truncated before any SOF marker")
        if data[pos] != 0xFF:
            raise ProbeError(f"JPEG: expected a marker at byte {pos}")
        while pos + 1 < n and data[pos + 1] == 0xFF:   # fill bytes
            pos += 1
        if pos + 2 > n:
            raise ProbeError("JPEG: truncated before any SOF marker")
        marker = data[pos + 1]
        if marker in STANDALONE_MARKERS:
            pos += 2
            continue
        if marker == 0xD9:
            raise ProbeError("JPEG: EOI reached without a SOF marker")
        if marker == 0xDA:
            raise ProbeError("JPEG: SOS reached without a SOF marker")
        if pos + 4 > n:
            raise ProbeError("JPEG: truncated segment header")
        length = struct.unpack(">H", data[pos + 2:pos + 4])[0]
        if marker in SOF_MARKERS:
            if pos + 9 > n or length < 7:
                raise ProbeError("JPEG: truncated SOF segment")
            precision, height, width, components = struct.unpack(">BHHB", data[pos + 4:pos + 10])
            if not width or not height:
                raise ProbeError("JPEG: zero dimension in SOF")
            return ArtifactInfo("image", "jpeg", width, height,
                                notes=(f"SOF{marker - 0xC0}, {precision}-bit, {components} "
                                       "components; EXIF orientation not applied",))
        pos += 2 + length


# ── ISO-BMFF ─────────────────────────────────────────────────────────────────

def _boxes(data: bytes, start: int, end: int):
    """Yield (kind, payload_start, payload_end) for the boxes in data[start:end]."""
    pos = start
    while pos + 8 <= end:
        size, kind = struct.unpack(">I4s", data[pos:pos + 8])
        header = 8
        if size == 1:
            if pos + 16 > end:
                raise ProbeError("ISO-BMFF: truncated largesize box")
            size = struct.unpack(">Q", data[pos + 8:pos + 16])[0]
            header = 16
        elif size == 0:
            size = end - pos
        if size < header or pos + size > end:
            raise ProbeError(f"ISO-BMFF: box {kind!r} runs past the data (size {size})")
        yield kind.decode("latin-1"), pos + header, pos + size
        pos += size


def _first(data: bytes, start: int, end: int, kind: str):
    for k, s, e in _boxes(data, start, end):
        if k == kind:
            return s, e
    return None


def _full_header(data: bytes, start: int):
    return data[start], start + 4


def _mvhd(data: bytes, start: int, end: int):
    version, p = _full_header(data, start)
    if version == 1:
        timescale, duration = struct.unpack(">IQ", data[p + 16:p + 28])
    else:
        timescale, duration = struct.unpack(">II", data[p + 8:p + 16])
    return timescale, duration


def _mdhd(data: bytes, start: int, end: int):
    version, p = _full_header(data, start)
    if version == 1:
        timescale, duration = struct.unpack(">IQ", data[p + 16:p + 28])
    else:
        timescale, duration = struct.unpack(">II", data[p + 8:p + 16])
    return timescale, duration


def _tkhd_rotated(data: bytes, start: int, end: int) -> bool:
    version, p = _full_header(data, start)
    # v0: creation(4) modification(4) track_id(4) reserved(4) duration(4) reserved(8)
    # layer/alt/volume/reserved(8) -> matrix at +36 after version/flags (+40 from the box
    # payload; width/height follow at +76). v1 widens the three timestamps to 8 bytes.
    matrix_at = p + (48 if version == 1 else 36)
    if matrix_at + 36 > end:
        raise ProbeError("ISO-BMFF: truncated tkhd")
    a, b, _, c, d = struct.unpack(">5i", data[matrix_at:matrix_at + 20])
    return a == 0 and d == 0 and b != 0 and c != 0


def _stsd_entry(data: bytes, start: int, end: int):
    _, p = _full_header(data, start)
    count = struct.unpack(">I", data[p:p + 4])[0]
    if not count:
        return None
    for kind, s, e in _boxes(data, p + 4, end):
        # VisualSampleEntry: reserved(6) data_reference_index(2) pre_defined(2) reserved(2)
        # pre_defined(12) width(2) height(2) — width at +24 from the entry payload.
        if e - s >= 28:
            width, height = struct.unpack(">HH", data[s + 24:s + 28])
            return kind, width, height
        return kind, None, None
    return None


def probe_mp4(data: bytes) -> ArtifactInfo:
    top = list(_boxes(data, 0, len(data)))
    kinds = [k for k, _, _ in top]
    if "ftyp" not in kinds:
        raise ProbeError("ISO-BMFF: no ftyp box")
    container = "mov" if data[8:12] == b"qt  " else "mp4"
    fragmented = "moof" in kinds
    moov = next(((s, e) for k, s, e in top if k == "moov"), None)
    if moov is None:
        if container == "mov":
            return ArtifactInfo("unknown", "mov", notes=("unsupported container: mov without moov",))
        raise ProbeError("ISO-BMFF: no moov box (truncated or not a finished file)")
    ms, me = moov
    notes = []
    mv = _first(data, ms, me, "mvhd")
    if mv is None:
        raise ProbeError("ISO-BMFF: moov without mvhd")
    timescale, duration = _mvhd(data, *mv)
    duration_s = None
    if timescale and duration:
        duration_s = duration / timescale
    elif fragmented:
        notes.append("fragmented (moof present, mvhd duration 0): duration unavailable")
    else:
        notes.append("mvhd duration 0: duration unavailable")

    info = ArtifactInfo("video", container, duration_s=duration_s)
    for k, ts, te in _boxes(data, ms, me):
        if k != "trak":
            continue
        mdia = _first(data, ts, te, "mdia")
        if mdia is None:
            continue
        hdlr = _first(data, *mdia, "hdlr")
        handler = data[hdlr[0] + 8:hdlr[0] + 12].decode("latin-1") if hdlr else ""
        if handler == "soun":
            info.has_audio_track = True
            continue
        if handler != "vide":
            continue
        info.has_video_track = True
        if info.width is not None:
            continue   # first video track wins
        minf = _first(data, *mdia, "minf")
        stbl = _first(data, *minf, "stbl") if minf else None
        stsd = _first(data, *stbl, "stsd") if stbl else None
        entry = _stsd_entry(data, *stsd) if stsd else None
        if entry is None or entry[1] is None:
            raise ProbeError("ISO-BMFF: video track without a readable stsd sample entry")
        codec, width, height = entry
        info.codec = codec
        if codec not in VIDEO_CODECS:
            notes.append(f"unfamiliar video sample entry {codec!r}")
        tkhd = _first(data, ts, te, "tkhd")
        if tkhd and _tkhd_rotated(data, *tkhd):
            width, height = height, width
            notes.append("tkhd matrix rotated 90°/270°: dimensions swapped")
        info.width, info.height = width, height
        mdhd = _first(data, *mdia, "mdhd")
        if mdhd and duration_s is not None:
            mts, mdur = _mdhd(data, *mdhd)
            if mts and mdur and abs(mdur / mts - duration_s) > TOLERANCES["duration_s_abs"]:
                notes.append(f"mdhd duration {mdur / mts:.2f} s differs from mvhd "
                             f"{duration_s:.2f} s")
    if not info.has_video_track:
        info.kind = "unknown" if info.has_audio_track else "video"
        notes.append("no video track")
    if info.width is None and info.has_video_track:
        raise ProbeError("ISO-BMFF: video track carries no dimensions")
    info.notes = tuple(notes)
    return info


# ── aspect comparison ────────────────────────────────────────────────────────

def aspect_matches(width: int, height: int, aspect: str, tol: float | None = None):
    """(ok, ratio, target) — absolute tolerance on the w/h ratio (TOLERANCES)."""
    try:
        a, b = (int(x) for x in str(aspect).strip().split(":"))
        target = a / b
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"malformed aspect {aspect!r}") from exc
    if not width or not height:
        raise ValueError("width and height must be positive")
    ratio = width / height
    tol = TOLERANCES["aspect_ratio_abs"] if tol is None else tol
    return round(abs(ratio - target), 6) <= tol, ratio, target
