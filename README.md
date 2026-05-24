# Simulator

A 2D robot physics simulator.

## Project Structure

```
src/simulator/
├── renderer_base.py        
├── renderer_primitives.py  
├── renderer.py             
├── physics.py              
├── objects.py              
├── world.py                
└── controller.py           

tests/
├── test_renderer_primitives.py  
└── test_fb_dynamics.py          
```


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
