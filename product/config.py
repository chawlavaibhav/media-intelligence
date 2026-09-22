"""Settings, read once from the environment. Secrets are read by NAME and never logged."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# Key names whose values must never reach a log line, an error message, a prompt or a page.
SECRET_ENV_NAMES = ("ANTHROPIC_API_KEY", "GOOGLE_API_KEY", "GEMINI_API_KEY", "MI_VERTEX_SA_JSON",
                    "MI_SECRET_KEY", "ELEVENLABS_API_KEY", "FAL_KEY")


def _env(name: str, default: str | None = None) -> str | None:
    v = os.environ.get(name)
    return v if v not in (None, "") else default


@dataclass
class Settings:
    data_dir: Path
    # "simulated": no paid call can leave the process (providers + reasoning are local stand-ins).
    # "live": real providers; still refused per call unless the job's budget authorises it.
    provider_mode: str = "simulated"
    reasoning_mode: str = "simulated"
    creative_model: str = "claude-opus-5"
    reviewer_provider: str = "gemini"            # "gemini" (independent family) or "anthropic"
    reviewer_model: str = "gemini-3.5-flash"
    reviewer_fallback_model: str = "claude-sonnet-5"
    vertex_project: str | None = None
    vertex_region: str = "us-central1"
    max_upload_bytes: int = 40 * 1024 * 1024
    account_default_ceiling_usd: Decimal = Decimal("25.00")
    worker_concurrency: int = 4
    lease_seconds: int = 900
    # Hold every finished cut for an operator look before the customer sees it (H-6: on for early beta).
    hold_before_preview: bool = True
    base_url: str = "http://localhost:8080"
    fault_injection: dict = field(default_factory=dict)

    @property
    def db_path(self) -> Path:
        return self.data_dir / "mi.sqlite3"

    @property
    def media_dir(self) -> Path:
        return self.data_dir / "media"

    def secret(self, name: str) -> str | None:
        return _env(name)


def load(data_dir: str | Path | None = None, **overrides) -> Settings:
    d = Path(data_dir or _env("MI_DATA_DIR", str(REPO / ".mi-data"))).resolve()
    s = Settings(
        data_dir=d,
        provider_mode=_env("MI_PROVIDER_MODE", "simulated"),
        reasoning_mode=_env("MI_REASONING_MODE", "simulated"),
        creative_model=_env("MI_CREATIVE_MODEL", "claude-opus-5"),
        reviewer_provider=_env("MI_REVIEWER_PROVIDER", "gemini"),
        reviewer_model=_env("MI_REVIEWER_MODEL", "gemini-3.5-flash"),
        vertex_project=_env("MI_VERTEX_PROJECT"),
        vertex_region=_env("MI_VERTEX_REGION", "us-central1"),
        hold_before_preview=_env("MI_HOLD_BEFORE_PREVIEW", "1") == "1",
        base_url=_env("MI_BASE_URL", "http://localhost:8080"),
        worker_concurrency=int(_env("MI_WORKER_CONCURRENCY", "4")),
    )
    for k, v in overrides.items():
        setattr(s, k, v)
    if s.provider_mode not in ("simulated", "live") or s.reasoning_mode not in ("simulated", "live"):
        raise ValueError("MI_PROVIDER_MODE / MI_REASONING_MODE must be 'simulated' or 'live'")
    s.data_dir.mkdir(parents=True, exist_ok=True)
    s.media_dir.mkdir(parents=True, exist_ok=True)
    return s


def scrub(text: str) -> str:
    """Replace any secret value that appears in text with its name."""
    text = str(text)
    for n in SECRET_ENV_NAMES:
        v = os.environ.get(n)
        if v and len(v) > 6 and v in text:
            text = text.replace(v, f"<{n}>")
    return text
