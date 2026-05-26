"""QuantU Dashboard — Gravity Lab Page"""
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from quantu.core.gravity import (
    compute_potential_field, compute_force_field, escape_velocity
)
from quantu.constants import G, M_earth, M_sun, R_earth
from quantu.viz.color_maps import COLORMAPS

st.set_page_config(page_title="QuantU · Gravity Lab", page_icon="🌍", layout="wide")

from theme import apply_theme, page_header, section_divider, info_tooltip, PLOTLY_LAYOUT, COLORS
apply_theme()

page_header("Gravity Field Laboratory",
            "Explore Newtonian gravitational fields with interactive mass placement", "🌍")

st.latex(r"F = \frac{GMm}{r^2} \qquad \Phi = -\frac{GM}{r} \qquad v_{esc} = \sqrt{\frac{2GM}{r}}")

# ── Sidebar Controls ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Field Parameters")

    # Preset scenarios
    preset = st.selectbox("📋 Preset Scenario", [
        "Custom", "Earth-Moon", "Sun-Jupiter", "Binary Stars", "Triple System"
    ])

    PRESETS = {
        "Earth-Moon": [
            (5.97, np.array([-2.0, 0.0])),
            (0.073, np.array([2.0, 0.0])),
        ],
        "Sun-Jupiter": [
            (100.0, np.array([0.0, 0.0])),
            (10.0, np.array([5.0, 0.0])),
        ],
        "Binary Stars": [
            (50.0, np.array([-3.0, 0.0])),
            (50.0, np.array([3.0, 0.0])),
        ],
        "Triple System": [
            (40.0, np.array([0.0, 0.0])),
            (20.0, np.array([4.0, 3.0])),
            (15.0, np.array([-3.0, -4.0])),
        ],
    }

    if preset != "Custom":
        preset_data = PRESETS[preset]
        n_masses = len(preset_data)
        st.info(f"Loaded **{preset}** preset with {n_masses} bodies")
    else:
        n_masses = st.slider("Number of masses", 1, 5, 2)

    grid_res = st.slider("Grid resolution", 50, 300, 150)
    field_extent = st.slider("Field extent (×10⁹ m)", 1, 20, 10)

    st.markdown("### 🎨 Visualization")
    show_vectors = st.checkbox("Show force vectors", True)
    show_contours = st.checkbox("Show equipotential lines", True)
    show_streamlines = st.checkbox("Show field lines", False)
    vector_density = st.slider("Vector density", 8, 30, 16) if show_vectors else 16

    st.markdown("### 🪨 Mass Configuration")
    masses_config = []

    if preset != "Custom":
        for i, (m_val, pos_val) in enumerate(preset_data):
            st.markdown(f"**Mass {i+1}** — {m_val:.2f} ×10²⁴ kg at ({pos_val[0]:.1f}, {pos_val[1]:.1f}) ×10⁹ m")
            masses_config.append((m_val * 1e24, pos_val * 1e9))
    else:
        for i in range(n_masses):
            with st.expander(f"🪨 Mass {i+1}", expanded=(i < 2)):
                m = st.slider(f"Mass (×10²⁴ kg)", 0.1, 100.0,
                              float([30.0, 10.0, 5.0, 20.0, 15.0][i % 5]), key=f"m_{i}")
                c1, c2 = st.columns(2)
                with c1:
                    px = st.slider(f"X (×10⁹ m)", -field_extent+1, field_extent-1,
                                    int([-3, 3, 0, -5, 5][i % 5]), key=f"px_{i}")
                with c2:
                    py = st.slider(f"Y (×10⁹ m)", -field_extent+1, field_extent-1,
                                    int([0, 0, 4, -2, 2][i % 5]), key=f"py_{i}")
                masses_config.append((m * 1e24, np.array([px * 1e9, py * 1e9])))

# ── Compute Fields ───────────────────────────────────────────────────
extent = field_extent * 1e9
x = np.linspace(-extent, extent, grid_res)
y = np.linspace(-extent, extent, grid_res)
X, Y = np.meshgrid(x, y)

potential = compute_potential_field(masses_config, X, Y, softening=extent * 0.01)
gx, gy = compute_force_field(masses_config, X, Y, softening=extent * 0.01)
g_mag = np.sqrt(gx**2 + gy**2)

# Clip for visualization
pot_clipped = np.clip(potential, np.percentile(potential, 2), np.percentile(potential, 98))

