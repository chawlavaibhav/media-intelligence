# Canon retrieval — scores

Corpus 1300 claims. Cited (truth): RentOK 82 (union of 4 jobs on one brief), Mokobara 22. Overlap between the two briefs: 17 claims (77% of Mokobara's).

## rentok (|truth| = 82)

| method | P@10 | P@20 | P@50 | R@20 | R@50 | R@20 / max |
|---|---|---|---|---|---|---|
| fixed popular list (learned from Mokobara job, no query) | 0.70 | 0.85 | – | 0.21 | – | 0.85 |
| agentic (blind LLM agent over a label index, 7 tool calls) | 0.80 | 0.65 | 0.56 | 0.16 | 0.34 | 0.65 |
| LLM re-rank of hybrid(LLM sub-queries) top-60 (blind) | 1.00 | 0.65 | – | 0.16 | – | 0.65 |
| hybrid (LLM sub-queries, RRF) | 0.60 | 0.60 | 0.34 | 0.15 | 0.21 | 0.60 |
| hybrid (LLM sub-queries) + cross-encoder rerank | 0.40 | 0.50 | 0.28 | 0.12 | 0.17 | 0.50 |
| dense bge-base (LLM sub-queries, RRF) | 0.50 | 0.40 | 0.30 | 0.10 | 0.18 | 0.40 |
| hybrid (brief + LLM sub-queries) + cross-encoder rerank | 0.50 | 0.40 | 0.26 | 0.10 | 0.16 | 0.40 |
| hybrid bm25+bge-base RRF (brief) | 0.30 | 0.35 | 0.24 | 0.09 | 0.15 | 0.35 |
| bm25 (LLM sub-queries, RRF) | 0.50 | 0.35 | 0.26 | 0.09 | 0.16 | 0.35 |
| hybrid + cross-encoder rerank (brief) | 0.40 | 0.30 | 0.28 | 0.07 | 0.17 | 0.30 |
| bm25 (brief, claim text only) | 0.30 | 0.25 | 0.18 | 0.06 | 0.11 | 0.25 |
| bm25 (brief, contextual doc) | 0.10 | 0.20 | 0.30 | 0.05 | 0.18 | 0.20 |
| dense bge-small-en-v1.5 (brief) | 0.20 | 0.20 | 0.18 | 0.05 | 0.11 | 0.20 |
| dense bge-base-en-v1.5 (brief) | 0.20 | 0.15 | 0.20 | 0.04 | 0.12 | 0.15 |
| dense bge-base (brief, claim text only) | 0.10 | 0.10 | 0.06 | 0.02 | 0.04 | 0.10 |
| random | 0.06 | 0.06 | 0.06 | 0.02 | 0.04 | 0.06 |
| dense e5-base-v2 (brief) | 0.10 | 0.05 | 0.08 | 0.01 | 0.05 | 0.05 |

## mokobara (|truth| = 22)

| method | P@10 | P@20 | P@50 | R@20 | R@50 | R@20 / max |
|---|---|---|---|---|---|---|
| fixed popular list (learned from RentOK jobs, no query) | 0.50 | 0.55 | 0.28 | 0.50 | 0.64 | 0.55 |
| agentic (blind LLM agent over a label index, 7 tool calls) | 0.30 | 0.40 | 0.26 | 0.36 | 0.59 | 0.40 |
| LLM re-rank of hybrid(LLM sub-queries) top-60 (blind) | 0.50 | 0.35 | – | 0.32 | – | 0.35 |
| dense bge-small-en-v1.5 (brief) | 0.20 | 0.20 | 0.10 | 0.18 | 0.23 | 0.20 |
| bm25 (LLM sub-queries, RRF) | 0.10 | 0.20 | 0.12 | 0.18 | 0.27 | 0.20 |
| hybrid (LLM sub-queries, RRF) | 0.00 | 0.15 | 0.12 | 0.14 | 0.27 | 0.15 |
| dense bge-base (brief, claim text only) | 0.10 | 0.10 | 0.04 | 0.09 | 0.09 | 0.10 |
| hybrid + cross-encoder rerank (brief) | 0.20 | 0.10 | 0.06 | 0.09 | 0.14 | 0.10 |
| hybrid (LLM sub-queries) + cross-encoder rerank | 0.10 | 0.10 | 0.04 | 0.09 | 0.09 | 0.10 |
| hybrid (brief + LLM sub-queries) + cross-encoder rerank | 0.20 | 0.10 | 0.08 | 0.09 | 0.18 | 0.10 |
| dense bge-base (LLM sub-queries, RRF) | 0.10 | 0.05 | 0.04 | 0.05 | 0.09 | 0.05 |
| random | 0.01 | 0.01 | 0.01 | 0.01 | 0.03 | 0.01 |
| bm25 (brief, claim text only) | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| bm25 (brief, contextual doc) | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| dense bge-base-en-v1.5 (brief) | 0.00 | 0.00 | 0.06 | 0.00 | 0.14 | 0.00 |
| dense e5-base-v2 (brief) | 0.00 | 0.00 | 0.04 | 0.00 | 0.09 | 0.00 |
| hybrid bm25+bge-base RRF (brief) | 0.00 | 0.00 | 0.02 | 0.00 | 0.05 | 0.00 |
