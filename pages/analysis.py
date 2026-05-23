"""
pages/analysis.py — Core AI analysis dashboard.
Runs all ML models and displays results in a premium layout.
"""

import streamlit as st
import numpy as np
from utils.nlp_utils import (
    tokenize_and_lemmatize, extract_skills, compute_missing_skills,
    compute_tfidf_ats, get_top_keywords
)
from utils.pdf_utils import get_word_count
from models.ml_models import (
    classify_resume, predict_hire_probability,
    cluster_candidates, run_pca
)
from models.suggestions import generate_suggestions
from utils.charts import (
    role_confidence_bar, ats_gauge, hire_probability_gauge,
    pca_scatter, dendrogram_fig, skill_radar, keyword_frequency_bar
)
import pandas as pd


def _run_analysis():
    """Execute full ML pipeline and persist results to session state."""
    text = st.session_state.resume_text
    jd   = st.session_state.get("job_description", "")

    # 1. NLP Preprocessing
    tokens = tokenize_and_lemmatize(text)
    st.session_state.preprocessed_tokens = tokens

    # 2. Skill Extraction
    skills = extract_skills(text)
    st.session_state.extracted_skills = skills

    # 3. Naive Bayes Classification
    role, role_probs, nb_metrics = classify_resume(text)
    st.session_state.predicted_role = role
    st.session_state.role_confidence = role_probs
    st.session_state.nb_metrics = nb_metrics

    # 4. Missing Skills
    missing = compute_missing_skills(skills, role)
    st.session_state.missing_skills = missing

    # 5. ATS Score
    ats = compute_tfidf_ats(text, jd)
    st.session_state.ats_score = ats

    # 6. Logistic Regression — Hire Probability
    wc = get_word_count(text)
    hire_prob, feat_imp, lr_metrics = predict_hire_probability(
        text, ats, len(skills), wc, role
    )
    st.session_state.hire_probability = hire_prob
    st.session_state.feat_importance = feat_imp
    st.session_state.lr_metrics = lr_metrics

    # 7. K-Means Clustering (simulate candidate pool)
    np.random.seed(42)
    n_pool = 19
    pool_features = [
        {
            "ats":     float(np.clip(np.random.normal(ats, 18), 10, 100)),
            "skills":  int(np.clip(np.random.normal(len(skills), 4), 1, 25)),
            "words":   int(np.clip(np.random.normal(wc, 200), 80, 1500)),
            "prob":    float(np.clip(np.random.normal(hire_prob, 0.15), 0.05, 0.98)),
            "role_id": 0,
            "cluster": 0,
        }
        for _ in range(n_pool)
    ]
    # Insert current candidate
    current_feat = {"ats": ats, "skills": len(skills), "words": wc,
                    "prob": hire_prob, "role_id": 0, "cluster": 0}
    all_features = pool_features + [current_feat]
    labels_pool  = [f"C{i+1:02d}" for i in range(n_pool)] + ["YOU"]

    cluster_labels, personas, kmeans, scaler, km_metrics = cluster_candidates(all_features)

    my_cluster = cluster_labels[-1]
    my_persona = personas[-1]
    st.session_state.candidate_cluster = my_cluster
    st.session_state.cluster_label = my_persona
    st.session_state.km_metrics = km_metrics

    # Update features with cluster info
    for i, feat in enumerate(all_features):
        feat["cluster"] = cluster_labels[i]

    # 8. PCA
    pca_result = run_pca(all_features, labels=labels_pool)
    st.session_state.pca_data = pca_result

    # 9. Keyword frequency
    kw = get_top_keywords(text, 15)
    st.session_state.top_keywords = kw

    # 10. AI Suggestions
    suggestions = generate_suggestions(
        resume_text=text,
        ats_score=ats,
        hire_prob=hire_prob,
        role=role,
        missing_skills=missing,
        word_count=wc,
        skill_count=len(skills),
    )
    st.session_state.suggestions = suggestions

    # Pool data for dendrogram
    st.session_state.pool_labels = labels_pool
    st.session_state.analysis_done = True


