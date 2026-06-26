import sys
import time
import numpy as np
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src" / "simulator"))

from dynamics.ab_algorithm import ABAlgorithm
from objects import TwoLink
from physics import PhysicsEngine
from renderer import Renderer
from world import World


def run_experiment(name: str, gravity: list[float]) -> None:
    print("=" * 60)
    print(name)
    print(f"Gravity: {gravity}")
    print("=" * 60)

    fd_solver = ABAlgorithm()

    physics = PhysicsEngine(
        fd_solver,
        gravity=gravity,
    )

    renderer = Renderer(
        x_limits=(-3, 3),
        y_limits=(-3, 3),
    )

    world = World(physics, renderer)

    robot = TwoLink()

    robot.model["gravity"] = np.array(gravity)

    robot.q[0] = 0.5
    robot.q[1] = -0.4

    robot.qd[:] = 0.0

    world.add_object(robot)

    world.run(400)

    renderer.close()

    time.sleep(1)


def main():

    experiments = [
        ("Earth gravity", [0.0, -9.81, 0.0]),
        ("Moon gravity", [0.0, -1.62, 0.0]),
        ("Mars gravity", [0.0, -3.71, 0.0]),
    ]

    for name, gravity in experiments:
        run_experiment(name, gravity)

    print("\nGravity comparison completed.")


if __name__ == "__main__":
    main()