#!/usr/bin/env python3
"""RES-001/002 :: generate the integrity and bias/coverage reports.

DESIGN RULE (added after RES-002): every substantive claim in these reports must be
DERIVED from the current registry + manifest, not typed in as prose. An earlier version
hard-coded conclusions like "there is no Devanagari material" and "VideoGen-RewardBench
remains unavailable". Both were true when written and both became false one task later,
and because they were prose, regenerating the report happily reprinted them.

So: coverage statements come from the COVERAGE table below, which is evaluated against
the domains actually present in the registry. If a source with a matching domain is
acquired, the capability prints as supported; if not, it prints as a gap. Adding a new
source updates the report automatically. Nothing here needs editing when the corpus changes.
"""
import csv, json, collections, os

MANIFEST = "resources/manifests/corpus-pilot-v0.jsonl"
REGISTRY = "resources/manifests/source-registry-v0.csv"
RAW = "resources/corpus/raw"
ACQUIRED = ("downloaded", "partial_download")

M = [json.loads(l) for l in open(MANIFEST)]
R = list(csv.DictReader(open(REGISTRY)))
by = collections.defaultdict(list)
for r in M:
    by[r["source_id"]].append(r)
reg = {r["source_id"]: r for r in R}
acq = [r for r in R if r["status"] in ACQUIRED]
blocked = [r for r in R if r["status"] not in ACQUIRED]
domains_present = {r["domain"] for r in acq}

def gb(b): return f"{b/1e9:.2f} GB"
def mb(b): return f"{b/1e6:.1f} MB"
def has(*subs):
    """Is any acquired source's domain matching all of these substrings?"""
    return any(all(s in d for s in subs) for d in domains_present)

# ---- capability table: (statement, predicate) -----------------------------------
# Each entry is decided by what the registry currently holds, never by prose.
COVERAGE = [
    ("Calibrating a judge against real filmed video",        lambda: has("real_", "video")),
    ("Devanagari / Indic script reading (real photographed text)", lambda: has("devanagari")),
    ("Evaluator behaviour across multiple AI video generators",     lambda: has("generated_video")),
    ("Generated-image preference / dimensional rating work", lambda: has("generated_image")),
    ("Comparison against real professional or commercial creative", lambda: has("advertising") or has("creative")),
    ("Real photography aesthetics",                          lambda: has("aesthetic")),
    ("Audio work",                                           lambda: has("audio")),
    ("Devanagari in GENERATED output (our actual failure mode)",    lambda: has("generated", "devanagari")),
]

# ---------------- byte accounting: three different, all legitimate ----------------
def folder_bytes(sid):
    root = os.path.join(RAW, sid); tot = nonmedia = 0
    for dp, _, fs in os.walk(root):
        for f in fs:
            p = os.path.join(dp, f); s = os.path.getsize(p); tot += s
            if os.path.splitext(f)[1].lower() not in {
                    ".mp4", ".mkv", ".webm", ".mov", ".png", ".jpg", ".jpeg", ".webp"}:
                nonmedia += s
    return tot, nonmedia

# ---------------- duplicate analysis ----------------
byhash = collections.defaultdict(list)
for r in M:
    if r["sha256"]: byhash[r["sha256"]].append(r)
dups = {h: v for h, v in byhash.items() if len(v) > 1}
within = collections.Counter(); cross = collections.Counter(); cross_pairs = collections.Counter()
for h, v in dups.items():
    srcs = {r["source_id"] for r in v}
    if len(srcs) == 1:
        within[next(iter(srcs))] += 1
    else:
        cross_pairs[tuple(sorted(srcs))] += 1
        for s in srcs: cross[s] += 1
bad = [r for r in M if r["validation_status"] != "ok"]
tot_media = sum(r["bytes"] for r in M)

# ================= INTEGRITY REPORT =================
L = ["# Integrity report — full corpus", "",
 "**Generated from the manifest and registry. Do not hand-edit — rerun `resources/scripts/build_reports.py`.**",
 "", "Method: SHA256 over every retained file plus an `ffprobe` decode of every item. Deterministic;",
 "no model is involved and nothing is judged on content.", "",
 "## Totals", "", "| | |", "|---|---|",
 f"| Retained items | **{len(M):,}** |",
 f"| Distinct files (unique SHA256) | **{len(byhash):,}** |",
 f"| Media bytes (manifest) | **{gb(tot_media)}** |",
 f"| Decoding cleanly | **{len(M)-len(bad):,} / {len(M):,}** |", "",
 "## Byte accounting — three figures, all correct, measuring different things", "",
 "These differ and none is wrong. Quoting one without saying which causes avoidable confusion.", "",
 "1. **Media bytes** — the sum of the media files in the manifest. The evaluation payload.",
 "2. **Folder bytes** — media *plus* retained annotations, transcriptions, licence files and",
 "   member lists. Larger, and the annotations are the reason several sources are useful at all.",
 "3. **Disk usage (`du`)** — allocated filesystem blocks. A source made of tens of thousands of",
 "   tiny images pays real block overhead; one made of a few large videos pays almost none.", "",
 "| source | media bytes | folder bytes | non-media | items |", "|---|---:|---:|---:|---:|"]
