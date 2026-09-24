"""The job state machine. Five creative stages; as many technical states as the work needs.

Worker states are advanced by the orchestrator; customer states wait for a person; pause states wait
for a named condition (budget, provider, operator). Every transition is a compare-and-set in the
store, so a restarted worker can never apply a step twice.
"""
from __future__ import annotations

# state -> (creative stage 1..5, customer-facing label, who acts)
STATES = {
    "submitted":          (1, "Understanding your brief", "worker"),
    "understanding":      (1, "Understanding your brief", "worker"),
    "needs_answers":      (1, "A few questions for you", "customer"),
    "refused":            (1, "We can't take this one on", "none"),
    "directing":          (3, "Developing the creative direction", "worker"),
    "awaiting_approval":  (3, "Creative direction ready for your approval", "customer"),
    "planning":           (4, "Preparing production", "worker"),
    "producing":          (5, "Producing", "worker"),
    "checking":           (5, "Checking the work", "worker"),
    "operator_hold":      (5, "Final quality review", "operator"),
    "ready_for_review":   (5, "Ready for your review", "customer"),
    "revising":           (5, "Making your changes", "worker"),
    "accepted":           (5, "Delivered", "none"),
    "rejected":           (5, "Closed (rejected)", "none"),
    "paused_budget":      (5, "Paused — needs more budget", "customer"),
    "paused_provider":    (5, "Paused — a production service is unavailable; retrying", "worker"),
    "paused_operator":    (5, "Paused by our team", "operator"),
    "failed":             (5, "Stopped — our team has been notified", "operator"),
}

WORKER_STATES = ("submitted", "understanding", "directing", "planning", "producing", "checking", "revising",
                 "paused_provider")
CUSTOMER_STATES = ("needs_answers", "awaiting_approval", "ready_for_review", "paused_budget")
TERMINAL = ("accepted", "rejected", "refused")
PAUSES = ("paused_budget", "paused_provider", "paused_operator")

# The customer progress rail (Understanding → Creative direction → Preparing assets → Producing → Checking → Ready)
RAIL = [
    ("Understanding", ("submitted", "understanding", "needs_answers")),
    ("Creative direction", ("directing", "awaiting_approval")),
    ("Preparing assets", ("planning",)),
    ("Producing", ("producing", "revising")),
    ("Checking", ("checking", "operator_hold")),
    ("Ready for review", ("ready_for_review", "accepted")),
]

ALLOWED = {
    "submitted": {"understanding", "failed", "paused_operator"},
    "understanding": {"needs_answers", "refused", "directing", "failed", "paused_budget", "paused_operator", "paused_provider"},
    "needs_answers": {"understanding", "paused_operator", "rejected"},
    "directing": {"awaiting_approval", "planning", "failed", "paused_budget", "paused_operator", "paused_provider", "refused"},
    "awaiting_approval": {"directing", "planning", "rejected", "paused_operator"},
    "planning": {"producing", "failed", "paused_budget", "paused_operator", "paused_provider"},
    "producing": {"checking", "failed", "paused_budget", "paused_provider", "paused_operator"},
    "checking": {"producing", "operator_hold", "ready_for_review", "failed", "paused_budget", "paused_provider", "paused_operator"},
    "operator_hold": {"ready_for_review", "producing", "paused_operator", "failed"},
    "ready_for_review": {"accepted", "revising", "rejected", "directing", "paused_operator"},
    "revising": {"producing", "directing", "failed", "paused_budget", "paused_operator", "paused_provider"},
    "paused_budget": {"understanding", "directing", "planning", "producing", "checking", "revising", "rejected", "paused_operator"},
    "paused_provider": {"understanding", "directing", "planning", "producing", "checking", "revising", "failed", "paused_operator"},
    "paused_operator": set(STATES) - {"paused_operator"},
    "failed": {"understanding", "directing", "planning", "producing", "checking", "revising", "paused_operator", "rejected"},
    "accepted": set(), "rejected": set(), "refused": set(),
}


def can(frm: str, to: str) -> bool:
    return to in ALLOWED.get(frm, set())


def label(state: str) -> str:
    return STATES[state][1]


def rail_position(state: str, resume_state: str | None = None) -> int:
    s = resume_state if state in PAUSES and resume_state else state
    for i, (_, members) in enumerate(RAIL):
        if s in members:
            return i
    return len(RAIL) - 1
