# PRODUCTION WORKFLOW — every job, stage by stage

Each stage names what it writes into the job record (`JOB-TEMPLATE.yaml`). A stage with no written
output is not done. Job records live at `agency/jobs/<JOB-ID>/JOB.yaml` on a branch
`work/agency-job-<job-id>` (the accepted pilot's precedent: the job branch carries the evidence and
is pushed, never merged; what enters `main` is a distilled production-learning case by PR, via
`/media-agency-sync`).

Cost profile of a job: stages 1–7 are USD 0. Money moves only in stage 9, only under `spend.cap`.

## 0. Sync from main — one session, many job branches (MAIN → AGENCY)

The session is long-lived; the branch is per job. At the start of EVERY new job:

```bash
git status --short                      # must be empty: an unfinished job is never merged over
git fetch origin main
git rev-parse --short origin/main       # the candidate production base
```

- Working tree dirty → the previous job is unfinished. Commit and push it to its own job branch
  (archive), or finish it; never rebase/merge main into it. Then continue.
- Compare `origin/main` with the previous job's `production_base_sha` (last `JOB.yaml` on the
  previous job branch, or the sha in the READY block). If it moved, refresh per `BOOTSTRAP.md`
  §Refresh: PROJECT-MEMORY, CONTROL-STATE, Canon shape / compiled packs, routing evidence, runtime
  production rules, production-learning cases + promoted patterns, and the Upwork context where the
  job is commercial.
- Create the job branch from the fetched base and record it:

```bash
git checkout -b work/agency-job-<job-id> origin/main
```

Write `production_base_sha` (full sha of `origin/main`) into `JOB.yaml`. **The base never changes
during a running job** — a job is reproducible against the sha it started from; the next job
refreshes again. Claude memory is never a substitute for this fetch.

## 1. Open the job — start the clock

Write `job_id`, `class`, `production_base_sha`, `branch`, `ttao.job_start_utc` (now, UTC, from
`date -u`) and the brief verbatim into `JOB.yaml`. **Before reading anything else.** The pilot's
TTAO had to be reconstructed from session metadata; yours must not. Commit the opened record.

## 2. Intake → Normalized Request

Fill every `intake.*` field. Sources, in order: the brief; the commercial repo (`PROFILE.md` defines
package contents, sizes, revision counts, the delivery note); production judgment for non-critical
gaps. Ask the user only when a missing value could invalidate the output (exact Hindi wording,
a legal line, whether a supplied bottle may be regenerated or must be composited, deadline vs cap).
Record every judgment call in `intake.assumptions`.

Then write the Normalized Request (`nr.*`): modality (R05), requested_operation (R01), entities,
`text_requirements` (every exact string with script + placement + may_reflow), language topology /
market, acceptance intent, ambiguity markers. Use the vocabulary of
`runtime/canon/KIND-NR-BINDING-v0.yaml` and `runtime/contracts/DELIVERABLE-KINDS.yaml`. The NR is
what the customer said, conservatively; it is never edited later — deviations are recorded against it.

Job class (one): `customer_work` · `upwork_portfolio` · `spec_work` · `internal_experiment`.
Portfolio and spec work still get a full intake; the "client" is the positioning in `PROFILE.md`.

## 3. Template-first / learning-first

Before designing anything, read the accepted templates and cases loaded at bootstrap and decide:

- Same production class as an accepted template? → `template.reused: <template_id>`. Reuse its
  **structure, production logic, QA and workflow**. Do not copy its surface aesthetics. Its numbers
  (pacing, holds, beat lengths) are `evidence_scope: this_accepted_template` — carry them as a
  starting point and say so; do not present them as norms.
- Any case defect (`SYSTEM-DEFECTS.yaml`) or directional route note (`ROUTE-OBSERVATIONS.yaml`)
  touching this job's routes → list in `template.learning_applied` with the id.
- No fitting template → `template.reused: none`, one line why.

