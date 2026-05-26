"""
Tensor Calculations
====================

Implements metric tensor construction and basic tensor operations
for educational GR visualization.

Supported metrics:
  • Minkowski (flat spacetime)
  • Schwarzschild (non-rotating black hole)
  • Kerr simplified (rotating, equatorial)
  • FLRW (cosmological)
"""

import numpy as np
from ..constants import G, c


def minkowski_metric():
    """Minkowski metric η_μν = diag(-1, 1, 1, 1)."""
    return np.diag([-1.0, 1.0, 1.0, 1.0])


def schwarzschild_metric(r, M, theta=np.pi/2):
    """
    Schwarzschild metric g_μν at radius r.
    Coordinates: (t, r, θ, φ)

    g = diag(-(1-r_s/r), 1/(1-r_s/r), r², r²sin²θ)
    """
    r_s = 2 * G * M / c**2
    f = 1 - r_s / r
    g = np.zeros((4, 4))
    g[0, 0] = -f * c**2
    g[1, 1] = 1.0 / f
    g[2, 2] = r**2
    g[3, 3] = r**2 * np.sin(theta)**2
    return g


def kerr_metric_equatorial(r, M, a):
    """
    Simplified Kerr metric in the equatorial plane (θ=π/2).
    a = J/(Mc) is the spin parameter.
    """
    r_s = 2 * G * M / c**2
    Sigma = r**2  # At θ=π/2: Σ = r²
    Delta = r**2 - r_s * r + a**2
    g = np.zeros((4, 4))
    g[0, 0] = -(1 - r_s * r / Sigma) * c**2
    g[0, 3] = -r_s * r * a / Sigma
    g[3, 0] = g[0, 3]
    g[1, 1] = Sigma / Delta
    g[2, 2] = Sigma
    g[3, 3] = (r**2 + a**2 + r_s * r * a**2 / Sigma)
    return g


def christoffel_symbols_numerical(metric_func, coords, dx=1e-6):
    """
    Compute Christoffel symbols Γᵘ_αβ numerically.

    Γᵘ_αβ = ½ gᵘˡ (∂_α g_βλ + ∂_β g_αλ - ∂_λ g_αβ)

    Parameters
    ----------
    metric_func : callable
        Function(coords) → metric tensor g_μν as (n,n) array.
    coords : np.ndarray, shape (n,)
        Current coordinates.
    dx : float
        Finite difference step.
    """
    n = len(coords)
    g = metric_func(coords)
    g_inv = np.linalg.inv(g)

    # Compute metric derivatives ∂_σ g_μν
    dg = np.zeros((n, n, n))  # dg[sigma, mu, nu]
    for sigma in range(n):
        coords_p = coords.copy()
        coords_m = coords.copy()
        coords_p[sigma] += dx
        coords_m[sigma] -= dx
        g_p = metric_func(coords_p)
        g_m = metric_func(coords_m)
        dg[sigma] = (g_p - g_m) / (2 * dx)

    # Christoffel symbols
    gamma = np.zeros((n, n, n))
    for mu in range(n):
        for alpha in range(n):
            for beta in range(n):
                for lam in range(n):
                    gamma[mu, alpha, beta] += 0.5 * g_inv[mu, lam] * (
                        dg[alpha, beta, lam] +
                        dg[beta, alpha, lam] -
                        dg[lam, alpha, beta]
                    )
    return gamma


def ricci_tensor_numerical(metric_func, coords, dx=1e-6):
    """
    Compute Ricci tensor R_μν numerically (educational, not optimized).
    R_μν = ∂_λ Γᵏ_μν - ∂_ν Γᵏ_μλ + Γᵏ_λσ Γᵒ_μν - Γᵏ_νσ Γᵒ_μλ
    """
    n = len(coords)
    gamma = christoffel_symbols_numerical(metric_func, coords, dx)

    # Compute derivatives of Christoffel symbols
    dgamma = np.zeros((n, n, n, n))  # dgamma[d, mu, alpha, beta]
    for d in range(n):
        c_p = coords.copy()
        c_m = coords.copy()
        c_p[d] += dx
        c_m[d] -= dx
        g_p = christoffel_symbols_numerical(metric_func, c_p, dx)
        g_m = christoffel_symbols_numerical(metric_func, c_m, dx)
        dgamma[d] = (g_p - g_m) / (2 * dx)

    R = np.zeros((n, n))
    for mu in range(n):
        for nu in range(n):
            for lam in range(n):
                R[mu, nu] += dgamma[lam, lam, mu, nu] - dgamma[nu, lam, mu, lam]
                for sig in range(n):
                    R[mu, nu] += (gamma[lam, lam, sig] * gamma[sig, mu, nu]
                                  - gamma[lam, nu, sig] * gamma[sig, mu, lam])
    return R
