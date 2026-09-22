# Media Intelligence P1 — the product

Status, evidence and blockers: `coordination/p1/P1-BUILD-STATUS.md`. Operating it: `deploy/RUNBOOK-P1.md`.

```
python3 -m unittest discover -s product/tests -t .      # 37 tests, USD 0
python3 -m product.smoke                                  # media engine on this host + dry jobs + backup/restore
MI_DATA_DIR=/tmp/mi python3 -m product.admin init-operator --email you@example.com
MI_DATA_DIR=/tmp/mi python3 -m product.web.app --port 8080 &   MI_DATA_DIR=/tmp/mi python3 -m product.worker &
```
Defaults are `MI_PROVIDER_MODE=simulated` and `MI_REASONING_MODE=simulated`: nothing paid can leave the host.

| Module | Role |
|---|---|
| `store.py` `states.py` | authoritative job state, ledger (atomic reserve + attempt ids), leases, events, timings |
| `orchestrator.py` `worker.py` | five-stage pipeline as idempotent steps; asset graph; pauses; revision |
| `reasoning.py` `contracts.py` `simulated.py` | strategist, creative director, isolated reviewers; output contracts |
| `canon_access.py` | ten adopted packs via the runtime lookup; bounded, logged deep retrieval |
| `providers.py` `dispatch.py` | the one paid-dispatch path (nano-banana-2, Veo 3.1 fast i2v, Lyria) |
| `prompts.py` `compose.py` `media.py` | deterministic prompts; exact text/logos by code; ffmpeg assembly |
| `verify.py` `data/FAILURE-CONTROLS-v1.yaml` | checks on exact file versions; the presentation gateway |
| `learning.py` | metrics and the production-learning case skeleton |
| `web/` `service.py` `admin.py` | customer + operator app; accounts; backup/restore |
