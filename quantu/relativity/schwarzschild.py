"""
Schwarzschild Metric & Gravitational Lensing
==============================================

The Schwarzschild solution describes spacetime around a non-rotating,
uncharged, spherically symmetric mass. It is the simplest black hole solution.

Metric (in Schwarzschild coordinates):
    ds² = -(1 - r_s/r)c²dt² + dr²/(1 - r_s/r) + r²(dθ² + sin²θ dφ²)

where r_s = 2GM/c² is the Schwarzschild radius (event horizon).

Key features:
  • Event horizon at r = r_s
  • Photon sphere at r = 1.5·r_s
  • Gravitational redshift: z = 1/√(1 - r_s/r) - 1
  • Light deflection: Δφ ≈ 4GM/(c²b) for weak field
"""

import numpy as np
from ..constants import G, c


class SchwarzschildMetric:
    """Schwarzschild spacetime computations."""

    def __init__(self, mass: float):
        """
        Parameters
        ----------
        mass : float
            Central mass (kg).
        """
        self.M = mass
        self.r_s = 2 * G * mass / c**2  # Schwarzschild radius

    @property
    def event_horizon(self) -> float:
        """Event horizon radius (m)."""
        return self.r_s

    @property
    def photon_sphere(self) -> float:
        """Photon sphere radius: r = 1.5·r_s."""
        return 1.5 * self.r_s

    @property
    def isco(self) -> float:
        """Innermost Stable Circular Orbit: r = 3·r_s."""
        return 3.0 * self.r_s

    def metric_component_tt(self, r: np.ndarray) -> np.ndarray:
        """g_tt = -(1 - r_s/r)."""
        return -(1.0 - self.r_s / r)

    def metric_component_rr(self, r: np.ndarray) -> np.ndarray:
        """g_rr = 1/(1 - r_s/r)."""
        return 1.0 / (1.0 - self.r_s / r)

    def gravitational_redshift(self, r: np.ndarray) -> np.ndarray:
        """
        Gravitational redshift factor.
        z = 1/√(1 - r_s/r) - 1
        """
        factor = 1.0 - self.r_s / r
        factor = np.maximum(factor, 1e-20)  # Avoid sqrt of negative
        return 1.0 / np.sqrt(factor) - 1.0

    def time_dilation(self, r: np.ndarray) -> np.ndarray:
        """
        Gravitational time dilation: dτ/dt = √(1 - r_s/r).
        A clock at radius r ticks slower by this factor.
        """
        factor = 1.0 - self.r_s / r
        return np.sqrt(np.maximum(factor, 0.0))

    def light_deflection_angle(self, b: float) -> float:
        """
        Weak-field light deflection angle (radians).
        Δφ ≈ 4GM/(c²b)

        Parameters
        ----------
        b : float — impact parameter (m)
        """
        return 4 * G * self.M / (c**2 * b)

    def effective_potential(self, r: np.ndarray, L: float, m: float = 1.0) -> np.ndarray:
        """
        Effective potential for radial motion.
        V_eff(r) = -GMm/r + L²/(2mr²) - GML²/(mc²r³)

        The last term is the relativistic correction.
        """
        V = (-G * self.M * m / r
             + L**2 / (2 * m * r**2)
             - G * self.M * L**2 / (m * c**2 * r**3))
        return V

    def compute_lensing_grid(self, grid_size=200, extent=10.0):
        """
        Compute gravitational lensing distortion on a background grid.

        Returns displaced grid coordinates showing how a background
        star field would appear around the black hole.
        """
        x = np.linspace(-extent, extent, grid_size)
        y = np.linspace(-extent, extent, grid_size)
        X, Y = np.meshgrid(x, y)

        # Impact parameter in units of r_s
        b = np.sqrt(X**2 + Y**2)
        b = np.maximum(b, 0.1)

        # Deflection angle (simplified)
        alpha = 2.0 / b  # In units of r_s

        # Radial displacement
        X_lensed = X * (1 + alpha / b)
        Y_lensed = Y * (1 + alpha / b)

        return X, Y, X_lensed, Y_lensed, b

    def embedding_diagram(self, r_range=(1.01, 10.0), n_points=200):
        """
        Flamm's paraboloid: the embedding diagram of the Schwarzschild metric.

        The 2D equatorial slice embeds into 3D as:
            z(r) = 2√(r_s · (r - r_s))
        """
        r = np.linspace(r_range[0] * self.r_s, r_range[1] * self.r_s, n_points)
        z = 2 * np.sqrt(self.r_s * (r - self.r_s))

        theta = np.linspace(0, 2 * np.pi, 100)
        R, Theta = np.meshgrid(r, theta)
        Z = 2 * np.sqrt(self.r_s * (R - self.r_s))

        X = R * np.cos(Theta) / self.r_s
        Y = R * np.sin(Theta) / self.r_s
        Z = Z / self.r_s

        return X, Y, Z
