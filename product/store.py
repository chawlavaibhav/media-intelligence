"""The authoritative job store: SQLite (WAL), one file, every write a transaction.

Closes MOKOBARA-ODYSSEY-007:LG-1 (attempt ids minted by counting a file appended at settle): attempt
ids are minted from the ledger itself, inside the same BEGIN IMMEDIATE transaction that checks the
budget and writes the reservation, so two concurrent reservations can never share an id and can
never jointly cross the cap.
"""
from __future__ import annotations

import contextlib
import hashlib
import json
import secrets
import sqlite3
import threading
import time
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterator

SCHEMA = """
CREATE TABLE IF NOT EXISTS accounts (
  id TEXT PRIMARY KEY, name TEXT NOT NULL, ceiling_usd TEXT NOT NULL, auto_approve INTEGER NOT NULL DEFAULT 0,
  created TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY, account_id TEXT, email TEXT UNIQUE NOT NULL, name TEXT, role TEXT NOT NULL,
  pw_hash TEXT, created TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS invites (
  token_hash TEXT PRIMARY KEY, account_id TEXT, email TEXT NOT NULL, role TEXT NOT NULL, created TEXT NOT NULL,
  used_at TEXT);
CREATE TABLE IF NOT EXISTS sessions (
  token_hash TEXT PRIMARY KEY, user_id TEXT NOT NULL, created TEXT NOT NULL, expires REAL NOT NULL);
CREATE TABLE IF NOT EXISTS jobs (
  id TEXT PRIMARY KEY, account_id TEXT NOT NULL, created_by TEXT NOT NULL, title TEXT NOT NULL,
  media TEXT NOT NULL, state TEXT NOT NULL, resume_state TEXT, brief_json TEXT NOT NULL, brief_sha256 TEXT NOT NULL,
  budget_usd TEXT NOT NULL, budget_authorised_by TEXT, budget_authorised_at TEXT,
  version INTEGER NOT NULL DEFAULT 1, lease_owner TEXT, lease_until REAL NOT NULL DEFAULT 0,
  pause_reason TEXT, created TEXT NOT NULL, updated TEXT NOT NULL, approved_at TEXT, first_cut_at TEXT,
  presented_at TEXT, closed_at TEXT, outcome TEXT);
CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT, job_id TEXT NOT NULL, utc TEXT NOT NULL, actor TEXT NOT NULL,
  kind TEXT NOT NULL, data_json TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS artifacts (
  id INTEGER PRIMARY KEY AUTOINCREMENT, job_id TEXT NOT NULL, kind TEXT NOT NULL, version INTEGER NOT NULL,
  data_json TEXT NOT NULL, sha256 TEXT NOT NULL, created TEXT NOT NULL, created_by TEXT NOT NULL,
  UNIQUE(job_id, kind, version));
CREATE TABLE IF NOT EXISTS nodes (
  job_id TEXT NOT NULL, node_id TEXT NOT NULL, kind TEXT NOT NULL, deps_json TEXT NOT NULL, spec_json TEXT NOT NULL,
  status TEXT NOT NULL, selected_asset_id TEXT, draws INTEGER NOT NULL DEFAULT 0, max_draws INTEGER NOT NULL DEFAULT 2,
  cut INTEGER NOT NULL DEFAULT 1, note TEXT, updated TEXT NOT NULL, PRIMARY KEY (job_id, node_id));
CREATE TABLE IF NOT EXISTS assets (
  id TEXT PRIMARY KEY, job_id TEXT NOT NULL, node_id TEXT, kind TEXT NOT NULL, role TEXT, path TEXT NOT NULL,
  sha256 TEXT NOT NULL, content_type TEXT NOT NULL, bytes INTEGER NOT NULL, source TEXT NOT NULL,
  attempt_id TEXT, status TEXT NOT NULL, cut INTEGER, meta_json TEXT NOT NULL, created TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS attempts (
  id TEXT PRIMARY KEY, job_id TEXT NOT NULL, seq INTEGER NOT NULL, node_id TEXT, route TEXT NOT NULL,
  category TEXT NOT NULL, reserved_usd TEXT NOT NULL, settled_usd TEXT, status TEXT NOT NULL,
  failure_class TEXT, counts_against_route INTEGER, request_ref TEXT, detail TEXT, is_repair INTEGER NOT NULL DEFAULT 0,
  reserved_at TEXT NOT NULL, settled_at TEXT, started REAL, ended REAL, UNIQUE (job_id, seq));
CREATE TABLE IF NOT EXISTS checks (
  id INTEGER PRIMARY KEY AUTOINCREMENT, job_id TEXT NOT NULL, asset_id TEXT NOT NULL, asset_sha256 TEXT NOT NULL,
  check_id TEXT NOT NULL, status TEXT NOT NULL, blocking INTEGER NOT NULL, runner TEXT NOT NULL,
  detail TEXT NOT NULL, evidence_json TEXT NOT NULL, control_ids TEXT NOT NULL, created TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS waivers (
  id INTEGER PRIMARY KEY AUTOINCREMENT, job_id TEXT NOT NULL, asset_id TEXT NOT NULL, check_id TEXT NOT NULL,
  by_user TEXT NOT NULL, reason TEXT NOT NULL, created TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS feedback (
  id INTEGER PRIMARY KEY AUTOINCREMENT, job_id TEXT NOT NULL, asset_id TEXT, target TEXT, text TEXT NOT NULL,
  kind TEXT NOT NULL, by_user TEXT NOT NULL, created TEXT NOT NULL, resolved_in_cut INTEGER);
CREATE TABLE IF NOT EXISTS timings (
  id INTEGER PRIMARY KEY AUTOINCREMENT, job_id TEXT NOT NULL, phase TEXT NOT NULL, label TEXT,
  started REAL NOT NULL, ended REAL);
CREATE TABLE IF NOT EXISTS llm_calls (
  id INTEGER PRIMARY KEY AUTOINCREMENT, job_id TEXT NOT NULL, role TEXT NOT NULL, provider TEXT NOT NULL,
  model TEXT NOT NULL, isolated INTEGER NOT NULL, input_sha256 TEXT NOT NULL, context_kinds TEXT NOT NULL,
  output_json TEXT, usage_json TEXT, status TEXT NOT NULL, attempt_id TEXT, started REAL NOT NULL, ended REAL);
CREATE TABLE IF NOT EXISTS deliveries (
  id INTEGER PRIMARY KEY AUTOINCREMENT, job_id TEXT NOT NULL, asset_id TEXT NOT NULL, asset_sha256 TEXT NOT NULL,
  accepted_by TEXT NOT NULL, created TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS overrides (
  id INTEGER PRIMARY KEY AUTOINCREMENT, job_id TEXT NOT NULL, kind TEXT NOT NULL, target TEXT NOT NULL,
  founder_user_id TEXT NOT NULL, founder_email TEXT NOT NULL, reason TEXT NOT NULL, data_json TEXT NOT NULL, created TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS rulebook_versions (
  id INTEGER PRIMARY KEY AUTOINCREMENT, worker TEXT NOT NULL, version INTEGER NOT NULL, card_json TEXT NOT NULL,
  by TEXT NOT NULL, reason TEXT NOT NULL, source_lesson TEXT, created TEXT NOT NULL, UNIQUE(worker, version));
CREATE TABLE IF NOT EXISTS request_fingerprints (
  job_id TEXT NOT NULL, fingerprint TEXT NOT NULL, route TEXT NOT NULL, node_id TEXT, sent INTEGER NOT NULL,
  first_utc TEXT NOT NULL, last_utc TEXT NOT NULL, PRIMARY KEY (job_id, fingerprint));
CREATE TABLE IF NOT EXISTS shelf_items (
  id TEXT PRIMARY KEY, account_id TEXT NOT NULL, kind TEXT NOT NULL, key TEXT NOT NULL, version INTEGER NOT NULL,
  data_json TEXT NOT NULL, path TEXT, sha256 TEXT, status TEXT NOT NULL, decided_by TEXT, decided_at TEXT,
  source_job_id TEXT, created TEXT NOT NULL, UNIQUE(account_id, kind, key, version));
CREATE TABLE IF NOT EXISTS shelf_uses (
  job_id TEXT NOT NULL, shelf_item_id TEXT NOT NULL, version INTEGER NOT NULL, used_for TEXT NOT NULL, created TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS equipment_rows (
  id TEXT NOT NULL, version INTEGER NOT NULL, generator TEXT NOT NULL, routes TEXT NOT NULL, action_class TEXT NOT NULL,
  verdict TEXT NOT NULL, sample_count INTEGER NOT NULL, evidence_json TEXT NOT NULL, note TEXT, alternative TEXT,
  by TEXT NOT NULL, source_lesson TEXT, created TEXT NOT NULL, PRIMARY KEY (id, version));
CREATE TABLE IF NOT EXISTS recipe_library (
  id TEXT PRIMARY KEY, source_job_id TEXT NOT NULL, account_id TEXT, media TEXT NOT NULL, product_category TEXT,
  action_classes TEXT NOT NULL, routes TEXT NOT NULL, outcome TEXT NOT NULL, customer_words TEXT, recipe_json TEXT NOT NULL,
  summary TEXT NOT NULL, private INTEGER NOT NULL DEFAULT 0, by TEXT NOT NULL, source_lesson TEXT, created TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS failure_diary (
  id TEXT PRIMARY KEY, source_job_id TEXT, account_id TEXT, media TEXT, action_classes TEXT NOT NULL, routes TEXT NOT NULL,
  failure_mode TEXT NOT NULL, text TEXT NOT NULL, private INTEGER NOT NULL DEFAULT 0, by TEXT NOT NULL,
  source_lesson TEXT, created TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS judge_qualifications (
  id TEXT PRIMARY KEY, judge TEXT NOT NULL, model TEXT NOT NULL, report_sha256 TEXT NOT NULL, result_json TEXT NOT NULL,
  recorded_by TEXT NOT NULL, recorded_at TEXT NOT NULL, revoked_by TEXT, revoked_at TEXT, revoke_note TEXT);
CREATE TABLE IF NOT EXISTS lessons (
  id TEXT PRIMARY KEY, job_id TEXT NOT NULL, worker TEXT NOT NULL, target TEXT NOT NULL, proposal_json TEXT NOT NULL,
  why TEXT NOT NULL, evidence_json TEXT NOT NULL, status TEXT NOT NULL, decided_by TEXT, decided_at TEXT,
  decision_note TEXT, applied_json TEXT, created TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS ix_events_job ON events(job_id, id);
CREATE INDEX IF NOT EXISTS ix_attempts_job ON attempts(job_id, seq);
CREATE INDEX IF NOT EXISTS ix_assets_job ON assets(job_id);
CREATE INDEX IF NOT EXISTS ix_checks_asset ON checks(asset_id);
CREATE INDEX IF NOT EXISTS ix_jobs_state ON jobs(state, lease_until);
"""

