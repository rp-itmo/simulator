import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/simulator')))

from physics import PhysicsEngine
from pygame_renderer import PygameRenderer
from world import World
from objects import CartPole
from dynamics.ab_algorithm import ABAlgorithm

def test_pygame_renderer_fps(monkeypatch):
    fd_solver = ABAlgorithm()
    physics = PhysicsEngine(fd_solver, gravity=[0.0, -9.81, 0.0])
    renderer = PygameRenderer()
    world = World(physics, renderer)
    world.add_object(CartPole())

    monkeypatch.setattr("world.time.sleep", lambda dt: None)

    steps = 500
    start_time = time.perf_counter()
    world.run(steps)
    end_time = time.perf_counter()

    total_time = end_time - start_time
    fps = steps / total_time
    
    renderer.close()
    
    print(f"\n[Benchmark] Pygame FPS: {fps:.2f}")
    assert fps > 100, f"Hiệu năng quá thấp: {fps:.2f} FPS"