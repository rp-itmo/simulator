import sys
import numpy as np

from physics import PhysicsEngine
from renderer import Renderer
from pygame_renderer import PygameRenderer

from world import World

from objects import RobotTree, TwoLink, Tree7, CartPole
from dynamics.ab_algorithm import ABAlgorithm


def main():

    fd_solver = ABAlgorithm()

    physics = PhysicsEngine(fd_solver, gravity=[0.0, -9.81, 0.0])
    renderer = Renderer()
    # renderer = PygameRenderer()

    world = World(physics, renderer)

    # robot = TwoLink()
    # robot = Tree7()

    # robot = RobotTree()
    # robot.some_tree(8,2)

    robot = CartPole()

    world.add_object(robot)

    world.run(1000)


if __name__ == "__main__":
    main()
