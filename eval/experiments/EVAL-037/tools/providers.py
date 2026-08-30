#!/usr/bin/env python3
"""EVAL-037 — provider adapters.

One adapter per model key. Each builds a FRESH, STATELESS request per trial: the
system prompt, the brief as the only user message, and (FULL_CANON only) the three
Canon tools. Nothing from a previous trial or attempt is ever carried in.

Parameter choices are deliberate and are NOT free to change after the freeze:

  sol    OpenAI Responses API, reasoning.effort="high". Sampling left at provider
         defaults - temperature/top_p are never set.

  sonnet Anthropic Messages API, thinking={"type":"adaptive"},
         output_config={"effort":"high"}. On claude-sonnet-5 `budget_tokens` is
         REMOVED (400) and temperature/top_p/top_k are REMOVED (400), so "sampling:
         provider defaults" is both the instruction and the only legal call.

  haiku  Anthropic Messages API, thinking={"type":"enabled","budget_tokens":8000}.
         claude-haiku-4-5 is a pre-4.6 model: it takes budget_tokens and REJECTS the
         `effort` control. budget_tokens must be < max_tokens, hence max_tokens=16000.

  gemma  Google Gemini API, provider defaults throughout. No thinking budget, no
         effort, no reasoning_effort - those controls do not exist on this model and
         must not be invented. See PREFLIGHT NOTE below.

max_tokens is a required transport parameter, not a sampling control. It is set
uniformly and generously so no trial is truncated by our own ceiling.

PREFLIGHT NOTE (gemma FULL_CANON): Gemma models served through the Gemini API have
historically not supported function calling or a separate system instruction. The
gemma-full-canon lane therefore has a hard preflight gate: if the exact model will not
accept tool declarations, the worker STOPS and escalates. It must NOT quietly run a
tool-less "FULL_CANON" lane - that would be a different condition wearing this one's
name.
"""
import json
import os

MAX_TOKENS = {"sol": 32000, "sonnet": 32000, "haiku": 16000, "gemma": 8192}


class ProviderError(RuntimeError):
    """Transport/technical failure. Carries the class that licenses a retry."""

    def __init__(self, message, failure_class):
        super().__init__(message)
        self.failure_class = failure_class


class Adapter:
    """Base adapter. Subclasses implement build_request() and call()."""

    provider = None
    model_key = None

    def __init__(self, model_id, tool_schemas=None):
        self.model_id = model_id
        self.tool_schemas = tool_schemas or []

    def build_request(self, system_prompt, user_message):
        raise NotImplementedError

    def call(self, request, canon_dispatch=None):
        raise NotImplementedError

    @staticmethod
    def request_digest(request):
        import hashlib
        return hashlib.sha256(
            json.dumps(request, sort_keys=True, default=str).encode()).hexdigest()


# --------------------------------------------------------------------------
class OpenAIResponsesAdapter(Adapter):
    provider, model_key = "OpenAI", "sol"

    def build_request(self, system_prompt, user_message):
        req = {
            "model": self.model_id,
            "instructions": system_prompt,
            "input": [{"role": "user", "content": user_message}],
            "reasoning": {"effort": "high"},
            "max_output_tokens": MAX_TOKENS["sol"],
        }
        if self.tool_schemas:
            req["tools"] = [{"type": "function", "name": t["name"],
                             "description": t["description"],
                             "parameters": t["input_schema"]}
                            for t in self.tool_schemas]
        return req

    def call(self, request, canon_dispatch=None):
        try:
            from openai import OpenAI
        except ImportError as e:  # pragma: no cover
            raise ProviderError(f"openai SDK missing: {e}", "sdk_error")
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        return _agentic_loop_openai(client, request, canon_dispatch)


# --------------------------------------------------------------------------
class AnthropicMessagesAdapter(Adapter):
    provider = "Anthropic"

    def __init__(self, model_id, tool_schemas=None, model_key="sonnet"):
        super().__init__(model_id, tool_schemas)
        self.model_key = model_key

    def build_request(self, system_prompt, user_message):
        req = {
            "model": self.model_id,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_message}],
            "max_tokens": MAX_TOKENS[self.model_key],
        }
        if self.model_key == "sonnet":
            # claude-sonnet-5: adaptive thinking is the only on-mode; budget_tokens
            # and temperature/top_p/top_k are removed and return 400.
            req["thinking"] = {"type": "adaptive"}
            req["output_config"] = {"effort": "high"}
        elif self.model_key == "haiku":
            # claude-haiku-4-5 is pre-4.6: explicit budget, and `effort` is rejected.
            req["thinking"] = {"type": "enabled", "budget_tokens": 8000}
        if self.tool_schemas:
            req["tools"] = list(self.tool_schemas)
        return req

    def call(self, request, canon_dispatch=None):
        try:
            import anthropic
        except ImportError as e:  # pragma: no cover
            raise ProviderError(f"anthropic SDK missing: {e}", "sdk_error")
        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        return _agentic_loop_anthropic(client, request, canon_dispatch)


