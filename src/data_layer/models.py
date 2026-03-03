"""Stage 1 — Data Layer: core domain models."""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class LogEvent:
    """Normalised representation of a single log line."""
    timestamp: Optional[float]
    service: str          # maps to 'dataset' column (hdfs / bgl)
    level: str            # empty string if not available in source
    message: str
    meta: dict = field(default_factory=dict)
    label: Optional[int] = None
