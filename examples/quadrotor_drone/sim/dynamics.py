import numpy as np

M = 1.0
m = 0.2
l = 0.5
I = 0.05
L = 0.25
g = 9.81


def dynamics(state, u):
    y, z, phi, theta, vy, vz, vphi, vtheta = state
    F1, F2 = u
    F = F1 + F2
    tau = (F2 - F1) * L

    A = np.array([
        [M + m, 0, m * l * np.cos(theta)],
        [0, M + m, -m * l * np.sin(theta)],
        [np.cos(theta), -np.sin(theta), l],
    ])

    b = np.array([
        -F * np.sin(phi) + m * l * np.sin(theta) * vtheta ** 2,
        F * np.cos(phi) - (M + m) * g + m * l * np.cos(theta) * vtheta ** 2,
        g * np.sin(theta),
    ])

    ay, az, atheta = np.linalg.solve(A, b)
    aphi = tau / I

    return np.array([vy, vz, vphi, vtheta, ay, az, aphi, atheta])


def step(state, u, dt):
    k1 = dynamics(state, u)
    k2 = dynamics(state + dt / 2 * k1, u)
    k3 = dynamics(state + dt / 2 * k2, u)
    k4 = dynamics(state + dt * k3, u)
    return state + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
