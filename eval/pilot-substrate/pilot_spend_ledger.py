#!/usr/bin/env python3
"""EVAL-035: persistent, append-only spend ledger for the PILOT-001 tranche.

WHY THIS EXISTS (Controller correction 2, CONTROLLER-EVAL-035-RETURN-REVIEW-2-2026-08-28)

    The previous pass handed live dispatch an in-memory `BudgetGuard`. EMP-001 already paid
    to learn why that is wrong: process-local spend state resets across processes, so a
    tranche ceiling silently becomes a per-process ceiling. And the in-memory guard's
    `record()` returns no cost reference, while RES-007 requires every provider attempt's
    `cost_ref` to resolve to an immutable cost-ledger row.

    This module is the PILOT-001 equivalent of EMP-001's accepted durable ledger
    (eval/empirical-tranche-1/spend_ledger.py), reusing its semantics as design precedent
    WITHOUT touching EMP-001's frozen tranche id, ceiling, stages, history or records:

      * append-only JSONL, one record per line, sequence-numbered from 1;
      * reserve BEFORE dispatch — the reservation counts against the ceiling immediately,
        which is what stops two processes from both being told the same headroom is free;
      * settle AFTER dispatch under the SAME stable `cost_ref` the reservation created;
      * release ONLY on provably pre-dispatch failure, as a new record — never a rewrite;
      * ambiguous post-dispatch outcomes settle conservatively and never release;
      * reopening a run reconstructs committed + pending spend from disk — never zero;
      * any unreadable line, unknown type, sequence gap or shrunken file raises
        `LedgerCorrupt` rather than returning a best guess;
      * an OS file lock serialises reserve/settle across processes on this machine.

WHERE THE CEILING COMES FROM

    Not from this module. `open_pilot_runtime()` first verifies the full PILOT-001
    authority chain (`pilot_authorisation.verify_authority`): a COMMITTED Controller
    decision carrying a machine-readable authorisation block, matched by the local runtime
    file. The run's ceiling is the verified LOCAL ceiling (never above the committed cap).
    No such committed decision exists today, so no live runtime can be opened from the
    committed repository state — tests prove it.

NOT COMMITTED

    Run roots live under the git-ignored `eval/runs/`. Runtime state about money is
    machine-local and never enters git. Deleting the authorisation file does not erase
    what a run already spent: permission and history are different facts.
"""
from __future__ import annotations

import json
import os
import sys
from contextlib import contextmanager
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
EMP001 = HERE.parent / "empirical-tranche-1"
if str(EMP001) not in sys.path:
    sys.path.insert(0, str(EMP001))
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from budget_guard import BudgetExceeded  # noqa: E402

import pilot_authorisation as PA  # noqa: E402

TRANCHE_ID = "PILOT-001"
DEFAULT_RUN_ROOT = REPO_ROOT / "eval" / "runs" / "pilot-001"
RECORD_TYPES = ("reservation", "spend", "release")


