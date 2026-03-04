# Predictive Log Anomaly Engine
## UI and Automation Validation Report

**Stage:** 7.1 (Demo UI) + 7.2 (Quality Gate)
**Date:** 2026-03-04
**Status:** PASS — Demo-ready

---

## 1. UI Overview

### Purpose

The Demo UI is a single-page HTML interface embedded inside the existing FastAPI
service. It provides a lightweight, presentation-ready interface for demonstrating
the three core system capabilities: log event ingestion, real-time alert
monitoring, and natural-language retrieval (RAG Ask). No React, no build tools,
no external dependencies beyond the already-installed FastAPI stack.

### Panels

| # | Panel | Purpose |
|---|-------|---------|
| 1 | **Ingest** | Send synthetic or custom log events to the anomaly detection pipeline |
| 2 | **Alerts** | View the in-memory alert ring buffer with severity, score, and timestamp |
| 3 | **RAG Ask** | Ask natural-language questions about the system; returns answer + ranked sources |

### User Workflow

```
Browser opens http://localhost:8000/
          |
          +--[Tab 1: Ingest]----> POST /ingest (1 or 10 events)
          |                            |
          |                            +---> InferenceEngine scores window
          |                            +---> AlertManager emits alert if anomaly
          |                            +---> Response: window_emitted / alert
          |
          +--[Tab 2: Alerts]----> GET /alerts
          |                            |
          |                            +---> Ring buffer (last 200 alerts)
          |                            +---> Table: timestamp | severity | service | score | evidence
          |
          +--[Tab 3: RAG Ask]--> POST /query
                                       |
                                       +---> Keyword match on built-in KB (8 docs)
                                       +---> Response: answer (str) + sources (top-3)
```

---

## 2. UI Technical Implementation

### Files

| File | Role | Size |
|------|------|------|
| `templates/index.html` | Single-page UI (HTML + inline CSS + vanilla JS) | 498 lines |
| `src/api/ui.py` | FastAPI router: `GET /` + `POST /query` | 248 lines |
| `src/api/routes.py` | Core API: `/ingest`, `/alerts`, `/health`, `/metrics` | 174 lines |
| `src/api/app.py` | Application factory; mounts both routers + middleware | 123 lines |

### API Endpoints (all endpoints used by the UI)

| Method | Path | Served by | Description |
|--------|------|-----------|-------------|
| `GET`  | `/` | `ui_router` (ui.py) | Serves `templates/index.html` as HTMLResponse |
| `POST` | `/ingest` | `router` (routes.py) | Ingest a tokenised log event; returns window + alert |
| `GET`  | `/alerts` | `router` (routes.py) | Returns last N alerts from the ring buffer |
| `POST` | `/query` | `ui_router` (ui.py) | RAG stub: keyword search + top-3 KB sources |

Auth: All four paths are in the default `PUBLIC_ENDPOINTS` (`/health,/metrics,/,/query`).
`DISABLE_AUTH=true` is set in `docker-compose.yml` so no API key is required in demo mode.

### Panel-to-Endpoint Mapping

```
Panel 1 (Ingest)
  Button: "Run Demo Ingest"   -> POST /ingest  (single event from textarea)
  Button: "Ingest 10 Events"  -> POST /ingest  (loop: 10 events, different services/tokens)
  Response display: JSON with window_emitted, risk_result, alert

Panel 2 (Alerts)
  Button: "Refresh"           -> GET /alerts
  Table columns: Timestamp (UTC) | Severity | Service | Score | Evidence (truncated 70 chars)
  Severity badges: critical (red) | high (orange) | medium (yellow) | low (green)

Panel 3 (RAG Ask)
  Input + "Ask" button        -> POST /query  {"question": "<user input>"}
  Quick-help links: alerts | model | ingest | dataset | threshold | docker
  Response display: Answer paragraph + source list (id, relevance score, snippet)
```

### Data Flow

