"""The rulebook (spec §5, §7.4): every worker's card (mission, vision, KRA, instructions) and every form's JSON schema,
as versioned data.

Seed versions are the YAML files in this folder. Later versions live in the store (`rulebook_versions`) and are created
only by `Rulebook.change_card` — which is called by an approved lesson or by a founder edit, and records who and why.
Every AI call includes its worker's CURRENT card and records the card version on the form it returns.
"""
from __future__ import annotations

import copy
import functools
import json
from pathlib import Path

import yaml

from product import schema as schema_mod

HERE = Path(__file__).parent
CARDS_DIR = HERE / "cards"
FORMS_DIR = HERE / "forms"
LIBRARY_DIR = HERE.parent / "library"

AI_WORKERS = ("waiter", "pantry_checker", "chef", "recipe_checker", "small_taster", "big_taster", "diary_writer")
CODE_WORKERS = ("head_cook", "door_guard", "librarian", "sign_painter", "measuring_tools")
PEOPLE = ("customer", "founder")
META_FIELDS = ("job_id", "form_version", "written_by", "rulebook_card_version", "created_utc")


@functools.lru_cache(maxsize=1)
def action_classes() -> list:
    return yaml.safe_load((LIBRARY_DIR / "action_classes.yaml").read_text())["classes"]


def action_class_ids() -> list:
    return [c["id"] for c in action_classes()]


def _resolve(node):
    """Replace `$enum: name` markers with the enum from the named data list."""
    if isinstance(node, dict):
        out = {k: _resolve(v) for k, v in node.items() if k != "$enum"}
        if node.get("$enum") == "action_classes":
            out["enum"] = action_class_ids()
        return out
    if isinstance(node, list):
        return [_resolve(v) for v in node]
    return node


@functools.lru_cache(maxsize=1)
def seed_cards() -> dict:
    out = {}
    for f in sorted(CARDS_DIR.glob("*.yaml")):
        d = yaml.safe_load(f.read_text())
        for c in d.get("cards", [d]):
            out[c["worker"]] = c
    return out


@functools.lru_cache(maxsize=1)
def forms() -> dict:
    out = {}
    for f in sorted(FORMS_DIR.glob("*.yaml")):
        d = yaml.safe_load(f.read_text())
        for fm in d.get("forms", [d]):
            fm = dict(fm)
            fm["schema"] = _resolve(fm["schema"])
            out[fm["form"]] = fm
    return out


def form(name: str) -> dict:
    return forms()[name]


def form_schema(name: str) -> dict:
    return forms()[name]["schema"]


def ai_schema(name: str) -> dict:
    """The part of a form the model fills (the whole form unless the form lists `ai_fields`)."""
    f = forms()[name]
    s = copy.deepcopy(f["schema"])
    if f.get("ai_fields"):
        keep = f["ai_fields"]
        s["properties"] = {k: v for k, v in s["properties"].items() if k in keep}
        s["required"] = [k for k in s["required"] if k in keep]
    return s


def validate(name: str, body: dict) -> list:
    return schema_mod.errors(body, form_schema(name))


class Rulebook:
    """Current cards, backed by the store. Seeds from the YAML files; changes are new versions, never edits."""

    def __init__(self, store):
        self.store = store

    def card(self, worker: str) -> dict:
        row = self.store.q1("SELECT card_json FROM rulebook_versions WHERE worker=? ORDER BY version DESC LIMIT 1", (worker,))
        if row:
            return json.loads(row["card_json"])
        return copy.deepcopy(seed_cards()[worker])

    def version(self, worker: str) -> int:
        return int(self.card(worker)["version"])

    def history(self, worker: str) -> list:
        seed = seed_cards()[worker]
        rows = self.store.q("SELECT * FROM rulebook_versions WHERE worker=? ORDER BY version", (worker,))
        return [{"version": seed["version"], "by": "seed (repository)", "reason": "initial card", "created": None}] + \
               [{"version": r["version"], "by": r["by"], "reason": r["reason"], "created": r["created"],
                 "source_lesson": r["source_lesson"]} for r in rows]

    def change_card(self, worker: str, changes: dict, *, by: str, reason: str, source_lesson: str | None = None) -> int:
        """A new card version with `changes` applied (top-level keys; `kra_add` appends; `instructions` merges).
        Callers: an approved lesson (lessons/queue.py) or a founder edit — both already authorised upstream."""
        if not reason or len(reason.strip()) < 10:
            raise ValueError("a rulebook change needs a reason")
        cur = self.card(worker)
        new = copy.deepcopy(cur)
        for k, v in changes.items():
            if k == "kra_add":
                new["kra"] = list(new.get("kra", [])) + ([v] if isinstance(v, str) else list(v))
            elif k == "instructions" and isinstance(v, dict):
                new.setdefault("instructions", {}).update(v)
            elif k in ("worker", "version", "kind"):
                continue
            else:
                new[k] = v
        new["version"] = int(cur["version"]) + 1
        errs = schema_mod.errors(new, form_schema("rulebook_card"))
        if errs:
            raise ValueError(f"the changed card is not valid: {errs[:3]}")
        from product.store import utc_now
        with self.store.tx() as c:
            c.execute("INSERT INTO rulebook_versions (worker, version, card_json, by, reason, source_lesson, created) VALUES (?,?,?,?,?,?,?)",
                      (worker, new["version"], json.dumps(new, ensure_ascii=False), by, reason.strip(), source_lesson, utc_now()))
        return new["version"]

    def card_at(self, worker: str, version: int) -> dict:
        seed = seed_cards()[worker]
        if int(version) == int(seed["version"]):
            return copy.deepcopy(seed)
        row = self.store.q1("SELECT card_json FROM rulebook_versions WHERE worker=? AND version=?", (worker, int(version)))
        if not row:
            raise KeyError(f"{worker} v{version}")
        return json.loads(row["card_json"])

    def restore(self, worker: str, version: int, *, by: str, reason: str, source_lesson: str | None = None) -> int:
        """A new card version whose content is exactly version `version` (an undo or an automatic rollback — history is
        never rewritten)."""
        if not reason or len(reason.strip()) < 10:
            raise ValueError("a rulebook restore needs a reason")
        new = self.card_at(worker, version)
        new["version"] = self.version(worker) + 1
        from product.store import utc_now
        with self.store.tx() as c:
            c.execute("INSERT INTO rulebook_versions (worker, version, card_json, by, reason, source_lesson, created) VALUES (?,?,?,?,?,?,?)",
                      (worker, new["version"], json.dumps(new, ensure_ascii=False), by, reason.strip(), source_lesson, utc_now()))
        return new["version"]

    def card_text(self, worker: str, form_name: str) -> tuple:
        """(system text, card version): the stable prefix of every AI call — card first, then the form's instructions."""
        c = self.card(worker)
        kra = "\n".join(f"  {i + 1}. {k}" for i, k in enumerate(c.get("kra", [])))
        text = (f"RULEBOOK CARD — {worker} (version {c['version']})\nMission: {c['mission']}\n"
                + (f"Vision: {c['vision']}\n" if c.get("vision") else "")
                + f"KRA (what you are measured on):\n{kra}\n\n"
                + (c.get("instructions") or {}).get(form_name, "").strip())
        return text, int(c["version"])
