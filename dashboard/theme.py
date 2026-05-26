"""
QuantU Dashboard — Shared Theme & Layout System
=================================================
Provides consistent NASA-inspired dark theme, Plotly layout defaults,
and reusable UI components across all dashboard pages.

Usage:
    from theme import apply_theme, page_header, PLOTLY_LAYOUT, metric_card
"""

import streamlit as st

# ── Plotly Dark Layout Constant ──────────────────────────────────────
PLOTLY_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="#0d1117",
    plot_bgcolor="#0d1117",
    font=dict(family="Inter, sans-serif", color="#c9d1d9", size=12),
    margin=dict(l=50, r=30, t=50, b=50),
    hoverlabel=dict(
        bgcolor="#21262d",
        bordercolor="#58a6ff",
        font=dict(family="JetBrains Mono, monospace", size=12, color="#e6edf3"),
    ),
    legend=dict(
        bgcolor="rgba(22,27,34,0.8)",
        bordercolor="#30363d",
        borderwidth=1,
        font=dict(size=11),
    ),
)

PLOTLY_SCENE = dict(
    bgcolor="#0d1117",
    xaxis=dict(
        backgroundcolor="#0d1117",
        gridcolor="#21262d",
        showbackground=True,
        zerolinecolor="#30363d",
    ),
    yaxis=dict(
        backgroundcolor="#0d1117",
        gridcolor="#21262d",
        showbackground=True,
        zerolinecolor="#30363d",
    ),
    zaxis=dict(
        backgroundcolor="#0d1117",
        gridcolor="#21262d",
        showbackground=True,
        zerolinecolor="#30363d",
    ),
)

# ── Color Palette ────────────────────────────────────────────────────
COLORS = {
    "blue": "#58a6ff",
    "purple": "#bc8cff",
    "green": "#3fb950",
    "orange": "#d29922",
    "red": "#f85149",
    "pink": "#f778ba",
    "cyan": "#79c0ff",
    "gold": "#FFD700",
    "white": "#e6edf3",
    "muted": "#8b949e",
}


def apply_theme():
    """Apply the QuantU NASA-inspired dark theme to any page."""
    st.markdown(_THEME_CSS, unsafe_allow_html=True)


