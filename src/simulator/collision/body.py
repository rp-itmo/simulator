from dataclasses import dataclass

from .shapes import CollisionShape, Vector2


@dataclass
class RigidBody:
    name: str
    shape: CollisionShape
    position: Vector2
    velocity: Vector2
    is_static: bool = False

    def update(self, dt: float) -> None:
        if self.is_static:
            return

        self.position = self.position + self.velocity * dt
