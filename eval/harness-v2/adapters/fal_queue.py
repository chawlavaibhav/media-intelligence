"""fal queue adapter: one route family, parameterised by route key, body from the pinned OpenAPI.

LIFECYCLE (fal queue API; the QueueStatus component in every pinned schema names these fields)

    submit    POST https://queue.fal.run/<endpoint_id>      Authorization: Key $FAL_KEY
              -> {request_id, status_url, response_url, cancel_url, status}
    poll      GET  status_url   -> {status: IN_QUEUE | IN_PROGRESS | COMPLETED}
    result    GET  response_url -> the route's Output component (images[] / video / audio)
    download  GET  <artifact url>                            (fal CDN; no auth header)

    The submit is the trial. Polls, the result read and the download are lifecycle steps.

BODY PINS

    `ROUTE_PINS` says, per route key, which schema field gets which case value. A field that is
    not in the pinned schema's Input component is refused at build time, an enum value outside
    the schema's enum is refused, and every output-count field is pinned to 1. Nothing the
    caller passes reaches the body except the media inputs the route needs (URLs of accepted
    draws / reference assets / drive audio), and those only under their declared roles.

SIZE POLICY (recorded on every dry-run row; MD-C10 asks the Controller to confirm it)

    SIZE_A       long side 1024, exact aspect, multiples of 16, <= 1,048,576 px - keeps every
                 "first megapixel" / "1K" price basis (flux, qwen, recraft, gpt-image-2 medium
                 at 1024x1024 for 1:1).
    SIZE_SEEDREAM short side 1024 - the pinned schema requires >= 1024x1024 total pixels and the
                 pinned 0.0675 tier applies up to 1536x1536 total area.
"""
from __future__ import annotations

import re
from pathlib import Path

import hv2_paths
from providers import PreDispatchRefusal
from . import base as B

FAL_SCHEMAS = hv2_paths.SCHEMAS / "fal"

SIZE_A = {"1:1": (1024, 1024), "4:5": (816, 1024), "9:16": (720, 1280), "16:9": (1280, 720), "3:4": (768, 1024)}
SIZE_SEEDREAM = {"1:1": (1024, 1024), "4:5": (1024, 1280), "9:16": (1080, 1920), "16:9": (1920, 1080), "3:4": (1024, 1365)}

class Const:
    """A literal pinned value. Strings must be wrapped so a typo in a resolver name can never
    be sent to a provider as a literal field value."""
    __slots__ = ("value",)

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Const({self.value!r})"


K = Const

