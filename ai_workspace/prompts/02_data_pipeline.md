## Prompt — Data Pipeline

## Objective:
Document the data ingestion and normalization layer.

## Components:
- KaggleDatasetLoader
- SyntheticLogGenerator
- ScenarioBuilder
- LogEvent dataclass

## Instructions:
Explain how raw logs are collected and normalized.

Document the following processes:

1. Dataset ingestion
2. Schema normalization
3. Synthetic event generation
4. Scenario building (normal → degradation → failure)

## Outputs produced:

data/raw/
data/synth/
data/processed/events.parquet
schema.md

## Expected Output:
A description of the complete data ingestion pipeline.