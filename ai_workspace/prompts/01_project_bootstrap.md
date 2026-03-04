## Prompt — Project Bootstrap

## Objective:
Review and document the initial system setup of the Predictive Log Anomaly Engine.

## Scope:
- Dataset selection strategy
- Synthetic log generation
- Project directory structure
- Data schema definition

## Instructions:
1. Describe the purpose of the system:
   Predictive detection of system failures using log sequence modeling.

2. Explain the three data sources:
   - Synthetic logs
   - Public datasets (LogHub / BGL / Kaggle)
   - Chaos-generated logs (optional future stage)

3. Document the unified schema used for log events:
   LogEvent:
   - timestamp
   - service
   - level
   - message
   - metadata
   - label (optional)

4. Describe how raw data is stored in:

data/raw

and synthetic data in:

data/synth

## Expected Output:
A short system bootstrap report describing the data foundation of the project.