YOU ARE WORKING INSIDE THIS REPO:
C:\Users\ORENS\predictive-log-anomaly-engine

MODE: EXECUTION (audit + report only). Do NOT implement anything.

OBJECTIVE:
Produce ONE markdown report file that audits the current repo state and confirms what is closed/completed up to Stage 5 (inclusive).

NON-NEGOTIABLE:
- Do NOT modify code, tests, configs, or docs (report file only).
- Do NOT rename/move files.
- Use only repo facts (read files + list directories). No assumptions.
- Keep report concise but complete.

OUTPUT:
Create/overwrite this file ONLY:
reports/stage_05_system_audit_report.md

WHAT TO INCLUDE IN THE REPORT (strict structure):

1) Repo Snapshot
- Current timestamp (local time)
- Git status summary (clean/dirty; list changed files if any)
- Python version detected (if available)
- OS note: Windows

2) Stage Closure Summary (Stages 0–5)
For each stage (0,1,2,3,4,5) include a table row:
- Stage ID + Name
- Purpose (1 line)
- Entry script(s) (path)
- Key inputs (paths)
- Key outputs/artifacts (paths)
- Evidence of completion (existing report/log/artifact file)
- Status: PASS/UNKNOWN (PASS only if evidence exists)

3) Artifacts Inventory (by folder)
List the important files found in:
- artifacts/
- models/
- reports/
- data/synth/ (if exists)
- data/processed/ (only list the main parquet files, do not dump huge outputs)
For each folder: show file name, size, last modified time.

4) Verification Evidence
Run and record results (do not skip):
- pytest -q  (must show pass count and duration)
If a script is safe and fast, also run:
- python scripts/stage_05_runtime_demo.py --mode demo --model ensemble --n-events 50000
ONLY if it is known to complete fast; otherwise state "not executed" and why.

5) Known Gaps / Risks (only from evidence)
- List only concrete gaps found (missing files, empty files like 0 bytes, inconsistent names).
- Do NOT propose big refactors. Minimal notes only.

6) Exact PowerShell Commands (copy-paste)
Include the exact commands you ran for verification.

IMPLEMENTATION INSTRUCTIONS:
- Start by listing:
  scripts/ , src/ , tests/ , artifacts/ , models/ , reports/ , data/ (if exists)
- Read existing stage reports under reports/ (stage_04_*.md, stage_05_*.md, stage_27_*.md, stage_28_*.md, stage_31_*.md if relevant) to extract facts.
- Use the repo as source of truth.
- Produce the report and stop.

BEGIN NOW.