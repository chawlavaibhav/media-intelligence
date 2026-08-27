"""The clip container must be exactly reproducible and must fail closed."""
import json
import os

import pytest

from clipseq import ClipError, ClipSequence, decode_png, encode_png


def _clip(clip_id="t", n=6, w=8, h=6, fps=12):
    frames = [bytearray(bytes([(i * 7 + j) % 256 for j in range(w * h * 3)]))
              for i in range(n)]
    return ClipSequence(clip_id, w, h, fps, frames)


def test_png_roundtrip_is_lossless():
    rgb = bytes(range(48)) * 3
    w, h, back = decode_png(encode_png(12, 4, rgb))
    assert (w, h) == (12, 4)
    assert bytes(back) == rgb


def test_content_hash_is_stable_and_pixel_sensitive():
    a, b = _clip(), _clip()
    assert a.content_hash() == b.content_hash()
    b.frames[2][0] = (b.frames[2][0] + 1) % 256
    assert a.content_hash() != b.content_hash()


def test_content_hash_ignores_clip_id_but_not_fps():
    a = _clip("one")
    b = _clip("two")
    assert a.content_hash() == b.content_hash(), "identical pixels are the same material"
    c = _clip("one", fps=24)
    assert a.content_hash() != c.content_hash(), "frame rate is part of a clip's identity"


def test_write_read_roundtrip(tmp_path):
    a = _clip()
    a.write(tmp_path / "c")
    b = ClipSequence.read(tmp_path / "c")
    assert b.content_hash() == a.content_hash()
    assert b.n_frames == a.n_frames and b.fps == a.fps


def test_zero_frame_clip_is_rejected():
    with pytest.raises(ClipError):
        ClipSequence("z", 4, 4, 12, [])


def test_bad_fps_is_rejected():
    with pytest.raises(ClipError):
        ClipSequence("z", 4, 4, 0, [bytearray(48)])


@pytest.mark.parametrize("break_it,why", [
    (lambda d: (d / "frame-00002.png").write_bytes(b"nope"), "not a png"),
    (lambda d: (d / "frame-00002.png").unlink(), "missing frame"),
    (lambda d: (d / "clip.json").write_text("{"), "unparseable sidecar"),
])
def test_unreadable_clip_fails_closed(tmp_path, break_it, why):
    _clip().write(tmp_path / "c")
    break_it(tmp_path / "c")
    with pytest.raises(ClipError):
        ClipSequence.read(tmp_path / "c")


def test_silently_swapped_frame_is_caught(tmp_path):
    """The case the per-frame hash exists for: pixels changed, sidecar untouched."""
    a = _clip()
    a.write(tmp_path / "c")
    swapped = bytearray(a.frames[0])
    swapped[5] ^= 0xFF
    (tmp_path / "c" / "frame-00003.png").write_bytes(
        encode_png(a.width, a.height, bytes(swapped)))
    with pytest.raises(ClipError):
        ClipSequence.read(tmp_path / "c")


def test_truncated_png_fails_closed(tmp_path):
    _clip().write(tmp_path / "c")
    f = tmp_path / "c" / "frame-00001.png"
    f.write_bytes(f.read_bytes()[:40])
    with pytest.raises(ClipError):
        ClipSequence.read(tmp_path / "c")


def test_declared_frame_count_must_match_disk(tmp_path):
    a = _clip()
    a.write(tmp_path / "c")
    side = json.loads((tmp_path / "c" / "clip.json").read_text())
    side["n_frames"] = 0
    (tmp_path / "c" / "clip.json").write_text(json.dumps(side))
    with pytest.raises(ClipError):
        ClipSequence.read(tmp_path / "c")


def test_greyscale_png_is_refused():
    """A narrow decoder is deliberate: guessing at an unexpected format would be
    the same class of error as guessing at a defect."""
    import struct
    import zlib
    ihdr = struct.pack(">IIBBBBB", 2, 2, 8, 0, 0, 0, 0)   # colour type 0 = grey

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))
    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
           + chunk(b"IDAT", zlib.compress(bytes(6))) + chunk(b"IEND", b""))
    with pytest.raises(ClipError):
        decode_png(png)


def test_motion_load_is_zero_for_a_still_clip_and_positive_otherwise():
    still = ClipSequence("s", 4, 4, 12, [bytearray(48)] * 5)
    assert still.motion_load() == 0.0
    assert _clip().motion_load() > 0.0


def test_written_frames_are_byte_identical_across_two_writes(tmp_path):
    a = _clip()
    s1 = a.write(tmp_path / "x")
    s2 = a.write(tmp_path / "y")
    assert s1["frame_png_hashes"] == s2["frame_png_hashes"]
    assert os.path.getsize(tmp_path / "x" / "frame-00000.png") == \
        os.path.getsize(tmp_path / "y" / "frame-00000.png")
