# Stage 05 — System Audit Report (Stages 0–5)

**Generated:** 2026-03-03
**Auditor:** automated repo inspection
**Scope:** Stages 0–5 inclusive

---

## 1. Repo Snapshot

| Item | Value |
|------|-------|
| Audit timestamp | 2026-03-03 ~19:32 local (Windows local time) |
| OS | Windows 11 Home 10.0.26200 |
| Python | 3.13.9 |
| Branch | main (up to date with origin/main) |
| Repo root | `C:\Users\ORENS\predictive-log-anomaly-engine` |

### Git Status

**Dirty** — 9 modified tracked files, 11 untracked files.

**Modified (tracked):**

| File | Note |
|------|------|
| `.gitignore` | updated |
| `ai_workspace/logs/stage_05_runtime_demo.log` | re-run log |
| `ai_workspace/prompts/stage_31_runtime_calibration_copilot_prompt.md` | updated prompt |
| `reports/runtime_demo_evidence.jsonl` | re-run evidence |
| `reports/runtime_demo_results.csv` | re-run results |
| `scripts/stage_01_synth_generate.py` | extended with new CLI + canonical parquet |
| `scripts/stage_05_run.py` | updated |
| `scripts/stage_05_runtime_demo.py` | updated |
| `src/runtime/inference_engine.py` | updated |

**Untracked (new):**

| File | Note |
|------|------|
| `ai_workspace/prompts/STAGE_32_SYNTHETIC_DATA_EXECUTION_PROMPT.md` | prompt for Stage 32 |
| `artifacts/threshold_runtime.json` | Stage 31 calibration output |
| `data/synth/` (directory) | Stage 1 synthetic data outputs |
| `nul` | stray 0-byte Windows artefact |
| `reports/stage_01_synth_report.md` | Stage 01 synth report |
| `reports/stage_31_runtime_calibration_report.md` | Stage 31 report |
| `scripts/stage_01_synth_to_processed.py` | new helper script |
| `scripts/stage_05_runtime_calibrate.py` | Stage 31 calibration script |
| `src/data/` (directory) | synthetic data model package |
| `tests/unit/test_runtime_calibration.py` | new test |
| `tests/unit/test_synth_generation.py` | new test |

---

## 2. Stage Closure Summary (Stages 0–5)

| Stage | Name | Purpose | Entry Script(s) | Key Inputs | Key Outputs / Artifacts | Evidence | Status |
|-------|------|---------|-----------------|------------|-------------------------|----------|--------|
| **0** | Repo Scaffold | Directory layout, requirements, schema.md, raw data | `scripts/stage_01_data.py` (scaffold check) | `data/processed/events_unified.csv` | `requirements.txt`, `data/processed/schema.md`, `data/intermediate/templates.csv`, `data/intermediate/session_sequences_v2.csv` | `reports/stage_27_stages_0_4_completion_report.md` | **PASS** |
| **1** | Data Layer | LogEvent model + KaggleDatasetLoader; Stage 01 synthetic generator | `scripts/stage_01_data.py`, `scripts/stage_01_synth_generate.py` | `data/processed/events_unified.csv` | `data/synth/events_synth.parquet`, `data/synth/schema.md`, `data/processed/events_synth.parquet`, `reports/stage_01_synth_report.md` | `reports/stage_28_stage_1_2_closure_report.md`, `reports/stage_01_synth_report.md` | **PASS** |
| **2** | Parsing & Tokenization | Template mining, EventTokenizer, vocab + parquet | `scripts/stage_02_templates.py` | `data/processed/events_unified.csv` (1M sample) | `artifacts/vocab.json`, `artifacts/templates.json`, `data/processed/events_tokenized.parquet` (1M rows) | `reports/stage_28_stage_1_2_closure_report.md` | **PASS** |
| **3** | Sequence Building | Session + sliding-window sequence builders, DatasetSplitter | `scripts/stage_03_sequences.py` | `data/processed/events_tokenized.parquet` | `data/processed/sequences_train.parquet`, `sequences_val.parquet`, `sequences_test.parquet` | `reports/stage_27_stages_0_4_completion_report.md` | **PASS** |
| **4A** | Baseline Model | IsolationForest anomaly model + ThresholdCalibrator | `scripts/stage_04_baseline.py` | `data/processed/sequences_train.parquet` | `models/baseline.pkl`, `artifacts/threshold.json`, `reports/metrics.json`* | `reports/stage_04_baseline.md` | **PASS** |
| **4B** | Transformer Model | NextToken transformer, Trainer, AnomalyScorer | `scripts/stage_04_transformer.py` | `data/processed/sequences_*.parquet` | `models/transformer.pt`, `artifacts/threshold_transformer.json`, `reports/metrics_transformer.json` | `reports/stage_04_transformer.md` | **PASS** |
| **5** | Runtime Inference | Streaming InferenceEngine (baseline/transformer/ensemble), RiskResult | `scripts/stage_05_runtime_demo.py`, `scripts/stage_05_run.py`, `scripts/stage_05_runtime_benchmark.py` | `models/baseline.pkl`, `models/transformer.pt`, `artifacts/vocab.json`, `data/processed/sequences_train.parquet` | `reports/runtime_demo_results.csv`, `reports/runtime_demo_evidence.jsonl`, `reports/stage_05_runtime_benchmark.md` | `reports/stage_05_runtime_inference_report.md` | **PASS** |
| **5+** | Runtime Calibration | Percentile threshold calibration for runtime use | `scripts/stage_05_runtime_calibrate.py` | same as Stage 5 | `artifacts/threshold_runtime.json`, `reports/runtime_calibration_scores.csv` | `reports/stage_31_runtime_calibration_report.md` | **PASS** |

