"""
Orbital Mechanics Module
=========================

Implements classical orbital mechanics:

  • Kepler orbit generation (elliptical, parabolic, hyperbolic)
  • Orbital element ↔ state vector conversion
  • Hohmann transfer calculations
  • Vis-viva equation
  • Orbital period and energy

Key Equations
-------------
**Vis-Viva** (orbital energy):

    v² = G·M · (2/r - 1/a)

**Orbital Period** (Kepler's 3rd law):

    T = 2π · √(a³ / (G·M))

**Hohmann Transfer ΔV**:

    Δv₁ = √(G·M/r₁) · (√(2r₂/(r₁+r₂)) - 1)
    Δv₂ = √(G·M/r₂) · (1 - √(2r₁/(r₁+r₂)))
"""

import numpy as np
from typing import Tuple, Optional
from ..constants import G


def orbital_period(a: float, M: float) -> float:
    """
    Kepler's Third Law: T = 2π√(a³/(GM)).

    Parameters
    ----------
    a : float
        Semi-major axis (m).
    M : float
        Central body mass (kg).

    Returns
    -------
    T : float
        Orbital period (seconds).
    """
    return 2 * np.pi * np.sqrt(a**3 / (G * M))


def vis_viva(M: float, r: float, a: float) -> float:
    """
    Vis-viva equation: v = √(GM(2/r - 1/a)).

    Parameters
    ----------
    M : float
        Central mass (kg).
    r : float
        Current radial distance (m).
    a : float
        Semi-major axis (m). Use a=∞ for parabolic.

    Returns
    -------
    v : float
        Orbital velocity (m/s).
    """
    return np.sqrt(G * M * (2.0 / r - 1.0 / a))


def specific_orbital_energy(M: float, a: float) -> float:
    """
    Specific orbital energy: ε = -GM/(2a).

    Negative for bound (elliptical), zero for parabolic,
    positive for hyperbolic orbits.
    """
    return -G * M / (2.0 * a)


def kepler_orbit(
    a: float,
    e: float,
    M_central: float,
    n_points: int = 500,
    include_velocity: bool = False,
) -> dict:
    """
    Generate a Keplerian orbit in the orbital plane.

    Parameters
    ----------
    a : float
        Semi-major axis (m).
    e : float
        Eccentricity (0 ≤ e < 1 for elliptical).
    M_central : float
        Central body mass (kg).
    n_points : int
        Number of orbit points.
    include_velocity : bool
        If True, also compute velocity vectors.

    Returns
    -------
    orbit : dict
        Keys: 'x', 'y', 'r', 'theta', 'T' (period).
        If include_velocity: also 'vx', 'vy'.
    """
    # True anomaly array
    theta = np.linspace(0, 2 * np.pi, n_points)

    # Orbit equation: r = a(1-e²) / (1 + e·cos(θ))
    p = a * (1 - e**2)  # Semi-latus rectum
    r = p / (1 + e * np.cos(theta))

    x = r * np.cos(theta)
    y = r * np.sin(theta)

    T = orbital_period(a, M_central)

    result = {
        'x': x, 'y': y, 'r': r, 'theta': theta,
        'T': T, 'a': a, 'e': e, 'p': p,
    }

    if include_velocity:
        # Velocity components in perifocal frame
        mu = G * M_central
        h = np.sqrt(mu * p)  # Specific angular momentum
        vr = (mu / h) * e * np.sin(theta)        # Radial velocity
        vt = (mu / h) * (1 + e * np.cos(theta))  # Tangential velocity
        vx = vr * np.cos(theta) - vt * np.sin(theta)
        vy = vr * np.sin(theta) + vt * np.cos(theta)
        result['vx'] = vx
        result['vy'] = vy

    return result


