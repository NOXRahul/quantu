"""
Newtonian Gravity Module
=========================

Implements classical gravitational physics:

  • Point-mass gravitational force (Newton's law)
  • Gravitational potential energy & field
  • Escape velocity
  • Multi-source field superposition
  • 2D/3D field intensity maps

Fundamental Equations
---------------------
**Newton's Law of Universal Gravitation**:

    F⃗ = -G·M·m / |r⃗|² · r̂

**Gravitational Potential**:

    Φ(r) = -G·M / |r⃗|

**Escape Velocity** (from energy conservation E_k + E_p = 0):

    v_esc = √(2·G·M / r)

**Gravitational Field** (force per unit mass):

    g⃗(r⃗) = -G·M / |r⃗|² · r̂ = -∇Φ
"""

import numpy as np
from typing import Union, List, Tuple, Optional
from ..constants import G


# ==============================================================================
# POINT-MASS GRAVITY
# ==============================================================================

def gravitational_force(
    M: float,
    m: float,
    r_vec: np.ndarray,
) -> np.ndarray:
    """
    Compute gravitational force vector on mass m due to mass M.

    F⃗ = -G·M·m / |r⃗|³ · r⃗

    where r⃗ points from M to m.

    Parameters
    ----------
    M : float
        Source mass (kg).
    m : float
        Test mass (kg).
    r_vec : np.ndarray, shape (2,) or (3,)
        Displacement vector from M to m (meters).

    Returns
    -------
    F : np.ndarray
        Force vector on m (Newtons), directed toward M.
    """
    r = np.linalg.norm(r_vec)
    if r < 1e-10:
        return np.zeros_like(r_vec)
    return -G * M * m / r**3 * r_vec


def gravitational_potential(
    M: float,
    r: Union[float, np.ndarray],
) -> Union[float, np.ndarray]:
    """
    Gravitational potential Φ = -G·M / r.

    Parameters
    ----------
    M : float
        Source mass (kg).
    r : float or ndarray
        Distance(s) from the source (meters). Must be > 0.

    Returns
    -------
    Φ : float or ndarray
        Gravitational potential (J/kg).
    """
    r = np.asarray(r, dtype=float)
    # Avoid division by zero with a softening
    r_safe = np.maximum(r, 1e-10)
    return -G * M / r_safe


def gravitational_field(
    M: float,
    r_vec: np.ndarray,
) -> np.ndarray:
    """
    Gravitational field vector g⃗ = -G·M / |r⃗|³ · r⃗.

    This is the force per unit mass at position r⃗ from the source.

    Parameters
    ----------
    M : float
        Source mass (kg).
    r_vec : np.ndarray, shape (2,) or (3,)
        Position vector relative to the source.

    Returns
    -------
    g : np.ndarray
        Gravitational field vector (m/s²).
    """
    r = np.linalg.norm(r_vec)
    if r < 1e-10:
        return np.zeros_like(r_vec)
    return -G * M / r**3 * r_vec


def escape_velocity(M: float, r: float) -> float:
    """
    Escape velocity from a gravitational well.

    v_esc = √(2·G·M / r)

    Parameters
    ----------
    M : float
        Central mass (kg).
    r : float
        Distance from center (meters).

    Returns
    -------
    v_esc : float
        Escape velocity (m/s).
    """
    return np.sqrt(2 * G * M / r)


# ==============================================================================
# MULTI-SOURCE FIELD SUPERPOSITION
# ==============================================================================

def compute_potential_field(
    masses: List[Tuple[float, np.ndarray]],
    grid_x: np.ndarray,
    grid_y: np.ndarray,
    softening: float = 1e6,
) -> np.ndarray:
    """
    Compute the gravitational potential on a 2D meshgrid from multiple masses.

    Uses the principle of superposition: Φ_total = Σ Φ_i.

    Parameters
    ----------
    masses : list of (mass, position)
        Each entry is (M, np.array([x, y])) in kg and meters.
    grid_x, grid_y : np.ndarray
        2D meshgrid arrays.
    softening : float
        Softening length to avoid singularities (meters).

    Returns
    -------
    potential : np.ndarray
        2D array of gravitational potential values.
    """
    potential = np.zeros_like(grid_x)
    for M, pos in masses:
        dx = grid_x - pos[0]
        dy = grid_y - pos[1]
        r = np.sqrt(dx**2 + dy**2 + softening**2)
        potential += -G * M / r
    return potential


def compute_force_field(
    masses: List[Tuple[float, np.ndarray]],
    grid_x: np.ndarray,
    grid_y: np.ndarray,
    softening: float = 1e6,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute the gravitational force field (per unit mass) on a 2D meshgrid.

    g⃗ = -∇Φ = Σ_i [-G·M_i / r_i³ · r⃗_i]

    Parameters
    ----------
    masses : list of (mass, position)
    grid_x, grid_y : 2D meshgrid arrays
    softening : float
        Softening length.

    Returns
    -------
    gx, gy : np.ndarray
        Components of the gravitational field.
    """
    gx = np.zeros_like(grid_x)
    gy = np.zeros_like(grid_y)
    for M, pos in masses:
        dx = grid_x - pos[0]
        dy = grid_y - pos[1]
        r = np.sqrt(dx**2 + dy**2 + softening**2)
        factor = -G * M / r**3
        gx += factor * dx
        gy += factor * dy
    return gx, gy


def compute_field_magnitude(
    masses: List[Tuple[float, np.ndarray]],
    grid_x: np.ndarray,
    grid_y: np.ndarray,
    softening: float = 1e6,
) -> np.ndarray:
    """
    Compute |g⃗| = √(gx² + gy²) over the grid.
    """
    gx, gy = compute_force_field(masses, grid_x, grid_y, softening)
    return np.sqrt(gx**2 + gy**2)
