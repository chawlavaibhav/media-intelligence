#!/usr/bin/env python3
"""
Decode a PNG to a canonical RGBA8 raster, so visual equivalence is judged on PIXELS.

WHY THIS EXISTS  (Controller review, second pass)
    The battery's visibility gate previously compared the SHA-256 of the **encoded PNG file**. That
    is too strong a test. PNG is a container: the same picture can be written as many different byte
    streams — a different zlib compression level, a different IDAT chunk split, an extra ancillary
    chunk — and every one of them has a different file hash while decoding to identical pixels.

    Using the file hash therefore risks the exact error the gate exists to prevent, only inverted:
    it would call two visually identical images "different", admit the pair as a test item, and then
    mark a checker WRONG for correctly reporting that the two pictures look the same.

    Two hashes are now kept, and they answer different questions:

        file_sha256(path)         encoded artifact identity — did this exact FILE change?
        pixel_fingerprint(path)   visible pixel identity    — does this PICTURE look different?

    `devtext.is_valid_mismatch()` decides `raster_identical` on the pixel fingerprint. The file hash
    is retained for artifact integrity: it is what a checker run should record to prove it read the
    bytes we shipped.

WHY A DECODER RATHER THAN A LIBRARY
    Neither Pillow nor numpy is present on this machine, and pulling in an image library to answer
    "are these two rasters equal" would add a substantial dependency to a battery whose whole point
    is being reproducible from pinned local tooling. PNG decoding is fully specified and the parts
    we need are small: parse chunks, inflate with `zlib` (stdlib), reverse the per-scanline filters,
    expand to RGBA8.

    This is NOT a general-purpose PNG library and must not become one. It decodes exactly the
    narrow contract below and **rejects everything else** rather than returning a guess. A wrong
    raster here would silently corrupt every visibility decision the battery makes, with no visible
    symptom — the exact failure mode the battery exists to catch, one level down.

THE SUPPORTED CONTRACT — narrow, explicit, and fail-closed
    Accepted:
      * non-interlaced only;
      * bit depths 1, 2, 4, 8 — and only in the combinations the PNG spec permits per colour type;
      * colour types 0 (grayscale), 2 (truecolour), 3 (indexed), 4 (gray+alpha), 6 (RGBA);
      * `tRNS` for **indexed images only**, where it is faithfully applied per-index;
      * ancillary chunks that cannot change a decoded raster in any accepted combination — see
        `_IGNORE_CHUNKS`. `hb-view` emits `bKGD`, which is a *suggested* compositing background and
        is advisory only: with `tRNS` rejected on grayscale and truecolour, no accepted image has
        transparency for it to composite against, so it cannot alter a pixel.

    Rejected with `UnsupportedPNG`:
      * interlaced images;
      * **bit depth 16** — the sample unpacking here keeps the high byte only, so two 16-bit images
        differing in their low bytes would fingerprint identically. That is exactly the silent
        collision this module exists to prevent, so 16-bit is refused rather than truncated;
      * colour-type / bit-depth combinations the spec does not allow;
      * **`tRNS` on grayscale or truecolour** — it makes one sample value fully transparent and
        materially changes the RGBA raster. It is not implemented, so a file carrying it is refused
        rather than fingerprinted as though transparency did not exist;
      * `tRNS` on colour types 4 or 6, where the spec forbids it — its presence means the file is
        not what its header claims;
      * chunks that change how an image is meant to look and that this decoder does not implement:
        `gAMA`, `sRGB`, `iCCP`, `cHRM` (colour management) and `acTL` (APNG animation, where
        decoding only the default image would silently drop the rest);
      * any unrecognised **critical** chunk. Unrecognised *ancillary* chunks are skipped, which is
        what the PNG specification's ancillary bit exists to permit.

    The battery's own images sit well inside this: `hb-view` emits 8-bit grayscale, non-interlaced,
    with `bKGD` and no `tRNS`.

No network, no model, no spend.
"""
from __future__ import annotations

import hashlib
import struct
import zlib
from dataclasses import dataclass
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

# Channels per pixel, by PNG colour type.
_CHANNELS = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}

# Bit depths this decoder implements faithfully. 16 is deliberately absent: see the module
# docstring — truncating to the high byte would let two different images collide.
_SUPPORTED_BIT_DEPTHS = (1, 2, 4, 8)

