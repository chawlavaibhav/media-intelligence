"""Reasoning components, invoked programmatically by the orchestrator.

Every call has: a role (input/output contract in contracts.py), named context blocks, a ledger
reservation before it leaves (category=reasoning), schema validation, ONE bounded repair re-ask,
a recorded outcome (llm_calls) and a classified failure. Independent roles (reviewers/inspectors)
can only receive the context kinds listed for them — producer reasoning cannot reach them by
construction, and the store records which kinds each call saw.

Backends: AnthropicBackend (Claude Messages API, raw HTTPS — the SDK is not a dependency of this
deployment), GeminiBackend (generateContent; can take the assembled MP4 so the reviewer sees and
hears the film), SimulatedBackend (deterministic, no network; every output is labelled simulated
and can never satisfy an independent-verification obligation).
"""
from __future__ import annotations

import base64
import json
import re
import time
import urllib.error
import urllib.request
from decimal import Decimal

from product import contracts, schema
from product.config import Settings, scrub
from product.store import BudgetExhausted, Store, dec, sha256_json
from runtime.execute import provider_errors

# USD per million tokens: (input, output). Anthropic first-party list prices (claude-api reference, cached
# 2026-06-24; IDs confirmed). Gemini: ai.google.dev/gemini-api/docs/pricing, paid tier, read 2026-09-23 (output
# includes thinking tokens). Override with MI_PRICE_<MODEL>=in,out.
PRICES = {
    "claude-opus-5": (Decimal("5"), Decimal("25")),
    "claude-opus-5-5": (Decimal("4"), Decimal("20")),
    "claude-sonnet-5": (Decimal("2"), Decimal("10")),
    "claude-haiku-4-5": (Decimal("1"), Decimal("5")),
    # Azure OpenAI Global Standard, ≤ short-context tier (prices.azure.com retail API, eastus, read 2026-09-23)
    "gpt-5.6-sol": (Decimal("4.00"), Decimal("20.00")),
    "gpt-5.6-terra": (Decimal("2.00"), Decimal("12.00")),
    "gpt-5.5": (Decimal("5.00"), Decimal("30.00")),
    "gemini-3.5-flash": (Decimal("1.50"), Decimal("9.00")),
    "gemini-3.1-pro-preview": (Decimal("2.00"), Decimal("12.00")),   # ≤ 200k-token prompts
    "simulated": (Decimal("0"), Decimal("0")),
}
PRICE_BASIS = {"gemini-3.5-flash": "ai.google.dev pricing page, paid tier, 2026-09-23"}

ALLOWED_CONTEXT = {
    "direction_reviewer": {"BRIEF", "INTENT", "DIRECTION"},
    "inspector": {"INSTRUCTION", "REFERENCE_NOTE"},
    "reviewer": {"BRIEF", "INTENT", "DIRECTION", "DETERMINISTIC_CHECKS", "MEDIA_NOTE"},
}


class ReasoningFailed(Exception):
    pass


class ProviderUnavailable(Exception):
    pass


def _price(model: str) -> tuple:
    import os
    env = os.environ.get("MI_PRICE_" + re.sub(r"[^A-Z0-9]", "_", model.upper()))
    if env:
        i, o = env.split(",")
        return Decimal(i), Decimal(o)
    return PRICES.get(model, (Decimal("10"), Decimal("50")))


def cost_of(model: str, usage: dict) -> Decimal:
    pin, pout = _price(model)
    inp = Decimal(usage.get("input_tokens", 0))
    cw = Decimal(usage.get("cache_creation_input_tokens", 0))
    cr = Decimal(usage.get("cache_read_input_tokens", 0))
    out = Decimal(usage.get("output_tokens", 0))
    return (inp * pin + cw * pin * Decimal("1.25") + cr * pin * Decimal("0.1") + out * pout) / Decimal(1_000_000)


def _extract_json(text: str):
    text = text.strip()
    m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.S)
    if m:
        text = m.group(1)
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < 0:
        raise ValueError("no JSON object in the reply")
    return json.loads(text[start:end + 1])


