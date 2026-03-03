You are working inside this existing repo:
C:\Users\ORENS\predictive-log-anomaly-engine

Goal:
Close Stage 1 (Data Layer) and Stage 2 (Parsing + Template Mining) COMPLETELY
with full artifacts written to disk and verification logs.

Do NOT modify Stage 3+ code.
Do NOT retrain models.
Only validate and finalize Stage 1 and Stage 2.

-----------------------------------------
PART 1 — Stage 1 Validation
-----------------------------------------

1. Import and validate:
   - LogEvent dataclass
   - KaggleDatasetLoader

2. Execute:
   python scripts/stage_01_data.py --mode full

3. Ensure:
   - data/processed/schema.md exists
   - events_unified.csv loads successfully
   - normalize_schema() returns valid structure
   - No exceptions

4. Write validation log to:
   ai_workspace/logs/stage_01_data_full.log

-----------------------------------------
PART 2 — Stage 2 Full Execution
-----------------------------------------

1. Execute FULL mode:
   python scripts/stage_02_templates.py --mode full

2. Ensure these artifacts exist:

   - artifacts/templates.json
   - artifacts/vocab.json
   - data/processed/events_tokenized.parquet

3. Validate:
   - parquet file row count > 0
   - token_id column exists
   - file size > 100MB

4. Write execution log to:
   ai_workspace/logs/stage_02_templates_full.log

-----------------------------------------
PART 3 — Artifact Integrity Check
-----------------------------------------

Programmatically verify:

- templates.json entries > 1000
- vocab.json includes PAD=0 and UNK=1
- events_tokenized.parquet columns include:
  [timestamp, service, template_id, token_id, label]

-----------------------------------------
PART 4 — Produce Closing Report
-----------------------------------------

Generate file:
reports/stage_28_stage_1_2_closure_report.md

Include:
- Artifact sizes
- Row counts
- Memory usage during run
- Confirmation that Stage 1 + 2 are fully closed
- Any warnings if detected

Final output must state:

STAGE_1_2_STATUS = CLOSED