**DESIGN_REUSE_PROVENANCE (case 002).** Any treatment, component or asset carried in from earlier
work — a seam pill, a panel system, a type treatment, a plate, a packshot — gets a `plan.assets[].reuse`
record BEFORE it is used: `source_asset` (path @ sha or case/version), `source_verdict` (the human
verdict that asset actually received), and `reuse_status`:

| `reuse_status` | Meaning | What it permits |
|---|---|---|
| `rejected` | the human rejected the version it came from | nothing, unless the human explicitly re-approves it for this job (`human_reapproval` recorded verbatim) |
| `accepted_in_context` | accepted once, in a specific plate / aspect / subject / context | reuse only in that same context; any change of aspect, plate, subject or context → `fresh_qa_required: true` and the full QA of the new file |
| `reusable_candidate` | accepted more than once across contexts, or promoted as a template | reuse with QA of the new file; still not a Canon rule |

`accepted_in_context` is never read as universally reusable. This is an operator record, not doctrine.

## 4. Deterministic Canon pack lookup

Apply `canon/packs/pack-triggers-v0.yaml` to the NR by hand or via the runtime:
universal packs + modality base packs + conditionals (`text_requirements` non-empty →
typography_and_copy; product/packshot entity → product_appearance; language topology or market IN →
indian_indic_context; advertising intent → commercial_communication). Under the uncertainty rule
inject the union. Record `canon.packs_selected` (all fired ids) and `canon.packs_injected` (only
those compiled and accepted — today `product_appearance`, `composition_and_attention`);
`canon.missing_domains` = the rest. The runtime does this lookup in-process at USD 0 (no spec, no
fixture needed):

```bash
python3 -c '
import sys, json; sys.path.insert(0, ".")
from runtime.canon import normalize, lookup
job = json.load(open(sys.argv[1]))          # a PRODUCTION-JOB-v1 brief (shape: runtime/fixtures/alpha-briefs/*.json)
lk = lookup(normalize(job))                  # kind binding -> CANON-010 NR -> trigger table -> accepted compiled packs
print("selected:", [f"{s.pack_id}:{s.status}" for s in lk.selections])
print("injected:", lk.injected_pack_ids, "| gaps:", lk.gap_pack_ids)
print("prefix sha256:", lk.prefix_sha256, "| tokens:", lk.tokens, "| check ids:", len(lk.check_ids))
' agency/jobs/<id>/brief.job.json
```

Write the brief as a PRODUCTION-JOB-v1 JSON first (`deliverable_request.kind` from
`runtime/contracts/DELIVERABLE-KINDS.yaml`; `exact_text_strings[]` with `script` and `placement`;
`reference_assets[]` roles) — that file is the NR's source and goes in the job directory.

(`python3 -m runtime.cli <brief.json>` also does it, but for a brief with no recorded reasoning
pass it refuses AND writes the unanswered prompt into `runtime/fixtures/planner/unanswered/` inside
the checkout — a repo mutation. Use it only with `--store` and delete the spill, or prefer the
in-process call above.)

**Do not compile, paraphrase or invent a pack** for a missing domain. Proceed on the brief and
record the gap in `learning.canon_gaps` only if the production actually fails for want of it.

## 5. Creative blueprint — the concept

Canon constrains; it does not direct. Write `blueprint.*` before any route is chosen:

| Field | Must answer |
|---|---|
| `first_read` | what the eye lands on first, second, third (CA-D1 — one cue per beat) |
| `hook` | why anyone stops scrolling |
| `offer`, `product`, `proof`, `cta` | where each sits and how big, in that hierarchy |
| `attention_order` | the path across the frame / across cuts |
| `brand_world` | one light source, palette, register (PA-D4/PA-D6) |
| `remember` | the one thing the viewer keeps |
| `muted_test` | for video: does it work with the sound off? (yes / no / n-a) |
| `deviations` | any pack default overridden, with the brief clause that forces it |

