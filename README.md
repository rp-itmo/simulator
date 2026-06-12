# Robot Simulator

A Python-based robot arm simulator with video recording capability.



## Problem: How to Record Robot Simulations?

### The Challenge

We needed to add video recording capability to a matplotlib-based robot simulator. The requirement was to:
1. Capture each frame of the simulation
2. Save it as a video file (MP4/AVI)
3. Use OpenCV for future extensibility (robotics + AI projects)

### Our Solution

We used **OpenCV** (`cv2.VideoWriter`) to capture and encode video frames:

1. **Frame Capture**: After matplotlib renders each frame, we capture it from the canvas buffer
2. **Color Conversion**: matplotlib gives RGBA format, OpenCV needs BGR - we convert using `cv2.cvtColor()`
3. **Video Encoding**: OpenCV's `VideoWriter` handles MP4/AVI encoding efficiently
4. **Auto Folder**: Recordings automatically save to `recording_simulation/` folder

### Why OpenCV Instead of imageio?

| Feature | OpenCV | imageio |
|---------|--------|---------|
| Computer Vision | ✅ Yes | ❌ No |
| Real-time camera support | ✅ Yes | ❌ No |
| ML/AI integration | ✅ Yes | ❌ No |
| Industry standard for robotics | ✅ Yes | ❌ No |

OpenCV is the better choice for robotics + AI projects since you may later want to:
- Process video with ML models
- Add real camera feeds
- Do object detection (YOLO, etc.)

## Files Added/Modified

### New Files
- **`src/simulator/video_recorder.py`** - OpenCV-based video recording class
- **`src/simulator/spatial/__init__.py`** - Module initialization for relative imports

### Modified Files
- **`src/simulator/renderer.py`** - Added frame capture and recording to `update()` method
- **`src/simulator/main.py`** - Added CLI arguments for recording control
- **`src/simulator/world.py`** - Simplified recording setup
- **`src/simulator/dynamics/ab_algorithm.py`** - Fixed scalar extraction bug
- **`pyproject.toml`** - Added `opencv-python` dependency

## How to Run

### Prerequisites

Install dependencies:
```bash
pip install opencv-python matplotlib scipy numpy
```

### Basic Usage

```bash
# Run from the simulator-master folder
cd simulator-master

# Run simulation with default robot (CartPole)
python src/simulator/main.py --steps 300

# Record to video (saved in recording_simulation/ folder)
python src/simulator/main.py --record my_robot.mp4 --steps 200 --fps 15
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--robot` | Robot type: `cartpole`, `two-link`, `tree7`, `robot-tree` | `cartpole` |
| `--steps` | Number of simulation steps | `1000` |
| `--record` | Output filename for recording | (no recording) |
| `--fps` | Frames per second for video | `30.0` |
| `--format` | Video format: `mp4`, `avi` | (auto-detected) |

### Examples

```bash
# Record CartPole (default robot)
python src/simulator/main.py --record cartpole_demo.mp4 --steps 300 --fps 20

# Record Two-Link robot
python src/simulator/main.py --robot two-link --record two_link.mp4 --steps 200

# Record Tree7 robot with custom FPS
python src/simulator/main.py --robot tree7 --record tree7_sim.mp4 --fps 30

# Record with custom path
python src/simulator/main.py --record /path/to/my_video.mp4 --steps 150
```

## Output Location

Videos are saved in the `recording_simulation/` folder (automatically created):

```
TEAM-005/
├── recording_simulation/
│   ├── my_robot.mp4
│   ├── cartpole_demo.mp4
│   └── tree7_sim.mp4
└── ...
```

## Robot Models Available

1. **CartPole** - Simple pole on a cart (default)
2. **TwoLink** - Two-segment arm
3. **Tree7** - 7-DOF tree structure
4. **RobotTree** - Custom tree with configurable DOF

## Technical Details

### Dynamics Computation
- Uses **Articulated Body Algorithm (ABA)** from Featherstone's Rigid Body Dynamics
- Integrates equations of motion using `scipy.integrate.solve_ivp`
- Supports gravity, joint torques, and external forces

### Rendering
- Matplotlib-based 2D visualization
- LineCollection for efficient link drawing
- Scattered points for joints
- World frame axes displayed (red=X, green=Y)

### Recording Process
1. Each simulation step renders the robot
2. `renderer.update()` captures the canvas as RGBA numpy array
3. `VideoRecorder.add_frame()` converts RGBA→BGR and writes to file
4. On completion, `VideoRecorder.stop()` finalizes the video file

## Future Extensions

With OpenCV installed, you can now:
- Add real camera feeds to the simulation
- Implement ML-based controllers
- Use computer vision for feedback control
- Integrate object detection for target tracking
- Add image processing pipelines



