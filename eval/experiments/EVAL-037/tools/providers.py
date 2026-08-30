#!/usr/bin/env python3
"""EVAL-037 — provider adapters, usage capture and failure classification.

One adapter per model key. Each builds a FRESH, STATELESS request per attempt.
Nothing from a previous trial or attempt is carried in.

Parameter choices are part of the freeze and are NOT free to change afterwards:

  sol    OpenAI Responses API, reasoning.effort="high". Sampling left at provider
         defaults - temperature/top_p are never set.
  sonnet Anthropic Messages API, thinking={"type":"adaptive"},
         output_config={"effort":"high"}. On claude-sonnet-5 `budget_tokens` and
         temperature/top_p/top_k are REMOVED (400), so "sampling: provider defaults"
         is both the instruction and the only legal call.
  haiku  Anthropic Messages API, thinking={"type":"enabled","budget_tokens":8000}.
         claude-haiku-4-5 is pre-4.6: it takes budget_tokens and REJECTS `effort`.
         budget_tokens must be < max_tokens, hence max_tokens=16000.
  gemma  Google Gemini API, provider defaults throughout. No thinking budget, no
         effort, no reasoning_effort - those controls are not set for this model.

max_tokens is a required transport parameter, not a sampling control.

TOOL LOOP GUARD
  MAX_TOOL_TURNS is an emergency stop against literal runaway execution only. It is
  NOT a retrieval budget: the model may retrieve as much as it wants below it. Hitting
  it is a model+condition EXECUTION FAILURE, recorded as such, and is never retried as
  though it were a transient provider fault.

USAGE
  Every provider turn - including every intermediate turn caused by a tool call - is
  recorded with its own usage, stop reason, latency, request id and model version. A
  field the provider does not expose is stored as null. Nothing is invented.
"""
import json
import os
import time

MAX_TOKENS = {"sol": 32000, "sonnet": 32000, "haiku": 16000, "gemma": 8192}

# The emergency guard. Not a retrieval budget. See module docstring.
MAX_TOOL_TURNS = 100

# ---------------------------------------------------------------------------
# Failure classification. Only TRANSIENT classes may be retried.
TRANSIENT_CLASSES = {
    "timeout",
    "connection_error",
    "rate_limit_429",
    "server_error_5xx",
}

# Deterministic: the same request would fail the same way. Retrying these would be
# creative resampling wearing a technical retry's clothes.
DETERMINISTIC_CLASSES = {
    "invalid_request_4xx",
    "auth_error",
    "tool_schema_rejected",
    "context_overflow",
    "tool_loop_guard_exhausted",
    "model_refusal",
    "truncated_response",
    "empty_response",
    "sdk_error",
}

ALL_FAILURE_CLASSES = TRANSIENT_CLASSES | DETERMINISTIC_CLASSES

_CONTEXT_MARKERS = ("context window", "maximum context", "context length", "too long",
                    "token limit", "exceeds the maximum", "prompt is too long")
_TOOL_SCHEMA_MARKERS = ("tool", "function_declaration", "input_schema", "parameters")


def is_transient(failure_class):
    return failure_class in TRANSIENT_CLASSES


class ProviderError(RuntimeError):
    """A provider/transport failure carrying the class that decides retry eligibility."""

    def __init__(self, message, failure_class, detail=None):
        super().__init__(message)
        if failure_class not in ALL_FAILURE_CLASSES:
            raise ValueError(f"unknown failure class {failure_class!r}")
        self.failure_class = failure_class
        self.detail = detail or {}


