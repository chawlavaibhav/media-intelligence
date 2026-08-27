#!/usr/bin/env python3
"""Deterministic builder for the EMP-001 Latin exact-text qualification pack.

WHAT THIS PACK IS FOR

    One job only: qualify a text judge against **correctly formed but wrong Latin text**, so that
    the A-TEXT screen is scored by an instrument whose false-pass behaviour is known. It is not
    evidence about any generator, and it may not be reported as one.

    It is a SEPARATE artifact from the frozen Devanagari battery. Nothing here reads, writes or
    depends on `eval/battery/devanagari-exactness/`, and `build()` refuses outright to write
    anywhere inside it — a mistyped `--out` must fail, not quietly overwrite a frozen baseline.

WHY THE CORRUPTIONS ARE HAND-AUTHORED AND THEN MACHINE-CHECKED

    Truth is known by construction: each of the 48 base strings is paired with exactly one
    corruption that a person wrote down deliberately, together with the class it belongs to and a
    human-readable note. The builder then re-derives the class from the two strings alone
    (`classify_edit`) and refuses to build if the derived class disagrees with the declared one.

    So the pack is auditable in prose AND mechanically verified. A hand-authored corruption that
    silently became a two-character edit, or drifted into another class, stops the build.

THE SHAPE

    48 base strings x 2 strata = 96 items.

      * match     — the drawn string IS the target. rendered_string == target_string.
      * mismatch  — a corrupted string is drawn and the judge is asked about the ORIGINAL. That
                    is the trap: every language prior the model has says "yes, that's it".

    Every base string appears in BOTH strata, so base identity carries no signal, and the pack is
    50/50, so "always match" and "always mismatch" both score exactly 50%.

    Exactly one mismatch opportunity per base string, and exactly 8 mismatches per failure class.

DETERMINISM

    No clock, no RNG, no environment. The manifest is a pure function of the table below, sorted
    by item_id, serialised as UTF-8 JSON with a fixed key order, and fingerprinted with SHA-256
    over the final bytes. Rebuilding on any machine must reproduce the committed bytes exactly —
    which is what `test_rebuilding_reproduces_the_committed_bytes_exactly` checks.

    The manifest is deliberately machine-independent: it carries STRINGS, not pixels. Rasterising
    the strings for an actual judge run is a separate, font-pinned step (`render_latin_pack.py`)
    whose output is a build product, exactly as the Devanagari battery treats its own images.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import string
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKAGE_ROOT = HERE.parent
REPO_ROOT = PACKAGE_ROOT.parent.parent

DEFAULT_OUT = HERE / "latin-pack-v1.jsonl"
FROZEN_DEVANAGARI_BATTERY = REPO_ROOT / "eval" / "battery" / "devanagari-exactness"

PACK_VERSION = "latin-pack-v1"
SCRIPT = "latin"

FAILURE_CLASSES = (
    "confusable_substitution",
    "omission",
    "insertion",
    "transposition",
    "case_diacritic",
    "punctuation_digit_space",
)

# Pairs that are confusable *by shape*, not by case. A pair whose members differ only in case
# belongs to `case_diacritic`, so nothing here may fold to the same letter.
CONFUSABLE_PAIRS = frozenset({
    frozenset({"0", "O"}), frozenset({"1", "l"}), frozenset({"5", "S"}),
    frozenset({"8", "B"}), frozenset({"2", "Z"}), frozenset({"6", "G"}),
    frozenset({"I", "l"}),
})

PUNCT_DIGIT_SPACE = frozenset(string.digits) | frozenset(string.punctuation) | frozenset(" ")


class ForbiddenOutputPath(RuntimeError):
    """The requested output path is inside a protected frozen artifact."""


class PackConstructionError(RuntimeError):
    """A hand-authored corruption does not match the class it declares."""


# ---------------------------------------------------------------------------------------------
# The table. base string, declared failure class, the corrupted string that gets drawn, and a
# note a human can audit without running anything.
#
# Ordered so that index i uses FAILURE_CLASSES[i % 6]; eight full cycles give exactly 8 per class.
# ---------------------------------------------------------------------------------------------
BASES: tuple[tuple[str, str, str, str], ...] = (
    ("Flat 50% Off", "confusable_substitution", "Flat 5O% Off", "digit 0 -> capital O"),
    ("Handcrafted Soap", "omission", "Handcrated Soap", "dropped the f in 'crafted'"),
    ("Fresh Roasted", "insertion", "Fressh Roasted", "doubled the s in 'Fresh'"),
    ("Festive Offer", "transposition", "Fesitve Offer", "swapped ti -> it in 'Festive'"),
    ("Café Mocha", "case_diacritic", "Cafe Mocha", "dropped the acute accent on e"),
    ("Rs. 1,299 only", "punctuation_digit_space", "Rs. 1,199 only", "price digit 2 -> 1"),

    ("MEGA SALE", "confusable_substitution", "MEGA 5ALE", "capital S -> digit 5"),
    ("Free Shipping", "omission", "Free Shiping", "dropped one p in 'Shipping'"),
    ("Daily Essentials", "insertion", "Dailly Essentials", "doubled the l in 'Daily'"),
    ("Chocolate Truffle", "transposition", "Chocolate Turffle", "swapped ru -> ur in 'Truffle'"),
    ("Crème Caramel", "case_diacritic", "Creme Caramel", "dropped the grave accent on e"),
    ("Save 20% Today", "punctuation_digit_space", "Save 30% Today", "claim digit 2 -> 3"),

    ("Buy 1 Get 1", "confusable_substitution", "Buy l Get 1", "digit 1 -> lowercase l"),
    ("Limited Edition", "omission", "Limited Editon", "dropped the i in 'Edition'"),
    ("Hand Wash Only", "insertion", "Hand Wassh Only", "doubled the s in 'Wash'"),
    ("Almond Butter", "transposition", "Almond Buttre", "swapped er -> re at the end"),
    ("Décor Studio", "case_diacritic", "Decor Studio", "dropped the acute accent on e"),
    ("Pack of 12", "punctuation_digit_space", "Pack of 13", "count digit 2 -> 3"),

    ("Order ID B2049", "confusable_substitution", "Order ID 82049", "capital B -> digit 8"),
    ("Winter Collection", "omission", "Winter Collecton", "dropped the i in 'Collection'"),
    ("Natural Honey", "insertion", "Naturral Honey", "doubled the r in 'Natural'"),
    ("Kitchen Essentials", "transposition", "Kitchen Essentiasl", "swapped ls -> sl at the end"),
    ("Piña Colada", "case_diacritic", "Pina Colada", "dropped the tilde on n"),
    ("Call 1800-123-456", "punctuation_digit_space", "Call 1800.123-456", "hyphen -> full stop"),

    ("ZONE 2 DELIVERY", "confusable_substitution", "ZONE Z DELIVERY", "digit 2 -> capital Z"),
    ("Assorted Spices", "omission", "Assorted Spies", "dropped the c in 'Spices'"),
    ("Best Seller", "insertion", "Bestt Seller", "doubled the t in 'Best'"),
    ("Morning Blend", "transposition", "Mornign Blend", "swapped ng -> gn in 'Morning'"),
    ("New Delhi", "case_diacritic", "New delhi", "capital D -> lowercase d"),
    ("Buy 2, Get 1 Free", "punctuation_digit_space", "Buy 2. Get 1 Free", "comma -> full stop"),

    ("Grade G6 Steel", "confusable_substitution", "Grade 66 Steel", "capital G -> digit 6"),
    ("Stainless Steel", "omission", "Stainles Steel", "dropped one s in 'Stainless'"),
    ("Gift Hamper", "insertion", "Giftt Hamper", "doubled the t in 'Gift'"),
    ("Silver Jewellery", "transposition", "Silver Jewellrey", "swapped er -> re in 'Jewellery'"),
    ("Made in India", "case_diacritic", "Made In India", "lowercase i -> capital I"),
    ("Size: XL", "punctuation_digit_space", "Size; XL", "colon -> semicolon"),

    ("Type II Filter", "confusable_substitution", "Type Il Filter", "capital I -> lowercase l"),
    ("Organic Turmeric", "omission", "Organic Turmeic", "dropped the r in 'Turmeric'"),
    ("Slim Fit Shirt", "insertion", "Sliim Fit Shirt", "doubled the i in 'Slim'"),
    ("Copper Bottle", "transposition", "Copper Bottel", "swapped le -> el at the end"),
    ("SUMMER SALE", "case_diacritic", "SUMMEr SALE", "capital R -> lowercase r"),
    ("Net Wt 500 g", "punctuation_digit_space", "Net Wt 500g", "removed the space before g"),

    ("OPEN 24x7", "confusable_substitution", "0PEN 24x7", "capital O -> digit 0"),
    ("Express Delivery", "omission", "Expres Delivery", "dropped one s in 'Express'"),
    ("Refill Pack", "insertion", "Refilll Pack", "tripled the l in 'Refill'"),
    ("Ceramic Planter", "transposition", "Ceramic Plantre", "swapped er -> re at the end"),
    ("Extra Soft", "case_diacritic", "Extra soft", "capital S -> lowercase s"),
    ("MRP 499/-", "punctuation_digit_space", "MRP 499 /-", "inserted a space before /-"),
)


def nfc(s: str) -> str:
    """NFC and nothing else. No stripping, no case folding."""
    return unicodedata.normalize("NFC", s)


def _fold(ch: str) -> str:
    """Strip combining marks and case, so 'e' and 'é' and 'E' all fold together."""
    decomposed = unicodedata.normalize("NFD", ch)
    stripped = "".join(c for c in decomposed if not unicodedata.combining(c))
    return stripped.casefold()


def _single_deletion(base: str, other: str) -> int | None:
    """Index deleted from `base` to give `other`, or None if it is not a single deletion."""
    if len(other) != len(base) - 1:
        return None
    for i in range(len(base)):
        if base[:i] + base[i + 1:] == other:
            return i
    return None


def classify_edit(base: str, rendered: str) -> str:
    """Re-derive the failure class from the two strings alone.

    Order matters. Transposition is two differing positions, so it is checked before the
    single-substitution rules. A confusable PAIR is checked before the case/diacritic rule and
    before the punctuation/digit rule, because '0' vs 'O' is a shape confusion that happens to
    involve a digit, and 'I' vs 'l' is a shape confusion that is not a case change.

    Raises PackConstructionError for anything that is not exactly one controlled edit.
    """
    base, rendered = nfc(base), nfc(rendered)
    if base == rendered:
        raise PackConstructionError("rendered string is identical to the base after NFC")

    if len(base) == len(rendered):
        diff = [i for i, (a, b) in enumerate(zip(base, rendered)) if a != b]

        if len(diff) == 2 and diff[1] == diff[0] + 1:
            i, j = diff
            if base[i] == rendered[j] and base[j] == rendered[i]:
                return "transposition"
            raise PackConstructionError(
                f"two adjacent characters differ but are not a swap: {base!r} -> {rendered!r}")

        if len(diff) == 1:
            i = diff[0]
            a, b = base[i], rendered[i]
            if frozenset({a, b}) in CONFUSABLE_PAIRS:
                return "confusable_substitution"
            if _fold(a) == _fold(b):
                return "case_diacritic"
            if a in PUNCT_DIGIT_SPACE or b in PUNCT_DIGIT_SPACE:
                return "punctuation_digit_space"
            raise PackConstructionError(
                f"single substitution {a!r} -> {b!r} belongs to no controlled class")

        raise PackConstructionError(
            f"{len(diff)} characters differ; a controlled item changes exactly one thing")

    deleted = _single_deletion(base, rendered)
    if deleted is not None:
        ch = base[deleted]
        return "punctuation_digit_space" if ch in PUNCT_DIGIT_SPACE else "omission"

    inserted = _single_deletion(rendered, base)
    if inserted is not None:
        ch = rendered[inserted]
        return "punctuation_digit_space" if ch in PUNCT_DIGIT_SPACE else "insertion"

    raise PackConstructionError(
        f"length differs by more than one controlled edit: {base!r} -> {rendered!r}")


def _record(item_id: str, base_id: str, base: str, target: str, rendered: str,
            expected: str, failure_class: str | None, edit_detail: str | None) -> dict:
    """Fixed key order. The order IS part of the frozen serialization."""
    return {
        "item_id": item_id,
        "base_id": base_id,
        "pack_version": PACK_VERSION,
        "script": SCRIPT,
        "base_string": base,
        "target_string": target,
        "rendered_string": rendered,
        "expected": expected,
        "failure_class": failure_class,
        "edit_detail": edit_detail,
        "truth_origin": "constructed_by_code_no_human_label",
    }


def build_records() -> list[dict]:
    """Build the 96 records in memory, validating every hand-authored corruption."""
    if len(BASES) != 48:
        raise PackConstructionError(f"expected 48 base strings, found {len(BASES)}")

    seen: set[str] = set()
    records: list[dict] = []

    for i, (raw_base, declared_class, raw_rendered, note) in enumerate(BASES):
        base, rendered = nfc(raw_base), nfc(raw_rendered)

        if base in seen:
            raise PackConstructionError(f"duplicate base string {base!r}")
        seen.add(base)

        if declared_class != FAILURE_CLASSES[i % len(FAILURE_CLASSES)]:
            raise PackConstructionError(
                f"base {i} declares {declared_class!r} but its slot is "
                f"{FAILURE_CLASSES[i % len(FAILURE_CLASSES)]!r}")

        derived = classify_edit(base, rendered)
        if derived != declared_class:
            raise PackConstructionError(
                f"base {i} {base!r}: declared {declared_class!r}, machine-derived {derived!r}")

        if any("ऀ" <= ch <= "ॿ" for ch in base + rendered):
            raise PackConstructionError(
                f"base {i}: Devanagari found in the Latin pack. The two batteries stay separate.")

        base_id = f"lb-{i:02d}"
        records.append(_record(f"lx-{2 * i:04d}", base_id, base, base, base,
                               "match", None, None))
        records.append(_record(f"lx-{2 * i + 1:04d}", base_id, base, base, rendered,
                               "mismatch", declared_class, note))

    records.sort(key=lambda r: r["item_id"])
    return records


def serialize(records: list[dict]) -> bytes:
    """UTF-8 JSONL, one record per line, fixed key order, trailing newline. Nothing else."""
    return "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records).encode("utf-8")


def _reject_protected_path(out_path: Path) -> None:
    out_path = out_path.resolve()
    battery = FROZEN_DEVANAGARI_BATTERY.resolve()
    if out_path == battery or battery in out_path.parents:
        raise ForbiddenOutputPath(
            f"refusing to write {out_path} — it resolves inside the frozen Devanagari battery at "
            f"{battery}. That battery is a protected baseline: EMP-001 reads its contract and "
            f"never writes to it. Choose an output path outside it.")


def build(out_path: Path | str = DEFAULT_OUT, write_fingerprint: bool = True) -> dict:
    """Build, validate and write the pack. Returns a summary. Makes no network call."""
    out_path = Path(out_path)
    _reject_protected_path(out_path)

    records = build_records()
    payload = serialize(records)
    digest = hashlib.sha256(payload).hexdigest()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(payload)

    if write_fingerprint:
        fingerprint_path = out_path.with_suffix(".sha256")
        _reject_protected_path(fingerprint_path)
        fingerprint_path.write_text(f"{digest}  {out_path.name}\n", encoding="utf-8")

    return {
        "pack_version": PACK_VERSION,
        "path": str(out_path),
        "items": len(records),
        "match": sum(r["expected"] == "match" for r in records),
        "mismatch": sum(r["expected"] == "mismatch" for r in records),
        "base_strings": len({r["base_id"] for r in records}),
        "failure_classes": {
            c: sum(r["failure_class"] == c for r in records) for c in FAILURE_CLASSES},
        "sha256": digest,
        "external_calls": 0,
        "spend_usd": "0",
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Build the frozen EMP-001 Latin qualification pack.")
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    args = ap.parse_args(argv)
    summary = build(out_path=Path(args.out))
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
