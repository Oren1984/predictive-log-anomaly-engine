SYSTEM ROLE:
Controlled AI engineering agent.

STRICT RULES:
- Only create/modify files inside:
  ai_workspace/stage_26_hdfs_supervised/
  ai_workspace/reports/
  ai_workspace/logs/
  data/models/
  data/intermediate/   (output files only)
- Do NOT modify previous stages outputs.
- Do NOT retrain or alter IsolationForest pipeline.
- No notebooks.

INPUT:
data/intermediate/session_features_v2.csv

OBJECTIVE:
Train a supervised baseline classifier for HDFS ONLY using existing labels.

DATA FILTER:
Use only rows where dataset == "hdfs".

FEATURES:
Use numeric columns excluding: session_id, dataset, label

SPLIT:
Stratified split by label:
- train 80%
- val 10%
- test 10%
random_state=42

MODEL (baseline):
LogisticRegression(max_iter=2000, class_weight="balanced", n_jobs=-1 if supported)
Use StandardScaler (fit on train only).
Use a Pipeline.

EVALUATION:
Compute on val and test:
- ROC AUC
- PR AUC (Average Precision)
- Precision, Recall, F1 (threshold=0.5 + also best F1 threshold on val)
- Confusion matrix

OUTPUTS:
1) Model:
   data/models/hdfs_logreg_v1.pkl
2) Scores:
   data/intermediate/hdfs_supervised_scores_v1.csv
   Columns: session_id, label, proba, pred_0_5, pred_bestF1
3) Report:
   ai_workspace/reports/stage_26_hdfs_supervised_report_v1.md
   Must include:
   - dataset sizes (train/val/test)
   - anomaly rate
   - metrics tables (val + test)
   - chosen bestF1 threshold from val
   - confusion matrices (test)
4) Plots (PNG) saved under:
   ai_workspace/stage_26_hdfs_supervised/
   - roc_curve_hdfs_v1.png
   - pr_curve_hdfs_v1.png
   - confusion_hdfs_v1.png
5) Log:
   ai_workspace/logs/stage_26_hdfs_supervised_v1.log
6) Script:
   ai_workspace/stage_26_hdfs_supervised/run_hdfs_supervised_v1.py

FINAL:
Print "Stage 26 (HDFS supervised) completed successfully."
List generated files.
Stop.