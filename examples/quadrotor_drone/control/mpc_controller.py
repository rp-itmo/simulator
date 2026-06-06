from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class MPCConfig:
    mass_estimate: float = 1.2
    gravity: float = 9.81

    horizon_steps: int = 18
    dt: float = 0.005

    kp_x: float = 4.8
    kd_x: float = 4.2
    kp_z: float = 7.4
    kd_z: float = 5.2

    theta_kp: float = 18.0
    theta_kd: float = 4.0

    max_force_x: float = 18.0
    max_force_z: float = 24.0
    max_torque: float = 2.4
    max_tilt: float = 0.55


class QuadrotorMPC:
    def __init__(self, config: MPCConfig | None = None) -> None:
        self.config = config or MPCConfig()

    def command(self, state: np.ndarray, reference: np.ndarray) -> np.ndarray:
        """
        State:
            [x, z, theta, vx, vz, theta_dot]

        Reference:
            [x_ref, z_ref, vx_ref, vz_ref]

        Output:
            [Fx, Fz, pitch_torque]
        """
        cfg = self.config

        position = state[:2]
        theta = state[2]
        velocity = state[3:5]
        theta_dot = state[5]

        reference_position = reference[:2]
        reference_velocity = reference[2:4]

        position_error = reference_position - position
        velocity_error = reference_velocity - velocity

        desired_acc = np.array(
            [
                cfg.kp_x * position_error[0] + cfg.kd_x * velocity_error[0],
                cfg.kp_z * position_error[1] + cfg.kd_z * velocity_error[1],
            ],
            dtype=float,
        )

        predicted_position = position.copy()
        predicted_velocity = velocity.copy()
        preview_error = np.zeros(2, dtype=float)

        for _ in range(cfg.horizon_steps):
            predicted_velocity += desired_acc * cfg.dt
            predicted_position += predicted_velocity * cfg.dt
            preview_error += reference_position - predicted_position

        preview_error = preview_error / cfg.horizon_steps
        desired_acc += 0.25 * np.array([cfg.kp_x, cfg.kp_z]) * preview_error

        desired_theta = -desired_acc[0] / cfg.gravity
        desired_theta = np.clip(desired_theta, -cfg.max_tilt, cfg.max_tilt)

        force_x = cfg.mass_estimate * desired_acc[0]
        force_z = cfg.mass_estimate * (cfg.gravity + desired_acc[1])

        pitch_torque = cfg.theta_kp * (desired_theta - theta) - cfg.theta_kd * theta_dot

        force_x = np.clip(force_x, -cfg.max_force_x, cfg.max_force_x)
        force_z = np.clip(force_z, -2.0, cfg.max_force_z)
        pitch_torque = np.clip(pitch_torque, -cfg.max_torque, cfg.max_torque)

        return np.array([force_x, force_z, pitch_torque], dtype=float)