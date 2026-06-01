import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

from camera import Camera, ViewMode


class Renderer:

    def __init__(
        self,
        x_limits=(-10.0, 10.0),
        y_limits=(-10.0, 10.0),
        max_colors=20
    ):

        self.fig = plt.figure(figsize=(10, 8))

        self.ax = self.fig.add_subplot(
            111,
            aspect="equal"
        )

        self.camera = Camera(
            x_limits=x_limits,
            y_limits=y_limits
        )

        self.follow_enabled = True

        self.camera.apply_to_axes(self.ax)

        self.fig.canvas.mpl_connect(
            "key_press_event",
            self._on_key_press
        )

        self.fig.canvas.mpl_connect(
            "scroll_event",
            self._on_scroll
        )

        plt.show(block=False)

        self.links_lines = None
        self.joints_circles = None
        self.base_point = None

        self.colors = plt.cm.rainbow(
            np.linspace(0, 1, max_colors)
        )

    def _on_scroll(self, event):

        if event.button == "up":
            self.camera.zoom_in()

        elif event.button == "down":
            self.camera.zoom_out()

        self.camera.apply_to_axes(self.ax)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def _on_key_press(self, event):

        pan_step = 2.0

        if event.key in ["v", "V"]:
            self.camera.toggle_view_mode()

        elif event.key in ["f", "F"]:
            self.follow_enabled = not self.follow_enabled

        elif event.key == "left":
            self.follow_enabled = False
            self.camera.pan(-pan_step, 0.0)

        elif event.key == "right":
            self.follow_enabled = False
            self.camera.pan(pan_step, 0.0)

        elif event.key == "up":
            self.follow_enabled = False
            self.camera.pan(0.0, pan_step)

        elif event.key == "down":
            self.follow_enabled = False
            self.camera.pan(0.0, -pan_step)

        self.camera.apply_to_axes(self.ax)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def _draw_grid(self):

        xmin, xmax = self.ax.get_xlim()
        ymin, ymax = self.ax.get_ylim()

        step = 1.0

        x_values = np.arange(
            np.floor(xmin),
            np.ceil(xmax) + step,
            step
        )

        y_values = np.arange(
            np.floor(ymin),
            np.ceil(ymax) + step,
            step
        )

        for x in x_values:
            self.ax.axvline(
                x,
                color="gray",
                alpha=0.15,
                linewidth=0.5
            )

        for y in y_values:
            self.ax.axhline(
                y,
                color="gray",
                alpha=0.15,
                linewidth=0.5
            )

    def _draw_world_frame(self):

        axis_label_offset = 0.5

        if self.camera.view_mode == ViewMode.TOP:
            # TOP view shows X-Y projection.
            # Z axis is hidden.
            self.ax.axhline(
                0.0,
                color="green",
                alpha=0.5,
                linewidth=1.5
            )

            self.ax.axvline(
                0.0,
                color="red",
                alpha=0.5,
                linewidth=1.5
            )

            self.ax.text(
                self.ax.get_xlim()[1] - axis_label_offset,
                axis_label_offset,
                "X",
                color="red"
            )

            self.ax.text(
                axis_label_offset,
                self.ax.get_ylim()[1] - axis_label_offset,
                "Y",
                color="green"
            )

        else:
            # LEFT view shows X-Z projection.
            # Y axis is hidden.
            self.ax.axhline(
                0.0,
                color="blue",
                alpha=0.5,
                linewidth=1.5
            )

            self.ax.axvline(
                0.0,
                color="red",
                alpha=0.5,
                linewidth=1.5
            )

            self.ax.text(
                self.ax.get_xlim()[1] - axis_label_offset,
                axis_label_offset,
                "X",
                color="red"
            )

            self.ax.text(
                axis_label_offset,
                self.ax.get_ylim()[1] - axis_label_offset,
                "Z",
                color="blue"
            )

    def _draw_tree(self, obj, q):

        parents = obj.model["parent"]

        nodes = []
        edges = []
        angles = [0.0] * len(parents)

        length = 1.0

        base_x, base_y = self.camera.project(
            obj.get_position()
        )

        for i in range(len(parents)):

            parent = parents[i]

            if parent == -1:
                x_p, y_p = base_x, base_y
                angles[i] = q[i]

            else:
                x_p, y_p = nodes[parent]
                angles[i] = angles[parent] + q[i]

            x_child = x_p + length * np.cos(angles[i])

            if self.camera.view_mode == ViewMode.TOP:
                y_child = y_p + length * np.sin(angles[i])
            else:
                y_child = y_p + 0.5 * np.sin(q[i])

            nodes.append(
                (
                    x_child,
                    y_child
                )
            )

            edges.append(
                (
                    x_p,
                    y_p,
                    x_child,
                    y_child
                )
            )

        return nodes, edges

    def update(self, objects, dt=0.0001):

        if not objects:
            return

        self.ax.cla()

        if (
            self.follow_enabled
            and self.camera.target is not None
        ):
            self.camera.update()

        self.camera.apply_to_axes(self.ax)

        self._draw_grid()
        self._draw_world_frame()

        for obj in objects:

            if self.camera.target is None:
                self.camera.follow(obj)

            nodes, edges = self._draw_tree(
                obj,
                obj.q
            )

            links = []

            for x_p, y_p, x_c, y_c in edges:
                links.append(
                    [
                        [x_p, y_p],
                        [x_c, y_c]
                    ]
                )

            links = np.array(links)
            points = np.array(nodes)

            self.links_lines = LineCollection(
                links,
                colors=self.colors[:len(links)],
                linewidths=3
            )

            self.ax.add_collection(
                self.links_lines
            )

            self.joints_circles = self.ax.scatter(
                points[:, 0],
                points[:, 1],
                c="lightblue",
                s=50,
                zorder=10
            )

            base_x, base_y = self.camera.project(
                obj.get_position()
            )

            self.base_point = self.ax.scatter(
                base_x,
                base_y,
                c="blue",
                s=70,
                zorder=10
            )

        self.ax.set_title(
            f"View: {self.camera.view_mode.name} | "
            f"Zoom: {self.camera.zoom:.2f} | "
            f"Follow: {self.follow_enabled}\n"
            f"Mouse Wheel = Zoom | "
            f"V = View | "
            f"F = Follow | "
            f"Arrows = Pan"
        )

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def close(self):

        plt.close(self.fig)
