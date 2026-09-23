"""Settings, read once from the environment. Secrets are read by NAME and never logged."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# Key names whose values must never reach a log line, an error message, a prompt or a page.
SECRET_ENV_NAMES = ("AZURE_OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY", "GEMINI_API_KEY", "MI_VERTEX_SA_JSON",
                    "MI_SECRET_KEY", "ELEVENLABS_API_KEY", "FAL_KEY")


def _env(name: str, default: str | None = None) -> str | None:
    v = os.environ.get(name)
    return v if v not in (None, "") else default


# Spec §9.3: each worker's model is configuration (MI_MODEL_<WORKER>="provider:model"), never hard-coded in a station.
# Tiers: strongest (chef) — company A; strong, another company (recipe checker, big taster, small-taster escalation) —
# company B; cheap (waiter, pantry checker, small taster, diary writer). The decision slot is optional (spec §9.3, H4).
# Amendment 1 §1: image jobs only use a cheaper chef (MI_MODEL_CHEF_IMAGE), a mid-tier model from the film chef's company.
DEFAULT_WORKER_MODELS = {
    "chef": "azure_openai:gpt-5.6-sol",
    "chef_image": "azure_openai:gpt-5.6-terra",
    "recipe_checker": "gemini:gemini-3.1-pro-preview",
    "big_taster": "gemini:gemini-3.1-pro-preview",
    "small_taster_escalation": "gemini:gemini-3.1-pro-preview",
    "waiter": "anthropic:claude-haiku-4-5",
    "pantry_checker": "anthropic:claude-haiku-4-5",
    "small_taster": "anthropic:claude-haiku-4-5",
    "diary_writer": "anthropic:claude-haiku-4-5",
}
COMPANY = {"anthropic": "anthropic", "azure_openai": "openai", "openai": "openai", "gemini": "google", "decision": "decision"}
# Reasoning effort per worker (spec §9.4: medium by default).
DEFAULT_EFFORT = {"chef": "medium", "chef_image": "medium", "recipe_checker": "medium", "big_taster": "medium", "small_taster_escalation": "medium"}


def worker_models() -> dict:
    out = dict(DEFAULT_WORKER_MODELS)
    for w in list(out):
        v = _env("MI_MODEL_" + w.upper())
        if v:
            out[w] = v
    dm = _env("MI_MODEL_DECISION")
    if dm:
        out["decision"] = dm
    return out


def check_independence(models: dict):
    """The chef and the judges must come from different AI companies (spec §3, §9.3, checklist C4)."""
    def company(w):
        return COMPANY.get(models[w].split(":", 1)[0], models[w].split(":", 1)[0])
    for chef in [c for c in ("chef", "chef_image") if c in models]:
        for judge in ("recipe_checker", "big_taster"):
            if company(judge) == company(chef):
                raise ValueError(f"the {chef} ({models[chef]}) and the {judge} ({models[judge]}) are from the same company; "
                                 f"the judges must be independent")


@dataclass
class Settings:
    data_dir: Path
    # "simulated": no paid call can leave the process (providers + reasoning are local stand-ins).
    # "live": real providers; still refused per call unless the job's budget authorises it.
    provider_mode: str = "simulated"
    reasoning_mode: str = "simulated"
    creative_model: str = "claude-opus-5"
    creative_provider: str = "anthropic"          # "anthropic" | "azure_openai" (founder 2026-09-23: GPT family on Aight Azure)
    reviewer_provider: str = "gemini"            # "gemini" (independent family) or "anthropic"
    reviewer_model: str = "gemini-3.5-flash"
    reviewer_fallback_model: str = "claude-sonnet-5"
    # An UNQUALIFIED model reviewer's PASS is not evidence (MOKO7 v1 qualification 2026-09-23: Gemini 3.5 Flash 1/6,
    # Gemini 3.1 Pro @4 fps 1/6, both passing a torn bag as "faithful"). Its FAILs still count. A person confirms the rest.
    reviewer_qualified: bool = False
    review_fps: float | None = None              # frames/s the video reviewer samples (Gemini videoMetadata); None = provider default
    media_surface: str = "gemini_api"             # "gemini_api" (GOOGLE_API_KEY) | "vertex" (service account)
    vertex_project: str | None = None
    vertex_region: str = "us-central1"
    max_upload_bytes: int = 40 * 1024 * 1024
    account_default_ceiling_usd: Decimal = Decimal("25.00")
    worker_concurrency: int = 4
    lease_seconds: int = 900
    # Hold every finished cut for the founder's look before the customer sees it. Amendment 1 §3: off by default — the
    # customer's preview is the final check; the founder may switch it on (MI_HOLD_BEFORE_PREVIEW=1) to intervene.
    hold_before_preview: bool = False
    base_url: str = "http://localhost:8080"
    fault_injection: dict = field(default_factory=dict)
    models: dict = field(default_factory=lambda: dict(DEFAULT_WORKER_MODELS))
    # Judges that have passed qualification (spec §10). Until then a judge's "no" blocks and its "yes" = founder confirms.
    qualified_judges: tuple = ()

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
        creative_provider=_env("MI_CREATIVE_PROVIDER", "anthropic"),
        reviewer_provider=_env("MI_REVIEWER_PROVIDER", "gemini"),
        reviewer_model=_env("MI_REVIEWER_MODEL", "gemini-3.5-flash"),
        review_fps=float(_env("MI_REVIEW_FPS")) if _env("MI_REVIEW_FPS") else None,
        reviewer_qualified=_env("MI_REVIEWER_QUALIFIED", "0") == "1",
        vertex_project=_env("MI_VERTEX_PROJECT"),
        media_surface=_env("MI_MEDIA_SURFACE", "gemini_api"),
        vertex_region=_env("MI_VERTEX_REGION", "us-central1"),
        hold_before_preview=_env("MI_HOLD_BEFORE_PREVIEW", "0") == "1",
        base_url=_env("MI_BASE_URL", "http://localhost:8080"),
        worker_concurrency=int(_env("MI_WORKER_CONCURRENCY", "4")),
        models=worker_models(),
        qualified_judges=tuple(x for x in (_env("MI_QUALIFIED_JUDGES", "") or "").split(",") if x),
    )
    for k, v in overrides.items():
        setattr(s, k, v)
    check_independence(s.models)
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
