"""Operator command line: bootstrap, accounts, invitations, backup and restore.

There is deliberately NO command here that overrides a check, picks a take, releases a file or resumes a job: those are
the founder's decisions and need the founder signed in to the web app (spec §6.4, product/authority.py).

    python3 -m product.admin init-founder --email founder@example.com      # ONCE: the one founder account (invitation link)
    python3 -m product.admin init-operator --email ops@example.com         # staff: view and pause; cannot override anything
    python3 -m product.admin create-account --name "Acme" --ceiling 40
    python3 -m product.admin invite --email buyer@acme.com --account acct_... [--role customer]
    python3 -m product.admin backup --out /backups/mi-2026-09-23.tar.gz
    python3 -m product.admin restore --from /backups/mi-2026-09-23.tar.gz --data-dir /srv/mi-restore
    python3 -m product.admin metrics --job job_...
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import tarfile
import tempfile
from pathlib import Path

from product import config, learning
from product.service import Service
from product.store import Store


def backup(settings, out: Path) -> dict:
    """Online-consistent backup: sqlite backup API for the database, then the media tree."""
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as d:
        snap = Path(d) / "mi.sqlite3"
        src = sqlite3.connect(settings.db_path)
        dst = sqlite3.connect(snap)
        with dst:
            src.backup(dst)
        src.close(); dst.close()
        with tarfile.open(out, "w:gz") as tar:
            tar.add(snap, arcname="mi.sqlite3")
            if settings.media_dir.exists():
                tar.add(settings.media_dir, arcname="media")
            cases = settings.data_dir / "cases"
            if cases.exists():
                tar.add(cases, arcname="cases")
    return {"out": str(out), "bytes": out.stat().st_size}


def restore(archive: Path, data_dir: Path) -> dict:
    data_dir.mkdir(parents=True, exist_ok=True)
    if (data_dir / "mi.sqlite3").exists():
        raise SystemExit(f"{data_dir} already holds a database; restore into an empty directory")
    with tarfile.open(archive, "r:gz") as tar:
        for m in tar.getmembers():
            if m.name.startswith("/") or ".." in Path(m.name).parts:
                raise SystemExit(f"refusing unsafe path in archive: {m.name}")
        tar.extractall(data_dir)
    st = Store(data_dir / "mi.sqlite3")
    ok = st.q1("PRAGMA integrity_check")[0]
    jobs = st.q1("SELECT COUNT(*) FROM jobs")[0]
    rows = st.q("SELECT id FROM assets")
    found = sum(Path(st.asset(r["id"])["path"]).exists() for r in rows)
    return {"integrity": ok, "jobs": jobs, "assets": len(rows), "asset_files_present": found, "data_dir": str(data_dir)}


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init-founder"); p.add_argument("--email", required=True)
    p = sub.add_parser("init-operator"); p.add_argument("--email", required=True)
    p = sub.add_parser("create-account"); p.add_argument("--name", required=True); p.add_argument("--ceiling", default="25"); p.add_argument("--auto-approve", action="store_true")
    p = sub.add_parser("invite"); p.add_argument("--email", required=True); p.add_argument("--account"); p.add_argument("--role", default="customer")
    p = sub.add_parser("backup"); p.add_argument("--out", required=True)
    p = sub.add_parser("restore"); p.add_argument("--from", dest="src", required=True); p.add_argument("--data-dir", required=True)
    p = sub.add_parser("metrics"); p.add_argument("--job", required=True)
    a = ap.parse_args()
    if a.cmd == "restore":
        print(json.dumps(restore(Path(a.src), Path(a.data_dir)))); return
    s = config.load()
    st = Store(s.db_path)
    svc = Service(s, st)
    if a.cmd == "init-founder":
        tok = svc.create_invite(email=a.email, role="founder", account_id=None, by="cli")
        print(f"{s.base_url}/invite/{tok}")
    elif a.cmd == "init-operator":
        tok = svc.create_invite(email=a.email, role="operator", account_id=None, by="cli")
        print(f"{s.base_url}/invite/{tok}")
    elif a.cmd == "create-account":
        print(st.create_account(a.name, ceiling_usd=a.ceiling, auto_approve=a.auto_approve))
    elif a.cmd == "invite":
        tok = svc.create_invite(email=a.email, role=a.role, account_id=a.account, by="cli")
        print(f"{s.base_url}/invite/{tok}")
    elif a.cmd == "backup":
        print(json.dumps(backup(s, Path(a.out))))
    elif a.cmd == "metrics":
        print(json.dumps(learning.metrics(st, a.job), indent=1, default=str))


if __name__ == "__main__":
    main()
