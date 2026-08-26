#!/usr/bin/env python3
"""CANON-010 — validate the request-freeze package and emit REQUEST-COVERAGE-EXTENSION.jsonl.

FAILS CLOSED. Every gate below corresponds to a way this package could quietly become wrong, and
each one is stated in the CANON-010 task's "Mechanical gates" section. Nothing is written unless all
of them pass.

    G1  the original 30-bank bytes changed
    G2  an extension item lacks requested operation or input/output cardinality semantics
    G3  a workflow/provider/model value appears as the resolution of a requested operation
    G4  customer-specified provenance is assigned to something the customer did not say
    G5  a runnable Wave-1 multi-turn item exists without a frozen history contract
    G6  language variants are exact duplicates with no language-dependent requirement
    G7  a grammar field has no provenance rule or operation rule

Run: python3 canon/experiments/pre-execution-freeze/validate_request_freeze.py
"""
from __future__ import annotations

import collections
import hashlib
import json
import pathlib
import re
import sys

import yaml

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
GRAMMAR = HERE / "MEDIA-REQUEST-GRAMMAR-v1.yaml"
EXT_SRC = HERE / "request-coverage-extension-source.yaml"
EXT_OUT = HERE / "REQUEST-COVERAGE-EXTENSION.jsonl"
BANK_DIR = ROOT / "canon/experiments/v1/brief-bank"

# G1. The frozen 30-bank, hashed at the moment CANON-010 began, against `main`'s committed bytes.
# The Controller decision requires these 30 to stay byte-identical as the generation-core /
# value-gate bank. If either hash moves, this package is invalid regardless of anything else.
FROZEN_30_BANK = {
    "briefs-source.yaml": "95ef1c4110b811b8b98650193493321108e581d22708cc82db70fc8f7ed6f43b",
    "briefs.jsonl": "2e313d04f98ab8c2ea76e8b28dc2762a7759966053583f3935c42908a5dae8f8",
}

# G3. Production routes. A customer asks for an outcome; these are techniques for producing one.
# Admitting any of them as a requested_operation collapses customer intent into workflow mode.
WORKFLOW_TOKENS = {
    "inpaint", "inpainting", "outpaint", "outpainting", "img2img", "image2image", "text2img",
    "txt2img", "controlnet", "lora", "ipadapter", "ip-adapter", "upscale", "upscaling",
    "segment_and_composite", "sdxl", "flux", "diffusion", "checkpoint", "sampler", "cfg",
    "latent", "denoise", "workflow_mode", "pipeline",
}
# G3/model names. Canon must not select models or providers anywhere in this package.
PROVIDER_TOKENS = {
    "midjourney", "dall-e", "dalle", "stable diffusion", "firefly", "imagen", "runway",
    "pika", "kling", "veo", "sora", "luma", "seedream", "recraft", "ideogram", "openai",
    "anthropic", "google", "fal.ai",
}


def fail(errors: list[str], gate: str, msg: str) -> None:
    errors.append(f"[{gate}] {msg}")


def gate_1_bank_unchanged(errors: list[str]) -> dict:
    """The original 30 briefs must be byte-identical."""
    observed = {}
    for name, expected in FROZEN_30_BANK.items():
        path = BANK_DIR / name
        if not path.exists():
            fail(errors, "G1", f"{name} is missing from the frozen 30-bank")
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        observed[name] = digest
        if digest != expected:
            fail(errors, "G1",
                 f"{name} CHANGED. expected sha256 {expected[:16]}… got {digest[:16]}… — the "
                 f"original 30 briefs must remain byte-identical")
    src = BANK_DIR / "briefs-source.yaml"
    if src.exists():
        doc = yaml.safe_load(src.read_text()) or {}
        n = len(doc.get("briefs") or [])
        if n != 30:
            fail(errors, "G1", f"the frozen bank holds {n} briefs, expected 30")
        observed["brief_count"] = n
    return observed