def classify_exception(exc):
    """Map a provider exception onto a failure class, without importing any SDK.

    Duck-typed on status_code and class name so it works identically for every
    provider and needs no SDK present. When nothing identifies the error, it falls to
    `sdk_error`, which is DETERMINISTIC - the safe default, because an unrecognised
    error must never earn a free resample.
    """
    if isinstance(exc, ProviderError):
        return exc.failure_class
    name = type(exc).__name__.lower()
    msg = str(exc).lower()
    status = getattr(exc, "status_code", None) or getattr(exc, "code", None)
    try:
        status = int(status)
    except (TypeError, ValueError):
        status = None

    if status == 408 or "timeout" in name or "timedout" in name:
        return "timeout"
    if "connection" in name or "connect" in msg and "refused" in msg:
        return "connection_error"
    if status == 429 or "ratelimit" in name:
        return "rate_limit_429"
    if status is not None and 500 <= status < 600:
        return "server_error_5xx"
    if status in (401, 403) or "authentication" in name or "permission" in name:
        return "auth_error"
    if status is not None and 400 <= status < 500:
        if any(m in msg for m in _CONTEXT_MARKERS):
            return "context_overflow"
        if all(m in msg for m in ("tool", "schema")) or "function_declaration" in msg:
            return "tool_schema_rejected"
        return "invalid_request_4xx"
    if any(m in msg for m in _CONTEXT_MARKERS):
        return "context_overflow"
    return "sdk_error"


# Provider finish/stop reasons that mean the answer was cut off or declined.
TRUNCATION_REASONS = {"max_tokens", "length", "max_output_tokens", "incomplete",
                      "MAX_TOKENS", "model_length"}
REFUSAL_REASONS = {"refusal", "safety", "blocklist", "prohibited_content", "SAFETY"}


# ---------------------------------------------------------------------------
def _num(v):
    """Coerce to int, or None. Never guesses a token count."""
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def _get(obj, *names):
    for n in names:
        if isinstance(obj, dict) and n in obj:
            return obj[n]
        v = getattr(obj, n, None)
        if v is not None:
            return v
    return None


def turn_record(turn_index, started, raw, provider):
    """One provider turn's complete usage/cost evidence. Missing fields stay null.

    INSTRUMENTATION FIX (Gemini usage capture). The google-genai response object names
    its usage block `usage_metadata`, not `usage`, so a lookup on `usage` alone found
    nothing and every Gemini token field was recorded as null while the provider had in
    fact reported them. Both names are consulted, `usage` first, so the Anthropic and
    OpenAI branches resolve exactly as before. The provider-reported object is retained
    verbatim in `provider_reported_usage` either way; this only makes the parsed fields
    reach the ledger. It changes no request, no prompt and no model behaviour.
    """
    usage = _get(raw, "usage", "usage_metadata") or {}
    u = _serialise(usage) if not isinstance(usage, dict) else usage

    if provider == "Anthropic":
        inp = _num(_get(u, "input_tokens"))
        cached = _num(_get(u, "cache_read_input_tokens"))
        out = _num(_get(u, "output_tokens"))
        reasoning = _num(_get(u, "thinking_tokens", "reasoning_tokens"))
        stop = _get(raw, "stop_reason")
    elif provider == "OpenAI":
        inp = _num(_get(u, "input_tokens"))
        details = _get(u, "input_tokens_details") or {}
        cached = _num(_get(details, "cached_tokens"))
        out = _num(_get(u, "output_tokens"))
        odet = _get(u, "output_tokens_details") or {}
        reasoning = _num(_get(odet, "reasoning_tokens"))
        stop = _get(raw, "status") or _get(raw, "incomplete_details")
    else:  # Google Gemini API
        inp = _num(_get(u, "prompt_token_count"))
        cached = _num(_get(u, "cached_content_token_count"))
        out = _num(_get(u, "candidates_token_count"))
        reasoning = _num(_get(u, "thoughts_token_count"))
        cands = _get(raw, "candidates") or []
        stop = _get(cands[0], "finish_reason") if cands else None

    return {
        "turn_index": turn_index,
        "provider": provider,
        "provider_model_version": _stringify(_get(raw, "model", "model_version")),
        "provider_request_id": _stringify(_get(raw, "id", "response_id", "request_id")),
        "input_tokens": inp,
        "cached_input_tokens": cached,
        "output_tokens": out,
        "reasoning_tokens": reasoning,
        "stop_reason": _stringify(stop),
        "latency_ms": int((time.time() - started) * 1000),
        "provider_reported_usage": _serialise(usage) if usage else None,
    }


def _stringify(v):
    if v is None:
        return None
    if isinstance(v, (str, int, float, bool)):
        return str(v)
    return str(_serialise(v))


