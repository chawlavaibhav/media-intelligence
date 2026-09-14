"""One command: a customer brief in, the complete dry Alpha-1 chain out.

    python3 -m runtime.alpha.cli <brief.json> [--store DIR] [--accept | --reject]
        [--post-draw clean|lettering_then_clean|lettering_always|no_artifact] [--at UTC]
        [--consent-ref REF] [--json]

Exit 0 when the chain reached its intended dry end state; 3 when it refused (the refusal is
printed with its code and reason, which is a valid result — a precise refusal is the product
working); 2 on a usage error. Nothing is sent anywhere; nothing costs money.
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile

from .run import HUMAN_VERDICTS, POST_DRAW_SCENARIOS, AlphaRunner


def render(result) -> str:
    out = [f"ALPHA-1 DRY RUN  {result.job_id}  profile {result.profile}", "=" * 78]
    for s in result.stages:
        mark = {"ok": "OK  ", "refused": "REF ", "skipped": "--  "}[s.status]
        out.append(f"  {mark} {s.stage:<14} {s.summary}")
        if s.refusal:
            out.append(f"       {s.refusal['code']}: {s.refusal['message'][:400]}")
    out.append("")
    out.append(f"FINAL STATE: {result.final_state}")
    out.append(f"run dir: {result.run_dir}")
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="runtime.alpha.cli", description=__doc__)
    ap.add_argument("brief")
    ap.add_argument("--store", default=None, help="job/outcome/template store root (default: a throwaway directory)")
    ap.add_argument("--at", default=None, help="fixed UTC timestamp for a reproducible run")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--accept", action="store_true", help="the human accepts the (synthetic) result")
    g.add_argument("--reject", action="store_true", help="the human rejects the (synthetic) result")
    ap.add_argument("--post-draw", default="clean", choices=POST_DRAW_SCENARIOS,
                    help="scripted synthetic post-draw scenario (never a paid detector)")
    ap.add_argument("--consent-ref", default=None, help="supply a consent reference for identifiable-person assets")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    verdict = "accept" if args.accept else ("reject" if args.reject else None)
    assert verdict in HUMAN_VERDICTS
    store = args.store or tempfile.mkdtemp(prefix="runtime-alpha-")
    result = AlphaRunner().run(args.brief, store_root=store, human_verdict=verdict, post_draw=args.post_draw,
                               at=args.at, consent_ref=args.consent_ref)
    print(json.dumps(result.summary(), ensure_ascii=False, indent=2) if args.json else render(result))
    return 0 if result.refusal is None else 3


if __name__ == "__main__":
    sys.exit(main())
