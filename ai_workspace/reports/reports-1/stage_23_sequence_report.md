# Stage 23 Sequence Builder Report

**Generated:** 2026-03-03  
**Execution time:** 51.6s  
**Peak memory:** 710.8 MB  

---

## Summary

| Metric | Value |
|--------|------:|
| Total sessions | 495,405 |
| Avg sequence length | 2.02 |
| Median sequence length | 2.0 |
| Max sequence length | 34 |
| Template vocabulary size | 7,833 |
| Feature columns (top-N raw+norm) | 200 |
| Total elapsed | 51.6s |
| Peak memory | 710.8 MB |

---

## Label Distribution (session level)

| Label | Sessions | Pct |
|------:|---------:|----:|
| 0 | 400,897 | 80.92% |
| 1 | 94,508 | 19.08% |

---

## Dataset Distribution

| Dataset | Sessions | Pct |
|---------|--------:|----:|
| hdfs | 404,179 | 81.59% |
| bgl | 91,226 | 18.41% |

---

## Top 10 Longest Sessions

| session_id | dataset | label | sequence_length |
|------------|---------|------:|----------------:|
| blk_-2891794341254261063 | hdfs | 1 | 34 |
| blk_-5224041993350565248 | hdfs | 0 | 24 |
| blk_2866275036574950116 | hdfs | 0 | 24 |
| blk_-8333455052087360327 | hdfs | 0 | 22 |
| blk_-5375761801379702192 | hdfs | 1 | 20 |
| blk_5762192118127023083 | hdfs | 0 | 20 |
| blk_-6954586533193620247 | hdfs | 0 | 20 |
| blk_-7288708571822700018 | hdfs | 0 | 18 |
| blk_-442823578746301707 | hdfs | 0 | 18 |
| blk_-1016453873803095686 | hdfs | 0 | 18 |

---

## Output Files

| File | Shape |
|------|-------|
| `session_sequences.csv` | 495,405 rows x 6 cols |
| `session_features.csv`  | 495,405 rows x 204 cols |

---

*Stage 23 completed successfully.*
