"""Sealed artifact store (EVAL-024 / EVAL-038 pattern): committed bytes, never overwritten.

WHY NOT REUSE eval/pilot-substrate/artifact_store.py DIRECTLY

    It is byte-safe and immutable (exactly the properties needed) but it names files by
    attempt id only, maps only video content types (everything else becomes `.bin`), and has
    no request.json / record.json / manifest trio. This module keeps the same refusals
    (bytes only, never empty, never overwrite, sha256 over the exact bytes written) and adds:

      media/<trial_id>.<ext>          the artifact bytes
      <trial_id>.request.json         the exact request body, written BEFORE dispatch;
                                      config_hash = sha256 of these bytes
      <trial_id>.record.json          sha256, byte count, content type, provider metadata
      <trial_id>.attempt.json         the persisted attempt (every outcome, not only ok)
      manifest.jsonl                  append-only, one line per sealed artifact

    An existing path is never overwritten: a correction is a new trial id, never an edit.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

EXT_BY_CONTENT_TYPE = {
    "image/png": ".png", "image/jpeg": ".jpg", "image/jpg": ".jpg", "image/webp": ".webp",
    "video/mp4": ".mp4", "video/webm": ".webm", "video/quicktime": ".mov",
    "audio/wav": ".wav", "audio/x-wav": ".wav", "audio/wave": ".wav", "audio/mpeg": ".mp3",
    "audio/mp3": ".mp3", "audio/ogg": ".ogg", "audio/opus": ".opus", "application/octet-stream": ".bin",
}
MEDIA_KIND_BY_PREFIX = {"image/": "image", "video/": "video", "audio/": "audio"}
_SAFE = re.compile(r"[^A-Za-z0-9._-]+")


class ArtifactIntegrityError(RuntimeError):
    """The bytes could not be persisted with intact provenance."""


def safe_id(s: str) -> str:
    return _SAFE.sub("_", s).strip("_")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_json(obj) -> bytes:
    """The one serialisation used for request bodies everywhere (dry-run and dispatch)."""
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


class SealedStore:
    def __init__(self, root: Path | str):
        self.root = Path(root)
        self.media_dir = self.root / "media"
        self.manifest_path = self.root / "manifest.jsonl"

    # -- paths --------------------------------------------------------------------------
    def request_path(self, trial_id: str) -> Path:
        return self.root / f"{safe_id(trial_id)}.request.json"

    def record_path(self, trial_id: str) -> Path:
        return self.root / f"{safe_id(trial_id)}.record.json"

    def attempt_path(self, trial_id: str) -> Path:
        return self.root / f"{safe_id(trial_id)}.attempt.json"

    # -- writes ---------------------------------------------------------------------------
    def _write_new(self, path: Path, data: bytes) -> None:
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError(f"{path.name}: bytes only, got {type(data).__name__}")
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            raise ArtifactIntegrityError(
                f"{path} already exists - sealed files are immutable; a correction is a new trial "
                f"id, never an overwrite")
        with path.open("xb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        if path.stat().st_size != len(data):
            raise ArtifactIntegrityError(f"{path}: wrote {path.stat().st_size} of {len(data)} bytes")

    def write_request(self, trial_id: str, body_bytes: bytes) -> tuple[Path, str]:
        """Written BEFORE dispatch. Returns (path, config_hash = sha256 of the bytes)."""
        path = self.request_path(trial_id)
        self._write_new(path, bytes(body_bytes))
        return path, hashlib.sha256(bytes(body_bytes)).hexdigest()

    def seal(self, trial_id: str, data: bytes, content_type: str | None,
             provider_meta: dict | None = None, suffix: str = "") -> dict:
        """Persist media bytes + record + manifest line. Refuses str, empty bytes, existing paths."""
        if isinstance(data, str):
            raise TypeError("seal takes bytes, not str: media must never travel through text APIs")
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError(f"seal takes bytes, got {type(data).__name__}")
        data = bytes(data)
        if not data:
            raise ArtifactIntegrityError("refusing to seal an empty artifact payload")
        ct = (content_type or "").split(";")[0].strip().lower()
        ext = EXT_BY_CONTENT_TYPE.get(ct, ".bin")
        kind = next((k for p, k in MEDIA_KIND_BY_PREFIX.items() if ct.startswith(p)), "other")
        sid = safe_id(trial_id) + (f".{safe_id(suffix)}" if suffix else "")
        media_path = self.media_dir / f"{sid}{ext}"
        self._write_new(media_path, data)
        sha = hashlib.sha256(data).hexdigest()
        record = {
            "trial_id": trial_id, "artifact_id": f"art-{sha[:12]}",
            "relative_path": str(media_path.relative_to(self.root)),
            "bytes": len(data), "sha256": sha, "content_type": content_type, "media_kind": kind,
            "sealed_at": _now(), "provider": provider_meta or {}, "immutable": True, "synthetic": False,
        }
        rec_path = self.root / f"{sid}.record.json"
        self._write_new(rec_path, (json.dumps(record, indent=1, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8"))
        with self.manifest_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, sort_keys=True, ensure_ascii=False) + "\n")
            fh.flush()
            os.fsync(fh.fileno())
        record["output_location"] = str(media_path)
        return record

    def write_attempt(self, trial_id: str, attempt: dict) -> Path:
        path = self.attempt_path(trial_id)
        self._write_new(path, (json.dumps(attempt, indent=1, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8"))
        return path

    # -- reads ----------------------------------------------------------------------------
    def verify(self, record: dict) -> bool:
        path = self.root / record["relative_path"]
        if not path.exists():
            return False
        data = path.read_bytes()
        return len(data) == record["bytes"] and hashlib.sha256(data).hexdigest() == record["sha256"]

    def manifest(self) -> list[dict]:
        if not self.manifest_path.exists():
            return []
        return [json.loads(line) for line in self.manifest_path.read_text(encoding="utf-8").splitlines() if line.strip()]
