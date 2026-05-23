"""
pages/candidate.py — Candidate personal dashboard.
Shows personalized results, score breakdown, and action plan.
"""

import streamlit as st
from utils.charts import ats_gauge, hire_probability_gauge, skill_radar


def render():
    st.markdown("""
    <div class="page-header">
        <div class="page-title">Your Dashboard</div>
        <p class="page-subtitle">Personalized insights and your path to the next offer.</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.analysis_done:
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:3rem;">
            <div style="font-size:3rem;margin-bottom:1rem;">👤</div>
            <div style="font-size:1.1rem;font-weight:700;color:var(--text-primary);margin-bottom:0.5rem;">
                No Analysis Yet
            </div>
            <div style="color:var(--text-muted);margin-bottom:1.5rem;font-size:0.9rem;">
                Upload your resume and run analysis to see your personalized dashboard.
            </div>
        </div>
        """, unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬆️  Upload Resume"):
                st.session_state.current_page = "upload"
                st.rerun()
        with col2:
            if st.button("🔮  Run Analysis"):
                st.session_state.current_page = "analysis"
                st.rerun()
        return

    name    = st.session_state.candidate_name or "Candidate"
    role    = st.session_state.predicted_role or "–"
    ats     = st.session_state.ats_score or 0
    prob    = st.session_state.hire_probability or 0
    persona = st.session_state.cluster_label or "–"
    skills  = st.session_state.extracted_skills or []
    missing = st.session_state.missing_skills or []
    suggestions = st.session_state.suggestions or []

    # ── Profile card ──────────────────────────────────────
    overall = round((ats + prob * 100) / 2)
    grade = "A+" if overall >= 85 else ("A" if overall >= 75 else ("B" if overall >= 60 else ("C" if overall >= 45 else "D")))

    st.markdown(f"""
    <div class="glass-card" style="display:flex;gap:2rem;align-items:center;
                                    margin-bottom:1.5rem;flex-wrap:wrap;">
        <div style="min-width:80px;height:80px;border-radius:50%;
                    background:linear-gradient(135deg,var(--accent),var(--danger));
                    display:flex;align-items:center;justify-content:center;
                    font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:#fff;">
            {name[0].upper() if name else 'U'}
        </div>
        <div style="flex:1;">
            <div style="font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:800;
                        color:var(--text-primary);margin-bottom:0.25rem;">{name}</div>
            <div style="font-size:0.9rem;color:var(--text-secondary);margin-bottom:0.5rem;">
                Targeting: <strong style="color:var(--accent);">{role}</strong>
            </div>
            <span class="badge badge-accent">{persona}</span>
        </div>
        <div style="text-align:center;">
            <div style="font-family:'Syne',sans-serif;font-size:3rem;font-weight:800;
                        background:linear-gradient(135deg,var(--accent),var(--accent));
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                        line-height:1;">{grade}</div>
            <div style="font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;
                        letter-spacing:0.1em;margin-top:0.25rem;">Overall Grade</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Score gauges ──────────────────────────────────────
    st.markdown('<div class="section-label">✦ Score Breakdown</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<div style='text-align:center;font-size:0.78rem;color:var(--text-muted);margin-bottom:0;'>ATS Score</div>", unsafe_allow_html=True)
        fig_ats = ats_gauge(ats)
        if fig_ats:
            st.plotly_chart(fig_ats, use_container_width=True, theme=None, config={"displayModeBar": False})
    with col_b:
        st.markdown("<div style='text-align:center;font-size:0.78rem;color:var(--text-muted);margin-bottom:0;'>Hire Probability</div>", unsafe_allow_html=True)
        fig_hire = hire_probability_gauge(prob)
        if fig_hire:
            st.plotly_chart(fig_hire, use_container_width=True, theme=None, config={"displayModeBar": False})

    # ── Progress bars ─────────────────────────────────────
    st.markdown('<div class="section-label">✦ Performance Metrics</div>', unsafe_allow_html=True)
    metrics = [
        ("ATS Score",        ats,          "How well your resume matches job descriptions"),
        ("Hire Probability",  prob * 100,   "Logistic Regression hiring likelihood"),
        ("Skill Coverage",    min(100, len(skills) * 5.5), "Skills detected vs typical requirements"),
    ]
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    for label, val, tip in metrics:
        color = ("var(--success)" if val >= 75 else ("var(--warning)" if val >= 50 else "var(--danger)"))
        st.markdown(f"""
        <div style="margin-bottom:1rem;">
            <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
                <div>
                    <span style="font-weight:600;font-size:0.9rem;color:var(--text-primary);">{label}</span>
                    <span style="font-size:0.78rem;color:var(--text-muted);margin-left:8px;">{tip}</span>
                </div>
                <span style="font-weight:700;color:{color};">{val:.0f}%</span>
            </div>
            <div class="custom-progress">
                <div class="custom-progress-fill"
                     style="width:{min(val,100):.0f}%;background:linear-gradient(90deg,{color},{color}88);">
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Skills radar ──────────────────────────────────────
    st.markdown('<div class="section-label" style="margin-top:1rem;">✦ Skill Map</div>', unsafe_allow_html=True)
    radar_fig = skill_radar(skills, missing, role)
    st.plotly_chart(radar_fig, use_container_width=True, theme=None, config={"displayModeBar": False})

    # ── Action plan ───────────────────────────────────────
    st.markdown('<div class="section-label">✦ Your Action Plan</div>', unsafe_allow_html=True)
    if suggestions:
        priority_items = [s for s in suggestions if s.get("priority") == 1][:3]
        other_items    = [s for s in suggestions if s.get("priority") != 1][:3]

        if priority_items:
            st.markdown("""
            <div style="font-size:0.8rem;font-weight:700;color:var(--danger);margin-bottom:0.75rem;">
                🔴 High Priority Actions
            </div>
            """, unsafe_allow_html=True)
            for s in priority_items:
                st.markdown(f"""
                <div class="suggestion-item">
                    <div class="suggestion-icon">{s.get('icon','💡')}</div>
                    <div>
                        <div class="suggestion-title">{s.get('title','')}</div>
                        <div class="suggestion-text">{s.get('text','')}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        if other_items:
            st.markdown("""
            <div style="font-size:0.8rem;font-weight:700;color:var(--warning);
                        margin-top:1rem;margin-bottom:0.75rem;">
                🟡 Additional Improvements
            </div>
            """, unsafe_allow_html=True)
            for s in other_items:
                st.markdown(f"""
                <div class="suggestion-item">
                    <div class="suggestion-icon">{s.get('icon','💡')}</div>
                    <div>
                        <div class="suggestion-title">{s.get('title','')}</div>
                        <div class="suggestion-text">{s.get('text','')}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── CTA ───────────────────────────────────────────────
    st.markdown('<div style="height:1rem;"></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📑  Download PDF Report", use_container_width=True):
            st.session_state.current_page = "report"
            st.rerun()
    with c2:
        if st.button("🔄  Re-analyze Resume", use_container_width=True):
            st.session_state.analysis_done = False
            st.session_state.current_page = "analysis"
            st.rerun()
