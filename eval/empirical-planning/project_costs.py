#!/usr/bin/env python3
"""EVAL-039B cost projection — deterministic, offline, stdlib + PyYAML only.

    python3 project_costs.py --inputs COST-PROJECTION-INPUTS-2026-09.yaml \
        --roster ROSTER-REFRESH-2026-09.yaml \
        --out-yaml COST-PROJECTION-2026-09.yaml --out-md COST-PROJECTION-2026-09.md \
        [--test-cases TEST-CASES.yaml]

DEPENDENCY (stated as required by the task): generation COUNTS come from the campaign plan
(coordination/plans/2026-09-05-CAPABILITY-LAB-CAMPAIGN-v1.md §E, §C.3, §C.3c, §C.3d) as written into the
INPUTS file, until EVAL-039A's TEST-CASES.yaml exists. When it does, pass --test-cases <path>
(schema: items[].{item_id, routes[], repeats, seconds|chars|minutes}) and the counts are regenerated from
it instead of the INPUTS tranche lines; the evaluator lines, caps and assumptions still come from INPUTS.
Unit PRICES always come from the roster (regular_price only; promo prices are never read).

Rules implemented (task §4):
  * regular price only — promo_price is ignored entirely (promo_prices_used is always false);
  * a route or variant whose price is null, whose currency is not USD, whose unit cannot be converted with the
    line's unit_quantity, or whose route_status is not `pinned` contributes 0 and is listed under
    unpinned_lines_excluded with the reason — unless the roster gives a `fallback` whose status is `pinned`,
    in which case the fallback price is used and the line is billed as cash (the fallback's pool);
  * billing pool = the roster's billing_pool for the surface actually priced;
  * Seedance 2.5 uses the generation counts the plan gives (4 where it says 4);
  * Veo prices come from the Vertex pin (the roster's vertex records), never from fal;
  * outputs are byte-for-byte reproducible: no timestamps, ordered iteration, fixed rounding.
"""
import argparse
import math
import sys
from collections import OrderedDict

import yaml


def represent_odict(dumper, data):
    return dumper.represent_dict(data.items())


yaml.add_representer(OrderedDict, represent_odict)

PROJECTABLE_UNITS = {
    # unit token -> function(price, unit_quantity, unit_kind) -> per-generation USD
    'per_second': lambda p, q, k: p * q,
    'per_input_video_second': lambda p, q, k: p * q,
    'per_image': lambda p, q, k: p * 1.0,
    'per_image_first_megapixel': lambda p, q, k: p * 1.0,   # 1 MP outputs assumed (assumption A-03)
    'per_1000_characters': lambda p, q, k: p * q / 1000.0,
    'per_1M_characters': lambda p, q, k: p * q / 1e6,
    'per_minute': lambda p, q, k: p * q,
    'per_clip': lambda p, q, k: p * 1.0,
    'per_30s_clip': lambda p, q, k: p * 1.0,
}


def r4(x):
    return float(f'{x:.4f}')


def load(path):
    with open(path) as fh:
        return yaml.safe_load(fh)


def find_route(roster, route_key):
    for r in roster['routes']:
        if r['route_key'] == route_key:
            return r
    return None


def find_variant(route, name):
    for v in route.get('variants') or []:
        if v['variant'] == name:
            return v
    return None


