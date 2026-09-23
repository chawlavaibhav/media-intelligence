# Media Intelligence P1 v2 — the product

Built to `coordination/p1-v2/P1-V2-BUILD-SPEC.md`; judged by `coordination/p1-v2/P1-V2-FOUNDER-CHECKLIST.md`.
Defaults are `MI_PROVIDER_MODE=simulated` and `MI_REASONING_MODE=simulated`: nothing paid can leave the host.

## Reproduce from a fresh checkout (USD 0)

```
git clone https://github.com/chawlavaibhav/media-intelligence && cd media-intelligence && git checkout claude/p1-v2-build
python3 -m venv .venv && .venv/bin/pip install -r deploy/requirements.txt      # plus ffmpeg, Pillow with raqm, fonts-noto-core and librsvg2-bin (Debian/Ubuntu apt names)
PYTHONPATH=. .venv/bin/python -m unittest discover -s product/tests -t .       # every test, v2 and v1 (~25-30 min)
PYTHONPATH=. .venv/bin/python -m product.smoke                                  # media engine + dry jobs + backup/restore
PYTHONPATH=. .venv/bin/python -m product.qualification.judges                   # judges' harness, simulated (qualifies nothing)
# optional: clone the private evidence repo next to this one (../mi-p1-evidence) to also run the checks on the
# verbatim 23-September records and to give the judges' harness its 14 cases
MI_DATA_DIR=/tmp/mi .venv/bin/python -m product.admin init-founder --email you@example.com   # once; prints an invite link
MI_DATA_DIR=/tmp/mi .venv/bin/python -m product.web.app --port 8080 &   MI_DATA_DIR=/tmp/mi .venv/bin/python -m product.worker &
```

## Layout (spec §12)

| Where | What |
|---|---|
| `flow.py` (`states.py` re-exports it) | states, founder-only exits, the send-back table and its limits (§6) |
| `orchestrator.py` | the small flow controller: one station per state; customer and founder decisions |
| `stations/waiter.py` `pantry.py` `chef.py` `recipe_check.py` `head_cook.py` `assembly.py` `tasters.py` `changes.py` `diary.py` | one module per worker (§3) |
| `stations/simulated.py` | deterministic stand-ins for the seven AI workers (tests and dry runs only) |
| `ai.py` | every AI call: card + form schema + the customer's exact words + input forms + tray; records card version, tray, estimated cost |
| `rulebook/` | worker cards (mission, vision, KRA, instructions) and form schemas as versioned data (§4, §5, §7.4) |
| `library/` | equipment sheet, failure diary, recipe library, Canon pages, the librarian's trays (§7.3, §8) |
| `shelf/` | the customer shelf (§7.2) |
| `lessons/` | the lesson queue; founder approves, edits or rejects (§7.5) |
| `authority.py` | only a signed-in founder session can override, pick a take, release, resume or decide a lesson (§6.4) |
| `cost.py` | the quote's reasoning line and the per-worker reasoning report (§9.4) |
| `qualification/judges.py` | the judges' qualification harness (§10) |
| `store.py` `dispatch.py` `providers.py` `media.py` `compose.py` `verify.py` `web/` `admin.py` | kept from v1 and adapted |
