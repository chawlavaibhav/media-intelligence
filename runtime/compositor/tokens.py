"""One design-token source for every shared compositor primitive (SD-04: square + rounded cards).

A wrapper card, tab or bubble takes its radius, border, shadow, spacing and safe area from a DesignTokens
instance and nothing else. The instance is frozen: a renderer cannot write a radius per call. `check_geometry`
(gates.py) refuses a card whose values differ from the tokens it claims to come from.
"""
from __future__ import annotations

from dataclasses import dataclass, field, fields


@dataclass(frozen=True)
class DesignTokens:
    card_radius: int
    card_border_px: int
    card_shadow: tuple            # (blur, offset, alpha)
    safe_x: int
    safe_y: int
    spacing: tuple = (12, 24, 48, 96)
    contrast_body: float = 4.5
    contrast_display: float = 3.0
    display_threshold_px: int = 48
    min_gap_px: int = 0           # default disjointness gap for critical regions
    source: str = field(default="tokens", compare=False)

    @classmethod
    def from_mapping(cls, m: dict, *, source: str = "mapping") -> "DesignTokens":
        known = {f.name for f in fields(cls)}
        data = {k: v for k, v in m.items() if k in known}
        if "card_shadow" in data:
            data["card_shadow"] = tuple(data["card_shadow"])
        if "spacing" in data:
            data["spacing"] = tuple(data["spacing"])
        data["source"] = source
        return cls(**data)

    def safe_area(self, canvas: tuple) -> tuple:
        x0, y0, x1, y1 = canvas
        return (x0 + self.safe_x, y0 + self.safe_y, x1 - self.safe_x, y1 - self.safe_y)