# ── Visualization ────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Gravitational Potential Φ(x, y)")
    fig_pot = go.Figure(data=go.Heatmap(
        x=x / 1e9, y=y / 1e9, z=pot_clipped,
        colorscale=COLORMAPS['gravity_well'],
        colorbar=dict(title=dict(text="Φ (J/kg)", font=dict(size=11)),
                      tickfont=dict(size=10)),
        hovertemplate="x: %{x:.1f}×10⁹ m<br>y: %{y:.1f}×10⁹ m<br>Φ: %{z:.3e} J/kg<extra></extra>",
    ))

    # Add mass markers with glowing rings
    for i, (m, pos) in enumerate(masses_config):
        marker_size = max(10, min(30, m / 1e24 * 0.4))
        # Glow ring
        fig_pot.add_trace(go.Scatter(
            x=[pos[0] / 1e9], y=[pos[1] / 1e9],
            mode='markers', showlegend=False,
            marker=dict(size=marker_size + 12, color='rgba(248,81,73,0.2)',
                        symbol='circle', line=dict(width=0)),
        ))
        # Core marker
        fig_pot.add_trace(go.Scatter(
            x=[pos[0] / 1e9], y=[pos[1] / 1e9],
            mode='markers+text', text=[f"M{i+1}"],
            marker=dict(size=marker_size, color=COLORS['red'],
                        symbol='circle',
                        line=dict(width=2, color='rgba(255,255,255,0.6)')),
            textposition='top center',
            textfont=dict(color='white', size=11, family='JetBrains Mono'),
            showlegend=False,
            hovertemplate=f"<b>Mass {i+1}</b><br>m = {m:.3e} kg<br>"
                          f"pos = ({pos[0]/1e9:.1f}, {pos[1]/1e9:.1f}) ×10⁹ m<extra></extra>",
        ))

    if show_contours:
        fig_pot.add_trace(go.Contour(
            x=x / 1e9, y=y / 1e9, z=pot_clipped,
            ncontours=15, showscale=False,
            contours=dict(coloring='none', showlabels=True,
                          labelfont=dict(size=9, color='rgba(255,255,255,0.5)')),
            line=dict(color='rgba(255,255,255,0.25)', width=1),
        ))

    fig_pot.update_layout(
        **PLOTLY_LAYOUT,
        xaxis_title="x (×10⁹ m)", yaxis_title="y (×10⁹ m)",
        yaxis=dict(scaleanchor="x"), height=520,
    )
    st.plotly_chart(fig_pot, use_container_width=True)

