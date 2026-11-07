import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

import numpy as np


def controller(q, dq, t, knee_sit, thigh_jump, kp_jump):
    q_home = np.array([0, 0.9, -1.8] * 4)
    q_sit  = np.array([0, -knee_sit / 2, knee_sit] * 4)
    q_jump = np.array([0, thigh_jump, -0.9] * 4)

    if t <= 2.0:  # стойка
        q_dest = q_home
        Kp = 100
    elif t <= 4.0:  # присед
        q_dest = q_sit
        Kp = 100
    elif t < 4.5:  # толчок: своя сила
        q_dest = q_jump
        Kp = kp_jump
    else:  # полёт и приземление
        q_dest = q_home
        Kp = 100

    torques = Kp * (q_dest - q) - 1 * dq  # Kp вместо 100
    return torques


class Controller_ROS2_Bridge(Node):

    def __init__(self):
        super().__init__('controller')
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

        self.publisher = self.create_publisher(
            JointState,
            '/joint_commands',
            10)
        self.publisher  # prevent unused variable warning

    def listener_callback(self, msg):
        best_knee, best_thigh, best_kp = -1.8, 1.5, 300
        t = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
        q, dq = np.array(msg.position), np.array(msg.velocity)
        torques = controller(q, dq, t, best_knee, best_thigh, best_kp)
        reply = JointState()
        reply.header.stamp = msg.header.stamp
        reply.name = msg.name
        reply.effort = torques.tolist()
        self.publisher.publish(reply)


def main(args=None):

    rclpy.init(args=args)

    node = Controller_ROS2_Bridge()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    if rclpy.ok():
        rclpy.shutdown()


if __name__=="__main__":
    main()
