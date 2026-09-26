# Canon retrieval test: result (2026-09-25)

**Question.** Given a real customer brief, can a retriever find the Canon claims a producer actually cited by hand on
that job?

**Cost:** US$0. Local models on CPU, plus four blind Claude sub-agent steps inside a Claude Code session.
**Reproduce:**
1. `python3 run_retrieval_eval.py` (about 30 minutes on 4 CPUs).
2. `python3 score_runs.py` (seconds).

Full tables are in `SCORES.md`.

## Setup

**Corpus.** 1,300 accepted claims from 37 sources (`canon/knowledge/current/*/source-knowledge.yaml`).

**Queries.** The verbatim customer words of two briefs, taken from the job branches (`brief-rentok.txt`, `brief-mokobara.txt`).

**Ground truth.** `canon/validation/HAND-RETRIEVED-CLAIMS.yaml`:
- RentOK: 82 claims, the union of 4 jobs on the same brief.
- Mokobara: 22 claims.

**Blind steps.** Each agent saw only the brief and a sandbox copy of the corpus, never the ground truth.
- **Sub-queries.** An agent wrote 12 book-vocabulary search queries per brief (`llm-queries.json`).
- **Agentic retrieval.** An agent returned 50 ranked IDs per brief (`agentic-results.json`). It chose to scan a one-line index of all 1,300 concept labels and read about 15 claims in full, using 7 tool calls.
- **LLM re-rank.** An agent picked and ranked 20 of the top 60 candidates from the hybrid sub-query run (`llm-rerank.json`).

**Methods.**
- BM25, on the claim text alone and on a "contextual" document (source + label + claim + scope).
- Dense embeddings: bge-small, bge-base and e5-base.
- Hybrid BM25 + dense, fused by reciprocal rank.
- A bge-reranker-base cross-encoder.
- LLM sub-queries.
- The agentic run and the LLM re-rank.
- A **fixed popular-claims list with no query at all**, learned from the *other* brief's jobs.
- A random ordering.

## Results (P@k = the share of the top k that the producer actually cited)

| Method | RentOK P@10 | RentOK P@20 | Mokobara P@10 | Mokobara P@20 | Mokobara R@50 |
|---|---|---|---|---|---|
| Random | 0.06 | 0.06 | 0.01 | 0.01 | 0.03 |
| BM25 on the raw brief | 0.30 | 0.25 | 0.00 | 0.00 | 0.00 |
| Dense bge-base on the raw brief | 0.20 | 0.15 | 0.00 | 0.00 | 0.14 |
| Hybrid on the raw brief | 0.30 | 0.35 | 0.00 | 0.00 | 0.05 |
| Hybrid on the raw brief + cross-encoder | 0.40 | 0.30 | 0.20 | 0.10 | 0.14 |
| Hybrid on **LLM sub-queries** | 0.60 | 0.60 | 0.00 | 0.15 | 0.27 |
| …+ cross-encoder re-rank | 0.40 | 0.50 | 0.10 | 0.10 | 0.09 |
| …+ **LLM re-rank** (from the top 60) | **1.00** | 0.65 | 0.50 | 0.35 | – |
| **Agentic LLM over the label index** | 0.80 | 0.65 | 0.30 | 0.40 | **0.59** |
| **Fixed popular list, no query** | 0.70 | **0.85** | **0.50** | **0.55** | **0.64** |

**Overlap.** 77% of Mokobara's cited claims (17 of 22) were also cited on the RentOK jobs. Across all 5 jobs there are only
87 distinct cited claims: 22 were cited on 3 or more jobs, and 6 on all 5.

## What this says

1. **Classic RAG does not work on this Canon.**
   - Keyword and embedding search on the brief scored near random on Mokobara (P@20 0.00–0.20).
   - On RentOK they reached at most 0.35.
   - This confirms the earlier 0/22 keyword finding. The brief's words ("castaway", "bag", "arms") share almost no vocabulary with the books ("demonstration", "unique selling proposition", "reveal").
2. **A generic cross-encoder made things worse**, not better. It does not know what ad-craft relevance is.
3. **Putting an LLM in the loop is what makes retrieval work.**
   - LLM-written sub-queries roughly doubled precision.
   - An LLM re-ranking candidates is very precise: RentOK P@10 of 1.00; Mokobara put 7 of the 8 pooled hits in its top 20. Its limit is the first-stage pool, which held only 8 of Mokobara's 22.
   - An LLM scanning a compact **index of labels** (the Vercel / `llms.txt` pattern) was the best retriever.
4. **A small fixed list beat every retriever.** The claims producers actually use form a small, stable core, not something specific to each brief.

## Consequences for the design (consistent with MASTER-PLAN.md)

- **Do not build a vector or RAG system for the Canon.** It is the wrong tool for this corpus.
- **If the Canon feeds the author at all, give it two layers:**
  1. **A small fixed core card:** the roughly 20–40 claims that recur across jobs, compiled into short plain lines (the ≤15-question critique card fits this).
  2. **On-demand lookup by an LLM over a one-line-per-claim label index** for brief-specific extras, capped at about 10 claims.
- **Whether any of this improves finished media is still untested.** Mokobara v3 cited more Canon than any other job and was rejected. The week-3 ablation (CANON-ABL-1 in MASTER-PLAN §5) is the test that matters.

## Honest limits

- **Only 2 distinct briefs.** RentOK's 82 claims come from 4 jobs on one brief. Treat the numbers as directional; they are not statistics.
- **"Cited" is not the same as "needed".** Producers found claims through grep, packs and earlier job files. The 77% overlap may partly reflect habit: copying citations from previous jobs (the "experience-following" effect in arXiv 2505.16067). That would favour the fixed list and inflate its score.
- **The compiled packs were built to cover these exact IDs** (CANON-DONE condition B). Their 100% recall (369 IDs, 28% of the corpus) is circular, so they are not ranked here.
- **The agentic agent's behaviour depends on the agent.** It used 7 tool calls and a label scan, not many greps. A different agent or budget would score differently.
- **One run each, no seeds varied, CPU models only.** Larger embedding models or API embedders were not tried.
