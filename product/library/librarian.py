"""The librarian (spec §8): code, no AI. Builds a small TRAY per worker instead of sending the whole library.

  1. Filter by labels (media, action classes in the plan, routes allowed, the customer's account for private items).
  2. Rank by similarity to the order (BM25, as v1's deep_retrieve; an embedding index may sit behind the same interface).
  3. Keep the top items within the worker's hard token cap.
Every tray is logged in the job file (artifact `tray`, and the ids on the llm_calls row), so we can see what a worker knew.
The library can grow without the tray growing: cost per job stays flat.
"""
from __future__ import annotations

import json

from product import library, rulebook
from product.library import bm25, stats, tokens

CAPS = {"chef": 6000, "recipe_checker": 4000, "pantry_checker": 1500}
MAX_COOKBOOK_PAGES = 6
MAX_RECIPES = 3
# Founder rulings 2026-09-24: "weaken the impact of failure notes unless they repeat multiple times — it's causing more harm
# than good", and "use stats — what is significant and what is not per the sample size". A failure note reaches a tray only
# when its kind recurs significantly more often than a one-off, given how many jobs are on record (exact binomial test,
# stats.recurs_significantly), and was not since prevented; one note per kind; a few at most; each labelled as a watch-out
# with its rate and confidence interval.
MAX_FAILURES = {"chef": 3, "recipe_checker": 5}


def _item(d, score, section=None):
    text = d["text"]
    return {"id": d["id"], "section": section or d["section"], "text": text, "tokens": tokens(text), "score": float(score),
            "action_classes": d.get("action_classes", []), "routes": d.get("routes", [])}


class Librarian:
    def __init__(self, store, equipment, failures, recipes, shelf):
        self.store, self.equipment, self.failures, self.recipes, self.shelf = store, equipment, failures, recipes, shelf

    # ── sections ────────────────────────────────────────────────────────────────────────────────────────────
    def _failures(self, query, classes, routes, account_id, media, worker="chef"):
        rows = [r for r in self.failures.all(account_id) if set(r["action_classes"]) & set(classes)
                and (not routes or not r["routes"] or set(r["routes"]) & set(routes)) and (not r.get("media") or r["media"] == media)
                and stats.recurs_significantly(r.get("times_seen", 1), r.get("jobs_on_record", 1)) and r.get("recurrence") != "PREVENTED"]
        out, kinds = [], set()
        for s, d in bm25(query, rows):
            if d.get("failure_mode") in kinds:
                continue
            kinds.add(d.get("failure_mode"))
            out.append(_item({**d, "text": f"Watch-out ({stats.describe(d['times_seen'], d['jobs_on_record'])}): {d['text']}"}, s))
            if len(out) >= MAX_FAILURES.get(worker, 3):
                break
        return out

    def _recipes(self, query, media, category, account_id, classes):
        rows = [r for r in self.recipes.all(account_id) if r["media"] == media]
        scored = []
        for s, d in bm25(query, rows):
            boost = (1.0 if category and d.get("product_category") == category else 0) + 0.5 * len(set(d["action_classes"]) & set(classes))
            scored.append((s + boost, d))
        scored.sort(key=lambda x: -x[0])
        return [_item(d, s) for s, d in scored[:MAX_RECIPES]]

    def _equipment(self, classes, routes):
        out = []
        for r in self.equipment.rows():
            if r["action_class"] in classes or (r["action_class"] == "any" and set(r["routes"]) & set(routes or r["routes"])):
                text = (f"{r['id']} v{r['version']}: {r['generator']} on {'/'.join(r['routes'])} × {r['action_class']} → {r['verdict'].upper()} "
                        f"(samples {r['sample_count']}; evidence {', '.join(r['evidence_refs']) or 'none'}). {r.get('note') or ''}"
                        + (f" Alternative: {r['alternative']}" if r.get("alternative") else ""))
                out.append(_item({"id": r["id"], "section": "equipment_sheet", "text": text}, 2.0))
        return out

    def _cookbooks(self, query, cookbook_args):
        if not cookbook_args:
            return [], None
        pages, record = library.cookbook_pages(**cookbook_args)
        return [_item(d, s) for s, d in bm25(query, pages)[:MAX_COOKBOOK_PAGES]], record

    def _shelf(self, account_id):
        summ = self.shelf.summary(account_id)
        compact = {k: [{kk: vv for kk, vv in e.items() if kk in ("id", "key", "version", "description", "hex", "name", "role", "shows")}
                       for e in v] for k, v in summ.items() if v}
        if not compact:
            return []
        return [_item({"id": f"SHELF-{account_id}", "section": "customer_shelf", "text": json.dumps(compact, ensure_ascii=False)}, 3.0)]

    # ── trays ───────────────────────────────────────────────────────────────────────────────────────────────
    def tray(self, job_id: str, worker: str, *, query: str, media: str, account_id: str, action_classes=(), routes=(),
             product_category: str | None = None, cookbook_args: dict | None = None) -> dict:
        cap = CAPS[worker]
        classes = [c for c in action_classes if c and c != "none"]
        record = None
        if worker == "pantry_checker":
            groups = [self._equipment(classes or rulebook.action_class_ids(), routes)]
        elif worker == "recipe_checker":
            groups = [self._failures(query, classes, routes, account_id, media, worker), self._equipment(classes, routes),
                      self._recipes(query, media, product_category, account_id, classes)]
        else:  # chef
            cook, record = self._cookbooks(query, cookbook_args)
            groups = [cook, self._shelf(account_id), self._recipes(query, media, product_category, account_id, classes),
                      self._failures(query, classes, routes, account_id, media, worker)]      # craft first, watch-outs last
        # round-robin across sections so every section is represented before any one fills the cap
        chosen, used = [], 0
        queues = [list(g) for g in groups]
        while any(queues):
            for q in queues:
                if not q:
                    continue
                it = q.pop(0)
                if used + it["tokens"] <= cap:
                    chosen.append(it)
                    used += it["tokens"]
        tray = {"for_worker": worker, "cap_tokens": cap, "tokens": used,
                "items": [{k: v for k, v in i.items() if k != "text"} | {"text": i["text"]} for i in chosen]}
        log = {"for_worker": worker, "cap_tokens": cap, "tokens": used,
               "items": [{"id": i["id"], "section": i["section"], "tokens": i["tokens"], "score": i["score"]} for i in chosen]}
        errs = rulebook.validate("tray", log)
        if errs:
            raise ValueError(f"tray log invalid: {errs[:3]}")
        self.store.put_artifact(job_id, f"tray:{worker}", {**log, "query": query[:500], "filters": {"media": media, "action_classes": classes,
                                                                                                    "routes": list(routes)},
                                                            "cookbook_record": {k: record[k] for k in ("packs_injected", "tokens")} if record else None},
                                "librarian")
        return tray
