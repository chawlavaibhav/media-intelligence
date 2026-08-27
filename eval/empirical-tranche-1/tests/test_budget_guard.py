"""EMP-001 authorisation and budget negative controls.

Every test here is a control that must FIRE. A guard that never refuses proves nothing, so each
case below is a way the tranche could start spending money it was never given, and the assertion
is that the attempt raises before anything could be dispatched.

The three cases carried verbatim from the implementation plan are marked PLAN.
"""
import sys
from decimal import Decimal
from pathlib import Path

import pytest

from budget_guard import (
    AUTHORISATION_EXAMPLE_PATH,
    BudgetExceeded,
    BudgetGuard,
    NotAuthorised,
    load_authorisation,
    open_guard,
)


# --------------------------------------------------------------------- ceiling
def test_refuses_without_positive_authorisation():  # PLAN
    with pytest.raises(ValueError):
        BudgetGuard(authorised_usd=Decimal('0'), spent_usd=Decimal('0'))


def test_refuses_negative_authorisation():
    with pytest.raises(ValueError):
        BudgetGuard(authorised_usd=Decimal('-1.00'), spent_usd=Decimal('0'))


def test_reserve_fails_before_crossing_ceiling():  # PLAN
    g = BudgetGuard(authorised_usd=Decimal('10.00'), spent_usd=Decimal('9.80'))
    with pytest.raises(BudgetExceeded):
        g.reserve(Decimal('0.21'))


def test_record_never_silently_exceeds_ceiling():  # PLAN
    g = BudgetGuard(authorised_usd=Decimal('10.00'), spent_usd=Decimal('9.90'))
    with pytest.raises(BudgetExceeded):
        g.record(Decimal('0.11'))


def test_refused_record_does_not_move_spent():
    g = BudgetGuard(authorised_usd=Decimal('10.00'), spent_usd=Decimal('9.90'))
    with pytest.raises(BudgetExceeded):
        g.record(Decimal('0.11'))
    assert g.spent_usd == Decimal('9.90')


def test_reserve_exactly_at_ceiling_is_allowed():
    g = BudgetGuard(authorised_usd=Decimal('10.00'), spent_usd=Decimal('9.80'))
    g.reserve(Decimal('0.20'))
    g.record(Decimal('0.20'))
    assert g.spent_usd == Decimal('10.00')


def test_spend_accumulates_and_then_closes_the_door():
    g = BudgetGuard(authorised_usd=Decimal('1.00'))
    for _ in range(10):
        g.record(Decimal('0.10'))
    assert g.spent_usd == Decimal('1.00')
    with pytest.raises(BudgetExceeded):
        g.reserve(Decimal('0.01'))


def test_float_amounts_are_refused_so_money_is_never_binary_rounded():
    g = BudgetGuard(authorised_usd=Decimal('10.00'))
    with pytest.raises(TypeError):
        g.record(0.11)
    with pytest.raises(TypeError):
        g.reserve(0.11)


def test_negative_amounts_cannot_manufacture_headroom():
    g = BudgetGuard(authorised_usd=Decimal('10.00'), spent_usd=Decimal('9.99'))
    with pytest.raises(ValueError):
        g.record(Decimal('-5.00'))
    assert g.spent_usd == Decimal('9.99')


# --------------------------------------------------------- authorisation gate
def test_committed_example_authorisation_is_disabled():
    auth = load_authorisation(AUTHORISATION_EXAMPLE_PATH)
    assert auth.authorised is False
    assert auth.max_consumed_api_spend_usd == Decimal('0')
    assert auth.tranche_id == 'EMP-001'
    assert auth.retries_authorised == 0


