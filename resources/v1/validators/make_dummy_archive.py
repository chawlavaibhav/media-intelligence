#!/usr/bin/env python3
"""Generate a DUMMY class-C archive at scale, proving the schema holds >=1,000 attempts.

R-C3: this writes into a BUILD DIRECTORY and is never committed. It is a deterministic proof
artifact, not evidence. What is committed is the generator, the expected counts and the fingerprint
the validator checks against.

EVERY VALUE IS SYNTHETIC. Vendor and model names are deliberately fictional ('dummy-vendor-a',
'dummy-image-v0') so nothing here can be mistaken for a real endpoint, price or capability claim.
No provider was called and no money was spent.

Determinism: hashes derive from record identity, timestamps are fixed constants. The same command
produces byte-identical output every time.
"""
import argparse, hashlib, json, os

DEFAULT_OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "build", "empirical-archive-dummy")
N_ITEMS, N_REPEATS = 250, 4          # 1,000 attempts
T0, T1 = "2026-01-01T00:00:00Z", "2026-01-01T00:00:30Z"

# capability ids are Eval's canonical ids, stored verbatim; observation units are the canonical
# vocabulary, stored verbatim. Resources invents neither.
# lane ids are the FROZEN machine vocabulary (RI-C2): image | general_video | native_av | lipsync | tts
LANES = [
    ("dummy-vendor-a", "dummy-image-v0", "images.generate", "single_call", "image", "image",
     [("exact_text_latin", "whole_asset"), ("object_count", "whole_asset"),
      ("attribute_binding", "whole_asset"), ("spatial_relationship", "whole_asset"),
      ("delivery_format_compliance", "whole_asset"), ("typography_legibility", "whole_asset")]),
    ("dummy-vendor-b", "dummy-video-v0", "video.generate", "single_call", "general_video", "video",
     [("action_adherence", "whole_asset"), ("motion_action_quality", "sequence"),
      ("physics_material_appearance", "frame"), ("person_stability_in_clip", "asset_set_over_time"),
      ("text_logo_stability_in_clip", "asset_set_over_time"),
      ("delivery_format_compliance", "whole_asset"), ("multi_shot_spatial_continuity", "shot_pair")]),
    ("dummy-vendor-c", "dummy-av-v0", "av.generate", "single_call", "native_av", "audio_video",
     [("spoken_language_correctness", "whole_asset"), ("single_speaker_lip_sync", "sequence"),
      ("audio_video_synchronisation", "sequence"), ("emotional_prosodic_fit", "whole_asset"),
      ("delivery_format_compliance", "whole_asset")]),
]


def h(s):
    return hashlib.sha256(s.encode()).hexdigest()


