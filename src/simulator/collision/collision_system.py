from .broad_phase import BroadPhaseDetector
from .narrow_phase import NarrowPhaseDetector


class CollisionSystem:

    def __init__(self):
        self.broad_phase = BroadPhaseDetector()
        self.narrow_phase = NarrowPhaseDetector()

    def detect_collisions(self, bodies):

        collisions = []

        candidate_pairs = self.broad_phase.find_candidate_pairs(bodies)

        for body_a, body_b in candidate_pairs:

            collision = self.narrow_phase.check_collision(
                body_a,
                body_b
            )

            if collision is not None:
                collisions.append(collision)

        return collisions
