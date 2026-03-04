## Prompt — Template Mining

## Objective:
Explain how the system learns the "language of logs".

## Components:
- LogParser
- TemplateMiner
- EventTokenizer

## Process:
1. Parse raw logs
2. Extract log templates
3. Convert templates to token IDs
4. Build vocabulary

## Artifacts:

artifacts/templates.json
artifacts/vocab.json
processed/events_tokenized.parquet

## Expected Output:
A clear explanation of how logs become structured tokens used for modeling.