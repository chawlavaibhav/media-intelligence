"""Input resolver (EVAL-041 part 2): a committed INPUTS.yaml maps (case_id, arm, role) to a SEALED artifact.

WHAT THIS DOES, IN PLAIN ENGLISH

    Half two of the image battery (edit / extend / composite / reference cases) and the image-to-video arms of
    VID-TOPO3-01 need an input picture. Until now the adapters rendered a `$pending_artifact` placeholder in that
    slot and every such row refused to dispatch. This module is the ONLY way a real input reaches an adapter:

      1. the Controller writes `INPUTS.yaml` next to the plan, one line per (case, arm, role), each naming a sealed
         artifact - a constructed stand-in FIXTURE (`fixture:<run_id>:<fixture_id>`, from `run_live.py fixtures`)
         or a PRIOR TRIAL's artifact (`<run_id>:<trial_id>[:<suffix>]`, e.g. the Controller-accepted 9:16 plate);
      2. `run_live.py plan --inputs INPUTS.yaml` resolves every role at PLAN time: loads the bytes from the sealed
         store, verifies sha256 against the sealed record (and against the `sha256` the line pins, when given),
         and renders the body WITH those bytes, so the plan's body_sha256 commits to the exact input;
      3. `execute` re-resolves at DISPATCH time and refuses the trial if the INPUTS file's sha changed, if any
         resolved input's sha differs from the plan's, or if the rendered body differs from the plan's.

    A role nobody mapped stays `$pending_artifact` and the row keeps refusing (`input_unresolved:<role>`).

HOW THE BYTES TRAVEL

    fal routes take URLs (`image_url` / `image_urls` / `start_image_url`, pinned schema type `string`, no format
    constraint in the pinned bytes): the resolver hands a DATA URI (`data:<mime>;base64,...`), so no upload step,
    no third host and no key leaves this machine. Source: the pinned fal OpenAPI extracts under schemas/fal/
    (`image_urls: {type: array, items: {type: string}}`, `image_url: {type: string}` - silent on the URI scheme);
    fal's public API documentation states that data URIs are accepted wherever a file URL is; that statement is
    NOT in the pinned bytes and is proven by the first live smoke test, never assumed by a test here.
    Vertex routes take bytes inline: Gemini image edit `reference_images` [(bytes, mime)], Veo i2v `image_bytes`
    + `image_mime`, Veo ref2v `reference_images`.

DECOYS ARE NEVER SENT

    A fixture record with `is_decoy: true` (the same-category decoy tins / portraits of the stand-in spec) refuses
    to resolve: decoys belong to the qualification pack (Q4 judging), not to the generation. IMG-COMP-01 sends the
    portrait and the packshot; IMG-REF-* send the identity views in order (reference_asset_1 .. n).
"""
from __future__ import annotations

import base64
import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

import yaml

import hv2_paths
import store as S

DEFAULT_RUNS_ROOT = hv2_paths.EVAL_ROOT / "experiments" / "EVAL-040" / "runs"
FIXTURES_SUBDIR = "fixtures"                      # <run>/artifacts/fixtures/<fixture_id>.fixture.json
WILDCARD_ARM = "*"
# adapters whose request carries a recorded CHOICE (`$pending_choice` in adapters/base): (what, adapter input key).
# Mapped in INPUTS.yaml as role `choice:<what>` with ref `literal:<value>`; a missing line keeps the row refusing.
CHOICE_ROLES = {"sarvam_tts": (("speaker_id_lowercase", "voice"),), "elevenlabs_direct": (("voice", "voice"),)}
DATA_URI_SOURCE = ("pinned fal OpenAPI extracts (schemas/fal/*.json): image_url / image_urls / start_image_url are `type: string` "
                   "with no format constraint; data URIs per fal's public API documentation (not in the pinned bytes; proven by the "
                   "first live smoke, never by a test)")


class InputsError(RuntimeError):
    """The mapping file or a referenced artifact cannot be trusted. Nothing was sent."""


