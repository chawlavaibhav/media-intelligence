# Cloud-session bootstrap for overnight Canon / Eval / Resources workers

**Date:** 26 Aug 2026  
**Status:** CONTROLLER-PREPARED FOR USER ASSIGNMENT  
**Purpose:** make the overnight runbooks executable by fresh cloud-browser sessions with zero prior chat context and no access to the user's laptop.

## 1. Environment assumption — cloud only

Assume the worker is a fresh cloud/browser session.

It may use only capabilities actually available in that session, such as:

- GitHub repository access;
- public web research;
- any cloud code/file execution explicitly exposed in that session.

It must **not** assume access to:

- the user's Mac/laptop filesystem;
- git-ignored raw media stored only on that laptop;
- local Downloads folders, local books, local archives or local working directories;
- environment variables or API keys configured only on the laptop;
- local databases/services;
- prior chat history, prior hidden context or the Controller's memory beyond committed repository evidence.

If a needed artifact is not in GitHub, not publicly retrievable under the task rules, and not otherwise explicitly available to the cloud session, record it as `not_available_in_cloud_session`. Do not ask the sleeping user to upload it unless all independent work is exhausted; continue other packages.

## 2. Authority and evidence order for a zero-context session

Read these in this order before making project claims:

1. `PROJECT-MEMORY.md` — navigation map, not final authority;
2. `coordination/PROJECT-CONTRACT.md`;
3. `shared/COMMUNICATION-STANDARD.md`;
4. `shared/AUTONOMY-POLICY.md`;
5. `coordination/CONTROL-STATE.md` — newer Controller state overrides stale task/handoff wording when supported by the underlying decision/task records;
6. `coordination/plans/2026-08-26-THREE-STREAM-OVERNIGHT-PROGRAM.md`;
7. this cloud-session bootstrap;
8. the assigned stream's `CHARTER.md` and `HANDOFF.md`;
9. the assigned stream's overnight runbook;
10. the stream-specific evidence named by that runbook.

When documents conflict, use the repository's established authority order: committed evidence and validators for factual state; explicit durable Controller decisions for project decisions; newer Controller state/task records over stale narrative handoffs. Do not silently reconcile a conflict — note it in the morning brief if material.

## 3. Required startup acknowledgement — before work begins

Before editing anything, the worker must post one concise startup message in chat. **Do not wait for a reply after posting it; immediately continue the autonomous work.**

The startup message must contain all seven points:

1. **Role:** what this stream owns and explicitly does not own.
2. **Product end-state:** how this stream contributes to the API-native media production intelligence layer and Cost per Accepted Outcome.
3. **Current starting state:** the important quantified baseline for this stream.
4. **Tonight's work:** exact work-package IDs being executed.
5. **Tonight's prohibitions:** money/API/source/ingestion/human-judgement/merge limits relevant to the stream.
6. **Cloud constraint:** confirm no laptop/local-file/API-key access is being assumed and state how unavailable local artifacts will be handled.
7. **Morning deliverable:** what concrete artifacts/Controller Brief should exist when the session finishes.

Also include the exact Communication Standard acknowledgement required by `shared/COMMUNICATION-STANDARD.md`.

The purpose is diagnostic: before the user goes to sleep, they can see whether the worker understood the assignment. The worker should then continue without requesting confirmation.

## 4. General cloud execution rule

The overnight program distinguishes **design/specification completion** from **runtime verification**.

If the cloud session has a code runner/workspace, use it where the runbook calls for local tests/dummy fixtures.

If it does not:

- complete the schema, manifest, algorithms, test cases, known-answer fixtures and expected assertions in repository files;
- mark execution status honestly as `implementation_written_not_executed_in_cloud` or `runtime_verification_blocked_no_runner`;
- do not claim tests passed;
- do not stop unrelated research/design work.

A missing terminal is not an architecture stop. It is an execution-environment limitation to record.

## 5. Canon cloud-readiness interpretation

Canon's overnight C1–C4 work is intended to be cloud-executable from GitHub + public web research.

### Available in cloud

- all 19 accepted Canon source-knowledge directories and their audit records are committed;
- the Canon schemas/specs, coverage history, findings and handoff are committed;
- C1 live-19 rebaseline can therefore be performed from repository evidence;
- C2 brief-bank/oracle-context work uses committed Canon only;
- C3 is package/design only and must not call external LLM experiment APIs;
- C4 is official-route source research only.

### Not available / not needed tonight

- local book PDFs or course files are not required for C1–C4;
- if C4 discovers that a proposed candidate can only be assessed by reading a local copy not in GitHub, record access as unresolved/needs later acquisition rather than assuming the laptop copy exists;
- no source ingestion is authorised, so the worker must not need local source files to finish tonight's authorised tranche.

Canon should be able to complete essentially all C1–C4 planning work in a browser-only cloud session, except optional code-based validation if no runner exists.

## 6. Eval cloud-readiness interpretation

Eval's E1–E4 work is cloud-executable from GitHub + official public model/API documentation. E5 has a split outcome depending on whether code execution exists.

### E1 — capability contract

Fully cloud-executable from committed Eval/Canon/Resources evidence.

### E2 — current workflow/API/access/pricing inventory

