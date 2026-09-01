#!/usr/bin/env python3
"""EVAL-038 — deterministic injection-payload builder (USD 0).

Implements canon/compilation/INJECTION-CONTRACT-v0.md against the two compiled packs,
selected per brief by canon/packs/pack-triggers-v0.yaml. Serializes the EXACT system
and user payload for every brief, records byte counts, SHA-256 digests and token
estimates (ceil(chars/4), the repo convention), and verifies every payload fits each
candidate model's input quota with headroom — the §5.4 pre-check of
canon/findings/PROPOSED-EVAL-038-SUBSTITUTION-DESIGN.md.

Authority: DN-07 (canon/candidates/canon-014/REP-07-DECISION-NOTES.md).
Zero model calls, zero network, zero spend. Deterministic: same tree -> same bytes.
"""
import hashlib
import math
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[4]
E37 = ROOT / "eval/experiments/EVAL-037"
E38 = ROOT / "eval/experiments/EVAL-038"
COMP = ROOT / "canon/compilation"

# ── Injection-contract §2: the invariant system-prompt block, verbatim from the
#    contract's fenced block.
def contract_block():
    text = (COMP / "INJECTION-CONTRACT-v0.md").read_text()
    m = re.search(r"```\n(CANON_DOCTRINE.*?)```", text, re.S)
    if not m:
        sys.exit("FATAL: CANON_DOCTRINE fenced block not found in INJECTION-CONTRACT-v0.md")
    return m.group(1).rstrip("\n")

# ── Trigger-table selection per brief. The NR-field mapping from each brief's prose is
#    recorded here as data so the manifest carries it; the trigger table itself
#    (pack-triggers-v0.yaml) supplies modality base sets, universal packs and conditions.
BRIEF_NR = {
    "B01": {"modality": "video", "requested_operation": "generate",
            "text_requirements_nonempty": True,   # brand name + positioning must appear
            "product_or_packshot_entity_present": False,  # software product, no packshot
            "language_topology_present_or_market_IN": True,  # "credible and Indian"
            "advertising_acceptance_intent": True,
            "website_snapshot": "rentok.com"},
    "B02": {"modality": "static_image", "requested_operation": "generate",
            "text_requirements_nonempty": True,   # two prices must be legible
            "product_or_packshot_entity_present": False,  # API product, no physical hero
            "language_topology_present_or_market_IN": True,  # Indian businesses, INR
            "advertising_acceptance_intent": True,
            "website_snapshot": "getaight.ai"},
    "B03": {"modality": "static_image", "requested_operation": "generate",
            "text_requirements_nonempty": False,
            "product_or_packshot_entity_present": True,   # drink is the unmistakable hero
            "language_topology_present_or_market_IN": True,  # urban Indian consumers
            "advertising_acceptance_intent": True,
            "website_snapshot": None},
    "B04": {"modality": "video", "requested_operation": "generate",
            "text_requirements_nonempty": False,
            "product_or_packshot_entity_present": True,   # serum demonstrated on camera
            "language_topology_present_or_market_IN": True,  # Indian D2C brand
            "advertising_acceptance_intent": True,
            "website_snapshot": None},
    "B05": {"modality": "video", "requested_operation": "generate",
            "text_requirements_nonempty": False,
            "product_or_packshot_entity_present": False,
            "language_topology_present_or_market_IN": False,  # unmarked cinematic scene
            "advertising_acceptance_intent": False,           # drama, not an ad
            "website_snapshot": None},
    "B06": {"modality": "static_image", "requested_operation": "generate",
            "text_requirements_nonempty": False,
            "product_or_packshot_entity_present": True,   # the watch
            "language_topology_present_or_market_IN": False,
            "advertising_acceptance_intent": True,        # e-commerce hero image
            "website_snapshot": None},
}

COMPILED = {
    "composition_and_attention": COMP / "PACK-composition_and_attention-v0.yaml",
    "product_appearance": COMP / "PACK-product_appearance-v0.yaml",
}

CONDITION_TO_PACK = {
    "text_requirements_nonempty": "typography_and_copy",
    "product_or_packshot_entity_present": "product_appearance",
    "language_topology_present_or_market_IN": "indian_indic_context",
    "advertising_acceptance_intent": "commercial_communication",
}

# Input quotas (tokens) the payload must fit with headroom, per the §5.4 pre-check.
MODEL_INPUT_QUOTA = {"claude-haiku-4-5-20251001": 200_000, "gemma-4-31b-it": 16_000}
HEADROOM = 0.85  # payload must use at most 85% of quota

V2_INSTRUCTIONS = """
FINAL_PRODUCTION_PACKAGE schema v2 requirements (INJECTION-CONTRACT-v0 §3):

Add one required section, DOCTRINE_DEVIATIONS, immediately after FAILURE_PREVENTION.
One line per overridden pack default: `<decision-id>: overridden because <verbatim brief
clause>`. The literal value `none` is valid only when every injected default was accepted.
A brief-fixed deliverable parameter (aspect ratio, duration, placement, format) is itself
a forcing brief clause: record any collision with a pack default here, citing the brief's
parameter clause — never fabricate a scene-based justification for a brief-fixed parameter.

FAILURE_PREVENTION must begin with one line per injected check id, in pack order:
`<check-id>: pass` or `<check-id>: fix: <what was changed to make it pass>`. A missing
check id is a package defect. Free-form additions are allowed after the check-id lines.

VISUAL_SYSTEM must contain these four typed subfields, each on its own labelled line:
`attention_order:` (1st/2nd/3rd read, each with its single dominant cue — CA-D1),
`surface_finish_per_key_object:` (object -> matte/diffuse, glossy/direct, or glare — PA-D1),
`implied_light_source:` (the one nameable fictional source and its direction — PA-D2/PA-D4),
`placement_zone:` (subject zone + the stated reason, never a ratio — CA-D2/PA-D5).
When the pack feeding a subfield was not injected for this request, write the literal
`not_governed_by_injected_doctrine` — absence must be distinguishable from neglect.
""".strip()

