"""Fixture mode (EVAL-041 part 2): constructed stand-in inputs for image half two, from STAND-IN-SPEC.yaml.

    python3 eval/harness-v2/run_live.py fixtures --spec eval/experiments/EVAL-040/fixtures/STAND-IN-SPEC.yaml \\
        --run-id <id> --out <dir> --auth eval/harness-v2/authorization.half2.local.yaml [--dry] [--max-dispatches N]

WHAT IT DOES, IN PLAIN ENGLISH

    The spec lists every stand-in the half-two cases need (a showroom sofa with a staff member, a masala pack, a
    backwaters banner, a model portrait and a lipstick packshot, a mustard-oil tin in three views, a recurring host
    in three views) plus same-category decoys. Each is SYNTHETIC: generated once on the spec's generation route
    (nano-banana-2), derived from its parent by one edit call on the derivation route (nano-banana-pro-edit, the
    parent's sealed bytes handed over through the same input resolver the battery uses), or set by code
    (composite.py: exact label strings on a blank label, USD 0). Every output is sealed as a FIXTURE under
    `<out>/artifacts/` with a record at `<out>/artifacts/fixtures/<fixture_id>.fixture.json` that carries the prompt,
    the asset id, `constructed_synthetic: true`, `for_case`, `role`, `is_decoy`, the parent's sha256 for a derived
    view, the overlay's placed strings, and - for `record_srgb_of` - the measured mean sRGB of the central region.

    `--dry` writes FIXTURE-PLAN.yaml (+ sha256): the ordered steps, each priced from the roster, and the total.
    Without `--dry` the plan is executed under the Controller's authorisation with the SAME ledger, caps, 0 retries,
    reservation-before-send and resumability as `execute`: a step with an attempt, a fixture record or a refusal
    record is skipped on resume; a cap breach stops the run before anything is sent.

ORDER

    1. every `generate` (assets, then their decoys) - independent calls;
    2. every `overlay` (USD 0) on its raw generation - the canonical fixture id is the OVERLAID image, the raw draw is
       sealed as `<id>__raw`;
    3. every `derived_views` edit call, with the CANONICAL parent (overlaid where the spec overlays: the tin's label
       must survive into the side and top views) as the single reference input.

COMMITMENT

    A generate step's body_sha256 is committed at plan time (no inputs). A derive step's body depends on the parent's
    bytes, which do not exist at plan time: the plan commits its TEMPLATE sha (the body with the placeholder) and the
    parent fixture id; at dispatch the parent's sealed sha256 is verified against its record and recorded on the
    fixture record, and the rendered body sha is written on the attempt. Overlays commit the strings and the fonts.
"""
from __future__ import annotations

import hashlib
import json
import tempfile
import traceback
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import yaml

import hv2_paths
import inputs as INP
import ledger as L
import pricing as PR
import store as S
import surfaces
from adapters import adapter_for as _adapter_for
from adapters import base as B
from budget_guard import BudgetExceeded, NotAuthorised
from providers import DispatchRefused, PreDispatchRefusal

FIXTURE_PLAN_FILE = "FIXTURE-PLAN.yaml"
FIXTURE_PLAN_SHA_FILE = "FIXTURE-PLAN.sha256"
STATE_FILE = "FIXTURES-STATE.json"
LOG_FILE = "FIXTURES-LOG.jsonl"
TRIALS_DIR = "trials"
ARTIFACTS_DIR = "artifacts"
LEDGER_DIR = "ledger"
RAW_SUFFIX = "__raw"
FIXTURE_TRANCHE = "1a"
RESOLUTION_CLASS = "~1 MP (1024-class)"
# The pinned SYSTEM font files the img-r1-composite record used (the blueprints' Noto Serif Devanagari / Inter are not on
# this machine; Kohinoor Devanagari Bold and Helvetica Neue Bold were the recorded substitutes). A spec may override with `fonts:`.
DEFAULT_FONTS = {"devanagari": {"file": "/System/Library/Fonts/Kohinoor.ttc", "face_index": 3},
                 "latin": {"file": "/System/Library/Fonts/HelveticaNeue.ttc", "face_index": 1}}