def gate_7_grammar_rules(grammar: dict, errors: list[str]) -> None:
    """Every grammar field needs a provenance rule and an operation rule."""
    for f in grammar.get("fields", []):
        fid = f.get("id", "?")
        if not f.get("provenance_rule"):
            fail(errors, "G7", f"grammar field {fid} ({f.get('field')}) has no provenance_rule")
        if not f.get("operation_rule"):
            fail(errors, "G7", f"grammar field {fid} ({f.get('field')}) has no operation_rule")
    ops = grammar["vocabularies"]["requested_operation"]
    for bad in ops.get("forbidden_values", []):
        if bad in ops["values"]:
            fail(errors, "G3", f"grammar admits production route {bad!r} as a requested_operation")
    if not ops.get("forbidden_values"):
        fail(errors, "G3", "grammar declares no forbidden production-route values")


def gate_3_no_workflow(item: dict, errors: list[str], allowed_ops: set[str]) -> None:
    """Requested operation must be customer intent, never a workflow mode or a provider."""
    op = item.get("requested_operation")
    if op not in allowed_ops:
        fail(errors, "G3", f"{item['item_id']}: requested_operation {op!r} is not in the grammar "
                           f"vocabulary")
    if isinstance(op, str) and op.lower() in WORKFLOW_TOKENS:
        fail(errors, "G3", f"{item['item_id']}: requested_operation {op!r} is a production route, "
                           f"not customer intent")
    blob = json.dumps(item, ensure_ascii=False).lower()
    for tok in WORKFLOW_TOKENS:
        if re.search(rf"\b{re.escape(tok)}\b", blob):
            fail(errors, "G3", f"{item['item_id']}: contains workflow token {tok!r} — customer "
                               f"requests describe outcomes, not techniques")
    for tok in PROVIDER_TOKENS:
        if re.search(rf"\b{re.escape(tok)}\b", blob):
            fail(errors, "G3", f"{item['item_id']}: names provider/model {tok!r}; Canon does not "
                               f"select models or providers")


def gate_2_required_semantics(item: dict, errors: list[str], grammar: dict) -> None:
    """Operation, supplied inputs and cardinality/set semantics must all be present."""
    iid = item.get("item_id", "?")
    if not item.get("requested_operation"):
        fail(errors, "G2", f"{iid}: no requested_operation")
    ds = item.get("deliverable_set")
    if not ds:
        fail(errors, "G2", f"{iid}: no deliverable_set — output cardinality semantics are required")
        return
    for key in ("cardinality", "variation_axis", "acceptance_basis"):
        if key not in ds:
            fail(errors, "G2", f"{iid}: deliverable_set is missing {key}")
    if ds.get("acceptance_basis") == "best_n_of_m" and "best_n" not in ds:
        fail(errors, "G2", f"{iid}: acceptance_basis best_n_of_m without best_n")

    op = item.get("requested_operation")
    ops_vocab = grammar["vocabularies"]["requested_operation"]["values"]
    needs_asset = ops_vocab.get(op, {}).get("supplied_asset_required")
    supplied = item.get("supplied_inputs") or []
    if needs_asset and not supplied:
        fail(errors, "G2", f"{iid}: operation {op!r} acts on a supplied artefact but none is given")
    if needs_asset:
        roles = {a.get("role") for a in supplied}
        if op in ("edit", "animate", "restore", "extend") and "subject_of_operation" not in roles:
            fail(errors, "G2", f"{iid}: operation {op!r} needs an asset with role "
                               f"subject_of_operation; got {sorted(roles)}")
    if op == "variants" and ds.get("cardinality", 1) <= 1:
        fail(errors, "G2", f"{iid}: requested_operation variants requires cardinality > 1")
    if not item.get("constraints"):
        fail(errors, "G2", f"{iid}: no constraints block")
    else:
        for k in ("hard", "soft", "free"):
            if k not in item["constraints"]:
                fail(errors, "G2", f"{iid}: constraints missing {k!r}")
    if not item.get("preservation_semantics"):
        fail(errors, "G2", f"{iid}: no preservation/change semantics")
    if not item.get("grammar_features"):
        fail(errors, "G2", f"{iid}: no grammar_features mapping")
    if "runnable_wave1" not in item:
        fail(errors, "G2", f"{iid}: runnable_wave1 not declared")