def test_committed_example_authorisation_carries_no_secret():
    """Scan the DATA, not the prose.

    An earlier version of this test grepped the whole file and tripped over the word "token" in
    the comment that says no token belongs there. Comments explaining the rule are not violations
    of it; the control is that no credential-shaped key or value is actually declared.
    """
    import yaml
    data = yaml.safe_load(AUTHORISATION_EXAMPLE_PATH.read_text(encoding='utf-8')) or {}
    forbidden_keys = {'api_key', 'apikey', 'secret', 'token', 'password', 'credential',
                      'openai_api_key', 'google_api_key', 'fal_key'}
    assert not (set(k.lower() for k in data) & forbidden_keys)
    for value in data.values():
        if isinstance(value, str):
            assert not value.startswith(('sk-', 'sk_', 'AIza', 'ghp_'))
    # And no data line — comments excluded — may carry a long opaque literal.
    for line in AUTHORISATION_EXAMPLE_PATH.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        assert 'sk-' not in line and 'AIza' not in line


def test_disabled_authorisation_cannot_open_a_guard():
    with pytest.raises(NotAuthorised):
        open_guard(AUTHORISATION_EXAMPLE_PATH)


def test_missing_authorisation_file_cannot_open_a_guard(tmp_path):
    with pytest.raises(NotAuthorised):
        open_guard(tmp_path / 'does-not-exist.yaml')


def _write(tmp_path, body):
    p = tmp_path / 'authorization.local.yaml'
    p.write_text(body, encoding='utf-8')
    return p


def test_authorised_true_with_zero_ceiling_is_still_refused(tmp_path):
    p = _write(tmp_path, "authorised: true\ntranche_id: EMP-001\n"
                         "max_consumed_api_spend_usd: 0\nretries_authorised: 0\n")
    with pytest.raises(NotAuthorised):
        open_guard(p)


def test_authorisation_for_a_different_tranche_is_refused(tmp_path):
    p = _write(tmp_path, "authorised: true\ntranche_id: EMP-002\n"
                         "max_consumed_api_spend_usd: 10.00\nretries_authorised: 0\n")
    with pytest.raises(NotAuthorised):
        open_guard(p)


def test_authorisation_above_the_proposed_ceiling_is_refused(tmp_path):
    p = _write(tmp_path, "authorised: true\ntranche_id: EMP-001\n"
                         "max_consumed_api_spend_usd: 25.00\nretries_authorised: 0\n")
    with pytest.raises(NotAuthorised):
        open_guard(p)


def test_any_authorised_retry_is_refused(tmp_path):
    """Retries authorised is 0 and is not a field the runner may quietly raise."""
    p = _write(tmp_path, "authorised: true\ntranche_id: EMP-001\n"
                         "max_consumed_api_spend_usd: 10.00\nretries_authorised: 1\n")
    with pytest.raises(NotAuthorised):
        open_guard(p)


def test_a_correctly_authorised_file_opens_a_guard_at_that_exact_ceiling(tmp_path):
    p = _write(tmp_path, "authorised: true\ntranche_id: EMP-001\n"
                         "max_consumed_api_spend_usd: 10.00\nretries_authorised: 0\n"
                         "approved_by: someone\napproved_at: '2026-08-26'\n")
    g = open_guard(p)
    assert g.authorised_usd == Decimal('10.00')
    assert g.spent_usd == Decimal('0')


def test_the_string_true_is_not_an_approval(tmp_path):
    """`authorised: "true"` is a string, not a decision. Fail closed on it."""
    p = _write(tmp_path, "authorised: 'true'\ntranche_id: EMP-001\n"
                         "max_consumed_api_spend_usd: 10.00\nretries_authorised: 0\n")
    with pytest.raises(NotAuthorised):
        open_guard(p)


# ------------------------------------------------------------- runtime hygiene
def test_the_local_authorisation_filename_is_gitignored():
    root = Path(__file__).resolve().parents[3]
    ignored = (root / '.gitignore').read_text(encoding='utf-8')
    assert 'authorization.local.yaml' in ignored


def test_no_local_authorisation_file_is_committed():
    pkg = Path(__file__).resolve().parents[1]
    assert not (pkg / 'authorization.local.yaml').exists()
