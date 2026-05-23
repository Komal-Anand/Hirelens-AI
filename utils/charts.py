"""
utils/charts.py — Plotly chart helpers with HireLens dark theme.
Gracefully degrades when Plotly is unavailable.
"""

import streamlit as st
import numpy as np

try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

def get_colors():
    return {
        "ACCENT": "#810B38",
        "ACCENT_LIGHT": "#A21A4F",
        "ACCENT_CYAN": "#DCC3AA",
        "ACCENT_MINT": "#F1E2D1",
        "BG": "rgba(0,0,0,0)",
        "GRID_COLOR": "rgba(44,13,13,0.06)",
        "TEXT_COLOR": "rgba(44,13,13,0.7)",
        "TITLE_COLOR": "#2C0D0D",
        "SUCCESS": "#2F7D55",
        "WARNING": "#A76516",
        "DANGER": "#A21A4F",
        "LEGEND_BG": "rgba(241,226,209,0.68)",
        "LEGEND_BORDER": "rgba(44,13,13,0.12)",
        "AXIS_LINE": "rgba(44,13,13,0.15)",
        "GAUGE_BG": "rgba(241,226,209,0.68)",
        "GAUGE_BORDER": "rgba(44,13,13,0.12)",
        "RADAR_FILL_REQ": "rgba(129,11,56,0.15)",
        "RADAR_FILL_HAVE": "rgba(47,125,85,0.15)",
        "BAR_BG": "rgba(129,11,56,0.24)",
        "STEP_DANGER": "rgba(162,26,79,0.15)",
        "STEP_WARN": "rgba(167,101,22,0.15)",
        "STEP_SUCCESS": "rgba(47,125,85,0.15)",
        "PCA_LABEL": "rgba(44,13,13,0.88)",
        "CLUSTER_2": "#A21A4F",
        "CLUSTER_6": "#810B38",
    }

def _get_layout_base():
    c = get_colors()
    return dict(
        paper_bgcolor=c["BG"],
        plot_bgcolor=c["BG"],
        font=dict(family="DM Sans, sans-serif", color=c["TEXT_COLOR"], size=12),
        legend=dict(
            bgcolor=c["LEGEND_BG"],
            bordercolor=c["LEGEND_BORDER"],
            borderwidth=1,
            font=dict(size=11),
        ),
    )

def _apply_base(fig):
    c = get_colors()
    fig.update_layout(**_get_layout_base())
    fig.update_xaxes(
        showgrid=True, gridcolor=c["GRID_COLOR"],
        zeroline=False, tickfont=dict(color=c["TEXT_COLOR"]),
        linecolor=c["AXIS_LINE"]
    )
    fig.update_yaxes(
        showgrid=True, gridcolor=c["GRID_COLOR"],
        zeroline=False, tickfont=dict(color=c["TEXT_COLOR"]),
        linecolor=c["AXIS_LINE"]
    )
    return fig


def _stub_fig(title="Chart unavailable"):
    """Return minimal empty figure when plotly unavailable."""
    if not PLOTLY_AVAILABLE:
        return None
    fig = go.Figure()
    fig.update_layout(**_get_layout_base(), title=title, height=200)
    return fig


def role_confidence_bar(role_scores: dict):
    if not PLOTLY_AVAILABLE or not role_scores:
        return _stub_fig("Role Confidence")
    c = get_colors()
    roles  = list(role_scores.keys())
    scores = [role_scores[r] * 100 for r in roles]
    colors = [c["ACCENT"] if s == max(scores) else c["BAR_BG"] for s in scores]
    fig = go.Figure(go.Bar(
        x=scores, y=roles, orientation="h",
        marker=dict(color=colors, line=dict(width=0), cornerradius=6),
        text=[f"{s:.1f}%" for s in scores],
        textposition="outside",
        textfont=dict(color=c["TEXT_COLOR"], size=11),
    ))
    fig = _apply_base(fig)
    fig.update_layout(
        title=dict(text="Role Match Confidence", font=dict(size=14, color=c["TITLE_COLOR"])),
        xaxis=dict(showgrid=False, showticklabels=False, range=[0, max(scores)*1.25]),
        yaxis=dict(showgrid=False, categoryorder="total ascending"),
        showlegend=False, height=280,
    )
    return fig


