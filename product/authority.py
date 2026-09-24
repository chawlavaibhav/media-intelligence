"""Founder-only authority (spec §0 rule 4, §6.4).

A small-taster "no", a recipe-checker `send_back`, a big-taster `fail`/`fix`, a door-guard block, a take choice, a
release to the customer, and leaving a founder pause can be decided ONLY by a signed-in user whose role is `founder`,
with a written reason. There is no environment flag, admin command, worker path or actor string that does it.

How it is enforced:
  1. Every override entry point takes a web SESSION TOKEN, never a name. `founder_proof()` resolves the token against the
     sessions table; only a live session of a `founder` user yields a `FounderProof`. Anything else — the worker
     process, a script, the admin CLI, an AI worker, "operator:claude…" — is refused and the refusal is logged as an
     event on the job.
  2. The store re-checks the proof (the session hash must still exist, unexpired, for a founder user) before it writes a
     founder-only state change (store.transition) or an override row (store.add_override).
  3. The door guard (verify.gateway) counts a waiver only when its override row names a founder user; a waiver written any
     other way is ignored and shown as ignored.
Anyone with write access to the database file itself can still forge rows; that is outside what application code can
prevent and is why the database lives on the founder's machine or VM only.
"""
from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass

MIN_REASON = 15


class NotFounder(PermissionError):
    pass


@dataclass(frozen=True)
class FounderProof:
    user_id: str
    email: str
    session_hash: str

    @property
    def actor(self) -> str:
        return f"founder:{self.email}"


def _hash(tok: str) -> str:
    return hashlib.sha256(tok.encode()).hexdigest()


def founder_proof(store, session_token, *, job_id: str | None = None, action: str = "override") -> FounderProof:
    """The only way to obtain a FounderProof. Refusals are logged on the job."""
    who = "unknown"
    if isinstance(session_token, str) and session_token:
        row = store.q1("SELECT s.user_id, s.expires, s.token_hash, u.role, u.email FROM sessions s JOIN users u ON u.id=s.user_id "
                       "WHERE s.token_hash=?", (_hash(session_token),))
        if row and row["expires"] >= time.time() and row["role"] == "founder":
            return FounderProof(row["user_id"], row["email"], row["token_hash"])
        who = (f"{row['role']}:{row['email']}" if row else f"not a signed-in session ({str(session_token)[:40]})")
    else:
        who = f"not a session token ({type(session_token).__name__}: {str(session_token)[:40]})"
    if job_id:
        store.event(job_id, who, "override_refused", {"action": action, "why": "only the founder, signed in, can do this"})
    raise NotFounder(f"refused: only the founder can {action} (caller: {who})")


def verify_proof(store, proof) -> bool:
    """Store-side re-check: the proof must still correspond to a live founder session."""
    if not isinstance(proof, FounderProof):
        return False
    row = store.q1("SELECT s.expires, u.role FROM sessions s JOIN users u ON u.id=s.user_id WHERE s.token_hash=? AND s.user_id=?",
                   (proof.session_hash, proof.user_id))
    return bool(row and row["role"] == "founder" and row["expires"] >= time.time())


def check_reason(reason: str) -> str:
    r = (reason or "").strip()
    if len(r) < MIN_REASON:
        raise ValueError(f"an override needs a written reason a colleague could audit (at least {MIN_REASON} characters)")
    return r


def is_founder_user(store, user_id: str | None) -> bool:
    if not user_id:
        return False
    u = store.user(user_id)
    return bool(u and u["role"] == "founder")
