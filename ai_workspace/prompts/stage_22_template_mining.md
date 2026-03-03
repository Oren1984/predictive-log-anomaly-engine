SYSTEM ROLE:
Controlled AI engineering agent.

STRICT RULES:
- Work ONLY inside:
  ai_workspace/stage_22_template_mining/
  ai_workspace/reports/
  ai_workspace/logs/
  data/intermediate/
- Do NOT modify other stages.

INPUT:
data/processed/events_sample_1m.csv

OBJECTIVE:
Implement lightweight Drain-style log template miner.

TASKS:
1) Parse message column.
2) Replace dynamic tokens:
   - numbers
   - IP addresses
   - block IDs
3) Generate:
   - template_id
   - template_text
4) Save:
   data/intermediate/events_with_templates.csv
5) Save template dictionary:
   data/intermediate/templates.csv

REPORT:
ai_workspace/reports/stage_22_template_report.md

Include:
- Unique templates count
- Top 20 templates
- Template frequency distribution
- Execution time

Script path:
ai_workspace/stage_22_template_mining/run_template_mining.py

FINAL:
Print: "Stage 22 completed successfully."