Then render the pack check lines by id (`PA-D1..D10`, `CA-D1..D11`) against the blueprint — each
`pass | n-a | deviation:<clause>`. For Indian/Hindi work, originate the Hindi copy; never translate
the English line word for word (pilot lesson, `preprod/CANON-BRIEF.md`).

Consult Canon persona review (Karl disconfirmer, Ezra copy) when the job is customer-facing copy;
their verdicts are input, not acceptance.

## 6. Production plan

Break the deliverable into assets with dependencies (`plan.assets[]`): plate(s), packshot
treatment, composed statics per size, motion from an accepted still, audio, assembly. State for
each asset its exact-text mechanism (`code_set_on_textless_plate` default) and whether it reuses an
existing accepted asset (`reuse_of: <path @ sha>` — nothing is duplicated when an accepted asset
already serves). Format variants (4:5 / 1:1 / 9:16 / WhatsApp 800×800) are compositor renditions of
one accepted master, never separate draws — and each rendition is a deliverable of its own for QA
(stage 11: FORMAT_SPECIFIC_REVALIDATION). List every delivered geometry under `plan.deliverables[]`.

## 7. Route selection — evidence, not fame

For each generative asset write `plan.assets[].route` from:
routing evidence (cell status + `production_use_allowed`) → job requirements → surface
availability → price (roster + pin, live) → pool liquidity → directional production notes as
tie-breakers only. Rules:

- `clean_observed` + `production_use_allowed: true` → routable. `manual_only` → routable only
  with the human's explicit OK in this job. `false` → never, not even as fallback.
- Cheapest clean route that satisfies the requirement wins; name the declared fallback.
- A `directional_only` cell or an n=1 case observation may break a tie or trigger a
  **micro-qualification** (one cheap draw, human gate, then freeze, then build dependents). It may
  not be presented as Registry truth.
- Required capability with no clean cell (e.g. single-speaker native speech from an anchored still)
  → micro-qualify before any dependent spend. Record it as `plan.micro_qualifications[]`.
- Unknown provider liquidity is not executable: read the pool balance (`runtime/execute/pools.py`
  shape: balance, read_utc, source) and write it to `spend.pool_readings`. No reading for a pool →
  no dispatch on that pool (A7 is a hard stop, not a NOT_RUN to carry).

The offline planner does the evidence + price part for a PRODUCTION-SPEC-v1 — which exists only
for briefs with a recorded reasoning pass (the committed fixtures). For a new brief, read the
evidence from the bootstrap table and price each route through the runtime's own PriceBook (roster
+ pin, live; USD 0; the quantity facts are what the provider bills on):

```bash
python3 -m runtime.route.cli --plan <spec.yaml> --profile alpha_human_release     # fixture specs only
python3 -c '
import sys; sys.path.insert(0, ".")
from runtime.route.cli import build_router
pb = build_router()[0].prices
for rk, facts in [("flux-2-pro", {"params": {}}), ("seedream-5-pro-edit", {"params": {}}),
                  ("minimax-h3-max-i2v", {"params": {"duration_s": 10}}), ("kling-v3-pro-i2v", {"params": {"duration_s": 10}})]:
    q = pb.quote(rk, facts)
    print(rk, "priced" if q.priced else "UNPRICED", q.unit_price, q.unit, "x", q.quantity, q.quantity_unit, "=", q.expected_cost_usd, q.billing_pool, "" if q.priced else q.reason)
'
```

An `UNPRICED` route (no live pin, promo price, or a unit whose quantity is not in the facts — e.g.
`per_1000_characters` needs `params.chars`) is never auto-selected; supply the fact or route
elsewhere. Known defect (15 Sep 2026, found by the USD-0 mock): the runtime PriceBook multiplies a
per-1000-characters price by the raw character count (Sarvam 79 chars quoted USD 2.48 instead of
≈ 0.0025); until it is fixed, cross-check per-character quotes against
`eval/harness-v2/pricing.py` and record the harness figure in `plan.assets[].route.unit_price_usd`. Planner exclusions (e.g. RR-3 Devanagari) apply to the agency's routes too.
Note: the Alpha-1 profile auto-routes 26 cells; the agency may route `manual_only` cells with the
human's OK — that is a human decision on this job, not a runtime policy change.

