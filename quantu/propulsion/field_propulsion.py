"""
Theoretical Field Propulsion
==============================

⚠️ SPECULATIVE — Educational visualization only.

Explores hypothetical propulsion via gravitational field manipulation:
  • Gravity gradient propulsion concept
  • Field asymmetry visualization
  • Energy requirement estimation

These models are NOT experimentally verified. They serve as educational
tools for understanding why "reactionless drives" violate known physics
(conservation of momentum) and the enormous energy scales involved.
"""

import numpy as np
from ..constants import G, c


class FieldPropulsionConcept:
    """
    ⚠️ SPECULATIVE: Theoretical field propulsion visualization.
    For educational demonstration of why field propulsion is difficult.
    """

    def __init__(self, field_strength=1.0, asymmetry=0.1):
        self.field_strength = field_strength
        self.asymmetry = asymmetry

    def asymmetric_field(self, X, Y):
        """
        Visualize an asymmetric gravitational-like field.
        Shows directional field gradient that WOULD produce net force
        if such manipulation were possible.
        """
        r = np.sqrt(X**2 + Y**2)
        r = np.maximum(r, 0.1)
        # Asymmetric potential: stronger in +x than -x
        potential = -self.field_strength / r * (1 + self.asymmetry * X / r)
        return potential

    def gravity_gradient_force(self, X, Y, M=1.0, delta_g=0.01):
        """
        Tidal / gravity gradient force visualization.
        In real physics, this is used by gravity gradient stabilization
        of satellites — NOT propulsion.
        """
        r = np.sqrt(X**2 + Y**2)
        r = np.maximum(r, 0.1)
        g_base = G * M / r**2
        # Gradient: dg/dr = -2GM/r³
        gradient = -2 * G * M / r**3
        Fx = gradient * X / r * delta_g
        Fy = gradient * Y / r * delta_g
        return Fx, Fy

    def energy_requirement(self, mass, delta_v, method='field'):
        """
        Estimate energy requirements for various propulsion methods.
        Shows how field propulsion would require enormous energy.
        """
        # Kinetic energy for conventional propulsion
        E_kinetic = 0.5 * mass * delta_v**2
        # Mass-energy equivalence limit
        E_mass = mass * c**2
        # Hypothetical field propulsion (assuming 0.01% efficiency)
        E_field = E_kinetic / 0.0001

        return {
            'kinetic_J': E_kinetic,
            'mass_energy_J': E_mass,
            'field_propulsion_J': E_field,
            'kinetic_GJ': E_kinetic / 1e9,
            'ratio_to_mass_energy': E_kinetic / E_mass,
        }
