"""Local media decoding with the standard library and ffmpeg. No third-party Python.

    decode_png(bytes)            8-bit PNG: grey / grey+alpha / RGB / RGBA / palette, all five filter types
    encode_png(rows, w, h, ...)  the matching writer (test fixtures; filter type selectable)
    resize_nearest(img, w, h)    nearest-neighbour resample (stdlib), used before a masked diff
    ffprobe(path)                container, size, aspect, duration, fps, audio presence (JSON probe)
    decode_image_ffmpeg(path)    any image ffmpeg reads -> RGB Image (JPEG, WebP, ...)
    decode_video_frames(path)    first / middle / last frames -> RGB Images
    decode_audio_pcm(path)       16-bit mono PCM at a given rate
    make_test_video / write_wav  tiny local fixtures for the tests (never committed)

FAIL CLOSED. A file that cannot be parsed raises `ProbeError`; a missing tool raises `ToolUnavailable`.
Neither is ever turned into "0 objects" or "no audio" by this module - the caller maps them to the
absence reasons `parse_failure` / `instrument_unavailable`.

This module and `gate_wrapper.py` are the only places in eval/harness-v2 outside transports.py that
run a subprocess, and both run LOCAL tools only (ffmpeg / ffprobe / the gate script). One ffmpeg
process at a time, by construction: every call here is synchronous.
"""
from __future__ import annotations

import json
import math
import struct
import subprocess
import wave
import zlib
from array import array
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

FFMPEG_BIN = "ffmpeg"
FFPROBE_BIN = "ffprobe"
PNG_SIG = b"\x89PNG\r\n\x1a\n"
CHANNELS_BY_COLOUR_TYPE = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}


class ProbeError(RuntimeError):
    """The input could not be decoded as the declared kind of media. Never a guess."""


class ToolUnavailable(RuntimeError):
    """ffmpeg / ffprobe is not on PATH (or not runnable)."""


# ------------------------------------------------------------------------------ images
@dataclass
class Image:
    width: int
    height: int
    channels: int
    data: bytes                      # row-major, packed, 8-bit

    def rows(self) -> list[bytes]:
        stride = self.width * self.channels
        return [self.data[y * stride:(y + 1) * stride] for y in range(self.height)]

    def pixel(self, x: int, y: int) -> tuple:
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError((x, y))
        i = (y * self.width + x) * self.channels
        return tuple(self.data[i:i + self.channels])

    def to_rgb(self) -> "Image":
        if self.channels == 3:
            return self
        out = bytearray()
        d = self.data
        if self.channels == 4:
            for i in range(0, len(d), 4):
                out += d[i:i + 3]
        elif self.channels == 1:
            for v in d:
                out += bytes((v, v, v))
        elif self.channels == 2:
            for i in range(0, len(d), 2):
                v = d[i]
                out += bytes((v, v, v))
        else:
            raise ProbeError(f"cannot convert {self.channels}-channel image to RGB")
        return Image(self.width, self.height, 3, bytes(out))

    def to_grey(self) -> "Image":
        """ITU-R BT.601 luma (0.299 R + 0.587 G + 0.114 B), rounded to 8 bits."""
        if self.channels == 1:
            return self
        if self.channels == 2:
            return Image(self.width, self.height, 1, bytes(self.data[0::2]))
        rgb = self.to_rgb().data
        out = bytearray(self.width * self.height)
        for i in range(self.width * self.height):
            r, g, b = rgb[3 * i], rgb[3 * i + 1], rgb[3 * i + 2]
            out[i] = int(0.299 * r + 0.587 * g + 0.114 * b + 0.5)
        return Image(self.width, self.height, 1, bytes(out))


def _paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    if pb <= pc:
        return b
    return c


def _unfilter(ftype: int, cur: bytearray, prev: bytes, bpp: int) -> None:
    n = len(cur)
    if ftype == 0:
        return
    if ftype == 1:                                   # Sub
        for i in range(bpp, n):
            cur[i] = (cur[i] + cur[i - bpp]) & 0xFF
    elif ftype == 2:                                 # Up
        for i in range(n):
            cur[i] = (cur[i] + prev[i]) & 0xFF
    elif ftype == 3:                                 # Average
        for i in range(n):
            a = cur[i - bpp] if i >= bpp else 0
            cur[i] = (cur[i] + ((a + prev[i]) >> 1)) & 0xFF
    elif ftype == 4:                                 # Paeth
        for i in range(n):
            a = cur[i - bpp] if i >= bpp else 0
            c = prev[i - bpp] if i >= bpp else 0
            cur[i] = (cur[i] + _paeth(a, prev[i], c)) & 0xFF
    else:
        raise ProbeError(f"PNG filter type {ftype} is not defined")


