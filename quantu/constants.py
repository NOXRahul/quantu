"""
Physical Constants for QuantU Simulations
==========================================

All constants are in SI units unless otherwise noted.
Sources: CODATA 2018 recommended values via scipy.constants.

Mathematical Reference
----------------------
These constants appear throughout gravitational and relativistic equations:

  • Gravitational force    : F = G·M·m / r²
  • Schwarzschild radius   : r_s = 2·G·M / c²
  • Gravitational potential : Φ = -G·M / r
  • Planck length           : ℓ_P = √(ℏ·G / c³)
"""

import scipy.constants as _sc

# ==============================================================================
# FUNDAMENTAL CONSTANTS
# ==============================================================================

G = _sc.gravitational_constant          # 6.674e-11  m³/(kg·s²)
c = _sc.speed_of_light                  # 2.998e+08  m/s
h = _sc.Planck                          # 6.626e-34  J·s
hbar = _sc.hbar                         # 1.055e-34  J·s
k_B = _sc.Boltzmann                     # 1.381e-23  J/K
epsilon_0 = _sc.epsilon_0               # 8.854e-12  F/m
mu_0 = _sc.mu_0                         # 1.257e-06  N/A²
e_charge = _sc.elementary_charge        # 1.602e-19  C
m_electron = _sc.electron_mass          # 9.109e-31  kg
m_proton = _sc.proton_mass              # 1.673e-27  kg

# ==============================================================================
# ASTRONOMICAL CONSTANTS
# ==============================================================================

M_sun = 1.989e30        # kg — Solar mass
M_earth = 5.972e24      # kg — Earth mass
M_moon = 7.342e22       # kg — Lunar mass
M_jupiter = 1.898e27    # kg — Jupiter mass

R_sun = 6.957e8         # m  — Solar radius
R_earth = 6.371e6       # m  — Earth radius
R_moon = 1.737e6        # m  — Lunar radius

AU = _sc.astronomical_unit  # 1.496e+11 m — Astronomical Unit
ly = _sc.light_year         # 9.461e+15 m — Light-year
pc = _sc.parsec             # 3.086e+16 m — Parsec

# Earth-Sun distance
D_earth_sun = 1.0 * AU     # m
# Earth-Moon distance
D_earth_moon = 3.844e8     # m

# Standard gravitational acceleration at Earth surface
g0 = _sc.g                  # 9.807 m/s²

# ==============================================================================
# DERIVED CONSTANTS
# ==============================================================================

# Schwarzschild radius of the Sun: r_s = 2GM/c²
r_s_sun = 2 * G * M_sun / c**2     # ≈ 2.953 km

# Planck length: ℓ_P = √(ℏG/c³)
import numpy as _np
l_planck = _np.sqrt(hbar * G / c**3)   # ≈ 1.616e-35 m

# Planck mass: m_P = √(ℏc/G)
m_planck = _np.sqrt(hbar * c / G)      # ≈ 2.176e-8 kg

# Planck time: t_P = ℓ_P / c
t_planck = l_planck / c                # ≈ 5.391e-44 s
