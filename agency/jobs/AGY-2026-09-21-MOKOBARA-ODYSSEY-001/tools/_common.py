"""Shared helpers for AGY-2026-09-21-MOKOBARA-ODYSSEY-001 dispatch. stdlib only (urllib).

PROVENANCE (this job): byte-copied 2026-09-21 from
media-intelligence-rentok-cq experiments/RENTOK-CREATIVE-QUALITY-001/treatments/tools/_common.py @ 41d97c6
(sha256 7971b67010a2425de762515db1120b6b9c893fda2b2c039022dcd2a0dbbae1c5); only this header block is added.

Original header follows.

PROVENANCE: byte-copied 2026-09-21 from Lane A's tools/_common.py
(agency/jobs/AGY-2026-09-20-RENTOK-GAME-LANE-A-001/tools/_common.py @ 7dab37a, sha256 of the original recorded in
LEDGER-SUMMARY.md) — itself adapted from tools/reference-kit/_common.py (Cumin Job B kit @ 5c33173) with the fal
helper removed. The only edit here is this header. Run with /usr/bin/python3 after `source ~/.mi-keys`.
"""

from __future__ import annotations

import base64
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

KEY_NAMES = ("FAL_KEY", "GOOGLE_API_KEY", "SARVAM_API_KEY", "ELEVENLABS_API_KEY", "ANTHROPIC_API_KEY",
             "GOOGLE_CLOUD_VISION_API_KEY")   # FAL_KEY kept only so a stray value is scrubbed from any log line


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def key(name: str) -> str:
    """Read a key by NAME from the environment (`source ~/.mi-keys` first). Never printed."""
    v = os.environ.get(name)
    if not v:
        sys.exit(f"{name} is not in the environment; run `source ~/.mi-keys` first (value never printed)")
    return v


def scrub(text: str) -> str:
    for n in KEY_NAMES:
        v = os.environ.get(n)
        if v and v in text:
            text = text.replace(v, f"<{n}>")
    return text


def http(method: str, url: str, headers: dict, body: bytes | None = None, timeout: float = 180.0):
    """Returns (status, bytes, content_type). HTTP errors are returned, not raised; key values scrubbed from text."""
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(), r.headers.get("Content-Type")
    except urllib.error.HTTPError as e:
        return e.code, e.read(), e.headers.get("Content-Type")


def http_json(method: str, url: str, headers: dict, payload: dict | None = None, timeout: float = 180.0):
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    status, data, _ = http(method, url, {**headers, "Content-Type": "application/json"}, body, timeout)
    try:
        return status, json.loads(data.decode("utf-8"))
    except ValueError:
        return status, {"$unparseable_body": scrub(data.decode("utf-8", "replace")[:400])}


def b64file(path: str | Path) -> tuple[str, str]:
    p = Path(path)
    mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp",
            "mp4": "video/mp4", "wav": "audio/wav", "mp3": "audio/mpeg"}[p.suffix.lower().lstrip(".")]
    return base64.b64encode(p.read_bytes()).decode("ascii"), mime


def spend_guard(args, route: str, quantity: float, unit: str, unit_price_usd: float, recipe: str) -> Path:
    """Refuse unless --confirm-spend and --ledger are given; write the reservation line first; return the ledger path."""
    est = quantity * unit_price_usd
    print(f"[{recipe}] route={route} quantity={quantity} {unit} x USD {unit_price_usd} = est USD {est:.4f}")
    if getattr(args, "dry_run", False):
        print("DRY RUN: nothing sent."); sys.exit(0)
    if not getattr(args, "confirm_spend", False) or not getattr(args, "ledger", None):
        sys.exit("REFUSED: pass --confirm-spend and --ledger <file> to send a paid request. "
                 "Nothing was sent. (No spend record exists for this pilot as of 2026-09-14; get one signed first.)")
    ledger = Path(args.ledger)
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a") as f:
        f.write(json.dumps({"utc": now(), "recipe": recipe, "route": route, "quantity": quantity, "unit": unit,
                            "unit_price_usd": unit_price_usd, "est_usd": round(est, 6), "status": "reserved"}) + "\n")
    return ledger


def settle(ledger: Path, request_id, status: str, note: str = "") -> None:
    with ledger.open("a") as f:
        f.write(json.dumps({"utc": now(), "request_id": request_id, "status": status, "note": scrub(note)[:300]}) + "\n")


def gcloud_sa_token(credential_file: str = "~/.aight-litellm-keys/vertex-sa.json") -> str:
    """Access token from the service-account file via the gcloud CLI inside a THROW-AWAY config dir, so the machine's
    default gcloud account (vaibhav@wherehouse.io, project supe-ask-staging) is never read or written.
    PROVENANCE: copied from eval/harness-v2/transports.py GcloudServiceAccountTokenSource."""
    cred = Path(credential_file).expanduser()
    if not cred.exists():
        sys.exit(f"credential file {credential_file} does not exist; nothing was sent")
    tmp = tempfile.mkdtemp(prefix="pilot-gcloud-")
    env = {**os.environ, "CLOUDSDK_CONFIG": tmp, "CLOUDSDK_CORE_DISABLE_PROMPTS": "1"}
    try:
        r = subprocess.run(["gcloud", "auth", "activate-service-account", "--key-file", str(cred)],
                           env=env, capture_output=True, text=True, timeout=60)
        if r.returncode != 0:
            sys.exit(f"gcloud activate-service-account failed (exit {r.returncode}); nothing was sent")
        r = subprocess.run(["gcloud", "auth", "print-access-token"], env=env, capture_output=True, text=True, timeout=60)
        if r.returncode != 0 or not r.stdout.strip():
            sys.exit("gcloud print-access-token failed; nothing was sent")
        return r.stdout.strip()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def poll(check, interval_s: float = 5.0, max_checks: int = 120):
    """Bounded polling. `check()` returns (done, value). Never resubmits. 120 x 5 s = 10 min ceiling
    (Kling v3 Pro p95 was 460 s in the Lab; Registry latency rows)."""
    for i in range(max_checks):
        done, value = check()
        if done:
            return value
        time.sleep(interval_s)
    return {"$timeout": True, "checks": max_checks}


def save(out: str | Path, data: bytes) -> Path:
    p = Path(out); p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(data)
    print(f"saved {p} ({len(data)} bytes)"); return p
