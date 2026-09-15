# Media Agency Operator — how to run it

**What it is.** Two project Claude Code skills that turn any session in a dedicated worktree into a
persistent media *production* operator for commercial work (Upwork orders, portfolio tiles, spec
creatives): `/media-agency` produces; `/media-agency-sync` feeds what was learned back into
`main` by PR. Authority is always read from the current repository files at the start of each job —
the skills carry procedure, not knowledge, so they do not go stale when Canon, the routing map,
the runtime or the Upwork profile move.

Files: `.claude/skills/media-agency/{SKILL.md, BOOTSTRAP.md, PRODUCTION-WORKFLOW.md,
QA-CHECKLIST.md, JOB-TEMPLATE.yaml}` and `.claude/skills/media-agency-sync/SKILL.md`.

## 1. Launch the dedicated session

One worktree, one long-lived session, many job branches.

```bash
cd ~/Vaibhav_Personal_Projects/media-intelligence
git fetch origin main
git worktree add ../media-intelligence-worktrees/agency origin/main
cd ../media-intelligence-worktrees/agency
```

Create the local-only instruction file (git-ignored; not committed) so the session knows its role:

```bash
cat > CLAUDE.local.md <<'EOF'
You are the dedicated Media Agency Operator for this worktree.
For any request involving creating/editing images, videos, ads, posters, portfolio creatives or
Upwork media, invoke /media-agency before doing production work. Current repository authority
overrides memory. Never mutate Canon, Registry or Controller state as an incidental consequence
of production.
EOF
```

Start `claude` in that directory. Provider keys are read by name from the environment
(`source ~/.mi-keys` before any paid job); nothing in the repo or the skills holds a secret.

## 2. Submit a job

Type `/media-agency` followed by the brief (paste the client's message, attach or path the
product photo), and state the spend cap for this job if you are authorising money:

```
/media-agency
Client brief: <paste>
Attachments: <paths>
Spend cap for this job: USD 6 (fal cash + Vertex credits), 0 retries, approver Vaibhav
```

Without a stated cap the operator plans at USD 0 and stops before generation. The first job in a
session prints the `MEDIA AGENCY READY` block (main sha, packs available, learning cases, commercial
profile version, spend authority) and then the start-of-job summary: concept, routes, expected spend,
TTAO clock started. It asks a question only when a missing value could invalidate the output.

Per job the operator: cuts `work/agency-job-<id>` from `origin/main`; opens
`agency/jobs/<id>/JOB.yaml` with `production_base_sha` and the clock; runs intake → Normalized
Request → template/learning check → deterministic Canon pack lookup → creative blueprint →
production plan → evidence-aware routing → pre-dispatch gates → (paid) generation under the cap
with one ledger line per attempt → code composition → post-draw QA (frames for video) → bounded
repair → your **ACCEPT / SPECIFIC REPAIR / REJECT**.

Only you accept. Delivery to a client is a separate, human step (C-8).

## 3. Refresh current state

Automatic. At the start of every new job the operator runs `git fetch origin main`, compares the
sha with the previous job's `production_base_sha`, re-reads only the authority that changed
(`BOOTSTRAP.md` §Refresh), and cuts the new job branch from the new base. The base of a running
job never changes. To force a refresh mid-session, finish or archive the open job (commit + push
its branch) and start the next.

When the Upwork profile (`../upwork-project/PROFILE.md`) changes, the operator re-reads the
positioning before any new portfolio batch.

## 4. How accepted learning enters the system — the closed loop

```
MAIN
 → MEDIA AGENCY            (/media-agency; job branch cut from origin/main; base sha recorded)
 → REAL PRODUCTION         (paid attempts under a job cap; one ledger line each)
 → HUMAN ACCEPTANCE        (ACCEPT / SPECIFIC REPAIR / REJECT; only a person accepts)
 → PRODUCTION LEARNING     (LEARNING-PACKET.yaml on the job branch; learning_status: pending_sync; branch pushed)
 → /media-agency-sync      (new integration branch from origin/main; packets distilled into
                            production-learning/cases/<CASE>/, validated by check_case.py
                            --source-ref <exact job commit> --source-dir agency/jobs/<id>, which byte-verifies
                            the accepted asset and fails closed on an unresolvable ref; every item classified:
                            1 PROMOTE — DETERMINISTIC SYSTEM · 2 CANDIDATE PATTERN ·
                            3 DIRECTIONAL MODEL OBSERVATION · 4 CANON GAP CANDIDATE ·
                            5 JOB-SPECIFIC / NO PROMOTION; only class-1 code + tests added)
 → REVIEWED PR             (never merged automatically; Canon / Registry / routing / Controller
                            changes are proposals in the PR text, never file edits)
 → MAIN                    (the Controller merges)
 → NEXT MEDIA JOB          (receives the merged learning through the normal startup refresh)
```

Job states, on every job's `JOB.yaml`: `production_status: open | accepted | rejected |
abandoned` and `learning_status: not_started | pending_sync | synced | no_promotion`; a synced job
records `sync.integration_branch`, `sync.integration_pr` and later `sync.merge_commit`. A job is
not closed on ACCEPT until its learning packet exists, so no production disappears without its
learning being examined.

Raw job branches (`work/agency-job-*`) are archival evidence: pushed, never merged, never rebased
onto a newer main. Only the distilled case and explicitly justified deterministic engineering
changes travel to `main`.

## 5. What the operator will not do

- Spend without a job-specific cap stated in the session, or treat prior authority as reusable
  money; an amendment never resets consumed spend.
- Let a generative model render critical copy by default — exact text is composed by code on a
  textless plate.
- Call anything ACCEPTED because gates passed or a judge liked it.
- Edit `canon/**`, `eval/registry/**`, `eval/capability-map/**`, sealed evidence or
  `coordination/**` as a side-effect of production or sync.
- Rediscover the resolved failure classes (text overflow, contrast, cover crop, geometry tokens,
  disjointness, video-frame text, pool liquidity, transient errors) — it uses the runtime's
  implementations.
- Skip the case-002 requirements: every delivered geometry is QA'd as its own final file
  (FORMAT_SPECIFIC_REVALIDATION); a multi-clip single narrator is judged by a human ear on the
  assembly (CROSS_CLIP_VOICE_CONTINUITY); reused treatments carry source, verdict and reuse status,
  and rejected material is never reused silently (DESIGN_REUSE_PROVENANCE).

## 6. Honest limits today (15 Sep 2026)

`runtime/alpha` and `runtime/route.cli --execute` are dry-only on `main`; paid dispatch is done the
way the accepted pilot did it — per-route adapters (`eval/harness-v2/adapters/**`) and recipes under
a per-job append-only ledger — until the runtime's live transport is wired behind a signed record.
Two of ten Canon packs are compiled; missing domains are recorded, never invented. The case validator
(`production-learning/tools/check_case.py`) accepts any honest outcome — accepted, rejected or abandoned,
template or no template — resolves evidence at `--source-ref` / `--source-dir`, byte-verifies an accepted
asset against its recorded sha256, and fails closed when a supplied ref cannot be inspected. The Cloud Vision
post-draw text detector is a paid call and is not authorised by default; frame passes are by eye.

## 7. Verify the setup

```bash
ls .claude/skills/media-agency .claude/skills/media-agency-sync      # both skill dirs present
git check-ignore -v CLAUDE.local.md                                   # ignored
python3 -c "import yaml; yaml.safe_load(open('.claude/skills/media-agency/JOB-TEMPLATE.yaml'))"
```

In an interactive session `/skills` lists `media-agency` and `media-agency-sync`; `/memory` lists
`CLAUDE.local.md` for the agency worktree.
