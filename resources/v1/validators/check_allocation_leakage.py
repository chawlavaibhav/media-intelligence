#!/usr/bin/env python3
"""Check an allocation for leakage between protected and non-protected roles, at three levels.

USAGE
  check_allocation_leakage.py <allocation.yaml> [more.yaml ...]

EXIT CODES
  0  checked, no collision found and every lineage was established
  1  checked, LEAK found                      -> a DATA INTEGRITY stop
  2  could not check (bad input, missing view, unknown item id)
  3  INDETERMINATE: independence could not be ESTABLISHED  -> NOT clean

Why 3 is separate from both 0 and 1 (R-C4). At `source_lineage` level an unregistered source yields
a `lin_unknown::` key. Comparing such keys and finding them different does NOT show independence:
two unregistered sources may be the same lab, the same collection effort, or one derived from the
other, and nothing in a source id says otherwise. Treating "different unknown keys" as "independent"
is exactly how an unregistered source gets silently certified as a clean holdout. So the tool
refuses to certify, and says so in its own outcome rather than burying it in a warning line.

Views are read from the BUILD directory (R-C3): they are deterministic derivations of the committed
manifest, rebuilt by build_views.py rather than committed. A missing build is exit 2, never a pass.
"""
import json, os, sys, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lineage_keys as lk

try:
    import yaml
except ImportError:
    print("[FAIL] PyYAML not available", file=sys.stderr); sys.exit(2)

V1 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(V1)
DEFAULT_MANIFEST = os.path.join(ROOT, "manifests", "corpus-pilot-v0.jsonl")
VIEWS_DIR = os.path.join(V1, "build", "views")

PROTECTED = {"qualification", "reserve"}
EXPOSED = {"development", "calibration"}
LEVEL_ORDER = ["byte", "content", "source_lineage"]

EXIT_CLEAN, EXIT_LEAK, EXIT_CANNOT_CHECK, EXIT_INDETERMINATE = 0, 1, 2, 3


def fatal(msg):
    print(f"[FAIL] {msg}", file=sys.stderr)
    sys.exit(EXIT_CANNOT_CHECK)


def load_manifest(path):
    if not os.path.isfile(path):
        fatal(f"manifest not found: {path}")
    recs = []
    with open(path) as fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                recs.append(json.loads(line))
            except json.JSONDecodeError as e:
                fatal(f"{path} line {n} unparseable: {e}")
    if not recs:
        fatal(f"{path} holds no records; refusing to check leakage against an empty manifest")
    if path == DEFAULT_MANIFEST and len(recs) < 1000:
        fatal(f"only {len(recs)} records in the main manifest; refusing to check against a truncated manifest")
    diag = lk.build_content_index(recs)
    return {r["item_id"]: r for r in recs}, diag


def load_view(view_id):
    path = os.path.join(VIEWS_DIR, view_id + ".jsonl")
    if not os.path.isfile(path):
        fatal(f"allocation references view '{view_id}' but {path} does not exist. "
              f"Views are deterministic build products: run build_views.py first.")
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


