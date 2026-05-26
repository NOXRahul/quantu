"""
N-Body Gravitational Simulation
=================================

Simulates the gravitational interaction of N massive bodies using
the Velocity Verlet integrator (symplectic, energy-conserving).

Physics
-------
Each body i experiences gravitational acceleration from all other bodies:

    a⃗ᵢ = Σⱼ≠ᵢ  -G·mⱼ·(r⃗ᵢ - r⃗ⱼ) / (|r⃗ᵢ - r⃗ⱼ|² + ε²)^(3/2)

where ε is a gravitational softening parameter to avoid numerical
singularities during close encounters.

The total energy E = T + V is monitored as a conservation diagnostic:
    T = ½ Σᵢ mᵢ|v⃗ᵢ|²
    V = -½ Σᵢ Σⱼ≠ᵢ G·mᵢ·mⱼ / |r⃗ᵢ - r⃗ⱼ|
"""

import numpy as np
from typing import List, Optional, Tuple
from ..constants import G


class Body:
    """A gravitational body with mass, position, and velocity."""

    def __init__(
        self,
        mass: float,
        position: np.ndarray,
        velocity: np.ndarray,
        name: str = "Body",
        color: str = "#FFFFFF",
        radius: float = 1.0,
    ):
        self.mass = mass
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.name = name
        self.color = color
        self.radius = radius


class NBodySimulation:
    """
    N-body gravitational simulation engine.

    Uses Velocity Verlet integration for long-term energy conservation.

    Example
    -------
    >>> sim = NBodySimulation(softening=1e8)
    >>> sim.add_body(Body(1.989e30, [0,0], [0,0], "Sun"))
    >>> sim.add_body(Body(5.972e24, [1.496e11,0], [0,29783], "Earth"))
    >>> history = sim.run(dt=86400, n_steps=365)
    """

    def __init__(self, softening: float = 1e6):
        """
        Parameters
        ----------
        softening : float
            Gravitational softening length (m) to prevent singularities.
        """
        self.bodies: List[Body] = []
        self.softening = softening
        self.time = 0.0

    def add_body(self, body: Body):
        """Add a gravitational body to the simulation."""
        self.bodies.append(body)

    def _compute_accelerations(self, positions: np.ndarray, masses: np.ndarray) -> np.ndarray:
        """
        Compute gravitational accelerations for all bodies.

        Parameters
        ----------
        positions : np.ndarray, shape (N, dim)
        masses : np.ndarray, shape (N,)

        Returns
        -------
        accelerations : np.ndarray, shape (N, dim)
        """
        n = len(masses)
        dim = positions.shape[1]
        acc = np.zeros((n, dim))

        for i in range(n):
            for j in range(i + 1, n):
                r_vec = positions[j] - positions[i]
                r2 = np.dot(r_vec, r_vec) + self.softening**2
                r3 = r2 * np.sqrt(r2)

                force_factor = G / r3
                acc[i] += force_factor * masses[j] * r_vec
                acc[j] -= force_factor * masses[i] * r_vec

        return acc

    def kinetic_energy(self) -> float:
        """Total kinetic energy: T = ½ Σ mᵢ|vᵢ|²."""
        return sum(0.5 * b.mass * np.dot(b.velocity, b.velocity) for b in self.bodies)

    def potential_energy(self) -> float:
        """Total gravitational potential energy: V = -½ Σᵢ Σⱼ≠ᵢ GMᵢMⱼ/rᵢⱼ."""
        V = 0.0
        for i, bi in enumerate(self.bodies):
            for j in range(i + 1, len(self.bodies)):
                bj = self.bodies[j]
                r = np.linalg.norm(bi.position - bj.position)
                r = max(r, self.softening)
                V -= G * bi.mass * bj.mass / r
        return V

    def total_energy(self) -> float:
        """Total energy E = T + V (conserved in Verlet integration)."""
        return self.kinetic_energy() + self.potential_energy()

    def run(
        self,
        dt: float,
        n_steps: int,
        record_interval: int = 1,
    ) -> dict:
        """
        Run the N-body simulation using Velocity Verlet.

        Parameters
        ----------
        dt : float
            Time step (seconds).
        n_steps : int
            Number of integration steps.
        record_interval : int
            Record state every N steps (for memory efficiency).

        Returns
        -------
        history : dict
            'times': array of timestamps
            'positions': dict mapping body name → array of positions
            'energies': array of total energies
        """
        n = len(self.bodies)
        dim = len(self.bodies[0].position)

        # Pack state
        masses = np.array([b.mass for b in self.bodies])
        positions = np.array([b.position.copy() for b in self.bodies])
        velocities = np.array([b.velocity.copy() for b in self.bodies])

        # Initial accelerations
        acc = self._compute_accelerations(positions, masses)

        # Storage
        n_records = n_steps // record_interval + 1
        times = np.zeros(n_records)
        pos_history = np.zeros((n_records, n, dim))
        energies = np.zeros(n_records)

        # Record initial state
        pos_history[0] = positions.copy()
        times[0] = self.time
        energies[0] = self.total_energy()

        record_idx = 1

        for step in range(1, n_steps + 1):
            # Velocity Verlet: position update
            positions += velocities * dt + 0.5 * acc * dt**2

            # New accelerations
            acc_new = self._compute_accelerations(positions, masses)

            # Velocity update
            velocities += 0.5 * (acc + acc_new) * dt
            acc = acc_new

            self.time += dt

            # Update body objects
            for i, b in enumerate(self.bodies):
                b.position = positions[i].copy()
                b.velocity = velocities[i].copy()

            # Record
            if step % record_interval == 0 and record_idx < n_records:
                pos_history[record_idx] = positions.copy()
                times[record_idx] = self.time
                energies[record_idx] = self.total_energy()
                record_idx += 1

        # Build output
        pos_dict = {}
        for i, b in enumerate(self.bodies):
            pos_dict[b.name] = pos_history[:record_idx, i, :]

        return {
            'times': times[:record_idx],
            'positions': pos_dict,
            'energies': energies[:record_idx],
        }


