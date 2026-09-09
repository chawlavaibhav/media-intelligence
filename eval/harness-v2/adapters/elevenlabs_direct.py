"""ElevenLabs, DIRECT REST on the user's own account (plan credits, not cash). Modelled on sarvam_tts.py.

PINNED SOURCES: schemas/elevenlabs/SCHEMA-INDEX.yaml (extracts) over the raw pages under
eval/empirical-planning/price-pins-2026-09/elevenlabs-direct/ (PIN-INDEX.yaml: url, fetch time, sha256).

    tts    POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128
           header xi-api-key: $ELEVENLABS_API_KEY
           body {"text" (Required), "model_id": "eleven_v3"}      -> raw mp3 bytes ("The generated audio file")
           The convert page's default model_id is eleven_multilingual_v2 and it does not name the v3 id; the pinned
           models page does ("eleven_v3 5,000 ~5 minutes"), so eleven_v3 is sent explicitly and 5,000 is the limit.
           language_code / voice_settings / seed / ... are pinned fields the adapter does NOT send: the route is
           measured as delivered with the voice's stored settings.
    music  POST https://api.elevenlabs.io/v1/music?output_format=mp3_44100_128      ("Compose music")
           body {"prompt" (<=4100 chars), "music_length_ms" (3000-600000), "model_id": "music_v1"}
           -> raw mp3 bytes; response header song-id is the provider's id.

Both are synchronous: one POST is the trial (0 retries, no poll). The answer is BYTES, not JSON, so the submit goes
through transports.post_bytes (the fourth verb); an error status carries a JSON body {"detail": {"status", "message"}}
which is parsed for the note only. Billing: ElevenLabs draws plan credits ("Text to Speech 1 credit per character";
"Eleven Music 900 credits per minute"); pricing.py prices this pool at 0 USD cash and records the credits natively,
and ledger.py caps them by `elevenlabs_cap_credits` (missing = 0 = forbidden).
"""
from __future__ import annotations

import json
import re

from providers import PreDispatchRefusal
from . import base as B

KEY_NAME = "ELEVENLABS_API_KEY"
OUTPUT_FORMAT = "mp3_44100_128"           # the pinned default of the convert page, sent explicitly so the artifact type is known
TTS_MODEL_ID = "eleven_v3"                # pinned models page
TTS_CHAR_LIMIT = 5000                     # pinned models page: "eleven_v3 5,000"
MUSIC_MODEL_ID = "music_v1"               # pinned compose page default, sent explicitly so the measured model is recorded
MUSIC_PROMPT_MAX_CHARS = 4100             # pinned compose page: "<=4100 characters"
MUSIC_LENGTH_MS_RANGE = (3000, 600000)    # pinned compose page: "3000-600000"

TTS_BODY_FIELDS = {"text", "model_id", "language_code", "voice_settings", "pronunciation_dictionary_locators", "seed",
                   "previous_text", "next_text", "previous_request_ids", "next_request_ids", "apply_text_normalization",
                   "apply_language_text_normalization", "use_pvc_as_ivc"}
MUSIC_BODY_FIELDS = {"prompt", "composition_plan", "music_length_ms", "model_id", "seed", "force_instrumental", "finetune_id",
                     "respect_sections_durations", "store_for_inpainting", "sign_with_c2pa"}
# A 4xx whose detail names one of these is the provider declining the CONTENT (a refusal), not a malformed request.
REFUSAL_MARKERS = ("moderation", "unsafe", "blocked", "policy", "prohibited", "not_allowed", "flagged")
VOICE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{1,64}$")


def error_detail(data) -> dict:
    """ElevenLabs error bodies are JSON {"detail": {"status": ..., "message": ...}} or {"detail": "..."}; never assume."""
    try:
        reply = json.loads(bytes(data).decode("utf-8")) if data else {}
    except (UnicodeDecodeError, ValueError, TypeError):
        return {"status": None, "message": f"non-JSON error body ({len(data) if data else 0} bytes)"}
    det = reply.get("detail") if isinstance(reply, dict) else None
    if isinstance(det, dict):
        return {"status": det.get("status"), "message": det.get("message")}
    if det:
        return {"status": None, "message": str(det)}
    if isinstance(reply, dict) and reply:
        return {"status": None, "message": str(reply)[:200]}
    return {"status": None, "message": ""}


