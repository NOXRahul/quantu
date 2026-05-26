"""QuantU Dashboard — Math Sandbox Page"""
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from quantu.math_engine.symbolic import (
    render_equation_latex, schwarzschild_metric_symbolic,
    einstein_field_equations_display, geodesic_equation_display,
)
from quantu.math_engine.tensors import minkowski_metric, schwarzschild_metric
from quantu.constants import M_sun, G, c

st.set_page_config(page_title="QuantU · Math Sandbox", page_icon="📐", layout="wide")

from theme import apply_theme, page_header, section_divider, info_tooltip, PLOTLY_LAYOUT, COLORS
apply_theme()

page_header("Mathematical Sandbox",
            "Explore the mathematics of gravity, spacetime, and propulsion", "📐")

tab1, tab2, tab3 = st.tabs(["📖 Equation Explorer", "🔢 Metric Tensors", "📊 Relativistic Effects"])

# ═══════════════════════════════════════════════════════════════════════
# TAB 1: EQUATION EXPLORER
# ═══════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### Core Physics Equations")
    info_tooltip("Click any equation to expand it and see the mathematical formulation "
                 "with a plain-English explanation of what it means physically.")

    equations = {
        "Newton's Gravitational Force": 'newton_gravity',
        "Gravitational Potential": 'gravitational_potential',
        "Escape Velocity": 'escape_velocity',
        "Vis-Viva Equation": 'vis_viva',
        "Kepler's Third Law": 'kepler_third',
        "Schwarzschild Metric": 'schwarzschild',
        "Alcubierre Warp Metric": 'alcubierre',
        "Tsiolkovsky Rocket Equation": 'tsiolkovsky',
        "Einstein Field Equations": 'einstein',
        "Casimir Energy Density": 'casimir',
        "Lorentz Force": 'lorentz_force',
        "Gravitational Time Dilation": 'time_dilation',
    }

    descriptions = {
        'newton_gravity': "The fundamental law of gravity: every mass attracts every other mass with a force proportional to their masses and inversely proportional to the square of the distance.",
        'gravitational_potential': "The gravitational potential energy per unit mass at distance r from mass M. It's always negative — you need to add energy to escape.",
        'escape_velocity': "The minimum velocity needed to escape a gravitational well without further propulsion. Independent of the escaping object's mass!",
        'vis_viva': "Relates orbital velocity to position and orbital shape. Works for all conic sections (circles, ellipses, parabolas, hyperbolas).",
        'kepler_third': "The square of the orbital period is proportional to the cube of the semi-major axis. Discovered empirically by Kepler, derived by Newton.",
        'schwarzschild': "The spacetime geometry around a non-rotating, uncharged, spherically symmetric mass. The simplest black hole solution.",
        'alcubierre': "⚠️ SPECULATIVE: A spacetime geometry allowing effective FTL travel via space contraction/expansion. Requires exotic matter.",
        'tsiolkovsky': "The fundamental rocket equation relating Δv to exhaust velocity and mass ratio. The tyranny of the rocket equation!",
        'einstein': "The master equation of General Relativity: spacetime geometry (left side) = matter-energy content (right side).",
        'casimir': "Quantum vacuum energy density between two parallel conducting plates. Experimentally verified — real negative energy density!",
        'lorentz_force': "The force on a charged particle moving through electromagnetic fields. Foundation of all electric propulsion.",
        'time_dilation': "Clocks run slower in stronger gravitational fields. GPS satellites must correct for this effect!",
    }

    # Category grouping
    categories = {
        "🌍 Classical Mechanics": ['newton_gravity', 'gravitational_potential', 'escape_velocity',
                                    'vis_viva', 'kepler_third'],
        "🕳️ General Relativity": ['schwarzschild', 'einstein', 'time_dilation'],
        "🚀 Propulsion & EM": ['tsiolkovsky', 'lorentz_force'],
        "⚠️ Speculative / Quantum": ['alcubierre', 'casimir'],
    }

    eq_name_to_key = {v: k for k, v in equations.items()}

    for cat_name, cat_keys in categories.items():
        st.markdown(f"#### {cat_name}")
        for key in cat_keys:
            name = eq_name_to_key.get(key, key)
            with st.expander(f"**{name}**"):
                st.latex(render_equation_latex(key))
                st.markdown(descriptions[key])
        st.markdown("")

    section_divider("Einstein Field Equations — Components")
    efe = einstein_field_equations_display()
    st.latex(efe['latex'])

    comp_cols = st.columns(2)
    items = list(efe['components'].items())
    mid = len(items) // 2
    with comp_cols[0]:
        for comp, desc in items[:mid]:
            st.markdown(f"""
            <div style="background:rgba(22,27,34,0.8); border:1px solid #30363d;
                        border-radius:8px; padding:0.6rem 0.8rem; margin:0.3rem 0;">
                <span style="color:#58a6ff; font-weight:600; font-family:'JetBrains Mono';">{comp}</span>
                <span style="color:#8b949e; font-size:0.85rem;"> — {desc}</span>
            </div>
            """, unsafe_allow_html=True)
    with comp_cols[1]:
        for comp, desc in items[mid:]:
            st.markdown(f"""
            <div style="background:rgba(22,27,34,0.8); border:1px solid #30363d;
                        border-radius:8px; padding:0.6rem 0.8rem; margin:0.3rem 0;">
                <span style="color:#bc8cff; font-weight:600; font-family:'JetBrains Mono';">{comp}</span>
                <span style="color:#8b949e; font-size:0.85rem;"> — {desc}</span>
            </div>
            """, unsafe_allow_html=True)

    section_divider("Geodesic Equation")
    geo = geodesic_equation_display()
    st.latex(geo['latex'])
    st.markdown(geo['description'])

