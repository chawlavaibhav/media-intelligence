# Spend authorisation of record — RentOK two-lane experiment

Recorded: 2026-09-20T18:14:39Z by the Media Intelligence Controller session, from the human Controller's answers in this session (a structured question in the Claude desktop app; wording of the options was written by the Controller session, the selection is the human's).

## Question 1 (cap per lane) — put to the human Controller verbatim

"Spend cap per lane for the RentOK game experiment? (Equal for both lanes; credits only — Google Vertex/Gemini, ElevenLabs, Sarvam; no fal; 0 hidden retries; hard stop at the cap; the Cumin USD 5/lane packages authorise nothing here.) I recommend USD 10 per lane: a 30-second game film needs sprites/backgrounds (nano-banana-2 ≈ USD 0.07 each), possibly Veo 3.1 Fast clips (USD 0.10/s), Lyria music (USD 0.06/clip), TTS, plus one repair round."

**Answer selected (verbatim option text):** "USD 10 per lane (Recommended)" — described as "USD 20 total across both lanes. Room for a micro-qualification draw, the asset set, one repair round."

## Question 2 (credits pool attestation) — verbatim

"The Google credit balance cannot be read by the project service account (Cloud Billing API is disabled on vertexaiproject-507518), and you had a 'Google Cloud balance refund' session today. Can you confirm the Google Vertex/Gemini credits pool is still funded and usable for this job? (Your answer is recorded verbatim as the pool attestation.)"

**Answer selected (verbatim option text):** "Yes, credits are funded — proceed" — described as "Recorded as the human attestation for the Google credits pool; every reservation stays an upper bound."

## What this authorises

| Lane | Job | Cap (USD) | Pools | Retries | Covers |
|---|---|---|---|---|---|
| A | AGY-2026-09-20-RENTOK-GAME-LANE-A-001 | 10.00 | Google Vertex/Gemini credits · ElevenLabs plan credits · Sarvam credits | 0 hidden; every re-send is a new counted attempt under the same cap | generation, micro-qualification, references, music, TTS, repairs |
| B | AGY-2026-09-20-RENTOK-GAME-LANE-B-001 | 10.00 | same | same | same |

- Caps are enforced against each lane's own append-only ledger () before every request leaves; nothing transfers between lanes; an amendment never resets consumed spend (C-6a).
- fal is excluded. No personal payment method; no new paid service.
- Pool balances: Google credits attested by the human above (not machine-readable); ElevenLabs/Sarvam balances are read from their APIs where the lane's tooling can, else attested by the same answer.
- Vendor-billed cost is a separate reconciliation field; the ledger figure is an upper bound (C-2).

## What this does not authorise

Anything outside these two jobs; any Controller-state, Canon, Registry or routing-map change; external delivery of either film (human release, C-8, stays with the human Controller at the blind evaluation).
