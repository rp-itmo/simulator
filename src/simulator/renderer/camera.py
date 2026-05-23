import numpy as np


class Camera:
    """
    Camera system for managing viewport transformations.
    Converts 2D world coordinates into view coordinates supporting
    switching views (e.g., from top, from side, pan, zoom).
    """

    def __init__(self, position=(0.0, 0.0), scale=1.0, view_type="top"):
        """
        Args:
            position (tuple): Offset (x, y) describing camera position.
            scale (float): Zoom level.
            view_type (str): 'top', 'side', etc. (Currently for basic switch view requirement).
        """
        self.position = np.array(position, dtype=float)
        self.scale = scale
        self.view_type = view_type

    def apply(self, point):
        """
        Transform a point from world coordinates to camera coordinates.

        Args:
            point (tuple, list, np.ndarray): The 2D point (x, y) to transform.

        Returns:
            np.ndarray: The transformed point (x', y').
        """
        p = np.array(point, dtype=float)

        # A basic view selection logic (can be expanded)
        # Assuming for now we just pan and scale in 2D space.
        # If 'side' view is requested on a 3D point, we could project XZ or YZ,
        # but the simulator objects presently operate in a 2D environment (X-Y).
        if self.view_type == "top":
            # For 2D, top view might just be direct mapping
            pass
        elif self.view_type == "side":
            # Just an example of how you might swap axes or apply specific projection
            pass

        return (p - self.position) * self.scale
