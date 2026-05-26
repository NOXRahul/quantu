"""
Numerical ODE/PDE Solvers
==========================

Implements core numerical integration methods used throughout QuantU:

  • RK4 (Runge-Kutta 4th order) — the workhorse of classical mechanics
  • Velocity Verlet — symplectic integrator for Hamiltonian systems
  • Adaptive RK45 wrapper — via scipy.integrate.solve_ivp

Mathematical Background
-----------------------
**Runge-Kutta 4th Order (RK4)**

Given dy/dt = f(t, y), the RK4 update is:

    k₁ = f(tₙ, yₙ)
    k₂ = f(tₙ + h/2, yₙ + h·k₁/2)
    k₃ = f(tₙ + h/2, yₙ + h·k₂/2)
    k₄ = f(tₙ + h, yₙ + h·k₃)
    yₙ₊₁ = yₙ + (h/6)(k₁ + 2k₂ + 2k₃ + k₄)

Local truncation error: O(h⁵), global error: O(h⁴).

**Velocity Verlet** (symplectic, energy-conserving for Hamiltonian systems)

    xₙ₊₁ = xₙ + vₙ·Δt + ½·aₙ·Δt²
    aₙ₊₁ = F(xₙ₊₁) / m
    vₙ₊₁ = vₙ + ½·(aₙ + aₙ₊₁)·Δt

Preserves phase-space volume (Liouville's theorem), making it ideal
for long-duration orbital / N-body simulations.
"""

import numpy as np
from scipy.integrate import solve_ivp
from typing import Callable, Tuple, Optional


# ==============================================================================
# RUNGE-KUTTA 4TH ORDER
# ==============================================================================

def rk4_step(
    f: Callable[[float, np.ndarray], np.ndarray],
    t: float,
    y: np.ndarray,
    h: float,
) -> np.ndarray:
    """
    Perform a single RK4 integration step.

    Parameters
    ----------
    f : callable
        Right-hand side function f(t, y) → dy/dt.
    t : float
        Current time.
    y : np.ndarray
        Current state vector.
    h : float
        Time step size.

    Returns
    -------
    y_next : np.ndarray
        State vector at t + h.
    """
    k1 = f(t, y)
    k2 = f(t + h / 2, y + h * k1 / 2)
    k3 = f(t + h / 2, y + h * k2 / 2)
    k4 = f(t + h, y + h * k3)
    return y + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)


