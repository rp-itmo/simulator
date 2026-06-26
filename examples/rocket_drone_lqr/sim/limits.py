from dataclasses import dataclass


@dataclass(frozen=True)
class RocketLimits:
    dt: float = 0.02

    mass: float = 1.0
    inertia: float = 0.08
    gravity: float = 9.81

    body_half_width: float = 0.25

    f1_min: float = 0.0
    f1_max: float = 18.0

    f2_min: float = 0.0
    f2_max: float = 10.0

    f3_min: float = 0.0
    f3_max: float = 10.0

    x_min: float = -8.0
    x_max: float = 8.0
    z_min: float = 0.0
    z_max: float = 8.0

    omega_max: float = 12.0