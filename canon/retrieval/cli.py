"""Command line for inspecting one bundle. Read-only; makes no model or provider call.

    python3 -m canon.retrieval.cli --request "..."            # human-readable summary
    python3 -m canon.retrieval.cli --request "..." --json     # the model-facing payload
    python3 -m canon.retrieval.cli --brief path/to/brief.txt --size compact
"""
import argparse
import json
import pathlib
import sys

from .budgets import PRESETS
from .tools import CanonContextTools


def _summarise(bundle):
    lines = []
    size = bundle["size"]
    spread = bundle["spread"]
    lines.append(f"corpus     {bundle['corpus']['surface']} · "
                 f"{bundle['corpus']['accepted_sources_available']} accepted sources · "
                 f"fingerprint {bundle['corpus']['corpus_fingerprint']['combined_digest'][:12]}")
    lines.append(f"plan       {bundle['plan']['detected_media']} · "
                 + ", ".join(q["question_id"] for q in bundle["plan"]["questions"]))
    lines.append(f"size       {size['total_chars']} chars "
                 f"(~{size['estimated_tokens']} tokens, budget {size['budget_chars']}) · "
                 f"{size['items_delivered_complete']}/{spread['items']} delivered whole")
    lines.append(f"spread     {spread['items']} items · {spread['distinct_sources']} sources · "
                 f"{spread['distinct_lineage_groups']} independent origins · "
                 + ", ".join(f"{k}×{v}" for k, v in sorted(spread["items_by_kind"].items())))
    if bundle["coverage"]["questions_with_no_item"]:
        lines.append("uncovered  " + ", ".join(bundle["coverage"]["questions_with_no_item"]))
    lines.append("")
    for item in bundle["items"]:
        content = item["content"]
        headline = (content.get("concept_label") or content.get("label")
                    or content.get("term") or content.get("visual_kind")
                    or (content.get("what_it_binds_to") or {}).get("target_path")
                    or item["item_id"])
        lines.append(f"  {item['n']:2d}. [{item['kind']}] {headline}")
        lines.append(f"      {item['source']['source_dir']} · {item['item_id']} · "
                     f"answers {item['answers_question']}")
        body = (content.get("claim") or content.get("description")
                or content.get("rationale") or content.get("definition_in_origin_frame")
                or content.get("what_the_visual_supports") or "")
        if body:
            lines.append(f"      {' '.join(body.split())[:200]}")
        epi = item["epistemics"]
        marks = [f"status={epi.get('source_status')}"]
        for field in ("claim_type", "source_uncertainty", "extraction_uncertainty",
                      "binding_status", "evidence_basis"):
            if epi.get(field):
                marks.append(f"{field}={epi[field]}")
        lines.append("      " + " · ".join(marks))
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build one Canon context bundle.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--request", help="the customer request text")
    source.add_argument("--brief", help="path to a file containing the request text")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--size", choices=sorted(PRESETS), default="default")
    parser.add_argument("--need", action="append", default=[],
                        help="a declared knowledge need; repeatable")
    parser.add_argument("--json", action="store_true", help="print the model-facing payload")
    args = parser.parse_args(argv)

    request = args.request or pathlib.Path(args.brief).read_text(encoding="utf-8")
    tools = CanonContextTools(args.repo_root)
    bundle = tools.canon_context(request, knowledge_needs=args.need, size=args.size)
    print(json.dumps(bundle, indent=2, ensure_ascii=False) if args.json
          else _summarise(bundle))
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