def _http(url: str, headers: dict, payload: dict, timeout: float) -> tuple:
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), method="POST",
                                 headers={**headers, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        try:
            return e.code, json.loads(body)
        except ValueError:
            return e.code, {"error": scrub(body[:500])}
    except (TimeoutError, urllib.error.URLError) as e:
        return None, {"error": scrub(str(e)), "timed_out": "timed out" in str(e).lower()}


class AnthropicBackend:
    provider = "anthropic"
    URL = "https://api.anthropic.com/v1/messages"

    def __init__(self, settings: Settings):
        self.s = settings

    def send(self, *, model, system_role, knowledge, user_text, media, schema_obj, max_tokens):
        key = self.s.secret("ANTHROPIC_API_KEY")
        if not key:
            raise ProviderUnavailable("ANTHROPIC_API_KEY is not configured")
        system = [{"type": "text", "text": system_role}]
        if knowledge:
            system.append({"type": "text", "text": "KNOWLEDGE\n" + knowledge, "cache_control": {"type": "ephemeral"}})
        content = []
        for mime, data in media:
            if mime.startswith("image/"):
                content.append({"type": "image", "source": {"type": "base64", "media_type": mime,
                                                             "data": base64.b64encode(data).decode()}})
            elif mime == "application/pdf":      # a customer's brief deck / storyboard reference
                content.append({"type": "document", "source": {"type": "base64", "media_type": mime,
                                                                "data": base64.b64encode(data).decode()}})
        content.append({"type": "text", "text": user_text})
        body = {"model": model, "max_tokens": max_tokens, "system": system,
                "thinking": {"type": "adaptive"}, "output_config": {"effort": "high"},
                "messages": [{"role": "user", "content": content}]}
        headers = {"x-api-key": key, "anthropic-version": "2023-06-01"}
        if model in ("claude-opus-5", "claude-fable-5-1"):
            # a safety-classifier refusal on a harmless ad brief is re-served by the platform's default fallback
            # instead of failing the job; the reply still reports which model answered (usage is billed per model)
            body["fallbacks"] = "default"
            headers["anthropic-beta"] = "server-side-fallback-2026-07-01"
        st, reply = _http(self.URL, headers, body, timeout=600)
        if st != 200:
            return st, reply, None, {}
        if reply.get("stop_reason") == "refusal":
            return 200, reply, None, reply.get("usage", {})
        text = "".join(b.get("text", "") for b in reply.get("content", []) if b.get("type") == "text")
        return 200, reply, text, reply.get("usage", {})


class AzureOpenAIBackend:
    """Azure OpenAI v1 chat completions (raw HTTPS). `model` is the deployment name. JSON mode + high reasoning effort."""
    provider = "azure_openai"

    def __init__(self, settings: Settings):
        self.s = settings

    def send(self, *, model, system_role, knowledge, user_text, media, schema_obj, max_tokens):
        key, base = self.s.secret("AZURE_OPENAI_API_KEY"), self.s.secret("AZURE_OPENAI_ENDPOINT")
        if not key or not base:
            raise ProviderUnavailable("AZURE_OPENAI_ENDPOINT / AZURE_OPENAI_API_KEY are not configured")
        system = system_role + ("\n\nKNOWLEDGE\n" + knowledge if knowledge else "")
        content = []
        for i, (mime, data) in enumerate(media):
            b64 = base64.b64encode(data).decode()
            if mime.startswith("image/"):
                content.append({"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}", "detail": "high"}})
            elif mime == "application/pdf":
                content.append({"type": "file", "file": {"filename": f"reference-{i + 1}.pdf", "file_data": f"data:{mime};base64,{b64}"}})
        content.append({"type": "text", "text": user_text})
        body = {"model": model, "max_completion_tokens": max_tokens, "reasoning_effort": "high",
                "response_format": {"type": "json_object"},
                "messages": [{"role": "system", "content": system}, {"role": "user", "content": content}]}
        st, reply = _http(base.rstrip("/") + "/openai/v1/chat/completions", {"api-key": key}, body, timeout=600)
        if st != 200:
            return st, reply, None, {}
        u = reply.get("usage") or {}
        cached = (u.get("prompt_tokens_details") or {}).get("cached_tokens", 0)
        usage = {"input_tokens": u.get("prompt_tokens", 0) - cached, "cache_read_input_tokens": cached,
                 "output_tokens": u.get("completion_tokens", 0)}
        ch = (reply.get("choices") or [{}])[0]
        if ch.get("finish_reason") == "content_filter":
            return 200, reply, None, usage
        return 200, reply, (ch.get("message") or {}).get("content") or None, usage


