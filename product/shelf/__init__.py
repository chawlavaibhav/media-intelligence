"""The customer shelf (spec §7.2): per account — logo(s), brand colours, brand fonts, product catalogue (photos with roles,
facts, approved product anchor), approved characters, approved master plates, tone notes, past jobs and verdicts.

Rules:
  - Items are PROPOSED by a job (the first onboarding job and every later one) and the customer approves each item once.
  - A change is a new version; old versions are never deleted.
  - A job records which item versions it used (`shelf_uses`).
  - An account sees only its own shelf: every read takes the account id and filters on it; there is no cross-account read.
Files live under <data>/shelf/<account_id>/ and are write-once.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from product.store import Store, new_id, sha256_bytes, utc_now

KINDS = ("logo", "brand_colour", "brand_font", "product", "product_photo", "character", "master_plate", "tone_note", "past_job")


class ShelfAccessDenied(PermissionError):
    pass


class Shelf:
    def __init__(self, store: Store, data_dir: Path):
        self.store = store
        self.root = Path(data_dir) / "shelf"

    # ── writing ─────────────────────────────────────────────────────────────────────────────────────
    def propose(self, account_id: str, *, kind: str, key: str, data: dict, source_job_id: str | None = None,
                file: Path | None = None, status: str = "proposed") -> str:
        """A new version of (kind, key) for this account. If an identical version already exists, returns it."""
        if kind not in KINDS:
            raise ValueError(f"unknown shelf kind {kind}")
        blob = Path(file).read_bytes() if file else None
        sha = sha256_bytes(blob) if blob is not None else None
        prev = self.latest(account_id, kind, key, any_status=True)
        if prev and json.loads(prev["data_json"]) == data and prev["sha256"] == sha and prev["status"] != "rejected":
            return prev["id"]
        version = (prev["version"] + 1) if prev else 1
        sid = new_id("shf")
        path = None
        if blob is not None:
            d = self.root / account_id / kind
            d.mkdir(parents=True, exist_ok=True)
            p = d / f"{key.replace('/', '_')[:60]}-v{version}{Path(file).suffix or '.bin'}"
            if p.exists():
                raise FileExistsError(p)
            shutil.copyfile(file, p)
            path = str(p)
        with self.store.tx() as c:
            c.execute("INSERT INTO shelf_items (id, account_id, kind, key, version, data_json, path, sha256, status, source_job_id, created) "
                      "VALUES (?,?,?,?,?,?,?,?,?,?,?)", (sid, account_id, kind, key, version, json.dumps(data, ensure_ascii=False),
                                                          path, sha, status, source_job_id, utc_now()))
        return sid

    def decide(self, account_id: str, item_id: str, *, approve: bool, by: str) -> None:
        """The customer (of THIS account) approves or rejects a proposed item, once."""
        row = self.item(account_id, item_id)
        if row["status"] != "proposed":
            raise ValueError(f"this item was already {row['status']}")
        with self.store.tx() as c:
            c.execute("UPDATE shelf_items SET status=?, decided_by=?, decided_at=? WHERE id=? AND account_id=?",
                      ("approved" if approve else "rejected", by, utc_now(), item_id, account_id))

    def record_use(self, job_id: str, account_id: str, item_id: str, used_for: str):
        row = self.item(account_id, item_id)
        with self.store.tx() as c:
            c.execute("INSERT INTO shelf_uses (job_id, shelf_item_id, version, used_for, created) VALUES (?,?,?,?,?)",
                      (job_id, item_id, row["version"], used_for, utc_now()))

    # ── reading (always scoped to one account) ─────────────────────────────────────────────────────
    def item(self, account_id: str, item_id: str):
        row = self.store.q1("SELECT * FROM shelf_items WHERE id=? AND account_id=?", (item_id, account_id))
        if row is None:
            raise ShelfAccessDenied("not found")          # another account's item looks exactly like a missing one
        return row

    def items(self, account_id: str, *, kind: str | None = None, status: str | None = None) -> list:
        sql, args = "SELECT * FROM shelf_items WHERE account_id=?", [account_id]
        if kind:
            sql += " AND kind=?"; args.append(kind)
        if status:
            sql += " AND status=?"; args.append(status)
        return self.store.q(sql + " ORDER BY kind, key, version", args)

    def latest(self, account_id: str, kind: str, key: str, *, any_status: bool = False):
        sql = "SELECT * FROM shelf_items WHERE account_id=? AND kind=? AND key=?" + ("" if any_status else " AND status='approved'")
        return self.store.q1(sql + " ORDER BY version DESC LIMIT 1", (account_id, kind, key))

    def approved(self, account_id: str, kind: str | None = None) -> list:
        """The newest APPROVED version of every key (older versions stay on the shelf as history)."""
        out = {}
        for r in self.items(account_id, kind=kind, status="approved"):
            out[(r["kind"], r["key"])] = r
        return list(out.values())

    def uses(self, job_id: str) -> list:
        return self.store.q("SELECT * FROM shelf_uses WHERE job_id=? ORDER BY rowid", (job_id,))

    def summary(self, account_id: str) -> dict:
        """What the waiter pre-fills and the librarian puts on the chef's tray (approved items only)."""
        out = {"brand_colours": [], "logos": [], "fonts": [], "products": [], "characters": [], "master_plates": [], "tone_notes": [],
               "past_jobs": []}
        for r in self.approved(account_id):
            d = json.loads(r["data_json"])
            entry = {"id": r["id"], "key": r["key"], "version": r["version"], **{k: v for k, v in d.items() if k != "private"}}
            {"brand_colour": out["brand_colours"], "logo": out["logos"], "brand_font": out["fonts"], "product": out["products"],
             "product_photo": out["products"], "character": out["characters"], "master_plate": out["master_plates"],
             "tone_note": out["tone_notes"], "past_job": out["past_jobs"]}[r["kind"]].append(entry)
        return out
