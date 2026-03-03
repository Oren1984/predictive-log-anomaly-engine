SYSTEM ROLE:
Controlled AI engineering agent.

STRICT RULES:
- Only create/modify files inside:
  ai_workspace/stage_23_sequence_builder/
  ai_workspace/reports/
  ai_workspace/logs/
  data/intermediate/
- Do NOT modify previous stages or templates mining outputs.

INPUT:
data/intermediate/events_with_templates.csv

OBJECTIVE (V2):
Build session-level datasets with:
A) ordered template sequences (for DL future)
B) template frequency features (top-N)
C) transition/bigram features (top-M)
D) lightweight sequence stats (entropy, unique ratio)

REQUIRED OUTPUTS:

1) data/intermediate/session_sequences_v2.csv
   Columns:
   - session_id, dataset, label
   - sequence_length
   - ordered_template_sequence (comma-separated template_ids)
   - unique_template_count

2) data/intermediate/session_features_v2.csv
   Must include:
   - session_id, dataset, label
   - sequence_length
   - unique_template_count
   - unique_ratio = unique_template_count / sequence_length
   - template_entropy (Shannon entropy of template_id distribution in session)
   - Top-100 template frequency features (raw + normalized) => 200 cols
   - Top-100 bigram/transition frequency features (raw + normalized) => 200 cols
     Bigram definition: consecutive template ids: "tidA>tidB"

3) Report:
   ai_workspace/reports/stage_23_sequence_report_v2.md
   Include:
   - Total sessions
   - Avg/median/max sequence length
   - Label distribution (session level)
   - Dataset distribution
   - Top 10 longest sessions
   - #unique templates, #unique bigrams (global)
   - Which top-100 templates selected + top-20 shown
   - Which top-100 bigrams selected + top-20 shown
   - Execution time + peak memory

4) Log:
   ai_workspace/logs/stage_23_sequence_v2.log

5) Script:
   ai_workspace/stage_23_sequence_builder/run_sequence_builder_v2.py

IMPLEMENTATION NOTES:
- Preserve event order within session (use original row order if no timestamp).
- Efficient approach allowed:
  - Build ordered sequences per session once
  - Extract global bigram counts across sessions
  - Select top-100 bigrams
  - Build feature matrix
- Deterministic behavior (seed=42 if randomness used).
- Use pandas/numpy + standard library (collections.Counter).
- No notebook.

FINAL:
Print: "Stage 23 (v2) completed successfully."
List generated files.
DO NOT proceed to Stage 24.