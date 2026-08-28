#!/usr/bin/env python3
"""EVAL-035 (corrected): machine-verifiable, fail-closed spend authority for PILOT-001.

WHY THE FIRST PASS WAS REJECTED

    The first-pass gate verified only that a local YAML file pointed at SOME existing file
    under coordination/decisions/. Its own test proved a local file referencing a
    NON-authorising decision could open a live guard. The Controller ruled that unacceptable
    (`CONTROLLER-EVAL-035-RETURN-REVIEW-2026-08-28.md`, correction 2): decision-file
    existence is not authority.

THE CORRECTED CHAIN — TWO DOCUMENTS THAT MUST MECHANICALLY AGREE

    1. A COMMITTED Controller decision under coordination/decisions/ that carries an
       explicit machine-readable authorisation block (fenced ```yaml with a top-level
       `machine_authorisation` mapping) naming: tranche `PILOT-001`, `authorised: true`
       (the boolean), a positive spend cap, `retries_authorised: 0`, and approval
       identity/date. Prose approval is not enough — the block is the deterministic,
       parseable statement of authority. No such decision exists in the repository today,
       so this gate CANNOT open from committed state, and a test proves that.

    2. A LOCAL, git-ignored runtime file (`authorization.pilot.local.yaml`) the human
       materialises at execution time, which must MATCH the committed authority: same
       tranche, a ceiling no greater than the committed cap, the same zero-retry policy,
       and its own approval identity/date. A locally edited YAML alone can therefore never
       manufacture spend authority: without the matching committed Controller block it is
       refused, whatever it says.

    This module verifies PERMISSION only. The live spend guard is the persistent
    append-only run ledger in `pilot_spend_ledger.py` (`open_pilot_runtime`), which calls
    `verify_authority` before touching any money state — an in-memory guard is never the
    pilot's spend history (EMP-001 lesson), and Resources requires a durable `cost_ref`.

    This module DEFINES the record format (explicitly permitted by the review decision); it
    does not create authority. No decision is written here, and the committed state must
    keep failing until a future Controller decision — after explicit user approval —
    supplies the matching block.
"""
from __future__ import annotations

import re
import sys
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
EMP001 = HERE.parent / "empirical-tranche-1"
if str(EMP001) not in sys.path:
    sys.path.insert(0, str(EMP001))

from budget_guard import NotAuthorised  # noqa: E402

PILOT_TRANCHE_ID = "PILOT-001"
PILOT_AUTHORISATION_PATH = HERE / "authorization.pilot.local.yaml"
DECISIONS_DIR = REPO_ROOT / "coordination" / "decisions"
RETRIES_AUTHORISED = 0

_FENCED_YAML = re.compile(r"```yaml\s*\n(.*?)```", re.DOTALL)


def _load_yaml(text: str):
    import yaml

    return yaml.safe_load(text)


