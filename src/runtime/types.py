"""Stage 5 — Runtime: result types."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RiskResult:
    """
    Result of a single anomaly-scoring window emitted by InferenceEngine.

    Fields
    ------
    stream_key        : identity of the log stream (service:session_id)
    timestamp         : wall-clock or log timestamp of the last event in the window
    model             : which model produced the score ("baseline"|"transformer"|"ensemble")
    risk_score        : anomaly score (higher = more anomalous; ensemble normalised to ~1.0)
    is_anomaly        : True when risk_score >= threshold
    threshold         : decision threshold used
    evidence_window   : dict with decoded token/template info
    top_predictions   : optional list of top-k next-token predictions (transformer only)
    meta              : free-form extra metadata
    """

    stream_key: str
    timestamp: float | str
    model: str
    risk_score: float
    is_anomaly: bool
    threshold: float
    evidence_window: dict
    top_predictions: Optional[list] = None
    meta: dict = field(default_factory=dict)

    # ------------------------------------------------------------------
    def to_dict(self) -> dict:
        """Serialisable dict (suitable for JSON / CSV)."""
        return {
            "stream_key": self.stream_key,
            "timestamp": self.timestamp,
            "model": self.model,
            "risk_score": self.risk_score,
            "is_anomaly": self.is_anomaly,
            "threshold": self.threshold,
            "evidence_window": self.evidence_window,
            "top_predictions": self.top_predictions,
            "meta": self.meta,
        }
