## Prompt — Runtime Inference Engine

## Objective:
Describe how the trained model operates in real time.

## Components:
- SequenceBuffer
- InferenceEngine
- RiskResult dataclass

## Runtime process:

1. Logs are ingested continuously
2. Rolling sequences are built
3. Model predictions are generated
4. Risk score is calculated

## RiskResult fields:

- `risk_score`: The calculated risk score for the current sequence.
- `is_anomaly`: Boolean indicating if the sequence is anomalous.
- `top_predictions`: The top predicted events for the sequence.
- `evidence_window`: The window of events used to generate the risk score.

## Expected Output:
Explain how the system performs real-time anomaly detection.