class LedgerCorrupt(RuntimeError):
    """The spend ledger cannot be read as a complete, ordered history. Refusing to guess."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _decimal(value, field: str) -> Decimal:
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise LedgerCorrupt(f"{field}: {value!r} is not a decimal amount") from exc


def _require_decimal(value, name: str) -> None:
    if not isinstance(value, Decimal):
        raise TypeError(
            f"{name} must be a Decimal, got {type(value).__name__}. Money is never a "
            f"float here: binary rounding inside a ceiling comparison turns a hard limit "
            f"into a soft one.")


class PilotRun:
    """Identity and paths for one PILOT-001 run. Spend is recorded against the run id."""

    def __init__(self, run_dir: Path, record: dict):
        self.run_dir = Path(run_dir)
        self.record = record
        self.run_id = record["run_id"]

    @property
    def run_json_path(self) -> Path:
        return self.run_dir / "run.json"

    @property
    def ledger_path(self) -> Path:
        return self.run_dir / "spend-ledger.jsonl"

    @property
    def lock_path(self) -> Path:
        return self.run_dir / ".ledger.lock"

    @classmethod
    def create(cls, root: Path | str, run_id: str, ceiling_usd: Decimal,
               decision_ref: str, authorisation_path: str) -> "PilotRun":
        _require_decimal(ceiling_usd, "ceiling_usd")
        run_dir = Path(root) / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        record = {
            "tranche_id": TRANCHE_ID,
            "run_id": run_id,
            "created_at": _now(),
            "authorised_ceiling_usd": str(ceiling_usd),
            "decision_ref": decision_ref,
            "authorisation_path": str(authorisation_path),
            "retries_authorised": 0,
        }
        run_json = run_dir / "run.json"
        if run_json.exists():
            raise LedgerCorrupt(
                f"{run_json} already exists; create() must not overwrite a run record. "
                f"Open the existing run instead — its history is the truth.")
        run_json.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n",
                            encoding="utf-8")
        (run_dir / "spend-ledger.jsonl").touch()
        return cls.open(root, run_id)

    @classmethod
    def open(cls, root: Path | str, run_id: str) -> "PilotRun":
        run_dir = Path(root) / run_id
        run_json = run_dir / "run.json"
        if not run_json.exists():
            raise LedgerCorrupt(
                f"no run record at {run_json}. Spend is recorded against a RUN; without "
                f"its record there is no way to know what has already been consumed, and "
                f"assuming zero is the one answer that can overspend.")
        try:
            record = json.loads(run_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise LedgerCorrupt(f"{run_json} is not readable JSON") from exc
        if record.get("tranche_id") != TRANCHE_ID or not record.get("run_id"):
            raise LedgerCorrupt(f"{run_json} does not identify a {TRANCHE_ID} run")
        _decimal(record.get("authorised_ceiling_usd"), "authorised_ceiling_usd")
        (run_dir / "spend-ledger.jsonl").touch()
        return cls(run_dir, record)

    @property
    def ceiling_usd(self) -> Decimal:
        return _decimal(self.record["authorised_ceiling_usd"], "authorised_ceiling_usd")


class PilotBudget:
    """Durable spend for one PILOT-001 run, reconstructed from the ledger on every read.

    Implements the same `reserve` / `record` / `release` protocol as the in-memory
    `BudgetGuard`, so the route works against it without knowing the difference — but
    `record()` returns a stable `cost_ref` that survives reservation → settlement and
    resolves to this ledger's rows.
    """

    def __init__(self, run: PilotRun):
        self.run = run
        # Append-only: bytes already parsed can never legitimately change. The offset
        # also detects in-process truncation — a shorter file means rewritten history.
        self._cache: list[dict] = []
        self._offset: int = 0
        self._open_reservation: dict | None = None

    # -- locking -----------------------------------------------------------------------
    @contextmanager
    def _locked(self):
        """Serialise read-modify-append across processes on this machine."""
        import fcntl

        self.run.lock_path.parent.mkdir(parents=True, exist_ok=True)
        with self.run.lock_path.open("a+") as fh:
            fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(fh.fileno(), fcntl.LOCK_UN)

    # -- reading -----------------------------------------------------------------------
    def records(self) -> list[dict]:
        """Parse the whole ledger, or refuse. There is no partial read."""
        path = self.run.ledger_path
        if not path.exists():
            raise LedgerCorrupt(f"{path} is missing; an absent history is not an empty one")

        size = path.stat().st_size
        if size < self._offset:
            raise LedgerCorrupt(
                f"{path} shrank from {self._offset} to {size} bytes. The spend ledger is "
                f"append-only; a shorter file means history was rewritten or truncated.")
        if size == self._offset:
            return self._cache

        with path.open("r", encoding="utf-8") as fh:
            fh.seek(self._offset)
            fresh = fh.read()
            consumed = self._offset + len(fresh.encode("utf-8"))

        rows = self._cache
        for line in fresh.splitlines():
            if not line.strip():
                continue
            n = len(rows) + 1
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise LedgerCorrupt(f"{path} line {n} is not valid JSON") from exc
            if not isinstance(row, dict):
                raise LedgerCorrupt(f"{path} line {n} is not a record")
            if row.get("type") not in RECORD_TYPES:
                raise LedgerCorrupt(
                    f"{path} line {n}: unknown record type {row.get('type')!r}. Known "
                    f"types are {RECORD_TYPES}; an unrecognised one may mean anything, "
                    f"including money.")
            if row.get("seq") != n:
                raise LedgerCorrupt(
                    f"{path} line {n}: expected seq {n}, found {row.get('seq')!r}. A gap "
                    f"means a record was lost, and guessing what it was is how a hard "
                    f"limit springs a leak.")
            if row["type"] in ("reservation", "spend"):
                if "amount_usd" not in row:
                    raise LedgerCorrupt(f"{path} line {n}: {row['type']} record has no "
                                        f"amount")
                _decimal(row["amount_usd"], f"line {n} amount_usd")
                if not row.get("cost_ref"):
                    raise LedgerCorrupt(f"{path} line {n}: {row['type']} record has no "
                                        f"cost_ref; an anonymous cost cannot be handed "
                                        f"to Resources")
            rows.append(row)

        self._offset = consumed
        return rows

    def _totals(self) -> tuple[Decimal, Decimal]:
        """(committed, pending). Pending = reservations neither settled nor released."""
        rows = self.records()
        settled = {r.get("reservation_id") for r in rows
                   if r["type"] in ("spend", "release") and r.get("reservation_id")}
        committed = Decimal("0")
        pending = Decimal("0")
        for r in rows:
            if r["type"] == "spend":
                committed += _decimal(r["amount_usd"], "amount_usd")
            elif r["type"] == "reservation" and r["reservation_id"] not in settled:
                pending += _decimal(r["amount_usd"], "amount_usd")
        return committed, pending

    def committed_usd(self) -> Decimal:
        return self._totals()[0]

    def pending_usd(self) -> Decimal:
        return self._totals()[1]

    @property
    def spent_usd(self) -> Decimal:
        """Committed plus still-outstanding reservations. Pending counts, deliberately."""
        committed, pending = self._totals()
        return committed + pending

    @property
    def authorised_usd(self) -> Decimal:
        return self.run.ceiling_usd

    def remaining_usd(self) -> Decimal:
        return self.run.ceiling_usd - self.spent_usd

    # -- writing -----------------------------------------------------------------------
    def _append(self, record: dict) -> dict:
        """Append one record. Caller must hold the lock."""
        rows = self.records()
        record = {"seq": len(rows) + 1, "at": _now(), **record}
        with self.run.ledger_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, sort_keys=True) + "\n")
            fh.flush()
            os.fsync(fh.fileno())
        return record

    def _check(self, amount: Decimal) -> None:
        committed, pending = self._totals()
        after = committed + pending + amount
        if after > self.run.ceiling_usd:
            raise BudgetExceeded(
                f"{TRANCHE_ID} ceiling: committed {committed} + pending {pending} + "
                f"{amount} would reach {after}, above the authorised "
                f"{self.run.ceiling_usd}.")

    def reserve(self, estimated_usd: Decimal, **context) -> str:
        """Called BEFORE dispatch. Persists a reservation that counts against the cap."""
        _require_decimal(estimated_usd, "estimated_usd")
        if estimated_usd < 0:
            raise ValueError("a reservation cannot be negative")
        with self._locked():
            self._check(estimated_usd)
            rows = self.records()
            reservation_id = f"res-{len(rows) + 1:06d}"
            self._open_reservation = self._append({
                "type": "reservation",
                "reservation_id": reservation_id,
                "cost_ref": f"pilot-cost-{reservation_id}",
                "amount_usd": str(estimated_usd),
                **{k: v for k, v in context.items() if v is not None},
            })
        return reservation_id

    def record(self, actual_usd: Decimal, **context) -> str:
        """Called AFTER dispatch. Settles the open reservation under its stable cost_ref."""
        _require_decimal(actual_usd, "actual_usd")
        if actual_usd < 0:
            raise ValueError(
                "a negative spend record would manufacture headroom; a correction is a "
                "new additive ledger entry, never a subtraction here")
        with self._locked():
            reservation = self._open_reservation
            reservation_id = reservation["reservation_id"] if reservation else None
            # The reservation already counts; settling replaces it, so check the DELTA.
            reserved = (_decimal(reservation["amount_usd"], "amount_usd") if reservation
                        else Decimal("0"))
            delta = actual_usd - reserved
            if delta > 0:
                self._check(delta)
            rows = self.records()
            record = self._append({
                "type": "spend",
                "reservation_id": reservation_id,
                "cost_ref": (reservation["cost_ref"] if reservation
                             else f"pilot-cost-unreserved-{len(rows) + 1:06d}"),
                "amount_usd": str(actual_usd),
                **{k: v for k, v in context.items() if v is not None},
            })
            self._open_reservation = None
        return record["cost_ref"]

    def release(self) -> None:
        """The dispatch provably never happened. Give the headroom back, additively."""
        if not self._open_reservation:
            return
        with self._locked():
            self._append({
                "type": "release",
                "reservation_id": self._open_reservation["reservation_id"],
                "reason": "dispatch did not occur",
            })
            self._open_reservation = None

    @property
    def cost_ref(self) -> str | None:
        return self._open_reservation["cost_ref"] if self._open_reservation else None


def open_pilot_runtime(root: Path | str, run_id: str,
                       authorisation_path: Path | str = PA.PILOT_AUTHORISATION_PATH,
                       decisions_dir: Path = PA.DECISIONS_DIR) -> PilotBudget:
    """The ONLY supported way to obtain a live PILOT-001 spend guard.

    Verifies the full authority chain first (committed Controller machine-authorisation
    block + matching local runtime file — fails closed today, because no committed
    authorising decision exists), then opens or creates the persistent run. Reopening an
    existing run reconstructs prior committed and pending spend from disk; it never resets
    to zero. A run whose recorded ceiling no longer matches the currently verified
    authority fails closed rather than picking either number.
    """
    authority = PA.verify_authority(authorisation_path, decisions_dir)
    ceiling = authority["max_consumed_api_spend_usd"]
    run_dir = Path(root) / run_id
    if run_dir.joinpath("run.json").exists():
        run = PilotRun.open(root, run_id)
        if run.ceiling_usd != ceiling:
            raise LedgerCorrupt(
                f"run {run_id} was created with ceiling {run.ceiling_usd} but the "
                f"currently verified authority says {ceiling}. A ceiling that changed "
                f"mid-run needs a Controller decision, not a guess about which number "
                f"governs.")
    else:
        run = PilotRun.create(root, run_id, ceiling_usd=ceiling,
                              decision_ref=str(authority["committed"]["decision_path"]),
                              authorisation_path=str(authorisation_path))
    return PilotBudget(run)
