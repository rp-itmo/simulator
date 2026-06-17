"""8-figure trajectory in x-z."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class FigureEightTrajectory:
    """A smooth vertical number-8 reference."""

    center_x: float = 0.0
    center_z: float = 4.0
    amp_x: float = 1.15
    amp_z: float = 2.25
    period: float = 12.0

    def sample(self, time: float) -> np.ndarray:
        """Return [x, z, vx, vz, ax, az]."""
        omega = 2.0 * np.pi / self.period
        wt = omega * time

        x = self.center_x + self.amp_x * np.sin(2.0 * wt) / 2.0
        z = self.center_z + self.amp_z * np.sin(wt)

        vx = self.amp_x * omega * np.cos(2.0 * wt)
        vz = self.amp_z * omega * np.cos(wt)

        ax = -2.0 * self.amp_x * omega**2 * np.sin(2.0 * wt)
        az = -self.amp_z * omega**2 * np.sin(wt)

        return np.array([x, z, vx, vz, ax, az], dtype=float)
