"""EVAL-040 battery ledger: subclasses of EMP-001's spend ledger, nothing edited in place.

WHAT IS INHERITED (unchanged, by subclassing `eval/empirical-tranche-1/spend_ledger.py`)

    append-only JSONL with sequence numbers, fsync, a file lock across processes,
    `LedgerCorrupt` on any unreadable or out-of-order line, additive-only corrections
    (never negative), reserve-before-send and conservative settlement.

WHAT IS OVERRIDDEN, AND WHY (task §2.3: create / open / _check / remaining_usd / authorised_usd)

    * the tranche id is EVAL-040, and the ceiling and the two per-tranche caps (1a, 1b) come
      from an authorisation file instead of module constants, because EMP-001's constants
      (USD 10, stages qualification/atex) belong to a different authority;
    * `_check` enforces the ceiling and the per-tranche caps over `amount_usd_equiv` across
      every billing pool, so an INR reservation cannot slip past the USD-equivalent cap;
    * `reserve`/`record` additionally REQUIRE `billing_pool`, `currency` and `amount_usd_equiv`
      on every row (they validate and then call the inherited method; the append logic is not
      re-implemented). This is the one deviation from the whitelist in the task file, recorded
      in the Executor report: the invariant "every record carries billing_pool and currency"
      cannot be enforced anywhere else without editing the frozen module.

NO LIVE LEDGER FROM THE COMMITTED STATE

    `authorization.local.yaml` is gitignored and does not exist tonight; the committed
    `authorization.example.yaml` says `authorised: false`. `open_battery_ledger()` therefore
    raises `NotAuthorised` from the committed state - a test proves it.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from pathlib import Path

import hv2_paths
import spend_ledger as SL                       # read-only import from EMP-001
from budget_guard import BudgetExceeded, NotAuthorised, _require_decimal  # noqa: F401

HERE = hv2_paths.HERE
TRANCHE_ID = "EVAL-040"
MAX_PROPOSED_CEILING_USD = Decimal("175.00")    # plan §B / decision §3 rule 6
TRANCHE_NAMES = ("1a", "1b")
POOLS = ("cash", "credits", "sarvam_credits")
CURRENCIES = ("USD", "INR")
RETRIES_AUTHORISED = 0
AUTH_EXAMPLE_PATH = HERE / "authorization.example.yaml"
AUTH_LOCAL_PATH = HERE / "authorization.local.yaml"
DEFAULT_RUN_ROOT = hv2_paths.RUN_ROOT

LedgerCorrupt = SL.LedgerCorrupt


# ------------------------------------------------------------------------- authorisation
@dataclass(frozen=True)
class BatteryAuthorisation:
    authorised: bool
    tranche_id: str | None
    max_consumed_api_spend_usd: Decimal
    tranche_caps_usd: dict
    retries_authorised: int
    approved_by: str | None
    approved_at: str | None
    source_path: str
    sha256: str | None
    refusals: tuple = field(default_factory=tuple)


def load_battery_authorisation(path: Path | str = AUTH_LOCAL_PATH) -> BatteryAuthorisation:
    """Same rules as `budget_guard.load_authorisation`, applied to EVAL-040's shape.

    boolean `true` only (never a truthy string); tranche id must be EVAL-040; ceiling > 0 and
    <= the plan's USD 175; retries exactly 0; every tranche cap > 0 and <= the ceiling.
    """
    import yaml

    path = Path(path)
    if not path.exists():
        return BatteryAuthorisation(False, None, Decimal("0"), {}, 0, None, None, str(path), None,
                                    ("no authorisation file exists at that path",))
    raw = path.read_bytes()
    data = yaml.safe_load(raw.decode("utf-8")) or {}
    if not isinstance(data, dict):
        raise NotAuthorised(f"{path}: authorisation file is not a mapping")
    refusals: list[str] = []
    raw_auth = data.get("authorised", False)
    if raw_auth is not True:
        refusals.append(f"authorised is {raw_auth!r}, not the boolean true")
    tranche_id = data.get("tranche_id")
    if tranche_id != TRANCHE_ID:
        refusals.append(f"tranche_id is {tranche_id!r}, expected {TRANCHE_ID!r}")
    try:
        ceiling = Decimal(str(data.get("max_consumed_api_spend_usd", 0)))
    except (InvalidOperation, ValueError):
        ceiling = Decimal("0")
        refusals.append("max_consumed_api_spend_usd is not a number")
    else:
        if ceiling <= 0:
            refusals.append(f"max_consumed_api_spend_usd is {ceiling}, which authorises nothing")
        elif ceiling > MAX_PROPOSED_CEILING_USD:
            refusals.append(f"max_consumed_api_spend_usd {ceiling} exceeds the proposed EVAL-040 ceiling "
                            f"{MAX_PROPOSED_CEILING_USD}; raising it is a Controller decision")
    raw_retries = data.get("retries_authorised", 0)
    if raw_retries != RETRIES_AUTHORISED:
        refusals.append(f"retries_authorised is {raw_retries!r}; EVAL-040 authorises exactly 0")
    caps_raw = data.get("tranche_caps_usd") or {}
    caps: dict[str, Decimal] = {}
    if not isinstance(caps_raw, dict) or set(caps_raw) != set(TRANCHE_NAMES):
        refusals.append(f"tranche_caps_usd must name exactly {list(TRANCHE_NAMES)}")
    else:
        for name, v in caps_raw.items():
            try:
                cap = Decimal(str(v))
            except (InvalidOperation, ValueError):
                refusals.append(f"tranche cap {name} is not a number")
                continue
            if cap <= 0 or cap > ceiling:
                refusals.append(f"tranche cap {name}={cap} must be > 0 and <= the ceiling {ceiling}")
            caps[name] = cap
    return BatteryAuthorisation(
        authorised=raw_auth is True, tranche_id=tranche_id, max_consumed_api_spend_usd=ceiling,
        tranche_caps_usd=caps, retries_authorised=raw_retries if isinstance(raw_retries, int) else 0,
        approved_by=data.get("approved_by"), approved_at=data.get("approved_at"),
        source_path=str(path), sha256=hashlib.sha256(raw).hexdigest(), refusals=tuple(refusals))


# --------------------------------------------------------------------------------- run
class BatteryRun(SL.TrancheRun):
    """One EVAL-040 run directory. The run id is what spend is recorded against."""

    @classmethod
    def create(cls, root: Path | str, run_id: str, authorisation: BatteryAuthorisation,
               mode: str = "live") -> "BatteryRun":
        if authorisation.refusals:
            raise NotAuthorised("cannot create a battery run from a refused authorisation:\n  - "
                                + "\n  - ".join(authorisation.refusals))
        run_dir = Path(root) / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        record = {
            "tranche_id": TRANCHE_ID,
            "run_id": run_id,
            "created_at": SL._now(),
            "mode": mode,
            "authorisation_path": authorisation.source_path,
            "authorisation_sha256": authorisation.sha256,
            "total_ceiling_usd": str(authorisation.max_consumed_api_spend_usd),
            "tranche_caps_usd": {k: str(v) for k, v in authorisation.tranche_caps_usd.items()},
            "billing_pools": list(POOLS),
            "cap_basis": "amount_usd_equiv across every pool; INR at the COST-TABLE display rate 95.4211",
            "retries_authorised": RETRIES_AUTHORISED,
        }
        run = cls(run_dir, record)
        if not run.run_json_path.exists():
            run.run_json_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n",
                                         encoding="utf-8")
        run.ledger_path.touch()
        return cls.open(root, run_id)

    @classmethod
    def open(cls, root: Path | str, run_id: str) -> "BatteryRun":
        run_dir = Path(root) / run_id
        run_json = run_dir / "run.json"
        if not run_json.exists():
            raise LedgerCorrupt(
                f"no run record at {run_json}. Spend is recorded against a RUN; without its record "
                f"there is no way to know what has already been consumed.")
        try:
            record = json.loads(run_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise LedgerCorrupt(f"{run_json} is not readable JSON") from exc
        if record.get("tranche_id") != TRANCHE_ID or not record.get("run_id"):
            raise LedgerCorrupt(f"{run_json} does not identify an {TRANCHE_ID} run")
        try:
            Decimal(str(record["total_ceiling_usd"]))
            {k: Decimal(str(v)) for k, v in record["tranche_caps_usd"].items()}
        except (KeyError, InvalidOperation, AttributeError) as exc:
            raise LedgerCorrupt(f"{run_json} carries no readable ceiling / tranche caps") from exc
        (run_dir / "spend-ledger.jsonl").touch()
        return cls(run_dir, record)

    @property
    def ceiling_usd(self) -> Decimal:
        return Decimal(str(self.record["total_ceiling_usd"]))

    @property
    def tranche_caps(self) -> dict[str, Decimal]:
        return {k: Decimal(str(v)) for k, v in self.record["tranche_caps_usd"].items()}


# ------------------------------------------------------------------------------ budget
class BatteryBudget(SL.TrancheBudget):
    """Cumulative spend for one EVAL-040 run; the ceiling and caps are the RUN's, not constants."""

    def _check(self, stage: str, amount: Decimal) -> None:
        caps = self.run.tranche_caps
        if stage not in caps:
            raise ValueError(
                f"unknown tranche {stage!r}. EVAL-040 tranches are {sorted(caps)}; a tranche with no "
                f"declared cap must not inherit the whole ceiling.")
        committed, pending, by_stage = self._totals()
        total_after = committed + pending + amount
        ceiling = self.run.ceiling_usd
        if total_after > ceiling:
            raise BudgetExceeded(
                f"EVAL-040 ceiling: spent {committed + pending} + {amount} would reach {total_after}, "
                f"above the authorised {ceiling} (USD-equivalent across pools).")
        cap = caps[stage]
        stage_after = by_stage.get(stage, Decimal("0")) + amount
        if stage_after > cap:
            raise BudgetExceeded(
                f"tranche {stage} cap: {by_stage.get(stage, Decimal('0'))} + {amount} would reach "
                f"{stage_after}, above the authorised {cap}.")

    def remaining_usd(self) -> Decimal:
        return self.run.ceiling_usd - self.spent_usd()

    def totals_by_pool(self) -> dict[str, dict[str, Decimal]]:
        """Per-pool totals (committed + pending), native and USD-equivalent. Reported, never capped."""
        rows = self.records()
        settled = {r["reservation_id"] for r in rows
                   if r["type"] in ("spend", "release") and r.get("reservation_id")}
        out: dict[str, dict[str, Decimal]] = {}
        for r in rows:
            live = (r["type"] in ("spend", "correction")
                    or (r["type"] == "reservation" and r.get("reservation_id") not in settled))
            if not live:
                continue
            pool = r.get("billing_pool", "unknown")
            slot = out.setdefault(pool, {"native": Decimal("0"), "usd_equiv": Decimal("0"),
                                         "currency": r.get("currency", "USD")})
            slot["native"] += Decimal(str(r.get("amount_native", r.get("amount_usd"))))
            slot["usd_equiv"] += Decimal(str(r.get("amount_usd_equiv", r.get("amount_usd"))))
        return out

    def tranche(self, name: str) -> "PoolStageBudget":
        if name not in self.run.tranche_caps:
            raise ValueError(f"unknown tranche {name!r}; EVAL-040 tranches are {sorted(self.run.tranche_caps)}")
        return PoolStageBudget(self, name)


