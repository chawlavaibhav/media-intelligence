#!/usr/bin/env python3
"""Blind judging packet for an EVAL-040 run: build (blind), commit, reveal, merge verdicts, apply E1/E2.

    python3 eval/harness-v2/judging_packet.py build  --run-id <id> --out <dir> --key-dir <dir OUTSIDE the repo>
    python3 eval/harness-v2/judging_packet.py reveal --run-id <id> --out <dir> --key-dir <dir>

BUILD  copies every sealed artifact of the run to `<out>/judging/<blind_id>.<ext>`. Blind ids are a seeded random
       permutation over the whole set (`J01..Jnn`); the bytes are copied verbatim (bytes are evidence) and their
       sha256 is re-checked after the copy. `JUDGING-SHEET.md` carries only blind id + case id + the case's acceptance
       contract (ACCEPTANCE-CONTRACTS.md at the plan's commit): no route, arm, surface, price or repeat number, and a
       mechanical word-bounded scan of every text file in the packet refuses the build if one leaks. The reveal key
       (blind id -> trial / route / repeat) is written ONLY to `<key-dir>/REVEAL-<run-id>.json` - the key dir must be
       outside the repo - and a salted sha256 commitment of it to `<out>/judging/REVEAL-COMMITMENT.txt`
       (EVAL-038 strip_blind.py pattern). Artifacts whose embedded metadata (PNG text chunks, JPEG APP segments, WEBP
       EXIF/XMP, C2PA) could name the model are NOTED under `<out>/judging-build/METADATA-NOTES.json` (keyed by trial id,
       outside the judge's directory) and never altered.
REVEAL verifies the commitment, reads the Controller's `<out>/judging/VERDICTS.yaml` (blind_id -> accept|reject + note;
       every blind id must have one), merges into `<out>/RESULTS.yaml` per case x route x repeat, and applies
       ELIMINATION-RULES E1/E2 per (route, question) with the planned trial count as the denominator (the frozen
       proportions: E1 refusal/error >= 37.5 %, E2 accepts <= 25 %, never rounded in a route's favour). A trial with no
       artifact (refusal, error, timeout, not dispatched) is a reject for E2 (E5) and, when it was a provider refusal or
       error, counts under E1.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import re
import struct
import sys
import zlib
from datetime import datetime, timezone
from pathlib import Path

import yaml

import hv2_paths
import casebook as CB
import run_live as RL
import store as S
import surfaces

JUDGING_DIR = "judging"
BUILD_DIR = "judging-build"
SHEET = "JUDGING-SHEET.md"
COMMITMENT = "REVEAL-COMMITMENT.txt"
VERDICTS = "VERDICTS.yaml"
TEMPLATE = "VERDICTS.template.yaml"
RESULTS = "RESULTS.yaml"
RULES_REF = "eval/empirical-planning/STAGE-A-FREEZE-2026-09/ELIMINATION-RULES.md"
CONTRACTS_REL = f"{CB.FREEZE_REL}/ACCEPTANCE-CONTRACTS.md"
GENERIC_VOCAB = ("gemini", "google", "openai", "flux", "seedream", "qwen", "recraft", "bytedance", "alibaba", "imagen", "c2pa", "adobe", "photoshop", "stability", "dall")
PROVIDER_STATUSES = ("refusal", "error", "timeout")


class PacketRefused(RuntimeError):
    """The packet cannot be built or revealed as asked; nothing was written past the refusal."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def question_of(case_id: str) -> str:
    """The case family = the question a (route, case set) answers: IMG-CORE-01..04 -> IMG-CORE; IMG-TEXT-01/02 -> IMG-TEXT."""
    return re.sub(r"-\d+$", "", case_id)


def _outside_repo(key_dir: Path) -> bool:
    kd = key_dir.resolve()
    root = hv2_paths.REPO_ROOT.resolve()
    return kd != root and root not in kd.parents


def _commitment(salt: str, seed: str, mapping: dict) -> str:
    return hashlib.sha256(f"{salt}|{seed}|".encode("utf-8") + S.canonical_json(mapping)).hexdigest()


