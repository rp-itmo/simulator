import numpy as np
from scipy.linalg import solve_continuous_are

from examples.rocket_drone_lqr.sim.dynamics import RocketForces, RocketState
from examples.rocket_drone_lqr.sim.limits import RocketLimits
from examples.rocket_drone_lqr.sim.trajectory import TrajectoryPoint


class LQRController:
    def __init__(self, limits: RocketLimits | None = None):
        self.limits = limits or RocketLimits()

        self.k_x = self._lqr(3.0, 2.0, 5.0)
        self.k_z = self._lqr(10.0, 7.0, 2.0)

        self.max_side_force = 0.55
        self.max_tilt = 0.28
        self.tilt_kp = 3.0
        self.tilt_kd = 1.2

    def _lqr(self, q_pos: float, q_vel: float, r_val: float) -> np.ndarray:
        a = np.array([[0.0, 1.0], [0.0, 0.0]], dtype=float)
        b = np.array([[0.0], [1.0]], dtype=float)
        q = np.diag([q_pos, q_vel])
        r = np.array([[r_val]], dtype=float)
        p = solve_continuous_are(a, b, q, r)
        return np.linalg.inv(r) @ b.T @ p

    def control(self, state: RocketState, reference: TrajectoryPoint) -> RocketForces:
        x_error = np.array(
            [state.x - reference.x, state.vx - reference.vx],
            dtype=float,
        )
        z_error = np.array(
            [state.z - reference.z, state.vz - reference.vz],
            dtype=float,
        )

        ax_cmd = float(reference.ax - (self.k_x @ x_error)[0])
        az_cmd = float(reference.az - (self.k_z @ z_error)[0])

        ax_cmd = float(np.clip(ax_cmd, -1.4, 1.4))
        az_cmd = float(np.clip(az_cmd, -2.0, 2.0))

        f1 = self.limits.mass * (self.limits.gravity + az_cmd)
        f1 = float(np.clip(f1, self.limits.f1_min, self.limits.f1_max))

        side_cmd = 0.7 * reference.vx + 0.25 * (reference.x - state.x)

        if state.theta > self.max_tilt:
            side_cmd -= self.tilt_kp * (state.theta - self.max_tilt)

        if state.theta < -self.max_tilt:
            side_cmd -= self.tilt_kp * (state.theta + self.max_tilt)

        side_cmd -= self.tilt_kd * state.omega

        side_cmd = float(np.clip(
            side_cmd,
            -self.max_side_force,
            self.max_side_force,
        ))
        if abs(state.theta) > 0.45:
            side_cmd = 0.0

        # F2 — вправо, F3 — влево.
        if side_cmd > 0.0:
            f2 = side_cmd
            f3 = 0.0
        else:
            f2 = 0.0
            f3 = -side_cmd

        return RocketForces(f1=f1, f2=f2, f3=f3).clipped(self.limits)