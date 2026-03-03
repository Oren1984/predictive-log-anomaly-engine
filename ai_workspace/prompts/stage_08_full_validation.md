# Stage 08 — Closeout (Docker + CI/CD + Tests + Observability) — One Shot

You are working inside my repo. Your job is to CLOSE Stage 08 completely in one pass.

Stage 08 definition (MUST):
- Docker Compose stack: api + prometheus + grafana (db optional)
- Dockerfile builds successfully (no push)
- Observability:
  - API exposes /metrics (Prometheus format) and /health
  - Prometheus scrapes api:8000/metrics
  - Grafana auto-provisioned datasource (Prometheus) + dashboard imported on first boot
- CI (GitHub Actions):
  - lint + pytest
  - docker build
  - integration smoke: compose up -> wait -> GET /health 200 -> GET /metrics 200 -> compose down
  - security (recommended): pip-audit + trivy (may be non-blocking but must run and output results)
- Minimum tests:
  - Unit tests exist and run for:
    - generator/patterns
    - parser/template miner
    - sequence builder
    - scorer
  - Integration test:
    - ingest -> alert created (or deterministic path that proves pipeline can produce an alert)

STRICT RULES:
- Do NOT change business logic unless a bug prevents Stage 08 from passing.
- Do NOT refactor project structure.
- You MAY add/adjust ONLY Stage-08-related files: Dockerfile, docker-compose.yml, prometheus config, grafana provisioning, ci workflow, smoke script, tests if missing.
- Everything must work on Windows PowerShell.
- Prefer minimal changes; fix only what is required to pass.

TASKS (DO ALL):
1) Audit current repo for Stage 08 artifacts:
   - Dockerfile, docker-compose.yml
   - prometheus/prometheus.yml
   - grafana provisioning (datasource + dashboards)
   - dashboard JSON exists
   - .github/workflows/ci.yml
   - scripts/smoke_test.sh (or create it)
   - tests folder coverage for required unit + integration tests
2) Identify what is missing or broken vs the Stage 08 MUST list.
3) Implement ONLY what’s needed to make Stage 08 pass end-to-end.
4) Run local verification commands (provide exact PowerShell commands I should run) including:
   - docker compose down -v
   - docker compose build
   - docker compose up -d
   - docker compose ps
   - curl http://localhost:8000/health
   - curl http://localhost:8000/metrics
   - ingest sample event(s) and verify /alerts returns expected result
   - docker compose logs api/prometheus/grafana (only if needed)
   - docker compose down -v
5) Ensure CI workflow is correct:
   - triggers on push to main/dev and PRs
   - jobs: tests, security, docker (with smoke)
   - docker job must always teardown with `docker compose down -v` even on failure
6) Produce a Closeout report with evidence.

DELIVERABLES (MUST CREATE/UPDATE):
A) `reports/STAGE_08_CLOSEOUT.md` with:
   - timestamp
   - checklist with PASS/FAIL items
   - `docker compose ps` output
   - `/health` response body
   - `/metrics` status (HTTP 200) + first ~20 lines excerpt
   - Prometheus scrape status (how to verify targets page + expected "UP")
   - Grafana provisioning status (datasource + dashboard present)
   - CI summary: jobs + what they run
   - If any FAIL: root cause + exact fix + re-run instructions
B) Ensure `scripts/smoke_test.sh` exists and is idempotent:
   - down -v
   - up -d --build
   - retry /health up to 90s
   - verify /metrics 200
   - down -v
C) Ensure `.github/workflows/ci.yml` includes:
   - lint + pytest
   - pip-audit
   - trivy fs scan (non-blocking is OK, but must run)
   - docker build
   - docker compose smoke (up->health->metrics->down)

STOP CONDITION:
You are done ONLY when either:
- Stage 08 is PASS with evidence in `reports/STAGE_08_CLOSEOUT.md`
OR
- Stage 08 is FAIL, but you documented exact root cause + exact fix required + commands to validate.

Now start by scanning the repo and listing the exact missing/broken items relative to Stage 08.
Then implement fixes and produce the closeout report.