# ------------------------------------------------------------------------------ contracts
def contract_text(case_id: str, commit: str) -> str:
    try:
        md = CB.git_show(commit, CONTRACTS_REL).decode("utf-8")
        m = re.search(r"^## " + re.escape(case_id) + r"( \([^)]*\))?\n(.*?)(?=^## |^# |\Z)", md, re.M | re.S)
        if m:
            return (f"{case_id}{m.group(1) or ''}\n" + m.group(2).strip() + "\n")
    except Exception:  # noqa: BLE001 - fall back to the TEST-CASES list
        pass
    book = CB.CaseBook.from_git(commit)
    lines = book.case(case_id).get("acceptance_contract") or []
    return f"{case_id}\n" + "\n".join(f"- {l}" for l in lines) + "\n"


# ------------------------------------------------------------------------------ metadata guard
def _vocab_hits(text: str, vocab: list) -> list[str]:
    low = text.lower()
    return sorted({v for v in vocab if v and len(v) >= 4 and v.lower() in low})


def _png_chunks(data: bytes):
    pos = 8
    while pos + 8 <= len(data):
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        payload = data[pos + 8:pos + 8 + length]
        yield ctype, payload
        pos += 12 + length
        if ctype == b"IEND":
            break


def scan_metadata(data: bytes, ext: str, vocab: list) -> list[str]:
    """Flags for embedded text/metadata that could carry a model name. Reads bytes; alters nothing."""
    flags: list[str] = []
    vocab = list(vocab) + list(GENERIC_VOCAB)
    ext = ext.lower()
    texts: list[tuple[str, str]] = []
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        for ctype, payload in _png_chunks(data):
            name = ctype.decode("latin-1", "replace")
            if ctype == b"tEXt":
                kw, _, txt = payload.partition(b"\x00")
                texts.append((f"png chunk tEXt ({kw.decode('latin-1', 'replace')})", txt.decode("latin-1", "replace")))
            elif ctype == b"zTXt":
                kw, _, rest = payload.partition(b"\x00")
                try:
                    txt = zlib.decompress(rest[1:]).decode("latin-1", "replace")
                except Exception:  # noqa: BLE001
                    txt = ""
                texts.append((f"png chunk zTXt ({kw.decode('latin-1', 'replace')})", txt))
            elif ctype == b"iTXt":
                kw, _, rest = payload.partition(b"\x00")
                comp = rest[:1] == b"\x01"
                body = rest[2:]
                _, _, body = body.partition(b"\x00")     # language tag
                _, _, body = body.partition(b"\x00")     # translated keyword
                try:
                    txt = (zlib.decompress(body) if comp else body).decode("utf-8", "replace")
                except Exception:  # noqa: BLE001
                    txt = ""
                texts.append((f"png chunk iTXt ({kw.decode('latin-1', 'replace')})", txt))
            elif ctype in (b"eXIf", b"caBX"):
                texts.append((f"png chunk {name} ({'C2PA/JUMBF' if ctype == b'caBX' else 'EXIF'})", payload.decode("latin-1", "replace")))
    elif data[:2] == b"\xff\xd8":
        pos = 2
        while pos + 4 <= len(data):
            if data[pos] != 0xFF:
                break
            marker = data[pos + 1]
            if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
                pos += 2
                continue
            if marker == 0xDA:
                break
            (seglen,) = struct.unpack(">H", data[pos + 2:pos + 4])
            payload = data[pos + 4:pos + 2 + seglen]
            if 0xE0 <= marker <= 0xEF:
                head = payload[:32].decode("latin-1", "replace")
                kind = "Exif" if head.startswith("Exif") else ("XMP" if "ns.adobe.com/xap" in head else ("JUMBF/C2PA" if "jumb" in head.lower() else "APP"))
                texts.append((f"jpeg APP{marker - 0xE0} ({kind})", payload.decode("latin-1", "replace")))
            pos += 2 + seglen
    elif data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        pos = 12
        while pos + 8 <= len(data):
            fourcc = data[pos:pos + 4]
            (size,) = struct.unpack("<I", data[pos + 4:pos + 8])
            payload = data[pos + 8:pos + 8 + size]
            if fourcc in (b"EXIF", b"XMP ", b"C2PA"):
                texts.append((f"webp chunk {fourcc.decode('latin-1').strip()}", payload.decode("latin-1", "replace")))
            pos += 8 + size + (size & 1)
    else:
        texts.append(("whole file (unknown container)", data.decode("latin-1", "replace")))
        hits = _vocab_hits(texts[0][1], [v for v in vocab if len(v) >= 5])
        return [f"whole-file scan names {h}" for h in hits]
    for where, txt in texts:
        flags.append(where)
        for h in _vocab_hits(txt, vocab):
            flags.append(f"{where} names {h}")
    return flags


