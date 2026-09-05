"""Roster + COST-TABLE reader and the execution-time price check.

WHAT THIS DOES, IN PLAIN ENGLISH

    Before any money is reserved for a call, the harness re-reads the September roster
    (`ROSTER-REFRESH-2026-09.yaml`) from disk and works out, from the roster's own pinned
    numbers and the billing rules the freeze package wrote down, what ONE call of this route
    for this case should cost. If the case row disagrees with the roster, or the roster does
    not carry a pinned regular price, or the billing quantity rule is unknown, the call is
    REFUSED before anything is reserved or sent (`PreDispatchRefusal`). A promotional price is
    never used. Nothing here contacts a provider.

QUANTITY RULES (verbatim sources)

    per_image                one output image per call                     roster billing_unit_verbatim
    per_second               the row's billed seconds (duration_s)          roster billing_unit_verbatim
    kling_lipsync_5s_rollup  input seconds rolled up to the next 5 s        COST-TABLE.rules[6]
    elevenlabs_music_minute  output minutes rounded up                      COST-TABLE.rules[6]
    veo_extend_15s           8 s + 7 s over two API calls in ONE trial      roster variant extend-15s / task §2.2
    per_1000_characters      characters / 1000 (ElevenLabs USD; Sarvam INR) roster billing_unit_verbatim
    per_clip                 one 30-s clip per call (Lyria)                 roster billing_unit_verbatim
    flux_edit_addon          0.03 first output MP + 0.015 per input MP      roster price_addons (flux-2-pro-edit)

INR

    Sarvam invoices in INR. The reservation is kept in INR (`amount_native`) and carries a
    USD-equivalent (`amount_usd_equiv`) at the display rate the COST-TABLE names (95.4211,
    `INR->USD display rate ... from the August file`) so the USD-equivalent cap can be checked
    across pools. That rate is a display convention, not an FX quote, and is recorded on the row.
"""
from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass, asdict
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import yaml

import hv2_paths  # noqa: F401  (sys.path for the frozen packages)
from providers import PreDispatchRefusal  # noqa: E402  (read-only import from EMP-001)

INR_USD_DISPLAY_RATE = Decimal("95.4211")   # COST-TABLE.rules: INR->USD display rate 95.4211
ONE = Decimal("1")


class PricingError(RuntimeError):
    """A roster or cost-table fact could not be read as the declared shape."""


@dataclass(frozen=True)
class PriceCheck:
    route_key: str
    roster_key: str
    roster_variant: str | None
    route_status: str
    price_status: str
    unit_price: Decimal | None          # roster-implied unit price for this row (native currency)
    currency: str
    unit: str | None
    quantity: Decimal | None
    quantity_unit: str | None
    quantity_rule: str | None
    amount_native: Decimal | None
    amount_usd_equiv: Decimal | None
    fx_rate: Decimal | None
    pin_ref: str | None
    ok: bool
    refusal_reason: str | None

    def as_dict(self) -> dict:
        d = asdict(self)
        for k, v in list(d.items()):
            if isinstance(v, Decimal):
                d[k] = str(v)
        return d


def _dec(v) -> Decimal | None:
    if v is None:
        return None
    return Decimal(str(v))


def _round6(v: Decimal) -> Decimal:
    return v.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)


