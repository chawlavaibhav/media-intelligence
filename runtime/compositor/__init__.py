"""Deterministic compositor gates (promoted from production-learning case UPWORK-INTRO-001).

The pilot's V3 film was rejected for text clipped at edges, text lost against photographs, cropped
creatives and mixed card geometry; its V4 ad beat for an offer/code collision. None of those was a model
failure — each was a compositor drawing without a rule. The V4 compositor (pilots/…/v4/tools/design4.py)
turned every rule into a function that raises; this package ports those rules into the runtime as pure
stdlib functions over geometry and colour so any renderer (Pillow, hb-view, a browser) can be held to them.
Pixel reading stays with the caller: the contrast gate takes luminance samples, never an image.
"""
from runtime.compositor.gates import LayoutRefused  # noqa: F401
from runtime.compositor.tokens import DesignTokens  # noqa: F401