# ------------------------------------------------------------------------------ build
def _leak_needles(plan: dict) -> list[str]:
    needles = set()
    for t in plan["trials"]:
        e = surfaces.REGISTRY.get(t["route_key"])
        needles |= {t["route_key"], t["trial_id"], e.surface, e.surface_model_id, e.adapter, t["billing_pool"], "repeat_index", "billing_pool"}
        if "_" in (t["arm"] or ""):
            needles.add(t["arm"])
    return sorted(needles)


def _leaks(text: str, needles: list[str]) -> list[str]:
    return [n for n in needles if re.search(r"(?<![A-Za-z0-9_])" + re.escape(n) + r"(?![A-Za-z0-9_])", text, re.I)]


def _runs(out, run_id, extra_runs):
    """[(out_dir, run_id, plan, store)] — the primary run first, then any extra runs (e.g. a redo run) judged in ONE blind set."""
    runs = [(Path(out), run_id)] + [(Path(o), r) for o, r in (extra_runs or [])]
    return [(o, r, RL.load_plan(o, r), S.SealedStore(o / RL.ARTIFACTS_DIR)) for o, r in runs]


def build(out: Path | str, run_id: str, key_dir: Path | str, seed: str | None = None, extra_runs: list | None = None) -> dict:
    out = Path(out)
    key_dir = Path(key_dir)
    runs = _runs(out, run_id, extra_runs)
    plan = runs[0][2]
    if not _outside_repo(key_dir):
        raise PacketRefused(f"key dir {key_dir} is inside the repo {hv2_paths.REPO_ROOT}; the reveal key is held OFF-repo only")
    jd, bd = out / JUDGING_DIR, out / BUILD_DIR
    if jd.exists():
        raise PacketRefused(f"{jd} already exists; a packet is built once (the blinding must not be re-drawn while judging is open)")
    items = []
    for r_out, r_id, r_plan, r_store in runs:
        for t in r_plan["trials"]:
            a = r_store.load_attempt(t["trial_id"])      # a recovered attempt (recover_fal.py) supersedes the original
            if a is None:
                continue
            if a.get("status") != "ok" or not a.get("artifact"):
                continue
            rec = a["artifact"]
            if not r_store.verify(rec):
                raise PacketRefused(f"{t['trial_id']}: sealed artifact bytes do not match their record; refusing to judge unverifiable evidence")
            items.append((dict(t, _run_id=r_id, _store_root=str(r_store.root)), rec, a))
    if not items:
        raise PacketRefused(f"run {run_id} has no artifact to judge")
    seed = seed or os.urandom(16).hex()
    salt = os.urandom(16).hex()
    order = list(range(len(items)))
    random.Random(seed).shuffle(order)
    width = max(2, len(str(len(items))))
    vocab = _leak_needles(plan)
    mapping: dict[str, dict] = {}
    metadata_notes: dict[str, list] = {}
    jd.mkdir(parents=True, exist_ok=False)
    bd.mkdir(parents=True, exist_ok=True)
    for rank, idx in enumerate(order, 1):
        t, rec, a = items[idx]
        bid = f"J{rank:0{width}d}"
        src = Path(t["_store_root"]) / rec["relative_path"]
        ext = src.suffix
        data = src.read_bytes()
        dst = jd / f"{bid}{ext}"
        dst.write_bytes(data)
        if hashlib.sha256(dst.read_bytes()).hexdigest() != rec["sha256"]:
            raise PacketRefused(f"{bid}: copied bytes do not hash to the sealed sha256")
        metadata_notes[t["trial_id"]] = scan_metadata(data, ext, vocab)
        mapping[bid] = {"trial_id": t["trial_id"], "run_id": t["_run_id"], "case_id": t["case_id"], "route_key": t["route_key"], "arm": t["arm"],
                        "repeat_index": t["repeat_index"], "surface": t["surface"], "sha256": rec["sha256"], "ext": ext, "file": dst.name}
    # the judge-facing sheet: blind id + case id + contract only
    commit = plan["header"]["commit"]
    by_case: dict[str, list] = {}
    for bid, m in mapping.items():
        by_case.setdefault(m["case_id"], []).append(m["file"])
    lines = [f"# Blind judging sheet - run {run_id}", "",
             "Judge each file from the picture alone against its case's acceptance contract. Record one verdict per file in",
             f"`{VERDICTS}` (copy `{TEMPLATE}`): `verdict: accept` or `verdict: reject`, plus a one-line note. Do not open file",
             "metadata, the run's other directories, the plan or the ledger before every verdict is written; the mapping from",
             f"blind id to what produced it is sealed off this machine's repo and committed in `{COMMITMENT}`.",
             "Some files may carry embedded text metadata; it is not evidence and must not be read.", ""]
    for case_id in plan["header"]["cases"]:
        files = sorted(by_case.get(case_id, []))
        if not files:
            continue
        lines += [f"## {contract_text(case_id, commit).strip()}", "", "Files: " + ", ".join(files), ""]
    sheet = "\n".join(lines) + "\n"
    template = yaml.safe_dump({"run_id": run_id, "verdicts": {bid: {"verdict": None, "note": ""} for bid in sorted(mapping)}}, sort_keys=False)
    for name, text in ((SHEET, sheet), (TEMPLATE, template)):
        bad = _leaks(text, vocab)
        if bad:
            import shutil
            shutil.rmtree(jd, ignore_errors=True)
            raise PacketRefused(f"{name} would leak {bad}; packet not written")
        (jd / name).write_text(text, encoding="utf-8")
    commitment = _commitment(salt, seed, mapping)
    (jd / COMMITMENT).write_text(
        f"{commitment}\n"
        f"commitment = sha256(salt | seed | canonical_json(mapping)); the salt, seed and mapping live only in the off-repo reveal key\n"
        f"items: {len(mapping)}\nblind_ids: {', '.join(sorted(mapping))}\ncreated_utc: {_now()}\n", encoding="utf-8")
    key_dir.mkdir(parents=True, exist_ok=True)
    key_path = key_dir / f"REVEAL-{run_id}.json"
    if key_path.exists():
        raise PacketRefused(f"{key_path} already exists; refusing to overwrite a reveal key")
    key_path.write_text(json.dumps({"run_id": run_id, "runs": [[str(o), r] for o, r, _, _ in runs], "seed": seed, "salt": salt,
                                    "commitment": commitment, "created_utc": _now(), "mapping": mapping}, indent=1, sort_keys=True), encoding="utf-8")
    (bd / "METADATA-NOTES.json").write_text(json.dumps(metadata_notes, indent=1, sort_keys=True), encoding="utf-8")
    (bd / "BUILD.json").write_text(json.dumps({"run_id": run_id, "built_utc": _now(), "n_artifacts": len(mapping), "key_path": str(key_path),
                                                "commitment": commitment, "metadata_flagged_trials": sorted(t for t, f in metadata_notes.items() if f),
                                                "note": "this directory is NOT part of the judge's packet"}, indent=1), encoding="utf-8")
    return {"run_id": run_id, "n_artifacts": len(mapping), "judging_dir": str(jd), "key_path": str(key_path), "commitment": commitment,
            "metadata_flagged": sum(1 for f in metadata_notes.values() if f)}


