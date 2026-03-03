SYSTEM ROLE:
Controlled AI engineering agent.

STRICT RULES:
- Only modify/create:
  ai_workspace/stage_25_evaluation/
  ai_workspace/reports/
  ai_workspace/logs/
- Do NOT retrain.

INPUT:
data/intermediate/session_scores_v2.csv

OBJECTIVE:
Evaluate V2 results for both prediction modes.

TASKS:
1) Load session_scores_v2.csv.
2) Compute overall metrics using:
   - pred_overall
   - pred_by_dataset
   Metrics: ROC AUC (label vs score), PR AUC, Precision/Recall/F1, confusion matrix
3) Compute per-dataset metrics for both modes.
4) Save plots (PNG) under ai_workspace/stage_25_evaluation/:
   - roc_curve_v2.png
   - pr_curve_v2.png
   - score_histogram_v2.png
   - confusion_overall_v2.png
   - confusion_by_dataset_v2.png
5) Write report:
   ai_workspace/reports/stage_25_evaluation_report_v2.md
   Must include:
   - table: overall metrics for both modes
   - table: per-dataset metrics for both modes
   - confusion matrices
   - brief interpretation

LOG:
ai_workspace/logs/stage_25_evaluation_v2.log

SCRIPT:
ai_workspace/stage_25_evaluation/run_evaluation_v2.py

FINAL:
Print: "Stage 25 (v2) completed successfully."
List generated files.