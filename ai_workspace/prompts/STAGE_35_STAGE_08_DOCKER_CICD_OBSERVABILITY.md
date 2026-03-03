You are working inside the repo "predictive-log-anomaly-engine".
Implement Stage 8 end-to-end: Docker + CI/CD + Tests + Observability stack with fully automatic Grafana provisioning.

HIGH-LEVEL GOAL
"Always runs" and can be validated automatically:
- Local: `docker compose up --build` brings up API + Prometheus + Grafana.
- Grafana auto-loads Prometheus as datasource AND auto-imports a ready dashboard.
- CI: runs pytest, security checks, docker build, and a smoke test that boots compose and calls GET /health.

CONSTRAINTS / RULES
- Do NOT break any existing functionality. All 199 tests must still pass.
- Keep Stage 7 API behavior exactly the same.
- Use minimal, clean additions. Prefer small, obvious files over complex logic.
- GitHub Actions must run on ubuntu-latest.
- No Docker Hub push.
- Do not add heavy new dependencies unless necessary.
- Use ports:
  - API: 8000
  - Prometheus: 9090
  - Grafana: 3000
- Auth:
  - /health and /metrics are public already.
  - For local demos, set DISABLE_AUTH=true in compose for the API service so ingest can be tested easily.
- Prometheus must scrape the API metrics endpoint.

DELIVERABLES (CREATE/UPDATE EXACTLY THESE)
1) Dockerfile (repo root)
- Production Dockerfile for the FastAPI API.
- Must bind to 0.0.0.0:8000
- Add HEALTHCHECK using curl to /health.

2) docker-compose.yml (repo root)
- Services:
  a) api (build from Dockerfile)
     - ports: "8000:8000"
     - env: DISABLE_AUTH=true
  b) prometheus
     - ports: "9090:9090"
     - mount ./prometheus/prometheus.yml
  c) grafana
     - ports: "3000:3000"
     - mount provisioning + dashboard files so Grafana auto-configures itself
     - set admin password via env (GF_SECURITY_ADMIN_PASSWORD=admin) for local demo
- Ensure dependencies/ordering works (grafana depends_on prometheus, etc.)

3) Prometheus config
- Create `prometheus/prometheus.yml`
- Configure scrape target to hit api:8000/metrics (docker network DNS name "api").

4) Grafana provisioning + dashboard auto-import
- Create:
  - `grafana/provisioning/datasources/datasource.yml` (Prometheus datasource pointing to http://prometheus:9090)
  - `grafana/provisioning/dashboards/dashboards.yml` (loads dashboards from mounted folder)
  - `grafana/dashboards/stage08_api_observability.json` (a simple dashboard)
Dashboard requirements:
- Panels for:
  - ingest_events_total (rate over 1m if possible)
  - ingest_windows_total (rate)
  - alerts_total by severity (stacked or separate)
  - ingest_latency_seconds p95 using histogram_quantile on ingest_latency_seconds_bucket
  - scoring_latency_seconds p95 using histogram_quantile on scoring_latency_seconds_bucket
- Use Prometheus queries that match our metric names from Stage 7.

5) CI workflow
- Create `.github/workflows/ci.yml` with jobs:
  A) tests:
     - checkout
     - setup-python (3.11)
     - pip install -r requirements.txt
     - run pytest (full suite)
  B) security (recommended):
     - pip-audit (python dependency audit)
     - trivy filesystem scan (repo)
  C) docker:
     - docker build (API image)
     - integration smoke test:
       1) docker compose up -d --build
       2) wait until http://localhost:8000/health returns status "healthy" (retry loop)
       3) curl http://localhost:8000/metrics and ensure it returns 200
       4) docker compose down -v
- Keep the smoke test reliable and fast.
- Use bash in CI for scripts.

6) Smoke test script (local + CI reuse)
- Create `scripts/smoke_test.sh`
- Should:
  - docker compose up -d --build
  - retry GET /health for up to ~60 seconds
  - curl /metrics
  - docker compose down -v
- Make it idempotent.

7) Documentation
- Create `docs/STAGE_35_STAGE_08_DOCKER_CICD_OBSERVABILITY.md` documenting:
  - What Stage 8 adds
  - Exact commands to run locally (PowerShell compatible)
  - URLs:
    - API: http://localhost:8000
    - /health, /metrics
    - Prometheus: http://localhost:9090 (Targets page)
    - Grafana: http://localhost:3000 (login admin/admin)
  - How to see the dashboard and which panels exist
  - CI summary: what gets run

OUTPUT REQUIREMENTS
After implementing:
- Print a concise file tree of all new/modified files.
- Print exact local run commands for Windows PowerShell:
  1) docker compose up --build -d
  2) curl http://localhost:8000/health
  3) open Grafana/Prometheus URLs
  4) docker compose down -v
- Do NOT create any extra documentation files beyond the one specified in docs/.
- Do NOT add docs/ subfolders beyond what is necessary.

Implement now.