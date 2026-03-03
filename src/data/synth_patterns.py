"""
src.data.synth_patterns — Failure pattern definitions (re-exported).

This module re-exports all FailurePattern implementations from
src.synthetic.patterns so that code importing from src.data works alongside
code that imports from src.synthetic.
"""
from src.synthetic.patterns import (  # noqa: F401
    AuthBruteForcePattern,
    DiskFullPattern,
    FailurePattern,
    MemoryLeakPattern,
    NetworkFlapPattern,
)

__all__ = [
    "FailurePattern",
    "MemoryLeakPattern",
    "DiskFullPattern",
    "AuthBruteForcePattern",
    "NetworkFlapPattern",
]
