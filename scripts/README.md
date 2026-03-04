# Scripts

This directory contains executable pipeline scripts used to run
different stages of the anomaly detection system.

Scripts are organized by stage number and represent the system workflow.


## Examples:

- 10_download_data.py      → download datasets
- 20_prepare_events.py     → parse raw logs into structured events
- 30_build_sequences.py    → generate event sequences
- 40_train_baseline.py     → train baseline model
- 50_run_api.py            → start the API service

These scripts can be executed individually or as part of a full pipeline run.