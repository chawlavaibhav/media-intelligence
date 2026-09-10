"""The price side of a route decision. Wraps the harness; invents nothing; opens no socket.

WHERE A PRICE COMES FROM, AND WHERE IT MUST NOT COME FROM

    NOT from the routing evidence map. The map carries `unit_price_usd_pinned` and per-question cost
    figures, and they are HISTORY: the numbers were recorded against the surface each draw actually
    ran on, and the roster has since re-pointed four Gemini-named routes off Vertex and fal onto the
    Gemini Developer API. The map still says `surface: vertex` for nano-banana-2. A runtime that read
    the map's price would quote a customer a price from a surface it is no longer calling.

    The price comes from the ROSTER, re-read from disk at every decision, through the harness's own
    reader (`eval/harness-v2/pricing.py`), which is the same code the Lab prices its calls with:

        map cell.route_key
          -> eval/harness-v2/surfaces.py       which roster row and variant this route is
          -> pricing.Roster.record(...)        the price-bearing record (route | variant | fallback)
          -> pricing.unit_price_for(...)       the roster-implied unit price, addons included
          -> pricing.quantity_for(...)         the billing quantity for one call
          -> price pin index                   the pin must exist, be a `price` pin, and be on disk

    The last step is what the supersession note costs us: the master PIN-INDEX does not list the
    Gemini Developer API pricing page and has NO entry at all for wan-2.2-a14b, whose pins live in
    their own sub-indexes. So the pin check reads every PIN-INDEX under the pin root, master and sub.

A ROUTE WITH NO LIVE PIN IS NEVER AUTO-SELECTED

    "Live" here means all of: the roster row's `route_status` is `pinned`; the roster carries a
    regular price in a unit that can be projected onto one call (a promotional price is never used —
    that rule is the roster's, not ours); the pin file the roster names is listed as a `price` pin in
    some pin index; and those bytes are actually present in this checkout.

IMPORTING THE HARNESS IN A SPARSE CHECKOUT

    `pricing.py` imports `providers` from `eval/empirical-tranche-1/`, which this worktree's sparse
    checkout does not materialise. Rather than copy the roster reader (which would be a second
    opinion about prices, the exact thing this project keeps refusing to build), a minimal stand-in
    module is installed for that ONE imported name when it is missing, and the decision records that
    it happened. The price logic executed is the harness's own, unchanged.
"""
from __future__ import annotations

import sys
import types
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path

import yaml

PIN_INDEX_NAME = "PIN-INDEX.yaml"


class PriceError(RuntimeError):
    pass


# --------------------------------------------------------------------------- harness bridge
_BRIDGE: dict = {}


def harness(root: Path) -> dict:
    """Import the harness pricing + surface modules once. No network, no key, no provider call."""
    if _BRIDGE:
        return _BRIDGE
    hv2 = Path(root) / "eval" / "harness-v2"
    if not hv2.is_dir():
        raise PriceError(f"{hv2} is not in this checkout; the router prices through the harness")
    if str(hv2) not in sys.path:
        sys.path.insert(0, str(hv2))
    import hv2_paths  # noqa: F401  (puts the frozen packages on sys.path, no side effect beyond that)

    stubbed = False
    try:
        import providers  # noqa: F401
    except ModuleNotFoundError:
        mod = types.ModuleType("providers")

        class PreDispatchRefusal(RuntimeError):
            """Stand-in for the frozen EMP-001 name, present only when that tree is not checked out."""

        mod.PreDispatchRefusal = PreDispatchRefusal
        sys.modules["providers"] = mod
        stubbed = True

    import pricing
    import surfaces
    _BRIDGE.update({"pricing": pricing, "surfaces": surfaces,
                    "surface_registry": surfaces.SurfaceRegistry(),
                    "providers_stubbed": stubbed,
                    "modules": [str(Path(pricing.__file__)), str(Path(surfaces.__file__))]})
    return _BRIDGE


# --------------------------------------------------------------------------- pins
class PinBook:
    """Every price pin the project has recorded, master index and sub-indexes together."""

    def __init__(self, pin_root: Path):
        self.pin_root = Path(pin_root)
        self.by_file: dict[str, list[dict]] = {}
        self.indexes: list[str] = []
        for index in sorted(self.pin_root.rglob(PIN_INDEX_NAME)):
            data = yaml.safe_load(index.read_text(encoding="utf-8")) or {}
            self.indexes.append(str(index))
            for pin in data.get("pins") or []:
                self.by_file.setdefault(str(pin.get("pin_file")), []).append(
                    {"index": str(index), "pin_kind": pin.get("pin_kind"),
                     "evidence_quote": pin.get("evidence_quote"), "url": pin.get("url"),
                     "route_key": pin.get("route_key")})

    def check(self, root: Path, pin_ref: str | None) -> dict:
        if not pin_ref:
            return {"live": False, "reason": "the roster names no price pin for this route"}
        entries = self.by_file.get(pin_ref, [])
        priced = [e for e in entries if e.get("pin_kind") == "price"]
        if not entries:
            return {"live": False, "pin_ref": pin_ref, "indexes": [],
                    "reason": f"pin {pin_ref} is named by the roster but listed in no PIN-INDEX under "
                              f"{self.pin_root}"}
        if not priced:
            kinds = sorted({e.get("pin_kind") for e in entries})
            return {"live": False, "pin_ref": pin_ref, "indexes": [e["index"] for e in entries],
                    "reason": f"pin {pin_ref} is indexed only as {kinds!r}; a page_only or schema_page "
                              f"pin carries no price for this id"}
        if not (Path(root) / pin_ref).exists():
            return {"live": False, "pin_ref": pin_ref, "indexes": [e["index"] for e in priced],
                    "reason": f"pin {pin_ref} is indexed as a price pin but its bytes are not in this checkout"}
        return {"live": True, "pin_ref": pin_ref, "indexes": [e["index"] for e in priced],
                "evidence_quote": priced[0].get("evidence_quote"), "url": priced[0].get("url")}


