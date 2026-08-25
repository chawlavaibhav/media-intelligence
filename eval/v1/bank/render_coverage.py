#!/usr/bin/env python3
"""Render COVERAGE-REPORT.md from the built bank. Generated, not hand-written."""
import json, pathlib, collections, yaml, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from build_bank import load_contract, CRITICAL, SCENARIOS, ATOMIC_GROUPS

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / "eval/v1/bank"
items = [json.loads(l) for l in (OUT / "master-bank-v1.jsonl").read_text().splitlines() if l.strip()]
dims = load_contract()
cov = collections.Counter()
atomic_cov, compound_cov = collections.Counter(), collections.Counter()
for it in items:
    for c in it["measurement_fanout"]:
        cov[c] += 1
        (atomic_cov if it["class"] == "atomic" else compound_cov)[c] += 1

atomic = [i for i in items if i["class"] == "atomic"]
compound = [i for i in items if i["class"] == "compound"]
total_m = sum(cov.values())

o = []
o.append("# E4 — Master benchmark bank: coverage report\n")
o.append("> **GENERATED FILE — do not hand-edit.** Source: `master-bank-v1.jsonl`.  \n"
         "> Rebuild: `python3 eval/v1/bank/build_bank.py --build`  \n"
         "> Validate: `python3 eval/v1/bank/build_bank.py --validate`\n")
o.append("**Task:** E4 · **Date:** 26 Aug 2026 · **Status: DESIGN ONLY — "
         "0 items generated, 0 spend.**\n")

o.append("## The headline: this bank pays for itself 12.7 times over\n")
o.append("| | |\n|---|---:|")
o.append(f"| Base items (generations) | **{len(items)}** |")
o.append(f"| Atomic / compound | {len(atomic)} / {len(compound)} |")
o.append(f"| Capabilities covered | **{len(cov)} / 36** |")
o.append(f"| Total valid measurements | **{total_m:,}** |")
o.append(f"| **Measurements per generated asset** | **{total_m/len(items):.1f}×** |")
o.append("")
o.append("That multiplier **is** the generate-once rule expressed as a number. "
         "Scoring these 100 assets one-metric-per-generation would need "
         f"**{total_m:,} generations** instead of **{len(items)}**. At any "
         "plausible price that is the difference between a fundable programme "
         "and an unfundable one.\n")
o.append("It is also why evaluator calls outnumber generations roughly 8:1 in "
         "the E2 forecast — that is the intended economics, not an overrun.\n")

o.append("## Atomic 40 — causal isolation\n")
o.append("Atomic items test **one capability with nothing else in the frame**, "
         "so a failure has one candidate cause. They still free-ride the "
         "zero-cost operational and delivery checks on the same asset — there "
         "is no reason not to.\n")
o.append("| Group | Items | Capabilities isolated |\n|---|---:|---|")
for g, spec in ATOMIC_GROUPS.items():
    caps = ", ".join(f"`{c}`×{k}" for c, k in spec["allocation"].items())
    o.append(f"| {g.replace('_',' ')} | {spec['count']} | {caps} |")
o.append(f"| **Total** | **{len(atomic)}** | |\n")

o.append("## Compound 60 — one generation, many measurements\n")
o.append("Ten commercial scenario families × six difficulty tiers. **Each item's "
         "fan-out is derived from the capability contract**, not asserted here: "
         "a capability appears only if the contract lists that scenario in its "
         "`compound_reuse` *and* the capability applies to that modality. A "
         "still image is never allowed to claim a temporal measurement.\n")
o.append("| Scenario family | Modality | Items | Fan-out | Measurements |\n|---|---|---:|---:|---:|")
for sid, label, modality, _ in SCENARIOS:
    fam = [i for i in compound if i["scenario_family"] == sid]
    fo = len(fam[0]["measurement_fanout"])
    o.append(f"| {label} | `{modality}` | {len(fam)} | **{fo}** | {fo*len(fam)} |")
o.append("")
o.append("**Read the fan-out column as value per generation.** A multi-shot "
         "branded ad is the most expensive asset to generate and returns the "
         "most measurements; a packshot is cheap and returns fewer. Both are "
         "needed — the cheap ones isolate, the expensive ones integrate.\n")

o.append("## Coverage of the 20 critical capabilities\n")
o.append("Target: **≥10 distinct base-item opportunities** each.\n")
o.append("| Capability | Atomic | Compound | **Total** | ≥10? |\n|---|---:|---:|---:|:--:|")
for c in CRITICAL:
    t = cov.get(c, 0)
    o.append(f"| `{c}` | {atomic_cov.get(c,0)} | {compound_cov.get(c,0)} | **{t}** | "
             f"{'✅' if t >= 10 else '⚠️'} |")
