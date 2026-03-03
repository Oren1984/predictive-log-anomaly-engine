"""Stage 7 — API: FastAPI application factory."""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI

from ..health.checks import HealthChecker
from ..observability.metrics import MetricsMiddleware, MetricsRegistry
from ..security.auth import AuthMiddleware
from .pipeline import Pipeline
from .routes import router
from .settings import Settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def _lifespan(app: FastAPI):
    """Load ML models on startup; nothing to clean up on shutdown."""
    pipeline: Pipeline = app.state.pipeline
    logger.info("API startup: loading inference pipeline ...")
    try:
        pipeline.load_models()
        logger.info("API startup: pipeline ready")
    except Exception as exc:
        logger.error("API startup: pipeline load failed: %s", exc)
        # Continue anyway so /health can report unhealthy
    yield
    logger.info("API shutdown")


def create_app(
    settings: Optional[Settings] = None,
    pipeline: Optional[Pipeline] = None,
) -> FastAPI:
    """
    Application factory.

    Parameters
    ----------
    settings    : Settings instance (env-driven when None)
    pipeline    : pre-built Pipeline (skip model loading when provided)
                  Useful in tests — pass a mock Pipeline with a no-op load_models.
    """
    cfg = settings or Settings()

    # ------------------------------------------------------------------
    # Metrics (created before pipeline so pipeline can reference it)
    # ------------------------------------------------------------------
    metrics: Optional[MetricsRegistry] = None
    if cfg.metrics_enabled:
        metrics = MetricsRegistry()

    # ------------------------------------------------------------------
    # Pipeline
    # ------------------------------------------------------------------
    if pipeline is None:
        pipeline = Pipeline(settings=cfg, metrics=metrics)

    # ------------------------------------------------------------------
    # Health checker
    # ------------------------------------------------------------------
    health_checker = HealthChecker(pipeline=pipeline)

    # ------------------------------------------------------------------
    # App
    # ------------------------------------------------------------------
    app = FastAPI(
        title="Predictive Log Anomaly Engine",
        description="Stage 7 — REST API for real-time log anomaly detection",
        version="0.7.0",
        lifespan=_lifespan,
    )

    # Attach shared state
    app.state.pipeline = pipeline
    app.state.metrics = metrics
    app.state.health_checker = health_checker
    app.state.settings = cfg

    # ------------------------------------------------------------------
    # Middleware (outermost first → innermost last)
    # ------------------------------------------------------------------
    if cfg.metrics_enabled:
        app.add_middleware(MetricsMiddleware)

    app.add_middleware(
        AuthMiddleware,
        api_key=cfg.api_key,
        disable_auth=cfg.disable_auth,
        public_paths=cfg.public_endpoints,
    )

    # ------------------------------------------------------------------
    # Routes
    # ------------------------------------------------------------------
    app.include_router(router)

    return app
