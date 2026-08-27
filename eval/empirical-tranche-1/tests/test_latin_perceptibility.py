"""Perceptibility controls for the Latin pack.

A mismatch nobody can SEE is not a hard item — it is a way to mark a judge wrong for correctly
reporting what was drawn. The Devanagari battery learned this twice (precomposed nukta; the
zero-width non-joiner) and settled on one rule: a difference must survive NFC *and* show up in the
DECODED RASTER.

This module applies the same rule to Latin, and keeps two things strictly apart:

  MECHANICAL perceptibility  — decided on pixels, by code, here, at zero spend. Committed.
  HUMAN perceptibility       — 'can a person reading a real surface tell?' completed by a real
                               reviewer after rendering. The answers are now durable evidence and
                               routine rebuilds must preserve them.
"""
import csv
import json
from pathlib import Path

import pytest

import render_latin_pack as rlp
import human_review as HR

PKG = Path(__file__).resolve().parents[1]
TQ = PKG / 'text_qualification'
MECHANICAL = TQ / 'perceptibility-mechanical.json'
HUMAN_SHEET = TQ / 'perceptibility-review.csv'


def record():
    return json.loads(MECHANICAL.read_text(encoding='utf-8'))


# ------------------------------------------------------ the gate actually fires
def test_the_pixel_gate_calls_a_real_corruption_visible(tmp_path):
    assert rlp.is_visibly_different('Flat 50% Off', 'Flat 5O% Off', tmp_path) is True


def test_the_pixel_gate_calls_a_zero_width_edit_invisible(tmp_path):
    """NEGATIVE CONTROL. A zero-width space differs in codepoints and draws identical pixels.

    If this returns True the gate is comparing something other than the picture, and every
    'visible' verdict it has ever issued is worthless.
    """
    assert rlp.is_visibly_different('Flat 50% Off', 'Flat 50%​ Off', tmp_path) is False


def test_the_pixel_gate_calls_an_identical_string_invisible(tmp_path):
    assert rlp.is_visibly_different('MEGA SALE', 'MEGA SALE', tmp_path) is False


# --------------------------------------------------- the committed record
def test_mechanical_record_covers_every_mismatch_item():
    r = record()
    assert len(r['items']) == 48
    assert r['pack_sha256'] == (TQ / 'latin-pack-v1.sha256').read_text().split()[0]


def test_every_mismatch_is_visible_in_decoded_pixels():
    bad = [i['item_id'] for i in record()['items'] if not i['visible_in_decoded_pixels']]
    assert bad == [], f'invisible mismatches would penalise a correct judge: {bad}'


def test_every_mismatch_also_differs_after_nfc():
    bad = [i['item_id'] for i in record()['items'] if not i['differs_after_nfc']]
    assert bad == []


def test_record_pins_the_exact_font_bytes_it_rendered_with():
    prov = record()['render_provenance']
    assert prov['font_sha256'] and len(prov['font_sha256']) == 64
    assert prov['font_file'] and prov['point_size']
    assert prov['tool'] == 'hb-view'


def test_record_declares_zero_spend_and_zero_calls():
    r = record()
    assert r['external_calls'] == 0
    assert r['spend_usd'] == '0'


# ------------------------------------------------ the completed human review
def test_human_sheet_has_the_required_columns():
    with HUMAN_SHEET.open(encoding='utf-8') as fh:
        header = next(csv.reader(fh))
    assert header == ['item_id', 'visible_difference', 'usable_surface', 'reviewer_note']


def test_committed_human_review_satisfies_the_frozen_rule_and_pack_binding():
    status = HR.review_status(HUMAN_SHEET)
    assert status['ok'] is True
    assert status['items_reviewed'] == 96
    assert status['usable_yes'] == 96
    assert status['mismatch_visible_yes'] == 48
    assert status['bound_rows'] == 96


def test_match_rows_do_not_need_a_visible_difference_verdict():
    with HUMAN_SHEET.open(encoding='utf-8') as fh:
        rows = list(csv.DictReader(fh))
    assert any(r['visible_difference'] == '' for r in rows)
    assert HR.resolved(HUMAN_SHEET) is True


def test_renderer_preserves_an_existing_completed_review(tmp_path, monkeypatch):
    p = tmp_path / 'review.csv'
    p.write_text('item_id,visible_difference,usable_surface,reviewer_note\n'
                 'sentinel,,yes,do-not-overwrite\n')
    monkeypatch.setattr(rlp, 'HUMAN_SHEET', p)
    before = p.read_bytes()
    rlp._ensure_human_sheet([])
    assert p.read_bytes() == before


def test_record_marks_human_review_complete():
    r = record()
    human = r['human_perceptibility_review']
    assert human['status'] == 'COMPLETE_HUMAN_REVIEW'
    assert human['resolved'] is True
    assert human['usable_yes'] == 96
    assert human['mismatch_visible_yes'] == 48
    assert human['performed_by_this_worker'] is False


# ------------------------------------------------------------------ isolation
def test_renderer_refuses_to_write_inside_the_frozen_devanagari_battery():
    battery = PKG.parents[1] / 'eval' / 'battery' / 'devanagari-exactness' / 'build'
    with pytest.raises(rlp.ForbiddenOutputPath):
        rlp.render_pack(out_dir=battery)
