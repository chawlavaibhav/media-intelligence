# BOOTSTRAP — load current authority once per session

Run this for the FIRST job of a session, before any intake. Read; do not summarise to the user.
`$REPO` = the root of this checkout. `$UPWORK` = the commercial repo,
`~/Vaibhav_Personal_Projects/upwork-project` (a sibling of the `media-intelligence*` directories).

## 1. Pin HEAD and prove the protected trees are untouched

```bash
git rev-parse --short HEAD && git status --short -- canon eval/registry eval/capability-map coordination
```

Record the sha. Any uncommitted change under those four paths → stop and report before doing
production work (the operator never mutates them; if they are dirty, someone else is mid-task).

## 2. Read, in this order

| Read | Why (what you take from it) |
|---|---|
| `PROJECT-MEMORY.md` §1, §2, §5, §7 | the authority map; what is zero vs no longer zero; the traps |
| `coordination/CONTROL-STATE.md` §2, §3, §5, §6, §8 | what is authorised, what is blocked, spend of record, the runtime's dispatch state |
| `canon/CANON-SHAPE-v1.md` §4–§5 | how Canon is consumed: deterministic pack lookup → gates → templates |
| `canon/packs/pack-triggers-v0.yaml` | which NR fields fire which pack (table lookup, never judgment) |
| the two compiled packs' decision ids + CHECK lines (command below) | the check lines you render by id |
| routing table (command below) | the 61 cells: status, production use, accepts, pinned price, surface, pool, text mechanism |
| `runtime/ALPHA-1.md` §"What exists" / §"Does not exist" | what the runtime can do dry; that live dispatch is NOT wired in `runtime/` |
| `production-learning/README.md` + every `cases/*/README.md`, `PROMOTION-QUEUE.yaml`, `ACCEPTED-TEMPLATE.yaml`, `ROUTE-OBSERVATIONS.yaml` | accepted patterns, promoted gates, candidate patterns, directional model notes |
| `$UPWORK/PROFILE.md` — `## Status` line, the LIVE title + overview, `### v2 Project Catalog packages`, `### v2 Portfolio plan`, `### Delivery checklist` | what is sold, package contents, sizes, the promise, the QA the profile commits to |
| `$UPWORK/LOG.md` — last entry only | what is live on Upwork today |

Pack decisions and check lines (USD 0):

```bash
python3 -c '
import yaml
for p in ["product_appearance","composition_and_attention"]:
    d=yaml.safe_load(open(f"canon/compilation/PACK-{p}-v0.yaml"))
    print("==", p, "status", d["status"])
    for x in d["decisions"]:
        print(x["decision_id"], "|", x["question"]); print("   CHECK:", x["check"], "  [", x["check_id"], "]")
'
```

Routing table (USD 0). Prices shown are the map's pins WITH the roster's billing unit (per_image,
per_second, per_1000_characters, per_clip …) — a per-second route costs unit × duration. The
runtime re-prices from the roster at decision time (workflow §7); the map's number is history:

```bash
python3 -c '
import sys, yaml; sys.path.insert(0, ".")
from runtime.route.cli import build_router
t=yaml.safe_load(open("eval/capability-map/TAINT-REGISTER-v1.yaml"))
m=yaml.safe_load(open("eval/capability-map/ROUTING-EVIDENCE-MAP-v0.yaml"))
pb=build_router()[0].prices
def unit(rk):
    try:
        e=pb.surfaces.get(rk); return (pb.roster.record(e.roster_key,e.roster_variant).get("regular_price") or {}).get("unit")
    except Exception: return "?"
px={(q,c):(v.get("unit_price_usd_pinned"),v.get("surface"),v.get("billing_pool"),v.get("text_mechanism"),v.get("route_key"))
    for q,qd in m["questions"].items() for c,v in qd["cells"].items()}
for r in m["routing_rules"]: print(r.get("id"), r.get("status") or "", "|", str(r.get("rule"))[:200])
print()
for c in sorted(t["cells"], key=lambda c:(c["question"],c["map_cell_name"])):
    p=px.get((c["question"],c["map_cell_name"]),("?","?","?","?","?"))
    q,n,st,use=c["question"],c["map_cell_name"],c["evidence_status"],str(c["production_use_allowed"])
    acc=str(c["map_reported_accepts"])+"/"+str(c["map_reported_trials"])
    print(q.ljust(9),n.ljust(44),st.ljust(17),("use="+use).ljust(16),("acc="+acc).ljust(8),"price",p[0],unit(p[4]),"surf",p[1],"pool",p[2],"txt",p[3])
print("summary:", t["summary"]["by_evidence_status"], t["summary"]["by_production_use_allowed"])
'
```

Production-learning count and commercial version:

```bash
ls production-learning/cases | wc -l; ls production-learning/cases
grep -m1 "^_Last updated" ~/Vaibhav_Personal_Projects/upwork-project/PROFILE.md | cut -c1-200
```

## 3. Spend authority

`known` only if the user has stated a job-specific cap **in this session** (amount, currency, what
it covers). Anything else — prior pilot packages, `CONTROL-STATE` spend of record, an
`authorization.local.yaml` on disk, a provider balance — is `absent`. Never infer money.

## 4. Print exactly this, nothing more

```
MEDIA AGENCY READY
main: <sha>
Canon packs available: <compiled+accepted pack ids found in §2>
production-learning cases: <count> (<ids>)
commercial profile: ../upwork-project/PROFILE.md — <its "Last updated" line, shortened>
spend authority for this job: <known: <cap> | absent>
```

Then wait for, or proceed with, the job.

## Refresh — before every later job in the same session

```bash
git rev-parse --short HEAD
```

If unchanged, keep the loaded context. If changed, list what moved and re-read only that:

```bash
git diff --stat <old-sha>..HEAD -- PROJECT-MEMORY.md coordination canon/CANON-SHAPE-v1.md canon/packs canon/compilation eval/capability-map runtime production-learning
```

Also re-check `$UPWORK/PROFILE.md`'s `_Last updated` line before any new **portfolio** batch; if it
changed, re-read the positioning sections — positioning drives the batch.

Material changes = any of: a new Controller decision, a CONTROL-STATE refresh, a routing-map or
taint-register regeneration, a new or changed compiled pack, a new production-learning case, a
runtime gate change, a changed Upwork profile. Cosmetic history edits are not material.