# v2 columns on llm_calls: which worker and form, the rulebook card version, the fingerprint of the customer's exact
# words the call carried, the librarian's tray, and the estimated cost (simulated mode reports estimates, spec §9.4)
LLM_CALL_COLUMNS = [("worker", "TEXT"), ("form", "TEXT"), ("card_version", "INTEGER"), ("exact_words_sha256", "TEXT"),
                    ("tray_ids", "TEXT"), ("est_in_tokens", "INTEGER"), ("est_out_tokens", "INTEGER"), ("est_cost_usd", "TEXT")]

HELD_STATUSES = ("reserved", "uncertain")      # money held but not settled
MONEY = Decimal("0.000001")


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def dec(v) -> Decimal:
    return Decimal(str(v if v is not None else "0"))


def money(v) -> str:
    return str(dec(v).quantize(MONEY))


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_json(obj) -> str:
    return sha256_bytes(json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode())


def new_id(prefix: str) -> str:
    return f"{prefix}_{secrets.token_hex(8)}"


class BudgetExhausted(Exception):
    def __init__(self, job_id: str, needed: Decimal, available: Decimal, budget: Decimal):
        self.job_id, self.needed, self.available, self.budget = job_id, needed, available, budget
        self.shortfall = (needed - available).quantize(Decimal("0.01"))
        super().__init__(f"job {job_id}: needs USD {needed} but only USD {available} of USD {budget} remains "
                         f"(shortfall USD {self.shortfall})")


