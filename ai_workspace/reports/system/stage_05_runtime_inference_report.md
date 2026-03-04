# Stage 05 — Runtime Inference Report

**Date:** 2026-03-03
**Status:** Complete

---

## 1. What Was Implemented

### Core Runtime Package (`src/runtime/`)

| File | Class | Purpose |
|------|-------|---------|
| `types.py` | `RiskResult` | Dataclass holding one scored window's result |
| `sequence_buffer.py` | `SequenceBuffer` | Rolling per-stream token window with stride-based emission |
| `inference_engine.py` | `InferenceEngine` | Orchestrates buffer + model scoring + thresholding |
| `__init__.py` | — | Package exports |

#### SequenceBuffer
- `deque(maxlen=window_size)` gives automatic sliding behaviour
- Emission schedule: fires at event #`window_size`, then every `stride` events
- LRU eviction when `max_stream_keys` is reached (insertion-order dict)
- Works with both `LogEvent` objects and plain `dict` events
- Key format: `"{service}:{session_id}"` (service-only mode: `"{service}:"`)

#### InferenceEngine
- **Modes:** `baseline` | `transformer` | `ensemble`
- `load_artifacts()` loads vocab, thresholds, models; re-fits the baseline
  feature extractor on training sequences to ensure feature-column consistency
- `score_baseline()` — `BaselineFeatureExtractor` (204 features) + `BaselineAnomalyModel` (IsolationForest)
- `score_transformer()` — `AnomalyScorer` (per-token NLL from `NextTokenTransformerModel`)
- `ensemble` scoring: normalised average `(b_score/thr_b + t_score/thr_t) / 2`, threshold = 1.0
- `explain()` — decodes top-5 token IDs to template text via `artifacts/vocab.json`
- `_get_top_predictions()` — optional top-k next-token probabilities (transformer/ensemble)

#### RiskResult fields
| Field | Type | Description |
|-------|------|-------------|
| `stream_key` | str | `service:session_id` identity |
| `timestamp` | float | Last event timestamp in window |
| `model` | str | `baseline` / `transformer` / `ensemble` |
| `risk_score` | float | Anomaly score (higher = more anomalous) |
| `is_anomaly` | bool | `risk_score >= threshold` |
| `threshold` | float | Decision threshold used |
| `evidence_window` | dict | tokens, template_ids, templates_preview, start/end timestamps |
| `top_predictions` | list\|None | Top-k next-token probs (transformer/ensemble only) |
| `meta` | dict | window_size, label, emit_index |

---

### Scripts

| Script | Purpose |
|--------|---------|
| `scripts/stage_05_runtime_demo.py` | Stream events, emit RiskResults, save CSV + JSONL |
| `scripts/stage_05_runtime_benchmark.py` | Measure throughput, latency, memory |
| `scripts/stage_05_run.py` | One-command wrapper (demo + benchmark) |

All scripts accept `--key-by service|session` (default: `service`).
With `--key-by service` all events per service share one rolling window,
which is the correct streaming model for most deployments.
With `--key-by session` each session_id gets its own buffer (suitable for
long HDFS sessions or session-aware alerting in full-mode data).

---

### Tests (`tests/unit/`)

| File | Tests | Coverage |
|------|-------|---------|
| `test_sequence_buffer.py` | 22 | key derivation, emission timing, stride, labels, LogEvent compat, LRU eviction |
| `test_inference_engine_smoke.py` | 20 | None-before-full, RiskResult fields, scoring helpers, all 3 modes |
| `test_explain_decode.py` | 14 | vocab.json structure, templates.json, offset decode, engine.explain() |

**Total: 56 new tests + 44 existing = 100 tests, all passing.**

---

## 2. How to Run

### Install dependencies
```powershell
pip install -r requirements.txt
```

### Run all tests
```powershell
pytest -q
```

### One-command wrapper (demo + benchmark)
```powershell
python scripts/stage_05_run.py --mode demo --model ensemble
```

### Individual scripts
```powershell
python scripts/stage_05_runtime_demo.py --mode demo --model baseline
python scripts/stage_05_runtime_demo.py --mode demo --model transformer
python scripts/stage_05_runtime_demo.py --mode demo --model ensemble
python scripts/stage_05_runtime_benchmark.py --mode demo --model ensemble
```

### Stream key modes
```powershell
# Service-level stream (recommended for demo, default)
python scripts/stage_05_runtime_demo.py --mode demo --model ensemble --key-by service

# Session-level stream (use with full-mode data where sessions are long)
python scripts/stage_05_runtime_demo.py --mode demo --model ensemble --key-by session
```

---

## 3. Demo Results Summary

**Run:** `python scripts/stage_05_run.py --mode demo --model ensemble`
**Data:** `data/processed/events_tokenized.parquet` (first 20,000 events)
**Settings:** window_size=50, stride=10, key_by=service

