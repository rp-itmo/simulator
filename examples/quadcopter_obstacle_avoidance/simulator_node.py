import time
import zmq
import mujoco
import mujoco.viewer

MODEL_PATH = "skydio_x2/scene.xml"

def main():
    print("[Simulator] Setting up ZeroMQ Server...")
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    print("[Simulator] Loading MuJoCo Model...")
    model = mujoco.MjModel.from_xml_path(MODEL_PATH)
    data = mujoco.MjData(model)
    model.opt.timestep = 0.01

    # Start drone slightly in the air
    data.qpos[0:3] = [0.0, 0.0, 0.1]
    mujoco.mj_forward(model, data)

    print("[Simulator] Launching Viewer...")
    with mujoco.viewer.launch_passive(model, data) as viewer:
        while viewer.is_running():
            step_start = time.time()

            # 1. Wait for Controller to send motor commands
            msg = socket.recv_json()
            if "ctrl" in msg:
                data.ctrl[0:4] = msg["ctrl"]

            # 2. Step Physics
            mujoco.mj_step(model, data)

            # 3. Extract Sensor State
            state = {
                "time": data.time,
                "qpos": data.qpos.tolist(),
                "qvel": data.qvel.tolist()
            }

            # 4. Reply with new state
            socket.send_json(state)

            # Keep GUI responsive
            viewer.sync()
            time_until_next = model.opt.timestep - (time.time() - step_start)
            if time_until_next > 0:
                time.sleep(time_until_next)

if __name__ == "__main__":
    main()