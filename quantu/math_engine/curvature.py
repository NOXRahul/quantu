"""
Curvature Computations
========================

Implements curvature calculations for embedded surfaces and spacetime:
  • Gaussian curvature for 2D surfaces
  • Ricci scalar from metric
  • Geodesic deviation visualization
"""

import numpy as np


def gaussian_curvature_surface(X, Y, Z):
    """
    Compute Gaussian curvature K of a surface z = f(x,y).

    K = (f_xx · f_yy - f_xy²) / (1 + f_x² + f_y²)²

    Parameters
    ----------
    X, Y, Z : 2D meshgrid arrays

    Returns
    -------
    K : 2D array of Gaussian curvature values
    """
    # First derivatives
    Zy, Zx = np.gradient(Z)
    # Second derivatives
    Zxy, Zxx = np.gradient(Zx)
    Zyy, _ = np.gradient(Zy)

    numerator = Zxx * Zyy - Zxy**2
    denominator = (1 + Zx**2 + Zy**2)**2

    K = numerator / np.maximum(denominator, 1e-20)
    return K


def mean_curvature_surface(X, Y, Z):
    """
    Mean curvature H of a surface z = f(x,y).

    H = [(1+f_y²)f_xx - 2f_xf_yf_xy + (1+f_x²)f_yy] / [2(1+f_x²+f_y²)^(3/2)]
    """
    Zy, Zx = np.gradient(Z)
    Zxy, Zxx = np.gradient(Zx)
    Zyy, _ = np.gradient(Zy)

    num = ((1 + Zy**2) * Zxx - 2 * Zx * Zy * Zxy + (1 + Zx**2) * Zyy)
    den = 2 * (1 + Zx**2 + Zy**2)**1.5

    return num / np.maximum(den, 1e-20)


def ricci_scalar_from_metric_2d(g11, g22, g12=None):
    """
    Compute Ricci scalar for a 2D diagonal metric.

    For a 2D metric ds² = g₁₁dx² + g₂₂dy², the Gaussian curvature
    (which equals half the Ricci scalar) can be computed from the
    metric components.

    This is a simplified educational computation.
    """
    # For diagonal 2D metric, R = 2K where K is Gaussian curvature
    # K = -1/(2√(g₁₁g₂₂)) [∂/∂x(∂√g₂₂/∂x / √g₁₁) + ∂/∂y(∂√g₁₁/∂y / √g₂₂)]
    sg1 = np.sqrt(np.maximum(g11, 1e-20))
    sg2 = np.sqrt(np.maximum(g22, 1e-20))

    # Numerical derivatives
    d_sg2_x = np.gradient(sg2, axis=1)
    d_sg1_y = np.gradient(sg1, axis=0)

    term1 = np.gradient(d_sg2_x / sg1, axis=1)
    term2 = np.gradient(d_sg1_y / sg2, axis=0)

    K = -1 / (sg1 * sg2) * (term1 + term2)
    R = 2 * K  # Ricci scalar = 2 × Gaussian curvature in 2D
    return R, K