class PoolStageBudget(SL.StageBudget):
    """One tranche's (1a / 1b) view of the run budget, with pool fields required on every row."""

    @property
    def authorised_usd(self) -> Decimal:
        return self.budget.run.tranche_caps[self.stage]

    def remaining_usd(self) -> Decimal:
        tranche_left = self.budget.remaining_usd()
        cap = self.budget.run.tranche_caps[self.stage]
        return min(tranche_left, cap - self.budget.stage_spent_usd(self.stage))

    @staticmethod
    def _require_pool_fields(amount: Decimal, context: dict) -> None:
        pool = context.get("billing_pool")
        if pool not in POOLS:
            raise ValueError(f"every ledger row needs billing_pool in {POOLS}; got {pool!r}")
        if context.get("currency") not in CURRENCIES:
            raise ValueError(f"every ledger row needs currency in {CURRENCIES}; got {context.get('currency')!r}")
        usd = context.get("amount_usd_equiv")
        if usd is None:
            raise ValueError("every ledger row needs amount_usd_equiv (the amount the cap is checked over)")
        if Decimal(str(usd)) != amount:
            raise ValueError(
                f"amount_usd_equiv {usd} must equal the reserved/recorded amount {amount}: the cap is "
                f"checked over the USD-equivalent, and a row whose two amounts disagree hides money")
        if context.get("amount_native") is None:
            raise ValueError("every ledger row needs amount_native (the vendor's own currency amount)")

    def reserve(self, estimated_usd: Decimal, **context) -> str:
        _require_decimal(estimated_usd, "estimated_usd")
        self._require_pool_fields(estimated_usd, context)
        ctx = {k: (str(v) if isinstance(v, Decimal) else v) for k, v in context.items()}
        return super().reserve(estimated_usd, **ctx)

    def record(self, actual_usd: Decimal, **context) -> str:
        _require_decimal(actual_usd, "actual_usd")
        self._require_pool_fields(actual_usd, context)
        ctx = {k: (str(v) if isinstance(v, Decimal) else v) for k, v in context.items()}
        return super().record(actual_usd, **ctx)


