"""
Alcubierre Warp Drive Metric
==============================

⚠️ SPECULATIVE / THEORETICAL — Not experimentally verified.

The Alcubierre metric (1994) describes a spacetime geometry that allows
effective faster-than-light travel by contracting space ahead and expanding
it behind a "warp bubble."

Metric:
    ds² = -c²dt² + (dx - v_s·f(r_s)·dt)² + dy² + dz²

Shape function:
    f(r_s) = [tanh(σ(r_s + R)) - tanh(σ(r_s - R))] / [2·tanh(σR)]

where:
  - v_s = bubble velocity (dx_s/dt)
  - R = bubble radius
  - σ = wall thickness parameter (larger = thinner walls)
  - r_s = √((x - x_s)² + y² + z²)

Energy density (enormous negative energy required):
    T⁰⁰ = -(c⁴/8πG) · v_s² · (y² + z²) / (2r_s²) · (df/dr_s)²

Reference: Alcubierre, M. (1994). Classical and Quantum Gravity, 11(5), L73.
"""

import numpy as np
from ..constants import G, c


class AlcubierreWarpDrive:
    """Alcubierre warp metric visualization and analysis."""

    def __init__(self, R: float = 1.0, sigma: float = 8.0, v_s: float = 1.0):
        """
        Parameters
        ----------
        R : float
            Bubble radius (arbitrary units for visualization).
        sigma : float
            Wall thickness parameter. Higher = thinner walls.
        v_s : float
            Bubble velocity (in units of c for display).
        """
        self.R = R
        self.sigma = sigma
        self.v_s = v_s

    def shape_function(self, r_s: np.ndarray) -> np.ndarray:
        """
        Alcubierre shape function f(r_s).
        f(r_s) = [tanh(σ(r_s + R)) - tanh(σ(r_s - R))] / [2·tanh(σR)]
        """
        numerator = np.tanh(self.sigma * (r_s + self.R)) - np.tanh(self.sigma * (r_s - self.R))
        denominator = 2.0 * np.tanh(self.sigma * self.R)
        return numerator / denominator

    def shape_function_derivative(self, r_s: np.ndarray) -> np.ndarray:
        """df/dr_s — needed for energy density computation."""
        dr = 1e-6
        return (self.shape_function(r_s + dr) - self.shape_function(r_s - dr)) / (2 * dr)

    def energy_density(self, x: np.ndarray, y: np.ndarray, x_s: float = 0.0) -> np.ndarray:
        """
        Compute the energy density required for the warp bubble.

        T⁰⁰ ∝ -v_s² · y² / (2r_s²) · (df/dr_s)²

        Returns negative values — this is the exotic (negative) energy
        requirement that makes the Alcubierre drive physically problematic.
        """
        r_s = np.sqrt((x - x_s)**2 + y**2)
        r_s = np.maximum(r_s, 1e-10)
        dfdr = self.shape_function_derivative(r_s)
        rho = -(self.v_s**2 * y**2) / (2 * r_s**2) * dfdr**2
        return rho

    def compute_bubble_2d(self, grid_size=200, extent=3.0, x_s=0.0):
        """
        Compute the warp bubble shape function on a 2D grid.

        Returns
        -------
        X, Y : meshgrid arrays
        f_values : shape function values
        rho : energy density values
        """
        x = np.linspace(-extent, extent, grid_size)
        y = np.linspace(-extent, extent, grid_size)
        X, Y = np.meshgrid(x, y)
        r_s = np.sqrt((X - x_s)**2 + Y**2)
        f_values = self.shape_function(r_s)
        rho = self.energy_density(X, Y, x_s)
        return X, Y, f_values, rho

    def compute_bubble_3d(self, grid_size=80, extent=3.0):
        """Compute 3D warp bubble as a surface of revolution."""
        r = np.linspace(0, extent, grid_size)
        theta = np.linspace(0, 2 * np.pi, grid_size)
        R_mesh, Theta = np.meshgrid(r, theta)

        f = self.shape_function(R_mesh)
        X = R_mesh * np.cos(Theta)
        Y = R_mesh * np.sin(Theta)
        Z = f
        return X, Y, Z

    def metric_perturbation(self, x, y, x_s=0.0):
        """
        Compute the metric perturbation h_tx = -v_s · f(r_s).
        This is the off-diagonal metric component that creates the warp effect.
        """
        r_s = np.sqrt((x - x_s)**2 + y**2)
        return -self.v_s * self.shape_function(r_s)

    def total_energy_estimate(self, extent=5.0, grid_size=300):
        """
        Estimate total energy in the warp bubble (in arbitrary units).
        Integrates the energy density over the 2D cross-section.
        """
        X, Y, _, rho = self.compute_bubble_2d(grid_size, extent)
        dx = X[0, 1] - X[0, 0]
        dy = Y[1, 0] - Y[0, 0]
        return np.sum(rho) * dx * dy
