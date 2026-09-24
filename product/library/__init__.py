"""The kitchen library (spec §7.3): cookbooks (Canon), failure diary, recipe library, equipment sheet.

Every item carries labels — media, product_category, action_classes, routes, outcome, brand/account (private items are
never shown to another account), source_job_id — so the librarian (librarian.py) can filter before it ranks.
Seeds live in this folder; everything the product learns lives in the store and is added only through an approved lesson.
"""
from __future__ import annotations

import functools
import json
import math
import re
from collections import Counter
from pathlib import Path

import yaml

from product.store import Store, new_id, utc_now

HERE = Path(__file__).parent
ATLAS = HERE.parent.parent / "production-learning" / "atlas" / "2026-09-22" / "FAILURE-ATLAS-CLASSIFIED.yaml"
ROUTES = ("IMG", "FILM-A", "FILM-B", "FILM-C")
ROUTE_GENERATORS = {"IMG": ["nano-banana-2"], "FILM-A": ["nano-banana-2", "code_motion"], "FILM-B": ["nano-banana-2", "veo-3.1-fast-i2v"],
                    "FILM-C": ["nano-banana-2", "veo-3.1-fast-i2v"]}
RANK = {"reliable": 0, "risky": 1, "cannot": 2}
_WORD = re.compile(r"[a-z][a-z0-9']+")
_STOP = set("the a an of and or to in on for with is are be as by it its that this from at not no into than their his her they "
            "them which what when how why can may more most one two was were has have had".split())


