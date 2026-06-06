from __future__ import annotations

import pathlib
import time
import numpy as np
import mujoco
from mujoco import viewer

from control.mpc_controller import QuadrotorMPC
ROOT = pathlib.Path(__file__).resolve().parent
MODEL_PATH = ROOT / "models" / "quadrotor_2d.xml"
controller = QuadrotorMPC()
def state_from_data(data):
    return np.array(
        [
            data.qpos[0],  # x
            data.qpos[1],  # z
            data.qpos[2],  # theta
            data.qvel[0],  # vx
            data.qvel[1],  # vz
            data.qvel[2],  # theta_dot
        ],
        dtype=float,
    )

def main() -> None:
    model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))
    data = mujoco.MjData(model)

    print("MuJoCo model loaded successfully")
    print(f"Model path: {MODEL_PATH}")

    with viewer.launch_passive(model, data) as sim_viewer:
        while sim_viewer.is_running():
            state = state_from_data(data)

            reference = np.array(
                [
                    1.0,  # target x
                    5.0,  # target z
                    0.0,  # target vx
                    0.0,  # target vz
                ],
                dtype=float,
            )

            data.ctrl[:] = controller.command(state, reference)

            mujoco.mj_step(model, data)
            sim_viewer.sync()
            time.sleep(model.opt.timestep)


if __name__ == "__main__":
    main()