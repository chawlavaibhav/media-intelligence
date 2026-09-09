"""vlm_screen -> a SCREENED, NOT QUALIFIED instrument: one artifact + its case's acceptance contract, judged line by line by a
Gemini model on the Gemini Developer API (Controller decision CONTROLLER-GEMINI-MODELS-VIA-GEMINI-KEY-2026-09-09: Gemini-named
models run on the key NAMED GOOGLE_API_KEY at generativelanguage.googleapis.com, never Vertex).

    contract line i  ->  {rule_id: R<i>, kind: accept_only | reject | mixed | unclassified, verdict: pass | fail | cannot_judge, evidence}
    overall          ->  derived IN CODE by the Controller's own rule: any line failing = reject; every line passing = accept;
                         otherwise cannot_judge. The model is never asked for the overall verdict.
    image            ->  the sealed bytes inline (png / jpg / webp, no re-encode)
    video            ->  3 frames (first / middle / last) via imageio.stream_video_frames, downscaled and PNG-encoded, inline
    audio            ->  every line cannot_judge, no call, USD 0

Strict JSON out (responseMimeType application/json + a response schema), temperature 0. The prompt text, the response schema,
the model id, the frame policy and the sha256 of SCREEN-QUALIFICATION-CRITERIA-v0.yaml are all in the instrument config, so
config_hash changes when any of them does. qualification_status is `screened_not_qualified`: registry_gate refuses it
(it is specified for no deterministic capability) and evidence_map.py files its output under the screened tier only.

Fail-closed vocabulary (harness verdicts): accept -> pass, reject -> fail, cannot_judge / refusal / HTTP error / unparseable
answer -> absent (never pass). The key value lives in one request header and nowhere else; provider text is scrubbed before
it enters a result. Only transports.py opens a socket: this module calls `transport.post_json` and nothing else, so
transports.FakeTransport stands in for GeminiApiTransport in the tests.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import re
from pathlib import Path

import yaml

import hv2_paths  # noqa: F401
import harness as H
from providers import PreDispatchRefusal
from . import common as C
from . import imageio as IO

HERE = Path(__file__).resolve().parent
INSTRUMENT_ID = "vlm_screen"
VERSION = "0.1.0"
DEFAULT_MODEL = "gemini-3.1-flash"            # a config value, not a claim that the id exists or is the right one
QUALIFICATION_STATUS = "screened_not_qualified"
CAPABILITIES = ("acceptance_contract_screen",)  # not one of EVALUATOR-PLAN's deterministic capabilities: the gate refuses it
KEY_NAME = "GOOGLE_API_KEY"
SURFACE = "gemini_api"
CRITERIA_PATH = HERE / "SCREEN-QUALIFICATION-CRITERIA-v0.yaml"
CRITERIA_REF = "eval/harness-v2/instruments/SCREEN-QUALIFICATION-CRITERIA-v0.yaml"
VIDEO_FRAMES = 3
FRAME_MAX_SIDE = 768
IMAGE_MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
VIDEO_EXT = (".mp4", ".mov", ".webm", ".mkv")
AUDIO_EXT = (".wav", ".mp3", ".m4a", ".flac", ".ogg", ".aac")
RULE_VERDICTS = ("pass", "fail", "cannot_judge")
OVERALLS = ("accept", "reject", "cannot_judge")

PROMPT_TEMPLATE = """You are screening ONE generated {media_word} against an acceptance contract that a human reviewer wrote before seeing it.
The contract is a numbered list of rules. Judge each rule ONLY from what is visible in the attached {evidence_word}; never guess and never assume anything about sound, smell, motion or intent that the pixels do not show.

Verdict vocabulary per rule:
  pass          = an "ACCEPT only if" condition visibly holds, or a "REJECT if" condition is visibly absent.
  fail          = the condition is visibly violated (the ACCEPT condition does not hold, or the REJECT condition is present).
  cannot_judge  = the evidence is not in the {evidence_word} (audio, speech, timing, motion between frames, lettering too small or blurred to read, a script you cannot read letter by letter).

