#!/usr/bin/env python3
"""Render the worked CANON_CONTEXT example from committed ids — never by hand.

Same discipline as canon/experiments/v1/value-gate/build_oracle_contexts.py: every `principle` in
the example is pulled out of the committed SPEC-03 extraction by id, so the example cannot be
accidentally strengthened by a worker writing a better version of what a source said. The
surrounding fields (applicability, implication, failure mode, uncertainty, limits) are authored
here and are derived from the same records' scope, remedies, problems, caveats and evidence blocks.

Re-render:  python3 canon/context/build_example_context.py
Validate:   python3 canon/validation/validate_canon_context.py canon/context/examples/*.yaml
"""
import pathlib, subprocess, sys, yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
K = ROOT / 'canon/knowledge/current'
objs, owner, srcid = {}, {}, {}
for d in sorted(K.iterdir()):
    if not d.is_dir():
        continue
    sk = yaml.safe_load((d / 'source-knowledge.yaml').read_text()) or {}
    for o in sk.get('source_knowledge') or []:
        objs[o['sk_id']] = o
        owner[o['sk_id']] = d.name
        srcid[o['sk_id']] = sk.get('source_id')

def n(t): return ' '.join(str(t or '').split())
def claim(i): return n(objs[i]['claim'])
def loc(i): return n((objs[i].get('provenance') or {}).get('locator'))
def chars(i): return list((objs[i].get('evidence') or {}).get('characteristics') or [])

commit = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'],
                        capture_output=True, text=True).stdout.strip()

G = [
    ('KG-01', 'sk_lsm_c003_0014',
     'Polished, mirror-like surfaces — the steel case, crown and crystal. The source restricts the family of angles to direct reflection by its own stipulation (sk_lsm_c003_0013).',
     'Decide the highlight before the frame: size the key light to fill the family of angles for the case if the metal should read as lit across its length, or place camera and light so the source falls outside it if the case should read dark. There is no third setting; a light half in the family gives a partial highlight nobody chose.',
     'A light placed by eye lands partly inside the family, so the case carries an accidental highlight shape and the crystal a reflection of whatever is in front of it. This is the most common way a watch hero image is rejected.',
     'None recorded on the claim itself; the source states no mechanism (mechanism_absent) and the supporting figure was not inspected.'),
    ('KG-02', 'sk_lsm_c003_0017',
     'Black, dark or transparent subjects — a dark dial, a black strap, the crystal.',
     'Treat a dark dial as the place the direct reflection will show first, not the place it is safest. Its low diffuse return is what makes any stray reflection prominent, so control the direct component there before adding fill anywhere else.',
     'The dark dial is lit as if it were a dark object needing more light; the added source lands in the family of angles and the dial returns a visible reflection of it instead of reading black.',
     'None recorded — explicitly stated, argued, repeated within the source, mechanism given.'),
    ('KG-03', 'sk_fre_c003_0019',
     'A subject with strong intrinsic attraction surrounded by structure that converges on it — which a round watch face on a plain ground is.',
     'Centring is available for this subject rather than a default to be avoided; if the composition is centred, give the surround a reason to converge (concentric or flat ground) instead of leaving the watch merely in the middle of empty space.',
     'Centring is rejected on the general "bull\'s-eye" objection and the watch is pushed off-centre without a compositional reason, producing an arbitrary placement that neither centring nor the rule of thirds supports.',
     'The source asserts "any number of situations" and shows exactly one (extractor_observed); the figure was not inspected; and the same passage proposes to improve its own strongest centring case by cropping to square.'),
    ('KG-04', 'sk_hop_sa_0051',
     'Claims that can be stated as figures or definite facts — water resistance, movement accuracy, power reserve, warranty length.',
     'Replace each adjective in the on-image line with the figure behind it, if a figure exists. If no figure exists, the line is describing nothing and should be cut rather than softened.',
     'The hero line reads as approved marketing language that asserts quality without any statement that could be checked, so it carries no weight and occupies the space a checkable claim would have had.',
     'The believability mechanism rests on the premise that an advertiser cannot lie in the best media, stated as fact and unsupported; no comparison of a vague and a specific version of the same advertisement is reported.'),
    ('KG-05', 'sk_hop_sa_0050',
     'Written or spoken selling claims — here, the headline and any on-image copy.',
     'Remove superlatives outright rather than qualifying them. The cost is not the weak line itself but the discount the reader then applies to the specific claims sitting beside it.',
     'A superlative in the headline suggests looseness and carelessness of truth, and the specific figures elsewhere in the same image lose the credibility they would otherwise have had.',
     'The contamination claim — that a superlative discredits the advertiser\'s other statements — is the strongest part of this record and is asserted with no case, comparison or measurement.'),
]

Q = [
    ('PQ-01',
     'Where is the key light placed relative to the watch case and crystal?',
     'A polished case either carries a chosen highlight or an accidental one; a reflection of the room in the crystal is the single most common reason a watch hero image is not accepted.',
     ['KG-01', 'KG-02']),
    ('PQ-02',
     'Where does the watch sit in the frame, and is a centred composition defensible here?',
     'Placement is decided once and constrains crop, aspect ratio and every later repair; an unreasoned placement costs a regeneration rather than an edit.',
     ['KG-03']),
    ('PQ-03',
     'What does the on-image claim line actually say?',
     'The line is generated with the image and cannot be swapped cheaply afterwards; a line that asserts nothing checkable wastes the space and discounts the rest of the frame.',
     ['KG-04', 'KG-05']),
]

