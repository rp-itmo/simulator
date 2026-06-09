"""Main entry point for the robot simulator."""

from __future__ import annotations

import argparse
import pathlib
import sys

from simulator.dynamics.ab_algorithm import ABAlgorithm
from simulator.objects import CartPole, RobotTree, Tree7, TwoLink
from simulator.physics import PhysicsEngine
from simulator.renderer import Renderer
from simulator.world import World


DEFAULT_RECORDING_FOLDER = "recording_simulation"


def resolve_record_path(record_arg: str | None) -> str | None:
    """Resolve video recording path.

    If only a filename is given, the file is saved inside
    the default recording_simulation/ folder.
    """
    if record_arg is None:
        return None

    record_path = pathlib.Path(record_arg)

    if record_path.parent == pathlib.Path("."):
        recording_folder = pathlib.Path(DEFAULT_RECORDING_FOLDER)
        recording_folder.mkdir(parents=True, exist_ok=True)
        record_path = recording_folder / record_path
    else:
        record_path.parent.mkdir(parents=True, exist_ok=True)

    return str(record_path)


def create_robot(robot_name: str):
    """Create a robot object based on the command-line argument."""
    if robot_name == "two-link":
        return TwoLink()

    if robot_name == "tree7":
        return Tree7()

    if robot_name == "robot-tree":
        robot = RobotTree()
        robot.some_tree(8, 2)
        return robot

    if robot_name == "cartpole":
        return CartPole()

    raise ValueError(f"Unknown robot type: {robot_name}")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Robot simulator with dynamics, rendering, and video recording."
    )

    parser.add_argument(
        "--robot",
        type=str,
        default="cartpole",
        choices=["two-link", "tree7", "robot-tree", "cartpole"],
        help="Robot type to simulate.",
    )

    parser.add_argument(
        "--steps",
        type=int,
        default=1000,
        help="Number of simulation steps.",
    )

    parser.add_argument(
        "--dt",
        type=float,
        default=0.02,
        help="Simulation time step in seconds.",
    )

    parser.add_argument(
        "--record",
        type=str,
        metavar="FILENAME",
        help="Record simulation to a video file.",
    )

    parser.add_argument(
        "--fps",
        type=float,
        default=30.0,
        help="Frame rate for video recording.",
    )

    parser.add_argument(
        "--format",
        type=str,
        choices=["mp4", "avi"],
        help="Video format. Auto-detected from extension if not specified.",
    )

    parser.add_argument(
        "--xlim",
        type=float,
        nargs=2,
        default=(-10.0, 10.0),
        metavar=("XMIN", "XMAX"),
        help="Renderer x-axis limits.",
    )

    parser.add_argument(
        "--ylim",
        type=float,
        nargs=2,
        default=(-10.0, 10.0),
        metavar=("YMIN", "YMAX"),
        help="Renderer y-axis limits.",
    )

    return parser.parse_args()


def main() -> int:
    """Run the robot simulator."""
    args = parse_args()

    if args.steps <= 0:
        print("Error: --steps must be a positive integer.", file=sys.stderr)
        return 1

    if args.dt <= 0:
        print("Error: --dt must be a positive number.", file=sys.stderr)
        return 1

    record_path = resolve_record_path(args.record)

    fd_solver = ABAlgorithm()
    physics = PhysicsEngine(fd_solver, gravity=[0.0, -9.81, 0.0])

    renderer = Renderer(
        x_limits=tuple(args.xlim),
        y_limits=tuple(args.ylim),
        record_path=record_path,
        record_fps=args.fps,
        record_format=args.format,
    )

    world = World(physics, renderer)
    world.dt = args.dt

    robot = create_robot(args.robot)
    world.add_object(robot)

    print(f"Starting simulation")
    print(f"Robot: {args.robot}")
    print(f"Steps: {args.steps}")
    print(f"dt: {args.dt}")

    if record_path is not None:
        print(f"Recording: {record_path}")

    try:
        world.run(args.steps)
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user.")
    finally:
        renderer.close()

    if record_path is not None:
        print(f"Recording saved: {record_path}")

    print("Simulation finished.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())