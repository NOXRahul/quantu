"""QuantU Dashboard — Orbital Mechanics Page"""
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from quantu.core.orbital import kepler_orbit, hohmann_transfer, orbital_period
from quantu.core.nbody import NBodySimulation, Body, sun_earth_moon
from quantu.constants import G, M_sun, AU
from quantu.viz.color_maps import COLORMAPS

st.set_page_config(page_title="QuantU · Orbital Mechanics", page_icon="🪐", layout="wide")

from theme import apply_theme, page_header, section_divider, info_tooltip, PLOTLY_LAYOUT, COLORS
apply_theme()

page_header("Orbital Mechanics Laboratory",
            "Kepler orbits, Hohmann transfers, and N-body gravitational simulation", "🪐")

st.latex(r"T = 2\pi\sqrt{\frac{a^3}{GM}} \qquad v^2 = GM\left(\frac{2}{r} - \frac{1}{a}\right)")

tab1, tab2, tab3 = st.tabs(["🔵 Kepler Orbits", "🔄 Hohmann Transfer", "🌌 N-Body Simulation"])

# ═══════════════════════════════════════════════════════════════════════
# TAB 1: KEPLER ORBITS
# ═══════════════════════════════════════════════════════════════════════
with tab1:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### Parameters")

        orbit_preset = st.selectbox("📋 Preset", [
            "Custom", "Mercury", "Earth", "Mars", "Halley's Comet", "Pluto"
        ])

        ORBIT_PRESETS = {
            "Mercury": (1.0, 0.2056, 0.387),
            "Earth": (1.0, 0.0167, 1.0),
            "Mars": (1.0, 0.0934, 1.524),
            "Halley's Comet": (1.0, 0.967, 17.83),
            "Pluto": (1.0, 0.2488, 39.48),
        }

        if orbit_preset != "Custom":
            mass_sol, ecc, sma_au = ORBIT_PRESETS[orbit_preset]
            st.info(f"**{orbit_preset}**: e={ecc}, a={sma_au} AU")
        else:
            mass_sol = st.slider("Central mass (×M☉)", 0.1, 10.0, 1.0, key="kep_mass")
            ecc = st.slider("Eccentricity (e)", 0.0, 0.97, 0.3, 0.01)
            sma_au = st.slider("Semi-major axis (AU)", 0.1, 40.0, 1.0, 0.1)

        mass = mass_sol * M_sun
        sma = sma_au * AU

        orbit = kepler_orbit(sma, ecc, mass, n_points=500, include_velocity=True)
        T = orbital_period(sma, mass)

        st.markdown("### Orbital Properties")
        st.metric("Period", f"{T / 86400:.1f} days")
        st.metric("Periapsis", f"{sma * (1 - ecc) / AU:.4f} AU")
        st.metric("Apoapsis", f"{sma * (1 + ecc) / AU:.4f} AU")

        # Velocity at key points
        v_peri = np.sqrt(G * mass * (1 + ecc) / (sma * (1 - ecc)))
        v_apo = np.sqrt(G * mass * (1 - ecc) / (sma * (1 + ecc)))
        st.metric("v (periapsis)", f"{v_peri/1000:.2f} km/s")
        st.metric("v (apoapsis)", f"{v_apo/1000:.2f} km/s")

        animate = st.checkbox("🎬 Animate orbiting body", True)

    with col2:
        ox = orbit['x'] / AU
        oy = orbit['y'] / AU

        if animate:
            # Create animation frames
            n_frames = 60
            indices = np.linspace(0, len(ox) - 1, n_frames, dtype=int)

            frames = []
            for idx in indices:
                frames.append(go.Frame(
                    data=[
                        go.Scatter(x=ox, y=oy, mode='lines', name='Orbit',
                                   line=dict(color=COLORS['blue'], width=2)),
                        go.Scatter(x=[0], y=[0], mode='markers', name='Star',
                                   marker=dict(size=16, color=COLORS['gold'], symbol='star',
                                               line=dict(width=1, color='rgba(255,255,255,0.5)'))),
                        go.Scatter(x=[ox[0]], y=[oy[0]], mode='markers', name='Periapsis',
                                   marker=dict(size=7, color=COLORS['green'], symbol='diamond')),
                        go.Scatter(x=[ox[len(ox)//2]], y=[oy[len(oy)//2]], mode='markers', name='Apoapsis',
                                   marker=dict(size=7, color=COLORS['red'], symbol='diamond')),
                        go.Scatter(x=[ox[idx]], y=[oy[idx]], mode='markers', name='Body',
                                   marker=dict(size=12, color=COLORS['cyan'],
                                               line=dict(width=2, color='white'))),
                        # Velocity vector
                        go.Scatter(x=[ox[idx], ox[min(idx+3, len(ox)-1)]],
                                   y=[oy[idx], oy[min(idx+3, len(oy)-1)]],
                                   mode='lines', name='Velocity',
                                   line=dict(color=COLORS['orange'], width=2, dash='dot')),
                    ],
                    name=str(idx),
                ))

            fig = go.Figure(
                data=frames[0].data if frames else [],
                frames=frames,
                layout=go.Layout(
                    **PLOTLY_LAYOUT,
                    xaxis_title="x (AU)", yaxis_title="y (AU)",
                    yaxis=dict(scaleanchor="x"), height=580,
                    updatemenus=[dict(
                        type="buttons",
                        showactive=False,
                        y=1.02, x=0.5, xanchor="center",
                        buttons=[
                            dict(label="▶ Play", method="animate",
                                 args=[None, {"frame": {"duration": 80, "redraw": True},
                                              "fromcurrent": True, "transition": {"duration": 0}}]),
                            dict(label="⏸ Pause", method="animate",
                                 args=[[None], {"frame": {"duration": 0, "redraw": False},
                                                "mode": "immediate", "transition": {"duration": 0}}]),
                        ],
                        font=dict(color="white"),
                        bgcolor="rgba(31,111,235,0.6)",
                        bordercolor=COLORS['blue'],
                    )],
                ),
            )
        else:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=ox, y=oy, mode='lines', name='Orbit',
                                     line=dict(color=COLORS['blue'], width=2)))
            fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers', name='Star',
                                     marker=dict(size=16, color=COLORS['gold'], symbol='star')))
            fig.add_trace(go.Scatter(x=[ox[0]], y=[oy[0]], mode='markers', name='Periapsis',
                                     marker=dict(size=8, color=COLORS['green'], symbol='diamond')))
            fig.add_trace(go.Scatter(x=[ox[len(ox)//2]], y=[oy[len(oy)//2]], mode='markers',
                                     name='Apoapsis',
                                     marker=dict(size=8, color=COLORS['red'], symbol='diamond')))
            fig.update_layout(**PLOTLY_LAYOUT, xaxis_title="x (AU)", yaxis_title="y (AU)",
                              yaxis=dict(scaleanchor="x"), height=580)

        st.plotly_chart(fig, use_container_width=True)

    # Orbit comparison
    section_divider("Orbit Comparison")
    info_tooltip("Compare how eccentricity changes the shape of an orbit — "
                 "from perfect circles (e=0) to near-parabolic escapes (e→1).")

    compare_eccs = st.multiselect("Select eccentricities to compare",
                                   [0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 0.95],
                                   default=[0.0, 0.3, 0.7, 0.95])
    if compare_eccs:
        fig_comp = go.Figure()
        comp_colors = ['#58a6ff', '#3fb950', '#d29922', '#f85149', '#bc8cff', '#f778ba', '#79c0ff']
        for ci, e_val in enumerate(sorted(compare_eccs)):
            orb = kepler_orbit(AU, e_val, M_sun, n_points=500)
            fig_comp.add_trace(go.Scatter(
                x=orb['x'] / AU, y=orb['y'] / AU,
                mode='lines', name=f'e = {e_val}',
                line=dict(color=comp_colors[ci % len(comp_colors)], width=2),
            ))
        fig_comp.add_trace(go.Scatter(x=[0], y=[0], mode='markers', name='Star',
                                       marker=dict(size=12, color=COLORS['gold'], symbol='star'),
                                       showlegend=False))
        fig_comp.update_layout(**PLOTLY_LAYOUT, title="Orbit Shape vs Eccentricity",
                                xaxis_title="x (AU)", yaxis_title="y (AU)",
                                yaxis=dict(scaleanchor="x"), height=450)
        st.plotly_chart(fig_comp, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════
# TAB 2: HOHMANN TRANSFER
# ═══════════════════════════════════════════════════════════════════════
with tab2:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### Transfer Parameters")

        transfer_preset = st.selectbox("📋 Mission Preset", [
            "Custom", "Earth → Mars", "Earth → Venus", "Earth → Jupiter"
        ])

        TRANSFER_PRESETS = {
            "Earth → Mars": (1.0, 1.524),
            "Earth → Venus": (0.723, 1.0),
            "Earth → Jupiter": (1.0, 5.203),
        }

        if transfer_preset != "Custom":
            r1_au, r2_au = TRANSFER_PRESETS[transfer_preset]
            st.info(f"**{transfer_preset}**: {r1_au} AU → {r2_au} AU")
        else:
            r1_au = st.slider("Inner orbit (AU)", 0.3, 3.0, 1.0, 0.1)
            r2_au = st.slider("Outer orbit (AU)", r1_au + 0.1, 10.0, 1.524, 0.1)

        result = hohmann_transfer(M_sun, r1_au * AU, r2_au * AU)

        st.markdown("### Transfer Results")
        st.metric("Δv₁ (departure)", f"{result['dv1']/1000:.2f} km/s")
        st.metric("Δv₂ (arrival)", f"{result['dv2']/1000:.2f} km/s")
        st.metric("Total Δv", f"{result['dv_total']/1000:.2f} km/s")
        st.metric("Transfer time", f"{result['transfer_time']/86400:.1f} days")

    with col2:
        theta = np.linspace(0, 2 * np.pi, 300)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=r1_au * np.cos(theta), y=r1_au * np.sin(theta),
            mode='lines', name=f'Inner ({r1_au} AU)',
            line=dict(color=COLORS['green'], width=2),
        ))
        fig.add_trace(go.Scatter(
            x=r2_au * np.cos(theta), y=r2_au * np.sin(theta),
            mode='lines', name=f'Outer ({r2_au} AU)',
            line=dict(color=COLORS['red'], width=2),
        ))
        # Transfer ellipse
        a_t = result['a_transfer'] / AU
        e_t = 1 - r1_au / a_t
        t_theta = np.linspace(0, np.pi, 200)
        p_t = a_t * (1 - e_t**2)
        r_t = p_t / (1 + e_t * np.cos(t_theta))
        fig.add_trace(go.Scatter(
            x=r_t * np.cos(t_theta), y=r_t * np.sin(t_theta),
            mode='lines', name='Transfer orbit',
            line=dict(color=COLORS['orange'], width=2.5, dash='dash'),
        ))

        # Departure and arrival markers
        fig.add_trace(go.Scatter(
            x=[r1_au], y=[0], mode='markers+text', text=["Departure"],
            marker=dict(size=10, color=COLORS['green'], symbol='triangle-up',
                        line=dict(width=1, color='white')),
            textposition='bottom center', textfont=dict(color=COLORS['green'], size=10),
            showlegend=False,
        ))
        fig.add_trace(go.Scatter(
            x=[-r2_au], y=[0], mode='markers+text', text=["Arrival"],
            marker=dict(size=10, color=COLORS['red'], symbol='triangle-down',
                        line=dict(width=1, color='white')),
            textposition='bottom center', textfont=dict(color=COLORS['red'], size=10),
            showlegend=False,
        ))

        fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers', name='Sun',
                                  marker=dict(size=14, color=COLORS['gold'], symbol='star',
                                              line=dict(width=1, color='rgba(255,255,255,0.4)')),
                                  showlegend=False))
        fig.update_layout(
            **PLOTLY_LAYOUT,
            title="Hohmann Transfer Orbit",
            xaxis_title="x (AU)", yaxis_title="y (AU)",
            yaxis=dict(scaleanchor="x"), height=580,
        )
        st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════
