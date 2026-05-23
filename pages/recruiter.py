"""
pages/recruiter.py — Recruiter dashboard for batch candidate analysis.
Demonstrates K-Means clustering and PCA on a simulated candidate pool.
"""

import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
from utils.charts import pca_scatter, dendrogram_fig
from models.ml_models import cluster_candidates, run_pca


# ── Simulated candidate pool ───────────────────────────────────────────────────
SAMPLE_CANDIDATES = [
    {"name": "Priya Sharma",     "role": "Data Scientist",    "ats": 88, "skills": 18, "words": 620, "prob": 0.91},
    {"name": "Alex Chen",        "role": "ML Engineer",       "ats": 82, "skills": 15, "words": 540, "prob": 0.85},
    {"name": "James Wilson",     "role": "Backend Engineer",  "ats": 74, "skills": 12, "words": 480, "prob": 0.72},
    {"name": "Fatima Al-Rashid", "role": "Data Analyst",      "ats": 68, "skills": 10, "words": 420, "prob": 0.65},
    {"name": "Lucas Santos",     "role": "Frontend Engineer", "ats": 61, "skills": 9,  "words": 380, "prob": 0.58},
    {"name": "Aisha Patel",      "role": "Data Engineer",     "ats": 79, "skills": 14, "words": 510, "prob": 0.78},
    {"name": "Tom Bradley",      "role": "DevOps Engineer",   "ats": 55, "skills": 8,  "words": 350, "prob": 0.48},
    {"name": "Mei Lin",          "role": "Full Stack",        "ats": 71, "skills": 13, "words": 460, "prob": 0.69},
    {"name": "Carlos Mendez",    "role": "Data Scientist",    "ats": 43, "skills": 6,  "words": 280, "prob": 0.35},
    {"name": "Nadia Kowalski",   "role": "ML Engineer",       "ats": 91, "skills": 20, "words": 680, "prob": 0.94},
    {"name": "Raj Patel",        "role": "Backend Engineer",  "ats": 67, "skills": 11, "words": 430, "prob": 0.61},
    {"name": "Sofia Ferrari",    "role": "Data Analyst",      "ats": 58, "skills": 9,  "words": 370, "prob": 0.52},
]


