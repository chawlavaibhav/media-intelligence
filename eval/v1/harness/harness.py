"""Generate-once evaluation harness.

    frozen item manifest
        -> ONE generation/transform call
        -> immutable output artifact + provenance
        -> evaluator fan-out by eligible capability
        -> measurements (many per asset)
        -> failure co-occurrence
        -> operational metrics
        -> Registry rows (only from qualified instruments)

The harness enforces nine invariants. Each exists because getting it wrong
produces a number that LOOKS like evidence and is not.
"""
from __future__ import annotations
import json, pathlib, uuid
from typing import Callable

from models import (GenerationProvenance, Measurement, RegistryRow,
                    ABSENCE_REASONS, VERDICTS, QUALIFICATION_STATUSES,
                    REGISTRY_WRITABLE, config_hash, sha256_str)


class HarnessError(RuntimeError):
    """Raised on any invariant violation. The harness FAILS CLOSED.

    EVAL-002 found a run that raised integrity errors and still exited
    successfully. Raising is not enough; the caller must not be able to
    continue as if nothing happened.
    """


class Instrument:
    """An evaluator, plus the qualification that decides whether to believe it."""

    def __init__(self, instrument_id, version, config: dict,
                 qualification_status="screened_not_qualified",
                 calibration_ref=None, capabilities=(), observation_unit="frame",
                 cost_per_call=0.0, fn: Callable | None = None):
        if qualification_status not in QUALIFICATION_STATUSES:
            raise HarnessError(f"unknown qualification status {qualification_status}")
        self.id = instrument_id
        self.version = version
        self.config = config
        self.config_hash = config_hash(config)
        self.qualification_status = qualification_status
        self.calibration_ref = calibration_ref
        self.capabilities = set(capabilities)
        self.observation_unit = observation_unit
        self.cost_per_call = cost_per_call
        self.fn = fn

    @property
    def registry_writable(self) -> bool:
        return self.qualification_status in REGISTRY_WRITABLE


