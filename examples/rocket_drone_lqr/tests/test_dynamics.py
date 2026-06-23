from examples.rocket_drone_lqr.sim.dynamics import (
    RocketDynamics,
    RocketForces,
    RocketState,
)
from examples.rocket_drone_lqr.sim.limits import RocketLimits


def test_rocket_hover_with_gravity_compensation():
    limits = RocketLimits()
    dynamics = RocketDynamics(limits)

    state = RocketState(
        x=0.0,
        z=4.0,
        theta=0.0,
        vx=0.0,
        vz=0.0,
        omega=0.0,
    )

    forces = RocketForces(
        f1=limits.mass * limits.gravity,
        f2=0.0,
        f3=0.0,
    )

    next_state = dynamics.step(state, forces)

    assert abs(next_state.z - state.z) < 1e-3
    assert abs(next_state.vz) < 1e-3