# ------------------------------------------------- 1. the committed Controller authority
def read_committed_authority(decision_path: Path) -> tuple[dict | None, list[str]]:
    """Parse a committed Controller decision for its machine_authorisation block.

    Returns (authority, refusals). `authority` is the validated block or None. Every
    defect is listed rather than summarised, so a refusal explains itself completely.
    """
    refusals: list[str] = []
    if not decision_path.exists():
        return None, [f"decision file {decision_path} does not exist in this repository"]

    text = decision_path.read_text(encoding="utf-8")
    blocks = []
    for match in _FENCED_YAML.finditer(text):
        try:
            data = _load_yaml(match.group(1))
        except Exception:
            continue
        if isinstance(data, dict) and "machine_authorisation" in data:
            blocks.append(data["machine_authorisation"])

    if not blocks:
        return None, [
            f"{decision_path.name} contains no machine_authorisation block. A Controller "
            f"decision authorises spend only when it carries the explicit "
            f"machine-readable authorisation record; prose (or mere existence of the "
            f"file) is not machine-verifiable authority."]
    if len(blocks) > 1:
        return None, [f"{decision_path.name} contains {len(blocks)} machine_authorisation "
                      f"blocks; an ambiguous authority is no authority"]

    auth = blocks[0]
    if not isinstance(auth, dict):
        return None, [f"{decision_path.name}: machine_authorisation is not a mapping"]

    if auth.get("authorised") is not True:
        refusals.append(f"committed authorised is {auth.get('authorised')!r}, "
                        f"not the boolean true")
    if auth.get("tranche_id") != PILOT_TRANCHE_ID:
        refusals.append(f"committed tranche_id is {auth.get('tranche_id')!r}, "
                        f"expected {PILOT_TRANCHE_ID!r}")
    try:
        cap = Decimal(str(auth.get("max_consumed_api_spend_usd", 0)))
    except Exception:
        cap = Decimal("0")
        refusals.append(f"committed max_consumed_api_spend_usd "
                        f"{auth.get('max_consumed_api_spend_usd')!r} is not a number")
    else:
        if cap <= 0:
            refusals.append(f"committed max_consumed_api_spend_usd is {cap}, "
                            f"which authorises nothing")
    if auth.get("retries_authorised") != RETRIES_AUTHORISED:
        refusals.append(f"committed retries_authorised is "
                        f"{auth.get('retries_authorised')!r}; PILOT-001 authorises "
                        f"exactly {RETRIES_AUTHORISED}")
    for required in ("approved_by", "approved_at"):
        if not auth.get(required):
            refusals.append(f"committed {required} is missing — an anonymous or undated "
                            f"authority is not durable authority")

    if refusals:
        return None, refusals
    return {"tranche_id": auth["tranche_id"], "max_consumed_api_spend_usd": cap,
            "retries_authorised": auth["retries_authorised"],
            "approved_by": auth["approved_by"], "approved_at": auth["approved_at"],
            "decision_path": str(decision_path)}, []


def find_committed_authority(decisions_dir: Path = DECISIONS_DIR
                             ) -> tuple[dict | None, list[str]]:
    """Scan every committed Controller decision for a valid PILOT-001 authority block.

    Today this finds nothing — that is the correct, tested state. If more than one valid
    block ever exists, that is an authority conflict and the gate refuses.
    """
    found = []
    for path in sorted(decisions_dir.glob("*.md")):
        authority, _ = read_committed_authority(path)
        if authority:
            found.append(authority)
    if not found:
        return None, [
            f"no committed Controller decision under {decisions_dir} carries a valid "
            f"machine_authorisation block for {PILOT_TRANCHE_ID}. PILOT-001 paid "
            f"execution has not been authorised."]
    if len(found) > 1:
        return None, [f"{len(found)} committed decisions carry valid "
                      f"{PILOT_TRANCHE_ID} authority blocks "
                      f"({[a['decision_path'] for a in found]}); conflicting authority "
                      f"must be resolved by the Controller, not picked from"]
    return found[0], []


