import math
from dataclasses import dataclass


@dataclass
class TrajectoryPoint:
    x: float
    z: float
    vx: float
    vz: float
    ax: float
    az: float
    theta: float


class FigureEightTrajectory:
    def __init__(
        self,
        center_x: float = 0.0,
        center_z: float = 4.0,
        amplitude_x: float = 3.0,
        amplitude_z: float = 1.4,
        period: float = 70.0,
    ):
        self.center_x = center_x
        self.center_z = center_z
        self.amplitude_x = amplitude_x
        self.amplitude_z = amplitude_z
        self.omega = 2.0 * math.pi / period

    def get(self, t: float) -> TrajectoryPoint:
        s = self.omega * t

        x = self.center_x + self.amplitude_x * math.sin(s)
        z = self.center_z + self.amplitude_z * math.sin(2.0 * s)

        vx = self.amplitude_x * self.omega * math.cos(s)
        vz = 2.0 * self.amplitude_z * self.omega * math.cos(2.0 * s)

        ax = -self.amplitude_x * self.omega**2 * math.sin(s)
        az = -4.0 * self.amplitude_z * self.omega**2 * math.sin(2.0 * s)

        theta = 0.0

        return TrajectoryPoint(x=x, z=z, vx=vx, vz=vz, ax=ax, az=az, theta=theta)