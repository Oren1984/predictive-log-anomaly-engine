# Stage 04B — Transformer Report

**Mode**: demo  **Device**: cpu
**Elapsed**: 2.6s

## Architecture
| Param | Value |
|-------|-------|
| vocab_size | 7836 |
| d_model | 32 |
| n_heads | 2 |
| n_layers | 1 |
| max_seq_len | 128 |
| batch_size | 32 |
| max_epochs | 2 |

## Training History
| Epoch | Train Loss | Val Loss |
|-------|------------|----------|
| 1 | 9.0932 | 8.8977 |
| 2 | 8.7497 | 8.7143 |


## Threshold Calibration
- Threshold: 0.03405
- Val F1: 0.7746

## Test Metrics
- ROC-AUC: 0.6324
- PR-AUC:  0.6485

```
              precision    recall  f1-score   support

      normal       0.83      0.44      0.58        43
     anomaly       0.69      0.93      0.79        57

    accuracy                           0.72       100
   macro avg       0.76      0.69      0.68       100
weighted avg       0.75      0.72      0.70       100

```

## Artifacts
- `models/transformer.pt`
- `artifacts/threshold_transformer.json`
- `reports/metrics_transformer.json`