# ------------------------------------------------------------------------------ elimination
def e1_threshold(n: int) -> int:
    """Minimum refusals/hard errors that eliminate: >= 37.5 % of n, rounded UP (8 -> 3, 4 -> 2, 6 -> 3, 2 -> 1)."""
    return int(math.ceil(0.375 * n - 1e-9))


def e2_threshold(n: int) -> int:
    """Maximum accepts that still eliminate: <= 25 % of n, rounded DOWN (8 -> 2, 4 -> 1, 6 -> 1, 2 -> 0)."""
    return int(math.floor(0.25 * n + 1e-9))


def apply_elimination(trials: list[dict]) -> list[dict]:
    groups: dict[tuple, list] = {}
    for t in trials:
        groups.setdefault((t["question"], t["route_key"]), []).append(t)
    rows = []
    for (question, route), ts in sorted(groups.items()):
        n = len(ts)
        refusals = sum(1 for t in ts if t.get("dispatched") and t.get("status") in PROVIDER_STATUSES)
        accepts = sum(1 for t in ts if t.get("verdict") == "accept")
        not_dispatched = sum(1 for t in ts if not t.get("dispatched"))
        e1, e2 = e1_threshold(n), e2_threshold(n)
        by = []
        if refusals >= e1:
            by.append("E1")
        if accepts <= e2:
            by.append("E2")
        rows.append({"question": question, "route_key": route, "arms": sorted({t.get("arm") for t in ts if t.get("arm")}), "n_planned": n,
                     "refusals_or_errors": refusals, "accepts": accepts, "rejects": n - accepts, "not_dispatched": not_dispatched,
                     "e1_threshold": e1, "e2_threshold": e2, "eliminated": bool(by), "eliminated_by": by})
    return rows


