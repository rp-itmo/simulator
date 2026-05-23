import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from .base import RendererBackend


class MatplotlibBackend(RendererBackend):
    """
    Matplotlib-based visualization backend.
    """

    def __init__(self, max_colors=20):
        self.fig = None
        self.ax = None
        self.x_limits = (-10.0, 10.0)
        self.y_limits = (-10.0, 10.0)

        # We can simulate immediate mode by storing geometries every frame
        # and then efficiently dispatching them to matplotlib collections/patches.
        self.lines = []
        self.line_colors = []
        self.line_widths = []

        self.circles = []
        self.rects = []

        # Colormap for some default variety if needed
        self.default_colors = plt.cm.rainbow(np.linspace(0, 1, max_colors))

    def init(self, x_limits=(-10.0, 10.0), y_limits=(-10.0, 10.0), **kwargs):
        self.x_limits = x_limits
        self.y_limits = y_limits

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, aspect="equal")
        self.ax.set_xlim(x_limits)
        self.ax.set_ylim(y_limits)

        plt.show(block=False)

    def clear(self):
        """Prepare for new frame by emptying primitive lists and clearing the axis."""
        self.lines.clear()
        self.line_colors.clear()
        self.line_widths.clear()
        self.circles.clear()
        self.rects.clear()

        self.ax.clear()
        self.ax.set_xlim(self.x_limits)
        self.ax.set_ylim(self.y_limits)
        self.ax.set_aspect("equal")

        # Redraw the world frame origin markers
        self.ax.annotate(
            "",
            xy=(self.x_limits[1] / 10, 0),
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color="red", alpha=0.5),
        )
        self.ax.annotate(
            "",
            xy=(0, self.y_limits[1] / 10),
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color="green", alpha=0.5),
        )

    def draw_line(self, start, end, color="black", width=3):
        self.lines.append([start, end])
        self.line_colors.append(color)
        self.line_widths.append(width)

    def draw_circle(self, center, radius, color="blue"):
        # We store these to apply directly via matplotlib Patch
        self.circles.append(
            {"center": center, "radius": radius, "color": color})

    def draw_box(self, center, width, height, angle=0.0, color="green"):
        # plt.Rectangle expects bottom-left corner and angle in degrees
        cx, cy = center
        w2 = width / 2
        h2 = height / 2

        # Calculate bottom-left unrotated, then apply rotation offset
        # This gives the origin of the rectangle for matplotlib
        dx = -w2 * math.cos(angle) + h2 * math.sin(angle)
        dy = -w2 * math.sin(angle) - h2 * math.cos(angle)
        lower_left = (cx + dx, cy + dy)

        self.rects.append({
            "ll": lower_left,
            "w": width,
            "h": height,
            "an_deg": math.degrees(angle),
            "color": color
        })

    def render(self):
        """Dispatches all geometries to the active subplot."""
        # Render lines via LineCollection for better performance
        if self.lines:
            lc = LineCollection(
                self.lines, colors=self.line_colors, linewidths=self.line_widths)
            self.ax.add_collection(lc)

        # Draw circles
        for c in self.circles:
            circle_patch = plt.Circle(
                c["center"], c["radius"], color=c["color"], zorder=10)
            self.ax.add_patch(circle_patch)

        # Draw boxes
        for r in self.rects:
            rect_patch = plt.Rectangle(
                r["ll"], r["w"], r["h"], angle=r["an_deg"], color=r["color"], zorder=5, fill=True
            )
            self.ax.add_patch(rect_patch)

        # Optional: update base pivot point explicitly
        self.ax.scatter(0.0, 0.0, c="blue", s=50, zorder=10)

        # Flush graph state
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()

    def close(self):
        if self.fig:
            plt.close(self.fig)