def hohmann_transfer(
    M: float,
    r1: float,
    r2: float,
) -> dict:
    """
    Compute a Hohmann transfer orbit between two circular orbits.

    Parameters
    ----------
    M : float
        Central mass (kg).
    r1 : float
        Inner orbit radius (m).
    r2 : float
        Outer orbit radius (m).

    Returns
    -------
    transfer : dict
        Keys: 'dv1', 'dv2', 'dv_total', 'transfer_time',
              'a_transfer', 'v1_circular', 'v2_circular'.
    """
    mu = G * M

    # Circular velocities
    v1_circ = np.sqrt(mu / r1)
    v2_circ = np.sqrt(mu / r2)

    # Transfer orbit semi-major axis
    a_t = (r1 + r2) / 2.0

    # Velocities at periapsis and apoapsis of transfer orbit
    v_t1 = np.sqrt(mu * (2.0 / r1 - 1.0 / a_t))
    v_t2 = np.sqrt(mu * (2.0 / r2 - 1.0 / a_t))

    # Delta-v maneuvers
    dv1 = abs(v_t1 - v1_circ)
    dv2 = abs(v2_circ - v_t2)

    # Transfer time = half the transfer orbit period
    t_transfer = np.pi * np.sqrt(a_t**3 / mu)

    return {
        'dv1': dv1,
        'dv2': dv2,
        'dv_total': dv1 + dv2,
        'transfer_time': t_transfer,
        'a_transfer': a_t,
        'v1_circular': v1_circ,
        'v2_circular': v2_circ,
    }


def state_to_elements(
    r_vec: np.ndarray,
    v_vec: np.ndarray,
    mu: float,
) -> dict:
    """
    Convert state vector (r⃗, v⃗) to classical orbital elements.

    Parameters
    ----------
    r_vec : np.ndarray, shape (3,)
        Position vector (m).
    v_vec : np.ndarray, shape (3,)
        Velocity vector (m/s).
    mu : float
        Gravitational parameter GM (m³/s²).

    Returns
    -------
    elements : dict
        'a' (semi-major axis), 'e' (eccentricity),
        'i' (inclination), 'omega' (arg periapsis),
        'Omega' (RAAN), 'nu' (true anomaly).
    """
    r = np.linalg.norm(r_vec)
    v = np.linalg.norm(v_vec)

    # Specific angular momentum
    h_vec = np.cross(r_vec, v_vec)
    h = np.linalg.norm(h_vec)

    # Eccentricity vector
    e_vec = (np.cross(v_vec, h_vec) / mu) - (r_vec / r)
    e = np.linalg.norm(e_vec)

    # Semi-major axis
    energy = 0.5 * v**2 - mu / r
    if abs(energy) < 1e-20:
        a = float('inf')  # Parabolic
    else:
        a = -mu / (2 * energy)

    # Inclination
    i = np.arccos(np.clip(h_vec[2] / h, -1, 1))

    # Node vector
    k_hat = np.array([0, 0, 1.0])
    n_vec = np.cross(k_hat, h_vec)
    n = np.linalg.norm(n_vec)

    # RAAN (Ω)
    if n > 1e-10:
        Omega = np.arccos(np.clip(n_vec[0] / n, -1, 1))
        if n_vec[1] < 0:
            Omega = 2 * np.pi - Omega
    else:
        Omega = 0.0

    # Argument of periapsis (ω)
    if n > 1e-10 and e > 1e-10:
        omega = np.arccos(np.clip(np.dot(n_vec, e_vec) / (n * e), -1, 1))
        if e_vec[2] < 0:
            omega = 2 * np.pi - omega
    else:
        omega = 0.0

    # True anomaly (ν)
    if e > 1e-10:
        nu = np.arccos(np.clip(np.dot(e_vec, r_vec) / (e * r), -1, 1))
        if np.dot(r_vec, v_vec) < 0:
            nu = 2 * np.pi - nu
    else:
        nu = 0.0

    return {
        'a': a, 'e': e, 'i': np.degrees(i),
        'omega': np.degrees(omega),
        'Omega': np.degrees(Omega),
        'nu': np.degrees(nu),
    }