class Roster:
    """A fresh read of the roster file. `reload()` is called at every check, by design."""

    def __init__(self, path: Path | str = hv2_paths.ROSTER):
        self.path = Path(path)
        self.sha256: str | None = None
        self._routes: dict[str, dict] = {}
        self.reload()

    def reload(self) -> None:
        raw = self.path.read_bytes()
        self.sha256 = hashlib.sha256(raw).hexdigest()
        data = yaml.safe_load(raw.decode("utf-8"))
        routes = data.get("routes") if isinstance(data, dict) else None
        if not isinstance(routes, list):
            raise PricingError(f"{self.path}: no routes list")
        self._routes = {r["route_key"]: r for r in routes if isinstance(r, dict) and r.get("route_key")}
        self.meta = data.get("meta") or {}

    def record(self, roster_key: str, variant: str | None) -> dict:
        """The price-bearing record: the route, one of its variants, or its fal fallback."""
        route = self._routes.get(roster_key)
        if route is None:
            raise PricingError(f"roster has no route_key {roster_key!r}")
        if variant is None:
            return {"source": "route", "route_status": route.get("route_status"),
                    "regular_price": route.get("regular_price") or {},
                    "promo_price": route.get("promo_price"), "pin_ref": route.get("pin_ref"),
                    "price_addons": route.get("price_addons"),
                    "billing_unit_verbatim": route.get("billing_unit_verbatim"),
                    "surface": route.get("surface"), "surface_model_id": route.get("surface_model_id"),
                    "billing_pool": route.get("billing_pool")}
        if variant == "fallback":
            fb = route.get("fallback")
            if not isinstance(fb, dict):
                raise PricingError(f"roster route {roster_key!r} has no fallback record")
            return {"source": "fallback", "route_status": fb.get("route_status"),
                    "regular_price": fb.get("regular_price") or {},
                    "promo_price": fb.get("promo_price"), "pin_ref": fb.get("pin_ref"),
                    "price_addons": fb.get("price_addons") or route.get("price_addons"),
                    "billing_unit_verbatim": fb.get("billing_unit_verbatim"),
                    "surface": fb.get("surface"), "surface_model_id": fb.get("surface_model_id"),
                    "billing_pool": fb.get("billing_pool")}
        for v in route.get("variants") or []:
            if v.get("variant") == variant:
                return {"source": f"variant:{variant}", "route_status": v.get("route_status"),
                        "regular_price": v.get("regular_price") or {},
                        # a route-level promotion applies to its variants unless the variant says otherwise
                        "promo_price": v.get("promo_price") or route.get("promo_price"), "pin_ref": v.get("pin_ref"),
                        "price_addons": route.get("price_addons"),
                        "billing_unit_verbatim": route.get("billing_unit_verbatim"),
                        "surface": route.get("surface"), "surface_model_id": v.get("surface_model_id"),
                        "billing_pool": route.get("billing_pool")}
        raise PricingError(f"roster route {roster_key!r} has no variant {variant!r}")


class CostTable:
    """Read-only view of COST-TABLE.yaml (totals, rows, rules) for reconciliation."""

    def __init__(self, path: Path | str = hv2_paths.COST_TABLE):
        self.path = Path(path)
        raw = self.path.read_bytes()
        self.sha256 = hashlib.sha256(raw).hexdigest()
        self.data = yaml.safe_load(raw.decode("utf-8"))

    @property
    def rules(self) -> list:
        return list(self.data.get("rules") or [])

    @property
    def totals(self) -> dict:
        return dict(self.data.get("totals") or {})

    @property
    def rows(self) -> list:
        return list(self.data.get("rows") or [])

    @property
    def route_catalogue(self) -> dict:
        return dict(self.data.get("route_catalogue") or {})

    @property
    def priced_against_roster(self) -> dict:
        return dict(self.data.get("priced_against_roster") or {})


# --------------------------------------------------------------------------- quantity rules
def _ceil_to(n: Decimal, step: int) -> Decimal:
    return Decimal(int(math.ceil(n / Decimal(step)))) * Decimal(step)


def quantity_for(route_key: str, unit: str | None, case_row: dict) -> tuple[Decimal, str, str] | None:
    """(quantity, quantity_unit, rule_id) for one call, or None when no rule is known."""
    params = case_row.get("params") or {}
    row_qty = _dec(case_row.get("quantity"))
    row_unit = case_row.get("quantity_unit")

    if route_key == "kling-lipsync-a2v":
        # COST-TABLE.rules: input seconds rolled up to 5-s increments (6-s or 8-s plate -> 10 s)
        plate_s = _dec(params.get("plate_seconds")) or _dec(case_row.get("plate_seconds"))
        if plate_s is None:
            # the row already carries the rolled-up quantity; recompute from the declared plate
            m = str(params.get("billed_input_seconds", ""))
            if "6-s plate" in m:
                plate_s = Decimal(6)
            elif "8-s plate" in m:
                plate_s = Decimal(8)
        if plate_s is None:
            return None
        return _ceil_to(plate_s, 5), "seconds", "kling_lipsync_5s_rollup"
    if route_key == "elevenlabs-music":
        secs = _dec(params.get("duration_s")) or _dec(case_row.get("duration_s"))
        if secs is None and row_unit == "minutes" and row_qty is not None:
            secs = row_qty * 60
        if secs is None:
            return None
        return Decimal(int(math.ceil(secs / Decimal(60)))), "minutes", "elevenlabs_music_minute"
    if route_key == "veo-3.1-fast-extend":
        return Decimal(15), "seconds", "veo_extend_15s"
    if unit in ("per_1000_characters", "per_1M_characters"):
        chars = _dec(params.get("chars"))
        if chars is None:
            return None
        return chars, "chars", unit
    if unit in ("per_image", "per_image_first_megapixel"):
        return Decimal(1), "images", "per_image"
    if unit == "per_clip":
        return Decimal(1), "clips", "per_clip"
    if unit in ("per_second", "per_input_video_second"):
        d = params.get("duration_s")
        if isinstance(d, (int, float)) or (isinstance(d, str) and d.strip().isdigit()):
            return Decimal(str(d)), "seconds", "per_second"
        if route_key.startswith("gemini-omni") and row_qty is not None:
            # duration is a recorded string ("longest supported <= 15"); the vendor page caps Omni
            # Flash at 10 s, so the rule returns the page's maximum and the row is reconciled
            return Decimal(10), "seconds", "per_second_omni_page_max_10s"
        return None
    return None


