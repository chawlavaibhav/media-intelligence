# Finding 06 — Grammar of the Shot, ch.4 (Pass 1)

**Date:** 23 Aug 2026 · **Source:** Thompson & Bowen, 2nd ed., ch.4, book pp.93–112
**Mode:** source-only Pass 1, isolated.

## Human learning notes

The chapter's frame is that **shots are recorded in order to be cut**, so every framing decision
is really a decision about a future join. Its subject is the small set of geometric contracts
that make separate recordings read as one continuous event.

The four edges of the frame become the audience's compass. From that: **screen direction** must
persist across cuts — exit frame left, enter frame right. Subjects' attention creates **sight
lines**, which viewers actively trace to work out who relates to whom and where everything sits.
The first shot's sight line fixes an **axis of action**, and all later camera positions must stay
within the 180-degree arc on one side of it. Between two shots of the same subject, move at least
**30 degrees** or the cut reads as a jump rather than as new information. Shots covering different
characters must **match each other** on size, placement, height and lens angle. A look off-frame
sets up an expectation that the next shot must **pay off** from a corresponding vantage.

Conventionally a scene runs **outside in** — wide for context, tightening for intimacy.

## Counts

```
13 candidate ideas
10 atoms
   2 operational        (gos_001, gos_008 — propose no new vocabulary)
   8 pending_vocabulary
 3 human_notes
```

## IR-field coverage

| Field | Atoms |
|---|---:|
| `video.continuity_requirements` | 8 |
| `video.temporal_structure` | 5 |
| `relationships` | 2 |
| `video.temporal_hierarchy` | 1 |
| `static.composition` | 1 |

First source in this batch to reach the **video extension** at all, and it saturates
`continuity_requirements`. Also the first to reach **`relationships`**.

**Still untouched after four sources:** everything in `intent`, `audience`, `message`, `entities`,
`brand`, `delivery`, `acceptance`, and `video.dialogue_intent`.

## Proposed vocabulary

Failure modes (7): `continuity_of_action_break`, `contradictory_sight_lines`, `crossed_action_line`,
`jump_cut`, `mismatched_reciprocal_framing`, `reversed_screen_direction`, `unresolved_eyeline`

Repairs (7): `add_payoff_shot`, `change_focal_length`, `increase_angle_change`,
`match_payoff_vantage`, `match_reciprocal_framing`, `redirect_subject_attention`,
`reframe_within_180_arc`, `reshoot_matching_action`, `restore_screen_direction`

## Flagged for human review

**1. `gos_005` has consequences for how runtime evaluation must work.**
A crossed action line is undetectable in any single shot — the fault is a *relation between
shots*, and it appears only on assembly. Any evaluator that scores frames or clips independently
is structurally incapable of catching it. The same is true of `reversed_screen_direction`,
`jump_cut` and `mismatched_reciprocal_framing`: four of this chapter's seven failure modes are
between-shot properties. This is knowledge about **what an evaluator must be shaped like**, not
just about what makes video good. Recorded as an atom; flagged because it may belong somewhere
else entirely.

**2. `relationships` was specified correctly.**
SPEC-01's worked example for that field was `{subject: person_456, relation: looking_at,
object: product_123}`. `gos_003` and `gos_009` are that exact structure, arrived at from a 2009
cinematography text. Independent confirmation of a field we invented.

**3. The source supplies a blanket exception clause.**
Book p105: creative reasons override any of these guidelines. This propagated
`exceptions_status: source_supported` across most atoms — a very different profile from a source
that states principles unconditionally. How the Canon should treat a source-level clause versus a
per-principle exception is a judgment call, not applied here.

**4. Two more Production IR candidates.**
`shoot_coverage_to_give_the_editor_choices` is "generate several options for a downstream
chooser" — a Production IR decision about variant count. `minimise_take_count_for_cost` is cost
modelling. Neither has a Creative IR home, correctly.

**5. A structural echo worth noting.**
This chapter ends with its own eight-point numbered review restating its principles operationally.
That is the second source in this batch to author its own summary-of-rules section. Whether that
correlates with clean extraction is a question for the aggregate.

## Visual-context status

No unresolved items. The 180-degree geometry is described in prose as fully as it is drawn, and
no atom rests on a diagram alone. Figures were not rendered.
