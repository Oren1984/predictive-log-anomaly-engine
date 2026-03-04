# Stage 24 Baseline Model Report

**Generated:** 2026-03-03  
**Execution time:** 24.1s  
**Peak memory:** 1406.9 MB  

---

## Model Configuration

| Parameter | Value |
|-----------|-------|
| Model | IsolationForest |
| n_estimators | 200 |
| random_state | 42 |
| Chosen contamination | 0.05 |
| Feature count | 201 |
| Training sessions | 495,405 |
| Observed anomaly rate | 19.08% |

---

## Contamination Sweep

Contamination selected by highest PR-AUC (average precision score)  
against ground-truth labels. This is for selection only — the model  
is fully unsupervised during training.

| Contamination | PR-AUC | Train time | |
|--------------|-------:|-----------|---|
| 0.05 | 0.2518 | 5.7s | **chosen** |
| 0.10 | 0.2518 | 5.8s | |
| 0.20 | 0.2518 | 5.7s | |

---

## Score Distribution

*(Anomaly score = -score_samples; higher = more anomalous)*

| Stat | Value |
|------|------:|
| Min | 0.3042 |
| Mean | 0.3400 |
| Median | 0.3362 |
| 95th pct | 0.3733 |
| Max | 0.4860 |

---

## Predictions Summary

| Metric | Value |
|--------|------:|
| Total sessions | 495,405 |
| Predicted anomalies | 24,753 (5.00%) |
| Actual anomalies (label=1) | 94,508 (19.08%) |

---

## Sanity Metrics (pred vs label)

*(Unsupervised model — labels used only for evaluation, not training)*

| Metric | Value |
|--------|------:|
| Precision | 0.3598 |
| Recall | 0.0942 |
| F1 | 0.1494 |
| PR-AUC (best) | 0.2518 |

```
              precision    recall  f1-score   support

           0       0.82      0.96      0.88    400897
           1       0.36      0.09      0.15     94508

    accuracy                           0.80    495405
   macro avg       0.59      0.53      0.52    495405
weighted avg       0.73      0.80      0.74    495405

```

---

## Output Files

| File | Description |
|------|-------------|
| `isolation_forest.pkl` | Trained IsolationForest model |
| `session_scores.csv` | Per-session anomaly scores and predictions (495,405 rows) |

---

*Stage 24 completed successfully.*
