"""Veo 3.1 on Vertex AI (regional endpoint us-central1): t2v, i2v, ref2v and extend.

PINNED SOURCES (eval/harness-v2/schemas/vertex/SCHEMA-INDEX.yaml)

    submit    POST {regional}/models/<id>:predictLongRunning
              body {"instances":[{"prompt", ("image":{"bytesBase64Encoded","mimeType"}) |
                                  ("referenceImages":[{"image":{...},"referenceType":"asset"}]) |
                                  ("video":{"bytesBase64Encoded","mimeType"})}],
                    "parameters":{"sampleCount":1,"durationSeconds","aspectRatio","resolution","generateAudio"}}
              -> {"name": "projects/.../operations/<id>"}
    poll      POST {regional}/models/<id>:fetchPredictOperation  body {"operationName": <name>}
              -> {"name","done", "response":{"raiMediaFilteredCount","videos":[{"bytesBase64Encoded"|"gcsUri","mimeType"}]}}
    bytes     returned inline when no storageUri is given ("If not provided, video bytes are
              returned in the response" - pinned guide page)

    Field names: VideoGenerationModelParams (sampleCount, durationSeconds, aspectRatio,
    resolution, generateAudio, seed ...), VideoGenerationModelInstance (prompt, image, video,
    lastFrame, referenceImages[].referenceType), the t2v / i2v / references / extend guides.
    Extend: the input `video` instance is extended by a fixed 7 s (pinned extend page); the
    15-s item is 8-s generate + extend, two API calls inside ONE trial (reservation covers 15 s).

    `personGeneration` is not sent (vendor default), `seed` is never sent (SEED-POLICY unset).
"""
from __future__ import annotations

from providers import PreDispatchRefusal
from . import base as B

ALLOWED_DURATIONS = (4, 6, 8)          # pinned t2v guide: "Veo 3 models: 4, 6, or 8"
ALLOWED_ASPECTS = ("16:9", "9:16")
ALLOWED_RESOLUTIONS = ("720p", "1080p")
PARAM_FIELDS = {"sampleCount", "durationSeconds", "aspectRatio", "resolution", "generateAudio", "seed",
                "storageUri", "fps", "personGeneration", "negativePrompt", "enhancePrompt", "compressionQuality",
                "resizeMode", "task", "pubsubTopic", "enablePromptRewriting"}


