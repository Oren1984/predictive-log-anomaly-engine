# Stage 08 Closeout — Fix ingest→alert (feature mismatch) and produce final PASS report

Context:
Stage 08 stack is up: /health 200, /metrics 200, Prometheus target UP.
However Integration requirement "ingest → alert created" fails due to runtime error:

"X has 4 features, but IsolationForest is expecting 204 features as input."

Goal:
Close Stage 08 with ONE deterministic path that produces at least 1 alert in local Docker + CI smoke, without adding new stages.

Rules:
- Minimal changes only.
- Do NOT refactor project structure.
- Do NOT change business logic except to make Stage 08 stable.
- Prefer "demo-safe" behavior: ingest should NOT crash due to model/artifact mismatch.
- Windows PowerShell commands must work.

Tasks:
1) Locate where IsolationForest scoring happens and where features vector is built.
2) Implement safe fallback behavior:
   - If model artifact expects n_features != len(X), or scoring raises the mismatch exception,
     then DO NOT fail the request.
   - Log a warning and use a fallback scorer (rule-based / percentile / safe default).
   - Ensure metrics reflect an error counter increment (if already exists).
3) Make alert creation deterministic for demo/Stage08:
   - In "compose/demo mode" ensure after N ingests (e.g., 20–60) at least 1 alert is emitted.
   - Prefer using existing AlertPolicy thresholds; if needed, add a specific DEMO env var to lower thresholds
     ONLY for compose (not for production default).
4) Update/ensure integration test:
   - A test that posts events and asserts alerts count >= 1 (or directly asserts alerts_total increments).
   - Must pass in CI.
5) Update scripts/smoke_test.sh (if needed):
   - After health/metrics, POST events (PowerShell-friendly alternative or curl.exe in CI)
   - Then verify /alerts count >= 1 OR alerts_total > 0.
6) Produce final report:
   - Create/overwrite: reports/STAGE_08_CLOSEOUT.md
   - Include the root cause, the chosen fix (fallback behavior), exact commands to validate locally,
     and evidence criteria.

Local validation commands to target:
- docker compose down -v
- docker compose up -d --build
- curl http://localhost:8000/health
- curl http://localhost:8000/metrics
- POST 60 events to /ingest (curl.exe or Invoke-RestMethod)
- curl http://localhost:8000/alerts should show count >= 1
- docker compose down -v

Stop only when Stage 08 is PASS with reproducible ingest→alert.