Use official public provider docs for current model identity, endpoint, constraints and pricing.

**Do not inspect or infer the user's laptop credentials.** For execution access record only what the cloud session can establish:

- `cloud_session_configured_access: yes` only if the session explicitly exposes working provider access;
- otherwise `cloud_session_configured_access: no_or_unknown`;
- `user_laptop_credentials: not_visible_to_cloud_session`.

This inventory is about what is technically available and what would cost money later, not permission to call it tonight.

### E3 — evaluator qualification specifications

Package/design only. Existing Devanagari battery metadata and human-validation records in GitHub may be used. If a referenced raw asset is not committed, design around its committed manifest/record and mark byte-level inspection unavailable rather than searching the laptop.

### E4 — 100-item bank design

Fully cloud-executable; no media generation is required.

### E5 — generate-once harness / empty Registry interface

- If the cloud session has a repository code runner: implement and run dummy/synthetic tests as specified.
- If it has GitHub editing but no runner: still implement the schemas/harness code where feasible, create frozen dummy fixtures and expected assertions, instantiate the Registry schema **empty**, and mark runtime verification blocked.
- Never create empirical Registry rows or pretend dummy outputs are model evidence.

Lack of laptop API keys is irrelevant because no paid empirical call is authorised tonight.

## 7. Resources cloud-readiness interpretation

This stream has the largest laptop dependency and must handle it explicitly.

### Critical fact

The **34,786-item / 5.70 GB raw external corpus is not committed to GitHub**. The repository contains committed source records, manifests, generated reports, scripts and small historical samples; most raw media is git-ignored and was retained on the acquisition machine. Therefore a fresh cloud worker cannot truthfully re-decode, re-hash or visually inspect the full raw corpus tonight.

### R1 — requirements matrix

Fully cloud-executable from the three-stream plans and committed stream evidence.

### R2 — existing-corpus rebaseline

Perform a **metadata/evidence rebaseline** from committed source records, manifests, integrity/bias reports and prior Controller briefs.

The worker may report historical observations such as `34,786/34,786 decode cleanly` **only as previously committed/observed results**, with provenance to the report. It may not say it reran those checks in cloud.

Legacy evidence reconciliation may search legitimately accessible GitHub repositories, including `chawlavaibhav/media-factory`. For any expected media bytes not committed or otherwise accessible, use `metadata_only` or `unavailable_in_cloud_session` exactly as supported by evidence.

### R3 — allocation/leakage/lineage/storage contract

Design and schema work is fully cloud-executable. Validators can be written. They are only `verified` if the cloud session actually has a runner and the required committed fixture data.

### R4 — missing-pack supply routes

Fully cloud-executable as research only. No downloads/acquisition from new source families tonight.

### R5 — existing-resource Eval views

Build **logical/view manifests from committed manifests/source metadata only**, without copying raw media. Do not assert that every referenced raw file is present in the cloud. Include a field such as `payload_availability_in_this_session` when useful.

### R8 — legacy/empirical archive

Schema and GitHub-history reconciliation are cloud-executable. Do not try to recover laptop-only generated media. Record the exact availability state instead.

## 8. Questions and overnight autonomy

The user will be asleep. Do not ask routine questions.

When uncertainty arises:

1. first resolve it from the runbook, Project Contract, Control State, Charter, prior decisions and committed evidence;
2. if multiple scientifically valid choices remain inside the approved task, choose the most conservative/reversible option and document it;
3. if one work package hits a mandatory stop, freeze/document that package and continue other independent packages unless the runbook says the dependency blocks them;
4. only stop the whole stream when the Autonomy Policy requires it and no independent approved work remains.

Never broaden scope merely to stay busy.

## 9. What each worker should understand before starting

### Canon

"I am not collecting books tonight. I am turning the existing 19-source knowledge base into an explicit picture of what it covers for the first commercial product, creating one reusable 30-brief commercial-intent bank, packaging the first clean test of whether Canon adds value, and researching only the few source gaps that the live corpus actually justifies. My end-state is a proven creative knowledge layer that improves planning/critique without selecting models."

### Eval

"I am not benchmarking models tonight. I am finishing the measurement architecture so later paid generations are not duplicated or scientifically vague: 36 capabilities, six instrument families, a 100-item generate-once/multi-score bank, a current official workflow/cost inventory and the harness/Registry interface. My end-state is an empirical Capability Lab that tells the product what current workflows can do, under which conditions, at what reliability and cost."

### Resources

"I am not downloading datasets tonight. I am converting the existing corpus and the new Canon/Eval plans into one evidence-supply map: what is already sufficient, what is missing, how protected sets/lineage/rights work, how old failures are preserved, and legitimate routes for the small controlled packs still needed. My end-state is an evidence service that can mechanically say whether every experiment has valid independent material."

If the worker's startup acknowledgement materially differs from these meanings, it should reread the shared plan and its runbook before editing.

## 10. Morning truth standard

The morning Controller Brief must distinguish:

- completed and verified in this cloud session;
- completed design/implementation but not runtime-verified;
- based on previously committed observations that were not rerun;
- blocked specifically because raw laptop/local material was unavailable;
- not attempted because it belongs to a later gated task.

A smaller honest completion state is preferable to a falsely complete one.