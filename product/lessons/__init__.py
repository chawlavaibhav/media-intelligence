"""The lesson queue (spec §7.5, §4.11), automated by amendment 1 §4 (founder decision 2026-09-23): learning is automated.

The diary writer proposes; code classifies each proposal and applies it by kind — no founder approval needed:

  careful   equipment → risky/cannot, a failure-diary entry, a stricter check    applied immediately
  record    a recipe kept with its outcome (recipe library)                      applied immediately
  bold      equipment → reliable                                                  applied once ≥ 2 ACCEPTED jobs support it
  customer  one customer's taste or brand fact                                   applied to THAT customer's shelf only
  rulebook  rulebook card / KRA wording                                          applied as a new card version, then WATCHED:
            the next 5 jobs that use it are compared with the previous 5; acceptance down or blocking checks up →
            rolled back automatically (a new version with the old content), and the rollback is recorded
  founder_only  money limits, budgets, spend caps, who may override, safety rules, form (schema) changes, ANY change
            to a checker's card, and any other card change that edits or removes what is there (not a plain added line)
            never applied automatically; waits for the founder's weekly review (never inside a running job)

2026-09-24 (independent reviewer, founder: "do both the fixes"): the class is decided by WHAT a lesson changes, not by its
words. A word list let "let the door guard release a film with a continuity mistake for repeat customers" through because
it said none of the words. The word list stays only as an extra tripwire: a hit forces review, it never allows anything.
Retry limits (flow.SEND_BACKS) and the master-plate continuity rule (stations/recipe_check.py R3/R4) are code, so no card
wording can change them.

Every applied lesson is logged with its job, its evidence and before/after. The founder's weekly digest (/ops/digest)
lists them with an Undo per item; undo restores the exact previous version and records who undid it.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone

from product.authority import check_reason, verify_proof
from product.store import Store, new_id, sha256_json, utc_now

TARGETS = ("rulebook_card", "equipment_sheet", "recipe_library", "failure_diary", "customer_shelf", "form")
RANK = {"reliable": 0, "risky": 1, "cannot": 2}
WATCH_JOBS = 5
BOLD_SUPPORT = 2
SYSTEM = "system:auto-apply"
JUDGES = ("head_cook", "gatekeeper")          # kitchen v3: the head cook tastes; the gatekeeper checks the dish
# Every worker that checks or can block work: its card only changes at the founder's review (reviewer, 2026-09-24).
CHECKERS = JUDGES + ("head_cook_av", "door_guard", "measuring_tools")
# The only card changes code can tell are purely additive: a new KRA line, or an instruction under a NEW key.
ADDITIVE_KEYS = ("kra_add", "instructions")
# Money, spend, who may override, safety — founder only, never applied by code (amendment 1 §4, last row).
FOUNDER_ONLY_WORDS = re.compile(
    r"\b(budgets?|usd|prices?|pricing|costs?|spend(?:ing)?|caps?|ceilings?|refunds?|charges?|payments?|pay|money|dollars?|"
    r"overrid\w*|waiv\w*|who may|may override|authori[sz]\w*|permissions?|safety|safeguards?|founder)\b", re.I)


class LessonQueue:
    def __init__(self, store: Store, *, rulebook, equipment, recipes, failures, shelf):
        self.store, self.rulebook, self.equipment, self.recipes, self.failures, self.shelf = \
            store, rulebook, equipment, recipes, failures, shelf

    # ── classification ──────────────────────────────────────────────────────────────────────────────────
    def classify(self, target: str, diff: dict) -> tuple:
        """(kind, support_key). Code decides, from the target and the change itself — never the model."""
        # rules (cards, equipment) that touch money, overrides or safety are the founder's; data entries (a recipe kept, a
        # failure described, a shelf fact) may quote a customer's words about price without changing any rule
        if target == "form" or (target in ("rulebook_card", "equipment_sheet") and FOUNDER_ONLY_WORDS.search(json.dumps(diff, ensure_ascii=False))):
            return "founder_only", None
        if target == "customer_shelf":
            return "customer", None
        if target == "rulebook_card":
            # a checker's card can relax a check, and code cannot tell looser wording from stricter: the founder reviews it
            if diff.get("worker") in CHECKERS or not self._additive(diff):
                return "founder_only", None
            return "rulebook", None                            # a plain added line, then the 5-job watch
        if target == "recipe_library":
            return "record", None
        if target == "failure_diary":
            return "careful", None
        if target == "equipment_sheet":
            new = diff.get("verdict")
            if new not in RANK:
                return "careful", None                         # a note: adds evidence, relaxes nothing
            cur = self._equipment_before(diff)
            olds = [RANK.get(v["verdict"], 1) for v in cur["verdicts"]] or [1]
            if RANK[new] >= max(olds):
                return "careful", None
            return "bold", f"equipment:{diff.get('action_class')}:{','.join(sorted(cur['routes']))}:{new}"
        raise ValueError(target)

    def _additive(self, diff: dict) -> bool:
        """True only if the change adds and removes/rewrites nothing on the worker's current card."""
        changes = diff.get("changes") or {}
        if not changes or set(changes) - set(ADDITIVE_KEYS):
            return False
        if "instructions" in changes:
            new = changes["instructions"]
            try:
                cur = (self.rulebook.card(diff.get("worker")) or {}).get("instructions") or {}
            except Exception:  # noqa: BLE001 — an unknown worker is not additive
                return False
            if not isinstance(new, dict) or set(new) & set(cur):
                return False
        return True

    def _equipment_before(self, diff: dict) -> dict:
        row = next((r for r in self.equipment.rows() if r["id"] == diff.get("id")), None) if diff.get("id") else None
        routes = diff.get("routes") or (row or {}).get("routes") or ["FILM-C"]
        return {"row": row, "routes": routes,
                "verdicts": [self.equipment.verdict(diff.get("action_class") or (row or {}).get("action_class"), r) for r in routes]}

    # ── intake ──────────────────────────────────────────────────────────────────────────────────────────
    def enqueue(self, job_id: str, lessons_form: dict) -> list:
        ids = []
        for w in lessons_form.get("per_worker", []):
            pc = w.get("proposed_change")
            if not pc:
                continue
            if pc["target"] not in TARGETS:
                raise ValueError(pc["target"])
            kind, key = self.classify(pc["target"], pc["diff"])
            lid = new_id("lsn")
            with self.store.tx() as c:
                c.execute("INSERT INTO lessons (id, job_id, worker, target, proposal_json, why, evidence_json, status, created, kind, "
                          "support_key) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                          (lid, job_id, w["worker"], pc["target"], json.dumps(pc["diff"], ensure_ascii=False), pc.get("why", ""),
                           json.dumps(w.get("evidence_refs", [])), "pending", utc_now(), kind, key))
            self._process(lid)
            ids.append(lid)
        return ids

    def _process(self, lid: str):
        row = self.lesson(lid)
        kind = row["kind"]
        if kind == "founder_only":
            return self._set(lid, status="founder_only", decision_note="money, overrides or safety: only the founder decides")
        if kind == "bold":
            support = self._support(row["support_key"])
            if len(support) < BOLD_SUPPORT:
                return self._set(lid, status="waiting_support",
                                 decision_note=f"bolder change: applied once {BOLD_SUPPORT} accepted jobs support it ({len(support)} so far)")
            self._apply_auto(row, note=f"bolder change supported by {len(support)} accepted jobs: {', '.join(support)}")
            for other in self.store.q("SELECT id FROM lessons WHERE support_key=? AND status='waiting_support'", (row["support_key"],)):
                self._set(other["id"], status="applied_with_support", decided_by=SYSTEM, decided_at=utc_now(),
                          decision_note=f"applied by lesson {lid}")
            return
        note = {"careful": "more careful: applied immediately", "record": "a recipe kept with its outcome: applied immediately",
                "customer": "this customer's taste or brand fact: applied to their shelf only",
                "rulebook": f"new card version applied; the next {WATCH_JOBS} jobs are watched against the previous {WATCH_JOBS}"}[kind]
        self._apply_auto(row, note=note)

    def _support(self, key: str) -> list:
        rows = self.store.q("SELECT DISTINCT l.job_id FROM lessons l JOIN jobs j ON j.id=l.job_id WHERE l.support_key=? "
                            "AND j.outcome='accepted'", (key,))
        return [r["job_id"] for r in rows]

    def _apply_auto(self, row, *, note: str):
        applied = self._apply(row, json.loads(row["proposal_json"]), by=SYSTEM)
        watch = applied.pop("_watch", None)
        self._set(row["id"], status="applied", decided_by=SYSTEM, decided_at=utc_now(), decision_note=note,
                  applied_json=json.dumps(applied, default=str, ensure_ascii=False), watch_json=json.dumps(watch) if watch else None)
        self.store.event(row["job_id"], SYSTEM, "lesson_applied", {"lesson": row["id"], "kind": row["kind"], "target": row["target"],
                                                                   "evidence": json.loads(row["evidence_json"]), "note": note})

    def _set(self, lid, **cols):
        cols = {k: v for k, v in cols.items()}
        with self.store.tx() as c:
            c.execute(f"UPDATE lessons SET {', '.join(k + '=?' for k in cols)} WHERE id=?", (*cols.values(), lid))

    # ── reads ───────────────────────────────────────────────────────────────────────────────────────────
    def waiting(self) -> list:
        """What still needs the founder: money/override/safety lessons only."""
        return self.store.q("SELECT * FROM lessons WHERE status IN ('waiting','founder_only') ORDER BY created")

    def all(self, job_id: str | None = None) -> list:
        if job_id:
            return self.store.q("SELECT * FROM lessons WHERE job_id=? ORDER BY created", (job_id,))
        return self.store.q("SELECT * FROM lessons ORDER BY created DESC")

    def digest(self, days: int = 7) -> list:
        since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        return self.store.q("SELECT * FROM lessons WHERE created>=? OR undone_at>=? OR decided_at>=? ORDER BY created DESC",
                            (since, since, since))

    def lesson(self, lesson_id: str):
        row = self.store.q1("SELECT * FROM lessons WHERE id=?", (lesson_id,))
        if row is None:
            raise KeyError(lesson_id)
        return row

    # ── the founder: decide a founder-only lesson; undo an applied one ─────────────────────────────────
    def _founder(self, row, founder, action):
        if not verify_proof(self.store, founder):
            self.store.event(row["job_id"], getattr(founder, "actor", str(founder)[:60]), "override_refused",
                             {"action": f"{action} lesson {row['id']}", "why": "only the founder, signed in, may do this"})
            raise PermissionError(f"only the founder can {action} a lesson")

    def decide(self, lesson_id: str, *, founder, decision: str, note: str, edited_diff: dict | None = None) -> dict:
        """A lesson that waits for the founder (money, overrides, safety — or one still waiting for support): approve | edit
        (approve with the founder's edited diff) | reject. Founder only."""
        row = self.lesson(lesson_id)
        self._founder(row, founder, "decide")
        if row["status"] not in ("waiting", "founder_only", "waiting_support"):
            raise ValueError(f"lesson already {row['status']}")
        note = check_reason(note)
        if decision not in ("approve", "edit", "reject"):
            raise ValueError(decision)
        applied = None
        if decision in ("approve", "edit"):
            diff = edited_diff if decision == "edit" else json.loads(row["proposal_json"])
            applied = self._apply(row, diff, by=founder.actor)
            applied.pop("_watch", None)
        status = {"approve": "approved", "edit": "approved_edited", "reject": "rejected"}[decision]
        self._set(lesson_id, status=status, decided_by=founder.actor, decided_at=utc_now(), decision_note=note,
                  applied_json=json.dumps(applied, default=str) if applied else None)
        self.store.event(row["job_id"], founder.actor, "lesson_decided", {"lesson": lesson_id, "status": status, "applied": applied})
        return {"status": status, "applied": applied}

    def undo(self, lesson_id: str, *, founder, note: str) -> dict:
        """Restore the exact previous version of whatever the lesson changed. Founder only; who and why are recorded."""
        row = self.lesson(lesson_id)
        self._founder(row, founder, "undo")
        if row["status"] not in ("applied", "approved", "approved_edited"):
            raise ValueError(f"lesson is {row['status']}; only an applied lesson can be undone")
        note = check_reason(note)
        applied = json.loads(row["applied_json"] or "{}")
        restored = self._restore(row, applied, by=founder.actor, note=note)
        self._set(lesson_id, status="undone", undone_by=founder.actor, undone_at=utc_now(), undo_note=note,
                  applied_json=json.dumps({**applied, "undo": restored}, default=str, ensure_ascii=False))
        self.store.event(row["job_id"], founder.actor, "lesson_undone", {"lesson": lesson_id, "restored": restored, "note": note})
        return restored

    # ── apply / restore ───────────────────────────────────────────────────────────────────────────────
    def _apply(self, row, diff: dict, *, by: str) -> dict:
        t, lid = row["target"], row["id"]
        job = self.store.job(row["job_id"])
        if t == "rulebook_card":
            worker = diff["worker"]
            before = self.rulebook.version(worker)
            v = self.rulebook.change_card(worker, diff.get("changes", {}), by=by, reason=f"lesson {lid}: {row['why'][:200]}",
                                          source_lesson=lid)
            baseline = self._jobs_using(worker, before, before_utc=utc_now())[-WATCH_JOBS:]
            return {"target": t, "worker": worker, "before": {"version": before}, "after": {"version": v}, "new_version": v,
                    "_watch": {"worker": worker, "from_version": before, "to_version": v, "baseline_jobs": baseline, "status": "watching"}}
        if t == "equipment_sheet":
            if not diff.get("id"):             # change the row that decides this (class, route) today, so undo restores it exactly
                decider = [v["row"] for v in self._equipment_before(diff)["verdicts"] if v.get("row")]
                if decider:
                    diff = {**diff, "id": decider[0]}
            cur = self._equipment_before(diff)
            before = cur["row"] or (cur["verdicts"][0] if cur["verdicts"] else None)
            out = self.equipment.apply(diff, by=by, source_lesson=lid)
            after = next(r for r in self.equipment.rows() if r["id"] == out["id"])
            return {"target": t, **out, "before": before, "before_row": cur["row"], "after": after}
        if t == "recipe_library":
            rid = self.recipes.add({"source_job_id": row["job_id"], "account_id": job["account_id"] if job else None,
                                    "media": diff.get("media") or (job["media"] if job else "image"), **diff}, by=by, source_lesson=lid)
            return {"target": t, "id": rid, "before": None, "after": {"id": rid}}
        if t == "failure_diary":
            fid = self.failures.add({"source_job_id": row["job_id"], **diff}, by=by, source_lesson=lid,
                                    account_id=job["account_id"] if job and diff.get("private") else None)
            return {"target": t, "id": fid, "before": None, "after": {"id": fid}}
        if t == "customer_shelf":
            if not job:
                raise ValueError("a shelf lesson needs its job's account")
            acct = job["account_id"]
            prev = self.shelf.latest(acct, diff["kind"], diff["key"])
            sid = self.shelf.propose(acct, kind=diff["kind"], key=diff["key"], data=diff.get("data", {}), source_job_id=row["job_id"])
            if self.shelf.item(acct, sid)["status"] == "proposed":
                self.shelf.decide(acct, sid, approve=True, by=f"{by} (lesson {lid}, this customer's shelf only)")
            return {"target": t, "shelf_item": sid, "account_id": acct, "before": {"shelf_item": prev["id"]} if prev else None,
                    "after": {"shelf_item": sid}}
        return {"target": t, "status": "needs_builder", "note": "a form (schema) change is recorded as approved; a builder applies it"}

    def _restore(self, row, applied: dict, *, by: str, note: str) -> dict:
        t = row["target"]
        why = f"undo of lesson {row['id']} by {by}: {note[:200]}"
        if t == "rulebook_card":
            v = self.rulebook.restore(applied["worker"], applied["before"]["version"], by=by, reason=why)
            return {"worker": applied["worker"], "restored_version": applied["before"]["version"], "as_version": v}
        if t == "equipment_sheet":
            if applied.get("before_row"):
                v = self.equipment.restore(applied["before_row"], by=by, source_lesson=row["id"])
            else:
                v = self.equipment.restore({**applied["after"], "verdict": "withdrawn", "note": why}, by=by, source_lesson=row["id"])
            return {"id": applied["id"], "as_version": v}
        if t in ("recipe_library", "failure_diary"):
            with self.store.tx() as c:
                gone = c.execute(f"SELECT * FROM {t} WHERE id=?", (applied["id"],)).fetchone()
                c.execute(f"DELETE FROM {t} WHERE id=?", (applied["id"],))
            return {"removed": applied["id"], "row": dict(gone) if gone else None}
        if t == "customer_shelf":
            with self.store.tx() as c:
                c.execute("UPDATE shelf_items SET status='withdrawn', decided_by=?, decided_at=? WHERE id=? AND account_id=?",
                          (why[:200], utc_now(), applied["shelf_item"], applied["account_id"]))
            return {"withdrawn": applied["shelf_item"], "current": (applied.get("before") or {}).get("shelf_item")}
        return {"note": "nothing was applied"}

    # ── rulebook watch: 5 jobs after vs the previous 5 ─────────────────────────────────────────────────
    def _jobs_using(self, worker: str, version: int, *, before_utc: str | None = None, after_utc: str | None = None) -> list:
        sql = ("SELECT j.id, j.closed_at FROM jobs j WHERE j.closed_at IS NOT NULL AND j.outcome IS NOT NULL AND EXISTS "
               "(SELECT 1 FROM llm_calls c WHERE c.job_id=j.id AND c.worker=? AND c.card_version=?)")
        args = [worker, version]
        if before_utc:
            sql += " AND j.closed_at<=?"
            args.append(before_utc)
        if after_utc:
            sql += " AND j.closed_at>=?"
            args.append(after_utc)
        return [r["id"] for r in self.store.q(sql + " ORDER BY j.closed_at, j.id", tuple(args))]

    def _score(self, jobs: list) -> dict:
        acc = sum(1 for j in jobs if self.store.job(j)["outcome"] == "accepted")
        blocking = 0
        for j in jobs:
            g = self.store.artifact(j, "gateway_report") or {"results": []}
            blocking += sum(len(r.get("measured_blocking", r.get("blocking", []))) for r in g["results"])
        return {"jobs": jobs, "accepted": acc, "acceptance": round(acc / len(jobs), 3) if jobs else None, "blocking_checks": blocking}

    def review_watches(self) -> list:
        """Called after every closed job. Returns the lessons rolled back now."""
        rolled = []
        for row in self.store.q("SELECT * FROM lessons WHERE status='applied' AND watch_json IS NOT NULL"):
            w = json.loads(row["watch_json"])
            if w.get("status") != "watching":
                continue
            after = self._jobs_using(w["worker"], w["to_version"], after_utc=row["decided_at"])[:WATCH_JOBS]
            if len(after) < WATCH_JOBS:
                continue
            base = [j for j in w["baseline_jobs"]]
            b, a = self._score(base), self._score(after)
            worse = bool(base) and ((a["acceptance"] < b["acceptance"]) or a["blocking_checks"] > b["blocking_checks"])
            w.update(status="rolled_back" if worse else "kept", before=b, after=a, reviewed=utc_now())
            if worse:
                why = (f"rolled back automatically (lesson {row['id']}): acceptance {b['acceptance']} → {a['acceptance']}, "
                       f"blocking checks {b['blocking_checks']} → {a['blocking_checks']} over {WATCH_JOBS} jobs")
                v = self.rulebook.restore(w["worker"], w["from_version"], by="system:watch", reason=why)
                w["rolled_back_as_version"] = v
                self._set(row["id"], status="rolled_back", watch_json=json.dumps(w), decision_note=why)
                self.store.event(row["job_id"], "system:watch", "lesson_rolled_back", {"lesson": row["id"], "why": why, "version": v})
                rolled.append(row["id"])
            else:
                self._set(row["id"], watch_json=json.dumps(w))
        return rolled
