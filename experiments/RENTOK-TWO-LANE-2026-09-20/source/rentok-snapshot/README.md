# Frozen product-source snapshot — rentok.com (fetched by the Controller, USD 0)

Fetched: see `fetched_utc.txt`. Hashes: `SHA256SUMS.txt`. Pages: `home.html` (https://rentok.com/), `complaint-management.html`, `tenant-verification.html`, `autopay.html` (each `https://rentok.com/<name>`). `*.txt` = visible text extracted from each page (scripts/styles stripped, duplicate lines removed) for reading; the `.html` is the evidence.

Both lanes verify every product claim against these same bytes, so that a difference in claims between lanes is a difference in reasoning, not in what the site showed at the time. A lane may fetch further pages itself; it must record URL, UTC time and sha256 of anything it relies on.
