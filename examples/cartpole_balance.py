import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src" / "simulator"))

from dynamics.ab_algorithm import ABAlgorithm
from objects import CartPole
from physics import PhysicsEngine
from renderer import Renderer
from world import World


def run_experiment(initial_angle: float, experiment_name: str) -> None:
    print("=" * 60)
    print(experiment_name)
    print(f"Initial pole angle: {initial_angle:.2f} rad")
    print("=" * 60)

    fd_solver = ABAlgorithm()

    physics = PhysicsEngine(
        fd_solver,
        gravity=[0.0, -9.81, 0.0],
    )

    renderer = Renderer(
        x_limits=(-4, 4),
        y_limits=(-3, 3),
    )

    world = World(physics, renderer)

    robot = CartPole()

    # cart position
    robot.q[0] = 0.0

    # pole angle
    robot.q[1] = initial_angle

    robot.qd[:] = 0.0

    world.add_object(robot)

    world.run(400)

    renderer.close()

    time.sleep(1)


def main():

    experiments = [
        (0.25, "Experiment 1"),
        (0.75, "Experiment 2"),
        (1.25, "Experiment 3"),
    ]

    for angle, name in experiments:
        run_experiment(angle, name)

    print("\nAll experiments completed.")


if __name__ == "__main__":
    main()