Evidence: exactly one sentence per rule stating what you see that decides it. Transcribe any lettering VERBATIM in its own script (Devanagari stays Devanagari) and compare it character by character with the contract; a single wrong, missing, doubled or invented character is a fail.
{frames_note}
Return ONLY JSON of the form {{"rules": [{{"rule_id": "R1", "verdict": "pass|fail|cannot_judge", "evidence": "..."}}, ...]}} with one entry per rule, in the order given, and nothing else. Do not give an overall verdict; it is computed from your per-rule answers.

CONTRACT
{rules_block}
"""
FRAMES_NOTE_VIDEO = ("The attached images are {n} frames of one video clip, sampled at the start, the middle and the end (in that order, timestamps given). "
                     "Judge continuity, drift, warping and camera movement only where it is inferable across these frames; anything about sound, "
                     "speech, flicker or timing that three frames cannot show is cannot_judge.")
FRAMES_NOTE_IMAGE = "The attached image is the whole artifact."

RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "rules": {"type": "ARRAY", "items": {
            "type": "OBJECT",
            "properties": {"rule_id": {"type": "STRING"}, "verdict": {"type": "STRING", "enum": list(RULE_VERDICTS)}, "evidence": {"type": "STRING"}},
            "required": ["rule_id", "verdict", "evidence"]}},
    },
    "required": ["rules"],
}
GENERATION_CONFIG = {"temperature": 0, "responseMimeType": "application/json", "responseSchema": RESPONSE_SCHEMA}


class ScreenError(RuntimeError):
    """The instrument cannot form a judgement; the caller records absent, never pass."""


# ------------------------------------------------------------------------------ criteria file
def load_criteria(path: Path | str | None = None) -> dict:
    p = Path(path) if path else CRITERIA_PATH
    raw = p.read_bytes()
    data = yaml.safe_load(raw.decode("utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("thresholds"), dict):
        raise C.CriteriaError(f"{p}: no thresholds mapping")
    data["_sha256"] = hashlib.sha256(raw).hexdigest()
    data["_path"] = str(p)
    data["_frozen"] = data.get("frozen") is True
    return data


# ------------------------------------------------------------------------------ the contract
_ACCEPT = re.compile(r"\bACCEPT\b", re.I)
_REJECT = re.compile(r"\bREJECT\b", re.I)


def parse_contract(contract) -> list[dict]:
    """Every contract line is one rule. kind: accept_only ('ACCEPT only if ...'), reject ('REJECT if ...'), mixed (both), unclassified."""
    lines = contract if isinstance(contract, (list, tuple)) else [contract]
    rules = []
    for i, text in enumerate(lines, 1):
        t = " ".join(str(text or "").split())
        if not t:
            continue
        a, r = bool(_ACCEPT.search(t)), bool(_REJECT.search(t))
        kind = "mixed" if a and r else "accept_only" if a else "reject" if r else "unclassified"
        rules.append({"rule_id": f"R{i}", "kind": kind, "text": t})
    if not rules:
        raise ScreenError("the case has no acceptance_contract lines; nothing to screen against")
    return rules


def derive_overall(rule_verdicts: list) -> str:
    """The Controller's rule, applied in code: any failing line (ACCEPT-only or REJECT) = reject; all passing = accept; else cannot_judge."""
    vs = [r.get("verdict") for r in rule_verdicts]
    if any(v == "fail" for v in vs):
        return "reject"
    if vs and all(v == "pass" for v in vs):
        return "accept"
    return "cannot_judge"


def render_prompt(rules: list, media_kind: str, n_frames: int = 0, template: str = PROMPT_TEMPLATE) -> str:
    block = "\n".join(f"{r['rule_id']} [{r['kind']}]: {r['text']}" for r in rules)
    if media_kind == "video":
        note = FRAMES_NOTE_VIDEO.format(n=n_frames)
        media_word, evidence_word = "video clip", "frames"
    else:
        note, media_word, evidence_word = FRAMES_NOTE_IMAGE, "image", "image"
    return template.format(media_word=media_word, evidence_word=evidence_word, frames_note=note, rules_block=block)


