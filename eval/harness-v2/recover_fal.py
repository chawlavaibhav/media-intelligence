#!/usr/bin/env python3
"""recover_fal: fetch the results of fal queue jobs that were SUBMITTED and BILLED but whose outcome the
first live lane wrote off (the 202-status misread, Image Round 1, 2026-09-08). No re-submit, no new charge.

    python3 eval/harness-v2/recover_fal.py --run-id <id> --out <dir> [--trial <trial_id> ...] [--dry]

For every `<out>/artifacts/<trial>.attempt.json` whose status is not ok and whose error class is a poll
error (`poll_http_2xx`, `poll_budget_exhausted`) with a recoverable fal request id, this script:
  1. GETs the job's status URL (queue.fal.run only; the key goes nowhere else) until COMPLETED,
  2. GETs the result, 3. downloads the artifact from fal's own host,
  4. seals it under the ORIGINAL trial id (media + record + manifest line; the store refuses overwrites),
  5. writes `<trial>.attempt.recovered.json` beside the untouched original attempt, carrying the original
     verbatim plus a `recovery` block (what was fetched, when, how many status checks, sha256),
  6. runs the post-artifact instruments through the runner's own routine (observation only),
  7. appends a `recovered` event to RUN-LOG.jsonl.
The ledger is NOT touched: the original reservation was settled conservatively at the pinned price, which is
what fal charges for a completed job. `store.load_attempt()` prefers the recovered record wherever the
harness reads attempts (instruments for repeat 2, judging packet, status), so the trial counts as a real
draw with an artifact — never as a retry (a retry would be a second submit; this makes none).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import hv2_paths
import run_live as RL
import store as S
from adapters import base as B
from adapters import fal_queue as FQ

RECOVERABLE = re.compile(r"^(poll_http_2\d\d|poll_budget_exhausted|poll_network_failure|poll_timeout)$")
REQUEST_ID_IN_NOTE = re.compile(r"\b([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\b")
MAX_STATUS_CHECKS = 60
POLL_INTERVAL_S = 3.0


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def request_id_of(attempt: dict) -> str | None:
    rid = attempt.get("provider_request_id")
    if isinstance(rid, str) and rid:
        return rid
    m = REQUEST_ID_IN_NOTE.search(attempt.get("raw_status_note") or "")
    return m.group(1) if m else None


def candidates(store: S.SealedStore, only: set[str] | None = None) -> list[tuple[str, dict]]:
    out = []
    for p in sorted(store.root.glob("*.attempt.json")):
        a = json.loads(p.read_text(encoding="utf-8"))
        tid = a.get("trial_id")
        if only and tid not in only:
            continue
        if a.get("status") == "ok" or store.recovered_attempt_path(tid).exists():
            continue
        if not RECOVERABLE.match(a.get("error_class") or ""):
            continue
        if not request_id_of(a) or not str(a.get("endpoint", "")).startswith("https://queue.fal.run/"):
            continue
        out.append((tid, a))
    return out


def recover_one(tid: str, attempt: dict, store: S.SealedStore, transport, headers: dict, sleep=time.sleep, log=None) -> dict:
    rid = request_id_of(attempt)
    endpoint = attempt["endpoint"].rstrip("/")
    # fal's request URLs hang off the APP id (owner/app), not the full endpoint path: a submit to
    # queue.fal.run/bytedance/seedream/v5/pro/text-to-image is tracked at
    # queue.fal.run/bytedance/seedream/requests/<id>/status (observed 2026-09-08: the full path answers 405).
    # Endpoints that are exactly owner/app (fal-ai/flux-2-pro) are unchanged by this rule.
    parts = endpoint.split("://", 1)[1].split("/")            # ["queue.fal.run", owner, app, ...]
    app_base = "https://" + "/".join(parts[:3])
    bases = [app_base] + ([endpoint] if endpoint != app_base else [])
    status_url = response_url = None
    checks = 0
    last = None
    for base in bases:
        status_url, response_url = f"{base}/requests/{rid}/status", f"{base}/requests/{rid}"
        if not (FQ.trusted_fal_url(status_url) and FQ.trusted_fal_url(response_url)):
            return {"trial_id": tid, "recovered": False, "reason": "status/response URL not on queue.fal.run; key not sent"}
        done = False
        for i in range(MAX_STATUS_CHECKS):
            if i:
                sleep(POLL_INTERVAL_S)
            checks += 1
            code, st = transport.get_json(status_url, headers)
            s = (st or {}).get("status") if isinstance(st, dict) else None
            last = (code, s)
            if code in (200, 202) and s == "COMPLETED":
                done = True
                break
            if code in (200, 202) and s in ("IN_QUEUE", "IN_PROGRESS"):
                continue
            break                                             # 404/405/other: try the next base, if any
        if done:
            break
    else:
        return {"trial_id": tid, "recovered": False, "reason": f"status poll answered {last[0]} / {last[1]!r} after {checks} checks (bases tried: {bases})", "request_id": rid}
    code, out = transport.get_json(response_url, headers)
    out = out if isinstance(out, dict) else {}
    if code != 200 or out.get("error") or out.get("detail"):
        return {"trial_id": tid, "recovered": False, "reason": f"result read answered {code}: {str(out.get('error') or out.get('detail') or out)[:200]}", "request_id": rid}
    url = FQ._artifact_url(out)
    if not url or not FQ.trusted_fal_url(url, kind="download"):
        return {"trial_id": tid, "recovered": False, "reason": f"no trusted artifact url in the result ({url!r})", "request_id": rid}
    dcode, data, ct = transport.get_bytes(url, {})
    if dcode != 200 or not data:
        return {"trial_id": tid, "recovered": False, "reason": f"download answered {dcode}", "request_id": rid, "artifact_url": url}
    ct = ct or FQ._guess_ct(url)
    record = store.seal(tid, bytes(data), ct, {"request_id": rid, "artifact_url": url, "content_type": ct, "recovered_without_resubmit": True})
    original_sha = hashlib.sha256(store.attempt_path(tid).read_bytes()).hexdigest()
    recovered = dict(attempt)
    recovered.update({
        "status": "ok", "error_class": None, "outcome_resolved": True, "ambiguous_dispatch": False,
        "raw_status_note": f"recovered without re-submit from fal request {rid}: the job had COMPLETED; original poll misread HTTP 202",
        "provider_request_id": rid, "completed_at": _now(),
        "artifact": {k: record[k] for k in ("artifact_id", "relative_path", "bytes", "sha256", "content_type", "media_kind")},
        "lifecycle_counts": {**(attempt.get("lifecycle_counts") or {}), "recovery_status_checks": checks, "recovery_result_reads": 1, "recovery_downloads": 1,
                             "submits": (attempt.get("lifecycle_counts") or {}).get("submits", 1)},
        "recovery": {"at": _now(), "from_request_id": rid, "status_url": status_url, "response_url": response_url, "artifact_url": url,
                     "original_attempt_sha256": original_sha, "original_error_class": attempt.get("error_class"),
                     "ledger": "untouched: the reservation was settled conservatively at the pinned price, which is what a completed job bills",
                     "resubmitted": False},
    })
    store.write_recovered_attempt(tid, recovered)
    if log:
        log("recovered", trial_id=tid, request_id=rid, artifact_sha256=record["sha256"], bytes=record["bytes"], status_checks=checks)
    return {"trial_id": tid, "recovered": True, "request_id": rid, "sha256": record["sha256"], "bytes": record["bytes"], "status_checks": checks}


def run(out: Path | str, run_id: str, only: set[str] | None = None, dry: bool = False, transport=None, key_loader=None,
        sleep=time.sleep, auth_path: Path | str | None = None) -> dict:
    out = Path(out)
    store = S.SealedStore(out / RL.ARTIFACTS_DIR)
    todo = candidates(store, only)
    summary = {"run_id": run_id, "candidates": [t for t, _ in todo], "results": [], "dry": dry}
    if dry or not todo:
        return summary
    if transport is None:
        import transports as T
        transport = T.FalQueueTransport()          # queue.fal.run status/result + fal CDN download; no submit verb is used here
    key = (key_loader or B.KeyLoader()).read("FAL_KEY")
    headers = {"Authorization": f"Key {key}"}
    del key
    runner = RL.LiveRunner(out, run_id, auth_path or RL.L.AUTH_LOCAL_PATH, RL.live_transport_factory)
    runner.plan = RL.load_plan(out, run_id)

    def log(event, **fields):
        runner._log(event, **fields)

    for tid, attempt in todo:
        try:
            res = recover_one(tid, attempt, store, transport, headers, sleep=sleep, log=log)
        except Exception as exc:  # noqa: BLE001
            res = {"trial_id": tid, "recovered": False, "reason": f"{type(exc).__name__}: {B.scrub(str(exc), [headers['Authorization']])}"}
        if res.get("recovered"):
            trial = next((t for t in runner.plan["trials"] if t["trial_id"] == tid), None)
            rec = store.load_attempt(tid)
            if trial and rec:
                try:
                    runner._instruments(trial, rec)
                except Exception as exc:  # noqa: BLE001
                    res["instruments_error"] = f"{type(exc).__name__}: {exc}"
        summary["results"].append(res)
    return summary


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--run-id", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--trial", action="append", default=None)
    p.add_argument("--dry", action="store_true", help="list candidates; fetch nothing")
    a = p.parse_args(argv)
    s = run(a.out, a.run_id, set(a.trial) if a.trial else None, dry=a.dry)
    print(json.dumps(s, indent=1, default=str))
    return 0 if all(r.get("recovered") for r in s["results"]) else 1


if __name__ == "__main__":
    sys.exit(main())
