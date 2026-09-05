"""BatteryHarness(Harness): the frozen V1 harness with bytes-aware artifact I/O. Nothing else changes.

WHAT IS OVERRIDDEN, AND WHY

    generate()   the frozen harness writes a TEXT payload (`p.write_text(payload)`); a battery artifact is
                 bytes (PNG / MP4 / WAV). The override feeds the frozen generate() a small text pointer
                 (`BYTES:<sha256>:<len>:<content_type>`) so every guard it has (duplicate generation,
                 repeat-vs-retry, lane vocabulary, one call = one trial) still runs, then writes the real
                 bytes beside it as `<asset_id><ext>` and points the provenance record at those bytes.
    measure()    the frozen harness hands the instrument `read_text()` of the artifact; the override hands
                 it the PATH. Every other check (unknown asset / instrument / capability fan-out / failed
                 attempt) is repeated verbatim, and the Measurement is built the same way.

WHAT IS INHERITED, DELIBERATELY

    write_registry_row   NOT overridden. `BatteryHarness.write_registry_row is Harness.write_registry_row`
                         is a test. registry_row_for() only adds the registry gate IN FRONT of it and the
                         SCHEMA-v1 uncertainty block AFTER it.
    everything else      derive_frames, trial ids, operational metrics, storage handoff, dump.

This task writes no Registry row anywhere; the class exists so Stage A can, once a Controller freezes
a criterion (MD-C1) and ratifies the instrument's use.
"""
from __future__ import annotations

import pathlib

import hv2_paths  # noqa: F401
import harness as H
from models import ABSENCE_REASONS, Measurement, VERDICTS, sha256_str
import store as S
from instruments import registry_gate as RG


class BatteryHarness(H.Harness):
    def __init__(self, root, clock=None):
        super().__init__(root, clock)
        self._real_assets: set = set()          # asset ids whose generator declared synthetic: false

    # ---------------------------------------------------------------- generation
    def generate(self, item: dict, provider_cfg: dict, generator, **kw):
        """Same contract as Harness.generate; the generator returns `payload_bytes` + `content_type`."""
        holder: dict = {}

        def text_generator(it, cfg):
            r = generator(it, cfg)
            if r.get("api_status", "ok") != "ok":
                return r
            data = r.get("payload_bytes")
            if "payload" in r and data is None:
                raise TypeError("a battery artifact is bytes (payload_bytes), never a text payload")
            if not isinstance(data, (bytes, bytearray)) or not data:
                raise TypeError("generator returned no bytes for an ok attempt; an empty artifact is not an artifact")
            data = bytes(data)
            holder["bytes"] = data
            holder["content_type"] = r.get("content_type") or "application/octet-stream"
            holder["synthetic"] = r.get("synthetic", True)
            pointer = f"BYTES:{sha256_str(data.decode('latin-1'))}:{len(data)}:{holder['content_type']}"
            return {**{k: v for k, v in r.items() if k not in ("payload_bytes",)}, "payload": pointer}

        prov = super().generate(item, provider_cfg, text_generator, **kw)
        if prov.api_status == "ok" and "bytes" in holder:
            ct = holder["content_type"].split(";")[0].strip().lower()
            ext = S.EXT_BY_CONTENT_TYPE.get(ct, ".bin")
            p = self.assets_dir / f"{prov.asset_id}{ext}"
            if p.exists():
                raise H.HarnessError(f"asset {prov.asset_id} already on disk - assets are immutable")
            p.write_bytes(holder["bytes"])
            import hashlib
            prov.output_path = str(p)
            prov.output_sha256 = hashlib.sha256(holder["bytes"]).hexdigest()
            prov.output_bytes = len(holder["bytes"])
            prov.media_kind = next((k for pfx, k in S.MEDIA_KIND_BY_PREFIX.items() if ct.startswith(pfx)), prov.media_kind)
            if holder["synthetic"] is False:
                self._real_assets.add(prov.asset_id)
        return prov

    # ---------------------------------------------------------------- measuring
    def measure(self, asset_id: str, capability: str, instrument_id: str, item: dict,
                observation_unit: str = "artifact", sampled_frames: int | None = None) -> Measurement:
        """Harness.measure with the artifact handed to the instrument as a PATH (bytes on disk)."""
        if asset_id not in self.provenance:
            raise H.HarnessError(f"unknown asset {asset_id}")
        instr = self.instruments.get(instrument_id)
        if instr is None:
            raise H.HarnessError(f"unknown instrument {instrument_id}")
        if capability not in instr.capabilities:
            raise H.HarnessError(f"instrument {instrument_id} is not specified for capability {capability}. "
                                 f"Qualification NEVER generalises across judgement families.")
        if capability not in item.get("measurement_fanout", []):
            raise H.HarnessError(f"capability {capability} is not in item {item['item_id']}'s measurement fan-out.")
        prov = self.provenance[asset_id]
        mid = self._new_id("msr", f"{asset_id}|{capability}|{instrument_id}|{len(self.measurements)}")
        if prov.api_status != "ok":
            raise H.HarnessError(f"attempt {prov.attempt_id} has status {prov.api_status!r} and produced no artifact, so there is "
                                 f"nothing to measure; the failure is already preserved on the attempt row.")
        r = instr.fn(pathlib.Path(prov.output_path), item, capability)
        verdict = r.get("verdict", "absent")
        if verdict not in VERDICTS:
            raise H.HarnessError(f"instrument returned unknown verdict {verdict}")
        absence = r.get("absence_reason")
        if verdict == "absent" and absence not in ABSENCE_REASONS:
            raise H.HarnessError(f"absent verdict needs a reason from {ABSENCE_REASONS}; got {absence}")
        if verdict != "absent" and absence is not None:
            raise H.HarnessError("a pass/fail verdict must not carry an absence reason")
        m = Measurement(
            measurement_id=mid, asset_id=asset_id, trial_asset_id=self.trial_asset_id(asset_id),
            item_id=item["item_id"], capability=capability, verdict=verdict, absence_reason=absence,
            instrument_id=instr.id, instrument_version=instr.version, instrument_config_hash=instr.config_hash,
            instrument_qualification_status=instr.qualification_status, instrument_calibration_ref=instr.calibration_ref,
            observation_unit=observation_unit, sampled_frames=sampled_frames, defects=r.get("defects", []),
            cost_evaluator=instr.cost_per_call,
            evaluator_cost_ref=self._ledger_line(prov.attempt_id, "evaluator", instr.cost_per_call, prov.currency),
            latency_s=r.get("latency_s"), measured_at=self._clock(),
            synthetic=(self.trial_asset_id(asset_id) not in self._real_assets))
        self.measurements.append(m)
        return m

    # ---------------------------------------------------------------- registry
    def registry_row_for(self, capability: str, instrument_id: str, measurements, conditions: dict,
                         difficulty_level: int, repeats_per_item: int):
        """Registry gate in front, the INHERITED write_registry_row in the middle, uncertainty after."""
        instr = self.instruments.get(instrument_id)
        if instr is None:
            raise RG.RegistryGateRefused(f"unknown instrument {instrument_id}")
        RG.assert_registry_eligible(capability, instr)
        RG.assert_measurements_real(measurements)
        row = self.write_registry_row(capability, instrument_id, measurements, conditions, difficulty_level, repeats_per_item)
        RG.attach_uncertainty(row)
        return row