# ------------------------------------------------------- 2. the local runtime approval
def load_pilot_authorisation(path: Path | str = PILOT_AUTHORISATION_PATH,
                             decisions_dir: Path = DECISIONS_DIR) -> dict:
    """Validate the local runtime file AGAINST the committed authority.

    Never raises on a merely absent/disabled file — absence is the expected committed
    state. Returns a status dict listing every refusal reason.
    """
    path = Path(path)
    status = {"source_path": str(path), "authorised": False,
              "max_consumed_api_spend_usd": Decimal("0"),
              "committed_authority": None, "refusals": []}

    if not path.exists():
        status["refusals"].append(
            "no local PILOT-001 runtime authorisation file exists — it is materialised "
            "only from an explicit human approval at execution time")
        # Still report the committed side so the status is complete.
        committed, committed_refusals = find_committed_authority(decisions_dir)
        status["committed_authority"] = committed
        status["refusals"].extend(committed_refusals)
        return status

    data = _load_yaml(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise NotAuthorised(f"{path}: authorisation file is not a mapping")

    refusals: list[str] = []

    if data.get("authorised") is not True:
        refusals.append(f"local authorised is {data.get('authorised')!r}, "
                        f"not the boolean true")
    if data.get("tranche_id") != PILOT_TRANCHE_ID:
        refusals.append(f"local tranche_id is {data.get('tranche_id')!r}, "
                        f"expected {PILOT_TRANCHE_ID!r}")
    try:
        ceiling = Decimal(str(data.get("max_consumed_api_spend_usd", 0)))
    except Exception:
        ceiling = Decimal("0")
        refusals.append(f"local max_consumed_api_spend_usd "
                        f"{data.get('max_consumed_api_spend_usd')!r} is not a number")
    else:
        if ceiling <= 0:
            refusals.append(f"local max_consumed_api_spend_usd is {ceiling}, "
                            f"which authorises nothing")
    if data.get("retries_authorised") != RETRIES_AUTHORISED:
        refusals.append(f"local retries_authorised is "
                        f"{data.get('retries_authorised')!r}; PILOT-001 authorises "
                        f"exactly {RETRIES_AUTHORISED}")
    for required in ("approved_by", "approved_at"):
        if not data.get(required):
            refusals.append(f"local {required} is missing — an anonymous or undated "
                            f"approval is not an approval")

    # ---- the committed side: the part a local edit can never manufacture --------------
    # The local file must NAME the committed decision it enacts, and THAT decision must
    # itself carry a valid machine_authorisation block — its specific defects are surfaced
    # verbatim so a refusal explains itself.
    committed = None
    decision_ref = data.get("decision_ref")
    if not decision_ref:
        refusals.append("local decision_ref is missing — the runtime approval must "
                        "name the committed decision it enacts")
        _, scan_refusals = find_committed_authority(decisions_dir)
        refusals.extend(scan_refusals)
    else:
        ref_path = (Path(decision_ref) if Path(decision_ref).is_absolute()
                    else REPO_ROOT / decision_ref)
        try:
            inside = ref_path.resolve().is_relative_to(Path(decisions_dir).resolve())
        except AttributeError:      # pragma: no cover — Python < 3.9 has no is_relative_to
            inside = str(ref_path.resolve()).startswith(str(Path(decisions_dir).resolve()))
        if not inside:
            refusals.append(f"local decision_ref {decision_ref!r} is not under "
                            f"{decisions_dir} — only committed Controller decisions "
                            f"carry authority")
        else:
            committed, committed_refusals = read_committed_authority(ref_path)
            refusals.extend(committed_refusals)

    status["committed_authority"] = committed
    if committed:
        # A second valid committed authority elsewhere is a conflict, not a choice.
        all_found, _ = find_committed_authority(decisions_dir)
        if all_found is None:
            refusals.append("conflicting authority: more than one committed decision "
                            "carries a valid PILOT-001 machine_authorisation block; the "
                            "Controller must resolve which governs")
        if ceiling > committed["max_consumed_api_spend_usd"]:
            refusals.append(
                f"local ceiling {ceiling} exceeds the committed authorised cap "
                f"{committed['max_consumed_api_spend_usd']}; a runner may narrow an "
                f"authority, never widen it")

    status.update({"authorised": data.get("authorised") is True,
                   "max_consumed_api_spend_usd": ceiling, "refusals": refusals})
    return status


def verify_authority(path: Path | str = PILOT_AUTHORISATION_PATH,
                     decisions_dir: Path = DECISIONS_DIR) -> dict:
    """Verify the full PILOT-001 authority chain, or raise NotAuthorised with every reason.

    Returns {"max_consumed_api_spend_usd": Decimal, "committed": <committed authority>}.
    This function verifies PERMISSION only — it deliberately returns no guard object.
    The live spend guard is the persistent, append-only run ledger
    (`pilot_spend_ledger.open_pilot_runtime`), which calls this first: EMP-001 already
    paid to learn that an in-memory ceiling is a per-process ceiling wearing a tranche
    ceiling's clothes, and its `record()` returns no cost_ref for Resources to resolve.
    """
    status = load_pilot_authorisation(path, decisions_dir)
    if status["refusals"]:
        raise NotAuthorised(
            f"PILOT-001 paid execution is not authorised ({status['source_path']}):\n  - "
            + "\n  - ".join(status["refusals"]))
    return {"max_consumed_api_spend_usd": status["max_consumed_api_spend_usd"],
            "committed": status["committed_authority"]}
