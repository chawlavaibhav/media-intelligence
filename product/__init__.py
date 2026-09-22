"""Media Intelligence P1 — the customer-facing production product.

The runtime (`runtime/`) holds the contracts, Canon lookup, price book, compositor gates and provider
error classes. This package holds what turns them into a product: the persistent job store and
ledger, the orchestrator and worker, the reasoning components, the shared provider dispatch, the
media engine, the verification gateway, and the customer/operator web application.

Authoritative job state lives in the store (`product/store.py`), never in an LLM conversation.
"""
