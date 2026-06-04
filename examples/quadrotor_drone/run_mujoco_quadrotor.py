from __future__ import annotations

import pathlib
import time

import mujoco
from mujoco import viewer


ROOT = pathlib.Path(__file__).resolve().parent
MODEL_PATH = ROOT / "models" / "quadrotor_2d.xml"


def main() -> None:
    model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))
    data = mujoco.MjData(model)

    print("Loaded MuJoCo model:")
    print(MODEL_PATH)

    with viewer.launch_passive(model, data) as sim_viewer:
        while sim_viewer.is_running():
            mujoco.mj_step(model, data)
            sim_viewer.sync()
            time.sleep(model.opt.timestep)


if __name__ == "__main__":
    main()