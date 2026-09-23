# Spend record — P1 live validation (2026-09-23)

**Authorised by the founder (Vaibhav), 2026-09-23, in the laptop session, verbatim:**
> USD 20 approved, run the reviewer qualification first. you already have gcp key. you also have azure account access of
> aight. probably pick a model from gpt family for now. 4. approved. 5. i will judge

| Item | Cap (USD) | Order |
|---|---:|---|
| Reviewer qualification — MOKO7 v1 + v2 through the product's reviewer (Gemini 3.5 Flash, Gemini API key) | 1.00 | first |
| One live image job through the web UI | 4.00 | after qualification |
| One live 30-s film job through the web UI | 15.00 | after the image job |
| **Total ceiling (cumulative; an amendment never resets consumed spend)** | **20.00** | |

- Reasoning: a GPT-family model on the **getaight** Azure subscription (b832f4a1) only — never the Wherehouse default
  subscription, never resource group project-1. Media: Gemini API key (stills, and Veo/Lyria where the Gemini API serves them).
- Enforcement: each run is a product job with its own ledger and a budget ≤ its line above; the reservation is refused past it.
- Judge of outputs: the founder. Hosting (decision 4): approved — one small VM + DNS, created after the live jobs pass locally.
- Spend of record is appended below as it happens (ledger figures, not estimates).

## Spend of record
| When (UTC) | What | Ledger USD | Cumulative |
|---|---|---:|---:|
| 2026-09-23 | Reviewer qualification v1 — gemini-3.5-flash @1 fps (1 call) | 0.037200 | 0.037200 |
| 2026-09-23 | Reviewer qualification v1 — gemini-3.1-pro-preview @4 fps (1 call) | 0.066064 | 0.103264 |
| 2026-09-23 | Azure OpenAI gpt-5.6-sol connection test (1 call) | 0.001240 | 0.104504 |
| 2026-09-23 | Live image job (job_20260923_6720871c) through understanding, 2 directions, 6 stills — at operator hold for takes | 2.178217 | 2.282721 |
