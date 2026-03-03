"""Stage 4B — Transformer: GPT-style causal next-token model."""
from __future__ import annotations

import math
from pathlib import Path
from typing import Optional

import torch
import torch.nn as nn

from .config import TransformerConfig


class _PositionalEncoding(nn.Module):
    """Fixed sinusoidal positional encoding."""

    def __init__(self, d_model: int, max_len: int, dropout: float):
        super().__init__()
        self.dropout = nn.Dropout(dropout)
        pe = torch.zeros(max_len, d_model)
        pos = torch.arange(max_len).unsqueeze(1).float()
        div = torch.exp(
            torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)
        )
        pe[:, 0::2] = torch.sin(pos * div)
        pe[:, 1::2] = torch.cos(pos * div)
        self.register_buffer("pe", pe.unsqueeze(0))  # (1, max_len, d_model)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (B, T, d_model)
        x = x + self.pe[:, : x.size(1)]
        return self.dropout(x)


class NextTokenTransformerModel(nn.Module):
    """
    Causal (decoder-only) transformer that predicts next token.

    Input  : token IDs  (B, T)
    Output : logits     (B, T, vocab_size)

    PAD tokens (id=0) are masked in the key-padding mask so they
    do not influence attention.
    """

    def __init__(self, cfg: TransformerConfig):
        super().__init__()
        self.cfg = cfg
        self.embedding = nn.Embedding(cfg.vocab_size, cfg.d_model,
                                      padding_idx=cfg.pad_id)
        self.pos_enc = _PositionalEncoding(cfg.d_model, cfg.max_seq_len,
                                           cfg.dropout)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=cfg.d_model,
            nhead=cfg.n_heads,
            dim_feedforward=cfg.d_ff,
            dropout=cfg.dropout,
            batch_first=True,
        )
        self.encoder = nn.TransformerEncoder(encoder_layer,
                                             num_layers=cfg.n_layers)
        self.fc_out = nn.Linear(cfg.d_model, cfg.vocab_size)

    # ------------------------------------------------------------------
    def _causal_mask(self, size: int, device: torch.device) -> torch.Tensor:
        """Upper-triangular mask (True = masked out)."""
        mask = torch.triu(torch.ones(size, size, device=device), diagonal=1)
        return mask.bool()

    def forward(
        self,
        input_ids: torch.Tensor,          # (B, T)
        key_padding_mask: Optional[torch.Tensor] = None,  # (B, T)
    ) -> torch.Tensor:                    # (B, T, vocab_size)
        T = input_ids.size(1)
        causal = self._causal_mask(T, input_ids.device)
        x = self.embedding(input_ids)     # (B, T, d_model)
        x = self.pos_enc(x)
        x = self.encoder(
            x,
            mask=causal,
            src_key_padding_mask=key_padding_mask,
            is_causal=True,
        )
        return self.fc_out(x)             # (B, T, vocab_size)

    # ------------------------------------------------------------------
    def save(self, path: Path | str) -> None:
        torch.save({"state_dict": self.state_dict(),
                    "cfg": self.cfg}, path)

    @classmethod
    def load(cls, path: Path | str,
             map_location: str = "cpu") -> "NextTokenTransformerModel":
        from .config import TransformerConfig as _TC
        with torch.serialization.safe_globals([_TC]):
            ckpt = torch.load(path, map_location=map_location,
                              weights_only=True)
        model = cls(ckpt["cfg"])
        model.load_state_dict(ckpt["state_dict"])
        return model