class Harness:
    def __init__(self, root: pathlib.Path, clock=None):
        self.root = pathlib.Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.assets_dir = self.root / "assets"
        self.assets_dir.mkdir(exist_ok=True)
        self.provenance: dict[str, GenerationProvenance] = {}   # asset_id -> prov
        self.attempts: dict[str, GenerationProvenance] = {}     # attempt_id -> prov
        self.measurements: list[Measurement] = []
        self.registry_rows: list[RegistryRow] = []
        self.instruments: dict[str, Instrument] = {}
        # (item_id, config_hash) -> asset_id, for the duplicate-generation guard
        self._generated: dict[tuple, str] = {}
        self._t = 0
        self._clock = clock or self._tick

    def _tick(self):
        # Deterministic clock: Date.now()-style nondeterminism would make runs
        # unreproducible, and reproducibility is a thing we MEASURE.
        self._t += 1
        return f"T{self._t:06d}"

    def _new_id(self, prefix, seed_material):
        return f"{prefix}-{sha256_str(seed_material)[:12]}"

    # ---------------------------------------------------------------- register
    def register_instrument(self, instrument: Instrument):
        self.instruments[instrument.id] = instrument

    # -------------------------------------------------------------- generation
    def generate(self, item: dict, provider_cfg: dict, generator: Callable,
                 repeat_of: str | None = None, repeat_index: int | None = None,
                 retry_of: str | None = None, retry_reason: str | None = None,
                 force: bool = False) -> GenerationProvenance:
        """Make ONE generation attempt for one item.

        INVARIANT 3 - a retry is a NEW attempt id and NEVER replaces an output.
        INVARIANT 4 (guard) - refuses to regenerate an item/config that already
        has a successful asset, unless it is an explicitly declared experimental
        REPEAT or a production RETRY.

        E-C4: `repeat_of` and `retry_of` are DIFFERENT and MUTUALLY EXCLUSIVE.
        A repeat is design-time and estimates reproducibility. A retry is
        result-time and belongs to the accepted-outcome chain. One attempt is
        never both.
        """
        cfg = dict(provider_cfg)
        chash = config_hash({"item": item["item_id"], **cfg})
        key = (item["item_id"], chash)

        if repeat_of is not None and retry_of is not None:
            raise HarnessError(
                "An attempt cannot be BOTH an experimental repeat and a "
                "production retry. A repeat is decided before the run to "
                "measure reproducibility; a retry is decided after seeing a "
                "failure. Only retries belong in the CpAO retry chain, so "
                "allowing both would corrupt reliability and cost at once.")
        if retry_of is not None and retry_reason is None:
            raise HarnessError(
                "A production retry requires retry_reason. An unexplained "
                "retry is indistinguishable from an experimental repeat.")
        if repeat_of is not None and repeat_index in (None, 0):
            raise HarnessError(
                "An experimental repeat requires a repeat_index >= 1. "
                "repeat_index 0 is the first attempt of a repeat set, not a "
                "repeat of anything.")

        if key in self._generated and repeat_of is None and retry_of is None \
                and not force:
            raise HarnessError(
                f"DUPLICATE GENERATION REFUSED for item {item['item_id']} "
                f"config {chash[:12]}: asset {self._generated[key]} already "
                f"exists. Evaluating another capability on an existing asset "
                f"needs NO new generation - that is the point of the bank's "
                f"measurement fan-out. If this is a deliberate reliability "
                f"repeat pass repeat_of/repeat_index; if it is a production "
                f"retry after a failure pass retry_of/retry_reason. Either is "
                f"recorded as a new attempt; they are never interchangeable.")

        if retry_of is not None and retry_of not in self.attempts:
            raise HarnessError(f"retry_of references unknown attempt {retry_of}")
        if repeat_of is not None and repeat_of not in self.attempts:
            raise HarnessError(f"repeat_of references unknown attempt {repeat_of}")

        attempt_id = self._new_id("att", f"{item['item_id']}|{chash}|{len(self.attempts)}")
        requested_at = self._clock()
        result = generator(item, cfg)          # dummy/local in tests; never paid here
        completed_at = self._clock()

        status = result.get("api_status", "ok")
        asset_id = None
        out_path = out_hash = None

        if status == "ok":
            payload = result["payload"]
            asset_id = self._new_id("ast", f"{attempt_id}|{sha256_str(payload)}")
            p = self.assets_dir / f"{asset_id}.bin"
            if p.exists():
                raise HarnessError(f"asset {asset_id} already on disk - assets are immutable")
            p.write_text(payload)
            out_path, out_hash = str(p), sha256_str(payload)

        prov = GenerationProvenance(
            attempt_id=attempt_id, asset_id=asset_id or "", item_id=item["item_id"],
            provider=cfg.get("provider", ""), model=cfg.get("model", ""),
            version=cfg.get("version", ""), endpoint=cfg.get("endpoint", ""),
            workflow=cfg.get("workflow", ""), lane=cfg.get("lane", ""),
            config_hash=chash, config_path=cfg.get("config_path", ""),
            input_hashes=cfg.get("input_hashes", []),
            reference_hashes=cfg.get("reference_hashes", []),
            seed=cfg.get("seed"), seed_policy=cfg.get("seed_policy", "unsupported"),
            requested_at=requested_at, completed_at=completed_at,
            api_status=status, error_class=result.get("error_class"),
            output_path=out_path, output_sha256=out_hash,
            cost_generation=result.get("cost_generation"),
            currency=cfg.get("currency", "USD"),
            repeat_index=(repeat_index or 0), repeat_of_attempt_id=repeat_of,
            retry_of_attempt_id=retry_of, retry_reason=retry_reason,
        )
        self.attempts[attempt_id] = prov
        if asset_id:
            # INVARIANT 1 - exactly one provenance record per asset.
            if asset_id in self.provenance:
                raise HarnessError(f"asset {asset_id} already has a provenance record")
            self.provenance[asset_id] = prov
            self._generated.setdefault(key, asset_id)
        return prov

    def derive_frames(self, asset_id: str, n: int) -> list[GenerationProvenance]:
        """Extract child assets (frames) from a parent clip.

        INVARIANT 4 - children carry parent_asset_id and add NO new trials.
        No generation call is made. This is sampling, not producing.
        """
        if asset_id not in self.provenance:
            raise HarnessError(f"unknown parent asset {asset_id}")
        parent = self.provenance[asset_id]
        out = []
        for i in range(n):
            fid = self._new_id("ast", f"{asset_id}|frame{i}")
            payload = f"FRAME{i}_OF_{asset_id}"
            p = self.assets_dir / f"{fid}.bin"
            p.write_text(payload)
            prov = GenerationProvenance(
                attempt_id=parent.attempt_id, asset_id=fid, item_id=parent.item_id,
                provider=parent.provider, model=parent.model, version=parent.version,
                endpoint=parent.endpoint, workflow=parent.workflow, lane=parent.lane,
                config_hash=parent.config_hash, config_path=parent.config_path,
                requested_at=parent.requested_at, completed_at=parent.completed_at,
                api_status="ok", output_path=str(p), output_sha256=sha256_str(payload),
                cost_generation=0.0,          # a frame costs nothing to extract
                parent_asset_id=asset_id, derivation=f"frame_sample[{i}]",
            )
            self.provenance[fid] = prov
            out.append(prov)
        return out

    def trial_asset_id(self, asset_id: str) -> str:
        """Walk to the trial that owns this asset. Frames resolve to their clip."""
        seen = set()
        cur = asset_id
        while True:
            if cur in seen:
                raise HarnessError(f"provenance cycle at {cur}")
            seen.add(cur)
            p = self.provenance.get(cur)
            if p is None:
                raise HarnessError(f"unknown asset {cur}")
            if not p.parent_asset_id:
                return cur
            cur = p.parent_asset_id

    # --------------------------------------------------------------- measuring
    def measure(self, asset_id: str, capability: str, instrument_id: str,
                item: dict, observation_unit: str = "frame",
                sampled_frames: int | None = None) -> Measurement:
        """Run ONE evaluator over an EXISTING asset. Never generates.

        INVARIANT 2 - many measurements may point at one asset.
        """
        if asset_id not in self.provenance:
            raise HarnessError(f"unknown asset {asset_id}")
        instr = self.instruments.get(instrument_id)
        if instr is None:
            raise HarnessError(f"unknown instrument {instrument_id}")
        if capability not in instr.capabilities:
            raise HarnessError(
                f"instrument {instrument_id} is not specified for capability "
                f"{capability}. Qualification NEVER generalises across "
                f"judgement families.")
        if capability not in item.get("measurement_fanout", []):
            raise HarnessError(
                f"capability {capability} is not in item {item['item_id']}'s "
                f"measurement fan-out. The bank decides what an asset may "
                f"validly evidence, not the caller.")

        prov = self.provenance[asset_id]
        mid = self._new_id("msr", f"{asset_id}|{capability}|{instrument_id}|{len(self.measurements)}")

        if prov.api_status != "ok":
            m = Measurement(
                measurement_id=mid, asset_id=asset_id,
                trial_asset_id=self.trial_asset_id(asset_id) if prov.asset_id else "",
                item_id=item["item_id"], capability=capability, verdict="absent",
                absence_reason="refused" if prov.api_status == "refused" else "generation_failed",
                instrument_id=instr.id, instrument_version=instr.version,
                instrument_config_hash=instr.config_hash,
                instrument_qualification_status=instr.qualification_status,
                observation_unit=observation_unit, measured_at=self._clock(),
                synthetic=True)
            self.measurements.append(m)
            return m

        r = instr.fn(pathlib.Path(prov.output_path).read_text(), item, capability)
        verdict = r.get("verdict", "absent")
        if verdict not in VERDICTS:
            raise HarnessError(f"instrument returned unknown verdict {verdict}")
        absence = r.get("absence_reason")
        if verdict == "absent" and absence not in ABSENCE_REASONS:
            raise HarnessError(
                f"absent verdict needs a reason from {ABSENCE_REASONS}; got {absence}")
        if verdict != "absent" and absence is not None:
            raise HarnessError("a pass/fail verdict must not carry an absence reason")

        m = Measurement(
            measurement_id=mid, asset_id=asset_id,
            trial_asset_id=self.trial_asset_id(asset_id),
            item_id=item["item_id"], capability=capability, verdict=verdict,
            absence_reason=absence, instrument_id=instr.id,
            instrument_version=instr.version, instrument_config_hash=instr.config_hash,
            instrument_qualification_status=instr.qualification_status,
            instrument_calibration_ref=instr.calibration_ref,
            observation_unit=observation_unit, sampled_frames=sampled_frames,
            defects=r.get("defects", []),          # MULTIPLE defects permitted
            cost_evaluator=instr.cost_per_call, latency_s=r.get("latency_s"),
            measured_at=self._clock(), synthetic=True)
        self.measurements.append(m)
        return m

    def fan_out(self, asset_id: str, item: dict, routing: dict[str, str]) -> list[Measurement]:
        """Score ONE asset on every eligible capability. No regeneration."""
        out = []
        for cap in item.get("measurement_fanout", []):
            iid = routing.get(cap)
            if iid is None:
                continue
            out.append(self.measure(asset_id, cap, iid, item))
        return out

    # ---------------------------------------------------------------- analysis
    def failure_cooccurrence(self) -> dict:
        """Which defects appear TOGETHER on one output.

        Counting term frequencies cannot express two defects on one output, and
        a real recorded case was lost that way. Repair selection depends on
        knowing what co-occurs.
        """
        per_asset: dict[str, set] = {}
        for m in self.measurements:
            for d in m.defects:
                per_asset.setdefault(m.asset_id, set()).add(d["term"])
        pairs: dict[tuple, int] = {}
        for terms in per_asset.values():
            ts = sorted(terms)
            for i in range(len(ts)):
                for j in range(i + 1, len(ts)):
                    pairs[(ts[i], ts[j])] = pairs.get((ts[i], ts[j]), 0) + 1
        return {"per_asset_defect_sets": {k: sorted(v) for k, v in per_asset.items()},
                "co_occurrence": {f"{a} + {b}": n for (a, b), n in sorted(pairs.items())},
                "multi_defect_assets": sum(1 for v in per_asset.values() if len(v) > 1)}

    def operational_metrics(self) -> dict:
        atts = list(self.attempts.values())
        n = len(atts)
        gen = sum(a.cost_generation or 0 for a in self.provenance.values())
        ev = sum(m.cost_evaluator or 0 for m in self.measurements)
        return {
            "attempts": n,
            "assets_produced": sum(1 for a in atts if a.api_status == "ok"),
            "api_errors": sum(1 for a in atts if a.api_status == "error"),
            "refusals": sum(1 for a in atts if a.api_status == "refused"),
            "error_classes": {c: sum(1 for a in atts if a.error_class == c)
                              for c in {a.error_class for a in atts} if c},
            # E-C4: these are DIFFERENT numbers and are never summed together.
            "experimental_repeats": sum(1 for a in atts if a.is_experimental_repeat()),
            "production_retries": sum(1 for a in atts if a.is_production_retry()),
            "trial_assets": len({self.trial_asset_id(a) for a in self.provenance}),
            "derived_assets": sum(1 for p in self.provenance.values() if p.parent_asset_id),
            "measurements": len(self.measurements),
            # Cost components stay separate, always.
            "cost_generation_total": round(gen, 6),
            "cost_evaluator_total": round(ev, 6),
            "measurements_per_trial_asset": (
                round(len(self.measurements) / max(1, len({self.trial_asset_id(a)
                      for a in self.provenance})), 2)),
            "routing_scores_computed": 0,      # INVARIANT 8 - never
            # CpAO divides the cost of a RETRY CHAIN by accepted outcomes.
            # Experimental repeats are excluded on purpose: they are an
            # experiment-design cost, not the cost of rescuing one outcome.
            "cost_in_retry_chains": round(sum(
                a.cost_generation or 0 for a in atts
                if a.is_production_retry()), 6),
            "cost_in_experimental_repeats": round(sum(
                a.cost_generation or 0 for a in atts
                if a.is_experimental_repeat()), 6),
        }

    def retry_chain(self, attempt_id: str) -> list[str]:
        """Ordered production-retry chain ending at this attempt.

        Follows retry_of ONLY. An experimental repeat is never part of a chain,
        because nothing failed to cause it.
        """
        chain, cur, seen = [], attempt_id, set()
        while cur:
            if cur in seen:
                raise HarnessError(f"retry chain cycle at {cur}")
            seen.add(cur)
            chain.append(cur)
            a = self.attempts.get(cur)
            if a is None:
                raise HarnessError(f"unknown attempt {cur} in retry chain")
            cur = a.retry_of_attempt_id
        return list(reversed(chain))

    # ---------------------------------------------------------------- registry
    # --- E-C5: a Registry row is ONE cell. These must agree across every
    # scoreable measurement in it, or the row is not a measurement of anything.
    CELL_KEYS_MEASUREMENT = (
        "capability", "instrument_id", "instrument_version",
        "instrument_config_hash", "instrument_qualification_status",
        "observation_unit",
    )
    CELL_KEYS_PROVENANCE = (
        "provider", "model", "version", "endpoint", "workflow", "lane",
        "config_hash",
    )

    def write_registry_row(self, capability: str, instrument_id: str,
                           measurements: list[Measurement], conditions: dict,
                           difficulty_level: int, repeats_per_item: int
                           ) -> RegistryRow:
        """Write an empirical Registry row - refusing far more often than not.

        INVARIANT 5 - every row names an exact instrument configuration.
        INVARIANT 9 - no synthetic measurement may EVER become a row.
                      E-C6: there is NO override parameter. None exists.
        E-C5      - the row must be ONE coherent cell. Mixing two models, two
                    capabilities, two instrument configurations or incompatible
                    conditions produces a number that describes nothing, and a
                    plausible-looking average is worse than no row at all.
        """
        instr = self.instruments[instrument_id]
        if not instr.registry_writable:
            raise HarnessError(
                f"REGISTRY WRITE REFUSED: instrument {instr.id} has "
                f"qualification status '{instr.qualification_status}'. Only "
                f"{REGISTRY_WRITABLE} may produce a Registry row. A capability "
                f"number produced by an unqualified checker is not a weak "
                f"measurement - it is not a measurement.")
        if not measurements:
            raise HarnessError("REGISTRY WRITE REFUSED: no measurements. "
                               "An empty check is not a passing check.")

        # E-C6: absolute. No parameter, flag or call option can bypass this.
        if any(m.synthetic for m in measurements):
            raise HarnessError(
                "REGISTRY WRITE REFUSED: synthetic/dummy measurements may never "
                "become empirical Registry rows. There is no override.")

        scored = [m for m in measurements if m.verdict in ("pass", "fail")]
        if not scored:
            raise HarnessError("REGISTRY WRITE REFUSED: no scoreable measurements")

        # ---- E-C5 homogeneity: measurement-side ----------------------------
        for k in self.CELL_KEYS_MEASUREMENT:
            vals = {getattr(m, k) for m in scored}
            if len(vals) > 1:
                raise HarnessError(
                    f"REGISTRY WRITE REFUSED: mixed cell. Measurements disagree "
                    f"on '{k}': {sorted(map(str, vals))}. One row is one "
                    f"vendor+model+version+workflow+capability+conditions; "
                    f"aggregating across a difference produces a number that "
                    f"describes nothing.")

        # ...and they must match what the CALLER asked for, not merely agree
        # with each other. A self-consistent row about the wrong thing is worse.
        if scored[0].capability != capability:
            raise HarnessError(
                f"REGISTRY WRITE REFUSED: requested capability '{capability}' "
                f"but measurements are for '{scored[0].capability}'.")
        if scored[0].instrument_id != instrument_id:
            raise HarnessError(
                f"REGISTRY WRITE REFUSED: requested instrument "
                f"'{instrument_id}' but measurements came from "
                f"'{scored[0].instrument_id}'.")
        if scored[0].instrument_config_hash != instr.config_hash:
            raise HarnessError(
                "REGISTRY WRITE REFUSED: measurements carry a different "
                "instrument configuration hash than the instrument now "
                "registered. A prompt or threshold change makes a DIFFERENT "
                "instrument and its results may not be pooled.")

        # ---- E-C5 homogeneity: provenance-side -----------------------------
        provs = []
        for m in scored:
            pr = self.provenance.get(m.trial_asset_id)
            if pr is None:
                raise HarnessError(
                    f"REGISTRY WRITE REFUSED: measurement {m.measurement_id} "
                    f"references unknown trial asset {m.trial_asset_id}.")
            provs.append(pr)
        for k in self.CELL_KEYS_PROVENANCE:
            vals = {getattr(pr, k) for pr in provs}
            if len(vals) > 1:
                raise HarnessError(
                    f"REGISTRY WRITE REFUSED: mixed cell. Trials disagree on "
                    f"'{k}': {sorted(map(str, vals))}. Two providers, models, "
                    f"versions, endpoints, workflows or request configurations "
                    f"may never share one Registry row.")

        # ---- E-C5 declared conditions must not contradict the trials -------
        for ck, cv in (conditions or {}).items():
            seen = {getattr(pr, ck) for pr in provs if hasattr(pr, ck)}
            if seen and len(seen) == 1 and str(next(iter(seen))) != str(cv):
                raise HarnessError(
                    f"REGISTRY WRITE REFUSED: declared condition {ck}={cv!r} "
                    f"contradicts the trials, which carry {next(iter(seen))!r}.")

        # ---- E-C5/E-C4 repeat structure must be REAL, not caller-asserted --
        n_items = len({m.item_id for m in scored})
        trials = len({m.trial_asset_id for m in scored})
        by_item = {}
        for pr in provs:
            by_item.setdefault(pr.item_id, set()).add(pr.attempt_id)
        observed_max = max((len(v) for v in by_item.values()), default=0)
        if repeats_per_item < 1:
            raise HarnessError("REGISTRY WRITE REFUSED: repeats_per_item must be >= 1.")
        if observed_max > repeats_per_item:
            raise HarnessError(
                f"REGISTRY WRITE REFUSED: caller declared repeats_per_item="
                f"{repeats_per_item} but an item has {observed_max} distinct "
                f"attempts. The declared repeat count is not trusted over the "
                f"attempts actually present - that is how repeats get counted "
                f"as independent items and confidence gets overstated.")
        # A production retry is NOT a repeat and must not be pooled as one.
        retries = [pr for pr in provs if pr.is_production_retry()]
        if retries:
            raise HarnessError(
                f"REGISTRY WRITE REFUSED: {len(retries)} trial(s) in this cell "
                f"are production RETRIES. A retry exists because something "
                f"failed; pooling it with clean trials biases the pass rate "
                f"upward. Retries belong to the acceptance/CpAO chain, not to a "
                f"capability pass-rate cell.")

        passes = sum(1 for m in scored if m.verdict == "pass")
        gen_cost = sum(pr.cost_generation or 0 for pr in provs)
        ev_cost = sum(m.cost_evaluator or 0 for m in scored)
        cell = gen_cost + ev_cost
        # ZERO-PASS RULE: never infinity, never a sentinel.
        upp = round(cell / passes, 6) if passes else None
        lower = None if passes else round(cell, 6)

        row = RegistryRow(
            entry_id=self._new_id("cap", f"{capability}|{instrument_id}|{len(self.registry_rows)}"),
            provider=provs[0].provider, model=provs[0].model,
            version=provs[0].version, endpoint=provs[0].endpoint,
            workflow=provs[0].workflow,
            capability=capability, difficulty_level=difficulty_level,
            observation_unit=scored[0].observation_unit, conditions=conditions,
            n_items=n_items, repeats_per_item=repeats_per_item, trials=trials,
            passes=passes, pass_rate=round(passes / len(scored), 6),
            failed_trials=[{"trial_id": m.trial_asset_id, "defects": m.defects}
                           for m in scored if m.verdict == "fail"],
            instrument_id=instr.id, instrument_version=instr.version,
            instrument_config_hash=instr.config_hash,
            instrument_qualification_status=instr.qualification_status,
            instrument_calibration_ref=instr.calibration_ref,
            cost_generation_total=round(gen_cost, 6),
            cost_evaluator_total=round(ev_cost, 6),
            usd_per_pass=upp, usd_per_pass_lower_bound=lower,
            tested_date=self._clock(),
            synthetic=False)
        self.registry_rows.append(row)
        return row

    # ------------------------------------------------------------ storage out
    # E-C7: Resources owns the durable attempt/artifact/measurement/acceptance
    # storage contract; Eval owns measurement semantics. Eval therefore emits
    # the canonical FOUR-RECORD model and does NOT keep a competing persistent
    # manifest of its own.

    STORAGE_CLASS = "C_irreproducible_empirical"

    def emit_attempts(self) -> list[dict]:
        """One record per provider/transform call - INCLUDING failures.

        An attempt is written because the call was MADE, not because it
        succeeded. A refusal or timeout cost money and latency and produced no
        asset; all three facts matter and none may be reduced to an aggregate
        counter. Attempts with no artifact survive here on their own.
        """
        out = []
        for aid, a in sorted(self.attempts.items()):
            out.append({
                "attempt_id": a.attempt_id,
                "eval_item_id": a.item_id,
                "provider": a.provider,
                "model_id": a.model,
                "model_version": a.version,
                "endpoint": a.endpoint,
                "workflow": a.workflow,
                "lane": a.lane,
                "config_hash": a.config_hash,
                "config_location": a.config_path,
                "reference_asset_hashes": a.reference_hashes,
                "input_hashes": a.input_hashes,
                "seed": a.seed,
                "seed_policy": a.seed_policy,
                "requested_at": a.requested_at,
                "completed_at": a.completed_at,
                "api_status": a.api_status,
                "error_detail": a.error_class,
                # E-C4: two INDEPENDENT concepts, never interchangeable.
                "repeat_index": a.repeat_index,
                "repeat_of_attempt_id": a.repeat_of_attempt_id,
                "retry_of_attempt_id": a.retry_of_attempt_id,
                "retry_reason": a.retry_reason,
                "cost_generation": a.cost_generation,
                "cost_transform": a.cost_transform,
                "currency": a.currency,
                "produced_artifact": a.asset_id or None,
            })
        return out

    def emit_artifacts(self) -> list[dict]:
        """Bytes produced by an attempt. Derived assets point to their parent
        and add NO independent trial."""
        out = []
        for aid, p in sorted(self.provenance.items()):
            # output_location is recorded RELATIVE to the harness root. An
            # absolute working path is machine-specific noise that makes an
            # otherwise deterministic handoff differ on every run, and would
            # be meaningless to Resources when it archives these rows.
            loc = p.output_path
            if loc:
                try:
                    loc = str(pathlib.Path(loc).relative_to(self.root))
                except ValueError:
                    pass
            out.append({
                "artifact_id": aid,
                "attempt_id": p.attempt_id,
                "eval_item_id": p.item_id,
                "trial_artifact_id": self.trial_asset_id(aid),
                "parent_artifact_id": p.parent_asset_id,
                "derivation": p.derivation,
                "is_derived": bool(p.parent_asset_id),
                "output_hash": p.output_sha256,
                "output_location": loc,
                "storage_class": self.STORAGE_CLASS,
            })
        return out

    def emit_measurements(self) -> list[dict]:
        """Many per artifact. Eval owns the semantics of every field here."""
        out = []
        for m in self.measurements:
            out.append({
                "measurement_id": m.measurement_id,
                "artifact_id": m.asset_id,
                "trial_artifact_id": m.trial_asset_id,
                "eval_item_id": m.item_id,
                "capability_id": m.capability,
                "instrument_ref": {
                    "id": m.instrument_id,
                    "version": m.instrument_version,
                    "config_hash": m.instrument_config_hash,
                    "qualification_status": m.instrument_qualification_status,
                    "qualification_ref": (m.instrument_calibration_ref
                                          or "required_but_no_calibrated_instrument"),
                },
                # Canon/Eval canonical vocabulary, verbatim. No Resources-side
                # or Eval-side second vocabulary is introduced.
                "observation_unit": m.observation_unit,
                "sampled_frames": m.sampled_frames,
                "result": m.verdict,
                "absence_reason": m.absence_reason,
                "defects": m.defects,
                "evaluator_cost": m.cost_evaluator,
                "measured_at": m.measured_at,
                "synthetic": m.synthetic,
            })
        return out

    def emit_acceptances(self) -> list[dict]:
        """Eval does NOT decide acceptance in the benchmark harness.

        Acceptance is a production decision made by a person or an approved
        production experiment. Inventing one here would manufacture the
        numerator of Cost per Accepted Outcome. This is deliberately empty.
        """
        return []

    def emit_storage_handoff(self, path: pathlib.Path) -> dict:
        path = pathlib.Path(path)
        path.mkdir(parents=True, exist_ok=True)
        parts = {
            "attempts": self.emit_attempts(),
            "artifacts": self.emit_artifacts(),
            "measurements": self.emit_measurements(),
            "acceptances": self.emit_acceptances(),
        }
        for name, rows in parts.items():
            (path / f"{name}.jsonl").write_text(
                "".join(json.dumps(r, sort_keys=True) + "\n" for r in rows))
        summary = {
            "contract": "resources_canonical_v1",
            "records": {k: len(v) for k, v in parts.items()},
            "attempts_without_artifact": sum(
                1 for a in parts["attempts"] if not a["produced_artifact"]),
            "derived_artifacts": sum(1 for a in parts["artifacts"] if a["is_derived"]),
            "trial_artifacts": len({a["trial_artifact_id"] for a in parts["artifacts"]}),
            "acceptance_decided_by_eval": False,
            "observation_unit_vocabulary": sorted(
                {m["observation_unit"] for m in parts["measurements"]}),
        }
        (path / "handoff-summary.json").write_text(
            json.dumps(summary, indent=2, sort_keys=True))
        return summary

    def dump(self, path: pathlib.Path):
        """Emit the canonical handoff plus Eval-local analysis views.

        The analysis views are DERIVED and disposable. They are not a second
        persistent store and Resources should never archive them.
        """
        path = pathlib.Path(path)
        self.emit_storage_handoff(path)
        (path / "operational-metrics.json").write_text(
            json.dumps(self.operational_metrics(), indent=2, sort_keys=True))
        (path / "failure-cooccurrence.json").write_text(
            json.dumps(self.failure_cooccurrence(), indent=2, sort_keys=True))