| Metric | Value |
|--------|-------|
| Events processed | 20,000 |
| Windows emitted | 1,991 |
| Stream keys (services) | 2 (hdfs:, bgl:) |
| HDFS windows | 1,398 |
| BGL windows | 593 |
| Anomalies flagged | 1,991 (100%) |
| Elapsed | ~0.7 s (stream only) |
| Events/sec (stream only) | ~29,000 |

**Output files:**
- `reports/runtime_demo_results.csv` — 1,991 rows (one per emitted window)
- `reports/runtime_demo_evidence.jsonl` — full evidence including decoded templates

The 100% anomaly rate in demo mode is expected — see Known Limitations below.

---

## 4. Benchmark Summary

**Run:** `python scripts/stage_05_run.py --mode demo --model ensemble`
**Mode:** ensemble (baseline + transformer combined)

| Metric | Ensemble | Baseline only |
|--------|----------|---------------|
| Events/sec | 362 | 744 |
| Avg window latency | 27.0 ms | 13.1 ms |
| P95 window latency | 31.3 ms | — |
| Artifact load time | 0.18 s | 0.05 s |
| Peak RSS | 461 MB | 428 MB |
| Windows emitted | 1,991 | 1,991 |

**Notes:**
- The transformer roughly doubles latency vs baseline alone (~13ms → ~27ms per window)
- Memory overhead is modest (~33 MB extra for transformer over baseline)
- Artifact loading is fast (<0.2s) since models are small (baseline: 1.6 MB, transformer: 2.1 MB)
- The bottleneck in ensemble mode is the per-window transformer forward pass (CPU)

---

## 5. Known Limitations & Next Steps

### Limitations

**1. Demo-mode model calibration mismatch**
The demo pipeline (`run_0_4.py --mode demo`) trains on only 2,000 sessions,
producing sequences of 2–3 tokens. The runtime window of 50 tokens has a very
different `sequence_length` feature distribution, causing the IsolationForest
to flag all windows as anomalous. **Fix:** Run `python scripts/run_0_4.py --mode full`
to train on the full 495,405 sessions before running Stage 5 in full mode.

**2. Ensemble threshold not tuned**
The ensemble score is `(b_norm + t_norm) / 2` with threshold=1.0. In demo mode,
the transformer NLL (~4.5) is ~130x the transformer threshold (0.034), dominating
the ensemble and causing all windows to be flagged.
**Fix:** Calibrate ensemble on a validation set after full-mode training.

**3. Feature extractor not persisted**
`BaselineFeatureExtractor` is re-fitted on `sequences_train.parquet` at every
engine start. In full mode this takes negligible extra time (<0.5s for 1600
sequences). Saving the fitted extractor as an artifact would eliminate this.

**4. Session-level streaming limitation (HDFS)**
HDFS sessions have only 2–3 events per block. With `--key-by session` no windows
are emitted for most sessions. Use `--key-by service` for continuous sliding-window
streaming, or increase the HDFS log stream to large service-level aggregations.

**5. Transformer throughput**
At ~362 events/sec on CPU, the ensemble mode would process 1.3M events/hour.
For higher throughput, use `--model baseline` (~744 events/sec) or run the
transformer on GPU.

### Next Steps

**Stage 6 — Alerts / n8n Integration:**
- Add `AlertRule` class that evaluates RiskResult thresholds
- HTTP webhook callback for n8n workflows when anomalies are detected
- Configurable alert suppression (cooldown, min_score thresholds)

**Stage 7 — REST API:**
- FastAPI wrapper around InferenceEngine
- `POST /ingest` accepts a batch of events, returns list of RiskResults
- `GET /stats` returns buffer state, anomaly counts, throughput metrics
- SSE or WebSocket endpoint for real-time anomaly stream

**Model improvements:**
- Train on full 495K sessions for accurate anomaly detection
- Calibrate ensemble weights on held-out validation data
- Add bigram features to the runtime extractor (matching session_features_v2.csv)

---

## Appendix: File Manifest

```
src/runtime/
  __init__.py                      # exports InferenceEngine, SequenceBuffer, RiskResult
  types.py                         # RiskResult dataclass
  sequence_buffer.py               # SequenceBuffer
  inference_engine.py              # InferenceEngine

scripts/
  stage_05_runtime_demo.py         # stream demo
  stage_05_runtime_benchmark.py    # throughput / latency / memory benchmark
  stage_05_run.py                  # one-command wrapper

tests/unit/
  test_sequence_buffer.py          # 22 tests
  test_inference_engine_smoke.py   # 20 tests
  test_explain_decode.py           # 14 tests

reports/
  stage_05_runtime_inference_report.md   (this file)
  stage_05_runtime_benchmark.md          (generated by benchmark script)
  runtime_demo_results.csv               (1,991 rows)
  runtime_demo_evidence.jsonl            (1,991 JSON lines)

ai_workspace/logs/
  stage_05_runtime_demo.log
  stage_05_runtime_benchmark.log
```
