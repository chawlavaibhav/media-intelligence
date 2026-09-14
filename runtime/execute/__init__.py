"""runtime/execute — the bridge from a ROUTE-DECISION to provider attempts (PC-03C, lane F, 14 Sep 2026).

    bridge.py         ExecutionBridge.build() renders every attempt the decision allows through the
                      harness adapter's dry_run(); .run() performs dry mode (sends nothing) or refuses live
    manifest.py       the EXECUTION-MANIFEST-v0 shapes, ids, hashes and a person-readable rendering
    authorisation.py  the signed runtime spend authorisation a LIVE dispatch would need; none exists

WHAT THIS PACKAGE DOES NOT DO. It never constructs a transport, never reads a key, never opens a socket.
Under dispatch_mode dry every attempt is rendered and priced and nothing leaves the machine; under
dispatch_mode live it refuses, because no signed runtime spend authorisation exists and live dispatch is
not wired in this tranche. Both refusals name exactly what is missing.
"""
