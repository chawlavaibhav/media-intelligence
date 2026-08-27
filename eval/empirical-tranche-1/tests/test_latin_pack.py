"""Structural controls on the frozen Latin exact-text qualification pack.

The pack exists for one job: qualify a text judge against correctly formed but WRONG Latin text.
It is not evidence about any generator. Every control below is a way the pack could quietly stop
being a fair test — an unbalanced stratum, a mismatch nobody can see, a base string that carries
the answer, a rebuild that is not reproducible — and each one must fail loudly.

The three cases carried verbatim from the implementation plan are marked PLAN.
"""
import json
import subprocess
import sys
import unicodedata
from pathlib import Path

import pytest

import build_latin_pack as blp

PKG = Path(__file__).resolve().parents[1]
PACK = PKG / 'text_qualification' / 'latin-pack-v1.jsonl'
FINGERPRINT = PKG / 'text_qualification' / 'latin-pack-v1.sha256'

ALLOWED_CLASSES = {'confusable_substitution', 'omission', 'insertion', 'transposition',
                   'case_diacritic', 'punctuation_digit_space'}


def rows():
    return [json.loads(x) for x in PACK.read_text(encoding='utf-8').splitlines() if x.strip()]


# ------------------------------------------------------------------ balance
def test_pack_is_exactly_96_balanced_items():  # PLAN
    r = rows()
    assert len(r) == 96
    assert sum(x['expected'] == 'match' for x in r) == 48
    assert sum(x['expected'] == 'mismatch' for x in r) == 48


def test_one_mismatch_per_base_string():  # PLAN
    mismatches = [x for x in rows() if x['expected'] == 'mismatch']
    assert len({x['base_id'] for x in mismatches}) == 48


def test_mismatch_classes_are_controlled():  # PLAN
    assert {x['failure_class'] for x in rows() if x['expected'] == 'mismatch'} <= ALLOWED_CLASSES


def test_every_base_string_appears_in_both_strata():
    """Base identity must carry no signal. A judge cannot win by memorising which strings are bad."""
    r = rows()
    matched = {x['base_id'] for x in r if x['expected'] == 'match'}
    mismatched = {x['base_id'] for x in r if x['expected'] == 'mismatch'}
    assert matched == mismatched
    assert len(matched) == 48


def test_neither_trivial_strategy_beats_a_coin():
    r = rows()
    assert sum(x['expected'] == 'match' for x in r) / len(r) == 0.5


def test_every_failure_class_is_equally_represented():
    r = [x for x in rows() if x['expected'] == 'mismatch']
    counts = {c: sum(x['failure_class'] == c for x in r) for c in ALLOWED_CLASSES}
    assert set(counts.values()) == {8}, counts


def test_match_items_declare_no_failure_class():
    assert all(x['failure_class'] is None for x in rows() if x['expected'] == 'match')


# ------------------------------------------------- truth known by construction
def test_a_match_item_renders_exactly_its_target():
    for x in rows():
        if x['expected'] == 'match':
            assert x['rendered_string'] == x['target_string']


def test_a_mismatch_renders_something_other_than_its_target():
    for x in rows():
        if x['expected'] == 'mismatch':
            assert x['rendered_string'] != x['target_string']


def test_every_mismatch_differs_after_nfc_not_merely_in_codepoints():
    """Two encodings of one accented letter draw the same picture.

    The Devanagari battery learned this the hard way with the nukta. A 'mismatch' that is only an
    encoding difference would mark a judge WRONG for correctly reporting what it saw.
    """
    for x in rows():
        if x['expected'] == 'mismatch':
            a = unicodedata.normalize('NFC', x['rendered_string'])
            b = unicodedata.normalize('NFC', x['target_string'])
            assert a != b, x['item_id']


def test_the_target_of_a_mismatch_is_its_base_string():
    """The judge is shown wrong text and asked about the RIGHT string. That is the trap."""
    for x in rows():
        if x['expected'] == 'mismatch':
            assert x['target_string'] == x['base_string']


def test_each_mismatch_is_exactly_one_controlled_edit():
    for x in rows():
        if x['expected'] == 'mismatch':
            assert blp.classify_edit(x['base_string'], x['rendered_string']) == x['failure_class'], \
                (x['item_id'], x['base_string'], x['rendered_string'], x['failure_class'])


def test_every_item_carries_an_edit_detail_a_human_can_audit():
    for x in rows():
        if x['expected'] == 'mismatch':
            assert isinstance(x['edit_detail'], str) and x['edit_detail'].strip()


# ------------------------------------------------------------------ isolation
def test_the_pack_is_latin_only_and_contains_no_devanagari():
    for x in rows():
        for value in (x['base_string'], x['target_string'], x['rendered_string']):
            assert not any('ऀ' <= ch <= 'ॿ' for ch in value), x['item_id']


def test_builder_refuses_to_write_inside_the_frozen_devanagari_battery(tmp_path):
    repo = PKG.parents[1]
    forbidden = repo / 'eval' / 'battery' / 'devanagari-exactness' / 'latin-pack-v1.jsonl'
    with pytest.raises(blp.ForbiddenOutputPath):
        blp.build(out_path=forbidden)


def test_builder_refuses_any_path_under_the_battery_even_nested(tmp_path):
    repo = PKG.parents[1]
    forbidden = repo / 'eval' / 'battery' / 'devanagari-exactness' / 'build' / 'x' / 'p.jsonl'
    with pytest.raises(blp.ForbiddenOutputPath):
        blp.build(out_path=forbidden)


# -------------------------------------------------------------- determinism
def test_rebuilding_reproduces_the_committed_bytes_exactly(tmp_path):
    out = tmp_path / 'latin-pack-v1.jsonl'
    blp.build(out_path=out)
    assert out.read_bytes() == PACK.read_bytes()


def test_committed_fingerprint_matches_the_committed_manifest():
    import hashlib
    digest = hashlib.sha256(PACK.read_bytes()).hexdigest()
    assert FINGERPRINT.read_text(encoding='utf-8').split()[0] == digest


def test_records_are_sorted_by_item_id_with_stable_key_order():
    r = rows()
    assert [x['item_id'] for x in r] == sorted(x['item_id'] for x in r)
    keys = [tuple(x.keys()) for x in r]
    assert len(set(keys)) == 1


def test_the_manifest_ends_with_a_newline_and_has_no_blank_lines():
    raw = PACK.read_bytes()
    assert raw.endswith(b'\n')
    assert b'\n\n' not in raw


def test_the_builder_makes_no_network_call(monkeypatch, tmp_path):
    import socket

    def explode(*a, **k):
        raise AssertionError('the pack builder attempted a network connection')

    monkeypatch.setattr(socket.socket, 'connect', explode)
    monkeypatch.setattr(socket, 'create_connection', explode)
    blp.build(out_path=tmp_path / 'p.jsonl')
