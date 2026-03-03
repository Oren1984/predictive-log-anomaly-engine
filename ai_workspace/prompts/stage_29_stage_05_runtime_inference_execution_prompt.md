You are working inside this existing repo:
C:\Users\ORENS\predictive-log-anomaly-engine

Goal (Stage 5 — Runtime Inference):
Implement Stage 5 COMPLETELY (runtime ingestion + rolling buffer + inference + evidence)
using the artifacts/models already produced in stages 0–4.

Do NOT download any new dataset.
Do NOT build API (Stage 7) yet.
Do NOT implement Alerts/n8n (Stage 6) yet.
Focus only on a production-quality Stage 5 runtime module + demo runner + tests + report.

-----------------------------------------
INPUTS (must be used)
-----------------------------------------
- data/processed/events_tokenized.parquet
- data/intermediate/session_sequences_v2.csv
- models/baseline.pkl
- models/transformer.pt
- artifacts/threshold.json
- artifacts/threshold_transformer.json
- artifacts/vocab.json
- artifacts/templates.json
- Stage 1–4 code already exists under src/ and scripts/

-----------------------------------------
REQUIRED STAGE 5 CLASSES (names matter)
-----------------------------------------

1) SequenceBuffer (rolling window)
- Purpose: maintain rolling token windows per key (service/host/session)
- Requirements:
  - init(window_size:int, stride:int=1, max_stream_keys:int=5000)
  - ingest(event: LogEvent or dict-like with {timestamp, service, session_id, token_id, label?})
  - get_window(stream_key) -> Sequence (tokens + timestamps + label? + sequence_id)
  - should_emit(stream_key) -> bool  (true when window full + stride step reached)
  - reset(stream_key) / clear()

2) RiskResult dataclass
Fields:
- stream_key: str
- timestamp: float|str
- model: str ("baseline" | "transformer" | "ensemble")
- risk_score: float (0..1 or unbounded but consistent)
- is_anomaly: bool
- threshold: float
- evidence_window: dict with:
  - tokens (last N token_ids)
  - template_ids (if available)
  - templates_preview (top 5 decoded templates)
  - window_start_ts, window_end_ts
- top_predictions (optional for transformer: topk next-token probs)
- meta: dict (any extra details)

3) InferenceEngine
- Purpose: orchestrate buffer + model scoring + thresholding
- Requirements:
  - init(mode="baseline"|"transformer"|"ensemble", window_size=50, stride=10)
  - load_artifacts() loads vocab/templates/thresholds/models using relative paths
  - ingest(event) -> Optional[RiskResult]
    - Adds event to SequenceBuffer
    - If should_emit() then scores the window and returns RiskResult
    - Else returns None
  - score_baseline(sequence) -> float
    - MUST use BaselineFeatureExtractor and BaselineAnomalyModel in a consistent way
    - If baseline model expects session_features: implement fallback extractor from tokens (counts) for runtime
  - score_transformer(sequence) -> float
    - Use AnomalyScorer (NLL per token) from Stage 4B
  - decide(score, threshold) -> bool
  - explain(sequence) -> evidence dict including decoded template snippets

IMPORTANT:
- Provide 3 inference modes:
  A) baseline only
  B) transformer only
  C) ensemble (simple: normalize both scores + average, then threshold on val-based default)

-----------------------------------------
STAGE 5 SCRIPTS
-----------------------------------------

Create scripts:

1) scripts/stage_05_runtime_demo.py
- Simulate a stream by reading:
  - data/processed/events_tokenized.parquet (preferred)
- Feed events ordered by timestamp for a single service or mixed.
- Use window_size=50 stride=10 (defaults).
- Print a concise console output line for each emitted RiskResult:
  ts | key | model | score | thresh | is_anom | top_template_preview
- Save emitted results to:
  reports/runtime_demo_results.csv
- Also write a small JSONL file for evidence:
  reports/runtime_demo_evidence.jsonl

2) scripts/stage_05_runtime_benchmark.py
- Run through N events (default 200k or demo mode 20k)
- Measure:
  - events/sec
  - average latency per emitted window
  - peak memory (best effort, psutil)
- Write:
  reports/stage_05_runtime_benchmark.md

3) scripts/stage_05_run.py
- One command wrapper:
  python scripts/stage_05_run.py --mode demo --model ensemble
- Runs demo + benchmark (demo mode small)

-----------------------------------------
LOGGING (required)
-----------------------------------------
- All scripts must log to:
  ai_workspace/logs/stage_05_runtime_demo.log
  ai_workspace/logs/stage_05_runtime_benchmark.log
- Use logging with FileHandler + StreamHandler.
- Include: start/end timestamps, mode, file paths, window params, counts.

-----------------------------------------
TESTS (required)
-----------------------------------------
Add tests under tests/:

1) test_sequence_buffer.py
- ingest N events, verify window emission timing, stride behavior

2) test_inference_engine_smoke.py
- load artifacts/models
- ingest a tiny synthetic event list (handmade minimal) and ensure:
  - returns None until window full
  - returns RiskResult after window full
  - RiskResult fields present

3) test_explain_decode.py
- verify token_id -> template string decode works using artifacts/vocab/templates

All tests must pass with:
pytest -q

-----------------------------------------
DELIVERABLES (required)
-----------------------------------------
- src/runtime/sequence_buffer.py
- src/runtime/inference_engine.py
- src/runtime/types.py (RiskResult etc.)
- scripts/stage_05_runtime_demo.py
- scripts/stage_05_runtime_benchmark.py
- scripts/stage_05_run.py
- reports/stage_05_runtime_inference_report.md (NEW)
- tests/* (3 tests)
- logs under ai_workspace/logs/

-----------------------------------------
REPORT (must be produced)
-----------------------------------------
Create:
reports/stage_05_runtime_inference_report.md

Must include:
1) What was implemented (classes + scripts)
2) How to run (exact PowerShell commands)
3) Demo results summary (how many windows emitted, anomaly rate observed)
4) Benchmark summary (events/sec, latency, peak memory)
5) Known limitations + next steps (Stage 6 alerts, Stage 7 API)

-----------------------------------------
WINDOWS POWERSHELL COMMANDS (must print at end)
-----------------------------------------
pip install -r requirements.txt
pytest -q
python scripts/stage_05_run.py --mode demo --model ensemble

Also print individual commands:
python scripts/stage_05_runtime_demo.py --mode demo --model baseline
python scripts/stage_05_runtime_demo.py --mode demo --model transformer
python scripts/stage_05_runtime_demo.py --mode demo --model ensemble
python scripts/stage_05_runtime_benchmark.py --mode demo --model ensemble

IMPORTANT:
- Use relative paths + pathlib everywhere.
- Keep demo mode fast (limit to 20k-50k events).
- Full mode should support large runs, but do not auto-run full mode.
- Do not modify Stage 26 code.
- If baseline runtime needs a different feature representation than session_features_v2.csv, implement a minimal token-count extractor for runtime scoring.

Proceed to implement Stage 5 now.
After implementation, run pytest -q and run the demo wrapper to ensure everything works.
Then generate the report file and confirm its path.