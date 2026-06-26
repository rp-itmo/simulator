from examples.rocket_drone_lqr.communication.messages import (
    ControlRequest,
    ControlResponse,
)
from examples.rocket_drone_lqr.sim.dynamics import RocketForces, RocketState
from examples.rocket_drone_lqr.sim.trajectory import TrajectoryPoint


def test_control_request_roundtrip():
    request = ControlRequest(
        time=1.5,
        state=RocketState(x=1.0, z=2.0, theta=0.1, vx=0.2, vz=0.3, omega=0.4),
        reference=TrajectoryPoint(
            x=1.1,
            z=2.1,
            vx=0.2,
            vz=0.3,
            ax=0.0,
            az=0.0,
            theta=0.0,
        ),
    )

    restored = ControlRequest.from_dict(request.to_dict())

    assert restored == request


def test_control_response_roundtrip():
    response = ControlResponse(
        forces=RocketForces(f1=9.8, f2=0.5, f3=0.1),
    )

    restored = ControlResponse.from_dict(response.to_dict())

    assert restored == response