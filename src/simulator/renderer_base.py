from abc import ABC, abstractmethod
from typing import Tuple

Color = Tuple[int, int, int]


class Primitive(ABC):
    @abstractmethod
    def draw(self, renderer: "RendererBase") -> None: ...


class RendererBase(ABC):
    def __init__(self, headless: bool = False) -> None:
        self.headless = headless

    @abstractmethod
    def draw_line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        color: Color = (0, 0, 0),
        width: float = 1.0,
    ) -> None: ...

    @abstractmethod
    def draw_circle(
        self,
        x: float,
        y: float,
        radius: float,
        color: Color = (0, 0, 0),
        filled: bool = True,
    ) -> None: ...

    @abstractmethod
    def draw_rectangle(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        color: Color = (0, 0, 0),
        filled: bool = False,
    ) -> None: ...

    @abstractmethod
    def draw_polygon(
        self,
        points: list[Tuple[float, float]],
        color: Color = (0, 0, 0),
        filled: bool = False,
    ) -> None: ...

    @abstractmethod
    def draw_text(
        self,
        x: float,
        y: float,
        content: str,
        color: Color = (0, 0, 0),
        font_size: int = 12,
    ) -> None: ...

    @abstractmethod
    def clear(self) -> None: ...

    @abstractmethod
    def render(self) -> None: ...
