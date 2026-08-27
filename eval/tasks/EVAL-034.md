# Task EVAL-034: Stage-A route, price and seed refresh

**TASK ID:** EVAL-034  
**AUTONOMY MODE:** autonomous  
**RESOURCE BUDGET:** USD 0 / INR 0. Public web research permitted. No provider/model calls and no account/payment actions.

## Objective

Make the frozen 12-slot Stage-A admission screen costable and execution-addressable using current official provider evidence.

## Scope

For each core slot:
IMG-01, IMG-02, IMG-03, IMG-04,
VID-01, VID-02, VID-03, VID-04, VID-05,
AUD-01, AUD-02, AUD-03

verify from official/primary documentation:
- exact current model ID/version;
- direct or aggregator route;
- route availability;
- generation billing unit and current price;
- evaluator-relevant output constraints;
- seed support and exact seed semantics;
- relevant duration/resolution/audio limits;
- authentication/environment variable required;
- whether route is execution-ready from the existing harness;
- any retirement/deprecation date.

Never substitute a sibling model because a frozen slot is inconvenient.

## Outputs

Create a new dated machine-readable refresh under `eval/empirical-planning/` rather than rewriting historical price evidence.

Classify each slot:
- EXECUTION_READY
- METADATA_READY_ADAPTER_MISSING
- ROUTE_OR_VERSION_UNRESOLVED
- NO_CURRENT_VALID_ROUTE

Compute:
- exact Stage-A generation cost for every fully priced slot;
- lower/upper totals only where mathematically justified;
- the largest remaining price/route gaps;
- the minimum useful live Stage-A subset that could be authorised without changing the scientific roster.

Also verify seed policy implications for the two-repeat Stage-A design.

## Evidence rule

Official provider/aggregator documentation is final evidence for identity, route and price. Secondary sources may be leads only and must not establish a price/model fact.

## Restrictions

No spend. No API calls. No account creation/funding. No roster redesign. No replacing unresolved models. Do not edit historical forecast files to make old numbers look current.

Commit and push to `work/eval-034-stage-a-supply-refresh`. Do not merge.