def resolve_price(roster, route_key, variant):
    """Return (price_value, unit, pool, status, basis, reason_if_excluded)."""
    route = find_route(roster, route_key)
    if route is None:
        return None, None, None, 'missing', None, f'route_key {route_key} not in roster'
    target = route
    basis = f'{route_key} ({route["surface"]}: {route["surface_model_id"]})'
    if variant:
        v = find_variant(route, variant)
        if v is None:
            return None, None, None, 'missing', None, f'variant {variant} not in roster record {route_key}'
        target = v
        basis = f'{route_key}/{variant} ({route["surface"]}: {v["surface_model_id"]})'
    status = target.get('route_status')
    rp = target.get('regular_price') or {}
    pool = route['billing_pool']
    if status == 'pinned' and rp.get('value') is not None and rp.get('currency') == 'USD' and rp.get('unit') in PROJECTABLE_UNITS:
        return rp['value'], rp['unit'], pool, status, basis, None
    # try the route-level fallback (one level, task §1)
    fb = route.get('fallback')
    if fb and fb.get('route_status') == 'pinned':
        frp = fb.get('regular_price') or {}
        if frp.get('value') is not None and frp.get('currency') == 'USD' and frp.get('unit') in PROJECTABLE_UNITS:
            fbasis = f'{route_key} FALLBACK ({fb["surface"]}: {fb["surface_model_id"]})'
            return frp['value'], frp['unit'], fb['billing_pool'], 'pinned (fallback)', fbasis, None
    # excluded
    if status != 'pinned':
        reason = f'route_status {status}'
        if target.get('unpinned_reason'):
            reason += f' — {target["unpinned_reason"]}'
    elif rp.get('value') is None:
        reason = 'price null'
    elif rp.get('currency') != 'USD':
        reason = f'currency {rp.get("currency")} not projectable in USD (pinned_but_not_projectable)'
    else:
        reason = f'unit {rp.get("unit")} not convertible per generation (pinned_but_not_projectable)'
    return None, rp.get('unit'), pool, status, basis, reason


