# Robot Simulator – Core 2D Rendering Primitives #19

## Project Overview

This repository contains a 2D robot simulation environment with a Matplotlib‑based renderer.  
As part of Ticket #19, the renderer has been extended with a set of core 2D drawing primitives that can be used independently of the robot model.

These functions allow you to visualise obstacles, target points, trajectories, labels, and any other auxiliary information directly inside the simulation window.

## Team & Role

- Lead: Dennis Alexander Burdin  
- Dev: Artem Shaturnyi  
- Tester: Bashar Alahmad

## Implemented Drawing Primitives

All drawing methods are part of the `Renderer` class (`src/simulator/renderer.py`) and share a common interface:

- Accept positions as lists or tuples `[x, y]`
- Support `kwargs` to pass any Matplotlib style option
- Automatically update the canvas (`draw_idle()`)
- Return the created artist for later modifications 

Method and Description:

`draw_line(start, end, color='black', linewidth=2.0, alpha=1.0, **kwargs)` 
Line from `start` to `end`

`draw_circle(center, radius=1.0, color='lightblue', fill=True, alpha=1.0, linewidth=1.0, **kwargs)`  
Circle with given center and radius. Returns the `Circle` patch. 

`draw_rectangle(pos, width, height, angle=0.0, color='gray', fill=True, alpha=1.0, **kwargs)`  
Rectangle with center at `pos`. Width and height are full extents. Returns the `Rectangle` patch. 

`draw_polygon(vertices, color='green', fill=True, alpha=1.0, linewidth=1.0, **kwargs)` 
Polygon defined by a list of vertices `[(x1,y1), (x2,y2), ...]`. Returns the `Polygon` patch. 

`draw_text(position, text, fontsize=10, color='black', alpha=1.0, **kwargs)` 
 Text label at `position`. Returns the `Text` object. 

## Testing
All primitives are covered by 33 unit tests (see tests/test_renderer.py).

Run the tests with:
`pytest tests/test_renderer.py -v`