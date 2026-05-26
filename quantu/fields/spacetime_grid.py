"""
Spacetime Grid Module
======================

Visualizes spacetime curvature using a deformable grid (rubber-sheet analogy).
The grid deforms in response to mass, simulating how massive objects curve spacetime.

The displacement is proportional to the Newtonian potential:
    z(x,y) ∝ -Σ GM_i / |r - r_i|
"""

import numpy as np
from typing import List, Tuple
from ..constants import G


class SpacetimeGrid:
    """Deformable spacetime grid for curvature visualization."""

    def __init__(self, x_range=(-10, 10), y_range=(-10, 10), resolution=80):
        x = np.linspace(*x_range, resolution)
        y = np.linspace(*y_range, resolution)
        self.X, self.Y = np.meshgrid(x, y)
        self.Z = np.zeros_like(self.X)
        self.resolution = resolution

    def add_mass(self, mass, position, scale=1.0, softening=0.3):
        """
        Deform the grid by a mass source.

        Parameters
        ----------
        mass : float — relative mass (1.0 = solar-like)
        position : [x, y] — position on the grid
        scale : float — deformation depth multiplier
        softening : float — prevents infinite well depth
        """
        dx = self.X - position[0]
        dy = self.Y - position[1]
        r = np.sqrt(dx**2 + dy**2 + softening**2)
        self.Z -= scale * mass / r

    def reset(self):
        """Reset grid to flat spacetime."""
        self.Z = np.zeros_like(self.X)

    def get_surface_data(self):
        """Return meshgrid data for 3D surface plotting."""
        return self.X, self.Y, self.Z

    def get_wireframe_lines(self, step=2):
        """Extract wireframe lines for plotting."""
        lines_x, lines_y, lines_z = [], [], []
        for i in range(0, self.X.shape[0], step):
            lines_x.append(self.X[i, :])
            lines_y.append(self.Y[i, :])
            lines_z.append(self.Z[i, :])
        for j in range(0, self.X.shape[1], step):
            lines_x.append(self.X[:, j])
            lines_y.append(self.Y[:, j])
            lines_z.append(self.Z[:, j])
        return lines_x, lines_y, lines_z
