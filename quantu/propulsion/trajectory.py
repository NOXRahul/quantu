"""
Spacecraft Trajectory Planner
===============================

Simulates spacecraft trajectories with various propulsion profiles:
  • Constant thrust (ion drive)
  • Impulse maneuvers (chemical rockets)
  • Gravity assists
  • Multi-body trajectory planning (patched conics)
"""

import numpy as np
from typing import List, Tuple, Optional
from ..constants import G, g0
from ..math_engine.solvers import rk4_integrate


class TrajectoryPlanner:
    """Spacecraft trajectory simulation with thrust profiles."""

    def __init__(self, central_mass: float, spacecraft_mass: float = 1000.0):
        self.M = central_mass
        self.m_sc = spacecraft_mass
        self.mu = G * central_mass

    def constant_thrust_trajectory(
        self,
        r0: np.ndarray,
        v0: np.ndarray,
        thrust: float,
        isp: float,
        thrust_direction: np.ndarray,
        duration: float,
        dt: float = 3600.0,
    ) -> dict:
        """
        Simulate trajectory with constant thrust.

        Parameters
        ----------
        r0 : np.ndarray — initial position [x, y] (m)
        v0 : np.ndarray — initial velocity [vx, vy] (m/s)
        thrust : float — thrust force (N)
        isp : float — specific impulse (s)
        thrust_direction : np.ndarray — unit thrust direction [dx, dy]
        duration : float — burn duration (s)
        dt : float — time step (s)
        """
        v_e = isp * g0
        mdot = thrust / v_e

        t_dir = thrust_direction / np.linalg.norm(thrust_direction)

        def rhs(t, state):
            x, y, vx, vy, mass = state
            r = np.sqrt(x**2 + y**2)
            r3 = r**3

            # Gravity
            ax_g = -self.mu * x / r3
            ay_g = -self.mu * y / r3

            # Thrust (if fuel remains)
            if mass > self.m_sc * 0.1:  # 10% dry mass limit
                a_thrust = thrust / mass
                ax_t = a_thrust * t_dir[0]
                ay_t = a_thrust * t_dir[1]
                dm = -mdot
            else:
                ax_t = ay_t = 0.0
                dm = 0.0

            return np.array([vx, vy, ax_g + ax_t, ay_g + ay_t, dm])

        state0 = np.array([r0[0], r0[1], v0[0], v0[1], self.m_sc])
        t_arr, state_arr = rk4_integrate(rhs, state0, (0, duration), dt)

        return {
            'times': t_arr,
            'x': state_arr[:, 0],
            'y': state_arr[:, 1],
            'vx': state_arr[:, 2],
            'vy': state_arr[:, 3],
            'mass': state_arr[:, 4],
            'delta_v': v_e * np.log(state_arr[0, 4] / state_arr[:, 4]),
        }

    def coast_trajectory(self, r0, v0, duration, dt=3600.0):
        """Unpowered (coasting) trajectory under central gravity."""

        def rhs(t, state):
            x, y, vx, vy = state
            r3 = (x**2 + y**2)**1.5
            return np.array([vx, vy, -self.mu * x / r3, -self.mu * y / r3])

        state0 = np.array([r0[0], r0[1], v0[0], v0[1]])
        t_arr, state_arr = rk4_integrate(rhs, state0, (0, duration), dt)

        return {
            'times': t_arr,
            'x': state_arr[:, 0],
            'y': state_arr[:, 1],
            'vx': state_arr[:, 2],
            'vy': state_arr[:, 3],
        }

    def gravity_assist(self, v_inf_in, v_planet, M_planet, r_periapsis):
        """
        Calculate gravity assist maneuver (simplified 2D).

        The spacecraft gains velocity by "borrowing" from the planet's
        orbital energy — a slingshot maneuver.
        """
        mu_p = G * M_planet
        v_inf = np.linalg.norm(v_inf_in - v_planet)

        # Turn angle
        delta = 2 * np.arcsin(1 / (1 + r_periapsis * v_inf**2 / mu_p))

        # Rotate v_inf by delta
        cos_d, sin_d = np.cos(delta), np.sin(delta)
        v_rel = v_inf_in - v_planet
        v_out_rel = np.array([
            cos_d * v_rel[0] - sin_d * v_rel[1],
            sin_d * v_rel[0] + cos_d * v_rel[1],
        ])
        v_out = v_out_rel + v_planet

        return {
            'v_out': v_out,
            'turn_angle_deg': np.degrees(delta),
            'delta_v': np.linalg.norm(v_out) - np.linalg.norm(v_inf_in),
        }

    def delta_v_budget(self, maneuvers: List[dict]) -> dict:
        """
        Calculate total Δv budget from a list of maneuvers.

        Parameters
        ----------
        maneuvers : list of dict
            Each: {'name': str, 'delta_v': float}
        """
        total = sum(m['delta_v'] for m in maneuvers)
        return {
            'maneuvers': maneuvers,
            'total_delta_v': total,
            'total_delta_v_km_s': total / 1000,
        }
