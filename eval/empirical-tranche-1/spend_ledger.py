#!/usr/bin/env python3
"""Durable cumulative spend for one EMP-001 run. The ceiling is a property of the TRANCHE.

WHAT WENT WRONG BEFORE

    `BudgetGuard.spent_usd` lived in memory. Qualification could open the USD 10 authorisation,
    spend most of it, and exit; A-TEXT could then reopen the SAME authorisation file and start
    again from zero. The USD 10 EMP-001 ceiling was a per-PROCESS ceiling wearing a tranche
    ceiling's clothes, and no test noticed because every test ran in one process.

    Spend is therefore recorded here, on disk, against a RUN ID — not against the authorisation
    file, and not against a live object. Deleting or replacing the authorisation file does not
    erase what was already spent, because the two are different facts: one is permission, the
    other is history.

TWO CEILINGS, BOTH FROZEN

    Total consumed API spend for EMP-001:      USD 10.00, absolute.
    Text-judge qualification, inside that:     USD  6.00, absolute.
    A-TEXT:                                    whatever qualification did not use.

    A stage cap is enforced even when the authorisation file names the full USD 10. The
    authorisation says what the tranche may spend; it does not say what a stage may spend.

RESERVE, THEN RECORD — AND PENDING COUNTS

    `reserve()` writes a reservation record before dispatch. `record()` settles it with the actual
    billed amount. Between those two moments the reservation counts against the ceiling, which is
    what stops two concurrent processes from both being told the same headroom is free.

    A reservation whose call never happened is `release()`d, so a dispatch that failed before it
    reached a provider does not permanently burn budget. Both are additive ledger records; the
    ledger is append-only and is never rewritten.

CORRECTIONS ARE ADDITIVE, AND NEVER NEGATIVE

    Real billed amounts arrive later than the call. A correction is a NEW record with an explicit
    type and reason. A negative correction is refused outright: subtracting from spend is how a
    ceiling quietly acquires headroom nobody approved.

FAIL CLOSED

    Any unreadable line, missing field, sequence gap or unknown record type raises `LedgerCorrupt`
    rather than returning a best guess. A gap means a record was lost, and guessing what it was is
    exactly how a hard limit springs a leak.

NOT COMMITTED

    The run root is gitignored. It is runtime state about money, it is machine-local, and it must
    never enter git.
"""
from __future__ import annotations

import json
import os
from contextlib import contextmanager
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

from budget_guard import BudgetExceeded

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
DEFAULT_RUN_ROOT = REPO_ROOT / "eval" / "runs" / "tranche-1"

TRANCHE_ID = "EMP-001"

# Controller-frozen. coordination/CONTROL-STATE.md.
TOTAL_CEILING_USD = Decimal("10.00")
STAGE_CAPS: dict[str, Decimal | None] = {
    "qualification": Decimal("6.00"),
    "atex": None,               # remaining tranche headroom only
}
RETRIES_AUTHORISED = 0

RECORD_TYPES = ("reservation", "spend", "release", "correction")