```
[Browser JS fetch()]
        |
        v
[FastAPI AuthMiddleware]  -- public path bypass for / and /query
        |
        v
[FastAPI MetricsMiddleware] -- increments request counters
        |
        v
[Route handler]
        |
  /ingest --> Pipeline.process_event()
                  SequenceBuffer.ingest()  -> window when full
                  InferenceEngine.score()  -> RiskResult
                  AlertManager.emit()      -> Alert (if anomaly)
                  Returns IngestResponse (window_emitted, risk_result, alert)
        |
  /alerts --> Pipeline.recent_alerts()
                  Returns deque of last ALERT_BUFFER_SIZE alerts
        |
  /query  --> _best_answer(question)       -> answer string (keyword lookup)
              _top_sources(question, k=3)  -> ranked KB documents
                  Returns QueryResponse (answer, sources)
```

### Key UX Features

- **Loading indicator**: status span updates to "Sending..." / "Searching..." during requests
- **Error messages**: network errors and HTTP non-200 responses shown with red status
- **JSON validation**: `JSON.parse()` on ingest payload before sending; shows "Invalid JSON" on failure
- **Evidence truncation**: alert evidence truncated at 70 characters in table; full value in tooltip
- **Quick-help links**: six pre-filled RAG questions for live demos (click to populate input)
- **Batch ingest**: "Ingest 10 Events" button sends 10 events across hdfs/bgl services automatically

---

## 3. Automation and Testing

### Test Structure

```
tests/
  test_pipeline_smoke.py          <- Always-fast smoke (18 tests, ~3.4s)
  test_stage_06_alert_policy.py   <- Unit: AlertPolicy (15 tests)
  test_stage_06_dedup_cooldown.py <- Unit: AlertManager dedup/cooldown (12 tests)
  test_stage_06_n8n_outbox.py     <- Unit: N8n outbox dry-run (13 tests)
  test_stage_07_auth.py           <- Integration: AuthMiddleware (11 tests)
  test_stage_07_ingest_integration.py <- Integration: /ingest + /alerts (8 tests)
  test_stage_07_metrics.py        <- Integration: MetricsRegistry + /metrics (14 tests)
  helpers_stage_07.py             <- Shared MockPipeline + stub helpers
  integration/
    test_smoke_api.py             <- Integration: full pipeline smoke (16 tests)
  unit/
    test_calibrator.py            <- Unit: ThresholdCalibrator (10 tests)
    test_explain_decode.py        <- Unit: token decode/explain
    test_inference_engine_smoke.py <- Smoke: InferenceEngine (*slow*, needs artifacts)
    test_placeholder.py           <- Placeholder tests
    test_runtime_calibration.py   <- Integration: calibration script (*slow*, needs artifacts)
    test_sequence_buffer.py       <- Unit: SequenceBuffer (18 tests)
    test_sequences.py             <- Unit: sequence builders + splitter (14 tests)
    test_synth_generation.py      <- Unit: SyntheticLogGenerator (7 tests)
    test_tokenizer.py             <- Unit: TemplateTokenizer (14 tests)
```

### Test Counts and Markers

| Category | Count | How to run |
|----------|-------|------------|
| Total collected | 233 | `pytest` |
| **Fast suite (CI default)** | **211** | `pytest -m "not slow"` |
| Integration tests | 56 | `pytest -m integration` |
| Slow (model-dependent) | 22 | `pytest -m slow` |
| Pipeline smoke (new Stage 7.2) | 18 | `pytest tests/test_pipeline_smoke.py` |
| Deselected in fast run | 22 | auto-skipped in CI |

