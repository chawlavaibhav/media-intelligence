"""One invocation, the whole Alpha-1 chain, dry.

    customer brief (JSON)
      -> intake (PRODUCTION-JOB-v1; consent, profile, kind, motion-dependency gates)
      -> Production Specification (PRODUCTION-SPEC-v1; deterministic Canon lookup; recorded plan)
      -> evidence-aware ROUTE-DECISION (register + price pins; fallback declared; manual when needed)
      -> EXECUTION-MANIFEST (every attempt rendered and priced through the harness adapter; nothing sent)
      -> pre-dispatch gate (canon.gate over the rendered package)
      -> dry attempts with a synthetic post-draw artifact and a scripted text detector
      -> bounded repair / human acceptance (a supplied verdict, because Alpha 1 is human release)
      -> OUTCOME-EVENT-v1 (empirical memory of the CHAIN, marked dry_run)
      -> template promotion when the outcome was accepted

Nothing between the brief and the end state is typed by a person. Every stage either produces
its object or refuses with a code and a reason, and the run stops at the first refusal. The run
opens no socket: the reasoning pass is served from the frozen Stage-A blueprint (or a recorded
fixture), the provider request is rendered by the harness adapter's dry_run(), the artifact is a
synthetic PNG of the declared aspect, and the text detector is scripted. All of that is labelled
as such in the objects it writes. A dry run proves the chain; it measures nothing about a model.

Controller rulings this runner obeys: C-7 (the Alpha-1 family — read from the policy profile),
C-8 (human approval; an automated judge is never the authority), C-6c (code-composed exact copy is
its own route identity), and the rider that adoption is not spend authority (dispatch_mode dry;
spend_authority none). USD 0 by construction.
"""
from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any

from canon.gate import textscan

from .. import paths
from ..canon.normalize import normalize
from ..canon.templates import TemplateLibrary
from ..errors import Refusal
from ..execute.bridge import ExecutionBridge
from ..intake import Intake, JobStore
from ..loop import driver, memory, synthetic
from ..route.attempt_id import load_identities
from ..route.decision import ExecuteRefused, Router, RouterRefusal
from ..route.evidence import EvidenceBase
from ..route.price import PriceBook
from ..route.profile import load_profile
from ..route.spec import Spec, SpecError
from ..spec.compile import SpecCompiler
from ..util import canonical_json, sha256_obj

POST_DRAW_SCENARIOS = ("clean", "lettering_then_clean", "lettering_always", "no_artifact")
HUMAN_VERDICTS = ("accept", "reject", None)

STAGES = ("intake", "spec", "canon", "route", "manifest", "dry_execution", "loop", "outcome_event", "template")


@dataclass
class StageRecord:
    stage: str
    status: str                      # ok | refused | skipped
    summary: str = ""
    refusal: dict | None = None
    artifact_path: str | None = None


@dataclass
class AlphaRunResult:
    brief_path: str
    job_id: str | None = None
    profile: str | None = None
    stages: list = field(default_factory=list)
    final_state: str = "not_started"
    refusal: dict | None = None
    objects: dict = field(default_factory=dict)   # stage -> the object (in memory)
    run_dir: str | None = None

    def stage(self, name: str) -> StageRecord | None:
        return next((s for s in self.stages if s.stage == name), None)

    def summary(self) -> dict:
        return {
            "brief": self.brief_path, "job_id": self.job_id, "profile": self.profile,
            "final_state": self.final_state, "refusal": self.refusal,
            "stages": [{"stage": s.stage, "status": s.status, "summary": s.summary,
                        "refusal": s.refusal, "artifact": s.artifact_path} for s in self.stages],
        }


def _refusal_dict(exc: Exception) -> dict:
    if isinstance(exc, Refusal):
        return {"code": exc.code, "message": exc.message,
                "context": json.loads(canonical_json(_jsonable(exc.context)))}
    if isinstance(exc, ExecuteRefused):
        return {"code": "EXECUTE_REFUSED", "message": "; ".join(exc.reasons), "context": {}}
    if isinstance(exc, (RouterRefusal, SpecError)):
        return {"code": type(exc).__name__.upper(), "message": str(exc), "context": {}}
    return {"code": type(exc).__name__, "message": str(exc), "context": {}}


