import pytest
from renderer import Renderer

from objects import CartPole

class TestRendererBackend:
    REQUIRED_METHODS = {'update', '_draw_object', '_draw_robot_tree', 'draw_line', 'draw_circle', 'draw_box', 'close'}
    
    @pytest.mark.parametrize('method_name', REQUIRED_METHODS)
    def test_method_exists(self, method_name):
        assert hasattr(Renderer, method_name)
    
    @pytest.mark.parametrize('method_name', REQUIRED_METHODS)
    def test_method_implements(self, method_name):
        assert callable(getattr(Renderer, method_name))


    def test_unknown_backend_error_is_raised(self):
        with pytest.raises(ValueError):
            Renderer("bla bla bla - unknown backend type")
    
    def test_headless_option_exists(self):
        try: 
            renderer = Renderer("headless")
        except ValueError:
            assert(False)
        else:
            assert(True)
    
    def test_common_use_no_errors(self):
        try:
            renderer = Renderer("headless")
            renderer.draw_box((2,3), 10, 15, 5, "green")
            renderer.draw_circle((3,5), 5, "blue")
            renderer.draw_line((1,1), (5,5), "black", 4)
            robot = CartPole()
            renderer.update([robot])
            renderer.close()
        except:
            assert(False)
        else:
            assert(True)