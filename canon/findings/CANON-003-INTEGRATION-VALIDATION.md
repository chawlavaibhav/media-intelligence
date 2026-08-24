# CANON-003 — Integration validation record

**Date:** 24 Aug 2026  
**Branch:** `work/canon-003-integration-16`

## Purpose

Record what was independently revalidated during the 16-book integration, including defects that lane-local ephemeral validators did not catch and the evidence used to close them.

## Reproducible instrument

Integration added:

- `canon/validation/validate_canon003_integrated.py`
- `tests/test_validate_canon003_integrated.py`

The validator checks mechanically reproducible constraints from SPEC-03/04/05 and intentionally does not pretend to re-judge source interpretation, visual meaning or extraction quality.

Validator development used a red/green sequence. The initial test failed because the validator module did not exist. After implementation, a corpus run exposed an over-strict validator assumption: it required inspected figure refs for `text_and_visual`, although the frozen SPEC-03 mechanical rule requires that only for `visual`. A regression test was added first, observed failing, and the validator was then corrected. The five unit tests passed in the last complete GitHub Actions run.

## Last complete strict corpus run

After the validator correction and after all 16 accepted directories were present, the strict run saw:

- 16 books
- 505 SourceKnowledge objects
- 54 SourceConceptSystems
- 417 ontology terms
- 53 concepts
- 111 operational bindings

It reported exactly **24 data errors**, all confined to three directories:

1. *Made to Stick*: one YAML parse failure caused by quoting inside a flow-style mapping.
2. *Scientific Advertising*: 16 remedy terms (`t_hop_sa_0016` through `t_hop_sa_0031`) lacked SPEC-05's required `executable_by` field.
3. *Alchemy*: 7 remedy terms (`t_sut_alc_0009` through `t_sut_alc_0015`) lacked the same field.

No other accepted directory had an error in that run.

## Integration repairs

The integration branch made only mechanical compliance repairs to those failures:

- re-quoted the Made to Stick role scalar without changing its value;
- added `executable_by: [unknown]` to all 16 Hopkins remedies;
- added `executable_by: [unknown]` to all 7 Sutherland remedies.

`unknown` is an allowed SPEC-05 value and is intentionally used rather than inferring a generative, deterministic, physical or human executor that the extraction did not establish.

Original lane checkpoint commits remain unchanged on their source branches; the repairs are explicit integration-time corrections.

## Post-repair verification

The auto-running temporary GitHub Actions workflow was removed after it created noisy failure notifications. It is not part of the integration deliverable.

Post-repair verification therefore used the prior strict run as a closed defect inventory plus direct verification of every modified defect:

- the exact repaired Made to Stick YAML content was parsed successfully with PyYAML;
- branch content was re-read for Hopkins terms 0016–0031 and all 16 contain `executable_by: [unknown]`;
- branch content was re-read for Sutherland terms 0009–0015 and all 7 contain `executable_by: [unknown]`;
- none of the repairs changed ids, references, counts, source claims, concepts, bindings or relationships.

Because the final full validator was not re-executed after deleting the noisy workflow, this record does **not** claim a fresh end-to-end CI run on the final head. It claims the narrower thing supported by the evidence: the last full run had a complete 24-defect inventory, every listed defect was repaired, the one previously unparsable document now parses, and all previously missing required fields are present.

## Acceptance consequence

The integration validator should remain committed and be used as the mechanical acceptance instrument in the next controlled environment. Lane-local scratchpad validators should no longer be treated as durable verification evidence.
