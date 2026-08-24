#!/usr/bin/env node
// EVAL-002 · Local evaluation harness — SYNTHETIC FIXTURES ONLY.
//
// What this proves: that a test item can flow through evaluation and come out as a traceable,
// aggregated result which obeys the counting rules the approved battery requires.
// What this does NOT prove: anything about any model. It makes no network call and reads no real
// generated media. Every input is hand-written mock data.
//
// Usage:
//   node eval/harness/run-fixture.mjs --fixture <file.json> [--out <dir>] [--check]
//   node eval/harness/run-fixture.mjs --all [--out <dir>] [--check]

import { readFileSync, writeFileSync, readdirSync, existsSync, mkdirSync } from "node:fs";
import { join, resolve, basename, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { scoreTranscription, norm, loadItems, parseArgs, DEFAULT_TARGET } from "../scripts/check-vlm.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));

// --- vocabularies fixed by the approved design; the harness may not invent members -------------
const OBSERVATION_UNITS = ["frame", "shot", "shot_pair", "sequence", "whole_asset", "asset_set_over_time"];
const INSTRUMENT_STATES = ["calibrated", "provisional_uncalibrated", "published_calibration_only",
                           "deterministic", "required_but_no_calibrated_instrument"];
/** Only a `calibrated` or `deterministic` instrument may produce a Registry-eligible number. */
const REGISTRY_ELIGIBLE_STATES = ["calibrated", "deterministic"];
const APPROVED_V0_DIMENSIONS = ["exact_text_devanagari", "exact_text_latin",
  "person_identity_across_prompts", "object_count", "spatial_relationship",
  "text_stability_across_frames", "operational_behaviour"];

const problems = [];
const fail = (code, msg) => problems.push({ severity: "error", code, msg });
const warn = (code, msg) => problems.push({ severity: "warning", code, msg });

// --- scoring -----------------------------------------------------------------------------------

/** Derive a verdict for one scored dimension, using the real checker code where applicable. */
function evaluateScored(sc, item) {
  // Text dimensions: run the ACTUAL judgement function from check-vlm.mjs, so the harness
  // exercises production code rather than a reimplementation of it.
  if (sc.score_via === "check-vlm.scoreTranscription") {
    const r = scoreTranscription(sc.transcription, item.target);
    return { verdict: r.exact_match ? "pass" : "fail", detail: r };
  }
  // Sequence dimensions: correctness and stability are two independent results.
  if (Array.isArray(sc.frame_transcriptions)) {
    const normed = sc.frame_transcriptions.map(norm);
    const distinct = [...new Set(normed)];
    const stable = distinct.length === 1;
    const modal = distinct
      .map((v) => [v, normed.filter((x) => x === v).length])
      .sort((a, b) => b[1] - a[1])[0][0];
    const correct = modal === norm(item.target);
    return {
      verdict: correct && stable ? "pass" : "fail",
      detail: { correctness: correct ? "pass" : "fail", stability: stable ? "pass" : "fail",
                distinct_readings: distinct.length, frames_sampled: sc.frames_sampled ?? normed.length },
    };
  }
  return { verdict: sc.verdict ?? "not_measured", detail: sc.results ?? null };
}

/** Cost fields must be an explicit number or an explicit "not measured" — never guessed. */
function auditCost(cost, where) {
  const out = {};
  for (const k of ["usd_per_call", "usd_per_evaluation", "usd_human_verification_per_trial"]) {
    const v = cost?.[k];
    if (v === undefined) { warn("COST_FIELD_ABSENT", `${where}: cost field '${k}' absent; recorded as not_measured`); out[k] = null; out[`${k}_state`] = "not_measured"; }
    else if (v === null)  { out[k] = null; out[`${k}_state`] = "not_measured"; }
    else if (typeof v === "number") { out[k] = v; out[`${k}_state`] = "fixture_value"; }
    else { fail("COST_FIELD_INVALID", `${where}: cost field '${k}' is neither a number nor null`); out[k] = null; out[`${k}_state`] = "invalid"; }
  }
  out.currency = cost?.currency ?? null;
  return out;
}

function runFixture(fx, path) {
  if (fx.SYNTHETIC_FIXTURE !== true) fail("NOT_LABELLED_SYNTHETIC", `${basename(path)}: fixture is not labelled SYNTHETIC_FIXTURE:true`);
  const items = Object.fromEntries(fx.items.map((i) => [i.item_id, i]));
  const rows = [];

  for (const t of fx.trials) {
    const item = items[t.item_id];
    if (!item) { fail("UNKNOWN_ITEM", `trial ${t.trial_id} references unknown item ${t.item_id}`); continue; }
    if (!OBSERVATION_UNITS.includes(item.observation_unit))
      fail("BAD_OBSERVATION_UNIT", `${item.item_id}: '${item.observation_unit}' is not in the SPEC-04 vocabulary`);

    for (const sc of t.scored) {
      const st = sc.instrument?.state;
      if (!INSTRUMENT_STATES.includes(st)) fail("BAD_INSTRUMENT_STATE", `${t.trial_id}/${sc.dimension}: unknown instrument state '${st}'`);
      if (!APPROVED_V0_DIMENSIONS.includes(sc.dimension))
        warn("NON_V0_DIMENSION", `${t.trial_id}: '${sc.dimension}' is not one of the seven approved V0 dimensions`);

      const ev = evaluateScored(sc, item);
      rows.push({
        trial_id: t.trial_id,
        item_id: t.item_id,
        repeat_index: t.repeat_index ?? 0,
        generation_ref: t.generation_ref,
        dimension: sc.dimension,
        difficulty_level: item.difficulty_level ?? null,
        observation_unit: item.observation_unit,
        // A sequence trial yields ONE observation however many frames were sampled.
        observations: 1,
        frames_sampled: sc.frames_sampled ?? (sc.frame_transcriptions?.length ?? null),
        instrument: sc.instrument,
        registry_eligible: REGISTRY_ELIGIBLE_STATES.includes(st),
        verdict: ev.verdict,
        detail: ev.detail,
        defects: sc.defects ?? [],
        defect_count: (sc.defects ?? []).length,
        cost: auditCost(sc.cost, `${t.trial_id}/${sc.dimension}`),
      });
    }
  }
  return rows;
}

function aggregate(rows) {
  const distinctGenerations = new Set(rows.map((r) => r.generation_ref));
  const byDim = {};

  for (const r of rows) {
    const d = (byDim[r.dimension] ??= {
      dimension: r.dimension, observation_unit: r.observation_unit,
      items: new Set(), trials: new Set(), generations: new Set(),
      observations: 0, passes: 0, fails: 0, not_measured: 0,
      defect_terms: {}, registry_eligible: true, instrument_states: new Set(),
    });
    d.items.add(r.item_id);
    d.trials.add(r.trial_id);
    d.generations.add(r.generation_ref);
    d.observations += r.observations;
    if (r.verdict === "pass") d.passes++;
    else if (r.verdict === "not_measured") d.not_measured++;
    else d.fails++;
    for (const df of r.defects) d.defect_terms[df.term] = (d.defect_terms[df.term] ?? 0) + 1;
    if (!r.registry_eligible) d.registry_eligible = false;
    d.instrument_states.add(r.instrument?.state ?? "unknown");
  }

  // --- the correlation rule, enforced ---------------------------------------------------------
  // Within one dimension, one generation may back at most one trial.
  for (const d of Object.values(byDim)) {
    if (d.generations.size !== d.trials.size)
      fail("GENERATION_DOUBLE_COUNTED",
        `${d.dimension}: ${d.trials.size} trials but only ${d.generations.size} distinct generations — a generation is being counted more than once as an independent trial`);
  }
  // Across dimensions, sharing is legal and must be reported rather than summed away.
  const genToDims = {};
  for (const r of rows) (genToDims[r.generation_ref] ??= new Set()).add(r.dimension);
  const shared = Object.entries(genToDims).filter(([, s]) => s.size > 1)
    .map(([g, s]) => ({ generation_ref: g, dimensions: [...s] }));

  const dimensions = Object.values(byDim).map((d) => {
    const scored = d.passes + d.fails;
    return {
      dimension: d.dimension,
      observation_unit: d.observation_unit,
      n_items: d.items.size,            // independence is counted on ITEMS
      n_trials: d.trials.size,          // attempts, including repeats
      n_generations: d.generations.size,
      n_observations: d.observations,
      passes: d.passes, fails: d.fails, not_measured: d.not_measured,
      pass_rate: scored ? +(d.passes / scored).toFixed(4) : null,
      pass_rate_basis: scored ? `${d.passes}/${scored} scored trials across ${d.items.size} independent item(s)` : "no scored trials",
      defect_terms: d.defect_terms,
      instrument_states: [...d.instrument_states],
      registry_eligible: d.registry_eligible,
      registry_note: d.registry_eligible ? "instrument state permits a Registry entry"
        : "NOT Registry-eligible: instrument is not calibrated/deterministic (EVAL-001 rule)",
    };
  }).sort((a, b) => a.dimension.localeCompare(b.dimension));

  // A run that failed its own integrity checks may not present ANY dimension as Registry-eligible,
  // however good the instrument state looks. Found by the fx-04 negative control: without this,
  // a fixture the harness had just rejected still reported a clean pass rate marked eligible.
  const hardErrors = problems.filter((p) => p.severity === "error");
  if (hardErrors.length) {
    for (const d of dimensions) {
      d.registry_eligible = false;
      d.registry_note = `NOT Registry-eligible: this run raised ${hardErrors.length} integrity error(s); results are quarantined regardless of instrument state`;
    }
  }

  const sumTrials = dimensions.reduce((n, d) => n + d.n_trials, 0);
  return {
    run_integrity: hardErrors.length ? "failed" : "ok",
    integrity_errors: hardErrors.length,
    distinct_generations: distinctGenerations.size,
    dimension_results: sumTrials,
    shared_generations: shared,
    shared_generation_note: shared.length
      ? `${shared.length} generation(s) scored on more than one dimension: ${sumTrials} dimension-results come from only ${distinctGenerations.size} generation(s). These are NOT ${sumTrials} independent trials.`
      : "no generation was scored on more than one dimension",
    dimensions,
  };
}

function humanSummary(fx, agg, probs) {
  const L = [];
  L.push(`SYNTHETIC HARNESS RUN — ${fx.fixture_id}`);
  L.push(`MOCK DATA ONLY. No model was called. This is plumbing validation, not a measurement.`);
  L.push("");
  L.push(`Generations produced: ${agg.distinct_generations}`);
  L.push(`Dimension results:    ${agg.dimension_results}`);
  L.push(`  ${agg.shared_generation_note}`);
  L.push("");
  for (const d of agg.dimensions) {
    L.push(`${d.dimension}  [looked at per: ${d.observation_unit}]`);
    L.push(`   independent items: ${d.n_items}   attempts: ${d.n_trials}   observations: ${d.n_observations}`);
    L.push(`   pass/fail/not-measured: ${d.passes}/${d.fails}/${d.not_measured}` +
           (d.pass_rate === null ? "   pass rate: n/a" : `   pass rate: ${d.pass_rate} (${d.pass_rate_basis})`));
    const defs = Object.entries(d.defect_terms);
    if (defs.length) L.push(`   defects recorded: ${defs.map(([t, n]) => `${t} ×${n}`).join(", ")}`);
    L.push(`   instrument state: ${d.instrument_states.join(", ")} — ${d.registry_note}`);
    L.push("");
  }
  if (probs.length) {
    L.push("CHECKS RAISED:");
    for (const p of probs) L.push(`   [${p.severity}] ${p.code}: ${p.msg}`);
  } else {
    L.push("CHECKS: all invariants held.");
  }
  return L.join("\n");
}

// --- entry point --------------------------------------------------------------------------------

const argv = process.argv.slice(2);
const arg = (k) => { const i = argv.indexOf(k); return i >= 0 ? argv[i + 1] : undefined; };
if (argv.includes("-h") || argv.includes("--help") || argv.length === 0) {
  console.log(`
run-fixture.mjs — local evaluation harness, SYNTHETIC FIXTURES ONLY

  --fixture <file.json>   run one fixture
  --all                   run every positive fixture in eval/harness/fixtures/
  --negative              run the negative controls in fixtures/negative/ and PASS only if
                          EVERY one is individually rejected, each raising the error codes it
                          declares (proves the guards actually fire, per fixture)
  --selftest              regression coverage for the harness AND the checker:
                          (a) proves --negative would catch a negative fixture that was NOT
                              rejected; (b) proves per-item targets did not change checker
                              judgement and that malformed item files are rejected
  --out <dir>             write machine-readable results (default: eval/harness/out/)
  --check                 compare against the stored expected result and exit non-zero on drift
  -h, --help              this text

Makes no network call. Reads no real generated media. Produces no benchmark evidence.
`);
  process.exit(0);
}

// ---------------------------------------------------------------------------
// --selftest : regression coverage for the --negative verdict itself.
//
// Why this exists. --negative originally passed when `totalErrors > 0` across the whole run. With
// a single negative fixture that looks fine. With two or more it is unsound: one fixture's errors
// cover for another fixture that was silently ACCEPTED, so a broken guard would go unnoticed —
// exactly the failure the negative controls exist to detect. These cases pin the corrected
// per-fixture behaviour so the weaker check cannot come back unnoticed.
// ---------------------------------------------------------------------------
if (argv.includes("--selftest")) {
  const cases = [
    {
      name: "all fixtures rejected with their declared codes -> PASS",
      records: [
        { fixture_id: "a", error_count: 2, codes: ["BAD_OBSERVATION_UNIT", "GENERATION_DOUBLE_COUNTED"], expected_error_codes: ["GENERATION_DOUBLE_COUNTED"] },
        { fixture_id: "b", error_count: 1, codes: ["BAD_INSTRUMENT_STATE"], expected_error_codes: ["BAD_INSTRUMENT_STATE"] },
      ],
      expect: true,
    },
    {
      name: "one fixture NOT rejected while another is -> FAIL (the bug being guarded against)",
      records: [
        { fixture_id: "a", error_count: 2, codes: ["BAD_OBSERVATION_UNIT", "GENERATION_DOUBLE_COUNTED"], expected_error_codes: null },
        { fixture_id: "b-silently-accepted", error_count: 0, codes: [], expected_error_codes: ["BAD_INSTRUMENT_STATE"] },
      ],
      expect: false,
      note: "aggregate totalErrors would be 2 > 0 here, so the OLD check passed this. It must now fail.",
    },
    {
      name: "fixture rejected but for the wrong reason -> FAIL",
      records: [{ fixture_id: "a", error_count: 1, codes: ["BAD_OBSERVATION_UNIT"], expected_error_codes: ["GENERATION_DOUBLE_COUNTED"] }],
      expect: false,
    },
    {
      name: "no negative fixtures at all -> FAIL (an empty suite must not read as success)",
      records: [],
      expect: false,
    },
  ];

  let bad = 0;
  console.log("A · --negative verifies each fixture individually");
  for (const c of cases) {
    const got = judgeNegative(c.records).ok;
    const ok = got === c.expect;
    if (!ok) bad++;
    console.log(`  ${ok ? "PASS" : "FAIL"}  ${c.name}`);
    if (c.note) console.log(`          note: ${c.note}`);
    if (!ok) console.log(`          expected ok=${c.expect}, got ok=${got}`);
  }

  // ---- B · checker regression (EVAL-003) --------------------------------------------------
  // The per-item-target feature must not have changed any verdict. This re-scores every stored
  // historical transcription through BOTH code paths and requires byte-identical results.
  console.log("\nB · checker: per-item targets did not change judgement");
  const HIST = ["vlm_qwen-qwen3-vl-235b-a22b-instruct", "vlm_anthropic-claude-sonnet-4-5"];
  let n = 0, mism = 0;
  for (const f of HIST) {
    const stored = JSON.parse(readFileSync(join(HERE, "..", "runs", "finding-01-devanagari-check", `${f}.json`), "utf8"));
    for (const rec of Object.values(stored)) {
      if (rec.raw === undefined) continue;
      n++;
      const a = scoreTranscription(rec.raw);                  // single-target path
      const b = scoreTranscription(rec.raw, DEFAULT_TARGET);  // explicit-target path
      const same = a.normalized === rec.normalized && a.exact_match === rec.exact_match
                && a.edit_distance === rec.edit_distance
                && b.normalized === a.normalized && b.exact_match === a.exact_match
                && b.edit_distance === a.edit_distance;
      if (!same) mism++;
    }
  }
  const histOk = n === 27 && mism === 0;
  if (!histOk) bad++;
  console.log(`  ${histOk ? "PASS" : "FAIL"}  ${n} stored transcriptions re-scored via both paths, ${mism} mismatches (expect 27 / 0)`);

  // ---- C · malformed per-item files must be rejected, each with a reason -------------------
  console.log("\nC · malformed per-item input is rejected, not silently skipped");
  const fxDir = join(HERE, "fixtures", "per-item");
  const mal = [
    ["items-valid.jsonl", false, "valid file loads"],
    ["items-malformed-missing-target.jsonl", true, "missing required field"],
    ["items-malformed-duplicate-id.jsonl", true, "duplicate id"],
    ["items-malformed-missing-image.jsonl", true, "image not found"],
    ["items-malformed-bad-json.jsonl", true, "unparseable line"],
  ];
  for (const [file, shouldThrow, why] of mal) {
    let threw = false, msg = "";
    try { loadItems(join(fxDir, file)); } catch (e) { threw = true; msg = e.message; }
    const ok = threw === shouldThrow;
    if (!ok) bad++;
    console.log(`  ${ok ? "PASS" : "FAIL"}  ${file} -> ${threw ? "rejected" : "accepted"}  (${why})`);
    if (threw && ok) console.log(`          reason given: ${msg.split("\n")[0].slice(0, 90)}`);
  }

  // ---- D · the two input modes are mutually exclusive ---------------------------------------
  console.log("\nD · --input and --items cannot be combined");
  let exclusive = false;
  try { parseArgs(["--input", "x", "--items", "y"]); } catch { exclusive = true; }
  if (!exclusive) bad++;
  console.log(`  ${exclusive ? "PASS" : "FAIL"}  combining both modes is rejected`);

  console.log(bad === 0
    ? `\nSELFTEST OK — all groups passed.`
    : `\nSELFTEST FAILED — ${bad} check(s) wrong.`);
  process.exit(bad === 0 ? 0 : 1);
}

const fixtureDir = join(HERE, "fixtures");
const negative = argv.includes("--negative");
const listJson = (d) => readdirSync(d).filter((f) => f.endsWith(".json") && !f.endsWith(".expected.json")).sort().map((f) => join(d, f));
const files = negative ? listJson(join(fixtureDir, "negative"))
  : argv.includes("--all") ? listJson(fixtureDir)
  : [resolve(arg("--fixture"))];
const outDir = resolve(arg("--out") ?? join(HERE, "out"));
mkdirSync(outDir, { recursive: true });

let drift = 0, totalErrors = 0;
/** Per-fixture record so --negative can verify each one individually, not just in aggregate. */
const perFixture = [];
for (const f of files) {
  problems.length = 0;
  const fx = JSON.parse(readFileSync(f, "utf8"));
  const rows = runFixture(fx, f);
  const agg = aggregate(rows);
  const result = {
    SYNTHETIC_RESULT: true,
    WARNING: "Produced from mock fixtures by eval/harness/run-fixture.mjs. NOT a benchmark result. Must never be copied into the Capability Registry.",
    fixture_id: fx.fixture_id,
    harness: "eval/harness/run-fixture.mjs",
    network_calls: 0,
    rows, aggregate: agg, checks: [...problems],
  };
  const fixtureErrors = problems.filter((p) => p.severity === "error");
  totalErrors += fixtureErrors.length;
  perFixture.push({
    fixture_id: fx.fixture_id,
    error_count: fixtureErrors.length,
    codes: [...new Set(fixtureErrors.map((e) => e.code))],
    expected_error_codes: fx.expected_error_codes ?? null,
  });
  const outFile = join(outDir, `${fx.fixture_id}.result.json`);
  writeFileSync(outFile, JSON.stringify(result, null, 2));
  console.log(humanSummary(fx, agg, problems));
  console.log(`\n-> machine-readable: ${outFile}\n${"=".repeat(78)}`);

  const expectedFile = f.replace(/\.json$/, ".expected.json");
  if (argv.includes("--check")) {
    if (!existsSync(expectedFile)) { console.error(`no expected file: ${expectedFile}`); drift++; continue; }
    const expected = JSON.parse(readFileSync(expectedFile, "utf8"));
    const got = JSON.stringify(agg);
    if (got !== JSON.stringify(expected.aggregate)) {
      console.error(`DRIFT in ${fx.fixture_id}: aggregate does not match expected`);
      drift++;
    } else console.log(`CHECK OK — ${fx.fixture_id} matches its expected aggregate.`);
  }
}
/**
 * Verdict for negative-control mode. EVERY fixture must be individually rejected, and where a
 * fixture declares `expected_error_codes` those specific codes must appear.
 *
 * An aggregate `totalErrors > 0` test is NOT sufficient: with two or more negative fixtures it
 * passes even when one of them was silently accepted, because the other one's errors cover for it.
 * `--selftest` below is regression coverage for exactly that.
 */
export function judgeNegative(records) {
  const failures = [];
  for (const r of records) {
    if (r.error_count === 0) {
      failures.push(`${r.fixture_id}: expected rejection but the harness raised NO errors`);
      continue;
    }
    if (r.expected_error_codes) {
      const missing = r.expected_error_codes.filter((c) => !r.codes.includes(c));
      if (missing.length)
        failures.push(`${r.fixture_id}: rejected, but missing expected code(s): ${missing.join(", ")}`);
    }
  }
  return { ok: records.length > 0 && failures.length === 0, failures, checked: records.length };
}

if (negative) {
  const v = judgeNegative(perFixture);
  for (const r of perFixture)
    console.log(`  ${r.error_count > 0 ? "REJECTED" : "NOT REJECTED"}  ${r.fixture_id}  codes=[${r.codes.join(", ")}]`);
  if (v.ok) {
    console.log(`NEGATIVE CONTROLS OK — all ${v.checked} fixture(s) individually rejected with their declared codes.`);
  } else {
    console.error(`NEGATIVE CONTROLS FAILED:`);
    for (const f of v.failures) console.error(`   ${f}`);
  }
  process.exit(v.ok && drift === 0 ? 0 : 1);
}
// Exit non-zero on drift OR on integrity errors, so a broken run cannot be mistaken for a clean one.
process.exit(drift > 0 || totalErrors > 0 ? 1 : 0);