def tokens(text: str) -> int:
    """Token estimate used for tray caps and cost estimates (≈ 4 characters per token)."""
    return max(1, len(text or "") // 4)


def words(text: str) -> list:
    return [w for w in _WORD.findall((text or "").lower()) if w not in _STOP]


# ── action classes (code floor under the model's labels) ─────────────────────────────────────────────────────────
@functools.lru_cache(maxsize=1)
def _classes():
    d = yaml.safe_load((HERE / "action_classes.yaml").read_text())["classes"]
    return [(c["id"], [re.compile(p, re.I) for p in c.get("patterns", [])], bool(c.get("manipulation"))) for c in d]


def classify(text: str) -> list:
    """Every action class whose patterns the text matches, most restrictive first."""
    return [cid for cid, pats, _ in _classes() if any(p.search(text or "") for p in pats)]


def manipulation_classes() -> set:
    return {cid for cid, _, m in _classes() if m}


# A negation governs the words after it up to the next clause boundary: "without spoken words or dialogue", "no voice".
# "not only" and "never stop(s)" do not negate what follows, so they are left alone (the floor stays strict).
_NEGATED = re.compile(r"(?:\b(?:without|no|not|never|nor)\b(?!\s+(?:only|stop))|n't\b)"
                      r"(?:(?!\b(?:and|but|then|while|whereas|when|so|as)\b)[^.,;:!?\u2013\u2014])*", re.I)
# Clause boundaries used to find clauses that describe a still picture rather than an action.
_CLAUSE = re.compile(r"[.,;:!?\u2013\u2014]|\s-\s|\b(?:and|but|then|while|before|after)\b", re.I)
# "still" used as a NOUN (a picture), not as an adjective ("a still hand") or adverb ("stays still").
_STILL_NOUN = re.compile(r"\bstills\b|\bstill\s+(?:of|image|images|frame|frames|shot|shots|picture|pictures|photo|photos|state|states)\b"
                         r"|\bas\s+a\s+still\b|\b(?:a|the|one)\s+still\s*$", re.I)


def _unnegated(text: str) -> str:
    return _NEGATED.sub(" ", text or "")


def _without_still_clauses(text: str) -> str:
    """The text with every clause that describes a still picture blanked out (the clause boundaries are kept)."""
    out, pos = [], 0
    for m in list(_CLAUSE.finditer(text)) + [None]:
        end = m.start() if m else len(text)
        clause = text[pos:end]
        out.append(" " if _STILL_NOUN.search(clause) else clause)
        if m:
            out.append(" . ")
            pos = m.end()
    return "".join(out)


def floor_class(text: str, model_class: str | None) -> str:
    """The class code will hold an action to: the model's class, unless the text matches a MORE restrictive one.
    Two or more distinct manipulations in one action are `multi_step_manipulation`.
    Words inside a negated clause ("without spoken words or dialogue") are not an action, and a clause that describes a
    still picture ("a still of the phone unfolded", "the folded and unfolded still states") performs no manipulation —
    but any other clause in the same text is still held to every class its words match."""
    text = _unnegated(text)
    hits = classify(text)
    manip_set = manipulation_classes()
    if _STILL_NOUN.search(text):
        acting = set(classify(_without_still_clauses(text)))
        hits = [h for h in hits if h not in manip_set or h in acting]
    manip = [h for h in hits if h in manip_set]
    order = [cid for cid, _, _ in _classes()]
    if len(set(manip)) >= 2 and "hands_work_mechanism" not in manip:
        hits = ["multi_step_manipulation"] + hits
    cands = ([model_class] if model_class in order else []) + hits
    if not cands:
        return model_class or "none"
    return min(cands, key=order.index)


# ── equipment sheet ─────────────────────────────────────────────────────────────────────────────────────────────
# Which routes can attempt a class at all. A class a route cannot attempt is simply not offered on that route.
ATTEMPTABLE = {
    "IMG": {"product_state_still", "product_still_from_clean_photo", "product_still_from_infographic_photo", "legible_text_on_product", "none"},
    "FILM-A": {"product_state_still", "camera_move_static_product", "product_still_from_clean_photo",
               "product_still_from_infographic_photo", "legible_text_on_product", "none"},
    "FILM-B": {"camera_move_static_product", "speech_or_lipsync", "identifiable_person", "legible_text_on_product"},
    "FILM-C": {"hands_work_mechanism", "multi_step_manipulation", "insert_object_into_container", "lift_closed_product",
               "simple_hand_gesture", "person_performance", "speech_or_lipsync", "identifiable_person", "legible_text_on_product"},
}


class EquipmentSheet:
    def __init__(self, store: Store):
        self.store = store

    @staticmethod
    @functools.lru_cache(maxsize=1)
    def seed() -> list:
        return yaml.safe_load((HERE / "equipment_seed.yaml").read_text())["rows"]

    def rows(self) -> list:
        """Seed rows overlaid by store versions (the newest version of each id wins); new ids are added."""
        out = {r["id"]: {**r, "version": 1, "by": "seed (repository)", "source_lesson": None} for r in self.seed()}
        for r in self.store.q("SELECT * FROM equipment_rows ORDER BY id, version"):
            ev = json.loads(r["evidence_json"])
            ev = ev if isinstance(ev, dict) else {"refs": ev}          # older rows stored a plain list of evidence ids
            out[r["id"]] = {"id": r["id"], "version": r["version"], "generator": r["generator"], "routes": json.loads(r["routes"]),
                            "action_class": r["action_class"], "verdict": r["verdict"], "sample_count": r["sample_count"],
                            "evidence_refs": ev.get("refs") or [], "note": r["note"], "alternative": r["alternative"],
                            "by": r["by"], "source_lesson": r["source_lesson"],
                            **{k: ev[k] for k in ("successes", "failures", "basis") if k in ev}}
        return [self._with_statistics(r) for r in out.values()]

    # Founder ruling 2026-09-24: "apply stats to the equipment sheet too". A verdict is only as strong as its sample.
    CANNOT_IF_FAILURE_RATE_ABOVE = 0.5      # significantly more likely to fail than to work
    RELIABLE_IF_FAILURE_RATE_BELOW = 0.25   # significantly likely to work

    @classmethod
    def _with_statistics(cls, r: dict) -> dict:
        """A row that records `successes`/`failures` gets its verdict computed from them (exact one-sided 95 % bounds on
        the failure rate); the written verdict is kept as `declared_verdict`. Policy and deterministic rows, `note` rows
        and rows without counts keep their declared verdict."""
        from product.library import stats
        r = dict(r)
        r["declared_verdict"] = r["verdict"]
        if r.get("basis") in ("policy", "deterministic", "lesson") or r["verdict"] not in RANK or "failures" not in r:
            r["evidence"] = {"policy": "a founder decision, not an observation", "deterministic": "deterministic code",
                             "lesson": "set by a lesson without counts, not a statistical result"}.get(r.get("basis"), "no counts recorded")
            return r
        f, n = int(r.get("failures") or 0), int(r.get("failures") or 0) + int(r.get("successes") or 0)
        if n and stats.lower_bound(f, n) > cls.CANNOT_IF_FAILURE_RATE_ABOVE:
            r["verdict"] = "cannot"
        elif n and stats.upper_bound(f, n) < cls.RELIABLE_IF_FAILURE_RATE_BELOW:
            r["verdict"] = "reliable"
        else:
            r["verdict"] = "risky"
        lo, hi = stats.interval(f, n) if n else (0.0, 1.0)
        r["evidence"] = (f"{f} of {n} attempts failed (failure rate 95% CI {lo:.0%}–{hi:.0%})" if n else "no attempts yet")
        return r

    def verdict(self, action_class: str, route: str) -> dict:
        """reliable | risky | cannot for (class, route), with the row that decided it. No row = unknown = risky."""
        if action_class not in ATTEMPTABLE.get(route, set()):
            return {"verdict": "cannot", "row": None, "why": f"{route} cannot attempt {action_class}", "alternative": None}
        rows = [r for r in self.rows() if r["action_class"] == action_class and route in r["routes"] and r["verdict"] in RANK]
        if not rows:
            return {"verdict": "risky", "row": None, "why": "unknown: no equipment row yet — treated as risky", "alternative": None}
        worst = max(rows, key=lambda r: RANK[r["verdict"]])
        return {"verdict": worst["verdict"], "row": worst["id"], "why": worst.get("note") or "", "alternative": worst.get("alternative")}

    def alternative(self, action_class: str) -> str | None:
        for r in self.rows():
            if r["action_class"] == action_class and r.get("alternative"):
                return r["alternative"]
        return None

    def apply(self, change: dict, *, by: str, source_lesson: str | None) -> dict:
        """Write a new version of a row (or a new row). Called only by an approved lesson (lessons/queue.py)."""
        need = ("action_class", "verdict")
        if any(k not in change for k in need) or change["verdict"] not in ("reliable", "risky", "cannot", "note"):
            raise ValueError(f"an equipment-sheet change needs {need} with a valid verdict")
        cur = next((r for r in self.rows() if r["id"] == change.get("id")), None) if change.get("id") else None
        rid = change.get("id") or f"EQ-L{new_id('')[1:9]}"
        version = (cur["version"] + 1) if cur else 1
        row = {"generator": change.get("generator") or (cur or {}).get("generator") or "veo-3.1-fast-i2v",
               "routes": change.get("routes") or (cur or {}).get("routes") or ["FILM-C"],
               "sample_count": int(change.get("sample_count", (cur or {}).get("sample_count", 0))),
               "evidence_refs": change.get("evidence_refs") or (cur or {}).get("evidence_refs") or [],
               # evidence accumulates: a lesson adds its observed successes/failures to what the row already had
               "counts": {k: int((cur or {}).get(k) or 0) + int(change.get(k) or 0) for k in ("successes", "failures")
                          if k in change or k in (cur or {})},
               # a lesson that sets a verdict without bringing counts is a declared verdict, labelled as such; with counts,
               # the statistics decide (founder rulings 2026-09-24: learning is automatic; verdicts follow the evidence)
               "basis": change.get("basis") or (None if ("successes" in change or "failures" in change) else "lesson"),
               "note": change.get("note") or (cur or {}).get("note"), "alternative": change.get("alternative") or (cur or {}).get("alternative")}
        with self.store.tx() as c:
            c.execute("INSERT INTO equipment_rows VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                      (rid, version, row["generator"], json.dumps(row["routes"]), change["action_class"], change["verdict"],
                       (sum(row["counts"].values()) if row["counts"] else row["sample_count"]),
                       json.dumps({"refs": row["evidence_refs"], **row["counts"], **({"basis": row["basis"]} if row["basis"] else {})}),
                       row["note"], row["alternative"], by, source_lesson, utc_now()))
        return {"id": rid, "version": version, "action_class": change["action_class"], "verdict": change["verdict"]}


    def restore(self, row: dict, *, by: str, source_lesson: str | None) -> int:
        """A new version of `row["id"]` with exactly the given content (an undo — history is never rewritten)."""
        cur = next((r for r in self.rows() if r["id"] == row["id"]), None)
        version = (cur["version"] + 1) if cur else 1
        with self.store.tx() as c:
            c.execute("INSERT INTO equipment_rows VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                      (row["id"], version, row.get("generator") or "veo-3.1-fast-i2v", json.dumps(row.get("routes") or []), row["action_class"],
                       row.get("declared_verdict") or row["verdict"], int(row.get("sample_count") or 0),
                       json.dumps({"refs": row.get("evidence_refs") or [], **{k: row[k] for k in ("successes", "failures", "basis") if k in row}}),
                       row.get("note"),
                       row.get("alternative"), by, source_lesson, utc_now()))
        return version


