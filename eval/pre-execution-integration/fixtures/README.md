# EVAL-011 negative fixtures

Each directory holds the ONE file a fixture mutates, plus the gate it must trip.

These are materialised from `validators/test_negative_fixtures.py` so a reviewer can read the
broken input without running anything. The test builds them in a temp copy at run time; these
copies are for inspection and are never read by the validator.

| fixture | gate | mutated file |
|---|---|---|
| `nc-family-count-12` | G1 | CONDITION-ENVELOPE-CONTRACT.yaml |
| `nc-cells-4096` | G2 | CONDITION-ENVELOPE-CONTRACT.yaml |
| `nc-drop-a-family` | G1 | CONDITION-ENVELOPE-CONTRACT.yaml |
| `nc-operation-vocab-drift` | G3 | CONDITION-ENVELOPE-CONTRACT.yaml |
| `nc-provenance-collapse` | G4 | CONDITION-ENVELOPE-CONTRACT.yaml |
| `nc-layer13-claims-cpao` | G5 | STAGED-EXECUTION-PLAN.yaml |
| `nc-vid05-early-cpao` | G6 | SCIENTIFIC-SLOT-SUPPLY-RECONCILIATION.yaml |
| `nc-seed-pooling` | G7 | CONDITION-ENVELOPE-CONTRACT.yaml |
| `nc-sourcing-deletes-a-slot` | G8 | SCIENTIFIC-SLOT-SUPPLY-RECONCILIATION.yaml |
| `nc-silent-sibling-substitution` | G9 | SCIENTIFIC-SLOT-SUPPLY-RECONCILIATION.yaml |
| `nc-partial-stage-totalled` | G10 | PRICE-READY-STAGED-FORECAST.yaml |
| `nc-cash-outlay-guessed` | G10 | PRICE-READY-STAGED-FORECAST.yaml |
| `nc-173-hours-mandatory` | G11 | EVALUATOR-AND-MATERIAL-STAGE-MAP.yaml |
| `nc-stage-counts-do-not-reconcile` | G13 | STAGED-EXECUTION-PLAN.yaml |
| `nc-stage-q-spends-generations` | G13 | STAGED-EXECUTION-PLAN.yaml |
| `nc-pass-rate-saving-invented` | G13 | STAGED-EXECUTION-PLAN.yaml |
