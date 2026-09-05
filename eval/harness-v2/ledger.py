"""EVAL-040 battery ledger: subclasses of EMP-001's spend ledger, nothing edited in place.

WHAT IS INHERITED (unchanged, by subclassing `eval/empirical-tranche-1/spend_ledger.py`)

    append-only JSONL with sequence numbers, fsync, a file lock across processes, `LedgerCorrupt` on any
    unreadable or out-of-order line, additive-only corrections (never negative), reserve-before-send and
    conservative settlement.

WHERE THE NUMBERS COME FROM (Auditor AF-1 / AF-2)

    EVERY ceiling and cap comes from `authorization.local.yaml` - a file materialised from the Controller's
    signed spend record (coordination/decisions/DRAFT-SPEND-AUTHORISATION-TRANCHE-1-2026-09-05.md), whose
    `machine_authorisation` block this loader reads field for field. There is NO ceiling constant in code.
    The loader refuses when the file is absent, `authorised` is not the boolean true, `approved_by` /
    `approved_at` are empty, or `price_basis_roster_sha256` differs from the sha256 of the roster ON DISK
    (mandatory, not optional). `BatteryRun.open` takes the authorisation and re-validates on every open; it
    never takes a ceiling from `run.json`, and a run whose recorded ceiling exceeds the file's is refused.

CAPS

    `_check` enforces the ceiling and the 1a / 1b caps over `amount_usd_equiv` across every pool, and
    `PoolStageBudget.reserve/record` additionally enforce `sarvam_cap_inr` over the NATIVE INR amounts of
    the sarvam_credits pool, so neither an INR row nor a USD row can slip past either cap. `reserve` and
    `record` are overridden only to REQUIRE billing_pool / currency / amount_native / amount_usd_equiv and
    to apply the INR sub-cap; the append logic is the inherited one (MD-C14).

NO LIVE LEDGER FROM THE COMMITTED STATE

    `authorization.local.yaml` is gitignored and does not exist; the committed `authorization.example.yaml`
    says `authorised: false`. `open_battery_ledger()` therefore raises `NotAuthorised` - a test proves it.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from pathlib import Path

import hv2_paths
import spend_ledger as SL                       # read-only import from EMP-001
from budget_guard import BudgetExceeded, NotAuthorised, _require_decimal  # noqa: F401

HERE = hv2_paths.HERE
TRANCHE_ID = "EVAL-040-TRANCHE-1"
TRANCHE_NAMES = ("1a", "1b")
POOLS = ("cash", "credits", "sarvam_credits")
INR_POOL = "sarvam_credits"
CURRENCIES = ("USD", "INR")
RETRIES_AUTHORISED = 0
PRICE_VERIFICATION_REQUIRED = "required_before_every_paid_call"
AUTH_FIELDS = ("tranche_id", "authorised", "item_basis_commit", "price_basis_roster_sha256", "max_consumed_usd_equivalent",
               "cap_1a_usd", "cap_1b_usd", "sarvam_cap_inr", "retries_authorised", "execution_time_route_price_verification",
               "images_before_video", "approved_by", "approved_at")
AUTH_EXAMPLE_PATH = HERE / "authorization.example.yaml"
AUTH_LOCAL_PATH = HERE / "authorization.local.yaml"
DEFAULT_RUN_ROOT = hv2_paths.RUN_ROOT

LedgerCorrupt = SL.LedgerCorrupt


# ------------------------------------------------------------------------- authorisation
@dataclass(frozen=True)
class BatteryAuthorisation:
    authorised: bool
    tranche_id: str | None
    item_basis_commit: str | None
    price_basis_roster_sha256: str | None
    roster_sha256_on_disk: str | None
    max_consumed_usd_equivalent: Decimal
    caps_usd: dict
    sarvam_cap_inr: Decimal
    retries_authorised: int
    execution_time_route_price_verification: str | None
    images_before_video: bool | None
    approved_by: str | None
    approved_at: str | None
    source_path: str
    sha256: str | None
    refusals: tuple = field(default_factory=tuple)

    @property
    def permitted(self) -> bool:
        return not self.refusals


def _dec(v):
    try:
        return Decimal(str(v))
    except (InvalidOperation, ValueError, TypeError):
        return None


def load_battery_authorisation(path: Path | str = AUTH_LOCAL_PATH, roster_path: Path | str = hv2_paths.ROSTER) -> BatteryAuthorisation:
    """Read the `machine_authorisation` block and list every reason it would be refused. Never guesses."""
    import yaml

    path = Path(path)
    on_disk = hashlib.sha256(Path(roster_path).read_bytes()).hexdigest() if Path(roster_path).exists() else None
    blank = dict(authorised=False, tranche_id=None, item_basis_commit=None, price_basis_roster_sha256=None, roster_sha256_on_disk=on_disk,
                 max_consumed_usd_equivalent=Decimal("0"), caps_usd={}, sarvam_cap_inr=Decimal("0"), retries_authorised=0,
                 execution_time_route_price_verification=None, images_before_video=None, approved_by=None, approved_at=None,
                 source_path=str(path), sha256=None)
    if not path.exists():
        return BatteryAuthorisation(**blank, refusals=("no authorisation file exists at that path",))
    raw = path.read_bytes()
    data = yaml.safe_load(raw.decode("utf-8")) or {}
    block = data.get("machine_authorisation") if isinstance(data, dict) else None
    if not isinstance(block, dict):
        return BatteryAuthorisation(**{**blank, "sha256": hashlib.sha256(raw).hexdigest()},
                                    refusals=("the file carries no machine_authorisation mapping (the signed record's block)",))
    refusals: list[str] = []
    missing = [f for f in AUTH_FIELDS if f not in block]
    if missing:
        refusals.append(f"missing fields {missing}")
    unknown = [f for f in block if f not in AUTH_FIELDS and f != "media_role"]
    if unknown:
        refusals.append(f"unknown fields {unknown}; the loader reads exactly the signed record's field names")
    g = block.get
    if g("authorised") is not True:
        refusals.append(f"authorised is {g('authorised')!r}, not the boolean true")
    if g("tranche_id") != TRANCHE_ID:
        refusals.append(f"tranche_id is {g('tranche_id')!r}, expected {TRANCHE_ID!r}")
    ibc = g("item_basis_commit")
    if not isinstance(ibc, str) or not re.fullmatch(r"[0-9a-f]{7,40}", ibc.strip()):
        refusals.append(f"item_basis_commit {ibc!r} is not a commit sha")
    sha = g("price_basis_roster_sha256")
    if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{64}", sha):
        refusals.append("price_basis_roster_sha256 is not a sha256")
    elif on_disk is None:
        refusals.append("the roster file is missing on disk, so price_basis_roster_sha256 cannot be verified")
    elif sha != on_disk:
        refusals.append(f"price_basis_roster_sha256 {sha[:12]}... differs from the roster on disk {on_disk[:12]}...; the price basis moved")
    ceiling = _dec(g("max_consumed_usd_equivalent"))
    if ceiling is None or ceiling <= 0:
        refusals.append(f"max_consumed_usd_equivalent {g('max_consumed_usd_equivalent')!r} is not a positive amount")
        ceiling = Decimal("0")
    caps: dict[str, Decimal] = {}
    for name, key in (("1a", "cap_1a_usd"), ("1b", "cap_1b_usd")):
        cap = _dec(g(key))
        if cap is None or cap <= 0:
            refusals.append(f"{key} {g(key)!r} is not a positive amount")
        elif ceiling and cap > ceiling:
            refusals.append(f"{key} {cap} exceeds max_consumed_usd_equivalent {ceiling}")
        else:
            caps[name] = cap
    inr = _dec(g("sarvam_cap_inr"))
    if inr is None or inr < 0:
        refusals.append(f"sarvam_cap_inr {g('sarvam_cap_inr')!r} is not a non-negative INR amount")
        inr = Decimal("0")
    if g("retries_authorised") != RETRIES_AUTHORISED:
        refusals.append(f"retries_authorised is {g('retries_authorised')!r}; exactly 0 is authorised")
    if g("execution_time_route_price_verification") != PRICE_VERIFICATION_REQUIRED:
        refusals.append(f"execution_time_route_price_verification must be {PRICE_VERIFICATION_REQUIRED!r}")
    if not isinstance(g("images_before_video"), bool):
        refusals.append(f"images_before_video {g('images_before_video')!r} is not a boolean")
    for k in ("approved_by", "approved_at"):
        if not isinstance(g(k), str) or not g(k).strip():
            refusals.append(f"{k} is empty; an unsigned record authorises nothing")
    return BatteryAuthorisation(
        authorised=g("authorised") is True, tranche_id=g("tranche_id"), item_basis_commit=ibc if isinstance(ibc, str) else None,
        price_basis_roster_sha256=sha if isinstance(sha, str) else None, roster_sha256_on_disk=on_disk,
        max_consumed_usd_equivalent=ceiling, caps_usd=caps, sarvam_cap_inr=inr,
        retries_authorised=g("retries_authorised") if isinstance(g("retries_authorised"), int) else -1,
        execution_time_route_price_verification=g("execution_time_route_price_verification"),
        images_before_video=g("images_before_video") if isinstance(g("images_before_video"), bool) else None,
        approved_by=g("approved_by"), approved_at=str(g("approved_at")) if g("approved_at") else None,
        source_path=str(path), sha256=hashlib.sha256(raw).hexdigest(), refusals=tuple(refusals))


def _require_permitted(auth: BatteryAuthorisation, what: str) -> None:
    if not isinstance(auth, BatteryAuthorisation):
        raise TypeError(f"{what} needs a BatteryAuthorisation (load_battery_authorisation); the ledger never trusts a run directory alone")
    if auth.refusals:
        raise NotAuthorised(f"EVAL-040 paid execution is not authorised ({auth.source_path}):\n  - " + "\n  - ".join(auth.refusals))


# --------------------------------------------------------------------------------- run
class BatteryRun(SL.TrancheRun):
    """One EVAL-040 run directory. Its numbers are the AUTHORISATION's, re-validated on every open."""

    def __init__(self, run_dir: Path, record: dict, authorisation: BatteryAuthorisation):
        super().__init__(run_dir, record)
        self.authorisation = authorisation

    @classmethod
    def create(cls, root: Path | str, run_id: str, authorisation: BatteryAuthorisation, mode: str = "live") -> "BatteryRun":
        _require_permitted(authorisation, "BatteryRun.create")
        run_dir = Path(root) / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        record = {
            "tranche_id": TRANCHE_ID, "run_id": run_id, "created_at": SL._now(), "mode": mode,
            "authorisation_path": authorisation.source_path, "authorisation_sha256": authorisation.sha256,
            "item_basis_commit": authorisation.item_basis_commit, "price_basis_roster_sha256": authorisation.price_basis_roster_sha256,
            "total_ceiling_usd": str(authorisation.max_consumed_usd_equivalent),
            "tranche_caps_usd": {k: str(v) for k, v in authorisation.caps_usd.items()},
            "sarvam_cap_inr": str(authorisation.sarvam_cap_inr),
            "billing_pools": list(POOLS), "retries_authorised": RETRIES_AUTHORISED,
            "cap_basis": "amount_usd_equiv across every pool; INR at the COST-TABLE display rate 95.4211; sarvam_cap_inr over native INR",
            "note": "these numbers are a RECORD of the authorisation at creation; every open re-reads the authorisation file and uses the file's numbers",
        }
        run = cls(run_dir, record, authorisation)
        if not run.run_json_path.exists():
            run.run_json_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        run.ledger_path.touch()
        return cls.open(root, run_id, authorisation)

    @classmethod
    def open(cls, root: Path | str, run_id: str, authorisation: BatteryAuthorisation) -> "BatteryRun":
        _require_permitted(authorisation, "BatteryRun.open")
        run_dir = Path(root) / run_id
        run_json = run_dir / "run.json"
        if not run_json.exists():
            raise LedgerCorrupt(f"no run record at {run_json}. Spend is recorded against a RUN; without its record there is no way to know what has already been consumed.")
        try:
            record = json.loads(run_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise LedgerCorrupt(f"{run_json} is not readable JSON") from exc
        if record.get("tranche_id") != TRANCHE_ID or record.get("run_id") != run_id:
            raise LedgerCorrupt(f"{run_json} does not identify {TRANCHE_ID} run {run_id!r}")
        recorded = _dec(record.get("total_ceiling_usd"))
        if recorded is None:
            raise LedgerCorrupt(f"{run_json} carries no readable ceiling")
        if recorded > authorisation.max_consumed_usd_equivalent:
            raise NotAuthorised(f"{run_json} records a ceiling {recorded} above the authorisation file's {authorisation.max_consumed_usd_equivalent}; "
                                f"a run directory can never raise a cap")
        for name, cap in authorisation.caps_usd.items():
            rc = _dec((record.get("tranche_caps_usd") or {}).get(name))
            if rc is not None and rc > cap:
                raise NotAuthorised(f"{run_json} records cap {name}={rc} above the authorisation file's {cap}")
        (run_dir / "spend-ledger.jsonl").touch()
        return cls(run_dir, record, authorisation)

    @property
    def ceiling_usd(self) -> Decimal:
        return self.authorisation.max_consumed_usd_equivalent

    @property
    def tranche_caps(self) -> dict[str, Decimal]:
        return dict(self.authorisation.caps_usd)

    @property
    def sarvam_cap_inr(self) -> Decimal:
        return self.authorisation.sarvam_cap_inr


# ------------------------------------------------------------------------------ budget
class BatteryBudget(SL.TrancheBudget):
    """Cumulative spend for one EVAL-040 run; the ceiling and caps are the AUTHORISATION's, never constants."""

    def _check(self, stage: str, amount: Decimal) -> None:
        caps = self.run.tranche_caps
        if stage not in caps:
            raise ValueError(f"unknown tranche {stage!r}. EVAL-040 tranches are {sorted(caps)}; a tranche with no declared cap must not inherit the whole ceiling.")
        committed, pending, by_stage = self._totals()
        total_after = committed + pending + amount
        ceiling = self.run.ceiling_usd
        if total_after > ceiling:
            raise BudgetExceeded(f"EVAL-040 ceiling: spent {committed + pending} + {amount} would reach {total_after}, above the authorised {ceiling} (USD-equivalent across pools).")
        cap = caps[stage]
        stage_after = by_stage.get(stage, Decimal("0")) + amount
        if stage_after > cap:
            raise BudgetExceeded(f"tranche {stage} cap: {by_stage.get(stage, Decimal('0'))} + {amount} would reach {stage_after}, above the authorised {cap}.")

    def remaining_usd(self) -> Decimal:
        return self.run.ceiling_usd - self.spent_usd()

    def totals_by_pool(self) -> dict[str, dict[str, Decimal]]:
        """Per-pool totals (committed + pending), native and USD-equivalent."""
        rows = self.records()
        settled = {r["reservation_id"] for r in rows if r["type"] in ("spend", "release") and r.get("reservation_id")}
        out: dict[str, dict[str, Decimal]] = {}
        for r in rows:
            live = (r["type"] in ("spend", "correction") or (r["type"] == "reservation" and r.get("reservation_id") not in settled))
            if not live:
                continue
            pool = r.get("billing_pool", "unknown")
            slot = out.setdefault(pool, {"native": Decimal("0"), "usd_equiv": Decimal("0"), "currency": r.get("currency", "USD")})
            slot["native"] += Decimal(str(r.get("amount_native", r.get("amount_usd"))))
            slot["usd_equiv"] += Decimal(str(r.get("amount_usd_equiv", r.get("amount_usd"))))
        return out

    def inr_native_live(self) -> Decimal:
        return self.totals_by_pool().get(INR_POOL, {}).get("native", Decimal("0"))

    def _check_inr(self, amount_native: Decimal) -> None:
        cap = self.run.sarvam_cap_inr
        after = self.inr_native_live() + amount_native
        if after > cap:
            raise BudgetExceeded(f"sarvam_cap_inr: INR {self.inr_native_live()} + {amount_native} would reach {after}, above the authorised INR {cap}.")

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
            raise ValueError(f"amount_usd_equiv {usd} must equal the reserved/recorded amount {amount}: a row whose two amounts disagree hides money")
        if context.get("amount_native") is None:
            raise ValueError("every ledger row needs amount_native (the vendor's own currency amount)")
        if (pool == INR_POOL) != (context.get("currency") == "INR"):
            raise ValueError(f"pool {pool} and currency {context.get('currency')} disagree")

    def _inr_guard(self, context: dict, settling: bool = False) -> None:
        if context.get("billing_pool") == INR_POOL:
            native = Decimal(str(context["amount_native"]))
            if settling and self._open_reservation is not None:
                native -= Decimal(str(self._open_reservation.get("amount_native", "0")))
            if native > 0:
                self.budget._check_inr(native)

    def reserve(self, estimated_usd: Decimal, **context) -> str:
        _require_decimal(estimated_usd, "estimated_usd")
        self._require_pool_fields(estimated_usd, context)
        self._inr_guard(context)
        ctx = {k: (str(v) if isinstance(v, Decimal) else v) for k, v in context.items()}
        return super().reserve(estimated_usd, **ctx)

    def record(self, actual_usd: Decimal, **context) -> str:
        _require_decimal(actual_usd, "actual_usd")
        self._require_pool_fields(actual_usd, context)
        self._inr_guard(context, settling=True)
        ctx = {k: (str(v) if isinstance(v, Decimal) else v) for k, v in context.items()}
        return super().record(actual_usd, **ctx)


# --------------------------------------------------------------------------- opening
def open_battery_ledger(root: Path | str = DEFAULT_RUN_ROOT, run_id: str = "eval-040-run",
                        authorisation_path: Path | str = AUTH_LOCAL_PATH, mode: str = "live") -> BatteryBudget:
    """The ONLY way to obtain a live battery budget. Re-reads and re-validates the authorisation file every time."""
    auth = load_battery_authorisation(authorisation_path)
    _require_permitted(auth, "open_battery_ledger")
    run_dir = Path(root) / run_id
    run = BatteryRun.open(root, run_id, auth) if (run_dir / "run.json").exists() else BatteryRun.create(root, run_id, auth, mode=mode)
    return BatteryBudget(run)


def authorisation_status(path: Path | str = AUTH_LOCAL_PATH) -> dict:
    auth = load_battery_authorisation(path)
    return {"path": auth.source_path, "file_exists": Path(auth.source_path).exists(), "authorised": auth.authorised,
            "tranche_id": auth.tranche_id, "max_consumed_usd_equivalent": str(auth.max_consumed_usd_equivalent),
            "caps_usd": {k: str(v) for k, v in auth.caps_usd.items()}, "sarvam_cap_inr": str(auth.sarvam_cap_inr),
            "roster_sha256_bound": auth.price_basis_roster_sha256 == auth.roster_sha256_on_disk,
            "retries_authorised": auth.retries_authorised, "refusals": list(auth.refusals), "paid_execution_permitted": auth.permitted}
