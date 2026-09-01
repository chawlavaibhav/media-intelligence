#!/usr/bin/env python3
"""EVAL-038 judging pipeline — strip, leak-check, blind, commit (USD 0).

Design source: canon/findings/PROPOSED-EVAL-038-SUBSTITUTION-DESIGN.md §4 and §5.5;
blinding pattern: canon/experiments/v1/value-gate/prepare_real_run.py (OS-entropy key
held OFF-repo; salted SHA-256 commitment committed before judging; key revealed after
all verdicts are in).

Stripping is uniform across every package (baseline and treatment alike), so the act
of stripping reveals nothing: the sections FAILURE_PREVENTION, DOCTRINE_DEVIATIONS and
KNOWLEDGE_AND_WEBSITE_USE are removed whole — they are where treatment self-discloses
(GAP-06). A mechanical leak scan then proves no treatment marker survives.

Usage:
  strip_blind.py strip <in.txt> <out.txt>          # strip one package
  strip_blind.py dryrun <pkg1> <pkg2>              # §5.5: strip two committed packages,
                                                   # leak-scan, report; writes nothing
  strip_blind.py blind <manifest_out_dir> <label=path>...
        # strip every input, generate an OS-entropy key OFF-repo (path printed),
        # write blinded copies P1..Pn in shuffled order + a salted SHA-256 commitment
"""
import hashlib
import json
import os
import pathlib
import re
import sys

SECTIONS_TO_STRIP = {"FAILURE_PREVENTION", "DOCTRINE_DEVIATIONS", "KNOWLEDGE_AND_WEBSITE_USE"}
SECTION_RE = re.compile(r"^(?:#{1,4}\s+)?(?:\*\*)?([A-Z][A-Z_]{3,})(?:\*\*)?:?$")

# Treatment markers that must not survive stripping. Word-boundary guards keep
# 'package'/'packshot' from tripping the 'pack' scan.
LEAK_PATTERNS = [
    (re.compile(r"\bcanon\b", re.I), "the word 'Canon'"),
    (re.compile(r"KNOWLEDGE_AND_WEBSITE_USE"), "the KNOWLEDGE_AND_WEBSITE_USE header"),
    (re.compile(r"DOCTRINE_DEVIATIONS"), "the DOCTRINE_DEVIATIONS header"),
    (re.compile(r"\b(?:PA|CA)-D\d+\b"), "a pack check id"),
    (re.compile(r"\bdoctrine\b", re.I), "the word 'doctrine'"),
    (re.compile(r"\b(?:composition_and_attention|product_appearance|typography_and_copy|"
                r"indian_indic_context|commercial_communication|concept_and_distinctiveness|"
                r"critique_and_effectiveness|colour_and_visual_register|"
                r"camera_and_spatial_grammar|editing_pacing_and_short_form)\b"), "a pack id"),
    (re.compile(r"\bsk_[a-z]+_"), "a source-knowledge item id"),
    (re.compile(r"not_governed_by_injected_doctrine"), "the v2 not-governed literal"),
]

def strip_text(text):
    out, skipping = [], False
    for line in text.splitlines():
        m = SECTION_RE.match(line.strip())
        if m:
            skipping = m.group(1) in SECTIONS_TO_STRIP
            if skipping:
                continue
        if not skipping:
            out.append(line)
    res = "\n".join(out)
    return re.sub(r"\n{3,}", "\n\n", res).rstrip("\n") + "\n"

def leaks(text):
    found = []
    for pat, what in LEAK_PATTERNS:
        m = pat.search(text)
        if m:
            found.append(f"{what} ({m.group(0)!r})")
    return found

def cmd_strip(src, dst):
    stripped = strip_text(pathlib.Path(src).read_text())
    bad = leaks(stripped)
    if bad:
        sys.exit(f"LEAK in {src}: " + "; ".join(bad))
    pathlib.Path(dst).write_text(stripped)
    print(f"stripped {src} -> {dst} (clean)")

def cmd_dryrun(paths):
    ok = True
    for p in paths:
        stripped = strip_text(pathlib.Path(p).read_text())
        bad = leaks(stripped)
        status = "CLEAN" if not bad else "LEAK: " + "; ".join(bad)
        if bad:
            ok = False
        print(f"{p}: {len(stripped)} bytes stripped, {status}")
    print("PASS: strip pipeline leaks no treatment marker" if ok else "FAIL")
    sys.exit(0 if ok else 1)

def cmd_blind(outdir, pairs):
    outdir = pathlib.Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    entries = []
    for pair in pairs:
        label, path = pair.split("=", 1)
        stripped = strip_text(pathlib.Path(path).read_text())
        bad = leaks(stripped)
        if bad:
            sys.exit(f"LEAK in {path}: " + "; ".join(bad))
        entries.append((label, path, stripped))
    key = os.urandom(16).hex()
    salt = os.urandom(16).hex()
    # deterministic shuffle under the secret key: sort by HMAC-ish digest
    order = sorted(range(len(entries)),
                   key=lambda i: hashlib.sha256(f"{key}|{entries[i][0]}".encode()).hexdigest())
    mapping = {}
    for rank, i in enumerate(order, 1):
        label, path, stripped = entries[i]
        bid = f"P{rank:02d}"
        (outdir / f"{bid}.txt").write_text(stripped)
        mapping[bid] = {"label": label, "source_path": path,
                        "stripped_sha256": hashlib.sha256(stripped.encode()).hexdigest()}
    commitment = hashlib.sha256(f"{salt}|{key}".encode()).hexdigest()
    (outdir / "BLINDING-COMMITMENT.json").write_text(json.dumps({
        "commitment_sha256_of_salt_pipe_key": commitment,
        "packages": sorted(mapping),
        "reveal_rule": "salt|key published only after all verdicts are committed",
    }, indent=1, sort_keys=True))
    keyfile = pathlib.Path.home() / ".eval038-blinding-key.json"
    keyfile.write_text(json.dumps({"key": key, "salt": salt, "mapping": mapping},
                                  indent=1, sort_keys=True))
    print(f"blinded {len(entries)} packages into {outdir}")
    print(f"commitment committed; KEY HELD OFF-REPO at {keyfile} — do not commit it")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cmd = sys.argv[1]
    if cmd == "strip":
        cmd_strip(sys.argv[2], sys.argv[3])
    elif cmd == "dryrun":
        cmd_dryrun(sys.argv[2:])
    elif cmd == "blind":
        cmd_blind(sys.argv[2], sys.argv[3:])
    else:
        sys.exit(__doc__)
