"""The flow (spec §6): the persisted state machine, the send-back rules (the dashed lines of the structure diagram) and
their limits. Code holds the state; stations do the work; every state change is an event with actor and reason.

Two kinds of exit need the founder (spec §6.4) and the store refuses them without a founder proof (authority.py):
  - leaving `paused_for_founder`, `failed` or `paused_operator` (a person decides what happens next), and
  - `operator_hold -> ready_for_review` (releasing a file to the customer).
Pausing is open to the system and to any operator; deciding is not.

Amendment 1 §3 (founder decision 2026-09-23): nobody waits for the founder. Every send-back limit ends with the SYSTEM
(a safer plan, a safer route, an automatic repair) and then the CUSTOMER (accept as is / change / stop) — never in a
founder-only state. The founder-only states remain for a founder who CHOOSES to intervene (pausing a job, switching the
hold before preview on), and every founder override stays available; none is ever required.
"""
from __future__ import annotations

import json

# state -> (creative stage 1..5, customer-facing label, who acts)
STATES = {
    "submitted":                (1, "Understanding your brief", "worker"),
    "understanding":            (1, "Understanding your brief", "worker"),
    "needs_answers":            (1, "A few questions for you", "customer"),
    "refused":                  (1, "We can't take this one on", "none"),
    "feasibility":              (2, "Checking we can make it", "worker"),
    "awaiting_customer_input":  (2, "We need something from you", "customer"),
    "directing":                (3, "Developing the creative plan", "worker"),
    "awaiting_approval":        (3, "Creative plan ready for your approval", "customer"),
    "planning":                 (4, "Preparing production", "worker"),
    "producing":                (5, "Producing", "worker"),
    "awaiting_master_approval": (5, "Approve the look of your film", "customer"),
    "awaiting_taste":           (5, "Taste the first shot of your film", "customer"),
    "checking":                 (5, "Checking the work", "worker"),
    "needs_customer_decision":  (5, "A check failed — your decision is needed", "customer"),
    "operator_hold":            (5, "Final quality check by our team", "founder"),
    "ready_for_review":         (5, "Ready for your review", "customer"),
    "revising":                 (5, "Making your changes", "worker"),
    "accepted":                 (5, "Delivered", "none"),
    "rejected":                 (5, "Closed (rejected)", "none"),
    "abandoned":                (5, "Closed", "none"),
    "paused_budget":            (5, "Paused — needs more budget", "customer"),
    "paused_provider":          (5, "Paused — a production service is unavailable; retrying", "worker"),
    "paused_operator":          (5, "Paused by our team", "founder"),
    "paused_for_founder":       (5, "Our team is reviewing a decision", "founder"),
    "failed":                   (5, "Stopped — our team has been notified", "founder"),
}

WORKER_STATES = ("submitted", "understanding", "feasibility", "directing", "planning", "producing", "checking", "revising",
                 "paused_provider")
CUSTOMER_STATES = ("needs_answers", "awaiting_customer_input", "awaiting_approval", "awaiting_master_approval", "awaiting_taste",
                   "ready_for_review", "paused_budget", "needs_customer_decision")
TERMINAL = ("accepted", "rejected", "refused", "abandoned")
PAUSES = ("paused_budget", "paused_provider", "paused_operator", "paused_for_founder")

# Leaving these states is a founder decision (authority.py mints the proof; store.transition checks it).
FOUNDER_ONLY_FROM = ("paused_for_founder", "failed", "paused_operator")
FOUNDER_ONLY_EDGES = {("operator_hold", "ready_for_review")}

RAIL = [
    ("Understanding", ("submitted", "understanding", "needs_answers")),
    ("Checking we can make it", ("feasibility", "awaiting_customer_input")),
    ("Creative plan", ("directing", "awaiting_approval")),
    ("Producing", ("planning", "producing", "awaiting_master_approval", "awaiting_taste", "revising")),
    ("Checking", ("checking", "operator_hold", "needs_customer_decision")),
    ("Ready for review", ("ready_for_review", "accepted")),
]