# ═══════════════════════════════════════════════════════════════════════
# TAB 2: METRIC TENSORS
# ═══════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### Metric Tensor Explorer")
    info_tooltip("The metric tensor g_μν defines the geometry of spacetime. "
                 "It tells you how to measure distances and angles in curved space.")

    metric_choice = st.selectbox("Select metric", [
        "Minkowski (Flat Spacetime)",
        "Schwarzschild (Black Hole)",
    ])

    if metric_choice.startswith("Minkowski"):
        g = minkowski_metric()
        st.markdown("**Minkowski metric** — flat spacetime of Special Relativity")
        st.latex(r"\eta_{\mu\nu} = \text{diag}(-1, 1, 1, 1)")
        info_tooltip("In flat spacetime, the metric is simply diagonal with signature (-,+,+,+). "
                     "The minus sign on the time component is what makes time different from space.")
    else:
        mc1, mc2 = st.columns(2)
        with mc1:
            r_val = st.slider("Radius r (×r_s)", 1.1, 20.0, 3.0, 0.1)
        with mc2:
            bh_mass = st.slider("Mass (×M☉)", 1, 100, 10) * M_sun
        r_s = 2 * G * bh_mass / c**2
        g = schwarzschild_metric(r_val * r_s, bh_mass)
        st.markdown(f"**Schwarzschild metric** at r = {r_val:.1f}·r_s")
        st.markdown(f"Schwarzschild radius: r_s = `{r_s:.3e}` m")

    # Color-coded tensor display
    st.markdown("#### g_μν =")
    col_labels = ["t", "r", "θ", "φ"]

    # Build colored tensor table
    table_html = """
    <div style="overflow-x:auto;">
    <table style="border-collapse:collapse; font-family:'JetBrains Mono',monospace;
                  font-size:0.85rem; width:100%; background:rgba(13,17,23,0.8);
                  border:1px solid #30363d; border-radius:8px;">
    <tr style="background:rgba(22,27,34,0.9);">
        <th style="padding:8px 12px; color:#8b949e; border:1px solid #21262d;"></th>
    """
    for label in col_labels:
        table_html += f'<th style="padding:8px 12px; color:#58a6ff; border:1px solid #21262d; text-align:center;">{label}</th>'
    table_html += "</tr>"

    for i in range(4):
        table_html += f'<tr><td style="padding:8px 12px; color:#bc8cff; font-weight:600; border:1px solid #21262d;">{col_labels[i]}</td>'
        for j in range(4):
            val = g[i, j]
            if abs(val) < 1e-15:
                color = "#30363d"
                display = "0"
            elif i == j:
                color = "#3fb950" if val > 0 else "#f85149"
                display = f"{val:.6e}"
            else:
                color = "#d29922"
                display = f"{val:.6e}"
            table_html += f'<td style="padding:8px 12px; color:{color}; border:1px solid #21262d; text-align:right;">{display}</td>'
        table_html += "</tr>"
    table_html += "</table></div>"
    st.markdown(table_html, unsafe_allow_html=True)

    # Determinant and properties
    section_divider("Tensor Properties")
    det_g = np.linalg.det(g)

    p1, p2, p3 = st.columns(3)
    with p1:
        st.metric("det(g_μν)", f"{det_g:.6e}")
    with p2:
        trace = np.trace(g)
        st.metric("Tr(g_μν)", f"{trace:.6f}")
    with p3:
        sig = np.sign(np.diag(g))
        sig_str = "(" + ",".join("+" if s > 0 else "−" for s in sig) + ")"
        st.metric("Signature", sig_str)

    # Inverse metric
    try:
        g_inv = np.linalg.inv(g)
        st.markdown("#### g^μν (inverse) =")

        inv_html = """
        <div style="overflow-x:auto;">
        <table style="border-collapse:collapse; font-family:'JetBrains Mono',monospace;
                      font-size:0.85rem; width:100%; background:rgba(13,17,23,0.8);
                      border:1px solid #30363d; border-radius:8px;">
        <tr style="background:rgba(22,27,34,0.9);">
            <th style="padding:8px 12px; color:#8b949e; border:1px solid #21262d;"></th>
        """
        for label in col_labels:
            inv_html += f'<th style="padding:8px 12px; color:#58a6ff; border:1px solid #21262d; text-align:center;">{label}</th>'
        inv_html += "</tr>"

        for i in range(4):
            inv_html += f'<tr><td style="padding:8px 12px; color:#bc8cff; font-weight:600; border:1px solid #21262d;">{col_labels[i]}</td>'
            for j in range(4):
                val = g_inv[i, j]
                if abs(val) < 1e-15:
                    color = "#30363d"
                    display = "0"
                elif i == j:
                    color = "#3fb950" if val > 0 else "#f85149"
                    display = f"{val:.6e}"
                else:
                    color = "#d29922"
                    display = f"{val:.6e}"
                inv_html += f'<td style="padding:8px 12px; color:{color}; border:1px solid #21262d; text-align:right;">{display}</td>'
            inv_html += "</tr>"
        inv_html += "</table></div>"
        st.markdown(inv_html, unsafe_allow_html=True)

        # Verify g · g^-1 = I
        identity_check = g @ g_inv
        err = np.max(np.abs(identity_check - np.eye(4)))
        if err < 1e-10:
            st.success(f"✅ Verified: g · g⁻¹ = I (max error: {err:.2e})")
        else:
            st.warning(f"⚠️ g · g⁻¹ ≠ I (max error: {err:.2e})")

    except np.linalg.LinAlgError:
        st.error("Metric is singular at this radius — cannot compute inverse.")

    # Spacetime interval calculator
    section_divider("Spacetime Interval Calculator")
    info_tooltip("The spacetime interval ds² determines whether two events are separated "
                 "by a timelike (ds² < 0), spacelike (ds² > 0), or lightlike (ds² = 0) interval.")

    ic1, ic2, ic3, ic4 = st.columns(4)
    with ic1:
        dt = st.number_input("dt (s)", value=1.0, format="%.4f", key="si_dt")
    with ic2:
        dr = st.number_input("dr (m)", value=0.0, format="%.4f", key="si_dr")
    with ic3:
        dtheta = st.number_input("dθ (rad)", value=0.0, format="%.4f", key="si_dth")
    with ic4:
        dphi = st.number_input("dφ (rad)", value=0.0, format="%.4f", key="si_dphi")

    dx = np.array([dt, dr, dtheta, dphi])
    ds2 = dx @ g @ dx

    ds_cols = st.columns(3)
    with ds_cols[0]:
        st.metric("ds²", f"{ds2:.6e}")
    with ds_cols[1]:
        if ds2 < 0:
            interval_type = "Timelike (causal)"
            interval_color = COLORS['green']
        elif ds2 > 0:
            interval_type = "Spacelike (acausal)"
            interval_color = COLORS['red']
        else:
            interval_type = "Lightlike (null)"
            interval_color = COLORS['orange']
        st.markdown(f"**Type:** <span style='color:{interval_color}'>{interval_type}</span>",
                    unsafe_allow_html=True)
    with ds_cols[2]:
        if ds2 < 0:
            proper_time = np.sqrt(-ds2) / c
            st.metric("Proper time dτ", f"{proper_time:.6e} s")
        elif ds2 > 0:
            proper_dist = np.sqrt(ds2)
            st.metric("Proper distance", f"{proper_dist:.6e} m")

