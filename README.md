# 🚁 MuJoCo 2D Quadrotor – MPC Control with Figure-8 Tracking under Wind Disturbance

## 📌 Overview
This project implements a complete closed-loop robotics control system for a planar quadrotor simulated in MuJoCo. It integrates physics simulation, MPC-style controller, figure-8 trajectory tracking, sinusoidal wind disturbance, and performance evaluation with video and image outputs.

## 📁 Project Structure
.
├── models/quadrotor_2d.xml
├── sim/__init__.py
├── sim/trajectory.py
├── sim/wind.py
├── sim/metrics.py
├── control/mpc_controller.py
├── run_mujoco_quadrotor.py
├── requirements.txt
└── outputs/quadrotor_figure8_mujoco.mp4
└── outputs/quadrotor_figure8_final.png

## 📦 Requirements
pip install -r requirements.txt

Dependencies:
- mujoco >= 3.2.0
- numpy >= 1.26
- matplotlib >= 3.8
- imageio >= 2.34
- imageio-ffmpeg >= 0.5

## 🤖 System Model
State: [x, z, θ, vx, vz, θ̇]  
Inputs: Fx (force x), Fz (force z), τθ (pitch torque)

## 🌪️ Wind Disturbance
Fx = Ax sin(2πfx t + φ)  
Fz = Az sin(2πfz t) - bias - kx  

## 📈 Reference Trajectory
Figure-8 path in x–z space:  
[x, z, vx, vz, ax, az]

## 🎮 MPC Controller
a_des = a_ref + Kp(p_ref - p) + Kd(v_ref - v)  
Output: [Fx, Fz, τ]  
Features:
- Horizon prediction (18 steps)
- Robust tracking under model mismatch

## ⚙️ Control Limits
Fx: ±22 N  
Fz: [-2, 24] N  
Torque: ±2.4 Nm  

## 📊 Metrics
- Mean tracking error  
- Max tracking error  
- Position bounds  
- Final state error  

## 🎥 Outputs
outputs/quadrotor_figure8_mujoco.mp4  
outputs/quadrotor_figure8_final.png  

## ▶️ Run
python run_mujoco_quadrotor.py --viewer  
python run_mujoco_quadrotor.py --render-video --duration 20  

## 🚁 MuJoCo Model
3-DOF planar quadrotor with:
- x/z slide joints
- pitch hinge
- corridor constraints
- mocap reference marker
- fixed camera view

## 🔬 Key Features
MPC control + wind disturbance + MuJoCo physics + trajectory tracking + metrics + video generation.

## 📌 Conclusion
Complete robotics control pipeline combining simulation, control, disturbance modeling, and evaluation in a single MuJoCo environment.