SRGB_REGION = "central box: x 40-60 %, y 40-60 % of the picture"
PLAN_STATEMENT = ("This fixture plan is the ordered list of the stand-in generations, derivations and code overlays run_live.py fixtures will make "
                  "under the named authorisation. Generate steps commit a body sha256; derive steps commit a template sha256 and their parent "
                  "fixture id (the parent's sealed sha256 is verified at dispatch); overlay steps cost USD 0. Every output is constructed_synthetic.")


class FixturePlanRefused(RuntimeError):
    """The fixture plan cannot be drawn or executed as asked. Nothing was sent."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# ------------------------------------------------------------------------------------ spec -> steps
def load_spec(path: Path | str) -> tuple[dict, str]:
    p = Path(path)
    raw = p.read_bytes()
    spec = yaml.safe_load(raw.decode("utf-8"))
    if not isinstance(spec, dict) or not isinstance(spec.get("assets"), list):
        raise FixturePlanRefused(f"{p}: expected a mapping with an `assets` list")
    for k in ("generation_route", "derivation_route"):
        if not spec.get(k):
            raise FixturePlanRefused(f"{p}: no {k}")
    return spec, hashlib.sha256(raw).hexdigest()


def trial_id_for(fixture_id: str, route_key: str) -> str:
    return S.safe_id(f"FIXTURE__{fixture_id}__{route_key}__r1")


def steps_from_spec(spec: dict) -> list[dict]:
    """The ordered steps: generates (assets then decoys), overlays, derived views."""
    gen_route, der_route = spec["generation_route"], spec["derivation_route"]
    generates, overlays, derives = [], [], []
    seen: set[str] = set()

    def _new(fid: str) -> str:
        if fid in seen:
            raise FixturePlanRefused(f"duplicate fixture id {fid!r} in the spec")
        seen.add(fid)
        return fid

    for a in spec["assets"]:
        for k in ("id", "for", "role", "kind", "prompt", "aspect"):
            if not a.get(k):
                raise FixturePlanRefused(f"asset {a.get('id')!r} lacks {k}")
        kind = a["kind"]
        if kind not in ("generate", "generate_then_overlay"):
            raise FixturePlanRefused(f"asset {a['id']}: unknown kind {kind!r}")
        has_overlay = kind == "generate_then_overlay"
        if has_overlay and not a.get("overlay"):
            raise FixturePlanRefused(f"asset {a['id']}: generate_then_overlay without an overlay list")
        raw_id = a["id"] + (RAW_SUFFIX if has_overlay else "")
        generates.append({"kind": "generate", "fixture_id": _new(raw_id), "canonical_id": a["id"], "raw_of": (a["id"] if has_overlay else None),
                          "for_case": a["for"], "role": a["role"], "is_decoy": False, "decoy_of": None, "prompt": a["prompt"].strip(),
                          "aspect": str(a["aspect"]), "route_key": gen_route, "record_srgb_of": a.get("record_srgb_of"), "note": a.get("note")})
        for d in a.get("decoys") or []:
            if not d.get("id") or not d.get("prompt"):
                raise FixturePlanRefused(f"asset {a['id']}: a decoy lacks id / prompt")
            generates.append({"kind": "generate", "fixture_id": _new(d["id"]), "canonical_id": d["id"], "raw_of": None, "for_case": a["for"],
                              "role": "decoy", "is_decoy": True, "decoy_of": a["id"], "prompt": d["prompt"].strip(), "aspect": str(a["aspect"]),
                              "route_key": gen_route, "record_srgb_of": None, "note": "same-category decoy for the qualification pack; never sent to a provider as an input"})
        if has_overlay:
            strings = []
            for i, s in enumerate(a["overlay"]):
                for k in ("text", "script", "size_pt", "colour", "y_frac"):
                    if s.get(k) is None:
                        raise FixturePlanRefused(f"asset {a['id']}: overlay string {i} lacks {k}")
                strings.append({"id": s.get("id") or f"s{i + 1}", **{k: s[k] for k in ("text", "script", "size_pt", "colour", "y_frac")},
                                "anchor": s.get("anchor", "center"), **({"x_frac": s["x_frac"]} if "x_frac" in s else {})})
            overlays.append({"kind": "overlay", "fixture_id": _new(a["id"]), "canonical_id": a["id"], "raw_of": None, "for_case": a["for"], "role": a["role"],
                             "is_decoy": False, "decoy_of": None, "parent_fixture_id": raw_id, "strings": strings, "route_key": None,
                             "exact_strings_by_code": True, "overlay_note": a.get("overlay_note"), "headline_fixture": a.get("headline_fixture"),
                             "record_srgb_of": a.get("record_srgb_of")})
        for v in a.get("derived_views") or []:
            if not v.get("id") or not v.get("edit_prompt"):
                raise FixturePlanRefused(f"asset {a['id']}: a derived view lacks id / edit_prompt")
            derives.append({"kind": "derive", "fixture_id": _new(v["id"]), "canonical_id": v["id"], "raw_of": None, "for_case": a["for"], "role": a["role"],
                            "is_decoy": False, "decoy_of": None, "parent_fixture_id": a["id"], "prompt": v["edit_prompt"].strip(), "aspect": str(a["aspect"]),
                            "route_key": der_route, "record_srgb_of": None, "note": "derived view of the same subject: one edit call with the canonical parent as the reference"})
    steps = generates + overlays + derives
    for i, st in enumerate(steps, 1):
        st["seq"] = i
        st["trial_id"] = trial_id_for(st["fixture_id"], st["route_key"] or "overlay")
    return steps


def fixture_case_row(step: dict) -> dict:
    """The case row an adapter needs for a fixture call; priced by the roster like any battery row."""
    return {"case_id": f"FIXTURE-{step['fixture_id']}", "item_id": f"FIXTURE-{step['fixture_id']}", "lane": "IMG",
            "route_key": step["route_key"], "arm": f"fixture_{step['kind']}", "repeat_index": 1, "tranche": FIXTURE_TRANCHE,
            "params": {"aspect": step["aspect"], "resolution": RESOLUTION_CLASS, "audio": "not_applicable",
                       "refs": (1 if step["kind"] == "derive" else 0), "seed": "unset"},
            "quantity": 1, "quantity_unit": "images", "price_status": "pinned", "route_status": "pinned", "conditional": False,
            "conditional_note": None, "conditions": {}, "language": None, "reference_assets": [], "prompt": step["prompt"],
            "constructed_synthetic": True, "fixture_id": step["fixture_id"], "for_case": step["for_case"]}


# ------------------------------------------------------------------------------------ plan
def build_fixture_plan(out: Path | str, run_id: str, spec_path: Path | str, auth_path: Path | str) -> dict:
    out = Path(out)
    if (out / FIXTURE_PLAN_FILE).exists():
        raise FixturePlanRefused(f"{out / FIXTURE_PLAN_FILE} already exists; a fixture plan is written once. Use a new run id.")
    auth = L.load_battery_authorisation(auth_path)
    if auth.refusals:
        raise NotAuthorised(f"build_fixture_plan: not authorised ({auth.source_path}):\n  - " + "\n  - ".join(auth.refusals))
    spec, spec_sha = load_spec(spec_path)
    steps = steps_from_spec(spec)
    registry = surfaces.REGISTRY
    pricing = PR.Pricing()
    fonts = dict(spec.get("fonts") or DEFAULT_FONTS)
    total = Decimal("0")
    by_route: dict[str, dict] = {}
    for st in steps:
        if st["kind"] == "overlay":
            st.update({"unit_price": "0", "estimated_usd_equiv": "0", "billing_pool": None, "currency": "USD", "body_sha256": None,
                       "template_body_sha256": None, "fonts": fonts, "usd": 0})
            continue
        if st["route_key"] not in registry.keys():
            raise FixturePlanRefused(f"step {st['fixture_id']}: route {st['route_key']!r} is not in the SurfaceRegistry")
        entry = registry.get(st["route_key"])
        if entry.media_kind != "image":
            raise FixturePlanRefused(f"step {st['fixture_id']}: {st['route_key']} is not an image route")
        ad = _adapter_for(entry, pricing=pricing)
        row = fixture_case_row(st)
        d = ad.dry_run(row)
        pc = d["price"]
        # a derive step's only refusal may be its missing input (the parent does not exist yet); anything else refuses the plan
        reasons = [x for x in (d["refusal_reason"] or "").split("; ") if x] if not d["would_dispatch"] else []
        blocking = [x for x in reasons if not x.startswith("input_unresolved:")]
        if blocking or (reasons and st["kind"] != "derive"):
            raise FixturePlanRefused(f"step {st['fixture_id']} ({st['route_key']}) cannot dispatch: {d['refusal_reason']}")
        amt = Decimal(pc["amount_usd_equiv"])
        total += amt
        slot = by_route.setdefault(st["route_key"], {"calls": 0, "usd_equiv": Decimal("0"), "billing_pool": entry.billing_pool})
        slot["calls"] += 1
        slot["usd_equiv"] += amt
        st.update({"surface": entry.surface, "adapter": entry.adapter, "surface_model_id": entry.surface_model_id, "endpoint": d["url"],
                   "billing_pool": entry.billing_pool, "currency": pc["currency"], "unit_price": pc["unit_price"], "quantity": pc["quantity"],
                   "quantity_unit": pc["quantity_unit"], "price_pin_ref": pc["pin_ref"], "estimated_usd_equiv": str(amt),
                   "key_name": entry.key_name, "credential_file_name": entry.credential_file_name,
                   "body_sha256": (d["body_sha256"] if st["kind"] == "generate" else None),
                   "template_body_sha256": (d["body_sha256"] if st["kind"] == "derive" else None),
                   "body_basis": ("rendered at plan time (no inputs)" if st["kind"] == "generate"
                                  else "template with the parent placeholder; the live body carries the parent's sealed bytes (data URI) and is verified at dispatch")})
    header = {"plan": "EVAL-041-FIXTURE-PLAN", "run_id": run_id, "mode": "fixtures", "generated_utc": _now(), "statement": PLAN_STATEMENT,
              "spec_path": str(spec_path), "spec_sha256": spec_sha, "spec_package": spec.get("package"),
              "generation_route": spec["generation_route"], "derivation_route": spec["derivation_route"], "overlay_tool": "eval/harness-v2/composite.py",
              "tranche_id": auth.tranche_id, "authorisation_path": auth.source_path, "authorisation_sha256": auth.sha256, "roster_sha256": pricing.roster.sha256,
              "fonts": fonts, "counts": {"steps": len(steps), "generate": sum(1 for s in steps if s["kind"] == "generate"),
                                         "decoys": sum(1 for s in steps if s["is_decoy"]), "overlay": sum(1 for s in steps if s["kind"] == "overlay"),
                                         "derive": sum(1 for s in steps if s["kind"] == "derive")},
              "estimated_by_route": {k: {"calls": v["calls"], "billing_pool": v["billing_pool"], "usd_equiv": str(v["usd_equiv"])} for k, v in by_route.items()},
              "estimated_total_usd_equiv": str(total), "spec_nominal_usd": (spec.get("counts") or {}).get("nominal_usd"),
              "retries_authorised": L.RETRIES_AUTHORISED, "every_output": "constructed_synthetic: true; never presented as a customer photo"}
    plan = {"header": header, "steps": steps}
    out.mkdir(parents=True, exist_ok=True)
    text = ("# EVAL-041 FIXTURE PLAN - the ordered stand-in steps run_live.py fixtures will make; written BEFORE any dispatch; execute refuses if these bytes change.\n"
            + yaml.safe_dump(plan, sort_keys=False, allow_unicode=True, width=160))
    (out / FIXTURE_PLAN_FILE).write_text(text, encoding="utf-8")
    (out / FIXTURE_PLAN_SHA_FILE).write_text(f"{_sha_file(out / FIXTURE_PLAN_FILE)}  {FIXTURE_PLAN_FILE}\n", encoding="utf-8")
    return plan


def plan_summary(plan: dict) -> dict:
    h = plan["header"]
    return {"run_id": h["run_id"], "steps": h["counts"], "estimated_by_route": h["estimated_by_route"],
            "estimated_total_usd_equiv": h["estimated_total_usd_equiv"], "spec_nominal_usd": h["spec_nominal_usd"], "spec_sha256": h["spec_sha256"]}


def load_fixture_plan(out: Path | str, run_id: str) -> dict:
    out = Path(out)
    p, s = out / FIXTURE_PLAN_FILE, out / FIXTURE_PLAN_SHA_FILE
    if not p.exists() or not s.exists():
        raise FixturePlanRefused(f"no committed fixture plan at {p}; run `fixtures --dry` first. Nothing was sent.")
    recorded, actual = s.read_text(encoding="utf-8").split()[0], _sha_file(p)
    if recorded != actual:
        raise FixturePlanRefused(f"{p} hashes to {actual[:12]}... but the sha file records {recorded[:12]}...; the plan changed. Nothing was sent.")
    plan = yaml.safe_load(p.read_text(encoding="utf-8"))
    if not isinstance(plan, dict) or plan.get("header", {}).get("run_id") != run_id:
        raise FixturePlanRefused(f"{p} is not the fixture plan of run {run_id!r}")
    plan["_sha256"] = actual
    return plan


# ------------------------------------------------------------------------------------ records
def fixture_record_path(out: Path | str, fixture_id: str) -> Path:
    return Path(out) / ARTIFACTS_DIR / INP.FIXTURES_SUBDIR / f"{S.safe_id(fixture_id)}.fixture.json"


def central_mean_srgb(path: Path) -> dict:
    """Mean sRGB over the central 20 % box, via the stdlib/ffmpeg decoder. Never raises: records the failure instead."""
    try:
        from instruments import imageio as IO
        img = IO.decode_image_ffmpeg(path)
        W, H = img.width, img.height
        x0, x1, y0, y1 = int(W * 0.4), max(int(W * 0.6), int(W * 0.4) + 1), int(H * 0.4), max(int(H * 0.6), int(H * 0.4) + 1)
        acc = [0, 0, 0]
        n = 0
        d = img.data
        c = img.channels
        for y in range(y0, y1):
            for x in range(x0, x1):
                i = (y * W + x) * c
                acc[0] += d[i]
                acc[1] += d[i + 1]
                acc[2] += d[i + 2]
                n += 1
        return {"mean_srgb": [round(a / n) for a in acc], "region": SRGB_REGION, "box": [x0, y0, x1, y1], "pixels": n}
    except Exception as exc:  # noqa: BLE001
        return {"mean_srgb": None, "region": SRGB_REGION, "error": f"{type(exc).__name__}: {exc}"}


# ------------------------------------------------------------------------------------ runner
class FixtureRunner:
    """Executes a committed fixture plan: same ledger, caps, 0 retries, reservation-before-send and resumability as LiveRunner."""

    def __init__(self, out: Path | str, run_id: str, auth_path: Path | str, transport_factory, adapter_kwargs: dict | None = None,
                 adapter_for=None, render_text=None):
        self.out = Path(out)
        self.run_id = run_id
        self.auth_path = Path(auth_path)
        self.transport_factory = transport_factory
        self.adapter_kwargs = dict(adapter_kwargs or {})
        self.adapter_for = adapter_for or _adapter_for
        self.render_text = render_text                  # tests inject a glyph renderer that needs no hb-view
        self.registry = surfaces.REGISTRY
        self.store = S.SealedStore(self.out / ARTIFACTS_DIR)
        self.plan: dict | None = None
        self.budget: L.BatteryBudget | None = None
        self.pricing: PR.Pricing | None = None

    # -- records ------------------------------------------------------------------------------
    def _trial_record_path(self, trial_id: str, kind: str) -> Path:
        return self.out / TRIALS_DIR / f"{S.safe_id(trial_id)}.{kind}.json"

    def is_terminal(self, step: dict) -> bool:
        tid = step["trial_id"]
        return (fixture_record_path(self.out, step["fixture_id"]).exists() or self.store.attempt_path(tid).exists()
                or self._trial_record_path(tid, "pre_dispatch_refusal").exists() or self._trial_record_path(tid, "harness_error").exists())

    def _log(self, event: str, **fields) -> None:
        self.out.mkdir(parents=True, exist_ok=True)
        with (self.out / LOG_FILE).open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({"at": _now(), "event": event, "run_id": self.run_id, **fields}, sort_keys=True, ensure_ascii=False, default=str) + "\n")

    def _write_state(self, **fields) -> None:
        path = self.out / STATE_FILE
        rec = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"run_id": self.run_id, "started_at": _now()}
        rec.update(fields, updated_at=_now())
        path.write_text(json.dumps(rec, indent=1, sort_keys=True, default=str) + "\n", encoding="utf-8")

    def _write_trial_record(self, step: dict, kind: str, **fields) -> Path:
        path = self._trial_record_path(step["trial_id"], kind)
        path.parent.mkdir(parents=True, exist_ok=True)
        n = 1
        while path.exists():
            n += 1
            path = self._trial_record_path(step["trial_id"], f"{kind}.{n}")
        rec = {"trial_id": step["trial_id"], "kind": kind, "at": _now(), "fixture_id": step["fixture_id"], "step_kind": step["kind"],
               "route_key": step.get("route_key"), "seq": step["seq"], **fields}
        path.write_text(json.dumps(rec, indent=1, sort_keys=True, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
        return path

    def _write_fixture_record(self, step: dict, artifact: dict, **extra) -> dict:
        rec = {"fixture_id": step["fixture_id"], "canonical_id": step.get("canonical_id"), "raw_of": step.get("raw_of"), "for_case": step["for_case"],
               "role": step["role"], "kind": step["kind"], "is_decoy": bool(step.get("is_decoy")), "decoy_of": step.get("decoy_of"),
               "constructed_synthetic": True, "never_a_customer_photo": True, "prompt": step.get("prompt"), "route_key": step.get("route_key"),
               "trial_id": step["trial_id"], "run_id": self.run_id, "parent_fixture_id": step.get("parent_fixture_id"),
               "relative_path": artifact["relative_path"], "sha256": artifact["sha256"], "bytes": artifact["bytes"], "content_type": artifact["content_type"],
               "media_kind": artifact["media_kind"], "artifact_id": artifact["artifact_id"], "spec_sha256": self.plan["header"]["spec_sha256"],
               "sealed_at": _now(), "record_srgb_of": step.get("record_srgb_of"), "note": step.get("note"), **extra}
        path = fixture_record_path(self.out, step["fixture_id"])
        self.store._write_new(path, (json.dumps(rec, indent=1, sort_keys=True, ensure_ascii=False, default=str) + "\n").encode("utf-8"))
        return rec

    # -- opening ------------------------------------------------------------------------------
    def open(self) -> L.BatteryAuthorisation:
        self.plan = load_fixture_plan(self.out, self.run_id)
        auth = L.load_battery_authorisation(self.auth_path)
        if auth.refusals:
            raise NotAuthorised(f"fixtures: not authorised ({auth.source_path}):\n  - " + "\n  - ".join(auth.refusals))
        root = self.out / LEDGER_DIR
        if (root / self.run_id / "run.json").exists():
            run = L.BatteryRun.open(root, self.run_id, auth)
        else:
            run = L.BatteryRun.create(root, self.run_id, auth, mode="fixtures")
        self.budget = L.BatteryBudget(run)
        self.pricing = PR.Pricing()
        return auth

    # -- steps ---------------------------------------------------------------------------------
    def _parent(self, step: dict) -> INP.ResolvedInput:
        pid = step["parent_fixture_id"]
        try:
            return INP.load_fixture_at(self.store.root, self.run_id, pid, "reference_asset_1", f"fixture:{self.run_id}:{pid}")
        except INP.InputsError as exc:
            raise PreDispatchRefusal(f"{step['trial_id']}: parent fixture {pid} is not available ({exc}); nothing was sent") from exc

    def _dispatch_call(self, step: dict) -> dict:
        entry = self.registry.get(step["route_key"])
        row = fixture_case_row(step)
        inputs: dict = {}
        parent = None
        if step["kind"] == "derive":
            parent = self._parent(step)
            needed = INP.roles_needed(entry, row)
            inputs = INP.build_inputs(entry, needed, {needed[0][0]: parent})
        transport = self.transport_factory(entry, step)
        # the default gcloud token source is enabled ONLY by run_live.main (it passes the flag in adapter_kwargs); this module never sets it
        adapter = self.adapter_for(entry, pricing=self.pricing, transport=transport, budget=self.budget, store=self.store, **self.adapter_kwargs)
        if step["kind"] == "derive":
            template = adapter.build_request(row)             # the placeholder body the plan committed to
            if template.body_sha256 != step["template_body_sha256"]:
                raise PreDispatchRefusal(f"{step['trial_id']}: the template body sha256 {template.body_sha256[:12]}... differs from the plan's "
                                         f"{step['template_body_sha256'][:12]}...; nothing was sent")
        request = adapter.build_request(row, inputs)
        if step["kind"] == "generate" and request.body_sha256 != step["body_sha256"]:
            raise PreDispatchRefusal(f"{step['trial_id']}: the rendered body sha256 {request.body_sha256[:12]}... differs from the plan's "
                                     f"{step['body_sha256'][:12]}...; the plan is executed verbatim or not at all. Nothing was sent.")
        attempt = adapter.dispatch(row, inputs, call_context={"trial_id": step["trial_id"]})
        attempt["_parent"] = parent
        attempt["_body_sha256"] = request.body_sha256
        return attempt

    def _overlay(self, step: dict) -> dict:
        import composite as CP
        parent = self._parent(step)
        fonts = dict(self.plan["header"]["fonts"])
        for name, f in fonts.items():
            if not Path(f["file"]).exists():
                raise PreDispatchRefusal(f"{step['trial_id']}: font for {name} missing at {f['file']}; the overlay needs the pinned system font (USD 0, nothing sent)")
            f["sha256"] = hashlib.sha256(Path(f["file"]).read_bytes()).hexdigest()
        plate_path = self.store.root / parent.relative_path
        with tempfile.TemporaryDirectory(prefix="fixture-overlay-") as td:
            png, placed = CP.composite_one(plate_path, {"strings": step["strings"]}, fonts, Path(td), render_text=self.render_text)
        art = self.store.seal(step["trial_id"], png, "image/png", {"derived_from_fixture": parent.artifact_id, "derived_from_sha256": parent.sha256, "usd": 0,
                                                                 "method": "deterministic overlay (composite.py)", "constructed_synthetic": True})
        srgb = central_mean_srgb(self.store.root / art["relative_path"])
        rec = self._write_fixture_record(step, art, parent_sha256=parent.sha256, overlay={"strings": placed, "fonts": fonts, "usd": 0,
                                                                                            "exact_strings_by_code": True, "headline_fixture": step.get("headline_fixture"),
                                                                                            "overlay_note": step.get("overlay_note")},
                                         central_srgb=srgb, usd="0")
        return {"status": "ok", "artifact": {k: art[k] for k in ("artifact_id", "relative_path", "bytes", "sha256", "content_type", "media_kind")}, "record": rec}

    # -- the run -------------------------------------------------------------------------------
    def execute(self, max_dispatches: int | None = None) -> dict:
        auth = self.open()
        steps = self.plan["steps"]
        self._write_state(status="running", plan_sha256=self.plan["_sha256"], authorisation_sha256=auth.sha256, mode="fixtures")
        self._log("run_started", n_steps=len(steps), max_dispatches=max_dispatches, ceiling_usd_equiv=str(auth.max_consumed_usd_equivalent))
        summary = {"run_id": self.run_id, "status": "running", "dispatched": 0, "overlaid": 0, "skipped": 0, "errors": [], "order": [], "stop_reason": None,
                   "fixtures_sealed": []}
        for step in steps:
            tid = step["trial_id"]
            if self.is_terminal(step):
                summary["skipped"] += 1
                continue
            if step["kind"] != "overlay" and max_dispatches is not None and summary["dispatched"] >= max_dispatches:
                summary["status"], summary["stop_reason"] = "paused_max_dispatches", f"max_dispatches {max_dispatches} reached"
                break
            self._log("dispatching", trial_id=tid, seq=step["seq"], kind=step["kind"], fixture_id=step["fixture_id"], estimated_usd_equiv=step.get("estimated_usd_equiv"))
            try:
                if step["kind"] == "overlay":
                    res = self._overlay(step)
                    summary["overlaid"] += 1
                    summary["order"].append(tid)
                    summary["fixtures_sealed"].append(step["fixture_id"])
                    self._log("overlaid", trial_id=tid, fixture_id=step["fixture_id"], artifact_sha256=res["artifact"]["sha256"])
                    continue
                attempt = self._dispatch_call(step)
            except (BudgetExceeded, NotAuthorised) as exc:
                reason = f"{type(exc).__name__}: {exc}"
                summary["status"], summary["stop_reason"] = ("stopped_cap_reached" if isinstance(exc, BudgetExceeded) else "stopped_not_authorised"), reason
                self._log("stopped", trial_id=tid, reason=reason)
                break
            except (PreDispatchRefusal, DispatchRefused) as exc:
                reason = f"{type(exc).__name__}: {exc}"
                self._write_trial_record(step, "pre_dispatch_refusal", reason=reason, sent=False)
                summary["errors"].append({"trial_id": tid, "kind": "pre_dispatch_refusal", "note": reason[:300]})
                self._log("pre_dispatch_refusal", trial_id=tid, reason=reason)
                continue
            except Exception as exc:  # noqa: BLE001 - one step's failure never ends the run
                reason = f"{type(exc).__name__}: {exc}"
                self._write_trial_record(step, "harness_error", error=reason, traceback=traceback.format_exc()[-4000:])
                summary["errors"].append({"trial_id": tid, "kind": "harness_error", "note": reason[:300]})
                self._log("harness_error", trial_id=tid, error=reason)
                continue
            summary["dispatched"] += 1
            summary["order"].append(tid)
            art = attempt.get("artifact") or {}
            parent = attempt.pop("_parent", None)
            body_sha = attempt.pop("_body_sha256", None)
            self._log("dispatched", trial_id=tid, status=attempt.get("status"), error_class=attempt.get("error_class"), billing_state=attempt.get("billing_state"),
                      cost_ref=attempt.get("cost_ref"), artifact_sha256=art.get("sha256"), provider_request_id=attempt.get("provider_request_id"), body_sha256=body_sha)
            if attempt.get("status") == "ok" and art:
                srgb = central_mean_srgb(self.store.root / art["relative_path"])
                try:
                    self._write_fixture_record(step, art, parent_sha256=(parent.sha256 if parent else None), body_sha256=body_sha, central_srgb=srgb,
                                               usd=attempt.get("reserved_amount_usd_equiv"), provider_request_id=attempt.get("provider_request_id"),
                                               aspect=step["aspect"], exact_strings_by_code=False)
                    summary["fixtures_sealed"].append(step["fixture_id"])
                except Exception as exc:  # noqa: BLE001
                    summary["errors"].append({"trial_id": tid, "kind": "fixture_record", "note": f"{type(exc).__name__}: {exc}"[:300]})
                    self._log("fixture_record_failed", trial_id=tid, error=f"{type(exc).__name__}: {exc}")
            else:
                summary["errors"].append({"trial_id": tid, "kind": "attempt", "status": attempt.get("status"), "error_class": attempt.get("error_class"),
                                          "note": (attempt.get("raw_status_note") or "")[:300]})
        if summary["status"] == "running":
            summary["status"] = "completed" if all(self.is_terminal(s) for s in steps) else "incomplete"
        remaining = sum(1 for s in steps if not self.is_terminal(s))
        self._write_state(status=summary["status"], stop_reason=summary["stop_reason"], n_dispatched_last_session=summary["dispatched"],
                          n_overlaid_last_session=summary["overlaid"], n_remaining=remaining, n_errors=len(summary["errors"]))
        self._log("run_finished", status=summary["status"], n_dispatched=summary["dispatched"], n_overlaid=summary["overlaid"], n_skipped=summary["skipped"],
                  n_remaining=remaining, stop_reason=summary["stop_reason"])
        summary["remaining"] = remaining
        return summary


def status(out: Path | str, run_id: str) -> dict:
    out = Path(out)
    plan = load_fixture_plan(out, run_id)
    store = S.SealedStore(out / ARTIFACTS_DIR)
    rows = []
    for st in plan["steps"]:
        rp = fixture_record_path(out, st["fixture_id"])
        a = store.load_attempt(st["trial_id"])
        rows.append({"fixture_id": st["fixture_id"], "kind": st["kind"], "sealed": rp.exists(), "attempt_status": (a or {}).get("status"),
                     "estimated_usd_equiv": st.get("estimated_usd_equiv")})
    return {"run_id": run_id, "steps": rows, "sealed": sum(1 for r in rows if r["sealed"]), "planned": len(rows),
            "estimated_total_usd_equiv": plan["header"]["estimated_total_usd_equiv"]}
