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

ONE AUTHORISATION = ONE CAP, ACROSS EVERY RUN THAT USED IT (Auditor AF-4)

    A cap used to be enforced inside ONE run directory, so a second run under the same signed record was
    handed the whole cap again: `topo3-plates` + `topo3-smoke` + `topo3-video` spent USD 10.364 under a
    USD 9.96 record, and the `wan2` runs spent past their record the same way. The ledger therefore pools:
    every OTHER run under the pooling scope whose `run.json` records the SAME `authorisation_sha256` (the bytes
    of the signed record, never its filename) is counted into the ceiling, the 1a / 1b caps, the INR sub-cap,
    the credits sub-cap and the call limit - so is this run's own ledger, exactly as before. The pooling
    scope is the run root itself plus, when that root is a runner's `<out>/ledger` directory, the `ledger`
    directory of every sibling `<out>`; that is one run per `--out`, which is how the runners lay runs out.
    `BatteryRun.create` refuses outright when the pooled total has already consumed the ceiling (or the call
    limit), naming the sibling runs and the combined total, so a new run cannot dispatch at all. It fails
    CLOSED: a sibling `run.json` or ledger that cannot be read raises `LedgerCorrupt` rather than counting
    zero. Per-run numbers stay reportable (`spent_usd`, `paid_calls`) beside the pooled ones
    (`combined_spent_usd`, `combined_paid_calls`, `sibling_run_ids`).

CALLS ARE CAPPED TOO, WHEN THE RECORD SAYS SO (Auditor AF-5)

    A signed record that says "no more than N paid calls" was enforced nowhere: a fixtures run made 19 paid
    calls under a "<= 16 calls" record and a vision-judge run made 206 against 200. `max_paid_calls` is an
    OPTIONAL field of the same `machine_authorisation` block, read like every other limit - there is no call
    constant in code. Absent means the record sets NO call limit (`authorisation_status` says so in words).
    Present, it is enforced over the same pooled set of runs, and the call that would exceed it is refused
    at `reserve()`, before any dispatch.

    The `elevenlabs_credits` pool (ElevenLabs DIRECT, plan credits) is the symmetrical case: its cash amount is
    always 0 USD and its NATIVE amount is credits, capped by `elevenlabs_cap_credits`. That field is OPTIONAL in
    the authorisation file (the signed 13-field record predates it): missing = 0 = every credit call refused.

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
POOLS = ("cash", "credits", "sarvam_credits", "elevenlabs_credits")
INR_POOL = "sarvam_credits"
CREDIT_POOL = "elevenlabs_credits"                 # plan credits: cash 0 USD, native = credits, capped by elevenlabs_cap_credits
CURRENCIES = ("USD", "INR")
RETRIES_AUTHORISED = 0
PRICE_VERIFICATION_REQUIRED = "required_before_every_paid_call"
AUTH_FIELDS = ("tranche_id", "authorised", "item_basis_commit", "price_basis_roster_sha256", "max_consumed_usd_equivalent",
               "cap_1a_usd", "cap_1b_usd", "sarvam_cap_inr", "retries_authorised", "execution_time_route_price_verification",
               "images_before_video", "approved_by", "approved_at")
OPTIONAL_AUTH_FIELDS = ("elevenlabs_cap_credits",       # absent from older signed records: absent means 0 (forbidden)
                        "max_paid_calls")              # absent means the record sets NO limit on the number of paid calls