# Bit depths the PNG specification permits per colour type. Checked so an illegal combination is
# refused rather than decoded into something plausible.
_LEGAL_BIT_DEPTHS = {0: (1, 2, 4, 8, 16), 2: (8, 16), 3: (1, 2, 4, 8),
                     4: (8, 16), 6: (8, 16)}

# Chunks that change how an image is meant to look and that this decoder does not implement.
# Ignoring any of these would mean fingerprinting a raster that is not what the file describes.
_REJECT_CHUNKS = {
    b"gAMA": "gamma correction",
    b"sRGB": "sRGB colour space rendering intent",
    b"iCCP": "embedded ICC colour profile",
    b"cHRM": "chromaticity / white point",
    b"acTL": "APNG animation (decoding only the default image would drop frames silently)",
}

# Ancillary chunks that cannot change a decoded raster under the supported contract, and are
# therefore skipped deliberately rather than by omission.
_IGNORE_CHUNKS = {
    b"bKGD",   # suggested compositing background; advisory, and no accepted image has alpha to
               # composite (tRNS is rejected on grayscale/truecolour). hb-view emits this one.
    b"pHYs",   # physical pixel size; the fingerprint already carries pixel dimensions
    b"sBIT",   # significant-bits hint; advisory
    b"tEXt", b"zTXt", b"iTXt", b"tIME",   # metadata; cannot touch pixels
    b"hIST", b"sPLT",                     # palette hints for quantising displays; advisory
}


class UnsupportedPNG(RuntimeError):
    """Raised for any PNG feature this decoder does not fully implement.

    Deliberately fatal. Returning an approximate raster would corrupt the visibility gate without
    any visible symptom.
    """


@dataclass(frozen=True)
class Raster:
    """A decoded image in one canonical form: 8 bits per channel, RGBA, top-to-bottom."""
    width: int
    height: int
    rgba: bytes          # width * height * 4 bytes

    @property
    def pixel_format(self) -> str:
        return "RGBA8"

    def fingerprint(self) -> str:
        """SHA-256 over dimensions, format and pixel data.

        Dimensions and format are hashed **with** the pixels, not assumed: two rasters with the same
        byte payload but different shapes are different pictures, and must not collide.
        """
        h = hashlib.sha256()
        h.update(f"{self.pixel_format}:{self.width}x{self.height}:".encode("ascii"))
        h.update(self.rgba)
        return h.hexdigest()


def _is_critical(ctype: bytes) -> bool:
    """PNG's critical/ancillary bit: an uppercase first letter means the chunk is critical.

    A decoder may safely skip an ancillary chunk it does not recognise — that is what the bit is
    for. It may not skip an unrecognised critical one, so we refuse instead.
    """
    return not (ctype[0] & 0x20)


def _iter_chunks(data: bytes):
    if data[:8] != PNG_SIGNATURE:
        raise UnsupportedPNG("not a PNG file: signature mismatch")
    pos = 8
    while pos + 8 <= len(data):
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + length]
        if len(body) != length:
            raise UnsupportedPNG("truncated PNG chunk")
        yield ctype, body
        pos += 12 + length          # length + type + data + crc


def _paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    return b if pb <= pc else c


def _unfilter(raw: bytes, height: int, stride: int, bpp: int) -> bytearray:
    """Reverse the per-scanline filters. Each scanline is prefixed by one filter-type byte."""
    out = bytearray(height * stride)
    pos = 0
    for y in range(height):
        ftype = raw[pos]
        pos += 1
        line = bytearray(raw[pos:pos + stride])
        pos += stride
        base = y * stride
        prev = base - stride
        if ftype == 0:
            pass
        elif ftype == 1:                                   # Sub
            for i in range(bpp, stride):
                line[i] = (line[i] + line[i - bpp]) & 0xFF
        elif ftype == 2:                                   # Up
            if y:
                for i in range(stride):
                    line[i] = (line[i] + out[prev + i]) & 0xFF
        elif ftype == 3:                                   # Average
            for i in range(stride):
                a = line[i - bpp] if i >= bpp else 0
                b = out[prev + i] if y else 0
                line[i] = (line[i] + ((a + b) >> 1)) & 0xFF
        elif ftype == 4:                                   # Paeth
            for i in range(stride):
                a = line[i - bpp] if i >= bpp else 0
                b = out[prev + i] if y else 0
                c = out[prev + i - bpp] if (y and i >= bpp) else 0
                line[i] = (line[i] + _paeth(a, b, c)) & 0xFF
        else:
            raise UnsupportedPNG(f"unknown PNG filter type {ftype}")
        out[base:base + stride] = line
    return out