def check_one(path):
    if not os.path.isfile(path):
        fatal(f"allocation file not found: {path}")
    doc = yaml.safe_load(open(path))
    if not doc:
        fatal(f"allocation file parsed to nothing: {path}")
    for f in ("experiment_id", "allocation_version", "independence_level", "assignments"):
        if f not in doc:
            fatal(f"{path}: missing required field '{f}'")
    level = doc["independence_level"]
    if level not in LEVEL_ORDER:
        fatal(f"{path}: unknown independence_level {level!r}")

    man = doc.get("manifest")
    man = os.path.join(V1, man) if man and not os.path.isabs(man) else (man or DEFAULT_MANIFEST)
    index, diag = load_manifest(man)

    roles = resolve(doc["assignments"], index)
    print(f"\n=== {doc['experiment_id']} v{doc['allocation_version']} "
          f"({os.path.basename(path)}) · required independence: {level} ===")
    if man != DEFAULT_MANIFEST:
        print(f"    manifest: {os.path.relpath(man, ROOT)}")
    for r, recs in sorted(roles.items()):
        print(f"    {r:14s} {len(recs):>6,d} items")

    pairs = [(p, e) for p in sorted(PROTECTED & set(roles)) for e in sorted(EXPOSED & set(roles))]
    if "qualification" in roles and "reserve" in roles:
        pairs.append(("qualification", "reserve"))

    errors, indeterminate = [], []
    for lv in LEVEL_ORDER[:LEVEL_ORDER.index(level) + 1]:
        keyfn = lk.LEVELS[lv]
        keys = {r: {keyfn(x) for x in recs} for r, recs in roles.items()}
        for a, b in pairs:
            shared = keys[a] & keys[b]
            if shared:
                n_a = sum(1 for x in roles[a] if keyfn(x) in shared)
                n_b = sum(1 for x in roles[b] if keyfn(x) in shared)
                errors.append(
                    f"LEAK at level '{lv}': '{a}' and '{b}' share {len(shared)} key(s), "
                    f"affecting {n_a}/{len(roles[a])} ({100.0*n_a/len(roles[a]):.1f}%) of '{a}' "
                    f"and {n_b} of '{b}'")
                continue
            # R-C4: no shared key is not the same as independence ESTABLISHED.
            if lv == "source_lineage":
                unk_a = sorted({k for k in keys[a] if lk.is_unknown_lineage(k)})
                unk_b = sorted({k for k in keys[b] if lk.is_unknown_lineage(k)})
                if unk_a or unk_b:
                    src = sorted({k.split("::", 1)[1] for k in unk_a + unk_b})
                    indeterminate.append(
                        f"INDETERMINATE at level 'source_lineage': '{a}' vs '{b}' involves "
                        f"unregistered source(s) {src}. Their lineage is NOT ESTABLISHED, so "
                        f"independence cannot be certified. Different unknown keys are not evidence "
                        f"of different lineages. Register the source in lineage_keys.SOURCE_LINEAGE "
                        f"before using it in a protected role.")
                    continue
            print(f"    [PASS] {lv:14s} {a} vs {b}: no shared key"
                  + (" and every lineage established" if lv == "source_lineage" else ""))

    for r, recs in sorted(roles.items()):
        h = collections.Counter(x["sha256"] for x in recs)
        d = sum(v - 1 for v in h.values() if v > 1)
        if d:
            print(f"    [INFO] role '{r}' contains {d} redundant copy/copies (reported, never removed)")
    if diag["crops_with_unacquired_parent"]:
        print(f"    [INFO] {diag['crops_with_unacquired_parent']} item(s) have an unacquired parent "
              f"photograph ({', '.join(diag['orphan_parent_ids'])}); their content ancestry is "
              f"UNPROVEN, not independent")

    for e in errors:
        print(f"    [FAIL] {e}")
    for m in indeterminate:
        print(f"    [INDETERMINATE] {m}")
    if not errors and not indeterminate:
        print(f"    [PASS] allocation is clean at level '{level}' and every weaker level")
    return len(errors), len(indeterminate)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not args:
        fatal("no allocation file given")
    leaks = indet = 0
    for p in args:
        a, b = check_one(p)
        leaks += a
        indet += b
    print()
    if leaks:
        print(f"RESULT: {leaks} leak(s) found. Fail closed — this is a DATA INTEGRITY stop.")
        sys.exit(EXIT_LEAK)
    if indet:
        print(f"RESULT: {indet} comparison(s) INDETERMINATE — independence could not be established.")
        print("This is NOT a clean result. It is not a leak either; it is a refusal to certify.")
        sys.exit(EXIT_INDETERMINATE)
    print("RESULT: no leaks found at the required levels, and every lineage involved was established.")
    print("NOTE: absence of a detected collision is not proof of independence.")
    sys.exit(EXIT_CLEAN)


if __name__ == "__main__":
    main()