Marker definitions (`pyproject.toml`):

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts   = "--tb=short"
markers   = [
    "slow: model/data-file-dependent tests; skip in fast dev loops with '-m not slow'",
    "integration: API integration tests that use the FastAPI TestClient",
]
```

### Smoke Tests

**`tests/test_pipeline_smoke.py`** — always runs, no model files required:

| Class | Tests | Validates |
|-------|-------|-----------|
| `TestSyntheticGeneration` | 4 | Event generation schema, count, token IDs |
| `TestIngestPipeline` | 5 | `/ingest` 200s, schema, anomaly alert, 50-event batch, buffer persistence |
| `TestAlertsEndpoint` | 2 | `/alerts` 200, response schema |
| `TestQueryEndpoint` | 4 | `/query` 200, answer string, sources list, source fields |
| `TestDemoUI` | 3 | `GET /` 200, content-type html, all 3 panel IDs present |

### Integration Tests

`tests/integration/test_smoke_api.py` (marked `integration`):
- Full `ingest -> RiskResult -> Alert` pipeline via MockPipeline
- Alert severity mapping (ratio-based bucketing)
- Alert ring buffer persistence
- Prometheus metric counter increments
- UI page reachability and panel structure
- `/query` response schema validation

### Runtime Validation Script

`scripts/demo_run.py` — standalone in-process demo runner:

```
python scripts/demo_run.py             # 75 events, ~0.5s
python scripts/demo_run.py --events 200
```

Exercises the complete flow without a running server:
1. Generates synthetic events (MemoryLeakPattern, NetworkFlapPattern, AuthBruteForcePattern)
2. Posts to `/ingest` via FastAPI TestClient; measures throughput and alert rate
3. Fetches `/alerts`; renders a formatted table
4. Posts 3 questions to `/query`; wraps and prints answers with sources

### CI Pipeline

**`.github/workflows/ci.yml`** — three jobs:

```
Job A: Lint + Tests (Python 3.11, ubuntu-latest)
  - pip install requirements.txt + requirements-dev.txt
  - flake8 src/ scripts/ --exit-zero
  - pytest -q -m "not slow"                  <- 211 tests

Job B: Security Scan (needs: tests)
  - pip-audit -r requirements.txt
  - Trivy filesystem scan (HIGH,CRITICAL)

Job C: Docker Build + Smoke Test (needs: tests)
  - mkdir -p models artifacts
  - docker build -t anomaly-api:ci
  - docker compose up -d --build
  - Wait up to 90s for GET /health -> 200
  - GET /health          -> HTTP 200
  - GET /metrics         -> HTTP 200
  - POST 10 x /ingest    -> HTTP 200 each
  - GET /alerts          -> count >= 1
  - GET /             <- Stage 7.1 UI smoke
  - POST /query          <- Stage 7.1 RAG smoke
  - docker compose down -v
```

Triggers: `push` to main/dev + `pull_request` to main.

---

## 4. Integration with System Pipeline

### Full Pipeline Architecture

```
[Raw Logs]
    |
    v
Stage 01-03: Data + Template Mining + Sequences
    15.9M events (HDFS + BGL)
    7,833 unique log templates
    495,405 log sessions
    |
    v
Stage 04: Baseline Model Training
    IsolationForest (n_estimators=200)
    Trained on session-level feature vectors (407 features)
    BGL F1=0.96, HDFS F1=0.047
    |
    v
Stage 05: Runtime Inference Engine
    SequenceBuffer: sliding window per stream key (default: 50 events, stride 10)
    InferenceEngine: baseline / transformer / ensemble modes
    Produces RiskResult (stream_key, model, risk_score, is_anomaly, threshold, evidence)
    |
    v
Stage 06: Alert Management
    AlertManager: per-stream-key cooldown + severity bucketing
    N8nWebhookClient: dry-run outbox or live POST
    Produces Alert (UUID, severity, service, score, timestamp, evidence_window)
    |
    v
Stage 07: REST API
    POST /ingest  <--- (UI Panel 1)
    GET  /alerts  <--- (UI Panel 2)
    GET  /health
    GET  /metrics
    GET  /        <--- (Demo UI page)
    POST /query   <--- (UI Panel 3)
    |
    v
Stage 08: Docker + CI/CD + Observability
    Prometheus scrapes /metrics every 15s
    Grafana dashboards: event rate, window rate, alert severity, latency p95
```

### How the UI Interacts with Detection and RAG

**Anomaly Detection path (Panels 1 + 2):**

```
User clicks "Ingest 10 Events"
    -> JS sends 10 POST /ingest requests
    -> Each event enters SequenceBuffer for its service
    -> When buffer fills (WINDOW_SIZE events), InferenceEngine scores it
    -> In DEMO_MODE: fallback scorer returns DEMO_SCORE (100.0 >> threshold)
       guaranteeing an alert on every window
    -> AlertManager creates Alert with severity=critical
    -> Alert stored in deque ring buffer