# ------------------------------------------------------------------------------ media
def media_kind_of(path: Path | str) -> str:
    ext = Path(path).suffix.lower()
    if ext in IMAGE_MIME:
        return "image"
    if ext in VIDEO_EXT:
        return "video"
    if ext in AUDIO_EXT:
        return "audio"
    return "other"


def _inline(mime: str, data: bytes) -> dict:
    return {"inlineData": {"mimeType": mime, "data": base64.b64encode(data).decode("ascii")}}


def _downscale(img: IO.Image, max_side: int) -> IO.Image:
    longest = max(img.width, img.height)
    if max_side <= 0 or longest <= max_side:
        return img
    scale = max_side / longest
    return IO.resize_nearest(img, max(1, int(img.width * scale)), max(1, int(img.height * scale)))


def sample_video_frames(path: Path | str, n: int = VIDEO_FRAMES, max_side: int = FRAME_MAX_SIDE) -> list[dict]:
    """first / middle / last frames through ONE ffmpeg decode (imageio.stream_video_frames), holding at most a handful of raw
    frames in memory (an 8 GB machine; a 1080p frame is 6 MB). The middle index comes from ffprobe's frame count or
    duration x fps; the last frame is whatever the stream ends on, so an over-estimate cannot lose it."""
    info = IO.ffprobe(path)
    if not info["has_video"] or not info["width"] or not info["height"]:
        raise IO.ProbeError(f"{Path(path).name} has no video stream")
    w, h = int(info["width"]), int(info["height"])
    fps = info["fps"] or 25.0
    total = None
    try:
        total = int(info["nb_frames"]) if info.get("nb_frames") else None
    except ValueError:
        total = None
    if not total and info["duration_s"]:
        total = max(1, round(float(info["duration_s"]) * fps))
    mid_est = ((total - 1) // 2) if total else 0
    kept: dict = {}
    last = None
    count = 0
    for idx, buf in enumerate(IO.stream_video_frames(path, w, h)):
        count = idx + 1
        if idx == 0 or idx == mid_est:
            kept[idx] = buf
        last = (idx, buf)
    if count == 0 or last is None:
        raise IO.ProbeError(f"{Path(path).name}: ffmpeg decoded no frames")
    picks = [(0, kept[0])]
    mid_actual = (count - 1) // 2
    if mid_est in kept and 0 < mid_est < count - 1:
        picks.append((mid_est, kept[mid_est]))
    elif 0 < mid_actual < count - 1 and mid_actual in kept:
        picks.append((mid_actual, kept[mid_actual]))
    if last[0] > 0:
        picks.append(last)
    picks = picks[:n]
    out = []
    for idx, buf in picks:
        img = _downscale(IO.Image(w, h, 3, buf), max_side)
        png = IO.encode_png(img.rows(), img.width, img.height, channels=3)
        out.append({"frame_index": idx, "time_s": round(idx / fps, 3), "width": img.width, "height": img.height,
                    "source_width": w, "source_height": h, "png_bytes": len(png), "sha256": hashlib.sha256(png).hexdigest(), "_png": png})
    return out


def media_parts(path: Path | str, n_frames: int = VIDEO_FRAMES, max_side: int = FRAME_MAX_SIDE) -> tuple:
    """(media_kind, parts, meta). Images go inline as sealed; video as sampled PNG frames; audio yields no parts."""
    p = Path(path)
    if not p.exists() or p.stat().st_size == 0:
        raise IO.ProbeError(f"{p} does not exist or is empty")
    kind = media_kind_of(p)
    if kind == "image":
        data = p.read_bytes()
        return kind, [_inline(IMAGE_MIME[p.suffix.lower()], data)], {"images": 1, "bytes": len(data), "mime": IMAGE_MIME[p.suffix.lower()]}
    if kind == "video":
        frames = sample_video_frames(p, n_frames, max_side)
        parts = []
        for f in frames:
            parts.append({"text": f"frame {f['frame_index']} at t={f['time_s']} s"})
            parts.append(_inline("image/png", f.pop("_png")))
        return kind, parts, {"images": len(frames), "frames": frames}
    if kind == "audio":
        return kind, [], {"images": 0}
    raise IO.ProbeError(f"{p.name}: unsupported artifact type {p.suffix!r}")


# ------------------------------------------------------------------------------ key
def read_key_by_name(name: str = KEY_NAME, path: Path | str | None = None) -> str:
    """The key by NAME from the environment or the `export NAME=value` file adapters.base points at (a throw-away file in
    tests, never ~/.mi-keys). The value goes to the caller and nowhere else."""
    if name != KEY_NAME:
        raise PreDispatchRefusal(f"key name {name!r} is not the one this instrument may read ({KEY_NAME}); nothing was sent")
    value = os.environ.get(name)
    if value:
        return value
    if path is None:
        import adapters.base as B                 # looked up at call time so a test can redirect it
        path = B.DEFAULT_KEY_FILE
    path = Path(path).expanduser()
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)=(.*)$", line)
            if m and m.group(1) == name:
                v = m.group(2).strip().strip('"').strip("'")
                if v:
                    return v
    raise PreDispatchRefusal(f"{name} is not set in the environment or in {path.name} (read by name; never printed). Nothing was sent.")


