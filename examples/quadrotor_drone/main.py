import numpy as np
from examples.quadrotor_drone.sim.dynamics import step
from examples.quadrotor_drone.sim.scene import Scene
from examples.quadrotor_drone.control.lqr_controller import LQRController


def main():
    state = np.array([0.0, 0.0, 0.0, 0.3, 0.0, 0.0, 0.0, 0.0])
    controller = LQRController()
    scene = Scene()

    dt = 0.02
    for i in range(500):
        u = controller.compute(state)
        state = step(state, u, dt)
        scene.update(state)

    scene.close()


if __name__ == "__main__":
    main()
