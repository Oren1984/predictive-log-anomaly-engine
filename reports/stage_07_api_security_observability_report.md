# Stage 7 — API + Security + Observability Report

**Status: PASS**
**Date:** 2026-03-03
**Model:** claude-sonnet-4-6

---

## 1. Executive Summary

Stage 7 wraps the complete Stage 5–6 runtime pipeline (InferenceEngine →
AlertManager → N8nWebhookClient) in a production-ready FastAPI service.
All 40 new tests pass; the full 199-test suite passes with zero regressions.

---

## 2. Test Summary

| Test file | Tests | Result |
|---|---|---|
| `tests/test_stage_07_auth.py` | 11 | PASS |
| `tests/test_stage_07_ingest_integration.py` | 15 | PASS |
| `tests/test_stage_07_metrics.py` | 14 | PASS |
| **Stage 7 total** | **40** | **PASS** |
| Full suite (all stages) | 199 | PASS |

---

## 3. Endpoints Implemented

| Method | Path | Auth required | Description |
|---|---|---|---|
| `POST` | `/ingest` | Yes | Feed a tokenised event; returns window + optional alert |
| `GET` | `/alerts` | Yes | Ring-buffer of most-recent fired alerts |
| `GET` | `/health` | No | Liveness + readiness probe |
| `GET` | `/metrics` | No | Prometheus text-format metrics |

### POST /ingest

**Request body** (`application/json`):

```json
{
  "timestamp": 1704067200.0,
  "service": "hdfs",
  "session_id": "",
  "token_id": 10,
  "label": null
}
```

**Response** (`200 OK`):

```json
{
  "window_emitted": false,
  "risk_result": null,
  "alert": null
}
```

When a stride boundary is crossed:

```json
{
  "window_emitted": true,
  "risk_result": {
    "stream_key": "hdfs:",
    "timestamp": 1704067200.0,
    "model": "ensemble",
    "risk_score": 0.54,
    "is_anomaly": false,
    "threshold": 1.0,
    "evidence_window": { ... },
    "top_predictions": null,
    "meta": { "window_size": 50, "emit_index": 1 }
  },
  "alert": null
}
```

When an anomaly is detected (score ≥ threshold):

```json
{
  "window_emitted": true,
  "risk_result": { ... },
  "alert": {
    "alert_id": "3f8a2d1c-...",
    "severity": "critical",
    "service": "hdfs",
    "score": 2.4,
    "timestamp": 1704067200.0,
    "evidence_window": { ... },
    "model_name": "ensemble",
    "threshold": 1.0,
    "meta": { ... }
  }
}
```

### GET /alerts

Returns all alerts from the in-memory ring buffer (default cap: 200):

```json
{
  "count": 2,
  "alerts": [ { ... }, { ... } ]
}
```

### GET /health

```json
{
  "status": "healthy",
  "uptime_seconds": 12.3,
  "components": {
    "inference_engine": { "status": "ok", "artifacts_loaded": true },
    "alert_manager":    { "status": "ok" },
    "alert_buffer":     { "status": "ok", "size": 2 }
  }
}
```

Possible `status` values: `healthy` | `degraded` | `unhealthy`.

### GET /metrics

Prometheus text format. Example counters/histograms:

```
# HELP ingest_events_total Total events received by POST /ingest
ingest_events_total 1243.0
# HELP ingest_windows_total Total scoring windows emitted by InferenceEngine
ingest_windows_total 124.0
# HELP alerts_total Total alerts fired
alerts_total{severity="critical"} 2.0
alerts_total{severity="high"} 5.0
# HELP ingest_latency_seconds End-to-end /ingest handler latency in seconds
ingest_latency_seconds_bucket{le="0.01"} 1200.0
...
```

---

## 4. Security

**Mode: API Key (X-API-Key header)**

| Setting | Default | Env var |
|---|---|---|
| Key value | `""` (no enforcement) | `API_KEY` |
| Auth disabled | `false` | `DISABLE_AUTH=true` |
| Public paths | `/health`, `/metrics` | `PUBLIC_ENDPOINTS` |

Rules:
- Requests to `/health` and `/metrics` always pass (no key required).
- If `API_KEY` is empty, all requests pass with a logged warning.
- If `DISABLE_AUTH=true`, all requests pass unconditionally.
- Any other request without a valid `X-API-Key` receives `401 Unauthorized`.

---

## 5. Metrics Exposed (Prometheus)

| Metric | Type | Labels | Description |
|---|---|---|---|
| `ingest_events_total` | Counter | — | Events POSTed to `/ingest` |
| `ingest_windows_total` | Counter | — | Scoring windows emitted |
| `alerts_total` | Counter | `severity` | Alerts fired |
| `ingest_errors_total` | Counter | — | Unhandled errors in `/ingest` |
| `ingest_latency_seconds` | Histogram | — | `/ingest` end-to-end latency |
| `scoring_latency_seconds` | Histogram | — | Model scoring latency per window |

