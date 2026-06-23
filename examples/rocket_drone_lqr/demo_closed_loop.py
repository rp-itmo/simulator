import math

import matplotlib.animation as animation
import matplotlib.pyplot as plt

from examples.rocket_drone_lqr.control.lqr_controller import LQRController
from examples.rocket_drone_lqr.sim.dynamics import RocketDynamics, RocketState
from examples.rocket_drone_lqr.sim.limits import RocketLimits
from examples.rocket_drone_lqr.sim.trajectory import FigureEightTrajectory


def rocket_shape(x: float, z: float, theta: float) -> tuple[list[float], list[float]]:
    body = [
        (0.0, 0.45),
        (-0.18, -0.25),
        (0.18, -0.25),
        (0.0, 0.45),
    ]

    xs = []
    zs = []

    for bx, bz in body:
        rx = bx * math.cos(theta) - bz * math.sin(theta)
        rz = bx * math.sin(theta) + bz * math.cos(theta)
        xs.append(x + rx)
        zs.append(z + rz)

    return xs, zs


def main() -> None:
    limits = RocketLimits()
    dynamics = RocketDynamics(limits)
    controller = LQRController(limits)
    trajectory = FigureEightTrajectory()

    start_reference = trajectory.get(0.0)

    state = RocketState(
        x=start_reference.x,
        z=start_reference.z,
        theta=0.0,
        vx=start_reference.vx,
        vz=start_reference.vz,
        omega=0.0,
    )
    simulation_time = 70.0
    steps = int(simulation_time / limits.dt)

    ref_x = []
    ref_z = []
    real_x = []
    real_z = []
    states = []
    forces_log = []

    for step in range(steps):
        t = step * limits.dt
        reference = trajectory.get(t)
        forces = controller.control(state, reference)
        state = dynamics.step(state, forces)

        ref_x.append(reference.x)
        ref_z.append(reference.z)
        real_x.append(state.x)
        real_z.append(state.z)
        states.append(state)
        forces_log.append(forces)

    fig, ax = plt.subplots(figsize=(10, 7))

    ax.set_title("2D Rocket Drone LQR trajectory tracking")
    ax.set_xlabel("x")
    ax.set_ylabel("z")
    ax.set_xlim(limits.x_min, limits.x_max)
    ax.set_ylim(limits.z_min, limits.z_max)
    ax.grid(True)
    ax.set_aspect("equal", adjustable="box")

    ax.plot(ref_x, ref_z, "--", label="reference trajectory")
    real_line, = ax.plot([], [], label="rocket trajectory")
    rocket_line, = ax.plot([], [], linewidth=2, label="rocket body")
    thrust_line, = ax.plot([], [], linewidth=2, label="main thrust")
    text = ax.text(0.02, 0.95, "", transform=ax.transAxes)

    ax.legend(loc="upper right")

    frame_stride = 5
    frame_count = len(states) // frame_stride

    def update(frame: int):
        index = frame * frame_stride
        current_state = states[index]
        current_forces = forces_log[index]
        current_time = index * limits.dt

        real_line.set_data(real_x[:index], real_z[:index])

        xs, zs = rocket_shape(
            current_state.x,
            current_state.z,
            current_state.theta,
        )
        rocket_line.set_data(xs, zs)

        thrust_scale = 0.035 * current_forces.f1
        thrust_x = [
            current_state.x,
            current_state.x + thrust_scale * math.sin(current_state.theta),
        ]
        thrust_z = [
            current_state.z - 0.3,
            current_state.z - 0.3 - thrust_scale * math.cos(current_state.theta),
        ]
        thrust_line.set_data(thrust_x, thrust_z)

        text.set_text(
            f"t = {current_time:.1f} s\n"
            f"x = {current_state.x:.2f}, z = {current_state.z:.2f}\n"
            f"theta = {current_state.theta:.2f} rad\n"
            f"F1 = {current_forces.f1:.2f}, "
            f"F2 = {current_forces.f2:.2f}, "
            f"F3 = {current_forces.f3:.2f}"
        )

        return real_line, rocket_line, thrust_line, text

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=frame_count,
        interval=20,
        blit=True,
    )

    plt.show()


if __name__ == "__main__":
    main()