"""
Unit Tests for Orbital Mechanics
"""
import numpy as np
import pytest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from quantu.constants import G, M_sun, AU
from quantu.core.orbital import orbital_period, kepler_orbit, hohmann_transfer, vis_viva


class TestOrbitalMechanics:

    def test_earth_orbital_period(self):
        """Earth period ≈ 365.25 days."""
        T = orbital_period(AU, M_sun)
        T_days = T / 86400
        assert abs(T_days - 365.25) < 1.0  # Within 1 day

    def test_circular_orbit_velocity(self):
        """Vis-viva for circular orbit: v = √(GM/r)."""
        v = vis_viva(M_sun, AU, AU)
        v_expected = np.sqrt(G * M_sun / AU)
        assert abs(v - v_expected) / v_expected < 1e-10

    def test_kepler_orbit_closed(self):
        """Elliptical orbit should close on itself."""
        orbit = kepler_orbit(AU, 0.3, M_sun, n_points=1000)
        # First and last points should be close
        assert abs(orbit['x'][0] - orbit['x'][-1]) < 1e6
        assert abs(orbit['y'][0] - orbit['y'][-1]) < 1e6

    def test_hohmann_positive_dv(self):
        """Hohmann transfer should have positive Δv."""
        result = hohmann_transfer(M_sun, AU, 1.524 * AU)
        assert result['dv1'] > 0
        assert result['dv2'] > 0
        assert result['transfer_time'] > 0

    def test_hohmann_earth_mars(self):
        """Earth-Mars Hohmann: total Δv ≈ 5.6 km/s."""
        result = hohmann_transfer(M_sun, AU, 1.524 * AU)
        dv_total_km_s = result['dv_total'] / 1000
        assert 4.0 < dv_total_km_s < 7.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
