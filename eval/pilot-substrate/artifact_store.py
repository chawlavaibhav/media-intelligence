#!/usr/bin/env python3
"""EVAL-035: binary media persistence. Bytes in, bytes on disk, hash-bound provenance out.

WHY THIS FILE IS PARANOID ABOUT TEXT

    The existing V1 harness stores artifacts with `write_text`/`read_text` and hashes
    strings. That is correct for its synthetic self-tests and CATASTROPHIC for real media: a
    UTF-8 decode of MP4 bytes either raises or, worse, silently mangles the payload, and a
    hash of a decoded-and-re-encoded string is a hash of nothing that ever existed. This
    module is the byte-safe replacement for the pilot path:

      * accepts `bytes` ONLY — a `str` raises TypeError instead of being encoded;
      * writes with `write_bytes`; never opens a text handle;
      * SHA-256 and byte length are computed over the exact bytes written;
      * files are immutable — an existing path is refused, never overwritten.

    The tests feed it bytes that are INVALID UTF-8 on purpose, so any accidental text-API
    path in a future edit fails loudly rather than corrupting evidence quietly.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

# Media kind is derived from the provider's declared content type, defaulting conservatively.
# Vocabulary matches eval/v1/harness/models.py MEDIA_KINDS.
_CONTENT_TYPE_TO_KIND = {
    "video/mp4": ("video", ".mp4"),
    "video/webm": ("video", ".webm"),
    "video/quicktime": ("video", ".mov"),
}


class ArtifactIntegrityError(RuntimeError):
    """The bytes could not be persisted with intact provenance."""


def persist_video_bytes(data: bytes, out_dir: Path, attempt_id: str, trial_id: str,
                        identity: dict, provider_request_id: str | None,
                        content_type: str | None, declared_file_size: int | None,
                        source_url: str | None) -> dict:
    """Persist one returned media payload as immutable bytes with full provenance.

    Returns the artifact record: byte length, SHA-256, media kind, location, route/model
    identity, attempt/trial, provider request id, and whether the provider's declared file
    size matches what actually arrived (a mismatch is RECORDED, not hidden — the persisted
    truth is always the actual bytes).
    """
    if isinstance(data, str):
        raise TypeError(
            "persist_video_bytes takes bytes, not str. Real media must never travel "
            "through text APIs: a decode/encode round-trip mangles or destroys it.")
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError(f"persist_video_bytes takes bytes, got {type(data).__name__}")
    data = bytes(data)
    if not data:
        raise ArtifactIntegrityError("refusing to persist an empty artifact payload")

    media_kind, extension = _CONTENT_TYPE_TO_KIND.get(
        (content_type or "").lower(),
        ("video" if (content_type or "").lower().startswith("video/") else "other", ".bin"))

    sha256 = hashlib.sha256(data).hexdigest()
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{attempt_id}{extension}"
    if path.exists():
        raise ArtifactIntegrityError(
            f"artifact path {path} already exists — artifacts are immutable; a correction "
            f"is a new artifact, never an overwrite")
    path.write_bytes(data)

    written = path.stat().st_size
    if written != len(data):
        raise ArtifactIntegrityError(
            f"wrote {written} bytes but payload was {len(data)} bytes; the artifact on "
            f"disk does not match the bytes received")

    return {
        "artifact_id": f"art-{sha256[:12]}",
        "attempt_id": attempt_id,
        "trial_id": trial_id,
        **identity,
        "provider_request_id": provider_request_id,
        "output_sha256": sha256,
        "output_bytes": len(data),
        "output_location": str(path),
        "media_kind": media_kind,
        "content_type": content_type,
        "declared_file_size": declared_file_size,
        "declared_size_matches": (declared_file_size is None
                                  or declared_file_size == len(data)),
        "source_url": source_url,
        "immutable": True,
        "synthetic": False,
    }


def verify_artifact(record: dict) -> bool:
    """Recompute the stored file's hash and length against the record. Deterministic."""
    path = Path(record["output_location"])
    if not path.exists():
        return False
    data = path.read_bytes()
    return (len(data) == record["output_bytes"]
            and hashlib.sha256(data).hexdigest() == record["output_sha256"])