AUTH_EXAMPLE_PATH = HERE / "authorization.example.yaml"
AUTH_LOCAL_PATH = HERE / "authorization.local.yaml"
DEFAULT_RUN_ROOT = hv2_paths.RUN_ROOT
LEDGER_DIR_NAME = "ledger"    # the runners' `<out>/ledger` (run_live.LEDGER_DIR / fixtures.LEDGER_DIR); one run per --out,
                              # so the pooling scope reaches the sibling out directories' ledgers as well as this root

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
    elevenlabs_cap_credits: Decimal = Decimal("0")
    max_paid_calls: int | None = None          # None = the record names no call limit; it is never a constant in code

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
    unknown = [f for f in block if f not in AUTH_FIELDS and f not in OPTIONAL_AUTH_FIELDS and f != "media_role"]
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
        # A cap of exactly 0 is a valid signed statement: "no call in this tranche may dispatch under this
        # record" (Image Round 1 signs cap_1b_usd: 0.00). BatteryBudget._check then refuses every positive
        # reservation against it. Only a missing or negative cap is malformed.
        if cap is None or cap < 0:
            refusals.append(f"{key} {g(key)!r} is not a non-negative amount")
        elif ceiling and cap > ceiling:
            refusals.append(f"{key} {cap} exceeds max_consumed_usd_equivalent {ceiling}")
        else:
            caps[name] = cap
    inr = _dec(g("sarvam_cap_inr"))
    if inr is None or inr < 0:
        refusals.append(f"sarvam_cap_inr {g('sarvam_cap_inr')!r} is not a non-negative INR amount")
        inr = Decimal("0")
    credits = _dec(g("elevenlabs_cap_credits")) if "elevenlabs_cap_credits" in block else Decimal("0")
    if credits is None or credits < 0 or credits != credits.to_integral_value():
        refusals.append(f"elevenlabs_cap_credits {g('elevenlabs_cap_credits')!r} is not a non-negative whole number of credits")
        credits = Decimal("0")
    calls = None
    if "max_paid_calls" in block:
        raw_calls = _dec(g("max_paid_calls"))
        if raw_calls is None or raw_calls < 0 or raw_calls != raw_calls.to_integral_value():
            refusals.append(f"max_paid_calls {g('max_paid_calls')!r} is not a non-negative whole number of calls")
        else:
            calls = int(raw_calls)
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
        source_path=str(path), sha256=hashlib.sha256(raw).hexdigest(), refusals=tuple(refusals),
        elevenlabs_cap_credits=credits, max_paid_calls=calls)


def _require_permitted(auth: BatteryAuthorisation, what: str) -> None:
    if not isinstance(auth, BatteryAuthorisation):
        raise TypeError(f"{what} needs a BatteryAuthorisation (load_battery_authorisation); the ledger never trusts a run directory alone")
    if auth.refusals:
        raise NotAuthorised(f"EVAL-040 paid execution is not authorised ({auth.source_path}):\n  - " + "\n  - ".join(auth.refusals))


# ------------------------------------------------------------------- pooling (Auditor AF-4 / AF-5)
@dataclass(frozen=True)
class PooledSpend:
    """What the OTHER runs under this authorisation have already consumed. Never a guess: unreadable = refused."""
    run_ids: tuple = field(default_factory=tuple)
    usd_equiv: Decimal = Decimal("0")
    by_tranche: dict = field(default_factory=dict)
    inr_native: Decimal = Decimal("0")
    credits_native: Decimal = Decimal("0")
    paid_calls: int = 0

    @property
    def named(self) -> str:
        return ", ".join(self.run_ids) if self.run_ids else "(none)"


def pooling_scope(root: Path | str) -> list[Path]:
    """The run roots one authorisation's spend is pooled over.

    The root itself always. And, because each runner is given its own `--out` and keeps its ledger in
    `<out>/ledger/<run_id>/`, a root that IS such a `ledger` directory also pools every sibling out
    directory's `ledger`: those runs are siblings in every sense that matters to a signed cap.
    """
    root = Path(root)
    roots = [root]
    if root.name == LEDGER_DIR_NAME:
        outs = root.parent.parent
        if outs.is_dir():
            for sib in sorted(outs.iterdir()):
                if sib.is_dir() and sib != root.parent and (sib / LEDGER_DIR_NAME).is_dir():
                    roots.append(sib / LEDGER_DIR_NAME)
    return roots


def _ledger_rows(path: Path) -> list[dict]:
    """Read one OTHER run's ledger, with the same refusals the inherited reader applies to our own."""
    rows: list[dict] = []
    if not path.exists():
        return rows
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise LedgerCorrupt(f"{path} line {n} is not valid JSON; a sibling run's spend cannot be read, and counting it as zero is how a cap leaks") from exc
        if not isinstance(row, dict) or row.get("type") not in SL.RECORD_TYPES:
            raise LedgerCorrupt(f"{path} line {n}: unknown record type {row.get('type') if isinstance(row, dict) else row!r} in a sibling run's ledger")
        if row.get("seq") != len(rows) + 1:
            raise LedgerCorrupt(f"{path} line {n}: expected seq {len(rows) + 1}, found {row.get('seq')!r}; a gap in a sibling run's ledger means a record was lost")
        rows.append(row)
    return rows


