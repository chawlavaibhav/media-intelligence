#!/usr/bin/env python3
"""EVAL-037 — deterministic fake provider.

Exists so the whole runner can be exercised end to end WITHOUT a single real
experimental call. It makes no network request of any kind: no SDK import, no client,
no socket.

Scenarios:
  clean               every trial succeeds on the first attempt
  flaky               a named trial fails TRANSIENTLY once, then succeeds
  hard_fail           a named trial fails transiently forever (stops at 3 attempts)
  deterministic_fail  a named trial fails with a 400 (must NOT be retried at all)
  context_overflow    a named trial blows its context (model+condition execution failure)
  loop_guard          a named trial trips the tool-loop guard (execution failure)
  truncated           the provider reports a truncation stop reason
  malformed           a named trial returns a malformed answer once, then a valid one
  always_malformed    never well-formed (one repair, then failed_format)
  repair_flaky        the FORMAT REPAIR call fails transiently once, then succeeds
  canon_user          the model calls the Canon tools before answering
  website_user        the model calls website_read before answering
  tool_user           the model calls both Canon and website tools
  controlled_ok       CONTROLLED_CANON: declares RESEARCH_NEEDS, then 3 bounded
                      searches (limit=8) and 3 item reads — inside the allowance
  controlled_violation
                      CONTROLLED_CANON: 4 searches, one of them UNBOUNDED — must be
                      recorded failed_controlled_retrieval, never clamped or re-run
  controlled_overflow CONTROLLED_CANON: retrieves, then dies of context overflow, to
                      exercise EVIDENCE-002 (turns and transcripts survive a failure)

Determinism: every response is a pure function of (trial_id, attempt_index, phase,
scenario). No clock, no randomness.
"""
import hashlib
import json

SECTIONS = ["DELIVERABLE", "OBJECTIVE_INTERPRETATION", "CORE_CREATIVE_IDEA",
            "MESSAGE_AND_INFORMATION_HIERARCHY", "VISUAL_SYSTEM", "PRODUCTION_RECIPE",
            "GENERATION_PROMPTS", "DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS",
            "AUDIO_AND_EDIT", "FAILURE_PREVENTION", "HARD_CONSTRAINT_CHECK",
            "KNOWLEDGE_AND_WEBSITE_USE"]

MALFORMED_TEXT = "Here are three concepts you could consider. No headings.\n"


class FakeProviderError(RuntimeError):
    def __init__(self, message, failure_class, detail=None):
        super().__init__(message)
        self.failure_class = failure_class
        # EVIDENCE-002: a failing call still knows its completed turns and tool calls.
        self.detail = detail or {}


def _package(trial_id, attempt):
    seed = hashlib.sha256(f"{trial_id}:{attempt}".encode()).hexdigest()[:12]
    out = ["FINAL_PRODUCTION_PACKAGE", ""]
    for s in SECTIONS:
        out += [s, f"fake deterministic content for {trial_id} attempt {attempt} [{seed}]", ""]
    return "\n".join(out).strip() + "\n"


def _usage(trial_id, turn, provider):
    """Deterministic pseudo-usage, shaped like the real provider's fields."""
    h = int(hashlib.sha256(f"{trial_id}:{turn}".encode()).hexdigest()[:8], 16)
    inp, out, rsn = 1000 + h % 500, 200 + h % 300, 50 + h % 100
    return {"input_tokens": inp, "cached_input_tokens": h % 40,
            "output_tokens": out, "reasoning_tokens": rsn,
            "raw": {"input_tokens": inp, "output_tokens": out,
                    "cache_read_input_tokens": h % 40, "thinking_tokens": rsn}}


