# ADDENDUM C — Judge-reliability packet (experiment E6)

Purpose: measure whether the single human judge is a usable instrument before any verdict-based experiment is run. Three judges (the owner + two people who did not make or brief any of the pieces), blind order, same 15 artefacts, same scoring sheet. Cost: about two hours of each judge's time, USD 0. Output: agreement on accept/reject (Fleiss' κ) and on the named defect class.

## 1. The fifteen artefacts

All are committed or on disk; extract with `git show <ref>:<path> > file` for the git ones. Do not show the judges the case files, verdicts, or this list's "known verdict" column.

| # | Artefact | Where | sha256 (from Part 6 §0 / council 12) | Known verdict (hidden from judges) |
|---|---|---|---|---|
| 1 | Upwork intro V1 | `f6ca66f:pilots/upwork-intro-video-2026-09-14/assembly/v1/upwork-intro-first-pass.mp4` | `c073e9ab…` | specific repair |
| 2 | Upwork intro V2 | `…/assembly/v2/upwork-intro-v2.mp4` | `bdd4566e…` | rebuild direction |
| 3 | Upwork intro V3 | `…/v3/assembly/v3/upwork-intro-v3.mp4` | `ea81264d…` | reject |
| 4 | Upwork intro V4 | `…/v4/assembly/v4/upwork-intro-v4.mp4` | `09ed32c5…` | specific repair |
| 5 | Upwork intro V4.1 | `…/v4/assembly/v4.1/upwork-intro-v4.1.mp4` | `d1a5edf8…` | accept |
| 6 | Cumin V1 9:16 | `de1f978:agency/jobs/AGY-2026-09-15-CUMINCO-CHOPSTICKS-001/gen/final/cuminco-chopsticks-9x16.mp4` | `097e428e…` | reject |
| 7 | Cumin V2 9:16 | `…/gen/final/v2/cuminco-chopsticks-9x16.mp4` | `adaeaa37…` | reject |
| 8 | Cumin V3 9:16 | `…/gen/final/v3/cuminco-chopsticks-9x16.mp4` | `85d7410e…` | reject |
| 9 | Aarohi offer 4:5 | UPM `tile-01-aarohi-skin/aarohi-offer-cta-4x5.png` | `3b1fc474…` | accept |
| 10 | Kora hook 1:1 | UPM `tile-03-kora-threads/kora-hook-1-1x1.png` | `d6a09e2e…` | accept (after repair) |
| 11 | IronLeaf offer 4:5 | UPM `tile-04-ironleaf-nutrition/ironleaf-offer-4x5.png` | `333ebeb6…` | accept |
| 12 | Dhaba 47 Hindi 1:1 | UPM `tile-05-dhaba-47-hindi/dhaba47-hindi-1x1.png` | `69c230cd…` | accept |
| 13 | GyaanBox offer 1:1 | UPM `tile-06-gyaanbox-edtech/gyaanbox-offer-1x1.png` | `c3a71b09…` | accept |
| 14 | Brewa kettle scene 16:9 | UPM `tile-03-brewa-kettle/brewa-scene-1-kitchen-16x9.png` | `1e9f7281…` | accept (not an ad, by the owner's rubric) |
| 15 | Nivaas story 9:16 | UPM `_rejected/tile-07-nivaas-homes-REJECTED-2026-09-15/nivaas-story-9x16-15s.mp4` | `d501c1fb…` | reject |

## 2. Blind order

Rename the files `A01.mp4 … A15.png` using a seeded shuffle so that no judge sees version numbers or brand folders:

```python
import random
ids = list(range(1, 16)); random.seed(20260920); random.shuffle(ids)
print(ids)   # position -> artefact number; keep this mapping in a sealed file until scoring is done
```

Show each judge the same order. For videos, judges watch once with sound, once muted. For statics, judges view at phone size first (1080 px wide on a phone or a window scaled to 390 px), then full size.

## 3. Scoring sheet (one row per artefact per judge)

| Field | Values |
|---|---|
| Verdict | ACCEPT / SPECIFIC REPAIR / REJECT |
| Primary defect class (one) | none · not-an-ad (no proposition/hero/ask) · opening weak · product not central · text over subject · text unreadable/clipped · voice unnatural · voice/timing (overlap, hole, mismatch) · pacing · continuity/identity · assembly/crop/format · other (write one word) |
| One sentence | why |

Judges do not confer until all 15 rows are in.

## 4. Scoring

```python
# Fleiss' kappa on the 3-way verdict, and raw agreement on defect class
import itertools, collections
verdicts = {}  # artefact -> [v_judge1, v_judge2, v_judge3]
def fleiss(table, cats):
    N = len(table); n = len(next(iter(table.values())))
    P = []; pj = collections.Counter()
    for rows in table.values():
        c = collections.Counter(rows); pj.update(c)
        P.append((sum(v*v for v in c.values()) - n) / (n*(n-1)))
    Pbar = sum(P)/N; Pe = sum((pj[k]/(N*n))**2 for k in cats)
    return (Pbar - Pe) / (1 - Pe)
```

Reading rule (from Part 14 NODE 0): κ ≥ 0.6 → the owner may serve as one reviewer in later experiments; 0.4–0.6 → two non-author reviewers by unanimity, the owner advises; κ < 0.4 → stop all outcome experiments, write the rejection checklist with the three judges first, re-run on the checklist items.

Also report: agreement on the primary defect class (fraction of artefacts where ≥ 2 of 3 judges name the same class), and every artefact where the owner's blind verdict differs from his recorded verdict in the case files (column 5). That last number is the direct test of the concern in Part 13 U1.

## 5. What this does not test

Whether a paying customer would accept anything. All fifteen pieces were judged by the owner; the two extra judges are proxies for a second opinion, not for the market.
