## Prompt — Alerting System

## Objective:
Document the alert generation and notification system.

## Components:
- Alert dataclass
- AlertPolicy
- AlertManager
- N8nWebhookClient

## Alert workflow:

1. Inference engine detects anomaly
2. AlertPolicy evaluates severity
3. AlertManager deduplicates alerts
4. Webhook sends event to n8n

## Optional integrations:

Slack
Email
GitHub Issues

## Expected Output:
Explain how anomalies become operational alerts.