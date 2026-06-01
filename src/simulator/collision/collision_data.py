from dataclasses import dataclass

from .body import RigidBody
from .shapes import Vector2


@dataclass
class CollisionData:
    body_a: RigidBody
    body_b: RigidBody
    contact_point: Vector2
    normal: Vector2
    penetration_depth: float

    def print_info(self) -> None:
        print("\n========== COLLISION DATA ==========")
        print(f"Pair: {self.body_a.name} <-> {self.body_b.name}")
        print(
            f"Contact Point: "
            f"({self.contact_point.x:.3f}, {self.contact_point.y:.3f})"
        )
        print(
            f"Normal: "
            f"({self.normal.x:.3f}, {self.normal.y:.3f})"
        )
        print(
            f"Penetration Depth: "
            f"{self.penetration_depth:.3f}"
        )
