#!/usr/bin/env python3
"""Check an allocation for leakage between protected and non-protected roles, at three levels.

USAGE
  python3 resources/v1/validators/check_allocation_leakage.py <allocation.yaml> [more.yaml ...]

EXIT CODES
  0  every allocation passed
  1  at least one allocation leaks
  2  the tool could not do its job (missing/empty/unparseable input, no items resolved)

Exit 2 is deliberately distinct from exit 1. "I found no leak" and "I could not look" must never
produce the same result: an empty check is not a passing check.
"""
import json, os, sys, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lineage_keys as lk

try:
    import yaml
except ImportError:
    print("[FAIL] PyYAML not available", file=sys.stderr); sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MANIFEST = os.path.join(ROOT, "manifests", "corpus-pilot-v0.jsonl")
VIEWS_DIR = os.path.join(ROOT, "v1", "views")

PROTECTED = {"qualification", "reserve"}
EXPOSED = {"development", "calibration"}
LEVEL_ORDER = ["byte", "content", "source_lineage"]


def fatal(msg):
    print(f"[FAIL] {msg}", file=sys.stderr)
    sys.exit(2)


def load_manifest():
    if not os.path.isfile(MANIFEST):
        fatal(f"manifest not found: {MANIFEST}")
    recs = []
    with open(MANIFEST) as fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                recs.append(json.loads(line))
            except json.JSONDecodeError as e:
                fatal(f"manifest line {n} unparseable: {e}")
    if len(recs) < 1000:
        fatal(f"only {len(recs)} manifest records; refusing to check leakage against a truncated manifest")
    diag = lk.build_content_index(recs)
    return {r["item_id"]: r for r in recs}, diag


def load_view(view_id):
    path = os.path.join(VIEWS_DIR, view_id + ".jsonl")
    if not os.path.isfile(path):
        fatal(f"allocation references view '{view_id}' but {path} does not exist")
    ids = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line:
                ids.append(json.loads(line)["item_id"])
    if not ids:
        fatal(f"view '{view_id}' is empty; refusing to treat an empty role as a passing role")
    return ids


def resolve(assignments, index):
    """role -> list of manifest records. Unknown item ids are fatal, never skipped."""
    out = {}
    for role, entries in assignments.items():
        ids = []
        for e in entries or []:
            if isinstance(e, dict) and "view" in e:
                ids.extend(load_view(e["view"]))
            else:
                ids.append(e)
        recs = []
        for i in ids:
            if i not in index:
                fatal(f"role '{role}' references item id not present in the manifest: {i}")
            recs.append(index[i])
        if not recs:
            fatal(f"role '{role}' resolved to zero items")
        out[role] = recs
    return out


def check_one(path, index, diag):
    if not os.path.isfile(path):
        fatal(f"allocation file not found: {path}")
    with open(path) as fh:
        doc = yaml.safe_load(fh)
    if not doc:
        fatal(f"allocation file parsed to nothing: {path}")
    for f in ("experiment_id", "allocation_version", "independence_level", "assignments"):
        if f not in doc:
            fatal(f"{path}: missing required field '{f}'")
    level = doc["independence_level"]
    if level not in LEVEL_ORDER:
        fatal(f"{path}: unknown independence_level {level!r}")

    roles = resolve(doc["assignments"], index)
    print(f"\n=== {doc['experiment_id']} v{doc['allocation_version']} "
          f"({os.path.basename(path)}) · required independence: {level} ===")
    for r, recs in sorted(roles.items()):
        print(f"    {r:14s} {len(recs):>6,d} items")

    # A stricter level implies the weaker ones: content collisions matter when byte is required too.
    levels_to_check = LEVEL_ORDER[:LEVEL_ORDER.index(level) + 1]
    errors = []

    for lv in levels_to_check:
        keyfn = lk.LEVELS[lv]
        keys = {r: {keyfn(x) for x in recs} for r, recs in roles.items()}
        pairs = []
        for p in sorted(PROTECTED & set(roles)):
            for e in sorted(EXPOSED & set(roles)):
                pairs.append((p, e))
        if "qualification" in roles and "reserve" in roles:
            pairs.append(("qualification", "reserve"))
        for a, b in pairs:
            shared = keys[a] & keys[b]
            if shared:
                n_a = sum(1 for x in roles[a] if keyfn(x) in shared)
                n_b = sum(1 for x in roles[b] if keyfn(x) in shared)
                pct_a = 100.0 * n_a / len(roles[a])
                errors.append(
                    f"LEAK at level '{lv}': '{a}' and '{b}' share {len(shared)} key(s), "
                    f"affecting {n_a}/{len(roles[a])} ({pct_a:.1f}%) of '{a}' and {n_b} of '{b}'")
            else:
                print(f"    [PASS] {lv:14s} {a} vs {b}: no shared key")

    # Never silently deduplicate. Report and move on.
    for r, recs in sorted(roles.items()):
        h = collections.Counter(x["sha256"] for x in recs)
        d = sum(v - 1 for v in h.values() if v > 1)
        if d:
            print(f"    [INFO] role '{r}' contains {d} redundant copy/copies (reported, never removed)")

    # Unresolved ancestry is 'unproven', not 'clean'.
    if "content" in levels_to_check and diag["crops_with_unacquired_parent"]:
        print(f"    [INFO] {diag['crops_with_unacquired_parent']} item(s) have an unacquired parent "
              f"photograph ({', '.join(diag['orphan_parent_ids'])}); their content ancestry is "
              f"UNPROVEN, not independent")

    for e in errors:
        print(f"    [FAIL] {e}")
    if not errors:
        print(f"    [PASS] allocation is clean at level '{level}' and every weaker level")
    return len(errors)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not args:
        fatal("no allocation file given")
    index, diag = load_manifest()
    print(f"[OK] manifest loaded: {len(index):,} items; "
          f"{diag['crops_resolved_to_parent']:,} crops resolved to a parent photograph, "
          f"{diag['crops_with_unacquired_parent']} unresolved")
    total = sum(check_one(p, index, diag) for p in args)
    print()
    if total:
        print(f"RESULT: {total} leak(s) found. Fail closed — this is a DATA INTEGRITY stop.")
        sys.exit(1)
    print("RESULT: no leaks found at the required levels.")
    print("NOTE: absence of a detected collision is not proof of independence.")
    sys.exit(0)


if __name__ == "__main__":
    main()