# ═══════════════════════════════════════════════════════════════════════
# TAB 3: RELATIVISTIC EFFECTS
# ═══════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### Relativistic Effects near a Black Hole")

    re1, re2 = st.columns(2)
    with re1:
        bh_m = st.slider("Black hole mass (×M☉)", 1, 100, 10, key="rel_mass") * M_sun
    with re2:
        r_max = st.slider("Plot range (×r_s)", 5, 50, 20, key="rel_range")

    r_s_bh = 2 * G * bh_m / c**2

    r_range = np.linspace(1.01, r_max, 500) * r_s_bh

    # Time dilation
    td = np.sqrt(1 - r_s_bh / r_range)
    # Redshift
    z = 1 / td - 1
    # Effective potential
    L = 4.0 * G * bh_m / c
    V_eff = (-G * bh_m / r_range + L**2 / (2 * r_range**2)
             - G * bh_m * L**2 / (c**2 * r_range**3))

    c1, c2 = st.columns(2)
    with c1:
        fig_td = go.Figure()
        fig_td.add_trace(go.Scatter(
            x=r_range / r_s_bh, y=td, mode='lines',
            line=dict(color=COLORS['blue'], width=2.5), name='dτ/dt',
            fill='tozeroy', fillcolor='rgba(88,166,255,0.06)',
            hovertemplate="r/r_s: %{x:.2f}<br>dτ/dt: %{y:.4f}<extra></extra>",
        ))
        fig_td.add_trace(go.Scatter(
            x=r_range / r_s_bh, y=z, mode='lines',
            line=dict(color=COLORS['red'], width=2.5), name='Redshift z',
            hovertemplate="r/r_s: %{x:.2f}<br>z: %{y:.4f}<extra></extra>",
        ))
        # Key boundaries
        fig_td.add_vline(x=1.5, line_dash="dot", line_color=COLORS['orange'],
                          annotation_text="Photon sphere", annotation_font_color=COLORS['orange'])
        fig_td.add_vline(x=3.0, line_dash="dot", line_color=COLORS['green'],
                          annotation_text="ISCO", annotation_font_color=COLORS['green'])
        fig_td.update_layout(
            **PLOTLY_LAYOUT,
            title="Time Dilation & Gravitational Redshift",
            xaxis_title="r / r_s", yaxis_title="Value", height=420,
            yaxis=dict(range=[0, min(5, z.max() * 1.1)]),
        )
        st.plotly_chart(fig_td, use_container_width=True)

    with c2:
        fig_veff = go.Figure()
        V_norm = V_eff / abs(V_eff.min()) if V_eff.min() != 0 else V_eff
        fig_veff.add_trace(go.Scatter(
            x=r_range / r_s_bh, y=V_norm, mode='lines',
            line=dict(color=COLORS['purple'], width=2.5),
            fill='tozeroy', fillcolor='rgba(188,140,255,0.06)',
            hovertemplate="r/r_s: %{x:.2f}<br>V_eff: %{y:.4f}<extra></extra>",
        ))
        # Mark ISCO
        fig_veff.add_vline(x=3.0, line_dash="dot", line_color=COLORS['green'],
                            annotation_text="ISCO", annotation_font_color=COLORS['green'])
        fig_veff.update_layout(
            **PLOTLY_LAYOUT,
            title="Effective Potential V_eff(r)",
            xaxis_title="r / r_s", yaxis_title="V_eff (normalized)", height=420,
        )
        st.plotly_chart(fig_veff, use_container_width=True)

    # Key values table
    section_divider("Key Relativistic Values")

    key_radii = [1.5, 2.0, 3.0, 5.0, 10.0, 20.0]
    table_data = """
    <div style="overflow-x:auto;">
    <table style="border-collapse:collapse; font-family:'JetBrains Mono',monospace;
                  font-size:0.82rem; width:100%; background:rgba(13,17,23,0.8);
                  border:1px solid #30363d; border-radius:8px;">
    <tr style="background:rgba(22,27,34,0.9);">
        <th style="padding:8px 12px; color:#8b949e; border:1px solid #21262d;">r / r_s</th>
        <th style="padding:8px 12px; color:#58a6ff; border:1px solid #21262d;">dτ/dt</th>
        <th style="padding:8px 12px; color:#f85149; border:1px solid #21262d;">Redshift z</th>
        <th style="padding:8px 12px; color:#bc8cff; border:1px solid #21262d;">v_esc / c</th>
        <th style="padding:8px 12px; color:#d29922; border:1px solid #21262d;">Significance</th>
    </tr>
    """

    significance = {
        1.5: "Photon sphere",
        2.0: "2× event horizon",
        3.0: "ISCO",
        5.0: "Strong field",
        10.0: "Moderate field",
        20.0: "Weak field",
    }

    for r_ratio in key_radii:
        td_val = np.sqrt(1 - 1/r_ratio)
        z_val = 1/td_val - 1
        v_esc = np.sqrt(2 * G * bh_m / (r_ratio * r_s_bh)) / c
        sig = significance.get(r_ratio, "")

        td_color = COLORS['green'] if td_val > 0.5 else COLORS['orange'] if td_val > 0.1 else COLORS['red']

        table_data += f"""
        <tr>
            <td style="padding:8px 12px; color:#e6edf3; border:1px solid #21262d; text-align:center;">{r_ratio:.1f}</td>
            <td style="padding:8px 12px; color:{td_color}; border:1px solid #21262d; text-align:right;">{td_val:.6f}</td>
            <td style="padding:8px 12px; color:#f85149; border:1px solid #21262d; text-align:right;">{z_val:.4f}</td>
            <td style="padding:8px 12px; color:#bc8cff; border:1px solid #21262d; text-align:right;">{v_esc:.4f}</td>
            <td style="padding:8px 12px; color:#8b949e; border:1px solid #21262d;">{sig}</td>
        </tr>
        """
    table_data += "</table></div>"
    st.markdown(table_data, unsafe_allow_html=True)
