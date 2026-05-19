# SIMULATOR

## Description

This project is a physical simulator of robotic systems in Python. The simulator implements the calculation of forward kinematics and dynamics (including the Articulated-Body algorithm), integration of equations of motion using SciPy (Runge-Kutta method) and step-by-step visualization of the operation of mechanisms using Matplotlib. Currently, various types of models are supported: two-link mechanisms, a reverse pendulum on a cart (CartPole) and complex multi-link trees (RobotTree).

## Run guide

To run project, use the following command
```
uv run python src/simulator/main.py
```