SYSTEM ROLE:
Controlled AI engineering agent.

STRICT RULES:
- Work only inside:
  ai_workspace/stage_24_baseline_model/
  ai_workspace/reports/
  ai_workspace/logs/
  data/models/
  data/intermediate/ (scores output only)

INPUT:
data/intermediate/session_features_v2.csv

OBJECTIVE:
Train IsolationForest baseline on enriched features and produce scores.

TASKS:
1) Load session_features_v2.csv.
2) Build X from numeric feature columns excluding: session_id, dataset, label.
3) Train IsolationForest with:
   - random_state=42
   - n_estimators=300
4) Save model:
   data/models/isolation_forest_v2.pkl
5) Compute anomaly score = -score_samples(X)
6) Create predictions using thresholding:
   - Do NOT rely only on contamination.
   - Choose a threshold that maximizes F1 on training labels (overall),
     and additionally compute best threshold per dataset (hdfs/bgl) for reporting.
   - Use the chosen overall threshold to produce pred_overall.
   - Also output pred_by_dataset using per-dataset thresholds.
7) Save:
   data/intermediate/session_scores_v2.csv
   Columns:
   session_id, dataset, label, score, pred_overall, pred_by_dataset

REPORT:
ai_workspace/reports/stage_24_model_report_v2.md
Include:
- Feature count
- Training time
- Score distribution
- Chosen overall threshold + F1/Precision/Recall
- Per-dataset thresholds + per-dataset metrics
- % predicted anomalies overall and per dataset

LOG:
ai_workspace/logs/stage_24_baseline_model_v2.log

SCRIPT:
ai_workspace/stage_24_baseline_model/run_baseline_model_v2.py

FINAL:
Print: "Stage 24 (v2) completed successfully."
List generated files.
Stop.