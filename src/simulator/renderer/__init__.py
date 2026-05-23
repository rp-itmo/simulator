import numpy as np
from .camera import Camera


class Renderer:
    """
    Main Renderer interface wrapping a Camera and a specific graphics Backend.
    """

    def __init__(self, backend_type="matplotlib", camera=None, **kwargs):
        if camera is None:
            self.camera = Camera()
        else:
            self.camera = camera

        if backend_type == "matplotlib":
            from .backends.matplotlib_backend import MatplotlibBackend
            self.backend = MatplotlibBackend()
        elif backend_type == "headless":
            from .backends.headless_backend import HeadlessBackend
            self.backend = HeadlessBackend()
        else:
            raise ValueError(f"Unknown backend type: {backend_type}")

        self.backend.init(**kwargs)

    def update(self, objects, dt=0.0001):
        """
        Draws a list of objects and refreshes the frame.
        Usually called periodically by the simulation loop.
        """
        self.backend.clear()

        for obj in objects:
            self._draw_object(obj)

        self.backend.render()

    def _draw_object(self, obj):
        # Cleanly support user objects implementing their own custom draw logic based on abstract primitives
        if hasattr(obj, "draw"):
            obj.draw(self)
        # Fallback to standard generic tree structure logic if it matches legacy spec
        elif hasattr(obj, "model") and "parent" in obj.model:
            self._draw_robot_tree(obj)

    def _draw_robot_tree(self, obj):
        parents = obj.model["parent"]
        nodes = []
        angles = [0.0] * len(parents)
        length = 1.0
        q = obj.q

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

            start = (x_p, y_p)
            end = (x_child, y_child)

            # Dispatch to generic primitive drawers
            self.draw_line(start, end, color="blue", width=3)
            # Draw joint
            if parent != -1:
                self.draw_circle(start, radius=0.15, color="lightblue")

        # Draw end effectors/leafs
        for pt in nodes:
            self.draw_circle(pt, radius=0.15, color="lightblue")

    # --- Public Abstract Shapes Drawing API ---
    # Objects like Terrains, Walls, chained robots can use these primitives.

    def draw_line(self, start, end, color="black", width=1):
        start_cm = self.camera.apply(start)
        end_cm = self.camera.apply(end)
        self.backend.draw_line(start_cm, end_cm, color, width)

    def draw_circle(self, center, radius, color="blue"):
        r_cm = radius * self.camera.scale
        self.backend.draw_circle(self.camera.apply(center), r_cm, color)

    def draw_box(self, center, width, height, angle=0.0, color="green"):
        w_cm = width * self.camera.scale
        h_cm = height * self.camera.scale
        self.backend.draw_box(self.camera.apply(center),
                              w_cm, h_cm, angle, color)

    def close(self):
        """Clean up rendering resources."""
        self.backend.close()
