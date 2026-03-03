You are working inside this existing repo:
C:\Users\ORENS\predictive-log-anomaly-engine

Goal: Close stages 0–4 completely with NO gaps, using the data artifacts that ALREADY exist in this repo.
Do NOT download any new dataset.

Existing artifacts (must be used):
- data/raw/HDFS_1/HDFS.log
- data/raw/HDFS_2/*.log
- data/raw/BGL.log
- data/processed/events_unified.csv
- data/intermediate/templates.csv
- data/intermediate/events_with_templates.csv
- data/intermediate/session_sequences_v2.csv
- data/intermediate/session_features_v2.csv   (shape ~495,405 x 407, includes tid_* columns)
- Stage 26 scripts already exist under ai_workspace/stage_26_hdfs_supervised/ and logs under ai_workspace/logs/

Task 1 — Create clean "system-level" modules and classes (stages 1–3 packaging)
Create a new package under src/ that provides these EXACT classes (names matter):

Stage 1 (Data Layer):
- LogEvent dataclass: timestamp, service, level, message, meta(dict), label(optional)
- KaggleDatasetLoader with methods:
  download() -> no-op
  load_raw() -> loads existing raw files from data/raw if needed (minimal)
  normalize_schema() -> reads data/processed/events_unified.csv and returns list[LogEvent] OR a pandas dataframe in normalized schema.
Write schema.md to data/processed/schema.md describing columns that exist in events_unified.csv.

Stage 2 (Parsing + Template Mining):
- LogParser interface parse(raw)->LogEvent
- RegexLogParser and JsonLogParser (minimal implementations, mainly for completeness)
- TemplateMiner with:
  fit(events)
  transform(events)->template_ids
BUT in this repo we already have template outputs:
- templates.csv
- events_with_templates.csv
So implement TemplateMiner as a wrapper that can load existing templates and mapping:
  load_from_csv(templates_csv_path)
  transform_from_existing(events_with_templates_csv) -> returns template_ids
- EventTokenizer with encode/decode using templates.csv mapping.
Write outputs:
  artifacts/templates.json
  artifacts/vocab.json
  data/processed/events_tokenized.parquet (or csv if parquet not available)

Stage 3 (Sequence Builder):
- Sequence dataclass: tokens(list[int]), timestamps(list), label(optional), sequence_id
- SequenceBuilder interface build(events)->list[Sequence]
- SlidingWindowSequenceBuilder(window=50,stride=10)
- SessionSequenceBuilder that loads sequences from:
  data/intermediate/session_sequences_v2.csv (preferred)
If session_sequences_v2.csv already contains token lists, parse them correctly.
- DatasetSplitter with split_time_based() and split_stratified()
Write outputs:
  data/processed/sequences_train.parquet
  data/processed/sequences_val.parquet
  data/processed/sequences_test.parquet

Task 2 — Stage 4A Baseline module (wrap existing baseline work into classes)
Create under src/modeling:
- BaselineFeatureExtractor that can use:
  a) tid_* columns from session_features_v2.csv (preferred, already engineered)
  b) fallback to ngram/tfidf from sequences if needed
- BaselineAnomalyModel: fit(X,y), predict_proba(X), score(X)
  Use LogisticRegression(class_weight="balanced") as default.
- ThresholdCalibrator: fit(scores_val,y_val) -> best F1 threshold; is_anomaly(score).
Provide a script scripts/stage_04_baseline.py that trains and writes:
- models/baseline.pkl
- artifacts/threshold.json
- reports/stage_04_baseline.md (similar style to Stage 26 report)

Task 3 — Stage 4B Transformer Next-Token (NEW, must be implemented)
Implement a CPU-friendly Next-Token Transformer using PyTorch:
- TransformerConfig
- NextTokenTransformerModel
- Trainer (train/evaluate/save)
- AnomalyScorer: score sequences by negative log-likelihood (NLL) per token; output anomaly score per sequence.
Train on sequences_train, validate on sequences_val, pick threshold on val (best F1 if labels exist; otherwise percentile).
Write outputs:
- models/transformer.pt
- reports/stage_04_transformer.md
- reports/metrics_transformer.json
- artifacts/threshold_transformer.json

Task 4 — Scripts and one-command pipeline (stages 1–4)
Create scripts:
- scripts/stage_01_data.py -> loads existing events_unified.csv and writes normalized outputs
- scripts/stage_02_templates.py -> loads templates.csv + events_with_templates.csv and writes artifacts/templates.json + vocab.json + events_tokenized
- scripts/stage_03_sequences.py -> builds/loads sequences and writes train/val/test
- scripts/stage_04_baseline.py -> trains baseline on session_features_v2.csv and writes outputs
- scripts/stage_04_transformer.py -> trains transformer on sequences and writes outputs
- scripts/run_0_4.py -> runs stages 1–4 in order with --mode demo (fast defaults)

Rules:
- Must work on Windows PowerShell.
- Use relative paths and pathlib.
- Add robust logging to ai_workspace/logs with stage_xx names.
- Add minimal tests under tests/ for tokenizer, sequence parsing, calibrator.

Finally, print exact PowerShell commands to run:
pip install -r requirements.txt
python scripts/run_0_4.py --mode demo
and also each stage script individually.

IMPORTANT: Do not modify existing Stage 26 code except if you need to import utilities; focus on new src/ + scripts/ wrappers and new transformer stage.