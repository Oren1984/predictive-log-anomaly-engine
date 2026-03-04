# Stage 25 Evaluation Report

**Generated:** 2026-03-03  
**Execution time:** 2.0s  

---

## Overall Metrics

| Metric | Value |
|--------|------:|
| Sessions evaluated | 495,405 |
| Actual anomalies | 94,508 (19.08%) |
| Predicted anomalies | 24,753 (5.00%) |
| ROC AUC | 0.5398 |
| PR AUC | 0.2518 |
| Precision | 0.3598 |
| Recall | 0.0942 |
| F1 | 0.1494 |

---

## Per-Dataset Metrics

| Dataset | N | Anomalies | ROC AUC | PR AUC | Precision | Recall | F1 |
|---------|--:|----------:|--------:|-------:|----------:|-------:|---:|
| bgl | 91,226 | 85,018 (93.19%) | 0.6792 | 0.9698 | 1.0000 | 0.0976 | 0.1779 |
| hdfs | 404,179 | 9,490 (2.35%) | 0.5153 | 0.0273 | 0.0368 | 0.0639 | 0.0467 |

---

## Confusion Matrix

| | Predicted Normal | Predicted Anomaly |
|---|----------------:|------------------:|
| **Actual Normal**  | 385,050 (TN) | 15,847 (FP) |
| **Actual Anomaly** | 85,602 (FN) | 8,906 (TP) |

---

## Score Distribution

| Stat | Value |
|------|------:|
| Min  | 0.3042 |
| Mean | 0.3400 |
| Median | 0.3362 |
| Max  | 0.4860 |

---

## Notes

**Class imbalance:** The dataset is imbalanced (~19% anomalies at session level). PR AUC is a more informative metric than ROC AUC under imbalance, since it penalises false positives relative to the minority class.

**Contamination choice:** All three contamination candidates (0.05, 0.10, 0.20) yielded identical PR-AUC (0.2518) because `average_precision_score` is computed from continuous `score_samples`, which are independent of the contamination threshold. Contamination 0.05 was selected (lowest/first). The low F1 reflects that IsolationForest, an unsupervised method, cannot fully separate the anomaly distribution given the aggregate feature space used here.

**Interpretation:** ROC AUC > 0.5 confirms the model has learned a signal, but low recall shows many anomalous sessions are scored close to normal ones — consistent with the narrow score range observed (0.30–0.49).

---

## Generated Plots

| Plot | File |
|------|------|
| ROC Curve | `ai_workspace/stage_25_evaluation/roc_curve.png` |
| PR Curve | `ai_workspace/stage_25_evaluation/pr_curve.png` |
| Score Histogram | `ai_workspace/stage_25_evaluation/score_histogram.png` |
| Confusion Matrix | `ai_workspace/stage_25_evaluation/confusion_matrix.png` |

---

*Stage 25 completed successfully.*
