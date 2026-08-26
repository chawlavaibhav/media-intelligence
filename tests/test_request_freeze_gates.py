"""CANON-010 negative controls — prove every mechanical gate actually fires.

A gate that never fails proves nothing. Each test below deliberately breaks one invariant the
CANON-010 task requires the validator to catch, confirms the validator rejects it, and restores the
file. Nothing here is left mutated: every mutation is wrapped in try/finally against the original
bytes, including the frozen 30-brief bank.

Run standalone (python3 tests/test_request_freeze_gates.py) or under pytest.
"""
import subprocess, sys, json, pathlib, shutil, tempfile, yaml
ROOT = pathlib.Path('/home/user/media-intelligence')
V = ROOT/'canon/experiments/pre-execution-freeze/validate_request_freeze.py'
SRC = ROOT/'canon/experiments/pre-execution-freeze/request-coverage-extension-source.yaml'
BANK = ROOT/'canon/experiments/v1/brief-bank/briefs-source.yaml'

def run():
    r = subprocess.run([sys.executable, str(V)], capture_output=True, text=True, cwd=ROOT)
    return r.returncode, json.loads(r.stdout)

def with_mutation(fn, path):
    orig = path.read_bytes()
    try:
        fn()
        return run()
    finally:
        path.write_bytes(orig)

results = {}

# G1 — touch the frozen bank
def m1(): BANK.write_text(BANK.read_text() + "\n# tamper\n")
code, out = with_mutation(m1, BANK)
results['G1_bank_changed'] = (code == 1 and any('[G1]' in e for e in out.get('errors', [])))

def mutate_item(mutator):
    d = yaml.safe_load(SRC.read_text()); mutator(d)
    SRC.write_text(yaml.dump(d, allow_unicode=True, sort_keys=False))

# G2 — drop deliverable_set
def m2(): mutate_item(lambda d: d['items'][0].pop('deliverable_set'))
code, out = with_mutation(m2, SRC)
results['G2_missing_cardinality'] = (code == 1 and any('[G2]' in e for e in out.get('errors', [])))

# G3 — workflow value as the requested operation
def m3(): mutate_item(lambda d: d['items'][0].__setitem__('requested_operation', 'inpaint'))
code, out = with_mutation(m3, SRC)
results['G3_workflow_as_operation'] = (code == 1 and any('[G3]' in e for e in out.get('errors', [])))

# G4 — claim customer provenance with no evidence quote
def m4():
    def f(d):
        d['items'][0]['mutation_intents']['intents'][0]['detail'] = 'customer named this explicitly'
    mutate_item(f)
code, out = with_mutation(m4, SRC)
results['G4_invented_customer_provenance'] = (code == 1 and any('[G4]' in e for e in out.get('errors', [])))

# G5 — mark the multi-turn probe runnable
def m5():
    def f(d):
        for i in d['items']:
            if i['item_id'] == 'RX-11':
                i['runnable_wave1'] = True
    mutate_item(f)
code, out = with_mutation(m5, SRC)
results['G5_runnable_multiturn'] = (code == 1 and any('[G5]' in e for e in out.get('errors', [])))

# G6 — a non-English item with no language dependency
def m6():
    def f(d):
        for i in d['items']:
            if i['item_id'] == 'RX-02':
                i['language_dependency'] = None
    mutate_item(f)
code, out = with_mutation(m6, SRC)
results['G6_unearned_language'] = (code == 1 and any('[G6]' in e for e in out.get('errors', [])))

# G7 — a grammar field missing its provenance rule
G = ROOT/'canon/experiments/pre-execution-freeze/MEDIA-REQUEST-GRAMMAR-v1.yaml'
def m7():
    d = yaml.safe_load(G.read_text()); d['fields'][0].pop('provenance_rule')
    G.write_text(yaml.dump(d, allow_unicode=True, sort_keys=False))
code, out = with_mutation(m7, G)
results['G7_grammar_field_without_rule'] = (code == 1 and any('[G7]' in e for e in out.get('errors', [])))

print(json.dumps(results, indent=2))
sys.exit(0 if all(results.values()) else 1)


def test_all_gates_fire():
    """pytest entry point: every gate must reject its corresponding violation."""
    assert all(results.values()), [k for k, v in results.items() if not v]
