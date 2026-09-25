#!/usr/bin/env python3
"""Pre-flight for the overnight bake-off. Prints NAMES and yes/no only — never a key value.

    python3 eval/media-bakeoff-v0/preflight.py

Keys must already be in the environment (start the session with `source ~/.mi-keys && claude`).
Exit 0 = ready to ask the founder for GO; exit 1 = something missing (listed).
"""
from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

REQUIRED_KEYS = ["GOOGLE_API_KEY"]   # Nano Banana 2 + Veo via the Gemini API (or the Vertex SA file below)
# Writer: ANTHROPIC_API_KEY (Claude) or AZURE_OPENAI_* (GPT-5.6 Sol / Luna); at least one must be present.
OPTIONAL_KEYS = ["ANTHROPIC_API_KEY", "AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT", "SARVAM_API_KEY", "GOOGLE_CLOUD_VISION_API_KEY"]
FILES = {"vertex service account (optional)": Path.home() / ".aight-litellm-keys" / "vertex-sa.json"}
TOOLS = ["ffmpeg", "ffprobe", "git"]
MODULES = ["yaml"]


def main() -> int:
    missing = []
    print("KEYS (name: present?)")
    for k in REQUIRED_KEYS:
        ok = bool(os.environ.get(k))
        print(f"  {k}: {'yes' if ok else 'NO  <- required'}")
        if not ok:
            missing.append(k)
    for k in OPTIONAL_KEYS:
        print(f"  {k}: {'yes' if os.environ.get(k) else 'no (optional)'}")
    if not (os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("AZURE_OPENAI_API_KEY")):
        print("  NO writer key (need ANTHROPIC_API_KEY or AZURE_OPENAI_API_KEY)  <- required")
        missing.append("writer key")
    if not os.environ.get("AZURE_OPENAI_API_KEY"):
        print("  -> no Azure key: understand step uses Gemini Flash; GPT Image 2 fallback unavailable. Log in RUN-LOG.md")
    print("  fal: not used (not available)")
    for label, p in FILES.items():
        print(f"  {label}: {'yes' if p.exists() else 'no'}")
    print("TOOLS")
    for t in TOOLS:
        ok = shutil.which(t) is not None
        print(f"  {t}: {'yes' if ok else 'NO'}")
        if not ok and t != "git":
            missing.append(t)
    for m in MODULES:
        ok = importlib.util.find_spec(m) is not None
        print(f"  python module {m}: {'yes' if ok else 'NO'}")
        if not ok:
            missing.append(m)
    here = Path(__file__).resolve().parent
    for f in ("HANDOFF.md", "BRIEFS.yaml", "PROMPTS.md", "make_pairs.py", "score.py", "viewer.html"):
        if not (here / f).exists():
            missing.append(f)
    try:
        subprocess.run(["git", "ls-remote", "--exit-code", "origin", "claude/magical-volta-q45jee"],
                       check=True, capture_output=True, timeout=30)
        print("GIT: can reach origin branch: yes")
    except Exception:
        print("GIT: can reach origin branch: NO")
        missing.append("git origin")
    print("\nRESULT:", "READY — now write the explain-back and ask the founder for GO" if not missing
          else f"NOT READY — missing: {', '.join(missing)}")
    return 0 if not missing else 1


if __name__ == "__main__":
    sys.exit(main())
