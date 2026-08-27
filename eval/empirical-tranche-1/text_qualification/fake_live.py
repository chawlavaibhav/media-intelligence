#!/usr/bin/env python3
"""Fake-live transports: everything a provider call does, except the socket.

WHY THIS EXISTS

    EVAL-012 proved the refusal path exhaustively and never proved the inverse, because there was
    no way to exercise a real judge without paying a provider. That gap is what let a whole live
    orchestration go missing behind a passing test suite.

    A `FakeJudgeHttp` stands exactly where the HTTP call would be. It receives the real request
    built by the real judge — real prompt, real base64 image, real provider-specific headers — and
    it answers the way a perfect judge would: by looking at the picture.

    It "looks at the picture" by hashing the decoded image bytes and reading the string that was
    rendered into them from an index built off the real packs. That is deliberately the ONLY thing
    it does differently from a model. Everything upstream of the socket is the production path:
    request building, blinding, base64, auth headers, transport, response parsing, scoring.

    So a test using it fails if the live branch refuses, if blinding breaks, if the wrong auth
    header is sent, if the response parser mis-maps a refusal, or if the scorer stops comparing in
    code. That is what makes it a positive control rather than a mock of our own beliefs.

WHAT IT IS NOT

    It is not evidence about any model. A perfect reader is not a real one, and this file makes no
    claim about how any provider behaves. Its results are labelled `fake_live` and can no more
    populate the Registry than a dry run can.
"""
from __future__ import annotations

import base64
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Base64 payloads are large; find them without dragging the whole body through a JSON parse.
_B64_IMAGE = re.compile(r'"(?:image_url|data)"\s*:\s*"(?:data:image/png;base64,)?([A-Za-z0-9+/=]{64,})"')


def _hash(image_bytes: bytes) -> str:
    return hashlib.sha256(image_bytes).hexdigest()


def image_index_for(script: str) -> dict[str, str]:
    """Map sha256(image bytes) -> the string actually RENDERED into that image.

    This is the fake judge's eyes. It is built from the same rendered files the resolver sends, so
    a perfect reader and the index agree by construction.
    """
    import qualify_text as Q

    scripts = ("devanagari", "latin") if script == "both" else (script,)
    index: dict[str, str] = {}
    resolver = Q.ImageResolver()
    for s in scripts:
        for item in Q._script_items(s):
            index[_hash(resolver.bytes_for(s, item["item_id"]))] = item["drawn"]
    return index


