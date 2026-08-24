// Devanagari text checker — vision-model route.
// Asks a VLM to TRANSCRIBE (not to confirm), so an agreeable model can't just say "yes".
// Resumable: never re-pays for a sample already recorded.
//
// EVAL-002 change: paths are now supplied on the command line instead of being hard-coded to one
// machine. WHAT THE CHECKER JUDGES IS UNCHANGED — the prompt, the normalisation rule, the
// edit-distance function and the exact-match verdict are byte-identical to the version used for
// FINDINGS-01. Only where the files live, and how the run is invoked, has changed.
//
// The scoring functions are also exported so a local harness can exercise the real judgement code
// with fabricated inputs and no network call. See eval/harness/.

import { readFileSync, writeFileSync, existsSync, readdirSync, statSync, mkdirSync } from "node:fs";
import { join, extname, basename, dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

// ---------------------------------------------------------------------------
// JUDGEMENT — unchanged from the FINDINGS-01 version. Do not edit without a
// new approved task: changing any of this makes results incomparable with the
// original calibration study (AUTONOMY-POLICY stop condition 8).
// ---------------------------------------------------------------------------

export const PROMPT =
  "Transcribe the Devanagari (Hindi) text written on the signboard in this image, exactly as the " +
  "letterforms appear — character for character. Do NOT correct spelling. Do NOT guess what it was " +
  "meant to say. If the letterforms are not real Devanagari words, transcribe the nonsense exactly " +
  "as drawn. Reply with the transcription only, no commentary. If there is no Devanagari text, reply NONE.";

/** Default target retained so the original FINDINGS-01 run stays reproducible without arguments. */
export const DEFAULT_TARGET = "सुबह की पहली चाय";

export const norm = (s) =>
  (s || "").normalize("NFC").replace(/[\s​-‍]+/g, " ").replace(/[।."'`]/g, "").trim();

// character-level edit distance, so "recognisable but wrong" is visible as a small number
export function editDistance(a, b) {
  const m = [...a], n = [...b];
  const d = Array.from({ length: m.length + 1 }, (_, i) =>
    Array.from({ length: n.length + 1 }, (_, j) => (i === 0 ? j : j === 0 ? i : 0)));
  for (let i = 1; i <= m.length; i++)
    for (let j = 1; j <= n.length; j++)
      d[i][j] = Math.min(d[i-1][j] + 1, d[i][j-1] + 1, d[i-1][j-1] + (m[i-1] === n[j-1] ? 0 : 1));
  return d[m.length][n.length];
}

/**
 * The verdict, factored out verbatim from the original inline expression so it can be tested
 * offline. Given a raw transcription and a target, produces exactly the record shape the original
 * script wrote.
 */
export function scoreTranscription(raw, target = DEFAULT_TARGET) {
  const normalized = norm(raw);
  return {
    raw,
    normalized,
    exact_match: normalized === norm(target),
    edit_distance: editDistance(normalized, norm(target)),
  };
}

// ---------------------------------------------------------------------------
// PLUMBING — this is the part EVAL-002 changed.
// ---------------------------------------------------------------------------

const mime = (f) => ({ ".png": "image/png", ".webp": "image/webp", ".jpg": "image/jpeg" }[extname(f)] || "image/png");

const HELP = `
check-vlm.mjs — transcribe-and-compare checker for rendered Devanagari text

USAGE
  node eval/scripts/check-vlm.mjs --input <file|dir> --out <file.json> [options]

REQUIRED
  --input   <path>    image file, or directory of .png/.webp/.jpg images
  --out     <path>    JSON results file; created if absent, resumed if present

OPTIONS
  --model   <id>      vision model identifier (default: google/gemini-2.5-pro)
  --target  <string>  expected string to compare against
                      (default: the FINDINGS-01 target, so that run reproduces with no flag)
  --dry-run           validate inputs and list what WOULD be sent. Makes no network
                      call, needs no API key, and writes nothing.
  -h, --help          this text

ENVIRONMENT
  FAL_KEY             required for a real run; NOT required for --dry-run

NOTES
  The prompt, normalisation and verdict logic are unchanged from the version used for
  FINDINGS-01. Only paths and invocation changed. A checker must be re-calibrated whenever its
  model version changes — see eval/battery/INSTRUMENT-CALIBRATION-PLAN-V0.md.
`;

export function parseArgs(argv) {
  const out = { model: "google/gemini-2.5-pro", target: DEFAULT_TARGET, dryRun: false, help: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "-h" || a === "--help") out.help = true;
    else if (a === "--dry-run") out.dryRun = true;
    else if (a === "--input") out.input = argv[++i];
    else if (a === "--out") out.out = argv[++i];
    else if (a === "--model") out.model = argv[++i];
    else if (a === "--target") out.target = argv[++i];
    else throw new Error(`unknown argument: ${a}`);
  }
  return out;
}

/** Resolve --input to a sorted list of image paths. Accepts a single file or a directory. */
export function collectImages(input) {
  const p = resolve(input);
  if (!existsSync(p)) throw new Error(`--input path does not exist: ${p}`);
  if (statSync(p).isDirectory()) {
    const files = readdirSync(p).filter((f) => /\.(png|webp|jpg)$/i.test(f)).sort();
    if (files.length === 0) throw new Error(`no .png/.webp/.jpg files found in: ${p}`);
    return files.map((f) => join(p, f));
  }
  if (!/\.(png|webp|jpg)$/i.test(p)) throw new Error(`--input is not a supported image type: ${p}`);
  return [p];
}

async function transcribe(file, model, key) {
  const b64 = readFileSync(file).toString("base64");
  const res = await fetch("https://fal.run/fal-ai/any-llm/vision", {
    method: "POST",
    headers: { Authorization: `Key ${key}`, "Content-Type": "application/json" },
    body: JSON.stringify({ prompt: PROMPT, image_url: `data:${mime(file)};base64,${b64}`, model }),
  });
  const txt = await res.text();
  if (!res.ok) throw new Error(`${res.status} ${txt.slice(0, 300)}`);
  const j = JSON.parse(txt);
  return (j.output ?? j.response ?? "").trim();
}

async function main(argv) {
  let args;
  try {
    args = parseArgs(argv);
  } catch (e) {
    console.error(`error: ${e.message}`);
    console.error(HELP);
    process.exit(2);
  }
  if (args.help) { console.log(HELP); return; }

  const missing = [];
  if (!args.input) missing.push("--input");
  if (!args.out && !args.dryRun) missing.push("--out");
  if (missing.length) {
    console.error(`error: missing required argument(s): ${missing.join(", ")}`);
    console.error(HELP);
    process.exit(2);
  }

  let files;
  try {
    files = collectImages(args.input);
  } catch (e) {
    console.error(`error: ${e.message}`);
    process.exit(2);
  }

  if (args.dryRun) {
    console.log(`DRY RUN — no network call, nothing written.`);
    console.log(`  model:  ${args.model}`);
    console.log(`  target: «${args.target}»`);
    console.log(`  out:    ${args.out ? resolve(args.out) : "(not set; not needed for --dry-run)"}`);
    console.log(`  ${files.length} image(s) would be sent:`);
    for (const f of files) console.log(`    ${basename(f)}`);
    return;
  }

  const key = process.env.FAL_KEY;
  if (!key) { console.error("error: FAL_KEY missing (not needed for --dry-run)"); process.exit(1); }

  const outPath = resolve(args.out);
  mkdirSync(dirname(outPath), { recursive: true });
  const prior = existsSync(outPath) ? JSON.parse(readFileSync(outPath, "utf8")) : {};

  for (const file of files) {
    const id = basename(file);
    if (prior[id]?.raw !== undefined) { console.log(`skip  ${id}`); continue; }
    try {
      const raw = await transcribe(file, args.model, key);
      prior[id] = scoreTranscription(raw, args.target);
      console.log(`ok    ${id}  match=${prior[id].exact_match}  dist=${prior[id].edit_distance}  «${raw.replace(/\n/g, " ").slice(0, 60)}»`);
    } catch (e) {
      prior[id] = { error: String(e).slice(0, 200) };
      console.log(`FAIL  ${id}  ${prior[id].error}`);
    }
    writeFileSync(outPath, JSON.stringify(prior, null, 2));
  }
  console.log(`\nwrote ${outPath}`);
}

// Only run when invoked directly, so the harness can import the scoring functions safely.
if (process.argv[1] && resolve(process.argv[1]) === resolve(fileURLToPath(import.meta.url))) {
  await main(process.argv.slice(2));
}
