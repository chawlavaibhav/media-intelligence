"""EMP-001 preflight controls.

The preflight answers one question: is the repository mechanically ready to spend money, without
having spent any. Each check below is paired with a control proving the check can FAIL — a gate
that never fires proves nothing, and a preflight that always says READY is worse than none.
"""
import json
import socket
from pathlib import Path

import pytest

import preflight

PKG = Path(__file__).resolve().parents[1]
REPO = PKG.parents[1]
REGISTRY = REPO / 'eval' / 'registry' / 'registry-v1.jsonl'


# ------------------------------------------------------------- Q1 geometry
def test_geometry_fixture_count_is_102():
    r = preflight.check_geometry_fixtures()
    assert r['ok'] is True
    assert r['fixture_count'] == 102
    assert r['expected'] == 102


def test_geometry_check_fails_on_a_wrong_count(tmp_path):
    m = tmp_path / 'manifest.json'
    m.write_text(json.dumps({'counts': {'total': 99}, 'items': []}))
    r = preflight.check_geometry_fixtures(m)
    assert r['ok'] is False


def test_geometry_check_fails_when_an_image_is_missing(tmp_path):
    m = tmp_path / 'manifest.json'
    m.write_text(json.dumps({'counts': {'total': 102},
                             'items': [{'id': 'cv-0000', 'image': 'nope.png'}]}))
    r = preflight.check_geometry_fixtures(m)
    assert r['ok'] is False
    assert r['missing_images']


# ------------------------------------------------------------- Registry zero
def test_registry_has_zero_empirical_rows():
    r = preflight.check_registry_empirical_rows()
    assert r['ok'] is True
    assert r['empirical_row_count'] == 0


def test_registry_check_fails_if_a_row_appears(tmp_path):
    f = tmp_path / 'registry-v1.jsonl'
    f.write_text('# a comment\n{"entry_id": "smuggled-in"}\n')
    r = preflight.check_registry_empirical_rows(f)
    assert r['ok'] is False
    assert r['empirical_row_count'] == 1


# --------------------------------------------------------- protected baselines
def test_protected_baselines_are_unchanged():
    r = preflight.check_protected_baselines()
    assert r['ok'] is True, r['mismatches']
    assert r['checked'] >= 4


def test_baseline_check_fails_on_a_changed_file(tmp_path):
    target = tmp_path / 'thing.txt'
    target.write_text('after')
    baselines = tmp_path / 'protected-baselines.sha256'
    baselines.write_text('0' * 64 + '  thing.txt\n')
    r = preflight.check_protected_baselines(baselines, tmp_path)
    assert r['ok'] is False
    assert r['mismatches']


# ------------------------------------------------- one call = one trial (Q7)
def test_one_call_one_trial_contract_holds():
    r = preflight.check_one_call_one_trial()
    assert r['ok'] is True
    assert r['attempts'] == r['trials']
    assert r['refused_attempt_still_has_a_trial'] is True
    assert r['registry_rows_created'] == 0


def test_synthetic_measurement_cannot_become_a_registry_row():
    r = preflight.check_synthetic_cannot_reach_registry()
    assert r['ok'] is True
    assert r['refused'] is True
    assert 'synthetic' in r['refusal_message'].lower()


# ------------------------------------------------------------- authorisation
def test_authorisation_is_blocked_during_preparation():
    r = preflight.check_authorisation_blocked()
    assert r['ok'] is True
    assert r['paid_execution_permitted'] is False
    assert r['retries_authorised'] == 0


def test_authorisation_check_reports_not_ok_if_a_live_authorisation_appears(tmp_path):
    p = tmp_path / 'authorization.local.yaml'
    p.write_text("authorised: true\ntranche_id: EMP-001\n"
                 "max_consumed_api_spend_usd: 10.00\nretries_authorised: 0\n")
    r = preflight.check_authorisation_blocked(p)
    assert r['ok'] is False
    assert r['paid_execution_permitted'] is True


# ------------------------------------------------------- the whole dry run
def test_dry_run_needs_no_network_at_all(monkeypatch, tmp_path):
    """NEGATIVE CONTROL. Every socket is poisoned; --dry-run must still exit 0.

    The harness self-test runs IN-PROCESS inside the preflight precisely so that this patch
    covers it too. A subprocess would escape the poison and the control would be theatre.
    """
    def explode(*a, **k):
        raise AssertionError('EMP-001 dry-run attempted a network connection')

    monkeypatch.setattr(socket.socket, 'connect', explode)
    monkeypatch.setattr(socket.socket, 'connect_ex', explode)
    monkeypatch.setattr(socket, 'create_connection', explode)

    before = REGISTRY.read_bytes()
    code = preflight.main(['--dry-run', '--out', str(tmp_path / 'preflight-result.json')])
    assert code == 0
    assert REGISTRY.read_bytes() == before


def test_dry_run_writes_explicit_booleans(tmp_path):
    out = tmp_path / 'preflight-result.json'
    preflight.main(['--dry-run', '--out', str(out)])
    r = json.loads(out.read_text())
    assert r['verdict'] == 'PREFLIGHT_GREEN'
    assert r['dry_run'] is True
    assert r['external_calls'] == 0
    assert r['spend_usd'] == '0'
    for key in ('geometry_fixtures', 'registry_empirical_rows', 'protected_baselines',
                'one_call_one_trial', 'synthetic_cannot_reach_registry', 'authorisation_blocked',
                'harness_selftest'):
        assert r['checks'][key]['ok'] is True, key


def test_running_without_dry_run_is_refused_while_authorisation_is_absent(tmp_path):
    code = preflight.main(['--out', str(tmp_path / 'r.json')])
    assert code != 0


def test_harness_selftest_runs_and_is_green():
    r = preflight.check_harness_selftest()
    assert r['ok'] is True
    assert r['exit_code'] == 0
    assert r['checks_passed'] == r['checks_total'] > 0
    assert r['registry_rows_created'] == 0
