"""Shared setup for the router tests: find the checkout, build a router, keep everything offline.

`python3 -m unittest discover -s runtime/tests -p 'test_*.py'` from the repo root puts
`runtime/tests` on sys.path, not the repo root, so each test module imports this one first and it
puts the checkout root on the path.
"""
from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.route.attempt_id import load_identities            # noqa: E402
from runtime.route.decision import Router                        # noqa: E402
from runtime.route.evidence import EvidenceBase                  # noqa: E402
from runtime.route.price import PriceBook                        # noqa: E402
from runtime.route.profile import load_profile                   # noqa: E402
from runtime.route.spec import load_spec                         # noqa: E402

FIXTURES = ROOT / "runtime" / "route" / "fixtures"
SPEC_STATIC_OVERLAY = FIXTURES / "SPEC-static-ad-devanagari-overlay.yaml"
SPEC_STATIC_IN_SCENE = FIXTURES / "SPEC-static-ad-devanagari-in-scene.yaml"
SPEC_EDIT_PHOTO = FIXTURES / "SPEC-edit-supplied-photo.yaml"
SPEC_MOTION = FIXTURES / "SPEC-motion-6s-silent.yaml"


def evidence_base() -> EvidenceBase:
    return EvidenceBase(root=ROOT)


def price_book(ev: EvidenceBase, roster_path: Path | None = None,
               pin_root: Path | None = None) -> PriceBook:
    src = ev.binding.sources
    return PriceBook(root=ev.root,
                     roster_path=roster_path or (ev.root / src["roster"]),
                     pin_root=pin_root or (ev.root / src["price_pin_root"]))


def router(ev: EvidenceBase | None = None, prices: PriceBook | None = None) -> Router:
    ev = ev or evidence_base()
    return Router(ev, prices or price_book(ev), load_identities())


def profile(name: str, ev: EvidenceBase | None = None):
    ev = ev or evidence_base()
    return load_profile(name, ev.root / ev.binding.sources["policy_profiles"])


def spec(path: Path):
    return load_spec(path)


def plan(spec_path: Path, profile_name: str, *, committed="0", ev=None, prices=None) -> dict:
    ev = ev or evidence_base()
    r = router(ev, prices)
    return r.plan(load_spec(spec_path), profile(profile_name, ev),
                  already_committed_usd=Decimal(committed), customer_ref="acct-test")
