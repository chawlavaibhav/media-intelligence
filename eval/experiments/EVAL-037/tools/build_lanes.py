#!/usr/bin/env python3
"""EVAL-037 — generate the eight self-contained lane configs.

Each lane YAML is written to be READ ALONE. An execution worker opens
EXECUTION-CONTRACT.md, its own lane YAML, and the files that lane YAML names.
It never opens a sibling lane config, and a NO_CANON lane never opens
conditions/full-canon.yaml or any Canon path.

That means the lanes deliberately repeat shared facts instead of referring to a
shared file. The duplication is the isolation property, not an oversight; this
generator is what keeps the repeated facts identical.
"""
import hashlib
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = ROOT.parents[2]

BASE_COMMIT = "c6f8d910f7a3cdaaeafa2280313abfb9b898cddd"
FULL_KNOWLEDGE_FP = "cbd321aa3be7464e785a0d42de1764cdccc8bdd33bc023a376740f8f196bde60"
QA_FP = "1313c0babe2194a7bc71c1628f9fbec5fa4f35ca5ff5edc7f594662101dc62bd"

BRIEFS = ["B01", "B02", "B03", "B04", "B05", "B06"]
REPETITIONS = [1, 2, 3]

# brief -> the ONE website snapshot that brief permits. Everything else: none.
BRIEF_WEBSITE = {
    "B01": {"host": "rentok.com", "url": "https://rentok.com"},
    "B02": {"host": "getaight.ai", "url": "https://getaight.ai"},
    "B03": None, "B04": None, "B05": None, "B06": None,
}

MODELS = {
    "sol": {
        "provider": "OpenAI", "model": "gpt-5.6-sol", "api": "Responses API",
        "credential_env": "OPENAI_API_KEY",
        "settings": {"reasoning_effort": "high", "sampling": "provider defaults"},
        "settings_note": ("reasoning.effort=high on the Responses API. Sampling parameters are "
                          "left at provider defaults and must not be set explicitly."),
    },
    "sonnet": {
        "provider": "Anthropic", "model": "claude-sonnet-5", "api": "Messages API",
        "credential_env": "ANTHROPIC_API_KEY",
        "settings": {"thinking": "adaptive", "effort": "high", "sampling": "provider defaults"},
        "settings_note": ("Adaptive thinking with effort=high. Sampling parameters are left at "
                          "provider defaults and must not be set explicitly."),
    },
    "haiku": {
        "provider": "Anthropic", "model": "claude-haiku-4-5-20251001", "api": "Messages API",
        "credential_env": "ANTHROPIC_API_KEY",
        "settings": {"thinking": {"type": "enabled", "budget_tokens": 8000},
                     "sampling": "provider defaults"},
        "settings_note": ("Extended thinking enabled with an explicit 8000-token budget. Sampling "
                          "parameters are left at provider defaults and must not be set explicitly."),
    },
    "gemma": {
        "provider": "Google Gemini API", "model": "gemma-4-31b-it", "api": "Gemini API",
        "credential_env": "GEMINI_API_KEY",
        "settings": {"sampling": "provider defaults", "reasoning": "provider defaults"},
        "settings_note": ("Provider defaults throughout. Do NOT invent or pass unsupported "
                          "reasoning controls: there is no thinking budget, no effort parameter "
                          "and no reasoning_effort on this model. If a control is not documented "
                          "for gemma-4-31b-it, it is not set."),
    },
}

CONDITIONS = ["no-canon", "full-canon"]


def trial_plan(lane_id):
    """The exact 18 trials, in the exact order the worker must execute them.

    Repetition-major: all six briefs at repetition 1, then 2, then 3. The three
    repetitions of a brief are therefore maximally separated in execution order.
    Trials are independent regardless - every one is a fresh stateless request -
    but the ordering makes any accidental carry-over visible rather than hidden.
    """
    rows, i = [], 0
    for rep in REPETITIONS:
        for b in BRIEFS:
            i += 1
            rows.append({"order_index": i, "trial_id": f"E037-{lane_id}-{b}-R{rep}",
                         "brief_id": b, "repetition": rep})
    return rows


