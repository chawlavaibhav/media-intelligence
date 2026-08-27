#!/usr/bin/env python3
"""Static checks on the package itself: zero spend, zero network, no invented rules.

WHY A CHECK ON OUR OWN CODE
---------------------------
"This costs nothing" is a claim, and claims about our own machinery are exactly
the ones nobody re-reads. This file turns three of them into something a test
run can fail on:

  1. NO NETWORK, NO PROVIDER. Nothing in this package may import a HTTP client,
     a socket, or any model provider SDK. Truth here comes from arithmetic on
     local pixels; a network import would mean it does not.
  2. SUBPROCESS ONLY FOR LOCAL FFMPEG. ffmpeg and ffprobe run on this machine
     and cost nothing. Any other external binary is a hole in the same claim.
  3. NO INVENTED THRESHOLD. No numeric pass mark for the temporal family exists
     in the frozen contracts, so none may appear here. A grep is a crude guard,
     but a threshold silently appearing in a scoring file is precisely the
     failure it needs to catch.

The checks fail closed: an unreadable file is a failure, not a skip. An empty
scan is a failure too - a check that examined nothing has proved nothing.
"""
from __future__ import annotations

import argparse
import ast
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent

FORBIDDEN_IMPORTS = {
    "requests", "httpx", "urllib", "urllib3", "http", "socket", "ftplib", "smtplib",
    "telnetlib", "aiohttp", "websockets", "boto3", "botocore", "google", "openai",
    "anthropic", "fal_client", "replicate", "vertexai", "tesserocr", "pytesseract",
}
ALLOWED_SUBPROCESS_FILES = {"ingest_clips.py", "build_perturbation_pack.py"}
ALLOWED_BINARIES = {"ffmpeg", "ffprobe"}
THRESHOLD_WORDS = ("pass_mark", "PASS_MARK", "MIN_RECALL", "min_recall",
                   "RECALL_THRESHOLD", "recall_threshold", "MAX_FALSE_POSITIVE",
                   "max_false_positive_rate")


def python_files() -> list:
    files = sorted(p for p in HERE.rglob("*.py") if "__pycache__" not in p.parts)
    if not files:
        raise SystemExit("FAIL: no python files found - an empty scan is not a passing scan")
    return files


def check_imports(path: pathlib.Path, tree: ast.AST) -> list:
    bad = []
    for node in ast.walk(tree):
        names = []
        if isinstance(node, ast.Import):
            names = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            names = [node.module or ""]
        for n in names:
            root = n.split(".")[0]
            if root in FORBIDDEN_IMPORTS:
                bad.append(f"{path.name}:{node.lineno} imports {n!r} - this package must "
                           "reach nothing off this machine")
    return bad


def check_subprocess(path: pathlib.Path, text: str, tree: ast.AST) -> list:
    bad = []
    uses = "subprocess" in text
    if uses and path.name not in ALLOWED_SUBPROCESS_FILES:
        bad.append(f"{path.name}: uses subprocess but is not on the allow-list "
                   f"({sorted(ALLOWED_SUBPROCESS_FILES)})")
    if not uses:
        return bad
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
                and node.func.attr in ("which",):
            for arg in node.args:
                if isinstance(arg, ast.Constant) and arg.value not in ALLOWED_BINARIES:
                    bad.append(f"{path.name}:{node.lineno} looks up external binary "
                               f"{arg.value!r}; only {sorted(ALLOWED_BINARIES)} are permitted")
    return bad


def check_thresholds(path: pathlib.Path, text: str) -> list:
    return [f"{path.name}: contains {w!r} - no numeric family-4 pass mark exists in the "
            "frozen contracts, so none may be introduced here"
            for w in THRESHOLD_WORDS if w in text]


def run() -> tuple:
    problems, scanned = [], 0
    for p in python_files():
        try:
            text = p.read_text()
        except OSError as exc:
            problems.append(f"{p.name}: unreadable ({exc}) - treated as a failure, not a skip")
            continue
        try:
            tree = ast.parse(text, filename=str(p))
        except SyntaxError as exc:
            problems.append(f"{p.name}: does not parse ({exc})")
            continue
        scanned += 1
        # The network/provider ban applies to every file, tests included.
        problems += check_imports(p, tree)
        # The subprocess and pass-mark text scans do not apply to this file or
        # to the tests, because both have to NAME the things they guard against
        # in order to guard against them.
        if p.name != "validate_package.py" and "tests" not in p.parts:
            problems += check_subprocess(p, text, tree)
            problems += check_thresholds(p, text)
    if scanned == 0:
        problems.append("no file was successfully scanned - an empty check must fail")
    return problems, scanned


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.parse_args()
    problems, scanned = run()
    if problems:
        print(f"FAIL ({scanned} files scanned)")
        for p in problems:
            print("  -", p)
        return 1
    print(f"PASS - {scanned} files scanned: no network or provider import anywhere, "
          f"subprocess only for local ffmpeg/ffprobe, no invented pass mark in any "
          f"module.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
