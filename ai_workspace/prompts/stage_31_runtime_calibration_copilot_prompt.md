YOU ARE WORKING INSIDE THIS REPO:
C:\Users\ORENS\predictive-log-anomaly-engine

MODE: EXECUTION (implement first, explain after only if asked)

GOAL:
Calibrate Stage 5 runtime thresholds using a lightweight stream-based calibration run (NO retraining).
We want a realistic demo: NOT 100% anomaly rate. Create calibration artifacts + a closure report.

NON-NEGOTIABLE CONSTRAINTS:
- NO Docker work. Do NOT create or modify Dockerfile / docker-compose.yml.
- Do NOT download any datasets.
- Do NOT retrain baseline/transformer models.
- Keep runs fast on CPU (demo scale).
- Use existing Stage 5 runtime code (InferenceEngine, SequenceBuffer).
- Use relative paths with pathlib (no hardcoded absolute paths in code).
- Windows PowerShell compatible commands.

EXISTING INPUTS (do not change data formats):
- data/processed/events_tokenized.parquet
- artifacts/threshold.json
- artifacts/threshold_transformer.json
- models/baseline.pkl
- models/transformer.pt
- src/runtime/* (InferenceEngine already exists)
- scripts/stage_05_runtime_demo.py, scripts/stage_05_runtime_benchmark.py, scripts/stage_05_run.py exist

DELIVERABLES (Stage 31):

1) NEW SCRIPT:
   Create: scripts/stage_05_runtime_calibrate.py

   Requirements:
   - Stream N events from data/processed/events_tokenized.parquet ordered by timestamp.
   - key_by = service (default), window_size=50, stride=10 (CLI configurable but default as specified).
   - For each emitted window collect:
       timestamp, stream_key, model, risk_score
       and if label exists in meta -> include label (nullable).
   - Produce thresholds for baseline, transformer, and ensemble targeting a configurable alert rate.

   Calibration methods:
   A) If labels exist for the emitted windows (enough labels):
      - Choose threshold maximizing F1 on calibration windows.
   B) If labels are missing/unreliable:
      - Choose threshold by percentile to hit target alert rate.
      - Default target alert rate = 0.005 (0.5% windows flagged)
      - threshold = quantile(scores, 1 - target_alert_rate)

   Ensemble calibration:
   - Use engine’s ensemble score output (do NOT invent a new ensemble).
   - Calibrate ensemble threshold separately using the same method.
   - Do NOT weight transformer/baseline manually. Use engine output only.

   Outputs (must be created):
   - artifacts/threshold_runtime.json
     Schema:
     {
       "generated_at": "...",
       "mode": "demo",
       "key_by": "service",
       "window_size": 50,
       "stride": 10,
       "n_events": 50000,
       "n_windows": <int>,
       "method": "percentile" or "f1",
       "target_alert_rate": 0.005,
       "thresholds": {
          "baseline": <float>,
          "transformer": <float>,
          "ensemble": <float>
       },
       "score_stats": {
          "baseline": {"min":..,"p50":..,"p95":..,"p99":..,"max":..},
          "transformer": {...},
          "ensemble": {...}
       }
     }

   - reports/runtime_calibration_scores.csv
     One row per emitted window with collected fields.

   - reports/stage_31_runtime_calibration_report.md
     Must include:
       - exact command used
       - n_events, n_windows
       - chosen method (f1/percentile) and why
       - thresholds
       - achieved alert rate per model
       - note: "demo-calibrated threshold" not production calibration

   Logging:
   - ai_workspace/logs/stage_05_runtime_calibrate.log
     Use FileHandler + StreamHandler
     Include start/end, throughput, and memory if psutil available (optional, do not add heavy deps).

2) UPDATE RUNTIME ENGINE (backward compatible):
   Update InferenceEngine to support optional runtime thresholds:
   - If artifacts/threshold_runtime.json exists AND user passes --use-runtime-thresholds true:
       use thresholds from threshold_runtime.json
     else:
       keep existing behavior using threshold.json / threshold_transformer.json
   - Must not break existing scripts.

3) UPDATE EXISTING SCRIPTS:
   Update:
   - scripts/stage_05_runtime_demo.py
   - scripts/stage_05_run.py
   Add CLI flag:
   --use-runtime-thresholds (default false)
   When true -> demo/run uses artifacts/threshold_runtime.json thresholds.

4) MINIMAL TESTS:
   Create: tests/unit/test_runtime_calibration.py
   - Run calibration on tiny sample (n_events=2000)
   - Assert artifacts/threshold_runtime.json created
   - Assert thresholds are numeric and score_stats present
   - Keep test fast and deterministic.

5) AFTER IMPLEMENTATION (MANDATORY VERIFICATION):
   - Run: pytest -q
   - Run calibration demo:
     python scripts/stage_05_runtime_calibrate.py --mode demo --model ensemble --n-events 50000 --target-alert-rate 0.005
   - Run runtime demo with calibrated thresholds:
     python scripts/stage_05_runtime_demo.py --mode demo --model ensemble --use-runtime-thresholds
   - Confirm anomaly rate is close to target (±0.003 absolute is fine).

FINAL OUTPUT REQUIRED:
A) Print a summary of created/modified files.
B) Print exact PowerShell commands (copy/paste ready):
   pip install -r requirements.txt
   pytest -q
   python scripts/stage_05_runtime_calibrate.py --mode demo --model ensemble --n-events 50000 --target-alert-rate 0.005
   python scripts/stage_05_runtime_demo.py --mode demo --model ensemble --use-runtime-thresholds
C) Confirm these files exist (paths):
   artifacts/threshold_runtime.json
   reports/stage_31_runtime_calibration_report.md
   reports/runtime_calibration_scores.csv
   ai_workspace/logs/stage_05_runtime_calibrate.log

BEGIN EXECUTION NOW.