def render():
    if not st.session_state.resume_text:
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:3rem;">
            <div style="font-size:3rem;margin-bottom:1rem;">📄</div>
            <div style="font-size:1.2rem;font-weight:700;color:var(--text-primary);margin-bottom:0.5rem;">
                No Resume Loaded
            </div>
            <div style="color:var(--text-muted);margin-bottom:1.5rem;">
                Upload a resume first to run analysis.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⬆️  Go to Upload"):
            st.session_state.current_page = "upload"
            st.rerun()
        return

    # Run analysis if needed
    if not st.session_state.analysis_done:
        with st.spinner(""):
            st.markdown("""
            <div style="text-align:center;padding:2rem;">
                <div style="font-size:1rem;color:var(--text-secondary);margin-bottom:0.5rem;">
                    🔮 Running ML Pipeline…
                </div>
                <div style="font-size:0.82rem;color:var(--text-muted);">
                    NLP → Classification → Scoring → Clustering → PCA
                </div>
            </div>
            """, unsafe_allow_html=True)
            _run_analysis()
        st.rerun()

    # ── Page header ───────────────────────────────────────
    st.markdown(f"""
    <div class="page-header">
        <div class="page-title">AI Analysis</div>
        <p class="page-subtitle">
            Full ML analysis for
            <strong style="color:var(--accent);">{st.session_state.candidate_name or 'your resume'}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Top KPI row ───────────────────────────────────────
    k1, k2, k3, k4, k5 = st.columns(5)
    role = st.session_state.predicted_role
    ats  = st.session_state.ats_score
    prob = st.session_state.hire_probability
    persona = st.session_state.cluster_label or "–"
    skills_count = len(st.session_state.extracted_skills)

    ats_badge = ("badge-success" if ats >= 75 else ("badge-warning" if ats >= 50 else "badge-danger"))
    prob_badge = ("badge-success" if prob >= 0.7 else ("badge-warning" if prob >= 0.45 else "badge-danger"))

    with k1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{ats:.0f}%</div>
            <div class="metric-label">ATS Score</div>
        </div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{prob*100:.0f}%</div>
            <div class="metric-label">Hire Probability</div>
        </div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="font-size:1.2rem;">{role.split()[0]}</div>
            <div class="metric-label">Predicted Role</div>
        </div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{skills_count}</div>
            <div class="metric-label">Skills Found</div>
        </div>""", unsafe_allow_html=True)
    with k5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="font-size:1rem;">{persona.split()[-1] if persona != '–' else '–'}</div>
            <div class="metric-label">Persona</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div style="height:1.5rem;"></div>', unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────────
    tabs = st.tabs(["🧠 Classification", "📊 ATS & Hiring", "🔮 Clustering", "📐 PCA", "💡 Suggestions"])

    # ── Tab 1: Classification ─────────────────────────────
    with tabs[0]:
        col_chart, col_info = st.columns([1.4, 1])
        with col_chart:
            st.markdown('<div class="section-label">✦ Naive Bayes Role Confidence</div>', unsafe_allow_html=True)
            fig_role = role_confidence_bar(st.session_state.role_confidence)
            if fig_role:
                st.plotly_chart(fig_role, use_container_width=True, theme=None, config={"displayModeBar": False})

        with col_info:
            st.markdown('<div class="section-label">✦ Classification Result</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="glass-card">
                <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;
                            color:var(--text-muted);margin-bottom:0.5rem;">Predicted Role</div>
                <div style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;
                            color:var(--accent);margin-bottom:1rem;">{role}</div>
                <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;
                            color:var(--text-muted);margin-bottom:0.5rem;">Confidence</div>
                <div style="font-size:1.2rem;font-weight:700;color:var(--text-primary);margin-bottom:1rem;">
                    {st.session_state.role_confidence.get(role, 0)*100:.1f}%
                </div>
                <hr style="border-color:rgba(84,26,26,0.07);margin:0.75rem 0;">
                <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;
                            color:var(--text-muted);margin-bottom:0.5rem;">Model</div>
                <div style="font-size:0.88rem;color:var(--text-secondary);">Multinomial Naive Bayes</div>
                <div style="font-size:0.78rem;color:var(--text-muted);margin-top:0.25rem;">
                    TF-IDF (1,2)-gram features · {st.session_state.nb_metrics.get('classes',8)} classes
                </div>
            </div>
            """, unsafe_allow_html=True)

            nb = st.session_state.nb_metrics
            st.markdown(f"""
            <div class="glass-card" style="margin-top:1rem;">
                <div class="section-label" style="margin-bottom:0.75rem;">✦ Model Metrics</div>
                <div style="display:flex;gap:2rem;">
                    <div>
                        <div style="font-size:1.3rem;font-weight:800;color:var(--success);font-family:'Syne',sans-serif;">
                            {nb.get('accuracy','–')}%
                        </div>
                        <div style="font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.08em;">Accuracy</div>
                    </div>
                    <div>
                        <div style="font-size:1.3rem;font-weight:800;color:var(--danger);font-family:'Syne',sans-serif;">
                            {nb.get('f1_macro','–')}%
                        </div>
                        <div style="font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.08em;">F1 Macro</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # NLP Tokens preview
        st.markdown('<div class="section-label" style="margin-top:1.5rem;">✦ NLP Preprocessed Tokens</div>', unsafe_allow_html=True)
        tokens = st.session_state.preprocessed_tokens[:40]
        token_pills = "".join(f'<code style="margin:2px;display:inline-block;">{t}</code>' for t in tokens)
        st.markdown(f'<div style="line-height:2;">{token_pills}</div>', unsafe_allow_html=True)

        # Keyword frequency
        st.markdown('<div class="section-label" style="margin-top:1.5rem;">✦ Top Keywords</div>', unsafe_allow_html=True)
        kw_fig = keyword_frequency_bar(st.session_state.get("top_keywords", []))
        st.plotly_chart(kw_fig, use_container_width=True, theme=None, config={"displayModeBar": False})

    # ── Tab 2: ATS & Hiring ───────────────────────────────
    with tabs[1]:
        col_ats, col_hire = st.columns(2)

        with col_ats:
            st.markdown('<div class="section-label">✦ ATS Score</div>', unsafe_allow_html=True)
            ats_fig = ats_gauge(ats)
            if ats_fig:
                st.plotly_chart(ats_fig, use_container_width=True, theme=None, config={"displayModeBar": False})
            ats_verdict = ("🟢 Strong Match" if ats >= 75 else ("🟡 Moderate Match" if ats >= 50 else "🔴 Low Match"))
            ats_tip = ("JD keywords are well-reflected in your resume." if ats >= 75
                       else ("Add more JD-specific keywords and phrases." if ats >= 50
                             else "Significantly rework your resume to match the JD."))
            st.markdown(f"""
            <div class="glass-card">
                <div style="font-weight:700;font-size:0.95rem;margin-bottom:0.35rem;">{ats_verdict}</div>
                <div style="font-size:0.84rem;color:var(--text-secondary);">{ats_tip}</div>
                <div style="margin-top:0.75rem;font-size:0.72rem;color:var(--text-muted);">
                    Method: TF-IDF Cosine Similarity · NLTK tokenizer
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_hire:
            st.markdown('<div class="section-label">✦ Hire Probability</div>', unsafe_allow_html=True)
            hire_fig = hire_probability_gauge(prob)
            if hire_fig:
                st.plotly_chart(hire_fig, use_container_width=True, theme=None, config={"displayModeBar": False})
            hire_verdict = ("🟢 Highly Recommended" if prob >= 0.7
                            else ("🟡 Consider" if prob >= 0.45 else "🔴 Needs Improvement"))
            st.markdown(f"""
            <div class="glass-card">
                <div style="font-weight:700;font-size:0.95rem;margin-bottom:0.75rem;">{hire_verdict}</div>
                <div class="section-label" style="margin-bottom:0.5rem;">Feature Importance</div>
            """, unsafe_allow_html=True)
            feat_imp = st.session_state.get("feat_importance", {})
            for feat, imp in sorted(feat_imp.items(), key=lambda x: -x[1]):
                pct = min(100, imp)
                st.markdown(f"""
                <div style="margin-bottom:0.5rem;">
                    <div style="display:flex;justify-content:space-between;
                                font-size:0.8rem;color:var(--text-secondary);margin-bottom:3px;">
                        <span>{feat}</span><span>{pct:.1f}</span>
                    </div>
                    <div class="custom-progress">
                        <div class="custom-progress-fill" style="width:{min(pct,100)}%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            lr_m = st.session_state.get("lr_metrics", {})
            st.markdown(f"""
                <div style="margin-top:0.5rem;font-size:0.72rem;color:var(--text-muted);">
                    {lr_m.get('model','Logistic Regression')} ·
                    {lr_m.get('regularization','L2')} ·
                    Train acc: {lr_m.get('train_accuracy','–')}%
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Skills section
        st.markdown('<div class="section-label" style="margin-top:1.5rem;">✦ Skill Analysis</div>', unsafe_allow_html=True)
        s1, s2 = st.columns(2)
        with s1:
            st.markdown("""
            <div class="glass-card">
                <div style="font-weight:700;color:var(--success);margin-bottom:0.75rem;">
                    ✅ Skills Detected
                </div>
            """, unsafe_allow_html=True)
            detected = st.session_state.extracted_skills
            if detected:
                pills = "".join(f'<span class="skill-pill skill-present">{s}</span>' for s in detected)
                st.markdown(f'<div>{pills}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="color:var(--text-muted);font-size:0.85rem;">No skills detected.</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with s2:
            st.markdown("""
            <div class="glass-card">
                <div style="font-weight:700;color:var(--danger);margin-bottom:0.75rem;">
                    ❌ Missing Skills for Role
                </div>
            """, unsafe_allow_html=True)
            missing = st.session_state.missing_skills
            if missing:
                pills = "".join(f'<span class="skill-pill skill-missing">{s}</span>' for s in missing)
                st.markdown(f'<div>{pills}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="color:var(--success);font-size:0.85rem;">All key skills present! 🎉</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Skill radar
        st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)
        radar_fig = skill_radar(detected, missing, role)
        st.plotly_chart(radar_fig, use_container_width=True, theme=None, config={"displayModeBar": False})

    # ── Tab 3: Clustering ─────────────────────────────────
    with tabs[2]:
        c1, c2 = st.columns([1, 1.5])

        with c1:
            st.markdown('<div class="section-label">✦ Candidate Persona</div>', unsafe_allow_html=True)
            persona = st.session_state.cluster_label or "–"
            cluster_id = st.session_state.candidate_cluster
            km = st.session_state.get("km_metrics", {})
            st.markdown(f"""
            <div class="glass-card pulse-glow" style="text-align:center;padding:2rem;">
                <div style="font-size:3rem;margin-bottom:0.75rem;">{persona.split()[0] if persona != '–' else '🔮'}</div>
                <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:800;
                            color:var(--accent);margin-bottom:0.5rem;">{persona}</div>
                <div style="font-size:0.8rem;color:var(--text-muted);">Cluster {cluster_id}</div>
                <hr style="border-color:rgba(84,26,26,0.07);margin:1rem 0;">
                <div style="display:flex;justify-content:space-around;">
                    <div>
                        <div style="font-size:1rem;font-weight:700;color:var(--text-primary);">{km.get('k',4)}</div>
                        <div style="font-size:0.7rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.08em;">Clusters</div>
                    </div>
                    <div>
                        <div style="font-size:1rem;font-weight:700;color:var(--text-primary);">20</div>
                        <div style="font-size:0.7rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.08em;">Pool Size</div>
                    </div>
                    <div>
                        <div style="font-size:1rem;font-weight:700;color:var(--text-primary);">{km.get('inertia','–')}</div>
                        <div style="font-size:0.7rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.08em;">Inertia</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Persona explanations
            persona_desc = {
                "🚀 Rising Star": "High ATS score and skills with strong growth trajectory. Fast-learning candidate with solid fundamentals.",
                "💎 Top Performer": "Exceptional across all dimensions. High hire probability, rich skill set, and strong ATS alignment.",
                "📈 Growth Potential": "Moderate scores now but strong signals of future excellence. Worth a deeper look.",
                "🔧 Technical Specialist": "Deep technical expertise in niche areas. May lack breadth but excels in depth.",
            }
            desc = persona_desc.get(persona, "A unique candidate profile detected by K-Means clustering.")
            st.markdown(f"""
            <div class="glass-card" style="margin-top:1rem;">
                <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;
                            color:var(--accent);margin-bottom:0.5rem;">Persona Description</div>
                <div style="font-size:0.88rem;color:var(--text-secondary);line-height:1.6;">{desc}</div>
                <div style="margin-top:0.75rem;font-size:0.72rem;color:var(--text-muted);">
                    Algorithm: K-Means (k={km.get('k',4)}) · Init: k-means++ · Seed: 42
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="section-label">✦ Hierarchical Clustering</div>', unsafe_allow_html=True)
            pool_labels = st.session_state.get("pool_labels", [f"C{i}" for i in range(20)] + ["YOU"])
            dend_fig = dendrogram_fig(pool_labels[:12])  # Show 12 for readability
            if dend_fig:
                st.plotly_chart(dend_fig, use_container_width=True, theme=None, config={"displayModeBar": False})
            st.markdown("""
            <div style="font-size:0.78rem;color:var(--text-muted);text-align:center;margin-top:-0.5rem;">
                Ward linkage · Euclidean distance · Candidate feature space
            </div>
            """, unsafe_allow_html=True)

    # ── Tab 4: PCA ────────────────────────────────────────
    with tabs[3]:
        pca_data = st.session_state.get("pca_data")
        if pca_data:
            pca_df = pd.DataFrame({
                "PC1": pca_data["PC1"],
                "PC2": pca_data["PC2"],
                "Label": pca_data["Label"],
                "Cluster": [str(c) for c in pca_data["Cluster"]],
            })
            pca_fig = pca_scatter(pca_df)
            if pca_fig:
                st.plotly_chart(pca_fig, use_container_width=True, theme=None, config={"displayModeBar": False})

            ev = pca_data.get("explained_variance", [0, 0])
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{ev[0] if ev else '–'}%</div>
                    <div class="metric-label">PC1 Variance</div>
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{ev[1] if len(ev) > 1 else '–'}%</div>
                    <div class="metric-label">PC2 Variance</div>
                </div>""", unsafe_allow_html=True)
            with c3:
                total_ev = sum(ev[:2])
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{total_ev:.1f}%</div>
                    <div class="metric-label">Total Explained</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("""
            <div class="glass-card" style="margin-top:1rem;">
                <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;
                            color:var(--accent);margin-bottom:0.5rem;">About This Chart</div>
                <div style="font-size:0.85rem;color:var(--text-secondary);line-height:1.6;">
                    PCA reduces the 5-dimensional candidate feature space (ATS score, skill count,
                    word count, hire probability, role ID) to 2 principal components for visualization.
                    <strong style="color:var(--text-primary);">YOU</strong> are highlighted in the scatter.
                    Nearby candidates share similar profiles.
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Tab 5: Suggestions ────────────────────────────────
    with tabs[4]:
        st.markdown('<div class="section-label">✦ AI Improvement Recommendations</div>', unsafe_allow_html=True)
        suggestions = st.session_state.suggestions
        if not suggestions:
            st.markdown("""
            <div class="glass-card" style="text-align:center;padding:2rem;">
                <div style="font-size:2rem;">🎉</div>
                <div style="font-weight:700;margin-top:0.5rem;color:var(--success);">
                    Excellent resume! No major improvements needed.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            priority_map = {1: ("🔴", "High Priority"), 2: ("🟡", "Medium"), 3: ("🔵", "Low")}
            for s in suggestions:
                icon    = s.get("icon", "💡")
                title   = s.get("title", "")
                text    = s.get("text", "")
                prio    = s.get("priority", 2)
                pdot, plabel = priority_map.get(prio, ("🔵", "Low"))
                st.markdown(f"""
                <div class="suggestion-item">
                    <div class="suggestion-icon">{icon}</div>
                    <div style="flex:1;">
                        <div style="display:flex;align-items:center;gap:8px;margin-bottom:3px;">
                            <div class="suggestion-title">{title}</div>
                            <span style="font-size:0.65rem;color:var(--text-muted);">{pdot} {plabel}</span>
                        </div>
                        <div class="suggestion-text">{text}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Re-run button
        st.markdown('<div style="height:1rem;"></div>', unsafe_allow_html=True)
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔄  Re-run Analysis"):
                st.session_state.analysis_done = False
                st.rerun()
        with col_btn2:
            if st.button("📑  Generate PDF Report"):
                st.session_state.current_page = "report"
                st.rerun()
