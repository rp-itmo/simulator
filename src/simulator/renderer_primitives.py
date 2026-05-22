from __future__ import annotations
from dataclasses import dataclass, field
from typing import Tuple

from simulator.renderer_base import Primitive, RendererBase

Color = Tuple[int, int, int]


@dataclass
class Line(Primitive):
    x1: float
    y1: float
    x2: float
    y2: float
    color: Color = (0, 0, 0)
    width: float = 1.0

    def draw(self, renderer: RendererBase) -> None:
        renderer.draw_line(self.x1, self.y1, self.x2, self.y2, self.color, self.width)


@dataclass
class Circle(Primitive):
    x: float
    y: float
    radius: float
    color: Color = (0, 0, 0)
    filled: bool = True

    def draw(self, renderer: RendererBase) -> None:
        renderer.draw_circle(self.x, self.y, self.radius, self.color, self.filled)


@dataclass
class Rectangle(Primitive):
    x: float
    y: float
    width: float
    height: float
    color: Color = (0, 0, 0)
    filled: bool = False

    def draw(self, renderer: RendererBase) -> None:
        renderer.draw_rectangle(self.x, self.y, self.width, self.height, self.color, self.filled)


@dataclass
class Polygon(Primitive):
    points: list[Tuple[float, float]] = field(default_factory=list)
    color: Color = (0, 0, 0)
    filled: bool = False

    def draw(self, renderer: RendererBase) -> None:
        renderer.draw_polygon(self.points, self.color, self.filled)


@dataclass
class Text(Primitive):
    x: float
    y: float
    content: str = ""
    color: Color = (0, 0, 0)
    font_size: int = 12

    def draw(self, renderer: RendererBase) -> None:
        renderer.draw_text(self.x, self.y, self.content, self.color, self.font_size)
