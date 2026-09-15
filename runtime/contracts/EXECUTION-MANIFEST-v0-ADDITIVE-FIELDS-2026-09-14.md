# EXECUTION-MANIFEST-v0 — additive fields (14 Sep 2026, production-learning UPWORK-INTRO-001)

`EXECUTION-MANIFEST-v0.yaml` is a frozen contract; no v0 field is changed here. The bridge now ALSO writes
the fields below. A reader that knows only v0 can ignore them; a reader that wants pool liquidity reads them.
They are additive so the manifest can say "this attempt is authorised but its pool cannot pay for it"
(SD-11: spend authority != provider liquidity) without a new contract version for one block.

| Field | Where | Meaning |
|---|---|---|
| `pool_liquidity` | manifest | `{status: read \| partial \| unknown \| not_read, readings: {pool: {balance_usd, remaining_usd, read_utc, source}}, pools_without_reading: [...], attempts_blocked_by_pool: n, rule}` — `not_read` means build() was given no `PoolLiquidity`; nothing is assumed |
| `attempts[].pool_liquidity` | attempt | `{pool, status: funded \| not_funded \| unknown \| not_read, funded: true \| false \| null, reason}` — evaluated in reservation order, drawing the reading down |
| `attempts[].blocked_by_pool` | attempt | `true` when the pool reading cannot fund `expected_cost_usd`; then `would_dispatch` is `false` and `refusal_reason` carries `blocked_by_pool: …` |
| `attempts[].would_dispatch_if_funded` | attempt | the pool-agnostic answer the v0 field `would_dispatch` used to give: harness shape verified, price agrees with the harness, within the ceiling. Primary attempts only (fallbacks: `if_triggered_would_dispatch_if_funded`) |
| `pool_liquidity.attempts_not_dispatchable_unknown_liquidity` | manifest | attempts that would go if funded but whose pool is unknown / unread |

**Semantics change to the v0 field `would_dispatch` (Controller audit on PR #98, blocker 3 — fail closed):**
`would_dispatch` is `true` only when `would_dispatch_if_funded` holds AND the attempt's pool is positively
known to fund it (`pool_liquidity.funded: true`). An unknown or unread pool leaves it `false` with
`refusal_reason` `pool_liquidity_unknown: …`. Spend authority never implies a route is usable. Dry planning
keeps the hypothetical visible in `would_dispatch_if_funded`; the dry battery therefore shows
`would_dispatch: false` on every attempt (no pool is read at USD 0) and `would_dispatch_if_funded: true`
where it used to show `would_dispatch: true`.

Source of readings: `runtime/execute/pools.py` `PoolLiquidity.from_readings([...])` — each reading names the
pool, the balance (or `null` when the pool is known but not readable by API, e.g. Vertex credits), when it
was read and from where. The bridge never reads a balance itself. If a v1 of this contract is cut, these
fields fold into it.
