You are working inside this existing repo:
C:\Users\ORENS\predictive-log-anomaly-engine

Goal (Stage 30 — Synthetic Data Subsystem):
Implement the missing Synthetic subsystem for Stage 1 (Data Layer) in a production-ready way.
This is an ADD-ON to the existing real-data pipeline, not a replacement.

Do NOT download any new dataset.
Do NOT modify Stage 5 runtime engine except to optionally support ingesting synthetic events in demo scripts.
Do NOT build API (Stage 7) and do NOT implement Alerts/n8n (Stage 6) yet.

We already have real data and stages 0–5 completed. Now we add synthetic generation to close Stage 1 fully.

-----------------------------------------
EXISTING CONTEXT (must preserve)
-----------------------------------------
- Real artifacts already exist and must remain unchanged:
  - data/processed/events_unified.csv
  - data/processed/schema.md
  - artifacts/templates.json, artifacts/vocab.json
  - models/*, artifacts/threshold*.json, reports/*
- Stage 1 currently provides:
  - LogEvent dataclass
  - KaggleDatasetLoader with normalize_schema()
- We now add:
  - FailurePattern hierarchy
  - SyntheticLogGenerator
  - ScenarioBuilder (“normal → degradation → failure”)
  - Synthetic dataset outputs under data/synth/

-----------------------------------------
REQUIRED CLASSES (names matter)
-----------------------------------------

Create under src/synthetic/:

1) FailurePattern (abstract base class)
- name: str
- severity_curve: optional helper
- Methods:
  - emit_event(t: int, ctx: dict) -> LogEvent
  - is_failure_phase(t: int, ctx: dict) -> bool
  - label_for_event(t: int, ctx: dict) -> int  (0/1)

2) Patterns (implement 4)
- MemoryLeakPattern
- DiskFullPattern
- AuthBruteForcePattern
- NetworkFlapPattern

Each pattern must:
- Generate realistic log messages (NOT too verbose)
- Gradually increase anomaly probability during degradation phase
- Produce labels:
  - 0 for normal
  - 1 for degradation/failure (or configurable)
Keep the logic deterministic with a seed.

3) SyntheticLogGenerator
- init(patterns: list[FailurePattern], seed: int = 42)
- generate(n_events: int, scenario: dict) -> list[LogEvent]
- Support multiple services/hosts via meta fields:
  meta should include: host, component, scenario_id, phase (normal|degradation|failure)

4) ScenarioBuilder
- build_scenario(
    scenario_id: str,
    service: str,
    host: str,
    start_ts: float,
    n_events: int,
    phases: dict
  ) -> dict
Where phases is something like:
  {
    "normal": 0.60,
    "degradation": 0.30,
    "failure": 0.10
  }
Return scenario dict used by generator.

-----------------------------------------
SCHEMA REQUIREMENTS
-----------------------------------------
Synthetic events MUST be compatible with Stage 1 normalize_schema output:

Normalized schema columns:
- timestamp
- service
- level
- message
- session_id (string)
- label (int 0/1)
- meta (dict-like; when writing to disk, expand key fields or JSON-string)

Make sure synthetic events can be turned into a DataFrame with those columns.

-----------------------------------------
DELIVERABLES (required)
-----------------------------------------

1) Data outputs (write under data/synth/)
- data/synth/events_synth.csv            (full)
- data/synth/events_synth.parquet        (preferred if parquet available)
- data/synth/scenarios.json              (scenario definitions)
- data/synth/schema_synth.md             (explain columns + meta keys)
- data/synth/README.md                   (how to regenerate, how it’s labeled)

2) Scripts
Create scripts:
- scripts/stage_01_synth_generate.py
  Args:
    --mode {demo,full}
    --seed 42
    --events 200000 (default full) / 20000 (default demo)
    --outdir data/synth
  Behavior:
    - Build 4 scenarios (one per pattern) and also a hybrid scenario combining patterns
    - Generate events and write outputs
    - Log to ai_workspace/logs/stage_01_synth_generate.log

- scripts/stage_01_synth_validate.py
  Behavior:
    - Load outputs from data/synth/
    - Validate:
      - required columns present
      - label distribution present (both 0 and 1)
      - phase distribution
      - message non-empty
    - Produce a report:
      reports/stage_30_synthetic_data_report.md
    - Log to ai_workspace/logs/stage_01_synth_validate.log

3) Minimal tests
Add tests under tests/unit/:
- test_synth_patterns.py
  - deterministic generation with seed
  - labels exist and match phases
  - message format sanity
- test_synth_schema.py
  - output df has required schema
  - meta contains required keys

All tests must pass with:
pytest -q

-----------------------------------------
LOGGING (required)
-----------------------------------------
- stage_01_synth_generate.log
- stage_01_synth_validate.log
Both under ai_workspace/logs/
Include: mode, seed, n_events, phase counts, anomaly rate.

-----------------------------------------
REPORT (required)
-----------------------------------------
Write:
reports/stage_30_synthetic_data_report.md

Must include:
1) Executive summary (what was generated)
2) Scenarios table (id, service, host, phases, anomaly rate)
3) Label distribution
4) Example messages (few lines per pattern)
5) How to regenerate (exact PowerShell commands)
6) How it plugs into existing pipeline (stages 1–5)
7) Known limitations

-----------------------------------------
IMPORTANT RULES
-----------------------------------------
- Use pathlib and relative paths.
- Windows PowerShell compatible.
- Keep messages safe and non-sensitive (no real secrets).
- Do not modify Stage 26 code.
- Do not download anything.

-----------------------------------------
FINAL: Print exact PowerShell commands
-----------------------------------------
pip install -r requirements.txt
pytest -q
python scripts/stage_01_synth_generate.py --mode demo
python scripts/stage_01_synth_validate.py

Also print a "full" example (do not run automatically):
python scripts/stage_01_synth_generate.py --mode full --events 200000

Proceed to implement now, run tests, run demo generation + validation, and write the report.
Then confirm the paths of:
- data/synth/events_synth.csv (and parquet if created)
- reports/stage_30_synthetic_data_report.md
- ai_workspace/logs/stage_01_synth_generate.log
- ai_workspace/logs/stage_01_synth_validate.log