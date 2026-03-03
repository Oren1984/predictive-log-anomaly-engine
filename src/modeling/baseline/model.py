"""Stage 4A — Baseline: IsolationForest anomaly model wrapper."""
from __future__ import annotations

import pickle
from pathlib import Path
from typing import Optional

import numpy as np
from sklearn.ensemble import IsolationForest


class BaselineAnomalyModel:
    """
    Thin wrapper around sklearn IsolationForest for anomaly detection.

    Anomaly score convention: higher = more anomalous.
    (IsolationForest's score_samples() returns lower values for anomalies;
    we negate so the caller always uses higher-is-worse semantics.)

    Parameters
    ----------
    n_estimators : number of trees (default 300)
    random_state : reproducibility seed (default 42)
    """

    def __init__(self, n_estimators: int = 300, random_state: int = 42):
        self._model = IsolationForest(
            n_estimators=n_estimators,
            random_state=random_state,
        )
        self._fitted = False

    # ------------------------------------------------------------------
    def fit(self, X: np.ndarray) -> "BaselineAnomalyModel":
        """Fit the IsolationForest on feature matrix X."""
        self._model.fit(X)
        self._fitted = True
        return self

    def score(self, X: np.ndarray) -> np.ndarray:
        """
        Return anomaly scores (float32 array, shape [n]).
        Higher = more anomalous.
        """
        if not self._fitted:
            raise RuntimeError("Call fit() before score().")
        return (-self._model.score_samples(X)).astype(np.float32)

    def predict(self, X: np.ndarray, threshold: float) -> np.ndarray:
        """Return int8 predictions (1=anomaly) using given threshold."""
        scores = self.score(X)
        return (scores >= threshold).astype(np.int8)

    # ------------------------------------------------------------------
    def save(self, path: Path | str) -> None:
        with open(path, "wb") as f:
            pickle.dump(self._model, f)

    @classmethod
    def load(cls, path: Path | str) -> "BaselineAnomalyModel":
        obj = cls.__new__(cls)
        with open(path, "rb") as f:
            obj._model = pickle.load(f)
        obj._fitted = True
        return obj
