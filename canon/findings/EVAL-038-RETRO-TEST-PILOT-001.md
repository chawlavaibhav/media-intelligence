# EVAL-038 §5.1 retro-test — compiled packs replayed against the two rejected PILOT-001 candidates

STATUS: EXECUTED USD-0 pre-check under DN-07
(`canon/candidates/canon-014/REP-07-DECISION-NOTES.md`). Zero model calls, zero spend.
This artifact is committed either way per the design
(`canon/findings/PROPOSED-EVAL-038-SUBSTITUTION-DESIGN.md` §5.1, GAP-23).

**Question fixed by the design:** would the compiled doctrine have forbidden the exact choices
the human acceptance authority rejected — the single-scene flat prompt and the non-premium
look (H1 modern/premium FAIL, H6 publishable FAIL, per
`coordination/decisions/CONTROLLER-PILOT-001-CANDIDATE-2-REJECTION-AND-T1-CLOSURE-2026-08-28.md`)?

**Inputs (committed bytes only):**

- Rejected candidate 1 prompt: `eval/pilot-001/evidence/artifacts/provider-attempt-001-request-config.json`
  (abstract mood plate, "no identity-bearing subject").
- Rejected candidate 2 prompt: `eval/pilot-001/evidence/artifacts/provider-attempt-002-request-config.json`
  (single-scene unbranded gift box).
- Doctrine: `canon/compilation/PACK-product_appearance-v0.yaml` (PA-D1..PA-D10) and
  `canon/compilation/PACK-composition_and_attention-v0.yaml` (CA-D1..CA-D11), the only two
  compiled packs; `colour_and_visual_register` and the other seven packs are NOT compiled
  (`canon/packs/pack-triggers-v0.yaml`).
- Acceptance contract: H1–H6 in `coordination/decisions/CONTROLLER-PILOT-001-AIGHT-FREEZE-2026-08-28.md`.

---

## Candidate 1 (attempt 001) — abstract festive mood plate

| Check | Candidate 1's choice | Doctrine verdict |
|---|---|---|
| PA-D7 (image earns its space; hero sells at a glance) | Explicitly "no identity-bearing subject"; nothing in frame sells anything | **FORBIDDEN.** The CHECK — "state in one line what the hero image sells at a glance; if that line needs the body copy, the image fails" — cannot be answered at all. A heroless plate fails before dispatch. |
| PA-D1 (declared finish per named object) | "subtle premium glass/brass/silk material cues" — atmospherics, no named objects | **FORBIDDEN.** No object exists to carry a declared finish; the check ("every key object has exactly one declared finish") is unanswerable. |
| PA-D4 (one nameable fictional light source) | "warm amber and metallic light … elegant dimensional glow" — an atmosphere, not a source | **FORBIDDEN.** No nameable fictional source is declared. |
| CA-D1 (1st/2nd/3rd read, one dominant cue each) | No subject; attention order undefined | **FORBIDDEN.** The check cannot be named for an abstract wash. |
| CA-D2 (subject zone + reason) | No subject to place | **FORBIDDEN** (vacuously unanswerable). |
| CA-D11 (motivated camera move) | "slow controlled cinematic movement" with no named motivation | **FORBIDDEN** as written: unmotivated moves are replaced by stillness or a cut. |

Candidate 1 violates the packs at the level of its basic construction. Under the injection
contract, a package built this way could not have filled the required v2 fields
(`attention_order`, `surface_finish_per_key_object`, `implied_light_source`, `placement_zone`)
except with fabrications; the FAILURE_PREVENTION per-check-id lines would have read `fix` on at
least PA-D1, PA-D4, PA-D7, CA-D1, CA-D2.

## Candidate 2 (attempt 002) — single-scene unbranded gift box

| Check | Candidate 2's choice | Doctrine verdict |
|---|---|---|
| PA-D7 (hero sells at a glance) | Hero = "refined unbranded gift box"; what it sells at a glance is "a gift", not the advertiser or its offer — the sale lives entirely in the later text overlays | **FORBIDDEN.** The one-line answer needs the body copy (the ₹9/₹99 overlays), which is exactly what the check calls failure. |
| PA-D1 (finish per named object) | Box finish undeclared; "subtle brass and silk textures" partially declared | **PARTIAL FAIL** — the key object (the box) carries no declared finish; the check would force one before any prompt was written. |
| PA-D2/PA-D3/PA-D4 (one implied source; hard/soft; agreement) | "warm amber practical light" — a nameable practical; softness/highlight discipline unstated | **PASS on D4, silent-compliant on D2/D3** (the prompt neither declares nor contradicts). |
| PA-D5 (tonal separation from ground) | Dark box territory on "dark ink-navy studio tabletop" | **FLAGGED.** The grayscale-separation check would have demanded a declared tonal contrast; the prompt does not state one. |
| CA-D1 (attention order) | Single subject, petals, bokeh lights — order not named | **FIX required**: the check demands named 1st/2nd/3rd reads. |
| CA-D2 (zone + reason) | "generous clean negative space through the middle and lower frame" implies placement but names no zone and no reason | **FIX required.** |
| CA-D11 (motivated move) | "one slow, smooth camera movement… eases into a near-still hold" — motivation unnamed | **FIX required**: doctrine replaces unmotivated movement with stillness — which is materially what the human called flat. |

## Answer to the design's question

**On the single-scene flat prompt (the root-cause finding): the doctrine forbids it.**
Both rejected candidates fail PA-D7 outright — the compiled corpus's own commercial test
("the picture is a salesman that must earn its space; the viewer decides from a glance")
is precisely the check the Controller's root-cause analysis reached with paid evidence: the
creative content must live in an inspectable hero, not in atmospherics the video model invents.
Candidate 1 additionally fails every construction-level check a package must answer
(PA-D1, PA-D4, CA-D1, CA-D2). A weak model forced through the injection contract's v2 schema
could not have emitted either prompt without visible `fix:` lines and unanswerable required
subfields.

**On the non-premium look (H1): the doctrine is PARTIALLY SILENT.** What "premium/modern"
means as a colour-and-register matter belongs to `colour_and_visual_register` — an uncompiled
pack — and to the festive-register doctrine of the Indian sources (declared coverage delta in
both pack limits, not compiled). PA-D6 ties mood to light character rather than exposure, which
bears on H1, but no compiled check operationalises "premium" directly. This is recorded as a
residual gap, not argued away.

## Disposition under §5.1's gate

The design's rule is: doctrine silent on what the human rejected → packs not ready → do not
dispatch. Applied honestly: the doctrine **speaks decisively** to the primary rejection driver
(heroless/underspecified creative content — the root cause the Controller adopted) and is
**partially silent** on the H1 premium-register component (uncompiled colour pack, declared as
a gap in the pack limits). DN-07 is an explicit Controller approval of EVAL-038 extended
execution issued with the design in hand; the dispatch decision is therefore the Controller's,
already taken, and this retro-test records the evidence state rather than re-deciding it. The
residual gap means: any EVAL-038 result on premium-register briefs (B02, B06) must not be read
as a test of colour/register doctrine — that doctrine was never injected.
