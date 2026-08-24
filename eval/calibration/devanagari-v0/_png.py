"""Minimal dependency-free PNG read/write (RGB8, no interlace).

Exists only so crop geometry can be VERIFIED mechanically. This environment has no image
library, and an unverified crop would mean a reader and a checker judging the wrong region —
a correctness failure invisible in every artifact. Not a general-purpose codec.
"""
import struct, zlib

def write_rgb(path, w, h, px):
    """px: list of h rows, each a list of w (r,g,b) tuples."""
    raw = b"".join(b"\x00" + bytes(v for p in row for v in p) for row in px)
    def chunk(tag, data):
        c = tag + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)
    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 9))
           + chunk(b"IEND", b""))
    open(path, "wb").write(png)

def read_rgb(path):
    """-> (w, h, rows). Raises on anything this reader does not handle."""
    d = open(path, "rb").read()
    if d[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    i, idat, w = 8, b"", None
    while i < len(d):
        ln = struct.unpack(">I", d[i:i+4])[0]; tag = d[i+4:i+8]; body = d[i+8:i+8+ln]
        if tag == b"IHDR":
            w, h, depth, ctype, comp, filt, inter = struct.unpack(">IIBBBBB", body)
            if (depth, ctype, inter) != (8, 2, 0):
                raise ValueError(f"unsupported PNG: depth={depth} colour={ctype} interlace={inter}")
        elif tag == b"IDAT":
            idat += body
        elif tag == b"IEND":
            break
        i += 12 + ln
    if w is None:
        raise ValueError("no IHDR")
    raw, stride, rows, prev = zlib.decompress(idat), w * 3, [], bytearray(w * 3)
    pos = 0
    for _ in range(h):
        ft = raw[pos]; pos += 1
        line = bytearray(raw[pos:pos+stride]); pos += stride
        for x in range(stride):
            a = line[x-3] if x >= 3 else 0
            b = prev[x]
            c = prev[x-3] if x >= 3 else 0
            if   ft == 0: pass
            elif ft == 1: line[x] = (line[x] + a) & 255
            elif ft == 2: line[x] = (line[x] + b) & 255
            elif ft == 3: line[x] = (line[x] + ((a + b) >> 1)) & 255
            elif ft == 4:
                p = a + b - c; pa, pb, pc = abs(p-a), abs(p-b), abs(p-c)
                line[x] = (line[x] + (a if (pa <= pb and pa <= pc) else b if pb <= pc else c)) & 255
            else: raise ValueError(f"bad filter {ft}")
        rows.append([tuple(line[x*3:x*3+3]) for x in range(w)])
        prev = line
    return w, h, rows
