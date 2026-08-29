# EVAL-036 — Import Media Factory Historical Empirical Priors

**Owner:** Eval / Capability Lab  
**Spend:** USD 0  
**Generation authority:** 0  
**Registry authority:** NONE  
**Status:** AUTHORISED by
`coordination/decisions/CONTROLLER-PROGRAMME-RESET-MEDIA-FACTORY-PRIORS-2026-08-29.md`

## Objective

Import the already-recovered Media Factory evidence into `media-intelligence` as a compact,
provenance-preserving **historical empirical prior** set so future work stops rediscovering
questions already observed in real experiments.

This task does not qualify current models.
It does not populate the Capability Registry.
It does not run any API.
It does not rescore or regenerate historical media.

## Source material

Primary local source on the user's Mac:

- `~/Vaibhav_Personal_Projects/media-factory-controller-handoff.zip`
- original repo: `~/Vaibhav_Personal_Projects/media-factory`
- GitHub: `chawlavaibhav/media-factory`

Recovered pack contains:
- `EVIDENCE-MANIFEST.json` (206 rows);
- `MEDIA-FACTORY-EMPIRICAL-FINDINGS.md`;
- `MEDIA-FACTORY-ROUTING-PRIOR.md`;
- `PROMPT-ENRICHMENT-EVIDENCE.md`;
- `COST-SUMMARY.md`;
- `SOURCE-INDEX.md`;
- `source-copies/`;
- `selected-media/`;
- `contact-sheets/`.

Independently inspect the original Media Factory repo where needed.
Do not trust this task file as a substitute for the sources.

## Required output root

Create:

`eval/historical-priors/media-factory-v1/`

## Required artifacts

### 1. `PRIOR-MANIFEST.json`

Import the 206 recovered rows in a compact machine-readable form.

Each row must preserve at least:
- artifact id;
- modality;
- date;
- task/brief;
- workflow;
- model;
- provider;
- final media prompt if recovered;
- input/reference assets if recovered;
- output/source path;
- cost evidence if recovered;
- human pass/fail if recovered;
- human note if recovered;
- failure modes if recovered;
- generated-vs-composited text state;
- speech/lip-sync state where applicable;
- image-conditioning state;
- retry state;
- field-level evidence source;
- artifact SHA-256.

Do not fill unknown fields from memory.

### 2. `EVIDENCE-TIERS.md`

Preserve the recovered three-tier distinction exactly in meaning:

- Tier A — surviving artifacts + written human score/head-to-head evidence;
- Tier B — surviving artifacts + directional operator judgment, small n/no formal scoring;
- Tier C — operational anecdote/handoff/memory; not independently scoreable.

Explain in plain English that these tiers are not Registry qualification levels.

### 3. `HISTORICAL-ROUTING-PRIOR.md`

Import the recovered routing table, preserving:
- requirement/condition;
- preferred historical workflow;
- avoided workflow;
- why;
- evidence;
- confidence/evidence tier;
- freshness risk.

Header must say:

> HISTORICAL EMPIRICAL PRIOR — NOT A CURRENT CAPABILITY CLAIM; TARGETED FRESHNESS CHECK REQUIRED
> BEFORE PRODUCTION USE.

Do not convert any row into Registry data.

### 4. `PROMPT-ENRICHMENT-EVIDENCE.md`

Preserve the crucial corrected conclusion:

- an LLM creative-director/enrichment mechanism existed;
- production runtime preferred OpenAI when an OpenAI key existed;
- Claude Code authored many spike prompts interactively;
- **no controlled raw-vs-enriched media A/B survives**;
- no runtime enrichment logs survive;
- closest prompt-iteration pairs are directional only;
- excessive prompt choreography is a surviving counterexample.

Do not upgrade "plausible" to "proven".

### 5. `HISTORICAL-FINDINGS.md`

Import the evidence-recovered findings and the 12 claim dispositions.

At minimum preserve these corrections:
- 64 scored stills;
- Seedream 29/32, Nano 25/32;
- different failure profiles;
- image-first -> minimal I2V supported historically;
- in-scene still text sometimes exact;
- exact text through motion historically fragile;
- deterministic composition exact but can look aesthetically amateur;
- lip-sync routes differed;
- Veo/Wan policy asymmetry;
- multi-turn dialogue failure != all two-person dialogue failure;
- no automated router existed;
- cost ledger/dashboard disagreement.

### 6. `COST-RECONSTRUCTION.md`

Preserve both cost views and why they disagree.

Do not publish one fabricated "true total".

Include:
- ledger total USD 35.28 and its known over-count/gaps;
- dashboard/memory estimate USD 22.38 spike + ~USD 12.2 guddu;
- historical unit prices as historical only;
- derived cost per accepted still clearly labelled derived-now, not historically recorded.

### 7. `PROVENANCE.md`

Record:
- original repo and commit(s) where available;
- every imported source file path;
- SHA-256 of the handoff ZIP;
- SHA-256 of the imported pack files;
- which source evidence exists only locally;
- which curated evidence is also in `chawlavaibhav/Aight_Website/assets/gallery/`;
- which production outputs are missing permanently (e.g. Render /data corpus);
- PII-containing SQLite DB explicitly excluded.

### 8. Compact visual audit only

Do NOT commit the ~800 MB original corpus or the 117 MB pack wholesale.

You may import:
- small contact sheets/frame strips needed to audit the 64-still pattern and representative video
  defects;
- the original `scores.json`;
- compact source scripts needed to pin prompt/model conditions if repository policy allows.

For large/duplicated media:
- retain SHA/path/provenance references;
- use the already-public/accessible Aight gallery copies where available;
- do not invent a durable location when none exists.

If repository size/policy makes even the compact visual set inappropriate, stop and propose the
smallest alternative.

## Mechanical checks

Before returning:

1. Count imported prior rows = 206.
2. Count human-scored rows = 67.
3. Recompute the 64 consistency still headline:
   - Seedream 29/32 pass;
   - Nano 25/32 pass.
4. Verify the ten failure labels used for the historical failure-profile claim.
5. Verify no row under `eval/registry/` was added/changed.
6. Verify no API/provider call occurred.
7. Verify no historical artifact was regenerated or rescored.
8. Verify evidence-tier labels are present on every synthesized finding/routing claim.
9. Verify every model-specific routing statement includes date/freshness warning.
10. Verify the controlled prompt-enrichment A/B remains explicitly **NOT RECOVERABLE**.

## Boundaries

Do not:
- change Registry admission rules;
- add Registry rows;
- call any model/provider;
- browse current model prices;
- refresh capabilities;
- redesign Capability Contract;
- create Production IR;
- create Planner/router implementation;
- modify Canon;
- interpret the 206 rows as a current benchmark population;
- promote Tier C anecdotes to Tier A;
- copy PII databases;
- alter Media Factory history.

## Completion

Commit/push a branch:

`work/eval-036-media-factory-historical-priors`

Do not merge.

Return:
- branch;
- commit;
- base-main SHA;
- imported row count;
- scored row count;
- consistency recomputation;
- files created;
- compact visual evidence imported;
- source pack ZIP SHA;
- Registry diff = zero;
- API calls/spend = 0;
- any evidence contradiction discovered beyond the recovered pack;
- any source that could not be independently verified.
