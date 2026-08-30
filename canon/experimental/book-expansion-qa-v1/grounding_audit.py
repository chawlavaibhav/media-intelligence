#!/usr/bin/env python3
"""
INDEPENDENT grounding audit — the parent session's own quality check, not a lane self-report.

For every Q&A item whose `support` field contains a quoted string, verify that the quotation
actually occurs at the cited locator in the real source text. This is stronger than checking that
a page number is in range: it checks that the cited page says what the item claims it says.

Handles both page-marked sources (<<<PRINTED_PAGE n>>>) and section-marked ones
(<<<SPINE n | FILE .. | TITLE ..>>>), and falls back to whole-source search so a quotation that
is real but mis-located is distinguished from one that is not in the book at all.

Usage: python3 grounding_audit.py <qa-bank.yaml> <source.txt> [--sample N]
"""
import random
import re
import sys
import unicodedata

import yaml


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-").replace("‒", "-")
    # Join words broken across a line by a hyphen, then flatten all whitespace. Without this,
    # a quotation that is verbatim in the book fails to match because the scan wrapped a word.
    s = re.sub(r"-\s*\n\s*", "", s)
    s = re.sub(r"\s+", " ", s)
    # Punctuation and hyphenation vary between a quoting extractor and an OCR'd page; compare
    # on letters, digits and spaces only.
    s = re.sub(r"[^a-z0-9 ]+", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()


def load_source(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    if "<<<PRINTED_PAGE" in raw:
        parts = re.split(r"<<<PRINTED_PAGE (\d+) \| PDF_PAGE \d+>>>", raw)
        return {("p", int(parts[i])): parts[i + 1] for i in range(1, len(parts) - 1, 2)}, raw
    if "<<<PDF_PAGE" in raw:
        parts = re.split(r"<<<PDF_PAGE (\d+)>>>", raw)
        return {("p", int(parts[i])): parts[i + 1] for i in range(1, len(parts) - 1, 2)}, raw
    if "<<<SPINE" in raw:
        parts = re.split(r"<<<SPINE (\d+) \| FILE [^|]*\| TITLE ([^>]*)>>>", raw)
        d = {}
        for i in range(1, len(parts) - 2, 3):
            d[("s", int(parts[i]))] = parts[i + 2]
        return d, raw
    return {}, raw


def quotes_in(text):
    """Pull quoted fragments out of a support field."""
    out = []
    for m in re.finditer(r"[\"“]([^\"”]{25,300})[\"”]", text or ""):
        out.append(m.group(1))
    return out


def main():
    qa_path, src_path = sys.argv[1], sys.argv[2]
    sample = None
    for a in sys.argv[3:]:
        if a.startswith("--sample"):
            sample = int(a.split("=")[1]) if "=" in a else int(sys.argv[sys.argv.index(a) + 1])

    bank = yaml.safe_load(open(qa_path, encoding="utf-8"))
    items = bank.get("qa_items") if isinstance(bank, dict) else bank
    pages, whole = load_source(src_path)
    wnorm = norm(whole)

    checked = confirmed = mislocated = absent = 0
    noquote = 0
    problems = []

    pool = list(items)
    if sample and sample < len(pool):
        random.seed(11)
        pool = random.sample(pool, sample)

    for it in pool:
        qs = quotes_in(str(it.get("support", "")))
        if not qs:
            noquote += 1
            continue
        loc = str(it.get("source_locator", ""))
        cited = [int(n) for m in re.finditer(r"\bpp?\.\s*([\d\s,\-–and]+)", loc)
                 for n in re.findall(r"\d{1,3}", m.group(1))]
        for q in qs:
            checked += 1
            # A quotation may elide with "..." / "…". Each fragment must appear, but they need
            # not be contiguous -- that is what the ellipsis means. Checking the whole string as
            # one substring produced a wave of false failures on the first run.
            frags = [f for f in re.split(r"\.\.\.|…", q) if len(norm(f)) >= 20]
            if not frags:
                frags = [q]
            fn = [norm(f) for f in frags]
            joined = norm(" ".join(pages.get(("p", p), "") for p in
                                   range(min(cited) - 1, max(cited) + 2))) if cited else ""
            if joined and all(f in joined for f in fn):
                confirmed += 1
            elif all(f in wnorm for f in fn):
                mislocated += 1
                problems.append(("MISLOCATED", it["qa_id"], loc, q[:90]))
            else:
                missing = [f for f in fn if f not in wnorm]
                absent += 1
                problems.append(("NOT-IN-SOURCE", it["qa_id"], loc,
                                 (missing[0] if missing else q)[:90]))

    print(f"items considered      : {len(pool)}")
    print(f"  with no quotation   : {noquote}  (paraphrase-only support; not checkable this way)")
    print(f"quotations checked    : {checked}")
    print(f"  confirmed at locator: {confirmed}")
    print(f"  real but MISLOCATED : {mislocated}")
    print(f"  NOT FOUND in source : {absent}")
    if problems:
        print("\nproblems:")
        for kind, qid, loc, q in problems[:40]:
            print(f"  [{kind}] {qid} @ {loc}\n      {q!r}")
    return 1 if (mislocated or absent) else 0


if __name__ == "__main__":
    sys.exit(main())
