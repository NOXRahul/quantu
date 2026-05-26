"""
Unit Tests for Numerical Solvers
"""
import numpy as np
import pytest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from quantu.math_engine.solvers import rk4_step, rk4_integrate, velocity_verlet_step


class TestRK4:

    def test_exponential_decay(self):
        """dy/dt = -y → y(t) = e^(-t). RK4 should be accurate to O(h⁴)."""
        f = lambda t, y: -y
        y0 = np.array([1.0])
        t_arr, y_arr = rk4_integrate(f, y0, (0, 5), dt=0.01)
        y_exact = np.exp(-t_arr)
        error = np.max(np.abs(y_arr[:, 0] - y_exact))
        assert error < 1e-8, f"RK4 error too large: {error}"

    def test_harmonic_oscillator(self):
        """d²x/dt² = -x (SHO). Should conserve energy."""
        def f(t, y):
            return np.array([y[1], -y[0]])

        y0 = np.array([1.0, 0.0])  # x=1, v=0
        t_arr, y_arr = rk4_integrate(f, y0, (0, 20), dt=0.01)

        # Energy: E = ½(x² + v²) should be ~1.0 throughout
        E = 0.5 * (y_arr[:, 0]**2 + y_arr[:, 1]**2)
        assert np.max(np.abs(E - 0.5)) < 1e-6

    def test_single_step(self):
        """Single RK4 step on linear ODE dy/dt = 1."""
        f = lambda t, y: np.array([1.0])
        y = rk4_step(f, 0.0, np.array([0.0]), 0.1)
        assert abs(y[0] - 0.1) < 1e-15


class TestVelocityVerlet:

    def test_free_fall(self):
        """Constant acceleration: x = ½at². Verlet should be exact."""
        g = -9.81
        accel_func = lambda x: np.array([g])

        x = np.array([0.0])
        v = np.array([0.0])
        a = np.array([g])

        dt = 0.01
        for _ in range(100):
            x, v, a = velocity_verlet_step(x, v, a, accel_func, dt)

        t = 1.0
        x_exact = 0.5 * g * t**2
        assert abs(x[0] - x_exact) < 1e-10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
