"""Gemini Omni Flash video on the Gemini Developer API (Interactions API), key NAMED GOOGLE_API_KEY.

Controller decision CONTROLLER-GEMINI-MODELS-VIA-GEMINI-KEY-2026-09-09: Gemini-named models run on
generativelanguage.googleapis.com with the key named GOOGLE_API_KEY (name only), billed to that key's GCP account
(pool `credits`, "GCP credits via the Gemini API key").

PINNED SOURCES (eval/empirical-planning/price-pins-2026-09/gemini-api/PIN-INDEX.yaml; schemas/gemini_api/SCHEMA-INDEX.yaml)
    the Gemini API guide "Generate and edit videos with Gemini Omni Flash", the model page (stable id
    gemini-omni-1.1-flash; "Output video 3s-10s (360p/720p/1080p/4K, 24 FPS)") and the Interactions API reference:

    POST https://generativelanguage.googleapis.com/v1beta/interactions          header x-goog-api-key: <value>
    body {"model": "gemini-omni-1.1-flash",
          "input": [{"type":"text","text": prompt}, {"type":"image","data":<b64>,"mime_type":...}],
          "response_format": {"type":"video","aspect_ratio":"9:16","resolution":"720p","duration":"6s"},
          "generation_config": {"video_config": {"task": "text_to_video"}}}
    -> {"id":"v1_...","status":"completed","steps":[..., {"type":"model_output","content":[{"type":"video","mime_type":"video/mp4","data":<b64>}]}]}

    VideoResponseFormat (reference): aspect_ratio 16:9 | 9:16; resolution 360p | 720p (default) | 1080p | 4k; delivery
    inline (default: "Video data is returned inline in the response") | uri; duration string "The duration for the
    video output" - the reference gives no format, so the value keeps the pinned Vertex form for the same model
    ("integers between 3 and 10, followed by 's'"), which the model page's 3s-10s range agrees with.
    Interaction status (reference): completed | failed | cancelled | incomplete | budget_exceeded | in_progress |
    queued | requires_action. The guide: "Omni applies content safety filters to both input prompts and generated
    video ... Prompts that violate usage policies are blocked" - no response shape is given for a block, so a
    non-completed interaction whose errors[] speak of safety / policy / blocked content is classified `refusal`
    (moderation_block) and every other non-completed status stays `error` interaction_<status>, as on Vertex.
    The guide's REST examples pass the key as `?key=`; this adapter never puts it in the URL (header only).
    One synchronous POST is the whole trial (no `background`, no `stream`, no `previous_interaction_id`).
"""
from __future__ import annotations

from providers import PreDispatchRefusal  # noqa: F401
from . import base as B
from .gemini_api_image import HEADERS_TEMPLATE, check_gemini_api_entry
from .vertex_omni import VertexOmniAdapter

BODY_FIELDS = {"model", "input", "response_format", "generation_config"}
SAFETY_WORDS = ("safety", "blocked", "block", "policy", "prohibited", "harmful", "unsafe", "violat")


class GeminiApiOmniAdapter(VertexOmniAdapter):
    family = "gemini_api_omni"

    def build_request(self, case_row: dict, inputs: dict | None = None) -> B.Request:
        e = self.entry
        check_gemini_api_entry(e)
        inputs = self._check_inputs(inputs)
        prompt, a, res, d, input_parts, notes = self._render_fields(case_row, inputs)
        body = {
            "model": e.surface_model_id,
            "input": input_parts,
            "response_format": {"type": "video", "aspect_ratio": a, "resolution": res, "duration": f"{d}s"},
            "generation_config": {"video_config": {"task": "image_to_video" if "image_bytes" in inputs else "text_to_video"}},
        }
        self._guard_body(body, BODY_FIELDS, e.route_key)
        notes.append("Gemini Developer API surface (Interactions API): key NAMED GOOGLE_API_KEY in the x-goog-api-key header; "
                     "GCP credits via the Gemini API key; inline video bytes back (delivery default)")
        return B.Request("POST", e.endpoint, dict(HEADERS_TEMPLATE), body, notes=notes)

    def _credential(self) -> str:
        check_gemini_api_entry(self.entry)
        return self.key_loader.read(self.entry.key_name)          # by NAME, at dispatch only

    def _credential_file_name(self) -> str:
        return self.entry.credential_file_name

    def _auth_headers(self, credential: str) -> dict:
        return {"x-goog-api-key": credential, "Content-Type": "application/json"}

    def _not_completed(self, reply: dict, counts: dict, iid) -> B.Outcome:
        errs = reply.get("errors")
        if not isinstance(errs, list):
            errs = [reply.get("error")] if reply.get("error") else []
        text = " ".join(str(x.get("message") or x.get("code") or x) if isinstance(x, dict) else str(x) for x in errs)
        if any(w in text.lower() for w in SAFETY_WORDS):
            return B.Outcome("refusal", "moderation_block", f"interaction {reply.get('status')}: {text}"[:300],
                             ambiguous=False, outcome_resolved=True, lifecycle_counts=counts, provider_request_id=iid)
        return super()._not_completed(reply, counts, iid)
