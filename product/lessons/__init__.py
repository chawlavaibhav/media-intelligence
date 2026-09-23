"""The lesson queue (spec §7.5, §4.11). The diary writer PROPOSES; nothing changes until the founder approves each proposal.
Approved lessons are applied by code to their target store and the application is recorded on the lesson.

Targets and what "apply" does:
  rulebook_card    a new card version (Rulebook.change_card)            diff: {"worker": ..., "changes": {...}}
  equipment_sheet  a new row version (EquipmentSheet.apply)             diff: {"action_class", "verdict", "routes", ...}
  recipe_library   a new recipe-with-outcome entry (RecipeLibrary.add)  diff: {"summary", ...}
  failure_diary    a new failure entry (FailureDiary.add)               diff: {"text", "failure_mode", "action_classes", ...}
  customer_shelf   a PROPOSED shelf item — the customer still approves it (Shelf.propose)
  form             not applied automatically: a schema change needs a builder; the approval is recorded as such.
"""
from __future__ import annotations

import json

from product.authority import check_reason, verify_proof
from product.store import Store, new_id, utc_now

TARGETS = ("rulebook_card", "equipment_sheet", "recipe_library", "failure_diary", "customer_shelf", "form")


class LessonQueue:
    def __init__(self, store: Store, *, rulebook, equipment, recipes, failures, shelf):
        self.store, self.rulebook, self.equipment, self.recipes, self.failures, self.shelf = \
            store, rulebook, equipment, recipes, failures, shelf

    def enqueue(self, job_id: str, lessons_form: dict) -> list:
        ids = []
        with self.store.tx() as c:
            for w in lessons_form.get("per_worker", []):
                pc = w.get("proposed_change")
                if not pc:
                    continue
                if pc["target"] not in TARGETS:
                    raise ValueError(pc["target"])
                lid = new_id("lsn")
                c.execute("INSERT INTO lessons (id, job_id, worker, target, proposal_json, why, evidence_json, status, created) "
                          "VALUES (?,?,?,?,?,?,?,?,?)", (lid, job_id, w["worker"], pc["target"], json.dumps(pc["diff"], ensure_ascii=False),
                                                         pc.get("why", ""), json.dumps(w.get("evidence_refs", [])), "waiting", utc_now()))
                ids.append(lid)
        return ids

    def waiting(self) -> list:
        return self.store.q("SELECT * FROM lessons WHERE status='waiting' ORDER BY created")

    def all(self, job_id: str | None = None) -> list:
        if job_id:
            return self.store.q("SELECT * FROM lessons WHERE job_id=? ORDER BY created", (job_id,))
        return self.store.q("SELECT * FROM lessons ORDER BY created DESC")

    def lesson(self, lesson_id: str):
        row = self.store.q1("SELECT * FROM lessons WHERE id=?", (lesson_id,))
        if row is None:
            raise KeyError(lesson_id)
        return row

    def decide(self, lesson_id: str, *, founder, decision: str, note: str, edited_diff: dict | None = None) -> dict:
        """decision: approve | edit (approve with the founder's edited diff) | reject. Founder only."""
        row = self.lesson(lesson_id)
        if not verify_proof(self.store, founder):
            self.store.event(row["job_id"], getattr(founder, "actor", str(founder)[:60]), "override_refused",
                             {"action": f"decide lesson {lesson_id}", "why": "only the founder, signed in, decides lessons"})
            raise PermissionError("only the founder can approve, edit or reject a lesson")
        if row["status"] != "waiting":
            raise ValueError(f"lesson already {row['status']}")
        note = check_reason(note)
        if decision not in ("approve", "edit", "reject"):
            raise ValueError(decision)
        applied = None
        if decision in ("approve", "edit"):
            diff = edited_diff if decision == "edit" else json.loads(row["proposal_json"])
            applied = self._apply(row, diff, by=founder.actor)
        status = {"approve": "approved", "edit": "approved_edited", "reject": "rejected"}[decision]
        with self.store.tx() as c:
            c.execute("UPDATE lessons SET status=?, decided_by=?, decided_at=?, decision_note=?, applied_json=? WHERE id=?",
                      (status, founder.actor, utc_now(), note, json.dumps(applied, default=str) if applied else None, lesson_id))
        self.store.event(row["job_id"], founder.actor, "lesson_decided", {"lesson": lesson_id, "status": status, "applied": applied})
        return {"status": status, "applied": applied}

    def _apply(self, row, diff: dict, *, by: str) -> dict:
        t, lid = row["target"], row["id"]
        job = self.store.job(row["job_id"])
        if t == "rulebook_card":
            v = self.rulebook.change_card(diff["worker"], diff.get("changes", {}), by=by, reason=f"lesson {lid}: {row['why'][:200]}",
                                          source_lesson=lid)
            return {"target": t, "worker": diff["worker"], "new_version": v}
        if t == "equipment_sheet":
            return {"target": t, **self.equipment.apply(diff, by=by, source_lesson=lid)}
        if t == "recipe_library":
            rid = self.recipes.add({"source_job_id": row["job_id"], "account_id": job["account_id"] if job else None,
                                    "media": diff.get("media") or (job["media"] if job else "image"), **diff}, by=by, source_lesson=lid)
            return {"target": t, "id": rid}
        if t == "failure_diary":
            fid = self.failures.add({"source_job_id": row["job_id"], **diff}, by=by, source_lesson=lid,
                                    account_id=job["account_id"] if job and diff.get("private") else None)
            return {"target": t, "id": fid}
        if t == "customer_shelf":
            if not job:
                raise ValueError("a shelf lesson needs its job's account")
            sid = self.shelf.propose(job["account_id"], kind=diff["kind"], key=diff["key"], data=diff.get("data", {}),
                                     source_job_id=row["job_id"])
            return {"target": t, "shelf_item": sid, "status": "proposed — the customer approves it"}
        return {"target": t, "status": "needs_builder", "note": "a form (schema) change is recorded as approved; a builder applies it"}
