# 🌌 QuantU — Gravity Field Simulation & Advanced Propulsion Research Engine

<div align="center">

**A computational physics platform for simulating gravitational fields, spacetime curvature, and advanced propulsion concepts.**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-ff4b4b?logo=streamlit)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Educational](https://img.shields.io/badge/Purpose-Educational-orange)]()

</div>

---

## ⚠️ Disclaimer

This project is for **educational, simulation, and theoretical exploration** purposes only. It does NOT claim to produce real anti-gravity technology. Speculative concepts are clearly distinguished from established physics throughout the codebase and UI.

---

## 🚀 Features

### Established Physics
- **Newtonian Gravity** — Force fields, potentials, escape velocity, multi-body superposition
- **Orbital Mechanics** — Kepler orbits, Hohmann transfers, vis-viva equation
- **N-Body Simulation** — Velocity Verlet integrator with energy conservation tracking
- **Schwarzschild Metric** — Black hole geometry, gravitational lensing, time dilation
- **Ion Propulsion** — Tsiolkovsky equation, thrust-Isp trade-offs, trajectory planning
- **Tensor Mathematics** — Metric tensors, Christoffel symbols, Ricci tensor

### Speculative / Theoretical (⚠️)
- **Alcubierre Warp Drive** — Warp bubble visualization and exotic energy density
- **Frame Dragging** — Kerr metric and ergosphere visualization
- **Exotic Matter** — Casimir effect, negative energy density fields
- **Field Propulsion** — Theoretical concepts for educational comparison

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/rahulkafle/quantu.git
cd quantu

# Create virtual environment
python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

## 🖥️ Launch Dashboard

```bash
streamlit run dashboard/app.py
```

The dashboard opens at `http://localhost:8501` with 6 interactive simulation labs.

---

## 🏗️ Architecture

```
quantu/
├── quantu/                     # Core Python package
│   ├── constants.py            # Physical constants (SI)
│   ├── core/                   # Phase 1: Physics foundation
│   │   ├── gravity.py          #   Newtonian gravity
│   │   ├── orbital.py          #   Orbital mechanics
│   │   └── nbody.py            #   N-body simulation
│   ├── fields/                 # Phase 2: Field computation
│   │   ├── scalar_field.py     #   Scalar fields (potential)
│   │   ├── vector_field.py     #   Vector fields (force)
│   │   └── spacetime_grid.py   #   Spacetime curvature grid
│   ├── relativity/             # Phase 3: General Relativity
│   │   ├── schwarzschild.py    #   Black hole metrics
│   │   ├── alcubierre.py       #   ⚠️ Warp drive metric
│   │   ├── frame_dragging.py   #   Kerr metric
│   │   └── exotic_matter.py    #   ⚠️ Negative energy
│   ├── propulsion/             # Phase 4: Propulsion
│   │   ├── ion_drive.py        #   Ion thruster model
│   │   ├── em_drive.py         #   ⚠️ EM propulsion
│   │   ├── field_propulsion.py #   ⚠️ Field propulsion
│   │   └── trajectory.py       #   Trajectory planner
│   ├── math_engine/            # Phase 5: Mathematics
│   │   ├── solvers.py          #   RK4, Verlet, RK45
│   │   ├── tensors.py          #   Metric tensors
│   │   ├── symbolic.py         #   SymPy integration
│   │   └── curvature.py        #   Gaussian curvature
│   └── viz/                    # Visualization
│       ├── plotly_viz.py       #   Plotly dark-theme charts
│       ├── matplotlib_viz.py   #   Publication-quality plots
│       └── color_maps.py       #   Scientific color palettes
├── dashboard/                  # Phase 6: Streamlit UI
│   ├── app.py                  #   Main entry point
│   └── pages/
│       ├── 1_gravity_lab.py
│       ├── 2_orbital_mechanics.py
│       ├── 3_spacetime.py
│       ├── 4_warp_drive.py
│       ├── 5_propulsion.py
│       └── 6_math_sandbox.py
├── tests/                      # Unit tests
├── docs/                       # Documentation
├── requirements.txt
└── setup.py
```

---

## 🔬 Core Equations

| Concept | Equation | Status |
|---------|----------|--------|
| Newtonian Gravity | F = GMm/r² | ✅ Established |
| Gravitational Potential | Φ = -GM/r | ✅ Established |
| Schwarzschild Metric | ds² = -(1-rₛ/r)c²dt² + ... | ✅ Established |
| Alcubierre Metric | ds² = -c²dt² + (dx - vₛf·dt)² + ... | ⚠️ Speculative |
| Tsiolkovsky Equation | Δv = vₑ·ln(m₀/mf) | ✅ Established |
| Einstein Field Eqs | Gμν + Λgμν = (8πG/c⁴)Tμν | ✅ Established |

---

## 🗺️ Roadmap

- [x] Phase 1: Physics Foundation (gravity, orbital, N-body)
- [x] Phase 2: Field Visualization Engine
- [x] Phase 3: Advanced Theoretical Concepts (GR, warp drive)
- [x] Phase 4: Propulsion Simulation
- [x] Phase 5: Mathematical Engine
- [x] Phase 6: Interactive Dashboard
- [ ] Phase 7: GPU acceleration (CuPy/PyTorch)
- [ ] Phase 8: AI-generated field optimization
- [ ] Phase 9: Procedural universe simulation

---

## 👤 Author

**Rahul Kafle** — Computational Physics & Aerospace Engineering

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
