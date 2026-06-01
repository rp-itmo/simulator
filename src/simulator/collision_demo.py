from collision.shapes import Vector2, CircleShape, RectangleShape
from collision.body import RigidBody
from collision.physics_world import PhysicsWorld


def main():

    world = PhysicsWorld()

    ball = RigidBody(
        name="Ball",
        shape=CircleShape(radius=0.5),
        position=Vector2(-3.0, 2.0),
        velocity=Vector2(2.0, 0.0),
        is_static=False,
    )

    rectangle = RigidBody(
        name="Rectangle Platform",
        shape=RectangleShape(width=3.0, height=0.5),
        position=Vector2(0.0, 0.0),
        velocity=Vector2(0.0, 0.0),
        is_static=True,
    )

    world.add_body(ball)
    world.add_body(rectangle)

    dt = 0.016

    for step in range(200):

        collisions = world.update(dt)

        for collision in collisions:

            print(f"\nStep: {step}")
            collision.print_info()


if __name__ == "__main__":
    main()
