#!/bin/bash

echo "[1/3] Starting MuJoCo Simulator Node (Port 5555)..."
python simulator_node.py &

# Give the simulator a moment to bind to its port
sleep 2

echo "[2/3] Starting Controller Node (RRT + MPC)..."
python controller_node.py &

# Start the plotter immediately after to catch the Controller's first broadcast
echo "[3/3] Starting Plotter Dashboard Node (Port 5556)..."
python plotter_node.py

# Keep the Docker container alive while the processes run
wait