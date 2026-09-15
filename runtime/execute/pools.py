"""Provider-pool liquidity: can the billing pool a route is priced against actually fund the attempt?

WHY (production-learning UPWORK-INTRO-001, SD-11). The pilot's spend authority was INR 2,000; the fal
cash balance was USD 3.23, then 0.26. Two video slots were dropped and the Wan fallback was structurally
dead, and no plan knew it until the executor read the balance by hand. Spend authority != provider
liquidity. The bridge therefore takes a PoolLiquidity built from READINGS — a balance, when it was read,
from where — and marks every attempt funded / not funded / unknown. It never reads a balance itself
(that is a network call and a key) and never guesses one.
"""
from __future__ import annotations

from decimal import Decimal, InvalidOperation


class PoolLiquidity:
    """Balances per billing pool from explicit readings, drawn down as attempts reserve in order."""

    def __init__(self, readings: dict):
        self._readings = dict(readings)                     # pool -> {"balance_usd": Decimal|None, "read_utc", "source"}
        self._remaining = {p: r["balance_usd"] for p, r in readings.items()}

    @classmethod
    def from_readings(cls, readings) -> "PoolLiquidity":
        out: dict = {}
        for r in readings:
            pool = str(r.get("pool") or "").strip()
            if not pool:
                raise ValueError("a pool reading needs a pool name")
            if not r.get("read_utc") or not r.get("source"):
                raise ValueError(f"pool {pool!r}: a reading needs read_utc and source (where the balance came from)")
            raw = r.get("balance_usd")
            if raw is None:
                bal = None                                   # known pool, balance not readable (e.g. console only)
            else:
                try:
                    bal = Decimal(str(raw))
                except InvalidOperation:
                    raise ValueError(f"pool {pool!r}: balance_usd {raw!r} is not a decimal") from None
            out[pool] = {"balance_usd": bal, "read_utc": str(r["read_utc"]), "source": str(r["source"])}
        return cls(out)

    @property
    def pools(self) -> list:
        return sorted(self._readings)

    def reading(self, pool: str) -> dict | None:
        r = self._readings.get(pool)
        if r is None:
            return None
        return {"balance_usd": (str(r["balance_usd"]) if r["balance_usd"] is not None else None),
                "remaining_usd": (str(self._remaining[pool]) if self._remaining.get(pool) is not None else None),
                "read_utc": r["read_utc"], "source": r["source"]}

    def can_fund(self, pool: str, amount_usd) -> tuple:
        """(True|False|None, reason). None = unknown: no reading, or a reading without a balance."""
        amount = Decimal(str(amount_usd))
        r = self._readings.get(pool)
        if r is None:
            return None, f"pool {pool!r}: no reading supplied; liquidity unknown"
        if r["balance_usd"] is None:
            return None, f"pool {pool!r}: balance not readable ({r['source']}); liquidity unknown"
        left = self._remaining[pool]
        if left >= amount:
            return True, f"pool {pool!r}: {left} USD remaining of {r['balance_usd']} read {r['read_utc']} covers {amount}"
        return False, (f"pool {pool!r}: {left} USD remaining of {r['balance_usd']} read {r['read_utc']} "
                       f"({r['source']}) cannot fund {amount}")

    def reserve(self, pool: str, amount_usd) -> tuple:
        """can_fund, then draw the pool down when funded (unknown pools are not drawn)."""
        ok, why = self.can_fund(pool, amount_usd)
        if ok:
            self._remaining[pool] = self._remaining[pool] - Decimal(str(amount_usd))
        return ok, why