class GeminiBackend:
    provider = "gemini"

    def __init__(self, settings: Settings):
        self.s = settings

    def send(self, *, model, system_role, knowledge, user_text, media, schema_obj, max_tokens):
        key = self.s.secret("GOOGLE_API_KEY") or self.s.secret("GEMINI_API_KEY")
        if not key:
            raise ProviderUnavailable("GOOGLE_API_KEY is not configured")
        parts = []
        for mime, data in media:
            part = {"inlineData": {"mimeType": mime, "data": base64.b64encode(data).decode()}}
            if mime.startswith("video/") and getattr(self.s, "review_fps", None):
                part["videoMetadata"] = {"fps": self.s.review_fps}      # default sampling is 1 frame/s: too coarse for a 1-s warp
            parts.append(part)
        parts.append({"text": user_text})
        sys_text = system_role + ("\n\nKNOWLEDGE\n" + knowledge if knowledge else "")
        body = {"systemInstruction": {"parts": [{"text": sys_text}]}, "contents": [{"role": "user", "parts": parts}],
                "generationConfig": {"responseMimeType": "application/json", "maxOutputTokens": max_tokens}}
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        st, reply = _http(url, {"x-goog-api-key": key}, body, timeout=600)
        if st != 200:
            return st, reply, None, {}
        um = reply.get("usageMetadata") or {}
        usage = {"input_tokens": um.get("promptTokenCount", 0), "output_tokens": um.get("candidatesTokenCount", 0)
                 + um.get("thoughtsTokenCount", 0)}
        text = "".join(p.get("text", "") for c in reply.get("candidates") or [] for p in (c.get("content") or {}).get("parts") or [])
        return 200, reply, text or None, usage