def _stat_sig(path: Path) -> tuple:
    """(size, mtime) of a ledger file, so pooled totals are recomputed the moment a sibling run appends."""
    if not path.exists():
        return (-1, -1)
    st = path.stat()
    return (st.st_size, st.st_mtime_ns)


def _rows_totals(rows: list[dict]) -> dict:
    """Live totals for one ledger's rows: USD-equivalent, per tranche, native INR, native credits, paid calls."""
    settled = {r["reservation_id"] for r in rows if r["type"] in ("spend", "release") and r.get("reservation_id")}
    released = {r["reservation_id"] for r in rows if r["type"] == "release" and r.get("reservation_id")}
    usd, by_tranche, inr, credits = Decimal("0"), {}, Decimal("0"), Decimal("0")
    for r in rows:
        if not (r["type"] in ("spend", "correction") or (r["type"] == "reservation" and r.get("reservation_id") not in settled)):
            continue
        amount = Decimal(str(r.get("amount_usd", "0")))
        usd += amount
        stage = r.get("stage", "unknown")
        by_tranche[stage] = by_tranche.get(stage, Decimal("0")) + amount
        native = Decimal(str(r.get("amount_native", r.get("amount_usd", "0"))))
        if r.get("billing_pool") == INR_POOL:
            inr += native
        elif r.get("billing_pool") == CREDIT_POOL:
            credits += native
    # one paid call = one reservation that was not released, plus any spend recorded without one.
    calls = len({r["reservation_id"] for r in rows if r["type"] == "reservation" and r.get("reservation_id") not in released})
    calls += sum(1 for r in rows if r["type"] == "spend" and not r.get("reservation_id"))
    return {"usd": usd, "by_tranche": by_tranche, "inr": inr, "credits": credits, "calls": calls}


class SiblingLedgers:
    """Every OTHER run in the pooling scope that was authorised by the SAME authorisation.

    "The same" is the `authorisation_sha256` each run recorded in its `run.json` - the bytes of the signed
    record, not its filename. Editing the file in place therefore starts a NEW pool (that is what the wan2
    record did when its cap was raised mid-flight): the runs under the old bytes are still capped together,
    and the runs under the new bytes are capped together, but the two are not one pool. A cap raised in
    place is a new authorisation, and only the Controller can decide whether it re-authorises what is spent.
    """

    def __init__(self, root: Path | str, run_id: str, authorisation: BatteryAuthorisation, own_dir: Path | None = None):
        self.root = Path(root)
        self.run_id = run_id
        self.authorisation = authorisation
        self.own_dir = Path(own_dir) if own_dir is not None else self.root / run_id
        self._sig = None
        self._cached = PooledSpend()

    def _matches(self, record: dict) -> bool:
        sha = record.get("authorisation_sha256")
        return bool(sha) and sha == self.authorisation.sha256

    def runs(self) -> list[tuple[str, Path]]:
        """(run_id, run_dir) for every pooled sibling. Refuses rather than skipping what it cannot read."""
        found: list[tuple[str, Path]] = []
        for root in pooling_scope(self.root):
            if not root.is_dir():
                continue
            for run_dir in sorted(root.iterdir()):
                if not run_dir.is_dir() or run_dir.resolve() == self.own_dir.resolve():
                    continue
                run_json, ledger = run_dir / "run.json", run_dir / "spend-ledger.jsonl"
                if not run_json.exists():
                    if ledger.exists() and ledger.stat().st_size > 0:
                        raise LedgerCorrupt(f"{ledger} records spend but {run_json} is missing; a run whose authorisation cannot be identified "
                                            f"must not be assumed to be someone else's spend")
                    continue
                try:
                    record = json.loads(run_json.read_text(encoding="utf-8"))
                except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                    raise LedgerCorrupt(f"{run_json} is not readable JSON; a sibling run under this ledger root cannot be read, so the pooled "
                                        f"spend under {Path(self.authorisation.source_path).name} is unknown. Refusing rather than counting it as zero.") from exc
                if not isinstance(record, dict) or record.get("tranche_id") != TRANCHE_ID:
                    continue
                if not record.get("authorisation_sha256"):
                    raise LedgerCorrupt(f"{run_json} names no authorisation_sha256; there is no way to tell whether its spend belongs to this cap")
                if self._matches(record):
                    found.append((record.get("run_id") or run_dir.name, run_dir))
        return found

    def totals(self) -> PooledSpend:
        """Pooled totals, recomputed whenever a sibling ledger changed on disk (a concurrent run appends to it)."""
        runs = self.runs()
        sig = tuple((str(d), *_stat_sig(d / "spend-ledger.jsonl")) for _, d in runs)
        if sig == self._sig:
            return self._cached
        usd, by_tranche, inr, credits, calls = Decimal("0"), {}, Decimal("0"), Decimal("0"), 0
        for _, run_dir in runs:
            t = _rows_totals(_ledger_rows(run_dir / "spend-ledger.jsonl"))
            usd += t["usd"]
            inr += t["inr"]
            credits += t["credits"]
            calls += t["calls"]
            for stage, amount in t["by_tranche"].items():
                by_tranche[stage] = by_tranche.get(stage, Decimal("0")) + amount
        self._cached = PooledSpend(run_ids=tuple(rid for rid, _ in runs), usd_equiv=usd, by_tranche=by_tranche,
                                   inr_native=inr, credits_native=credits, paid_calls=calls)
        self._sig = sig
        return self._cached