def check_stop_reason(rec):
    """Turn a provider stop reason into a deterministic failure, where it is one."""
    stop = (rec.get("stop_reason") or "").strip()
    if not stop:
        return None
    if stop in TRUNCATION_REASONS or stop.lower() in {s.lower() for s in TRUNCATION_REASONS}:
        return "truncated_response"
    if stop in REFUSAL_REASONS or stop.lower() in {s.lower() for s in REFUSAL_REASONS}:
        return "model_refusal"
    return None


# ---------------------------------------------------------------------------
class Adapter:
    provider = None
    model_key = None

    def __init__(self, model_id, tool_schemas=None):
        self.model_id = model_id
        self.tool_schemas = list(tool_schemas or [])

    def build_request(self, system_prompt, user_content):
        raise NotImplementedError

    def call(self, request, dispatch=None, **_):
        raise NotImplementedError

    @staticmethod
    def request_digest(request):
        import hashlib
        return hashlib.sha256(
            json.dumps(request, sort_keys=True, default=str).encode()).hexdigest()


class OpenAIResponsesAdapter(Adapter):
    provider, model_key = "OpenAI", "sol"

    def build_request(self, system_prompt, user_content):
        req = {"model": self.model_id, "instructions": system_prompt,
               "input": [{"role": "user", "content": user_content}],
               "reasoning": {"effort": "high"},
               "max_output_tokens": MAX_TOKENS["sol"]}
        if self.tool_schemas:
            req["tools"] = [{"type": "function", "name": t["name"],
                             "description": t["description"],
                             "parameters": t["input_schema"]} for t in self.tool_schemas]
        return req

    def call(self, request, dispatch=None, **_):
        from openai import OpenAI
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        convo, turns, tool_log = list(request["input"]), [], []
        for turn in range(MAX_TOOL_TURNS):
            req = dict(request); req["input"] = convo
            t0 = time.time()
            try:
                resp = client.responses.create(**req)
            except Exception as e:
                raise ProviderError(str(e)[:600], classify_exception(e)) from e
            rec = turn_record(turn, t0, resp, self.provider)
            turns.append(rec)
            fail = check_stop_reason(rec)
            if fail:
                raise ProviderError(f"provider stop reason {rec['stop_reason']!r}", fail,
                                    {"turns": turns})
            calls = [o for o in (getattr(resp, "output", None) or [])
                     if getattr(o, "type", "") == "function_call"]
            if not calls:
                return _finish(getattr(resp, "output_text", None), tool_log, resp, turns)
            for c in calls:
                convo.append(c)
                out, meta = _run_tool(dispatch, c.name, json.loads(c.arguments or "{}"), turn)
                tool_log.append(meta)
                convo.append({"type": "function_call_output", "call_id": c.call_id,
                              "output": json.dumps(out, default=str)})
        raise ProviderError(
            f"tool loop guard: {MAX_TOOL_TURNS} provider turns without a final answer",
            "tool_loop_guard_exhausted", {"turns": turns, "tool_calls": len(tool_log)})


