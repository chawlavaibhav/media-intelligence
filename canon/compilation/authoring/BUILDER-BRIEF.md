# Builder brief — compile one doctrine pack

Authority: `coordination/decisions/CONTROLLER-CANON-COMPLETION-2026-09-22.md` (APPROVED).
Definition of done: `canon/validation/CANON-DONE-v0.md`. USD 0; no model or provider call.

You are building **one** pack: `<PACK_ID>` (given in your task). You write exactly two files:

- `canon/compilation/authoring/PACK-<PACK_ID>.authoring.yaml` — the authored pack
- `canon/compilation/authoring/BUILD-NOTE-<PACK_ID>.md` — what you did, what you left out, why

and you run the compiler, which writes `canon/compilation/PACK-<PACK_ID>-v0.yaml`. Touch nothing
else. Do not commit. Do not edit any other pack, any Canon knowledge file, the compiler, the
validator, or any coordination file. If something outside your two files must change, stop and
say so in the build note.

## Read, in this order (by command; never open whole knowledge files)

1. `canon/compilation/COMPILED-DOCTRINE-SPEC-v0.md` §1–§5 (what a decision is; the closure rule;
   conflicts; limit lines) and `canon/compilation/INJECTION-CONTRACT-v0.md` (how the text is
   consumed — a weak model edits a made decision, it never composes from principle).
2. The style example: `sed -n 114,270p canon/compilation/compile_pilot_packs.py` — the
   product_appearance decisions, conflicts and waivers as authored.
3. Your seed packet: `python3 canon/compilation/pack_seed.py <PACK_ID>` (domains, contributor
   sources, the SEED claims in full with their guard relations, and a one-line index of every
   other claim). Fetch any claim in full with `pack_seed.py --claim <id> [<id> ...]`; a source's
   concept systems with `--systems <source_dir>`.

## What the pack must be

- **8–12 decisions**, ids `<XX>-D1 …` where `<XX>` is the two-letter code given in your task.
  Each decision = one `question` a producer must answer for a brief, one `default` (the made
  decision, imperative, answer-shaped, with the deciding ids named in the text), one `check` (a
  line a checker can decide on the artifact or the board), `ids` (every claim / concept-system
  id the decision rests on), `feeds` (from: `MESSAGE_AND_INFORMATION_HIERARCHY`,
  `VISUAL_SYSTEM` or `VISUAL_SYSTEM.<field>`, `AUDIO_AND_EDIT`, `PRODUCTION_RECIPE`,
  `GENERATION_PROMPTS`, `FAILURE_PREVENTION`, `HARD_CONSTRAINT_CHECK`, `DOCTRINE_DEVIATIONS`),
  `limits` (verbatim caveat lines, may be empty).
- **Every SEED claim is cited by at least one decision.** That is the coverage condition (B).
  Group seeds by the question they answer; add non-seed claims from the index where a decision
  needs them; never cite an id you have not read in full.
- **Closure (GAP-11):** for every cited `sk_` id, each guard partner (`contradicts`,
  `qualified_by`, `trades_off_with`, `depends_on`) must be cited too, or named in a `conflicts`
  entry with a `resolution_rule`, or waived in `waivers` with a reason that says what the
  decision consumes and why the partner does not change it. The compiler fails closed and names
  the hole; resolve each one honestly — cite when the partner matters, conflict when both hold
  under different conditions, waive only when the decision genuinely does not consume the
  partner's content.
- **Terse budget:** the compiler renders the pack's `terse_injection_text` and refuses over
  2,500 tokens. If you cannot fit, cut decisions, not ids; report it in the build note.
- **Limits, not silence:** where the contributors do not cover something a brief in this domain
  will ask (a medium, a format, a market), write a `pack_limits` line saying so. The Devanagari
  limit line is added by the compiler. Look at the existing packs' coverage-delta lines for the
  shape.
- **Applicability:** list the modalities the decisions hold for (`static_image`, `video`,
  `image_sequence`, `audio`).
- **Nothing invented.** A default may only say what the cited claims say. Where two contributors
  disagree, that is a `conflicts` entry with a rule, not a blended sentence. Where the corpus is
  silent, that is a limit line.

## YAML shape

```yaml
pack_id: <PACK_ID>
applicability: [static_image, video, image_sequence]
decisions:
  - decision_id: XX-D1
    question: "…?"
    default: "… (sk_…, scs_…)"
    check: "…"
    ids: [sk_…, sk_…, scs_…]
    feeds: [MESSAGE_AND_INFORMATION_HIERARCHY, FAILURE_PREVENTION]
    limits: []
conflicts:
  - conflict_id: CF-01
    decision_ref: XX-D2
    kind: contradicts            # contradicts | trades_off_with | qualified_by | cross_source_tension
    between: [sk_a, sk_b]
    nature: "…"
    resolution_rule: "…"
waivers:
  - {ref: sk_a, relation: depends_on, partner: sk_c, reason: "…"}
pack_limits:
  - "…"
```

## Loop until green

```bash
python3 canon/compilation/compile_pilot_packs.py --only <PACK_ID>     # fail-closed: fix every message
python3 canon/validation/canon_done.py --pack <PACK_ID>                # seed coverage must reach missing 0
python3 canon/validation/validate_compiled_pack.py                     # must PASS
python3 canon/compilation/compile_pilot_packs.py --check               # every pack byte-stable
```

(`canon_done.py --pack` exits 2 while the pack's status is PROPOSED — that is expected; adoption
is the Controller's step. What you need from it is `missing 0`.)

## The build note (`BUILD-NOTE-<PACK_ID>.md`)

Short. (1) the decisions in one line each; (2) seed coverage: N of N, with the decision that
carries each seed; (3) every closure hole and how it was resolved (cite / conflict / waiver);
(4) every limit line and why; (5) what you deliberately did not compile from the contributors
and why; (6) terse tokens; (7) an estimate of the session tokens you used.

## Red flags — stop and write it in the note instead of pushing through

A seed claim that no honest question fits (say so; do not force a decision around it). A
guard partner you would have to waive but which actually changes the default. A pack that only
fits the budget by dropping seeds. Two contributors that contradict each other with no condition
that separates them.
