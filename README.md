# Simulator

A 2D robot physics simulator.

## Project Structure

src/simulator/
├── renderer_base.py        # Abstract base classes for renderer and primitives
├── renderer_primitives.py  # 2D shape data classes (Line, Circle, Rectangle, Polygon, Text)
├── renderer.py             # Matplotlib renderer implementation
├── physics.py              # Physics engine
├── objects.py              # Robot objects
├── world.py                # Simulation world
└── controller.py           # Robot controller
tests/
├── test_renderer_primitives.py  # Tests for primitive classes
└── test_fb_dynamics.py          # Tests for floating base dynamics


## Renderer Architecture

`RendererBase` is an abstract class that defines the interface for all rendering backends. Any backend (Matplotlib, Pygame, etc.) must implement:

- `draw_line`
- `draw_circle`
- `draw_rectangle`
- `draw_polygon`
- `draw_text`
- `clear`
- `render`

Each drawable shape inherits from `Primitive` and implements a `draw(renderer)` method.

## Running Tests

```bash
nox
```
