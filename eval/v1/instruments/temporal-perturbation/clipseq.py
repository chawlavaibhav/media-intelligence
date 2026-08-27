#!/usr/bin/env python3
"""ClipSequence - the canonical, hashable representation of a video clip.

WHY THIS EXISTS
---------------
A qualification fixture has to be reproducible byte-for-byte, otherwise "the
same fixture" is not the same experiment. Compressed video is a bad unit for
that: two ffmpeg builds can encode identical pixels into different bytes, so an
mp4's hash proves nothing durable.

So the scientific identity of a clip here is NOT an mp4. It is an ordered
sequence of decoded frames plus its frame rate, stored as lossless PNGs and
fingerprinted by a content hash over the ordered per-frame hashes. That hash is
stable across machines, ffmpeg versions and operating systems.

An mp4 may be exported afterwards for evaluators that need a playable file
(see export_mp4 in build_perturbation_pack.py). The export is a convenience
artifact; the frame sequence is the truth.

FAIL-CLOSED
-----------
Every loader in this file raises ClipError rather than returning a partial or
guessed result. A clip that cannot be read is never silently skipped and never
degraded into "no defect found". Callers must surface it.

Stdlib only: no numpy, no Pillow, no OpenCV, no network. The PNG codec below is
the same stdlib-zlib approach already proven in the family-2 cv-geometry pack
and the Devanagari battery's pngraster.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import struct
import zlib

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


class ClipError(Exception):
    """Raised whenever a clip, frame or manifest cannot be read with certainty.

    This is the fail-closed signal. It is never caught and turned into a
    'clean' verdict anywhere in this package.
    """


# --------------------------------------------------------------------------
# PNG codec - 8-bit truecolour RGB only, deliberately narrow
# --------------------------------------------------------------------------
def encode_png(width: int, height: int, rgb: bytes) -> bytes:
    """Encode raw RGB24 bytes (height*width*3) into a deterministic PNG."""
    expected = width * height * 3
    if len(rgb) != expected:
        raise ClipError(f"encode_png: expected {expected} bytes, got {len(rgb)}")
    stride = width * 3
    raw = bytearray()
    for y in range(height):
        raw.append(0)                       # filter type 0 (None), always
        raw += rgb[y * stride:(y + 1) * stride]

    def chunk(tag: bytes, data: bytes) -> bytes:
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return (PNG_MAGIC
            + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


def decode_png(data: bytes) -> tuple[int, int, bytearray]:
    """Decode an 8-bit RGB PNG to (width, height, raw RGB24 bytes).

    Supports all five PNG row filters so that any conforming 8-bit RGB encoder
    can be read back, but rejects everything else (palette, greyscale, alpha,
    16-bit, interlaced). Rejection is an error, never a best-effort guess.
    """
    if not data.startswith(PNG_MAGIC):
        raise ClipError("decode_png: not a PNG (bad magic)")
    pos = len(PNG_MAGIC)
    width = height = None
    idat = bytearray()
    saw_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            raise ClipError("decode_png: truncated chunk header")
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        tag = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + length]
        if len(body) != length:
            raise ClipError("decode_png: truncated chunk body")
        (crc,) = struct.unpack(">I", data[pos + 8 + length:pos + 12 + length] or b"\0\0\0\0")
        if crc != (zlib.crc32(tag + body) & 0xFFFFFFFF):
            raise ClipError(f"decode_png: CRC mismatch in chunk {tag!r}")
        if tag == b"IHDR":
            width, height, depth, ctype, comp, filt, interlace = struct.unpack(">IIBBBBB", body)
            if (depth, ctype, comp, filt, interlace) != (8, 2, 0, 0, 0):
                raise ClipError(
                    "decode_png: only 8-bit non-interlaced truecolour RGB is accepted; "
                    f"got depth={depth} colour_type={ctype} interlace={interlace}")
        elif tag == b"IDAT":
            idat += body
        elif tag == b"IEND":
            saw_iend = True
        pos += 12 + length
    if width is None:
        raise ClipError("decode_png: no IHDR")
    if not saw_iend:
        raise ClipError("decode_png: no IEND")
    if not idat:
        raise ClipError("decode_png: no image data")
    try:
        raw = zlib.decompress(bytes(idat))
    except zlib.error as exc:
        raise ClipError(f"decode_png: corrupt zlib stream ({exc})") from exc

    stride = width * 3
    if len(raw) != height * (stride + 1):
        raise ClipError("decode_png: decompressed size does not match header")

    out = bytearray(height * stride)
    prev = bytearray(stride)
    p = 0
    for y in range(height):
        ftype = raw[p]
        p += 1
        line = bytearray(raw[p:p + stride])
        p += stride
        if ftype == 0:
            pass
        elif ftype == 1:                                   # Sub
            for i in range(3, stride):
                line[i] = (line[i] + line[i - 3]) & 0xFF
        elif ftype == 2:                                   # Up
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 0xFF
        elif ftype == 3:                                   # Average
            for i in range(stride):
                left = line[i - 3] if i >= 3 else 0
                line[i] = (line[i] + ((left + prev[i]) >> 1)) & 0xFF
        elif ftype == 4:                                   # Paeth
            for i in range(stride):
                a = line[i - 3] if i >= 3 else 0
                b = prev[i]
                c = prev[i - 3] if i >= 3 else 0
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (line[i] + pr) & 0xFF
        else:
            raise ClipError(f"decode_png: unknown row filter {ftype}")
        out[y * stride:(y + 1) * stride] = line
        prev = line
    return width, height, out


# --------------------------------------------------------------------------
# Frame and ClipSequence
# --------------------------------------------------------------------------
class ClipSequence:
    """An ordered list of RGB24 frames plus fps and identifying metadata.

    frames: list[bytearray], each exactly width*height*3 bytes.
    """

    SCHEMA = "clipseq/v1"

    def __init__(self, clip_id: str, width: int, height: int, fps: int,
                 frames: list, provenance: dict | None = None):
        if not clip_id:
            raise ClipError("ClipSequence: clip_id must be non-empty")
        if width <= 0 or height <= 0:
            raise ClipError("ClipSequence: non-positive dimensions")
        if fps <= 0:
            raise ClipError("ClipSequence: fps must be a positive integer")
        if not frames:
            raise ClipError("ClipSequence: a clip with zero frames is not a clip")
        n = width * height * 3
        for i, f in enumerate(frames):
            if len(f) != n:
                raise ClipError(f"ClipSequence: frame {i} has {len(f)} bytes, expected {n}")
        self.clip_id = clip_id
        self.width = width
        self.height = height
        self.fps = fps
        self.frames = [bytearray(f) for f in frames]
        self.provenance = dict(provenance or {})

    # -- derived facts -----------------------------------------------------
    @property
    def n_frames(self) -> int:
        return len(self.frames)

    @property
    def duration_s(self) -> float:
        return round(self.n_frames / self.fps, 6)

    def frame_hashes(self) -> list:
        return [hashlib.sha256(bytes(f)).hexdigest() for f in self.frames]

    def content_hash(self) -> str:
        """Stable identity of the pixels + geometry + frame rate.

        Deliberately excludes clip_id and provenance: two clips with identical
        pixels ARE the same material, and the pack builder relies on that to
        detect a perturbation that changed nothing.
        """
        h = hashlib.sha256()
        h.update(f"{self.SCHEMA}|{self.width}x{self.height}@{self.fps}|{self.n_frames}\n".encode())
        for fh in self.frame_hashes():
            h.update(fh.encode())
            h.update(b"\n")
        return h.hexdigest()

    def motion_load(self) -> float:
        """Mean absolute inter-frame pixel change, normalised to 0.0-1.0.

        Recorded on every clip because the frozen Capability Contract v2 makes
        motion load a REQUIRED condition for motion_action_quality: a near-static
        clip scores perfectly on smoothness, so an instrument that only ever saw
        low-motion material has not been qualified for real motion. This number
        is a recorded condition, not a gate.
        """
        if self.n_frames < 2:
            return 0.0
        total = 0
        for a, b in zip(self.frames, self.frames[1:]):
            total += sum(abs(x - y) for x, y in zip(a, b))
        return round(total / ((self.n_frames - 1) * len(self.frames[0]) * 255), 8)

    def copy(self, clip_id: str | None = None) -> "ClipSequence":
        return ClipSequence(clip_id or self.clip_id, self.width, self.height,
                            self.fps, self.frames, self.provenance)

    # -- persistence -------------------------------------------------------
    def write(self, out_dir: pathlib.Path) -> dict:
        """Write frames as PNGs plus clip.json. Returns the sidecar dict."""
        out_dir = pathlib.Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        for stale in out_dir.glob("frame-*.png"):
            stale.unlink()
        hashes = []
        for i, f in enumerate(self.frames):
            png = encode_png(self.width, self.height, bytes(f))
            (out_dir / f"frame-{i:05d}.png").write_bytes(png)
            hashes.append(hashlib.sha256(png).hexdigest())
        side = {
            "schema": self.SCHEMA,
            "clip_id": self.clip_id,
            "width": self.width,
            "height": self.height,
            "fps": self.fps,
            "n_frames": self.n_frames,
            "duration_s": self.duration_s,
            "content_hash": self.content_hash(),
            "frame_pixel_hashes": self.frame_hashes(),
            "frame_png_hashes": hashes,
            "motion_load": self.motion_load(),
            "provenance": self.provenance,
        }
        (out_dir / "clip.json").write_text(json.dumps(side, indent=2, sort_keys=True) + "\n")
        return side

    @classmethod
    def read(cls, in_dir: pathlib.Path) -> "ClipSequence":
        """Read a ClipSequence back, verifying every frame against clip.json.

        Any mismatch, missing frame, extra frame or unreadable PNG raises
        ClipError. There is no lenient mode.
        """
        in_dir = pathlib.Path(in_dir)
        side_path = in_dir / "clip.json"
        if not side_path.is_file():
            raise ClipError(f"read: no clip.json in {in_dir}")
        try:
            side = json.loads(side_path.read_text())
        except json.JSONDecodeError as exc:
            raise ClipError(f"read: clip.json is not valid JSON ({exc})") from exc
        if side.get("schema") != cls.SCHEMA:
            raise ClipError(f"read: unsupported schema {side.get('schema')!r}")
        n = side["n_frames"]
        if n <= 0:
            raise ClipError("read: clip.json declares zero frames")
        on_disk = sorted(in_dir.glob("frame-*.png"))
        if len(on_disk) != n:
            raise ClipError(f"read: {len(on_disk)} frames on disk, clip.json declares {n}")
        frames = []
        for i in range(n):
            p = in_dir / f"frame-{i:05d}.png"
            if not p.is_file():
                raise ClipError(f"read: missing frame {p.name}")
            data = p.read_bytes()
            if hashlib.sha256(data).hexdigest() != side["frame_png_hashes"][i]:
                raise ClipError(f"read: {p.name} does not match its recorded hash")
            w, h, rgb = decode_png(data)
            if (w, h) != (side["width"], side["height"]):
                raise ClipError(f"read: {p.name} geometry differs from clip.json")
            frames.append(rgb)
        clip = cls(side["clip_id"], side["width"], side["height"], side["fps"],
                   frames, side.get("provenance"))
        if clip.content_hash() != side["content_hash"]:
            raise ClipError("read: reconstructed content hash differs from clip.json")
        return clip


def pixel(frame: bytearray, width: int, x: int, y: int) -> tuple:
    i = (y * width + x) * 3
    return frame[i], frame[i + 1], frame[i + 2]


def set_pixel(frame: bytearray, width: int, x: int, y: int, rgb: tuple) -> None:
    i = (y * width + x) * 3
    frame[i], frame[i + 1], frame[i + 2] = rgb