def looks_like_mp3(data: bytes) -> bool:
    return len(data) >= 4 and (data[:3] == b"ID3" or (data[0] == 0xFF and (data[1] & 0xE0) == 0xE0))


class ElevenLabsDirectAdapter(B.RouteAdapter):
    family = "elevenlabs_direct"

    # -- build --------------------------------------------------------------------------------
    def build_request(self, case_row: dict, inputs: dict | None = None) -> B.Request:
        inputs = self._check_inputs(inputs)
        wf = self.entry.workflow
        if wf == "tts":
            return self._build_tts(case_row, inputs)
        if wf == "music":
            return self._build_music(case_row, inputs)
        raise PreDispatchRefusal(f"{self.entry.route_key}: workflow {wf!r} is not one this adapter builds (tts | music)")

    def _build_tts(self, case_row: dict, inputs: dict) -> B.Request:
        e = self.entry
        params = case_row.get("params") or {}
        text = params.get("script") or params.get("line") or case_row.get("prompt")
        if not text or not str(text).strip():
            raise PreDispatchRefusal("a TTS request needs the case script")
        if len(text) > TTS_CHAR_LIMIT:
            raise PreDispatchRefusal(f"{TTS_MODEL_ID} accepts at most {TTS_CHAR_LIMIT} characters (pinned models page)")
        voice = inputs.get("voice")
        if not voice:
            # The voice is a PATH parameter, so it cannot carry a placeholder inside the body the way Sarvam's speaker does;
            # the dry-run row reads `input_unresolved:voice` and live dispatch refuses until the resolver hands one over.
            raise PreDispatchRefusal("input_unresolved:voice - the ElevenLabs voice_id path parameter must be supplied as the "
                                     "`voice` input (chosen and recorded at dispatch); nothing was sent")
        if not VOICE_ID_RE.fullmatch(str(voice)):
            raise PreDispatchRefusal(f"voice_id {voice!r} is not a plain identifier; refusing to put it in a URL path")
        body = {"text": text, "model_id": TTS_MODEL_ID}
        self._guard_body(body, TTS_BODY_FIELDS, e.route_key)
        headers = {"xi-api-key": f"<KEY:{KEY_NAME}>", "Content-Type": "application/json"}
        url = f"{e.endpoint}/{voice}?output_format={OUTPUT_FORMAT}"
        notes = [f"model_id {TTS_MODEL_ID} from the pinned models page (the convert page's default is eleven_multilingual_v2)",
                 f"output_format {OUTPUT_FORMAT} (pinned default) sent explicitly; voice settings left as stored on the voice"]
        return B.Request("POST", url, headers, body, notes=notes, rendered_chars=len(text))

    def _build_music(self, case_row: dict, inputs: dict) -> B.Request:
        e = self.entry
        params = case_row.get("params") or {}
        prompt = params.get("prompt") or case_row.get("prompt")
        if not prompt or not str(prompt).strip():
            raise PreDispatchRefusal("a music request needs the case prompt")
        if len(prompt) > MUSIC_PROMPT_MAX_CHARS:
            raise PreDispatchRefusal(f"the compose endpoint accepts a prompt of at most {MUSIC_PROMPT_MAX_CHARS} characters (pinned page)")
        secs = B.duration_s(case_row)
        if secs is None:
            raise PreDispatchRefusal("a music request needs params.duration_s (the clip length the row bills)")
        ms = int(secs) * 1000
        lo, hi = MUSIC_LENGTH_MS_RANGE
        if not lo <= ms <= hi:
            raise PreDispatchRefusal(f"music_length_ms {ms} is outside the pinned range {lo}-{hi}")
        body = {"prompt": prompt, "music_length_ms": ms, "model_id": MUSIC_MODEL_ID}
        self._guard_body(body, MUSIC_BODY_FIELDS, e.route_key)
        headers = {"xi-api-key": f"<KEY:{KEY_NAME}>", "Content-Type": "application/json"}
        url = f"{e.endpoint}?output_format={OUTPUT_FORMAT}"
        notes = [f"model_id {MUSIC_MODEL_ID} (pinned default) sent explicitly; output_format {OUTPUT_FORMAT} is what 'auto' resolves to for v1 models",
                 f"music_length_ms {ms} from params.duration_s {secs}"]
        return B.Request("POST", url, headers, body, notes=notes)

    # -- credential ---------------------------------------------------------------------------
    def _credential(self) -> str:
        return self.key_loader.read(KEY_NAME)

    def _auth_headers(self, credential: str) -> dict:
        return {"xi-api-key": credential, "Content-Type": "application/json"}

    # -- lifecycle: one POST, bytes back ------------------------------------------------------
    def _lifecycle(self, request: B.Request, headers: dict, attempt: dict) -> B.Outcome:
        counts: dict = {}
        r = self._submit(request.url, headers, request.body_bytes, attempt, counts, raw=True)
        if isinstance(r, B.Outcome):
            return r
        attempt["completed_at"] = self._now()
        try:
            status, data, content_type, resp_headers = r
        except (TypeError, ValueError):
            return B.Outcome("error", "malformed_response", "transport answered an unexpected shape for a bytes POST",
                             ambiguous=True, outcome_resolved=False, lifecycle_counts=counts)
        resp_headers = {str(k).lower(): v for k, v in (resp_headers or {}).items()} if isinstance(resp_headers, dict) else {}
        rid = resp_headers.get("song-id") or resp_headers.get("request-id") or resp_headers.get("x-request-id")
        meta = {k: resp_headers[k] for k in ("song-id", "request-id", "x-request-id") if k in resp_headers}
        if status != 200:
            det = error_detail(data)
            blob = f"{det.get('status') or ''} {det.get('message') or ''}".strip()
            refusal = 400 <= status < 500 and status != 429 and any(m in blob.lower() for m in REFUSAL_MARKERS)
            o = B.http_status_outcome(status, {}, counts, refusal=refusal, note=f"{status}: {blob}"[:300])
            o.provider_request_id = rid
            o.provider_meta = {**meta, "detail_status": det.get("status")}
            return o
        if not data:
            return B.Outcome("error", "no_artifact_returned", "200 response carried no audio bytes", ambiguous=False,
                             outcome_resolved=True, lifecycle_counts=counts, provider_request_id=rid, provider_meta=meta)
        data = bytes(data)
        ct = (content_type or "").split(";")[0].strip().lower()
        if ct.startswith("application/json") or ct.startswith("text/") or (not ct and data[:1] in (b"{", b"[")):
            return B.Outcome("error", "malformed_response", f"200 response was {ct or 'text'} instead of audio: {data[:120]!r}",
                             ambiguous=False, outcome_resolved=True, lifecycle_counts=counts, provider_request_id=rid, provider_meta=meta)
        if ct and not ct.startswith("audio/"):
            return B.Outcome("error", "malformed_response", f"200 response content type {ct!r} is not audio", ambiguous=False,
                             outcome_resolved=True, lifecycle_counts=counts, provider_request_id=rid, provider_meta=meta)
        if not ct and not looks_like_mp3(data):
            return B.Outcome("error", "malformed_response", "200 response without a content type does not look like mp3", ambiguous=False,
                             outcome_resolved=True, lifecycle_counts=counts, provider_request_id=rid, provider_meta=meta)
        return B.Outcome("ok", None, "", media=data, content_type=ct or "audio/mpeg", provider_request_id=rid,
                         provider_meta={**meta, "request_id": rid, "output_format": OUTPUT_FORMAT}, lifecycle_counts=counts)