TRACE_EXTRA = ['sk_lsm_c003_0004', 'sk_lsm_c003_0010']

L = []
w = L.append
w('# CANON_CONTEXT — worked example, v0.1')
w('#')
w('# Rendered from committed ids, never written by hand (spec R5). Illustrative only: it is built')
w('# for EVAL-037 brief B06 (watch hero image), which is concluded evidence, and it authorises')
w('# nothing. Validate with:')
w('#   python3 canon/validation/validate_canon_context.py canon/context/examples/B06-watch-hero.canon-context.yaml')
w('')
w('canon_context_version: v0.1')
w('context_id: b06-watch-hero-v0-1')
w('')
w('built_for:')
w('  request_ref: EVAL-037/B06')
w('  outcome_kind: single hero product image, wristwatch, with an on-image claim line')
w(f'  built_at_commit: {commit}')
w('')
w('budget:')
w('  max_guidance_entries: 8')
w('  max_principle_bytes: 4096')
w('  max_serialized_bytes: 16384')
w('  basis: >-')
w('    Spec R1 defaults. The principle budget is the value-gate oracle contexts own upper bound')
w('    (3,655 bytes) rounded up; the total budget adds the six-field scaffolding the oracle')
w('    contexts never carried. Not calibrated against accepted-outcome evidence.')
w('')
w('production_questions:')
for qid, q, why, ans in Q:
    w(f'  - question_id: {qid}')
    w(f'    question: >-')
    w(f'      {q}')
    w(f'    why_it_matters: >-')
    w(f'      {why}')
    w(f'    answered_by: [{", ".join(ans)}]')
w('')
w('key_guidance:')
for gid, ref, appl, impl, fail, unc in G:
    w(f'  - guidance_id: {gid}')
    w(f'    principle: >-')
    w(f'      {claim(ref)}')
    w(f'    render_mode: verbatim_claim')
    w(f'    rendered_from: {{ref: {ref}, field: claim}}')
    w(f'    applicability: >-')
    w(f'      {appl}')
    w(f'    concrete_implication: >-')
    w(f'      {impl}')
    w(f'    failure_mode: >-')
    w(f'      {fail}')
    w(f'    evidence:')
    w(f'      source_dir: {owner[ref]}')
    w(f'      refs: [{ref}]')
    w(f'      characteristics: [{", ".join(chars(ref))}]')
    w(f'    uncertainty: >-')
    w(f'      {unc}')
w('')
w('conflicts:')
w('  - conflict_id: CF-01')
w('    between: [sk_lsm_c003_0004, sk_lsm_c003_0010]')
w('    nature: >-')
w('      The extraction records these two as contradicting each other. A diffuse reflection has the')
w('      same brightness from every viewing angle; a direct reflection is visible only from the one')
w('      angle the geometry determines. Both are asserted without qualification by the same source.')
w('    resolution_rule: >-')
w('      Resolve by surface, not by preference: the contradiction is a scope boundary the source')
w('      draws elsewhere, not an open question. Apply the direct-reflection rules to the case, crown')
w('      and crystal, and the diffuse rules to a leather strap or matte dial. A single lighting')
w('      decision covering the whole watch is what makes these two look incompatible.')
w('    unresolved: false')
w('')
w('do_not_overgeneralize:')
for gid, lim, why in [
    ('KG-01',
     'Applies to mirror-like surfaces only. It licenses nothing about the strap, a matte dial, fabric or skin.',
     'The source stipulates that a family of angles for diffuse reflection would be meaningless (sk_lsm_c003_0013), so the concept has no defined behaviour off polished surfaces.'),
    ('KG-03',
     'Not a rule that centring is right for round subjects. It removes an objection for one described case.',
     'The source asserts "any number of situations" and shows exactly one, and the figure was not available for inspection.'),
    ('KG-04',
     'Not evidence that specific copy outperforms vague copy. It is a practitioner argument about why it should.',
     'No comparison of a vague and a specific version of the same advertisement is reported; the tungsten-lamp and price-reduction lines are illustrations, not results.'),
    ('KG-05',
     'The contamination effect is not quantified and must not be traded off against anything as if it were.',
     'The claim that a superlative discredits an advertiser\'s other statements is asserted with no case, comparison or measurement.'),
    ('KG-01',
     'None of this is evidence that any image model can execute the placement it implies.',
     'Book knowledge is never evidence about model capability (PROJECT-MEMORY.md section 4.2); the Capability Registry holds zero rows.'),
]:
    w(f'  - guidance_id: {gid}')
    w(f'    limit: >-')
    w(f'      {lim}')
    w(f'    why: >-')
    w(f'      {why}')
w('')
w('source_trace:')
for ref in [g[1] for g in G] + TRACE_EXTRA:
    w(f'  - ref: {ref}')
    w(f'    kind: source_knowledge')
    w(f'    source_dir: {owner[ref]}')
    w(f'    source_id: {srcid[ref]}')
    w(f'    locator: "{loc(ref)}"')
    w(f'    audit_status: complete')

out = ROOT / 'canon/context/examples/B06-watch-hero.canon-context.yaml'
out.write_text('\n'.join(L) + '\n')
print('wrote', out, out.stat().st_size, 'bytes')
