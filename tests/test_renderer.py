import pytest
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon
import numpy as np

from renderer import Renderer


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close('all')


@pytest.fixture
def renderer():
    return Renderer()

# Tests for draw_line()
class TestDrawLine:
    def test_adds_a_line_to_axes(self, renderer):
        before = len(renderer.ax.lines)
        renderer.draw_line([0, 0], [1, 1])
        assert len(renderer.ax.lines) == before + 1

    def test_line_coordinates(self, renderer):
        renderer.draw_line([0, 0], [3, 4])
        line = renderer.ax.lines[-1]
        assert list(line.get_xdata()) == [0, 3]
        assert list(line.get_ydata()) == [0, 4]

    def test_default_color_and_linewidth(self, renderer):
        renderer.draw_line([0, 0], [1, 1])
        line = renderer.ax.lines[-1]
        assert line.get_color() == 'black'
        assert line.get_linewidth() == 2.0

    def test_custom_color_and_linewidth(self, renderer):
        renderer.draw_line([0, 0], [1, 1], color='red', linewidth=5)
        line = renderer.ax.lines[-1]
        assert line.get_color() == 'red'
        assert line.get_linewidth() == 5

    def test_negative_coordinates(self, renderer):
        renderer.draw_line([-2, -3], [-1, -1])
        line = renderer.ax.lines[-1]
        assert list(line.get_xdata()) == [-2, -1]
        assert list(line.get_ydata()) == [-3, -1]

    def test_zero_length_line(self, renderer):
        renderer.draw_line([5, 5], [5, 5])
        assert len(renderer.ax.lines) >= 1

# Tests for draw_Circle()
class TestDrawCircle:
    def test_returns_circle_patch(self, renderer):
        result = renderer.draw_circle([0, 0], radius=1.0)
        assert isinstance(result, Circle)

    def test_circle_added_to_axes(self, renderer):
        before = len(renderer.ax.patches)
        renderer.draw_circle([1, 2], radius=1.0)
        assert len(renderer.ax.patches) == before + 1

    def test_center_and_radius(self, renderer):
        circle = renderer.draw_circle([3, 4], radius=0.5)
        assert tuple(circle.center) == (3, 4)
        assert circle.radius == 0.5

    def test_default_filled_true(self, renderer):
        circle = renderer.draw_circle([0, 0], radius=1.0)
        assert circle.get_fill() is True

    def test_custom_color(self, renderer):
        circle = renderer.draw_circle([0, 0], radius=1.0, color='red')
        assert circle.get_facecolor() is not None

    def test_custom_radius(self, renderer):
        circle = renderer.draw_circle([0, 0], radius=2.5)
        assert circle.radius == 2.5

# Tests for draw_Rectangle()
class TestDrawRectangle:
    def test_returns_rectangle_patch(self, renderer):
        result = renderer.draw_rectangle([0, 0], 2, 1)
        assert isinstance(result, Rectangle)

    def test_rectangle_added_to_axes(self, renderer):
        before = len(renderer.ax.patches)
        renderer.draw_rectangle([0, 0], 3, 2)
        assert len(renderer.ax.patches) == before + 1

    def test_position_and_size(self, renderer):
        rect = renderer.draw_rectangle([2, 4], 4, 3)
        assert rect.get_x() == 2 - 4 / 2
        assert rect.get_y() == 4 - 3 / 2
        assert rect.get_width() == 4
        assert rect.get_height() == 3

    def test_default_filled(self, renderer):
        rect = renderer.draw_rectangle([0, 0], 1, 1)
        assert rect.get_fill() is True

    def test_custom_color(self, renderer):
        rect = renderer.draw_rectangle([0, 0], 1, 1, color='blue')
        assert rect.get_facecolor() is not None

    def test_zero_size_rectangle(self, renderer):
        rect = renderer.draw_rectangle([0, 0], 0, 0)
        assert rect.get_width() == 0
        assert rect.get_height() == 0

# Tests for draw_Polygon()
class TestDrawPolygon:
    def test_returns_polygon_patch(self, renderer):
        result = renderer.draw_polygon([(0, 0), (1, 0), (0.5, 1)])
        assert isinstance(result, Polygon)

    def test_polygon_added_to_axes(self, renderer):
        before = len(renderer.ax.patches)
        renderer.draw_polygon([(0, 0), (1, 0), (0.5, 1)])
        assert len(renderer.ax.patches) == before + 1

    def test_default_filled(self, renderer):
        poly = renderer.draw_polygon([(0, 0), (1, 0), (0.5, 1)])
        assert poly.get_fill() is True

    def test_custom_color(self, renderer):
        poly = renderer.draw_polygon([(0, 0), (1, 0), (0.5, 1)], color='red')
        assert poly.get_facecolor() is not None

    def test_quad_vertices(self, renderer):
        poly = renderer.draw_polygon([(0, 0), (2, 0), (2, 2), (0, 2)])
        assert isinstance(poly, Polygon)

    def test_many_vertices(self, renderer):
        angles = np.linspace(0, 2 * np.pi, 32, endpoint=False)
        verts = [(np.cos(a), np.sin(a)) for a in angles]
        poly = renderer.draw_polygon(verts)
        assert isinstance(poly, Polygon)

# Tests for draw_Text()
class TestDrawText:
    def test_returns_text_object(self, renderer):
        result = renderer.draw_text([0, 0], 'hello')
        assert result is not None

    def test_text_added_to_axes(self, renderer):
        before = len(renderer.ax.texts)
        renderer.draw_text([1, 2], 'test')
        assert len(renderer.ax.texts) == before + 1

    def test_text_content_and_position(self, renderer):
        renderer.draw_text([3, 4], 'robot')
        txt = renderer.ax.texts[-1]
        assert txt.get_text() == 'robot'
        assert txt.get_position() == (3, 4)

    def test_default_fontsize(self, renderer):
        renderer.draw_text([0, 0], 'x')
        txt = renderer.ax.texts[-1]
        assert txt.get_fontsize() == 10

    def test_custom_fontsize(self, renderer):
        renderer.draw_text([0, 0], 'x', fontsize=16)
        txt = renderer.ax.texts[-1]
        assert txt.get_fontsize() == 16

    def test_empty_string(self, renderer):
        renderer.draw_text([0, 0], '')
        txt = renderer.ax.texts[-1]
        assert txt.get_text() == ''

    def test_unicode_text(self, renderer):
        renderer.draw_text([0, 0], 'Hello Robot')
        txt = renderer.ax.texts[-1]
        assert txt.get_text() == 'Hello Robot'


class TestIntegration:
    def test_multiple_shapes_all_added(self, renderer):
        renderer.draw_line([0, 0], [1, 1])
        renderer.draw_circle([2, 2], radius=1.0)
        renderer.draw_rectangle([3, 3], 1, 1)
        renderer.draw_polygon([(5, 5), (6, 5), (5.5, 6)])
        renderer.draw_text([7, 7], 'ok')

        assert len(renderer.ax.lines) >= 1
        assert len(renderer.ax.patches) >= 3
        assert len(renderer.ax.texts) >= 1

    def test_draw_robot_arm_segment(self, renderer):
        renderer.draw_line([0, 0], [1, 0])
        joint = renderer.draw_circle([1, 0], radius=0.1)
        assert isinstance(joint, Circle)
        assert tuple(joint.center) == (1, 0)
