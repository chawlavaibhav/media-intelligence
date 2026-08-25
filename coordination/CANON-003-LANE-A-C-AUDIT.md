# CANON-003 — Controller audit of Lane A and Lane C

> **HISTORICAL — Controller audit record, not current state.** Classified `HISTORICAL` by GOV-001 on
> 25 Aug 2026. The findings below remain **evidentially valid** for the CANON-003 batch and were not
> altered. They describe a batch that has since closed at 16 accepted books and been superseded by
> the Audit Gate v0.2 method; live Canon is now 19 sources. Any lane, branch or in-progress status
> named below is finished. Current state: `PROJECT-MEMORY.md` and `coordination/CONTROL-STATE.md`.


**Date:** 24 Aug 2026  
**Status:** Controller review complete for returned Lane A and Lane C branches.  
**Scope:** review only; no lane merge or cross-lane synthesis performed.

## Decision

- **Lane A accepted for Books 6–7** under the frozen CANON-003 method, subject to the planned final integration revalidation of all per-book outputs.
- **Lane C accepted for Books 13–15** under the frozen CANON-003 method, subject to the same final integration revalidation.
- Lane A and Lane C should now remain untouched until the dedicated CANON-003 integration/synthesis session.
- Book 8 remains assigned to `work/canon-003-rebalance-d`; Lane A did not produce an Alton extraction.

Together with the five pre-parallel usable books and accepted Lane D Books 16–18, the Controller-confirmed usable count is now **13**.

## Lane A audit

Branch: `work/canon-003-a`  
Common base: `4cbe25783cb2bccf1584c792d44ca54adf71bf3b`  
Ahead of common base: 5 commits.

### Book 6 — Timothy Samara, *Making and Breaking the Grid*

Fresh checkpoint: `c8cb9d4`.

Git history verifies that this checkpoint is exactly one commit after the common base and contains only the source-specific Book 6 representation files. The later Book 6 findings/lane records occur after that checkpoint. This satisfies the fresh-before-history rule.

The returned provenance is method-disciplined: source identity and printed-page anchors are verified; EPUB page-layout loss is explicitly distinguished from figure availability; only a partial figure-level visual claim is made; the unusually high object count is recorded as a source/section comparability issue rather than prompting a granularity change; production-like deterministic layout operations are parked/bound conservatively rather than translated into unsupported generative rules.

### Book 7 — Michael Freeman, *The Photographer's Eye: A Graphic Guide*

Fresh checkpoint: `5f95755`.

Git history verifies the Book 7 fresh checkpoint precedes the Book 7 findings/history work. The checkpoint itself contains the Freeman source-specific representation files; subsequent commits add only Book 7 findings and Lane A issue/checkpoint updates.

**Source identity correction retained:** the pre-batch inventory described the local artifact as Michael Freeman's 2007 *The Photographer's Eye*. The actual preselected local artifact is *The Photographer's Eye: A Graphic Guide* (Focal Press, 2013), a later distinct title by the same author. This is an inventory-identification error, not a post-result source substitution: the local artifact itself was the one present and selected before parallel results, and it still satisfies the photography/composition coverage rationale. Final integration must preserve the corrected identity and must not silently call it the 2007 book.

The provenance also correctly downgrades visual completeness because the local PDF is a Calibre-reflowed conversion rather than the designed printed page. It does not equate "PDF" with page-level verification. Visual-only measurements/counterfactuals are recorded as such, and physical camera remedies are not silently translated into generative controls.

### Reassigned Book 8

Lane A's checkpoint states source inspection had begun only in session scratch space before the rebalance, with no extraction, knowledge object or Alton directory committed. Compare-to-base confirms no Book 8 source-specific files exist on Lane A. Book 8 therefore remains owned by `work/canon-003-rebalance-d`.

## Lane C audit

Branch: `work/canon-003-c`  
Common base: `4cbe25783cb2bccf1584c792d44ca54adf71bf3b`  
Ahead of common base: 6 commits.

Git history shows the intended alternating pattern:

1. Book 13 fresh checkpoint `1222919`;
2. Book 13 post-checkpoint lane findings/history records;
3. Book 14 fresh checkpoint `a699a49`;
4. Book 14 post-checkpoint findings/history records;
5. Book 15 fresh checkpoint `f992d69`;
6. Book 15 post-checkpoint Lane C findings/checkpoint update.

This satisfies the frozen fresh-before-history rule for all three Lane C books.

### Book 13 — Claude C. Hopkins, *Scientific Advertising*

The extraction keeps Hopkins's own claims of scientific certainty separate from the evidence actually supplied in the processed section. `empirical_within_source` is not granted merely because the author says something was tested; unreported measurement claims are left as caveated practitioner claims. The full 24-page visual pass finds no figures and correctly distinguishes "no digitisation loss" from "the source itself does not reproduce the advertisements it argues from."

### Book 14 — Chip Heath & Dan Heath, *Made to Stick*

The Introduction is used as the coherent unit because that is where the six-principle framework exists as a framework. The system layer preserves the checklist/Curse-of-Knowledge structure instead of flattening it into six disconnected rules. Third-party empirical studies are recorded in prose caveats rather than mislabelled `empirical_within_source`, exposing a real evidence-vocabulary limitation without changing the frozen method.

### Book 15 — Rory Sutherland, *Alchemy*

The extraction preserves the source's anti-rational/practitioner character instead of converting it into a stronger rulebook. Source uncertainty and internal contradictions are retained; the implied working method is marked `extractor_synthesis`; no mechanism is invented where the source supplies none. The visual pass recovers the argument-carrying quadrant chart whose placements are absent from prose.

## Cross-lane observations to preserve for final synthesis

These are observations to carry forward, not schema changes now:

1. **Evidence-characteristic gap:** Lane C sees the same `empirical_within_source` limitation in three books but in different forms: claimed measurement without reported evidence, cited third-party research, and a mixture of own and third-party experiments. This is now a strong within-domain recurrence; only final cross-lane synthesis should decide whether it warrants a consolidated revision.
2. **Visual completeness is source-format-sensitive:** Lane A distinguishes no-page EPUBs from misleading reflowed PDFs; both can retain figures while losing authored page composition. File extension alone is not sufficient evidence of page-level visual completeness.
3. **Raw object counts are not comparable across books:** Lane A's similarly sized Samara and Freeman sections still produce materially different object counts, supporting source-shape as a real driver while preserving section size as a confound.
4. **System layer continues to earn its keep:** Lane C's framework-heavy sources would be materially flattened without SourceConceptSystems; *Alchemy* also shows why system origin (`source_explicit` vs `extractor_synthesis`) matters.

## Verification limitation

The lane workers report that all five accepted books pass the frozen SPEC-03/04/05 mechanical validation, using scratchpad validators. Those validators were not committed, so the Controller did **not** independently rerun the exact validation command in this audit. The acceptance here is therefore based on verified Git checkpoint order, changed-file scope, source/provenance/visual-method spot checks, and absence of a Controller-level method violation. The planned fresh CANON-003 integration session must mechanically revalidate every per-book output before final batch closure.

## Next gate

- Lane A: STOP; leave branch untouched.
- Lane C: STOP; leave branch untouched.
- Remaining work toward 18: audit/finish Lane B Books 9, 10 and 12; rebalance worker Books 8 and 11.
- Do not merge or synthesize lanes until the dedicated final integration session.
