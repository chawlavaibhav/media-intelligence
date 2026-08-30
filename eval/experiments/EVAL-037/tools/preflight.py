#!/usr/bin/env python3
"""EVAL-037 — model preflight. Verifies the EXACT model id is served.

This is a capability/availability check, NOT an experimental call: it never sends a
brief, never sends the EVAL-037 system prompt, and its output is never recorded as a
trial. Where a provider offers a model-listing endpoint it uses that and sends no
generation request at all.

The rule it exists to enforce: if the exact model id is unavailable, STOP. Do not
substitute a neighbouring model, a moving alias, or a dated sibling. A substituted
model silently destroys the comparison EVAL-037 exists to make.

  python3 tools/preflight.py --lane lanes/sonnet-full-canon.yaml
"""
import argparse
import os
import pathlib
import sys

import yaml

MOVING_ALIAS_MARKERS = ("latest", "-preview", "@latest")


def check_openai(model_id):
    from openai import OpenAI
    ids = {m.id for m in OpenAI(api_key=os.environ["OPENAI_API_KEY"]).models.list()}
    return model_id in ids, sorted(i for i in ids if i.startswith("gpt-5"))[:15]


def check_anthropic(model_id):
    import anthropic
    ids = {m.id for m in anthropic.Anthropic(
        api_key=os.environ["ANTHROPIC_API_KEY"]).models.list(limit=100)}
    return model_id in ids, sorted(ids)[:15]


def check_gemini(model_id):
    from google import genai
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    ids = {m.name.split("/")[-1] for m in client.models.list()}
    return model_id in ids, sorted(i for i in ids if "gemma" in i)[:15]


CHECKS = {"OpenAI": check_openai, "Anthropic": check_anthropic,
          "Google Gemini API": check_gemini}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    a = ap.parse_args()
    lane = yaml.safe_load(pathlib.Path(a.lane).read_text(encoding="utf-8"))
    m = lane["model"]
    print(f"lane      : {lane['lane_id']}")
    print(f"provider  : {m['provider']}")
    print(f"model id  : {m['model_id']}")

    for marker in MOVING_ALIAS_MARKERS:
        if marker in m["model_id"]:
            print(f"FAIL: {m['model_id']!r} looks like a moving alias ({marker!r}). "
                  "EVAL-037 forbids moving aliases.", file=sys.stderr)
            return 2

    cred = m["credential_env"]
    if not os.environ.get(cred):
        print(f"FAIL: {cred} is not set.", file=sys.stderr)
        return 2

    try:
        ok, nearby = CHECKS[m["provider"]](m["model_id"])
    except Exception as e:  # noqa: BLE001
        print(f"FAIL: could not list models: {e}", file=sys.stderr)
        return 2

    if not ok:
        print(f"FAIL: {m['model_id']!r} is NOT available.", file=sys.stderr)
        print(f"      nearby ids: {nearby}", file=sys.stderr)
        print("      STOP. Do not substitute. Escalate to the controller.", file=sys.stderr)
        return 2
    print("model available: yes")

    # No model-specific capability gate. Gemma 4 documents both function calling and
    # system instructions, so there is nothing special to assert here — every lane gets
    # the same exact-model preflight. If the live endpoint nevertheless rejects this
    # lane's exact tool configuration at run time, the runner records the concrete API
    # error and the lane STOPS. It never substitutes another model.
    return 0


if __name__ == "__main__":
    sys.exit(main())
