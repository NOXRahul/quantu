"""
Unit Tests for QuantU Core Physics
"""
import numpy as np
import pytest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from quantu.constants import G, M_sun, M_earth, R_earth, AU
from quantu.core.gravity import (
    gravitational_force, gravitational_potential, escape_velocity,
    compute_potential_field, compute_force_field,
)


class TestGravity:
    """Tests for Newtonian gravity computations."""

    def test_gravitational_force_direction(self):
        """Force should point from m toward M (attractive)."""
        F = gravitational_force(M_sun, M_earth, np.array([AU, 0.0]))
        assert F[0] < 0, "Force should be attractive (negative x)"
        assert abs(F[1]) < 1e-10, "No y-component expected"

    def test_gravitational_force_magnitude(self):
        """Verify F = GMm/r² for Sun-Earth."""
        r_vec = np.array([AU, 0.0])
        F = gravitational_force(M_sun, M_earth, r_vec)
        expected = G * M_sun * M_earth / AU**2
        assert abs(np.linalg.norm(F) - expected) / expected < 1e-10

    def test_gravitational_potential_sign(self):
        """Potential should be negative."""
        phi = gravitational_potential(M_earth, R_earth)
        assert phi < 0

    def test_escape_velocity_earth(self):
        """Earth escape velocity ≈ 11,186 m/s."""
        v = escape_velocity(M_earth, R_earth)
        assert abs(v - 11186) < 50  # Within 50 m/s

    def test_potential_field_superposition(self):
        """Two equal masses should create symmetric potential."""
        x = np.linspace(-5, 5, 50)
        X, Y = np.meshgrid(x, x)
        masses = [(1e24, np.array([-2, 0])), (1e24, np.array([2, 0]))]
        pot = compute_potential_field(masses, X, Y, softening=0.1)
        # Check symmetry: pot(x,y) ≈ pot(-x,y)
        assert np.allclose(pot, np.flip(pot, axis=1), atol=1e-20)


class TestEscapeVelocity:
    def test_larger_mass_higher_velocity(self):
        v1 = escape_velocity(M_earth, R_earth)
        v2 = escape_velocity(10 * M_earth, R_earth)
        assert v2 > v1

    def test_closer_distance_higher_velocity(self):
        v1 = escape_velocity(M_earth, R_earth)
        v2 = escape_velocity(M_earth, R_earth / 2)
        assert v2 > v1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