def table_text(rows: list[dict]) -> str:
    head = f"{'question':10s} {'route_key':18s} {'n':>3s} {'acc':>4s} {'rej':>4s} {'ref/err':>7s} {'n/d':>4s}  E1(>=)  E2(<=)  verdict"
    out = [head, "-" * len(head)]
    for r in rows:
        out.append(f"{r['question']:10s} {r['route_key']:18s} {r['n_planned']:3d} {r['accepts']:4d} {r['rejects']:4d} {r['refusals_or_errors']:7d} {r['not_dispatched']:4d}  "
                   f"{r['e1_threshold']:6d}  {r['e2_threshold']:6d}  {'ELIMINATED ' + '+'.join(r['eliminated_by']) if r['eliminated'] else 'survives'}")
    return "\n".join(out)


# ------------------------------------------------------------------------------ reveal
def _load_verdicts(path: Path) -> dict:
    if not path.exists():
        raise PacketRefused(f"no verdicts at {path}; the Controller writes them before the reveal")
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    v = raw.get("verdicts") if isinstance(raw, dict) and isinstance(raw.get("verdicts"), dict) else raw
    if not isinstance(v, dict):
        raise PacketRefused(f"{path} is not a mapping of blind id -> verdict")
    out = {}
    for bid, val in v.items():
        if isinstance(val, str):
            val = {"verdict": val, "note": ""}
        if not isinstance(val, dict) or val.get("verdict") not in ("accept", "reject"):
            raise PacketRefused(f"{path}: {bid} needs verdict accept|reject, got {val!r}")
        out[str(bid)] = {"verdict": val["verdict"], "note": str(val.get("note") or "")}
    return out


