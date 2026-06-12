"""Matplotlib-based renderer for robot simulations."""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

from .video_recorder import VideoRecorder, create_recorder


class Renderer:
    """Matplotlib-based renderer with video recording support."""

    def __init__(
        self,
        x_limits=(-10.0, 10.0),
        y_limits=(-10.0, 10.0),
        max_colors=20,
        record_path: str | None = None,
        record_fps: float = 30.0,
        record_format: str | None = None,
    ) -> None:
        """Initialize the renderer.

        Args:
            x_limits: Horizontal axis limits (min, max).
            y_limits: Vertical axis limits (min, max).
            max_colors: Maximum number of colors for robot links.
            record_path: If set, enable recording to this file path.
            record_fps: Frame rate for video recording.
            record_format: Recording format ("mp4" or "avi"). Auto-detected if None.
        """
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, aspect="equal")
        self.ax.set_xlim(x_limits)
        self.ax.set_ylim(y_limits)
        self.ax.set_aspect("equal")

        # world frame
        self.ax.annotate(
            "",
            xy=(x_limits[1] / 10, 0),
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color="red", alpha=0.5),
        )
        self.ax.annotate(
            "",
            xy=(0, y_limits[1] / 10),
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color="green", alpha=0.5),
        )

        plt.show(block=False)

        self.links_lines = None
        self.joints_circles = None
        self.colors = plt.cm.rainbow(np.linspace(0, 1, max_colors))

        self.base_patch = None

        # Video recording setup (deferred until first frame size is known)
        self._recorder: VideoRecorder | None = None
        self._record_enabled = record_path is not None
        self._record_path = record_path
        self._record_fps = record_fps
        self._record_format = record_format

    def _start_recording_if_needed(self, frame_size: tuple[int, int]) -> None:
        """Start recording if enabled and not already started.

        Args:
            frame_size: (width, height) of the frame.
        """
        if self._recorder is None and self._record_enabled:
            self._recorder = create_recorder(
                output_path=self._record_path,
                fps=self._record_fps,
                format=self._record_format,
            )
            self._recorder.start(frame_size)

    def update(self, objects, dt=0.0001):
        """Update the visualization and optionally record frames.

        Args:
            objects: List of robot objects to render.
            dt: Time step (for reference, not used in rendering).
        """
        if not objects:
            return

        all_links = []
        all_points = []

        def draw_tree(obj, q):
            parents = obj.model["parent"]
            nodes = []
            edges = []
            angles = [0.0] * len(parents)

            length = 1.0

            for i in range(len(parents)):
                parent = parents[i]

                if parent == -1:
                    x_p, y_p = 0.0, 0.0
                    angles[i] = q[i]
                else:
                    x_p, y_p = nodes[parent]
                    angles[i] = angles[parent] + q[i]

                x_child = x_p + length * np.cos(angles[i])
                y_child = y_p + length * np.sin(angles[i])

                nodes.append((x_child, y_child))
                edges.append((x_p, y_p, x_child, y_child))

            return nodes, edges

        for obj in objects:
            links = []
            points = []

            nodes, edges = draw_tree(obj, obj.q)

            for edge in edges:
                x_p, y_p, x_c, y_c = edge
                links.append([[x_p, y_p], [x_c, y_c]])

            links = np.array(links)
            points = np.array(nodes)

            all_links.append(links)
            all_points.append(points)

            if self.links_lines is None:
                self.links_lines = LineCollection(links, colors=self.colors, linewidths=3)
                self.ax.add_collection(self.links_lines)

                self.joints_circles = self.ax.scatter(
                    points[:, 0], points[:, 1], c="lightblue", s=40, zorder=10
                )
                self.ax.scatter(0.0, 0.0, c="blue", s=50, zorder=10)
            else:
                self.links_lines.set_segments(links)
                self.joints_circles.set_offsets(points)

        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()

        # Record frame if recording is enabled
        if self._record_enabled:
            frame = np.array(self.fig.canvas.buffer_rgba())
            height, width = frame.shape[:2]
            frame_size = (width, height)
            self._start_recording_if_needed(frame_size)

            if self._recorder is not None and self._recorder.is_recording():
                self._recorder.add_frame(frame)

    def close(self):
        """Close the renderer and finalize video recording."""
        if self._recorder is not None and self._recorder.is_recording():
            self._recorder.stop()
        plt.close(self.fig)

    def is_recording(self) -> bool:
        """Check if video recording is active."""
        return self._recorder is not None and self._recorder.is_recording()