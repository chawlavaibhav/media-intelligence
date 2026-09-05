"""Gemini Omni Flash 1.1 video on Vertex AI: the Interactions API on the global endpoint.

PINNED SOURCE (the Vertex "Generate videos from text prompts" guide, section "Generate videos
using Gemini Omni Flash", and the Interactions API reference; see schemas/vertex/SCHEMA-INDEX.yaml)

    POST https://aiplatform.googleapis.com/v1beta1/projects/<p>/locations/global/interactions
    body {"model": "gemini-omni-1.1-flash-preview",
          "input": [{"type":"text","text": prompt}],
          "response_format": [{"type":"video","aspect_ratio":"9:16","resolution":"720p","duration":"6s"}],
          "generation_config": {"video_config": {"task": "text_to_video"}}}
    -> interaction {"status":"completed", "steps":[..., {"type":"model_output","content":[{"type":"video","data":<b64>,"mime_type":"video/mp4"}]}]}

    "CLOUD_STORAGE_OUTPUT_URI: Optional ... If not provided, video bytes are returned in the
    response" - so no `delivery`/`gcs_uri` is sent and the bytes come back inline.
    DURATION: "integers between 3 and 10, followed by 's'". A case row that asks for more than
    10 s cannot be rendered on this surface; the dry run says so instead of guessing.
    Synchronous request (the guide's non-background form): one POST is the whole trial.
"""
from __future__ import annotations

from providers import PreDispatchRefusal
from . import base as B

ALLOWED_ASPECTS = ("16:9", "9:16")
ALLOWED_RESOLUTIONS = ("360p", "720p", "1080p", "4k")
MAX_DURATION_S = 10
MIN_DURATION_S = 3


class VertexOmniAdapter(B.RouteAdapter):
    family = "vertex_omni"

    def build_request(self, case_row: dict, inputs: dict | None = None) -> B.Request:
        e = self.entry
        inputs = self._check_inputs(inputs)
        notes: list[str] = []
        prompt = case_row.get("prompt")
        if not prompt or not str(prompt).strip():
            raise PreDispatchRefusal("a generation request needs a non-empty prompt")
        a = B.aspect(case_row)
        if a not in ALLOWED_ASPECTS:
            raise PreDispatchRefusal(f"aspect {a!r} is not in the pinned Omni enum {ALLOWED_ASPECTS}")
        res = str((case_row.get("params") or {}).get("resolution", "")).strip().lower()
        res = "720p" if res.startswith("720") else res
        if res not in ALLOWED_RESOLUTIONS:
            raise PreDispatchRefusal(f"resolution {res!r} is not in the pinned Omni enum {ALLOWED_RESOLUTIONS}")
        d = B.duration_s(case_row)
        if d is None:
            raw = (case_row.get("params") or {}).get("duration_s")
            d = MAX_DURATION_S
            notes.append(f"duration_s was {raw!r}; rendered at the pinned page maximum {MAX_DURATION_S}s")
        if not (MIN_DURATION_S <= d <= MAX_DURATION_S):
            raise PreDispatchRefusal(f"duration {d}s is outside the pinned Omni range {MIN_DURATION_S}-{MAX_DURATION_S}s")
        input_parts: list = [{"type": "text", "text": prompt}]
        if "image_bytes" in inputs:
            input_parts.append({"type": "image", "data": B.b64(inputs["image_bytes"]), "mime_type": inputs.get("image_mime") or "image/png"})
        body = {
            "model": e.surface_model_id,
            "input": input_parts,
            "response_format": [{"type": "video", "aspect_ratio": a, "resolution": res, "duration": f"{d}s"}],
            "generation_config": {"video_config": {"task": "image_to_video" if "image_bytes" in inputs else "text_to_video"}},
        }
        self._guard_body(body, {"model", "input", "response_format", "generation_config"}, e.route_key)
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
        iid = reply.get("id")
        if status != 200:
            err = reply.get("error") or {}
            return B.Outcome("error", str(err.get("status") or err.get("code") or f"http_{status}"), str(reply)[:300],
                             ambiguous=False, outcome_resolved=True, lifecycle_counts=counts, provider_request_id=iid)
        if reply.get("status") not in ("completed", None):
            return B.Outcome("error", f"interaction_{reply.get('status')}", str(reply.get("error") or reply.get("status"))[:300],
                             ambiguous=False, outcome_resolved=True, lifecycle_counts=counts, provider_request_id=iid)
        for step in reply.get("steps") or []:
            if step.get("type") != "model_output":
                continue
            for c in step.get("content") or []:
                if c.get("type") == "video":
                    if c.get("data"):
                        import base64
                        try:
                            data = base64.b64decode(c["data"])
                        except Exception as exc:  # noqa: BLE001
                            return B.Outcome("error", "malformed_response", f"video bytes were not valid base64: {exc}", ambiguous=False,
                                             outcome_resolved=True, lifecycle_counts=counts, provider_request_id=iid)
                        return B.Outcome("ok", None, "", media=data, content_type=c.get("mime_type") or "video/mp4",
                                         provider_request_id=iid, provider_meta={"interaction_id": iid, "usage": reply.get("usage")},
                                         lifecycle_counts=counts)
                    if c.get("uri"):
                        return B.Outcome("error", "artifact_not_inline", f"interaction returned a uri ({c['uri']}) instead of inline bytes",
                                         ambiguous=False, outcome_resolved=True, lifecycle_counts=counts, provider_request_id=iid)
        return B.Outcome("error", "no_artifact_returned", "completed interaction carried no video content", ambiguous=False,
                         outcome_resolved=True, lifecycle_counts=counts, provider_request_id=iid)