## 8. Pre-dispatch checks (USD 0)

Run before any paid call; write `qa.pre_dispatch`:

- Canon gate over the package and prompts: `python3 canon/gate/run_gate.py` (the LIMIT-TEXT
  no-lettering clause on every plate prompt; delivered-vs-declared aspect/duration).
- Exact strings: every critical string is in the copy deck byte-for-byte; none is in a generation
  prompt unless the job explicitly requires in-scene text.
- Spend: `spend.cap` stated by the user this session; planned attempts × pinned price ≤ cap;
  pool readings positive for every pool the plan touches.
- Consent gate for any identifiable person in a supplied asset.

Show the user: concept + routes + expected spend (stage output "start-of-job summary"). Proceed
only if the cap is known.

## 9. Generation — the honest dispatch mechanism

`runtime/alpha` and `runtime/route.cli --execute` are **dry-only on main** (live transport
deliberately unwired). Paid dispatch today is done the way the accepted pilot did it: per-route
recipes (`eval/harness-v2/adapters/**`, `transports.py`; the pilot's `preprod/recipes/*.py` on
`work/pilot-upwork-intro-video-v4`) under a **per-job append-only ledger** — reserve a line before
the request leaves, settle after, one line per attempt, failed calls included, 0 retries. Keys are
read by name from the environment (`source ~/.mi-keys`); never printed, never written to a file.

For each attempt append to `spend.attempts[]`: attempt id, route, surface, pool, pinned unit price,
quantity, reserved USD, start/end UTC, latency, status (`ok | provider_refusal |
infrastructure_transient | unclassified`), artifact path + sha256. Classify failures with
`runtime/execute/provider_errors.py`; a transient outage is retried only as a new attempt, counted.
Stamp `ttao.dispatch_start_utc` on the first call and `ttao.artifact_received_utc` on the last.

## 10. Deterministic composition

Copy, CTA, price, legal, layout wrappers, format variants, final framing — by code. Use the
existing gates, in this order, and record each in `qa.composition`:
`check_text_bounds` → `check_contrast` (opaque backing when the ratio fails) → `check_fit`
(contain by default; a `cover` needs `declared_crop` + reason) → `check_geometry` (one
`DesignTokens` source) → `check_disjoint` over `headline, offer, code, cta, legal`. Devanagari and
all exact type are shaped with HarfBuzz (`hb-view`) + Pillow (pilot `tools/adcomp.py`,
`eval/harness-v2/composite.py`). A render command that exits 0 is not an accepted result.

## 11. Post-draw QA

Run `QA-CHECKLIST.md` in full; write `qa.post_draw` and, for video, `qa.video_frames` with the
sampled frame list — a video with no `qa.video_frames` row cannot be presented for acceptance.

**FORMAT_SPECIFIC_REVALIDATION (case 002).** QA is per delivered file, keyed by geometry: every
1:1, 4:5, 9:16, WhatsApp, 16:9 or other final rendition gets its own `qa.final_geometry[]` row
with the composition gates (C1–C8) and the visual checks (stray lettering, subject/critical-object
obstruction, crop) run on THAT file. A master's PASS is recorded on the master only and transfers
to nothing. A geometry with no row cannot be delivered.

