import zmq
import time
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import block_diag
from scipy.interpolate import CubicSpline

# --- Constants & Environment ---
DRONE_MASS = 1.325
HOVER_CTRL = 3.2495625
GRAVITY = 9.80665
TOTAL_HOVER_THRUST = DRONE_MASS * GRAVITY
GLOBAL_TARGET_Z = 1.0
SIM_DURATION = 20

PILLAR_GEOM = np.array([
    [1.5,  0.0, 0.30], [3.0,  1.5, 0.30], [3.0, -1.5, 0.30],
    [5.0,  0.0, 0.35], [6.0,  2.0, 0.30], [6.0, -2.0, 0.30],
])
SAFETY_MARGIN = 0.36
START_POINT = (0.0, 0.0)
GOAL_POINT = (10.0, 0.0)
X_MIN, X_MAX, Y_MIN, Y_MAX = -1.0, 11.0, -4.0, 4.0

# --- RRT & Spline Functions (Collapsed for brevity, exactly the same as before) ---
class Node:
    def __init__(self, x, y): self.x, self.y, self.parent = x, y, None

def get_distance(n1, n2): return math.hypot(n1.x - n2.x, n1.y - n2.y)

def is_collision_free(n1, n2):
    A, B = np.array([n1.x, n1.y]), np.array([n2.x, n2.y])
    for cx, cy, r in PILLAR_GEOM:
        C = np.array([cx, cy])
        v, w = B - A, C - A
        c1 = np.dot(w, v)
        if c1 <= 0: dist = np.linalg.norm(C - A)
        else:
            c2 = np.dot(v, v)
            if c2 <= c1: dist = np.linalg.norm(C - B)
            else:
                b = c1 / c2
                dist = np.linalg.norm(C - (A + b * v))
        if dist < (r + SAFETY_MARGIN): return False
    return True

def run_rrt(start_raw, goal_raw):
    print("[Controller] Running RRT...")
    node_list = [Node(*start_raw)]
    goal_node = Node(*goal_raw)
    for _ in range(10000):
        rnd = Node(goal_node.x, goal_node.y) if random.random() < 0.1 else Node(random.uniform(X_MIN, X_MAX), random.uniform(Y_MIN, Y_MAX))
        nearest = node_list[np.argmin([get_distance(n, rnd) for n in node_list])]
        theta = math.atan2(rnd.y - nearest.y, rnd.x - nearest.x)
        new_node = Node(nearest.x + 0.4 * math.cos(theta), nearest.y + 0.4 * math.sin(theta))
        new_node.parent = nearest
        
        if is_collision_free(nearest, new_node):
            node_list.append(new_node)
            if get_distance(new_node, goal_node) <= 0.4 and is_collision_free(new_node, goal_node):
                goal_node.parent = new_node
                path = []
                curr = goal_node
                while curr:
                    path.append([curr.x, curr.y])
                    curr = curr.parent
                
                # --- THIS IS THE FIX: Return BOTH the path and the tree ---
                return np.array(path[::-1]), node_list
                
    raise RuntimeError("RRT Failed")

def prune_path(path_coords):
    pruned = [path_coords[0]]
    curr_idx = 0
    while curr_idx < len(path_coords) - 1:
        n1 = Node(*path_coords[curr_idx])
        furthest = curr_idx + 1
        for j in range(len(path_coords) - 1, curr_idx, -1):
            if is_collision_free(n1, Node(*path_coords[j])):
                furthest = j
                break
        pruned.append(path_coords[furthest])
        curr_idx = furthest
    return np.array(pruned)