# --------------------------------------------------------------------------- opening
def open_battery_ledger(root: Path | str = DEFAULT_RUN_ROOT, run_id: str = "eval-040-run",
                        authorisation_path: Path | str = AUTH_LOCAL_PATH,
                        mode: str = "live") -> BatteryBudget:
    """The ONLY way to obtain a live battery budget. Refuses from the committed state."""
    auth = load_battery_authorisation(authorisation_path)
    if auth.refusals:
        raise NotAuthorised(
            f"EVAL-040 paid execution is not authorised ({auth.source_path}):\n  - "
            + "\n  - ".join(auth.refusals))
    run_dir = Path(root) / run_id
    if (run_dir / "run.json").exists():
        run = BatteryRun.open(root, run_id)
    else:
        run = BatteryRun.create(root, run_id, auth, mode=mode)
    return BatteryBudget(run)


def authorisation_status(path: Path | str = AUTH_LOCAL_PATH) -> dict:
    auth = load_battery_authorisation(path)
    return {
        "path": auth.source_path, "file_exists": Path(auth.source_path).exists(),
        "authorised": auth.authorised, "tranche_id": auth.tranche_id,
        "max_consumed_api_spend_usd": str(auth.max_consumed_api_spend_usd),
        "tranche_caps_usd": {k: str(v) for k, v in auth.tranche_caps_usd.items()},
        "retries_authorised": auth.retries_authorised, "refusals": list(auth.refusals),
        "paid_execution_permitted": not auth.refusals,
    }
