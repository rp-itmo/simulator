import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon  # Added Polygon
from matplotlib.collections import LineCollection


class Renderer:
    def __init__(self, x_limits=(-10.0, 10.0), y_limits=(-10.0, 10.0), max_colors=20) -> None:
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, aspect="equal")
        self.ax.set_xlim(x_limits)
        self.ax.set_ylim(y_limits)
        self.ax.set_aspect("equal")

        # world frame
        self.ax.annotate(
            "",
            xy=(x_limits[1] / 10, 0),
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color="red", alpha=0.5),
        )
        self.ax.annotate(
            "",
            xy=(0, y_limits[1] / 10),
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color="green", alpha=0.5),
        )

        plt.show(block=False)

        self.links_lines = None
        self.joints_circles = None
        self.colors = plt.cm.rainbow(np.linspace(0, 1, max_colors))

        self.base_patch = None

    # New functions for drawing primitives

    def clear(self):
        """Clears the current drawing, resetting the axes for the next frame."""
        self.ax.cla()
        # Reset limits and aspect ratio after clearing
        self.ax.set_xlim(-self.view_size, self.view_size)
        self.ax.set_ylim(-self.view_size, self.view_size)
        self.ax.set_aspect("equal")
        
        # Redraw world frame axes
        self.ax.axhline(0, color='black', lw=1, alpha=0.2)
        self.ax.axvline(0, color='black', lw=1, alpha=0.2)

    def draw_line(self, start, end, color='black', linewidth=2.0, alpha=1.0, **kwargs):
        """Draws a line between two points [x,y]."""
        self.ax.plot([start[0], end[0]], [start[1], end[1]],
                    color=color, linewidth=linewidth, alpha=alpha, **kwargs)
        self.fig.canvas.draw_idle()
    
   
    def draw_circle(self, center, radius=1.0, color='lightblue', fill=True,
                    alpha=1.0, linewidth=1.0, **kwargs):
        """Draws a circle with given center [x,y] and radius."""
        circle = Circle((center[0], center[1]), radius=radius,
                        color=color, fill=fill, alpha=alpha,
                        linewidth=linewidth, **kwargs)
        self.ax.add_patch(circle)
        self.fig.canvas.draw_idle()
        return circle

    def draw_rectangle(self, pos, width, height, angle=0.0, color='gray',
                       fill=True, alpha=1.0, **kwargs):
        """
        Draws a rectangle with center at `pos` (list/tuple [x,y]).
        Width and height specify the dimensions.
        """
        x = pos[0] - width / 2
        y = pos[1] - height / 2
        rect = Rectangle((x, y), width, height, angle=angle,
                        facecolor=color if fill else 'none',
                        edgecolor=color, fill=fill, alpha=alpha, **kwargs)
        self.ax.add_patch(rect)
        self.fig.canvas.draw_idle()
        return rect

    def draw_polygon(self, vertices, color='green', 
                     fill=True, alpha=1.0, linewidth=1.0, **kwargs):
        """Draws a polygon from a list of vertices [(x1,y1), ...]."""
        poly = Polygon(vertices, facecolor=color if fill else 'none', 
                       edgecolor=color, fill=fill, alpha=alpha, 
                       linewidth=linewidth, **kwargs)
        self.ax.add_patch(poly)
        self.fig.canvas.draw_idle()
        return poly
    

    def draw_text(self, position, text, fontsize=10, color='black', alpha=1.0, **kwargs):
        """Draws text at position [x,y]."""
        txt = self.ax.text(position[0], position[1], text, 
                           fontsize=fontsize, color=color, alpha=alpha, **kwargs)
        self.fig.canvas.draw_idle()
        return txt

    # End of new functions for drawing primitives

    def update(self, objects, dt=0.0001):

        if not objects:
            return

        all_links = []
        all_points = []

        def draw_tree(obj, q):
            parents = obj.model["parent"]
            nodes = []
            edges = []
            angles = [0.0] * len(parents)

            length = 1.0

            for i in range(len(parents)):
                parent = parents[i]

                if parent == -1:
                    x_p, y_p = 0.0, 0.0
                    angles[i] = q[i]
                else:
                    x_p, y_p = nodes[parent]
                    angles[i] = angles[parent] + q[i]

                x_child = x_p + length * np.cos(angles[i])
                y_child = y_p + length * np.sin(angles[i])

                nodes.append((x_child, y_child))
                edges.append((x_p, y_p, x_child, y_child))

            return nodes, edges

        for obj in objects:
            links = []
            points = []

            nodes, edges = draw_tree(obj, obj.q)

            for edge in edges:
                x_p, y_p, x_c, y_c = edge
                links.append([[x_p, y_p], [x_c, y_c]])

            links = np.array(links)
            points = np.array(nodes)

            all_links.append(links)
            all_points.append(points)

            if self.links_lines is None:
                self.links_lines = LineCollection(links, colors=self.colors, linewidths=3)
                self.ax.add_collection(self.links_lines)

                self.joints_circles = self.ax.scatter(points[:, 0], points[:, 1], c="lightblue", s=40, zorder=10)
                self.ax.scatter(0.0, 0.0, c="blue", s=50, zorder=10)
            else:
                self.links_lines.set_segments(links)
                self.joints_circles.set_offsets(points)

        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()

    def close(self):
        plt.close(self.fig)