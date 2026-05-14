import pygame
import numpy as np
import sys
import colorsys
import os
import tkinter as tk
from tkinter import filedialog

class PygameRenderer:
    def __init__(self, x_limits=(-10.0, 10.0), y_limits=(-10.0, 10.0), max_colors=20):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 14) 
        
        # Configure display window
        self.width = 800
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pygame Backend (Scroll: Zoom | Drag: Pan | R: Reset | S: Save)")
        
        # Configure Margins
        self.margin_left = 60
        self.margin_right = 30
        self.margin_top = 30
        self.margin_bottom = 50
        
        # Save original state for the Reset feature (R key)
        self.orig_x_limits = list(x_limits)
        self.orig_y_limits = list(y_limits)
        # Current coordinate limits
        self.x_limits = list(x_limits)
        self.y_limits = list(y_limits)
        
        # State variables for Mouse Events
        self.is_panning = False
        self.last_mouse_pos = (0, 0)
        
        # Color Palette for robot links
        self.colors = []
        for i in range(max_colors):
            hue = i / max_colors
            r, g, b = colorsys.hsv_to_rgb(hue, 0.9, 0.9)
            self.colors.append((int(r * 255), int(g * 255), int(b * 255)))

    def _get_plot_dims(self):
        """Calculate the actual size of the plot area (excluding margins)"""
        pw = self.width - self.margin_left - self.margin_right
        ph = self.height - self.margin_top - self.margin_bottom
        return pw, ph

    def _to_screen(self, x, y):
        """
        Coordinate Mapping: WORLD -> SCREEN
        Convert real-world coordinates (meters) to screen coordinates (pixels)
        """
        pw, ph = self._get_plot_dims()
        screen_x = self.margin_left + (x - self.x_limits[0]) / (self.x_limits[1] - self.x_limits[0]) * pw
        screen_y = self.margin_top + (self.y_limits[1] - y) / (self.y_limits[1] - self.y_limits[0]) * ph
        return int(screen_x), int(screen_y)
    
    def _to_world(self, screen_x, screen_y):
        """
        Coordinate Mapping: SCREEN -> WORLD
        Determine real-world coordinates from mouse position (used for Zoom/Pan)
        """
        pw, ph = self._get_plot_dims()
        x = self.x_limits[0] + (screen_x - self.margin_left) / pw * (self.x_limits[1] - self.x_limits[0])
        y = self.y_limits[1] - (screen_y - self.margin_top) / ph * (self.y_limits[1] - self.y_limits[0])
        return x, y

    def _zoom(self, zoom_factor, mouse_pos):
        """Zoom simulation space, centered on the mouse cursor position"""
        mx, my = self._to_world(*mouse_pos)
        self.x_limits[0] = mx - (mx - self.x_limits[0]) * zoom_factor
        self.x_limits[1] = mx + (self.x_limits[1] - mx) * zoom_factor
        self.y_limits[0] = my - (my - self.y_limits[0]) * zoom_factor
        self.y_limits[1] = my + (self.y_limits[1] - my) * zoom_factor

    def _pan(self, dx, dy):
        """Shift camera view via mouse dragging"""
        pw, ph = self._get_plot_dims()
        w_world = self.x_limits[1] - self.x_limits[0]
        h_world = self.y_limits[1] - self.y_limits[0]
        
        dx_world = (dx / pw) * w_world
        dy_world = (dy / ph) * h_world
        
        self.x_limits[0] -= dx_world
        self.x_limits[1] -= dx_world
        self.y_limits[0] += dy_world
        self.y_limits[1] += dy_world

    def _get_optimal_step(self, view_range, max_ticks=8):
        raw_step = view_range / max_ticks
        magnitude = 10 ** np.floor(np.log10(raw_step)) 
        normalized = raw_step / magnitude
        
        if normalized < 1.5: step = 1.0
        elif normalized < 3.5: step = 2.0
        elif normalized < 7.5: step = 5.0
        else: step = 10.0
        
        return step * magnitude

    def _draw_axes(self):
        """Draw Bounding Box, Grid lines, and numerical Labels"""
        grid_color = (235, 235, 235)
        text_color = (0, 0, 0)
        box_color = (0, 0, 0)
        
        # Rectangle defining the exact drawing area (respecting margins)
        plot_rect = pygame.Rect(self.margin_left, self.margin_top, 
                                self.width - self.margin_left - self.margin_right, 
                                self.height - self.margin_top - self.margin_bottom)
        # Calculate grid step size for X and Y axes
        step_x = self._get_optimal_step(self.x_limits[1] - self.x_limits[0])
        step_y = self._get_optimal_step(self.y_limits[1] - self.y_limits[0])

        # Draw axis X
        start_x = np.ceil(self.x_limits[0] / step_x) * step_x
        for x in np.arange(start_x, self.x_limits[1] + step_x/2, step_x): 
            sx, _ = self._to_screen(x, 0)
            if self.margin_left <= sx <= self.width - self.margin_right:
                # draw grid line
                pygame.draw.line(self.screen, grid_color, (sx, self.margin_top), (sx, self.height - self.margin_bottom), 1)
                # draw tick line
                pygame.draw.line(self.screen, box_color, (sx, self.height - self.margin_bottom), (sx, self.height - self.margin_bottom + 5), 1)
                # draw number
                txt = self.font.render(f"{x:g}", True, text_color)
                self.screen.blit(txt, (sx - txt.get_width() // 2, self.height - self.margin_bottom + 10))

        # Draw axis Y
        start_y = np.ceil(self.y_limits[0] / step_y) * step_y
        for y in np.arange(start_y, self.y_limits[1] + step_y/2, step_y):
            _, sy = self._to_screen(0, y)
            if self.margin_top <= sy <= self.height - self.margin_bottom:
                # draw grid line
                pygame.draw.line(self.screen, grid_color, (self.margin_left, sy), (self.width - self.margin_right, sy), 1)
                # draw tick line
                pygame.draw.line(self.screen, box_color, (self.margin_left - 5, sy), (self.margin_left, sy), 1)
                # draw number
                txt = self.font.render(f"{y:g}", True, text_color)
                self.screen.blit(txt, (self.margin_left - txt.get_width() - 10, sy - txt.get_height() // 2))

        # ox, oy = self._to_screen(0, 0)
        # if self.margin_left <= ox <= self.width - self.margin_right:
        #     pygame.draw.line(self.screen, (150, 150, 150), (ox, self.margin_top), (ox, self.height - self.margin_bottom), 2)
        # if self.margin_top <= oy <= self.height - self.margin_bottom:
        #     pygame.draw.line(self.screen, (150, 150, 150), (self.margin_left, oy), (self.width - self.margin_right, oy), 2)

        pygame.draw.rect(self.screen, box_color, plot_rect, 1)

    def _save_figure(self):
        """Open Native OS Dialog to save screenshot"""
        root = tk.Tk()
        root.withdraw()
        
        root.attributes('-topmost', True)
        # Call Save As dialog
        file_path = filedialog.asksaveasfilename(
            title="Save the figure (Save As)",
            initialfile="simulator_figure.png",
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpg;*.jpeg"),
                ("Bitmap Image", "*.bmp"),
                ("All Files", "*.*")
            ]
        )
        
        root.destroy()
        
        if file_path:
            try:
                pygame.image.save(self.screen, file_path)
                print(f"[Pygame] Successfully saved figure at: {os.path.abspath(file_path)}")
            except Exception as e:
                print(f"[Pygame] ERROR: Could not save figure. Details: {e}")
        else:
            print("[Pygame] Figure save cancelled.")

    def update(self, objects, dt=0.0001):

        # EVENT POLLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Mouse events (Zoom & Pan)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: self._zoom(0.8, event.pos)
                elif event.button == 5: self._zoom(1.25, event.pos)
                elif event.button == 1: 
                    self.is_panning = True
                    self.last_mouse_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: self.is_panning = False

            elif event.type == pygame.MOUSEMOTION:
                if getattr(self, 'is_panning', False):
                    dx = event.pos[0] - self.last_mouse_pos[0]
                    dy = event.pos[1] - self.last_mouse_pos[1]
                    self._pan(dx, dy)
                    self.last_mouse_pos = event.pos

            # Keyboard events (Reset & Save) 
            elif event.type == pygame.KEYDOWN:
                char = event.unicode.lower()
                if event.key == pygame.K_r or char in ('r', 'к'):
                    self.x_limits = list(self.orig_x_limits)
                    self.y_limits = list(self.orig_y_limits)
                elif event.key == pygame.K_s or char in ('s', 'ы'):
                    self._save_figure()

        # DRAW ENVIRONMENT
        self.screen.fill((255, 255, 255))
        self._draw_axes()

        if not objects:
            pygame.display.flip()
            return

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

        # Clipping to ensure drawing only happens within the plot area
        plot_rect = pygame.Rect(self.margin_left, self.margin_top, 
                                self.width - self.margin_left - self.margin_right, 
                                self.height - self.margin_top - self.margin_bottom)
        self.screen.set_clip(plot_rect)

        # DRAW ROBOT
        origin = self._to_screen(0, 0)
        for obj in objects:
            nodes, edges = draw_tree(obj, obj.q)
            for i, edge in enumerate(edges):
                x_p, y_p, x_c, y_c = edge
                p_screen = self._to_screen(x_p, y_p)
                c_screen = self._to_screen(x_c, y_c)
                color = self.colors[i % len(self.colors)]
                pygame.draw.line(self.screen, color, p_screen, c_screen, 6)

            for node in nodes:
                n_screen = self._to_screen(node[0], node[1])
                pygame.draw.circle(self.screen, (173, 216, 230), n_screen, 10)

            x_arrow = self._to_screen(self.x_limits[1] / 20, 0)
            y_arrow = self._to_screen(0, self.y_limits[1] / 20)
            pygame.draw.line(self.screen, (255, 0, 0), origin, x_arrow, 2)
            pygame.draw.line(self.screen, (0, 255, 0), origin, y_arrow, 2)
            pygame.draw.circle(self.screen, (0, 0, 255), origin, 8)

        self.screen.set_clip(None)
        
        pygame.display.flip()

    def close(self):
        pygame.quit()