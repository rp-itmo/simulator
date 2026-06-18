import numpy as np
from examples.quadrotor_drone.sim.dynamics import dynamics, step


def test_dynamics_output_shape():
    state = np.zeros(8)
    u = np.array([5.0, 5.0])
    result = dynamics(state, u)
    assert result.shape == (8,)


def test_step_output_shape():
    state = np.zeros(8)
    u = np.array([5.0, 5.0])
    result = step(state, u, 0.01)
    assert result.shape == (8,)


def test_step_changes_state():
    state = np.zeros(8)
    state[3] = 0.1
    u = np.array([5.0, 5.0])
    result = step(state, u, 0.01)
    assert not np.allclose(result, state)