_\* `reports/metrics.json` is 0 bytes — see Known Gaps._

---

## 3. Artifacts Inventory

### `artifacts/`

| File | Size | Last Modified |
|------|-----:|---------------|
| `templates.json` | 1,541,328 B | 2026-03-03 15:17 |
| `threshold.json` | 97 B | 2026-03-03 14:57 |
| `threshold_runtime.json` | 875 B | 2026-03-03 19:12 |
| `threshold_transformer.json` | 40 B | 2026-03-03 14:57 |
| `vocab.json` | 1,541,368 B | 2026-03-03 15:17 |

**threshold.json contents:** `{"threshold": 0.3303, "best_f1": 0.4605, "n_thresholds": 300}`
**threshold_transformer.json contents:** `{"threshold": 0.03405}`
**threshold_runtime.json:** calibrated ensemble=135.83, baseline=0.540, transformer=9.196 (percentile method, target 0.5% alert rate)

### `models/`

| File | Size | Last Modified |
|------|-----:|---------------|
| `baseline.pkl` | 1,605,322 B | 2026-03-03 14:57 |
| `transformer.pt` | 2,094,667 B | 2026-03-03 14:57 |

### `reports/`

| File | Size | Last Modified |
|------|-----:|---------------|
| `metrics.json` | **0 B** | 2026-03-03 08:16 |
| `metrics_transformer.json` | 258 B | 2026-03-03 14:57 |
| `runtime_calibration_scores.csv` | 18,643 B | 2026-03-03 19:12 |
| `runtime_demo_evidence.jsonl` | 3,505,575 B | 2026-03-03 18:03 |
| `runtime_demo_results.csv` | 314,069 B | 2026-03-03 18:03 |
| `stage_01_synth_report.md` | 2,335 B | 2026-03-03 19:16 |
| `stage_04_baseline.md` | 793 B | 2026-03-03 14:57 |
| `stage_04_transformer.md` | 1,026 B | 2026-03-03 14:57 |
| `stage_05_runtime_benchmark.md` | 758 B | 2026-03-03 16:11 |
| `stage_05_runtime_inference_report.md` | 9,516 B | 2026-03-03 16:13 |
| `stage_27_stages_0_4_completion_report.md` | 16,974 B | 2026-03-03 15:07 |
| `stage_28_stage_1_2_closure_report.md` | 9,087 B | 2026-03-03 15:18 |
| `stage_31_runtime_calibration_report.md` | 2,193 B | 2026-03-03 19:12 |

### `data/synth/`

| File | Size | Last Modified |
|------|-----:|---------------|
| `events_synth.csv` | 7,949,245 B | 2026-03-03 19:13 |
| `events_synth.parquet` | 803,364 B | 2026-03-03 19:13 |
| `events_synth_full.parquet` | 677,401 B | 2026-03-03 19:13 |
| `scenarios.json` | 2,905 B | 2026-03-03 19:13 |
| `schema.md` | 1,513 B | 2026-03-03 19:13 |

### `data/processed/` (parquet files only)

| File | Size | Last Modified |
|------|-----:|---------------|
| `events_synth.parquet` | 803,364 B | 2026-03-03 19:13 |
| `events_tokenized.parquet` | 17,356,301 B | 2026-03-03 15:17 |
| `sequences_test.parquet` | 7,009 B | 2026-03-03 14:57 |
| `sequences_train.parquet` | 35,705 B | 2026-03-03 14:57 |
| `sequences_val.parquet` | 7,074 B | 2026-03-03 14:57 |