def _jsonable(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {str(k): _jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return [_jsonable(v) for v in obj]
    if isinstance(obj, Decimal):
        return str(obj)
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    return str(obj)


def _write(run_dir: Path, name: str, obj: Any) -> str:
    os.makedirs(run_dir, exist_ok=True)
    path = run_dir / name
    text = obj if isinstance(obj, str) else json.dumps(_jsonable(obj), ensure_ascii=False, indent=2, sort_keys=True)
    path.write_text(text + ("" if text.endswith("\n") else "\n"), encoding="utf-8")
    return str(path)


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class AlphaRunner:
    """Holds the read-only evidence and price books once; runs briefs one at a time."""

    def __init__(self, root: Path | str | None = None):
        self.ev = EvidenceBase(root=root)
        src = self.ev.binding.sources
        self.prices = PriceBook(root=self.ev.root, roster_path=self.ev.root / src["roster"],
                                pin_root=self.ev.root / src["price_pin_root"])
        self.router = Router(self.ev, self.prices, load_identities())
        self.profiles_path = self.ev.root / src["policy_profiles"]

    # ------------------------------------------------------------------ run
    def run(self, brief_path: str | Path, *, store_root: str | Path, human_verdict: str | None = None,
            post_draw: str = "clean", at: str | None = None, consent_ref: str | None = None,
            write_event: bool = True) -> AlphaRunResult:
        if post_draw not in POST_DRAW_SCENARIOS:
            raise ValueError(f"post_draw must be one of {POST_DRAW_SCENARIOS}")
        if human_verdict not in HUMAN_VERDICTS:
            raise ValueError(f"human_verdict must be one of {HUMAN_VERDICTS}")
        at = at or _utc_now()
        store_root = Path(store_root)
        result = AlphaRunResult(brief_path=str(brief_path))
        with open(brief_path, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
        if consent_ref:
            for asset in raw.get("reference_assets") or []:
                if asset.get("depicts_identifiable_person"):
                    asset["consent_ref"] = consent_ref
        result.job_id = raw.get("job_id")
        result.profile = raw.get("policy_profile")
        run_dir = store_root / "runs" / _safe(str(result.job_id or "no-job-id"))
        result.run_dir = str(run_dir)
        _write(run_dir, "00-brief.json", raw)

        # 1. intake ---------------------------------------------------------------------------
        try:
            intake = Intake(store=JobStore(store_root))
            taken = intake.submit(raw, now=at)
        except Refusal as exc:
            return self._refuse(result, "intake", exc, run_dir)
        job = taken.job
        result.objects["job"] = job
        result.stages.append(StageRecord("intake", "ok", f"job {job['job_id']} accepted under profile {job['policy_profile']}"
                                         + (" (existing job returned; idempotent)" if not taken.created else ""),
                                         artifact_path=_write(run_dir, "01-job.json", job)))
        profile = load_profile(job["policy_profile"], self.profiles_path)

        # 2. spec (Canon lookup + recorded plan inside) ------------------------------------------
        nr = normalize(job)
        library = TemplateLibrary(store_root / "templates")

        def template_planner(prompt, *, job, nr):
            tpl = library.match(nr, dispatch_mode=str(profile.limit("dispatch_mode")))
            return library.fill(tpl, job, nr) if tpl else None

        compiler = SpecCompiler(template_planner=template_planner)
        try:
            compiled = compiler.compile(job, compiled_utc=at, provenance=taken.provenance)
        except Refusal as exc:
            return self._refuse(result, "spec", exc, run_dir)
        spec = compiled.spec
        result.objects["spec"] = spec
        result.stages.append(StageRecord(
            "spec", "ok",
            f"{spec['spec_id']} kind={spec['deliverable']['kind']} text={spec['exact_text']['strategy']} "
            f"planner={spec['blueprint'].get('planner')}", artifact_path=_write(run_dir, "02-spec.json", spec)))
        canon = spec["canon"]
        result.stages.append(StageRecord(
            "canon", "ok",
            f"injected {[p['pack_id'] for p in canon['packs_selected'] if p.get('compiled')]}; "
            f"missing_domains={canon.get('missing_domains') or []}; prefix sha {canon['injected_context_sha256'][:12]}",
            artifact_path=_write(run_dir, "03-canon.json", {
                "packs_selected": canon["packs_selected"], "missing_domains": canon.get("missing_domains") or [],
                "injected_context_sha256": canon["injected_context_sha256"], "canon_gap": canon.get("canon_gap"),
                "payload_sha256": hashlib.sha256(compiled.canon_payload.encode("utf-8")).hexdigest(),
                "payload_chars": len(compiled.canon_payload)})))

        # 3. route ----------------------------------------------------------------------------
        # the decision's provenance records the spec path; keep it store-relative so two runs of the
        # same brief at the same time fingerprint identically wherever the store lives
        spec_obj = Spec(path=Path("runs") / _safe(str(result.job_id)) / "02-spec.json", data=spec)
        try:
            decision = self.router.plan(spec_obj, profile, already_committed_usd=Decimal("0"),
                                        customer_ref=job["customer_ref"], decided_utc=at)
        except (RouterRefusal, Refusal, SpecError) as exc:
            return self._refuse(result, "route", exc, run_dir)
        result.objects["decision"] = decision
        _write(run_dir, "04-route-decision.json", decision)
        primary = decision.get("primary") or {}
        fallback = decision.get("fallback") or {}
        route_summary = (f"primary={primary.get('route_key')} fallback={fallback.get('route_key')} "
                         f"manual={decision['manual_route_required']}")
        if decision["manual_route_required"]:
            result.stages.append(StageRecord("route", "refused", route_summary,
                                             refusal={"code": "MANUAL_ROUTE_REQUIRED",
                                                      "message": decision["manual_route_reason"], "context": {}},
                                             artifact_path=str(run_dir / "04-route-decision.json")))
            result.final_state = "manual_route_required"
            result.refusal = result.stages[-1].refusal
            return self._finish(result, run_dir)
        result.stages.append(StageRecord("route", "ok", route_summary, artifact_path=str(run_dir / "04-route-decision.json")))

        # 4. manifest -------------------------------------------------------------------------
        prompt_text = self._dispatched_prompt(spec)
        inputs = self._inputs_for(job, store_root)
        try:
            bridge = ExecutionBridge(root=self.ev.root)
            manifest = bridge.build(spec_obj, decision, profile, prompt_text=prompt_text, inputs=inputs,
                                    customer_ref=job["customer_ref"], built_utc=at)
        except (ExecuteRefused, Refusal) as exc:
            return self._refuse(result, "manifest", exc, run_dir)
        result.objects["manifest"] = manifest
        _write(run_dir, "05-execution-manifest.json", manifest)
        if manifest.get("blocked"):
            result.stages.append(StageRecord("manifest", "refused", "blocked: " + manifest["blocked"]["reason_code"],
                                             refusal={"code": manifest["blocked"]["reason_code"],
                                                      "message": manifest["blocked"]["reason"], "context": {}},
                                             artifact_path=str(run_dir / "05-execution-manifest.json")))
            result.final_state = "manifest_blocked"
            result.refusal = result.stages[-1].refusal
            return self._finish(result, run_dir)
        attempts = manifest["attempts"]
        would = [a["attempt_id"].split(":")[-2] + ":" + a["attempt_id"].split(":")[-1] for a in attempts if a["would_dispatch"]]
        result.stages.append(StageRecord(
            "manifest", "ok",
            f"{len(attempts)} attempts rendered; would_dispatch={len(would)} "
            f"(if funded: {sum(1 for a in attempts if a.get('would_dispatch_if_funded'))}; pool liquidity "
            f"{(manifest.get('pool_liquidity') or {}).get('status')}); "
            f"reasons={sorted({a['refusal_reason'] for a in attempts if a.get('refusal_reason')})}",
            artifact_path=str(run_dir / "05-execution-manifest.json")))

        # 5. dry execution --------------------------------------------------------------------
        try:
            executed = bridge.run(manifest, profile)
        except (ExecuteRefused, Refusal) as exc:
            return self._refuse(result, "dry_execution", exc, run_dir)
        result.objects["execution"] = executed
        result.stages.append(StageRecord("dry_execution", "ok", f"{executed['status']}; network={executed.get('network')}",
                                         artifact_path=_write(run_dir, "06-dry-execution.json", executed)))

        # 6. the loop: pre-dispatch gate, synthetic post-draw, bounded repair, human acceptance ---
        dispatchable = [a for a in attempts if a["would_dispatch"] or a.get("slot") == "primary"]
        loop_manifest = dict(manifest, attempts=dispatchable)
        detector, provider, sampler = self._post_draw_fixture(spec, dispatchable, post_draw)
        verdicts = self._verdicts(human_verdict, at)
        try:
            loop = driver.run_loop(spec, spec["blueprint"], loop_manifest, profile,
                                   artifact_provider=provider, detector=detector, human_verdicts=verdicts,
                                   product_entity=bool(nr.facets.get("product_entity_present")),
                                   write=False, now_utc=at, frame_sampler=sampler,
                                   canon_lookup={"corpus_digest": compiler.corpus.accepted_digest,
                                                 "injection_prefix_sha256": canon["injected_context_sha256"]})
        except Refusal as exc:
            return self._refuse(result, "loop", exc, run_dir)
        _write(run_dir, "07-package.txt", loop.package_text)
        _write(run_dir, "08-gate-pre.json", loop.pre)
        _write(run_dir, "09-loop.json", {
            "state": loop.state, "acceptance_state": loop.acceptance_state, "refusal": loop.refusal, "reason": loop.reason,
            "attempts": [{k: v for k, v in a.items() if not k.startswith("_")} for a in loop.attempts],
            "repairs": loop.repairs, "post_draw_scenario": post_draw, "human_verdict_supplied": human_verdict,
            "acceptance_transcript": loop.acceptance.to_event() if loop.acceptance else None})
        result.objects["loop"] = loop
        loop_summary = (f"pre={loop.pre['verdict']} attempts={len(loop.attempts)} repairs={len(loop.repairs)} "
                        f"acceptance={loop.acceptance_state}" + (f" refusal={loop.refusal}" if loop.refusal else ""))
        result.stages.append(StageRecord("loop", "ok" if loop.pre["verdict"] == "PASS" else "refused", loop_summary,
                                         refusal=None if loop.pre["verdict"] == "PASS" else
                                         {"code": "PRE_DISPATCH_GATE_" + loop.pre["verdict"],
                                          "message": ", ".join(loop.pre["blocking_failures"]), "context": {}},
                                         artifact_path=str(run_dir / "09-loop.json")))
        result.final_state = loop.acceptance_state
        if loop.pre["verdict"] != "PASS":
            # a blocking pre-dispatch gate is a refusal of the job (nothing was dispatched) - surfaced on
            # the run so the exit code and the battery row say so, not only the loop record
            result.refusal = result.stages[-1].refusal

        # 7. empirical memory event (written only when a human verdict was supplied) ----------------
        if human_verdict is None:
            result.stages.append(StageRecord("outcome_event", "skipped",
                                             "no human verdict supplied; the event is assembled but not written "
                                             "(Alpha 1 is human release)",
                                             artifact_path=_write(run_dir, "10-outcome-event.unwritten.json", loop.event)))
            result.stages.append(StageRecord("template", "skipped", "no accepted outcome"))
            return self._finish(result, run_dir)
        try:
            store = memory.OutcomeStore(store_root)
            written = store.write(loop.event) if write_event else None
        except Refusal as exc:
            return self._refuse(result, "outcome_event", exc, run_dir)
        _write(run_dir, "10-outcome-event.json", loop.event)
        result.objects["event"] = loop.event
        result.stages.append(StageRecord(
            "outcome_event", "ok",
            f"{loop.event['event_id']} decision={loop.event['acceptance']['decision']} dry_run={loop.event.get('dry_run')}",
            artifact_path=str(written) if written else str(run_dir / "10-outcome-event.json")))

        # 8. template promotion --------------------------------------------------------------------
        if loop.event["acceptance"]["decision"] != "accepted":
            result.stages.append(StageRecord("template", "skipped", f"outcome {loop.event['acceptance']['decision']}; nothing to promote"))
            return self._finish(result, run_dir)
        try:
            template = library.promote(spec, loop.event, nr=nr, created_utc=at)
        except Refusal as exc:
            return self._refuse(result, "template", exc, run_dir)
        result.objects["template"] = template
        result.stages.append(StageRecord("template", "ok",
                                         f"{template['template_id']} status={template.get('status')}",
                                         artifact_path=_write(run_dir, "11-template.json", template)))
        return self._finish(result, run_dir)

    # ------------------------------------------------------------------ helpers
    @staticmethod
    def _dispatched_prompt(spec: dict) -> str:
        """The prompt the FIRST provider call carries: the textless plate when code composes the
        strings (C-6c mechanism B), the motion prompt for a motion deliverable, else the main prompt.
        Never invented: an empty prompt is passed through and the bridge refuses it by name."""
        prompts = (spec.get("blueprint") or {}).get("generation_prompts") or {}
        if spec.get("deliverable", {}).get("motion") and prompts.get("motion"):
            return prompts["motion"] or ""
        if spec["exact_text"].get("text_mechanism") == "deterministic_text_composition" and prompts.get("textless_plate"):
            return prompts["textless_plate"] or ""
        return prompts.get("main") or ""

    @staticmethod
    def _inputs_for(job: dict, store_root: Path) -> dict | None:
        """A motion job derived from an accepted still hands the still over as the harness input
        role `image_url`. In a dry run the still is the accepted synthetic artifact of the job named
        in motion.depends_on, found in this store's outcome events; absent, no input is invented and
        the harness records input_unresolved on the attempt."""
        motion = (job.get("deliverable_request") or {}).get("motion") or {}
        dep = motion.get("depends_on")
        if not dep or dep == job.get("job_id"):
            return None
        outcomes = memory.OutcomeStore(store_root).dir
        if not outcomes.is_dir():
            return None
        for path in sorted(outcomes.glob("*.json")):
            try:
                ev = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            if ev.get("job_id") == dep and (ev.get("acceptance") or {}).get("decision") == "accepted":
                accepted = [a for a in ev.get("attempts") or [] if a.get("artifact_sha256")]
                sha = accepted[-1]["artifact_sha256"] if accepted else "unknown"
                return {"image_url": f"dry://accepted-still/{dep}/{sha}"}
        return None

    @staticmethod
    def _post_draw_fixture(spec: dict, attempts: list, scenario: str):
        """A synthetic PNG per attempt (declared aspect, seed = draw index) and a scripted detector
        keyed on those exact bytes. `no_artifact` yields None for every attempt (a dry attempt
        with nothing to inspect), which the post-draw gate reports as NOT_RUN, never PASS.

        Motion specs get an MP4 stub AND a frame sampler yielding synthetic 'sampled frames'
        (synthetic.frames_for_spec) scripted the same way, so the frame-level text scan runs: the
        scenario's lettering lands on the frames, and a video with no frames would be NOT_RUN."""
        aspect = spec["deliverable"]["aspect"]
        motion = bool(spec["deliverable"].get("motion"))
        script: dict = {}

        def artifact_for(attempt: dict):
            if scenario == "no_artifact":
                return None
            if motion:
                return synthetic.mp4_for_spec(spec, seed=int(attempt.get("draw_index") or 1))
            return synthetic.png_for_aspect(aspect, seed=int(attempt.get("draw_index") or 1))

        def frames_for(attempt: dict, artifact_bytes):
            if not motion or artifact_bytes is None:
                return None
            return synthetic.frames_for_spec(spec, seed=int(attempt.get("draw_index") or 1))

        for i, attempt in enumerate(attempts, start=1):
            data = artifact_for(attempt)
            if data is None:
                continue
            lettering = (scenario == "lettering_always") or (scenario == "lettering_then_clean" and i == 1)
            entry = {"status": "text" if lettering else "no_text",
                     "transcript": "40% 40%" if lettering else "",
                     "note": f"scripted synthetic detector; scenario {scenario}; attempt {i}"}
            script[hashlib.sha256(data).hexdigest()] = dict(entry)
            for k, frame in enumerate(frames_for(attempt, data) or [], start=1):
                script[hashlib.sha256(frame).hexdigest()] = dict(entry, note=entry["note"] + f"; synthetic frame {k}")
        detector = textscan.ScriptedDetector.from_json(script) if script else None
        return detector, artifact_for, (frames_for if motion else None)

    @staticmethod
    def _verdicts(human_verdict: str | None, at: str) -> list:
        if human_verdict is None:
            return []
        if human_verdict == "accept":
            return [{"decision": "accepted", "by": "controller", "utc": at,
                     "note": "human verdict supplied on the command line for the dry run; a synthetic plate was "
                             "shown, nothing real was judged", "contract_lines_failed": None}]
        return [{"decision": "rejected", "by": "controller", "utc": at,
                 "note": "human verdict supplied on the command line for the dry run",
                 "contract_lines_failed": ["REJECT if any other lettering or pseudo-lettering appears anywhere"]}]

    def _refuse(self, result: AlphaRunResult, stage: str, exc: Exception, run_dir: Path) -> AlphaRunResult:
        rec = StageRecord(stage, "refused", refusal=_refusal_dict(exc), summary=_refusal_dict(exc)["code"])
        rec.artifact_path = _write(run_dir, f"refusal-{stage}.json", rec.refusal)
        result.stages.append(rec)
        result.final_state = f"refused_at_{stage}"
        result.refusal = rec.refusal
        return self._finish(result, run_dir)

    @staticmethod
    def _finish(result: AlphaRunResult, run_dir: Path) -> AlphaRunResult:
        _write(run_dir, "SUMMARY.json", result.summary())
        return result


def _safe(s: str) -> str:
    return "".join(ch if (ch.isalnum() or ch in "-_.") else "_" for ch in s)
