from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
import math


@dataclass
class Vector2:
    x: float
    y: float

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float):
        return Vector2(self.x * scalar, self.y * scalar)

    def length(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y)

    def normalized(self):
        length = self.length()
        if length == 0:
            return Vector2(0.0, 0.0)
        return Vector2(self.x / length, self.y / length)


def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(value, max_value))


class CollisionShape(ABC):
    @abstractmethod
    def get_type(self) -> str:
        pass


@dataclass
class CircleShape(CollisionShape):
    radius: float

    def get_type(self) -> str:
        return "Circle"


@dataclass
class RectangleShape(CollisionShape):
    width: float
    height: float

    def get_type(self) -> str:
        return "Rectangle"


@dataclass
class PolygonShape(CollisionShape):
    vertices: List[Vector2]

    def get_type(self) -> str:
        return "Polygon"
