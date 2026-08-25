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
                 retry_of: str | None = None, retry_reason: str | None = None,
                 force: bool = False) -> GenerationProvenance:
        """Make ONE generation attempt for one item.

        INVARIANT 3 - a retry is a NEW attempt id and NEVER replaces an output.
        INVARIANT 4 (guard) - refuses to regenerate an item/config that already
        has a successful asset, unless it is an explicit retry or forced.
        """
        cfg = dict(provider_cfg)
        chash = config_hash({"item": item["item_id"], **cfg})
        key = (item["item_id"], chash)

        if key in self._generated and retry_of is None and not force:
            raise HarnessError(
                f"DUPLICATE GENERATION REFUSED for item {item['item_id']} "
                f"config {chash[:12]}: asset {self._generated[key]} already "
                f"exists. Evaluating another capability on an existing asset "
                f"needs NO new generation - that is the point of the bank's "
                f"measurement fan-out. If this is a deliberate reliability "
                f"repeat, pass retry_of/retry_reason so it is recorded as a "
                f"new attempt rather than silently duplicating a trial.")

        if retry_of is not None and retry_of not in self.attempts:
            raise HarnessError(f"retry_of references unknown attempt {retry_of}")

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
            "retries": sum(1 for a in atts if a.retry_of_attempt_id),
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
        }

    # ---------------------------------------------------------------- registry
    def write_registry_row(self, capability: str, instrument_id: str,
                           measurements: list[Measurement], conditions: dict,
                           difficulty_level: int, repeats_per_item: int,
                           allow_synthetic: bool = False) -> RegistryRow:
        """Write an empirical Registry row - refusing far more often than not.

        INVARIANT 5 - every row names an exact instrument configuration.
        INVARIANT 9 - no synthetic measurement may ever become a row.
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
        if any(m.synthetic for m in measurements) and not allow_synthetic:
            raise HarnessError(
                "REGISTRY WRITE REFUSED: synthetic/dummy measurements may never "
                "become empirical Registry rows.")

        scored = [m for m in measurements if m.verdict in ("pass", "fail")]
        if not scored:
            raise HarnessError("REGISTRY WRITE REFUSED: no scoreable measurements")

        # n_items counts INDEPENDENT base items, not trials and not frames.
        n_items = len({m.item_id for m in scored})
        trials = len({m.trial_asset_id for m in scored})
        passes = sum(1 for m in scored if m.verdict == "pass")
        gen_cost = sum(self.provenance[m.trial_asset_id].cost_generation or 0
                       for m in scored)
        ev_cost = sum(m.cost_evaluator or 0 for m in scored)
        cell = gen_cost + ev_cost
        # ZERO-PASS RULE: never infinity, never a sentinel.
        upp = round(cell / passes, 6) if passes else None
        lower = None if passes else round(cell, 6)

        row = RegistryRow(
            entry_id=self._new_id("cap", f"{capability}|{instrument_id}|{len(self.registry_rows)}"),
            provider=self.provenance[scored[0].trial_asset_id].provider,
            model=self.provenance[scored[0].trial_asset_id].model,
            version=self.provenance[scored[0].trial_asset_id].version,
            endpoint=self.provenance[scored[0].trial_asset_id].endpoint,
            workflow=self.provenance[scored[0].trial_asset_id].workflow,
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
            synthetic=any(m.synthetic for m in measurements))
        self.registry_rows.append(row)
        return row

    # ------------------------------------------------------------ storage out
    def artifact_manifest(self) -> list[dict]:
        """The handoff Resources archives. One row per asset."""
        rows = []
        for aid, p in sorted(self.provenance.items()):
            refs = [m.measurement_id for m in self.measurements if m.asset_id == aid]
            d = p.to_dict()
            d["trial_asset_id"] = self.trial_asset_id(aid)
            d["evaluator_result_refs"] = refs
            # Store the path RELATIVE to the harness root. An absolute working
            # path is machine-specific noise that makes an otherwise
            # deterministic manifest look like it changed between runs.
            if d.get("output_path"):
                try:
                    d["output_path"] = str(pathlib.Path(d["output_path"])
                                           .relative_to(self.root))
                except ValueError:
                    pass
            rows.append(d)
        return rows

    def dump(self, path: pathlib.Path):
        path = pathlib.Path(path)
        path.mkdir(parents=True, exist_ok=True)
        (path / "artifact-manifest.jsonl").write_text(
            "\n".join(json.dumps(r, sort_keys=True) for r in self.artifact_manifest()) + "\n")
        (path / "measurements.jsonl").write_text(
            "\n".join(json.dumps(m.to_dict(), sort_keys=True) for m in self.measurements) + "\n")
        (path / "operational-metrics.json").write_text(
            json.dumps(self.operational_metrics(), indent=2, sort_keys=True))
        (path / "failure-cooccurrence.json").write_text(
            json.dumps(self.failure_cooccurrence(), indent=2, sort_keys=True))
