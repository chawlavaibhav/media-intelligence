#!/usr/bin/env python3
"""EVAL-037 — substrate identity. Two digests, deliberately, to avoid self-reference.

The experiment-defining BYTES are the authority. No commit SHA is, and none can be:
the substrate was authored after the CANON-014 merge, so no commit contains both the
substrate and a fingerprint of itself. Requiring one would be an impossible
self-referential gate.

  common_substrate_digest
      Covers the substrate EXCLUDING lanes/. Every lane YAML embeds this value, which
      is non-circular precisely because lanes/ is outside its scope. It is what a lane
      verifies by itself, with no other file: the prompt, the briefs, the website
      snapshots, the conditions, the schemas, the tools and the validators it depends on.

  freeze_fingerprint
      Covers the WHOLE substrate, lanes included. It cannot live inside any file it
      covers, so it lives only in FREEZE-FINGERPRINT.yaml, which is excluded from its
      own scope. This is the value the controller approves and the PR records; a lane
      verifies it with `--check` rather than embedding it.

Both use the same algorithm as the Canon corpus index — sha256 over sorted
"path:sha256\\n" lines — so every fingerprint in this experiment is comparable.

  python3 tools/freeze_fingerprint.py            # write FREEZE-FINGERPRINT.yaml
  python3 tools/freeze_fingerprint.py --check    # verify both, exit 1 on drift
"""
import argparse
import hashlib
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
PKG = HERE.parent
OUT = PKG / "FREEZE-FINGERPRINT.yaml"
EXCLUDE_DIRS = {"runs", "__pycache__"}
EXCLUDE_FILES = {"FREEZE-FINGERPRINT.yaml"}


def files(exclude_lanes=False):
    out = []
    for p in sorted(PKG.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(PKG)
        if set(rel.parts) & EXCLUDE_DIRS or rel.name in EXCLUDE_FILES:
            continue
        if rel.name.startswith("."):
            continue
        if exclude_lanes and rel.parts[0] == "lanes":
            continue
        out.append(rel)
    return sorted(out, key=str)


def _digest(rels):
    rows = [(str(r), hashlib.sha256((PKG / r).read_bytes()).hexdigest()) for r in rels]
    canonical = "".join(f"{p}:{h}\n" for p, h in rows)
    return hashlib.sha256(canonical.encode()).hexdigest(), rows


def compute():
    """The full freeze fingerprint (lanes included)."""
    return _digest(files())


def compute_common():
    """The common-substrate digest (lanes excluded) — safe to embed in a lane."""
    return _digest(files(exclude_lanes=True))


def _recorded(key):
    if not OUT.exists():
        return None
    for line in OUT.read_text().splitlines():
        if line.startswith(f"{key}:"):
            return line.split(":", 1)[1].strip()
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    full, rows = compute()
    common, crows = compute_common()

    if a.check:
        bad = False
        for key, val in (("freeze_fingerprint", full), ("common_substrate_digest", common)):
            rec = _recorded(key)
            if rec != val:
                print(f"FREEZE DRIFT [{key}]\n  recorded: {rec}\n  computed: {val}",
                      file=sys.stderr)
                bad = True
        if bad:
            return 1
        print(f"freeze_fingerprint       intact: {full}")
        print(f"common_substrate_digest  intact: {common}")
        return 0

    lines = [
        "# EVAL-037 — substrate identity. The experiment-defining bytes are the authority.",
        "#",
        "# Regenerate:  python3 tools/freeze_fingerprint.py",
        "# Verify:      python3 tools/freeze_fingerprint.py --check",
        "#",
        "# freeze_fingerprint covers the WHOLE substrate including lanes/, so it cannot",
        "# live in any file it covers — it lives only here, and this file is excluded",
        "# from its own scope. This is the value the controller approves.",
        "#",
        "# common_substrate_digest excludes lanes/, which makes it safe for every lane",
        "# YAML to embed. That is the digest a lane verifies on its own.",
        "#",
        "# Both exclude runs/ (post-freeze lane evidence), __pycache__/ and dotfiles.",
        "",
        "experiment: EVAL-037",
        "scope: eval/experiments/EVAL-037/**",
        "algorithm: sha256-of-sorted-path-and-content",
        "",
        "# Canon provenance. This commit does NOT contain EVAL-037 and is not the",
        "# execution-lane starting commit.",
        "canon_base_commit: c6f8d910f7a3cdaaeafa2280313abfb9b898cddd",
        "canon_base_commit_role: the CANON-014 merge the corpus fingerprints were computed against",
        "",
        f"file_count: {len(rows)}",
        f"freeze_fingerprint: {full}",
        f"common_substrate_file_count: {len(crows)}",
        f"common_substrate_digest: {common}",
        "files:",
    ]
    for p, h in rows:
        lines += [f"  - path: {p}", f"    sha256: {h}"]
    OUT.write_text("\n".join(lines) + "\n")
    print(f"{len(rows)} files")
    print(f"freeze_fingerprint      : {full}")
    print(f"common_substrate_digest : {common} ({len(crows)} files, lanes excluded)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