# Units whose price can be projected onto one call. A token meter (per_1M_image_output_tokens) has
# no per-call quantity in the pinned bytes, so the roster's number is pinned but NOT projectable
# and the row is priced null (COST-TABLE: "pinned but not projectable").
PROJECTABLE_UNITS = ("per_image", "per_image_first_megapixel", "per_second", "per_input_video_second",
                     "per_1000_characters", "per_1M_characters", "per_clip", "per_minute")


def unit_price_for(route_key: str, rec: dict, case_row: dict) -> tuple[Decimal | None, str]:
    """Roster-implied unit price for this row (native currency), plus a note."""
    rp = rec.get("regular_price") or {}
    base = _dec(rp.get("value"))
    if base is None:
        return None, "no regular price in the roster (unpinned)"
    if rp.get("unit") not in PROJECTABLE_UNITS:
        return None, f"roster unit {rp.get('unit')!r} is not projectable onto one call (pinned but not projectable)"
    addons = rec.get("price_addons") or []
    if route_key == "flux-2-pro-edit" and addons:
        refs = (case_row.get("params") or {}).get("refs") or 0
        try:
            refs = int(refs)
        except (TypeError, ValueError):
            refs = 0
        addon = next((a for a in addons if a.get("addon") == "additional_megapixel"), None)
        if addon is None:
            return base, "flux_edit: no additional_megapixel addon in the roster"
        per_mp = _dec(addon.get("value")) or Decimal(0)
        # COST-TABLE priced this route at base + addon x 1 reference regardless of the row's
        # reference count; the roster says 'each input megapixel (reference images)'. The
        # roster-implied price counts every reference at ~1 MP each.
        return base + per_mp * Decimal(max(refs, 1)), f"flux_edit_addon: 0.03 + 0.015 x {max(refs, 1)} reference megapixel(s)"
    return base, rec.get("source") or "route"


