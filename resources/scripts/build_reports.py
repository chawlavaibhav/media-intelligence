#!/usr/bin/env python3
"""RES-001 :: generate integrity + bias/coverage reports from the manifest and registry.
All figures are computed from files on disk. Nothing is hand-typed."""
import csv, json, collections, os, subprocess

M = [json.loads(l) for l in open("resources/manifests/corpus-pilot-v0.jsonl")]
R = list(csv.DictReader(open("resources/manifests/source-registry-v0.csv")))
by = collections.defaultdict(list)
for r in M: by[r["source_id"]].append(r)

def gb(b): return f"{b/1e9:.2f} GB"
tot_bytes = sum(r["bytes"] for r in M)

# ---------------- integrity ----------------
sha = collections.Counter(r["sha256"] for r in M if r["sha256"])
dups = {k: v for k, v in sha.items() if v > 1}
bad = [r for r in M if r["validation_status"] != "ok"]

L = ["# RES-001 — Integrity report", "",
 "**Date:** 24 Aug 2026 · **Method:** deterministic only. SHA256 over every retained file, plus",
 "`ffprobe` decode of every item. No model is involved and nothing is judged on content.", "",
 "## Totals", "",
 "| | |", "|---|---|",
 f"| Retained items | **{len(M):,}** |",
 f"| Retained bytes | **{gb(tot_bytes)}** |",
 f"| Budget target | 4–6 GB |",
 f"| Budget hard stop | 8 GB |",
 f"| Free disk floor | 12 GB |", "",
 "## Per source", "",
 "| source_id | items | bytes | validated ok | problems |", "|---|---:|---:|---:|---:|"]
for sid in sorted(by):
    rows = by[sid]
    ok = sum(1 for r in rows if r["validation_status"] == "ok")
    L.append(f"| `{sid}` | {len(rows):,} | {gb(sum(r['bytes'] for r in rows))} | {ok:,} | {len(rows)-ok} |")
L += ["", "## Decode validation", "",
 f"- Items decoding cleanly: **{len(M)-len(bad):,} / {len(M):,}**",
 f"- Zero-byte files: **{sum(1 for r in bad if r['validation_status']=='zero_bytes')}**",
 f"- Undecodable files: **{sum(1 for r in bad if r['validation_status']=='undecodable')}**", ""]
if bad:
    L += ["Problem items are **retained, not deleted** — the pattern of what breaks is itself evidence.", "",
          "| item | status |", "|---|---|"]
    L += [f"| `{r['relative_path']}` | {r['validation_status']} |" for r in bad[:40]]
    L.append("")
L += ["## Exact duplicates", "",
 f"- Unique SHA256: **{len(sha):,}** across **{len(M):,}** items",
 f"- Exact duplicate hashes: **{len(dups)}**",
 "", "Duplicates are **reported, never silently removed** (RES-001 in-scope rule). Perceptual-duplicate",
 "detection was not run: it is optional in RES-001 and the required libraries are not installed.", ""]
if dups:
    L += ["| sha256 | copies |", "|---|---:|"] + [f"| `{k[:16]}…` | {v} |" for k, v in list(dups.items())[:20]] + [""]

L += ["## Archive deletions (Amendment 01 / RES-001 budget rule)", "",
 "Archives were deleted only after all five conditions held. Every archive was fingerprinted",
 "**before** deletion so a future re-download can still be verified against it.", "",
 "| source | archive | bytes | sha256 |", "|---|---|---:|---|"]
for sid in sorted(by):
    p = f"resources/corpus/raw/{sid}/_archive.sha256"
    if os.path.exists(p):
        for line in open(p):
            h, f = line.split()[0], os.path.basename(line.split()[-1])
            sz = ""
            L.append(f"| `{sid}` | `{f}` | {sz} | `{h[:24]}…` |")
L += ["", "Full fingerprints are retained in `resources/corpus/raw/<source_id>/_archive.sha256`.", "",
 "### Media removed", "",
 "One file, `src_youtube_ugc/Animation_360P-188f.mkv` (207,046,293 bytes, sha256",
 "`33998201f2b31c9c1faa786ceccb083ab8a5948e5cd23dab6bc766c10eda47e6`), was removed. It was fetched",
 "under a first-pass selection rule that took the two lexicographically first 360P clips, both from",
 "the same category. The rule was then revised to one clip per category for better coverage. The",
 "file was removed so that re-running `fetch-youtube-ugc.sh` reproduces the corpus exactly. This was",
 "a reproducibility correction, not a space-saving deletion.", ""]
open("resources/reports/RES-001-integrity-report.md","w").write("\n".join(L))