def _unpack_samples(row: bytes, bit_depth: int, count: int) -> list[int]:
    """Expand sub-byte or 16-bit samples to a flat list of integers, one per sample."""
    if bit_depth == 8:
        return list(row[:count])
    if bit_depth in (1, 2, 4):
        per_byte = 8 // bit_depth
        mask = (1 << bit_depth) - 1
        out = []
        for i in range(count):
            byte = row[i // per_byte]
            shift = 8 - bit_depth * (i % per_byte + 1)
            out.append((byte >> shift) & mask)
        return out
    raise UnsupportedPNG(f"unsupported bit depth {bit_depth}")


def decode(path: Path | str) -> Raster:
    """Decode a PNG file to a canonical RGBA8 `Raster`."""
    data = Path(path).read_bytes()
    ihdr = None
    palette = b""
    trns = None
    idat = bytearray()
    for ctype, body in _iter_chunks(data):
        if ctype in _REJECT_CHUNKS:
            raise UnsupportedPNG(
                f"PNG carries a {ctype.decode('ascii', 'replace')} chunk "
                f"({_REJECT_CHUNKS[ctype]}), which this decoder does not implement. "
                f"Refusing rather than fingerprinting a raster that is not what the file describes.")
        if ctype == b"IHDR":
            ihdr = struct.unpack(">IIBBBBB", body[:13])
        elif ctype == b"PLTE":
            palette = body
        elif ctype == b"tRNS":
            trns = body
        elif ctype == b"IDAT":
            idat += body
        elif ctype == b"IEND":
            break
        elif ctype in _IGNORE_CHUNKS:
            continue
        elif _is_critical(ctype):
            raise UnsupportedPNG(
                f"unrecognised CRITICAL PNG chunk {ctype.decode('ascii', 'replace')}; "
                f"refusing rather than decoding an image we may not understand")
        # else: an unrecognised ancillary chunk, which the spec allows a decoder to skip.

    if ihdr is None:
        raise UnsupportedPNG("PNG has no IHDR chunk")

    width, height, bit_depth, colour, compression, filt, interlace = ihdr
    if compression != 0 or filt != 0:
        raise UnsupportedPNG("non-standard PNG compression or filter method")
    if interlace != 0:
        raise UnsupportedPNG("interlaced PNG is not supported by this decoder")
    if colour not in _CHANNELS:
        raise UnsupportedPNG(f"unsupported PNG colour type {colour}")
    if bit_depth not in _LEGAL_BIT_DEPTHS[colour]:
        raise UnsupportedPNG(
            f"bit depth {bit_depth} is not legal for PNG colour type {colour}")
    if bit_depth not in _SUPPORTED_BIT_DEPTHS:
        raise UnsupportedPNG(
            f"bit depth {bit_depth} is not supported by this decoder. 16-bit samples would be "
            f"truncated to their high byte here, so two different images could produce the same "
            f"pixel fingerprint — refusing instead.")

    # tRNS is implemented for indexed images only. On grayscale and truecolour it makes one sample
    # value fully transparent, which materially changes the RGBA raster; on colour types 4 and 6
    # the spec forbids it outright. Either way, decoding as though it were absent would fingerprint
    # a picture with transparency as if it had none — precisely the silent error this gate exists
    # to prevent.
    if trns is not None and colour != 3:
        raise UnsupportedPNG(
            f"PNG carries a tRNS transparency chunk with colour type {colour}. "
            + ("The specification forbids tRNS for this colour type."
               if colour in (4, 6) else
               "tRNS on grayscale/truecolour changes the visible alpha and is not implemented "
               "here.")
            + " Refusing rather than decoding as if the image were opaque.")
    if colour == 3 and not palette:
        raise UnsupportedPNG("indexed PNG has no PLTE chunk")
    if trns is None:
        trns = b""

    channels = _CHANNELS[colour]
    stride = (width * channels * bit_depth + 7) // 8
    bpp = max(1, (channels * bit_depth + 7) // 8)
    raw = zlib.decompress(bytes(idat))
    if len(raw) != height * (stride + 1):
        raise UnsupportedPNG("decompressed PNG data has an unexpected length")
    planes = _unfilter(raw, height, stride, bpp)

    # Scale a sample of `bit_depth` bits up to the full 0..255 range, so a 1-bit image and an
    # 8-bit image of the same picture produce the same canonical raster.
    if bit_depth in (1, 2, 4):
        maxval = (1 << bit_depth) - 1
        def scale(v: int) -> int:
            return v * 255 // maxval
    else:
        def scale(v: int) -> int:
            return v

    rgba = bytearray(width * height * 4)

    # Fast paths for the 8-bit colour types. Correctness is identical to the general loop below —
    # this is slice assignment instead of a per-pixel Python loop, and the screening pass decodes
    # roughly two thousand images per build.
    if bit_depth == 8 and colour in (0, 2, 4, 6):
        opaque = b"\xff" * width
        for y in range(height):
            row = planes[y * stride:(y + 1) * stride]
            o, e = y * width * 4, (y + 1) * width * 4
            view = memoryview(rgba)[o:e]
            if colour == 0:
                view[0::4] = row[:width]; view[1::4] = row[:width]; view[2::4] = row[:width]
                view[3::4] = opaque
            elif colour == 4:
                g = row[0::2]
                view[0::4] = g; view[1::4] = g; view[2::4] = g; view[3::4] = row[1::2]
            elif colour == 2:
                view[0::4] = row[0::3]; view[1::4] = row[1::3]; view[2::4] = row[2::3]
                view[3::4] = opaque
            else:                                          # colour == 6
                view[:] = row[:width * 4]
        return Raster(width, height, bytes(rgba))

    for y in range(height):
        row = planes[y * stride:(y + 1) * stride]
        samples = _unpack_samples(row, bit_depth, width * channels)
        o = y * width * 4
        for x in range(width):
            s = x * channels
            if colour == 0:                                # grayscale
                g = scale(samples[s]); r = b = g; a = 255
            elif colour == 4:                              # grayscale + alpha
                g = scale(samples[s]); r = b = g; a = scale(samples[s + 1])
            elif colour == 2:                              # truecolour
                r = scale(samples[s]); g = scale(samples[s + 1]); b = scale(samples[s + 2]); a = 255
            elif colour == 6:                              # truecolour + alpha
                r, g, b, a = (scale(samples[s + k]) for k in range(4))
            else:                                          # colour == 3, indexed
                idx = samples[s]
                if (idx + 1) * 3 > len(palette):
                    raise UnsupportedPNG("palette index out of range")
                r, g, b = palette[idx * 3:idx * 3 + 3]
                a = trns[idx] if idx < len(trns) else 255
            p = o + x * 4
            rgba[p] = r; rgba[p + 1] = g; rgba[p + 2] = b; rgba[p + 3] = a
    return Raster(width, height, bytes(rgba))


def pixel_fingerprint(path: Path | str) -> str:
    """SHA-256 of the decoded RGBA8 raster. **This is what "looks the same" means here.**"""
    return decode(path).fingerprint()


def file_sha256(path: Path | str) -> str:
    """SHA-256 of the encoded file. Artifact identity, NOT visual identity."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def encode(raster: Raster, compression_level: int = 6, extra_text: bytes = b"") -> bytes:
    """Write a `Raster` back out as a PNG (RGBA8, no filtering).

    Present so tests can produce two byte streams that decode to the same pixels — the property the
    file-hash gate could not distinguish. It is not used to build the battery: battery images come
    from `hb-view` and nothing re-encodes them.
    """
    def chunk(ctype: bytes, body: bytes) -> bytes:
        return (struct.pack(">I", len(body)) + ctype + body
                + struct.pack(">I", zlib.crc32(ctype + body) & 0xFFFFFFFF))

    stride = raster.width * 4
    raw = bytearray()
    for y in range(raster.height):
        raw.append(0)                                      # filter type 0 (None)
        raw += raster.rgba[y * stride:(y + 1) * stride]
    out = bytearray(PNG_SIGNATURE)
    out += chunk(b"IHDR", struct.pack(">IIBBBBB", raster.width, raster.height, 8, 6, 0, 0, 0))
    if extra_text:
        out += chunk(b"tEXt", extra_text)
    out += chunk(b"IDAT", zlib.compress(bytes(raw), compression_level))
    out += chunk(b"IEND", b"")
    return bytes(out)