@dataclass
class ResolvedInput:
    role: str
    ref: str
    kind: str                       # fixture | trial
    run_id: str
    artifact_id: str                # fixture_id or trial_id
    suffix: str | None
    relative_path: str
    sha256: str
    bytes: int
    content_type: str
    data: bytes = field(repr=False)
    constructed_synthetic: bool = False
    is_decoy: bool = False
    for_case: str | None = None
    fixture_role: str | None = None

    def summary(self) -> dict:
        """What the plan records: everything except the bytes."""
        return {"role": self.role, "ref": self.ref, "kind": self.kind, "run_id": self.run_id, "artifact_id": self.artifact_id,
                "suffix": self.suffix, "relative_path": self.relative_path, "sha256": self.sha256, "bytes": self.bytes,
                "content_type": self.content_type, "constructed_synthetic": self.constructed_synthetic,
                "for_case": self.for_case, "fixture_role": self.fixture_role}

    @property
    def mime(self) -> str:
        return (self.content_type or "application/octet-stream").split(";")[0].strip().lower()

    def data_uri(self) -> str:
        return f"data:{self.mime};base64,{base64.b64encode(self.data).decode('ascii')}"


# ----------------------------------------------------------------------------------- refs
def parse_ref(ref: str) -> dict:
    """`fixture:<run_id>:<fixture_id>` or `<run_id>:<trial_id>[:<suffix>]`."""
    if not isinstance(ref, str) or not ref.strip():
        raise InputsError(f"input ref must be a non-empty string, got {ref!r}")
    parts = ref.strip().split(":")
    if parts[0] == "literal":
        # 2026-09-09: a recorded CHOICE (a voice name, a speaker id) - never bytes; the plan commits to the value
        value = ref.strip()[len("literal:"):]
        if not value or any(ch.isspace() for ch in value):
            raise InputsError(f"literal ref {ref!r} must be literal:<value> with no whitespace")
        return {"kind": "literal", "run_id": None, "artifact_id": value, "suffix": None}
    if parts[0] == "fixture":
        if len(parts) != 3 or not all(parts[1:]):
            raise InputsError(f"fixture ref {ref!r} must be fixture:<run_id>:<fixture_id>")
        return {"kind": "fixture", "run_id": parts[1], "artifact_id": parts[2], "suffix": None}
    if len(parts) not in (2, 3) or not all(parts):
        raise InputsError(f"trial ref {ref!r} must be <run_id>:<trial_id>[:<suffix>] (or fixture:<run_id>:<fixture_id>)")
    return {"kind": "trial", "run_id": parts[0], "artifact_id": parts[1], "suffix": (parts[2] if len(parts) == 3 else None)}


def _read_verified(root: Path, rec: dict, what: str) -> bytes:
    rel = rec.get("relative_path")
    sha = rec.get("sha256")
    if not rel or not sha:
        raise InputsError(f"{what}: the sealed record names no relative_path / sha256")
    path = root / rel
    if not path.exists():
        raise InputsError(f"{what}: sealed media {path} is missing")
    data = path.read_bytes()
    actual = hashlib.sha256(data).hexdigest()
    if actual != sha or (rec.get("bytes") is not None and len(data) != int(rec["bytes"])):
        raise InputsError(f"{what}: sealed bytes hash to {actual[:12]}... but the record says {sha[:12]}...; the artifact was altered. Nothing was sent.")
    return data


def load_fixture(runs_root: Path | str, run_id: str, fixture_id: str, role: str, ref: str) -> ResolvedInput:
    return load_fixture_at(Path(runs_root) / run_id / "artifacts", run_id, fixture_id, role, ref)


def load_fixture_at(store_root: Path | str, run_id: str, fixture_id: str, role: str, ref: str) -> ResolvedInput:
    """A fixture from an explicit sealed-store root (the fixtures runner's own store)."""
    root = Path(store_root)
    rec_path = root / FIXTURES_SUBDIR / f"{S.safe_id(fixture_id)}.fixture.json"
    if not rec_path.exists():
        raise InputsError(f"{ref}: no fixture record at {rec_path}")
    rec = json.loads(rec_path.read_text(encoding="utf-8"))
    if rec.get("is_decoy"):
        raise InputsError(f"{ref}: fixture {fixture_id} is a DECOY (same-category decoy for the qualification pack); decoys are never sent to a provider")
    if rec.get("constructed_synthetic") is not True:
        raise InputsError(f"{ref}: fixture record does not declare constructed_synthetic: true; a fixture never passes as a customer photo")
    data = _read_verified(root, rec, ref)
    return ResolvedInput(role=role, ref=ref, kind="fixture", run_id=run_id, artifact_id=fixture_id, suffix=None,
                         relative_path=rec["relative_path"], sha256=rec["sha256"], bytes=len(data), content_type=rec.get("content_type") or "image/png",
                         data=data, constructed_synthetic=True, is_decoy=False, for_case=rec.get("for_case"), fixture_role=rec.get("role"))


