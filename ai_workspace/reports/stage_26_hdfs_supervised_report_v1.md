# Stage 26 HDFS Supervised Baseline Report

**Generated:** 2026-03-03  
**Execution time:** 21.3s  
**Peak memory:** 4344.4 MB  

---

## Dataset

| Split | Rows | Anomalies | Anomaly Rate |
|-------|-----:|----------:|-------------:|
| Train | 323,343 | 7,592 | 2.35% |
| Val   | 40,418   | 949   | 2.35% |
| Test  | 40,418  | 949  | 2.35% |
| **Total HDFS** | 404,179 | 9,490 | 2.35% |

---

## Model

| Parameter | Value |
|-----------|-------|
| Algorithm | LogisticRegression |
| Scaler | StandardScaler (fit on train) |
| max_iter | 2000 |
| class_weight | balanced |
| Features | 404 numeric cols |
| Best F1 threshold (from val) | 0.71259 |

---

## Validation Metrics

| Threshold | ROC AUC | PR AUC | Precision | Recall | F1 | Pred Anom% |
|-----------|--------:|-------:|----------:|-------:|---:|-----------:|
| 0.5 | 0.6604 | 0.2334 | 0.0487 | 0.4752 | 0.0884 | 22.90% |
| bestF1=0.7126 | 0.6604 | 0.2334 | 0.5000 | 0.2181 | 0.3037 | 1.02% |

---

## Test Metrics

| Threshold | ROC AUC | PR AUC | Precision | Recall | F1 | Pred Anom% |
|-----------|--------:|-------:|----------:|-------:|---:|-----------:|
| 0.5 | 0.6624 | 0.1864 | 0.0475 | 0.4594 | 0.0862 | 22.69% |
| bestF1=0.7126 | 0.6624 | 0.1864 | 0.4261 | 0.1791 | 0.2522 | 0.99% |

---

## Confusion Matrices (test set)

**Threshold = 0.5**

| | Pred Normal | Pred Anomaly |
|---|---:|---:|
| **Actual Normal**  | 30,733 (TN) | 8,736 (FP) |
| **Actual Anomaly** | 513 (FN) | 436 (TP) |

**Threshold = bestF1 (0.71259)**

| | Pred Normal | Pred Anomaly |
|---|---:|---:|
| **Actual Normal**  | 39,240 (TN) | 229 (FP) |
| **Actual Anomaly** | 779 (FN) | 170 (TP) |

---

## Generated Plots

| Plot | File |
|------|------|
| ROC Curve | `ai_workspace/stage_26_hdfs_supervised/roc_curve_hdfs_v1.png` |
| PR Curve  | `ai_workspace/stage_26_hdfs_supervised/pr_curve_hdfs_v1.png` |
| Confusion | `ai_workspace/stage_26_hdfs_supervised/confusion_hdfs_v1.png` |

---

*Stage 26 (HDFS supervised) completed successfully.*
