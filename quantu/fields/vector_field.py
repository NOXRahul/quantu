"""
Vector Field Module
====================

Computes vector fields (force, velocity, acceleration) on grids.
A vector field assigns a vector to every point: F⃗(x,y) = (Fx, Fy).
"""

import numpy as np
from typing import Callable, Tuple


class VectorField:
    """2D vector field on a regular grid with streamline support."""

    def __init__(self, x_range, y_range, resolution=50):
        x = np.linspace(*x_range, resolution)
        y = np.linspace(*y_range, resolution)
        self.X, self.Y = np.meshgrid(x, y)
        self.U = np.zeros_like(self.X)
        self.V = np.zeros_like(self.Y)

    def evaluate(self, func: Callable):
        """Evaluate func(X, Y) → (U, V) on the grid."""
        self.U, self.V = func(self.X, self.Y)
        return self.U, self.V

    def magnitude(self) -> np.ndarray:
        return np.sqrt(self.U**2 + self.V**2)

    def normalized(self):
        """Return unit vectors for quiver plotting."""
        mag = self.magnitude()
        mag = np.maximum(mag, 1e-20)
        return self.U / mag, self.V / mag

    def add_source(self, strength, position, softening=1e-6):
        """Add a radial 1/r² source (e.g., gravitational field)."""
        dx = self.X - position[0]
        dy = self.Y - position[1]
        r = np.sqrt(dx**2 + dy**2 + softening**2)
        factor = -strength / r**3
        self.U += factor * dx
        self.V += factor * dy
