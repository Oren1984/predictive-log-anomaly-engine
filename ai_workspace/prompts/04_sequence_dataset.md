## Prompt — Sequence Dataset Builder

## Objective:
Describe how tokenized events are converted into sequences for model training.

## Components:
- Sequence dataclass
- SequenceBuilder
- SlidingWindowSequenceBuilder
- DatasetSplitter

## Process:
1. Convert events into token streams
2. Build sliding windows
3. Create labeled sequences
4. Split datasets into:

train
validation
test

## Outputs:

processed/sequences_train.parquet
processed/sequences_val.parquet
processed/sequences_test.parquet

## Expected Output:
A description of how sequential datasets are prepared for machine learning.