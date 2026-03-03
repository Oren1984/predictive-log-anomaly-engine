"""Stage 7 — API: route definitions."""
from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, Request
from starlette.responses import PlainTextResponse

from .schemas import (
    AlertListResponse,
    AlertSchema,
    HealthResponse,
    IngestRequest,
    IngestResponse,
    RiskResultSchema,
)

logger = logging.getLogger(__name__)

router = APIRouter()


# ---------------------------------------------------------------------------
# POST /ingest
# ---------------------------------------------------------------------------

@router.post("/ingest", response_model=IngestResponse)
async def ingest_event(body: IngestRequest, request: Request) -> IngestResponse:
    """
    Feed a single tokenised log event into the inference pipeline.

    Returns a scored window and optional alert whenever a stride boundary
    is crossed; otherwise returns ``window_emitted=False``.
    """
    pipeline = request.app.state.pipeline
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Pipeline not initialised")

    event = {
        "timestamp":  body.timestamp,
        "service":    body.service,
        "session_id": body.session_id,
        "token_id":   body.token_id,
        "label":      body.label,
    }

    try:
        result = pipeline.process_event(event)
    except Exception as exc:
        if pipeline.metrics:
            pipeline.metrics.ingest_errors_total.inc()
        logger.exception("Error processing ingest event: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    risk_schema = None
    if result["risk_result"] is not None:
        rr = result["risk_result"]
        risk_schema = RiskResultSchema(
            stream_key=rr["stream_key"],
            timestamp=float(rr["timestamp"]),
            model=rr["model"],
            risk_score=rr["risk_score"],
            is_anomaly=rr["is_anomaly"],
            threshold=rr["threshold"],
            evidence_window=rr["evidence_window"],
            top_predictions=rr.get("top_predictions"),
            meta=rr.get("meta", {}),
        )

    alert_schema = None
    if result["alert"] is not None:
        a = result["alert"]
        alert_schema = AlertSchema(
            alert_id=a["alert_id"],
            severity=a["severity"],
            service=a["service"],
            score=a["score"],
            timestamp=a["timestamp"],
            evidence_window=a["evidence_window"],
            model_name=a["model_name"],
            threshold=a["threshold"],
            meta=a.get("meta", {}),
        )

    return IngestResponse(
        window_emitted=result["window_emitted"],
        risk_result=risk_schema,
        alert=alert_schema,
    )


# ---------------------------------------------------------------------------
# GET /alerts
# ---------------------------------------------------------------------------

@router.get("/alerts", response_model=AlertListResponse)
async def list_alerts(request: Request) -> AlertListResponse:
    """Return the most-recent alerts from the in-memory ring buffer."""
    pipeline = request.app.state.pipeline
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Pipeline not initialised")

    raw = pipeline.recent_alerts()
    alerts = [
        AlertSchema(
            alert_id=a["alert_id"],
            severity=a["severity"],
            service=a["service"],
            score=a["score"],
            timestamp=a["timestamp"],
            evidence_window=a["evidence_window"],
            model_name=a["model_name"],
            threshold=a["threshold"],
            meta=a.get("meta", {}),
        )
        for a in raw
    ]
    return AlertListResponse(count=len(alerts), alerts=alerts)


# ---------------------------------------------------------------------------
# GET /health
# ---------------------------------------------------------------------------

@router.get("/health", response_model=HealthResponse)
async def health(request: Request) -> HealthResponse:
    """Liveness + readiness probe."""
    checker = getattr(request.app.state, "health_checker", None)
    if checker is None:
        return HealthResponse(
            status="unknown",
            uptime_seconds=0.0,
            components={},
        )
    payload = checker.check()
    return HealthResponse(**payload)


# ---------------------------------------------------------------------------
# GET /metrics
# ---------------------------------------------------------------------------

@router.get("/metrics", include_in_schema=False)
async def metrics(request: Request) -> PlainTextResponse:
    """Prometheus text-format metrics endpoint."""
    registry = getattr(request.app.state, "metrics", None)
    if registry is None:
        return PlainTextResponse("# metrics disabled\n")
    body, content_type = registry.generate_text()
    return PlainTextResponse(content=body, media_type=content_type)