def _filter(ftype: int, raw: bytes, prev: bytes, bpp: int) -> bytes:
    n = len(raw)
    out = bytearray(n)
    for i in range(n):
        a = raw[i - bpp] if i >= bpp else 0
        b = prev[i]
        c = prev[i - bpp] if i >= bpp else 0
        if ftype == 0:
            pred = 0
        elif ftype == 1:
            pred = a
        elif ftype == 2:
            pred = b
        elif ftype == 3:
            pred = (a + b) >> 1
        elif ftype == 4:
            pred = _paeth(a, b, c)
        else:
            raise ValueError(ftype)
        out[i] = (raw[i] - pred) & 0xFF
    return bytes(out)


def decode_png(data: bytes) -> Image:
    """Decode an 8-bit, non-interlaced PNG. Anything else raises ProbeError (fail closed)."""
    if not isinstance(data, (bytes, bytearray)) or len(data) < 8 or bytes(data[:8]) != PNG_SIG:
        raise ProbeError("not a PNG (signature mismatch or too short)")
    pos = 8
    ihdr = None
    palette = None
    idat = bytearray()
    seen_iend = False
    while pos + 8 <= len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        tag = bytes(data[pos + 4:pos + 8])
        body = bytes(data[pos + 8:pos + 8 + length])
        if len(body) != length or pos + 12 + length > len(data):
            raise ProbeError(f"PNG chunk {tag!r} is truncated")
        crc = struct.unpack(">I", data[pos + 8 + length:pos + 12 + length])[0]
        if (zlib.crc32(tag + body) & 0xFFFFFFFF) != crc:
            raise ProbeError(f"PNG chunk {tag!r} fails its CRC")
        pos += 12 + length
        if tag == b"IHDR":
            if length != 13:
                raise ProbeError("PNG IHDR has the wrong length")
            ihdr = struct.unpack(">IIBBBBB", body)
        elif tag == b"PLTE":
            palette = body
        elif tag == b"IDAT":
            idat += body
        elif tag == b"IEND":
            seen_iend = True
            break
    if ihdr is None or not seen_iend or not idat:
        raise ProbeError("PNG is missing IHDR, IDAT or IEND")
    w, h, depth, ctype, comp, filt, interlace = ihdr
    if depth != 8:
        raise ProbeError(f"PNG bit depth {depth} is not supported (8-bit only); refusing to guess")
    if ctype not in CHANNELS_BY_COLOUR_TYPE:
        raise ProbeError(f"PNG colour type {ctype} is not supported")
    if comp != 0 or filt != 0:
        raise ProbeError("PNG compression/filter method is not the standard one")
    if interlace != 0:
        raise ProbeError("interlaced PNG is not supported; refusing to guess")
    if w <= 0 or h <= 0 or w * h > 50_000_000:
        raise ProbeError(f"PNG dimensions {w}x{h} are not usable")
    channels = CHANNELS_BY_COLOUR_TYPE[ctype]
    if ctype == 3 and (palette is None or len(palette) % 3):
        raise ProbeError("palette PNG without a valid PLTE chunk")
    try:
        raw = zlib.decompress(bytes(idat))
    except zlib.error as exc:
        raise ProbeError(f"PNG image data is not a valid zlib stream: {exc}") from None
    stride = w * channels
    if len(raw) != h * (stride + 1):
        raise ProbeError(f"PNG image data has {len(raw)} bytes, expected {h * (stride + 1)}")
    out = bytearray()
    prev = bytes(stride)
    for y in range(h):
        start = y * (stride + 1)
        ftype = raw[start]
        cur = bytearray(raw[start + 1:start + 1 + stride])
        _unfilter(ftype, cur, prev, channels)
        out += cur
        prev = bytes(cur)
    if ctype == 3:
        rgb = bytearray()
        npal = len(palette) // 3
        for idx in out:
            if idx >= npal:
                raise ProbeError("palette index out of range")
            rgb += palette[3 * idx:3 * idx + 3]
        return Image(w, h, 3, bytes(rgb))
    return Image(w, h, channels, bytes(out))


def encode_png(rows: list[bytes], width: int, height: int, channels: int = 3, filter_type: int = 0,
               palette: bytes | None = None) -> bytes:
    """Write an 8-bit PNG. `filter_type` 0..4 is applied to every row (tests exercise all five)."""
    if len(rows) != height or any(len(r) != width * channels for r in rows):
        raise ValueError("rows do not match width x channels x height")
    if palette is not None:
        if channels != 1:
            raise ValueError("a palette PNG takes one index channel")
        ctype = 3
    else:
        ctype = {1: 0, 2: 4, 3: 2, 4: 6}[channels]
    raw = bytearray()
    prev = bytes(width * channels)
    for r in rows:
        raw.append(filter_type)
        raw += _filter(filter_type, r, prev, channels) if filter_type else r
        prev = r

    def chunk(tag: bytes, body: bytes) -> bytes:
        return struct.pack(">I", len(body)) + tag + body + struct.pack(">I", zlib.crc32(tag + body) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", width, height, 8, ctype, 0, 0, 0)
    png = PNG_SIG + chunk(b"IHDR", ihdr)
    if palette is not None:
        png += chunk(b"PLTE", palette)
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 6)) + chunk(b"IEND", b"")
    return png


