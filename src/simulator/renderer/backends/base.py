from abc import ABC, abstractmethod


class RendererBackend(ABC):
    """
    Clear abstract Renderer interface / base class.
    Defines the contract for pluggable drawing backends (Matplotlib, Pygame, OpenGL, Headless, etc.).
    """

    @abstractmethod
    def init(self, x_limits=(-10.0, 10.0), y_limits=(-10.0, 10.0), **kwargs):
        """Initialize the rendering backend, window, limits, etc."""
        pass

    @abstractmethod
    def clear(self):
        """Prepare for drawing a new frame by clearing the previous artifacts."""
        pass

    @abstractmethod
    def draw_line(self, start, end, color="black", width=1):
        """
        Draw a line segment.

        Args:
            start (tuple): (x, y) start point.
            end (tuple): (x, y) end point.
            color (str or tuple): Color specification.
            width (float): Line width.
        """
        pass

    @abstractmethod
    def draw_circle(self, center, radius, color="blue"):
        """
        Draw a circle (for joints, floating bases, etc.).

        Args:
            center (tuple): (x, y) center position.
            radius (float): Radius of the circle.
            color (str or tuple): Color specification.
        """
        pass

    @abstractmethod
    def draw_box(self, center, width, height, angle=0.0, color="green"):
        """
        Draw a rectangle or box (for terrains, walls-obstacles).

        Args:
            center (tuple): (x, y) geometric center of the box.
            width (float): Total width.
            height (float): Total height.
            angle (float): Rotation angle in radians from horizontal axis.
            color (str or tuple): Color specification.
        """
        pass

    @abstractmethod
    def render(self):
        """Update the screen/buffer with the queued shapes."""
        pass

    @abstractmethod
    def close(self):
        """Cleanup, close windows, or destroy contexts."""
        pass