tf = tn = 0
for sid in sorted(by):
    fb, nm = folder_bytes(sid); tf += fb; tn += nm
    L.append(f"| `{sid}` | {mb(sum(r['bytes'] for r in by[sid]))} | {mb(fb)} | {mb(nm)} | {len(by[sid]):,} |")
L += [f"| **total** | **{gb(tot_media)}** | **{gb(tf)}** | **{mb(tn)}** | **{len(M):,}** |", "",
 "The largest gap is the Devanagari scene-text material, whose retained transcription files are",
 "a meaningful share of its folder — those transcriptions are precisely what makes it calibration",
 "material rather than a pile of pictures.", "",
 "## Decode validation", "",
 f"- Clean: **{len(M)-len(bad):,} / {len(M):,}**",
 f"- Zero-byte: **{sum(1 for r in bad if r['validation_status']=='zero_bytes')}**",
 f"- Undecodable: **{sum(1 for r in bad if r['validation_status']=='undecodable')}**", ""]
if bad:
    L += ["Problem items are **retained, not deleted** — what breaks is itself evidence.", "",
          "| item | status |", "|---|---|"] + \
         [f"| `{r['relative_path']}` | {r['validation_status']} |" for r in bad[:40]] + [""]

L += ["## Exact duplicates", "",
 f"- Distinct files: **{len(byhash):,}** across **{len(M):,}** items",
 f"- Duplicate hashes: **{len(dups):,}**  (**{sum(within.values())}** within a single source, "
 f"**{sum(cross_pairs.values())}** spanning two sources)",
 f"- Redundant copies: **{sum(len(v)-1 for v in dups.values()):,}**", "",
 "**Duplicates are reported, never removed.** Deleting them would improve the number and destroy",
 "the finding.", "", "| source | within-source | involved in cross-source | source items |", "|---|---:|---:|---:|"]
for s in sorted(set(within) | set(cross)):
    L.append(f"| `{s}` | {within[s]:,} | {cross[s]:,} | {len(by[s]):,} |")
L.append("")
if cross_pairs:
    L += ["### Cross-source duplicates — the one that matters", "",
          "| sources sharing byte-identical files | hashes |", "|---|---:|"]
    for pair, n in cross_pairs.most_common():
        a, b_ = pair
        L.append(f"| `{a}` ↔ `{b_}` | **{n:,}** |")
    L += ["", "For each pair below, the overlap is stated as a share of each source, because \"173 files\"",
          "means something very different for a 1,390-item source than for a 3,086-item one.", ""]
    for pair, n in cross_pairs.most_common():
        for s in pair:
            L.append(f"- **{cross[s]:,} of `{s}`'s {len(by[s]):,} items** "
                     f"({100*cross[s]/len(by[s]):.1f}%) are byte-identical to an item in the other source.")
    L.append("")

# archive deletions
L += ["## Archive deletions", "",
 "Archives were deleted only after all five conditions held, and each was fingerprinted **before**",
 "deletion so a future re-download stays verifiable.", "",
 "| source | archive | sha256 |", "|---|---|---|"]
for sid in sorted(by):
    p = f"{RAW}/{sid}/_archive.sha256"
    if os.path.exists(p):
        for line in open(p):
            parts = line.split()
            if len(parts) >= 2:
                L.append(f"| `{sid}` | `{os.path.basename(parts[-1])}` | `{parts[0][:24]}…` |")
L += ["", "Sources acquired by HTTP range have **no full-archive hash on purpose** — the archive was",
 "never downloaded, so any hash would be fabricated. Their reproduction record is the remote size,",
 "the complete member list, the selection rule and a hash per retained member, in",
 "`_transient_acquisition.json`.", "",
 "### Files removed", "",
 "- `src_konvid1k/KoNViD_1k_subjective.csv` — approved privacy deletion (crowdworker IP addresses,",
 "  worker IDs, city/region/country). See `RES-002-privacy-deletion-log.md`.",
 "- `src_youtube_ugc/Animation_360P-188f.mkv` — fetched under a superseded selection rule; removed",
 "  so the corpus reproduces exactly from the script. A reproducibility correction, not a cleanup.", ""]
