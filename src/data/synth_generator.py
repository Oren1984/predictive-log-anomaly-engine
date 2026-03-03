"""
src.data.synth_generator — Synthetic log event generator (re-exported).

Re-exports SyntheticLogGenerator from src.synthetic.generator so that
both import paths (src.data and src.synthetic) work interchangeably.
"""
from src.synthetic.generator import SyntheticLogGenerator  # noqa: F401

__all__ = ["SyntheticLogGenerator"]