# --------------------------------------------------------------------------
class GeminiAdapter(Adapter):
    provider, model_key = "Google Gemini API", "gemma"

    def build_request(self, system_prompt, user_message):
        # Provider defaults throughout. No thinking config, no effort, no
        # reasoning_effort: those controls do not exist for gemma-4-31b-it.
        req = {
            "model": self.model_id,
            "contents": [{"role": "user", "parts": [{"text": user_message}]}],
            "config": {"system_instruction": system_prompt,
                       "max_output_tokens": MAX_TOKENS["gemma"]},
        }
        if self.tool_schemas:
            req["config"]["tools"] = [{"function_declarations": [
                {"name": t["name"], "description": t["description"],
                 "parameters": t["input_schema"]} for t in self.tool_schemas]}]
        return req

    def call(self, request, canon_dispatch=None):
        try:
            from google import genai
        except ImportError as e:  # pragma: no cover
            raise ProviderError(f"google-genai SDK missing: {e}", "sdk_error")
        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        return _agentic_loop_gemini(client, request, canon_dispatch)


# --------------------------------------------------------------------------
# Agentic loops. Each keeps the tool conversation inside ONE trial. Nothing
# crosses a trial boundary.
def _agentic_loop_openai(client, request, canon_dispatch, max_rounds=64):
    convo = list(request["input"])
    tool_log, text = [], None
    for _ in range(max_rounds):
        req = dict(request); req["input"] = convo
        resp = client.responses.create(**req)
        calls = [o for o in getattr(resp, "output", []) if getattr(o, "type", "") == "function_call"]
        if not calls:
            text = getattr(resp, "output_text", None)
            return _finish(text, tool_log, resp)
        for c in calls:
            convo.append(c)
            out, meta = _run_tool(canon_dispatch, c.name, json.loads(c.arguments or "{}"))
            tool_log.append(meta)
            convo.append({"type": "function_call_output", "call_id": c.call_id,
                          "output": json.dumps(out, default=str)})
    raise ProviderError("tool loop did not converge", "sdk_error")


def _agentic_loop_anthropic(client, request, canon_dispatch, max_rounds=64):
    messages = list(request["messages"])
    tool_log = []
    for _ in range(max_rounds):
        req = dict(request); req["messages"] = messages
        with client.messages.stream(**req) as stream:
            resp = stream.get_final_message()
        uses = [b for b in resp.content if getattr(b, "type", "") == "tool_use"]
        if not uses:
            text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
            return _finish(text, tool_log, resp)
        messages.append({"role": "assistant", "content": resp.content})
        results = []
        for u in uses:
            out, meta = _run_tool(canon_dispatch, u.name, u.input or {})
            tool_log.append(meta)
            results.append({"type": "tool_result", "tool_use_id": u.id,
                            "content": json.dumps(out, default=str)})
        messages.append({"role": "user", "content": results})  # all results, one message
    raise ProviderError("tool loop did not converge", "sdk_error")


def _agentic_loop_gemini(client, request, canon_dispatch, max_rounds=64):
    contents = list(request["contents"])
    tool_log = []
    for _ in range(max_rounds):
        resp = client.models.generate_content(model=request["model"], contents=contents,
                                              config=request["config"])
        parts = []
        for cand in (getattr(resp, "candidates", None) or []):
            parts += list(getattr(getattr(cand, "content", None), "parts", None) or [])
        calls = [p.function_call for p in parts if getattr(p, "function_call", None)]
        if not calls:
            return _finish(getattr(resp, "text", None), tool_log, resp)
        contents.append({"role": "model", "parts": parts})
        replies = []
        for c in calls:
            out, meta = _run_tool(canon_dispatch, c.name, dict(c.args or {}))
            tool_log.append(meta)
            replies.append({"function_response": {"name": c.name, "response": {"result": out}}})
        contents.append({"role": "user", "parts": replies})
    raise ProviderError("tool loop did not converge", "sdk_error")


def _run_tool(canon_dispatch, name, args):
    """Execute one Canon tool call and record what came back, by status."""
    import hashlib
    if canon_dispatch is None:
        raise ProviderError(f"model called {name!r} but no tool is exposed in this condition",
                            "sdk_error")
    out = canon_dispatch(name, args)
    items = out.get("results") or out.get("items") or out.get("sources") or []
    if isinstance(out, dict) and "source_status" in out and not items:
        items = [out]
    acc = sum(1 for i in items if isinstance(i, dict) and i.get("source_status") == "ACCEPTED")
    hold = sum(1 for i in items if isinstance(i, dict) and i.get("source_status") == "HOLD")
    qa = sum(1 for i in items if isinstance(i, dict) and i.get("kind") == "qa")
    every = all(isinstance(i, dict) and i.get("source_status") in ("ACCEPTED", "HOLD")
                for i in items) if items else True
    meta = {"name": name,
            "arguments_digest": hashlib.sha256(
                json.dumps(args, sort_keys=True, default=str).encode()).hexdigest(),
            "result_item_count": len(items), "accepted_items": acc, "hold_items": hold,
            "qa_items": qa, "every_item_carried_source_status": every}
    return out, meta


def _finish(text, tool_log, raw):
    if text is None or not str(text).strip():
        raise ProviderError("empty response", "empty_response")
    return {"text": text, "tool_calls": tool_log, "raw": _serialise(raw)}


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