class LedgerCorrupt(RuntimeError):
    """The spend ledger cannot be read as a complete, ordered history. Refusing to guess."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _decimal(value, field: str) -> Decimal:
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise LedgerCorrupt(f"{field}: {value!r} is not a decimal amount") from exc


def _require_decimal(value, name: str) -> None:
    if not isinstance(value, Decimal):
        raise TypeError(
            f"{name} must be a Decimal, got {type(value).__name__}. Money is never a float here: "
            f"binary rounding inside a ceiling comparison turns a hard limit into a soft one.")


class TrancheRun:
    """Identity and paths for one EMP-001 run. The run id is what spend is recorded against."""

    def __init__(self, run_dir: Path, record: dict):
        self.run_dir = Path(run_dir)
        self.record = record
        self.run_id = record["run_id"]

    # -- paths ---------------------------------------------------------------------------
    @property
    def run_json_path(self) -> Path:
        return self.run_dir / "run.json"

    @property
    def ledger_path(self) -> Path:
        return self.run_dir / "spend-ledger.jsonl"

    @property
    def lock_path(self) -> Path:
        return self.run_dir / ".ledger.lock"

    @property
    def evidence_dir(self) -> Path:
        d = self.run_dir / "evidence"
        d.mkdir(parents=True, exist_ok=True)
        return d

    # -- lifecycle -----------------------------------------------------------------------
    @classmethod
    def create(cls, root: Path | str, run_id: str, authorisation_path: Path | str,
               mode: str = "live") -> "TrancheRun":
        run_dir = Path(root) / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        record = {
            "tranche_id": TRANCHE_ID,
            "run_id": run_id,
            "created_at": _now(),
            "mode": mode,
            "authorisation_path": str(authorisation_path),
            "total_ceiling_usd": str(TOTAL_CEILING_USD),
            "stage_caps_usd": {k: (str(v) if v is not None else None)
                               for k, v in STAGE_CAPS.items()},
            "retries_authorised": RETRIES_AUTHORISED,
        }
        run = cls(run_dir, record)
        if not run.run_json_path.exists():
            run.run_json_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n",
                                         encoding="utf-8")
        run.ledger_path.touch()
        return cls.open(root, run_id)

    @classmethod
    def open(cls, root: Path | str, run_id: str) -> "TrancheRun":
        run_dir = Path(root) / run_id
        run_json = run_dir / "run.json"
        if not run_json.exists():
            raise LedgerCorrupt(
                f"no run record at {run_json}. Spend is recorded against a RUN; without its "
                f"record there is no way to know what has already been consumed, and assuming "
                f"zero is the one answer that can overspend.")
        try:
            record = json.loads(run_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise LedgerCorrupt(f"{run_json} is not readable JSON") from exc
        if record.get("tranche_id") != TRANCHE_ID or not record.get("run_id"):
            raise LedgerCorrupt(f"{run_json} does not identify an {TRANCHE_ID} run")
        (run_dir / "spend-ledger.jsonl").touch()
        return cls(run_dir, record)

    @property
    def mode(self) -> str:
        return self.record.get("mode", "live")


class TrancheBudget:
    """Cumulative spend for one run, reconstructed from the ledger on every read."""

    def __init__(self, run: TrancheRun):
        self.run = run

    # -- locking -------------------------------------------------------------------------
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

    # -- reading -------------------------------------------------------------------------
    def records(self) -> list[dict]:
        """Parse the whole ledger, or refuse. There is no partial read."""
        path = self.run.ledger_path
        if not path.exists():
            return []

        rows: list[dict] = []
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise LedgerCorrupt(f"{path} line {n} is not valid JSON") from exc
            if not isinstance(row, dict):
                raise LedgerCorrupt(f"{path} line {n} is not a record")
            if row.get("type") not in RECORD_TYPES:
                raise LedgerCorrupt(
                    f"{path} line {n}: unknown record type {row.get('type')!r}. Known types are "
                    f"{RECORD_TYPES}; an unrecognised one may mean anything, including money.")
            if row.get("seq") != len(rows) + 1:
                raise LedgerCorrupt(
                    f"{path} line {n}: expected seq {len(rows) + 1}, found {row.get('seq')!r}. A "
                    f"gap means a record was lost, and guessing what it was is how a hard limit "
                    f"springs a leak.")
            if row["type"] in ("reservation", "spend", "correction"):
                if "amount_usd" not in row:
                    raise LedgerCorrupt(f"{path} line {n}: {row['type']} record has no amount")
                _decimal(row["amount_usd"], f"line {n} amount_usd")
            rows.append(row)
        return rows

    def _totals(self) -> tuple[Decimal, Decimal, dict[str, Decimal]]:
        """Return (committed, pending, per-stage total including pending)."""
        rows = self.records()
        settled = {r["reservation_id"] for r in rows
                   if r["type"] in ("spend", "release") and r.get("reservation_id")}

        committed = Decimal("0")
        pending = Decimal("0")
        by_stage: dict[str, Decimal] = {}

        for r in rows:
            stage = r.get("stage", "unknown")
            if r["type"] in ("spend", "correction"):
                amount = _decimal(r["amount_usd"], "amount_usd")
                committed += amount
                by_stage[stage] = by_stage.get(stage, Decimal("0")) + amount
            elif r["type"] == "reservation" and r.get("reservation_id") not in settled:
                amount = _decimal(r["amount_usd"], "amount_usd")
                pending += amount
                by_stage[stage] = by_stage.get(stage, Decimal("0")) + amount

        return committed, pending, by_stage

    def committed_usd(self) -> Decimal:
        return self._totals()[0]

    def pending_usd(self) -> Decimal:
        return self._totals()[1]

    def spent_usd(self) -> Decimal:
        """Committed plus still-outstanding reservations. Pending counts, deliberately."""
        committed, pending, _ = self._totals()
        return committed + pending

    def stage_spent_usd(self, stage: str) -> Decimal:
        return self._totals()[2].get(stage, Decimal("0"))

    def remaining_usd(self) -> Decimal:
        return TOTAL_CEILING_USD - self.spent_usd()

    # -- writing -------------------------------------------------------------------------
    def _append(self, record: dict) -> dict:
        """Append one record. Caller must hold the lock."""
        rows = self.records()
        record = {"seq": len(rows) + 1, "at": _now(), **record}
        with self.run.ledger_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, sort_keys=True) + "\n")
            fh.flush()
            os.fsync(fh.fileno())
        return record

    def _check(self, stage: str, amount: Decimal) -> None:
        """Both ceilings, in one place. Raises BudgetExceeded before anything is written."""
        if stage not in STAGE_CAPS:
            raise ValueError(
                f"unknown stage {stage!r}. EMP-001 stages are {sorted(STAGE_CAPS)}; a stage with "
                f"no declared cap must not inherit the whole tranche.")

        committed, pending, by_stage = self._totals()
        total_after = committed + pending + amount
        if total_after > TOTAL_CEILING_USD:
            raise BudgetExceeded(
                f"EMP-001 total ceiling: spent {committed + pending} + {amount} would reach "
                f"{total_after}, above the absolute {TOTAL_CEILING_USD}.")

        cap = STAGE_CAPS[stage]
        if cap is not None:
            stage_after = by_stage.get(stage, Decimal("0")) + amount
            if stage_after > cap:
                raise BudgetExceeded(
                    f"{stage} sub-cap: stage spend {by_stage.get(stage, Decimal('0'))} + "
                    f"{amount} would reach {stage_after}, above the frozen {cap}. The "
                    f"authorisation names the tranche ceiling, not a stage's.")

    def correct(self, stage: str, amount_usd: Decimal, reason: str) -> dict:
        """Additive correction. Never negative, never a rewrite of an existing record."""
        _require_decimal(amount_usd, "amount_usd")
        if amount_usd <= 0:
            raise ValueError(
                "a correction must be positive. Subtracting from recorded spend is how a ceiling "
                "quietly acquires headroom nobody approved; if a call cost less than reserved, "
                "settle it with the true amount at record() time.")
        if not reason:
            raise ValueError("a correction must carry a reason")
        with self._locked():
            self._check(stage, amount_usd)
            return self._append({"type": "correction", "stage": stage,
                                 "amount_usd": str(amount_usd), "reason": reason})

    def stage(self, name: str) -> "StageBudget":
        if name not in STAGE_CAPS:
            raise ValueError(f"unknown stage {name!r}; EMP-001 stages are {sorted(STAGE_CAPS)}")
        return StageBudget(self, name)


class StageBudget:
    """One stage's view of the tranche budget.

    Implements the same `reserve` / `record` protocol as `BudgetGuard`, so a `TextJudge` built for
    the in-memory guard works against the persistent ledger without knowing the difference.
    """

    def __init__(self, budget: TrancheBudget, stage: str):
        self.budget = budget
        self.stage = stage
        self._open_reservation: dict | None = None

    # -- the BudgetGuard protocol -----------------------------------------------------------
    @property
    def authorised_usd(self) -> Decimal:
        cap = STAGE_CAPS[self.stage]
        return cap if cap is not None else TOTAL_CEILING_USD

    @property
    def spent_usd(self) -> Decimal:
        return self.budget.stage_spent_usd(self.stage)

    def remaining_usd(self) -> Decimal:
        """The smaller of this stage's remaining cap and the tranche's remaining headroom."""
        tranche_left = self.budget.remaining_usd()
        cap = STAGE_CAPS[self.stage]
        if cap is None:
            return tranche_left
        return min(tranche_left, cap - self.budget.stage_spent_usd(self.stage))

    def reserve(self, estimated_usd: Decimal, **context) -> str:
        """Called BEFORE dispatch. Writes a reservation that counts against both ceilings."""
        _require_decimal(estimated_usd, "estimated_usd")
        if estimated_usd < 0:
            raise ValueError("a reservation cannot be negative")
        with self.budget._locked():
            self.budget._check(self.stage, estimated_usd)
            rows = self.budget.records()
            reservation_id = f"res-{len(rows) + 1:06d}"
            self._open_reservation = self.budget._append({
                "type": "reservation", "stage": self.stage,
                "reservation_id": reservation_id,
                "cost_ref": f"cost-{reservation_id}",
                "amount_usd": str(estimated_usd),
                **{k: v for k, v in context.items() if v is not None},
            })
        return reservation_id

    def record(self, actual_usd: Decimal, **context) -> str:
        """Called AFTER dispatch with the actual billed amount. Settles the open reservation."""
        _require_decimal(actual_usd, "actual_usd")
        if actual_usd < 0:
            raise ValueError(
                "a negative spend record would manufacture headroom; a correction is a new "
                "additive ledger entry, never a subtraction here")
        with self.budget._locked():
            reservation = self._open_reservation
            reservation_id = reservation["reservation_id"] if reservation else None
            # The reservation already counted; settling replaces it, so check the DELTA only.
            reserved = (_decimal(reservation["amount_usd"], "amount_usd") if reservation
                        else Decimal("0"))
            delta = actual_usd - reserved
            if delta > 0:
                self.budget._check(self.stage, delta)
            record = self.budget._append({
                "type": "spend", "stage": self.stage,
                "reservation_id": reservation_id,
                "cost_ref": (reservation["cost_ref"] if reservation
                             else f"cost-unreserved-{actual_usd}"),
                "amount_usd": str(actual_usd),
                **{k: v for k, v in context.items() if v is not None},
            })
            self._open_reservation = None
        return record["cost_ref"]

    def release(self) -> None:
        """The dispatch never happened. Give the headroom back, as a new record."""
        if not self._open_reservation:
            return
        with self.budget._locked():
            self.budget._append({
                "type": "release", "stage": self.stage,
                "reservation_id": self._open_reservation["reservation_id"],
                "reason": "dispatch did not occur",
            })
            self._open_reservation = None

    @property
    def cost_ref(self) -> str | None:
        return self._open_reservation["cost_ref"] if self._open_reservation else None
