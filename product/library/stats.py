"""Exact binomial statistics for the library (stdlib only).

Founder ruling 2026-09-24: "statistics have all the information on confidence intervals, what is significant and what is
not per the sample size — use stats." A count on its own ("seen on 3 jobs") says nothing without the sample it came from;
these helpers turn a count k out of n into an interval and a significance decision.

Reference calculation under an iid Bernoulli model (jobs treated as independent trials). That is an assumption, not a
fact about our jobs; the numbers are a floor on uncertainty, not a guarantee.
"""
from __future__ import annotations

import math

ALPHA = 0.05


def _sf(k: int, n: int, p: float) -> float:
    """P(X >= k) for X ~ Binomial(n, p)."""
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1))


def _cdf(k: int, n: int, p: float) -> float:
    """P(X <= k)."""
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(0, k + 1))


def _bisect(f, target: float, increasing: bool) -> float:
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if (f(mid) < target) == increasing:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def lower_bound(k: int, n: int, alpha: float = ALPHA) -> float:
    """One-sided exact (Clopper-Pearson) lower confidence bound on the rate, level 1 - alpha."""
    if n <= 0 or k <= 0:
        return 0.0
    return _bisect(lambda p: _sf(k, n, p), alpha, increasing=True)


def upper_bound(k: int, n: int, alpha: float = ALPHA) -> float:
    """One-sided exact (Clopper-Pearson) upper confidence bound on the rate, level 1 - alpha."""
    if n <= 0:
        return 1.0
    if k >= n:
        return 1.0
    return _bisect(lambda p: _cdf(k, n, p), alpha, increasing=False)


def interval(k: int, n: int, alpha: float = ALPHA) -> tuple:
    """Two-sided exact (Clopper-Pearson) interval, level 1 - alpha."""
    return lower_bound(k, n, alpha / 2), upper_bound(k, n, alpha / 2)


def recurs_significantly(k: int, n: int, alpha: float = ALPHA) -> bool:
    """Does something seen on k of n jobs happen significantly more often than a one-off (a rate of 1/n)?
    One-sided exact test: the lower confidence bound on its rate is above 1/n."""
    return n > 0 and lower_bound(k, n, alpha) > 1.0 / n


def describe(k: int, n: int, alpha: float = ALPHA) -> str:
    lo, hi = interval(k, n, alpha)
    return f"seen on {k} of {n} jobs ({k / n:.0%}, {int(round((1 - alpha) * 100))}% CI {lo:.0%}–{hi:.0%})" if n else f"seen {k} times"
