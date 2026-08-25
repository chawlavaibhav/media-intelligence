#!/usr/bin/env python3
"""Generate a DUMMY class-C archive at scale, to prove the schema holds >=1,000 artifacts.

EVERY VALUE IS SYNTHETIC. No provider was called, no money was spent, no model produced anything.
Provider/model names are deliberately fictional placeholders ('dummy-vendor', 'dummy-image-v0') so
that nothing here can ever be mistaken for a real endpoint, a real price or a real capability claim.

Determinism: hashes are derived from the record's own identity, timestamps are fixed constants. The
same command produces byte-identical output every time.
"""
import hashlib, json, os, sys

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fixtures", "empirical-archive-dummy")
N_ITEMS, N_ATTEMPTS = 250, 4            # 1,000 artifacts
T0, T1 = "2026-01-01T00:00:00Z", "2026-01-01T00:00:30Z"

LANES = [
    ("dummy-vendor-a", "dummy-image-v0",    "images.generate",  "single_call",
     ["exact_text_latin", "object_count", "attribute_binding", "spatial_relationship",
      "delivery_format_compliance", "typography_legibility"], "image"),
    ("dummy-vendor-b", "dummy-video-v0",    "video.generate",   "single_call",
     ["action_adherence", "motion_action_quality", "physics_material_appearance",
      "person_stability_in_clip", "text_logo_stability_in_clip", "delivery_format_compliance",
      "multi_shot_spatial_continuity"], "whole_clip"),
    ("dummy-vendor-c", "dummy-av-v0",       "av.generate",      "single_call",
     ["spoken_language_correctness", "single_speaker_lip_sync", "audio_video_synchronisation",
      "emotional_prosodic_fit", "delivery_format_compliance"], "whole_clip"),
]


def h(s):
    return hashlib.sha256(s.encode()).hexdigest()


def main():
    os.makedirs(OUT, exist_ok=True)
    arts, meas, accs = [], [], []
    for i in range(N_ITEMS):
        vendor, model, endpoint, workflow, caps, unit = LANES[i % len(LANES)]
        item = f"DUMMY-ITEM-{i:04d}"
        for k in range(N_ATTEMPTS):
            aid = f"DUMMY-ART-{i:04d}-{k}"
            # Deterministic sprinkle of non-ok outcomes: they must survive in the record.
            status = "ok"
            if (i * N_ATTEMPTS + k) % 47 == 0:
                status = "refusal"
            elif (i * N_ATTEMPTS + k) % 83 == 0:
                status = "error"
            ok = status == "ok"
            arts.append({
                "artifact_id": aid, "trial_id": f"DUMMY-TRIAL-{i:04d}", "attempt_index": k,
                "eval_item_id": item, "provider": vendor, "model_id": model,
                "model_version": "dummy-2026-01-01", "endpoint": endpoint, "workflow": workflow,
                "prompt_hash": h("prompt|" + item), "config_hash": h("config|" + item + f"|{k}"),
                "config_location": f"dummy://configs/{item}/{k}.json",
                "reference_asset_hashes": [h("ref|" + item)] if i % 5 == 0 else [],
                "requested_at": T0, "completed_at": T1 if ok else None,
                "api_status": status,
                "output_hash": h("output|" + aid) if ok else None,
                "output_bytes": 1_048_576 if ok else None,
                "output_location": f"dummy://artifacts/{aid}" if ok else None,
                "cost_ref": f"dummy-ledger://{aid}",
                "storage_class": "C_irreproducible_empirical",
                "seed": (i * 100 + k) if vendor == "dummy-vendor-a" else None,
                "settings": {"note": "synthetic placeholder, not a real provider setting"},
                "error_detail": None if ok else f"synthetic {status} for schema testing",
            })
            if not ok:
                continue
            # THE POINT: many measurements over ONE stored artifact.
            for c in caps:
                meas.append({
                    "measurement_id": f"DUMMY-MEAS-{aid}-{c}", "artifact_id": aid,
                    "capability_id": c, "instrument_ref": f"dummy-instrument::{c}::v0",
                    "instrument_qualification_ref": "required_but_no_calibrated_instrument",
                    "observation_unit": unit, "result": {"dummy": True},
                    "measured_at": T1,
                    "evaluator_cost_ref": f"dummy-ledger://eval/{aid}/{c}",
                })
            if k == 0:
                accs.append({
                    "acceptance_id": f"DUMMY-ACC-{item}", "artifact_id": aid,
                    "accepted": (i % 3 != 0), "decided_by": "dummy-human-reviewer",
                    "decided_at": T1, "brief_ref": f"DUMMY-BRIEF-{i%10:02d}",
                    "rejection_reasons": [] if i % 3 != 0 else ["synthetic_rejection_reason"],
                    "retry_chain": [f"DUMMY-ART-{i:04d}-{x}" for x in range(N_ATTEMPTS)],
                })
    for name, rows in (("artifacts", arts), ("measurements", meas), ("acceptances", accs)):
        with open(os.path.join(OUT, name + ".jsonl"), "w") as fh:
            for r in rows:
                fh.write(json.dumps(r, sort_keys=True) + "\n")
    print(f"[OK] dummy archive written to {OUT}")
    print(f"     {len(arts):,} artifacts · {len(meas):,} measurements · {len(accs):,} acceptances")


if __name__ == "__main__":
    main()