class Reasoner:
    def __init__(self, settings: Settings, store: Store, simulated=None):
        self.s, self.store = settings, store
        from product.simulated import SimulatedReasoning
        self.sim = simulated or SimulatedReasoning()

    def _backend_and_model(self, role: str):
        if self.s.reasoning_mode == "simulated":
            return None, "simulated", "simulated"
        if role in ("reviewer", "inspector", "direction_reviewer") and self.s.reviewer_provider == "gemini":
            return GeminiBackend(self.s), "gemini", self.s.reviewer_model
        if role in ("reviewer", "inspector", "direction_reviewer"):
            return AnthropicBackend(self.s), "anthropic", self.s.reviewer_fallback_model
        if getattr(self.s, "creative_provider", "anthropic") == "azure_openai":
            return AzureOpenAIBackend(self.s), "azure_openai", self.s.creative_model
        return AnthropicBackend(self.s), "anthropic", self.s.creative_model

    def call(self, job_id: str, role: str, context: dict, *, knowledge: str | None = None, media: list = (),
             max_tokens: int = 16000, estimate_in_tokens: int | None = None) -> dict:
        system_role, out_schema = contracts.ROLES[role]
        isolated = role in contracts.ISOLATED_ROLES
        if isolated:
            extra = set(context) - ALLOWED_CONTEXT[role]
            if extra:
                raise ReasoningFailed(f"{role} is an independent role; refusing producer context {sorted(extra)}")
            if knowledge:
                raise ReasoningFailed(f"{role} is an independent role; it does not receive the producer's knowledge block")
        backend, provider, model = self._backend_and_model(role)
        user_text = "\n\n".join(f"## {k}\n{v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, indent=1)}"
                                for k, v in context.items())
        user_text += "\n\n## OUTPUT\nReturn one JSON object with exactly these fields (JSON Schema):\n" + json.dumps(out_schema)
        in_sha = sha256_json({"role": role, "context": context, "knowledge_sha": sha256_json(knowledge or ""),
                              "media": [(m, len(d)) for m, d in media]})
        est_in = estimate_in_tokens or (len(user_text) + len(knowledge or "") + len(system_role)) // 3 + 1500 * len(media)
        pin, pout = _price(model)
        estimate = (Decimal(est_in) * pin + Decimal(max_tokens) * pout) / Decimal(1_000_000)
        phase = "independent_review" if isolated else ("canon_consultation" if knowledge else "creative_reasoning")

        messages_extra = ""
        last_err, transient = None, False
        for attempt in range(3):
            att = self.store.reserve(job_id, route=f"llm:{model}", category="reasoning", amount_usd=estimate)
            call_id = self.store.llm_start(job_id, role=role, provider=provider, model=model, isolated=isolated,
                                           input_sha256=in_sha, context_kinds=sorted(context), attempt_id=att)
            with self.store.timed(job_id, phase, role):
                if backend is None:
                    out = self.sim.respond(role, context, media)
                    st, text, usage, reply = 200, json.dumps(out), {"input_tokens": 0, "output_tokens": 0}, {}
                else:
                    try:
                        st, reply, text, usage = backend.send(model=model, system_role=system_role, knowledge=knowledge,
                                                              user_text=user_text + messages_extra, media=list(media),
                                                              schema_obj=out_schema, max_tokens=max_tokens)
                    except ProviderUnavailable as e:
                        self.store.settle(att, status="released", settled_usd=0, failure_class="configuration", detail=str(e))
                        self.store.llm_end(call_id, status="not_configured")
                        raise
            actual = cost_of(model, usage)
            if st != 200 or text is None:
                cls = provider_errors.classify(http_status=st, message=str(reply)[:300], timed_out=bool(reply.get("timed_out")))
                charged = Decimal(0) if (st and 400 <= st < 500) else actual
                self.store.settle(att, status="failed", settled_usd=charged, failure_class=cls.get("failure_class"),
                                  counts_against_route=False, detail=scrub(str(reply))[:400])
                self.store.llm_end(call_id, status=f"http_{st}", usage=usage)
                last_err = f"{provider} HTTP {st}: {scrub(str(reply))[:200]}"
                if cls.get("retry_eligible") or st is None or (st and st >= 500) or st == 429:
                    transient = True
                    time.sleep(min(2 ** attempt, 8) if backend else 0)
                    continue
                raise ReasoningFailed(last_err)
            transient = False
            self.store.settle(att, status="ok", settled_usd=actual, detail=json.dumps(usage)[:300])
            try:
                out = _extract_json(text)
                errs = schema.errors(out, out_schema)
            except ValueError as e:
                out, errs = None, [str(e)]
            if not errs:
                if provider == "simulated":
                    out["_simulated"] = True
                self.store.llm_end(call_id, status="ok", output=out, usage=usage)
                out["_call"] = {"id": call_id, "provider": provider, "model": model, "isolated": isolated,
                                "context_kinds": sorted(context), "cost_usd": str(actual)}
                return out
            self.store.llm_end(call_id, status="invalid_output", output={"errors": errs[:20], "text": (text or "")[:2000]}, usage=usage)
            last_err = f"{role} output failed its contract: {errs[:5]}"
            if attempt >= 1:
                break
            messages_extra = ("\n\n## CORRECTION\nYour previous reply did not match the schema: " + "; ".join(errs[:12])
                              + "\nReturn the complete corrected JSON object only.")
        if transient:
            raise ProviderUnavailable(last_err)
        raise ReasoningFailed(last_err or f"{role} failed")