def sha256(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def build(model_key, cond_key):
    lane_id = f"{model_key}-{cond_key}"
    m = MODELS[model_key]
    full = cond_key == "full-canon"
    condition = "FULL_CANON" if full else "NO_CANON"
    plan = trial_plan(lane_id)
    L = []
    w = L.append

    w(f"# EVAL-037 lane: {lane_id}")
    w("#")
    w("# SELF-CONTAINED. This file plus EXECUTION-CONTRACT.md plus the files named below")
    w("# are everything this worker may read. Do not open a sibling lane config. Do not")
    w("# look at another EVAL-037 branch, PR, log, output or report.")
    if not full:
        w("#")
        w("# THIS IS A NO_CANON LANE. Do NOT read conditions/full-canon.yaml. Do NOT read")
        w("# anything under canon/. Do NOT import tools/canon_tools.py. The tested model")
        w("# receives no Canon instruction and no Canon tool.")
    w("")
    w("experiment: EVAL-037")
    w(f"lane_id: {lane_id}")
    w(f"branch: work/eval-037-{lane_id}")
    w(f"base_commit: {BASE_COMMIT}")
    w("base_commit_note: >-")
    w("  The frozen common substrate. Start from exactly this commit. If your HEAD's")
    w("  merge-base with this commit is not this commit, stop and escalate.")
    w("")
    w("model:")
    w(f"  key: {model_key}")
    w(f"  provider: {m['provider']}")
    w(f"  model_id: {m['model']}")
    w(f"  api: {m['api']}")
    w(f"  credential_env: {m['credential_env']}")
    w("  moving_alias: false")
    w("  alias_policy: >-")
    w("    This exact model id, never a moving alias and never a substitute. Preflight the")
    w("    id against the provider before the first trial. If it is unavailable, STOP and")
    w("    report. Substituting a different model silently destroys the comparison.")
    w("  settings:")
    for k, v in m["settings"].items():
        if isinstance(v, dict):
            w(f"    {k}:")
            for kk, vv in v.items():
                w(f"      {kk}: {vv}")
        else:
            w(f"    {k}: {v}")
    w("  settings_note: >-")
    for line in _wrap(m["settings_note"]):
        w(f"    {line}")
    w("")
    w(f"condition: {condition}")
    if full:
        w("condition_detail:")
        w("  canon_instruction: present")
        w("  addendum_path: conditions/full-canon.yaml")
        w("  addendum_key: addendum")
        w("  addendum_placement: >-")
        w("    Appended to the common system prompt, after its final line, separated by one")
        w("    blank line. The customer brief is the user message. Nothing else is added.")
        w("  canon_tools_exposed:")
        w("    - canon_catalog")
        w("    - canon_search")
        w("    - canon_read")
        w("  canon_tools_module: tools/canon_tools.py")
        w("  canon_tools_access: read-only")
        w("  corpus:")
        w("    roots:")
        w("      accepted: canon/knowledge/current")
        w("      hold: canon/candidates/canon-014")
        w("      qa: canon/qa/canon-014")
        w("    index: canon/knowledge/CANON-CORPUS-INDEX.yaml")
        w("  fingerprints:")
        w("    algorithm: sha256-of-sorted-path-and-content")
        w("    full_knowledge:")
        w("      file_count: 193")
        w(f"      combined_digest: {FULL_KNOWLEDGE_FP}")
        w("    qa:")
        w("      file_count: 23")
        w(f"      combined_digest: {QA_FP}")
        w("    verify_at_preflight: true")
        w("    on_mismatch: stop")
        w("  status_invariants:")
        w("    - Every returned object carries source_status.")
        w("    - source_status is ACCEPTED or HOLD, taken from the corpus, never inferred.")
        w("    - HOLD is never represented, relabelled or defaulted as accepted.")
        w("    - An object whose status cannot be established is not returned.")
        w("    - Q&A is accessible knowledge, not independent corroboration and not benchmark truth.")
        w("  model_discretion:")
        w("    # The model decides all of this. The harness imposes none of it.")
        w("    - whether to use Canon at all")
        w("    - what to search")
        w("    - what to read")
        w("    - whether to consume Q&A")
        w("    - how much to retrieve")
        w("    - when to stop")
        w("  no_aggregate_top_k: true")
        w("  no_canon_token_budget: true")
        w("  no_retrieval_count_budget: true")
        w("  mandatory_canon_use: false")
    else:
        w("condition_detail:")
        w("  canon_instruction: absent")
        w("  addendum_path: null")
        w("  canon_tools_exposed: []")
        w("  forbidden_reads:")
        w("    - conditions/full-canon.yaml")
        w("    - tools/canon_tools.py")
        w("    - canon/**")
        w("  forbidden_reads_note: >-")
        w("    The execution worker must not read the FULL_CANON condition file or any Canon")
        w("    content. The tested model is given the common system prompt and the brief, and")
        w("    nothing else. Reading Canon here would contaminate the control condition.")
    w("")
    w("prompt:")
    w("  system_prompt_path: common/system-prompt.txt")
    w(f"  system_prompt_sha256: {sha256(ROOT / 'common/system-prompt.txt')}")
    if full:
        w("  system_prompt_composition: common/system-prompt.txt + FULL_CANON addendum")
    else:
        w("  system_prompt_composition: common/system-prompt.txt verbatim, nothing appended")
    w("  user_message: the brief file's contents, verbatim, and nothing else")
    w("  no_few_shot_examples: true")
    w("  no_lane_specific_prompt_text: true")
    w("")
    w("briefs:")
    for b in BRIEFS:
        w(f"  {b}:")
        w(f"    path: common/briefs/{b}.txt")
        w(f"    sha256: {sha256(ROOT / f'common/briefs/{b}.txt')}")
        site = BRIEF_WEBSITE[b]
        if site:
            host = site["host"]
            w("    website:")
            w(f"      permitted_url: {site['url']}")
            w(f"      snapshot_dir: common/websites/{host}")
            w(f"      snapshot_html: common/websites/{host}/index.html")
            w(f"      snapshot_html_sha256: {sha256(ROOT / f'common/websites/{host}/index.html')}")
            w(f"      snapshot_text: common/websites/{host}/page.txt")
            w(f"      snapshot_text_sha256: {sha256(ROOT / f'common/websites/{host}/page.txt')}")
            w("      live_browsing: forbidden")
            w("      model_decides_whether_to_inspect: true")
        else:
            w("    website: null")
            w("    website_note: this brief permits no website")
    w("")
    w("websites:")
    w("  live_browsing_during_experimental_calls: forbidden")
    w("  other_websites: forbidden")
    w("  snapshots_taken: once, during the EVAL-037 setup/freeze task")
    w("  manifest: common/websites/WEBSITE-SNAPSHOT-MANIFEST.yaml")
    w("")
    w("execution:")
    w("  briefs: 6")
    w("  repetitions: 3")
    w("  trials: 18")
    w("  trial_count_is_exact: true")
    w("  one_model_one_condition_per_session: true")
    w("  fresh_provider_context_per_trial: true")
    w("  carry_state_between_trials: forbidden")
    w("  creative_quality_judging: forbidden")
    w("  media_generation: forbidden")
    w("  order_note: >-")
    w("    Execute in the order given. Repetition-major, so the three repetitions of a")
    w("    brief are maximally separated. Every trial is a fresh stateless request")
    w("    regardless.")
    w("  trials_plan:")
    for t in plan:
        w(f"    - order_index: {t['order_index']}")
        w(f"      trial_id: {t['trial_id']}")
        w(f"      brief_id: {t['brief_id']}")
        w(f"      repetition: {t['repetition']}")
        w(f"      brief_path: common/briefs/{t['brief_id']}.txt")
        site = BRIEF_WEBSITE[t["brief_id"]]
        w(f"      website_snapshot: {('common/websites/' + site['host']) if site else 'null'}")
    w("")
    w("retry_policy:")
    w("  technical_failure:")
    w("    initial_attempt: 1")
    w("    max_technical_retries: 2")
    w("    max_total_attempts_from_technical: 3")
    w("    qualifying_classes:")
    w("      - timeout")
    w("      - connection_error")
    w("      - rate_limit")
    w("      - server_error_5xx")
    w("      - empty_response")
    w("      - truncated_response")
    w("      - provider_refusal_non_content")
    w("      - sdk_error")
    w("    on_exhaustion: >-")
    w("      Record the trial as failed_technical with every attempt retained. Do not")
    w("      substitute a model, relax a setting or hand-write a package.")
    w("  format_repair:")
    w("    max: 1")
    w("    scope: format only")
    w("    permitted_when: >-")
    w("      The response is present and substantive but does not carry the required")
    w("      FINAL_PRODUCTION_PACKAGE section structure.")
    w("    forbidden: >-")
    w("      Changing, steering, enriching or improving the creative content. A format")
    w("      repair may ask only for the same answer in the required shape.")
    w("  forbidden_retry_reasons:")
    w("    - the answer looks creatively weak")
    w("    - the idea seems unoriginal or safe")
    w("    - the package is shorter than expected")
    w("    - a different sample would probably be better")
    w("    - the model did not use Canon" if full else "    - the model used no website")
    w("  forbidden_retry_note: >-")
    w("    Creative weakness is NEVER a reason for another attempt. Retrying on quality")
    w("    silently selects the best-of-N and destroys the comparison this experiment exists")
    w("    to make.")
    w("")
    w("spend:")
    w("  experiment_level_cap: none")
    w("  note: >-")
    w("    EVAL-037 has no experiment-level spend cap. Cost is recorded, not enforced.")
    w("")
    w("evidence:")
    w(f"  root: eval/experiments/EVAL-037/runs/{lane_id}")
    w(f"  attempt_ledger: eval/experiments/EVAL-037/runs/{lane_id}/attempt-ledger.json")
    w("  attempt_ledger_schema: schemas/attempt-ledger.schema.json")
    w(f"  result: eval/experiments/EVAL-037/runs/{lane_id}/result.json")
    w("  result_schema: schemas/result.schema.json")
    w(f"  raw_responses: eval/experiments/EVAL-037/runs/{lane_id}/raw/")
    w(f"  packages: eval/experiments/EVAL-037/runs/{lane_id}/packages/")
    w("  retention: >-")
    w("    Retain every output regardless of apparent quality, including outputs from")
    w("    failed and repaired attempts. Nothing is deleted, trimmed or tidied.")
    w("  validator: validators/validate_lane_run.py")
    w("")
    w("downstream:")
    w("  all_valid_packages_eligible_for_media_generation: true")
    w("  media_generation_in_scope: false")
    w("  acceptance_scoring_in_scope: false")
    w("  note: >-")
    w("    Media generation and final acceptance scoring are explicitly outside EVAL-037.")
    w("    Eligibility is never withdrawn on creative grounds.")
    w("")
    w("worker_obligations:")
    w("  - Start from the exact base_commit above.")
    w("  - Read only EXECUTION-CONTRACT.md, this lane YAML, and files this YAML names.")
    w("  - Never list or read a sibling lane config.")
    w("  - Never inspect another EVAL-037 execution branch, PR, log, output or report.")
    w("  - Preflight the exact model id; stop rather than substitute if unavailable.")
    if full:
        w("  - Preflight both Canon fingerprints; stop on mismatch.")
    w("  - Freeze and commit the runner BEFORE the first experimental call.")
    w("  - Make no runner, prompt or config change after the first call.")
    w("  - Execute exactly 18 trials, in the listed order.")
    w("  - Use a fresh stateless provider request for every trial.")
    w("  - Never pass output or state from one trial into another.")
    w("  - Retain every output regardless of apparent quality.")
    w("  - Do no creative judging.")
    w("  - Generate no media.")
    w("")
    return lane_id, "\n".join(L) + "\n"


def _wrap(s, width=88):
    words, lines, cur = s.split(), [], ""
    for word in words:
        if len(cur) + len(word) + 1 > width:
            lines.append(cur); cur = word
        else:
            cur = f"{cur} {word}".strip()
    if cur:
        lines.append(cur)
    return lines


def main():
    out = ROOT / "lanes"
    out.mkdir(exist_ok=True)
    written = []
    for mk in MODELS:
        for ck in CONDITIONS:
            lane_id, text = build(mk, ck)
            (out / f"{lane_id}.yaml").write_text(text, encoding="utf-8")
            written.append(lane_id)
    print(f"wrote {len(written)} lane configs: {', '.join(written)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