# --------------------------------------------------------------------------- quotes
@dataclass
class Quote:
    route_key: str
    priced: bool
    reason: str = ""
    surface: str | None = None
    surface_model_id: str | None = None
    adapter: str | None = None
    credential_name: str | None = None
    roster_key: str | None = None
    roster_variant: str | None = None
    route_status: str | None = None
    unit: str | None = None
    unit_price: Decimal | None = None
    currency: str = "USD"
    quantity: Decimal | None = None
    quantity_unit: str | None = None
    quantity_rule: str | None = None
    expected_cost_usd: Decimal | None = None
    billing_pool: str | None = None
    price_pin_ref: str | None = None
    pin_indexes: list = field(default_factory=list)
    pin_evidence_quote: str | None = None
    unit_price_note: str = ""
    conversion_note: str = ""

    def as_dict(self) -> dict:
        d = {k: v for k, v in self.__dict__.items()}
        for k in ("unit_price", "quantity", "expected_cost_usd"):
            if d[k] is not None:
                d[k] = str(d[k])
        return d


class PriceBook:
    """Roster + pins + the harness's own price rules. Re-reads the roster at every decision."""

    def __init__(self, root: Path, roster_path: Path, pin_root: Path):
        self.root = Path(root)
        self.roster_path = Path(roster_path)
        self.pin_root = Path(pin_root)
        self.bridge = harness(self.root)
        self.pricing = self.bridge["pricing"]
        self.surfaces = self.bridge["surface_registry"]
        self.roster = self.pricing.Roster(self.roster_path)      # fresh read, by design
        self.pins = PinBook(self.pin_root)

    def _rel(self, path) -> str:
        try:
            return str(Path(path).relative_to(self.root))
        except ValueError:
            return str(path)

    @property
    def provenance(self) -> dict:
        return {"roster": self._rel(self.roster_path),
                "roster_sha256": self.roster.sha256,
                "pin_indexes_read": len(self.pins.indexes),
                "harness_modules": [self._rel(m) for m in self.bridge["modules"]],
                "harness_providers_stubbed": self.bridge["providers_stubbed"],
                "map_prices_used": False,
                "map_prices_note": "the routing map's unit_price_usd_pinned and per-question cost "
                                   "figures are never read as prices; they were measured on surfaces "
                                   "the roster has since re-pointed"}

    def quote(self, route_key: str, case_row: dict) -> Quote:
        try:
            entry = self.surfaces.get(route_key)
        except Exception as exc:                              # noqa: BLE001 - reported, not raised
            return Quote(route_key=route_key, priced=False,
                         reason=f"no surface entry for {route_key!r} in the harness registry: {exc}")

        rec = self.roster.record(entry.roster_key, entry.roster_variant)
        rp = rec.get("regular_price") or {}
        unit = rp.get("unit")
        currency = rp.get("currency") or "USD"
        q = Quote(route_key=route_key, priced=False, surface=rec.get("surface") or entry.surface,
                  surface_model_id=rec.get("surface_model_id") or entry.surface_model_id,
                  adapter=entry.adapter, credential_name=entry.key_name,
                  roster_key=entry.roster_key, roster_variant=entry.roster_variant,
                  route_status=rec.get("route_status"), unit=unit, currency=currency,
                  billing_pool=rec.get("billing_pool") or entry.billing_pool,
                  price_pin_ref=rec.get("pin_ref"))

        pin = self.pins.check(self.root, q.price_pin_ref)
        q.pin_indexes = [self._rel(i) for i in pin.get("indexes", [])]
        q.pin_evidence_quote = pin.get("evidence_quote")
        if not pin["live"]:
            q.reason = pin["reason"]
            return q
        if q.route_status != "pinned":
            q.reason = (f"the roster records route_status={q.route_status!r} for "
                        f"{entry.roster_key}/{entry.roster_variant}: the price is known but the route "
                        f"cannot be called until that is resolved")
            return q

        unit_price, note = self.pricing.unit_price_for(route_key, rec, case_row)
        q.unit_price_note = note
        if unit_price is None:
            q.reason = f"no projectable unit price in the roster: {note}"
            return q

        qty = self.pricing.quantity_for(route_key, unit, case_row)
        if qty is None:
            q.reason = (f"the billing quantity for one call in unit {unit!r} cannot be read from this "
                        f"spec; the runtime refuses to estimate one")
            return q
        q.quantity, q.quantity_unit, q.quantity_rule = qty

        native = (unit_price * q.quantity)
        if currency == "USD":
            q.expected_cost_usd = self.pricing._round6(native)
        elif currency == "INR":
            rate = self.pricing.INR_USD_DISPLAY_RATE
            q.expected_cost_usd = self.pricing._round6(native / rate)
            q.conversion_note = (f"INR invoiced; USD equivalent at the COST-TABLE display rate "
                                 f"{rate} (a display convention, not an FX quote)")
        else:
            q.reason = f"currency {currency!r} has no declared USD conversion; the runtime refuses to guess one"
            return q

        q.unit_price = unit_price
        q.priced = True
        q.reason = (f"roster {entry.roster_key}"
                    + (f" variant {entry.roster_variant}" if entry.roster_variant else "")
                    + f", {unit_price} {currency} {unit} x {q.quantity} {q.quantity_unit}")
        return q
