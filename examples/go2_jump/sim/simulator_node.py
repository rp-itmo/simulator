import time
import numpy as np

import mujoco
import mujoco.viewer

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from builtin_interfaces.msg import Time

from config import MODEL

np.set_printoptions(precision=5)

m = mujoco.MjModel.from_xml_path(MODEL)
d = mujoco.MjData(m)

mujoco.mj_resetDataKeyframe(m, d, m.key("home").id)

class Simulator_ROS2_Bridge(Node):

    def __init__(self, viewer):
        super().__init__('simulator')
        self.viewer = viewer
        self.subscription = self.create_subscription(
            JointState,
            '/joint_commands',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

        self.publisher = self.create_publisher(
            JointState,
            '/joint_states',
            10)
        self.publisher  # prevent unused variable warning

        self.last_reply = 0.0
        self.create_timer(0.5, self.timer_controller)

    def timer_controller(self):
        if time.time() - self.last_reply > 0.5:
            self.send_state()

    def send_state(self):
        send = JointState()
        send.header.stamp.sec = int(d.time)
        send.header.stamp.nanosec = int((d.time - int(d.time)) * 1e9)
        send.position = d.qpos[3:].tolist()
        send.velocity = d.qvel[3:].tolist()
        self.publisher.publish(send)

    def listener_callback(self, msg):
        self.last_reply = time.time()
        d.ctrl[:] = msg.effort
        mujoco.mj_step(m, d)
        self.viewer.sync()
        time.sleep(m.opt.timestep)
        
        self.send_state()


def main(args=None):

    rclpy.init(args=args)

    with mujoco.viewer.launch_passive(m, d, show_left_ui=False, show_right_ui=False) as viewer:
        viewer.cam.type = mujoco.mjtCamera.mjCAMERA_FIXED
        viewer.cam.fixedcamid = m.camera("side_cam").id

        mujoco.mj_forward(m, d)  # посчитать центр масс до первого шага, иначе там нули
            
        base = m.body("base").id
        x0 = d.subtree_com[base][0]  # x центра масс всего оробота на старте

        node = Simulator_ROS2_Bridge(viewer)
        node.send_state()

        while viewer.is_running():
            rclpy.spin_once(node, timeout_sec=0.1)

        print(f"Длина прыжка в окне: {d.subtree_com[base][0] - x0:.3f} м")
    
        node.destroy_node()

    if rclpy.ok():
        rclpy.shutdown()


if __name__=="__main__":
    main()
