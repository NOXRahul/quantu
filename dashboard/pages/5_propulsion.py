"""QuantU Dashboard — Propulsion Simulator Page"""
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from quantu.propulsion.ion_drive import IonThruster
from quantu.propulsion.trajectory import TrajectoryPlanner
from quantu.constants import M_sun, AU, g0

st.set_page_config(page_title="QuantU · Propulsion", page_icon="⚡", layout="wide")

from theme import apply_theme, page_header, section_divider, info_tooltip, PLOTLY_LAYOUT, COLORS
apply_theme()

page_header("Propulsion Simulation Laboratory",
            "Ion drive performance, trajectory planning, and delta-v analysis", "⚡")

st.latex(r"\Delta v = v_e \ln\frac{m_0}{m_f} \qquad F = \dot{m} \cdot v_e \qquad I_{sp} = \frac{v_e}{g_0}")

tab1, tab2, tab3 = st.tabs(["🔋 Ion Thruster", "🛰️ Trajectory Planner", "📊 Δv Budget"])

# ═══════════════════════════════════════════════════════════════════════
# TAB 1: ION THRUSTER
# ═══════════════════════════════════════════════════════════════════════
with tab1:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### Thruster Parameters")

        thruster_preset = st.selectbox("📋 Thruster Type", [
            "Custom", "NSTAR (Dawn)", "NEXT-C", "Hall Effect (SPT-140)", "VASIMR"
        ])

        THRUSTER_PRESETS = {
            "NSTAR (Dawn)": (3100, 2.3, 0.62),
            "NEXT-C": (4190, 6.9, 0.70),
            "Hall Effect (SPT-140)": (1770, 4.5, 0.55),
            "VASIMR": (5000, 200.0, 0.60),
        }

        if thruster_preset != "Custom":
            isp, power_kw, efficiency = THRUSTER_PRESETS[thruster_preset]
            st.info(f"**{thruster_preset}**: Isp={isp}s, P={power_kw}kW, η={efficiency}")
        else:
            isp = st.slider("Specific Impulse Isp (s)", 500, 10000, 3000, 100)
            power_kw = st.slider("Input Power (kW)", 0.5, 50.0, 5.0, 0.5)
            efficiency = st.slider("Efficiency η", 0.1, 0.9, 0.65, 0.05)

        thruster = IonThruster(isp=isp, power_kw=power_kw, efficiency=efficiency)

        st.markdown("### Performance Metrics")
        st.metric("Thrust", f"{thruster.thrust * 1000:.2f} mN")
        st.metric("Exhaust Velocity", f"{thruster.v_e / 1000:.1f} km/s")
        st.metric("Mass Flow Rate", f"{thruster.mass_flow_rate * 1e6:.2f} mg/s")

        section_divider("Δv Calculator")
        m0 = st.number_input("Spacecraft mass (kg)", 100, 50000, 1000)
        m_prop = st.number_input("Propellant mass (kg)", 1, int(m0 * 0.9), 100)
        dv = thruster.delta_v(m0, m_prop)
        burn_t = thruster.burn_time(m_prop)
        st.metric("Available Δv", f"{dv / 1000:.2f} km/s")
        st.metric("Burn Time", f"{burn_t / 86400:.1f} days")

    with col2:
        # Thrust vs Isp
        envelope = thruster.performance_envelope(isp_range=(500, 10000))

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=envelope['isp'], y=envelope['thrust_mN'],
            mode='lines', name='Thrust (mN)',
            line=dict(color=COLORS['blue'], width=3),
            fill='tozeroy', fillcolor='rgba(88,166,255,0.08)',
            hovertemplate="Isp: %{x:.0f} s<br>Thrust: %{y:.2f} mN<extra></extra>",
        ))
        fig.add_vline(x=isp, line_dash="dash", line_color=COLORS['red'],
                       annotation_text=f"Current Isp = {isp}s",
                       annotation_font_color=COLORS['red'])
        fig.update_layout(
            **PLOTLY_LAYOUT,
            title="Thrust vs Specific Impulse (Constant Power)",
            xaxis_title="Isp (s)", yaxis_title="Thrust (mN)", height=340,
        )
        st.plotly_chart(fig, use_container_width=True)

        # Δv vs propellant mass fraction
        mass_fractions = np.linspace(0.01, 0.9, 200)
        dvs = thruster.v_e * np.log(1 / (1 - mass_fractions))

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=mass_fractions * 100, y=dvs / 1000,
            mode='lines', name='Δv',
            line=dict(color=COLORS['green'], width=3),
            fill='tozeroy', fillcolor='rgba(63,185,80,0.08)',
            hovertemplate="Propellant: %{x:.1f}%<br>Δv: %{y:.2f} km/s<extra></extra>",
        ))
        fig2.add_hline(y=dv / 1000, line_dash="dot", line_color=COLORS['orange'],
                        annotation_text=f"Current: {dv/1000:.1f} km/s",
                        annotation_font_color=COLORS['orange'])
        fig2.update_layout(
            **PLOTLY_LAYOUT,
            title="Tsiolkovsky: Δv vs Propellant Mass Fraction",
            xaxis_title="Propellant Fraction (%)", yaxis_title="Δv (km/s)", height=340,
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Thruster comparison
    section_divider("Thruster Technology Comparison")

    comparison = [
        {"name": "Chemical (Bipropellant)", "isp": 450, "thrust": "100,000 N", "power": "N/A", "status": "Mature"},
        {"name": "Ion (NSTAR)", "isp": 3100, "thrust": "92 mN", "power": "2.3 kW", "status": "Flight Proven"},
        {"name": "Ion (NEXT-C)", "isp": 4190, "thrust": "236 mN", "power": "6.9 kW", "status": "Flight Proven"},
        {"name": "Hall Effect", "isp": 1770, "thrust": "290 mN", "power": "4.5 kW", "status": "Flight Proven"},
        {"name": "VASIMR", "isp": 5000, "thrust": "5.7 N", "power": "200 kW", "status": "In Development"},
        {"name": "Nuclear Thermal", "isp": 900, "thrust": "110,000 N", "power": "N/A", "status": "Tested (1970s)"},
    ]

    isp_vals = [c['isp'] for c in comparison]
    names_comp = [c['name'] for c in comparison]
    bar_colors = [COLORS['blue'], COLORS['green'], COLORS['cyan'],
                  COLORS['orange'], COLORS['purple'], COLORS['red']]

    fig_comp = go.Figure(data=go.Bar(
        x=names_comp, y=isp_vals,
        marker_color=bar_colors,
        text=[f"{v:,}s" for v in isp_vals],
        textposition='outside',
        hovertemplate="%{x}<br>Isp: %{y:,} s<extra></extra>",
    ))
    fig_comp.update_layout(
        **PLOTLY_LAYOUT,
        title="Specific Impulse by Thruster Technology",
        xaxis_title="Thruster Type", yaxis_title="Isp (s)", height=400,
    )
    st.plotly_chart(fig_comp, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════
# TAB 2: TRAJECTORY PLANNER
# ═══════════════════════════════════════════════════════════════════════
with tab2:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### Mission Parameters")

        mission_preset = st.selectbox("📋 Mission", [
            "Custom", "Earth → Mars", "Earth → Jupiter", "Earth → Saturn"
        ])

        MISSION_PRESETS = {
            "Earth → Mars": (1.0, 0.1, 3000, 365, 1000, 90),
            "Earth → Jupiter": (1.0, 0.5, 4000, 730, 2000, 90),
            "Earth → Saturn": (1.0, 0.3, 5000, 1200, 1500, 90),
        }

        if mission_preset != "Custom":
            start_r, thrust_N, mission_isp, mission_days, sc_mass, thrust_angle = MISSION_PRESETS[mission_preset]
            st.info(f"**{mission_preset}** — {mission_days} days")
        else:
            start_r = st.slider("Start orbit (AU)", 0.5, 3.0, 1.0, 0.1)
            thrust_N = st.number_input("Thrust (N)", 0.001, 10.0, 0.1, format="%.3f")
            mission_isp = st.number_input("Mission Isp (s)", 500, 10000, 3000)
            mission_days = st.slider("Duration (days)", 30, 1500, 365)
            sc_mass = st.number_input("Spacecraft mass (kg)", 100, 10000, 1000)
            thrust_angle = st.slider("Thrust angle (°)", 0, 360, 90)

        t_rad = np.radians(thrust_angle)
        t_dir = np.array([np.cos(t_rad), np.sin(t_rad)])

    with col2:
        if st.button("▶ Simulate Trajectory", type="primary"):
            planner = TrajectoryPlanner(M_sun, sc_mass)
            r0 = np.array([start_r * AU, 0.0])
            v_circ = np.sqrt(planner.mu / (start_r * AU))
            v0 = np.array([0.0, v_circ])

            progress = st.progress(0, text="Computing trajectory...")
            result = planner.constant_thrust_trajectory(
                r0, v0, thrust_N, mission_isp, t_dir,
                mission_days * 86400, dt=3600,
            )
            progress.progress(100, text="✅ Trajectory computed!")

            st.session_state['traj_result'] = result
            st.session_state['traj_start_r'] = start_r

        if 'traj_result' in st.session_state:
            result = st.session_state['traj_result']
            start_r_saved = st.session_state.get('traj_start_r', 1.0)

            fig = go.Figure()

            # Color trajectory by velocity
            fig.add_trace(go.Scatter(
                x=result['x'] / AU, y=result['y'] / AU,
                mode='lines', name='Trajectory',
                line=dict(color=COLORS['blue'], width=2.5),
                hovertemplate="x: %{x:.3f} AU<br>y: %{y:.3f} AU<extra></extra>",
            ))

            # Start and end markers
            fig.add_trace(go.Scatter(
                x=[result['x'][0] / AU], y=[result['y'][0] / AU],
                mode='markers+text', text=["Start"], name='Departure',
                marker=dict(size=10, color=COLORS['green'], symbol='triangle-up',
                            line=dict(width=1, color='white')),
                textposition='bottom center', textfont=dict(color=COLORS['green'], size=10),
            ))
            fig.add_trace(go.Scatter(
                x=[result['x'][-1] / AU], y=[result['y'][-1] / AU],
                mode='markers+text', text=["End"], name='Arrival',
                marker=dict(size=10, color=COLORS['red'], symbol='square',
                            line=dict(width=1, color='white')),
                textposition='bottom center', textfont=dict(color=COLORS['red'], size=10),
            ))

            # Reference orbit
            theta = np.linspace(0, 2 * np.pi, 200)
            fig.add_trace(go.Scatter(
                x=start_r_saved * np.cos(theta), y=start_r_saved * np.sin(theta),
                mode='lines', name='Start orbit',
                line=dict(color=COLORS['green'], width=1, dash='dot'),
            ))
            fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers',
                                      marker=dict(size=14, color=COLORS['gold'], symbol='star'),
                                      name='Sun', showlegend=False))
            fig.update_layout(
                **PLOTLY_LAYOUT,
                title="Spacecraft Trajectory",
                xaxis_title="x (AU)", yaxis_title="y (AU)",
                yaxis=dict(scaleanchor="x"), height=550,
            )
            st.plotly_chart(fig, use_container_width=True)

            mc1, mc2, mc3, mc4 = st.columns(4)
            with mc1:
                st.metric("Final Δv", f"{result['delta_v'][-1]/1000:.2f} km/s")
            with mc2:
                st.metric("Propellant used", f"{result['mass'][0]-result['mass'][-1]:.1f} kg")
            with mc3:
                final_r = np.sqrt(result['x'][-1]**2 + result['y'][-1]**2)
                st.metric("Final orbit", f"{final_r/AU:.3f} AU")
            with mc4:
                st.metric("Remaining mass", f"{result['mass'][-1]:.1f} kg")
        else:
            st.markdown("""
            <div style="display:flex; align-items:center; justify-content:center;
                        height:400px; border:1px dashed #30363d; border-radius:12px;
                        background: rgba(22,27,34,0.5);">
                <div style="text-align:center; color:#8b949e;">
                    <div style="font-size:3rem; margin-bottom:0.5rem;">🛰️</div>
                    <div style="font-size:1.1rem;">Click <b>▶ Simulate Trajectory</b> to launch</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
# TAB 3: Δv BUDGET
# ═══════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### Common Mission Δv Requirements")
    info_tooltip("These are the approximate Δv values needed for common space missions. "
                 "Higher Δv means more propellant or a more efficient engine is needed.")

    missions = [
        {"name": "LEO insertion", "delta_v": 9400, "icon": "🌍"},
        {"name": "LEO → GTO", "delta_v": 2440, "icon": "📡"},
        {"name": "GTO → GEO", "delta_v": 1470, "icon": "🛰️"},
        {"name": "LEO → Moon", "delta_v": 3130, "icon": "🌙"},
        {"name": "LEO → Mars", "delta_v": 3600, "icon": "🔴"},
        {"name": "LEO → Jupiter", "delta_v": 6300, "icon": "🪐"},
        {"name": "LEO → Solar escape", "delta_v": 8750, "icon": "☀️"},
        {"name": "Earth escape", "delta_v": 11200, "icon": "🚀"},
    ]

    # Waterfall-style cumulative chart
    names = [f"{m['icon']} {m['name']}" for m in missions]
    dvs = [m['delta_v'] / 1000 for m in missions]
    bar_colors = [COLORS['blue'], COLORS['green'], COLORS['cyan'], COLORS['purple'],
                  COLORS['orange'], COLORS['red'], COLORS['pink'], '#ff7b72']

    fig = go.Figure(data=go.Bar(
        x=names, y=dvs,
        marker_color=bar_colors,
        text=[f"{d:.1f}" for d in dvs],
        textposition='outside',
        textfont=dict(color='white', size=11),
        hovertemplate="%{x}<br>Δv: %{y:.1f} km/s<extra></extra>",
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title="Δv Budget — Common Space Missions",
        xaxis_title="Mission", yaxis_title="Δv (km/s)", height=480,
        xaxis=dict(tickangle=-25),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Mission planner quick calc
    section_divider("Quick Mission Calculator")
    qc1, qc2, qc3 = st.columns(3)
    with qc1:
        target_dv = st.selectbox("Target mission",
                                  [f"{m['name']} ({m['delta_v']/1000:.1f} km/s)" for m in missions])
        target_dv_val = missions[[f"{m['name']} ({m['delta_v']/1000:.1f} km/s)"
                                   for m in missions].index(target_dv)]['delta_v']
    with qc2:
        calc_isp = st.number_input("Engine Isp (s)", 200, 10000, 3000, key="calc_isp")
    with qc3:
        calc_mass = st.number_input("Dry mass (kg)", 100, 100000, 1000, key="calc_dm")

    v_e = calc_isp * g0
    mass_ratio = np.exp(target_dv_val / v_e)
    prop_mass = calc_mass * (mass_ratio - 1)

    rc1, rc2, rc3 = st.columns(3)
    with rc1:
        st.metric("Mass Ratio (m₀/mf)", f"{mass_ratio:.2f}")
    with rc2:
        st.metric("Propellant Needed", f"{prop_mass:.0f} kg")
    with rc3:
        st.metric("Total Launch Mass", f"{calc_mass + prop_mass:.0f} kg")
