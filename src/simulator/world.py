import time


class World:
    """Simulation world managing physics and rendering.

    Coordinates the simulation loop, physics updates, and rendering.
    """
    def __init__(
        self,
        physics,
        renderer,
        record_path: str | None = None,
        record_fps: float = 30.0,
        record_format: str | None = None,
    ):
        """Initialize the world.

        Args:
            physics: Physics engine for dynamics simulation
            renderer: Renderer for visualization
            record_path: If set, enable recording to this file path
            record_fps: Frame rate for video recording
            record_format: Recording format ("mp4" or "avi")
        """
        self.physics = physics
        self.renderer = renderer
        self.objects = []
        self.time = 0
        self.dt = 0.02

    def set_plane(self, plane):
        self.plane = plane

    def add_object(self, obj):
        self.objects.append(obj)

    def step(self, i):
        self.physics.update(self.objects, self.dt)
        if i % 2 == 0:
            self.renderer.update(self.objects)
        self.time += self.dt

    def run(self, steps):
        for i in range(steps):
            self.step(i)
            time.sleep(self.dt)