def gate_4_provenance_honesty(item: dict, errors: list[str]) -> None:
    """A requirement may be attributed to the customer only if the request text carries it.

    The check is deliberately narrow and mechanical: any mutation intent whose detail claims the
    customer named it must correspond to something in the request text. Assigning customer
    provenance to a system decision is the error that lets a bad plan be scored as a misread request.
    """
    iid = item.get("item_id", "?")
    text = (item.get("request_text") or "").lower()
    mi = item.get("mutation_intents") or {}
    if not mi.get("preservation_default"):
        fail(errors, "G4", f"{iid}: mutation_intents has no preservation_default — implicit "
                           f"preservation must be recorded, never enumerated as customer statements")
    raw = item.get("request_text") or ""
    for intent in (mi.get("intents") or []):
        detail = (intent.get("detail") or "").lower()
        if "customer named this" in detail:
            # The author must point at the customer's actual words. Word-overlap heuristics cannot
            # do this across scripts — an English target description will never match a Devanagari
            # request — and a check that quietly passes on non-Latin text is worse than none.
            quote = intent.get("evidence_quote")
            if not quote:
                fail(errors, "G4",
                     f"{iid}: intent on {intent.get('target')!r} claims customer provenance but "
                     f"carries no evidence_quote pointing at the customer's words")
            elif quote not in raw:
                fail(errors, "G4",
                     f"{iid}: intent on {intent.get('target')!r} quotes {quote!r}, which does not "
                     f"appear in the request text")
    for exact in (item.get("constraints", {}).get("hard") or []):
        m = re.findall(r'"([^"]{2,})"', exact)
        for quoted in m:
            if quoted.lower() not in text and quoted not in (item.get("request_text") or ""):
                fail(errors, "G4",
                     f"{iid}: hard constraint quotes {quoted!r} which does not appear in the "
                     f"request text")


def gate_5_multi_turn(item: dict, errors: list[str], history_contract_frozen: bool) -> None:
    """No runnable Wave-1 multi-turn item without a frozen history contract."""
    iid = item.get("item_id", "?")
    is_multi = bool(item.get("representation_only")) or \
        "multi_turn_inheritance" in (item.get("covers_cooccurrence") or []) or \
        bool(re.search(r"round\s*[123]", (item.get("request_text") or ""), re.I))
    if is_multi:
        if item.get("runnable_wave1"):
            fail(errors, "G5", f"{iid}: multi-turn item marked runnable_wave1 while no request "
                               f"history contract is frozen")
        if not item.get("representation_only"):
            fail(errors, "G5", f"{iid}: multi-turn item not marked representation_only")
        if not item.get("representation_only_reason"):
            fail(errors, "G5", f"{iid}: representation_only without a stated reason")
    if item.get("representation_only") and item.get("runnable_wave1"):
        fail(errors, "G5", f"{iid}: representation_only and runnable_wave1 are contradictory")
    if is_multi and history_contract_frozen:
        pass  # placeholder: when a contract exists this gate relaxes by Controller decision


def gate_6_language_earned(items: list[dict], errors: list[str]) -> None:
    """A non-English item must earn its language with a stated, real dependency."""
    def norm(t: str) -> str:
        return re.sub(r"\s+", " ", (t or "")).strip().lower()

    seen: dict[str, str] = {}
    for it in items:
        iid = it["item_id"]
        lang = it.get("language")
        dep = it.get("language_dependency")
        if lang != "english" and not dep:
            fail(errors, "G6", f"{iid}: language {lang!r} with no language_dependency — a "
                               f"translated duplicate tests only translation")
        if lang != "english" and dep and len(dep.split()) < 12:
            fail(errors, "G6", f"{iid}: language_dependency is too thin to be a real requirement")
        key = norm(it.get("request_text"))
        if key in seen:
            fail(errors, "G6", f"{iid}: request text is an exact duplicate of {seen[key]}")
        seen[key] = iid
    # Two items with the same operation AND the same co-occurrence set differing only by language
    by_sig: dict[tuple, list[str]] = collections.defaultdict(list)
    for it in items:
        sig = (it.get("requested_operation"), tuple(sorted(it.get("covers_cooccurrence") or [])))
        by_sig[sig].append(it["item_id"])
    for sig, ids in by_sig.items():
        if len(ids) > 1:
            langs = {next(i["language"] for i in items if i["item_id"] == x) for x in ids}
            if len(langs) > 1:
                fail(errors, "G6", f"items {ids} differ only by language for operation {sig[0]!r} "
                                   f"with identical coverage — one of them adds nothing")


