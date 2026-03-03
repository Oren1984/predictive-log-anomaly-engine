"""Stage 4A — Baseline: feature extractor from Sequence objects."""
from __future__ import annotations

from collections import Counter
from typing import Optional

import numpy as np

from ...sequencing.models import Sequence


class BaselineFeatureExtractor:
    """
    Converts a list of Sequence objects into a 2-D numpy feature matrix.

    Features per sequence (mirrors session_features_v2.csv):
        * sequence_length      — number of tokens
        * unique_count         — distinct token IDs
        * unique_ratio         — unique_count / sequence_length (0 if len=0)
        * template_entropy     — Shannon entropy over token distribution
        * tid_raw_{tid}        — raw count of each token in top-K vocab
        * tid_norm_{tid}       — count / length (normalised)

    The vocabulary (top-K token IDs by corpus frequency) is fitted on
    the training set and fixed for val/test.

    Parameters
    ----------
    top_k : number of token-frequency features to include (default 100)
    """

    def __init__(self, top_k: int = 100):
        self.top_k = top_k
        self._vocab: list[int] = []          # fitted token IDs
        self._vocab_set: set[int] = set()
        self._feature_names: list[str] = []
        self._fitted = False

    # ------------------------------------------------------------------
    def fit(self, sequences: list[Sequence]) -> "BaselineFeatureExtractor":
        """Fit vocabulary from training sequences."""
        counter: Counter = Counter()
        for seq in sequences:
            counter.update(seq.tokens)
        self._vocab = [tid for tid, _ in counter.most_common(self.top_k)]
        self._vocab_set = set(self._vocab)
        self._feature_names = (
            ["sequence_length", "unique_count", "unique_ratio", "template_entropy"]
            + [f"tid_raw_{t}" for t in self._vocab]
            + [f"tid_norm_{t}" for t in self._vocab]
        )
        self._fitted = True
        return self

    # ------------------------------------------------------------------
    def transform(self, sequences: list[Sequence]) -> np.ndarray:
        """Return (n_sequences, n_features) float32 array."""
        if not self._fitted:
            raise RuntimeError("Call fit() before transform().")
        rows = [self._extract(seq) for seq in sequences]
        return np.array(rows, dtype=np.float32)

    def fit_transform(self, sequences: list[Sequence]) -> np.ndarray:
        return self.fit(sequences).transform(sequences)

    # ------------------------------------------------------------------
    def _extract(self, seq: Sequence) -> list[float]:
        tokens = seq.tokens
        n = len(tokens)
        counter = Counter(tokens)
        unique = len(counter)

        # Shannon entropy
        entropy = 0.0
        if n > 0:
            for cnt in counter.values():
                p = cnt / n
                entropy -= p * np.log2(p + 1e-12)

        scalar = [float(n), float(unique),
                  float(unique / n) if n else 0.0,
                  entropy]

        raw   = [float(counter.get(t, 0)) for t in self._vocab]
        normed = [float(counter.get(t, 0) / n) if n else 0.0
                  for t in self._vocab]
        return scalar + raw + normed

    # ------------------------------------------------------------------
    @property
    def feature_names(self) -> list[str]:
        return self._feature_names

    @property
    def n_features(self) -> int:
        return len(self._feature_names)
