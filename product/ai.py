"""Every AI worker's call (spec §3, §4, §5, §8, §9).

A call is built from, in this order:
  1. the worker's RULEBOOK CARD (current version) and the OUTPUT FORM schema — the stable prefix, so provider-side prompt
     caching applies (spec §8);
  2. CUSTOMER_EXACT_WORDS — the order slip's brief, byte for byte, on EVERY call (spec §4.1, test 11);
  3. the worker's input forms (named blocks);
  4. its TRAY from the librarian, if any.
It returns exactly one form, validated against its schema and stamped with job_id, form_version, written_by (worker +
model), rulebook_card_version and created_utc. The llm_calls row records the worker, form, card version, the fingerprint
of the exact words carried, the tray ids, and the ESTIMATED cost (token estimate × the configured model's price) — so a
simulated job reports what the reasoning would have cost live (spec §9.4).
Judges (recipe checker, small taster, big taster) can only receive the context blocks listed for them: the chef's
reasoning cannot reach them by construction.
"""
from __future__ import annotations

import json
from decimal import Decimal

from product import rulebook
from product.library import tokens
from product.reasoning import (AnthropicBackend, AzureOpenAIBackend, GeminiBackend, ReasoningFailed, _price)
from product.store import sha256_bytes, sha256_json, utc_now

# Expected answer size and thinking per worker (tokens) — the basis of the cost estimate; measured live values replace
# these once live jobs have run (the ledger records actuals).
EXPECTED_OUT = {"waiter": 1500, "pantry_checker": 1000, "chef": 3500, "recipe_checker": 1500, "small_taster": 350,
                "small_taster_escalation": 500, "big_taster": 1800, "diary_writer": 2000}
EXPECTED_THINKING = {"chef": 2000, "recipe_checker": 1000, "big_taster": 1000, "small_taster_escalation": 500}
BATCH_DISCOUNT = {"diary_writer": Decimal("0.5")}          # the diary writer runs after the job on batch pricing
IMAGE_TOKENS = 1300
VIDEO_TOKENS_PER_S = 300

JUDGE_CONTEXT = {
    "recipe_checker": {"CUSTOMER_EXACT_WORDS", "UNDERSTANDING", "FEASIBILITY", "RECIPE", "TRAY"},
    "small_taster": {"CUSTOMER_EXACT_WORDS", "INSTRUCTION", "MEASUREMENTS", "MEDIA_NOTE"},
    "big_taster": {"CUSTOMER_EXACT_WORDS", "UNDERSTANDING", "MEASUREMENTS", "MEDIA_NOTE", "MANDATORY"},
}


class Workers:
    def __init__(self, settings, store, reasoner, rulebook_obj, simulated):
        self.s, self.store, self.llm, self.rb, self.sim = settings, store, reasoner, rulebook_obj, simulated

    def model_of(self, key: str) -> tuple:
        spec = self.s.models.get(key) or self.s.models[key.replace("_escalation", "")]
        provider, _, model = spec.partition(":")
        return provider, model

    def _backend(self, provider):
        return {"anthropic": AnthropicBackend, "azure_openai": AzureOpenAIBackend, "gemini": GeminiBackend}[provider](self.s)

    def estimate(self, key: str, in_tokens: int) -> tuple:
        provider, model = self.model_of(key)
        pin, pout = _price(model)
        out = EXPECTED_OUT.get(key, 1000) + EXPECTED_THINKING.get(key, 0)
        usd = (Decimal(in_tokens) * pin + Decimal(out) * pout) / Decimal(1_000_000)
        usd *= BATCH_DISCOUNT.get(key, Decimal(1))
        return out, usd.quantize(Decimal("0.000001"))

    def call(self, job_id: str, worker: str, form: str, context: dict, *, exact_words: str, media: list = (),
             tray: dict | None = None, model_key: str | None = None, video_seconds: float = 30.0, sim_args: dict | None = None) -> dict:
        key = model_key or worker
        card_text, card_version = self.rb.card_text(worker, form)
        schema = rulebook.ai_schema(form)
        system = (card_text + f"\n\nOUTPUT FORM `{form}` (version {rulebook.form(form)['version']}). Return ONE JSON object "
                  "matching this JSON Schema, nothing else:\n" + json.dumps(schema, ensure_ascii=False))
        blocks = {"CUSTOMER_EXACT_WORDS": exact_words, **context}
        if tray is not None:
            blocks["TRAY"] = [{"id": i["id"], "section": i["section"], "text": i["text"]} for i in tray["items"]]
        if worker in JUDGE_CONTEXT:
            extra = set(blocks) - JUDGE_CONTEXT[worker]
            if extra:
                raise ReasoningFailed(f"{worker} is an independent judge; refusing context {sorted(extra)}")
        user_chars = sum(len(k) + len(v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)) for k, v in blocks.items())
        media_tokens = sum(IMAGE_TOKENS if m.startswith("image/") else int(VIDEO_TOKENS_PER_S * video_seconds) if m.startswith("video/")
                           else tokens(b.decode("latin-1")) for m, b in media)
        in_tokens = tokens(system) + user_chars // 4 + media_tokens
        out_tokens, est = self.estimate(key, in_tokens)
        provider, model = self.model_of(key)
        record = {"worker": worker, "form": form, "card_version": card_version,
                  "exact_words_sha256": sha256_bytes(exact_words.encode("utf-8")),
                  "tray_ids": json.dumps([i["id"] for i in tray["items"]]) if tray else None,
                  "est_in_tokens": in_tokens, "est_out_tokens": out_tokens, "est_cost_usd": str(est)}
        route = (self._backend(provider), provider, model) if self.s.reasoning_mode == "live" else None
        sim_fn = (lambda: self.sim.respond(worker, form, blocks, list(media), **(sim_args or {})))
        out = self.llm.call(job_id, f"{worker}:{form}", blocks, media=list(media), system_role=system, out_schema=schema,
                            route=route, sim=sim_fn, record=record, isolated=worker in JUDGE_CONTEXT,
                            effort=_effort(key), max_tokens=EXPECTED_OUT.get(key, 1000) * 3)
        call = out.pop("_call", {})
        simulated = out.pop("_simulated", False)
        body = {k: v for k, v in out.items() if not k.startswith("_")}
        body.update({"job_id": job_id, "form": form, "form_version": rulebook.form(form)["version"],
                     "written_by": {"worker": worker, "model": f"{provider}:{model}", "served_by": call.get("model"),
                                    "simulated": simulated},
                     "rulebook_card_version": card_version, "created_utc": utc_now(), "llm_call_id": call.get("id"),
                     "exact_words_sha256": record["exact_words_sha256"], "input_sha256": sha256_json(blocks)[:16]})
        return body


def _effort(key: str):
    from product.config import DEFAULT_EFFORT
    return DEFAULT_EFFORT.get(key)