# source specs: Const(literal) / a non-str literal, or a string naming a resolver in _resolve()
ROUTE_PINS: dict[str, dict] = {
    "gpt-image-2":        {"prompt": "prompt", "image_size": "size_a", "quality": K("medium"), "num_images": 1},
    "seedream-5-pro":     {"prompt": "prompt", "image_size": "size_seedream", "num_images": 1},
    "flux-2-pro":         {"prompt": "prompt", "image_size": "size_a"},
    "qwen-image-3":       {"prompt": "prompt", "image_size": "size_a", "num_images": 1},
    "recraft-v4":         {"prompt": "prompt", "image_size": "size_a"},
    "flux-2-pro-edit":    {"prompt": "prompt", "image_urls": "in:image_urls"},
    "nano-banana-pro-edit": {"prompt": "prompt", "image_urls": "in:image_urls", "num_images": 1, "resolution": K("1K")},
    "seedream-5-pro-edit": {"prompt": "prompt", "image_urls": "in:image_urls", "num_images": 1, "image_size": K("auto_1K")},
    "gpt-image-2-edit":   {"prompt": "prompt", "image_urls": "in:image_urls", "quality": K("medium"), "num_images": 1},
    "kling-v3-pro-audio": {"prompt": "prompt", "aspect_ratio": "aspect", "duration": "duration_str", "generate_audio": "audio_bool"},
    "kling-v3-pro":       {"prompt": "prompt", "aspect_ratio": "aspect", "duration": "duration_str", "generate_audio": "audio_bool"},
    "kling-v3-pro-15s":   {"prompt": "prompt", "aspect_ratio": "aspect", "duration": "duration_str", "generate_audio": "audio_bool"},
    "kling-v3-pro-10s":   {"prompt": "prompt", "aspect_ratio": "aspect", "duration": "duration_str", "generate_audio": "audio_bool"},
    "kling-v3-pro-i2v":   {"prompt": "prompt", "start_image_url": "in:image_url", "duration": "duration_str", "generate_audio": "audio_bool"},
    "minimax-h3-max":     {"prompt": "prompt", "prompt_expansion_mode": K("balanced"), "aspect_ratio": "aspect", "resolution": K("768P"), "duration": "duration_int"},
    "minimax-h3-max-480p": {"prompt": "prompt", "prompt_expansion_mode": K("balanced"), "aspect_ratio": "aspect", "resolution": K("480P"), "duration": "duration_int"},
    "minimax-h3-max-i2v": {"prompt": "prompt", "prompt_expansion_mode": K("balanced"), "image_url": "in:image_url", "resolution": K("768P"), "duration": "duration_int"},
    "wan-3.0-prime":      {"prompt": "prompt", "aspect_ratio": "aspect", "resolution": K("720p"), "duration": "duration_int", "audio": "audio_bool"},
    "wan-3.0-prime-i2v":  {"prompt": "prompt", "start_image_url": "in:image_url", "resolution": K("720p"), "duration": "duration_int", "audio": "audio_bool"},
    "seedance-2.5":       {"prompt": "prompt", "aspect_ratio": "aspect", "duration": "duration_str", "resolution": K("720p"), "generate_audio": "audio_bool"},
    "seedance-2.5-15s":   {"prompt": "prompt", "aspect_ratio": "aspect", "duration": "duration_str", "resolution": K("720p"), "generate_audio": "audio_bool"},
    "seedance-2.5-i2v":   {"prompt": "prompt", "image_url": "in:image_url", "duration": "duration_str", "resolution": K("720p"), "generate_audio": "audio_bool"},
    "seedance-2.5-ref2v": {"prompt": "prompt", "image_urls": "in:image_urls", "aspect_ratio": "aspect", "duration": "duration_str", "resolution": K("720p"), "generate_audio": "audio_bool"},
    "elevenlabs-v3":      {"text": "script", "voice": "in:voice"},
    "sync-lipsync-v3":    {"video_url": "in:video_url", "audio_url": "in:audio_url"},
    "kling-lipsync-a2v":  {"video_url": "in:video_url", "audio_url": "in:audio_url"},
    "elevenlabs-music":   {"prompt": "prompt", "music_length_ms": "duration_ms"},
}

_SCHEMA_CACHE: dict[str, dict] = {}
FAL_QUEUE_HOST = "queue.fal.run"
FAL_DOWNLOAD_SUFFIXES = (".fal.media", ".fal.run")


_HTTPS_HOST = re.compile(r"^https://([A-Za-z0-9.-]+)(?::\d+)?(?:[/?#]|$)")


def trusted_fal_url(url, kind: str = "queue") -> bool:
    """AF-7: the key header is only ever sent to https://queue.fal.run; downloads only from fal's own hosts.
    (A regex host parser, so this module never imports a network library - transports.py is the only one.)"""
    m = _HTTPS_HOST.match(str(url))
    if not m:
        return False
    host = m.group(1).lower()
    if kind == "queue":
        return host == FAL_QUEUE_HOST
    return host == FAL_QUEUE_HOST or any(host.endswith(sfx) for sfx in FAL_DOWNLOAD_SUFFIXES)


