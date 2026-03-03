SYSTEM ROLE:
Controlled AI engineering agent.

STRICT RULES:
- Only create/modify files inside:
  ai_workspace/stage_26_hdfs_supervised/
  ai_workspace/reports/
  ai_workspace/logs/
  data/models/
  data/intermediate/   (output only)
- Do NOT touch other stages.

INPUT:
data/intermediate/session_features_v2.csv

OBJECTIVE:
Improve Stage 26 slightly by model selection on HDFS only (same split), choosing best by VAL PR-AUC.

DATA:
Filter dataset == "hdfs".
Use numeric features excluding: session_id, dataset, label.

SPLIT:
Stratified split (same as v1):
train 80%, val 10%, test 10%, random_state=42.

MODELS TO COMPARE (use Pipeline with StandardScaler where relevant):
A) LogisticRegression L2 (baseline):
   LogisticRegression(max_iter=4000, class_weight="balanced")
B) LogisticRegression L1 feature selection:
   LogisticRegression(penalty="l1", solver="saga", max_iter=6000,
                      class_weight="balanced", C in [0.2, 0.5, 1.0])
C) HistGradientBoostingClassifier (nonlinear):
   HistGradientBoostingClassifier(max_depth=6, learning_rate=0.05,
                                  max_iter=300, random_state=42)

MODEL SELECTION:
- Choose best model by VAL PR-AUC (average_precision_score on probabilities/scores).
- For the chosen model, choose threshold on VAL that maximizes F1.
- Evaluate on TEST using the chosen threshold.

OUTPUTS (versioned v2):
1) data/models/hdfs_supervised_best_v2.pkl
2) data/intermediate/hdfs_supervised_scores_v2.csv
   Columns: session_id, label, proba_or_score, pred_0_5, pred_bestF1
3) ai_workspace/reports/stage_26_hdfs_supervised_report_v2.md
   Include:
   - split sizes + anomaly rate
   - comparison table (VAL): ROC AUC, PR AUC for each model
   - chosen model + params
   - TEST metrics: ROC AUC, PR AUC, Precision/Recall/F1 (0.5 + bestF1 threshold)
   - confusion matrix on TEST (bestF1)
4) Plots in ai_workspace/stage_26_hdfs_supervised/:
   - roc_curve_hdfs_v2.png
   - pr_curve_hdfs_v2.png
   - confusion_hdfs_v2.png
5) Log:
   ai_workspace/logs/stage_26_hdfs_supervised_v2.log
6) Script:
   ai_workspace/stage_26_hdfs_supervised/run_hdfs_supervised_v2.py

FINAL:
Print "Stage 26 (v2) completed successfully."
List generated files.
Stop.