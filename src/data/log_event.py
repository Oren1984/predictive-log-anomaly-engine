"""
src.data.log_event — Core LogEvent dataclass with IO helpers.

This module provides the canonical LogEvent type used by the synthetic pipeline.
It is compatible with src.data_layer.models.LogEvent (same fields) and adds
parquet-friendly to_dict() / from_dict() serialisation helpers.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Union


@dataclass
class LogEvent:
    """
    Normalised representation of a single log line.

    Fields
    ------
    timestamp : Unix timestamp (float) or datetime.  Stored as float internally.
    service   : Service / dataset name (e.g. "auth", "api", "billing", "db").
    level     : Log level string ("INFO", "WARNING", "ERROR", …).
    message   : Raw log message text.
    meta      : Arbitrary key/value metadata dict (host, component, phase, …).
    label     : Anomaly label.  0 = normal, 1 = anomalous.  None = unknown.
    """

    timestamp: Union[float, datetime]
    service:   str
    level:     str
    message:   str
    meta:      dict = field(default_factory=dict)
    label:     Optional[int] = None

    # ------------------------------------------------------------------
    # Serialisation helpers
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """
        Return a JSON-serialisable dict suitable for writing to parquet.

        The ``meta`` field is JSON-encoded to a string so it survives
        round-trips through parquet without requiring nested-type support.
        """
        ts = self.timestamp
        if isinstance(ts, datetime):
            ts = ts.timestamp()
        return {
            "timestamp": float(ts) if ts is not None else None,
            "service":   self.service,
            "level":     self.level,
            "message":   self.message,
            "meta":      json.dumps(self.meta or {}),
            "label":     int(self.label) if self.label is not None else None,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "LogEvent":
        """
        Reconstruct a LogEvent from a dict produced by to_dict().

        ``meta`` may be a JSON string (from parquet) or already a dict.
        """
        meta_raw = d.get("meta", "{}")
        if isinstance(meta_raw, str):
            try:
                meta = json.loads(meta_raw)
            except (json.JSONDecodeError, TypeError):
                meta = {}
        elif isinstance(meta_raw, dict):
            meta = meta_raw
        else:
            meta = {}

        lbl = d.get("label")
        return cls(
            timestamp=float(d["timestamp"]) if d.get("timestamp") is not None else None,
            service=str(d.get("service", "")),
            level=str(d.get("level", "")),
            message=str(d.get("message", "")),
            meta=meta,
            label=int(lbl) if lbl is not None else None,
        )

    # ------------------------------------------------------------------
    # Convenience
    # ------------------------------------------------------------------

    def timestamp_as_datetime(self) -> Optional[datetime]:
        """Return the timestamp as a UTC-aware datetime, or None."""
        if self.timestamp is None:
            return None
        ts = self.timestamp
        if isinstance(ts, datetime):
            return ts.astimezone(timezone.utc)
        return datetime.fromtimestamp(float(ts), tz=timezone.utc)
