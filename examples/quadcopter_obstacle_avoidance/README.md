

### `README.md`

# Autonomous Quadcopter Obstacle Avoidance (Ticket 31-55)

**Team Members:**
* [Mohammed Almaswary (517097)]
* [Teammate Name]

## Project Description
This project implements a distributed autonomous navigation system for a quadcopter in a 3D simulated environment. The system decomposes complex robotics tasks into three specialized nodes using the **ZeroMQ (ZMQ)** messaging protocol for inter-process communication.

### Architecture
1. **Simulator Node (`simulator_node.py`):** Acts as the ZeroMQ Server. Manages the MuJoCo physics engine, rendering, and sensor telemetry.
2. **Controller Node (`controller_node.py`):** The "Brain" of the system. Performs global RRT path planning, spline smoothing, and local path tracking via Pure Pursuit. It executes cascaded MPC (Altitude) and PD (Lateral) control loops to generate motor commands.
3. **Plotter Node (`plotter_node.py`):** A dedicated telemetry dashboard that listens to the network, visualizes the RRT search tree in real-time, and generates performance analytics upon simulation completion.

## Prerequisites
* Python 3.10+
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Recommended for grading)

## How to Run

### Option 1: Local Execution (Windows)
1. Ensure all dependencies are installed: 
   ```bash
   pip install -r requirements.txt
   ```
2. Run the provided batch file to orchestrate all three nodes simultaneously:
   ```bash
   .\start.bat
   ```

### Option 2: Docker Deployment (Linux / Evaluator)
This approach provides a fully isolated environment, satisfying the project's dependency management requirement.

1. **Build the container:**
   ```bash
   docker build -t quadcopter-rrt-mujoco .
   ```
2. **Run with GUI forwarding:**

   *Linux/Ubuntu:*
   ```bash
   xhost +local:docker
   docker run -it --rm --net=host --env="DISPLAY=\$DISPLAY" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" quadcopter-rrt-mujoco
   ```
   *Mac/Windows:* Ensure an X-Server (XQuartz/VcXsrv) is running and configure the `DISPLAY` variable as `host.docker.internal:0`.


