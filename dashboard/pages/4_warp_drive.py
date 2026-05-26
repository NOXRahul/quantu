"""QuantU Dashboard — Warp Drive Explorer Page"""
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from quantu.relativity.alcubierre import AlcubierreWarpDrive
from quantu.relativity.exotic_matter import CasimirEffect, NegativeEnergyField, QuantumVacuumFluctuation
from quantu.viz.color_maps import COLORMAPS

st.set_page_config(page_title="QuantU · Warp Drive", page_icon="🚀", layout="wide")

from theme import apply_theme, page_header, section_divider, info_tooltip, PLOTLY_LAYOUT, PLOTLY_SCENE, COLORS
apply_theme()

page_header("Alcubierre Warp Drive Explorer",
            "⚠️ SPECULATIVE — Theoretical visualization of the Alcubierre metric (1994)", "🚀")

st.latex(r"ds^2 = -c^2 dt^2 + (dx - v_s f(r_s) dt)^2 + dy^2 + dz^2")

st.markdown("""
<div class="disclaimer">
    ⚠️ <strong>Educational Disclaimer:</strong> The Alcubierre warp drive requires negative energy
    densities that likely violate known energy conditions. This visualization is purely
    theoretical and educational. No experimental evidence supports warp field generation.
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🫧 Warp Bubble", "⚡ Energy Density", "🔬 Exotic Matter"])

# ═══════════════════════════════════════════════════════════════════════
# TAB 1: WARP BUBBLE
# ═══════════════════════════════════════════════════════════════════════
with tab1:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### Bubble Parameters")

        warp_preset = st.selectbox("📋 Configuration", [
            "Custom", "Gentle Cruise", "Superluminal", "Thin Wall"
        ])

        WARP_PRESETS = {
            "Gentle Cruise": (1.5, 5.0, 0.5),
            "Superluminal": (1.0, 8.0, 3.0),
            "Thin Wall": (1.0, 25.0, 1.0),
        }

        if warp_preset != "Custom":
            R, sigma, v_s = WARP_PRESETS[warp_preset]
            st.info(f"**{warp_preset}**: R={R}, σ={sigma}, v/c={v_s}")
        else:
            R = st.slider("Bubble radius R", 0.1, 3.0, 1.0, 0.1)
            sigma = st.slider("Wall thickness σ", 1.0, 30.0, 8.0, 0.5)
            v_s = st.slider("Bubble velocity (v/c)", 0.1, 5.0, 1.0, 0.1)

        warp = AlcubierreWarpDrive(R=R, sigma=sigma, v_s=v_s)

        st.markdown("### Shape Function")
        st.latex(r"f(r_s) = \frac{\tanh(\sigma(r_s+R)) - \tanh(\sigma(r_s-R))}{2\tanh(\sigma R)}")

        # 1D profile
        r_1d = np.linspace(0, 4, 300)
        f_1d = warp.shape_function(r_1d)
        fig_1d = go.Figure()
        fig_1d.add_trace(go.Scatter(
            x=r_1d, y=f_1d, mode='lines',
            line=dict(color=COLORS['purple'], width=3),
            fill='tozeroy', fillcolor='rgba(188,140,255,0.1)',
            hovertemplate="r_s: %{x:.2f}<br>f(r_s): %{y:.4f}<extra></extra>",
        ))
        # Annotate bubble radius
        fig_1d.add_vline(x=R, line_dash="dash", line_color=COLORS['orange'],
                          annotation_text=f"R = {R}", annotation_position="top right",
                          annotation_font_color=COLORS['orange'])
        fig_1d.update_layout(
            **PLOTLY_LAYOUT,
            xaxis_title="r_s", yaxis_title="f(r_s)", height=250,
        )
        st.plotly_chart(fig_1d, use_container_width=True)

        info_tooltip("The shape function f(r_s) defines the warp bubble geometry. "
                     "f=1 inside the bubble (flat spacetime), f=0 outside, "
                     "with a smooth transition controlled by σ.")

    with col2:
        X3d, Y3d, Z3d = warp.compute_bubble_3d(grid_size=100, extent=3.0)
        fig = go.Figure(data=go.Surface(
            x=X3d, y=Y3d, z=Z3d,
            colorscale=COLORMAPS['warp_field'],
            opacity=0.88,
            contours=dict(z=dict(show=True, usecolormap=True, project_z=True)),
            lighting=dict(ambient=0.5, diffuse=0.6, specular=0.4, roughness=0.3),
            hovertemplate="x: %{x:.2f}<br>y: %{y:.2f}<br>f: %{z:.4f}<extra></extra>",
        ))

        scene = {**PLOTLY_SCENE}
        scene['camera'] = dict(eye=dict(x=1.5, y=1.5, z=1.0))
        scene['xaxis']['title'] = 'x'
        scene['yaxis']['title'] = 'y'
        scene['zaxis']['title'] = 'f(r_s)'

        fig.update_layout(
            **PLOTLY_LAYOUT,
            title="Alcubierre Warp Bubble — 3D Shape Function",
            scene=scene,
            height=620,
        )
        st.plotly_chart(fig, use_container_width=True)

    # Shape function comparison
    section_divider("Wall Thickness Comparison")
    sigmas_compare = [2.0, 5.0, 10.0, 20.0]
    fig_comp = go.Figure()
    comp_colors = [COLORS['blue'], COLORS['green'], COLORS['orange'], COLORS['red']]
    for si, sig in enumerate(sigmas_compare):
        w = AlcubierreWarpDrive(R=R, sigma=sig, v_s=v_s)
        f_vals = w.shape_function(r_1d)
        fig_comp.add_trace(go.Scatter(
            x=r_1d, y=f_vals, mode='lines', name=f'σ = {sig}',
            line=dict(color=comp_colors[si], width=2),
        ))
    fig_comp.update_layout(
        **PLOTLY_LAYOUT,
        title="Shape Function f(r_s) for Different Wall Thickness σ",
        xaxis_title="r_s", yaxis_title="f(r_s)", height=350,
    )
    st.plotly_chart(fig_comp, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════
# TAB 2: ENERGY DENSITY
# ═══════════════════════════════════════════════════════════════════════
with tab2:
    warp2 = AlcubierreWarpDrive(R=R, sigma=sigma, v_s=v_s)
    X2d, Y2d, f_vals, rho = warp2.compute_bubble_2d(grid_size=250, extent=3.0)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Warp Bubble Cross-Section")
        fig_f = go.Figure(data=go.Heatmap(
            z=f_vals, colorscale=COLORMAPS['warp_field'],
            colorbar=dict(title=dict(text="f(r_s)", font=dict(size=11))),
            hovertemplate="Row: %{y}<br>Col: %{x}<br>f: %{z:.4f}<extra></extra>",
        ))
        fig_f.update_layout(**PLOTLY_LAYOUT, height=450, xaxis_title="x", yaxis_title="y")
        st.plotly_chart(fig_f, use_container_width=True)

    with c2:
        st.markdown("### Energy Density T⁰⁰ (Negative = Exotic)")
        rho_clipped = np.clip(rho, np.percentile(rho, 1), np.percentile(rho, 99))
        fig_rho = go.Figure(data=go.Heatmap(
            z=rho_clipped, colorscale=COLORMAPS['energy_density'],
            colorbar=dict(title=dict(text="ρ", font=dict(size=11))),
            hovertemplate="Row: %{y}<br>Col: %{x}<br>ρ: %{z:.4e}<extra></extra>",
        ))
        fig_rho.update_layout(**PLOTLY_LAYOUT, height=450, xaxis_title="x", yaxis_title="y")
        st.plotly_chart(fig_rho, use_container_width=True)

    total_E = warp2.total_energy_estimate()
    st.metric("Total Exotic Energy (arb. units)", f"{total_E:.4e}")
    st.latex(r"T^{00} = -\frac{c^4}{8\pi G} \frac{v_s^2 (y^2+z^2)}{2r_s^2} \left(\frac{df}{dr_s}\right)^2")

    # Energy comparison table
    section_divider("Energy Scale Comparison")
    info_tooltip("To put the warp drive energy into perspective, here's how it compares to known energy sources.")

    energy_data = [
        ("☀️ Sun (1 second output)", "3.8 × 10²⁶ J", "Established"),
        ("💣 Tsar Bomba (50 MT)", "2.1 × 10¹⁷ J", "Established"),
        ("⚛️ E=mc² (1 kg)", "9.0 × 10¹⁶ J", "Established"),
        ("🌌 Milky Way luminosity (1 s)", "~10³⁷ J", "Established"),
        ("🚀 Alcubierre (original estimate)", "~10⁶⁴ J ≈ Jupiter mass", "Speculative"),
        ("🚀 Van Den Broeck (optimized)", "~10⁴⁵ J ≈ Sun mass×10⁻³", "Speculative"),
    ]

    st.markdown("| Source | Energy | Status |")
    st.markdown("|--------|--------|--------|")
    for name, energy, status in energy_data:
        badge = "🟢" if status == "Established" else "🟡"
        st.markdown(f"| {name} | {energy} | {badge} {status} |")

# ═══════════════════════════════════════════════════════════════════════
# TAB 3: EXOTIC MATTER
# ═══════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### Casimir Effect — Established Quantum Physics")
    st.latex(r"\frac{E}{A} = -\frac{\pi^2 \hbar c}{720 d^4}")

    info_tooltip("The Casimir effect is a real, experimentally verified phenomenon where "
                 "two conducting plates experience an attractive force due to quantum vacuum "
                 "fluctuations. It's the closest real physics to 'negative energy density'.")

    d_arr, E_arr, F_arr = CasimirEffect.compute_vs_distance(1e-9, 1e-6, 200)

    c1, c2 = st.columns(2)
    with c1:
        fig_ce = go.Figure()
        fig_ce.add_trace(go.Scatter(
            x=d_arr * 1e9, y=E_arr,
            mode='lines', line=dict(color=COLORS['blue'], width=2.5),
            name="Energy density",
            fill='tozeroy', fillcolor='rgba(88,166,255,0.08)',
            hovertemplate="d: %{x:.1f} nm<br>E/A: %{y:.4e} J/m²<extra></extra>",
        ))
        fig_ce.update_layout(
            **PLOTLY_LAYOUT,
            title="Casimir Energy vs Plate Separation",
            xaxis_title="Separation (nm)", yaxis_title="E/A (J/m²)", height=400,
        )
        st.plotly_chart(fig_ce, use_container_width=True)

    with c2:
        fig_cf = go.Figure()
        fig_cf.add_trace(go.Scatter(
            x=d_arr * 1e9, y=F_arr,
            mode='lines', line=dict(color=COLORS['green'], width=2.5),
            name="Force per area",
            fill='tozeroy', fillcolor='rgba(63,185,80,0.08)',
            hovertemplate="d: %{x:.1f} nm<br>F/A: %{y:.4e} N/m²<extra></extra>",
        ))
        fig_cf.update_layout(
            **PLOTLY_LAYOUT,
            title="Casimir Force vs Plate Separation",
            xaxis_title="Separation (nm)", yaxis_title="F/A (N/m²)", height=400,
        )
        st.plotly_chart(fig_cf, use_container_width=True)

    section_divider("Quantum Vacuum Fluctuations")
    st.markdown("### ⚠️ Vacuum Energy Field Visualization")
    info_tooltip("This visualization shows simulated quantum vacuum fluctuations — "
                 "random energy density variations inherent to empty space in QFT.")

    vac_res = st.slider("Resolution", 50, 300, 150, key="vac_res")
    Xv, Yv, Fv = QuantumVacuumFluctuation.generate(vac_res, 5.0)
    fig_vac = go.Figure(data=go.Heatmap(
        z=Fv, colorscale=COLORMAPS['energy_density'],
        colorbar=dict(title=dict(text="δρ", font=dict(size=11))),
        hovertemplate="x: %{x}<br>y: %{y}<br>δρ: %{z:.4e}<extra></extra>",
    ))
    fig_vac.update_layout(
        **PLOTLY_LAYOUT,
        title="Vacuum Energy Fluctuations (Visualization)",
        height=450,
    )
    st.plotly_chart(fig_vac, use_container_width=True)