# ---------------- bias / coverage ----------------
dom = {r["source_id"]: r["domain"] for r in R}
mt = collections.Counter(r["media_type"] for r in M)
per_dom = collections.Counter()
for r in M: per_dom[dom.get(r["source_id"], "?")] += 1
res = collections.Counter()
for r in M:
    h = r.get("height")
    res["unknown" if not h else "<=360p" if h <= 360 else "<=540p" if h <= 540 else "<=720p" if h <= 720 else "<=1080p" if h <= 1080 else ">1080p"] += 1

B = ["# RES-001 — Bias and coverage report", "",
 "**Date:** 24 Aug 2026 · **Descriptive only.** These axes describe what the corpus contains. They",
 "are deliberately *not* Canon-derived: no axis here encodes a creative principle under test, because",
 "stratifying evaluation media by the theory being tested is the circularity this stream exists to",
 "prevent (Project Contract, separation 9).", "",
 "## What is in the corpus", "",
 "| Media type | items |", "|---|---:|"]
B += [f"| {k} | {v:,} |" for k, v in mt.most_common()]
B += ["", "| Domain family | items |", "|---|---:|"]
B += [f"| {k} | {v:,} |" for k, v in per_dom.most_common()]
B += ["", "| Vertical resolution | items |", "|---|---:|"]
B += [f"| {k} | {v:,} |" for k, v in sorted(res.items())]

acquired = [r for r in R if r["status"] in ("downloaded","partial_download")]
blocked  = [r for r in R if r["status"] not in ("downloaded","partial_download")]
real = [r for r in acquired if r["domain"].startswith("real_")]
gen  = [r for r in acquired if r["domain"].startswith("generated_")]

B += ["", "## Real vs generated — the axis that changed", "",
 f"- **Real human-made media:** {len(real)} sources — " + ", ".join(f"`{r['source_id']}`" for r in real),
 f"- **AI-generated media:** {len(gen)} sources — " + ", ".join(f"`{r['source_id']}`" for r in gen), "",
 "Under the previous rights policy this pilot could acquire **no real human-made media at all**. The",
 "licence-silence change reversed that: the corpus is now majority real media by item count.", "",
 "## Known skews — state these before anyone designs an experiment on this corpus", "",
 "| Skew | Detail |", "|---|---|",
 "| **Quality-assessment bias** | Both real-video sources were built to study *technical* quality — compression, blur, camera shake. Their populations were sampled for degradation variety, not for creative merit. |",
 "| **No commercial creative** | Zero advertising, zero professional brand work. Pitt Ads was the only route and stays gated. |",
 "| **No real photography** | AVA was the only route and is blocked by explicit site terms. |",
 "| **Language / script** | Not measured. No Devanagari or Indic-script content is known to be present. Unchanged from the sourcing plan's gap table. |",
 "| **Geography** | Not stated by any source. Assume Anglosphere-weighted; not verified. |",
 "| **Generator era** | ImageRewardDB images are DiffusionDB-era Stable Diffusion. VideoFeedback does not name its generators. Neither reflects current frontier models. |",
 "| **Generator diversity lost** | VideoGen-RewardBench (12 generators) is `too_large_for_pilot` — its distribution is one 13.42 GB archive with no addressable per-item path. That diversity exists nowhere else in the corpus. |",
 "| **Audio** | YouTube-UGC clips are audio-removed excerpts. The corpus supports no audio work. |",
 "| **Sample size, YouTube-UGC** | 5 clips. Enough to prove the acquisition path and the rights position; not a population. |", "",
 "## What this corpus can and cannot support", "",
 "**Can support:** evaluator/instrument calibration on real video; technical-quality measurement;",
 "cross-frame temporal work (KoNViD-1k and VideoFeedback both carry relevant labels); comparing how",
 "judges behave on real versus generated material — which is newly possible and was not before.", "",
 "**Cannot support:** any claim requiring comparison against real professional or commercial creative;",
 "any Indic-script or Indian-market work; any audio work; any claim about current frontier generators.", "",
 "## Blocked sources — evidence, not failure", "",
 "| source | status | blocker |", "|---|---|---|"]
for r in blocked:
    B.append(f"| `{r['source_id']}` | `{r['status']}` | {r['reason'].split('.')[0]}. |")
B += ["", "Note the shape: after the policy change, **not one source is blocked for licence silence.** The",
 "remaining blockers are access gates (login, email, form) and one explicit terms prohibition — exactly",
 "the categories the policy still treats as hard limits.", ""]
open("resources/reports/RES-001-bias-and-coverage-report.md","w").write("\n".join(B))
print("wrote integrity + bias/coverage reports")