def load_trial_artifact(runs_root: Path | str, run_id: str, trial_id: str, suffix: str | None, role: str, ref: str) -> ResolvedInput:
    root = Path(runs_root) / run_id / "artifacts"
    sid = S.safe_id(trial_id) + (f".{S.safe_id(suffix)}" if suffix else "")
    rec_path = root / f"{sid}.record.json"
    if not rec_path.exists():
        raise InputsError(f"{ref}: no sealed artifact record at {rec_path}")
    rec = json.loads(rec_path.read_text(encoding="utf-8"))
    data = _read_verified(root, rec, ref)
    prov = rec.get("provider") or {}
    return ResolvedInput(role=role, ref=ref, kind="trial", run_id=run_id, artifact_id=trial_id, suffix=suffix,
                         relative_path=rec["relative_path"], sha256=rec["sha256"], bytes=len(data), content_type=rec.get("content_type") or "application/octet-stream",
                         data=data, constructed_synthetic=bool(prov.get("constructed_synthetic")), is_decoy=False)


@dataclass
class LiteralInput:
    """A recorded choice (e.g. the TTS speaker id) mapped through INPUTS.yaml as `literal:<value>`; no bytes, no store."""
    role: str
    ref: str
    value: str

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.value.encode("utf-8")).hexdigest()

    def summary(self) -> dict:
        return {"role": self.role, "ref": self.ref, "kind": "literal", "value": self.value, "sha256": self.sha256,
                "run_id": None, "artifact_id": None, "bytes": None, "mime": None, "constructed_synthetic": False, "is_decoy": False}


# ----------------------------------------------------------------------------------- file
class InputsFile:
    """The committed mapping. Read once; its sha256 is recorded on the plan and re-checked at execute."""

    def __init__(self, path: Path | str, runs_root: Path | str | None = None):
        self.path = Path(path)
        if not self.path.exists():
            raise InputsError(f"inputs file {self.path} does not exist")
        raw = self.path.read_bytes()
        self.sha256 = hashlib.sha256(raw).hexdigest()
        data = yaml.safe_load(raw.decode("utf-8")) or {}
        if not isinstance(data, dict) or not isinstance(data.get("inputs"), list):
            raise InputsError(f"{self.path}: expected a mapping with an `inputs` list")
        rr = runs_root or data.get("runs_root")
        self.runs_root = (Path(rr) if rr else DEFAULT_RUNS_ROOT)
        if not self.runs_root.is_absolute():
            self.runs_root = hv2_paths.REPO_ROOT / self.runs_root
        self.entries: list[dict] = []
        seen = set()
        for i, e in enumerate(data["inputs"]):
            if not isinstance(e, dict):
                raise InputsError(f"{self.path}: inputs[{i}] is not a mapping")
            for k in ("case_id", "role", "ref"):
                if not e.get(k):
                    raise InputsError(f"{self.path}: inputs[{i}] lacks {k}")
            parse_ref(e["ref"])
            arm = e.get("arm") or WILDCARD_ARM
            key = (e["case_id"], arm, e["role"])
            if key in seen:
                raise InputsError(f"{self.path}: duplicate mapping for {key}")
            seen.add(key)
            self.entries.append({"case_id": e["case_id"], "arm": arm, "role": e["role"], "ref": e["ref"].strip(),
                                 "sha256": (e.get("sha256") or None), "note": e.get("note")})

    def entries_for(self, case_id: str, arm: str | None) -> dict[str, dict]:
        """role -> entry; an exact-arm line beats a `*` line."""
        out: dict[str, dict] = {}
        for e in self.entries:
            if e["case_id"] != case_id or e["arm"] not in (WILDCARD_ARM, arm):
                continue
            if e["role"] in out and out[e["role"]]["arm"] != WILDCARD_ARM:
                continue
            out[e["role"]] = e
        return out

    def load(self, entry: dict) -> ResolvedInput:
        r = parse_ref(entry["ref"])
        if r["kind"] == "literal":
            return LiteralInput(role=entry["role"], ref=entry["ref"], value=r["artifact_id"])
        if r["kind"] == "fixture":
            res = load_fixture(self.runs_root, r["run_id"], r["artifact_id"], entry["role"], entry["ref"])
        else:
            res = load_trial_artifact(self.runs_root, r["run_id"], r["artifact_id"], r["suffix"], entry["role"], entry["ref"])
        if entry.get("sha256") and entry["sha256"] != res.sha256:
            raise InputsError(f"{entry['ref']}: INPUTS pins sha256 {entry['sha256'][:12]}... but the sealed artifact is {res.sha256[:12]}...; "
                              f"the mapping names other bytes than the store holds. Nothing was sent.")
        return res


