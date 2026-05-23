"""
pages/home.py — HireLens AI landing / hero page.
"""

import streamlit as st


def render():
    username = st.session_state.get("username", "Guest")
    # ── Hero ──────────────────────────────────────────────
    st.markdown(f"""
    <div class="page-header" style="text-align:center; padding: 2rem 1rem 1rem;">
        <div style="display:inline-block; padding:0.3rem 1rem; background:var(--bg-card);
                    border:1px solid var(--border); border-radius:99px; margin-bottom:1rem;">
            <span style="font-size:0.75rem; font-weight:700; text-transform:uppercase;
                         letter-spacing:0.1em; color:var(--accent);">
                ✦ Welcome, {username} ✦
            </span>
        </div>
        <h1 class="page-title" style="font-size:2.8rem; margin-bottom:0.5rem; line-height:1.2;">
            Analyze. Score. Hire <span style="color:var(--accent);">Smarter.</span>
        </h1>
        <p class="page-subtitle" style="font-size:1.05rem; max-width:560px; margin:0 auto 1.5rem; color:var(--text-secondary);">
            HireLens AI uses Naive Bayes, Logistic Regression, and
            Clustering to give you unprecedented resume intelligence.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── CTA buttons ───────────────────────────────────────
    col1, col2, col3, col4 = st.columns([2, 1.2, 1.2, 2][:4] if False else [1, 0.7, 0.7, 1])
    with col2:
        if st.button("🚀  Analyze Resume", use_container_width=True):
            st.session_state.current_page = "upload"
            st.rerun()
    with col3:
        if st.button("📊  Dashboard", use_container_width=True):
            st.session_state.current_page = "recruiter"
            st.rerun()

    st.markdown('<div style="height:1.5rem;"></div>', unsafe_allow_html=True)

    # ── Feature cards ─────────────────────────────────────
    st.markdown('<div class="section-label">✦ Core Capabilities</div>', unsafe_allow_html=True)

    features = [
        ("🧠", "Naive Bayes Classifier", "Multi-class TF-IDF resume classification across 8 job roles with confidence scoring."),
        ("📊", "ATS Scoring Engine", "TF-IDF cosine similarity between your resume and job description for real ATS compatibility."),
        ("🎯", "Hire Probability", "Logistic Regression model predicts your hiring likelihood with explainable feature weights."),
        ("🔮", "Candidate Personas", "K-Means clustering reveals your candidate archetype from a pool of peers."),
        ("📐", "PCA Visualization", "2D principal component analysis maps your position in the talent landscape."),
        ("🌳", "Hierarchical Clustering", "Ward-linkage dendrogram shows candidate similarity for batch analysis."),
    ]

    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="glass-card" style="margin-bottom:1rem; animation-delay:{i*0.08}s;">
                <div style="font-size:2rem; margin-bottom:0.75rem;">{icon}</div>
                <div style="font-family:'Syne',sans-serif; font-size:1rem; font-weight:700;
                            color:var(--text-primary); margin-bottom:0.5rem;">{title}</div>
                <div style="font-size:0.85rem; color:var(--text-secondary); line-height:1.55;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div style="height:1.5rem;"></div>', unsafe_allow_html=True)

    # ── Tech Stack ────────────────────────────────────────
    st.markdown('<div class="section-label">✦ Technology Stack</div>', unsafe_allow_html=True)

    techs = ["Python 3.11", "Streamlit", "scikit-learn", "NLTK", "Plotly", "pdfplumber", "fpdf2", "NumPy", "SciPy"]
    pills_html = "".join(f'<span class="skill-pill">{t}</span>' for t in techs)
    st.markdown(f'<div style="margin-bottom:2rem;">{pills_html}</div>', unsafe_allow_html=True)

    # ── Stats bar ─────────────────────────────────────────
    st.markdown('<div class="section-label">✦ Platform Stats</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    stats = [
        ("8", "Job Roles Classified"),
        ("6", "ML Models Integrated"),
        ("15+", "NLP Features"),
        ("100%", "Open Source"),
    ]
    for col, (val, label) in zip([c1, c2, c3, c4], stats):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div style="height:1.5rem;"></div>', unsafe_allow_html=True)

    # ── ML Concepts callout ───────────────────────────────
    st.markdown("""
    <div class="glass-card" style="border-left:3px solid var(--accent); padding:1.5rem 2rem;">
        <div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:0.15em;
                    color:var(--accent);margin-bottom:0.75rem;">✦ ML Concepts Covered</div>
        <div style="display:flex;flex-wrap:wrap;gap:10px;">
    """ + "".join(f'<span class="badge badge-accent">{t}</span>' for t in [
        "Naive Bayes", "Logistic Regression", "K-Means Clustering",
        "Hierarchical Clustering", "PCA", "TF-IDF", "NLP Preprocessing",
        "Text Classification", "Evaluation Metrics", "Cosine Similarity",
    ]) + """
        </div>
    </div>
    """, unsafe_allow_html=True)
