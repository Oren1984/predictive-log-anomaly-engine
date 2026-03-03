"""Stage 3 — Sequencing: core domain model."""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Sequence:
    """A single labelled event sequence represented as token IDs."""
    sequence_id: str
    tokens: list[int]
    timestamps: list = field(default_factory=list)
    label: Optional[int] = None

    # ------------------------------------------------------------------
    def __len__(self) -> int:
        return len(self.tokens)

    def __repr__(self) -> str:
        return (f"Sequence(id={self.sequence_id!r}, "
                f"len={len(self.tokens)}, label={self.label})")
