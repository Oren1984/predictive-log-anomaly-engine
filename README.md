# predictive-log-anomaly-engine

Proactive AI system that learns the “language of errors” from logs, builds sequences, and produces risk/anomaly alerts.

Structure aligned to: data → parsing/templates → sequences → baseline/transformer → runtime inference → alerts → API/observability.

---

## Demo UI (Stage 7.1)

A minimal single-page interface runs inside the FastAPI service — no React, no build step.

### Start the stack

```powershell
docker compose build
docker compose up
```

### Open the UI

```
http://localhost:8000/
```

### 3-step demo

| Step | Action | What to show |
|------|--------|--------------|
| **1 — Ingest** | Click **”Ingest 10 Events”** | 10 events are sent; the demo engine fires alerts immediately |
| **2 — Alerts** | Switch to the **Alerts** tab, click **”Refresh”** | Severity badges (critical / high / medium), scores, timestamps |
| **3 — RAG Ask** | Switch to the **RAG Ask** tab, type a question, click **”Ask”** | Natural-language answer + 3 ranked source documents |

#### Example questions for the RAG panel

- *”How does the alert threshold work?”*
- *”What model is used for anomaly detection?”*
- *”Tell me about the dataset”*
- *”How do I run with Docker?”*

### Other services

| Service | URL | Notes |
|---------|-----|-------|
| Prometheus | http://localhost:9090 | Raw metrics |
| Grafana | http://localhost:3000 | admin / admin - Stage 08 dashboard |

---

## Demo Mode Warmup (Stage 9.1)

When `DEMO_WARMUP_ENABLED=true` the API ingests a synthetic batch on startup so
the demo shows live data immediately — no manual clicks needed.

### How it works

1. App starts, models load (or fall back to demo scorer).
2. After ~2 seconds a background task ingests `DEMO_WARMUP_EVENTS` (default 75)
   synthetic log events through the normal `pipeline.process_event()` path.
3. With `DEMO_MODE=true` + `WINDOW_SIZE=5` the events quickly fill windows and
   trigger alerts — `GET /alerts` returns data before you even open the UI.
4. The task logs one summary line: `DEMO_WARMUP: ingested 75 events, alerts=15`.

### Env vars

| Variable | Default | Description |
|----------|---------|-------------|
| `DEMO_WARMUP_ENABLED` | `false` | Set `true` to activate warmup |
| `DEMO_WARMUP_EVENTS` | `75` | Number of synthetic events per warmup run |
| `DEMO_WARMUP_INTERVAL_SECONDS` | `0` | If `> 0`, repeat every N seconds; otherwise run once |

### Verify warmup after `docker compose up`

```bash
# Build and start the stack
docker compose down
docker compose up --build

# Wait ~5 seconds, then:
curl http://localhost:8000/health          # status: healthy
curl http://localhost:8000/alerts          # count > 0 (warmup fired alerts)
curl http://localhost:8000/metrics | grep ingest_events_total   # counter > 0
```

`DEMO_WARMUP_ENABLED` is `true` in `docker-compose.yml` but defaults to `false`
everywhere else, so tests and production are unaffected.

---

## Testing (Stage 7.2)

### Run the fast test suite (CI default)

```powershell
# All tests except slow model-dependent ones (~12 seconds)
python -m pytest -m "not slow"
```

### Run specific subsets

```powershell
# Unit tests only
python -m pytest tests/unit/

# Integration tests (API, FastAPI TestClient)
python -m pytest -m integration

# Pipeline smoke test (always-fast, synthetic events + full pipeline)
python -m pytest tests/test_pipeline_smoke.py -v

# Slow model-dependent tests (requires trained model files in models/)
python -m pytest -m slow
```

### Run the optional demo runner (no server needed)

```powershell
# 75 synthetic events, in-process TestClient, ~0.5 seconds
python scripts/demo_run.py

# Custom event count
python scripts/demo_run.py --events 200
```

### Test markers

| Marker | Meaning | When to run |
|--------|---------|-------------|
| *(none)* | Fast unit/smoke tests | Always |
| `integration` | FastAPI TestClient integration tests | Always in CI |
| `slow` | Model artifact-dependent tests | Locally after training |

### CI workflow

CI runs on every push and PR (`main`, `dev`) with three jobs:

| Job | What it does |
|-----|-------------|
| **Lint + Tests** | flake8 + `pytest -m "not slow"` |
| **Security** | pip-audit + Trivy |
| **Docker** | Build image + compose smoke (health, metrics, ingest, alerts, UI, query) |

---