# --- MPC Design ---
def design_mpc_gain(A_c, B_c, Q_diag, R_diag, N=20, dt=0.01):
    A_d = np.eye(A_c.shape[0]) + A_c * dt
    B_d = B_c * dt
    n_x, n_u = A_c.shape[0], B_c.shape[1]
    P_x, H_u = np.zeros((n_x * N, n_x)), np.zeros((n_x * N, n_u * N))
    A_pow = np.eye(n_x)
    for i in range(N):
        A_pow = A_pow @ A_d
        P_x[n_x * i : n_x * i + n_x, :] = A_pow
        for j in range(i + 1):
            H_u[n_x * i : n_x * i + n_x, n_u * j : n_u * j + n_u] = np.linalg.matrix_power(A_d, i - j) @ B_d
    Q_bar, R_bar = block_diag(*[np.diag(Q_diag)] * N), block_diag(*[np.diag(R_diag)] * N)
    H_T_Q = H_u.T @ Q_bar
    return (np.linalg.inv(H_T_Q @ H_u + R_bar) @ H_T_Q @ P_x)[0:n_u, :]

K_mpc_z = design_mpc_gain(np.array([[0.0, 1.0], [0.0, 0.0]]), np.array([[0.0], [1.0 / DRONE_MASS]]), [350.0, 45.0], [0.02])

# --- Main Controller Loop ---