class VertexVeoAdapter(B.RouteAdapter):
    family = "vertex_veo"

    def _params(self, case_row: dict, notes: list, with_duration: bool = True) -> dict:
        p: dict = {"sampleCount": 1}
        a = B.aspect(case_row)
        if a not in ALLOWED_ASPECTS:
            raise PreDispatchRefusal(f"aspect {a!r} is not in the pinned Veo enum {ALLOWED_ASPECTS}")
        p["aspectRatio"] = a
        res = str((case_row.get("params") or {}).get("resolution", "")).strip().lower()
        res = "720p" if res.startswith("720") else res
        if res not in ALLOWED_RESOLUTIONS:
            raise PreDispatchRefusal(f"resolution {res!r} is not in the pinned Veo enum {ALLOWED_RESOLUTIONS}")
        p["resolution"] = res
        if with_duration:
            d = B.duration_s(case_row)
            if d not in ALLOWED_DURATIONS:
                raise PreDispatchRefusal(f"duration_s {d!r} is not in the pinned Veo enum {ALLOWED_DURATIONS}")
            p["durationSeconds"] = d
        audio = B.audio_flag(case_row)
        if audio is not None:
            p["generateAudio"] = audio
        else:
            notes.append("audio flag not applicable; generateAudio left at the vendor default")
        return p

    def build_request(self, case_row: dict, inputs: dict | None = None) -> B.Request:
        e = self.entry
        inputs = self._check_inputs(inputs)
        notes: list[str] = []
        prompt = case_row.get("prompt")
        if not prompt or not str(prompt).strip():
            raise PreDispatchRefusal("a generation request needs a non-empty prompt")
        instance: dict = {"prompt": prompt}
        if e.workflow == "i2v":
            if "image_bytes" in inputs:
                instance["image"] = {"bytesBase64Encoded": B.b64(inputs["image_bytes"]), "mimeType": inputs.get("image_mime") or "image/png"}
            else:
                instance["image"] = B.pending_artifact(case_row, "plate_accepted_draw")
        elif e.workflow == "ref2v":
            refs = inputs.get("reference_images")
            n = int((case_row.get("params") or {}).get("refs") or 3)
            if refs:
                if len(refs) > 3:
                    raise PreDispatchRefusal("Veo accepts up to three asset reference images (pinned references page)")
                instance["referenceImages"] = [{"image": {"bytesBase64Encoded": B.b64(data), "mimeType": mime}, "referenceType": "asset"}
                                               for data, mime in refs]
            else:
                instance["referenceImages"] = [{"image": B.pending_artifact(case_row, f"reference_asset_{i + 1}"), "referenceType": "asset"}
                                               for i in range(min(n, 3))]
        followups = []
        if e.workflow == "extend":
            # call 1: 8-s generate; call 2: extend that video by the fixed 7 s (15 billed seconds)
            row8 = {**case_row, "params": {**(case_row.get("params") or {}), "duration_s": 8}}
            params = self._params(row8, notes)
            ext_params = {k: v for k, v in params.items() if k != "durationSeconds"}
            followups.append({"url": e.endpoint, "note": "extend: instances[0].video = call-1 output bytes (video/mp4); extended length is fixed at 7 s (pinned extend page)",
                              # `$from_call` is filled by THIS trial's lifecycle from call 1's sealed bytes; it is not a
                              # caller input, so has_pending() ignores it (PENDING_KEYS) and live dispatch proceeds.
                              "body": {"instances": [{"prompt": prompt, "video": {"$from_call": 1, "fields": "bytesBase64Encoded+mimeType (video/mp4)"}}], "parameters": ext_params}})
            notes.append("two API calls in one trial: 8 s + 7 s = 15 billed seconds")
        else:
            params = self._params(case_row, notes)
        body = {"instances": [instance], "parameters": params}
        self._guard_body(params, PARAM_FIELDS, e.route_key)
        headers = {"Authorization": "Bearer <TOKEN:gcloud-service-account>", "Content-Type": "application/json"}
        return B.Request("POST", e.endpoint, headers, body, followups=followups, notes=notes)

    # -- credential ---------------------------------------------------------------------------
    def _credential(self) -> str:
        if self.token_source is None:
            self.token_source = self._default_token_source()        # AF-8: MD-C3 resolver, live runner only
        return self.token_source.token()

    def _credential_file_name(self) -> str:
        return getattr(self.token_source, "credential_file_name", None) or self.entry.credential_file_name

    def _auth_headers(self, credential: str) -> dict:
        return {"Authorization": f"Bearer {credential}", "Content-Type": "application/json"}

    # -- lifecycle ----------------------------------------------------------------------------
    def _one_operation(self, url: str, headers: dict, payload: bytes, attempt: dict, counts: dict):
        """submit -> poll -> inline video bytes; returns (bytes, mime, name) or an Outcome."""
        r = self._submit(url, headers, payload, attempt, counts)
        if isinstance(r, B.Outcome):
            return r
        status, reply = r
        reply = reply if isinstance(reply, dict) else {}
        if status != 200:
            o = B.http_status_outcome(status, reply, counts, note=str(reply))
            err = B.error_of(reply)
            if not o.ambiguous and (err.get("status") or err.get("code")):
                o.error_class = str(err.get("status") or err.get("code"))
            return o
        name = reply.get("name")
        if not name:
            return B.Outcome("error", "malformed_response", "predictLongRunning returned 200 with no operation name",
                             ambiguous=True, outcome_resolved=False, lifecycle_counts=counts)
        attempt["provider_request_id"] = name
        poll_url = url.replace(":predictLongRunning", ":fetchPredictOperation")
        poll_payload = B.S.canonical_json({"operationName": name})

        def check():
            code, op = self.transport.post_json(poll_url, headers, poll_payload)
            if code != 200:
                return True, B.Outcome("error", f"poll_http_{code}", f"fetchPredictOperation answered {code} for {name}; final outcome unknown",
                                       ambiguous=True, outcome_resolved=False, lifecycle_counts=counts)
            if not isinstance(op, dict) or ("done" not in op and "name" not in op):
                return True, B.Outcome("error", "malformed_response", f"undocumented operation shape for {name}",
                                       ambiguous=True, outcome_resolved=False, lifecycle_counts=counts)
            return bool(op.get("done")), op

        op = self._poll(check, attempt, counts, "Veo operation")
        if isinstance(op, B.Outcome):
            return op
        if op.get("error"):
            err = B.error_of(op)
            return B.Outcome("error", str(err.get("status") or err.get("code") or "operation_error"), str(err)[:300],
                             ambiguous=False, outcome_resolved=True, lifecycle_counts=counts, provider_request_id=name)
        resp = op.get("response") or {}
        videos = resp.get("videos") or []
        if not videos:
            if resp.get("raiMediaFilteredCount"):
                return B.Outcome("refusal", "safety_filtered", str(resp.get("raiMediaFilteredReasons"))[:300],
                                 ambiguous=False, outcome_resolved=True, lifecycle_counts=counts, provider_request_id=name)
            return B.Outcome("error", "no_artifact_returned", "done operation carried no videos", ambiguous=False,
                             outcome_resolved=True, lifecycle_counts=counts, provider_request_id=name)
        v0 = videos[0]
        if v0.get("bytesBase64Encoded"):
            import base64
            try:
                data = base64.b64decode(v0["bytesBase64Encoded"])
            except Exception as exc:              # noqa: BLE001
                return B.Outcome("error", "malformed_response", f"video bytes were not valid base64: {exc}", ambiguous=False,
                                 outcome_resolved=True, lifecycle_counts=counts, provider_request_id=name)
            return data, (v0.get("mimeType") or "video/mp4"), name
        return B.Outcome("error", "artifact_not_inline", f"operation returned a gcsUri ({v0.get('gcsUri')}) instead of inline bytes; no storageUri was requested",
                         ambiguous=False, outcome_resolved=True, lifecycle_counts=counts, provider_request_id=name,
                         provider_meta={"gcsUri": v0.get("gcsUri")})

    def _lifecycle(self, request: B.Request, headers: dict, attempt: dict) -> B.Outcome:
        counts: dict = {}
        r = self._one_operation(request.url, headers, request.body_bytes, attempt, counts)
        if isinstance(r, B.Outcome):
            return r
        data, mime, name = r
        intermediates = []
        if request.followups:
            fu = request.followups[0]
            body = {"instances": [{"prompt": fu["body"]["instances"][0]["prompt"],
                                   "video": {"bytesBase64Encoded": B.b64(data), "mimeType": mime}}],
                    "parameters": fu["body"]["parameters"]}
            intermediates.append(("call1", data, mime))
            r2 = self._one_operation(fu["url"], headers, B.S.canonical_json(body), attempt, counts)
            if isinstance(r2, B.Outcome):
                r2.intermediates = intermediates
                r2.note = "extend call failed after the 8-s generate succeeded (call 1 sealed): " + r2.note
                return r2
            data, mime, name2 = r2
            name = f"{name} + {name2}"
        attempt["completed_at"] = self._now()
        return B.Outcome("ok", None, "", media=data, content_type=mime, provider_request_id=name,
                         provider_meta={"operation_name": name}, intermediates=intermediates, lifecycle_counts=counts)