# ── failure diary ──────────────────────────────────────────────────────────────────────────────────────────────
@functools.lru_cache(maxsize=1)
def _atlas_rows() -> list:
    if not ATLAS.exists():
        return []
    d = yaml.safe_load(ATLAS.read_text())
    out = []
    for r in d["defects"]:
        text = f"{r['failure_mode'].replace('_', ' ')}: {r.get('verbatim', '')}"
        routes = []
        low = text.lower()
        if re.search(r"\bveo|i2v|clip|video model", low):
            routes += ["FILM-B", "FILM-C"]
        if re.search(r"nano|still|image model|plate", low):
            routes += ["IMG", "FILM-A"]
        out.append({"id": f"ATLAS-{r['id']}", "section": "failure_diary", "failure_mode": r["failure_mode"], "bucket": r["bucket"],
                    "recurrence": r.get("recurrence"),
                    "action_classes": classify(text), "routes": routes, "media": None, "text": text[:700],
                    "account_id": None, "source_job_id": r.get("job")})
    return out


@functools.lru_cache(maxsize=1)
def _seed_failures() -> list:
    d = yaml.safe_load((HERE / "failure_seed_0923.yaml").read_text())["rows"]
    return [{**r, "section": "failure_diary", "account_id": None, "source_job_id": "P1-v1-2026-09-23", "bucket": None} for r in d]