# ----------------------------------------------------------------------------------- roles
def roles_needed(entry, case_row: dict) -> list[tuple[str, str]]:
    """[(role, adapter input key)] this route needs for this row, in the order the adapter consumes them.
    Mirrors the placeholder roles the adapters render (fal_queue._resolve, vertex_gemini_image, vertex_veo)."""
    params = case_row.get("params") or {}
    try:
        refs = int(params.get("refs") or 0)
    except (TypeError, ValueError):
        refs = 0
    out: list[tuple[str, str]] = []
    out += [(f"choice:{what}", key) for what, key in CHOICE_ROLES.get(entry.adapter, ())]
    if entry.adapter == "fal_queue":
        from adapters import fal_queue as FQ
        pins = FQ.ROUTE_PINS.get(entry.route_key) or {}
        for spec in pins.values():
            if not isinstance(spec, str) or not spec.startswith("in:"):
                continue
            key = spec[3:]
            if key == "image_urls":
                out += [(f"reference_asset_{i + 1}", "image_urls") for i in range(max(refs, 1))]
            elif key == "image_url":
                out.append(("plate_accepted_draw", "image_url"))
            elif key == "video_url":
                out.append(("plate_clip", "video_url"))
            elif key == "audio_url":
                out.append(("drive_audio", "audio_url"))
    elif entry.adapter == "vertex_gemini_image":
        if entry.workflow == "edit" or refs > 0:
            out += [(f"reference_asset_{i + 1}", "reference_images") for i in range(max(refs, 1))]
    elif entry.adapter == "vertex_veo":
        if entry.workflow == "i2v":
            out.append(("plate_accepted_draw", "image_bytes"))
        elif entry.workflow == "ref2v":
            out += [(f"reference_asset_{i + 1}", "reference_images") for i in range(min(refs or 3, 3))]
    return out


def build_inputs(entry, needed: list[tuple[str, str]], resolved: dict[str, ResolvedInput]) -> dict:
    """The adapter `inputs` dict in the role the adapter wants (data URIs for fal, bytes for Vertex)."""
    inputs: dict = {}
    for role, key in needed:
        r = resolved[role]
        if isinstance(r, LiteralInput):
            inputs[key] = r.value
            continue
        if entry.adapter == "fal_queue":
            if key == "image_urls":
                inputs.setdefault("image_urls", []).append(r.data_uri())
            else:
                inputs[key] = r.data_uri()
        elif key == "reference_images":
            inputs.setdefault("reference_images", []).append((r.data, r.mime))
        elif key == "image_bytes":
            inputs["image_bytes"] = r.data
            inputs["image_mime"] = r.mime
        else:
            raise InputsError(f"no input shape for role {role} / key {key} on adapter {entry.adapter}")
    return inputs


class InputResolver:
    """`for_row(case_row, entry)` -> (adapter inputs, [resolved summaries], [unresolved roles]). Nothing sent."""

    def __init__(self, inputs_file: InputsFile | None):
        self.file = inputs_file

    def for_row(self, case_row: dict, entry) -> tuple[dict, list[dict], list[str]]:
        needed = roles_needed(entry, case_row)
        if not needed:
            return {}, [], []
        mapped = self.file.entries_for(case_row.get("case_id"), case_row.get("arm")) if self.file else {}
        resolved: dict[str, ResolvedInput] = {}
        unresolved: list[str] = []
        for role, _key in needed:
            e = mapped.get(role)
            if e is None:
                unresolved.append(role)
                continue
            resolved[role] = self.file.load(e)        # InputsError on a sha / decoy problem propagates: refuse loudly
        if unresolved:
            # partial inputs are never handed over: the adapter would render placeholders for the rest anyway
            return {}, [resolved[r].summary() for r, _ in needed if r in resolved], unresolved
        return build_inputs(entry, needed, resolved), [resolved[r].summary() for r, _ in needed], []


def write_inputs_file(path: Path | str, lines: list[dict], runs_root: Path | str | None = None, note: str | None = None) -> Path:
    """Helper for tests and fixture runs: a well-formed INPUTS.yaml."""
    doc = {"inputs_file": "EVAL-041 INPUTS", "note": note or "maps (case_id, arm, role) -> a sealed artifact; the plan commits to these bytes",
           "data_uri_source": DATA_URI_SOURCE, **({"runs_root": str(runs_root)} if runs_root else {}), "inputs": lines}
    p = Path(path)
    p.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=160), encoding="utf-8")
    return p
