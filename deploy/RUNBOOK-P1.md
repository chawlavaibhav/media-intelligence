# P1 operator runbook

## Install (fresh VM, root)

```
REF=claude/confident-franklin-s1v8ln ./deploy/install.sh     # apt deps, user `mi`, /srv/mi, systemd units, smoke test
```
The install runs `python3 -m product.smoke` **before** enabling the services. It must print three PASS lines
(media engine on this host, dry image + film jobs, backup/restore). Do not take traffic on a FAIL.

Then: edit `/etc/mi/mi.env` (hostname, keys), copy `deploy/Caddyfile` to `/etc/caddy/Caddyfile` with the real
hostname, `systemctl reload caddy`, and then **the founder** creates the founder account:

```
sudo -u mi sh -c 'set -a; . /etc/mi/mi.env; PYTHONPATH=/srv/mi/app python3 -m product.admin init-founder --email founder@company'
```
The founder opens the printed link, sets the password, signs in → `/ops` → creates the customer account (per-job ceiling)
→ invites customers and any operators.

**The founder account is created and held only by the founder** (amendment 1 §6). A builder, an operator, an AI agent
or any script must never run `init-founder`, never receive the invite link, and never create, know or store the founder's
password — not in a file, an environment variable, a note or a chat. (The v1 builder held the operator login; that must
not happen again.) If anyone else ever held it, the founder resets it. Operators get their own accounts by invitation:
they can see and pause jobs, never decide.

## Modes

| Setting | Effect |
|---|---|
| `MI_PROVIDER_MODE=simulated` | no image/video/music call can leave the host; test media; USD 0 |
| `MI_REASONING_MODE=simulated` | no model call leaves the host; deterministic stand-ins |
| `live` (either) | real calls, each one reserved against the job's authorised budget first |
| `MI_HOLD_BEFORE_PREVIEW=1` | the founder chooses to look first: every finished cut waits in `operator_hold` until the founder releases it. Off by default |

Nobody waits for the founder (amendment 1 §3). An unqualified judge's "pass" is not evidence, so those checks go to the
customer: the preview says the customer's look is the final check, and their acceptance is recorded against each one.
A **measured** check (code on the exact file) that fails still never reaches the customer: the kitchen repairs it
automatically (2 rounds, within the approved budget), then asks the customer to stop or pay for a rework.

## Daily operation

- `/ops` lists every job and its state; a paused/failed job shows its reason.
- `/ops/jobs/<id>`: brief (frozen), intent, direction, pre-spend review, Canon trace, asset graph, ledger,
  reasoning calls (with the context each saw), assets, gateway table, metrics, event log.
- **Held before preview** (`operator_hold`, only when the founder switched the hold on): the founder looks at the media,
  waives a measured row only with a real reason, and releases. Waivers are recorded against the exact file version.
- **needs_customer_decision**: a measured check still fails after the automatic repairs; the customer chooses stop or
  a paid rework on their job page. Nothing to do unless they ask.
- **Weekly**: the founder reads `/ops/digest` — what the kitchen learned by itself, with Undo per item — and decides the
  lessons that touch money, overrides or safety (the only ones that wait).
- **paused_budget**: the customer raises the budget on their page (or the operator asks them to). Never raise
  a customer's budget on their behalf.
- **paused_provider**: retried automatically after 60 s. Persistent failures: check provider status / credit pools.
- **failed** (an internal error — a bug, not a decision): read the reason in the event log; fix; the founder resumes
  (goes back to the recorded state). The customer can always close a failed job themselves.

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
