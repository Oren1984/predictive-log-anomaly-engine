You are working inside this repo:
C:\Users\ORENS\predictive-log-anomaly-engine

Goal:
Calibrate Stage 5 runtime thresholds using a lightweight stream-based calibration run (NO retraining).
We want a realistic demo: NOT 100% anomaly rate. Create a small calibration artifact and a closure report.

Constraints:
- Do NOT download any datasets.
- Do NOT retrain baseline/transformer models.
- Keep runs fast on CPU (demo scale).
- Use existing Stage 5 runtime code (InferenceEngine, SequenceBuffer).
- Use relative paths with pathlib.
- Windows PowerShell compatible.

Inputs (existing):
- data/processed/events_tokenized.parquet
- artifacts/threshold.json
- artifacts/threshold_transformer.json
- models/baseline.pkl
- models/transformer.pt
- src/runtime/* (InferenceEngine already exists)
- scripts/stage_05_runtime_demo.py, stage_05_runtime_benchmark.py, stage_05_run.py exist

What to implement (Stage 31):
1) Add a NEW script:
   scripts/stage_05_runtime_calibrate.py

   It must:
   - Stream N events from data/processed/events_tokenized.parquet ordered by timestamp.
   - Use key-by=service (default) and window_size=50 stride=10.
   - For each emitted window, collect:
       timestamp, stream_key, model, risk_score, and if label exists in meta, collect it too.
   - Produce thresholds for baseline, transformer, and ensemble that target a configurable alert rate.

   Calibration methods:
   A) If labels are available for emitted windows:
      - Choose threshold that maximizes F1 on calibration windows.
   B) If labels are missing or unreliable:
      - Choose threshold by percentile to hit a target alert rate.
      - Default target alert rate: 0.5% windows flagged.
      - That means threshold = quantile(scores, 1 - 0.005).

   Ensemble calibration:
   - Use the engine’s ensemble score output (do NOT invent a new ensemble).
   - Calibrate its threshold separately using the same method.
   - Ensure ensemble is NOT dominated by transformer by using the engine’s own score.

   Outputs:
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
     (one row per emitted window with the collected fields)

   - reports/stage_31_runtime_calibration_report.md
     Must include:
       - command used
       - n_events, n_windows
       - chosen method (f1/percentile)
       - thresholds
       - achieved alert rate per model
       - note explaining this is “demo-calibrated threshold” not full production calibration

   Logging:
   - ai_workspace/logs/stage_05_runtime_calibrate.log
     FileHandler + StreamHandler, include start/end, memory (psutil if available), throughput.

2) Update InferenceEngine to support loading runtime thresholds optionally:
   - If artifacts/threshold_runtime.json exists and user passes --use-runtime-thresholds true,
     then use those thresholds instead of threshold.json / threshold_transformer.json.
   - Must be backward compatible (default keeps old thresholds).

3) Update scripts/stage_05_runtime_demo.py and scripts/stage_05_run.py to accept:
   --use-runtime-thresholds (default false)
   When true, demo should use artifacts/threshold_runtime.json thresholds.

4) Add minimal tests:
   tests/unit/test_runtime_calibration.py
   - Run calibration on a tiny sample (e.g., n_events=2000)
   - Assert artifacts/threshold_runtime.json created
   - Assert thresholds are numeric and score_stats present

5) After implementation:
   - Run: pytest -q
   - Run calibration demo:
     python scripts/stage_05_runtime_calibrate.py --mode demo --model ensemble --n-events 50000 --target-alert-rate 0.005
   - Run runtime demo with calibrated thresholds:
     python scripts/stage_05_runtime_demo.py --mode demo --model ensemble --use-runtime-thresholds
   - Confirm anomaly rate is close to target (within ±0.3% absolute is fine)

Finally:
Print exact PowerShell commands for:
pip install -r requirements.txt
pytest -q
python scripts/stage_05_runtime_calibrate.py --mode demo --model ensemble --n-events 50000 --target-alert-rate 0.005
python scripts/stage_05_runtime_demo.py --mode demo --model ensemble --use-runtime-thresholds
And confirm the paths of:
artifacts/threshold_runtime.json
reports/stage_31_runtime_calibration_report.md
reports/runtime_calibration_scores.csv
ai_workspace/logs/stage_05_runtime_calibrate.loggi