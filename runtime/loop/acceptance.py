"""Human acceptance (C-8): pending_human -> accepted | rejected | repair_requested, and nothing else.

WHAT IT ENFORCES, AND WHERE EACH RULE COMES FROM:
- `acceptance_authority` is read from the profile row; only "human" can be satisfied here, by a
  person's name as a plain string. A `by` that starts with "judge:" or "model:", is empty, or is
  not a string is refused (ACCEPTANCE_AUTOMATED_JUDGE). `automated_judge_in_release_path` is read
  and must be False (the qualification report EVAL-040 is why; POLICY-PROFILES.yaml note).
- There is NO transition to "delivered" in TRANSITIONS. Delivery is recorded only by an explicit
  `release(by=<person>)`, which requires state accepted, `autonomous_external_delivery` False and
  `human_approval_required_before_external_delivery` True — the two C-8 flags, read from the row.
- `abandon()` is the runtime's own exit (repair allowance exhausted, pre-dispatch block, no artifact
  to judge). It is a terminal state, never an acceptance, and carries no person.
- Every transition is appended to `transcript` with its UTC; `transcript_sha256` goes into the
  outcome event so the event can prove what was recorded.
"""
from __future__ import annotations

import json

from runtime.errors import Refusal
from runtime.loop import refusals
from runtime.util import sha256_obj

PENDING, ACCEPTED, REJECTED, REPAIR_REQUESTED, ABANDONED, DELIVERED = (
    "pending_human", "accepted", "rejected", "repair_requested", "abandoned", "delivered")
DECISIONS = (ACCEPTED, REJECTED, REPAIR_REQUESTED)
# state -> states a recorded DECISION or runtime exit may move to. "delivered" is deliberately
# absent: only release() reaches it, and release() is not a decision.
TRANSITIONS = {
    PENDING: (ACCEPTED, REJECTED, REPAIR_REQUESTED, ABANDONED),
    REPAIR_REQUESTED: (PENDING, ABANDONED),
    ACCEPTED: (),
    REJECTED: (),
    ABANDONED: (),
    DELIVERED: (),
}
TERMINAL_DECISION = {ACCEPTED: "accepted", REJECTED: "rejected", ABANDONED: "abandoned",
                     DELIVERED: "accepted"}
AUTOMATED_PREFIXES = ("judge:", "model:")


def _person(by) -> str:
    if not isinstance(by, str) or not by.strip():
        raise Refusal(refusals.ACCEPTANCE_AUTOMATED_JUDGE,
                      "an acceptance decision is recorded by a person named as a plain string; an "
                      "object or an empty name is not a person", got=repr(by))
    if by.strip().lower().startswith(AUTOMATED_PREFIXES):
        raise Refusal(refusals.ACCEPTANCE_AUTOMATED_JUDGE,
                      "an automated judge may not decide acceptance under this profile "
                      "(automated_judge_in_release_path is false; C-8)", by=by)
    return by.strip()


