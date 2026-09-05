"""Gemini image models on Vertex AI (global endpoint): generate, and edit with inline references.

    POST https://aiplatform.googleapis.com/v1/projects/<p>/locations/global/publishers/google/models/<id>:generateContent
    body {"contents":[{"role":"user","parts":[{"text": prompt}, {"inlineData":{"mimeType","data"}}...]}],
          "generationConfig":{"responseModalities":["IMAGE"],"candidateCount":1,"imageConfig":{"aspectRatio"}}}
    -> candidates[0].content.parts[*].inlineData.{mimeType,data}

    Body shape: live-proven on the Gemini Developer API by eval/experiments/EVAL-038/tools/generate_media.py
    (responseModalities + imageConfig.aspectRatio, inline image bytes back); the same generationConfig
    keys and the `global` location are on the pinned Vertex "Generate images with Gemini" page.
    Synchronous: one POST is the whole trial.
"""
from __future__ import annotations

from providers import PreDispatchRefusal
from . import base as B

ALLOWED_ASPECTS = ("1:1", "4:5", "9:16", "16:9", "3:4", "4:3", "3:2", "2:3", "21:9", "5:4")
GEN_CONFIG_FIELDS = {"responseModalities", "candidateCount", "imageConfig", "seed", "temperature", "maxOutputTokens"}


class VertexGeminiImageAdapter(B.RouteAdapter):
    family = "vertex_gemini_image"

    def build_request(self, case_row: dict, inputs: dict | None = None) -> B.Request:
        e = self.entry
        inputs = self._check_inputs(inputs)
        notes: list[str] = []
        prompt = case_row.get("prompt")
        if not prompt or not str(prompt).strip():
            raise PreDispatchRefusal("a generation request needs a non-empty prompt")
        a = B.aspect(case_row)
        if a not in ALLOWED_ASPECTS:
            raise PreDispatchRefusal(f"aspect {a!r} is not an aspect this adapter pins")
        parts: list = [{"text": prompt}]
        refs = inputs.get("reference_images")
        if e.workflow == "edit" or refs:
            if refs:
                parts += [{"inlineData": {"mimeType": mime, "data": B.b64(data)}} for data, mime in refs]
            else:
                n = int((case_row.get("params") or {}).get("refs") or 1)
                parts += [{"inlineData": B.pending_artifact(case_row, f"reference_asset_{i + 1}")} for i in range(n)]
        gen = {"responseModalities": ["IMAGE"], "candidateCount": 1, "imageConfig": {"aspectRatio": a}}
        self._guard_body(gen, GEN_CONFIG_FIELDS, e.route_key)
        body = {"contents": [{"role": "user", "parts": parts}], "generationConfig": gen}
        headers = {"Authorization": "Bearer <TOKEN:gcloud-service-account>", "Content-Type": "application/json"}
        return B.Request("POST", e.endpoint, headers, body, notes=notes)

    def _credential(self) -> str:
        if self.token_source is None:
            raise PreDispatchRefusal("no token source injected for Vertex; nothing was sent")
        return self.token_source.token()

    def _credential_file_name(self) -> str:
        return getattr(self.token_source, "credential_file_name", None) or self.entry.credential_file_name

    def _auth_headers(self, credential: str) -> dict:
        return {"Authorization": f"Bearer {credential}", "Content-Type": "application/json"}

    def _lifecycle(self, request: B.Request, headers: dict, attempt: dict) -> B.Outcome:
        counts: dict = {}
        r = self._submit(request.url, headers, request.body_bytes, attempt, counts)
        if isinstance(r, B.Outcome):
            return r
        status, reply = r
        reply = reply if isinstance(reply, dict) else {}
        attempt["completed_at"] = self._now()
        rid = reply.get("responseId")
        if status != 200:
            err = reply.get("error") or {}
            return B.Outcome("error", str(err.get("status") or err.get("code") or f"http_{status}"), str(reply)[:300],
                             ambiguous=False, outcome_resolved=True, lifecycle_counts=counts, provider_request_id=rid)
        cands = reply.get("candidates") or []
        if not cands:
            return B.Outcome("refusal", "moderation_block", str(reply.get("promptFeedback", ""))[:300],
                             ambiguous=False, outcome_resolved=True, lifecycle_counts=counts, provider_request_id=rid)
        c0 = cands[0]
        if c0.get("finishReason") in ("SAFETY", "BLOCKLIST", "PROHIBITED_CONTENT", "IMAGE_SAFETY"):
            return B.Outcome("refusal", "moderation_block", str(c0.get("finishReason")), ambiguous=False,
                             outcome_resolved=True, lifecycle_counts=counts, provider_request_id=rid)
        for part in (c0.get("content") or {}).get("parts") or []:
            blob = part.get("inlineData") or part.get("inline_data")
            if blob and blob.get("data"):
                import base64
                try:
                    data = base64.b64decode(blob["data"])
                except Exception as exc:          # noqa: BLE001
                    return B.Outcome("error", "malformed_response", f"image bytes were not valid base64: {exc}", ambiguous=False,
                                     outcome_resolved=True, lifecycle_counts=counts, provider_request_id=rid)
                mime = blob.get("mimeType") or blob.get("mime_type") or "image/png"
                return B.Outcome("ok", None, "", media=data, content_type=mime, provider_request_id=rid,
                                 provider_meta={"responseId": rid, "modelVersion": reply.get("modelVersion"), "usage": reply.get("usageMetadata")},
                                 lifecycle_counts=counts)
        return B.Outcome("error", "no_artifact_returned", f"200 response carried no inline image (finishReason={c0.get('finishReason')})",
                         ambiguous=False, outcome_resolved=True, lifecycle_counts=counts, provider_request_id=rid)
