"""
Exotic Matter & Negative Energy Density
=========================================

⚠️ SPECULATIVE / THEORETICAL — Educational visualization only.

Explores concepts related to negative energy density:
  • Casimir effect (experimentally verified QFT prediction)
  • Hypothetical exotic matter fields
  • Quantum vacuum fluctuation visualization

The Casimir Effect
------------------
Two uncharged conducting plates in vacuum experience an attractive force
due to quantum vacuum fluctuations. The energy density between plates:

    E/A = -π²ℏc / (720 d⁴)

This is one of the few known sources of "negative energy density"
in established physics.
"""

import numpy as np
from ..constants import hbar, c


class CasimirEffect:
    """Casimir effect energy density computation."""

    @staticmethod
    def energy_density(d: float) -> float:
        """
        Casimir energy density between parallel plates.
        E/A = -π²ℏc / (720 d⁴) [J/m²]

        Parameters
        ----------
        d : float — plate separation (m)
        """
        return -np.pi**2 * hbar * c / (720 * d**4)

    @staticmethod
    def force_per_area(d: float) -> float:
        """
        Casimir force per unit area.
        F/A = -π²ℏc / (240 d⁴) [N/m²]
        """
        return -np.pi**2 * hbar * c / (240 * d**4)

    @staticmethod
    def compute_vs_distance(d_min=1e-9, d_max=1e-6, n_points=200):
        """Compute Casimir energy and force as function of plate separation."""
        d = np.linspace(d_min, d_max, n_points)
        energy = -np.pi**2 * hbar * c / (720 * d**4)
        force = -np.pi**2 * hbar * c / (240 * d**4)
        return d, energy, force


class NegativeEnergyField:
    """
    ⚠️ SPECULATIVE: Hypothetical negative energy density field visualization.
    Used for educational demonstration of exotic matter concepts.
    """

    def __init__(self, amplitude=-1.0, radius=1.0, falloff=2.0):
        self.amplitude = amplitude
        self.radius = radius
        self.falloff = falloff

    def compute_field(self, X, Y):
        """Compute a Gaussian-envelope negative energy field."""
        r = np.sqrt(X**2 + Y**2)
        field = self.amplitude * np.exp(-(r / self.radius)**self.falloff)
        return field

    def compute_3d(self, grid_size=100, extent=3.0):
        x = np.linspace(-extent, extent, grid_size)
        y = np.linspace(-extent, extent, grid_size)
        X, Y = np.meshgrid(x, y)
        field = self.compute_field(X, Y)
        return X, Y, field


class QuantumVacuumFluctuation:
    """
    ⚠️ SPECULATIVE: Visual model of quantum vacuum energy fluctuations.
    Creates a random field representing zero-point energy fluctuations.
    """

    @staticmethod
    def generate(grid_size=200, extent=5.0, seed=42):
        """Generate a visualization of vacuum fluctuations."""
        rng = np.random.default_rng(seed)
        x = np.linspace(-extent, extent, grid_size)
        y = np.linspace(-extent, extent, grid_size)
        X, Y = np.meshgrid(x, y)

        # Superposition of random modes (simplified)
        field = np.zeros_like(X)
        for _ in range(50):
            kx = rng.normal(0, 2)
            ky = rng.normal(0, 2)
            phase = rng.uniform(0, 2 * np.pi)
            amp = rng.exponential(0.1)
            field += amp * np.cos(kx * X + ky * Y + phase)

        return X, Y, field