class FailureDiary:
    def __init__(self, store: Store):
        self.store = store

    def all(self, account_id: str | None, *, staff: bool = False) -> list:
        """staff=True only for the founder's pages; a tray always passes the job's account (private items stay private)."""
        rows = _seed_failures() + _atlas_rows()
        for r in self.store.q("SELECT * FROM failure_diary ORDER BY created"):
            if r["private"] and r["account_id"] != account_id and not staff:
                continue
            rows.append({"id": r["id"], "section": "failure_diary", "failure_mode": r["failure_mode"], "bucket": None,
                         "action_classes": json.loads(r["action_classes"]), "routes": json.loads(r["routes"]), "media": r["media"],
                         "text": r["text"], "account_id": r["account_id"], "source_job_id": r["source_job_id"]})
        # How many different jobs hit the same kind of failure, out of all jobs on record (founder 2026-09-24: a failure
        # only carries weight when it repeats significantly for the sample size — see library/stats.py).
        jobs, all_jobs = {}, set()
        for r in rows:
            job = r.get("source_job_id") or r["id"]
            jobs.setdefault(r.get("failure_mode"), set()).add(job)
            all_jobs.add(job)
        for r in rows:
            r["times_seen"] = len(jobs.get(r.get("failure_mode"), ()))
            r["jobs_on_record"] = len(all_jobs)
        return rows

    def add(self, entry: dict, *, by: str, source_lesson: str | None, account_id: str | None = None) -> str:
        fid = entry.get("id") or new_id("FD")
        with self.store.tx() as c:
            c.execute("INSERT INTO failure_diary VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                      (fid, entry.get("source_job_id"), account_id, entry.get("media"), json.dumps(entry.get("action_classes") or []),
                       json.dumps(entry.get("routes") or []), entry.get("failure_mode") or "unnamed", entry["text"],
                       int(bool(entry.get("private"))), by, source_lesson, utc_now()))
        return fid