def render():
    st.markdown("""
    <div class="page-header">
        <div class="page-title">Recruiter Dashboard</div>
        <p class="page-subtitle">
            Batch candidate analysis with clustering, ranking, and ML insights.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Top stats ─────────────────────────────────────────
    total     = len(SAMPLE_CANDIDATES)
    avg_ats   = np.mean([c["ats"] for c in SAMPLE_CANDIDATES])
    avg_prob  = np.mean([c["prob"] for c in SAMPLE_CANDIDATES])
    shortlist = sum(1 for c in SAMPLE_CANDIDATES if c["prob"] >= 0.70)

    m1, m2, m3, m4 = st.columns(4)
    for col, val, label in zip(
        [m1, m2, m3, m4],
        [total, f"{avg_ats:.0f}%", f"{avg_prob*100:.0f}%", shortlist],
        ["Total Candidates", "Avg ATS Score", "Avg Hire Prob", "Shortlisted"],
    ):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{val}</div>
                <div class="metric-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div style="height:1.5rem;"></div>', unsafe_allow_html=True)

    # ── Filter bar ────────────────────────────────────────
    st.markdown('<div class="section-label">✦ Filters</div>', unsafe_allow_html=True)
    f1, f2, f3 = st.columns(3)
    with f1:
        min_ats = st.slider("Min ATS Score", 0, 100, 40, key="rec_ats")
    with f2:
        min_prob = st.slider("Min Hire Probability (%)", 0, 100, 30, key="rec_prob")
    with f3:
        roles = ["All"] + sorted(set(c["role"] for c in SAMPLE_CANDIDATES))
        sel_role = st.selectbox("Role Filter", roles, key="rec_role")

    # Filter
    filtered = [
        c for c in SAMPLE_CANDIDATES
        if c["ats"] >= min_ats
        and c["prob"] * 100 >= min_prob
        and (sel_role == "All" or c["role"] == sel_role)
    ]

    st.markdown(f"""
    <div style="font-size:0.82rem;color:var(--text-muted);margin-bottom:1rem;">
        Showing <strong style="color:var(--accent);">{len(filtered)}</strong> of {total} candidates
    </div>
    """, unsafe_allow_html=True)

    # ── Candidate table ───────────────────────────────────
    st.markdown('<div class="section-label">✦ Candidate Rankings</div>', unsafe_allow_html=True)

    # Run clustering on filtered
    if filtered:
        features = [{"ats": c["ats"], "skills": c["skills"],
                     "words": c["words"], "prob": c["prob"],
                     "role_id": 0, "cluster": 0}
                    for c in filtered]
        try:
            cluster_labels, personas, _, _, _ = cluster_candidates(features, n_clusters=min(4, len(filtered)))
        except Exception:
            cluster_labels = [0] * len(filtered)
            personas = ["–"] * len(filtered)
    else:
        cluster_labels, personas = [], []

    # Build display rows
    rows_html = ""
    for i, (c, persona) in enumerate(zip(filtered, personas)):
        prob = c["prob"]
        ats  = c["ats"]
        prob_color = ("var(--success)" if prob >= 0.7 else ("var(--warning)" if prob >= 0.45 else "var(--danger)"))
        ats_color  = ("var(--success)" if ats >= 75 else ("var(--warning)" if ats >= 50 else "var(--danger)"))
        rank_medal = "🥇" if i == 0 else ("🥈" if i == 1 else ("🥉" if i == 2 else f"#{i+1}"))

        rows_html += f"""
        <tr style="border-bottom:1px solid rgba(84,26,26,0.05);">
            <td style="padding:0.75rem 0.5rem;font-weight:700;color:var(--accent);">{rank_medal}</td>
            <td style="padding:0.75rem 0.5rem;font-weight:600;color:var(--text-primary);">{c['name']}</td>
            <td style="padding:0.75rem 0.5rem;color:var(--text-secondary);font-size:0.85rem;">{c['role']}</td>
            <td style="padding:0.75rem 0.5rem;">
                <span style="color:{ats_color};font-weight:700;">{ats}%</span>
            </td>
            <td style="padding:0.75rem 0.5rem;">
                <span style="color:{prob_color};font-weight:700;">{prob*100:.0f}%</span>
            </td>
            <td style="padding:0.75rem 0.5rem;font-size:0.82rem;color:var(--text-secondary);">{persona}</td>
            <td style="padding:0.75rem 0.5rem;">
                <span class="badge {'badge-success' if prob >= 0.7 else ('badge-warning' if prob >= 0.45 else 'badge-danger')}">
                    {'Shortlist' if prob >= 0.7 else ('Review' if prob >= 0.45 else 'Pass')}
                </span>
            </td>
        </tr>
        """

    table_html = f"""
    <div class="glass-card" style="padding:0;overflow:hidden;">
        <table style="width:100%;border-collapse:collapse;font-family:'DM Sans',sans-serif;">
            <thead>
                <tr style="border-bottom:1px solid rgba(84,26,26,0.1);">
                    <th style="padding:0.75rem 0.5rem;text-align:left;font-size:0.72rem;
                               text-transform:uppercase;letter-spacing:0.1em;color:var(--text-muted);">#</th>
                    <th style="padding:0.75rem 0.5rem;text-align:left;font-size:0.72rem;
                               text-transform:uppercase;letter-spacing:0.1em;color:var(--text-muted);">Candidate</th>
                    <th style="padding:0.75rem 0.5rem;text-align:left;font-size:0.72rem;
                               text-transform:uppercase;letter-spacing:0.1em;color:var(--text-muted);">Role</th>
                    <th style="padding:0.75rem 0.5rem;text-align:left;font-size:0.72rem;
                               text-transform:uppercase;letter-spacing:0.1em;color:var(--text-muted);">ATS</th>
                    <th style="padding:0.75rem 0.5rem;text-align:left;font-size:0.72rem;
                               text-transform:uppercase;letter-spacing:0.1em;color:var(--text-muted);">Hire Prob</th>
                    <th style="padding:0.75rem 0.5rem;text-align:left;font-size:0.72rem;
                               text-transform:uppercase;letter-spacing:0.1em;color:var(--text-muted);">Persona</th>
                    <th style="padding:0.75rem 0.5rem;text-align:left;font-size:0.72rem;
                               text-transform:uppercase;letter-spacing:0.1em;color:var(--text-muted);">Decision</th>
                </tr>
            </thead>
            <tbody>{rows_html}</tbody>
        </table>
    </div>
    """
    components.html(table_html, height=400, scrolling=True)

    st.markdown('<div style="height:1.5rem;"></div>', unsafe_allow_html=True)

    # ── Cluster PCA visualization ─────────────────────────
    st.markdown('<div class="section-label">✦ Candidate Cluster Map (PCA)</div>', unsafe_allow_html=True)
    if filtered and len(filtered) >= 2:
        features = [{"ats": c["ats"], "skills": c["skills"],
                     "words": c["words"], "prob": c["prob"],
                     "role_id": 0, "cluster": cl}
                    for c, cl in zip(filtered, cluster_labels)]
        labels = [c["name"].split()[0] for c in filtered]
        pca_data = run_pca(features, labels=labels)
        if pca_data:
            pca_df = pd.DataFrame({
                "PC1": pca_data["PC1"],
                "PC2": pca_data["PC2"],
                "Label": pca_data["Label"],
                "Cluster": [str(c) for c in pca_data["Cluster"]],
            })
            fig = pca_scatter(pca_df)
            if fig:
                st.plotly_chart(fig, use_container_width=True, theme=None, config={"displayModeBar": False})

    # ── Dendrogram ────────────────────────────────────────
    st.markdown('<div class="section-label">✦ Hierarchical Clustering</div>', unsafe_allow_html=True)
    dend_labels = [c["name"].split()[0] for c in filtered[:10]]
    if len(dend_labels) >= 2:
        dend_fig = dendrogram_fig(dend_labels)
        if dend_fig:
            st.plotly_chart(dend_fig, use_container_width=True, theme=None, config={"displayModeBar": False})

    # ── Shortlist section ─────────────────────────────────
    shortlisted = [c for c in filtered if c["prob"] >= 0.70]
    if shortlisted:
        st.markdown('<div class="section-label">✦ Recommended Shortlist</div>', unsafe_allow_html=True)
        cols = st.columns(min(len(shortlisted), 3))
        for col, c in zip(cols, shortlisted[:3]):
            with col:
                st.markdown(f"""
                <div class="glass-card" style="border-color:rgba(16,185,129,0.25);">
                    <div style="font-size:1.5rem;margin-bottom:0.5rem;">👤</div>
                    <div style="font-weight:700;color:var(--text-primary);">{c['name']}</div>
                    <div style="font-size:0.82rem;color:var(--text-muted);margin-bottom:0.75rem;">{c['role']}</div>
                    <div style="display:flex;gap:1rem;">
                        <div>
                            <div style="font-weight:700;color:var(--success);">{c['ats']}%</div>
                            <div style="font-size:0.68rem;color:var(--text-muted);text-transform:uppercase;">ATS</div>
                        </div>
                        <div>
                            <div style="font-weight:700;color:var(--success);">{c['prob']*100:.0f}%</div>
                            <div style="font-size:0.68rem;color:var(--text-muted);text-transform:uppercase;">Hire</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