def build():
    attempts, artifacts, measurements, acceptances, ledger = [], [], [], [], []
    for i in range(N_ITEMS):
        vendor, model, endpoint, workflow, lane, kind, caps = LANES[i % len(LANES)]
        item = f"DUMMY-ITEM-{i:04d}"
        for k in range(N_REPEATS):
            aid = f"DUMMY-ATT-{i:04d}-{k}"
            # RI-C1: ONE CALL = ONE TRIAL. Each repeat is its own trial, linked backward by
            # repeat_of_attempt_id rather than by sharing a trial id.
            trial = f"DUMMY-TRIAL-{i:04d}-{k}"
            n = i * N_REPEATS + k
            status = "refusal" if n % 47 == 0 else ("error" if n % 83 == 0 else "ok")
            ok = status == "ok"
            att = {
                "attempt_id": aid, "trial_id": trial, "eval_item_id": item,
                "provider": vendor, "model_id": model, "model_version": "dummy-2026-01-01",
                "endpoint": endpoint, "workflow": workflow, "lane": lane,
                "prompt_hash": h("prompt|" + item), "config_hash": h(f"config|{item}|{k}"),
                "config_location": f"dummy://configs/{item}/{k}.json",
                "reference_asset_hashes": [h("ref|" + item)] if i % 5 == 0 else [],
                "requested_at": T0, "completed_at": T1 if ok else None,
                "status": status, "cost_ref": f"LEDGER-GEN-{i:04d}-{k}",
                "storage_class": "C_irreproducible_empirical",
                # A deliberate reliability repeat. NOT a retry.
                "repeat_index": k,
                "repeat_of_attempt_id": None if k == 0 else f"DUMMY-ATT-{i:04d}-0",
                "retry_of_attempt_id": None,
                "retry_reason": None,
                "seed": (i * 100 + k) if vendor == "dummy-vendor-a" else None,
                "settings": {"note": "synthetic placeholder, not a real provider setting"},
                "error_detail": None if ok else f"synthetic {status} for schema testing",
                "latency_ms": 30000 if ok else None,
            }
            attempts.append(att)
            # RI-C4: cost is a REFERENCE to an immutable entry. Clearly synthetic basis - a synthetic
            # test may never carry a fabricated real-provider cost.
            ledger.append({
                "ledger_entry_id": f"LEDGER-GEN-{i:04d}-{k}", "attempt_id": aid,
                "amount": 0.0, "currency": "XTS", "unit": "call", "recorded_at": T1,
                "basis": "synthetic_test", "immutable": True, "synthetic": True,
                "note": "synthetic placeholder; no provider was called and no money was spent",
            })
            if not ok:
                continue                       # no artifact: the call produced nothing
            art_id = f"DUMMY-ART-{i:04d}-{k}"
            artifacts.append({
                "artifact_id": art_id, "attempt_id": aid, "trial_id": trial,
                "output_hash": h("output|" + art_id), "output_bytes": 1_048_576,
                "output_location": f"dummy://artifacts/{art_id}", "media_kind": kind,
                "storage_class": "C_irreproducible_empirical",
                "derived_from_artifact_id": None, "derivation_type": None, "derivation_params": None,
            })
            # A sampled frame: a DERIVED artifact of the same trial and attempt, never a new trial.
            if kind in ("video", "audio_video") and k == 0:
                fid = art_id + "-FRAME-0"
                artifacts.append({
                    "artifact_id": fid, "attempt_id": aid, "trial_id": trial,
                    "output_hash": h("frame|" + fid), "output_bytes": 204_800,
                    "output_location": f"dummy://artifacts/{fid}", "media_kind": "image",
                    "storage_class": "C_irreproducible_empirical",
                    "derived_from_artifact_id": art_id, "derivation_type": "frame_sample",
                    "derivation_params": {"timestamp_s": 1.5},
                })
            for cap, unit in caps:
                measurements.append({
                    "measurement_id": f"DUMMY-MEAS-{art_id}-{cap}",
                    "artifact_id": art_id, "trial_id": trial,
                    "capability_id": cap,
                    "instrument_ref": f"dummy-instrument::{cap}", "instrument_version": "v0",
                    "instrument_config_hash": h(f"instrument|{cap}|v0"),
                    "instrument_qualification_ref": "required_but_no_calibrated_instrument",
                    "observation_unit": unit,
                    "result": {"dummy": True}, "absence_reason": None,
                    "defects": [], "measured_at": T1,
                    "evaluator_cost_ref": f"LEDGER-EVAL-{art_id}-{cap}",
                })
                ledger.append({
                    "ledger_entry_id": f"LEDGER-EVAL-{art_id}-{cap}",
                    "measurement_id": f"DUMMY-MEAS-{art_id}-{cap}",
                    "amount": 0.0, "currency": "XTS", "unit": "call", "recorded_at": T1,
                    "basis": "synthetic_test", "immutable": True, "synthetic": True,
                    "note": "synthetic evaluator cost, recorded separately from generation cost",
                })
        # Acceptance references only the FIRST attempt; retry_chain holds retries only, and this
        # synthetic run has none, so the chain is the single delivered attempt.
        item_ok = [a for a in attempts if a["eval_item_id"] == item and a["status"] == "ok"]
        if item_ok:
            first_ok = item_ok[0]
            acceptances.append({
                "acceptance_id": f"DUMMY-ACC-{item}", "trial_id": first_ok["trial_id"],
                "artifact_id": f"DUMMY-ART-{first_ok['attempt_id'].split('-',2)[2]}".replace(
                    "DUMMY-ART-", "DUMMY-ART-"),
                "accepted": (i % 3 != 0), "decided_by": "dummy-human-reviewer",
                "decided_at": T1, "brief_ref": f"DUMMY-BRIEF-{i % 10:02d}",
                "rejection_reasons": [] if i % 3 != 0 else ["synthetic_rejection_reason"],
                "retry_chain": [first_ok["attempt_id"]],
            })
    # fix acceptance artifact ids to real ones
    art_by_attempt = {r["attempt_id"]: r["artifact_id"] for r in artifacts
                      if r["derived_from_artifact_id"] is None}
    for c in acceptances:
        c["artifact_id"] = art_by_attempt.get(c["retry_chain"][0])
    return attempts, artifacts, measurements, acceptances, ledger


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=DEFAULT_OUT)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    sets = dict(zip(("attempts", "artifacts", "measurements", "acceptances", "cost_ledger"), build()))
    for name, rows in sets.items():
        with open(os.path.join(a.out, name + ".jsonl"), "w") as fh:
            for r in rows:
                fh.write(json.dumps(r, sort_keys=True) + "\n")
    print(f"[OK] dummy archive written to {a.out}")
    print("     " + " · ".join(f"{len(v):,} {k}" for k, v in sets.items()))


if __name__ == "__main__":
    main()