class Acceptance:
    def __init__(self, profile):
        self.profile = profile
        self.authority = str(profile.limit("acceptance_authority"))
        self.state = PENDING
        self.transcript: list = []
        self.delivered: dict | None = None

    # ── guards ──────────────────────────────────────────────────────────
    def _assert_human_authority(self):
        if self.authority != "human":
            raise Refusal(refusals.ACCEPTANCE_AUTHORITY_MISMATCH,
                          f"profile {getattr(self.profile, 'name', '?')!r} names acceptance_authority "
                          f"{self.authority!r}; this state machine records decisions only under a "
                          f"human authority", authority=self.authority)
        if bool(self.profile.limit("automated_judge_in_release_path")) is not False:
            raise Refusal(refusals.ACCEPTANCE_AUTOMATED_JUDGE,
                          "automated_judge_in_release_path is not false in the profile row; no "
                          "decision is recorded until it is", profile=getattr(self.profile, "name", "?"))

    def _move(self, to: str, *, decision, by, note, utc, contract_lines_failed=None):
        if to not in TRANSITIONS[self.state]:
            raise Refusal(refusals.ACCEPTANCE_INVALID_TRANSITION,
                          f"no transition {self.state} -> {to}", state=self.state, to=to)
        entry = {"from": self.state, "to": to, "decision": decision, "by": by, "note": note or "",
                 "utc": str(utc)}
        if contract_lines_failed is not None:
            entry["contract_lines_failed"] = [str(l) for l in contract_lines_failed]
        self.transcript.append(entry)
        self.state = to

    # ── transitions ─────────────────────────────────────────────────────
    def record(self, decision: str, by, note: str, utc: str, contract_lines_failed=None) -> dict:
        self._assert_human_authority()
        if decision not in DECISIONS:
            raise Refusal(refusals.ACCEPTANCE_DECISION_UNKNOWN,
                          f"decision must be one of {DECISIONS}; 'delivered' is not a decision, it is "
                          f"recorded by release()", got=decision)
        person = _person(by)
        self._move(decision, decision=decision, by=person, note=note, utc=utc,
                   contract_lines_failed=contract_lines_failed)
        return self.transcript[-1]

    def reopen(self, utc: str, note: str) -> dict:
        """repair_requested -> pending_human, when the repair draw is in front of the person."""
        self._move(PENDING, decision=None, by="runtime", note=note, utc=utc)
        return self.transcript[-1]

    def abandon(self, utc: str, reason: str) -> dict:
        self._move(ABANDONED, decision="abandoned", by="runtime", note=reason, utc=utc)
        return self.transcript[-1]

    def release(self, by, utc: str, *, artifact_sha256: str, content_type: str) -> dict:
        if self.state != ACCEPTED:
            raise Refusal(refusals.ACCEPTANCE_INVALID_TRANSITION,
                          "release requires state accepted", state=self.state)
        person = _person(by)
        if bool(self.profile.limit("autonomous_external_delivery")) is not False or \
                bool(self.profile.limit("human_approval_required_before_external_delivery")) is not True:
            raise Refusal(refusals.ACCEPTANCE_NO_AUTONOMOUS_DELIVERY,
                          "release is recorded only under a profile with autonomous_external_delivery "
                          "false and human_approval_required_before_external_delivery true (C-8)",
                          profile=getattr(self.profile, "name", "?"))
        self.delivered = {"artifact_sha256": str(artifact_sha256), "content_type": str(content_type),
                          "delivered_utc": str(utc), "released_by": person}
        self.transcript.append({"from": self.state, "to": DELIVERED, "decision": None, "by": person,
                                "note": "released by explicit human action", "utc": str(utc)})
        self.state = DELIVERED
        return dict(self.delivered)

    # ── views ───────────────────────────────────────────────────────────
    @property
    def transcript_sha256(self) -> str:
        return sha256_obj(self.transcript)

    def transcript_json(self) -> str:
        return json.dumps(self.transcript, ensure_ascii=False, indent=2)

    def to_event(self) -> dict:
        """The OUTCOME-EVENT acceptance block. Only a terminal state is an event."""
        if self.state not in TERMINAL_DECISION:
            raise Refusal(refusals.ACCEPTANCE_INVALID_TRANSITION,
                          "the acceptance is not terminal; no outcome event can be written yet",
                          state=self.state)
        last = next((t for t in reversed(self.transcript) if t.get("decision")), None)
        out = {"authority": self.authority, "decision": TERMINAL_DECISION[self.state],
               "decided_utc": last["utc"] if last else self.transcript[-1]["utc"],
               "transcript_sha256": self.transcript_sha256, "state": self.state}
        if last and last.get("note"):
            out["note"] = last["note"]
        if last and last.get("contract_lines_failed") is not None:
            out["contract_lines_failed"] = list(last["contract_lines_failed"])
        if self.state in (ACCEPTED, REJECTED, DELIVERED) and last:
            out["decided_by"] = last["by"]
        return out
