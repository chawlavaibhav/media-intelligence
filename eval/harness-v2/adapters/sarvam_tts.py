"""Sarvam bulbul v3 text-to-speech, direct REST.

PINNED SOURCE: docs.sarvam.ai "Text to Speech" REST reference (schemas/sarvam/SCHEMA-INDEX.yaml)

    POST https://api.sarvam.ai/text-to-speech      header api-subscription-key: $SARVAM_API_KEY
    body {"text", "language_code" (BCP-47, required), "speaker" (lowercase enum), "model": "bulbul:v3"}
    -> {"request_id", "audios": [<base64 WAV>]}

    bulbul:v3 does not support pitch / loudness; pace, temperature, sample rate are left at the
    vendor defaults so the route is measured as delivered. Synchronous: one POST is the trial.
    Sarvam bills in INR (Rs 3.00 per 1,000 characters); the ledger keeps INR and a USD-equivalent.
"""
from __future__ import annotations

from providers import PreDispatchRefusal
from . import base as B

LANGUAGE_CODE_BY_CASE_LANGUAGE = {"hi": "hi-IN", "hg": "hi-IN", "en": "en-IN"}


def language_code_for(case_lang) -> str | None:
    """BCP-47 for the case's COND-LANGUAGE.language: 'en' | 'hi' | 'hg' | 'hi-en (Hinglish)' (TEST-CASES wording).
    Hinglish is code-mixed Hindi and is sent as hi-IN (the pinned page lists hi-IN; bulbul reads Latin-script Hindi)."""
    if not isinstance(case_lang, str):
        return None
    key = case_lang.strip().lower()
    if key in LANGUAGE_CODE_BY_CASE_LANGUAGE:
        return LANGUAGE_CODE_BY_CASE_LANGUAGE[key]
    if key.startswith("hi") or "hinglish" in key:
        return "hi-IN"
    if key.startswith("en"):
        return "en-IN"
    return None
BODY_FIELDS = {"text", "language_code", "speaker", "model", "pace", "speech_sample_rate", "output_audio_codec",
               "temperature", "enable_preprocessing", "dict_id", "enable_cached_responses", "pitch", "loudness"}


class SarvamTTSAdapter(B.RouteAdapter):
    family = "sarvam_tts"

    def build_request(self, case_row: dict, inputs: dict | None = None) -> B.Request:
        e = self.entry
        inputs = self._check_inputs(inputs)
        notes: list[str] = []
        params = case_row.get("params") or {}
        text = params.get("script") or params.get("line") or case_row.get("prompt")
        if not text or not str(text).strip():
            raise PreDispatchRefusal("a TTS request needs the case script")
        if len(text) > 2500:
            raise PreDispatchRefusal("bulbul:v3 accepts at most 2500 characters (pinned page)")
        lang = inputs.get("language_code")
        if not lang:
            case_lang = ((case_row.get("conditions") or {}).get("COND-LANGUAGE") or {}).get("language") or case_row.get("language")
            lang = language_code_for(case_lang)
            if lang is None:
                raise PreDispatchRefusal(f"no BCP-47 language code for case language {case_lang!r}")
            notes.append(f"language_code {lang} from COND-LANGUAGE {case_lang} (Hinglish is code-mixed -> hi-IN)")
        speaker = inputs.get("voice") or B.pending_choice("speaker_id_lowercase")
        body = {"text": text, "language_code": lang, "speaker": speaker, "model": "bulbul:v3"}
        self._guard_body(body, BODY_FIELDS, e.route_key)
        headers = {"api-subscription-key": "<KEY:SARVAM_API_KEY>", "Content-Type": "application/json"}
        return B.Request("POST", e.endpoint, headers, body, notes=notes, rendered_chars=len(text))

    def _credential(self) -> str:
        return self.key_loader.read("SARVAM_API_KEY")

    def _auth_headers(self, credential: str) -> dict:
        return {"api-subscription-key": credential, "Content-Type": "application/json"}

    def _lifecycle(self, request: B.Request, headers: dict, attempt: dict) -> B.Outcome:
        counts: dict = {}
        r = self._submit(request.url, headers, request.body_bytes, attempt, counts)
        if isinstance(r, B.Outcome):
            return r
        status, reply = r
        reply = reply if isinstance(reply, dict) else {}
        attempt["completed_at"] = self._now()
        rid = reply.get("request_id")
        if status != 200:
            o = B.http_status_outcome(status, reply, counts, note=str(reply))
            o.provider_request_id = rid
            return o
        audios = reply.get("audios") or []
        if not audios or not audios[0]:
            return B.Outcome("error", "no_artifact_returned", "200 response carried no audio", ambiguous=False,
                             outcome_resolved=True, lifecycle_counts=counts, provider_request_id=rid)
        import base64
        try:
            data = base64.b64decode(audios[0])
        except Exception as exc:                  # noqa: BLE001
            return B.Outcome("error", "malformed_response", f"audio was not valid base64: {exc}", ambiguous=False,
                             outcome_resolved=True, lifecycle_counts=counts, provider_request_id=rid)
        return B.Outcome("ok", None, "", media=data, content_type="audio/wav", provider_request_id=rid,
                         provider_meta={"request_id": rid}, lifecycle_counts=counts)
