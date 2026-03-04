# Stage 08 — Docker + CI/CD + Observability

## What Stage 8 Adds

| Component | Description |
|---|---|
| **Dockerfile** | Production container for the FastAPI service (Python 3.11-slim + curl HEALTHCHECK) |
| **docker-compose.yml** | Three-service stack: API (8000) + Prometheus (9090) + Grafana (3000) |
| **prometheus/prometheus.yml** | Scrape config targeting `api:8000/metrics` every 15 s |
| **Grafana provisioning** | Auto-wires Prometheus datasource and imports the dashboard on first boot |
| **grafana/dashboards/stage08_api_observability.json** | 5-panel dashboard (events rate, windows rate, alerts by severity, p95 latencies) |
| **.github/workflows/ci.yml** | Three-job CI pipeline: tests → security → docker smoke test |
| **scripts/smoke_test.sh** | Local idempotent smoke test (start → wait → verify → teardown) |

---

## Local Quick Start (PowerShell)

### Prerequisites
- Docker Desktop running
- From the repo root

### Start the stack

```powershell
docker compose up --build -d
```

The first build takes ~2 min (pulling Python + Grafana/Prometheus images and installing Python deps).
Subsequent builds use layer cache and are much faster.

### Verify the API

```powershell
# Health check (no auth key needed)
curl http://localhost:8000/health

# Prometheus metrics
curl http://localhost:8000/metrics

# Ingest an event (auth disabled in compose)
curl -X POST http://localhost:8000/ingest `
     -H "Content-Type: application/json" `
     -d '{"service":"hdfs","token_id":10,"timestamp":1704067200}'

# List recent alerts
curl http://localhost:8000/alerts
```

### Service URLs

| Service | URL | Notes |
|---|---|---|
| API | http://localhost:8000 | FastAPI (Swagger UI at /docs) |
| API health | http://localhost:8000/health | Liveness probe |
| API metrics | http://localhost:8000/metrics | Prometheus text format |
| Prometheus | http://localhost:9090 | Targets page: Status → Targets |
| Grafana | http://localhost:3000 | Login: `admin` / `admin` |

### Open the dashboard

1. Go to http://localhost:3000
2. Login: **admin** / **admin**
3. Click **Dashboards** (left sidebar) → **Stage 08 API Observability**

### Tear down

```powershell
docker compose down -v
```

---

## Dashboard Panels

The `Stage 08 API Observability` dashboard contains five panels:

| Panel | Query | Description |
|---|---|---|
| **Ingest Events Rate** | `rate(ingest_events_total[1m])` | Events POSTed to /ingest per second |
| **Scoring Windows Rate** | `rate(ingest_windows_total[1m])` | Windows emitted by InferenceEngine per second |
| **Alerts by Severity** | `rate(alerts_total{severity=...}[1m])` | Stacked bar chart: critical / high / medium / low |
| **Ingest Latency p95** | `histogram_quantile(0.95, rate(ingest_latency_seconds_bucket[5m]))` | 95th-percentile /ingest handler latency |
| **Scoring Latency p95** | `histogram_quantile(0.95, rate(scoring_latency_seconds_bucket[5m]))` | 95th-percentile model scoring latency |

---

## Local Smoke Test Script

```powershell
bash scripts/smoke_test.sh
```

The script:
1. Runs `docker compose down -v` to clear stale state
2. Starts the stack with `docker compose up -d --build`
3. Retries `GET /health` for up to 60 seconds
4. Verifies `/metrics` returns HTTP 200
5. Runs `docker compose down -v`

---

## CI Pipeline Summary (`.github/workflows/ci.yml`)

Three parallel-eligible jobs triggered on push to `main`/`dev` and on pull requests:

### A) `tests`
- Python 3.11, pip cache
- `pip install -r requirements.txt`
- `python -m pytest --tb=short -q`
- Model-dependent tests auto-skip (no models in git checkout)

### B) `security` (runs after tests)
- **pip-audit**: scans Python dependencies for known CVEs
- **Trivy**: filesystem scan for HIGH/CRITICAL vulnerabilities (informational, non-blocking)

### C) `docker` (runs after tests)
1. `docker build` — validates the Dockerfile
2. `docker compose up -d --build` — starts the full stack
3. Retry loop (90 s) — waits for `/health` HTTP 200
4. `curl /health` — verifies JSON response
5. `curl /metrics` — verifies Prometheus endpoint returns HTTP 200
6. `docker compose down -v` — always runs (even on failure)

---

## Architecture Diagram

```
┌──────────────────────────────────────────────┐
│  docker compose network                      │
│                                              │
│  ┌──────────────────────────┐                │
│  │  api  (port 8000)        │                │
│  │  FastAPI + InferenceEng  │                │
│  │  /ingest /alerts         │◄───── user     │
│  │  /health /metrics        │                │
│  └────────────┬─────────────┘                │
│               │ scrape :8000/metrics         │
│  ┌────────────▼─────────────┐                │
│  │  prometheus  (port 9090) │                │
│  └────────────┬─────────────┘                │
│               │ datasource                   │
│  ┌────────────▼─────────────┐                │
│  │  grafana  (port 3000)    │◄───── browser  │
│  │  auto-provisioned dash   │                │
│  └──────────────────────────┘                │
└──────────────────────────────────────────────┘
```