# ── recipe library ─────────────────────────────────────────────────────────────────────────────────────────────
@functools.lru_cache(maxsize=1)
def _seed_recipes() -> list:
    return [
        {"id": "RL-0923-FILM", "section": "recipe_library", "media": "video", "product_category": "backpack", "outcome": "rejected",
         "action_classes": ["hands_work_mechanism", "insert_object_into_container", "lift_closed_product"], "routes": ["FILM-C"],
         "account_id": None, "source_job_id": "job_20260923_7d36a5b6",
         "text": "30-s 9:16 hands-only packing reel for a backpack: eight shots of hands sliding a laptop in, unzipping and folding "
                 "the front flap, packing clothes, re-zipping and lifting the bag, each shot generated independently. "
                 "Outcome REJECTED: 'two random hands, too many AI slops, robotic; the colour changed'."},
        {"id": "RL-0923-IMG", "section": "recipe_library", "media": "image", "product_category": "backpack", "outcome": "accepted",
         "action_classes": ["product_still_from_clean_photo"], "routes": ["IMG"], "account_id": None,
         "source_job_id": "job_20260923_6720871c",
         "text": "Launch poster, 1:1 and 4:5: the closed navy backpack alone, calm premium set, copy and logo set by code in a calm "
                 "top band. Outcome ACCEPTED after a colour, clearance and logo-size change."},
    ]


class RecipeLibrary:
    def __init__(self, store: Store):
        self.store = store

    def all(self, account_id: str | None, *, staff: bool = False) -> list:
        rows = list(_seed_recipes())
        for r in self.store.q("SELECT * FROM recipe_library ORDER BY created"):
            if r["private"] and r["account_id"] != account_id and not staff:
                continue
            rows.append({"id": r["id"], "section": "recipe_library", "media": r["media"], "product_category": r["product_category"],
                         "outcome": r["outcome"], "action_classes": json.loads(r["action_classes"]), "routes": json.loads(r["routes"]),
                         "account_id": r["account_id"], "source_job_id": r["source_job_id"],
                         "text": f"{r['summary']} Outcome {r['outcome'].upper()}" + (f": '{r['customer_words']}'" if r["customer_words"] else "")})
        return rows

    def add(self, entry: dict, *, by: str, source_lesson: str | None) -> str:
        rid = entry.get("id") or new_id("RL")
        with self.store.tx() as c:
            c.execute("INSERT INTO recipe_library VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                      (rid, entry["source_job_id"], entry.get("account_id"), entry["media"], entry.get("product_category"),
                       json.dumps(entry.get("action_classes") or []), json.dumps(entry.get("routes") or []), entry["outcome"],
                       entry.get("customer_words"), json.dumps(entry.get("recipe") or {}, ensure_ascii=False), entry["summary"],
                       int(bool(entry.get("private", True))), by, source_lesson, utc_now()))
        return rid


# ── cookbooks (Canon packs split into decision pages) ─────────────────────────────────────────────────────────────
_PAGE = re.compile(r"^([A-Z]{2,4}-D\d+) \[", re.M)


def cookbook_pages(media: str, brief_text: str, market: str, language: str, product: dict, exact_strings: list,
                   has_product_photo: bool) -> tuple:
    """(pages, record): the adopted packs the runtime selects for this job, split into one page per decision."""
    from product import canon_access
    packs = canon_access.practical_packs(media=media, brief_text=brief_text, market=market, language=language, product=product,
                                         exact_strings=exact_strings, has_product_photo=has_product_photo)
    payload = packs["payload"]
    pages = []
    marks = list(_PAGE.finditer(payload))
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(payload)
        body = payload[m.start():end]
        cut = body.find("\n\nCANON DOCTRINE PACK")
        body = (body[:cut] if cut > 0 else body).strip()
        pages.append({"id": m.group(1), "section": "cookbook", "text": body, "action_classes": [], "routes": [], "account_id": None})
    return pages, packs["record"]


def bm25(query: str, docs: list, key=lambda d: d["text"]) -> list:
    """Score docs against the query (BM25-style, as v1's deep_retrieve). Returns [(score, doc)] best first."""
    q = words(query)
    toks = [Counter(words(key(d))) for d in docs]
    n = len(docs) or 1
    df = Counter()
    for t in toks:
        df.update(set(t))
    avg = sum(sum(t.values()) for t in toks) / n if toks else 1
    out = []
    for d, t in zip(docs, toks):
        ln = sum(t.values()) or 1
        s = 0.0
        for w in set(q):
            if w in t:
                idf = math.log(1 + (n - df[w] + 0.5) / (df[w] + 0.5))
                s += idf * (t[w] * 2.2) / (t[w] + 1.2 * (0.25 + 0.75 * ln / avg))
        out.append((round(s, 4), d))
    return sorted(out, key=lambda x: -x[0])
