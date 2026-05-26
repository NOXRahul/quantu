"""
Electromagnetic Propulsion Concepts
=====================================

⚠️ SPECULATIVE / THEORETICAL — Educational visualization only.

Models conceptual electromagnetic propulsion:
  • Lorentz force field visualization
  • Magnetic confinement geometry
  • EM field interaction concepts
"""

import numpy as np
from ..constants import mu_0, epsilon_0, c


class EMFieldPropulsion:
    """Conceptual EM field propulsion modeling."""

    def __init__(self, field_strength=1.0, frequency=1e9):
        self.B0 = field_strength  # Tesla
        self.freq = frequency  # Hz
        self.omega = 2 * np.pi * frequency

    def magnetic_dipole_field(self, X, Y, moment=1.0):
        """
        Magnetic dipole field (simplified 2D projection).
        B_r = (μ₀/4π) · 2m·cosθ/r³
        B_θ = (μ₀/4π) · m·sinθ/r³
        """
        r = np.sqrt(X**2 + Y**2)
        r = np.maximum(r, 0.1)
        theta = np.arctan2(Y, X)
        B_r = (mu_0 / (4 * np.pi)) * 2 * moment * np.cos(theta) / r**3
        B_theta = (mu_0 / (4 * np.pi)) * moment * np.sin(theta) / r**3
        Bx = B_r * np.cos(theta) - B_theta * np.sin(theta)
        By = B_r * np.sin(theta) + B_theta * np.cos(theta)
        return Bx, By

    def solenoid_field(self, X, Y, n_turns=100, current=1.0, length=1.0):
        """
        Simplified solenoid B-field for magnetic confinement visualization.
        Inside: B = μ₀ · n · I (uniform)
        Outside: approximately dipole-like
        """
        r = np.sqrt(X**2 + Y**2)
        radius = length / 4
        inside = r < radius
        B_inside = mu_0 * (n_turns / length) * current
        Bx = np.where(inside, 0, 0)
        By = np.where(inside, B_inside, B_inside * (radius / r)**3)
        return Bx, By

    def lorentz_force(self, q, v, B):
        """Lorentz force: F = q(v × B)."""
        return q * np.cross(v, B)

    def em_field_energy_density(self, E_field, B_field):
        """
        Electromagnetic field energy density:
        u = ½ε₀E² + B²/(2μ₀)
        """
        return 0.5 * epsilon_0 * E_field**2 + B_field**2 / (2 * mu_0)

    def rotating_field(self, X, Y, t=0):
        """
        Rotating magnetic field visualization.
        ⚠️ SPECULATIVE propulsion concept.
        """
        Bx = self.B0 * np.cos(self.omega * t) * np.exp(-(X**2 + Y**2))
        By = self.B0 * np.sin(self.omega * t) * np.exp(-(X**2 + Y**2))
        return Bx, By
