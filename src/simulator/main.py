import time
import matplotlib.pyplot as plt

from renderer import Renderer
from world import World


def main():
    renderer = Renderer()
    world = World()

    try:
        while plt.fignum_exists(renderer.fig.number):
            world.update()
            renderer.update(world.get_objects())
            time.sleep(0.02)

    except KeyboardInterrupt:
        pass

    finally:
        renderer.close()


if __name__ == "__main__":
    main()
