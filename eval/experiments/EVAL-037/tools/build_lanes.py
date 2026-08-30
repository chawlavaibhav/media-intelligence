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
sys.path.insert(0, str(HERE))
FULL_KNOWLEDGE_FP = "cbd321aa3be7464e785a0d42de1764cdccc8bdd33bc023a376740f8f196bde60"
QA_FP = "1313c0babe2194a7bc71c1628f9fbec5fa4f35ca5ff5edc7f594662101dc62bd"

def _common_digest():
    """Computed at generation time, so a tools/ or prompt change forces a lane rebuild."""
    import freeze_fingerprint as FF
    return FF.compute_common()[0]


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

COMMON_FP = None  # filled in main() from the live substrate bytes


def trial_plan(lane_id):
    """The exact 18 trials, in the frozen deterministic pseudo-random order.

    Order = sort every trial id by sha256("EVAL-037|" + trial_id).

    This decorrelates execution position from brief and from repetition, so a
    position effect (provider warm-up, drift, rate-limit shaping) cannot line up with
    a brief or a repetition. It is deterministic and independently recomputable: the
    validator recomputes the whole ordering rather than checking order_index runs
    1..18, which would pass for any ordering at all.
    """
    ids = [f"E037-{lane_id}-{b}-R{rep}" for rep in REPETITIONS for b in BRIEFS]
    ids.sort(key=lambda t: hashlib.sha256(("EVAL-037|" + t).encode()).hexdigest())
    rows = []
    for i, tid in enumerate(ids, 1):
        b = tid.split("-")[-2]
        rep = int(tid.split("-R")[-1])
        rows.append({"order_index": i, "trial_id": tid, "brief_id": b, "repetition": rep})
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
    w("")
    w("substrate:")
    w("  # The experiment-defining BYTES are the authority, not a commit SHA. The")
    w("  # substrate was authored after the Canon merge, so no commit can contain both")
    w("  # itself and its own fingerprint; requiring one would be self-referential.")
    w("  algorithm: sha256-of-sorted-path-and-content")
    w(f"  common_substrate_digest: {COMMON_FP}")
    w("  common_substrate_scope: eval/experiments/EVAL-037/** excluding lanes/, runs/, dotfiles")
    w("  common_substrate_note: >-")
    w("    Safe to embed here because lanes/ is outside its scope. This is the digest")
    w("    this lane verifies on its own: prompt, briefs, website snapshots, conditions,")
    w("    schemas, tools and validators. Recompute and STOP on mismatch.")
    w("  freeze_fingerprint_file: FREEZE-FINGERPRINT.yaml")
    w("  freeze_fingerprint_note: >-")
    w("    The whole-substrate fingerprint covers lanes/ too, so it cannot be embedded")
    w("    in a lane without self-reference. It lives in FREEZE-FINGERPRINT.yaml, is")
    w("    recorded in the controller approval, and is verified with")
    w("    `tools/freeze_fingerprint.py --check` before dispatch.")
    w(f"  canon_base_commit: {BASE_COMMIT}")
    w("  canon_base_commit_role: >-")
    w("    Canon provenance only. This is the CANON-014 merge the two corpus")
    w("    fingerprints were computed against. It does NOT contain EVAL-037 and is not")
    w("    the execution-lane starting commit.")
    w("  execution_checkout_requirement: >-")
    w("    Run from any checkout that contains the approved frozen substrate (verified")
    w("    by freeze_fingerprint) and has canon_base_commit as an ancestor.")
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
    w("website_tool:")
    w("  name: website_read")
    w("  access: read-only")
    w("  module: tools/website_tools.py")
    w("  exposed_for_briefs: [B01, B02]")
    w("  not_exposed_for_briefs: [B03, B04, B05, B06]")
    w("  identical_across_conditions: true")
    w("  condition_independence_note: >-")
    w("    Website access is a property of the BRIEF, not of the condition. This tool is")
    w("    exposed identically in NO_CANON and FULL_CANON, and serves byte-identical")
    w("    snapshot content in both. It is not a Canon tool and carries no Canon")
    w("    semantics.")
    w("  returns:")
    w("    - the frozen page.txt for the website that brief permits")
    w("    - the snapshot sha256 actually served")
    w("    - the source URL")
    w("  live_browsing: forbidden")
    w("  other_domains: refused")
    w("  model_decides_whether_to_call: true")
    w("  recording: >-")
    w("    Every call is recorded with its arguments and the exact snapshot digest")
    w("    returned. website_snapshot_used is derived from actual calls and is never")
    w("    hardcoded.")
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
    w("  # A retry is licensed ONLY by a TRANSIENT provider failure. Deterministic")
    w("  # failures are recorded and never resampled — resampling them would be")
    w("  # creative resampling wearing a technical retry's clothes.")
    w("  transient_failure:")
    w("    initial_attempt: 1")
    w("    max_technical_retries: 2")
    w("    max_total_attempts_from_transient: 3")
    w("    retry_resends: the identical request, unchanged")
    w("    classes:")
    w("      - timeout")
    w("      - connection_error")
    w("      - rate_limit_429")
    w("      - server_error_5xx")
    w("    on_exhaustion: >-")
    w("      Record the trial as failed_technical with every attempt retained. Do not")
    w("      substitute a model, relax a setting or hand-write a package.")
    w("  deterministic_failure:")
    w("    retries: 0")
    w("    status: failed_execution")
    w("    classes:")
    w("      - invalid_request_4xx")
    w("      - auth_error")
    w("      - tool_schema_rejected")
    w("      - context_overflow")
    w("      - tool_loop_guard_exhausted")
    w("      - model_refusal")
    w("      - truncated_response")
    w("      - empty_response")
    w("      - sdk_error")
    w("    note: >-")
    w("      A stable 4xx caused by request, configuration or tool schema; context")
    w("      exhaustion; tool-loop exhaustion; provider truncation; or model refusal is")
    w("      recorded distinctly and receives NO automatic resampling. Context overflow")
    w("      or tool-loop exhaustion caused by the model's own retrieval is a")
    w("      model+condition EXECUTION FAILURE and is a real result of this experiment,")
    w("      not a transient provider fault.")
    w("  truncation_detection: >-")
    w("    Detected from the provider's own stop/finish reason, not inferred from missing")
    w("    section headings.")
    w("  format_repair:")
    w("    max: 1")
    w("    scope: format only")
    w("    request_contains:")
    w("      - the original customer brief")
    w("      - the original model answer, verbatim")
    w("      - exactly the frozen format-only instruction")
    w("    must_not_contain:")
    w("      - any other trial")
    w("      - any new creative guidance")
    w("    records: repair_source_response_digest")
    w("    permitted_when: >-")
    w("      The response is present and substantive but does not carry the required")
    w("      FINAL_PRODUCTION_PACKAGE section structure.")
    w("    on_transient_failure_during_repair: >-")
    w("      Retry THAT SAME format-repair request under the transient retry policy. It")
    w("      must NEVER fall back to a fresh creative generation.")
    w("    if_repair_still_invalid:")
    w("      retain_output: true")
    w("      status: failed_format")
    w("      eligible_for_media_generation: false")
    w("      note: An invalid repair is never labelled format_repaired.")
    w("  forbidden_retry_reasons:")
    w("    - the answer looks creatively weak")
    w("    - the idea seems unoriginal or safe")
    w("    - the package is shorter than expected")
    w("    - a different sample would probably be better")
    w("    - the model did not use Canon" if full else "    - the model did not read the website")
    w("  forbidden_retry_note: >-")
    w("    Creative weakness is NEVER a reason for another attempt. Retrying on quality")
    w("    silently selects the best-of-N and destroys the comparison this experiment exists")
    w("    to make.")
    w("")
    w("tool_loop_guard:")
    w("  max_provider_turns: 100")
    w("  purpose: emergency stop against literal runaway execution")
    w("  is_a_retrieval_budget: false")
    w("  note: >-")
    w("    The model may retrieve as much as it wants below this. Hitting the guard is a")
    w("    model+condition execution failure, preserved as such, and never rerun as a")
    w("    transient provider failure.")
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
    w(f"  raw_requests: eval/experiments/EVAL-037/runs/{lane_id}/requests/")
    w(f"  raw_responses: eval/experiments/EVAL-037/runs/{lane_id}/raw/")
    w(f"  tool_transcripts: eval/experiments/EVAL-037/runs/{lane_id}/transcripts/")
    w("  transcript_note: >-")
    w("    Every provider invocation retains its EXACT serialised request, not only a")
    w("    digest. Every tool call retains its real arguments, per-item identity")
    w("    (item id, source id, source_status, kind, Q&A flag) and the full tool result,")
    w("    so a later session can reconstruct exactly what the model asked for and got.")
    w("  usage_note: >-")
    w("    Usage is recorded per PROVIDER TURN, including every intermediate turn caused")
    w("    by a tool call, and summed to trial and lane totals. A field the provider does")
    w("    not expose is null; nothing is invented.")
    w("  price_snapshot: common/price-snapshot.yaml")
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
    w("  - Run from a checkout containing the approved frozen substrate; verify the")
    w("    common_substrate_digest above and the freeze fingerprint before dispatch.")
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
    global COMMON_FP
    COMMON_FP = _common_digest()
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
