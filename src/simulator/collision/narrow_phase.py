from .shapes import CircleShape, RectangleShape, Vector2, clamp
from .collision_data import CollisionData


class NarrowPhaseDetector:
    def check_collision(self, body_a, body_b):

        if isinstance(body_a.shape, CircleShape) and isinstance(body_b.shape, RectangleShape):
            return self._circle_rectangle(body_a, body_b)

        if isinstance(body_a.shape, RectangleShape) and isinstance(body_b.shape, CircleShape):

            collision = self._circle_rectangle(body_b, body_a)

            if collision is None:
                return None

            return CollisionData(
                body_a=body_a,
                body_b=body_b,
                contact_point=collision.contact_point,
                normal=collision.normal * -1,
                penetration_depth=collision.penetration_depth,
            )

        return None

    def _circle_rectangle(self, circle_body, rect_body):

        circle = circle_body.shape
        rect = rect_body.shape

        half_width = rect.width / 2.0
        half_height = rect.height / 2.0

        circle_center = circle_body.position
        rect_center = rect_body.position

        closest_x = clamp(
            circle_center.x,
            rect_center.x - half_width,
            rect_center.x + half_width,
        )

        closest_y = clamp(
            circle_center.y,
            rect_center.y - half_height,
            rect_center.y + half_height,
        )

        closest_point = Vector2(closest_x, closest_y)

        difference = circle_center - closest_point
        distance = difference.length()

        if distance > circle.radius:
            return None

        if distance == 0:
            normal = Vector2(0.0, 1.0)
            penetration = circle.radius
        else:
            normal = difference.normalized()
            penetration = circle.radius - distance

        return CollisionData(
            body_a=circle_body,
            body_b=rect_body,
            contact_point=closest_point,
            normal=normal,
            penetration_depth=penetration,
        )
