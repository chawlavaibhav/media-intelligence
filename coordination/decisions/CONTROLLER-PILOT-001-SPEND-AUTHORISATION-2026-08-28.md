# Controller — PILOT-001 Spend Authorisation — 2026-08-28

## Status
**PAID PILOT-001 EXECUTION AUTHORISED WITHIN THE FROZEN BOUNDARY.**

User approval received in chat on 2026-08-28 in response to the Controller's explicit proposal:

- max consumed API spend: **USD 2.00**
- retries authorised: **0**

This authority applies only to the frozen Aight vertical slice under
`coordination/decisions/CONTROLLER-PILOT-001-AIGHT-FREEZE-2026-08-28.md`.

It does not authorise:
- any third provider generation;
- automatic retry;
- T2 model comparison;
- Registry admission;
- Stage B/C;
- any model/provider substitution;
- any spend beyond USD 2.00.

The one-repair policy remains unchanged: at most one repair total. A second provider call is allowed
only if that single repair genuinely requires a new motion plate.

```yaml
machine_authorisation:
  tranche_id: PILOT-001
  authorised: true
  max_consumed_api_spend_usd: "2.00"
  retries_authorised: 0
  approved_by: "Vaibhav Chawla"
  approved_at: "2026-08-28T07:22:45Z"
```

## Execution conditions

Before dispatch:
1. reverify the exact direct Gemini model identifier, request contract, supported 8s / 9:16 / 720p
   configuration and current price;
2. use direct Gemini Developer API with `GEMINI_API_KEY` only;
3. materialise a matching local `authorization.pilot.local.yaml`;
4. open the persistent PILOT-001 spend runtime;
5. reserve estimated spend before the network send.

If the current provider contract has materially changed or the runtime credential is unavailable,
stop rather than substitute a route or fabricate evidence.
