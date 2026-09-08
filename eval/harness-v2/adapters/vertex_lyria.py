"""Lyria 2 (lyria-002) on Vertex AI, regional endpoint us-central1.

PINNED SOURCE: the Vertex "Lyria music generation" reference page (schemas/vertex/SCHEMA-INDEX.yaml)

    POST {regional}/models/lyria-002:predict
    body {"instances":[{"prompt": <en-US text>, ("negative_prompt")}], "parameters":{"sample_count": 1}}
    -> {"predictions":[{"audioContent": <base64 WAV, 30 s, 48 kHz>, "mimeType": "audio/wav"}]}

    `seed` "cannot be used with sample_count" and SEED-POLICY says unset, so it is never sent.
    Synchronous: one POST is the whole trial.
"""
from __future__ import annotations

from providers import PreDispatchRefusal
from . import base as B


class VertexLyriaAdapter(B.RouteAdapter):
    family = "vertex_lyria"

    def build_request(self, case_row: dict, inputs: dict | None = None) -> B.Request:
        e = self.entry
        self._check_inputs(inputs)
        prompt = case_row.get("prompt")
        if not prompt or not str(prompt).strip():
            raise PreDispatchRefusal("a music request needs a non-empty prompt")
        params = {"sample_count": 1}
        self._guard_body(params, {"sample_count"}, e.route_key)
        body = {"instances": [{"prompt": prompt}], "parameters": params}
        headers = {"Authorization": "Bearer <TOKEN:gcloud-service-account>", "Content-Type": "application/json"}
        return B.Request("POST", e.endpoint, headers, body, notes=["one 30-s clip per call (pinned page)"])

    def _credential(self) -> str:
        if self.token_source is None:
            self.token_source = self._default_token_source()        # AF-8: MD-C3 resolver, live runner only
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
        if status != 200:
            o = B.http_status_outcome(status, reply, counts, note=str(reply))
            err = B.error_of(reply)
            if not o.ambiguous and (err.get("status") or err.get("code")):
                o.error_class = str(err.get("status") or err.get("code"))
            return o
        preds = reply.get("predictions") or []
        if not preds or not preds[0].get("audioContent"):
            return B.Outcome("error", "no_artifact_returned", "predict returned no audioContent", ambiguous=False,
                             outcome_resolved=True, lifecycle_counts=counts)
        import base64
        try:
            data = base64.b64decode(preds[0]["audioContent"])
        except Exception as exc:                  # noqa: BLE001
            return B.Outcome("error", "malformed_response", f"audioContent was not valid base64: {exc}", ambiguous=False,
                             outcome_resolved=True, lifecycle_counts=counts)
        return B.Outcome("ok", None, "", media=data, content_type=preds[0].get("mimeType") or "audio/wav",
                         provider_meta={"deployedModelId": reply.get("deployedModelId"), "model": reply.get("model")},
                         lifecycle_counts=counts)