# TAB 3: N-BODY SIMULATION
# ═══════════════════════════════════════════════════════════════════════
with tab3:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### Simulation Settings")
        n_years = st.slider("Duration (years)", 0.5, 10.0, 2.0, 0.5)
        dt_hours = st.slider("Time step (hours)", 1, 48, 12)

        nbody_preset = st.selectbox("📋 System", [
            "Sun-Earth-Moon", "Binary Stars", "Figure-8 Three-Body"
        ])

        animate_nbody = st.checkbox("🎬 Animate playback", True)

        if st.button("▶ Run Simulation", type="primary"):
            if nbody_preset == "Sun-Earth-Moon":
                sim = sun_earth_moon()
            elif nbody_preset == "Binary Stars":
                sim = NBodySimulation()
                sim.add_body(Body("Star A", 1.0 * M_sun, np.array([-0.5*AU, 0, 0]),
                                  np.array([0, -15000, 0])))
                sim.add_body(Body("Star B", 0.8 * M_sun, np.array([0.5*AU, 0, 0]),
                                  np.array([0, 15000, 0])))
            else:  # Figure-8
                sim = NBodySimulation()
                v_scale = 25000
                sim.add_body(Body("A", M_sun, np.array([-AU, 0, 0]),
                                  np.array([0, -v_scale, 0])))
                sim.add_body(Body("B", M_sun, np.array([AU, 0, 0]),
                                  np.array([0, v_scale, 0])))
                sim.add_body(Body("C", M_sun, np.array([0, 0.5*AU, 0]),
                                  np.array([v_scale*0.5, 0, 0])))

            n_steps = int(n_years * 365.25 * 24 / dt_hours)
            record_every = max(1, n_steps // 2000)

            progress = st.progress(0, text="Integrating N-body system...")
            history = sim.run(dt=dt_hours * 3600, n_steps=n_steps, record_interval=record_every)
            progress.progress(100, text="✅ Simulation complete!")

            st.session_state['nbody_history'] = history
            st.session_state['nbody_sim'] = sim
            st.success(f"Simulated {n_steps:,} steps in {n_years} years")

    with col2:
        if 'nbody_history' in st.session_state:
            history = st.session_state['nbody_history']

            body_colors = {
                'Sun': COLORS['gold'], 'Star A': '#58a6ff', 'Star B': '#f85149',
                'Earth': '#4169E1', 'Moon': '#C0C0C0',
                'A': COLORS['blue'], 'B': COLORS['red'], 'C': COLORS['green'],
            }

            if animate_nbody:
                # Create animated playback
                names = list(history['positions'].keys())
                n_pts = len(list(history['positions'].values())[0])
                n_anim_frames = min(80, n_pts)
                frame_indices = np.linspace(0, n_pts - 1, n_anim_frames, dtype=int)

                base_data = []
                for name in names:
                    traj = history['positions'][name]
                    col = body_colors.get(name, '#fff')
                    # Trail
                    base_data.append(go.Scatter(
                        x=traj[:frame_indices[0]+1, 0] / AU,
                        y=traj[:frame_indices[0]+1, 1] / AU,
                        mode='lines', name=name,
                        line=dict(color=col, width=1.5),
                    ))
                    # Current position
                    base_data.append(go.Scatter(
                        x=[traj[frame_indices[0], 0] / AU],
                        y=[traj[frame_indices[0], 1] / AU],
                        mode='markers', showlegend=False,
                        marker=dict(color=col, size=10, line=dict(width=1.5, color='white')),
                    ))

                frames = []
                for fi in frame_indices:
                    frame_data = []
                    for name in names:
                        traj = history['positions'][name]
                        col = body_colors.get(name, '#fff')
                        frame_data.append(go.Scatter(
                            x=traj[:fi+1, 0] / AU, y=traj[:fi+1, 1] / AU,
                            mode='lines', name=name,
                            line=dict(color=col, width=1.5),
                        ))
                        frame_data.append(go.Scatter(
                            x=[traj[fi, 0] / AU], y=[traj[fi, 1] / AU],
                            mode='markers', showlegend=False,
                            marker=dict(color=col, size=10, line=dict(width=1.5, color='white')),
                        ))
                    frames.append(go.Frame(data=frame_data, name=str(fi)))

                fig = go.Figure(data=base_data, frames=frames)
                fig.update_layout(
                    **PLOTLY_LAYOUT,
                    title="N-Body Gravitational Simulation",
                    xaxis_title="x (AU)", yaxis_title="y (AU)",
                    yaxis=dict(scaleanchor="x"), height=580,
                    updatemenus=[dict(
                        type="buttons", showactive=False,
                        y=1.02, x=0.5, xanchor="center",
                        buttons=[
                            dict(label="▶ Play", method="animate",
                                 args=[None, {"frame": {"duration": 50, "redraw": True},
                                              "fromcurrent": True}]),
                            dict(label="⏸ Pause", method="animate",
                                 args=[[None], {"frame": {"duration": 0}, "mode": "immediate"}]),
                        ],
                        font=dict(color="white"),
                        bgcolor="rgba(31,111,235,0.6)",
                        bordercolor=COLORS['blue'],
                    )],
                )
            else:
                fig = go.Figure()
                for name, traj in history['positions'].items():
                    col = body_colors.get(name, '#fff')
                    fig.add_trace(go.Scatter(
                        x=traj[:, 0] / AU, y=traj[:, 1] / AU,
                        mode='lines', name=name,
                        line=dict(color=col, width=1.5),
                    ))
                    fig.add_trace(go.Scatter(
                        x=[traj[-1, 0] / AU], y=[traj[-1, 1] / AU],
                        mode='markers', showlegend=False,
                        marker=dict(color=col, size=10, line=dict(width=1.5, color='white')),
                    ))
                fig.update_layout(
                    **PLOTLY_LAYOUT,
                    title="N-Body Gravitational Simulation",
                    xaxis_title="x (AU)", yaxis_title="y (AU)",
                    yaxis=dict(scaleanchor="x"), height=580,
                )
            st.plotly_chart(fig, use_container_width=True)

            # Energy conservation plot
            E = history['energies']
            E0 = E[0] if E[0] != 0 else 1
            rel_err = abs((E[-1] - E[0]) / E0)

            fig_e = go.Figure()
            fig_e.add_trace(go.Scatter(
                y=(E - E[0]) / abs(E0), mode='lines',
                line=dict(color=COLORS['blue'], width=2), name='ΔE/E₀',
            ))
            fig_e.update_layout(**PLOTLY_LAYOUT, title="Energy Conservation",
                                 yaxis_title="ΔE/E₀", height=250)
            st.plotly_chart(fig_e, use_container_width=True)

            if rel_err < 1e-6:
                st.success(f"✅ Excellent energy conservation: ΔE/E₀ = {rel_err:.2e}")
            elif rel_err < 1e-3:
                st.warning(f"⚠️ Acceptable energy conservation: ΔE/E₀ = {rel_err:.2e}")
            else:
                st.error(f"❌ Poor energy conservation: ΔE/E₀ = {rel_err:.2e} — try smaller time step")
        else:
            st.markdown("""
            <div style="display:flex; align-items:center; justify-content:center;
                        height:400px; border:1px dashed #30363d; border-radius:12px;
                        background: rgba(22,27,34,0.5);">
                <div style="text-align:center; color:#8b949e;">
                    <div style="font-size:3rem; margin-bottom:0.5rem;">🌌</div>
                    <div style="font-size:1.1rem;">Click <b>▶ Run Simulation</b> to start</div>
                    <div style="font-size:0.85rem; margin-top:0.3rem;">
                        The N-body integrator will compute gravitational trajectories
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