class FakeAdapter:
    """Drop-in replacement for a providers.Adapter. Never touches the network."""

    def __init__(self, model_id, tool_schemas=None, scenario="clean", target_trial=None,
                 model_key="fake", provider="FAKE"):
        self.model_id = model_id
        self.tool_schemas = list(tool_schemas or [])
        self.scenario = scenario
        self.target_trial = target_trial
        self.model_key = model_key
        self.provider = provider
        self.calls = []

    def build_request(self, system_prompt, user_content):
        return {"model": self.model_id, "system": system_prompt,
                "messages": [{"role": "user", "content": user_content}],
                "tools": [t["name"] for t in self.tool_schemas]}

    @staticmethod
    def request_digest(request):
        return hashlib.sha256(
            json.dumps(request, sort_keys=True, default=str).encode()).hexdigest()

    def _turn(self, trial_id, turn, stop="end_turn"):
        u = _usage(trial_id, turn, self.provider)
        return {"turn_index": turn, "provider": self.provider,
                "provider_model_version": self.model_id,
                "provider_request_id": f"fake_req_{trial_id}_{turn}",
                "input_tokens": u["input_tokens"],
                "cached_input_tokens": u["cached_input_tokens"],
                "output_tokens": u["output_tokens"],
                "reasoning_tokens": u["reasoning_tokens"],
                "stop_reason": stop, "latency_ms": 10 + turn,
                "provider_reported_usage": u["raw"]}

    def _tool(self, dispatch, name, args, turn):
        import providers
        return providers._run_tool(dispatch, name, args, turn)

    def call(self, request, dispatch=None, trial_id=None, attempt=0, phase="creative"):
        self.calls.append({"trial_id": trial_id, "attempt": attempt, "phase": phase,
                           "digest": self.request_digest(request),
                           "system": request.get("system"),
                           "user": request["messages"][0]["content"],
                           "tools": request.get("tools", [])})
        hit = self.target_trial is None or trial_id == self.target_trial
        names = {t["name"] for t in self.tool_schemas}

        if self.scenario == "flaky" and hit and attempt == 0:
            raise FakeProviderError("simulated timeout", "timeout")
        if self.scenario == "hard_fail" and hit:
            raise FakeProviderError("simulated 503", "server_error_5xx")
        if self.scenario == "deterministic_fail" and hit:
            raise FakeProviderError("simulated 400 invalid_request", "invalid_request_4xx")
        if self.scenario == "context_overflow" and hit:
            raise FakeProviderError("prompt is too long for the context window",
                                    "context_overflow")
        if self.scenario == "loop_guard" and hit:
            raise FakeProviderError("tool loop guard: 100 provider turns",
                                    "tool_loop_guard_exhausted")
        if self.scenario == "truncated" and hit:
            raise FakeProviderError("provider stop reason 'max_tokens'",
                                    "truncated_response")
        if self.scenario == "repair_flaky" and hit and phase == "repair" \
                and attempt == 1:
            raise FakeProviderError("simulated timeout during format repair", "timeout")

        turns, tool_log, t = [], [], 0
        notes = []

        if self.scenario.startswith("controlled") and dispatch is not None \
                and "canon_search" in names:
            notes.append({"turn_index": 0, "text":
                          "RESEARCH_NEEDS:\n- how to light reflective surfaces\n"
                          "- how to keep spatial clarity in a tight interior\n"
                          "- how to structure information hierarchy in a poster"})
            plan = [("canon_search", {"query": "lighting reflective surfaces", "limit": 8}),
                    ("canon_search", {"query": "spatial clarity interior scene", "limit": 8}),
                    ("canon_search", {"query": "information hierarchy poster", "limit": 8})]
            if self.scenario == "controlled_violation":
                # a 4th search, and this one deliberately UNBOUNDED
                plan.append(("canon_search", {"query": "colour"}))
            for name, args in plan:
                turns.append(self._turn(trial_id, t, stop="tool_use")); t += 1
                _, meta = self._tool(dispatch, name, args, t)
                tool_log.append(meta)
            for iid in ("sk_lsmx_0046", "bnd_lsmx_002", "bnd_lsmx_007"):
                turns.append(self._turn(trial_id, t, stop="tool_use")); t += 1
                _, meta = self._tool(dispatch, "canon_read", {"item_id": iid}, t)
                tool_log.append(meta)
            if self.scenario == "controlled_overflow" and hit:
                raise FakeProviderError("prompt is too long for the context window",
                                        "context_overflow",
                                        {"turns": turns, "tool_calls": tool_log,
                                         "intermediate_text": notes})
            turns.append(self._turn(trial_id, t))
            return {"text": _package(trial_id, attempt), "tool_calls": tool_log,
                    "turns": turns, "intermediate_text": notes,
                    "raw": {"fake": True, "scenario": self.scenario, "phase": phase,
                            "trial_id": trial_id, "attempt": attempt,
                            "model": self.model_id}}

        want_canon = self.scenario in ("canon_user", "tool_user")
        want_web = self.scenario in ("website_user", "tool_user")

        if want_canon and dispatch is not None and "canon_search" in names:
            for name, args in (("canon_catalog", {}),
                               ("canon_search", {"query": "colour hierarchy", "limit": 5})):
                turns.append(self._turn(trial_id, t, stop="tool_use")); t += 1
                _, meta = self._tool(dispatch, name, args, t)
                tool_log.append(meta)

        if want_web and dispatch is not None and "website_read" in names:
            turns.append(self._turn(trial_id, t, stop="tool_use")); t += 1
            _, meta = self._tool(dispatch, "website_read", {}, t)
            tool_log.append(meta)

        turns.append(self._turn(trial_id, t))

        if self.scenario == "malformed" and hit and phase == "creative":
            text = MALFORMED_TEXT
        elif self.scenario == "always_malformed" and hit:
            text = MALFORMED_TEXT
        elif self.scenario == "repair_flaky" and hit and phase == "creative":
            text = MALFORMED_TEXT
        else:
            text = _package(trial_id, attempt)

        return {"text": text, "tool_calls": tool_log, "turns": turns,
                "intermediate_text": notes,
                "raw": {"fake": True, "scenario": self.scenario, "phase": phase,
                        "trial_id": trial_id, "attempt": attempt,
                        "model": self.model_id}}