class StaleState(Exception):
    """A transition was attempted from a state the job is no longer in."""


class WriteOnceViolation(Exception):
    """A file path that already holds a registered asset was about to be reused (spec §7.1: files are write-once)."""


LESSON_COLUMNS = ("kind", "support_key", "watch_json", "undone_by", "undone_at", "undo_note")


class Store:
    def __init__(self, db_path: str | Path):
        self.db_path = str(db_path)
        self.root = Path(db_path).resolve().parent
        self._local = threading.local()
        with self.connect() as c:
            c.executescript(SCHEMA)
            have = {r["name"] for r in c.execute("PRAGMA table_info(llm_calls)")}
            for col, typ in LLM_CALL_COLUMNS:
                if col not in have:
                    c.execute(f"ALTER TABLE llm_calls ADD COLUMN {col} {typ}")
            have = {r["name"] for r in c.execute("PRAGMA table_info(lessons)")}
            for col in LESSON_COLUMNS:                 # amendment 1 §4: kind, support, watch and undo of automated lessons
                if col not in have:
                    c.execute(f"ALTER TABLE lessons ADD COLUMN {col} TEXT")

    # ── connections ──────────────────────────────────────────────────────────────
    def connect(self) -> sqlite3.Connection:
        c = sqlite3.connect(self.db_path, timeout=30, isolation_level=None, check_same_thread=False)
        c.row_factory = sqlite3.Row
        c.execute("PRAGMA journal_mode=WAL")
        c.execute("PRAGMA busy_timeout=30000")
        c.execute("PRAGMA foreign_keys=ON")
        return c

    @property
    def _c(self) -> sqlite3.Connection:
        c = getattr(self._local, "conn", None)
        if c is None:
            c = self._local.conn = self.connect()
        return c

    @contextlib.contextmanager
    def tx(self) -> Iterator[sqlite3.Connection]:
        """BEGIN IMMEDIATE: one writer at a time across threads and processes."""
        c = self._c
        if c.in_transaction:          # nested: join the outer transaction
            yield c
            return
        for i in range(50):
            try:
                c.execute("BEGIN IMMEDIATE")
                break
            except sqlite3.OperationalError as e:
                if "locked" not in str(e) or i == 49:
                    raise
                time.sleep(0.05 * (i + 1))
        try:
            yield c
            c.execute("COMMIT")
        except BaseException:
            c.execute("ROLLBACK")
            raise

    def q(self, sql: str, args=()) -> list[sqlite3.Row]:
        return self._c.execute(sql, args).fetchall()

    def q1(self, sql: str, args=()) -> sqlite3.Row | None:
        return self._c.execute(sql, args).fetchone()

    # ── accounts / users ─────────────────────────────────────────────────────────
    def create_account(self, name: str, ceiling_usd="25.00", auto_approve=False) -> str:
        aid = new_id("acct")
        with self.tx() as c:
            c.execute("INSERT INTO accounts VALUES (?,?,?,?,?)", (aid, name, money(ceiling_usd), int(auto_approve), utc_now()))
        return aid

    def account(self, account_id: str):
        return self.q1("SELECT * FROM accounts WHERE id=?", (account_id,))

    def set_account(self, account_id: str, **fields):
        allowed = {"ceiling_usd", "auto_approve", "name"}
        with self.tx() as c:
            for k, v in fields.items():
                if k not in allowed:
                    raise ValueError(k)
                c.execute(f"UPDATE accounts SET {k}=? WHERE id=?", (money(v) if k == "ceiling_usd" else v, account_id))

    def user_by_email(self, email: str):
        return self.q1("SELECT * FROM users WHERE email=?", (email.strip().lower(),))

    def user(self, user_id: str):
        return self.q1("SELECT * FROM users WHERE id=?", (user_id,))

    # ── jobs ────────────────────────────────────────────────────────────────────
    def create_job(self, *, account_id: str, user_id: str, title: str, media: str, brief: dict,
                   budget_usd, state: str = "submitted") -> str:
        jid = "job_" + datetime.now(timezone.utc).strftime("%Y%m%d") + "_" + secrets.token_hex(4)
        now = utc_now()
        with self.tx() as c:
            c.execute("INSERT INTO jobs (id, account_id, created_by, title, media, state, brief_json, brief_sha256, "
                      "budget_usd, created, updated) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                      (jid, account_id, user_id, title, media, state, json.dumps(brief, ensure_ascii=False),
                       sha256_json(brief), money(budget_usd), now, now))
            self._event(c, jid, user_id, "job_created", {"media": media, "brief_sha256": sha256_json(brief)})
        return jid

    def job(self, job_id: str):
        return self.q1("SELECT * FROM jobs WHERE id=?", (job_id,))

    def job_for_account(self, job_id: str, account_id: str):
        return self.q1("SELECT * FROM jobs WHERE id=? AND account_id=?", (job_id, account_id))

    def jobs_for_account(self, account_id: str):
        return self.q("SELECT * FROM jobs WHERE account_id=? ORDER BY created DESC", (account_id,))

    def all_jobs(self):
        return self.q("SELECT * FROM jobs ORDER BY created DESC")

    def original_brief(self, job_id: str) -> dict:
        row = self.job(job_id)
        brief = json.loads(row["brief_json"])
        if sha256_json(brief) != row["brief_sha256"]:
            raise RuntimeError(f"job {job_id}: the stored original brief no longer matches its fingerprint")
        return brief

    def transition(self, job_id: str, frm: str | tuple, to: str, *, actor: str, data: dict | None = None,
                   founder=None, **fields) -> None:
        """Compare-and-set state change. Raises StaleState if the job is not in `frm`. A founder-only exit (flow.py)
        needs `founder=` a FounderProof that still matches a live founder session; otherwise PermissionError."""
        frm_t = (frm,) if isinstance(frm, str) else tuple(frm)
        from product.authority import verify_proof
        from product.flow import can, needs_founder
        cur = self.job(job_id)
        if cur is not None and cur["state"] in frm_t and needs_founder(cur["state"], to) and not verify_proof(self, founder):
            self.event(job_id, actor, "override_refused", {"action": f"{cur['state']} -> {to}",
                                                           "why": "only the founder, signed in, can do this"})
            raise PermissionError(f"refused: {cur['state']} -> {to} is the founder's decision (caller: {actor})")
        with self.tx() as c:
            row = c.execute("SELECT state FROM jobs WHERE id=?", (job_id,)).fetchone()
            if row is None or row["state"] not in frm_t:
                raise StaleState(f"job {job_id} is {row['state'] if row else 'missing'}, not {frm_t}")
            if not can(row["state"], to):
                raise StaleState(f"job {job_id}: {row['state']} -> {to} is not a permitted transition")
            if needs_founder(row["state"], to):
                if not verify_proof(self, founder):
                    raise PermissionError(f"refused: {row['state']} -> {to} is the founder's decision (caller: {actor})")
                actor = founder.actor
            sets = ["state=?", "updated=?", "version=version+1"]
            args: list[Any] = [to, utc_now()]
            for k, v in fields.items():
                sets.append(f"{k}=?"); args.append(v)
            c.execute(f"UPDATE jobs SET {', '.join(sets)} WHERE id=?", (*args, job_id))
            self._event(c, job_id, actor, "state", {"from": row["state"], "to": to, **(data or {})})

    def set_job(self, job_id: str, **fields):
        with self.tx() as c:
            sets = ", ".join(f"{k}=?" for k in fields) + ", updated=?"
            c.execute(f"UPDATE jobs SET {sets} WHERE id=?", (*fields.values(), utc_now(), job_id))

    # ── leases (one worker per job at a time; a dead worker's lease expires) ─────
    def claim(self, states: tuple, owner: str, lease_s: int) -> sqlite3.Row | None:
        now = time.time()
        with self.tx() as c:
            marks = ",".join("?" * len(states))
            row = c.execute(f"SELECT * FROM jobs WHERE state IN ({marks}) AND lease_until < ? ORDER BY updated LIMIT 1",
                            (*states, now)).fetchone()
            if row is None:
                return None
            c.execute("UPDATE jobs SET lease_owner=?, lease_until=? WHERE id=?", (owner, now + lease_s, row["id"]))
            if row["lease_owner"] and row["lease_owner"] != owner:
                self._event(c, row["id"], "system", "lease_taken_over", {"previous": row["lease_owner"], "by": owner})
        return self.job(row["id"])

    def renew(self, job_id: str, owner: str, lease_s: int) -> bool:
        with self.tx() as c:
            cur = c.execute("UPDATE jobs SET lease_until=? WHERE id=? AND lease_owner=?", (time.time() + lease_s, job_id, owner))
            return cur.rowcount == 1

    def release(self, job_id: str, owner: str):
        with self.tx() as c:
            # the owner is cleared too: a late heartbeat can no longer re-lock a released job, and the next worker's
            # claim is not mistaken for a takeover of a dead worker's lease
            c.execute("UPDATE jobs SET lease_until=0, lease_owner=NULL WHERE id=? AND lease_owner=?", (job_id, owner))

    # ── events ──────────────────────────────────────────────────────────────────
    def _event(self, c, job_id, actor, kind, data):
        c.execute("INSERT INTO events (job_id, utc, actor, kind, data_json) VALUES (?,?,?,?,?)",
                  (job_id, utc_now(), actor, kind, json.dumps(data, ensure_ascii=False, default=str)))

    def event(self, job_id: str, actor: str, kind: str, data: dict | None = None):
        with self.tx() as c:
            self._event(c, job_id, actor, kind, data or {})

    def events(self, job_id: str, kinds: tuple | None = None):
        rows = self.q("SELECT * FROM events WHERE job_id=? ORDER BY id", (job_id,))
        return [r for r in rows if kinds is None or r["kind"] in kinds]

    # ── versioned stage artifacts (intent, direction, plan, review ...) ─────────
    def put_artifact(self, job_id: str, kind: str, data: dict, by: str) -> int:
        with self.tx() as c:
            v = c.execute("SELECT COALESCE(MAX(version),0)+1 FROM artifacts WHERE job_id=? AND kind=?", (job_id, kind)).fetchone()[0]
            c.execute("INSERT INTO artifacts (job_id, kind, version, data_json, sha256, created, created_by) VALUES (?,?,?,?,?,?,?)",
                      (job_id, kind, v, json.dumps(data, ensure_ascii=False, default=str), sha256_json(data), utc_now(), by))
            self._event(c, job_id, by, "artifact", {"kind": kind, "version": v})
        return v

    def artifact(self, job_id: str, kind: str, version: int | None = None) -> dict | None:
        if version is None:
            row = self.q1("SELECT data_json FROM artifacts WHERE job_id=? AND kind=? ORDER BY version DESC LIMIT 1", (job_id, kind))
        else:
            row = self.q1("SELECT data_json FROM artifacts WHERE job_id=? AND kind=? AND version=?", (job_id, kind, version))
        return json.loads(row["data_json"]) if row else None

    def artifact_versions(self, job_id: str, kind: str):
        return self.q("SELECT version, created, created_by, sha256 FROM artifacts WHERE job_id=? AND kind=? ORDER BY version", (job_id, kind))

    # ── ledger ──────────────────────────────────────────────────────────────────
    def committed_usd(self, job_id: str, c=None) -> Decimal:
        """Settled money plus money held by unsettled reservations."""
        c = c or self._c
        total = Decimal(0)
        for r in c.execute("SELECT reserved_usd, settled_usd, status FROM attempts WHERE job_id=?", (job_id,)):
            total += dec(r["reserved_usd"]) if r["status"] in HELD_STATUSES else dec(r["settled_usd"])
        return total

    def reserve(self, job_id: str, *, route: str, category: str, amount_usd, node_id: str | None = None,
                is_repair: bool = False) -> str:
        """Atomically: check the job budget, mint the next attempt id, write the reservation."""
        amount = dec(amount_usd)
        with self.tx() as c:
            job = c.execute("SELECT budget_usd, budget_authorised_by FROM jobs WHERE id=?", (job_id,)).fetchone()
            budget = dec(job["budget_usd"])
            if category == "provider" and not job["budget_authorised_by"]:
                raise PermissionError(f"job {job_id}: no production budget has been authorised; nothing was sent")
            committed = self.committed_usd(job_id, c)
            if committed + amount > budget:
                raise BudgetExhausted(job_id, amount, max(budget - committed, Decimal(0)), budget)
            seq = c.execute("SELECT COALESCE(MAX(seq),0)+1 FROM attempts WHERE job_id=?", (job_id,)).fetchone()[0]
            aid = f"att-{seq:04d}"
            c.execute("INSERT INTO attempts (id, job_id, seq, node_id, route, category, reserved_usd, status, is_repair, "
                      "reserved_at, started) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                      (f"{job_id}:{aid}", job_id, seq, node_id, route, category, money(amount), "reserved", int(is_repair),
                       utc_now(), time.time()))
        return f"{job_id}:{aid}"

    def mark_request(self, attempt_id: str, request_ref: str):
        with self.tx() as c:
            c.execute("UPDATE attempts SET request_ref=? WHERE id=?", (request_ref, attempt_id))

    def settle(self, attempt_id: str, *, status: str, settled_usd, failure_class: str | None = None,
               counts_against_route: bool | None = None, detail: str = ""):
        if status not in ("ok", "failed", "released", "uncertain"):
            raise ValueError(status)
        with self.tx() as c:
            row = c.execute("SELECT status FROM attempts WHERE id=?", (attempt_id,)).fetchone()
            if row is None:
                raise KeyError(attempt_id)
            if row["status"] not in HELD_STATUSES:
                raise StaleState(f"{attempt_id} already settled as {row['status']}")
            c.execute("UPDATE attempts SET status=?, settled_usd=?, failure_class=?, counts_against_route=?, detail=?, "
                      "settled_at=?, ended=? WHERE id=?",
                      (status, None if status == "uncertain" else money(settled_usd), failure_class,
                       None if counts_against_route is None else int(counts_against_route), detail[:600], utc_now(),
                       time.time(), attempt_id))

    def attempts(self, job_id: str):
        return self.q("SELECT * FROM attempts WHERE job_id=? ORDER BY seq", (job_id,))

    def ledger_summary(self, job_id: str) -> dict:
        rows = self.attempts(job_id)
        out = {"budget_usd": self.job(job_id)["budget_usd"], "committed_usd": money(self.committed_usd(job_id)),
               "by_category": {}, "attempts": len(rows), "failed": 0, "uncertain": 0, "repair_usd": "0"}
        rep = Decimal(0)
        for r in rows:
            amt = dec(r["reserved_usd"]) if r["status"] in HELD_STATUSES else dec(r["settled_usd"])
            out["by_category"][r["category"]] = money(dec(out["by_category"].get(r["category"], 0)) + amt)
            out["failed"] += r["status"] == "failed"
            out["uncertain"] += r["status"] == "uncertain"
            if r["is_repair"]:
                rep += amt
        out["repair_usd"] = money(rep)
        return out

    # ── nodes (the production asset graph) ──────────────────────────────────────
    def put_node(self, job_id: str, node_id: str, *, kind: str, deps: list, spec: dict, max_draws: int = 2,
                 cut: int = 1, status: str = "pending"):
        with self.tx() as c:
            c.execute("INSERT OR REPLACE INTO nodes (job_id, node_id, kind, deps_json, spec_json, status, draws, max_draws, "
                      "cut, updated) VALUES (?,?,?,?,?,?,0,?,?,?)",
                      (job_id, node_id, kind, json.dumps(deps), json.dumps(spec, ensure_ascii=False), status, max_draws, cut, utc_now()))

    def nodes(self, job_id: str):
        return self.q("SELECT * FROM nodes WHERE job_id=? ORDER BY rowid", (job_id,))

    def node(self, job_id: str, node_id: str):
        return self.q1("SELECT * FROM nodes WHERE job_id=? AND node_id=?", (job_id, node_id))

    def set_node(self, job_id: str, node_id: str, **fields):
        with self.tx() as c:
            sets = ", ".join(f"{k}=?" for k in fields) + ", updated=?"
            c.execute(f"UPDATE nodes SET {sets} WHERE job_id=? AND node_id=?", (*fields.values(), utc_now(), job_id, node_id))

    def take_node(self, job_id: str, node_id: str) -> bool:
        """pending -> running, atomically; False when someone else already took it."""
        with self.tx() as c:
            cur = c.execute("UPDATE nodes SET status='running', updated=? WHERE job_id=? AND node_id=? AND status='pending'",
                            (utc_now(), job_id, node_id))
            return cur.rowcount == 1

    # ── assets ──────────────────────────────────────────────────────────────────
    def add_asset(self, job_id: str, *, path: Path, kind: str, source: str, content_type: str, node_id=None,
                  role=None, attempt_id=None, status="candidate", cut=None, meta=None) -> str:
        data = Path(path).read_bytes()
        aid = new_id("ast")
        p = Path(path).resolve()
        stored = str(p.relative_to(self.root)) if p.is_relative_to(self.root) else str(p)
        with self.tx() as c:
            if c.execute("SELECT 1 FROM assets WHERE path=? OR path=?", (stored, str(p))).fetchone():
                raise WriteOnceViolation(f"{stored} already holds a registered file; every version needs its own path")
            c.execute("INSERT INTO assets VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                      (aid, job_id, node_id, kind, role, stored, sha256_bytes(data), content_type, len(data), source,
                       attempt_id, status, cut, json.dumps(meta or {}, ensure_ascii=False, default=str), utc_now()))
        return aid

    def new_output_path(self, directory: Path, stem: str, ext: str) -> Path:
        """A path no asset has used and no file occupies: <stem>-v<k>.<ext>. Files are write-once (spec §7.1)."""
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        k = 1
        while True:
            p = directory / f"{stem}-v{k}.{ext}"
            rel = str(p.resolve().relative_to(self.root)) if p.resolve().is_relative_to(self.root) else str(p.resolve())
            if not p.exists() and not self.q1("SELECT 1 FROM assets WHERE path=? OR path=?", (rel, str(p.resolve()))):
                return p
            k += 1

    def _abs(self, row):
        """Asset rows carry paths relative to the data directory; callers get an absolute path."""
        if row is None:
            return None
        d = dict(row)
        if not Path(d["path"]).is_absolute():
            d["path"] = str(self.root / d["path"])
        return d

    def asset(self, asset_id: str):
        return self._abs(self.q1("SELECT * FROM assets WHERE id=?", (asset_id,)))

    def assets(self, job_id: str, **where):
        sql = "SELECT * FROM assets WHERE job_id=?"
        args: list = [job_id]
        for k, v in where.items():
            sql += f" AND {k}=?"; args.append(v)
        return [self._abs(r) for r in self.q(sql + " ORDER BY created", args)]

    def set_asset(self, asset_id: str, **fields):
        with self.tx() as c:
            sets = ", ".join(f"{k}=?" for k in fields)
            c.execute(f"UPDATE assets SET {sets} WHERE id=?", (*fields.values(), asset_id))

    # ── verification ────────────────────────────────────────────────────────────
    def record_check(self, job_id: str, asset_id: str, *, check_id: str, status: str, blocking: bool, runner: str,
                     detail: str, evidence: dict | None = None, control_ids=()):
        if status not in ("PASS", "FAIL", "NOT_VERIFIED", "FLAG"):
            raise ValueError(status)
        a = self.asset(asset_id)
        with self.tx() as c:
            c.execute("INSERT INTO checks (job_id, asset_id, asset_sha256, check_id, status, blocking, runner, detail, "
                      "evidence_json, control_ids, created) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                      (job_id, asset_id, a["sha256"], check_id, status, int(blocking), runner, detail[:2000],
                       json.dumps(evidence or {}, ensure_ascii=False, default=str), ",".join(control_ids), utc_now()))

    def checks(self, asset_id: str):
        """Latest result per check id for this exact asset version."""
        rows = self.q("SELECT * FROM checks WHERE asset_id=? ORDER BY id", (asset_id,))
        latest = {}
        for r in rows:
            latest[r["check_id"]] = r
        return list(latest.values())

    def waive(self, job_id, asset_id, check_id, by_user, reason):
        """Low-level row write. The door guard counts a waiver only when `by_user` is a founder user id AND a matching
        founder override row exists (verify.gateway) — use Kitchen.override_check, which checks the founder's session."""
        with self.tx() as c:
            c.execute("INSERT INTO waivers (job_id, asset_id, check_id, by_user, reason, created) VALUES (?,?,?,?,?,?)",
                      (job_id, asset_id, check_id, by_user, reason, utc_now()))
            self._event(c, job_id, by_user, "waiver", {"asset_id": asset_id, "check_id": check_id, "reason": reason})

    def add_override(self, job_id: str, *, kind: str, target: str, founder, reason: str, data: dict | None = None) -> int:
        from product.authority import check_reason, verify_proof
        if not verify_proof(self, founder):
            self.event(job_id, getattr(founder, "actor", str(founder)[:60]), "override_refused",
                       {"action": f"{kind} {target}", "why": "only the founder, signed in, can do this"})
            raise PermissionError(f"refused: only the founder can override ({kind} {target})")
        reason = check_reason(reason)
        with self.tx() as c:
            oid = c.execute("INSERT INTO overrides (job_id, kind, target, founder_user_id, founder_email, reason, data_json, created) "
                            "VALUES (?,?,?,?,?,?,?,?)", (job_id, kind, target, founder.user_id, founder.email, reason,
                                                          json.dumps(data or {}, ensure_ascii=False, default=str), utc_now())).lastrowid
            self._event(c, job_id, founder.actor, "founder_override", {"id": oid, "kind": kind, "target": target, "reason": reason})
        return oid

    def overrides(self, job_id: str, kind: str | None = None):
        rows = self.q("SELECT * FROM overrides WHERE job_id=? ORDER BY id", (job_id,))
        return [r for r in rows if kind is None or r["kind"] == kind]

    def waivers(self, asset_id: str):
        return self.q("SELECT * FROM waivers WHERE asset_id=?", (asset_id,))

    # ── feedback / delivery ─────────────────────────────────────────────────────
    def add_feedback(self, job_id, *, asset_id, target, text, kind, by_user) -> int:
        with self.tx() as c:
            cur = c.execute("INSERT INTO feedback (job_id, asset_id, target, text, kind, by_user, created) VALUES (?,?,?,?,?,?,?)",
                            (job_id, asset_id, target, text, kind, by_user, utc_now()))
            return cur.lastrowid

    def feedback(self, job_id):
        return self.q("SELECT * FROM feedback WHERE job_id=? ORDER BY id", (job_id,))

    def deliver(self, job_id, asset_id, by_user):
        a = self.asset(asset_id)
        with self.tx() as c:
            c.execute("INSERT INTO deliveries (job_id, asset_id, asset_sha256, accepted_by, created) VALUES (?,?,?,?,?)",
                      (job_id, asset_id, a["sha256"], by_user, utc_now()))

    def deliveries(self, job_id):
        return self.q("SELECT * FROM deliveries WHERE job_id=? ORDER BY id", (job_id,))

    # ── timings ─────────────────────────────────────────────────────────────────
    def timing_start(self, job_id: str, phase: str, label: str = "") -> int:
        with self.tx() as c:
            return c.execute("INSERT INTO timings (job_id, phase, label, started) VALUES (?,?,?,?)",
                             (job_id, phase, label, time.time())).lastrowid

    def timing_end(self, timing_id: int):
        with self.tx() as c:
            c.execute("UPDATE timings SET ended=? WHERE id=? AND ended IS NULL", (time.time(), timing_id))

    @contextlib.contextmanager
    def timed(self, job_id: str, phase: str, label: str = ""):
        tid = self.timing_start(job_id, phase, label)
        try:
            yield
        finally:
            self.timing_end(tid)

    def timings(self, job_id: str):
        return self.q("SELECT * FROM timings WHERE job_id=? ORDER BY started", (job_id,))

    # ── reasoning calls ─────────────────────────────────────────────────────────
    def llm_start(self, job_id, *, role, provider, model, isolated, input_sha256, context_kinds, attempt_id=None,
                  **v2) -> int:
        cols = [k for k, _ in LLM_CALL_COLUMNS if k in v2]
        with self.tx() as c:
            return c.execute("INSERT INTO llm_calls (job_id, role, provider, model, isolated, input_sha256, context_kinds, "
                             f"status, attempt_id, started{''.join(', ' + k for k in cols)}) VALUES (?,?,?,?,?,?,?,?,?,?{',?' * len(cols)})",
                             (job_id, role, provider, model, int(isolated), input_sha256, ",".join(context_kinds),
                              "running", attempt_id, time.time(), *[v2[k] for k in cols])).lastrowid

    def llm_end(self, call_id, *, status, output=None, usage=None):
        with self.tx() as c:
            c.execute("UPDATE llm_calls SET status=?, output_json=?, usage_json=?, ended=? WHERE id=?",
                      (status, json.dumps(output, ensure_ascii=False, default=str) if output is not None else None,
                       json.dumps(usage or {}), time.time(), call_id))

    def llm_calls(self, job_id):
        return self.q("SELECT * FROM llm_calls WHERE job_id=? ORDER BY id", (job_id,))

    # ── judge qualification (reviewer 2026-09-24: a judge is proven only by a recorded live run, never by a setting) ──
    def record_qualification(self, *, judge: str, model: str, result: dict, report_sha256: str, founder) -> str:
        """Called only by qualification.judges.run(live=True) for a judge whose live result met the confirmed pass marks."""
        from product.authority import verify_proof
        if not verify_proof(self, founder):
            raise PermissionError("only the founder, signed in, can record a judge's qualification")
        if not result.get("qualified") or result.get("simulated_run"):
            raise ValueError("only a live run that met the confirmed pass marks can qualify a judge")
        qid = new_id("qal")
        with self.tx() as c:
            c.execute("INSERT INTO judge_qualifications (id, judge, model, report_sha256, result_json, recorded_by, recorded_at) "
                      "VALUES (?,?,?,?,?,?,?)", (qid, judge, model, report_sha256, json.dumps(result, default=str), founder.actor, utc_now()))
        return qid

    def qualification(self, judge: str, model: str | None):
        """The standing qualification of `judge` for exactly this `provider:model` (a model change voids it), or None."""
        if not model:
            return None
        return self.q1("SELECT * FROM judge_qualifications WHERE judge=? AND model=? AND revoked_at IS NULL "
                       "ORDER BY recorded_at DESC LIMIT 1", (judge, model))

    def revoke_qualification(self, judge: str, *, founder, note: str) -> int:
        from product.authority import check_reason, verify_proof
        if not verify_proof(self, founder):
            raise PermissionError("only the founder, signed in, can revoke a judge's qualification")
        note = check_reason(note)
        with self.tx() as c:
            return c.execute("UPDATE judge_qualifications SET revoked_by=?, revoked_at=?, revoke_note=? WHERE judge=? AND revoked_at IS NULL",
                             (founder.actor, utc_now(), note, judge)).rowcount
