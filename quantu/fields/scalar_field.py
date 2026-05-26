"""
Scalar Field Module
====================

Computes scalar fields (gravitational potential, energy density) on grids.
A scalar field φ(x,y) assigns a single value to every point in space.
"""

import numpy as np
from typing import Tuple, Callable, Optional


class ScalarField:
    """2D/3D scalar field on a regular grid."""

    def __init__(self, x_range, y_range, resolution=200, z_range=None, z_resolution=None):
        self.is_3d = z_range is not None
        x = np.linspace(*x_range, resolution)
        y = np.linspace(*y_range, resolution)
        if self.is_3d:
            z = np.linspace(*z_range, z_resolution or resolution // 2)
            self.X, self.Y, self.Z = np.meshgrid(x, y, z, indexing='ij')
        else:
            self.X, self.Y = np.meshgrid(x, y)
            self.Z = None
        self.values = np.zeros_like(self.X)

    def evaluate(self, func: Callable) -> np.ndarray:
        """Evaluate func(X, Y) or func(X, Y, Z) on the grid."""
        if self.is_3d:
            self.values = func(self.X, self.Y, self.Z)
        else:
            self.values = func(self.X, self.Y)
        return self.values

    def add_point_source(self, strength, position, softening=1e-6):
        """Add a 1/r potential source: φ += -strength / r."""
        dx = self.X - position[0]
        dy = self.Y - position[1]
        if self.is_3d:
            dz = self.Z - position[2]
            r = np.sqrt(dx**2 + dy**2 + dz**2 + softening**2)
        else:
            r = np.sqrt(dx**2 + dy**2 + softening**2)
        self.values += -strength / r

    def gradient(self):
        """Compute ∇φ via finite differences."""
        if self.is_3d:
            return np.gradient(self.values)
        gy, gx = np.gradient(self.values)
        return gx, gy

    def clip(self, vmin, vmax):
        self.values = np.clip(self.values, vmin, vmax)
