# Gemma price pin — 2026-09-01

Single authorised network fetch under DN-07 (snapshot pattern, bytes + date):

- URL: `https://ai.google.dev/gemini-api/docs/pricing`
- Fetched: 2026-09-01 (curl -sL)
- File: `gemini-api-pricing.html`, 240,179 bytes
- SHA-256: `4752958931f5297cb502547a8c3a0ba386f96c2f3b52caf3e2cfe394b0bd690f`

What the pinned bytes say about Gemma 4: free tier input price "Free of charge",
output price "Free of charge", context caching "Free of charge"; paid tier
"Not available"; free tier "Used to improve our products: Yes".

Consequence: `price-snapshot-038.yaml` pins `gemma-4-31b-it` at USD 0.00 input /
0.00 output — an established official price (the design's Gemma-drop condition
"no unit price established" does not fire). Gemma trials therefore settle at
USD 0.00 in the spend ledger; usage tokens are still captured in full.