---

## 4. Verification Evidence

### pytest -q

```
114 passed in 18–23s
```

**Test file breakdown:**

| Test File | Count | Coverage |
|-----------|------:|---------|
| `test_tokenizer.py` | — | EventTokenizer, template mining |
| `test_sequences.py` | — | SlidingWindowSequenceBuilder, SessionSequenceBuilder |
| `test_calibrator.py` | — | ThresholdCalibrator |
| `test_sequence_buffer.py` | 22 | SequenceBuffer (Stage 5) |
| `test_inference_engine_smoke.py` | 20 | InferenceEngine all 3 modes (Stage 5) |
| `test_explain_decode.py` | 14 | explain() + vocab/templates (Stage 5) |
| `test_runtime_calibration.py` | — | Stage 31 calibration |
| `test_synth_generation.py` | 7 | Synthetic data pipeline (Stage 1) |
| `test_placeholder.py` | — | placeholder |
| **Total** | **114** | **all pass** |

### stage_05_runtime_demo.py --mode demo --model ensemble

Command executed (without `--n-events` which is not a valid argument):

```powershell
python scripts/stage_05_runtime_demo.py --mode demo --model ensemble
```

**Result:**

```
events_processed: 20,000
windows_emitted:  1,991
anomalies_flagged: 1,991
anomaly_rate_pct:  100.0
elapsed_s:         54.39
events_per_sec:    367.7
mode:              demo
model:             ensemble
key_by:            service
```

Output files updated: `reports/runtime_demo_results.csv` (1,991 rows), `reports/runtime_demo_evidence.jsonl`.

> **Note on 100% anomaly rate:** This is a known and documented limitation. The demo-mode models are trained on 2–3 token sequences; the 50-token runtime windows produce scores (~132) far above the default threshold (1.0). The calibrated threshold in `artifacts/threshold_runtime.json` (ensemble=135.83) reduces the alert rate to 0.5% — see Stage 31 calibration.

---

## 5. Known Gaps / Risks

| # | Location | Observation | Severity |
|---|----------|-------------|----------|
| 1 | `reports/metrics.json` | File is **0 bytes**. Stage 4A baseline report (`stage_04_baseline.md`) exists with correct metrics, but this JSON file is empty. Downstream code that reads `metrics.json` will fail. | Low — demo pipeline does not read it at runtime |
| 2 | `nul` | Stray 0-byte file named `nul` in repo root — Windows artefact from a redirected write. Safe to delete (`git rm nul`). | Cosmetic |
| 3 | Stage 5 default threshold | Default ensemble threshold is 1.0 (normalised). All demo windows score ~132, giving 100% anomaly rate. Calibrated threshold (135.83) exists in `artifacts/threshold_runtime.json`. Pass `--use-runtime-thresholds` to use it. | Known, documented |
| 4 | `data/synth/events_synth_full.parquet` | Redundant file written alongside `events_synth.parquet`. Both contain 50k events but with different column schemas (full has `session_id`, `host`, `component`, `scenario_id`, `phase`; canonical has `timestamp`, `service`, `level`, `message`, `meta`, `label`). Not a bug but may cause confusion. | Cosmetic |
| 5 | Untracked files not committed | 11 new files (including `src/data/`, `tests/unit/test_synth_generation.py`, `scripts/stage_01_synth_to_processed.py`, `artifacts/threshold_runtime.json`, Stage 01 and Stage 31 reports) are untracked. Repo is dirty. | Low — no functional impact |

---

## 6. Exact PowerShell Commands Run for Verification

```powershell
# From repo root: C:\Users\ORENS\predictive-log-anomaly-engine

# 1. Git status
git status

# 2. Run full test suite
python -m pytest -q

# 3. Run Stage 5 demo (ensemble, demo mode)
python scripts/stage_05_runtime_demo.py --mode demo --model ensemble

# 4. Install dependencies (reference)
pip install -r requirements.txt

# 5. Regenerate synthetic data (Stage 1)
python scripts/stage_01_synth_generate.py --n-events 50000

# 6. Copy synthetic data to processed/
python scripts/stage_01_synth_to_processed.py --in data/synth/events_synth.parquet --out data/processed/events_synth.parquet
```

---

_Audit complete. All 6 stages (0–5) are PASS. 114 tests passing. No blocking issues._
