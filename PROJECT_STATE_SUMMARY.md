📘 Predictive Log Anomaly Engine
Final Project State Summary – Stage 08 (Closed)
🎯 Project Mission

Build a proactive AI-based system that learns the “language of failures” in software systems.

The system analyzes real-time event sequences, detects toxic behavioral patterns, and raises alerts before critical failures impact end users.

This is not a static ML demo — this is a runtime-capable, observable, containerized system with CI/CD enforcement.

🧱 System Architecture Overview

The system is divided into logical layers:

Data Strategy & Contracts

Preprocessing & Template Mining

Sequence Modeling (Baseline AI Core)

Runtime Inference Engine

Alerts & Integrations

API Layer

Observability

Docker + CI/CD Automation

All planned macro components were implemented.

Transformer training was intentionally excluded by design (MVP stability focus).

✅ Stage-by-Stage Completion Summary
🟢 Stage 1 — Data Layer
Implemented:

LogEvent dataclass (contract definition)

Synthetic log generator

FailurePattern abstraction

ScenarioBuilder:

normal → degradation → failure flow

Structured schema normalization

Parquet artifact generation

Deliverables:
data/raw/
data/synth/
data/processed/events.parquet
schema.md

✔ Synthetic failure modeling implemented
✔ Structured event schema enforced

🟢 Stage 2 — Parsing & Template Mining
Implemented:

LogParser interface

TemplateMiner

EventTokenizer

Vocabulary artifact generation

Deliverables:
artifacts/templates.json
artifacts/vocab.json
processed/events_tokenized.parquet

✔ Stable template IDs
✔ Deterministic token encoding

🟢 Stage 3 — Sequence Builder
Implemented:

Sequence dataclass

SlidingWindowSequenceBuilder (window + stride)

DatasetSplitter

Deliverables:
processed/sequences_train.parquet
processed/sequences_val.parquet
processed/sequences_test.parquet

✔ Time-based splitting
✔ Sequence-based labeling

🟢 Stage 4 — Modeling (Baseline Production Core)

Transformer was intentionally excluded.

Implemented:

BaselineFeatureExtractor

BaselineAnomalyModel

ThresholdCalibrator

AnomalyScorer

Deliverables:
models/baseline.pkl
artifacts/threshold.json
reports/metrics.json

✔ Deterministic anomaly scoring
✔ Validation-based threshold calibration
✔ Stable risk signal

🟢 Stage 5 — Runtime Inference Engine
Implemented:

SequenceBuffer (rolling window per service)

InferenceEngine

RiskResult dataclass

Evidence window tracking

Runtime Flow:
ingest(event)
→ update buffer
→ score sequence
→ compare to threshold
→ return RiskResult

✔ Real-time scoring
✔ Evidence snapshot attached
✔ Stateless API + stateful buffer

🟢 Stage 6 — Alerts & n8n Integration
Implemented:

Alert dataclass

AlertPolicy (threshold + cooldown)

AlertManager (deduplication + emit)

N8nWebhookClient

Flow:
RiskResult → AlertPolicy → AlertManager → Webhook

✔ ingest → alert verified
✔ Deduplication logic active
✔ Cooldown supported

🟢 Stage 7 — API + Security + Observability
API (FastAPI)

Endpoints:

POST /ingest
GET  /alerts
GET  /health
GET  /metrics
Security:

Basic API protection layer

Structured request validation

Observability:

Prometheus metrics

Health checks

Grafana dashboard

Runtime counters

✔ Live metrics exposed
✔ Health endpoint validated
✔ Grafana export captured

🟢 Stage 8 — Docker + CI/CD + Tests (Fully Green)
Docker

docker-compose.yml

API container

Optional Prometheus + Grafana

Volume handling fixed (RW verified)

CI (GitHub Actions)

Pipeline includes:

flake8 lint

pytest

docker build

integration smoke test

pip-audit

trivy security scan

Smoke Test Flow:
compose up
→ wait for /health
→ POST /ingest (x10)
→ GET /alerts
→ verify alert count ≥ 1

✔ CI fully green
✔ ingest → alert verified in pipeline
✔ Docker build stable
✔ Security scan non-blocking

📊 System Capability Matrix
Capability	Status
Synthetic data modeling	✅
Template mining	✅
Tokenization	✅
Sequence modeling	✅
Baseline anomaly scoring	✅
Real-time inference	✅
Alert generation	✅
n8n integration	✅
FastAPI service	✅
Prometheus metrics	✅
Grafana dashboard	✅
Dockerized runtime	✅
CI/CD enforced	✅
Security scanning	✅
Transformer training	❌ (intentionally excluded)
🧠 Architectural Classification

This project is:

A runtime-capable anomaly detection engine

Sequence-aware

CI-enforced

Containerized

Observable

Alert-integrated

Production-structured

This is not a notebook project.

This is a system.

🏁 Final Status

Stage 08 is officially closed.

System is:

Stable

Test-covered

Observable

Dockerized

CI-verified

Transformer upgrade is optional future enhancement and not required for MVP completeness.

📌 Recommended Repository Tags

You may tag the repo as:

v1.0-stage08-mvp

or

v1.0-predictive-anomaly-engine
🔒 Official Declaration

All macro components defined in the original system-level execution plan were implemented.

Project is considered closed at MVP production-grade level.