"""
pages/report.py — PDF report generation and download page.
"""

import streamlit as st
import streamlit.components.v1 as components
from models.report_gen import generate_pdf_report
from datetime import datetime
from textwrap import dedent


def render():
    st.markdown("""
    <div class="page-header">
        <div class="page-title">PDF Report</div>
        <p class="page-subtitle">
            Generate and download your branded HireLens AI analysis report.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.analysis_done:
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:3rem;">
            <div style="font-size:3rem;margin-bottom:1rem;">📑</div>
            <div style="font-size:1.1rem;font-weight:700;color:var(--text-primary);margin-bottom:0.5rem;">
                No Analysis Found
            </div>
            <div style="color:var(--text-muted);margin-bottom:1.5rem;font-size:0.9rem;">
                Complete an analysis first to generate your PDF report.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔮  Run Analysis First"):
            st.session_state.current_page = "analysis"
            st.rerun()
        return

    # ── Report Preview card ───────────────────────────────
    name    = st.session_state.candidate_name or "Anonymous"
    role    = st.session_state.predicted_role or "–"
    ats     = st.session_state.ats_score or 0
    prob    = st.session_state.hire_probability or 0
    persona = st.session_state.cluster_label or "–"
    skills  = st.session_state.extracted_skills or []
    missing = st.session_state.missing_skills or []
    suggestions = st.session_state.suggestions or []
    nb_m    = st.session_state.get("nb_metrics", {})
    lr_m    = st.session_state.get("lr_metrics", {})
    km_m    = st.session_state.get("km_metrics", {})

    col_preview, col_options = st.columns([1.6, 1])

    with col_preview:
        st.markdown('<div class="section-label">✦ Report Preview</div>', unsafe_allow_html=True)

        # Simulated report preview card
        ats_badge_color = ("var(--success)" if ats >= 75 else ("var(--warning)" if ats >= 50 else "var(--danger)"))
        prob_badge_color = ("var(--success)" if prob >= 0.7 else ("var(--warning)" if prob >= 0.45 else "var(--danger)"))

        report_html = dedent(f"""
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    font-family: 'DM Sans', sans-serif;
                    background: var(--bg-primary);
                    color: var(--text-primary);
                }}

                .report-frame {{
                    max-width: 100%;
                    padding: 0;
                }}

                .glass-card {{
                    background: rgba(84,26,26,0.03);
                    border: 1px solid rgba(84,26,26,0.08);
                    border-radius: 20px;
                    box-shadow: 0 24px 80px rgba(0,0,0,0.3);
                    padding: 2rem;
                    color: var(--text-primary);
                }}

                .glass-card div {{ word-wrap: break-word; }}

                .skill-pill {{
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    margin: 0 0.35rem 0.35rem 0;
                    padding: 0.45rem 0.75rem;
                    border-radius: 999px;
                    background: rgba(129,11,56,0.18);
                    color: var(--bg-primary);
                    font-size: 0.75rem;
                    line-height: 1.2;
                }}

                .skill-missing {{
                    background: rgba(129,11,56,0.18);
                    color: var(--danger);
                }}

                .badge {{
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    padding: 0.35rem 0.65rem;
                    border-radius: 999px;
                    background: rgba(129,11,56,0.16);
                    color: var(--danger);
                    font-size: 0.68rem;
                }}

                .report-header-title {{
                    font-family: 'Syne', sans-serif;
                    font-size: 1.4rem;
                    font-weight: 800;
                    color: var(--accent);
                }}

                .report-subtitle {{
                    font-size: 0.75rem;
                    color: var(--text-muted);
                }}

                .report-label {{
                    font-size: 0.65rem;
                    text-transform: uppercase;
                    letter-spacing: 0.1em;
                    color: var(--text-muted);
                    margin-bottom: 0.4rem;
                }}

                .report-value-large {{
                    font-size: 1.6rem;
                    font-weight: 800;
                    font-family: 'Syne', sans-serif;
                }}
            </style>

            <div class="report-frame">
                <div class="glass-card">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;
                                border-bottom:2px solid rgba(129,11,56,0.3);padding-bottom:1rem;
                                margin-bottom:1.25rem;flex-wrap:wrap;gap:1rem;">
                        <div>
                            <div class="report-header-title">🔮 HireLens AI</div>
                            <div class="report-subtitle">Resume Analysis Report</div>
                        </div>
                        <div style="text-align:right;min-width:140px;">
                            <div class="report-subtitle">{datetime.now().strftime('%B %d, %Y')}</div>
                            <div class="report-subtitle">Confidential</div>
                        </div>
                    </div>

                    <div style="margin-bottom:1.25rem;">
                        <div class="report-label">Candidate</div>
                        <div style="font-size:1.1rem;font-weight:700;color:var(--text-primary);">{name}</div>
                        <div style="font-size:0.85rem;color:var(--text-secondary);">Target Role: {role}</div>
                        <div style="font-size:0.85rem;color:var(--text-secondary);margin-top:0.2rem;">Persona: {persona}</div>
                    </div>

                    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1rem;margin-bottom:1.25rem;">
                        <div style="background:rgba(84,26,26,0.03);border-radius:14px;padding:1rem;border:1px solid rgba(84,26,26,0.07);">
                            <div class="report-label">ATS Score</div>
                            <div class="report-value-large" style="color:{ats_badge_color};">{ats:.1f}%</div>
                        </div>
                        <div style="background:rgba(84,26,26,0.03);border-radius:14px;padding:1rem;border:1px solid rgba(84,26,26,0.07);">
                            <div class="report-label">Hire Probability</div>
                            <div class="report-value-large" style="color:{prob_badge_color};">{prob*100:.1f}%</div>
                        </div>
                    </div>

                    <div style="margin-bottom:1.25rem;">
                        <div class="report-label">Skills Detected ({len(skills)})</div>
                        <div>{''.join(f'<span class="skill-pill">{s}</span>' for s in skills[:12])}
                            {f'<span style="color:var(--text-muted);font-size:0.78rem;"> +{len(skills)-12} more</span>' if len(skills) > 12 else ''}
                        </div>
                    </div>

                    {f'''<div style="margin-bottom:1.25rem;">
                        <div class="report-label" style="color:var(--danger);">Missing Skills</div>
                        <div>{''.join(f'<span class="skill-pill skill-missing">{s}</span>' for s in missing)}</div>
                    </div>''' if missing else ''}

                    <div style="margin-bottom:0.75rem;">
                        <div class="report-label">Top Recommendations ({len(suggestions)})</div>
                        {''.join(f'''<div style="display:flex;gap:8px;margin-bottom:0.75rem;align-items:flex-start;flex-wrap:wrap;">
                            <div style="font-size:0.95rem;line-height:1.1;">{s.get('icon','💡')}</div>
                            <div style="min-width:0;flex:1;">
                                <div style="font-size:0.82rem;font-weight:600;color:var(--text-primary);">{s.get('title','')}</div>
                                <div style="font-size:0.76rem;color:var(--text-muted);line-height:1.5;">{s.get('text','')[:110]}...</div>
                            </div>
                        </div>''' for s in suggestions[:3])}
                    </div>

                    <div style="border-top:1px solid rgba(84,26,26,0.07);padding-top:0.75rem;margin-top:0.75rem;">
                        <div class="report-label">ML Models Applied</div>
                        <div style="display:flex;flex-wrap:wrap;gap:0.5rem;">
                            {''.join(f'<span class="badge">{m}</span>' for m in [
                                'Naive Bayes', 'Logistic Regression', 'K-Means', 'PCA',
                                'Hierarchical Clustering', 'TF-IDF', 'NLP Pipeline'
                            ])}
                        </div>
                    </div>
                </div>
            </div>
        """).strip()
        components.html(report_html, height=850, scrolling=True)

    with col_options:
        st.markdown('<div class="section-label">✦ Report Options</div>', unsafe_allow_html=True)

        # Options
        st.markdown("""
        <div class="glass-card">
            <div style="font-weight:700;color:var(--text-primary);margin-bottom:1rem;">
                📋 What's Included
            </div>
        """, unsafe_allow_html=True)

        sections = [
            ("✅", "Candidate Profile & Scores"),
            ("✅", "ATS Score with Verdict"),
            ("✅", "Hire Probability Breakdown"),
            ("✅", "Detected & Missing Skills"),
            ("✅", "AI Improvement Suggestions"),
            ("✅", "ML Models & Methodology"),
            ("✅", "Candidate Persona"),
        ]
        for icon, label in sections:
            st.markdown(f"""
            <div style="display:flex;gap:8px;align-items:center;margin-bottom:0.5rem;">
                <span style="font-size:0.85rem;">{icon}</span>
                <span style="font-size:0.85rem;color:var(--text-secondary);">{label}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Eval metrics summary
        st.markdown("""
        <div class="glass-card" style="margin-top:1rem;">
            <div style="font-weight:700;color:var(--text-primary);margin-bottom:1rem;">
                🧠 Model Metrics
            </div>
        """, unsafe_allow_html=True)

        model_metrics = [
            ("Naive Bayes Accuracy",    f"{nb_m.get('accuracy','–')}%"),
            ("NB F1 Macro",             f"{nb_m.get('f1_macro','–')}%"),
            ("LR Train Accuracy",       f"{lr_m.get('train_accuracy','–')}%"),
            ("K-Means Clusters",        f"{km_m.get('k','4')}"),
            ("K-Means Inertia",         f"{km_m.get('inertia','–')}"),
        ]
        for label, val in model_metrics:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;
                        margin-bottom:0.5rem;padding-bottom:0.5rem;
                        border-bottom:1px solid rgba(84,26,26,0.05);">
                <span style="font-size:0.82rem;color:var(--text-secondary);">{label}</span>
                <span style="font-size:0.82rem;font-weight:700;color:var(--accent);">{val}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Generate & Download ───────────────────────────────
    st.markdown('<div style="height:1.5rem;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">✦ Generate Report</div>', unsafe_allow_html=True)

    col_gen, col_note = st.columns([1, 2])
    with col_gen:
        if st.button("📥  Generate & Download PDF", use_container_width=True):
            with st.spinner("Generating PDF..."):
                try:
                    pdf_bytes = generate_pdf_report(
                        candidate_name=name,
                        role=role,
                        ats_score=ats,
                        hire_prob=prob,
                        cluster_label=persona,
                        skills=skills,
                        missing_skills=missing,
                        suggestions=suggestions,
                        eval_metrics={**nb_m, **lr_m, **km_m},
                    )

                    filename = f"HireLens_Report_{name.replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.pdf"

                    st.download_button(
                        label="⬇️  Click to Download PDF",
                        data=pdf_bytes,
                        file_name=filename,
                        mime="application/pdf",
                        use_container_width=True,
                    )

                    st.markdown("""
                    <div style="margin-top:0.75rem;padding:0.75rem 1rem;
                                background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.3);
                                border-radius:10px;font-size:0.85rem;color:var(--success);">
                        ✅ Report generated successfully! Click the button above to download.
                    </div>
                    """, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Report generation failed: {e}")
                    st.info("Tip: Run `pip install fpdf2` for full PDF support.")

    with col_note:
        st.markdown("""
        <div style="padding:0.75rem 1rem;background:rgba(129,11,56,0.08);
                    border:1px solid rgba(129,11,56,0.2);border-radius:10px;
                    font-size:0.82rem;color:var(--text-secondary);line-height:1.6;">
            <strong style="color:var(--accent);">ℹ️ Note:</strong>
            The PDF report includes all analysis results.
            Install <code>fpdf2</code> for a fully styled branded PDF.
            Without it, a plain-text fallback is provided.
        </div>
        """, unsafe_allow_html=True)

    # ── Share actions ─────────────────────────────────────
    st.markdown('<div style="height:1rem;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">✦ Next Steps</div>', unsafe_allow_html=True)
    n1, n2, n3 = st.columns(3)
    with n1:
        if st.button("🏠  Back to Home", use_container_width=True):
            st.session_state.current_page = "home"
            st.rerun()
    with n2:
        if st.button("📊  Recruiter View", use_container_width=True):
            st.session_state.current_page = "recruiter"
            st.rerun()
    with n3:
        if st.button("🔄  New Analysis", use_container_width=True):
            st.session_state.resume_text = None
            st.session_state.analysis_done = False
            st.session_state.current_page = "upload"
            st.rerun()
