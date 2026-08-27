"""The frozen EMP-001 config must match the Controller decision, field for field.

These are drift controls. Every number here was fixed by
`coordination/decisions/CONTROLLER-FIRST-EMPIRICAL-TRANCHE-PREPARATION-2026-08-26.md` and
`coordination/CONTROL-STATE.md`. If a runner ever needs a different value, that is a Controller
decision, and this test is what makes the change visible instead of silent.
"""
from decimal import Decimal
from pathlib import Path

import yaml

CONFIG = Path(__file__).resolve().parents[1] / 'config.yaml'


def cfg():
    return yaml.safe_load(CONFIG.read_text(encoding='utf-8'))


def test_tranche_is_prepared_but_not_authorised():
    c = cfg()
    assert c['tranche_id'] == 'EMP-001'
    assert c['status'] == 'PREPARED_NOT_AUTHORISED'


def test_spend_ceiling_and_retries_are_frozen():
    c = cfg()
    assert Decimal(str(c['external_spend_ceiling_usd'])) == Decimal('10.00')
    assert c['retries_authorised'] == 0


def test_qualification_shape_is_frozen():
    q = cfg()['qualification']
    assert q['repeats_per_shape'] == 3
    assert q['devanagari_items'] == 96
    assert q['latin_items'] == 96
    assert q['shapes'] == ['transcribe', 'verdict']


def test_both_judge_candidates_require_an_exact_version_at_execution():
    cands = cfg()['qualification']['judge_candidates']
    assert [c['provider'] for c in cands] == ['anthropic', 'google']
    assert [c['model_alias'] for c in cands] == ['claude-haiku-4-5-20251001', 'gemini-3.5-flash-lite']
    assert cands[0]['exact_model_id_required'] is True
    assert cands[1]['snapshot_or_exact_version_required'] is True


def test_atex_is_four_items_two_unseeded_repeats_two_routes():
    a = cfg()['atex']
    assert a['seed_policy'] == 'unseeded'
    assert a['repeats_per_item'] == 2
    assert a['items'] == ['ATEXT-01', 'ATEXT-02', 'ATEXT-03', 'ATEXT-04']
    assert set(a['slots']) == {'IMG-01', 'IMG-02'}
    assert a['slots']['IMG-01']['route'] == 'openai/gpt-image-2'
    assert a['slots']['IMG-02']['route'] == 'fal-ai/ideogram/v3'
    assert a['slots']['IMG-01']['generations'] == 8
    assert a['slots']['IMG-02']['generations'] == 8


def test_maximum_future_generations_is_exactly_sixteen():
    a = cfg()['atex']
    declared = sum(s['generations'] for s in a['slots'].values())
    derived = len(a['items']) * a['repeats_per_item'] * len(a['slots'])
    assert declared == derived == 16


def test_config_declares_no_secret():
    raw = CONFIG.read_text(encoding='utf-8')
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        assert 'sk-' not in line and 'AIza' not in line
