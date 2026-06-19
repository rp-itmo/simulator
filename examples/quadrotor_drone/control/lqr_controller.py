import numpy as np
from scipy.linalg import solve_continuous_are
from examples.quadrotor_drone.sim.dynamics import dynamics, M, m, g


def linearize(state_eq, u_eq, eps=1e-5):
    n = len(state_eq)
    k = len(u_eq)
    A = np.zeros((n, n))
    B = np.zeros((n, k))

    for i in range(n):
        dx = np.zeros(n)
        dx[i] = eps
        f1 = dynamics(state_eq + dx, u_eq)
        f2 = dynamics(state_eq - dx, u_eq)
        A[:, i] = (f1 - f2) / (2 * eps)

    for i in range(k):
        du = np.zeros(k)
        du[i] = eps
        f1 = dynamics(state_eq, u_eq + du)
        f2 = dynamics(state_eq, u_eq - du)
        B[:, i] = (f1 - f2) / (2 * eps)

    return A, B


class LQRController:
    def __init__(self, Q=None, R=None):
        self.state_eq = np.zeros(8)
        self.u_eq = np.array([(M + m) * g / 2, (M + m) * g / 2])

        A, B = linearize(self.state_eq, self.u_eq)

        if Q is None:
            Q = np.eye(8)
        if R is None:
            R = np.eye(2)

        P = solve_continuous_are(A, B, Q, R)
        self.K = np.linalg.inv(R) @ B.T @ P

    def compute(self, state):
        return self.u_eq - self.K @ (state - self.state_eq)