def ats_gauge(score: float):
    if not PLOTLY_AVAILABLE:
        return None
    c = get_colors()
    bar_color = c["SUCCESS"] if score >= 75 else (c["WARNING"] if score >= 50 else c["DANGER"])
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number=dict(suffix="%", font=dict(size=36, color=c["TITLE_COLOR"], family="Syne, sans-serif")),
        gauge=dict(
            axis=dict(range=[0, 100], tickcolor=c["TEXT_COLOR"],
                      tickfont=dict(size=10, color=c["TEXT_COLOR"]), nticks=6),
            bar=dict(color=bar_color, thickness=0.35),
            bgcolor=c["GAUGE_BG"],
            bordercolor=c["GAUGE_BORDER"], borderwidth=1,
            steps=[
                dict(range=[0, 50],  color=c["STEP_DANGER"]),
                dict(range=[50, 75], color=c["STEP_WARN"]),
                dict(range=[75, 100],color=c["STEP_SUCCESS"]),
            ],
            threshold=dict(line=dict(color=bar_color, width=3),
                           thickness=0.85, value=score),
        ),
    ))
    fig = _apply_base(fig)
    fig.update_layout(height=220, margin=dict(l=30, r=30, t=30, b=10))
    return fig


def hire_probability_gauge(prob: float):
    if not PLOTLY_AVAILABLE:
        return None
    c = get_colors()
    color = c["SUCCESS"] if prob >= 0.7 else (c["WARNING"] if prob >= 0.45 else c["DANGER"])
    pct = round(prob * 100, 1)
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=pct,
        delta=dict(reference=60, valueformat=".1f",
                   increasing=dict(color=c["SUCCESS"]),
                   decreasing=dict(color=c["DANGER"])),
        number=dict(suffix="%", font=dict(size=34, color=c["TITLE_COLOR"], family="Syne, sans-serif")),
        gauge=dict(
            axis=dict(range=[0, 100], tickfont=dict(color=c["TEXT_COLOR"], size=10)),
            bar=dict(color=color, thickness=0.3),
            bgcolor=c["GAUGE_BG"],
            bordercolor=c["GAUGE_BORDER"], borderwidth=1,
            steps=[
                dict(range=[0, 45],  color=c["STEP_DANGER"]),
                dict(range=[45, 70], color=c["STEP_WARN"]),
                dict(range=[70, 100],color=c["STEP_SUCCESS"]),
            ],
        ),
    ))
    fig = _apply_base(fig)
    fig.update_layout(height=210, margin=dict(l=30, r=30, t=20, b=10))
    return fig


def pca_scatter(pca_df):
    if not PLOTLY_AVAILABLE:
        return None
    c = get_colors()
    palette = [c["ACCENT"], c["CLUSTER_2"], c["ACCENT_MINT"], c["WARNING"], c["DANGER"], c["CLUSTER_6"], c["ACCENT_CYAN"]]
    clusters = pca_df["Cluster"].unique()
    fig = go.Figure()
    for i, cl in enumerate(sorted(clusters)):
        mask   = pca_df["Cluster"] == cl
        subset = pca_df[mask]
        sizes  = [16 if lbl == "YOU" else 10 for lbl in subset["Label"]]
        fig.add_trace(go.Scatter(
            x=subset["PC1"], y=subset["PC2"],
            mode="markers",
            name=f"Cluster {cl}",
            marker=dict(
                size=sizes,
                color=palette[i % len(palette)],
                opacity=0.85,
                line=dict(width=1, color=c["PCA_LABEL"]),
            ),
            text=subset["Label"],
            hovertemplate="<b>%{text}</b><br>PC1: %{x:.2f}<br>PC2: %{y:.2f}<extra></extra>",
        ))
    fig = _apply_base(fig)
    fig.update_layout(
        title=dict(text="PCA — Candidate Grouping", font=dict(size=14, color=c["TITLE_COLOR"])),
        xaxis_title="Principal Component 1",
        yaxis_title="Principal Component 2",
        height=380,
    )
    return fig


