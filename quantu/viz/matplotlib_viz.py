"""
Matplotlib Visualization Utilities
====================================
Static 2D/3D plots for publication-quality figures.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


def setup_dark_style():
    """Apply QuantU dark theme to matplotlib."""
    plt.rcParams.update({
        'figure.facecolor': '#0d1117',
        'axes.facecolor': '#0d1117',
        'axes.edgecolor': '#30363d',
        'text.color': '#c9d1d9',
        'axes.labelcolor': '#c9d1d9',
        'xtick.color': '#8b949e',
        'ytick.color': '#8b949e',
        'grid.color': '#21262d',
        'font.family': 'sans-serif',
        'font.size': 11,
    })


def plot_potential_field(X, Y, values, title="Gravitational Potential", save_path=None):
    setup_dark_style()
    fig, ax = plt.subplots(figsize=(10, 8))
    cp = ax.contourf(X, Y, values, levels=40, cmap='inferno')
    plt.colorbar(cp, ax=ax, label="Φ (J/kg)")
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_aspect('equal')
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    return fig


def plot_vector_field(X, Y, U, V, title="Force Field", save_path=None):
    setup_dark_style()
    fig, ax = plt.subplots(figsize=(10, 8))
    mag = np.sqrt(U**2 + V**2)
    ax.streamplot(X, Y, U, V, color=mag, cmap='plasma', density=1.5, linewidth=1)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_aspect('equal')
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    return fig


def plot_spacetime_3d(X, Y, Z, title="Spacetime Curvature", save_path=None):
    setup_dark_style()
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='coolwarm', alpha=0.85, edgecolor='#333', linewidth=0.3)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("Curvature")
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    return fig