def image_from_rows(rows: list[bytes], width: int, height: int, channels: int = 3) -> Image:
    return Image(width, height, channels, b"".join(rows))


def resize_nearest(img: Image, width: int, height: int) -> Image:
    if width <= 0 or height <= 0:
        raise ValueError("target size must be positive")
    if (width, height) == (img.width, img.height):
        return img
    c = img.channels
    src = img.data
    out = bytearray()
    for y in range(height):
        sy = (y * img.height) // height
        row_off = sy * img.width * c
        for x in range(width):
            sx = (x * img.width) // width
            i = row_off + sx * c
            out += src[i:i + c]
    return Image(width, height, c, bytes(out))


# ------------------------------------------------------------------------------ ffmpeg
@dataclass
class PCM:
    rate: int
    samples: list                    # 16-bit signed ints, mono


def _run(cmd: list[str], timeout_s: float = 120.0) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(cmd, capture_output=True, timeout=timeout_s)
    except FileNotFoundError as exc:
        raise ToolUnavailable(f"{cmd[0]} is not on PATH: {exc}") from None
    except subprocess.TimeoutExpired as exc:
        raise ProbeError(f"{cmd[0]} timed out after {timeout_s}s") from exc


def tools() -> dict:
    """Availability and version line of ffmpeg / ffprobe. Records, never installs."""
    out = {}
    for name, binary in (("ffmpeg", FFMPEG_BIN), ("ffprobe", FFPROBE_BIN)):
        try:
            r = _run([binary, "-version"], timeout_s=20)
            line = (r.stdout or b"").decode("utf-8", "replace").splitlines()
            out[name] = {"available": r.returncode == 0, "version": (line[0] if line else ""), "binary": binary}
        except ToolUnavailable as exc:
            out[name] = {"available": False, "version": None, "binary": binary, "reason": str(exc)}
    return out


def _require(binary: str, name: str) -> None:
    t = tools()[name]
    if not t["available"]:
        raise ToolUnavailable(t.get("reason") or f"{name} is not available")


