# P1 operator runbook

## Install (fresh VM, root)

```
REF=claude/confident-franklin-s1v8ln ./deploy/install.sh     # apt deps, user `mi`, /srv/mi, systemd units, smoke test
```
The install runs `python3 -m product.smoke` **before** enabling the services. It must print three PASS lines
(media engine on this host, dry image + film jobs, backup/restore). Do not take traffic on a FAIL.

Then: edit `/etc/mi/mi.env` (hostname, keys), copy `deploy/Caddyfile` to `/etc/caddy/Caddyfile` with the real
hostname, `systemctl reload caddy`, and create the first operator:

```
sudo -u mi sh -c 'set -a; . /etc/mi/mi.env; PYTHONPATH=/srv/mi/app python3 -m product.admin init-operator --email you@company'
```
Open the printed link, set a password, sign in → `/ops` → create the customer account (per-job ceiling) → invite.

## Modes

| Setting | Effect |
|---|---|
| `MI_PROVIDER_MODE=simulated` | no image/video/music call can leave the host; test media; USD 0 |
| `MI_REASONING_MODE=simulated` | no model call leaves the host; deterministic stand-ins |
| `live` (either) | real calls, each one reserved against the job's authorised budget first |
| `MI_HOLD_BEFORE_PREVIEW=1` | every finished cut waits in `operator_hold` for an operator look (recommended for the first beta jobs) |

A simulated review can never pass the independent-review check; in simulated mode every cut stops at
`operator_hold` and can only reach the customer through named waivers. That is by design.

## Daily operation

- `/ops` lists every job and its state; a paused/failed job shows its reason.
- `/ops/jobs/<id>`: brief (frozen), intent, direction, pre-spend review, Canon trace, asset graph, ledger,
  reasoning calls (with the context each saw), assets, gateway table, metrics, event log.
- **Gateway blocked** (`operator_hold`): look at the media. For each FAIL/NOT_VERIFIED row either get it fixed
  (pause → change → resume) or waive it with a real reason (e.g. "listened end to end on headphones: no speech").
  Release sends the cut to the customer. Waivers are recorded against the exact file version.
- **paused_budget**: the customer raises the budget on their page (or the operator asks them to). Never raise
  a customer's budget on their behalf.
- **paused_provider**: retried automatically after 60 s. Persistent failures: check provider status / credit pools.
- **failed**: read the reason in the event log; fix; `Resume` (goes back to the recorded state).

## Worker restart / crash

Safe at any moment. Leases expire (15 min) or are taken over; the new worker settles or resumes whatever the
dead one left in flight (a Veo clip with an operation id is polled, not re-bought; anything else is recorded
`uncertain`, kept as spent, and never silently re-sent).

## Backup and restore

- Nightly `mi-backup.timer` (21:30 UTC): `product.admin backup` → `/srv/mi/data/backups/`, copied to
  `MI_BACKUP_BUCKET` when set; 7 days kept locally.
- Restore drill: `python3 -m product.admin restore --from <archive> --data-dir /srv/mi/restore-test` → prints
  `integrity`, job count and asset files present. To switch over: stop services, point `MI_DATA_DIR` at the
  restored directory (asset paths are relative to it), start services.

## Retention and deletion

Customer material lives only under `MI_DATA_DIR/media/<job>/` and the database, never in git. To delete a
customer's job on request: stop the worker, `DELETE` the job's rows (jobs, events, artifacts, nodes, assets,
attempts, checks, waivers, feedback, timings, llm_calls, deliveries) and remove `media/<job>` and `cases/<job>`,
then take a fresh backup and expire older ones. (A one-command purge is not built yet.)

## Secrets

Only in `/etc/mi/mi.env` (0640 root:mi) and the Vertex key file (0600). Values are read by name, scrubbed from
every stored error/log line, never sent to a model and never shown on a page.
