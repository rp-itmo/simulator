from examples.rocket_drone_lqr.control.lqr_controller import LQRController
from examples.rocket_drone_lqr.sim.dynamics import RocketState
from examples.rocket_drone_lqr.sim.limits import RocketLimits
from examples.rocket_drone_lqr.sim.trajectory import TrajectoryPoint


def test_lqr_controller_returns_limited_forces():
    limits = RocketLimits()
    controller = LQRController(limits)

    state = RocketState(
        x=0.0,
        z=4.0,
        theta=0.0,
        vx=0.0,
        vz=0.0,
        omega=0.0,
    )

    reference = TrajectoryPoint(
        x=1.0,
        z=4.2,
        vx=0.2,
        vz=0.0,
        ax=0.0,
        az=0.0,
        theta=0.0,
    )

    forces = controller.control(state, reference)

    assert limits.f1_min <= forces.f1 <= limits.f1_max
    assert limits.f2_min <= forces.f2 <= limits.f2_max
    assert limits.f3_min <= forces.f3 <= limits.f3_max


def test_lqr_controller_uses_f2_for_right_motion():
    controller = LQRController()

    state = RocketState(
        x=0.0,
        z=4.0,
        theta=0.0,
        vx=0.0,
        vz=0.0,
        omega=0.0,
    )

    reference = TrajectoryPoint(
        x=1.0,
        z=4.0,
        vx=0.5,
        vz=0.0,
        ax=0.0,
        az=0.0,
        theta=0.0,
    )

    forces = controller.control(state, reference)

    assert forces.f2 > 0.0
    assert forces.f3 == 0.0