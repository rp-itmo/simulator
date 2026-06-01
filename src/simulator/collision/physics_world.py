from .shapes import Vector2
from .collision_system import CollisionSystem


class PhysicsWorld:

    def __init__(self, gravity=None):

        self.gravity = gravity if gravity is not None else Vector2(0.0, -9.81)

        self.bodies = []

        self.collision_system = CollisionSystem()

    def add_body(self, body):
        self.bodies.append(body)

    def update(self, dt):

        for body in self.bodies:

            if not body.is_static:
                body.velocity = body.velocity + self.gravity * dt
                body.update(dt)

        return self.collision_system.detect_collisions(
            self.bodies
        )