def base_system_prompt():
    """EVAL-037 v1 system prompt adapted for EVAL-038: no tools, v2 sections."""
    v1 = (E37 / "common/system-prompt.txt").read_text()
    out = v1.replace("Use tools only when you judge them useful.\n\n", "")
    out = out.replace(
        "FAILURE_PREVENTION\nHARD_CONSTRAINT_CHECK\nKNOWLEDGE_AND_WEBSITE_USE",
        "FAILURE_PREVENTION\nDOCTRINE_DEVIATIONS\nHARD_CONSTRAINT_CHECK\nKNOWLEDGE_AND_WEBSITE_USE")
    out = out.replace(
        "List only knowledge/website sources actually used.",
        "List only knowledge/website sources actually used. Website material, when the "
        "brief permits a website, is provided verbatim in the user message; no browsing "
        "exists here.")
    return out.rstrip("\n") + "\n\n" + V2_INSTRUCTIONS

def gap_notice(selected, injected):
    missing = [p for p in selected if p not in injected]
    if not missing:
        return ""
    return ("CANON COVERAGE GAP: the trigger table selects these packs for this request, "
            "but they are not yet compiled and are therefore NOT injected: "
            + ", ".join(missing) + ". Canon has no delivered doctrine for those domains in "
            "this request — no defaults, no checks. Proceed on the brief alone for those "
            "domains, state this gap in FAILURE_PREVENTION, and do not attribute decisions "
            "in those domains to Canon.")

def selection_for(brief_id, triggers):
    nr = BRIEF_NR[brief_id]
    selected = list(triggers["universal_packs"])
    selected += triggers["modality_base_packs"][nr["modality"]]
    for cond, pack in CONDITION_TO_PACK.items():
        if nr[cond]:
            selected.append(pack)
    # canonical order: universal -> modality-base -> conditional (list already built so)
    injected = [p for p in selected if p in COMPILED]
    return selected, injected

def sha256(b):
    return hashlib.sha256(b).hexdigest()

def tokens(s):
    return math.ceil(len(s) / 4)

def main():
    triggers = yaml.safe_load((COMP.parent / "packs/pack-triggers-v0.yaml").read_text())
    block = contract_block()
    base = base_system_prompt()
    payload_dir = E38 / "payloads"
    payload_dir.mkdir(parents=True, exist_ok=True)
    manifest = {"experiment": "EVAL-038", "authority": "DN-07",
                "token_estimate_rule": "ceil(chars/4)", "briefs": {}}
    ok = True
    for brief_id in sorted(BRIEF_NR):
        nr = BRIEF_NR[brief_id]
        selected, injected = selection_for(brief_id, triggers)
        pack_texts, pack_digests = [], {}
        for p in injected:
            doc = yaml.safe_load(COMPILED[p].read_text())
            t = doc["terse_injection_text"]
            pack_texts.append(t)
            pack_digests[p] = sha256(t.encode())
        notice = gap_notice(selected, injected)
        system = base + "\n\n" + block + "\n\n" + "\n\n".join(pack_texts)
        if notice:
            system += "\n\n" + notice
        brief = (E37 / f"common/briefs/{brief_id}.txt").read_text()
        user = brief.rstrip("\n")
        site_digest = None
        if nr["website_snapshot"]:
            page = (E37 / f"common/websites/{nr['website_snapshot']}/page.txt").read_text()
            site_digest = sha256(page.encode())
            user += ("\n\n--- OFFICIAL WEBSITE SNAPSHOT (frozen, read-only, "
                     f"{nr['website_snapshot']}) ---\n" + page)
        (payload_dir / f"{brief_id}.system.txt").write_text(system)
        (payload_dir / f"{brief_id}.user.txt").write_text(user)
        total = tokens(system) + tokens(user)
        fits = {}
        for model, quota in MODEL_INPUT_QUOTA.items():
            fits[model] = total <= quota * HEADROOM
            if not fits[model]:
                ok = False
        manifest["briefs"][brief_id] = {
            "nr_mapping": nr,
            "packs_selected_by_trigger_table": selected,
            "packs_injected_compiled_only": injected,
            "packs_selected_but_uncompiled": [p for p in selected if p not in injected],
            "pack_text_sha256": pack_digests,
            "website_snapshot_sha256": site_digest,
            "system_sha256": sha256(system.encode()),
            "system_bytes": len(system.encode()),
            "user_sha256": sha256(user.encode()),
            "user_bytes": len(user.encode()),
            "input_tokens_estimate": total,
            "fits_quota_with_15pct_headroom": fits,
        }
    out = payload_dir / "PAYLOAD-MANIFEST.yaml"
    out.write_text("# EVAL-038 payload manifest — generated by tools/build_payloads.py\n"
                   "# Deterministic over the committed tree; regenerate and diff to verify.\n"
                   + yaml.safe_dump(manifest, sort_keys=True, allow_unicode=True, width=100))
    for brief_id, rec in sorted(manifest["briefs"].items()):
        print(f"{brief_id}: inject={rec['packs_injected_compiled_only']} "
              f"~{rec['input_tokens_estimate']} tok "
              f"fits={rec['fits_quota_with_15pct_headroom']}")
    print("PASS: all payloads fit all quotas with headroom" if ok
          else "FAIL: at least one payload exceeds a quota")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
