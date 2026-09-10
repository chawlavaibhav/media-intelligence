"""Gemini image models (Nano Banana 2 / Nano Banana Pro) on the Gemini Developer API, key NAMED GOOGLE_API_KEY.

Controller decision CONTROLLER-GEMINI-MODELS-VIA-GEMINI-KEY-2026-09-09: every Gemini-named model is called on
generativelanguage.googleapis.com with the key named GOOGLE_API_KEY in ~/.mi-keys (name only; the value never enters a
body, log, record or exception), billed to that key's GCP account (pool `credits`, "GCP credits via the Gemini API key").

    POST https://generativelanguage.googleapis.com/v1beta/models/<id>:generateContent      header x-goog-api-key: <value>
    body {"contents":[{"role":"user","parts":[{"text": prompt}, {"inlineData":{"mimeType","data"}}...]}],
          "generationConfig":{"responseModalities":["IMAGE"],"candidateCount":1,"imageConfig":{"aspectRatio"}}}
    -> candidates[0].content.parts[*].inlineData.{mimeType,data}; a blocked prompt returns no candidates
       (promptFeedback.blockReason) or finishReason IMAGE_SAFETY / SAFETY / PROHIBITED_CONTENT / BLOCKLIST.

PINNED SOURCES (eval/empirical-planning/price-pins-2026-09/gemini-api/PIN-INDEX.yaml; schemas/gemini_api/SCHEMA-INDEX.yaml)
    - the Gemini API generateContent reference: GenerationConfig.responseModalities, .candidateCount,
      .imageConfig{aspectRatio, imageSize (default 1K)}; FinishReason IMAGE_SAFETY "Candidates blocked due to unsafe
      image generation content"; PromptFeedback.blockReason.
    - the Gemini API image-generation guide: model ids gemini-3.1-flash-image / gemini-3-pro-image, header
      `x-goog-api-key`, "Gemini 3 image models generate 1K images by default" (so no imageSize is sent: the 1K price
      line is the one pinned), inline reference images for editing.
    - live-proven on THIS surface by eval/experiments/EVAL-038/tools/generate_media.py (2026-09-01).
    The guide's own examples use the newer Interactions API (`POST /v1beta/interactions`); this adapter keeps the
    generateContent form because the reference still documents every field it sends and the bytes are live-proven.

The body is the Vertex body byte for byte (VertexGeminiImageAdapter._build_body): the same model takes the same
request on both surfaces; only the URL and the credential differ. Synchronous: one POST is the whole trial.
"""
from __future__ import annotations

from providers import PreDispatchRefusal
from . import base as B
from .vertex_gemini_image import VertexGeminiImageAdapter

KEY_NAME = "GOOGLE_API_KEY"
HOST = "generativelanguage.googleapis.com"
HEADERS_TEMPLATE = {"x-goog-api-key": f"<KEY:{KEY_NAME}>", "Content-Type": "application/json"}


def check_gemini_api_entry(entry) -> None:
    """The registry entry must name the Gemini API key and a generativelanguage URL; a key can never go elsewhere.
    (A plain string check on purpose: adapters import no URL / network module - transports.py is the only one that may.)"""
    if entry.key_name != KEY_NAME:
        raise PreDispatchRefusal(f"{entry.route_key}: a gemini_api adapter reads only the key named {KEY_NAME}, "
                                 f"not {entry.key_name!r}; nothing was sent")
    url = str(entry.endpoint)
    if not url.startswith(f"https://{HOST}/"):
        raise PreDispatchRefusal(f"{entry.route_key}: endpoint {url!r} is not https://{HOST}/...; the Gemini API key "
                                 f"is sent to that host only; nothing was sent")
    if "?" in url or "#" in url or "@" in url:
        raise PreDispatchRefusal(f"{entry.route_key}: endpoint carries a query, fragment or userinfo; the key travels in the header, never the URL")


class GeminiApiImageAdapter(VertexGeminiImageAdapter):
    family = "gemini_api_image"

    def build_request(self, case_row: dict, inputs: dict | None = None) -> B.Request:
        check_gemini_api_entry(self.entry)
        body, notes = self._build_body(case_row, inputs)
        notes.append("Gemini Developer API surface: key NAMED GOOGLE_API_KEY in the x-goog-api-key header; GCP credits via the Gemini API key")
        return B.Request("POST", self.entry.endpoint, dict(HEADERS_TEMPLATE), body, notes=notes)

    def _credential(self) -> str:
        check_gemini_api_entry(self.entry)
        return self.key_loader.read(self.entry.key_name)          # by NAME, at dispatch only

    def _credential_file_name(self) -> str:
        return self.entry.credential_file_name

    def _auth_headers(self, credential: str) -> dict:
        return {"x-goog-api-key": credential, "Content-Type": "application/json"}