# ==============================================================================
# PRESET SCENARIOS
# ==============================================================================

def sun_earth_moon() -> NBodySimulation:
    """Create a Sun-Earth-Moon three-body system."""
    sim = NBodySimulation(softening=1e6)
    sim.add_body(Body(
        mass=1.989e30,
        position=[0.0, 0.0],
        velocity=[0.0, 0.0],
        name="Sun", color="#FFD700", radius=20,
    ))
    sim.add_body(Body(
        mass=5.972e24,
        position=[1.496e11, 0.0],
        velocity=[0.0, 29783.0],
        name="Earth", color="#4169E1", radius=8,
    ))
    sim.add_body(Body(
        mass=7.342e22,
        position=[1.496e11 + 3.844e8, 0.0],
        velocity=[0.0, 29783.0 + 1022.0],
        name="Moon", color="#C0C0C0", radius=4,
    ))
    return sim


def binary_star_system() -> NBodySimulation:
    """Create a binary star system with a planet."""
    sim = NBodySimulation(softening=1e8)
    sep = 5e10  # 50 million km separation
    m_star = 1.0e30

    v_orbit = np.sqrt(G * m_star / (2 * sep))

    sim.add_body(Body(m_star, [sep, 0], [0, v_orbit], "Star A", "#FF6B35", 15))
    sim.add_body(Body(m_star, [-sep, 0], [0, -v_orbit], "Star B", "#00B4D8", 15))
    sim.add_body(Body(
        1e25, [3e11, 0], [0, np.sqrt(G * 2 * m_star / 3e11)],
        "Planet", "#2ECC71", 6,
    ))
    return sim


def figure_eight() -> NBodySimulation:
    """
    The famous figure-eight three-body solution.

    Discovered by Moore (1993), proven by Chenciner & Montgomery (2000).
    Three equal masses chase each other along a figure-8 path.
    """
    sim = NBodySimulation(softening=0.0)

    # Normalized units where G=1, masses=1
    # We scale to physical units
    m = 1e26  # 100 Earth masses
    scale = 1e10  # 10 billion meters

    # Initial conditions from the figure-8 solution
    p = 0.347111
    q = 0.532728

    sim.add_body(Body(m, [0.97 * scale, -0.243 * scale],
                       [p * 1e3, q * 1e3], "Body 1", "#E74C3C", 8))
    sim.add_body(Body(m, [-0.97 * scale, 0.243 * scale],
                       [p * 1e3, q * 1e3], "Body 2", "#3498DB", 8))
    sim.add_body(Body(m, [0, 0],
                       [-2 * p * 1e3, -2 * q * 1e3], "Body 3", "#2ECC71", 8))
    return sim
