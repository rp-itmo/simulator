"""Small metric accumulator for tracking performance."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class TrackingMetrics:
    errors: list[float] = field(default_factory=list)
    max_abs_x: float = 0.0
    min_z: float = 1e9
    max_z: float = -1e9

    def update(self, state: np.ndarray, reference: np.ndarray) -> None:
        xz = state[:2]
        self.errors.append(float(np.linalg.norm(reference[:2] - xz)))
        self.max_abs_x = max(self.max_abs_x, abs(float(xz[0])))
        self.min_z = min(self.min_z, float(xz[1]))
        self.max_z = max(self.max_z, float(xz[1]))

    def summary(self) -> dict[str, float]:
        return {
            "mean_tracking_error": float(np.mean(self.errors)),
            "max_tracking_error": float(np.max(self.errors)),
            "max_abs_x": self.max_abs_x,
            "min_z": self.min_z,
            "max_z": self.max_z,
        }