class AnthropicMessagesAdapter(Adapter):
    provider = "Anthropic"

    def __init__(self, model_id, tool_schemas=None, model_key="sonnet"):
        super().__init__(model_id, tool_schemas)
        self.model_key = model_key

    def build_request(self, system_prompt, user_content):
        req = {"model": self.model_id, "system": system_prompt,
               "messages": [{"role": "user", "content": user_content}],
               "max_tokens": MAX_TOKENS[self.model_key]}
        if self.model_key == "sonnet":
            req["thinking"] = {"type": "adaptive"}
            req["output_config"] = {"effort": "high"}
        elif self.model_key == "haiku":
            req["thinking"] = {"type": "enabled", "budget_tokens": 8000}
        if self.tool_schemas:
            req["tools"] = list(self.tool_schemas)
        return req

    def call(self, request, dispatch=None, **_):
        import anthropic
        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        messages, turns, tool_log = list(request["messages"]), [], []
        for turn in range(MAX_TOOL_TURNS):
            req = dict(request); req["messages"] = messages
            t0 = time.time()
            try:
                with client.messages.stream(**req) as stream:
                    resp = stream.get_final_message()
            except Exception as e:
                raise ProviderError(str(e)[:600], classify_exception(e)) from e
            rec = turn_record(turn, t0, resp, self.provider)
            turns.append(rec)
            fail = check_stop_reason(rec)
            if fail:
                raise ProviderError(f"provider stop reason {rec['stop_reason']!r}", fail,
                                    {"turns": turns})
            uses = [b for b in resp.content if getattr(b, "type", "") == "tool_use"]
            if not uses:
                text = "".join(b.text for b in resp.content
                               if getattr(b, "type", "") == "text")
                return _finish(text, tool_log, resp, turns)
            messages.append({"role": "assistant", "content": resp.content})
            results = []
            for u in uses:
                out, meta = _run_tool(dispatch, u.name, u.input or {}, turn)
                tool_log.append(meta)
                results.append({"type": "tool_result", "tool_use_id": u.id,
                                "content": json.dumps(out, default=str)})
            messages.append({"role": "user", "content": results})  # all results, one message
        raise ProviderError(
            f"tool loop guard: {MAX_TOOL_TURNS} provider turns without a final answer",
            "tool_loop_guard_exhausted", {"turns": turns, "tool_calls": len(tool_log)})


class GeminiAdapter(Adapter):
    provider, model_key = "Google Gemini API", "gemma"

    def build_request(self, system_prompt, user_content):
        req = {"model": self.model_id,
               "contents": [{"role": "user", "parts": [{"text": user_content}]}],
               "config": {"system_instruction": system_prompt,
                          "max_output_tokens": MAX_TOKENS["gemma"]}}
        if self.tool_schemas:
            req["config"]["tools"] = [{"function_declarations": [
                {"name": t["name"], "description": t["description"],
                 "parameters": t["input_schema"]} for t in self.tool_schemas]}]
        return req

    def call(self, request, dispatch=None, **_):
        from google import genai
        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        contents, turns, tool_log = list(request["contents"]), [], []
        for turn in range(MAX_TOOL_TURNS):
            t0 = time.time()
            try:
                resp = client.models.generate_content(
                    model=request["model"], contents=contents, config=request["config"])
            except Exception as e:
                raise ProviderError(str(e)[:600], classify_exception(e)) from e
            rec = turn_record(turn, t0, resp, self.provider)
            turns.append(rec)
            fail = check_stop_reason(rec)
            if fail:
                raise ProviderError(f"provider finish reason {rec['stop_reason']!r}", fail,
                                    {"turns": turns})
            parts = []
            for cand in (getattr(resp, "candidates", None) or []):
                parts += list(getattr(getattr(cand, "content", None), "parts", None) or [])
            calls = [p.function_call for p in parts if getattr(p, "function_call", None)]
            if not calls:
                return _finish(getattr(resp, "text", None), tool_log, resp, turns)
            contents.append({"role": "model", "parts": parts})
            replies = []
            for c in calls:
                out, meta = _run_tool(dispatch, c.name, dict(c.args or {}), turn)
                tool_log.append(meta)
                replies.append({"function_response": {"name": c.name,
                                                      "response": {"result": out}}})
            contents.append({"role": "user", "parts": replies})
        raise ProviderError(
            f"tool loop guard: {MAX_TOOL_TURNS} provider turns without a final answer",
            "tool_loop_guard_exhausted", {"turns": turns, "tool_calls": len(tool_log)})


