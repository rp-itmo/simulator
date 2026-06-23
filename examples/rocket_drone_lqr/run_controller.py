from examples.rocket_drone_lqr.communication.messages import (
    ControlRequest,
    ControlResponse,
)
from examples.rocket_drone_lqr.communication.zmq_protocol import ZmqServer
from examples.rocket_drone_lqr.control.lqr_controller import LQRController


def main() -> None:
    controller = LQRController()
    server = ZmqServer()

    print("Rocket controller started")

    while True:
        message = server.receive()

        request = ControlRequest.from_dict(message)

        forces = controller.control(
            request.state,
            request.reference,
        )

        response = ControlResponse(
            forces=forces,
        )

        server.send(response.to_dict())


if __name__ == "__main__":
    main()