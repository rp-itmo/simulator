from enum import Enum


class ViewMode(Enum):
    TOP = "top"
    LEFT = "left"


class Camera:
    def init(self, x_limits=(-10.0, 10.0), y_limits=(-10.0, 10.0)):
        self.position = [0.0, 0.0, 0.0]
        self.zoom = 1.0
        self.view_mode = ViewMode.TOP
        self.target = None
        self.follow_smoothing = 0.25

        self.base_width = x_limits[1] - x_limits[0]
        self.base_height = y_limits[1] - y_limits[0]

    def toggle_view_mode(self):
        self.view_mode = ViewMode.LEFT if self.view_mode == ViewMode.TOP else ViewMode.TOP

    def follow(self, target):
        self.target = target

    def update(self):
        if self.target is None:
            return

        target_pos = self.target.get_position()

        for i in range(3):
            self.position[i] += (target_pos[i] - self.position[i]) * self.follow_smoothing

    def zoom_in(self):
        self.zoom = min(self.zoom * 1.25, 10.0)

    def zoom_out(self):
        self.zoom = max(self.zoom / 1.25, 0.2)

    def pan(self, dx, dy):
        dx /= self.zoom
        dy /= self.zoom

        if self.view_mode == ViewMode.TOP:
            self.position[0] += dx
            self.position[1] += dy
        else:
            self.position[0] += dx
            self.position[2] += dy

    def project(self, position):
        x, y, z = position

        if self.view_mode == ViewMode.TOP:
            return x, y

        return x, z

    def apply_to_axes(self, ax):
        cx, cy = self.project(self.position)

        half_width = self.base_width / (2.0 * self.zoom)
        half_height = self.base_height / (2.0 * self.zoom)

        ax.set_xlim(cx - half_width, cx + half_width)
        ax.set_ylim(cy - half_height, cy + half_height)
        ax.set_aspect("equal", adjustable="box")