def _scrub(text, secret: str | None) -> str:
    s = str(text)
    return s.replace(secret, "<REDACTED>") if secret else s


# ------------------------------------------------------------------------------ the answer
def parse_answer(status: int, doc, rules: list, secret: str | None = None) -> dict:
    """{kind: ok | http_error | refusal | malformed, rules: [...], finish_reason, usage, text_sha256, detail}."""
    if status != 200:
        detail = ""
        if isinstance(doc, dict):
            err = doc.get("error") if isinstance(doc.get("error"), dict) else {}
            detail = _scrub(f"{err.get('status') or ''} {err.get('message') or ''}".strip() or json.dumps(doc)[:200], secret)
        return {"kind": "http_error", "status": status, "detail": detail[:300]}
    if not isinstance(doc, dict):
        return {"kind": "malformed", "status": status, "detail": "answer is not a JSON object"}
    usage = doc.get("usageMetadata") if isinstance(doc.get("usageMetadata"), dict) else {}
    usage = {k: usage.get(k) for k in ("promptTokenCount", "candidatesTokenCount", "totalTokenCount", "thoughtsTokenCount") if usage.get(k) is not None}
    pf = doc.get("promptFeedback") if isinstance(doc.get("promptFeedback"), dict) else {}
    if pf.get("blockReason"):
        return {"kind": "refusal", "status": status, "detail": f"prompt blocked: {pf.get('blockReason')}", "usage": usage}
    cands = doc.get("candidates")
    if not isinstance(cands, list) or not cands or not isinstance(cands[0], dict):
        return {"kind": "refusal", "status": status, "detail": "no candidates in the answer", "usage": usage}
    cand = cands[0]
    finish = cand.get("finishReason")
    parts = ((cand.get("content") or {}).get("parts") or []) if isinstance(cand.get("content"), dict) else []
    text = "".join(str(p.get("text", "")) for p in parts if isinstance(p, dict))
    if not text.strip():
        return {"kind": "refusal", "status": status, "detail": f"empty answer (finishReason {finish})", "finish_reason": finish, "usage": usage}
    if finish not in (None, "STOP"):
        return {"kind": "refusal", "status": status, "detail": f"finishReason {finish}", "finish_reason": finish, "usage": usage}
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        return {"kind": "malformed", "status": status, "detail": f"answer is not JSON: {exc}", "finish_reason": finish, "usage": usage,
                "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()}
    got = parsed.get("rules") if isinstance(parsed, dict) else None
    if not isinstance(got, list):
        return {"kind": "malformed", "status": status, "detail": "JSON has no rules list", "finish_reason": finish, "usage": usage}
    by_id = {}
    for entry in got:
        if not isinstance(entry, dict):
            return {"kind": "malformed", "status": status, "detail": "a rules entry is not an object", "usage": usage}
        rid, verdict = str(entry.get("rule_id", "")).strip(), str(entry.get("verdict", "")).strip().lower()
        if verdict not in RULE_VERDICTS:
            return {"kind": "malformed", "status": status, "detail": f"verdict {verdict!r} for {rid or '?'} is not one of {RULE_VERDICTS}", "usage": usage}
        by_id[rid] = {"verdict": verdict, "evidence": _scrub(" ".join(str(entry.get("evidence", "")).split())[:600], secret)}
    out = []
    for r in rules:
        v = by_id.get(r["rule_id"])
        if v is None:
            v = {"verdict": "cannot_judge", "evidence": "no verdict returned for this rule"}
        out.append({"rule_id": r["rule_id"], "kind": r["kind"], "rule": r["text"], **v})
    return {"kind": "ok", "status": status, "rules": out, "finish_reason": finish, "usage": usage,
            "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()}


# ------------------------------------------------------------------------------ the session
class ScreenSession:
    """Everything one instrument instance needs: transport (injected; live only when None AND allow_live), model, prompt, counters.
    `max_calls` is a hard stop the runner sets from its cap; the default 0 means NO live call may leave this session."""

    def __init__(self, transport=None, model: str = DEFAULT_MODEL, key_reader=None, prompt_template: str = PROMPT_TEMPLATE,
                 n_frames: int = VIDEO_FRAMES, frame_max_side: int = FRAME_MAX_SIDE, max_calls: int = 0, criteria_path: Path | str | None = None):
        self.transport = transport
        self.model = model
        self.key_reader = key_reader or read_key_by_name
        self.prompt_template = prompt_template
        self.n_frames = int(n_frames)
        self.frame_max_side = int(frame_max_side)
        self.max_calls = int(max_calls)
        self.criteria = load_criteria(criteria_path)
        self.calls = 0
        self.prompt_tokens = 0
        self.output_tokens = 0
        self.total_tokens = 0
        self.log: list[dict] = []

    @property
    def config(self) -> dict:
        return {"instrument": INSTRUMENT_ID, "version": VERSION, "model": self.model, "surface": SURFACE,
                "endpoint_template": "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                "credential_name": KEY_NAME, "prompt_template": self.prompt_template, "frames_note_video": FRAMES_NOTE_VIDEO,
                "frames_note_image": FRAMES_NOTE_IMAGE, "generation_config": GENERATION_CONFIG, "video_frames": self.n_frames,
                "frame_max_side": self.frame_max_side, "overall_rule": "any failing line = reject; all lines pass = accept; else cannot_judge (derived in code)",
                "audio_policy": "cannot_judge, no call", "qualification_status": QUALIFICATION_STATUS,
                "criteria_ref": CRITERIA_REF, "criteria_file_sha256": self.criteria["_sha256"], "criteria_frozen": self.criteria["_frozen"],
                "tool_versions": C.tool_versions()}

    def _transport(self):
        if self.transport is None:
            import transports as T
            self.transport = T.GeminiApiTransport()
        return self.transport

    def evaluate(self, path: Path | str, contract) -> dict:
        try:
            rules = parse_contract(contract)
        except ScreenError as exc:
            return C.parse_failure(str(exc))
        base = {"model": self.model, "n_rules": len(rules)}
        try:
            kind, parts, meta = media_parts(path, self.n_frames, self.frame_max_side)
            base["artifact_sha256"] = C.sha256_file(path)
        except IO.ToolUnavailable as exc:
            return C.unavailable(str(exc))
        except (IO.ProbeError, OSError, ValueError) as exc:
            return C.parse_failure(str(exc), base)
        base.update({"media_kind": kind, **{k: v for k, v in meta.items() if k != "frames"}})
        if "frames" in meta:
            base["frames"] = meta["frames"]
        if kind == "audio":
            rv = [{"rule_id": r["rule_id"], "kind": r["kind"], "rule": r["text"], "verdict": "cannot_judge", "evidence": "audio: a vision screen cannot hear"} for r in rules]
            return self._finish("cannot_judge", rv, {**base, "calls": 0, "note": "audio artifact: no call made"}, note="cannot_judge: audio")
        prompt = render_prompt(rules, kind, meta.get("images", 0), self.prompt_template)
        base["prompt_sha256"] = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
        if self.calls >= self.max_calls:
            return C.result("absent", "not_measured", f"screen call budget exhausted ({self.calls}/{self.max_calls} calls); nothing was sent", base)
        try:
            secret = self.key_reader(KEY_NAME)
        except PreDispatchRefusal as exc:
            return C.unavailable(str(exc))
        from transports import gemini_generate_content_url
        body = {"contents": [{"role": "user", "parts": [{"text": prompt}, *parts]}], "generationConfig": GENERATION_CONFIG}
        payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
        base["request_bytes"] = len(payload)
        self.calls += 1
        try:
            status, doc = self._transport().post_json(gemini_generate_content_url(self.model), {"x-goog-api-key": secret}, payload)
        except Exception as exc:  # noqa: BLE001 - a transport failure is an absent verdict, and the key must not ride in the text
            return C.result("absent", "instrument_unavailable", f"transport failure: {_scrub(type(exc).__name__ + ': ' + str(exc), secret)[:300]}", {**base, "calls": 1})
        ans = parse_answer(status, doc, rules, secret)
        usage = ans.get("usage") or {}
        self.prompt_tokens += int(usage.get("promptTokenCount") or 0)
        self.output_tokens += int(usage.get("candidatesTokenCount") or 0)
        self.total_tokens += int(usage.get("totalTokenCount") or 0)
        m = {**base, "calls": 1, "http_status": status, "usage": usage, "finish_reason": ans.get("finish_reason"), "answer_sha256": ans.get("text_sha256")}
        self.log.append({"status": status, "kind": ans["kind"], "usage": usage})
        if ans["kind"] == "http_error":
            reason = "instrument_unavailable" if status in (401, 403, 404, 429) or status >= 500 else "other"
            return C.result("absent", reason, f"http {status}: {ans.get('detail', '')}", m)
        if ans["kind"] == "refusal":
            return C.result("absent", "other", f"model refusal: {ans.get('detail', '')}", m)
        if ans["kind"] == "malformed":
            return C.parse_failure(ans.get("detail", "unparseable answer"), m)
        return self._finish(derive_overall(ans["rules"]), ans["rules"], m)

    @staticmethod
    def _finish(overall: str, rule_verdicts: list, measurement: dict, note: str = "") -> dict:
        failing = [{"term": f"{r['rule_id']} fail: {r['evidence']}"} for r in rule_verdicts if r["verdict"] == "fail"]
        if overall == "accept":
            return C.result("pass", None, note or "accept: every contract line passed", measurement, overall="accept", rules=rule_verdicts)
        if overall == "reject":
            return C.result("fail", None, note or f"reject: {len(failing)} contract line(s) failed", measurement, defects=failing, overall="reject", rules=rule_verdicts)
        return C.result("absent", "other", note or "cannot_judge: no line failed and at least one could not be judged", measurement,
                        overall="cannot_judge", rules=rule_verdicts)


def contract_of(item: dict):
    inputs = C.inputs_of(item)
    if inputs.get("acceptance_contract") is not None:
        return inputs["acceptance_contract"]
    if isinstance(inputs.get("case_row"), dict) and inputs["case_row"].get("acceptance_contract") is not None:
        return inputs["case_row"]["acceptance_contract"]
    return item.get("acceptance_contract")


def instrument(transport=None, model: str = DEFAULT_MODEL, key_reader=None, criteria_path: Path | str | None = None,
               max_calls: int = 0, prompt_template: str = PROMPT_TEMPLATE, n_frames: int = VIDEO_FRAMES,
               frame_max_side: int = FRAME_MAX_SIDE) -> H.Instrument:
    """A harness.Instrument with qualification_status screened_not_qualified. `.session` is attached for counters and config."""
    session = ScreenSession(transport, model, key_reader, prompt_template, n_frames, frame_max_side, max_calls, criteria_path)

    def fn(path, item, capability):
        contract = contract_of(item) if isinstance(item, dict) else None
        if contract is None:
            return C.parse_failure("no acceptance_contract on the item (instrument_inputs.acceptance_contract or case_row)")
        return session.evaluate(path, contract)

    inst = H.Instrument(INSTRUMENT_ID, VERSION, session.config, qualification_status=QUALIFICATION_STATUS,
                        calibration_ref=f"{CRITERIA_REF}#thresholds", capabilities=CAPABILITIES, observation_unit="artifact", fn=fn)
    inst.session = session
    return inst