class Pricing:
    """Execution-time price check + dry-run pricing, from the roster at every call."""

    def __init__(self, roster_path: Path | str = hv2_paths.ROSTER,
                 registry=None, expected_roster_sha256: str | None = None,
                 catalogue: dict | None = None, cost_table_path: Path | str | None = hv2_paths.COST_TABLE):
        self.roster = Roster(roster_path)
        self.expected_roster_sha256 = expected_roster_sha256
        if registry is None:
            import surfaces
            registry = surfaces.REGISTRY
        self.registry = registry
        # The freeze catalogue (COST-TABLE.yaml -> route_catalogue) is the second authority: a route it
        # marks unpinned (e.g. veo-3.1-lite-i2v, for which the roster pins no image-input variant)
        # is refused even where the roster carries a number for the parent route.
        if catalogue is None and cost_table_path and Path(cost_table_path).exists():
            catalogue = CostTable(cost_table_path).route_catalogue
        self.catalogue = catalogue or {}

    # -- the check ------------------------------------------------------------------------
    def evaluate(self, route_key: str, case_row: dict) -> PriceCheck:
        """Compute the roster-implied cost of one call and list the reason it would be refused."""
        self.roster.reload()                                   # re-read the file, every time
        entry = self.registry.get(route_key)
        rec = self.roster.record(entry.roster_key, entry.roster_variant)
        rp = rec.get("regular_price") or {}
        currency = rp.get("currency") or entry.currency
        unit = rp.get("unit")
        route_status = rec.get("route_status")
        promo = rec.get("promo_price")

        unit_price, note = unit_price_for(route_key, rec, case_row)
        # price_status is about the PRICE only; route_status is tracked separately so a conditional route
        # with a pinned rate card (sora-2, sd3.5-large) still prices its conditional line while refusing dispatch
        price_status = "pinned" if unit_price is not None else "unpinned"
        q = quantity_for(route_key, unit, case_row)
        reasons: list[str] = []

        if self.expected_roster_sha256 and self.roster.sha256 != self.expected_roster_sha256:
            reasons.append(f"roster_sha256_drift: file sha256 {self.roster.sha256[:12]}... != expected {self.expected_roster_sha256[:12]}...")
        if route_status != "pinned":
            reasons.append(f"route_status_not_pinned: roster says {route_status!r}")
        if unit_price is None:
            reasons.append(f"price_unpinned: {note}")
        cat = self.catalogue.get(route_key) or {}
        if cat and cat.get("price_status") != "pinned":
            reasons.append(f"price_unpinned: the freeze catalogue (COST-TABLE route_catalogue) marks {route_key} "
                           f"{cat.get('price_status')!r} - see route_catalogue[{route_key}].note")
            price_status = "unpinned"
        if cat and cat.get("route_status") not in (None, "pinned"):
            reasons.append(f"route_status_not_pinned: the freeze catalogue marks {route_key} {cat.get('route_status')!r}")
        if case_row.get("price_status") not in (None, "pinned"):
            reasons.append(f"row_price_status_not_pinned: case row says {case_row.get('price_status')!r}")
        if case_row.get("route_status") not in (None, "pinned"):
            reasons.append(f"row_route_status_not_pinned: case row says {case_row.get('route_status')!r}")
        row_unit_price = _dec(case_row.get("unit_price"))
        if unit_price is not None and row_unit_price is not None and row_unit_price != unit_price:
            reasons.append(f"price_mismatch: case row unit_price {row_unit_price} != roster-implied {unit_price} ({note})")
        if promo and isinstance(promo, dict) and promo.get("used_in_totals"):
            reasons.append("promo_price_in_use: the roster marks a promotional price as used")
        if q is None:
            reasons.append(f"quantity_rule_unknown: no billing quantity rule for unit {unit!r} on {route_key}")
        else:
            row_qty = _dec(case_row.get("quantity"))
            if row_qty is not None and row_qty != q[0]:
                reasons.append(f"quantity_rule_mismatch: case row quantity {row_qty} {case_row.get('quantity_unit')} != rule {q[0]} {q[1]} ({q[2]})")

        amount_native = amount_usd = fx = None
        if unit_price is not None and q is not None and price_status == "pinned":
            qty = q[0]
            if q[2] == "per_1000_characters":
                amount_native = unit_price * qty / Decimal(1000)
            elif q[2] == "per_1M_characters":
                amount_native = unit_price * qty / Decimal(1_000_000)
            else:
                amount_native = unit_price * qty
            if currency == "INR":
                fx = INR_USD_DISPLAY_RATE
                amount_usd = amount_native / fx
            elif currency == "USD":
                fx = ONE
                amount_usd = amount_native
            else:
                reasons.append(f"currency_unknown: {currency!r}")

        return PriceCheck(
            route_key=route_key, roster_key=entry.roster_key, roster_variant=entry.roster_variant,
            route_status=str(route_status), price_status=price_status,
            unit_price=unit_price, currency=currency, unit=unit,
            quantity=(q[0] if q else None), quantity_unit=(q[1] if q else None),
            quantity_rule=(q[2] if q else None),
            amount_native=(_round6(amount_native) if amount_native is not None else None),
            amount_usd_equiv=(_round6(amount_usd) if amount_usd is not None else None),
            fx_rate=fx, pin_ref=rec.get("pin_ref"),
            ok=not reasons, refusal_reason=("; ".join(reasons) if reasons else None))

    def check(self, route_key: str, case_row: dict) -> PriceCheck:
        """The dispatch-time gate: refuse (nothing reserved, nothing sent) unless everything pins."""
        pc = self.evaluate(route_key, case_row)
        if not pc.ok:
            raise PreDispatchRefusal(
                f"price check refused {route_key} for {case_row.get('case_id')}: {pc.refusal_reason}. "
                f"Nothing was reserved and nothing was sent.")
        return pc
