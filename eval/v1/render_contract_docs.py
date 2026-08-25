#!/usr/bin/env python3
"""Render CAPABILITY-CONTRACT.md and CAPABILITY-DEPENDENCY-MATRIX.md from the YAML.

Generated, never hand-edited: the YAML is the single source of truth, so the
prose cannot drift away from the machine-readable contract. The project has
already paid for that failure mode once - "descriptions can be wrong for months
while every integrity check passes".

Run:  python3 eval/v1/render_contract_docs.py
"""
import yaml, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "eval/v1/capability-contract.yaml"
DOC = ROOT / "eval/v1/CAPABILITY-CONTRACT.md"
MTX = ROOT / "eval/v1/CAPABILITY-DEPENDENCY-MATRIX.md"

FAMILY_TITLES = {
    "A_constraint_fidelity": "A · Constraint fidelity — did it do the specific checkable thing it was told to do?",
    "B_text_brand": "B · Text & brand — the family the Indian-market scope makes unavoidable",
    "C_identity_references": "C · Identity & references — “is this the same person / the same product?”",
    "D_human_physical_realism": "D · Human & physical realism — the failures a customer notices instantly",
    "E_temporal_continuity": "E · Temporal / continuity — defects that exist *between* frames",
    "F_speech_audio": "F · Speech / audio",
    "G_commercial_creative": "G · Commercial / creative fitness — descriptive only, never a hard gate",
    "H_operational": "H · Operational / workflow behaviour — derived, never generates its own trials",
}
INSTRUMENT_NAMES = {
    1: "text/OCR", 2: "deterministic CV/geometry", 3: "structured visual VLM",
    4: "temporal/video", 5: "speech/audio/AV", 6: "creative/commercial",
    "operational": "operational logging (no instrument)",
}
STATUS_LABEL = {
    "measurable_now": "measurable now",
    "blocked_pending_instrument": "blocked — no qualified instrument",
    "blocked_pending_resource": "blocked — resource missing",
    "currently_unmeasurable": "currently unmeasurable",
}


