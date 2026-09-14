"""Synthetic artifacts for the USD-0 tranche: bytes the post-draw gate can probe, drawn by no model.

WHY. The post-draw gate needs an artifact; the dry profile sends nothing, so nothing comes back.
To prove the CHAIN (gate -> repair -> acceptance -> memory) runs end to end without spending, the
driver hands the gate a small valid PNG (or a header-only MP4 stub) of the declared aspect. These
bytes prove plumbing and measure nothing about any model — the same status the gate's
ScriptedDetector has ("human-observed truth keyed by sha256 — proves plumbing, measures nothing").

PNG: a real file — signature, IHDR, one IDAT of zlib-compressed filtered rows, IEND, CRCs — built
with `struct` and `zlib` only (no PIL in this environment). The flat colour is derived from `seed`
so two draws of the same aspect have different sha256s; the scripted detector fixtures under
runtime/fixtures/synthetic/ are keyed on those digests.

MP4: header-only. canon.gate.artifact.probe_mp4 reads ftyp, moov/mvhd (duration), trak/mdia/hdlr
('vide'), and the stsd VisualSampleEntry (width, height). This stub carries exactly those boxes and
no mdat, so the gate's geometry/duration/track rows run over it; it is NOT a playable file and is
never presented as one. Frames cannot be decoded from it (nor from a real MP4, in stdlib); the dry
chain therefore hands the gate synthetic "sampled frames" (`frames_for_spec`) so the frame-level text
scan runs — a video with no sampled frames is NOT-RUN at the gate, never PASS (frame_hygiene).
"""
from __future__ import annotations

import math
import struct
import zlib

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MIN_SIDE = 64


def _chunk(kind: bytes, payload: bytes) -> bytes:
    crc = zlib.crc32(kind + payload) & 0xFFFFFFFF
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", crc)


def make_png(width: int, height: int, *, seed: int = 1) -> bytes:
    if width <= 0 or height <= 0:
        raise ValueError("PNG dimensions must be positive")
    r, g, b = (seed * 53) % 256, (seed * 97) % 256, (seed * 193) % 256
    row = b"\x00" + bytes((r, g, b)) * width          # filter type 0, RGB
    raw = row * height
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)  # 8-bit RGB
    return (PNG_SIGNATURE + _chunk(b"IHDR", ihdr) + _chunk(b"IDAT", zlib.compress(raw, 9))
            + _chunk(b"IEND", b""))


def png_crc_ok(data: bytes) -> bool:
    """Every chunk's CRC matches — the file is a real PNG, not just a plausible header."""
    if data[:8] != PNG_SIGNATURE:
        return False
    pos = 8
    while pos + 12 <= len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        kind = data[pos + 4:pos + 8]
        payload = data[pos + 8:pos + 8 + length]
        crc = struct.unpack(">I", data[pos + 8 + length:pos + 12 + length])[0]
        if zlib.crc32(kind + payload) & 0xFFFFFFFF != crc:
            return False
        pos += 12 + length
        if kind == b"IEND":
            return pos == len(data)
    return False


def dimensions_for_aspect(aspect: str, min_side: int = MIN_SIDE) -> tuple:
    a, b = (int(x) for x in str(aspect).strip().split(":"))
    if a <= 0 or b <= 0:
        raise ValueError(f"aspect {aspect!r} is not W:H")
    k = math.ceil(min_side / min(a, b))
    return a * k, b * k


def png_for_aspect(aspect: str, *, seed: int = 1) -> bytes:
    w, h = dimensions_for_aspect(aspect)
    return make_png(w, h, seed=seed)


# ── ISO-BMFF stub ─────────────────────────────────────────────────────────────

def _box(kind: bytes, payload: bytes) -> bytes:
    return struct.pack(">I", 8 + len(payload)) + kind + payload


def _fullbox(kind: bytes, payload: bytes, version: int = 0) -> bytes:
    return _box(kind, bytes((version, 0, 0, 0)) + payload)


_UNITY_MATRIX = struct.pack(">9i", 0x00010000, 0, 0, 0, 0x00010000, 0, 0, 0, 0x40000000)


def make_mp4_stub(width: int, height: int, *, duration_s: float, timescale: int = 1000) -> bytes:
    duration = int(round(duration_s * timescale))
    ftyp = _box(b"ftyp", b"isom" + struct.pack(">I", 0x200) + b"isom" + b"iso2" + b"avc1" + b"mp41")
    mvhd = _fullbox(b"mvhd", struct.pack(">IIII", 0, 0, timescale, duration)
                    + struct.pack(">Ih", 0x00010000, 0x0100) + b"\x00" * 10 + _UNITY_MATRIX
                    + b"\x00" * 24 + struct.pack(">I", 2))
    tkhd = _fullbox(b"tkhd", struct.pack(">IIIII", 0, 0, 1, 0, duration) + b"\x00" * 8
                    + struct.pack(">hhhh", 0, 0, 0, 0) + _UNITY_MATRIX
                    + struct.pack(">II", width << 16, height << 16))
    mdhd = _fullbox(b"mdhd", struct.pack(">IIII", 0, 0, timescale, duration) + struct.pack(">HH", 0x55C4, 0))
    hdlr = _fullbox(b"hdlr", struct.pack(">I", 0) + b"vide" + b"\x00" * 12 + b"VideoHandler\x00")
    # VisualSampleEntry (78 bytes): reserved(6) dri(2) pre(2) res(2) pre(12) w(2) h(2) hres(4)
    # vres(4) res(4) frame_count(2) compressorname(32) depth(2) pre_defined(2)
    entry = (b"\x00" * 6 + struct.pack(">H", 1) + b"\x00" * 16 + struct.pack(">HH", width, height)
             + struct.pack(">IIIH", 0x00480000, 0x00480000, 0, 1) + b"\x00" * 32
             + struct.pack(">Hh", 0x0018, -1))
    stsd = _fullbox(b"stsd", struct.pack(">I", 1) + _box(b"avc1", entry))
    stbl = _box(b"stbl", stsd)
    minf = _box(b"minf", stbl)
    mdia = _box(b"mdia", mdhd + hdlr + minf)
    trak = _box(b"trak", tkhd + mdia)
    moov = _box(b"moov", mvhd + trak)
    return ftyp + moov


SYNTHETIC_FRAMES_PER_VIDEO = 3


def frames_for_spec(spec: dict, *, seed: int = 1, count: int = SYNTHETIC_FRAMES_PER_VIDEO) -> list:
    """Synthetic 'sampled frames' for a dry video attempt: `count` flat PNGs of the declared aspect with
    distinct digests per (seed, k). They stand in for frames a live run would sample from the returned
    clip (runtime/loop/frame_hygiene), so the dry chain exercises the frame-level text scan instead of
    passing a video nobody looked at. They prove plumbing and measure nothing — same status as the stub."""
    aspect = spec["deliverable"]["aspect"]
    return [png_for_aspect(aspect, seed=1000 * int(seed) + k) for k in range(1, int(count) + 1)]


def mp4_for_spec(spec: dict, *, seed: int = 1) -> bytes:
    """A stub of the spec's declared aspect and motion duration. `seed` widens the stub by one
    trailing free box so successive draws have distinct digests without changing geometry."""
    deliverable = spec["deliverable"]
    w, h = dimensions_for_aspect(deliverable["aspect"])
    seconds = float((deliverable.get("motion") or {}).get("seconds") or 0)
    return make_mp4_stub(w, h, duration_s=seconds) + _box(b"free", struct.pack(">I", seed))
