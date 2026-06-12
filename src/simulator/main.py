"""Main entry point for the robot simulator."""

from __future__ import annotations

import argparse
import os
import pathlib
import sys

# Add parent directory to path so we can import simulator as a package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulator.dynamics.ab_algorithm import ABAlgorithm
from simulator.objects import CartPole, RobotTree, Tree7, TwoLink
from simulator.physics import PhysicsEngine
from simulator.renderer import Renderer
from simulator.world import World

# Default recording folder
DEFAULT_RECORDING_FOLDER = "recording_simulation"


def resolve_record_path(record_arg: str | None) -> str | None:
    """Resolve the recording path.

    If record_arg is a filename (no directory separators), save to DEFAULT_RECORDING_FOLDER.
    Otherwise use the provided path directly.

    Args:
        record_arg: The --record argument value.

    Returns:
        Resolved path for recording, or None if recording is disabled.
    """
    if record_arg is None:
        return None

    record_path = pathlib.Path(record_arg)

    # If it's just a filename (no directory), use the default recording folder
    if record_path.parent == pathlib.Path("."):
        recording_folder = pathlib.Path(DEFAULT_RECORDING_FOLDER)
        recording_folder.mkdir(exist_ok=True)
        record_path = recording_folder / record_path

    return str(record_path)


def main():
    """Run the robot simulator."""
    parser = argparse.ArgumentParser(
        description="Robot arm simulator with video recording support"
    )
    parser.add_argument(
        "--robot",
        type=str,
        default="cartpole",
        choices=["two-link", "tree7", "robot-tree", "cartpole"],
        help="Robot type to simulate (default: cartpole)",
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=1000,
        help="Number of simulation steps (default: 1000)",
    )
    parser.add_argument(
        "--record",
        type=str,
        metavar="FILENAME",
        help="Record simulation to video (saved to recording_simulation/ folder)",
    )
    parser.add_argument(
        "--fps",
        type=float,
        default=30.0,
        help="Frame rate for video recording (default: 30.0)",
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["mp4", "avi"],
        help="Video format (auto-detected from extension if not specified)",
    )
    args = parser.parse_args()

    # Resolve recording path
    record_path = resolve_record_path(args.record)

    fd_solver = ABAlgorithm()

    physics = PhysicsEngine(fd_solver, gravity=[0.0, -9.81, 0.0])
    renderer = Renderer(
        record_path=record_path,
        record_fps=args.fps,
        record_format=args.format,
    )

    world = World(physics, renderer)

    # Select robot based on argument
    if args.robot == "two-link":
        robot = TwoLink()
    elif args.robot == "tree7":
        robot = Tree7()
    elif args.robot == "robot-tree":
        robot = RobotTree()
        robot.some_tree(8, 2)
    else:  # cartpole (default)
        robot = CartPole()

    world.add_object(robot)

    print(f"Starting simulation: {args.robot}")
    if record_path:
        print(f"Recording to: {record_path}")

    world.run(args.steps)

    if record_path:
        print(f"Recording saved to: {record_path}")


if __name__ == "__main__":
    main()