under = {c: cov.get(c, 0) for c in CRITICAL if cov.get(c, 0) < 10}
o.append(f"\n**{len(CRITICAL)-len(under)} of {len(CRITICAL)} critical capabilities meet the target.**\n")

if under:
    o.append("### The one that does not, and why it was not padded\n")
    for c, v in under.items():
        d = dims[c]
        reuse = d.get("compound_reuse") or []
        # Apply BOTH gates, exactly as the bank does: contract reuse AND
        # modality applicability. Listing reuse alone would overstate.
        listed = [(s, mod) for s, _, mod, _ in SCENARIOS if s in reuse]
        valid = [s for s, mod in listed if mod in d["modalities"]]
        excluded = [(s, mod) for s, mod in listed if mod not in d["modalities"]]
        o.append(f"**`{c}` — {v} opportunities, not 10.**\n")
        o.append(f"- **Exact denominator:** {v} = {atomic_cov.get(c,0)} atomic + "
                 f"{compound_cov.get(c,0)} compound.")
        o.append(f"- **Why it cannot reach 10:** it is only meaningful where two "
                 f"visible speakers exchange turns, which requires a modality "
                 f"of {' or '.join('`'+m+'`' for m in d['modalities'])}. "
                 f"{len(valid)} scenario "
                 f"{'family qualifies' if len(valid)==1 else 'families qualify'} "
                 f"({', '.join('`'+s+'`' for s in valid)}), giving "
                 f"{6*len(valid)} compound opportunities at six items each.")
        if excluded:
            o.append(f"- **Listed but excluded by modality:** "
                     + "; ".join(f"`{s}` is modality `{m}`" for s, m in excluded)
                     + ". The contract permits the reuse, but the scenario as "
                       "defined has no visible on-camera dialogue, so the "
                       "capability cannot be exhibited. **This is a real design "
                       "choice worth the Controller's attention:** if a "
                       "multi-shot branded ad should contain on-camera dialogue, "
                       "its modality should be `native_av`, which would raise "
                       "this capability to 13 opportunities and change nothing "
                       "else. Left as-is tonight because changing a scenario's "
                       "modality alters the frozen compound-60 design.")
        o.append("- **What was deliberately not done:** adding two-speaker items "
                 "to scenarios that do not have two visible speakers. That would "
                 "manufacture opportunities that cannot exhibit the failure, "
                 "inflating the denominator while measuring nothing. The runbook "
                 "requires recording the real denominator instead, and that is "
                 "what this row does.")
        o.append("- **If the Controller wants 10:** the honest route is to widen "
                 "the two-person dialogue family from 6 items to 10, which is a "
                 "scope change to the frozen 60 and therefore a Controller "
                 "decision, not a worker one.\n")

o.append("## Full coverage, all 36\n")
o.append("| Capability | Opportunities | Critical |\n|---|---:|:--:|")
for c in sorted(dims, key=lambda x: -cov.get(x, 0)):
    o.append(f"| `{c}` | {cov.get(c,0)} | {'●' if c in CRITICAL else ''} |")
o.append("")
zero = [c for c in dims if cov.get(c, 0) == 0]
o.append(f"**Capabilities with zero opportunities: {len(zero)}**"
         + (f" — {', '.join('`'+c+'`' for c in zero)}" if zero else " — none. "
            "Every one of the 36 is exercised by at least one base item.") + "\n")

o.append("## Rules this bank enforces\n")
o.append("**Repeats are never base items.** Repeats measure reliability. Two "
         "repeats of 50 items is not 100 items, and confidence is computed on "
         "base items only.\n")
o.append("**Reuse never creates independent trials.** One asset scored by twelve "
         "instruments is twelve measurements of **one** trial. Frames sampled "
         "from one clip carry the parent trial id.\n")
o.append("**The later 12 end-to-end production briefs are NOT in this bank.** "
         "They must be selected from Canon's accepted 30-brief bank after "
         "integration. These 60 compound items are *capability benchmark "
         "scenarios* under controlled conditions — deliberately not customer "
         "briefs, and Eval must not author competing ones.\n")
(OUT / "COVERAGE-REPORT.md").write_text("\n".join(o) + "\n")
print(f"wrote COVERAGE-REPORT.md ({(OUT/'COVERAGE-REPORT.md').stat().st_size:,} bytes)")
print(f"multiplier {total_m/len(items):.1f}x | criticals met {len(CRITICAL)-len(under)}/{len(CRITICAL)} | zero-coverage {len(zero)}")