def page_header(title: str, subtitle: str, icon: str = "🌌"):
    """Render a consistent animated page header."""
    st.markdown(f"""
    <div class="page-header">
        <div class="page-header-icon">{icon}</div>
        <h1 class="page-header-title">{title}</h1>
        <p class="page-header-subtitle">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def metric_card(label: str, value: str, delta: str = None, icon: str = "📊"):
    """Render a styled metric card with optional delta."""
    delta_html = f'<div class="mc-delta">{delta}</div>' if delta else ''
    st.markdown(f"""
    <div class="metric-card">
        <div class="mc-icon">{icon}</div>
        <div class="mc-body">
            <div class="mc-value">{value}</div>
            <div class="mc-label">{label}</div>
            {delta_html}
        </div>
    </div>
    """, unsafe_allow_html=True)


def section_divider(title: str = None):
    """Render a styled section divider with optional title."""
    if title:
        st.markdown(f"""
        <div class="section-divider">
            <span class="section-divider-text">{title}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="section-divider-line"></div>', unsafe_allow_html=True)


def physics_badge(text: str, badge_type: str = "established"):
    """Render a physics classification badge."""
    css_class = f"badge-{badge_type}"
    return f'<span class="status-badge {css_class}">{text}</span>'


def info_tooltip(text: str):
    """Render an informational tooltip block."""
    st.markdown(f"""
    <div class="info-tooltip">
        <div class="info-tooltip-icon">💡</div>
        <div class="info-tooltip-text">{text}</div>
    </div>
    """, unsafe_allow_html=True)


# ── CSS ──────────────────────────────────────────────────────────────
_THEME_CSS = """
<style>
    /* ═══ Fonts ═══ */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* ═══ CSS Variables ═══ */
    :root {
        --bg-primary: #0d1117;
        --bg-secondary: #161b22;
        --bg-tertiary: #21262d;
        --bg-elevated: #1c2333;
        --text-primary: #e6edf3;
        --text-secondary: #8b949e;
        --text-muted: #6e7681;
        --accent-blue: #58a6ff;
        --accent-purple: #bc8cff;
        --accent-green: #3fb950;
        --accent-orange: #d29922;
        --accent-red: #f85149;
        --accent-pink: #f778ba;
        --accent-cyan: #79c0ff;
        --border: #30363d;
        --border-muted: #21262d;
        --glow-blue: 0 0 20px rgba(88,166,255,0.3);
        --glow-purple: 0 0 20px rgba(188,140,255,0.3);
        --glow-green: 0 0 20px rgba(63,185,80,0.3);
        --radius-sm: 6px;
        --radius-md: 10px;
        --radius-lg: 16px;
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* ═══ Global ═══ */
    .stApp {
        background: var(--bg-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-primary);
    }

    /* Starfield background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background:
            radial-gradient(1.5px 1.5px at 20% 30%, rgba(88,166,255,0.4), transparent),
            radial-gradient(1px 1px at 40% 70%, rgba(188,140,255,0.3), transparent),
            radial-gradient(1.5px 1.5px at 60% 10%, rgba(63,185,80,0.3), transparent),
            radial-gradient(1px 1px at 80% 50%, rgba(247,120,186,0.3), transparent),
            radial-gradient(1px 1px at 10% 80%, rgba(121,192,255,0.3), transparent),
            radial-gradient(1.5px 1.5px at 90% 20%, rgba(88,166,255,0.3), transparent),
            radial-gradient(1px 1px at 50% 50%, rgba(210,153,34,0.2), transparent),
            radial-gradient(1px 1px at 30% 90%, rgba(188,140,255,0.2), transparent),
            radial-gradient(1.5px 1.5px at 70% 40%, rgba(63,185,80,0.2), transparent),
            radial-gradient(1px 1px at 15% 55%, rgba(88,166,255,0.25), transparent),
            radial-gradient(1px 1px at 85% 75%, rgba(247,120,186,0.2), transparent),
            radial-gradient(1.5px 1.5px at 45% 25%, rgba(121,192,255,0.2), transparent);
        pointer-events: none;
        z-index: 0;
        animation: twinkle 8s ease-in-out infinite alternate;
    }

    @keyframes twinkle {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.7; }
    }

    /* ═══ Sidebar ═══ */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1117 0%, #161b22 50%, #0d1117 100%);
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #58a6ff, #bc8cff, #f778ba);
        z-index: 10;
    }

    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: var(--accent-blue);
        font-weight: 600;
    }

    [data-testid="stSidebar"] .stSlider label,
    [data-testid="stSidebar"] .stCheckbox label,
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stNumberInput label {
        color: var(--text-secondary) !important;
        font-size: 0.85rem;
    }

    /* ═══ Page Header ═══ */
    .page-header {
        text-align: center;
        padding: 1.5rem 0 1.5rem 0;
        margin-bottom: 1.5rem;
        position: relative;
    }

    .page-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 10%;
        right: 10%;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--accent-blue), var(--accent-purple), transparent);
    }

    .page-header-icon {
        font-size: 2.5rem;
        margin-bottom: 0.3rem;
        filter: drop-shadow(0 0 10px rgba(88,166,255,0.4));
    }

    .page-header-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #58a6ff 0%, #bc8cff 40%, #f778ba 80%, #d29922 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.03em;
        line-height: 1.2;
        margin: 0;
        animation: gradientShift 6s ease-in-out infinite;
        background-size: 200% 200%;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .page-header-subtitle {
        color: var(--text-secondary);
        font-size: 1rem;
        font-weight: 300;
        margin-top: 0.3rem;
        letter-spacing: 0.02em;
    }

    /* ═══ Metric Cards ═══ */
    .metric-card {
        background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 1rem 1.2rem;
        display: flex;
        align-items: center;
        gap: 0.8rem;
        transition: var(--transition);
        margin-bottom: 0.5rem;
    }

    .metric-card:hover {
        border-color: var(--accent-blue);
        box-shadow: var(--glow-blue);
        transform: translateY(-1px);
    }

    .mc-icon {
        font-size: 1.5rem;
        filter: drop-shadow(0 0 6px rgba(88,166,255,0.3));
    }

    .mc-value {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--accent-blue);
        font-family: 'JetBrains Mono', monospace;
    }

    .mc-label {
        font-size: 0.75rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    .mc-delta {
        font-size: 0.8rem;
        color: var(--accent-green);
        font-family: 'JetBrains Mono', monospace;
    }

    /* ═══ Module Cards ═══ */
    .module-card {
        background: linear-gradient(145deg, var(--bg-secondary), var(--bg-elevated));
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        margin: 0.5rem 0;
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }

    .module-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple));
        opacity: 0;
        transition: var(--transition);
    }

    .module-card:hover {
        border-color: var(--accent-blue);
        box-shadow: var(--glow-blue);
        transform: translateY(-3px);
    }

    .module-card:hover::before {
        opacity: 1;
    }

    .module-card h3 {
        color: var(--accent-blue);
        font-size: 1.15rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .module-card p {
        color: var(--text-secondary);
        font-size: 0.88rem;
        line-height: 1.6;
        margin: 0;
    }

    /* ═══ Status Badges ═══ */
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.03em;
        text-transform: uppercase;
    }

    .badge-established {
        background: rgba(63,185,80,0.12);
        color: var(--accent-green);
        border: 1px solid rgba(63,185,80,0.25);
    }

    .badge-speculative {
        background: rgba(210,153,34,0.12);
        color: var(--accent-orange);
        border: 1px solid rgba(210,153,34,0.25);
    }

    .badge-new {
        background: rgba(88,166,255,0.12);
        color: var(--accent-blue);
        border: 1px solid rgba(88,166,255,0.25);
    }

    /* ═══ Stats Container ═══ */
    .stats-container {
        display: flex;
        gap: 1rem;
        justify-content: center;
        flex-wrap: wrap;
        margin: 1.5rem 0;
    }

    .stat-item {
        background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 1rem 1.8rem;
        text-align: center;
        min-width: 140px;
        transition: var(--transition);
    }

    .stat-item:hover {
        border-color: var(--accent-blue);
        box-shadow: var(--glow-blue);
        transform: translateY(-2px);
    }

    .stat-item .number {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'JetBrains Mono', monospace;
    }

    .stat-item .label {
        font-size: 0.75rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-top: 0.2rem;
    }

    /* ═══ Disclaimer ═══ */
    .disclaimer {
        background: rgba(210,153,34,0.08);
        border: 1px solid rgba(210,153,34,0.2);
        border-left: 3px solid var(--accent-orange);
        border-radius: var(--radius-sm);
        padding: 0.8rem 1rem;
        margin: 1rem 0;
        font-size: 0.85rem;
        color: var(--accent-orange);
    }

    /* ═══ Info Tooltip ═══ */
    .info-tooltip {
        display: flex;
        align-items: flex-start;
        gap: 0.6rem;
        background: rgba(88,166,255,0.06);
        border: 1px solid rgba(88,166,255,0.15);
        border-left: 3px solid var(--accent-blue);
        border-radius: var(--radius-sm);
        padding: 0.7rem 1rem;
        margin: 0.5rem 0;
    }

    .info-tooltip-icon { font-size: 1rem; }
    .info-tooltip-text {
        font-size: 0.85rem;
        color: var(--text-secondary);
        line-height: 1.5;
    }

    /* ═══ Section Dividers ═══ */
    .section-divider {
        display: flex;
        align-items: center;
        margin: 1.5rem 0;
        gap: 1rem;
    }

    .section-divider::before,
    .section-divider::after {
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border), transparent);
    }

    .section-divider-text {
        color: var(--text-muted);
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 600;
        white-space: nowrap;
    }

    .section-divider-line {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border), transparent);
        margin: 1.5rem 0;
    }

    /* ═══ Tabs ═══ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: var(--bg-secondary);
        border-radius: var(--radius-md);
        padding: 0.3rem;
        border: 1px solid var(--border);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: var(--radius-sm);
        padding: 0.5rem 1rem;
        font-weight: 500;
        font-size: 0.9rem;
        color: var(--text-secondary);
        transition: var(--transition);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(88,166,255,0.15), rgba(188,140,255,0.1));
        color: var(--accent-blue) !important;
        border-bottom: none !important;
    }

    .stTabs [data-baseweb="tab-highlight"] {
        background-color: transparent !important;
    }

    .stTabs [data-baseweb="tab-border"] {
        display: none;
    }

    /* ═══ Buttons ═══ */
    .stButton > button {
        background: linear-gradient(135deg, #1f6feb, #388bfd);
        color: white;
        border: none;
        border-radius: var(--radius-sm);
        font-weight: 600;
        font-size: 0.9rem;
        padding: 0.5rem 1.5rem;
        transition: var(--transition);
        font-family: 'Inter', sans-serif;
    }

    .stButton > button:hover {
        box-shadow: 0 0 20px rgba(56,139,253,0.4);
        transform: translateY(-1px);
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #238636, #2ea043);
    }

    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 0 20px rgba(46,160,67,0.4);
    }

    /* ═══ Expanders ═══ */
    .streamlit-expanderHeader {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
        font-weight: 500;
    }

    /* ═══ Metric ═══ */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 0.8rem 1rem;
        transition: var(--transition);
    }

    [data-testid="stMetric"]:hover {
        border-color: var(--accent-blue);
        box-shadow: 0 0 15px rgba(88,166,255,0.15);
    }

    [data-testid="stMetricLabel"] {
        color: var(--text-muted) !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    [data-testid="stMetricValue"] {
        color: var(--accent-blue) !important;
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* ═══ Scrollbar ═══ */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: var(--bg-primary);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--bg-tertiary);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--border);
    }

    /* ═══ LaTeX ═══ */
    .katex-display {
        background: rgba(22,27,34,0.5);
        border: 1px solid var(--border-muted);
        border-radius: var(--radius-sm);
        padding: 0.6rem 1rem;
        margin: 0.5rem 0;
    }

    /* ═══ Responsive ═══ */
    @media (max-width: 768px) {
        .page-header-title { font-size: 1.6rem; }
        .stats-container { gap: 0.5rem; }
        .stat-item { min-width: 100px; padding: 0.7rem 1rem; }
        .stat-item .number { font-size: 1.4rem; }
    }
</style>
"""
