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

Source of readings: `runtime/execute/pools.py` `PoolLiquidity.from_readings([...])` — each reading names the
pool, the balance (or `null` when the pool is known but not readable by API, e.g. Vertex credits), when it
was read and from where. The bridge never reads a balance itself. If a v1 of this contract is cut, these
fields fold into it.