_WORK = {"understanding", "feasibility", "directing", "planning", "producing", "checking", "revising"}
_WAITS = {"needs_answers", "awaiting_customer_input", "awaiting_approval", "awaiting_master_approval", "awaiting_taste"}

ALLOWED = {
    "submitted": {"understanding", "failed", "paused_operator"},
    "understanding": {"needs_answers", "refused", "feasibility", "failed", "paused_budget", "paused_operator", "paused_provider",
                      "paused_for_founder"},
    "needs_answers": {"understanding", "paused_operator", "rejected", "abandoned"},
    "feasibility": {"awaiting_customer_input", "directing", "failed", "paused_budget", "paused_operator", "paused_provider",
                    "paused_for_founder"},
    "awaiting_customer_input": {"understanding", "abandoned", "paused_operator"},
    "directing": {"awaiting_approval", "planning", "paused_for_founder", "failed", "paused_budget", "paused_operator",
                  "paused_provider", "refused"},
    "awaiting_approval": {"directing", "planning", "rejected", "abandoned", "paused_operator"},
    "planning": {"producing", "failed", "paused_budget", "paused_operator", "paused_provider"},
    "producing": {"awaiting_master_approval", "awaiting_taste", "checking", "directing", "paused_for_founder", "failed", "paused_budget",
                  "paused_provider", "paused_operator"},
    "awaiting_master_approval": {"producing", "abandoned", "paused_operator", "paused_for_founder"},
    "awaiting_taste": {"producing", "abandoned", "paused_operator"},
    "checking": {"producing", "directing", "operator_hold", "ready_for_review", "needs_customer_decision", "paused_for_founder",
                 "failed", "paused_budget", "paused_provider", "paused_operator"},
    "needs_customer_decision": {"producing", "abandoned", "paused_operator"},
    "operator_hold": {"ready_for_review", "producing", "paused_operator", "paused_for_founder", "failed", "abandoned"},
    "ready_for_review": {"accepted", "revising", "rejected", "abandoned", "paused_operator"},
    "revising": {"producing", "directing", "failed", "paused_budget", "paused_operator", "paused_provider", "paused_for_founder"},
    "paused_budget": _WORK | {"rejected", "abandoned", "paused_operator"},
    "paused_provider": _WORK | {"failed", "paused_operator"},
    # a pause never skips a check: resuming goes back to work, to a customer wait, or to the founder's hold — never
    # straight to the customer's review (that is operator_hold -> ready_for_review, founder only)
    "paused_operator": _WORK | _WAITS | {"operator_hold", "paused_for_founder", "abandoned", "rejected"},
    "paused_for_founder": _WORK | _WAITS | {"operator_hold", "paused_operator", "abandoned", "rejected"},
    "failed": _WORK | {"paused_operator", "paused_for_founder", "abandoned", "rejected"},
    "accepted": set(), "rejected": set(), "refused": set(), "abandoned": set(),
}


def can(frm: str, to: str) -> bool:
    return to in ALLOWED.get(frm, set())


# A customer may always walk away from a stopped job (amendment 1 §3: a job never waits on the founder to be closed).
CUSTOMER_EXITS = {("failed", "abandoned")}


def needs_founder(frm: str, to: str) -> bool:
    if (frm, to) in CUSTOMER_EXITS:
        return False
    return frm in FOUNDER_ONLY_FROM or (frm, to) in FOUNDER_ONLY_EDGES


def label(state: str) -> str:
    return STATES[state][1]


def rail_position(state: str, resume_state: str | None = None) -> int:
    s = resume_state if state in PAUSES and resume_state else state
    for i, (_, members) in enumerate(RAIL):
        if s in members:
            return i
    return len(RAIL) - 1


