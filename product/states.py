"""Kept for existing imports: the state machine now lives in product/flow.py (spec §6, §12)."""
from product.flow import (ALLOWED, CUSTOMER_STATES, FOUNDER_ONLY_EDGES, FOUNDER_ONLY_FROM, PAUSES, RAIL, STATES,  # noqa: F401
                          TERMINAL, WORKER_STATES, can, label, needs_founder, rail_position)