with col2:
    st.markdown("### Field Intensity |g⃗(x, y)|")
    g_mag_clipped = np.clip(g_mag, 0, np.percentile(g_mag, 95))
    fig_field = go.Figure(data=go.Heatmap(
        x=x / 1e9, y=y / 1e9, z=np.log10(g_mag_clipped + 1e-20),
        colorscale=COLORMAPS['energy_density'],
        colorbar=dict(title=dict(text="log₁₀|g|", font=dict(size=11)),
                      tickfont=dict(size=10)),
        hovertemplate="x: %{x:.1f}×10⁹ m<br>y: %{y:.1f}×10⁹ m<br>log₁₀|g|: %{z:.2f}<extra></extra>",
    ))

    # Force vectors — using proper 2D annotations (quiver-style arrows)
    if show_vectors:
        step = max(1, grid_res // vector_density)
        Xs = X[::step, ::step] / 1e9
        Ys = Y[::step, ::step] / 1e9
        Us = gx[::step, ::step]
        Vs = gy[::step, ::step]
        mag_s = np.sqrt(Us**2 + Vs**2)
        mag_s = np.maximum(mag_s, 1e-20)

        # Normalize and scale for display
        arrow_scale = (field_extent * 2 / vector_density) * 0.6
        Un = (Us / mag_s) * arrow_scale
        Vn = (Vs / mag_s) * arrow_scale

        # Draw arrows as line segments with arrowheads
        for ii in range(Xs.shape[0]):
            for jj in range(Xs.shape[1]):
                x0, y0 = Xs[ii, jj], Ys[ii, jj]
                dx, dy = Un[ii, jj], Vn[ii, jj]
                # Skip arrows near mass positions
                skip = False
                for _, pos in masses_config:
                    if abs(x0 - pos[0]/1e9) < arrow_scale * 0.5 and abs(y0 - pos[1]/1e9) < arrow_scale * 0.5:
                        skip = True
                        break
                if skip:
                    continue
                fig_field.add_annotation(
                    x=x0 + dx, y=y0 + dy, ax=x0, ay=y0,
                    xref="x", yref="y", axref="x", ayref="y",
                    showarrow=True,
                    arrowhead=2, arrowsize=1.2, arrowwidth=1.5,
                    arrowcolor="rgba(88,166,255,0.6)",
                )

    # Mass markers on field plot too
    for i, (m, pos) in enumerate(masses_config):
        marker_size = max(8, min(25, m / 1e24 * 0.3))
        fig_field.add_trace(go.Scatter(
            x=[pos[0] / 1e9], y=[pos[1] / 1e9],
            mode='markers', showlegend=False,
            marker=dict(size=marker_size, color=COLORS['red'],
                        line=dict(width=2, color='rgba(255,255,255,0.5)')),
        ))

    fig_field.update_layout(
        **PLOTLY_LAYOUT,
        xaxis_title="x (×10⁹ m)", yaxis_title="y (×10⁹ m)",
        yaxis=dict(scaleanchor="x"), height=520,
    )
    st.plotly_chart(fig_field, use_container_width=True)

# ── Field Lines (Streamlines) ────────────────────────────────────────
if show_streamlines:
    section_divider("Field Line Visualization")
    info_tooltip("Field lines show the direction a test mass would accelerate. "
                 "Lines converge toward massive bodies and never cross.")

    fig_stream = go.Figure()

    # Compute streamlines by integrating field from seed points
    n_seeds = 24
    seed_angles = np.linspace(0, 2 * np.pi, n_seeds, endpoint=False)
    for _, pos in masses_config:
        for angle in seed_angles:
            # Start seed points around each mass
            seed_r = extent * 0.08
            sx = pos[0] + seed_r * np.cos(angle)
            sy = pos[1] + seed_r * np.sin(angle)

            # Integrate field line (reverse direction — toward mass)
            line_x, line_y = [sx], [sy]
            cx, cy = sx, sy
            ds = extent * 0.015
            for _ in range(150):
                # Interpolate field at current point
                ix = int((cx + extent) / (2 * extent) * (grid_res - 1))
                iy = int((cy + extent) / (2 * extent) * (grid_res - 1))
                if ix < 0 or ix >= grid_res or iy < 0 or iy >= grid_res:
                    break
                fx_val = gx[iy, ix]
                fy_val = gy[iy, ix]
                f_mag = np.sqrt(fx_val**2 + fy_val**2)
                if f_mag < 1e-30:
                    break
                # Step in opposite direction (field lines point away from mass)
                cx -= ds * fx_val / f_mag
                cy -= ds * fy_val / f_mag
                line_x.append(cx)
                line_y.append(cy)

            if len(line_x) > 5:
                fig_stream.add_trace(go.Scatter(
                    x=[lx / 1e9 for lx in line_x],
                    y=[ly / 1e9 for ly in line_y],
                    mode='lines', showlegend=False,
                    line=dict(color='rgba(88,166,255,0.35)', width=1.2),
                ))

    # Mass markers
    for i, (m, pos) in enumerate(masses_config):
        fig_stream.add_trace(go.Scatter(
            x=[pos[0] / 1e9], y=[pos[1] / 1e9],
            mode='markers+text', text=[f"M{i+1}"],
            marker=dict(size=15, color=COLORS['red'],
                        line=dict(width=2, color='white')),
            textposition='top center', textfont=dict(color='white', size=11),
            showlegend=False,
        ))

    fig_stream.update_layout(
        **PLOTLY_LAYOUT,
        title="Gravitational Field Lines",
        xaxis_title="x (×10⁹ m)", yaxis_title="y (×10⁹ m)",
        yaxis=dict(scaleanchor="x"), height=500,
    )
    st.plotly_chart(fig_stream, use_container_width=True)

# ── Escape Velocity Calculator ───────────────────────────────────────
section_divider("Escape Velocity Calculator")

ec1, ec2, ec3 = st.columns(3)
with ec1:
    calc_mass = st.number_input("Central mass (kg)", value=M_earth, format="%.3e")
with ec2:
    calc_radius = st.number_input("Distance from center (m)", value=R_earth, format="%.3e")
with ec3:
    v_esc = escape_velocity(calc_mass, calc_radius)
    st.metric("Escape Velocity", f"{v_esc:.1f} m/s", f"{v_esc/1000:.2f} km/s")

info_tooltip(f"At this distance from a {calc_mass:.2e} kg body, you need "
             f"{v_esc/1000:.2f} km/s to escape its gravity completely — "
             f"that's {v_esc/340:.0f}× the speed of sound!")