class FakeJudgeHttp:
    """An injected stand-in for the socket. Records every call; opens none.

    `provider_cls` selects the response SHAPE, so the real parser is exercised.
    """

    def __init__(self, provider_cls, image_index: dict[str, str],
                 refuse_all: bool = False, error_all: bool = False,
                 false_pass_on_first_mismatch: bool = False):
        self.provider_cls = provider_cls
        self.image_index = image_index
        self.refuse_all = refuse_all
        self.error_all = error_all
        self.false_pass_on_first_mismatch = false_pass_on_first_mismatch
        self.calls: list[dict] = []
        self._mismatch_seen = 0

    # -- reading the request ------------------------------------------------------------------
    def _drawn_string(self, body: bytes) -> str:
        m = _B64_IMAGE.search(body.decode("utf-8"))
        if not m:
            raise AssertionError("no image found in the request body — the judge sent no picture")
        return self.image_index.get(_hash(base64.b64decode(m.group(1))), "")

    @staticmethod
    def _shape_of(body: bytes) -> str:
        """`verdict` prompts carry a TARGET line; `transcribe` prompts never do."""
        return "verdict" if b"TARGET:" in body else "transcribe"

    @staticmethod
    def _target_of(body: bytes) -> str:
        text = body.decode("utf-8")
        m = re.search(r"TARGET: (.*?)\\n", text)
        return json.loads(f'"{m.group(1)}"') if m else ""

    # -- answering ----------------------------------------------------------------------------
    def __call__(self, url, headers, body, timeout_s):
        self.calls.append({"url": url, "headers": dict(headers), "body": body})

        if self.error_all:
            return self._error()
        if self.refuse_all:
            return self._refusal()

        drawn = self._drawn_string(body)
        shape = self._shape_of(body)

        if shape == "transcribe":
            answer = drawn
            if self.false_pass_on_first_mismatch:
                target = self.image_index and None  # target is not visible in a blind payload
                # A blind payload cannot reveal the target, so a false pass is simulated the only
                # way it can occur in reality: the reader "autocorrects" a corrupted string into a
                # plausible one. The first corrupted image seen is read as its clean neighbour.
                clean = self._clean_neighbour(drawn)
                if clean is not None:
                    self._mismatch_seen += 1
                    if self._mismatch_seen == 1:
                        answer = clean
            return self._ok(answer)

        target = self._target_of(body)
        return self._ok("MATCH" if target == drawn else "MISMATCH")

    def _clean_neighbour(self, drawn: str) -> str | None:
        """If `drawn` is a corrupted render, return the clean string it was corrupted from."""
        if not hasattr(self, "_corruptions"):
            import qualify_text as Q

            self._corruptions = {}
            for s in ("devanagari", "latin"):
                try:
                    for item in Q._script_items(s):
                        if item["expected"] == "mismatch":
                            self._corruptions[item["drawn"]] = item["target"]
                except FileNotFoundError:
                    continue
        return self._corruptions.get(drawn)

    # -- provider-shaped responses -------------------------------------------------------------
    def _is_openai(self) -> bool:
        return self.provider_cls.__name__.startswith("OpenAI")

    def _is_anthropic(self) -> bool:
        return self.provider_cls.__name__.startswith("Anthropic")

    def _ok(self, text: str) -> dict:
        if self._is_openai():
            return {"id": f"resp_fake_{len(self.calls):05d}",
                    "output": [{"content": [{"type": "output_text", "text": text}]}],
                    "usage": {"input_tokens": 812, "output_tokens": 7}}
        if self._is_anthropic():
            return {"id": f"msg_fake_{len(self.calls):05d}", "type": "message",
                    "role": "assistant", "content": [{"type": "text", "text": text}],
                    "stop_reason": "end_turn",
                    "usage": {"input_tokens": 812, "output_tokens": 7}}
        return {"responseId": f"gen-fake-{len(self.calls):05d}",
                "candidates": [{"content": {"parts": [{"text": text}]}, "finishReason": "STOP"}],
                "usageMetadata": {"promptTokenCount": 640, "candidatesTokenCount": 6}}

    def _refusal(self) -> dict:
        if self._is_openai():
            return {"id": f"resp_fake_{len(self.calls):05d}",
                    "output": [{"content": [{"type": "refusal", "refusal": "I can't help."}]}],
                    "usage": {"input_tokens": 800, "output_tokens": 2}}
        if self._is_anthropic():
            return {"id": f"msg_fake_{len(self.calls):05d}", "type": "message",
                    "role": "assistant", "content": [], "stop_reason": "refusal",
                    "stop_details": {"type": "refusal", "category": "general_harms"},
                    "usage": {"input_tokens": 800, "output_tokens": 2}}
        return {"responseId": f"gen-fake-{len(self.calls):05d}",
                "candidates": [{"content": {"parts": []}, "finishReason": "SAFETY"}],
                "usageMetadata": {"promptTokenCount": 640, "candidatesTokenCount": 0}}

    def _error(self) -> dict:
        if self._is_openai():
            return {"id": f"resp_fake_{len(self.calls):05d}",
                    "error": {"type": "server_error", "code": "internal_error"},
                    "usage": {"input_tokens": 790, "output_tokens": 0}}
        if self._is_anthropic():
            return {"id": f"msg_fake_{len(self.calls):05d}",
                    "error": {"type": "api_error", "message": "backend unavailable"},
                    "usage": {"input_tokens": 790, "output_tokens": 0}}
        return {"responseId": f"gen-fake-{len(self.calls):05d}",
                "error": {"status": "UNAVAILABLE", "message": "backend overloaded"},
                "usageMetadata": {"promptTokenCount": 630, "candidatesTokenCount": 0}}


class FakeFalHttp:
    """Injected stand-in for the fal socket. Returns a deterministic artifact URL per call."""

    def __init__(self, refuse_every: int = 0, error_every: int = 0):
        self.calls: list[dict] = []
        self.refuse_every = refuse_every
        self.error_every = error_every

    def __call__(self, url, headers, body, timeout_s):
        self.calls.append({"url": url, "headers": dict(headers), "body": body})
        n = len(self.calls)
        rid = f"fal-fake-{n:04d}"
        if self.refuse_every and n % self.refuse_every == 0:
            return {"request_id": rid,
                    "error": {"type": "content_policy_violation", "message": "blocked"}}
        if self.error_every and n % self.error_every == 0:
            return {"request_id": rid,
                    "error": {"type": "internal_server_error", "message": "upstream failure"}}
        prompt = json.loads(body.decode("utf-8"))["prompt"]
        token = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]
        return {"request_id": rid,
                "images": [{"url": f"https://fal.media/files/fake/{token}.png",
                            "width": 1024, "height": 1024, "content_type": "image/png"}]}
