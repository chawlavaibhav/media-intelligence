"""runtime/route — turning a PRODUCTION-SPEC's capability requirements into a ROUTE-DECISION.

    evidence.py    the taint register and the routing map, fingerprint-bound; the evidence gate
    price.py       the roster, the price pins, and the harness's own price rules
    profile.py     the active policy profile, failing closed on any limit it does not carry
    spec.py        PRODUCTION-SPEC-v1, the only thing the router matches on
    attempt_id.py  the customer identity namespace a provider attempt would carry
    decision.py    candidate discovery, the fixed selection order, the cost envelope, execute's refusals
    cli.py         --plan (offline), --cells (audit), --execute (refuses)

Nothing in this package dispatches. There is no provider client here to call by accident.
"""
