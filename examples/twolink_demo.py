import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src" / "simulator"))

from physics import PhysicsEngine
from renderer import Renderer
from world import World

from objects import TwoLink
from dynamics.ab_algorithm import ABAlgorithm


def main():
    fd_solver = ABAlgorithm()

    physics = PhysicsEngine(fd_solver, gravity=[0.0, -9.81, 0.0])
    renderer = Renderer()

    world = World(physics, renderer)

    robot = TwoLink()

    world.add_object(robot)

    world.run(1000)


if __name__ == "__main__":
    main()
1