# ---------------------------------------------------------------------------
def _digest_keys(obj):
    """Copy `obj` with every mapping key coerced to a string. DIGEST PATH ONLY.

    INSTRUMENTATION FIX (Canon evidence digest). Canon YAML sources contain mappings
    whose keys are a mix of booleans and strings — YAML 1.1 reads a bare `on:`/`yes:`/
    `no:` key as a boolean — and `json.dumps(..., sort_keys=True)` then tries to order a
    bool against a str and raises TypeError. That aborted a Canon retrieval that had
    already succeeded, purely while computing an evidence hash.

    This normalisation is applied ONLY on the way to a hash. The object returned to the
    caller, and therefore to the model, is the untouched original: Canon content,
    ranking and status semantics are unaffected. All-string-key results digest exactly
    as they did before.
    """
    if isinstance(obj, dict):
        return {str(k): _digest_keys(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_digest_keys(v) for v in obj]
    return obj


def _digest_blob(obj):
    """The canonical serialisation used for evidence hashes. Never sent to a model."""
    return json.dumps(_digest_keys(obj), sort_keys=True, default=str)


def _run_tool(dispatch, name, args, turn_index):
    """Execute one tool call and build its COMPLETE transcript record.

    The record keeps the actual arguments and per-item identity - item id, source id,
    source_status, kind, Q&A flag - not just a hash and a count, so a later session can
    reconstruct exactly what knowledge the tested model asked for and received. The
    full tool result travels alongside in `_full_result` and is written to the
    attempt's transcript file by the runner.
    """
    import hashlib
    if dispatch is None:
        raise ProviderError(f"model called {name!r} but no tool is exposed here",
                            "tool_schema_rejected")
    out = dispatch(name, args)
    blob = _digest_blob(out)
    meta = {
        "turn_index": turn_index,
        "name": name,
        "arguments": args,                       # actual arguments, not only a hash
        "arguments_digest": hashlib.sha256(_digest_blob(args).encode()).hexdigest(),
        "result_digest": hashlib.sha256(blob.encode()).hexdigest(),
        "result_bytes": len(blob),
    }

    if name == "website_read":
        meta.update({
            "tool_family": "website",
            "source_url": out.get("source_url"),
            "snapshot_path": out.get("snapshot_path"),
            "snapshot_sha256": out.get("snapshot_sha256"),
            "source_html_sha256": out.get("source_html_sha256"),
            "content_chars": out.get("content_chars"),
            "live_browsing": False,
            "result_item_count": 1,
        })
        meta["_full_result"] = out
        return out, meta

    items = out.get("results") or out.get("items") or out.get("sources") or []
    if isinstance(out, dict) and "source_status" in out and not items:
        items = [out]
    refs = []
    for i in items:
        if not isinstance(i, dict):
            continue
        refs.append({
            "item_id": i.get("item_id") or i.get("source_dir"),
            "source_id": i.get("source_id"),
            "source_dir": i.get("source_dir"),
            "source_status": i.get("source_status"),
            "kind": i.get("kind", "source"),
            "is_qa": i.get("kind") == "qa",
            "not_benchmark_ground_truth": i.get("not_benchmark_ground_truth"),
            "rank": i.get("rank"),
            "score": i.get("score"),
        })
    meta.update({
        "tool_family": "canon",
        "result_item_count": len(items),
        "accepted_items": sum(1 for r in refs if r["source_status"] == "ACCEPTED"),
        "hold_items": sum(1 for r in refs if r["source_status"] == "HOLD"),
        "qa_items": sum(1 for r in refs if r["is_qa"]),
        "every_item_carried_source_status": (
            all(r["source_status"] in ("ACCEPTED", "HOLD") for r in refs) if refs else True),
        "retrieved_refs": refs,                  # per-item identity, fully retained
    })
    meta["_full_result"] = out
    return out, meta


def _finish(text, tool_log, raw, turns):
    if text is None or not str(text).strip():
        raise ProviderError("provider returned an empty response", "empty_response",
                            {"turns": turns})
    return {"text": text, "tool_calls": tool_log, "turns": turns,
            "raw": _serialise(raw)}


def _serialise(obj):
    for attr in ("model_dump", "to_dict", "dict"):
        fn = getattr(obj, attr, None)
        if callable(fn):
            try:
                return fn()
            except Exception:
                pass
    try:
        return json.loads(json.dumps(obj, default=str))
    except Exception:
        return {"repr": repr(obj)}


ADAPTERS = {
    "sol": lambda mid, ts: OpenAIResponsesAdapter(mid, ts),
    "sonnet": lambda mid, ts: AnthropicMessagesAdapter(mid, ts, "sonnet"),
    "haiku": lambda mid, ts: AnthropicMessagesAdapter(mid, ts, "haiku"),
    "gemma": lambda mid, ts: GeminiAdapter(mid, ts),
}
