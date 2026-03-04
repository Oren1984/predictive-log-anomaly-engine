## Prompt — Modeling System

## Objective:
Document the anomaly detection modeling layer.

## Two model types exist:


Baseline model
Transformer model

## Baseline components:
- BaselineFeatureExtractor
- BaselineAnomalyModel
- ThresholdCalibrator

## Transformer components:
- TransformerConfig
- NextTokenTransformerModel
- Trainer
- AnomalyScorer

## Artifacts produced:

models/baseline.pkl
models/transformer.pt
artifacts/threshold.json
reports/metrics.json

## Expected Output:
Explain how the system learns normal behavior and detects anomalies.