Each `MetricsRegistry` instance creates its own `CollectorRegistry`, preventing
duplicate-registration errors when running multiple instances in tests.

---

## 6. Health Checks Implemented

| Component | Critical | Check |
|---|---|---|
| `inference_engine` | Yes | `engine._artifacts_loaded == True` |
| `alert_manager` | No | manager object is not None |
| `alert_buffer` | No | `_alert_buffer` attribute present |

Status logic:
- `healthy`: all checks pass
- `degraded`: optional check fails, critical checks pass
- `unhealthy`: `inference_engine` not loaded

---

## 7. Project Structure

```
src/
  api/
    __init__.py        — exports create_app, Settings
    app.py             — create_app() factory with lifespan
    pipeline.py        — Pipeline container (engine + manager + buffer + metrics)
    routes.py          — Router: /ingest, /alerts, /health, /metrics
    schemas.py         — Pydantic v2 request/response models
    settings.py        — Env-driven Settings dataclass
  security/
    __init__.py
    auth.py            — AuthMiddleware (X-API-Key, public paths)
  observability/
    __init__.py
    metrics.py         — MetricsRegistry, MetricsMiddleware
    logging.py         — configure_logging()
  health/
    __init__.py
    checks.py          — HealthChecker

scripts/
  stage_07_run_api.py  — CLI entry-point (uvicorn)

tests/
  helpers_stage_07.py              — MockPipeline, MockInferenceEngine
  test_stage_07_auth.py            — 11 auth tests
  test_stage_07_ingest_integration.py — 15 endpoint tests
  test_stage_07_metrics.py         — 14 metrics tests
```

---

## 8. Integration Validation (ingest → alert)

End-to-end path verified by `test_ingest_anomaly_fires_alert` and
`test_alert_fired_increments_alerts_counter`:

```
POST /ingest (token_id=5, service=svc)
  → MockInferenceEngine.ingest() → RiskResult(is_anomaly=True, score=2.0)
  → AlertManager.emit()          → Alert(severity="critical")
  → N8nWebhookClient.send()      → DRY_RUN outbox
  → Pipeline._alert_buffer       → [{alert_id=..., severity=critical, ...}]
  → MetricsRegistry.alerts_total → incremented
  → GET /alerts                  → [{...}]
```

Severity ladder tested:
- score=3.0, threshold=1.0 → ratio 3.0 ≥ 1.5 → **critical** ✓
- score=2.0, threshold=1.0 → ratio 2.0 ≥ 1.5 → **critical** ✓
- score=0.4, threshold=1.0 → ratio 0.4 < 1.0 → no alert ✓

---

## 9. Run Commands

**Start the server:**

```powershell
python scripts/stage_07_run_api.py
# With options:
python scripts/stage_07_run_api.py --api-key changeme --port 8000 --model ensemble
python scripts/stage_07_run_api.py --disable-auth  # dev mode
```

**Smoke tests (after server is running):**

```powershell
# Health (no key)
curl http://localhost:8000/health

# Ingest event
curl -X POST http://localhost:8000/ingest `
     -H "X-API-Key: changeme" `
     -H "Content-Type: application/json" `
     -d '{"service":"hdfs","token_id":10,"timestamp":1704067200}'

# List alerts
curl http://localhost:8000/alerts -H "X-API-Key: changeme"

# Prometheus metrics
curl http://localhost:8000/metrics
```

**Run Stage 7 tests only:**

```powershell
python -m pytest tests/test_stage_07_auth.py tests/test_stage_07_ingest_integration.py tests/test_stage_07_metrics.py -v
```

---

## 10. Conclusion — Readiness for Stage 8

Stage 7 is **complete and production-ready** for the following reasons:

- All 40 Stage 7 tests pass; 199/199 full-suite tests pass.
- `/ingest` → `InferenceEngine` → `AlertManager` → ring buffer integration
  verified end-to-end with mock pipeline (avoids model-load overhead in CI).
- X-API-Key auth correctly enforces key for protected endpoints and skips
  `/health` and `/metrics`.
- Prometheus metrics are collected per-request with no global-registry
  conflicts (private `CollectorRegistry` per `MetricsRegistry` instance).
- Health check correctly reports `healthy` / `degraded` / `unhealthy`
  based on model-load status.
- All dependencies already present (`fastapi`, `uvicorn`, `prometheus-client`,
  `httpx`); added to `requirements.txt`.

**Stage 8** can build on this by adding: persistent alert storage (SQLite/
PostgreSQL), streaming ingest via WebSocket, batch-ingest endpoint, rate
limiting, or OpenTelemetry tracing.