def ffprobe(path: Path | str) -> dict:
    """`ffprobe -print_format json -show_format -show_streams`, reduced to the facts the probe needs."""
    _require(FFPROBE_BIN, "ffprobe")
    path = Path(path)
    if not path.exists() or path.stat().st_size == 0:
        raise ProbeError(f"{path} does not exist or is empty")
    r = _run([FFPROBE_BIN, "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)])
    if r.returncode != 0:
        raise ProbeError(f"ffprobe could not parse {path.name}: {(r.stderr or b'').decode('utf-8', 'replace')[:200]}")
    try:
        doc = json.loads(r.stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProbeError(f"ffprobe output for {path.name} is not JSON: {exc}") from None
    streams = doc.get("streams") or []
    fmt = doc.get("format") or {}
    if not streams:
        raise ProbeError(f"ffprobe found no streams in {path.name}")
    video = [s for s in streams if s.get("codec_type") == "video"]
    audio = [s for s in streams if s.get("codec_type") == "audio"]
    v0 = video[0] if video else {}
    width, height = v0.get("width"), v0.get("height")
    fps = None
    if v0.get("r_frame_rate"):
        try:
            fps = float(Fraction(v0["r_frame_rate"]))
        except (ValueError, ZeroDivisionError):
            fps = None
    duration = None
    for cand in (fmt.get("duration"), v0.get("duration"), (audio[0].get("duration") if audio else None)):
        try:
            if cand is not None:
                duration = float(cand)
                break
        except ValueError:
            continue
    aspect = None
    if width and height:
        g = math.gcd(int(width), int(height))
        aspect = f"{int(width) // g}:{int(height) // g}"
    return {
        "container": fmt.get("format_name"), "width": width, "height": height, "aspect": aspect,
        "aspect_float": (float(width) / float(height) if width and height else None),
        "duration_s": duration, "fps": fps, "has_video": bool(video), "has_audio": bool(audio),
        "video_codec": v0.get("codec_name"), "audio_codec": (audio[0].get("codec_name") if audio else None),
        "nb_frames": v0.get("nb_frames"), "n_video_streams": len(video), "n_audio_streams": len(audio),
        "pix_fmt": v0.get("pix_fmt"), "size_bytes": int(fmt.get("size") or path.stat().st_size),
    }


def _rawvideo(cmd_in: list[str], width: int, height: int) -> Image:
    r = _run([FFMPEG_BIN, "-v", "error", *cmd_in, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"])
    if r.returncode != 0 or len(r.stdout) < width * height * 3:
        raise ProbeError(f"ffmpeg produced no frame ({(r.stderr or b'').decode('utf-8', 'replace')[:200]})")
    return Image(width, height, 3, bytes(r.stdout[:width * height * 3]))


def decode_image_ffmpeg(path: Path | str) -> Image:
    info = ffprobe(path)
    if not info["width"] or not info["height"]:
        raise ProbeError(f"{Path(path).name} has no decodable picture")
    return _rawvideo(["-i", str(path), "-frames:v", "1"], int(info["width"]), int(info["height"]))


def decode_video_frames(path: Path | str, which=("first", "middle", "last")) -> list[Image]:
    info = ffprobe(path)
    if not info["has_video"] or not info["width"]:
        raise ProbeError(f"{Path(path).name} has no video stream")
    w, h = int(info["width"]), int(info["height"])
    dur = info["duration_s"] or 0.0
    fps = info["fps"] or 25.0
    times = {"first": 0.0, "middle": max(dur / 2.0, 0.0), "last": max(dur - 1.5 / fps, 0.0)}
    out = []
    for name in which:
        if name not in times:
            raise ValueError(name)
        t = times[name]
        cmd = (["-ss", f"{t:.3f}", "-i", str(path), "-frames:v", "1"] if t > 0 else ["-i", str(path), "-frames:v", "1"])
        out.append(_rawvideo(cmd, w, h))
    return out


def decode_audio_pcm(path: Path | str, rate: int = 16000) -> PCM:
    _require(FFMPEG_BIN, "ffmpeg")
    path = Path(path)
    if not path.exists() or path.stat().st_size == 0:
        raise ProbeError(f"{path} does not exist or is empty")
    r = _run([FFMPEG_BIN, "-v", "error", "-i", str(path), "-vn", "-f", "s16le", "-ac", "1", "-ar", str(rate), "-"])
    if r.returncode != 0 or len(r.stdout) < 2:
        raise ProbeError(f"ffmpeg could not decode audio from {path.name}: {(r.stderr or b'').decode('utf-8', 'replace')[:200]}")
    a = array("h")
    a.frombytes(r.stdout[: len(r.stdout) // 2 * 2])
    return PCM(rate, list(a))


# ------------------------------------------------------------------------------ fixtures
def write_wav(path: Path | str, samples: list, rate: int = 16000) -> Path:
    path = Path(path)
    a = array("h", [max(-32768, min(32767, int(s))) for s in samples])
    with wave.open(str(path), "wb") as fh:
        fh.setnchannels(1)
        fh.setsampwidth(2)
        fh.setframerate(rate)
        fh.writeframes(a.tobytes())
    return path


def make_test_audio(path: Path | str, seconds: float = 0.5, rate: int = 16000, freq: float = 440.0, amp: int = 12000) -> Path:
    n = int(seconds * rate)
    return write_wav(path, [amp * math.sin(2 * math.pi * freq * i / rate) for i in range(n)], rate)


def make_test_video(path: Path | str, width: int = 64, height: int = 48, seconds: float = 1.0, fps: int = 10,
                    with_audio: bool = True, audio_path: Path | str | None = None, audio_codec: str = "aac") -> Path:
    """A tiny synthetic clip (lavfi testsrc, mpeg4 in mp4; optional sine or a supplied audio file)."""
    _require(FFMPEG_BIN, "ffmpeg")
    path = Path(path)
    cmd = [FFMPEG_BIN, "-y", "-v", "error", "-f", "lavfi", "-i", f"testsrc=size={width}x{height}:rate={fps}"]
    if audio_path is not None:
        cmd += ["-i", str(audio_path)]
    elif with_audio:
        cmd += ["-f", "lavfi", "-i", "sine=frequency=440:sample_rate=16000"]
    cmd += ["-t", f"{seconds}", "-c:v", "mpeg4", "-q:v", "6", "-pix_fmt", "yuv420p"]
    if with_audio or audio_path is not None:
        cmd += ["-c:a", audio_codec, "-ar", "16000", "-ac", "1"]
    else:
        cmd += ["-an"]
    cmd += ["-shortest", str(path)]
    r = _run(cmd)
    if r.returncode != 0 or not path.exists():
        raise ProbeError(f"could not build the test clip: {(r.stderr or b'').decode('utf-8', 'replace')[:300]}")
    return path