def load_input_schema(entry) -> dict | None:
    """The Input component (properties + required) from the pinned fal OpenAPI bytes, or None."""
    if not entry.params_schema or "#" not in entry.params_schema or not entry.params_schema.startswith("eval/harness-v2/schemas/fal/"):
        return None
    rel, comp = entry.params_schema.split("#", 1)
    path = hv2_paths.REPO_ROOT / rel
    key = f"{path}#{comp}"
    if key not in _SCHEMA_CACHE:
        doc = B.load_json(path)
        models = doc.get("models") or []
        if not models:
            return None
        comps = ((models[0].get("openapi") or {}).get("components") or {}).get("schemas") or {}
        schema = comps.get(comp)
        if not schema:
            raise PreDispatchRefusal(f"pinned schema {path.name} has no component {comp}")
        _SCHEMA_CACHE[key] = schema
    return _SCHEMA_CACHE[key]


class FalQueueAdapter(B.RouteAdapter):
    family = "fal_queue"

    # -- body -------------------------------------------------------------------------------
    def _resolve(self, spec, case_row, inputs, notes):
        if isinstance(spec, Const):
            return spec.value
        if not isinstance(spec, str):
            return spec
        params = case_row.get("params") or {}
        if spec == "prompt":
            p = case_row.get("prompt")
            if not p or not str(p).strip():
                raise PreDispatchRefusal("a generation request needs a non-empty prompt (the blueprint's generation_prompt)")
            return p
        if spec == "script":
            s = params.get("script") or params.get("line") or case_row.get("prompt")
            if not s:
                raise PreDispatchRefusal("a TTS request needs the case script")
            return s
        if spec in ("size_a", "size_seedream"):
            a = B.aspect(case_row)
            table = SIZE_A if spec == "size_a" else SIZE_SEEDREAM
            if a is None:
                raise PreDispatchRefusal(f"no aspect ratio on the case row ({params.get('aspect')!r}); refusing to guess a size")
            if a not in table:
                raise PreDispatchRefusal(f"aspect {a} has no pinned size in policy {spec}")
            w, h = table[a]
            notes.append(f"size_policy={spec}: {a} -> {w}x{h}")
            return {"width": w, "height": h}
        if spec == "aspect":
            a = B.aspect(case_row)
            if a is None:
                raise PreDispatchRefusal(f"no aspect ratio on the case row ({params.get('aspect')!r})")
            return a
        if spec in ("duration_str", "duration_int"):
            d = B.duration_s(case_row)
            if d is None:
                raise PreDispatchRefusal(f"no integer duration_s on the case row ({params.get('duration_s')!r})")
            return str(d) if spec == "duration_str" else d
        if spec == "duration_ms":
            d = B.duration_s(case_row)
            if d is None:
                raise PreDispatchRefusal("no duration_s for the music length")
            return d * 1000
        if spec == "audio_bool":
            v = B.audio_flag(case_row)
            if v is None:
                notes.append("audio flag not applicable; schema default left in place")
            return v
        if spec.startswith("in:"):
            role = spec[3:]
            if role in inputs:
                return inputs[role]
            if role == "voice":
                notes.append("voice id chosen at dispatch and recorded (case params)")
                return B.pending_choice("voice_id")
            if role == "image_urls":
                n = params.get("refs") or 1
                try:
                    n = int(n)
                except (TypeError, ValueError):
                    n = 1
                return [B.pending_artifact(case_row, f"reference_asset_{i + 1}") for i in range(max(n, 1))]
            if role == "image_url":
                return B.pending_artifact(case_row, "plate_accepted_draw")
            if role == "video_url":
                return B.pending_artifact(case_row, "plate_clip")
            if role == "audio_url":
                return B.pending_artifact(case_row, "drive_audio")
            raise PreDispatchRefusal(f"unknown input role {role}")
        raise PreDispatchRefusal(f"unknown pin spec {spec!r}")

    def build_request(self, case_row: dict, inputs: dict | None = None) -> B.Request:
        entry = self.entry
        inputs = self._check_inputs(inputs)
        notes: list[str] = []
        if entry.shape_status != "verified" or entry.route_key not in ROUTE_PINS:
            body = {"$shape": "unverified", "$reason": entry.notes or "no pinned schema for this endpoint id"}
            return B.Request("POST", entry.endpoint, self._headers_template(), body, notes=["shape unverified: no fields rendered"])
        schema = load_input_schema(entry)
        if schema is None:
            raise PreDispatchRefusal(f"{entry.route_key}: pinned schema bytes carry no model; refusing to render a guessed body")
        props = schema.get("properties") or {}
        body: dict = {}
        for field_name, spec in ROUTE_PINS[entry.route_key].items():
            value = self._resolve(spec, case_row, inputs, notes)
            if value is None:
                continue
            body[field_name] = value
        # policy guards first (output count pinned to 1, seed only under `held`), then the schema
        self._guard_body(body, None, entry.route_key)
        # schema validation: field exists, enum respected, required present
        for k, v in body.items():
            if k not in props:
                raise PreDispatchRefusal(f"{entry.route_key}: field {k!r} is not in the pinned schema")
            enum = _enum_of(props[k])
            if enum and not isinstance(v, dict) and not isinstance(v, list) and v not in enum:
                raise PreDispatchRefusal(f"{entry.route_key}: {k}={v!r} is outside the pinned enum {enum}")
        missing = [r for r in (schema.get("required") or []) if r not in body]
        if missing:
            raise PreDispatchRefusal(f"{entry.route_key}: required schema fields {missing} are not pinned")
        self._guard_body(body, set(props), entry.route_key)
        rendered = len(body["text"]) if isinstance(body.get("text"), str) else None      # AF-9: the characters actually sent
        return B.Request("POST", entry.endpoint, self._headers_template(), body, notes=notes, rendered_chars=rendered)

    @staticmethod
    def _headers_template() -> dict:
        return {"Authorization": "Key <KEY:FAL_KEY>", "Content-Type": "application/json"}

    # -- credential ---------------------------------------------------------------------------
    def _credential(self) -> str:
        return self.key_loader.read("FAL_KEY")

    def _auth_headers(self, credential: str) -> dict:
        return {"Authorization": f"Key {credential}", "Content-Type": "application/json"}

    # -- lifecycle ----------------------------------------------------------------------------
    def _lifecycle(self, request: B.Request, headers: dict, attempt: dict) -> B.Outcome:
        counts: dict = {}
        r = self._submit(request.url, headers, request.body_bytes, attempt, counts)
        if isinstance(r, B.Outcome):
            return r
        status, reply = r
        reply = reply if isinstance(reply, dict) else {}
        if status != 200:
            detail = reply.get("detail") or B.error_of(reply).get("message") or reply
            refusal = status < 500 and "content" in str(detail).lower() and ("policy" in str(detail).lower() or "safety" in str(detail).lower())
            return B.http_status_outcome(status, reply, counts, refusal=refusal, note=str(detail))
        request_id, status_url, response_url = reply.get("request_id"), reply.get("status_url"), reply.get("response_url")
        if not (request_id and status_url and response_url):
            return B.Outcome("error", "malformed_response", "queue submit returned 200 without request_id/status_url/response_url; the job cannot be tracked",
                             ambiguous=True, outcome_resolved=False, lifecycle_counts=counts)
        attempt["provider_request_id"] = request_id
        if not (trusted_fal_url(status_url) and trusted_fal_url(response_url)):
            return B.Outcome("error", "untrusted_url", f"queue reply named a status/response URL off {FAL_QUEUE_HOST}; the key is never sent there; "
                             f"request {request_id} may still complete and bill", ambiguous=True, outcome_resolved=False,
                             lifecycle_counts=counts, provider_request_id=request_id)

        def check():
            code, st = self.transport.get_json(status_url, headers)
            if code != 200:
                return True, B.Outcome("error", f"poll_http_{code}", f"status poll answered {code} for {request_id}; final outcome unknown",
                                       ambiguous=True, outcome_resolved=False, lifecycle_counts=counts)
            s = (st or {}).get("status")
            if s == "COMPLETED":
                return True, st
            if s in ("IN_QUEUE", "IN_PROGRESS"):
                return False, st
            return True, B.Outcome("error", "malformed_response", f"undocumented queue status {s!r} for {request_id}",
                                   ambiguous=True, outcome_resolved=False, lifecycle_counts=counts)

        terminal = self._poll(check, attempt, counts, "fal queue")
        if isinstance(terminal, B.Outcome):
            return terminal
        attempt["completed_at"] = self._now()
        try:
            code, out = self.transport.get_json(response_url, headers)
        except Exception as exc:                     # noqa: BLE001
            api_status, error_class = B.classify_transport_failure(exc)
            return B.Outcome(api_status, f"result_{error_class}", f"result read failed after COMPLETED: {exc}",
                             ambiguous=True, outcome_resolved=False, lifecycle_counts=counts, provider_request_id=request_id)
        counts["result_reads"] = 1
        out = out if isinstance(out, dict) else {}
        if code != 200 or out.get("error") or out.get("detail"):
            detail = out.get("error") or out.get("detail") or out
            refusal = "content" in str(detail).lower() and ("policy" in str(detail).lower() or "safety" in str(detail).lower() or "nsfw" in str(detail).lower())
            return B.Outcome("refusal" if refusal else "error", "moderation_block" if refusal else (f"http_{code}" if code != 200 else "provider_error"),
                             str(detail)[:300], ambiguous=False, outcome_resolved=True, lifecycle_counts=counts, provider_request_id=request_id)
        url = _artifact_url(out)
        if not url:
            return B.Outcome("error", "no_artifact_returned", "COMPLETED result carried no media url", ambiguous=False,
                             outcome_resolved=True, lifecycle_counts=counts, provider_request_id=request_id)
        if not trusted_fal_url(url, kind="download"):
            return B.Outcome("error", "untrusted_url", f"artifact URL is not on a fal host; not fetched. URL recorded for a separately authorised fetch",
                             ambiguous=False, outcome_resolved=True, lifecycle_counts=counts, provider_request_id=request_id, provider_meta={"artifact_url": url})
        d = self._download(url, {}, counts)
        if isinstance(d, B.Outcome):
            d.provider_request_id = request_id
            return d
        data, ct = d
        return B.Outcome("ok", None, "", media=data, content_type=ct or _guess_ct(url), provider_request_id=request_id,
                         provider_meta={"request_id": request_id, "artifact_url": url, "content_type": ct}, lifecycle_counts=counts)


def _enum_of(prop: dict) -> list | None:
    if "enum" in prop:
        return prop["enum"]
    if "const" in prop:
        return [prop["const"]]
    for alt in prop.get("anyOf") or []:
        if "enum" in alt:
            return None            # anyOf with an object alternative: the string enum is not exhaustive
    return None


def _artifact_url(out: dict) -> str | None:
    for k in ("images",):
        v = out.get(k)
        if isinstance(v, list) and v and isinstance(v[0], dict) and v[0].get("url"):
            return v[0]["url"]
    for k in ("video", "audio", "image"):
        v = out.get(k)
        if isinstance(v, dict) and v.get("url"):
            return v["url"]
    return None


def _guess_ct(url: str) -> str | None:
    u = url.lower().split("?")[0]
    for ext, ct in ((".png", "image/png"), (".jpg", "image/jpeg"), (".jpeg", "image/jpeg"), (".webp", "image/webp"),
                    (".mp4", "video/mp4"), (".wav", "audio/wav"), (".mp3", "audio/mpeg")):
        if u.endswith(ext):
            return ct
    return None
