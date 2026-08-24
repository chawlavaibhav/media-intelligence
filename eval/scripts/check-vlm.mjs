// Devanagari text checker — vision-model route.
// Asks a VLM to TRANSCRIBE (not to confirm), so an agreeable model can't just say "yes".
// Resumable: never re-pays for a sample already recorded.

import { readFileSync, writeFileSync, existsSync, readdirSync } from "node:fs";
import { join, extname, basename } from "node:path";

const ROOT = "/Users/vaibhavchawla/Vaibhav_Personal_Projects/aight-eval";
const SAMPLES = join(ROOT, "samples/real");
const MODEL = process.argv[2] || "google/gemini-2.5-pro";
const OUT = join(ROOT, `results/vlm_${MODEL.replace(/[\/.]/g, "-")}.json`);
const TARGET = "सुबह की पहली चाय";
const KEY = process.env.FAL_KEY;
if (!KEY) { console.error("FAL_KEY missing"); process.exit(1); }

const PROMPT =
  "Transcribe the Devanagari (Hindi) text written on the signboard in this image, exactly as the " +
  "letterforms appear — character for character. Do NOT correct spelling. Do NOT guess what it was " +
  "meant to say. If the letterforms are not real Devanagari words, transcribe the nonsense exactly " +
  "as drawn. Reply with the transcription only, no commentary. If there is no Devanagari text, reply NONE.";

const norm = (s) =>
  (s || "").normalize("NFC").replace(/[\s​-‍]+/g, " ").replace(/[।."'`]/g, "").trim();

// character-level edit distance, so "recognisable but wrong" is visible as a small number
function editDistance(a, b) {
  const m = [...a], n = [...b];
  const d = Array.from({ length: m.length + 1 }, (_, i) =>
    Array.from({ length: n.length + 1 }, (_, j) => (i === 0 ? j : j === 0 ? i : 0)));
  for (let i = 1; i <= m.length; i++)
    for (let j = 1; j <= n.length; j++)
      d[i][j] = Math.min(d[i-1][j] + 1, d[i][j-1] + 1, d[i-1][j-1] + (m[i-1] === n[j-1] ? 0 : 1));
  return d[m.length][n.length];
}

const mime = (f) => ({ ".png": "image/png", ".webp": "image/webp", ".jpg": "image/jpeg" }[extname(f)] || "image/png");

async function transcribe(file) {
  const b64 = readFileSync(file).toString("base64");
  const res = await fetch("https://fal.run/fal-ai/any-llm/vision", {
    method: "POST",
    headers: { Authorization: `Key ${KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      prompt: PROMPT,
      image_url: `data:${mime(file)};base64,${b64}`,
      model: MODEL,
    }),
  });
  const txt = await res.text();
  if (!res.ok) throw new Error(`${res.status} ${txt.slice(0, 300)}`);
  const j = JSON.parse(txt);
  return (j.output ?? j.response ?? "").trim();
}

const prior = existsSync(OUT) ? JSON.parse(readFileSync(OUT, "utf8")) : {};
const files = readdirSync(SAMPLES).filter((f) => /\.(png|webp|jpg)$/i.test(f)).sort();

for (const f of files) {
  const id = basename(f);
  if (prior[id]?.raw !== undefined) { console.log(`skip  ${id}`); continue; }
  try {
    const raw = await transcribe(join(SAMPLES, f));
    const dist = editDistance(norm(raw), norm(TARGET));
    prior[id] = { raw, normalized: norm(raw), exact_match: norm(raw) === norm(TARGET), edit_distance: dist };
    console.log(`ok    ${id}  match=${prior[id].exact_match}  dist=${dist}  «${raw.replace(/\n/g, " ").slice(0, 60)}»`);
  } catch (e) {
    prior[id] = { error: String(e).slice(0, 200) };
    console.log(`FAIL  ${id}  ${prior[id].error}`);
  }
  writeFileSync(OUT, JSON.stringify(prior, null, 2));
}
console.log(`\nwrote ${OUT}`);
