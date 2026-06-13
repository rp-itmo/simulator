"""MPC-style controller for the MuJoCo 2D quadrotor."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class MPCConfig:
    """Controller parameters."""

    mass_estimate: float = 1.2
    gravity: float = 9.81
    horizon_steps: int = 18
    dt: float = 0.005
    max_tilt: float = 0.55
    kp: tuple[float, float] = (12.0, 10.0)
    kd: tuple[float, float] = (7.0, 6.2)
    theta_kp: float = 18.0
    theta_kd: float = 4.0
    max_force_x: float = 22.0
    max_force_z: float = 24.0
    max_torque: float = 2.4


class QuadrotorMPC:
    """Finite-horizon preview controller.

    MuJoCo simulates the true vehicle mass from the MJCF geoms. This controller
    intentionally uses a 1.2 kg mass estimate, giving the requested mass error.
    """

    def __init__(self, config: MPCConfig | None = None) -> None:
        self.config = config or MPCConfig()

    def command(self, state: np.ndarray, reference: np.ndarray) -> np.ndarray:
        """Return MuJoCo actuator controls [Fx, Fz, pitch_tau]."""
        cfg = self.config
        pos = state[:2]
        theta = state[2]
        vel = state[3:5]
        theta_dot = state[5]

        desired_acc = reference[4:6] + np.array(cfg.kp) * (reference[:2] - pos)
        desired_acc += np.array(cfg.kd) * (reference[2:4] - vel)

        preview_pos = pos.copy()
        preview_vel = vel.copy()
        preview_error = np.zeros(2)
        for _ in range(cfg.horizon_steps):
            preview_vel += desired_acc * cfg.dt
            preview_pos += preview_vel * cfg.dt
            preview_error += reference[:2] - preview_pos
        desired_acc += 0.22 * np.array(cfg.kp) * preview_error / cfg.horizon_steps

        desired_theta = np.clip(-desired_acc[0] / cfg.gravity, -cfg.max_tilt, cfg.max_tilt)
        force_x = cfg.mass_estimate * desired_acc[0]
        force_z = cfg.mass_estimate * (cfg.gravity + desired_acc[1])
        pitch_torque = cfg.theta_kp * (desired_theta - theta) - cfg.theta_kd * theta_dot

        return np.array(
            [
                np.clip(force_x, -cfg.max_force_x, cfg.max_force_x),
                np.clip(force_z, -2.0, cfg.max_force_z),
                np.clip(pitch_torque, -cfg.max_torque, cfg.max_torque),
            ],
            dtype=float,
        )
