import math
from dataclasses import dataclass

import numpy as np

from examples.rocket_drone_lqr.sim.limits import RocketLimits


@dataclass
class RocketState:
    x: float
    z: float
    theta: float
    vx: float
    vz: float
    omega: float

    def as_vector(self) -> np.ndarray:
        return np.array(
            [self.x, self.z, self.theta, self.vx, self.vz, self.omega],
            dtype=float,
        )

    @staticmethod
    def from_vector(vector: np.ndarray) -> "RocketState":
        return RocketState(
            x=float(vector[0]),
            z=float(vector[1]),
            theta=float(vector[2]),
            vx=float(vector[3]),
            vz=float(vector[4]),
            omega=float(vector[5]),
        )


@dataclass
class RocketForces:
    f1: float
    f2: float
    f3: float

    def clipped(self, limits: RocketLimits) -> "RocketForces":
        return RocketForces(
            f1=float(np.clip(self.f1, limits.f1_min, limits.f1_max)),
            f2=float(np.clip(self.f2, limits.f2_min, limits.f2_max)),
            f3=float(np.clip(self.f3, limits.f3_min, limits.f3_max)),
        )


class RocketDynamics:
    def __init__(self, limits: RocketLimits | None = None):
        self.limits = limits or RocketLimits()
        self.angular_damping = 0.7
        self.side_torque_gain = 0.01

    def derivatives(self, state: RocketState, forces: RocketForces) -> np.ndarray:
        limits = self.limits
        forces = forces.clipped(limits)

        sin_theta = math.sin(state.theta)
        cos_theta = math.cos(state.theta)

        nose_x = -sin_theta
        nose_z = cos_theta

        side_x = cos_theta
        side_z = sin_theta

        main_force = forces.f1

        # F2 толкает влево, F3 толкает вправо.
        side_force = forces.f2 - forces.f3

        torque = (
            self.side_torque_gain * limits.body_half_width * side_force
            - self.angular_damping * state.omega
        )

        fx = main_force * nose_x + side_force * side_x
        fz = main_force * nose_z + side_force * side_z

        ax = fx / limits.mass
        az = fz / limits.mass - limits.gravity
        alpha = torque / limits.inertia

        return np.array(
            [
                state.vx,
                state.vz,
                state.omega,
                ax,
                az,
                alpha,
            ],
            dtype=float,
        )

    def step(self, state: RocketState, forces: RocketForces) -> RocketState:
        dt = self.limits.dt

        y = state.as_vector()
        k1 = self.derivatives(RocketState.from_vector(y), forces)
        k2 = self.derivatives(RocketState.from_vector(y + 0.5 * dt * k1), forces)
        k3 = self.derivatives(RocketState.from_vector(y + 0.5 * dt * k2), forces)
        k4 = self.derivatives(RocketState.from_vector(y + dt * k3), forces)

        new_y = y + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

        new_y[0] = np.clip(new_y[0], self.limits.x_min, self.limits.x_max)
        new_y[1] = np.clip(new_y[1], self.limits.z_min, self.limits.z_max)
        new_y[2] = (new_y[2] + math.pi) % (2.0 * math.pi) - math.pi
        new_y[5] = np.clip(new_y[5], -self.limits.omega_max, self.limits.omega_max)

        return RocketState.from_vector(new_y)