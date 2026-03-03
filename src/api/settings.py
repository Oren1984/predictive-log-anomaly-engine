"""Stage 7 — API: application settings (env-driven)."""
from __future__ import annotations

import os
from dataclasses import dataclass, field


def _env_bool(name: str, default: bool) -> bool:
    val = os.environ.get(name, "").lower()
    if val in ("true", "1", "yes"):
        return True
    if val in ("false", "0", "no"):
        return False
    return default


@dataclass
class Settings:
    """
    All tuneable parameters for the Stage 7 API service.

    Each field falls back to an environment variable with the same name
    (upper-cased) when not supplied directly.
    """

    # -- Server
    api_host: str = field(
        default_factory=lambda: os.environ.get("API_HOST", "0.0.0.0")
    )
    api_port: int = field(
        default_factory=lambda: int(os.environ.get("API_PORT", "8000"))
    )

    # -- Security
    api_key: str = field(
        default_factory=lambda: os.environ.get("API_KEY", "")
    )
    disable_auth: bool = field(
        default_factory=lambda: _env_bool("DISABLE_AUTH", False)
    )
    public_endpoints: tuple[str, ...] = field(
        default_factory=lambda: tuple(
            p.strip()
            for p in os.environ.get("PUBLIC_ENDPOINTS", "/health,/metrics").split(",")
            if p.strip()
        )
    )

    # -- Observability
    metrics_enabled: bool = field(
        default_factory=lambda: _env_bool("METRICS_ENABLED", True)
    )

    # -- Inference pipeline
    model_mode: str = field(
        default_factory=lambda: os.environ.get("MODEL_MODE", "ensemble")
    )
    window_size: int = field(
        default_factory=lambda: int(os.environ.get("WINDOW_SIZE", "50"))
    )
    stride: int = field(
        default_factory=lambda: int(os.environ.get("STRIDE", "10"))
    )

    # -- Alert buffer
    alert_buffer_size: int = field(
        default_factory=lambda: int(os.environ.get("ALERT_BUFFER_SIZE", "200"))
    )

    # -- Alert cooldown
    alert_cooldown_seconds: float = field(
        default_factory=lambda: float(
            os.environ.get("ALERT_COOLDOWN_SECONDS", "60.0")
        )
    )

    # -- Demo / fallback mode
    # DEMO_MODE=true lowers the fallback scorer output to a value above the
    # model threshold so at least one alert fires even without trained models.
    # Never enable in production.
    demo_mode: bool = field(
        default_factory=lambda: _env_bool("DEMO_MODE", False)
    )
    demo_score: float = field(
        default_factory=lambda: float(os.environ.get("DEMO_SCORE", "2.0"))
    )
