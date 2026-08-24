#!/usr/bin/env python3
"""
Materialise the human-validated EVAL-005 battery view: the 96 approved items, and nothing else.

WHAT THIS IS
    A deterministic **filter**, not a builder. One human-validation pass rejected 5 of the 53 base
    words, which excludes the 10 items resting on them. This applies that frozen decision to the
    existing 106-item build and writes a checker-facing view containing only the survivors — in
    their original order, with their original content, byte for byte.

WHY A FILTER AND NOT A REBUILD
    The Controller decided PRUNE, DO NOT REBUILD. Two reasons matter:

      * The 106-item build is historical source material. It is what the reviewer actually saw, and
        it is what the packet fingerprint `e1cedf564603a94d` refers to. Regenerating the battery
        from the surviving 48 words would produce a *different* allocation — different perturbation
        choices, different direction assignment — that no human has looked at, while claiming the
        authority of a validation performed on something else.
      * Editing `build_items.py` to pretend the rejected words never existed would erase the
        evidence. The rejections are a finding about the EVAL-003 lexical pool, not an embarrassment
        to be tidied away.

    So nothing upstream changes. This script reads the build, drops ten ids, and writes the view.

FAIL CLOSED ON BATTERY IDENTITY
    The exclusion list is a set of ids that mean something only against ONE build. Applied to a
    different battery, `dx-0000` is a different item and the filter would silently remove the wrong
    thing. So the sha256 of `items.jsonl` is checked against the value recorded in the decision
    record, and a mismatch is fatal. It never rebuilds, never re-derives the exclusions, and never
    proceeds on a battery it was not adjudicated against.

Usage:
    python3 build_items.py --total 120                        # the historical 106-item build
    python3 apply_human_validation.py --from-build build      # writes build/validated/
    python3 apply_human_validation.py --from-build build --verify

No network, no model, no spend. Nothing here calls a checker or selects one.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_items import iid_reference_upper_bound  # noqa: E402
from checker_input import write_checker_inputs  # noqa: E402

HERE = Path(__file__).resolve().parent
RECORD = HERE / "human-validation" / "human-validation-v1.json"


class BatteryIdentityMismatch(RuntimeError):
    """The build on disk is not the one the human validation was performed against."""


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_record(path: Path = RECORD) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_items(build_dir: Path, record: dict) -> list[dict]:
    """Read the historical build, refusing to proceed unless it is the adjudicated one."""
    items_path = build_dir / "items.jsonl"
    if not items_path.exists():
        raise SystemExit(f"no battery at {items_path}; run: python3 build_items.py --total 120")
    expected = record["battery_identity"]["items_jsonl_sha256"]
    actual = sha256_file(items_path)
    if actual != expected:
        raise BatteryIdentityMismatch(
            f"battery identity mismatch — refusing to apply the human-validation decision.\n"
            f"  expected items.jsonl sha256: {expected}\n"
            f"  found                      : {actual}\n"
            f"The 10 excluded ids identify items in ONE specific build. Against a different build "
            f"they would remove different items. Rebuild the adjudicated battery, or open a new "
            f"human-validation pass against this one — do not filter blind.")
    return [json.loads(l) for l in items_path.read_text(encoding="utf-8").splitlines() if l.strip()]


def apply_exclusions(items: list[dict], record: dict) -> tuple[list[dict], list[dict]]:
    """Split into survivors and excluded, preserving the original order and content exactly."""
    excluded_ids = set(record["decisions"]["excluded_item_ids"])
    known = {i["item_id"] for i in items}
    missing = sorted(excluded_ids - known)
    if missing:
        raise BatteryIdentityMismatch(
            f"excluded ids not present in the battery: {missing}. Refusing to proceed.")
    survivors = [i for i in items if i["item_id"] not in excluded_ids]
    dropped = [i for i in items if i["item_id"] in excluded_ids]
    return survivors, dropped


def summarise(survivors: list[dict], record: dict, build_dir: Path) -> dict:
    mismatches = [i for i in survivors if i["expected_verdict"] == "mismatch"]
    hard = [i for i in mismatches if i["hard_opportunity"]]
    cls = collections.Counter(i["failure_class"] for i in mismatches)
    grp = collections.Counter(i["failure_group"] for i in mismatches)
    thin = sorted(c for c, n in cls.items() if n == 1)
    return {
        "view": "eval-005-human-validated-v1",
        "derived_from": {
            "items_jsonl_sha256": record["battery_identity"]["items_jsonl_sha256"],
            "packet_fingerprint": record["packet_fingerprint"],
            "note": "A filtered VIEW of the 106-item build. That build is unchanged and remains "
                    "the historical source material.",
        },
        "image_root_relative_to_this_directory": "..",
        "totals": {
            "items": len(survivors),
            "match": sum(1 for i in survivors if i["expected_verdict"] == "match"),
            "mismatch": len(mismatches),
        },
        "excluded": {
            "count": len(record["decisions"]["excluded_item_ids"]),
            "item_ids": record["decisions"]["excluded_item_ids"],
            "reason": "every item resting on a base word one Hindi-competent reviewer judged not a "
                      "real / well-formed Hindi word",
            "replaced": False,
        },
        "opportunity_model": {
            "hard_items": len(hard),
            "distinct_hard_base_words": len({i["base_word"] for i in hard}),
            "distinct_base_words": len({i["base_word"] for i in survivors}),
            "iid_reference_upper_bound_if_zero_false_passes_95pct":
                round(iid_reference_upper_bound(len(hard)), 4),
            "independence_status": "NOT ESTABLISHED — unchanged by human validation. Distinct base "
                                   "words remove obvious within-word correlation; they do not make "
                                   "the opportunities iid or exchangeable.",
            "epistemic_limit": "An iid Bernoulli REFERENCE calculation for sizing. Not a universal "
                               "checker error bound and not an estimate of real-world error.",
        },
        "coverage": {
            "failure_classes_represented": len(cls),
            "failure_groups_represented": len(grp),
            "by_class": dict(sorted(cls.items())),
            "by_group": dict(sorted(grp.items())),
            "thin_diagnostic_classes": {
                "classes": thin,
                "status": "THIN DIAGNOSTIC COVERAGE, NOT CLASS LOSS. Per-class figures were "
                          "already diagnostic signals and never rates.",
            },
        },
        "perceptibility_close_retained": record["decisions"]["perceptibility_close_retained"],
        "human_validation": {
            "reviewer_count": record["reviewer"]["count"],
            "epistemic_status": record["reviewer"]["epistemic_status"],
            "record": "human-validation/human-validation-v1.json",
        },
        "checker_qualification_started": False,
    }


def materialise(build_dir: Path, out_dir: Path, record: dict) -> dict:
    items = load_items(build_dir, record)
    survivors, _ = apply_exclusions(items, record)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "items.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in survivors), encoding="utf-8")
    # Checker-facing projections + the evaluator-side scoring key, through the same blind check
    # that guards the full battery. A leaking file cannot be written.
    write_checker_inputs(survivors, out_dir)
    summary = summarise(survivors, record, build_dir)
    (out_dir / "validated-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


# --------------------------------------------------------------------------------------------
# Verification
# --------------------------------------------------------------------------------------------
def verify(build_dir: Path, out_dir: Path, record: dict) -> int:
    fails = 0

    def check(name: str, ok: bool, detail: str = "") -> None:
        nonlocal fails
        print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail and not ok else ""))
        if not ok:
            fails += 1

    original = load_items(build_dir, record)
    check("original battery identity matches the adjudicated build",
          sha256_file(build_dir / "items.jsonl") == record["battery_identity"]["items_jsonl_sha256"])
    check("original battery history is intact — 106 items, 53 match, 53 mismatch, 37 hard",
          len(original) == 106
          and sum(1 for i in original if i["expected_verdict"] == "match") == 53
          and sum(1 for i in original if i["expected_verdict"] == "mismatch") == 53
          and sum(1 for i in original if i["hard_opportunity"]) == 37)

    survivors = [json.loads(l) for l in
                 (out_dir / "items.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    excluded_ids = record["decisions"]["excluded_item_ids"]

    # --- the frozen decision -----------------------------------------------------------------
    check("the exclusion set is exactly the ten frozen ids",
          sorted(excluded_ids) == sorted(["dx-0000", "dx-0003", "dx-0005", "dx-0020", "dx-0039",
                                          "dx-0053", "dx-0056", "dx-0058", "dx-0073", "dx-0092"]),
          str(sorted(excluded_ids)))
    surviving_ids = [i["item_id"] for i in survivors]
    check("no excluded id survives", not (set(excluded_ids) & set(surviving_ids)))
    check("exactly the excluded ids were removed, nothing else",
          set(i["item_id"] for i in original) - set(surviving_ids) == set(excluded_ids))

    # --- counts -------------------------------------------------------------------------------
    mismatches = [i for i in survivors if i["expected_verdict"] == "mismatch"]
    hard = [i for i in mismatches if i["hard_opportunity"]]
    check("96 surviving items", len(survivors) == 96, str(len(survivors)))
    check("48 match", sum(1 for i in survivors if i["expected_verdict"] == "match") == 48)
    check("48 mismatch", len(mismatches) == 48, str(len(mismatches)))
    check("50/50 balance preserved — 'always match' and 'always mismatch' still score 50%",
          sum(1 for i in survivors if i["expected_verdict"] == "match") == len(mismatches))
    check("33 hard opportunities", len(hard) == 33, str(len(hard)))
    check("on 33 distinct base words", len({i["base_word"] for i in hard}) == 33,
          str(len({i["base_word"] for i in hard})))
    check("48 distinct surviving base words", len({i["base_word"] for i in survivors}) == 48)

    # --- coverage -----------------------------------------------------------------------------
    all_classes = {i["failure_class"] for i in original if i["expected_verdict"] == "mismatch"}
    all_groups = {i["failure_group"] for i in original if i["expected_verdict"] == "mismatch"}
    cls = collections.Counter(i["failure_class"] for i in mismatches)
    grp = collections.Counter(i["failure_group"] for i in mismatches)
    check("20 of 20 failure classes remain represented",
          len(all_classes) == 20 and all(cls[c] for c in all_classes),
          str(sorted(c for c in all_classes if not cls[c])))
    check("5 of 5 failure groups remain represented",
          len(all_groups) == 5 and all(grp[g] for g in all_groups))
    thin = sorted(c for c in all_classes if cls[c] == 1)
    check("thin diagnostic classes are exactly the three recorded (not class loss)",
          thin == ["NASAL_SUBSTITUTE", "NUKTA_REMOVE", "REPH_TO_FULL_RA"], str(thin))

    # --- the human answers actually govern -----------------------------------------------------
    rejected_words = {r["word"] for r in record["decisions"]["rejected_base_words"]}
    check("five base words were rejected", len(rejected_words) == 5, str(sorted(rejected_words)))
    check("no surviving item uses any rejected base word",
          not any(i["base_word"] in rejected_words for i in survivors),
          str(sorted({i["base_word"] for i in survivors} & rejected_words)))
    import csv as _csv
    with open(HERE / "human-validation/responses/word-validation-sheet.completed.csv",
              encoding="utf-8", newline="") as f:
        answers = {r["word"]: r["is_real_wellformed_hindi_word"] for r in _csv.DictReader(f)}
    check("every one of the 48 surviving base words has a human YES",
          all(answers.get(b) == "yes" for b in {i["base_word"] for i in survivors}),
          str(sorted(b for b in {i["base_word"] for i in survivors} if answers.get(b) != "yes")))
    check("53 of 53 word responses, none unanswered, none UNSURE",
          len(answers) == 53 and all(v in ("yes", "no") for v in answers.values()))
    check("'राज -' is preserved as supplied (accepted, not reclassified)",
          answers.get("राज -") == "yes" and "राज -" in {i["base_word"] for i in survivors})

    # --- perceptibility CLOSE is retained, not treated as failure -------------------------------
    close_ids = record["decisions"]["perceptibility_close_retained"]["item_ids"]
    check("four CLOSE perceptibility items were recorded", len(close_ids) == 4, str(close_ids))
    check("every CLOSE item survives — CLOSE is not a failure",
          all(c in surviving_ids for c in close_ids),
          str([c for c in close_ids if c not in surviving_ids]))

    # --- no content mutation --------------------------------------------------------------------
    by_id = {i["item_id"]: i for i in original}
    check("no surviving item's content was mutated — byte-equal to the original build",
          all(s == by_id[s["item_id"]] for s in survivors))
    check("survivors are in the original order",
          surviving_ids == [i["item_id"] for i in original if i["item_id"] not in set(excluded_ids)])

    # --- what a checker would actually receive ---------------------------------------------------
    for name, expect_target in (("checker-input-transcribe.jsonl", False),
                                ("checker-input-verdict.jsonl", True)):
        rows = [json.loads(l) for l in (out_dir / name).read_text(encoding="utf-8").splitlines() if l.strip()]
        check(f"{name}: exactly the 96 surviving items, in order",
              [r["item_id"] for r in rows] == surviving_ids, f"{len(rows)} rows")
        has_target = any("target_string" in r for r in rows)
        check(f"{name}: target {'present' if expect_target else 'absent'}", has_target == expect_target)
    key = [json.loads(l) for l in (out_dir / "scoring-key.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    check("scoring-key.jsonl covers exactly the 96 surviving items",
          [r["item_id"] for r in key] == surviving_ids)

    # --- provenance ------------------------------------------------------------------------------
    for art in record["response_artifacts"]:
        p = HERE / "human-validation" / art["file"]
        check(f"provenance artifact unchanged: {art['file']}",
              p.exists() and sha256_file(p) == art["sha256"])
    check("record states one reviewer and that judgements are provenance, not ground truth",
          record["reviewer"]["count"] == 1
          and "NOT GROUND TRUTH" in record["reviewer"]["epistemic_status"].upper())
    check("record states 98 of 98 answered, 0 unanswered, 0 unsure",
          record["completeness"]["overall_answered"] == 98
          and record["completeness"]["unanswered"] == 0
          and record["completeness"]["unsure"] == 0)
    check("record carries the packet fingerprint e1cedf564603a94d",
          record["packet_fingerprint"] == "e1cedf564603a94d")
    check("all five rejected ids and their reasons are preserved as supplied",
          len(record["decisions"]["rejected_base_words"]) == 5
          and all("word_id" in r and "reason_as_supplied" in r
                  for r in record["decisions"]["rejected_base_words"]))
    check("record states checker qualification has NOT started",
          record["scope"]["checker_qualification_started"] is False
          and record["scope"]["checker_model_api_calls"] == 0)

    # --- fail closed --------------------------------------------------------------------------
    import tempfile
    with tempfile.TemporaryDirectory() as t:
        bad = Path(t) / "build"
        bad.mkdir()
        (bad / "items.jsonl").write_text(
            (build_dir / "items.jsonl").read_text(encoding="utf-8") + "\n", encoding="utf-8")
        try:
            load_items(bad, record)
            check("a battery whose identity does not match is REFUSED", False, "it was accepted")
        except BatteryIdentityMismatch:
            check("a battery whose identity does not match is REFUSED", True)
    return fails


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--from-build", type=Path, default=HERE / "build")
    ap.add_argument("--out-dir", type=Path, default=None, help="default: <build>/validated")
    ap.add_argument("--record", type=Path, default=RECORD)
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args()

    out_dir = a.out_dir or (a.from_build / "validated")
    record = load_record(a.record)

    if a.verify:
        if not (out_dir / "items.jsonl").exists():
            sys.exit(f"no validated view at {out_dir}; run without --verify first")
        print(f"Verifying the human-validated view at {out_dir}\n")
        fails = verify(a.from_build, out_dir, record)
        print()
        if fails:
            print(f"FAILED: {fails} check(s)")
            return 1
        print("ALL CHECKS PASSED")
        return 0

    summary = materialise(a.from_build, out_dir, record)
    t, o, c = summary["totals"], summary["opportunity_model"], summary["coverage"]
    print(f"wrote {out_dir}")
    print(f"  items {t['items']}  match {t['match']}  mismatch {t['mismatch']}")
    print(f"  hard opportunities {o['hard_items']} on {o['distinct_hard_base_words']} distinct base words")
    print(f"  base words {o['distinct_base_words']} (all human-accepted)")
    print(f"  classes {c['failure_classes_represented']}/20   groups {c['failure_groups_represented']}/5")
    print(f"  thin diagnostic classes: {c['thin_diagnostic_classes']['classes']}")
    print(f"  iid reference figure: {o['iid_reference_upper_bound_if_zero_false_passes_95pct']:.4f}")
    print(f"  excluded {summary['excluded']['count']} items, none replaced")
    print("\nNo checker has been selected or called.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
