"""
Symbolic Mathematics Engine
=============================

SymPy-based symbolic computation for:
  • Metric tensor symbolic representation
  • Einstein field equation display
  • Automated LaTeX generation
  • Christoffel symbol symbolic computation
"""

import sympy as sp
from sympy import symbols, Matrix, sqrt, sin, cos, Function, simplify, latex


def schwarzschild_metric_symbolic():
    """
    Construct the Schwarzschild metric symbolically.
    Returns the metric tensor, coordinates, and LaTeX.
    """
    t, r, theta, phi = symbols('t r theta phi')
    M, G_sym, c_sym = symbols('M G c', positive=True)
    r_s = 2 * G_sym * M / c_sym**2

    f = 1 - r_s / r

    g = Matrix([
        [-f * c_sym**2, 0, 0, 0],
        [0, 1/f, 0, 0],
        [0, 0, r**2, 0],
        [0, 0, 0, r**2 * sin(theta)**2],
    ])

    coords = [t, r, theta, phi]
    return {
        'metric': g,
        'coords': coords,
        'latex': latex(g),
        'line_element': (
            f"ds² = -({latex(f)})c²dt² + ({latex(1/f)})dr² "
            f"+ r²dθ² + r²sin²θ dφ²"
        ),
    }


def alcubierre_metric_symbolic():
    """Construct the Alcubierre warp metric symbolically."""
    t, x, y, z = symbols('t x y z')
    v_s, R_sym, sigma = symbols('v_s R sigma', positive=True)
    c_sym = symbols('c', positive=True)

    x_s = Function('x_s')(t)
    r_s = sqrt((x - x_s)**2 + y**2 + z**2)
    f = Function('f')(r_s)

    line_element = (
        f"ds² = -c²dt² + (dx - v_s·f(r_s)·dt)² + dy² + dz²"
    )

    return {
        'line_element': line_element,
        'shape_function': "f(r_s) = [tanh(σ(r_s+R)) - tanh(σ(r_s-R))] / [2tanh(σR)]",
        'energy_density': "T⁰⁰ = -(c⁴/8πG)·v_s²·(y²+z²)/(2r_s²)·(df/dr_s)²",
    }


def einstein_field_equations_display():
    """Return the Einstein Field Equations in symbolic/LaTeX form."""
    return {
        'equation': "G_μν + Λg_μν = (8πG/c⁴)T_μν",
        'einstein_tensor': "G_μν = R_μν - ½Rg_μν",
        'latex': r"G_{\mu\nu} + \Lambda g_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}",
        'components': {
            'G_μν': 'Einstein tensor (spacetime curvature)',
            'R_μν': 'Ricci tensor (volume-distortion curvature)',
            'R': 'Ricci scalar (trace of Ricci tensor)',
            'g_μν': 'Metric tensor (spacetime geometry)',
            'Λ': 'Cosmological constant (dark energy)',
            'T_μν': 'Stress-energy tensor (matter/energy content)',
        },
    }


def geodesic_equation_display():
    """Return the geodesic equation in LaTeX."""
    return {
        'equation': "d²xᵘ/dτ² + Γᵘ_αβ (dxᵅ/dτ)(dxᵝ/dτ) = 0",
        'latex': r"\frac{d^2 x^\mu}{d\tau^2} + \Gamma^\mu_{\alpha\beta} \frac{dx^\alpha}{d\tau} \frac{dx^\beta}{d\tau} = 0",
        'description': "Free-falling particles follow geodesics — the straightest possible paths in curved spacetime.",
    }


def render_equation_latex(equation_name: str) -> str:
    """Get LaTeX for common physics equations."""
    equations = {
        'newton_gravity': r"F = \frac{GMm}{r^2}",
        'gravitational_potential': r"\Phi = -\frac{GM}{r}",
        'escape_velocity': r"v_{esc} = \sqrt{\frac{2GM}{r}}",
        'vis_viva': r"v^2 = GM\left(\frac{2}{r} - \frac{1}{a}\right)",
        'kepler_third': r"T = 2\pi\sqrt{\frac{a^3}{GM}}",
        'schwarzschild': r"ds^2 = -\left(1-\frac{r_s}{r}\right)c^2 dt^2 + \frac{dr^2}{1-\frac{r_s}{r}} + r^2 d\Omega^2",
        'alcubierre': r"ds^2 = -c^2 dt^2 + (dx - v_s f(r_s) dt)^2 + dy^2 + dz^2",
        'tsiolkovsky': r"\Delta v = v_e \ln\frac{m_0}{m_f}",
        'einstein': r"G_{\mu\nu} + \Lambda g_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}",
        'casimir': r"\frac{E}{A} = -\frac{\pi^2 \hbar c}{720 d^4}",
        'lorentz_force': r"\vec{F} = q(\vec{v} \times \vec{B})",
        'time_dilation': r"\frac{d\tau}{dt} = \sqrt{1 - \frac{r_s}{r}}",
    }
    return equations.get(equation_name, r"\text{Unknown equation}")