def rk4_integrate(
    f: Callable[[float, np.ndarray], np.ndarray],
    y0: np.ndarray,
    t_span: Tuple[float, float],
    dt: float,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Integrate an ODE system using fixed-step RK4.

    Parameters
    ----------
    f : callable
        Right-hand side f(t, y) → dy/dt.
    y0 : np.ndarray
        Initial state vector, shape (n,).
    t_span : (t_start, t_end)
        Integration interval.
    dt : float
        Fixed time step.

    Returns
    -------
    t_arr : np.ndarray, shape (N,)
        Time points.
    y_arr : np.ndarray, shape (N, n)
        Solution array, each row is the state at t_arr[i].
    """
    t_start, t_end = t_span
    n_steps = int(np.ceil((t_end - t_start) / dt))
    t_arr = np.linspace(t_start, t_end, n_steps + 1)
    y_arr = np.zeros((n_steps + 1, len(y0)))
    y_arr[0] = y0

    y = np.array(y0, dtype=float)
    for i in range(n_steps):
        h = t_arr[i + 1] - t_arr[i]
        y = rk4_step(f, t_arr[i], y, h)
        y_arr[i + 1] = y

    return t_arr, y_arr


# ==============================================================================
# VELOCITY VERLET (SYMPLECTIC)
# ==============================================================================

def velocity_verlet_step(
    x: np.ndarray,
    v: np.ndarray,
    a: np.ndarray,
    accel_func: Callable[[np.ndarray], np.ndarray],
    dt: float,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Single step of the Velocity Verlet integrator.

    Parameters
    ----------
    x : np.ndarray
        Current positions.
    v : np.ndarray
        Current velocities.
    a : np.ndarray
        Current accelerations.
    accel_func : callable
        Function a(x) → acceleration at position x.
    dt : float
        Time step.

    Returns
    -------
    x_new, v_new, a_new : np.ndarray
        Updated positions, velocities, and accelerations.
    """
    x_new = x + v * dt + 0.5 * a * dt**2
    a_new = accel_func(x_new)
    v_new = v + 0.5 * (a + a_new) * dt
    return x_new, v_new, a_new


def velocity_verlet_integrate(
    x0: np.ndarray,
    v0: np.ndarray,
    accel_func: Callable[[np.ndarray], np.ndarray],
    t_span: Tuple[float, float],
    dt: float,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Integrate using Velocity Verlet over a time span.

    Returns
    -------
    t_arr : np.ndarray, shape (N,)
    x_arr : np.ndarray, shape (N, dim)
    v_arr : np.ndarray, shape (N, dim)
    """
    t_start, t_end = t_span
    n_steps = int(np.ceil((t_end - t_start) / dt))
    t_arr = np.linspace(t_start, t_end, n_steps + 1)

    x_arr = np.zeros((n_steps + 1, len(x0)))
    v_arr = np.zeros((n_steps + 1, len(v0)))

    x_arr[0] = x0
    v_arr[0] = v0
    a = accel_func(x0)

    for i in range(n_steps):
        step_dt = t_arr[i + 1] - t_arr[i]
        x, v, a = velocity_verlet_step(x_arr[i], v_arr[i], a, accel_func, step_dt)
        x_arr[i + 1] = x
        v_arr[i + 1] = v

    return t_arr, x_arr, v_arr


# ==============================================================================
# ADAPTIVE RK45 (SCIPY WRAPPER)
# ==============================================================================

def adaptive_rk45(
    f: Callable[[float, np.ndarray], np.ndarray],
    y0: np.ndarray,
    t_span: Tuple[float, float],
    t_eval: Optional[np.ndarray] = None,
    rtol: float = 1e-8,
    atol: float = 1e-10,
    max_step: float = np.inf,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Adaptive-step RK45 integration via scipy.integrate.solve_ivp.

    Useful when fixed-step RK4 is either too slow (large regions
    of smooth evolution) or inaccurate (close encounters in N-body).

    Parameters
    ----------
    f : callable
        RHS function f(t, y).
    y0 : np.ndarray
        Initial state.
    t_span : tuple
        (t_start, t_end).
    t_eval : np.ndarray, optional
        Times at which to store the solution.
    rtol, atol : float
        Relative and absolute tolerances.
    max_step : float
        Maximum allowed step size.

    Returns
    -------
    t_arr, y_arr : np.ndarray
    """
    sol = solve_ivp(
        f, t_span, y0,
        method="RK45",
        t_eval=t_eval,
        rtol=rtol,
        atol=atol,
        max_step=max_step,
        dense_output=False,
    )
    if not sol.success:
        raise RuntimeError(f"Integration failed: {sol.message}")
    return sol.t, sol.y.T


# ==============================================================================
# GEODESIC EQUATION SOLVER
# ==============================================================================

def geodesic_solver(
    christoffel_func: Callable[[np.ndarray], np.ndarray],
    x0: np.ndarray,
    u0: np.ndarray,
    tau_span: Tuple[float, float],
    dtau: float,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Solve the geodesic equation:

        d²xᵘ/dτ² + Γᵘ_αβ (dxᵅ/dτ)(dxᵝ/dτ) = 0

    This governs the motion of free-falling particles in curved spacetime.

    Parameters
    ----------
    christoffel_func : callable
        Given position x (shape (n,)), returns Christoffel symbols
        Γ as array of shape (n, n, n) where Γ[mu, alpha, beta].
    x0 : np.ndarray, shape (n,)
        Initial coordinates.
    u0 : np.ndarray, shape (n,)
        Initial 4-velocity dxᵘ/dτ.
    tau_span : tuple
        (τ_start, τ_end) — proper time interval.
    dtau : float
        Proper time step.

    Returns
    -------
    tau_arr, x_arr, u_arr : np.ndarray
    """
    n = len(x0)

    def geodesic_rhs(_tau, state):
        x = state[:n]
        u = state[n:]
        gamma = christoffel_func(x)
        # d²xᵘ/dτ² = -Γᵘ_αβ uᵅ uᵝ
        dudt = np.zeros(n)
        for mu in range(n):
            for alpha in range(n):
                for beta in range(n):
                    dudt[mu] -= gamma[mu, alpha, beta] * u[alpha] * u[beta]
        return np.concatenate([u, dudt])

    state0 = np.concatenate([x0, u0])
    tau_arr, state_arr = rk4_integrate(geodesic_rhs, state0, tau_span, dtau)

    x_arr = state_arr[:, :n]
    u_arr = state_arr[:, n:]
    return tau_arr, x_arr, u_arr