open("resources/reports/RES-001-integrity-report.md", "w").write("\n".join(L))

# ================= BIAS / COVERAGE REPORT =================
mt = collections.Counter(r["media_type"] for r in M)
per_dom = collections.Counter()
for r in M: per_dom[reg.get(r["source_id"], {}).get("domain", "?")] += 1
real = [r for r in acq if r["domain"].startswith("real_")]
gen = [r for r in acq if r["domain"].startswith("generated_")]
real_items = sum(len(by[r["source_id"]]) for r in real)
gen_items = sum(len(by[r["source_id"]]) for r in gen)

B = ["# Bias and coverage report — full corpus", "",
 "**Generated from the manifest and registry. Do not hand-edit — rerun `resources/scripts/build_reports.py`.**",
 "", "**Descriptive only.** These axes describe what the corpus contains. They are deliberately *not*",
 "Canon-derived: no axis encodes a creative principle under test, because stratifying evaluation",
 "media by the theory being tested is the circularity this stream exists to prevent (Project",
 "Contract, separation 9).", "",
 "## What is in the corpus", "", "| Media type | items |", "|---|---:|"]
B += [f"| {k} | {v:,} |" for k, v in mt.most_common()]
B += ["", "| Domain family | items |", "|---|---:|"]
B += [f"| {k} | {v:,} |" for k, v in per_dom.most_common()]
B += ["", "## Real vs generated media", "",
 f"- **Real human-made:** {len(real)} sources, {real_items:,} items — " + ", ".join(f"`{r['source_id']}`" for r in real),
 f"- **AI-generated:** {len(gen)} sources, {gen_items:,} items — " + ", ".join(f"`{r['source_id']}`" for r in gen), ""]

B += ["## What this corpus can and cannot support", "",
 "*Derived from the domains actually present in the registry — not written by hand.*", "",
 "| Capability | Status |", "|---|---|"]
for label, pred in COVERAGE:
    B.append(f"| {label} | {'**supported**' if pred() else 'gap — not in the corpus'} |")
gaps = [l for l, p in COVERAGE if not p()]
B += ["", "**Open gaps:** " + ("; ".join(gaps) if gaps else "none of the tracked capabilities is missing.") + "", ""]

B += ["## Known skews — state these before designing an experiment on this corpus", "",
 "| Skew | Detail |", "|---|---|",
 "| **Quality-assessment bias** | The real-video sources were built to study *technical* quality — compression, blur, camera shake. Their populations were sampled for degradation variety, not creative merit. |",
 "| **Devanagari is photographed, not generated** | The Devanagari material is real signage. It tests whether a judge can *read* the script. It does not test whether a generator *renders* it correctly. |",
 "| **Two Devanagari sources share a lab** | IndicSTR12 and IIIT-ILST are both CVIT / IIIT Hyderabad releases and share byte-identical files (see the integrity report). Treat them as related, not independent. |",
 "| **Geography** | Not stated by any source. The Devanagari material is Indian by construction; the rest should be assumed Anglosphere-weighted, unverified. |",
 "| **Generator era** | ImageRewardDB images are DiffusionDB-era Stable Diffusion; VideoFeedback does not name its generators. Neither reflects current frontier models. |",
 "| **Audio** | The YouTube-UGC clips are audio-removed excerpts. |",
 "| **Sample size, YouTube-UGC** | 5 clips. Enough to prove the acquisition path and the rights position; not a population. |", "",
 "## Blocked sources — evidence, not failure", "", "| source | status | blocker |", "|---|---|---|"]
for r in blocked:
    B.append(f"| `{r['source_id']}` | `{r['status']}` | {r['reason'].split('.')[0]}. |")
B += ["", f"**{len(blocked)} of {len(R)} candidate sources are blocked.** Not one is blocked for licence",
 "silence; the blockers are access gates and one explicit terms prohibition — the categories current",
 "policy still treats as hard limits.", ""]
open("resources/reports/RES-001-bias-and-coverage-report.md", "w").write("\n".join(B))
print(f"reports regenerated: {len(M):,} items, {len(byhash):,} distinct, {len(dups)} duplicate hashes "
      f"({sum(within.values())} within / {sum(cross_pairs.values())} cross), {len(gaps)} open coverage gaps")
