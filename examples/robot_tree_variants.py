import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src" / "simulator"))

from dynamics.ab_algorithm import ABAlgorithm
from objects import RobotTree
from physics import PhysicsEngine
from renderer import Renderer
from world import World

SELECTED_VARIANT = "balanced"

VARIANTS = {
    "balanced": {
        "nb": 6,
        "bf": 2,
        "taper": 1.0,
        "skew": 0.0,
        "description": "Balanced binary tree",
    },
    "dense": {
        "nb": 7,
        "bf": 3,
        "taper": 0.85,
        "skew": 0.25,
        "description": "Dense branching tree",
    },
    "curved": {
        "nb": 6,
        "bf": 2,
        "taper": 0.70,
        "skew": 0.45,
        "description": "Curved lightweight tree",
    },
}


def main():

    if SELECTED_VARIANT not in VARIANTS:
        raise ValueError(
            f"Unknown variant '{SELECTED_VARIANT}'. "
            f"Available variants: {list(VARIANTS.keys())}"
        )

    config = VARIANTS[SELECTED_VARIANT]

    print("=" * 60)
    print("Robot Tree Variant")
    print("=" * 60)
    print(f"Variant      : {SELECTED_VARIANT}")
    print(f"Description  : {config['description']}")
    print(f"Links        : {config['nb']}")
    print(f"Branch factor: {config['bf']}")
    print(f"Taper        : {config['taper']}")
    print(f"Skew         : {config['skew']}")
    print("=" * 60)

    fd_solver = ABAlgorithm()

    physics = PhysicsEngine(fd_solver)

    renderer = Renderer(
        x_limits=(-6, 6),
        y_limits=(-6, 6),
    )

    world = World(physics, renderer)

    robot = RobotTree()

    robot.some_tree(
        nb=config["nb"],
        bf=config["bf"],
        taper=config["taper"],
        skew=config["skew"],
    )

    world.add_object(robot)

    world.run(180)


if __name__ == "__main__":
    main()