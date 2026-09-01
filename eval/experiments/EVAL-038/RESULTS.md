# EVAL-038 — unblinded results

Reveal: `judging/REVEAL.json` (all 8 commitments verified: sha256(salt|key) matches
every committed `BLINDING-COMMITMENT.json`). Verdicts: `judging/verdicts/`.

## Primary endpoint — substitution thesis (packages)

Reviewer: the independent blinded agent (reviewer 2); the Controller abstained from
package judging, so this is a SINGLE-reviewer read, not the design's two-reviewer
unanimity (deviation recorded in reviewer-1 file).

Unblinded rankings — the three Sonnet NO_CANON repetitions took the **top three
positions on all six briefs, 18 of 18 top-3 slots**:

| Brief | Unblinded ranking (best first) | Best weak+packs position |
|---|---|---|
| B01 | sonnet-R3, sonnet-R1, sonnet-R2, gemma-R2, haiku-R1, gemma-R1, haiku-R2 | 4th (gemma) |
| B02 | sonnet-R1, sonnet-R3, sonnet-R2, gemma-R2, gemma-R1, haiku-R1, haiku-R2 | 4th (gemma) |
| B03 | sonnet-R1, sonnet-R3, sonnet-R2, gemma-R2, haiku-R1, gemma-R1, haiku-R2 | 4th (gemma) |
| B04 | sonnet-R2, sonnet-R3, sonnet-R1, haiku-R1, haiku-R2, gemma-R2, gemma-R1 | 4th (haiku) |
| B05 | sonnet-R2, sonnet-R1, sonnet-R3, haiku-R2, gemma-R1, gemma-R2, haiku-R1 | 4th (haiku) |
| B06 | sonnet-R1, sonnet-R3, sonnet-R2, gemma-R1, gemma-R2, haiku-R1, haiku-R2 | 4th (gemma) |

Decision rule (design §1): weak+packs supported on a brief only if it wins or ties
the strong baseline; programme-level support requires ≥3 of 6.

**Result: 0 of 6. The substitution thesis is REFUTED under this evidence — a real
negative result, committed as such.** A weak model consuming the two compiled packs
under forced injection did not match a strong model working alone on any brief; it
never outranked even one of the three strong-baseline repetitions.

## Secondary observations (honest, not spin)

- The weak models **did** consume the doctrine perfectly at the structural level:
  24/24 packages satisfied the v2 forced-consumption schema with zero defects. The
  gap is creative substance, not compliance — consistent with EVAL-037's lesson that
  bounded required structure completes while quality does not follow automatically.
- Reviewer-2 penalized "leftover citation artifacts" in several treatment packages —
  scars of the blinding scrub that fall disproportionately on treatment. The margin
  (18/18 top-3) is far beyond what that bias could account for, but it is a real
  blinding imperfection to fix before any rerun.
- Only 2 of 10 packs exist; colour/register and commercial-communication doctrine
  were never injected (declared in every payload). This result refutes "these two
  packs close the gap," not "any possible compiled Canon closes the gap."

## Media (product learning only — never Registry evidence)

Mapping: M01/V01 = haiku-packs; M02/V02 = sonnet-no-canon.

- **B06 image:** reviewers DISAGREE on the winner — Controller: M02 (sonnet) slightly
  better, both acceptable; agent: M01 (haiku) accept, M02 reject on close-inspection
  artifacts. Recorded as a disagreement per the design. Notable: the haiku-package
  image was at worst competitive with the strong baseline's at the pixel level —
  the packages' large quality gap compressed after generation.
- **B01 video:** unanimous V02 (sonnet) > V01 (haiku); Controller: neither is
  production grade. Consistent with the PILOT-001 root-cause lesson: text/UI baked
  into generated pixels (both clips) remains the salvageability blocker, and the
  deterministic-overlay discipline in the packages was the right call that the raw
  clips, judged alone, could not show.

## Spend (final)

Real consumed: **USD 1.793122** of the 10.00 cap (haiku 0.859122, gemma 0.000000,
media 0.934000). Ledger conservatively counts 2.293122 including the annotated
phantom 0.50 from the duplicate session. Retries: 0. Cap breaches: none.