# ── send-back rules (spec §6.2) — data, read by the stations and shown on the operator pages ──────────────────────
SEND_BACKS = [
    {"id": "SB-WAITER-QUESTIONS", "from": "waiter", "when": "ambiguity or missing must-have information",
     "to": "customer (questions)", "limit": 1, "limit_note": "at most 5 questions, asked once", "then": "decide with the stated defaults"},
    {"id": "SB-PANTRY-NEED-INPUT", "from": "pantry_checker", "when": "verdict need_input",
     "to": "customer (photo or fact request)", "limit": None, "limit_note": "the job pauses; USD 0 spent", "then": "—"},
    {"id": "SB-PANTRY-CANNOT", "from": "pantry_checker", "when": "verdict cannot_make",
     "to": "waiter -> customer with alternatives", "limit": None, "limit_note": "—", "then": "—"},
    {"id": "SB-RECIPE", "from": "recipe_checker", "when": "send_back", "to": "chef", "limit": 2,
     "limit_note": "2 rounds (per plan cycle: a customer change or a big-taster re-plan starts a new cycle)", "then": "SB-RECIPE-SAFE"},
    {"id": "SB-RECIPE-SAFE", "from": "system", "when": "the recipe checker sent the recipe back twice",
     "to": "system: the pantry checker's safest alternative for the problem shots, re-checked once", "limit": 1,
     "limit_note": "1 per plan cycle",
     "then": "customer: sees the objections in plain words and chooses go ahead / change the brief / stop (USD 0 spent)"},
    {"id": "SB-TASTER-RETRY", "from": "small_taster", "when": "output rejected", "to": "head cook retries that output",
     "limit": 2, "limit_note": "2 attempts per output, each retry changes something", "then": "SB-TASTER-REPLAN"},
    {"id": "SB-TASTER-REPLAN", "from": "small_taster", "when": "2 rejected attempts on one output",
     "to": "chef re-plans that shot (route/action change)", "limit": 1, "limit_note": "1 re-plan per shot",
     "then": "system: the shot switches to FILM-A (a still with code motion); the customer's preview notes it"},
    {"id": "SB-BIG-FIX", "from": "big_taster / door guard", "when": "verdict fix, or a measured check FAILED",
     "to": "system: automatic repair of only the named shots (or the failing files), within the approved budget",
     "limit": 2, "limit_note": "2 rounds; the approved budget is never exceeded (out of budget = paused_budget, the customer decides)",
     "then": "SB-BIG-STOP"},
    {"id": "SB-BIG-FAIL", "from": "big_taster", "when": "verdict fail with earliest_stage plan", "to": "chef (a new plan for the customer)",
     "limit": 1, "limit_note": "1 round", "then": "SB-BIG-STOP"},
    {"id": "SB-BIG-STOP", "from": "big_taster / door guard", "when": "fail again, or repairs used up",
     "to": "customer: sees the film with the plain report — accept as is / changes (priced) / reject; a measured FAIL "
           "never ships: the customer is told what failed and chooses stop or paid rework",
     "limit": 0, "limit_note": "the customer decides", "then": "—"},
    {"id": "SB-CUSTOMER-CHANGE", "from": "customer", "when": "change request",
     "to": "waiter classifies -> the affected station only", "limit": None, "limit_note": "per quote", "then": "—"},
]
RULES = {r["id"]: r for r in SEND_BACKS}


class LimitReached(Exception):
    def __init__(self, rule_id: str, key: str | None, used: int):
        self.rule_id, self.key, self.used = rule_id, key, used
        r = RULES[rule_id]
        super().__init__(f"{rule_id} ({r['from']} → {r['to']}): limit {r['limit_note']} reached"
                         + (f" for {key}" if key else ""))


def rounds_used(store, job_id: str, rule_id: str, key: str | None = None) -> int:
    n = 0
    for e in store.events(job_id, ("send_back",)):
        d = json.loads(e["data_json"])
        if d.get("rule") == rule_id and (key is None or d.get("key") == key):
            n += 1
    return n


def send_back(store, job_id: str, rule_id: str, *, key: str | None = None, actor: str = "system", why: str = "") -> int:
    """Record one use of a send-back route. Raises LimitReached (and records nothing) when the limit is used up."""
    rule = RULES[rule_id]
    used = rounds_used(store, job_id, rule_id, key)
    if rule["limit"] is not None and used >= rule["limit"]:
        raise LimitReached(rule_id, key, used)
    store.event(job_id, actor, "send_back", {"rule": rule_id, "key": key, "round": used + 1, "to": rule["to"], "why": why[:600]})
    return used + 1