def main():
    # 1. Plan Path
    raw_path, rrt_tree = run_rrt(START_POINT, GOAL_POINT)
    waypoints = prune_path(raw_path)
    _bk_t = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(waypoints, axis=0), axis=1))])
    cs_x, cs_y = CubicSpline(_bk_t, waypoints[:, 0]), CubicSpline(_bk_t, waypoints[:, 1])
    _t_fine = np.linspace(0.0, _bk_t[-1], 2000)
    trajectory = np.column_stack([cs_x(_t_fine), cs_y(_t_fine)])
    cum_dist = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(trajectory, axis=0), axis=1))])

    # 2. Setup ZeroMQ Connections
    print("[Controller] Connecting to Simulator (Port 5555) and Plotter (Port 5556)...")
    context = zmq.Context()
    
    sim_socket = context.socket(zmq.REQ)
    sim_socket.connect("tcp://localhost:5555")

    plot_socket = context.socket(zmq.PUSH)
    plot_socket.connect("tcp://localhost:5556")

    # 3. Send initial map data to the Plotter Node
    tree_lines = []
    for node in rrt_tree:
        if node.parent is not None:
            tree_lines.append([[node.x, node.y], [node.parent.x, node.parent.y]])

    plot_socket.send_json({
        "type": "init",
        "tree_lines": tree_lines,
        "raw_path": raw_path.tolist(),
        "waypoints": waypoints.tolist(),
        "spline": trajectory.tolist()
    })

    _pursuit_s = 0.0
    takeoff_time = None

    # Kickstart the Simulator REQ/REP loop
    sim_socket.send_json({"ctrl": [0.0, 0.0, 0.0, 0.0]})
    print("[Controller] Tracking started!")

    while True:
        # Wait for state from simulator
        state = sim_socket.recv_json()

        pos_x, pos_y, pos_z = state["qpos"][0:3]
        
        # Send telemetry to Plotter Node
        plot_socket.send_json({
            "type": "telemetry",
            "t": state["time"], "x": pos_x, "y": pos_y, "z": pos_z
        })

        if state["time"] > SIM_DURATION:
            print("[Controller] Simulation Complete. Telling plotter to render...")
            plot_socket.send_json({"type": "done"})
            break

        quat = state["qpos"][3:7]
        vel_x, vel_y, vel_z = state["qvel"][0:3]
        omega = state["qvel"][3:6]

        # Quat to Euler
        sinr_cosp = 2 * (quat[0] * quat[1] + quat[2] * quat[3])
        cosr_cosp = 1 - 2 * (quat[1]**2 + quat[2]**2)
        current_roll = math.atan2(sinr_cosp, cosr_cosp)
        
        sinp = math.sqrt(1 + 2 * (quat[0] * quat[2] - quat[1] * quat[3]))
        cosp = math.sqrt(1 - 2 * (quat[0] * quat[2] - quat[1] * quat[3]))
        current_pitch = 2 * math.atan2(sinp, cosp) - math.pi / 2
        
        siny_cosp = 2 * (quat[0] * quat[3] + quat[1] * quat[2])
        cosy_cosp = 1 - 2 * (quat[2]**2 + quat[3]**2)
        current_yaw = math.atan2(siny_cosp, cosy_cosp)

        # Pure Pursuit Logic
        if pos_z < (GLOBAL_TARGET_Z * 0.90) and takeoff_time is None:
            local_target_x, local_target_y = 0.0, 0.0
        elif takeoff_time is None:
            takeoff_time = state["time"]
            local_target_x, local_target_y = 0.0, 0.0
        elif (state["time"] - takeoff_time) < 2.0:
            local_target_x, local_target_y = 0.0, 0.0
        else:
            i_start = max(0, np.searchsorted(cum_dist, _pursuit_s) - 1)
            i_end = min(len(trajectory) - 1, np.searchsorted(cum_dist, _pursuit_s + 4.0))
            best_s, best_d2 = _pursuit_s, np.inf
            pos_xy = np.array([pos_x, pos_y])
            for i in range(i_start, i_end):
                seg = trajectory[i + 1] - trajectory[i]
                seg_l = np.dot(seg, seg)
                t = 0.0 if seg_l < 1e-12 else np.clip(np.dot(pos_xy - trajectory[i], seg) / seg_l, 0.0, 1.0)
                pt = trajectory[i] + t * seg
                d2 = np.dot(pos_xy - pt, pos_xy - pt)
                if d2 < best_d2:
                    best_d2, best_s = d2, cum_dist[i] + t * math.sqrt(seg_l)
            _pursuit_s = max(_pursuit_s, best_s)
            s_target = min(_pursuit_s + 0.8, cum_dist[-1])
            local_target_x = float(np.interp(s_target, cum_dist, trajectory[:, 0]))
            local_target_y = float(np.interp(s_target, cum_dist, trajectory[:, 1]))

        # Control Math
        world_error_x, world_error_y = local_target_x - pos_x, local_target_y - pos_y
        body_error_x = world_error_x * math.cos(current_yaw) + world_error_y * math.sin(current_yaw)
        body_error_y = -world_error_x * math.sin(current_yaw) + world_error_y * math.cos(current_yaw)
        body_vel_x = vel_x * math.cos(current_yaw) + vel_y * math.sin(current_yaw)
        body_vel_y = -vel_x * math.sin(current_yaw) + vel_y * math.cos(current_yaw)

        u_z_delta = -(K_mpc_z @ np.array([pos_z - GLOBAL_TARGET_Z, vel_z])).item()
        thrust = (TOTAL_HOVER_THRUST + u_z_delta) / max(math.cos(current_roll) * math.cos(current_pitch), 0.75)

        a_des_x, a_des_y = 3.0 * body_error_x - 3.2 * body_vel_x, 3.0 * body_error_y - 3.2 * body_vel_y
        t_pitch = np.clip(a_des_x / GRAVITY, -0.22, 0.22)
        t_roll = np.clip(-a_des_y / GRAVITY, -0.22, 0.22)

        torque_pitch = 26.0 * (t_pitch - current_pitch) - 6.0 * omega[1]
        torque_roll = 26.0 * (t_roll - current_roll) - 6.0 * omega[0]
        torque_yaw = 18.0 * (0.0 - current_yaw) - 4.5 * omega[2]

        f_base = thrust / 4.0
        m1 = f_base - torque_roll + torque_pitch - torque_yaw
        m2 = f_base + torque_roll + torque_pitch + torque_yaw
        m3 = f_base + torque_roll - torque_pitch - torque_yaw
        m4 = f_base - torque_roll - torque_pitch + torque_yaw
        
        ctrl_scale = TOTAL_HOVER_THRUST / (4.0 * HOVER_CTRL)
        ctrl = np.clip(np.array([m1, m2, m3, m4]) / ctrl_scale, 0.0, 13.0).tolist()

        # Send new motor commands back to simulator
        sim_socket.send_json({"ctrl": ctrl})

if __name__ == "__main__":
    main()