"""Run the MuJoCo 2D quadrotor with 8-figure trajectory and sinusoidal wind."""

from __future__ import annotations

import argparse
import pathlib
import time

import imageio.v2 as imageio
import mujoco
import numpy as np

from control.mpc_controller import QuadrotorMPC
from sim.metrics import TrackingMetrics
from sim.trajectory import FigureEightTrajectory
from sim.wind import SinusoidalWind


ROOT = pathlib.Path(__file__).resolve().parent
MODEL_PATH = ROOT / "models" / "quadrotor_2d.xml"
OUTPUT_DIR = ROOT / "outputs"


def state_from_data(data: mujoco.MjData) -> np.ndarray:
    """Read [x, z, theta, vx, vz, theta_dot] from MuJoCo."""
    return np.array(
        [
            data.qpos[0],
            data.qpos[1],
            data.qpos[2],
            data.qvel[0],
            data.qvel[1],
            data.qvel[2],
        ],
        dtype=float,
    )


def set_reference_marker(model: mujoco.MjModel, data: mujoco.MjData, reference: np.ndarray) -> None:
    marker_id = model.body("reference_marker").mocapid[0]
    data.mocap_pos[marker_id] = np.array([reference[0], 0.0, reference[1]])


def apply_wind(data: mujoco.MjData, wind_force: np.ndarray) -> None:
    data.qfrc_applied[:] = 0.0
    data.qfrc_applied[0] = wind_force[0]
    data.qfrc_applied[1] = wind_force[1]


def render_frame(renderer: mujoco.Renderer, model: mujoco.MjModel, data: mujoco.MjData) -> np.ndarray:
    camera_id = model.camera("overview").id
    renderer.update_scene(data, camera=camera_id)
    return renderer.render()


def simulate(duration: float, viewer: bool, render_video: bool, width: int, height: int) -> dict[str, float]:
    model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))
    data = mujoco.MjData(model)
    controller = QuadrotorMPC()
    trajectory = FigureEightTrajectory()
    wind = SinusoidalWind()
    metrics = TrackingMetrics()

    data.qpos[:] = np.array([0.0, 4.0, 0.0])
    mujoco.mj_forward(model, data)

    frames = []
    renderer = mujoco.Renderer(model, height=height, width=width) if render_video else None
    viewer_handle = None
    if viewer:
        from mujoco import viewer as mujoco_viewer

        viewer_handle = mujoco_viewer.launch_passive(model, data)

    steps = int(duration / model.opt.timestep)
    render_stride = max(1, int((1.0 / 30.0) / model.opt.timestep))

    try:
        for step in range(steps):
            state = state_from_data(data)
            reference = trajectory.sample(data.time)
            set_reference_marker(model, data, reference)

            wind_force = wind.force(data.time, state[:2])
            apply_wind(data, wind_force)
            data.ctrl[:] = controller.command(state, reference)

            mujoco.mj_step(model, data)
            metrics.update(state, reference)

            if viewer_handle:
                viewer_handle.sync()
                time.sleep(model.opt.timestep)

            if renderer and step % render_stride == 0:
                frames.append(render_frame(renderer, model, data))
    finally:
        if viewer_handle:
            viewer_handle.close()
        if renderer:
            renderer.close()

    OUTPUT_DIR.mkdir(exist_ok=True)
    if frames:
        video_path = OUTPUT_DIR / "quadrotor_figure8_mujoco.mp4"
        imageio.mimsave(video_path, frames, fps=30)
        imageio.imwrite(OUTPUT_DIR / "quadrotor_figure8_final.png", frames[-1])

    summary = metrics.summary()
    summary["final_x"] = float(data.qpos[0])
    summary["final_z"] = float(data.qpos[1])
    summary["final_theta"] = float(data.qpos[2])
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--duration", type=float, default=20.0)
    parser.add_argument("--viewer", action="store_true", help="Open the interactive MuJoCo viewer.")
    parser.add_argument("--render-video", action="store_true", help="Render MP4 and final PNG.")
    parser.add_argument("--width", type=int, default=960)
    parser.add_argument("--height", type=int, default=720)
    args = parser.parse_args()

    summary = simulate(
        duration=args.duration,
        viewer=args.viewer,
        render_video=args.render_video or not args.viewer,
        width=args.width,
        height=args.height,
    )

    print("MuJoCo 2D quadrotor, 8-figure trajectory, sinusoidal wind")
    for key, value in summary.items():
        print(f"{key}: {value:.3f}")


if __name__ == "__main__":
    main()