def lines_from_test_cases(tc):
    """Translate TEST-CASES.yaml items into projection lines (all placed in tranche T1a/T1b by item lane)."""
    out = []
    for item in tc.get('items', []):
        reps = int(item.get('repeats', 1))
        q = item.get('seconds') or item.get('chars') or item.get('minutes') or 1
        kind = 'seconds' if item.get('seconds') else 'chars' if item.get('chars') else 'minutes' if item.get('minutes') else 'images'
        for route in item['routes']:
            rk, _, var = route.partition('@')
            out.append(OrderedDict([('tranche', item.get('tranche', 'T1a')), ('route_key', rk), ('variant', var or None), ('lane', item.get('lane', 'test-case')),
                                    ('generations', reps), ('unit_quantity', q), ('unit_kind', kind), ('source', f'TEST-CASES.yaml item {item["item_id"]}')]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--inputs', required=True)
    ap.add_argument('--roster', required=True)
    ap.add_argument('--out-yaml', required=True)
    ap.add_argument('--out-md', required=True)
    ap.add_argument('--test-cases')
    a = ap.parse_args()
    inputs = load(a.inputs)
    roster = load(a.roster)
    caps = inputs['proposed_caps_usd']
    ev_prices = inputs['evaluator_prices']
    tranche_order = ['T0', 'T1a', 'T1b', 'T2', 'T3']

    # ---- generation lines -------------------------------------------------------------------
    lines = []
    if a.test_cases:
        lines = lines_from_test_cases(load(a.test_cases))
        count_source = f'TEST-CASES ({a.test_cases})'
    else:
        for t in inputs['tranches']:
            for ln in t.get('lines', []):
                d = OrderedDict(ln)
                d['tranche'] = t['tranche']
                lines.append(d)
        count_source = 'plan §E / §C.3 / §C.3c / §C.3d via INPUTS (no TEST-CASES.yaml yet)'

    priced = []
    excluded = []
    for ln in lines:
        val, unit, pool, status, basis, reason = resolve_price(roster, ln['route_key'], ln.get('variant'))
        gens = int(ln['generations'])
        row = OrderedDict([
            ('tranche', ln['tranche']), ('lane', ln.get('lane')), ('route_key', ln['route_key']), ('variant', ln.get('variant')),
            ('generations', gens), ('unit_quantity', ln.get('unit_quantity', 1)), ('unit_kind', ln.get('unit_kind', 'images')),
            ('source', ln.get('source')), ('addition', ln.get('addition')), ('note', ln.get('note')),
        ])
        if reason is None:
            per_gen = PROJECTABLE_UNITS[unit](float(val), float(ln.get('unit_quantity', 1)), ln.get('unit_kind'))
            row.update([('priced_on', basis), ('status', status), ('unit_price_usd', val), ('unit', unit), ('per_generation_usd', r4(per_gen)),
                        ('billing_pool', pool), ('line_usd', r4(per_gen * gens))])
            priced.append(row)
        else:
            row.update([('priced_on', basis), ('status', status), ('unit_price_usd', None), ('unit', unit), ('per_generation_usd', None),
                        ('billing_pool', pool), ('line_usd', 0.0), ('excluded_reason', reason)])
            excluded.append(row)

    # ---- T2 / T3 blended lines (assumption: route mix unknown until survivors are known) ----------
    t1 = [p for p in priced if p['tranche'] in ('T1a', 'T1b')]
    t1_gens = sum(p['generations'] for p in t1)
    t1_usd = sum(p['line_usd'] for p in t1)
    t1_cash = sum(p['line_usd'] for p in t1 if p['billing_pool'] == 'cash')
    blended = t1_usd / t1_gens if t1_gens else 0.0
    cash_share = (t1_cash / t1_usd) if t1_usd else 1.0
    for t in inputs['tranches']:
        if t.get('blended_generations'):
            g = int(t['blended_generations'])
            for pool, share in (('cash', cash_share), ('credits', 1.0 - cash_share)):
                priced.append(OrderedDict([
                    ('tranche', t['tranche']), ('lane', 'blended'), ('route_key', 'BLENDED-T1-AVERAGE'), ('variant', pool), ('generations', g if pool == 'cash' else 0),
                    ('unit_quantity', 1), ('unit_kind', 'generations'), ('source', t.get('blended_source')), ('addition', None),
                    ('note', f'{g} generations x blended Tranche-1 average USD {r4(blended)} per generation, split cash/credits in the Tranche-1 ratio ({r4(cash_share)} cash)'),
                    ('priced_on', 'Tranche-1 pinned lines (average)'), ('status', 'assumption'), ('unit_price_usd', r4(blended)), ('unit', 'per_generation_blended'),
                    ('per_generation_usd', r4(blended)), ('billing_pool', pool), ('line_usd', r4(blended * g * share))]))

    # ---- evaluators ---------------------------------------------------------------------------------
    ev_rows = []
    ev_excluded = []
    for t in inputs['tranches']:
        for e in t.get('evaluators', []):
            pr = ev_prices[e['evaluator']]
            calls = int(e['calls'])
            row = OrderedDict([('tranche', t['tranche']), ('evaluator', e['evaluator']), ('calls', calls), ('lanes', e.get('lanes')), ('source', e.get('source')),
                               ('unit_price_usd', pr.get('price_usd_per_call')), ('pinned', bool(pr.get('pinned'))), ('billing_pool', pr.get('billing_pool', 'cash'))])
            if pr.get('price_usd_per_call') is None:
                row['line_usd'] = 0.0
                row['excluded_reason'] = pr.get('unpinned_reason', 'price null')
                ev_excluded.append(row)
            else:
                row['line_usd'] = r4(calls * float(pr['price_usd_per_call']))
                ev_rows.append(row)

    # ---- by_tranche -----------------------------------------------------------------------------------
    by_tranche = []
    for tr in tranche_order:
        gl = [p for p in priced if p['tranche'] == tr]
        xl = [x for x in excluded if x['tranche'] == tr]
        el = [e for e in ev_rows if e['tranche'] == tr]
        ex = [e for e in ev_excluded if e['tranche'] == tr]
        cash = sum(p['line_usd'] for p in gl if p['billing_pool'] == 'cash') + sum(e['line_usd'] for e in el if e['billing_pool'] == 'cash')
        cred = sum(p['line_usd'] for p in gl if p['billing_pool'] == 'credits') + sum(e['line_usd'] for e in el if e['billing_pool'] == 'credits')
        total = cash + cred
        cap = caps.get(tr)
        nominal = sum(p['generations'] for p in gl if not p.get('addition')) + sum(x['generations'] for x in xl if not x.get('addition'))
        adds = sum(p['generations'] for p in gl if p.get('addition')) + sum(x['generations'] for x in xl if x.get('addition'))
        by_tranche.append(OrderedDict([
            ('tranche', tr),
            ('generations', sum(p['generations'] for p in gl) + sum(x['generations'] for x in xl)),
            ('generations_priced', sum(p['generations'] for p in gl)),
            ('generations_excluded_unpinned', sum(x['generations'] for x in xl)),
            ('generations_nominal_plan', nominal), ('generations_additions', adds),
            ('evaluator_calls', sum(e['calls'] for e in el) + sum(e['calls'] for e in ex)),
            ('evaluator_calls_excluded_unpinned', sum(e['calls'] for e in ex)),
            ('cash_usd', r4(cash)), ('credits_usd_equivalent', r4(cred)), ('total_usd_equivalent', r4(total)),
            ('unpinned_lines_excluded', [OrderedDict([('route_key', x['route_key']), ('variant', x['variant']), ('lane', x['lane']), ('generations', x['generations']), ('reason', x['excluded_reason'])]) for x in xl]
                                       + [OrderedDict([('evaluator', e['evaluator']), ('calls', e['calls']), ('reason', e['excluded_reason'])]) for e in ex]),
            ('priced_on_fallback', [OrderedDict([('route_key', p['route_key']), ('variant', p['variant']), ('lane', p['lane']), ('generations', p['generations']), ('priced_on', p['priced_on']), ('billing_pool', p['billing_pool']), ('usd', p['line_usd'])]) for p in gl if 'FALLBACK' in (p['priced_on'] or '')]),
            ('proposed_cap_usd', cap), ('headroom_usd', r4(cap - total) if cap is not None else None),
            ('within_cap', (total <= cap) if cap is not None else None),
        ]))

    # ---- by_route ---------------------------------------------------------------------------------------
    agg = OrderedDict()
    for p in priced + excluded:
        k = (p['route_key'], p['variant'] or '')
        if k not in agg:
            agg[k] = OrderedDict([('route_key', p['route_key']), ('variant', p['variant']), ('priced_on', p['priced_on']), ('status', p['status']), ('billing_pool', p['billing_pool']),
                                  ('unit_price_usd', p['unit_price_usd']), ('unit', p['unit']), ('generations', 0), ('usd', 0.0), ('tranches', []), ('excluded_reason', p.get('excluded_reason'))])
        agg[k]['generations'] += p['generations']
        agg[k]['usd'] = r4(agg[k]['usd'] + p['line_usd'])
        if p['tranche'] not in agg[k]['tranches']:
            agg[k]['tranches'].append(p['tranche'])
    by_route = list(agg.values())

    # ---- minimum viable round one -------------------------------------------------------------------------
    mvr_lanes = set(inputs['minimum_viable_round_one']['lanes'])
    mvr_gen = [p for p in priced if p['tranche'] in ('T1a', 'T1b') and p['lane'] in mvr_lanes and not p.get('addition')]
    mvr_ev = [e for e in ev_rows if e['tranche'] in ('T1a', 'T1b') and e.get('lanes') and set(e['lanes']) & mvr_lanes]
    mvr_cash = sum(p['line_usd'] for p in mvr_gen if p['billing_pool'] == 'cash') + sum(e['line_usd'] for e in mvr_ev if e['billing_pool'] == 'cash')
    mvr_cred = sum(p['line_usd'] for p in mvr_gen if p['billing_pool'] == 'credits') + sum(e['line_usd'] for e in mvr_ev if e['billing_pool'] == 'credits')
    t1_total = sum(t['total_usd_equivalent'] for t in by_tranche if t['tranche'] in ('T1a', 'T1b'))
    mvr = OrderedDict([
        ('definition', inputs['minimum_viable_round_one']['definition']),
        ('lanes', sorted(mvr_lanes)),
        ('generations', sum(p['generations'] for p in mvr_gen)),
        ('evaluator_calls', sum(e['calls'] for e in mvr_ev)),
        ('evaluator_note', 'evaluator lines whose lanes touch the minimum round are counted in full (upper bound), not apportioned'),
        ('cash_usd', r4(mvr_cash)), ('credits_usd_equivalent', r4(mvr_cred)), ('total_usd_equivalent', r4(mvr_cash + mvr_cred)),
        ('tranche_1_total_for_comparison', r4(t1_total)), ('is_subset_of_tranche_1', (mvr_cash + mvr_cred) <= t1_total + 1e-9),
        ('routes', [OrderedDict([('route_key', p['route_key']), ('variant', p['variant']), ('lane', p['lane']), ('generations', p['generations']), ('billing_pool', p['billing_pool']), ('usd', p['line_usd'])]) for p in mvr_gen]),
    ])

    # ---- totals / assumptions / output ------------------------------------------------------------------
    total_cash = r4(sum(t['cash_usd'] for t in by_tranche))
    total_cred = r4(sum(t['credits_usd_equivalent'] for t in by_tranche))
    music8 = inputs.get('music_lane_alternative_8', {})
    assumptions = [OrderedDict(x) for x in inputs['assumptions']]
    assumptions.append(OrderedDict([('id', 'A-BLEND'), ('assumption', f'T2 and T3 are priced at the blended Tranche-1 average of USD {r4(blended)} per generation (Tranche-1 pinned lines: {t1_gens} generations, USD {r4(t1_usd)}), split {r4(cash_share)} cash / {r4(1 - cash_share)} credits, because survivors are unknown until Stage A runs'), ('source', 'assumption (Executor); counts from plan §E')]))
    out = OrderedDict([
        ('meta', OrderedDict([('task', 'EVAL-039B'), ('status', 'PLANNING_ONLY_NOT_AUTHORISED'), ('generator', 'project_costs.py'), ('roster', a.roster), ('inputs', a.inputs),
                              ('count_source', count_source), ('price_source', 'ROSTER-REFRESH-2026-09.yaml regular_price (pinned) / fallback; never promo'),
                              ('promo_prices_used', False), ('credits_assumption_source', 'survey-2026-09-05 §4'), ('credit_balances', 'unknown (MD-1)'),
                              ('currency', 'USD list prices before tax; INR lines not converted')])),
        ('headline', OrderedDict([
            ('tranche_1_generations', sum(t['generations'] for t in by_tranche if t['tranche'] in ('T1a', 'T1b'))),
            ('tranche_1_cash_usd', r4(sum(t['cash_usd'] for t in by_tranche if t['tranche'] in ('T1a', 'T1b')))),
            ('tranche_1_credits_usd_equivalent', r4(sum(t['credits_usd_equivalent'] for t in by_tranche if t['tranche'] in ('T1a', 'T1b')))),
            ('tranche_1_total_usd_equivalent', r4(t1_total)), ('tranche_1_cap_usd', r4((caps.get('T1a') or 0) + (caps.get('T1b') or 0))),
            ('minimum_viable_round_one_usd_equivalent', mvr['total_usd_equivalent']),
            ('all_tranches_cash_usd', total_cash), ('all_tranches_credits_usd_equivalent', total_cred), ('all_tranches_total_usd_equivalent', r4(total_cash + total_cred)),
            ('all_tranches_cap_usd', r4(sum(v for v in caps.values() if v))),
        ])),
        ('by_tranche', by_tranche), ('by_route', by_route), ('minimum_viable_round_one', mvr),
        ('music_lane_alternative_8', OrderedDict([('note', music8.get('note')), ('extra_generations', music8.get('extra_generations')),
                                                  ('extra_usd_equivalent', r4(sum(p['per_generation_usd'] for p in priced if p['lane'] == 'music') if music8 else 0.0))])),
        ('evaluator_lines', ev_rows + ev_excluded), ('generation_lines', priced + excluded),
        ('assumptions', assumptions), ('promo_prices_used', False), ('credits_assumption_source', 'survey-2026-09-05 §4'), ('credit_balances', 'unknown (MD-1)'),
    ])
    with open(a.out_yaml, 'w') as fh:
        fh.write('# COST-PROJECTION-2026-09 — generated by project_costs.py; do not edit by hand (regenerate).\n')
        fh.write('# PLANNING ONLY. Nothing here authorises spend. Prices: regular list prices pinned in ROSTER-REFRESH-2026-09.yaml; promo never used.\n')
        fh.write(yaml.dump(out, sort_keys=False, allow_unicode=True, width=200))
    write_md(a.out_md, out, inputs, caps)


def write_md(path, out, inputs, caps):
    h = out['headline']
    bt = {t['tranche']: t for t in out['by_tranche']}
    mvr = out['minimum_viable_round_one']
    L = []
    L.append('# Cost projection for the September 2026 battery — plain-English reading of COST-PROJECTION-2026-09.yaml')
    L.append('')
    L.append('**Status: planning only. Nothing here authorises spend.** Generated by `project_costs.py` from the pinned roster; regenerate, do not edit.')
    L.append('')
    L.append('## The three numbers the Controller must approve')
    L.append('')
    L.append(f"1. **Tranche 1 total ≈ USD {h['tranche_1_total_usd_equivalent']:.2f}** against the proposed cap of USD {h['tranche_1_cap_usd']:.0f} (1a {caps.get('T1a')} + 1b {caps.get('T1b')}): "
             f"≈ USD {h['tranche_1_cash_usd']:.2f} cash on fal/direct vendors + ≈ USD {h['tranche_1_credits_usd_equivalent']:.2f} that would come off cloud credits if the credits exist (balances unverified, MD-1).")
    L.append(f"2. **Minimum viable round one ≈ USD {mvr['total_usd_equivalent']:.2f}** (USD {mvr['cash_usd']:.2f} cash + USD {mvr['credits_usd_equivalent']:.2f} credits): image core + text-to-video + image-to-video only, with their evaluators. This is the smallest round that still answers the routing questions.")
    L.append(f"3. **The caps** (USD {caps.get('T1a')} / {caps.get('T1b')} / {caps.get('T2')} / {caps.get('T3')}): T1a is {'within' if bt['T1a']['within_cap'] else 'OVER'} its cap by USD {abs(bt['T1a']['headroom_usd']):.2f}; T1b is {'within' if bt['T1b']['within_cap'] else 'OVER'} its cap by USD {abs(bt['T1b']['headroom_usd']):.2f}. See MD-6.")
    L.append('')
    L.append('## What this means')
    L.append('')
    L.append('- **Cash vs credits.** A route on Vertex AI, Bedrock or Azure Foundry is billed to that cloud account; if the account holds startup credits, that money is credits, not cash. '
             'Whether the three accounts actually hold credits was **not checked** tonight (no billing read was attempted) — so treat "credits" as "not cash if the credits exist", and the cap as a USD ceiling across both pools.')
    L.append('- **Two Azure routes are priced but not yet usable** (gpt-image-2, FLUX.2-pro need a resource + deployment: MD-9). Until then they are projected on fal at cash prices; the moment the deployment exists, USD '
             f"{sum(r['usd'] for r in out['by_route'] if 'FALLBACK' in (r['priced_on'] or '')):.2f} of Tranche 1 moves from cash to credits.")
    L.append('- **Regular prices only.** MiniMax H3 Max is on a 75 % launch promotion until 7 September (USD 0.02/s at 768p); the projection uses the post-promotion USD 0.08/s. Nothing in the totals relies on a promotion.')
    L.append('- **Video dominates.** Seedance 2.5 alone (USD 0.473 per second at 720p, 4 generations per lane) is the single largest cost line; Veo Fast / Lite / full, Omni Flash and Lyria are the credit-eligible lines.')
    L.append('')
    L.append('## By tranche')
    L.append('')
    L.append('| Tranche | Generations (priced / excluded) | Evaluator calls | Cash USD | Credits USD-eq | Total USD-eq | Cap | Headroom |')
    L.append('|---|---:|---:|---:|---:|---:|---:|---:|')
    for t in out['by_tranche']:
        L.append(f"| {t['tranche']} | {t['generations']} ({t['generations_priced']} / {t['generations_excluded_unpinned']}) | {t['evaluator_calls']} | {t['cash_usd']:.2f} | {t['credits_usd_equivalent']:.2f} | {t['total_usd_equivalent']:.2f} | {t['proposed_cap_usd'] if t['proposed_cap_usd'] is not None else '—'} | {t['headroom_usd'] if t['headroom_usd'] is not None else '—'} |")
    L.append('')
    L.append(f"All tranches: cash ≈ USD {h['all_tranches_cash_usd']:.2f}, credits ≈ USD {h['all_tranches_credits_usd_equivalent']:.2f}, total ≈ USD {h['all_tranches_total_usd_equivalent']:.2f} against caps totalling USD {h['all_tranches_cap_usd']:.0f}. "
             'T2 and T3 use a blended per-generation average because their route mix is unknown until Stage A has survivors (assumption A-BLEND).')
    L.append('')
    L.append('## Lines excluded because unpinned or not usable (they count 0 in the totals)')
    L.append('')
    L.append('| Tranche | Line | Generations / calls | Why excluded |')
    L.append('|---|---|---:|---|')
    for t in out['by_tranche']:
        for x in t['unpinned_lines_excluded']:
            name = x.get('route_key', x.get('evaluator')) + (f"/{x['variant']}" if x.get('variant') else '')
            L.append(f"| {t['tranche']} | {name} | {x.get('generations', x.get('calls'))} | {x['reason']} |")
    L.append('')
    L.append('Routes whose credit surface is priced but not yet enabled are **not** excluded: they are priced on their fal fallback as cash and listed per tranche under `priced_on_fallback` in the YAML (gpt-image-2, FLUX.2-pro — MD-9).')
    L.append('')
    L.append('Plain English: these lines are real work the plan wants, but tonight there is no verified price or no access, so they add USD 0 to the totals. Each one becomes a number the moment its blocker (key, deployment, id) is resolved — the totals above are therefore a floor, not a ceiling.')
    L.append('')
    L.append('## Minimum viable round one')
    L.append('')
    L.append(f"{mvr['definition']} — {mvr['generations']} generations and up to {mvr['evaluator_calls']} evaluator calls, ≈ USD {mvr['total_usd_equivalent']:.2f} (cash {mvr['cash_usd']:.2f}, credits {mvr['credits_usd_equivalent']:.2f}).")
    L.append('')
    L.append('| Route | Lane | Generations | Pool | USD |')
    L.append('|---|---|---:|---|---:|')
    for r in mvr['routes']:
        L.append(f"| {r['route_key']}{('/' + r['variant']) if r['variant'] else ''} | {r['lane']} | {r['generations']} | {r['billing_pool']} | {r['usd']:.2f} |")
    L.append('')
    L.append('## Largest cost lines (all tranches)')
    L.append('')
    L.append('| Route | Priced on | Pool | Generations | USD |')
    L.append('|---|---|---|---:|---:|')
    for r in sorted([r for r in out['by_route'] if r['usd']], key=lambda r: -r['usd'])[:12]:
        L.append(f"| {r['route_key']}{('/' + r['variant']) if r['variant'] else ''} | {r['priced_on']} | {r['billing_pool']} | {r['generations']} | {r['usd']:.2f} |")
    L.append('')
    L.append('## Music lane (MD-7)')
    L.append('')
    m8 = out['music_lane_alternative_8']
    L.append(f"Totals use 4 music generations (2 briefs × 2). If the Controller reads \"2 briefs × 2\" as 8, add {m8['extra_generations']} generations ≈ USD {m8['extra_usd_equivalent']:.2f}. {m8['note']}")
    L.append('')
    L.append('## Assumptions (each traceable)')
    L.append('')
    for x in out['assumptions']:
        L.append(f"- **{x['id']}** — {x['assumption']} _(source: {x['source']})_")
    L.append('')
    L.append('## What is NOT in these numbers')
    L.append('')
    L.append('Taxes; account pre-funding above consumed usage (fal, Sarvam); retries (0 authorised); human review time; Cloud Vision / VLM evaluator prices are plan nominals, not pinned; ASR evaluator is unpriced (model unnamed); anything marked excluded above.')
    L.append('')
    with open(path, 'w') as fh:
        fh.write('\n'.join(L))


if __name__ == '__main__':
    sys.exit(main())
