"""Sinusoidal wind disturbance for the planar MuJoCo quadrotor."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class SinusoidalWind:
    """World-frame force disturbance applied to x and z generalized forces."""

    x_amplitude: float = 0.85
    z_amplitude: float = 0.38
    x_frequency: float = 0.23
    z_frequency: float = 0.37
    phase: float = 0.6
    downward_bias: float = 0.16

    def force(self, time: float, xz: np.ndarray) -> np.ndarray:
        fx = self.x_amplitude * np.sin(2.0 * np.pi * self.x_frequency * time + self.phase)
        fz = (
            self.z_amplitude * np.sin(2.0 * np.pi * self.z_frequency * time)
            - self.downward_bias
            - 0.08 * xz[0]
        )
        return np.array([fx, fz], dtype=float)