def reveal(out: Path | str, run_id: str, key_dir: Path | str) -> dict:
    out = Path(out)
    plan = RL.load_plan(out, run_id)
    jd = out / JUDGING_DIR
    key_path = Path(key_dir) / f"REVEAL-{run_id}.json"
    if not key_path.exists():
        raise PacketRefused(f"no reveal key at {key_path}")
    if not (jd / COMMITMENT).exists():
        raise PacketRefused(f"no commitment at {jd / COMMITMENT}")
    key = json.loads(key_path.read_text(encoding="utf-8"))
    committed = (jd / COMMITMENT).read_text(encoding="utf-8").split()[0]
    recomputed = _commitment(key["salt"], key["seed"], key["mapping"])
    if recomputed != committed:
        raise PacketRefused(f"reveal key does not match the committed blinding: recomputed {recomputed[:12]}... != committed {committed[:12]}...")
    mapping = key["mapping"]
    verdicts = _load_verdicts(jd / VERDICTS)
    missing = sorted(set(mapping) - set(verdicts))
    unknown = sorted(set(verdicts) - set(mapping))
    if missing or unknown:
        raise PacketRefused(f"verdicts incomplete: missing {missing}, unknown {unknown}; every blind id needs exactly one verdict before the reveal")
    by_trial = {(m.get("run_id", run_id), m["trial_id"]): (bid, m) for bid, m in mapping.items()}
    runs = [(Path(o), r) for o, r in key.get("runs") or [[str(out), run_id]]]
    rows = []
    redone: set = set()
    for r_out, r_id in runs:
        r_plan = RL.load_plan(r_out, r_id)
        for t in r_plan["trials"]:
            if t.get("redo_of"):
                redone.add((t["redo_of"]["prev_run_id"], t["redo_of"]["trial_id"]))
    for r_out, r_id in runs:
      r_plan = RL.load_plan(r_out, r_id)
      store = S.SealedStore(r_out / RL.ARTIFACTS_DIR)
      for t in r_plan["trials"]:
        tid = t["trial_id"]
        if (r_id, tid) in redone:
            continue                                      # superseded by its redo trial in another run (an infrastructure fault, not a draw)
        a = store.load_attempt(tid)                       # recovered attempt preferred
        row = {"trial_id": tid, "run_id": r_id, "case_id": t["case_id"], "question": question_of(t["case_id"]), "route_key": t["route_key"], "arm": t["arm"],
               "repeat_index": t["repeat_index"], "dispatched": a is not None, "status": a.get("status") if a else None,
               "error_class": a.get("error_class") if a else None, "blind_id": None, "verdict": None, "verdict_basis": None, "note": "",
               "redo_of": t.get("redo_of")}
        if (r_id, tid) in by_trial:
            bid, _ = by_trial[(r_id, tid)]
            row.update(blind_id=bid, verdict=verdicts[bid]["verdict"], verdict_basis="blind_verdict", note=verdicts[bid]["note"])
        elif a is not None:
            row.update(verdict="reject", verdict_basis=f"no_artifact:{a.get('status')}")
        else:
            row.update(verdict="reject", verdict_basis="not_dispatched")
        rows.append(row)
    elimination = apply_elimination(rows)
    results = {"run_id": run_id, "revealed_utc": _now(), "commitment_verified": True, "commitment": committed, "key_path": str(key_path),
               "seed": key["seed"], "salt": key["salt"], "rules_ref": RULES_REF,
               "rule_text": "E1: refusal/hard error >= ceil(0.375 n); E2: accepts <= floor(0.25 n); n = planned trials per (route, question); E5: no artifact = reject",
               "trials": rows, "elimination": elimination}
    (out / RESULTS).write_text("# EVAL-040 results after the blind reveal; verdicts are the Controller's, merged by judging_packet.py\n"
                               + yaml.safe_dump(results, sort_keys=False, allow_unicode=True, width=160), encoding="utf-8")
    text = table_text(elimination)
    print(text)
    return {"run_id": run_id, "results_path": str(out / RESULTS), "elimination": elimination, "table_text": text}


# ------------------------------------------------------------------------------ cli
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("build", "reveal"):
        p = sub.add_parser(name)
        p.add_argument("--run-id", required=True)
        p.add_argument("--out", required=True)
        p.add_argument("--key-dir", required=True, help="a directory OUTSIDE the repo for the reveal key")
        p.add_argument("--extra-run", action="append", default=None, metavar="OUT:RUN_ID", help="judge another run (e.g. a redo run) in the SAME blind set")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "build":
            extra = []
            for spec in (a.extra_run or []):
                o, _, r = spec.rpartition(":")
                if not o or not r:
                    raise PacketRefused("--extra-run takes OUT_DIR:RUN_ID")
                extra.append((o, r))
            print(json.dumps(build(a.out, a.run_id, a.key_dir, extra_runs=extra), indent=1))
        else:
            r = reveal(a.out, a.run_id, a.key_dir)
            print(f"results: {r['results_path']}")
        return 0
    except (PacketRefused, RL.PlanRefused) as exc:
        print(f"REFUSED ({type(exc).__name__}): {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
