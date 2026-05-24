from __future__ import annotations
from unittest.mock import MagicMock
import pytest
from simulator.renderer_primitives import (
    Circle,
    Line,
    Polygon,
    Rectangle,
    Text,
)


@pytest.fixture
def renderer() -> MagicMock:
    
    return MagicMock()


class TestLine:
    def test_stores_attributes(self) -> None:
        line = Line(x1=0.0, y1=1.0, x2=5.0, y2=3.0, color=(255, 0, 0), width=2.0)

        assert (line.x1, line.y1, line.x2, line.y2) == (0.0, 1.0, 5.0, 3.0)
        assert line.color == (255, 0, 0)
        assert line.width == 2.0

    def test_uses_default_values(self) -> None:
        line = Line(x1=0.0, y1=0.0, x2=1.0, y2=1.0)

        assert line.color == (0, 0, 0)
        assert line.width == 1.0

    def test_draw_delegates_to_renderer(self, renderer: MagicMock) -> None:
        line = Line(x1=1.0, y1=2.0, x2=3.0, y2=4.0, color=(0, 255, 0), width=2.0)
        line.draw(renderer)

        renderer.draw_line.assert_called_once_with(1.0, 2.0, 3.0, 4.0, (0, 255, 0), 2.0)


class TestCircle:
    

    def test_stores_attributes(self) -> None:
        circle = Circle(x=3.0, y=4.0, radius=5.0, color=(0, 0, 255), filled=False)

        assert (circle.x, circle.y, circle.radius) == (3.0, 4.0, 5.0)
        assert circle.color == (0, 0, 255)
        assert circle.filled is False

    def test_uses_default_values(self) -> None:
        circle = Circle(x=0.0, y=0.0, radius=1.0)

        assert circle.color == (0, 0, 0)
        assert circle.filled is True

    def test_draw_delegates_to_renderer(self, renderer: MagicMock) -> None:
        circle = Circle(x=1.0, y=2.0, radius=3.0, color=(0, 0, 255), filled=False)
        circle.draw(renderer)

        renderer.draw_circle.assert_called_once_with(1.0, 2.0, 3.0, (0, 0, 255), False)


class TestRectangle:

    def test_stores_attributes(self) -> None:
        rect = Rectangle(x=1.0, y=2.0, width=10.0, height=5.0, color=(128, 128, 128), filled=True)

        assert (rect.x, rect.y, rect.width, rect.height) == (1.0, 2.0, 10.0, 5.0)
        assert rect.color == (128, 128, 128)
        assert rect.filled is True

    def test_uses_default_values(self) -> None:
        rect = Rectangle(x=0.0, y=0.0, width=1.0, height=1.0)

        assert rect.color == (0, 0, 0)
        assert rect.filled is False

    def test_draw_delegates_to_renderer(self, renderer: MagicMock) -> None:
        rect = Rectangle(x=2.0, y=3.0, width=4.0, height=5.0, color=(255, 255, 0), filled=True)
        rect.draw(renderer)

        renderer.draw_rectangle.assert_called_once_with(2.0, 3.0, 4.0, 5.0, (255, 255, 0), True)


class TestPolygon:

    def test_stores_attributes(self) -> None:
        points = [(0.0, 0.0), (2.0, 0.0), (1.0, 2.0)]
        poly = Polygon(points=points, color=(100, 200, 50), filled=True)

        assert poly.points == points
        assert poly.color == (100, 200, 50)
        assert poly.filled is True

    def test_uses_default_values(self) -> None:
        poly = Polygon()

        assert poly.points == []
        assert poly.color == (0, 0, 0)
        assert poly.filled is False

    def test_default_points_are_not_shared_between_instances(self) -> None:
        poly1 = Polygon()
        poly2 = Polygon()
        poly1.points.append((1.0, 2.0))
        assert poly2.points == []

    def test_draw_delegates_to_renderer(self, renderer: MagicMock) -> None:
        points = [(0.0, 0.0), (2.0, 0.0), (1.0, 2.0)]
        poly = Polygon(points=points, color=(100, 200, 50), filled=True)

        poly.draw(renderer)

        renderer.draw_polygon.assert_called_once_with(points, (100, 200, 50), True)


class TestText:

    def test_stores_attributes(self) -> None:
        text = Text(x=5.0, y=10.0, content="hello", color=(255, 255, 255), font_size=24)

        assert (text.x, text.y) == (5.0, 10.0)
        assert text.content == "hello"
        assert text.color == (255, 255, 255)
        assert text.font_size == 24

    def test_uses_default_values(self) -> None:
        text = Text(x=0.0, y=0.0)

        assert text.content == ""
        assert text.color == (0, 0, 0)
        assert text.font_size == 12

    def test_draw_delegates_to_renderer(self, renderer: MagicMock) -> None:
        text = Text(x=1.0, y=2.0, content="joint_1", color=(0, 0, 0), font_size=14)
        text.draw(renderer)

        renderer.draw_text.assert_called_once_with(1.0, 2.0, "joint_1", (0, 0, 0), 14)
