import numpy as np
from examples.quadrotor_drone.control.lqr_controller import LQRController, linearize


def test_k_matrix_shape():
    controller = LQRController()
    assert controller.K.shape == (2, 8)


def test_closed_loop_stable():
    controller = LQRController()
    A, B = linearize(controller.state_eq, controller.u_eq)
    closed_loop = A - B @ controller.K
    eigvals = np.linalg.eigvals(closed_loop)
    assert np.all(eigvals.real < 0)


def test_compute_output_shape():
    controller = LQRController()
    state = np.zeros(8)
    u = controller.compute(state)
    assert u.shape == (2,)