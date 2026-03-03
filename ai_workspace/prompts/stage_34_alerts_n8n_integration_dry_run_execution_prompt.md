Read the repository and current Stage 0–5 implementation.

We are implementing STAGE 6 — Alerts + n8n Integration, BUT:
- Do NOT actually send to n8n by default.
- Implement a real webhook client, but default behavior is DRY-RUN that writes payloads to disk.

Requirements:
1) Create domain objects:
- Alert(dataclass): alert_id, severity, service, score, timestamp, evidence_window, model_name, threshold, meta
- AlertPolicy: threshold, cooldown_seconds, aggregation_window_seconds, min_events, severity_buckets
- AlertManager: deduplication + cooldown + emit(Alert)->list[Alert] (or emit single)

2) Integrate with Stage 5:
- InferenceEngine outputs RiskResult (already exists). Convert RiskResult -> Alert using AlertPolicy.
- Evidence must include top templates or a short list of events from evidence_window.

3) n8n integration (safe by default):
- N8nWebhookClient with config from environment:
  - N8N_WEBHOOK_URL (optional)
  - N8N_DRY_RUN=true by default
  - N8N_TIMEOUT_SECONDS default 5
- If DRY_RUN or URL missing: write payload JSON to artifacts/n8n_outbox/<alert_id>.json
- If URL exists and DRY_RUN=false: POST JSON to webhook URL (requests), handle errors gracefully.

4) Add example payloads and stub docs:
- examples/n8n/sample_alert_payload.json
- examples/n8n/n8n_flow_stub.md (Webhook → Slack/Email, optional GitHub Issue)

5) Provide a demo script:
- scripts/stage_06_demo_alerts.py
  - simulate stream ingestion using existing synthetic generator or demo runtime
  - generate alerts and write to outbox
  - print summary counts

6) Tests:
- tests/test_stage_06_alert_policy.py
- tests/test_stage_06_dedup_cooldown.py
- tests/test_stage_06_n8n_outbox.py (ensures DRY_RUN writes files)

7) Update .env.example with the new variables.

After implementation:
- Print exact PowerShell commands to run:
  1) pytest -q
  2) python scripts/stage_06_demo_alerts.py --n-events 2000
  3) dir artifacts\n8n_outbox
Do not add unrelated refactors.