def main():
    doc = yaml.safe_load(SRC.read_text())
    dims = doc["dimensions"]
    by_family = collections.OrderedDict()
    for d in dims:
        by_family.setdefault(d["family"], []).append(d)

    o = []
    o.append("# Eval V1 — Capability & Measurement Contract\n")
    o.append("> **GENERATED FILE — do not hand-edit.**  \n"
             "> Source of truth: [`capability-contract.yaml`](capability-contract.yaml).  \n"
             "> Regenerate with `python3 eval/v1/render_contract_docs.py`.  \n"
             "> Validate with `python3 eval/v1/validate_capability_contract.py`.\n")
    o.append(f"**Task:** E1 · **Date:** {doc['date']} · **Status:** "
             f"`{doc['status']}` · **Contract version:** `{doc['contract_version']}`\n")
    o.append("## What this document is\n")
    o.append(
        "This is the **measurement contract**: it says what each of the 36 frozen capabilities "
        "*means*, at what unit it must be observed, how it is tested, which instrument judges it, "
        "and what has to be held fixed for two measurements to be comparable.\n\n"
        "**It contains no results.** No model has been measured, no instrument is qualified, and "
        "nothing here licenses a capability claim. Its purpose is that a later task cannot quietly "
        "redefine what a capability meant and report the rerun as the same experiment.\n")

    o.append("## The three rules that protect every number downstream\n")
    o.append(
        "**1 · One generation is one trial.** Several evaluators may score that one trial. Those "
        "are several *measurements* of one trial, never several trials. Frames sampled from one "
        "clip carry the parent trial id and remain one trial. Confidence is computed on "
        "independent **base items** — never on trials, never on frames. The founding example: a "
        "prior study's 14 samples came from only 4 independent sources, so treating them as 14 "
        "overstates confidence roughly threefold.\n\n"
        "**2 · The observation unit is load-bearing.** A misspelling that *changes* partway through "
        "a clip does not exist in any single frame — it exists only *between* frames. Choose the "
        "wrong unit and the defect is undetectable, not merely under-measured. The unit vocabulary "
        "is Canon's (`SPEC-04`), adopted unchanged: `frame`, `shot`, `shot_pair`, `sequence`, "
        "`whole_asset`, `asset_set_over_time`.\n\n"
        "**3 · Generate once, measure everything valid.** A generated asset may feed every "
        "measurement for which it is a valid observation unit. Never regenerate because a second "
        "evaluator wants to look. Reuse never turns one asset into multiple independent trials.\n")

    o.append("## Summary\n")
    ms = collections.Counter(d["measurability_status"] for d in dims)
    o.append("| | Count |\n|---|---:|")
    o.append(f"| Capabilities defined | **{len(dims)} / 36** |")
    o.append(f"| Measurable now | {ms['measurable_now']} |")
    o.append(f"| Blocked — no qualified instrument | {ms['blocked_pending_instrument']} |")
    o.append(f"| Blocked — resource missing | {ms['blocked_pending_resource']} |")
    o.append(f"| Usable as a hard routing constraint | {sum(1 for d in dims if d['routing_use']=='hard_constraint')} |")
    o.append(f"| Descriptive evidence only | {sum(1 for d in dims if d['routing_use']=='descriptive_only')} |")
    o.append(f"| Empirical results contained | **0** |\n")
    o.append("**Read that middle block plainly:** of 36 capabilities, "
             f"**{ms['measurable_now']} could be measured with what we have today**. "
             f"**{ms['blocked_pending_instrument']}** are waiting on a checker nobody has yet "
             f"proven trustworthy, and **{ms['blocked_pending_resource']}** are waiting on test "
             "material we do not hold. That is the real shape of the gap.\n")

    for fam, items in by_family.items():
        o.append(f"\n---\n\n## {FAMILY_TITLES.get(fam, fam)}\n")
        for d in items:
            o.append(f"### `{d['id']}` — {d['name_plain']}\n")
            o.append(f"{d['definition'].strip()}\n")
            o.append(f"- **Covers:** {d['inside'].strip()}")
            o.append(f"- **Does not cover:** {d['outside'].strip()}")
            o.append(f"- **Observation unit:** `{d['observation_unit']}` — {d['observation_span_detail'].strip()}")
            o.append(f"- **Applies to:** {', '.join(d['modalities'])}")
            o.append(f"- **Atomic probe:** {d['atomic_probe'].strip()}")
            reuse = d['compound_reuse']
            reuse_s = "every compound scenario" if reuse == ["ALL"] else ", ".join(f"`{r}`" for r in reuse)
            o.append(f"- **Reusable from:** {reuse_s}")
            sec = d.get('secondary_instrument')
            sec_s = f", corroborated by {INSTRUMENT_NAMES.get(sec, sec)}" if sec else ""
            o.append(f"- **Instrument:** {INSTRUMENT_NAMES.get(d['instrument_family'], d['instrument_family'])}{sec_s}")
            o.append(f"- **Human verifier:** {d['human_verifier'].strip() if d['human_verifier']!='none' else '*none*'}")
            o.append(f"- **External resource:** `{d['resource_requirement']}`")
            o.append(f"- **Result form:** `{d['result_form']}`")
            o.append(f"- **Routing use:** `{d['routing_use']}`")
            o.append(f"- **Status:** **{STATUS_LABEL[d['measurability_status']]}**")
            o.append(f"\n  **Difficulty ladder**\n")
            for lvl in d["difficulty_ladder"]:
                o.append(f"  {lvl['level']}. {lvl['observable']}")
            o.append(f"\n  **Failure vocabulary:** {d['failure_vocabulary'].strip()}")
            o.append(f"\n  **Held fixed for comparability:** {', '.join(f'`{c}`' for c in d['registry_conditions'])}")
            o.append(f"\n  **Note:** {d['measurability_note'].strip()}\n")

    o.append("\n---\n\n## Proposed changes — raised, not applied\n")
    o.append("The 36 capability ids remain exactly as the Controller froze them. "
             "These are proposals for review.\n")
    for pc in doc["proposed_changes"]:
        to = f" → {pc['to']}" if pc.get("to") else ""
        o.append(f"**{pc['ref']} · `{pc['type']}`{to} — {pc['subject']}**\n")
        o.append(f"{pc['detail'].strip()}\n")
    DOC.write_text("\n".join(o) + "\n")

    # ---------------- dependency matrix ----------------
    m = []
    m.append("# Eval V1 — Capability Dependency Matrix\n")
    m.append("> **GENERATED FILE — do not hand-edit.** Source: `capability-contract.yaml`.\n")
    m.append("This is the answer to one question: **what has to exist before each capability "
             "can actually be measured?** It is the shopping list behind the whole programme.\n")

    m.append("\n## Full matrix\n")
    m.append("| Capability | Unit | Instrument | Resource | Routing | Status |")
    m.append("|---|---|---|---|---|---|")
    for d in dims:
        m.append(f"| `{d['id']}` | `{d['observation_unit']}` | "
                 f"{INSTRUMENT_NAMES.get(d['instrument_family'], d['instrument_family'])} | "
                 f"`{d['resource_requirement']}` | `{d['routing_use']}` | "
                 f"{STATUS_LABEL[d['measurability_status']]} |")

    m.append("\n## Blockers, grouped by what would unblock them\n")
    inst = collections.defaultdict(list)
    for d in dims:
        if d["measurability_status"] == "blocked_pending_instrument":
            inst[INSTRUMENT_NAMES.get(d["instrument_family"], d["instrument_family"])].append(d["id"])
    m.append("### Waiting on an instrument nobody has qualified yet\n")
    m.append("| Instrument family | Capabilities it unblocks | Count |")
    m.append("|---|---|---:|")
    for k, v in sorted(inst.items(), key=lambda kv: -len(kv[1])):
        m.append(f"| {k} | {', '.join(f'`{x}`' for x in v)} | {len(v)} |")
    m.append("\n**Why this table is the priority list:** qualifying one instrument family "
             "unblocks every capability in its row at once. That is the cheapest possible "
             "ordering of the work.\n")

    res = [d["id"] for d in dims if d["measurability_status"] == "blocked_pending_resource"]
    m.append("### Waiting on test material we do not hold\n")
    m.append(f"{len(res)} capabilities: " + ", ".join(f"`{x}`" for x in res) + "\n")

    m.append("\n## Free riders — measurable on assets other dimensions already generate\n")
    free = [d["id"] for d in dims
            if d["resource_requirement"] == "no_external_resource"
            or d["compound_reuse"] == ["ALL"]]
    m.append("These cost **no additional generation at all**. They should be attached to every "
             "eligible asset by default; not doing so is wasted money.\n")
    for f in sorted(set(free)):
        m.append(f"- `{f}`")

    m.append("\n## Unit distribution\n")
    m.append("| Observation unit | Capabilities |\n|---|---:|")
    for k, v in collections.Counter(d["observation_unit"] for d in dims).most_common():
        m.append(f"| `{k}` | {v} |")
    m.append("\nA capability measured at `sequence`, `shot_pair` or `asset_set_over_time` "
             "**cannot** be scored from a single still image. Any item claiming to do so is a "
             "design defect, not a cheaper test.\n")
    MTX.write_text("\n".join(m) + "\n")
    print(f"wrote {DOC.relative_to(ROOT)} ({DOC.stat().st_size:,} bytes)")
    print(f"wrote {MTX.relative_to(ROOT)} ({MTX.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
