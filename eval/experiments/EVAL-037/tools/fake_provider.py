#!/usr/bin/env python3
"""EVAL-037 — deterministic fake provider.

Exists so the whole runner can be exercised end to end WITHOUT a single real
experimental call. It makes no network request of any kind; there is no SDK import
and no client construction anywhere in this file.

It is scriptable, so the validators can prove the runner obeys the retry contract:

  scenario "clean"          every trial succeeds first attempt
  scenario "flaky"          a named trial fails technically once, then succeeds
  scenario "hard_fail"      a named trial fails technically forever (must stop at 3 attempts)
  scenario "malformed"      a named trial returns a package missing sections once,
                            then returns a well-formed one (exactly one format repair)
  scenario "always_malformed" never well-formed (must NOT repair more than once)
  scenario "canon_user"     the model calls the Canon tools before answering

Determinism: every response is a pure function of (trial_id, attempt_index, scenario).
No clock, no randomness.
"""
import hashlib
import json

SECTIONS = ["DELIVERABLE", "OBJECTIVE_INTERPRETATION", "CORE_CREATIVE_IDEA",
            "MESSAGE_AND_INFORMATION_HIERARCHY", "VISUAL_SYSTEM", "PRODUCTION_RECIPE",
            "GENERATION_PROMPTS", "DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS",
            "AUDIO_AND_EDIT", "FAILURE_PREVENTION", "HARD_CONSTRAINT_CHECK",
            "KNOWLEDGE_AND_WEBSITE_USE"]


class FakeProviderError(RuntimeError):
    def __init__(self, message, failure_class):
        super().__init__(message)
        self.failure_class = failure_class


def _package(trial_id, attempt, sections=SECTIONS):
    seed = hashlib.sha256(f"{trial_id}:{attempt}".encode()).hexdigest()[:12]
    out = ["FINAL_PRODUCTION_PACKAGE", ""]
    for s in sections:
        out += [s, f"fake deterministic content for {trial_id} attempt {attempt} [{seed}]", ""]
    return "\n".join(out).strip() + "\n"


class FakeAdapter:
    """Drop-in replacement for a providers.Adapter. Never touches the network."""

    def __init__(self, model_id, tool_schemas=None, scenario="clean", target_trial=None,
                 model_key="fake", provider="FAKE"):
        self.model_id = model_id
        self.tool_schemas = tool_schemas or []
        self.scenario = scenario
        self.target_trial = target_trial
        self.model_key = model_key
        self.provider = provider
        self.calls = []            # every request this fake ever saw, for assertions

    def build_request(self, system_prompt, user_message):
        return {"model": self.model_id, "system": system_prompt,
                "messages": [{"role": "user", "content": user_message}],
                "tools": [t["name"] for t in self.tool_schemas]}

    @staticmethod
    def request_digest(request):
        return hashlib.sha256(
            json.dumps(request, sort_keys=True, default=str).encode()).hexdigest()

    def call(self, request, canon_dispatch=None, trial_id=None, attempt=0):
        self.calls.append({"trial_id": trial_id, "attempt": attempt,
                           "digest": self.request_digest(request),
                           "system": request.get("system"),
                           "user": request["messages"][0]["content"],
                           "tools": request.get("tools", [])})
        hit = self.target_trial is None or trial_id == self.target_trial

        if self.scenario == "flaky" and hit and attempt == 0:
            raise FakeProviderError("simulated timeout", "timeout")
        if self.scenario == "hard_fail" and hit:
            raise FakeProviderError("simulated 503", "server_error_5xx")

        tool_log = []
        if self.scenario == "canon_user" and canon_dispatch is not None:
            for name, args in (("canon_catalog", {}),
                               ("canon_search", {"query": "colour", "limit": 5})):
                out = canon_dispatch(name, args)
                items = out.get("results") or out.get("sources") or []
                tool_log.append({
                    "name": name,
                    "arguments_digest": hashlib.sha256(
                        json.dumps(args, sort_keys=True).encode()).hexdigest(),
                    "result_item_count": len(items),
                    "accepted_items": sum(1 for i in items if i.get("source_status") == "ACCEPTED"),
                    "hold_items": sum(1 for i in items if i.get("source_status") == "HOLD"),
                    "qa_items": sum(1 for i in items if i.get("kind") == "qa"),
                    "every_item_carried_source_status": all(
                        i.get("source_status") in ("ACCEPTED", "HOLD") for i in items)})

        if self.scenario == "malformed" and hit and attempt == 0:
            text = "Here are three great concepts you could consider.\n"
        elif self.scenario == "always_malformed" and hit:
            text = "Here are three great concepts you could consider.\n"
        else:
            text = _package(trial_id, attempt)
        return {"text": text, "tool_calls": tool_log,
                "raw": {"fake": True, "scenario": self.scenario,
                        "trial_id": trial_id, "attempt": attempt}}
