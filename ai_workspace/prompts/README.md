# AI Workspace Prompts

This directory contains structured prompts used to document and validate
the architecture of the Predictive Log Anomaly Engine.

Instead of storing large static reports, the system uses **prompts**
to regenerate documentation and system analysis on demand.

Each prompt represents a **major architectural phase** of the system.

---

## Prompt Structure

The prompts follow the lifecycle of the system:

| Prompt | Phase | Description |
|------|------|------|
| 01_project_bootstrap | System foundation | Dataset strategy and schema definition |
| 02_data_pipeline | Data ingestion | Loading, normalization, synthetic generation |
| 03_template_mining | Log language modeling | Template extraction and tokenization |
| 04_sequence_dataset | Dataset preparation | Sequence building and dataset splits |
| 05_modeling_system | Machine learning models | Baseline + Transformer models |
| 06_runtime_engine | Real-time inference | Streaming log analysis and anomaly scoring |
| 07_alerting_system | Alert management | Alert policy, deduplication and n8n integration |
| 08_api_observability | Service layer | FastAPI endpoints, monitoring and metrics |
| 09_packaging_devops | Deployment | Docker, CI/CD and system packaging |
| 10_system_audit | System validation | Full architecture and runtime validation |

---

## Usage

These prompts can be provided to an AI assistant (Claude, Copilot, etc.)
to automatically generate documentation, reports, or system audits.

Example workflow:

1. Select a prompt file
2. Provide it to the AI assistant
3. Ask the assistant to generate a system report or documentation

Example instruction:


Read the prompt file and generate a technical system report
based on the current repository structure.


---

## Why This Exists

Instead of storing many static reports that quickly become outdated,
the project keeps **prompt-driven documentation** that can regenerate
accurate reports at any time.

This keeps the repository clean while preserving full system knowledge.

---

## Related Directories


ai_workspace/
prompts/ → prompt-driven documentation
reports/ → generated reports
stage_21–26 → pipeline execution stages


---

## Summary

This prompt system documents the **complete lifecycle of the AI anomaly
detection engine**, from data ingestion to deployment and system auditing.