**CROSS_CLIP_VOICE_CONTINUITY (case 002).** When two or more clips are meant to be one narrator or
speaker, the assembled result gets `qa.voice_continuity` (D14): same perceived narrator identity,
compatible accent/timbre, delivery/cadence continuity, no narration holes or restarts at clip
boundaries — judged by a human ear on the assembly, in addition to per-clip transcript checks.
Transcript match is presence, not delivery. `SINGLE_VOICE_SOURCE` is a candidate pattern the
operator may choose; it is not mandatory. Contact sheets / key frames for every video assembly go under
`agency/jobs/<id>/qa/`. Stamp `ttao.qa_complete_utc`.

## 12. Bounded repair

A failed check → classify (`creative_direction · generation · audio · route · compositor · crop ·
text · product_fidelity · pacing · infrastructure`) → repair that layer only → new attempt or new
render, recorded. Accepted assets are kept (`reuse_of`). Repairs count toward `spend.cap`; the
repair allowance is finite — say when it is spent and stop.

## 13. Human release

Stamp `ttao.human_review_requested_utc`. Present: the candidate(s), the QA table, deviations,
actual spend so far, elapsed TTAO. Offer exactly **ACCEPT / SPECIFIC REPAIR / REJECT**. Record the
verdict verbatim with `ttao.human_decision_utc`. Only `ACCEPT` by the user sets
`outcome.status: accepted`. `SPECIFIC REPAIR` → stage 12 on the named element. `REJECT` → the
decision is recorded; ask what to change before spending again.

## 14. Close the job — the learning packet (AGENCY → PRODUCTION LEARNING)

On ACCEPT the job is **not closed** until `agency/jobs/<id>/LEARNING-PACKET.yaml` exists
(section `learning_packet` of `JOB-TEMPLATE.yaml`; it may be the same file). Minimum content:
source main sha · job class · original brief · final accepted asset refs + sha256 · every route
attempted · paid attempts · rejected attempts · human verdicts · repairs · known cost · TTAO ·
versions and review cycles · observed failures · root-cause class per failure · directional model
observations · candidate reusable patterns · candidate deterministic engineering improvements ·
Canon gap only if a real gap was exposed. Keep the five kinds apart: observed facts · human verdict
· directional model observations · deterministic system defects · candidate patterns.

Then set `production_status: accepted | rejected | abandoned` and
`learning_status: pending_sync` (or `no_promotion` when the packet says every item is
job-specific — still write the packet), commit, and push the job branch:

```bash
git push -u origin work/agency-job-<job-id>
```

The packet is raw material. Distilling it into `production-learning/cases/<CASE-ID>/` on a clean
integration branch from `origin/main` (validated by `production-learning/tools/check_case.py
--source-ref <exact job commit sha> --source-dir agency/jobs/<id>`, which byte-verifies the accepted asset), and opening the PR, is `/media-agency-sync`'s job — never
done on the job branch, and never by editing Canon, the Registry, routing files or Controller state.
Propose; do not apply.

Provenance for reuse: every accepted asset in `outcome.assets[]` carries path, sha256, the attempt
id that produced it, and the composition inputs, so it can later become portfolio, showreel, spec,
case study, a format variant, a demo, or template evidence without regeneration.

## KPIs recorded on every job

`CpAO` (sum of `spend.attempts[].reserved_usd`, failed calls included) · `TTAO`
(`human_decision_utc − job_start_utc`, on ACCEPT) · `human_review_cycles` · `versions_to_acceptance`.
Baseline: read `production-learning/cases/UPWORK-INTRO-001/TIME-AND-COST.yaml` at job end and
report both numbers side by side; never a blended score, never a faked comparison.

## Upwork portfolio batches

Re-read `PROFILE.md` positioning before the batch if its `_Last updated` line changed. The promise is
dependable, high-quality creative production at AI speed — not "we know AI tools". Across a batch
demonstrate a spread of: excellent still advertising · product in new scenes · video · creative
range · exact commercial copy · Indian / Hindi capability · variation · speed/reliability. No two
tiles from the same template look. Tile text never names a tool or model. Timing claims only from
real ledger timestamps (and only where the profile currently allows them).
