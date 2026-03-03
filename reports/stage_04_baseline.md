# Stage 04A — Baseline Report

**Mode**: demo
**Elapsed**: 0.9s

## Dataset
| Split | N |
|-------|---|
| train | 1600 |
| val   | 200 |
| test  | 200 |

## Features
- Dimensions: 204
- Top-K: 100 template frequency features

## Threshold Calibration (val set)
- Threshold: 0.33032
- Val F1: 0.4605

## Test Metrics
- ROC-AUC: 0.5327
- PR-AUC: 0.3117

```
              precision    recall  f1-score   support

      normal       0.78      0.52      0.63       143
     anomaly       0.35      0.63      0.45        57

    accuracy                           0.56       200
   macro avg       0.56      0.58      0.54       200
weighted avg       0.66      0.56      0.58       200

```

## Artifacts
- `models/baseline.pkl`
- `artifacts/threshold.json`
