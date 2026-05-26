"""QuantU Dashboard — Spacetime Curvature Page"""
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from quantu.fields.spacetime_grid import SpacetimeGrid
from quantu.relativity.schwarzschild import SchwarzschildMetric
from quantu.constants import M_sun
from quantu.viz.color_maps import COLORMAPS
from quantu.math_engine.curvature import gaussian_curvature_surface

st.set_page_config(page_title="QuantU · Spacetime", page_icon="🕳️", layout="wide")

from theme import apply_theme, page_header, section_divider, info_tooltip, PLOTLY_LAYOUT, PLOTLY_SCENE, COLORS
apply_theme()

page_header("Spacetime Curvature Visualizer",
            "Explore how mass curves spacetime — from the rubber-sheet model to Schwarzschild geometry", "🕳️")

st.latex(r"ds^2 = -\left(1-\frac{r_s}{r}\right)c^2 dt^2 + \frac{dr^2}{1-r_s/r} + r^2 d\Omega^2")

tab1, tab2, tab3 = st.tabs(["🌐 Spacetime Grid", "🕳️ Black Hole Geometry", "📊 Curvature Analysis"])

# ═══════════════════════════════════════════════════════════════════════
# TAB 1: SPACETIME GRID
# ═══════════════════════════════════════════════════════════════════════
with tab1:
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("### Mass Placement")

        grid_preset = st.selectbox("📋 Preset", [
            "Custom", "Single Star", "Binary System", "Cluster"
        ])

        GRID_PRESETS = {
            "Single Star": [(8.0, [0, 0])],
            "Binary System": [(5.0, [-3, 0]), (5.0, [3, 0])],
            "Cluster": [(4.0, [0, 0]), (2.0, [4, 3]), (2.0, [-4, -3]), (1.5, [0, 5])],
        }

        if grid_preset != "Custom":
            mass_list = GRID_PRESETS[grid_preset]
            n_masses = len(mass_list)
            st.info(f"Loaded **{grid_preset}** with {n_masses} masses")
        else:
            n_masses = st.slider("Number of masses", 1, 4, 1, key="st_nmass")
            mass_list = []

        grid_res = st.slider("Grid resolution", 30, 120, 70, key="st_res")
        depth_scale = st.slider("Curvature depth", 0.5, 5.0, 2.5, 0.1)
        show_wireframe = st.checkbox("Show wireframe", True)
        wireframe_density = st.slider("Wireframe lines", 8, 25, 15) if show_wireframe else 15

        if grid_preset == "Custom":
            for i in range(n_masses):
                with st.expander(f"Mass {i+1}", expanded=(i == 0)):
                    m = st.number_input(f"M{i+1} strength", 0.1, 20.0,
                                         float([5.0, 3.0, 2.0, 4.0][i % 4]), key=f"stm_{i}")
                    c1, c2 = st.columns(2)
                    with c1:
                        px = st.number_input(f"x{i+1}", -8.0, 8.0,
                                              float([0, 4, -4, 0][i % 4]), key=f"stpx_{i}")
                    with c2:
                        py = st.number_input(f"y{i+1}", -8.0, 8.0,
                                              float([0, 0, 0, 4][i % 4]), key=f"stpy_{i}")
                    mass_list.append((m, [px, py]))

    with col2:
        grid = SpacetimeGrid((-10, 10), (-10, 10), grid_res)
        for m, pos in mass_list:
            grid.add_mass(m, pos, scale=depth_scale)

        X, Y, Z = grid.get_surface_data()

        # Color by curvature depth
        fig = go.Figure(data=go.Surface(
            x=X, y=Y, z=Z,
            colorscale=COLORMAPS['gravity_well'],
            opacity=0.92,
            contours=dict(
                z=dict(show=True, usecolormap=True, highlightcolor=COLORS['blue'],
                       project_z=True)
            ),
            hovertemplate="x: %{x:.2f}<br>y: %{y:.2f}<br>Curvature: %{z:.3f}<extra></extra>",
            lighting=dict(ambient=0.5, diffuse=0.7, specular=0.3, roughness=0.5),
        ))

        # Wireframe with gradient color
        if show_wireframe:
            z_min, z_max = Z.min(), Z.max()
            for i in range(0, X.shape[0], max(1, X.shape[0] // wireframe_density)):
                z_row = Z[i, :]
                norm = (z_row - z_min) / (z_max - z_min + 1e-10)
                colors = [f'rgba({int(88 + 167*n)},{int(166 - 100*n)},{255},{0.35})' for n in norm]
                fig.add_trace(go.Scatter3d(
                    x=X[i, :], y=Y[i, :], z=Z[i, :],
                    mode='lines', line=dict(color='rgba(88,166,255,0.25)', width=1.2),
                    showlegend=False,
                ))
            for j in range(0, X.shape[1], max(1, X.shape[1] // wireframe_density)):
                fig.add_trace(go.Scatter3d(
                    x=X[:, j], y=Y[:, j], z=Z[:, j],
                    mode='lines', line=dict(color='rgba(188,140,255,0.2)', width=1),
                    showlegend=False,
                ))

        # Mass position markers
        for m, pos in mass_list:
            # Find Z at mass position
            ix = int((pos[0] + 10) / 20 * (grid_res - 1))
            iy = int((pos[1] + 10) / 20 * (grid_res - 1))
            ix = np.clip(ix, 0, grid_res - 1)
            iy = np.clip(iy, 0, grid_res - 1)
            z_at_mass = Z[iy, ix]

            fig.add_trace(go.Scatter3d(
                x=[pos[0]], y=[pos[1]], z=[z_at_mass],
                mode='markers',
                marker=dict(size=max(5, m * 1.5), color=COLORS['red'],
                            line=dict(width=1, color='white')),
                showlegend=False,
                hovertemplate=f"Mass: {m:.1f}<br>Position: ({pos[0]:.1f}, {pos[1]:.1f})<extra></extra>",
            ))

        scene = {**PLOTLY_SCENE}
        scene['camera'] = dict(eye=dict(x=1.8, y=1.8, z=1.2))
        scene['aspectratio'] = dict(x=1, y=1, z=0.5)
        scene['xaxis']['title'] = 'x'
        scene['yaxis']['title'] = 'y'
        scene['zaxis']['title'] = 'Curvature'

        fig.update_layout(
            **PLOTLY_LAYOUT,
            scene=scene,
            height=620,
        )
        st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════
# TAB 2: BLACK HOLE GEOMETRY
# ═══════════════════════════════════════════════════════════════════════
with tab2:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### Black Hole Parameters")

        bh_preset = st.selectbox("📋 Black Hole", [
            "Custom", "Stellar (10 M☉)", "Intermediate (1000 M☉)", "Supermassive (4M × 10⁶ M☉)"
        ])

        BH_PRESETS = {"Stellar (10 M☉)": 10, "Intermediate (1000 M☉)": 1000,
                      "Supermassive (4M × 10⁶ M☉)": 4e6}

        if bh_preset != "Custom":
            bh_mass_solar = BH_PRESETS[bh_preset]
            st.info(f"**{bh_preset}**: {bh_mass_solar:.0f} M☉")
        else:
            bh_mass_solar = st.slider("Mass (×M☉)", 1.0, 100.0, 10.0, 1.0)

        bh_mass = bh_mass_solar * M_sun
        bh = SchwarzschildMetric(bh_mass)

        st.markdown("### Key Properties")
        st.metric("Event Horizon (r_s)", f"{bh.event_horizon:.2e} m")
        st.metric("Photon Sphere (1.5 r_s)", f"{bh.photon_sphere:.2e} m")
        st.metric("ISCO (3 r_s)", f"{bh.isco:.2e} m")

        section_divider("Gravitational Redshift")
        r_factor = st.slider("Observer position r / r_s", 1.01, 20.0, 3.0, 0.01)
        z_val = bh.gravitational_redshift(r_factor * bh.r_s)
        td_val = bh.time_dilation(r_factor * bh.r_s)
        st.metric("Redshift z", f"{z_val:.4f}")
        st.metric("Time dilation dτ/dt", f"{td_val:.4f}")

        info_tooltip(f"At r = {r_factor:.2f} r_s, clocks tick {td_val:.4f}× slower than at infinity. "
                     f"Light is redshifted by z = {z_val:.4f}.")

    with col2:
        X_emb, Y_emb, Z_emb = bh.embedding_diagram(r_range=(1.01, 8.0), n_points=150)

        fig = go.Figure()

        # Embedding surface
        fig.add_trace(go.Surface(
            x=X_emb, y=Y_emb, z=Z_emb,
            colorscale=COLORMAPS['warp_field'],
            opacity=0.88,
            lighting=dict(ambient=0.4, diffuse=0.7, specular=0.4, roughness=0.3),
            hovertemplate="x/r_s: %{x:.2f}<br>y/r_s: %{y:.2f}<br>z/r_s: %{z:.2f}<extra></extra>",
        ))

        # Event horizon ring
        eh_theta = np.linspace(0, 2*np.pi, 100)
        fig.add_trace(go.Scatter3d(
            x=np.cos(eh_theta), y=np.sin(eh_theta),
            z=np.full(100, Z_emb.min() * 0.95),
            mode='lines', name='Event Horizon',
            line=dict(color=COLORS['red'], width=4),
        ))

        # Photon sphere ring
        fig.add_trace(go.Scatter3d(
            x=1.5 * np.cos(eh_theta), y=1.5 * np.sin(eh_theta),
            z=np.full(100, Z_emb.min() * 0.5),
            mode='lines', name='Photon Sphere',
            line=dict(color=COLORS['orange'], width=3, dash='dash'),
        ))

        # ISCO ring
        fig.add_trace(go.Scatter3d(
            x=3.0 * np.cos(eh_theta), y=3.0 * np.sin(eh_theta),
            z=np.full(100, Z_emb.min() * 0.2),
            mode='lines', name='ISCO',
            line=dict(color=COLORS['green'], width=2, dash='dot'),
        ))

        scene = {**PLOTLY_SCENE}
        scene['camera'] = dict(eye=dict(x=1.5, y=1.5, z=0.8))
        scene['xaxis']['title'] = 'x/r_s'
        scene['yaxis']['title'] = 'y/r_s'
        scene['zaxis']['title'] = 'z/r_s'

        fig.update_layout(
            **PLOTLY_LAYOUT,
            title="Flamm's Paraboloid — Embedding Diagram",
            scene=scene,
            height=580,
        )
        st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════
# TAB 3: CURVATURE ANALYSIS
# ═══════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### Gaussian Curvature Analysis")
    info_tooltip("Gaussian curvature K measures how a surface deviates from flatness. "
                 "K > 0 means sphere-like curvature, K < 0 means saddle-like, K = 0 means flat.")

    ca1, ca2 = st.columns(2)
    with ca1:
        curv_mass = st.slider("Mass strength", 1.0, 15.0, 5.0, 0.5, key="curv_m")
    with ca2:
        curv_scale = st.slider("Depth scale", 0.5, 5.0, 2.0, 0.1, key="curv_s")

    grid2 = SpacetimeGrid((-10, 10), (-10, 10), 100)
    grid2.add_mass(curv_mass, [0, 0], scale=curv_scale)
    X2, Y2, Z2 = grid2.get_surface_data()
    K = gaussian_curvature_surface(X2, Y2, Z2)
    K_clipped = np.clip(K, np.percentile(K, 2), np.percentile(K, 98))

    c1, c2 = st.columns(2)
    with c1:
        fig_k = go.Figure(data=go.Heatmap(
            z=K_clipped, colorscale=COLORMAPS['energy_density'],
            colorbar=dict(title=dict(text="K", font=dict(size=11))),
            hovertemplate="Row: %{y}<br>Col: %{x}<br>K: %{z:.4e}<extra></extra>",
        ))
        fig_k.update_layout(
            **PLOTLY_LAYOUT,
            title="Gaussian Curvature K(x,y)",
            height=450,
        )
        st.plotly_chart(fig_k, use_container_width=True)

    with c2:
        fig_z = go.Figure(data=go.Heatmap(
            z=Z2, colorscale=COLORMAPS['spacetime'],
            colorbar=dict(title=dict(text="z", font=dict(size=11))),
            hovertemplate="Row: %{y}<br>Col: %{x}<br>z: %{z:.4f}<extra></extra>",
        ))
        fig_z.update_layout(
            **PLOTLY_LAYOUT,
            title="Surface Height z(x,y)",
            height=450,
        )
        st.plotly_chart(fig_z, use_container_width=True)

    # Curvature statistics
    section_divider("Curvature Statistics")
    cs1, cs2, cs3, cs4 = st.columns(4)
    with cs1:
        st.metric("Max K", f"{K.max():.4e}")
    with cs2:
        st.metric("Min K", f"{K.min():.4e}")
    with cs3:
        st.metric("Mean K", f"{K.mean():.4e}")
    with cs4:
        st.metric("Std K", f"{K.std():.4e}")

    st.latex(r"K = \frac{f_{xx} f_{yy} - f_{xy}^2}{(1 + f_x^2 + f_y^2)^2}")