def main() -> int:
    errors: list[str] = []
    grammar = yaml.safe_load(GRAMMAR.read_text())
    ext = yaml.safe_load(EXT_SRC.read_text())
    items = ext["items"]
    allowed_ops = set(grammar["vocabularies"]["requested_operation"]["values"])

    bank = gate_1_bank_unchanged(errors)
    gate_7_grammar_rules(grammar, errors)
    gate_6_language_earned(items, errors)

    ids = [i["item_id"] for i in items]
    for dup, n in collections.Counter(ids).items():
        if n > 1:
            errors.append(f"[G2] duplicate item_id {dup}")

    for item in items:
        gate_2_required_semantics(item, errors, grammar)
        gate_3_no_workflow(item, errors, allowed_ops)
        gate_4_provenance_honesty(item, errors)
        gate_5_multi_turn(item, errors, history_contract_frozen=False)
        for feat in item.get("grammar_features", []):
            if feat not in {f["id"] for f in grammar["fields"]}:
                fail(errors, "G2", f"{item['item_id']}: unknown grammar feature {feat!r}")

    if errors:
        print(json.dumps({"status": "FAILED", "error_count": len(errors), "errors": errors},
                         indent=2, ensure_ascii=False))
        return 1

    rows = []
    for it in items:
        rows.append({
            "item_id": it["item_id"],
            "requested_operation": it["requested_operation"],
            "language": it["language"],
            "media_class": it["media_class"],
            "business": it["business"],
            "request_text": " ".join(it["request_text"].split()),
            "supplied_inputs": it.get("supplied_inputs", []),
            "mutation_intents": it.get("mutation_intents", {}),
            "motion_intent": it.get("motion_intent"),
            "constraints": it["constraints"],
            "preservation_semantics": " ".join(it["preservation_semantics"].split()),
            "deliverable_set": it["deliverable_set"],
            "acceptance_relevant": it["acceptance_relevant"],
            "grammar_features": it["grammar_features"],
            "covers_cooccurrence": it.get("covers_cooccurrence", []),
            "runnable_wave1": it["runnable_wave1"],
            "representation_only": bool(it.get("representation_only")),
            "language_dependency": it.get("language_dependency"),
        })
    EXT_OUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))

    summary = {
        "status": "PASSED",
        "gates": {
            "G1_frozen_30_bank_unchanged": "pass",
            "G2_required_semantics": "pass",
            "G3_no_workflow_or_provider_as_operation": "pass",
            "G4_provenance_honesty": "pass",
            "G5_multi_turn_not_runnable": "pass",
            "G6_language_earned": "pass",
            "G7_grammar_fields_have_rules": "pass",
        },
        "frozen_30_bank": bank,
        "grammar": {"fields": len(grammar["fields"]), "rules": len(grammar["rules"]),
                    "operations": sorted(allowed_ops)},
        "extension": {
            "items": len(rows),
            "by_operation": dict(collections.Counter(r["requested_operation"] for r in rows)),
            "by_language": dict(collections.Counter(r["language"] for r in rows)),
            "runnable_wave1": sum(1 for r in rows if r["runnable_wave1"]),
            "representation_only": sum(1 for r in rows if r["representation_only"]),
        },
        "output": str(EXT_OUT.relative_to(ROOT)),
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