def dendrogram_fig(labels: list):
    if not PLOTLY_AVAILABLE:
        return None
    c = get_colors()
    try:
        from scipy.cluster.hierarchy import linkage, dendrogram as scipy_dend
    except ImportError:
        fig = go.Figure()
        fig.update_layout(**_get_layout_base(), title="Dendrogram (scipy required)", height=300)
        return fig

    np.random.seed(42)
    n = max(len(labels), 2)
    X = np.random.randn(n, 5)
    Z = linkage(X, method="ward")
    dend = scipy_dend(Z, labels=labels, no_plot=True)

    fig = go.Figure()
    for xs, ys in zip(dend["icoord"], dend["dcoord"]):
        fig.add_trace(go.Scatter(
            x=xs, y=ys, mode="lines",
            line=dict(color=c["ACCENT"], width=1.5),
            showlegend=False, hoverinfo="skip",
        ))

    fig = _apply_base(fig)
    n_pts = len(labels)
    tick_x = [10 * (i + 0.5) for i in range(n_pts)]
    fig.update_layout(
        title=dict(text="Hierarchical Clustering — Ward Linkage",
                   font=dict(size=14, color=c["TITLE_COLOR"])),
        xaxis=dict(
            tickvals=[5 + 10*i for i in range(n_pts)],
            ticktext=labels,
            tickangle=-30,
            showgrid=False, tickfont=dict(size=9),
        ),
        yaxis=dict(title="Distance", showgrid=True, gridcolor=c["GRID_COLOR"]),
        height=350, showlegend=False,
    )
    return fig


def skill_radar(present: list, missing: list, role: str):
    if not PLOTLY_AVAILABLE:
        return None
    c = get_colors()
    from utils.nlp_utils import ROLE_REQUIRED_SKILLS
    required = ROLE_REQUIRED_SKILLS.get(role, present[:6])[:8]
    if not required:
        required = present[:6]
    present_set = {s.lower() for s in present}
    values_have = [1 if s.lower() in present_set else 0 for s in required]
    values_need = [1 for _ in required]
    categories  = required + [required[0]]
    values_have = values_have + [values_have[0]]
    values_need = values_need + [values_need[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_need, theta=categories, fill="toself", name="Required",
        fillcolor=c["RADAR_FILL_REQ"], line=dict(color=c["ACCENT"], width=2, dash="dot"),
    ))
    fig.add_trace(go.Scatterpolar(
        r=values_have, theta=categories, fill="toself", name="You Have",
        fillcolor=c["RADAR_FILL_HAVE"], line=dict(color=c["SUCCESS"], width=2),
    ))
    fig.update_layout(
        **_get_layout_base(),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=False, range=[0,1], showticklabels=False,
                            showline=False, showgrid=False),
            angularaxis=dict(tickfont=dict(size=10, color=c["TEXT_COLOR"]),
                             linecolor=c["GRID_COLOR"], gridcolor=c["GRID_COLOR"]),
        ),
        title=dict(text=f"Skill Coverage — {role}", font=dict(size=14, color=c["TITLE_COLOR"])),
        height=340,
    )
    return fig


def keyword_frequency_bar(keyword_counts: list):
    if not PLOTLY_AVAILABLE or not keyword_counts:
        return None
    c = get_colors()
    words  = [kw[0] for kw in keyword_counts[:15]]
    counts = [kw[1] for kw in keyword_counts[:15]]
    fig = go.Figure(go.Bar(
        x=counts, y=words, orientation="h",
        marker=dict(
            color=counts,
            colorscale=[[0, c["BAR_BG"]], [0.55, c["ACCENT_LIGHT"]], [1, c["CLUSTER_2"]]],
            showscale=False, cornerradius=5,
        ),
        text=counts, textposition="outside",
        textfont=dict(color=c["TEXT_COLOR"], size=10),
    ))
    fig = _apply_base(fig)
    fig.update_layout(
        title=dict(text="Top Resume Keywords", font=dict(size=14, color=c["TITLE_COLOR"])),
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False, autorange="reversed"),
        height=320, showlegend=False,
    )
    return fig
