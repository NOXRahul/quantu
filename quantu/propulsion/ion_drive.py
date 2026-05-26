"""
Ion Propulsion Module
======================

Models ion thruster physics — the most mature form of electric propulsion.

Key Equations:
  • Thrust:                F = ṁ · v_e
  • Exhaust velocity:      v_e = Isp · g₀
  • Specific impulse:      Isp = v_e / g₀
  • Tsiolkovsky equation:  Δv = v_e · ln(m₀/m_f)
  • Power:                 P = ½ · ṁ · v_e²
  • Efficiency:            η = F · v_e / (2P)

Typical values (NASA NEXT ion thruster):
  • Isp ≈ 4190 s
  • Thrust ≈ 0.236 N
  • Power ≈ 6.9 kW
"""

import numpy as np
from ..constants import g0


class IonThruster:
    """Ion propulsion performance model."""

    def __init__(self, isp=3000.0, power_kw=5.0, efficiency=0.65):
        """
        Parameters
        ----------
        isp : float — specific impulse (seconds)
        power_kw : float — input power (kilowatts)
        efficiency : float — total efficiency (0 to 1)
        """
        self.isp = isp
        self.power = power_kw * 1000  # Convert to watts
        self.efficiency = efficiency
        self.v_e = isp * g0  # Exhaust velocity (m/s)

    @property
    def thrust(self) -> float:
        """Thrust F = 2ηP/v_e (Newtons)."""
        return 2 * self.efficiency * self.power / self.v_e

    @property
    def mass_flow_rate(self) -> float:
        """Mass flow rate ṁ = F/v_e (kg/s)."""
        return self.thrust / self.v_e

    def delta_v(self, m0: float, m_propellant: float) -> float:
        """
        Tsiolkovsky rocket equation: Δv = v_e · ln(m₀/(m₀ - m_p))

        Parameters
        ----------
        m0 : float — initial mass (kg)
        m_propellant : float — propellant mass (kg)
        """
        mf = m0 - m_propellant
        if mf <= 0:
            return float('inf')
        return self.v_e * np.log(m0 / mf)

    def burn_time(self, m_propellant: float) -> float:
        """Time to expend propellant: t = m_p / ṁ (seconds)."""
        return m_propellant / self.mass_flow_rate

    def propellant_for_dv(self, m0: float, dv: float) -> float:
        """Propellant mass needed: m_p = m₀(1 - e^(-Δv/v_e))."""
        return m0 * (1 - np.exp(-dv / self.v_e))

    def performance_envelope(self, isp_range=(1000, 10000), n_points=100):
        """
        Compute thrust vs Isp trade-off at fixed power.
        F = 2ηP/(Isp·g₀)
        """
        isp_arr = np.linspace(*isp_range, n_points)
        v_e_arr = isp_arr * g0
        thrust_arr = 2 * self.efficiency * self.power / v_e_arr
        mdot_arr = thrust_arr / v_e_arr
        return {
            'isp': isp_arr,
            'thrust_mN': thrust_arr * 1000,
            'mass_flow_mg_s': mdot_arr * 1e6,
            'exhaust_vel_km_s': v_e_arr / 1000,
        }
