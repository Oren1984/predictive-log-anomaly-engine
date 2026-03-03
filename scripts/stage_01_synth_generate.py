"""
Stage 01 — Synthetic: generate synthetic log events.

Builds 4 single-pattern scenarios + 1 hybrid scenario and writes:
  data/synth/events_synth.csv
  data/synth/events_synth.parquet
  data/synth/scenarios.json

Logs to: ai_workspace/logs/stage_01_synth_generate.log

Usage:
    python scripts/stage_01_synth_generate.py --mode demo
    python scripts/stage_01_synth_generate.py --mode full --events 200000
    python scripts/stage_01_synth_generate.py --mode demo --seed 123
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import pandas as pd

from src.synthetic import (
    AuthBruteForcePattern,
    DiskFullPattern,
    MemoryLeakPattern,
    NetworkFlapPattern,
    ScenarioBuilder,
    SyntheticLogGenerator,
)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
LOG_DIR  = ROOT / "ai_workspace" / "logs"
OUT_DIR  = ROOT / "data" / "synth"
LOG_DIR.mkdir(parents=True, exist_ok=True)
OUT_DIR.mkdir(parents=True, exist_ok=True)

_log_path = LOG_DIR / "stage_01_synth_generate.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(_log_path, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)

# Fixed epoch for reproducible timestamps (2024-01-01 00:00:00 UTC)
_BASE_TS = 1_704_067_200.0

# Phase split used by all scenarios
_DEFAULT_PHASES = {"normal": 0.60, "degradation": 0.30, "failure": 0.10}


# ---------------------------------------------------------------------------
# Scenario definitions
# ---------------------------------------------------------------------------

def _build_scenarios(n_total: int, seed: int) -> list[dict]:
    """Return a list of 5 scenario dicts (4 single-pattern + 1 hybrid)."""
    builder = ScenarioBuilder()

    # Distribute events: 4 equal single-pattern + hybrid gets remainder
    n_each   = n_total // 5
    n_hybrid = n_total - 4 * n_each

    STEP = 3600  # seconds between scenario start times (1 hour apart)

    scenarios = [
        builder.build_scenario(
            scenario_id  = "mem_leak_001",
            service      = "app-server",
            host         = "host-01",
            start_ts     = _BASE_TS,
            n_events     = n_each,
            phases       = dict(_DEFAULT_PHASES),
            pattern_name = "memory_leak",
        ),
        builder.build_scenario(
            scenario_id  = "disk_full_001",
            service      = "storage",
            host         = "host-02",
            start_ts     = _BASE_TS + STEP,
            n_events     = n_each,
            phases       = dict(_DEFAULT_PHASES),
            pattern_name = "disk_full",
        ),
        builder.build_scenario(
            scenario_id  = "auth_brute_001",
            service      = "auth-service",
            host         = "host-03",
            start_ts     = _BASE_TS + 2 * STEP,
            n_events     = n_each,
            phases       = dict(_DEFAULT_PHASES),
            pattern_name = "auth_brute_force",
        ),
        builder.build_scenario(
            scenario_id  = "net_flap_001",
            service      = "network",
            host         = "host-04",
            start_ts     = _BASE_TS + 3 * STEP,
            n_events     = n_each,
            phases       = dict(_DEFAULT_PHASES),
            pattern_name = "network_flap",
        ),
        builder.build_hybrid_scenario(
            scenario_id   = "hybrid_001",
            service       = "hybrid-svc",
            host          = "host-05",
            start_ts      = _BASE_TS + 4 * STEP,
            n_events      = n_hybrid,
            pattern_names = [
                "memory_leak",
                "disk_full",
                "auth_brute_force",
                "network_flap",
            ],
            phases        = {"normal": 0.50, "degradation": 0.35, "failure": 0.15},
        ),
    ]
    return scenarios


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_generate(mode: str, seed: int, n_events: int, outdir: Path) -> dict:
    log.info("=== Stage 01 Synthetic Generate ===")
    log.info("mode=%s  seed=%d  n_events=%d  outdir=%s", mode, seed, n_events, outdir)

    t_start = time.perf_counter()
    outdir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Build scenarios and generator
    # ------------------------------------------------------------------
    scenarios = _build_scenarios(n_events, seed)
    log.info("Built %d scenarios", len(scenarios))
    for sc in scenarios:
        log.info("  %s: pattern=%s  n=%d  anomaly_rate=%.1f%%",
                 sc["scenario_id"],
                 sc.get("pattern_name", sc.get("pattern_names")),
                 sc["n_events"],
                 sc["anomaly_rate"] * 100)

    generator = SyntheticLogGenerator(
        patterns=[
            MemoryLeakPattern(),
            DiskFullPattern(),
            AuthBruteForcePattern(),
            NetworkFlapPattern(),
        ],
        seed=seed,
    )

    # ------------------------------------------------------------------
    # Generate events
    # ------------------------------------------------------------------
    log.info("Generating events ...")
    events = generator.generate_all(scenarios)
    log.info("Generated %d total events", len(events))

    df = SyntheticLogGenerator.events_to_dataframe(events)
    log.info("DataFrame shape: %s", df.shape)

    # ------------------------------------------------------------------
    # Label / phase statistics
    # ------------------------------------------------------------------
    label_counts = df["label"].value_counts().sort_index().to_dict()
    phase_counts = df["phase"].value_counts().to_dict()
    anomaly_rate = float(df["label"].mean() * 100)

    log.info("Label distribution: %s", label_counts)
    log.info("Phase distribution:  %s", phase_counts)
    log.info("Anomaly rate: %.2f%%", anomaly_rate)

    # ------------------------------------------------------------------
    # Write outputs
    # ------------------------------------------------------------------
    csv_path     = outdir / "events_synth.csv"
    parquet_path = outdir / "events_synth.parquet"
    scen_path    = outdir / "scenarios.json"

    df.to_csv(csv_path, index=False)
    log.info("CSV written: %s (%d rows)", csv_path, len(df))

    try:
        df.to_parquet(parquet_path, index=False)
        log.info("Parquet written: %s", parquet_path)
        parquet_ok = True
    except Exception as exc:
        log.warning("Parquet write failed (non-fatal): %s", exc)
        parquet_ok = False

    # Scenarios JSON (strip non-serialisable fields for clean output)
    sc_records = []
    for sc in scenarios:
        rec = {k: v for k, v in sc.items() if k != "rng"}
        sc_records.append(rec)
    with open(scen_path, "w", encoding="utf-8") as fh:
        json.dump(sc_records, fh, indent=2)
    log.info("Scenarios JSON written: %s", scen_path)

    elapsed = time.perf_counter() - t_start
    summary = {
        "n_events":       len(df),
        "n_scenarios":    len(scenarios),
        "label_counts":   label_counts,
        "phase_counts":   phase_counts,
        "anomaly_rate":   round(anomaly_rate, 2),
        "csv_path":       str(csv_path),
        "parquet_ok":     parquet_ok,
        "elapsed_s":      round(elapsed, 2),
        "seed":           seed,
        "mode":           mode,
    }

    log.info("--- Summary ---")
    for k, v in summary.items():
        log.info("  %s: %s", k, v)
    log.info("=== Stage 01 Synthetic Generate complete in %.2fs ===", elapsed)

    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Stage 01 Synthetic Generate")
    parser.add_argument("--mode",    default="demo", choices=["demo", "full"])
    parser.add_argument("--seed",    type=int, default=42)
    parser.add_argument("--events",  type=int, default=None,
                        help="Override default event count")
    parser.add_argument("--outdir",  type=Path, default=ROOT / "data" / "synth")
    args = parser.parse_args()

    n_events = args.events
    if n_events is None:
        n_events = 20_000 if args.mode == "demo" else 200_000

    run_generate(args.mode, args.seed, n_events, args.outdir)


if __name__ == "__main__":
    main()
