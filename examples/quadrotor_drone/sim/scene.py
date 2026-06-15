import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


class Scene:
    def __init__(self, xlim=(-3, 3), ylim=(-1, 4)):
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(xlim)
        self.ax.set_ylim(ylim)
        self.ax.set_aspect("equal")
        plt.show(block=False)

        self.drone_patch = Rectangle((0, 0), 0.5, 0.1, color="blue")
        self.ax.add_patch(self.drone_patch)

        self.pendulum_line, = self.ax.plot([], [], color="black", linewidth=2)
        self.pendulum_mass, = self.ax.plot([], [], "o", color="red", markersize=10)

    def update(self, state):
        y, z, phi, theta = state[:4]

        w, h = 0.5, 0.1
        cx = y - w / 2 * np.cos(phi) + h / 2 * np.sin(phi)
        cy = z - w / 2 * np.sin(phi) - h / 2 * np.cos(phi)
        self.drone_patch.set_xy((cx, cy))
        self.drone_patch.angle = np.degrees(phi)

        l = 0.5
        px = y + l * np.sin(theta)
        pz = z + l * np.cos(theta)
        self.pendulum_line.set_data([y, px], [z, pz])
        self.pendulum_mass.set_data([px], [pz])

        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()

    def close(self):
        plt.close(self.fig)