# --------------------------------------------------------------------------------- run
class BatteryRun(SL.TrancheRun):
    """One EVAL-040 run directory. Its numbers are the AUTHORISATION's, re-validated on every open."""

    def __init__(self, run_dir: Path, record: dict, authorisation: BatteryAuthorisation):
        super().__init__(run_dir, record)
        self.authorisation = authorisation
        # the OTHER runs this authorisation already paid for; read lazily, refreshed whenever one of them appends
        self.siblings = SiblingLedgers(self.run_dir.parent, self.run_id, authorisation, own_dir=self.run_dir)

    @classmethod
    def create(cls, root: Path | str, run_id: str, authorisation: BatteryAuthorisation, mode: str = "live") -> "BatteryRun":
        _require_permitted(authorisation, "BatteryRun.create")
        run_dir = Path(root) / run_id
        # AF-4: one authorisation is ONE cap. What the sibling runs already spent under this same signed
        # record is counted BEFORE the run exists, so a new run under a consumed cap never reaches dispatch.
        pooled = SiblingLedgers(root, run_id, authorisation, own_dir=run_dir).totals()
        if pooled.usd_equiv >= authorisation.max_consumed_usd_equivalent:
            raise BudgetExceeded(
                f"EVAL-040 ceiling: the authorisation {Path(authorisation.source_path).name} has already been consumed by "
                f"{len(pooled.run_ids)} run(s) [{pooled.named}] totalling USD {pooled.usd_equiv} of the authorised "
                f"{authorisation.max_consumed_usd_equivalent}. A new run does not get the cap again; nothing was dispatched.")
        if authorisation.max_paid_calls is not None and pooled.paid_calls >= authorisation.max_paid_calls:
            raise BudgetExceeded(
                f"max_paid_calls: the authorisation {Path(authorisation.source_path).name} authorises {authorisation.max_paid_calls} paid call(s) "
                f"and {pooled.paid_calls} have already been made by run(s) [{pooled.named}]. Nothing was dispatched.")
        run_dir.mkdir(parents=True, exist_ok=True)
        record = {
            "tranche_id": TRANCHE_ID, "run_id": run_id, "created_at": SL._now(), "mode": mode,
            "authorisation_path": authorisation.source_path, "authorisation_sha256": authorisation.sha256,
            "item_basis_commit": authorisation.item_basis_commit, "price_basis_roster_sha256": authorisation.price_basis_roster_sha256,
            "total_ceiling_usd": str(authorisation.max_consumed_usd_equivalent),
            "tranche_caps_usd": {k: str(v) for k, v in authorisation.caps_usd.items()},
            "sarvam_cap_inr": str(authorisation.sarvam_cap_inr),
            "elevenlabs_cap_credits": str(authorisation.elevenlabs_cap_credits),
            "max_paid_calls": (str(authorisation.max_paid_calls) if authorisation.max_paid_calls is not None else None),
            "billing_pools": list(POOLS), "retries_authorised": RETRIES_AUTHORISED,
            "cap_basis": "amount_usd_equiv across every pool; INR at the COST-TABLE display rate 95.4211; sarvam_cap_inr over native INR; "
                         "elevenlabs_cap_credits over native plan credits (cash 0)",
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
        run = cls(run_dir, record, authorisation)
        run.siblings.totals()   # AF-4: read the pooled runs now; an unreadable sibling refuses here, not at dispatch
        return run

    @property
    def ceiling_usd(self) -> Decimal:
        return self.authorisation.max_consumed_usd_equivalent

    @property
    def tranche_caps(self) -> dict[str, Decimal]:
        return dict(self.authorisation.caps_usd)

    @property
    def sarvam_cap_inr(self) -> Decimal:
        return self.authorisation.sarvam_cap_inr

    @property
    def elevenlabs_cap_credits(self) -> Decimal:
        return self.authorisation.elevenlabs_cap_credits

    @property
    def max_paid_calls(self) -> int | None:
        """The record's call limit, or None when it names none. Never a constant in code."""
        return self.authorisation.max_paid_calls

    def pooled_spend(self) -> PooledSpend:
        """What the OTHER runs under this same authorisation have already consumed."""
        return self.siblings.totals()


# ------------------------------------------------------------------------------ budget
class BatteryBudget(SL.TrancheBudget):
    """Cumulative spend for one EVAL-040 run AND for every other run under the same authorisation.

    The ceiling and caps are the AUTHORISATION's, never constants, and they are checked over the COMBINED
    total: this run's ledger plus every pooled sibling's (Auditor AF-4). Both numbers stay reportable -
    `spent_usd()` / `paid_calls()` are this run, `combined_spent_usd()` / `combined_paid_calls()` are the cap's.
    """

    # -- pooled reading -------------------------------------------------------------------
    def pooled(self) -> PooledSpend:
        return self.run.pooled_spend()

    def sibling_run_ids(self) -> tuple:
        return self.pooled().run_ids

    def sibling_spent_usd(self) -> Decimal:
        return self.pooled().usd_equiv

    def combined_spent_usd(self) -> Decimal:
        """What the authorisation has consumed in total: this run plus every run that shares it."""
        return self.spent_usd() + self.pooled().usd_equiv

    def paid_calls(self) -> int:
        """Paid calls made by THIS run: every reservation that was not released, plus any unreserved spend."""
        rows = self.records()
        cached = getattr(self, "_calls_cache", None)     # the ledger is append-only, so a count is stable per length
        if cached is not None and cached[0] == len(rows):
            return cached[1]
        n = _rows_totals(rows)["calls"]
        self._calls_cache = (len(rows), n)
        return n

    def combined_paid_calls(self) -> int:
        return self.paid_calls() + self.pooled().paid_calls

    def _pooled_note(self, pooled: PooledSpend) -> str:
        if not pooled.run_ids:
            return ""
        return (f" Pooled with {len(pooled.run_ids)} other run(s) under {Path(self.run.authorisation.source_path).name} "
                f"[{pooled.named}] which already consumed USD {pooled.usd_equiv}.")

    # -- the caps -------------------------------------------------------------------------
    def _check(self, stage: str, amount: Decimal) -> None:
        caps = self.run.tranche_caps
        if stage not in caps:
            raise ValueError(f"unknown tranche {stage!r}. EVAL-040 tranches are {sorted(caps)}; a tranche with no declared cap must not inherit the whole ceiling.")
        committed, pending, by_stage = self._totals()
        pooled = self.pooled()
        own = committed + pending
        total_after = own + pooled.usd_equiv + amount
        ceiling = self.run.ceiling_usd
        if total_after > ceiling:
            raise BudgetExceeded(f"EVAL-040 ceiling: spent {own + pooled.usd_equiv} + {amount} would reach {total_after}, above the authorised "
                                 f"{ceiling} (USD-equivalent across pools).{self._pooled_note(pooled)}")
        cap = caps[stage]
        stage_before = by_stage.get(stage, Decimal("0")) + pooled.by_tranche.get(stage, Decimal("0"))
        stage_after = stage_before + amount
        if stage_after > cap:
            raise BudgetExceeded(f"tranche {stage} cap: {stage_before} + {amount} would reach {stage_after}, above the authorised "
                                 f"{cap}.{self._pooled_note(pooled)}")

    def _check_calls(self, new_calls: int = 1) -> None:
        """AF-5: the record's OPTIONAL call limit, over the same pooled set. Absent = no limit."""
        limit = self.run.max_paid_calls
        if limit is None:
            return
        pooled = self.pooled()
        made = self.paid_calls() + pooled.paid_calls
        if made + new_calls > limit:
            raise BudgetExceeded(f"max_paid_calls: {made} paid call(s) have been made and this call would make {made + new_calls}, above the "
                                 f"authorised {limit} in {Path(self.run.authorisation.source_path).name}. Nothing was dispatched."
                                 + (f" Pooled with run(s) [{pooled.named}], which made {pooled.paid_calls}." if pooled.run_ids else ""))

    def remaining_usd(self) -> Decimal:
        return self.run.ceiling_usd - self.combined_spent_usd()

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
        before = self.inr_native_live() + self.pooled().inr_native
        after = before + amount_native
        if after > cap:
            raise BudgetExceeded(f"sarvam_cap_inr: INR {before} + {amount_native} would reach {after}, above the authorised INR {cap}.{self._pooled_note(self.pooled())}")

    def credits_native_live(self) -> Decimal:
        return self.totals_by_pool().get(CREDIT_POOL, {}).get("native", Decimal("0"))

    def _check_credits(self, amount_native: Decimal) -> None:
        cap = self.run.elevenlabs_cap_credits
        before = self.credits_native_live() + self.pooled().credits_native
        after = before + amount_native
        if after > cap:
            raise BudgetExceeded(f"elevenlabs_cap_credits: credits {before} + {amount_native} would reach {after}, "
                                 f"above the authorised {cap} (0 = the record authorises no ElevenLabs direct call).{self._pooled_note(self.pooled())}")

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
        pooled_stage = self.budget.pooled().by_tranche.get(self.stage, Decimal("0"))
        return min(tranche_left, cap - self.budget.stage_spent_usd(self.stage) - pooled_stage)

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
        if pool == CREDIT_POOL and amount != 0:
            raise ValueError(f"pool {CREDIT_POOL} bills plan credits: the cash amount must be 0, got {amount}")

    def _inr_guard(self, context: dict, settling: bool = False) -> None:
        if context.get("billing_pool") == INR_POOL:
            native = Decimal(str(context["amount_native"]))
            if settling and self._open_reservation is not None:
                native -= Decimal(str(self._open_reservation.get("amount_native", "0")))
            if native > 0:
                self.budget._check_inr(native)

    def _credits_guard(self, context: dict, settling: bool = False) -> None:
        if context.get("billing_pool") == CREDIT_POOL:
            native = Decimal(str(context["amount_native"]))
            if settling and self._open_reservation is not None:
                native -= Decimal(str(self._open_reservation.get("amount_native", "0")))
            if native > 0:
                self.budget._check_credits(native)

    def reserve(self, estimated_usd: Decimal, **context) -> str:
        _require_decimal(estimated_usd, "estimated_usd")
        self._require_pool_fields(estimated_usd, context)
        self.budget._check_calls(1)          # AF-5: a reservation IS the call, and it is written before dispatch
        self._inr_guard(context)
        self._credits_guard(context)
        ctx = {k: (str(v) if isinstance(v, Decimal) else v) for k, v in context.items()}
        return super().reserve(estimated_usd, **ctx)

    def record(self, actual_usd: Decimal, **context) -> str:
        _require_decimal(actual_usd, "actual_usd")
        self._require_pool_fields(actual_usd, context)
        if self._open_reservation is None:   # an unreserved settlement is a call the limit has not counted yet
            self.budget._check_calls(1)
        self._inr_guard(context, settling=True)
        self._credits_guard(context, settling=True)
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
            "elevenlabs_cap_credits": str(auth.elevenlabs_cap_credits),
            "max_paid_calls": (str(auth.max_paid_calls) if auth.max_paid_calls is not None else None),
            "paid_call_limit": (f"{auth.max_paid_calls} paid calls, pooled across every run under this authorisation"
                                if auth.max_paid_calls is not None else
                                "absent: this record sets NO limit on the number of paid calls (only the USD caps apply)"),
            "roster_sha256_bound": auth.price_basis_roster_sha256 == auth.roster_sha256_on_disk,
            "retries_authorised": auth.retries_authorised, "refusals": list(auth.refusals), "paid_execution_permitted": auth.permitted}
