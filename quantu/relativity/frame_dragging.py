"""
Frame Dragging & Kerr Metric (Simplified)
===========================================

The Kerr metric describes spacetime around a rotating mass.
Key phenomenon: frame dragging — spacetime itself is "dragged" in the
direction of rotation.

Simplified model (equatorial plane, θ = π/2):
  • Frame-dragging angular velocity: ω = 2GMa/(c²r³)
  • Ergosphere boundary: r_e = r_s/2 + √((r_s/2)² - a²cos²θ)
  • r_s = 2GM/c² (Schwarzschild radius)
  • a = J/(Mc) is the spin parameter (0 ≤ a ≤ r_s/2)
"""

import numpy as np
from ..constants import G, c


class KerrMetric:
    """Simplified Kerr (rotating black hole) metric."""

    def __init__(self, mass: float, spin_parameter: float = 0.5):
        """
        Parameters
        ----------
        mass : float — central mass (kg)
        spin_parameter : float — dimensionless spin a/M (0 to 1)
        """
        self.M = mass
        self.r_s = 2 * G * mass / c**2
        self.a = spin_parameter * self.r_s / 2  # a in meters

    def frame_dragging_rate(self, r: np.ndarray) -> np.ndarray:
        """
        Frame-dragging angular velocity ω(r) in the equatorial plane.
        ω = 2GMa / (c² r³) (weak-field approximation)
        """
        r_safe = np.maximum(r, self.r_s * 1.01)
        return 2 * G * self.M * self.a / (c**2 * r_safe**3)

    def ergosphere_radius(self, theta: np.ndarray) -> np.ndarray:
        """
        Ergosphere outer boundary: r_e(θ) = M + √(M² - a²cos²θ).
        In geometric units where r_s = 2M.
        """
        M_geom = self.r_s / 2
        return M_geom + np.sqrt(M_geom**2 - (self.a * np.cos(theta))**2)

    def compute_frame_drag_field(self, grid_size=100, extent_rs=10):
        """
        Compute frame-dragging velocity field on a 2D grid.

        Returns
        -------
        X, Y : meshgrid
        omega : frame-dragging angular velocity
        vx, vy : induced velocity components (tangential)
        """
        extent = extent_rs * self.r_s
        x = np.linspace(-extent, extent, grid_size)
        y = np.linspace(-extent, extent, grid_size)
        X, Y = np.meshgrid(x, y)
        r = np.sqrt(X**2 + Y**2)
        r = np.maximum(r, self.r_s * 1.01)

        omega = self.frame_dragging_rate(r)

        # Tangential velocity: v = ω × r (perpendicular to radial)
        vx = -omega * Y
        vy = omega * X

        return X, Y, omega, vx, vy

    def compute_ergosphere(self, n_points=200):
        """Compute ergosphere boundary curve."""
        theta = np.linspace(0, 2 * np.pi, n_points)
        r_e = self.ergosphere_radius(theta)
        x = r_e * np.cos(theta)
        y = r_e * np.sin(theta)
        return x, y, r_e
