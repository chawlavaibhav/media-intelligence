"""Controls on the four frozen A-TEXT comparability items.

A-TEXT is deliberately the narrowest possible question: on four shared items, does a route fail
badly enough on exact Devanagari/Hinglish text that deeper spend is already unjustified? It
isolates TEXT. It does not pretend to measure creative quality, and it cannot promote a slot.

The four cases carried verbatim from the implementation plan are marked PLAN.
"""
import json
from pathlib import Path

import yaml

PKG = Path(__file__).resolve().parents[1]
MANIFEST = PKG / 'atex' / 'atex-items-v1.jsonl'
CONTRACT = PKG / 'atex' / 'ATEXT-CONTRACT.md'
CONFIG = PKG / 'config.yaml'

FROZEN_TARGETS = ['शुभ दीपावली', 'आज की डील', 'Aaj ki Deal', 'SAVE 20% • ₹999']


def items():
    return [json.loads(x) for x in MANIFEST.read_text(encoding='utf-8').splitlines() if x.strip()]


# ------------------------------------------------------------------ PLAN invariants
def test_manifest_invariants():  # PLAN
    it = items()
    assert len(it) == 4
    assert len({x['item_id'] for x in it}) == 4
    assert all(x['operation'] == 'generate' for x in it)
    assert all(x['extra_text_forbidden'] is True for x in it)


# ------------------------------------------------------------------ frozen targets
def test_the_four_targets_are_exactly_the_frozen_strings():
    assert [x['target_string'] for x in items()] == FROZEN_TARGETS


def test_item_ids_match_the_frozen_config():
    cfg = yaml.safe_load(CONFIG.read_text(encoding='utf-8'))
    assert [x['item_id'] for x in items()] == cfg['atex']['items']


def test_the_pack_covers_devanagari_hinglish_and_a_commercial_claim():
    it = items()
    assert it[0]['script'] == 'devanagari'
    assert it[2]['script'] == 'latin_hinglish'
    assert any('₹' in x['target_string'] for x in it)


# ------------------------------------------------- the prompt isolates text, deliberately
def test_every_prompt_carries_its_target_exactly_once():
    for x in items():
        assert x['prompt'].count(x['target_string']) == 1


def test_every_prompt_forbids_any_other_text_logo_or_reference_identity():
    for x in items():
        p = x['prompt'].lower()
        assert 'only text' in p or 'only textual content' in p
        assert 'no logo' in p
        assert 'no other text' in p or 'no additional text' in p


def test_every_item_is_a_plain_one_to_one_poster():
    for x in items():
        assert x['aspect_ratio'] == '1:1'
        assert x['reference_identity'] is None
        assert x['product_identity'] is None


# --------------------------------------------------------------- repeats and seeds
def test_repeats_are_unseeded_on_both_routes():
    """Unseeded on purpose: the first comparison is an INHERENT-VARIANCE comparison."""
    for x in items():
        assert x['seed_policy'] == 'unseeded'
        assert x['seed'] is None
        assert x['repeats_per_slot'] == 2


def test_unseeded_evidence_is_marked_unpoolable_with_held_seed_evidence():
    for x in items():
        assert x['poolable_with_held_seed_evidence'] is False


# --------------------------------------------------------------- scoring and stop rule
def test_primary_score_is_blind_transcription_plus_code_comparison():
    for x in items():
        assert x['primary_measurement'] == 'transcribe_then_code_exact_comparison'
        assert x['verdict_is_diagnostic_only'] is True


def test_the_hard_elimination_rule_is_frozen_and_bounded():
    text = CONTRACT.read_text(encoding='utf-8')
    assert 'zero exact matches' in text
    assert 'not a universal model incapability' in text
    assert 'is not promotion' in text


def test_the_contract_states_atex_cannot_promote_a_slot():
    text = CONTRACT.read_text(encoding='utf-8').lower()
    assert 'partial evidence' in text
    assert 'stage-a survivor' in text


def test_no_cpao_may_be_reported():
    assert 'cpao' in CONTRACT.read_text(encoding='utf-8').lower()


# --------------------------------------------------------------- the 16-call ceiling
def test_four_items_two_repeats_two_routes_is_sixteen():
    cfg = yaml.safe_load(CONFIG.read_text(encoding='utf-8'))
    assert len(items()) * cfg['atex']['repeats_per_item'] * len(cfg['atex']['slots']) == 16


def test_manifest_is_deterministic_and_sorted():
    raw = MANIFEST.read_bytes()
    assert raw.endswith(b'\n')
    assert [x['item_id'] for x in items()] == sorted(x['item_id'] for x in items())
