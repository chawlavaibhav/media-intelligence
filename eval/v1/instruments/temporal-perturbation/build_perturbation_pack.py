#!/usr/bin/env python3
"""Build and verify the temporal perturbation qualification pack.

WHAT THIS PRODUCES
------------------
For every base clip it produces:
  * one CLEAN CONTROL - the clip untouched. An instrument that reports a defect
    here is producing a false positive, and false positives are half the frozen
    family-4 gate.
  * one fixture per applicable perturbation - the clip broken on purpose, at a
    known frame, in a known way.
and, once for the pack:
  * CORRUPT CONTROLS - deliberately unreadable artifacts that the loader must
    refuse. If any of them loads, or loads as "clean", the machinery is unsafe
    and the build fails.

Everything is written into an INJECTED-TRUTH MANIFEST: the source clip hash, the
transformation and its parameters, the affected frame and time interval, the
affected region where one applies, and the output hash. Nothing in that manifest
comes from a human judgement or a model.

WHAT THIS DOES NOT DO
---------------------
It does not call any model, evaluator, provider or network service. It does not
score anything. It does not qualify anything. Gate arithmetic is in
qualify_temporal.py, and even that cannot award a qualification on its own.

Usage:
  python3 build_perturbation_pack.py --build            # constructed stand-ins
  python3 build_perturbation_pack.py --build --ingest-config path/to/clips.json
  python3 build_perturbation_pack.py --verify
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import platform
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import perturbations as P                                     # noqa: E402
from clipseq import ClipError, ClipSequence, encode_png       # noqa: E402

REPO_ROOT = HERE.parents[3]
FIXTURES = HERE / "fixtures"
PACK_SCHEMA = "temporal-perturbation-pack/v1"
PLAN_VERSION = "plan-v1"

# Files whose bytes define the transformation. Any edit changes the pack's
# configuration hash, which is what stops a modified perturbation being reported
# as the same experiment.
CONFIG_SOURCES = ("clipseq.py", "perturbations.py", "build_perturbation_pack.py")


def config_hash() -> str:
    h = hashlib.sha256()
    h.update((PACK_SCHEMA + "|" + PLAN_VERSION + "\n").encode())
    for name in CONFIG_SOURCES:
        h.update(name.encode())
        h.update(hashlib.sha256((HERE / name).read_bytes()).digest())
    return h.hexdigest()


# --------------------------------------------------------------------------
# the fixture plan
# --------------------------------------------------------------------------
def plan_for(clip: ClipSequence, donor: ClipSequence) -> list:
    """Derive this clip's fixture list from the clip's own properties.

    Positions are fractions of the clip length rather than fixed frame numbers,
    so the identical plan applies to a 48-frame stand-in and to a 480-frame real
    clip with no editing. Every entry names the perturbation, its arguments and
    why it is or is not applicable.
    """
    n = clip.n_frames
    prov = clip.provenance
    regions = prov.get("regions") or {}
    region_source = prov.get("region_source", "geometric_default")
    shots = [tuple(s) for s in (prov.get("shots") or [[0, n]])]

    def span(frac_num, frac_den, min_len):
        return max(min_len, (n * frac_num) // frac_den)

    entries = [
        ("frame_freeze", lambda c: P.frame_freeze(c, n // 4, span(1, 8, 2))),
        ("frame_duplication", lambda c: P.frame_duplication(c, n // 3, span(1, 12, 2), 1)),
        ("frame_drop", lambda c: P.frame_drop(c, n // 2, span(1, 12, 2))),
        ("frame_reversal", lambda c: P.frame_reversal(c, n // 5, span(1, 6, 3))),
        ("segment_reordering",
         lambda c: P.segment_reordering(c, (2 * n) // 3, span(1, 8, 2), n // 6)),
        ("midclip_horizontal_flip",
         lambda c: P.midclip_horizontal_flip(c, n // 2, min(n, n // 2 + span(1, 6, 2)))),
        ("framing_discontinuity", lambda c: P.framing_discontinuity(c, n // 2, n)),
        ("technical_corruption",
         lambda c: P.technical_corruption(c, (3 * n) // 8,
                                          min(n, (3 * n) // 8 + span(1, 10, 2)))),
    ]

    if len(shots) >= 2:
        entries.append(("shot_horizontal_flip",
                        lambda c: P.shot_horizontal_flip(c, 1, shots)))
    if donor is not None:
        entries.append(("identity_splice",
                        lambda c: P.identity_splice(c, donor, n // 3, span(1, 8, 2))))
    if regions.get("product"):
        entries.append(("product_region_substitution",
                        lambda c: P.product_region_substitution(
                            c, regions["product"], n // 2, n, region_source)))
    if regions.get("text"):
        entries.append(("text_region_mutation",
                        lambda c: P.text_region_mutation(
                            c, regions["text"], (3 * n) // 5, n, 3, region_source)))
        if prov.get("text_string") and prov.get("material_class") == "constructed_stand_in":
            import build_dummy_clips as bdc
            before = prov["text_string"]
            after = ("DEAL ENDED" if before != "DEAL ENDED" else "SALE OVER")
            entries.append(("text_glyph_substitution",
                            lambda c: P.text_glyph_substitution(
                                c, regions["text"], (3 * n) // 5, n,
                                lambda f, w, box, s: bdc.render_text(f, w, box, s),
                                before, after, region_source)))
    return entries


def skipped_reasons(clip: ClipSequence, donor) -> list:
    """Say out loud which perturbations this clip could NOT carry, and why.

    Silence about a missing perturbation would read later as coverage that
    never existed.
    """
    prov = clip.provenance
    regions = prov.get("regions") or {}
    shots = prov.get("shots") or [[0, clip.n_frames]]
    out = []
    if len(shots) < 2:
        out.append({"perturbation_type": "shot_horizontal_flip",
                    "reason": "clip declares a single shot; a screen-direction "
                              "violation across a cut cannot be constructed without a cut",
                    "capabilities_not_covered_for_this_clip": ["multi_shot_spatial_continuity"]})
    if donor is None:
        out.append({"perturbation_type": "identity_splice",
                    "reason": "no donor clip of matching geometry available",
                    "capabilities_not_covered_for_this_clip": ["person_stability_in_clip"]})
    if not regions.get("product"):
        out.append({"perturbation_type": "product_region_substitution",
                    "reason": "no product region declared or defaulted",
                    "capabilities_not_covered_for_this_clip": ["product_stability_in_clip"]})
    if not regions.get("text"):
        out.append({"perturbation_type": "text_region_mutation",
                    "reason": "no text region declared or defaulted",
                    "capabilities_not_covered_for_this_clip": ["text_logo_stability_in_clip"]})
    if prov.get("material_class") != "constructed_stand_in":
        out.append({"perturbation_type": "text_glyph_substitution",
                    "reason": "we do not own the glyphs in supplied footage; "
                              "text_region_mutation covers the same capability with "
                              "pixel-level rather than string-level truth",
                    "capabilities_not_covered_for_this_clip": []})
    return out


# --------------------------------------------------------------------------
# corrupt controls - the deliberately broken inputs
# --------------------------------------------------------------------------
def write_corrupt_controls(clip: ClipSequence, out_root: pathlib.Path) -> list:
    """Write artifacts that MUST fail to load.

    Frozen master-spec rule 6: test the machinery with deliberately broken
    inputs, and never let an empty check report success. Each of these is a
    different way a clip can be unusable, and the pack asserts that each one
    raises rather than returning a clean verdict.
    """
    out_root.mkdir(parents=True, exist_ok=True)
    controls = []

    def fresh(name):
        d = out_root / name
        if d.exists():
            shutil.rmtree(d)
        small = ClipSequence(name, clip.width, clip.height, clip.fps,
                             clip.frames[:4], clip.provenance)
        small.write(d)
        return d

    d = fresh("nc-truncated-frame")
    f = d / "frame-00002.png"
    f.write_bytes(f.read_bytes()[:60])
    controls.append((d, "a frame file is cut short mid-stream"))

    d = fresh("nc-corrupt-crc")
    f = d / "frame-00001.png"
    b = bytearray(f.read_bytes())
    b[-6] ^= 0xFF
    f.write_bytes(bytes(b))
    controls.append((d, "a chunk CRC no longer matches its data"))

    d = fresh("nc-missing-frame")
    (d / "frame-00003.png").unlink()
    controls.append((d, "clip.json declares more frames than exist on disk"))

    d = fresh("nc-silent-frame-swap")
    swapped = bytearray(clip.frames[0])
    swapped[0] = (swapped[0] + 128) & 0xFF
    (d / "frame-00002.png").write_bytes(encode_png(clip.width, clip.height, bytes(swapped)))
    controls.append((d, "a frame's pixels were replaced without updating clip.json - "
                        "the case a hash check exists to catch"))

    d = fresh("nc-zero-frames")
    side = json.loads((d / "clip.json").read_text())
    side["n_frames"] = 0
    (d / "clip.json").write_text(json.dumps(side, indent=2, sort_keys=True))
    controls.append((d, "an empty clip must fail, not pass as 'nothing wrong found'"))

    d = fresh("nc-not-a-png")
    (d / "frame-00000.png").write_bytes(b"this is not a video frame")
    controls.append((d, "a frame that is not an image at all"))

    d = fresh("nc-bad-json")
    (d / "clip.json").write_text("{ this is not json")
    controls.append((d, "an unparseable sidecar"))

    records = []
    for path, why in controls:
        try:
            ClipSequence.read(path)
        except ClipError as exc:
            records.append({
                "control_id": path.name,
                "kind": "corrupt_control",
                "what_is_wrong": why,
                "expected_behaviour": "loader raises ClipError; the run stops; the clip is "
                                      "never scored and never counted as clean",
                "observed": "ClipError",
                "observed_message": str(exc)[:200],
                "fail_closed": True,
            })
        else:
            raise ClipError(
                f"FAIL-CLOSED BREACH: corrupt control {path.name} loaded successfully. "
                "The pack is not safe to use and the build is aborted.")
    return records


def null_perturbation_control(clip: ClipSequence) -> dict:
    """Prove the builder refuses a transformation that changes nothing."""
    try:
        P.null_perturbation(clip)
    except P.NullPerturbationError as exc:
        return {"control_id": "nc-null-perturbation",
                "kind": "builder_control",
                "what_is_wrong": "a declared perturbation that leaves the pixels identical",
                "expected_behaviour": "builder raises NullPerturbationError and the fixture "
                                      "is never written",
                "observed": "NullPerturbationError",
                "observed_message": str(exc)[:200],
                "fail_closed": True}
    raise ClipError("FAIL-CLOSED BREACH: a no-op perturbation was accepted as a defect.")


# --------------------------------------------------------------------------
# build
# --------------------------------------------------------------------------
def export_mp4(clip_dir: pathlib.Path, clip: ClipSequence) -> dict | None:
    """Optional playable export for evaluators that need a video file.

    The mp4 is a convenience, not the fixture's identity: encoders differ
    between builds, so its bytes are not promised to be reproducible. The frame
    sequence's content hash is. That distinction is recorded here rather than
    left for someone to discover.
    """
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        return None
    out = clip_dir / f"{clip.clip_id}.mp4"
    cmd = [ffmpeg, "-y", "-nostdin", "-v", "error", "-framerate", str(clip.fps),
           "-i", str(clip_dir / "frame-%05d.png"), "-c:v", "libx264",
           "-preset", "veryslow", "-crf", "12", "-pix_fmt", "yuv420p", str(out)]
    res = subprocess.run(cmd, capture_output=True, check=False)
    if res.returncode != 0 or not out.is_file():
        return {"exported": False,
                "error": res.stderr.decode("utf-8", "replace").strip()[:300]}
    return {"exported": True, "path": out.name,
            "sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
            "byte_reproducibility": "NOT GUARANTEED across ffmpeg builds; the "
                                    "frame-sequence content_hash is the fixture identity",
            "command": cmd[1:]}


def build(base_clips: list, out_root: pathlib.Path, mp4: bool = False) -> dict:
    if not base_clips:
        raise ClipError("build: no base clips - an empty pack is a failure, not a pack")
    out_root.mkdir(parents=True, exist_ok=True)
    fixtures, skipped, base_records = [], [], []

    for k, clip in enumerate(base_clips):
        donor = None
        for cand in base_clips[k + 1:] + base_clips[:k]:
            if (cand.width, cand.height, cand.fps) == (clip.width, clip.height, clip.fps) \
                    and cand.content_hash() != clip.content_hash():
                donor = cand
                break

        base_dir = out_root / "base" / clip.clip_id
        side = clip.write(base_dir)
        base_records.append({
            "clip_id": clip.clip_id,
            "content_hash": side["content_hash"],
            "n_frames": side["n_frames"],
            "width": side["width"],
            "height": side["height"],
            "fps": side["fps"],
            "duration_s": side["duration_s"],
            "motion_load": side["motion_load"],
            "material_class": clip.provenance.get("material_class"),
            "source_file_sha256": clip.provenance.get("source_file_sha256"),
            "shots": clip.provenance.get("shots"),
            "shot_source": clip.provenance.get("shot_source"),
            "region_source": clip.provenance.get("region_source"),
        })

        # clean control: the same clip, untouched
        fixtures.append({
            "fixture_id": f"{clip.clip_id}__clean",
            "kind": "clean_control",
            "perturbation_type": None,
            "defect_present": False,
            "source_clip_id": clip.clip_id,
            "source_content_hash": side["content_hash"],
            "output_content_hash": side["content_hash"],
            "output_n_frames": side["n_frames"],
            "output_motion_load": side["motion_load"],
            "fps": side["fps"],
            "affected_output_frames": None,
            "affected_output_time_s": None,
            "affected_region_xywh": None,
            "targets_capabilities": sorted({c for v in P.CAPABILITY_TARGETS.values() for c in v}),
            "purpose": "false-positive measurement: any defect reported here is wrong",
            "path": str((out_root / 'base' / clip.clip_id).relative_to(out_root)),
            "independent_opportunity_id": clip.clip_id,
            "material_class": clip.provenance.get("material_class"),
        })

        for ptype, fn in plan_for(clip, donor):
            try:
                perturbed, truth = fn(clip)
            except P.NullPerturbationError as exc:
                # The transformation left the pixels untouched on THIS clip -
                # typically a defaulted region that turns out to be featureless,
                # so there is nothing there to break. That is real information,
                # not a build failure: the fixture is not written, the gap is
                # recorded, and the capability's coverage drops accordingly.
                # Any other ClipError is a parameter or code fault and still
                # aborts the build.
                skipped.append({
                    "clip_id": clip.clip_id,
                    "perturbation_type": ptype,
                    "reason": f"transformation changed nothing on this clip ({exc}). "
                              "No fixture was written: a defect that is invisible would "
                              "score every instrument as a miss and corrupt the recall "
                              "figure.",
                    "capabilities_not_covered_for_this_clip": P.CAPABILITY_TARGETS[ptype],
                })
                continue
            fixture_id = f"{clip.clip_id}__{ptype}"
            fdir = out_root / "perturbed" / fixture_id
            pside = perturbed.write(fdir)
            rec = dict(truth)
            rec.update({
                "fixture_id": fixture_id,
                "kind": "perturbed",
                "path": str(fdir.relative_to(out_root)),
                "frame_png_hashes_sha256": hashlib.sha256(
                    "".join(pside["frame_png_hashes"]).encode()).hexdigest(),
                # Frames from one clip are ONE trial. This id is what the gate
                # counts, so 13 fixtures from 1 clip never read as 13 clips.
                "independent_opportunity_id": clip.clip_id,
                "material_class": clip.provenance.get("material_class"),
            })
            if mp4:
                rec["mp4_export"] = export_mp4(fdir, perturbed)
            fixtures.append(rec)

        for s in skipped_reasons(clip, donor):
            skipped.append({"clip_id": clip.clip_id, **s})

    controls = write_corrupt_controls(base_clips[0], out_root / "controls")
    controls.append(null_perturbation_control(base_clips[0]))

    by_type = {}
    for f in fixtures:
        if f["kind"] == "perturbed":
            by_type[f["perturbation_type"]] = by_type.get(f["perturbation_type"], 0) + 1

    cap_cover = {}
    for f in fixtures:
        if f["kind"] != "perturbed":
            continue
        for cap in f["targets_capabilities"]:
            e = cap_cover.setdefault(cap, {"fixtures": 0, "independent_clips": set(),
                                           "perturbation_types": set()})
            e["fixtures"] += 1
            e["independent_clips"].add(f["independent_opportunity_id"])
            e["perturbation_types"].add(f["perturbation_type"])
    capability_coverage = {
        cap: {"fixtures": v["fixtures"],
              "independent_clips": len(v["independent_clips"]),
              "perturbation_types": sorted(v["perturbation_types"])}
        for cap, v in sorted(cap_cover.items())}

    coverage_warnings = []
    frozen_temporal = sorted({c for v in P.CAPABILITY_TARGETS.values() for c in v})
    for cap in frozen_temporal:
        cov = capability_coverage.get(cap)
        if not cov:
            coverage_warnings.append(
                f"{cap}: NO fixture in this pack supplies truth for it. The protocol "
                "cannot be run for this capability against this material.")
        elif cov["independent_clips"] < 2:
            coverage_warnings.append(
                f"{cap}: only {cov['independent_clips']} independent clip(s) carry truth "
                "for it. One clip is one opportunity, so any rate computed here rests on "
                "almost nothing.")

    material_classes = sorted({b["material_class"] for b in base_records})
    manifest = {
        "schema": PACK_SCHEMA,
        "task": "EVAL-026",
        "plan_version": PLAN_VERSION,
        "configuration_hash": config_hash(),
        "status": "MACHINERY_BUILT_NO_INSTRUMENT_QUALIFIED",
        "material_classes": material_classes,
        "is_approved_qualification_pack": material_classes == ["supplied_real_clip"],
        "generated_by": "eval/v1/instruments/temporal-perturbation/build_perturbation_pack.py",
        "environment": {
            "python": platform.python_version(),
            "note": "recorded for diagnosis only; fixture identity is the frame-sequence "
                    "content hash, which does not depend on it",
        },
        "counts": {
            "base_clips": len(base_records),
            "perturbed_fixtures": sum(by_type.values()),
            "clean_controls": len(base_records),
            "corrupt_controls": len([c for c in controls if c["kind"] == "corrupt_control"]),
            "builder_controls": len([c for c in controls if c["kind"] == "builder_control"]),
            "perturbation_types_used": len(by_type),
            "by_perturbation_type": dict(sorted(by_type.items())),
        },
        "capability_coverage": capability_coverage,
        "coverage_warnings": coverage_warnings,
        "base_clips": base_records,
        "fixtures": fixtures,
        "controls": controls,
        "skipped": skipped,
        "external_calls": 0,
        "model_or_evaluator_calls": 0,
        "human_labels_used": 0,
        "spend_usd": 0.0,
        "caveats": [
            "No instrument is qualified by this pack. It is material plus machinery.",
            "Frames from one clip are ONE independent opportunity. Count "
            "independent_opportunity_id, never fixture count, when reporting a rate.",
            "A qualification earned here is valid only at or above the frame sample rate "
            "it was measured at, and only under these clips' conditions.",
            "mp4 exports are a convenience; only the frame-sequence content hash is a "
            "reproducible identity.",
        ],
    }
    if material_classes != ["supplied_real_clip"]:
        manifest["caveats"].insert(0,
            "THIS PACK CONTAINS CONSTRUCTED STAND-IN MATERIAL. It proves the machinery "
            "runs. It is not the approved 12-clip base and cannot qualify the temporal "
            "family under the frozen family-4 conditions.")

    (out_root / "MANIFEST.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return manifest


# --------------------------------------------------------------------------
# verify
# --------------------------------------------------------------------------
def verify(out_root: pathlib.Path) -> tuple:
    """Re-read every fixture from disk and re-check it against the manifest."""
    problems = []
    mpath = out_root / "MANIFEST.json"
    if not mpath.is_file():
        return False, [f"no manifest at {mpath}; run --build first"]
    m = json.loads(mpath.read_text())

    if not m.get("fixtures"):
        return False, ["manifest lists zero fixtures - an empty check is not a passing check"]
    if m.get("configuration_hash") != config_hash():
        problems.append("configuration_hash differs from the current source: the "
                        "transformation code changed, so this is a DIFFERENT pack and "
                        "must be rebuilt before use")

    for f in m["fixtures"]:
        d = out_root / f["path"]
        try:
            clip = ClipSequence.read(d)
        except ClipError as exc:
            problems.append(f"{f['fixture_id']}: {exc}")
            continue
        if clip.content_hash() != f["output_content_hash"]:
            problems.append(f"{f['fixture_id']}: content hash differs from manifest")
        if clip.n_frames != f["output_n_frames"]:
            problems.append(f"{f['fixture_id']}: frame count differs from manifest")
        if f["kind"] == "perturbed":
            if not f.get("defect_present"):
                problems.append(f"{f['fixture_id']}: perturbed fixture not marked defective")
            iv = f.get("affected_output_frames")
            if not iv or not (0 <= iv[0] < iv[1] <= clip.n_frames):
                problems.append(f"{f['fixture_id']}: affected interval {iv} is not inside "
                                f"a clip of {clip.n_frames} frames")
            src = next((b for b in m["base_clips"]
                        if b["clip_id"] == f["source_clip_id"]), None)
            if src is None:
                problems.append(f"{f['fixture_id']}: names an unknown source clip")
            elif src["content_hash"] != f["source_content_hash"]:
                problems.append(f"{f['fixture_id']}: source hash does not match its base clip")
            if clip.content_hash() == f["source_content_hash"]:
                problems.append(f"{f['fixture_id']}: output is identical to its source - "
                                "the injected defect changed nothing")

    for c in m.get("controls", []):
        if c["kind"] != "corrupt_control":
            continue
        d = out_root / "controls" / c["control_id"]
        try:
            ClipSequence.read(d)
        except ClipError:
            pass
        else:
            problems.append(f"FAIL-CLOSED BREACH: corrupt control {c['control_id']} "
                            "loaded without error")
    return (not problems), problems


def rebuild_is_identical(base_clips: list, out_root: pathlib.Path) -> tuple:
    """Rebuild in a scratch location and compare hashes, not bytes on disk."""
    m1 = json.loads((out_root / "MANIFEST.json").read_text())
    tmp = out_root.parent / (out_root.name + "-rebuild-check")
    if tmp.exists():
        shutil.rmtree(tmp)
    try:
        m2 = build(base_clips, tmp, mp4=False)
        a = {f["fixture_id"]: f["output_content_hash"] for f in m1["fixtures"]}
        b = {f["fixture_id"]: f["output_content_hash"] for f in m2["fixtures"]}
        diffs = [k for k in sorted(set(a) | set(b)) if a.get(k) != b.get(k)]
        return (not diffs), diffs
    finally:
        if tmp.exists():
            shutil.rmtree(tmp)


# --------------------------------------------------------------------------
# committed fingerprint
# --------------------------------------------------------------------------
def fingerprint(manifest: dict) -> dict:
    """A small, committable summary of a build.

    The frames themselves are git-ignored: several thousand PNGs would add
    weight without adding truth, because committed stdlib-only code rebuilds
    them byte-identically. What IS committed is this fingerprint, so a reviewer
    on a fresh clone can rebuild and prove they got the same pack rather than
    taking a claim on trust.

    The same precedent as the Devanagari battery's committed SHA-256 record -
    but WITHOUT that battery's rebuild risk, since nothing here depends on an
    uncommitted font or any proprietary asset.
    """
    return {
        "schema": "temporal-perturbation-fingerprint/v1",
        "task": manifest["task"],
        "plan_version": manifest["plan_version"],
        "configuration_hash": manifest["configuration_hash"],
        "material_classes": manifest["material_classes"],
        "is_approved_qualification_pack": manifest["is_approved_qualification_pack"],
        "counts": manifest["counts"],
        "capability_coverage": manifest["capability_coverage"],
        "coverage_warnings": manifest["coverage_warnings"],
        "base_clip_content_hashes": {b["clip_id"]: b["content_hash"]
                                     for b in manifest["base_clips"]},
        "base_clip_motion_load": {b["clip_id"]: b["motion_load"]
                                  for b in manifest["base_clips"]},
        "fixture_content_hashes": {f["fixture_id"]: f["output_content_hash"]
                                   for f in manifest["fixtures"]},
        "controls": [{"control_id": c["control_id"], "kind": c["kind"],
                      "observed": c["observed"], "fail_closed": c["fail_closed"]}
                     for c in manifest["controls"]],
        "skipped": manifest["skipped"],
        "external_calls": manifest["external_calls"],
        "model_or_evaluator_calls": manifest["model_or_evaluator_calls"],
        "human_labels_used": manifest["human_labels_used"],
        "spend_usd": manifest["spend_usd"],
        "caveats": manifest["caveats"],
    }


def fingerprint_matches(manifest: dict, path: pathlib.Path) -> tuple:
    if not path.is_file():
        return False, [f"no committed fingerprint at {path}"]
    committed = json.loads(path.read_text())
    fresh = fingerprint(manifest)
    diffs = [k for k in sorted(set(committed) | set(fresh))
             if committed.get(k) != fresh.get(k)]
    return (not diffs), diffs


# --------------------------------------------------------------------------
def load_base_clips(args) -> list:
    if args.ingest_config:
        import ingest_clips
        return ingest_clips.ingest_manifest(pathlib.Path(args.ingest_config),
                                            FIXTURES / "base-ingested")
    if args.base_dir:
        base = pathlib.Path(args.base_dir)
        dirs = sorted(d for d in base.iterdir() if (d / "clip.json").is_file())
        if not dirs:
            raise ClipError(f"no ClipSequences under {base}")
        return [ClipSequence.read(d) for d in dirs]
    import build_dummy_clips
    return build_dummy_clips.build_all()


def main() -> int:
    ap = argparse.ArgumentParser(description="Build/verify the temporal perturbation pack.")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--rebuild-check", action="store_true",
                    help="rebuild into a scratch dir and prove the hashes are identical")
    ap.add_argument("--ingest-config", default=None,
                    help="JSON config of supplied real clips (see ingest_clips.py)")
    ap.add_argument("--base-dir", default=None,
                    help="directory of already-ingested ClipSequences")
    ap.add_argument("--out-dir", default=None)
    ap.add_argument("--mp4", action="store_true", help="also export playable mp4s")
    ap.add_argument("--write-fingerprint", default=None,
                    help="write the small committable summary of this build")
    ap.add_argument("--check-fingerprint", default=None,
                    help="rebuild and prove the result matches a committed fingerprint")
    args = ap.parse_args()

    out_root = pathlib.Path(args.out_dir) if args.out_dir else FIXTURES / "pack"
    rc = 0
    if args.build:
        clips = load_base_clips(args)
        m = build(clips, out_root, mp4=args.mp4)
        c = m["counts"]
        print(f"base clips              {c['base_clips']}")
        print(f"perturbed fixtures      {c['perturbed_fixtures']}")
        print(f"clean controls          {c['clean_controls']}")
        print(f"corrupt controls        {c['corrupt_controls']} (all refused, as required)")
        print(f"perturbation types      {c['perturbation_types_used']}")
        print(f"skipped (recorded)      {len(m['skipped'])}")
        for w in m["coverage_warnings"]:
            print(f"  COVERAGE WARNING: {w}")
        print(f"material classes        {', '.join(m['material_classes'])}")
        print(f"approved qualification pack: {m['is_approved_qualification_pack']}")
        print(f"external calls {m['external_calls']} · human labels {m['human_labels_used']} "
              f"· spend USD {m['spend_usd']}")
        print(f"\nmanifest: {out_root / 'MANIFEST.json'}")
        if args.write_fingerprint:
            pathlib.Path(args.write_fingerprint).write_text(
                json.dumps(fingerprint(m), indent=2, sort_keys=True) + "\n")
            print(f"fingerprint written to {args.write_fingerprint}")
        if args.check_fingerprint:
            same, diffs = fingerprint_matches(m, pathlib.Path(args.check_fingerprint))
            print("committed fingerprint:", "MATCHES" if same else f"DIFFERS in {diffs}")
            rc |= 0 if same else 1
        if args.rebuild_check:
            same, diffs = rebuild_is_identical(clips, out_root)
            print("rebuild reproducibility:", "IDENTICAL" if same else f"DIFFERS {diffs}")
            rc |= 0 if same else 1
    if args.verify:
        ok, problems = verify(out_root)
        if ok:
            print("PASS - every fixture present, hash-identical, and every corrupt "
                  "control still refused.")
        else:
            print("FAIL")
            for p in problems[:40]:
                print("  -", p)
            rc |= 1
    if not args.build and not args.verify:
        ap.print_help()
        rc = 2
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
