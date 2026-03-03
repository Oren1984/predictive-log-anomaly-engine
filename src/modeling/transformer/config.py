"""Stage 4B — Transformer: configuration dataclass."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass
class TransformerConfig:
    """
    Hyper-parameters for the next-token transformer.

    All defaults are chosen to be CPU-trainable on a laptop
    within a few minutes on a ~500K-session dataset.
    """
    # Architecture
    vocab_size: int = 7835          # len(templates) + 2 (PAD + UNK)
    d_model: int = 64               # embedding dimension
    n_heads: int = 4                # attention heads (d_model // n_heads = 16)
    n_layers: int = 2               # TransformerEncoder layers
    d_ff: int = 128                 # feed-forward hidden size
    max_seq_len: int = 512          # maximum context length
    dropout: float = 0.1

    # Training
    batch_size: int = 64
    max_epochs: int = 5
    learning_rate: float = 3e-4
    weight_decay: float = 1e-2
    patience: int = 3               # early-stopping patience (val-loss)
    pad_id: int = 0

    # Scoring
    score_reduction: str = "mean"   # "mean" | "max" over per-token NLL

    # ------------------------------------------------------------------
    def save(self, path: Path | str) -> None:
        Path(path).write_text(json.dumps(asdict(self), indent=2))

    @classmethod
    def load(cls, path: Path | str) -> "TransformerConfig":
        data = json.loads(Path(path).read_text())
        return cls(**data)
