"""
Plotly Visualization Engine
============================
High-level Plotly wrappers for QuantU physics visualizations.
All figures use a dark NASA-inspired theme.
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from .color_maps import COLORMAPS


DARK_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="#0d1117",
    plot_bgcolor="#0d1117",
    font=dict(family="Inter, sans-serif", color="#c9d1d9"),
    margin=dict(l=40, r=40, t=50, b=40),
)


class PlotlyVisualizer:
    """Factory for physics-themed Plotly figures."""

    @staticmethod
    def potential_heatmap(X, Y, values, title="Gravitational Potential"):
        fig = go.Figure(data=go.Heatmap(
            x=X[0, :], y=Y[:, 0], z=values,
            colorscale=COLORMAPS['gravity_well'],
            colorbar=dict(title="Φ (J/kg)"),
        ))
        fig.update_layout(title=title, xaxis_title="x", yaxis_title="y",
                          aspectmode='equal', **DARK_LAYOUT)
        return fig

    @staticmethod
    def vector_field(X, Y, U, V, title="Gravitational Field"):
        mag = np.sqrt(U**2 + V**2)
        mag_safe = np.maximum(mag, 1e-20)
        un, vn = U / mag_safe, V / mag_safe
        fig = go.Figure(data=go.Cone(
            x=X.flatten(), y=Y.flatten(), z=np.zeros_like(X).flatten(),
            u=un.flatten(), v=vn.flatten(), w=np.zeros_like(X).flatten(),
            colorscale=COLORMAPS['spacetime'],
            sizemode="absolute", sizeref=0.3,
        ))
        fig.update_layout(title=title, **DARK_LAYOUT)
        return fig

    @staticmethod
    def spacetime_surface(X, Y, Z, title="Spacetime Curvature"):
        fig = go.Figure(data=go.Surface(
            x=X, y=Y, z=Z,
            colorscale=COLORMAPS['gravity_well'],
            colorbar=dict(title="Curvature"),
            opacity=0.9,
        ))
        fig.update_layout(
            title=title,
            scene=dict(
                xaxis_title="x", yaxis_title="y", zaxis_title="Curvature",
                bgcolor="#0d1117",
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.0)),
            ),
            **DARK_LAYOUT,
        )
        return fig

    @staticmethod
    def orbit_plot(trajectories, names=None, colors=None, title="Orbital Trajectories"):
        fig = go.Figure()
        for i, traj in enumerate(trajectories):
            name = names[i] if names else f"Body {i}"
            color = colors[i] if colors else None
            fig.add_trace(go.Scatter(
                x=traj[:, 0], y=traj[:, 1],
                mode='lines', name=name,
                line=dict(color=color, width=2),
            ))
            fig.add_trace(go.Scatter(
                x=[traj[-1, 0]], y=[traj[-1, 1]],
                mode='markers', name=f"{name} (now)",
                marker=dict(color=color, size=8),
                showlegend=False,
            ))
        fig.update_layout(title=title, xaxis_title="x (m)", yaxis_title="y (m)",
                          yaxis=dict(scaleanchor="x"), **DARK_LAYOUT)
        return fig

    @staticmethod
    def energy_plot(times, energies, title="Energy Conservation"):
        fig = go.Figure()
        e0 = energies[0] if energies[0] != 0 else 1.0
        relative = (energies - energies[0]) / abs(e0)
        fig.add_trace(go.Scatter(
            x=times, y=relative, mode='lines',
            line=dict(color="#58a6ff", width=2), name="ΔE/E₀",
        ))
        fig.update_layout(title=title, xaxis_title="Time (s)",
                          yaxis_title="Relative Energy Error", **DARK_LAYOUT)
        return fig

    @staticmethod
    def warp_bubble(X, Y, Z, energy, title="Alcubierre Warp Bubble"):
        fig = make_subplots(rows=1, cols=2,
                            specs=[[{'type': 'surface'}, {'type': 'heatmap'}]],
                            subplot_titles=["Warp Geometry", "Energy Density"])
        fig.add_trace(go.Surface(
            x=X, y=Y, z=Z, colorscale=COLORMAPS['warp_field'],
            showscale=False, opacity=0.85,
        ), row=1, col=1)
        fig.add_trace(go.Heatmap(
            z=energy, colorscale=COLORMAPS['energy_density'],
            colorbar=dict(title="ρ", x=1.05),
        ), row=1, col=2)
        fig.update_layout(title=title, **DARK_LAYOUT)
        return fig
