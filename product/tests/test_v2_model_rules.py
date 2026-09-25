"""Model rules found by the judges' model trial (2026-09-24).

1. Independence is about who MADE the model, not who hosts it: Kimi, DeepSeek and Mistral served from the Aight Azure
   resource are not OpenAI models, and a Gemini model served anywhere is still Google's.
2. A model that cannot see images must never be given a seeing job: DeepSeek-V4-Flash dropped the attached photos without
   an error and judged the plan blind. Refuse at start-up (configuration) and at the call (media attached).
"""
from __future__ import annotations

import os
import unittest

from product import config
from product.reasoning import AnthropicBackend, AzureOpenAIBackend, ReasoningFailed


def models(**over):
    return {**config.DEFAULT_WORKER_MODELS, **over}


class Maker(unittest.TestCase):
    def test_maker_is_read_from_the_model_name_not_the_host(self):
        self.assertEqual(config.maker("azure_openai:gpt-5.6-sol"), "openai")
        self.assertEqual(config.maker("azure_openai:Kimi-K2.6"), "moonshot")
        self.assertEqual(config.maker("azure_openai:DeepSeek-V4-Flash"), "deepseek")
        self.assertEqual(config.maker("azure_openai:Mistral-Large-3"), "mistral")
        self.assertEqual(config.maker("gemini:gemini-3.1-pro-preview"), "google")
        self.assertEqual(config.maker("anthropic:claude-haiku-4-5"), "anthropic")

    def test_an_unknown_model_falls_back_to_its_host(self):
        self.assertEqual(config.maker("azure_openai:some-new-model"), "openai")

    def test_a_judge_from_another_maker_on_the_chefs_host_is_independent(self):
        config.check_independence(models(head_cook="azure_openai:Kimi-K2.6", gatekeeper="azure_openai:Kimi-K2.6"))

    def test_a_judge_from_the_chefs_maker_is_refused_whatever_the_host(self):
        with self.assertRaises(ValueError):
            config.check_independence(models(gatekeeper="azure_openai:gpt-5.6-luna"))
        with self.assertRaises(ValueError):
            config.check_independence(models(chef="gemini:gemini-3.1-pro-preview", chef_image="gemini:gemini-3.1-pro-preview",
                                             head_cook="vertex:gemini-3.1-pro-preview"))


class Vision(unittest.TestCase):
    def test_a_text_only_model_is_refused_for_any_worker_that_is_shown_pictures(self):
        for w in ("waiter", "chef", "head_cook", "head_cook_av", "gatekeeper"):
            with self.subTest(worker=w), self.assertRaises(ValueError):
                config.check_vision(models(**{w: "azure_openai:DeepSeek-V4-Flash"}))

    def test_a_text_only_model_is_allowed_where_nothing_is_shown(self):
        config.check_vision(models(diary_writer="azure_openai:DeepSeek-V4-Flash"))

    def test_the_text_only_list_can_be_extended_from_the_environment(self):
        os.environ["MI_TEXT_ONLY_MODELS"] = "some-blind-model"
        try:
            self.assertFalse(config.can_see("azure_openai:some-blind-model"))
            self.assertTrue(config.can_see("azure_openai:Kimi-K2.6"))
        finally:
            os.environ.pop("MI_TEXT_ONLY_MODELS")

    def test_the_azure_backend_refuses_media_it_cannot_send_instead_of_dropping_it(self):
        class S:
            def secret(self, name):
                return "x"
        with self.assertRaises(ReasoningFailed):
            AzureOpenAIBackend(S()).send(model="gpt-5.6-sol", system_role="", knowledge=None, user_text="t",
                                         media=[("video/mp4", b"....")], schema_obj={}, max_tokens=10)
        with self.assertRaises(ReasoningFailed):
            AzureOpenAIBackend(S()).send(model="DeepSeek-V4-Flash", system_role="", knowledge=None, user_text="t",
                                         media=[("image/png", b"....")], schema_obj={}, max_tokens=10)
        with self.assertRaises(ReasoningFailed):
            AnthropicBackend(S()).send(model="claude-haiku-4-5", system_role="", knowledge=None, user_text="t",
                                       media=[("video/mp4", b"....")], schema_obj={}, max_tokens=10)


if __name__ == "__main__":
    unittest.main()
