from .base import RendererBackend


class HeadlessBackend(RendererBackend):
    """
    Headless renderer backend for fast simulation 
    without any UI/graphical overhead (e.g. for RL training/CI).
    """

    def init(self, x_limits=(-10.0, 10.0), y_limits=(-10.0, 10.0), **kwargs):
        pass

    def clear(self):
        pass

    def draw_line(self, start, end, color="black", width=1):
        pass

    def draw_circle(self, center, radius, color="blue"):
        pass

    def draw_box(self, center, width, height, angle=0.0, color="green"):
        pass

    def render(self):
        pass

    def close(self):
        pass
