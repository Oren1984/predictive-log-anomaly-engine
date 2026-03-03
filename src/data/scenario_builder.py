"""
src.data.scenario_builder — Scenario definition builder (re-exported).

Re-exports ScenarioBuilder from src.synthetic.scenario_builder so that
both import paths (src.data and src.synthetic) work interchangeably.
"""
from src.synthetic.scenario_builder import ScenarioBuilder  # noqa: F401

__all__ = ["ScenarioBuilder"]
