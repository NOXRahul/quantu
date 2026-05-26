"""
QuantU — Gravity Field Simulation & Advanced Propulsion Research Engine
========================================================================
Main Streamlit Dashboard Entry Point

Launch: streamlit run dashboard/app.py
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ── Page Config ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="QuantU · Gravity Research Engine",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
)

from theme import apply_theme, page_header, section_divider, COLORS

apply_theme()

# ── Sidebar ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 0.5rem 0;">
        <div style="font-size:2.5rem; filter: drop-shadow(0 0 12px rgba(88,166,255,0.5));">🌌</div>
        <div style="font-size:1.4rem; font-weight:800;
             background: linear-gradient(135deg, #58a6ff, #bc8cff);
             -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            QuantU
        </div>
        <div style="font-size:0.75rem; color:#8b949e; letter-spacing:0.08em; text-transform:uppercase;">
            Gravity Research Engine
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    ### 🧭 Navigation
    Use the sidebar pages to access:
    - 🌍 **Gravity Lab**
    - 🪐 **Orbital Mechanics**
    - 🕳️ **Spacetime Curvature**
    - 🚀 **Warp Drive Explorer**
    - ⚡ **Propulsion Simulator**
    - 📐 **Math Sandbox**
    """)
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; padding:0.5rem 0;">
        <div style="font-size:0.7rem; color:#6e7681; letter-spacing:0.05em;">
            v0.2.0 · EDUCATIONAL USE ONLY
        </div>
        <div style="font-size:0.65rem; color:#30363d; margin-top:0.3rem;">
            Built with Python · NumPy · Plotly · Streamlit
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Main Content ─────────────────────────────────────────────────────
page_header(
    "QuantU",
    "Gravity Field Simulation & Advanced Propulsion Research Engine",
    icon="🌌"
)

# Stats with animated gradient
st.markdown("""
<div class="stats-container">
    <div class="stat-item">
        <div class="number">6</div>
        <div class="label">Simulation Labs</div>
    </div>
    <div class="stat-item">
        <div class="number">12+</div>
        <div class="label">Physics Models</div>
    </div>
    <div class="stat-item">
        <div class="number">4</div>
        <div class="label">Integrators</div>
    </div>
    <div class="stat-item">
        <div class="number">3</div>
        <div class="label">Metric Tensors</div>
    </div>
    <div class="stat-item">
        <div class="number">40+</div>
        <div class="label">Source Files</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Module Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="module-card">
        <h3>🌍 Gravity Lab <span class="status-badge badge-established">Established</span></h3>
        <p>Newtonian gravitational fields, potential maps, escape velocity calculator,
        and multi-body force superposition with interactive mass placement.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="module-card">
        <h3>🕳️ Spacetime Curvature <span class="status-badge badge-established">Established</span></h3>
        <p>Schwarzschild metric, gravitational lensing, Flamm's paraboloid,
        spacetime grid deformation, and Gaussian curvature analysis.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="module-card">
        <h3>🪐 Orbital Mechanics <span class="status-badge badge-established">Established</span></h3>
        <p>Kepler orbits with animation, Hohmann transfers, N-body simulation with
        Velocity Verlet integration and energy conservation tracking.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="module-card">
        <h3>🚀 Warp Drive Explorer <span class="status-badge badge-speculative">Speculative</span></h3>
        <p>Alcubierre warp metric visualization, warp bubble geometry,
        energy density computation, and exotic matter analysis.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="module-card">
        <h3>⚡ Propulsion Lab <span class="status-badge badge-established">Established</span></h3>
        <p>Ion thruster modeling, Tsiolkovsky equation, trajectory planning,
        delta-v budget analysis, and thruster comparison.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="module-card">
        <h3>📐 Math Sandbox <span class="status-badge badge-established">Established</span></h3>
        <p>Symbolic tensor computation, LaTeX equation explorer,
        metric tensor builder, and relativistic effects visualizer.</p>
    </div>
    """, unsafe_allow_html=True)

# Disclaimer
st.markdown("""
<div class="disclaimer">
    ⚠️ <strong>Educational Disclaimer:</strong> This platform is for educational,
    simulation, and theoretical exploration purposes only. Speculative concepts
    (marked with ⚠️) are clearly distinguished from established physics.
    No claims of experimental viability are made for theoretical propulsion concepts.
</div>
""", unsafe_allow_html=True)

# Core Equations
section_divider("Core Equations")

eq1, eq2, eq3 = st.columns(3)
with eq1:
    st.latex(r"F = \frac{GMm}{r^2}")
    st.caption("Newton's Law of Gravitation")
with eq2:
    st.latex(r"ds^2 = -\left(1-\frac{r_s}{r}\right)c^2 dt^2 + \frac{dr^2}{1-r_s/r} + r^2 d\Omega^2")
    st.caption("Schwarzschild Metric")
with eq3:
    st.latex(r"G_{\mu\nu} + \Lambda g_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}")
    st.caption("Einstein Field Equations")
