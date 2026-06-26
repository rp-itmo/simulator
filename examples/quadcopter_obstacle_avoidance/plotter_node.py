import zmq
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Environment Constants for Plotting
GLOBAL_TARGET_Z = 1.0
PILLAR_GEOM = np.array([
    [1.5,  0.0, 0.20], [3.0,  1.5, 0.20], [3.0, -1.5, 0.20],
    [5.0,  0.0, 0.25], [6.0,  2.0, 0.20], [6.0, -2.0, 0.20],
])
SAFETY_MARGIN = 0.36
START_POINT = (0.0, 0.0)
GOAL_POINT = (10.0, 0.0)
X_MIN, X_MAX, Y_MIN, Y_MAX = -1.0, 11.0, -4.0, 4.0

def main():
    print("[Plotter] Starting Telemetry Listener on Port 5556...")
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://*:5556")

    tree_lines, raw_path, waypoints, spline = [], [], [], []
    t_hist, x_hist, y_hist, z_hist = [], [], [], []

    print("[Plotter] Waiting for Controller data...")
    
    while True:
        msg = socket.recv_json()

        # 1. Receive the planned paths at startup
        if msg["type"] == "init":
            print("[Plotter] Received map and trajectory data.")
            tree_lines = msg["tree_lines"]
            raw_path = np.array(msg["raw_path"])
            waypoints = np.array(msg["waypoints"])
            spline = np.array(msg["spline"])

        # 2. Receive live drone positions during flight
        elif msg["type"] == "telemetry":
            t_hist.append(msg["t"])
            x_hist.append(msg["x"])
            y_hist.append(msg["y"])
            z_hist.append(msg["z"])

        # 3. Receive the shutdown signal and draw the plot
        elif msg["type"] == "done":
            print("[Plotter] Simulation complete. Generating beautiful graphs...")
            break

    # --- Draw the Matplotlib Graphs ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Left Graph: 2D Map
    for line in tree_lines:
        ax1.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], color="grey", alpha=0.2, linewidth=0.5)

    ax1.plot(x_hist, y_hist, label="Drone Flight Path", color="dodgerblue", linewidth=2.5)
    ax1.plot(spline[:, 0], spline[:, 1], color="black", linestyle="--", linewidth=1.5, label="Spline Smooth Path")
    ax1.plot(raw_path[:, 0], raw_path[:, 1], color="orange", linestyle=":", linewidth=1.5, label="Raw RRT Path", alpha=0.6)
    ax1.plot(waypoints[:, 0], waypoints[:, 1], "g^--", markersize=6, linewidth=1.0, label="Pruned Backbone", alpha=0.8)

    ax1.scatter(START_POINT[0], START_POINT[1], color="green", marker="o", s=100, label="Start", zorder=5)
    ax1.scatter(GOAL_POINT[0], GOAL_POINT[1], color="orange", marker="*", s=150, label="Goal", zorder=5)

    for i, pillar in enumerate(PILLAR_GEOM):
        cx, cy, r = pillar
        ax1.add_patch(plt.Circle((cx, cy), r, color="lightcoral", alpha=0.85, label="Pillar" if i == 0 else ""))
        ax1.add_patch(plt.Circle((cx, cy), r + SAFETY_MARGIN, color="lightcoral", fill=False, linestyle=":", linewidth=1.2, alpha=0.5, label="Safety margin" if i == 0 else ""))
        ax1.text(cx, cy, str(i + 1), ha="center", va="center", fontsize=8, fontweight="bold", color="white")

    ax1.set_title("Top-Down Flight Path (RRT & ZeroMQ)")
    ax1.set_xlabel("X (m)")
    ax1.set_ylabel("Y (m)")
    ax1.set_xlim(X_MIN, X_MAX)
    ax1.set_ylim(Y_MIN, Y_MAX)
    ax1.set_aspect("equal")
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(loc="upper left", fontsize=7.5)

    # Right Graph: Altitude
    ax2.plot(t_hist, z_hist, label="Drone Altitude", color="purple")
    ax2.axhline(y=GLOBAL_TARGET_Z, color="darkred", linestyle="--", label="Target Z")
    ax2.set_title("Vertical Tracking Profile")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Altitude (m)")
    ax2.set_ylim(0, 1.5)
    ax2.grid(True, linestyle="--")
    ax2.legend()

    plt.tight_layout()
    
    out_path = Path(__file__).parent / "rrt_zmq_distributed_results.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(f"[Plotter] Results image saved to -> {out_path}")
    
    plt.show()

if __name__ == "__main__":
    main()