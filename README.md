# Predictive Log Anomaly Engine

**Tech Stack:**  
Python | FastAPI | Docker | Prometheus | Grafana | CI/CD

AI system that learns the “language of failures” in software logs and detects risky behavioral patterns before incidents happen.

Instead of reacting to failures after they occur, the engine analyzes event sequences in real time and produces early anomaly alerts.

This project demonstrates how an AI-powered observability pipeline can be built as a complete runtime system.

---

## Project Highlights

1. Log anomaly detection using sequence modeling

2. Runtime inference engine

3. Alert generation and severity scoring

4. FastAPI service with interactive UI

5. Observability with Prometheus + Grafana

6. Containerized deployment with Docker

7. CI/CD validation pipeline

---

## System Architecture

The system follows a full AI runtime pipeline:

Logs
 ↓
Parsing & Template Mining
 ↓
Sequence Builder
 ↓
ML Scoring Engine
 ↓
Alert Manager
 ↓
API Service
 ↓
Monitoring & Dashboards

## Main Components

1. Log Parser & Template Miner

2. Sequence Builder

3. Baseline AI Models

4. Runtime Inference Engine

5. Alert Manager

6. FastAPI API Service

7. Prometheus Metrics

8. Grafana Dashboard

---

## Demo UI

The project includes a minimal single-page interface built directly inside the FastAPI service.

No frontend framework is required.

---
## Start the System
docker compose build
docker compose up

---

## Open the UI
http://localhost:8000

---

## Demo Walkthrough
Step	Action	What happens
1. Ingest Events	Click Ingest 10 Events	Synthetic logs enter the pipeline
2. Alerts	Open Alerts tab	Alerts appear with severity + score
3. RAG Ask	Ask a question	System returns answer with sources

---

## Example Questions

1. How does the alert threshold work?

2. What model is used for anomaly detection?

3. What dataset is used for training?

4. How do I run the system with Docker?

---

## Monitoring

Two monitoring services are included.

   Service	           URL
1. Prometheus	http://localhost:9090

2. Grafana	   http://localhost:3000


## Grafana Dashboard Displays

1. Ingestion rate

2. Anomaly score distribution

3. Alert counts

4. System health metrics

---

## Quick Test Run
1. Run the fast test suite
pytest -m "not slow"

2. Run integration tests
pytest -m integration

---

## Tech Stack

Core technologies used:

1. Python

2. FastAPI

3. Machine Learning models

4. Prometheus

5. Grafana

6. Docker

7. Pytest

8. GitHub Actions

---

## Project Team

Developed as part of an AI Engineering project.


## Team Members

1. Oren Salami — DevOps / QA / System Integration

2. Dan Kalfon — Backend Developer


3. Nahshon Raizman — Full-Stack Developer

4. Jonathan Finkelstein — Full-Stack Developer

---

## Project Status

Documentation & Finalization

The system includes:

1. Runtime inference

2. Alert pipeline

3. Observability stack

4. Docker deployment

5. CI/CD validation

The repository represents a complete AI engineering prototype.

---

Built as part of an Applied AI Engineering project.