User clicks "Refresh" on Alerts tab
    -> JS sends GET /alerts
    -> API returns all buffered alerts sorted by insertion order
    -> JS renders table with severity color-coding
```

**RAG (Panel 3):**

```
User types question, clicks "Ask"
    -> JS sends POST /query {"question": "..."}
    -> _best_answer(): case-insensitive keyword scan against 12 answer templates
    -> _top_sources(): word-overlap ranking of 8 KB documents
    -> Returns {"answer": "...", "sources": [{id, score, snippet}, ...]}
    -> JS renders answer paragraph + 3 source cards
```

**Note on RAG:** The current `/query` implementation is a built-in keyword-matching
stub. It does not call an embedding model or vector database. The 8 KB documents
and 12 answer templates cover the core system concepts (alerts, model, ingest,
window, dataset, score, threshold, API, templates, Docker, Grafana, Prometheus).
This is intentional for the demo — the RAG Ask panel demonstrates the interface
pattern without requiring a live retrieval backend.

---

## 5. System Readiness Assessment

### UI Readiness

| Aspect | Status | Notes |
|--------|--------|-------|
| Panel 1 — Ingest | **READY** | Default payload, manual JSON, single + batch ingest |
| Panel 2 — Alerts | **READY** | Table with severity badges, timestamp (UTC), truncated evidence |
| Panel 3 — RAG Ask | **READY** | Answer display, 3 ranked sources, 6 quick-help links |
| Loading indicators | **READY** | Status spans update to Sending/Searching/Done/Error |
| Error handling | **READY** | JSON parse errors, HTTP non-200, network errors |
| Demo mode (Docker) | **READY** | DEMO_MODE=true, DEMO_SCORE=100.0, alerts fire on every window |
| Auth | **READY** | DISABLE_AUTH=true in docker-compose.yml; `/` and `/query` in public endpoints |
| Cross-platform | **READY** | Works on Windows + Docker; relative fetch() paths |

### Automation Readiness

| Component | Status | Notes |
|-----------|--------|-------|
| Unit tests | **READY** | 133 fast unit tests; no external deps |
| Integration tests (56) | **READY** | TestClient-based; MockPipeline; no model files |
| Pipeline smoke (18) | **READY** | Synthetic events; validates full ingest→alert→query path |
| Slow tests (22) | **CONDITIONAL** | Need trained model files in `models/`; auto-skip in CI |
| CI workflow | **READY** | 3 jobs; pytest -m "not slow"; Docker smoke (all 6 endpoints) |
| Demo runner | **READY** | ~0.5s; no server; no model files; formatted console output |

**Overall assessment:** The system is demo-ready. All three UI panels are wired to
real or stub API endpoints, all pass automated tests, and the CI pipeline validates
the full Docker stack end-to-end on every push.

---

## 6. Verification Instructions

### Start the Stack

```powershell
# Build and start all services
docker compose build
docker compose up
```

Services started:

| Service | URL | Credentials |
|---------|-----|-------------|
| API + Demo UI | http://localhost:8000/ | none (DISABLE_AUTH=true) |
| Prometheus | http://localhost:9090 | none |
| Grafana | http://localhost:3000 | admin / admin |

### Manual Demo Steps

**Step 1 — Open the UI**

```
http://localhost:8000/
```

Expected: Dark-themed single-page interface with three tabs (1 — Ingest, 2 — Alerts, 3 — RAG Ask).

---

**Step 2 — Run Demo Ingest**

1. On the Ingest tab, click **"Ingest 10 Events"**.
2. Watch the status update: `"10 events sent — N alert(s) fired"`.
3. The JSON result panel shows the last ingest response.

What to say: *"The engine is receiving tokenised log events. With DEMO_MODE enabled,
every scoring window fires a critical alert — no trained models needed."*

---

**Step 3 — Refresh Alerts**

1. Click the **"2 — Alerts"** tab.
2. Click **"Refresh"**.
3. Table appears with rows like:

| Timestamp (UTC) | Severity | Service | Score | Evidence |
|-----------------|----------|---------|-------|----------|
| 2024-01-01 ... | CRITICAL | hdfs | 3.000 | {"tokens":... |

What to say: *"The alert ring buffer holds the 200 most recent detections.
Severity is automatically bucketed: critical when score/threshold >= 1.5x,
high at 1.2x, medium at 1.0x."*

---

**Step 4 — Ask a RAG Question**

1. Click the **"3 — RAG Ask"** tab.
2. Type: `How does the alert threshold work?`  (or click a quick-help link)
3. Click **"Ask"**.
4. Answer appears along with 3 ranked source documents.

What to say: *"The RAG panel lets you query the system's knowledge base in natural language.
It returns a direct answer plus the top-3 source documents with relevance scores."*

---

### Verify with Automated Tests

```powershell
# Full fast suite (211 tests, ~12 seconds)
python -m pytest -m "not slow"

# Pipeline smoke only (18 tests, ~3.4 seconds)
python -m pytest tests/test_pipeline_smoke.py -v

# In-process demo runner (no server, ~0.5 seconds)
python scripts/demo_run.py

# Integration tests only
python -m pytest -m integration

# Slow model-dependent tests (requires models/ artifacts)
python -m pytest -m slow
```

---

## Appendix A — File Inventory

| File | Purpose | Stage |
|------|---------|-------|
| `templates/index.html` | Single-page demo UI | 7.1 |
| `src/api/ui.py` | UI router + RAG stub endpoint | 7.1 |
| `src/api/routes.py` | Core API endpoints | 7 |
| `src/api/app.py` | FastAPI application factory | 7 |
| `src/api/pipeline.py` | Pipeline container (InferenceEngine + AlertManager) | 7 |
| `src/api/schemas.py` | Pydantic v2 request/response models | 7 |
| `src/api/settings.py` | Env-driven config (DISABLE_AUTH, DEMO_MODE, etc.) | 7 |
| `src/security/auth.py` | X-API-Key auth middleware | 7 |
| `src/observability/metrics.py` | Prometheus MetricsRegistry + middleware | 7 |
| `src/health/checks.py` | HealthChecker (healthy/degraded/unhealthy) | 7 |
| `tests/test_pipeline_smoke.py` | Always-fast pipeline smoke (18 tests) | 7.2 |
| `tests/integration/test_smoke_api.py` | API integration smoke (16 tests) | 8 |
| `tests/test_stage_07_*.py` | Auth + ingest + metrics integration (33 tests) | 7 |
| `scripts/demo_run.py` | Standalone in-process demo runner | 7.2 |
| `pyproject.toml` | pytest config + markers (slow, integration) | 7.2 |
| `.github/workflows/ci.yml` | 3-job CI pipeline | 8 |
| `docker-compose.yml` | api + prometheus + grafana; demo env | 8 |
| `Dockerfile` | python:3.11-slim; uvicorn factory entrypoint | 8 |

## Appendix B — Environment Variables (Demo Mode)

| Variable | Demo Value | Description |
|----------|-----------|-------------|
| `DISABLE_AUTH` | `true` | Skip API key auth for all endpoints |
| `DEMO_MODE` | `true` | Use fallback scorer (no model needed) |
| `DEMO_SCORE` | `100.0` | Fallback score (>> threshold -> always alert) |
| `MODEL_MODE` | `baseline` | Use IsolationForest path |
| `WINDOW_SIZE` | `5` | 5-event windows (faster demo feedback) |
| `STRIDE` | `1` | Score on every new event |
| `ALERT_COOLDOWN_SECONDS` | `0` | No cooldown (every window fires) |
| `ALERT_BUFFER_SIZE` | `200` | (default) Ring buffer for GET /alerts |
| `PUBLIC_ENDPOINTS` | `/health,/metrics,/,/query` | Paths that bypass auth |
