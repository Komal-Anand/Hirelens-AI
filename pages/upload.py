"""
pages/upload.py — Resume upload + text extraction page.
"""

import streamlit as st
from utils.pdf_utils import (
    extract_text_from_upload, get_word_count, get_char_count, estimate_pages
)


def render():
    st.markdown("""
    <div class="page-header">
        <div class="page-title">Upload Resume</div>
        <p class="page-subtitle">
            Drop your PDF or TXT resume to begin AI-powered analysis.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_upload, col_info = st.columns([1.6, 1])

    with col_upload:
        st.markdown('<div class="section-label">✦ Resume File</div>', unsafe_allow_html=True)

        uploaded = st.file_uploader(
            label="",
            type=["pdf", "txt"],
            accept_multiple_files=False,
            help="Supported: PDF and plain text (.txt)",
            label_visibility="collapsed",
        )

        if uploaded:
            with st.spinner("Extracting text..."):
                try:
                    text = extract_text_from_upload(uploaded)
                    st.session_state.resume_text = text
                    st.session_state.resume_filename = uploaded.name
                    st.session_state.analysis_done = False  # reset on new upload

                    wc = get_word_count(text)
                    cc = get_char_count(text)
                    pages = estimate_pages(text)

                    st.markdown(f"""
                    <div class="glass-card" style="margin-top:1rem; border-color:rgba(16,185,129,0.3);">
                        <div style="display:flex;align-items:center;gap:10px;margin-bottom:1rem;">
                            <span style="font-size:1.4rem;">✅</span>
                            <span style="font-weight:700;color:var(--success);font-size:1rem;">
                                Resume extracted successfully
                            </span>
                        </div>
                        <div style="display:flex;gap:2rem;flex-wrap:wrap;">
                            <div>
                                <div style="font-size:1.6rem;font-weight:800;color:var(--accent);
                                            font-family:'Syne',sans-serif;">{wc:,}</div>
                                <div style="font-size:0.72rem;text-transform:uppercase;
                                            letter-spacing:0.1em;color:var(--text-muted);">Words</div>
                            </div>
                            <div>
                                <div style="font-size:1.6rem;font-weight:800;color:var(--accent);
                                            font-family:'Syne',sans-serif;">{cc:,}</div>
                                <div style="font-size:0.72rem;text-transform:uppercase;
                                            letter-spacing:0.1em;color:var(--text-muted);">Characters</div>
                            </div>
                            <div>
                                <div style="font-size:1.6rem;font-weight:800;color:var(--accent);
                                            font-family:'Syne',sans-serif;">~{pages}</div>
                                <div style="font-size:0.72rem;text-transform:uppercase;
                                            letter-spacing:0.1em;color:var(--text-muted);">Pages</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Extraction failed: {e}")
                    st.session_state.resume_text = None

        # Optional job description
        st.markdown('<div class="section-label" style="margin-top:1.5rem;">✦ Job Description (Optional)</div>', unsafe_allow_html=True)
        jd = st.text_area(
            label="",
            placeholder="Paste the job description here for precise ATS scoring...",
            height=160,
            label_visibility="collapsed",
            key="jd_input",
        )
        st.session_state.job_description = jd

        # Candidate name
        st.markdown('<div class="section-label">✦ Candidate Name (Optional)</div>', unsafe_allow_html=True)
        name = st.text_input(
            label="",
            placeholder="e.g. Alex Chen",
            label_visibility="collapsed",
            key="cname_input",
        )
        st.session_state.candidate_name = name

    with col_info:
        # Tips card
        st.markdown("""
        <div class="glass-card" style="margin-top:2.5rem;">
            <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:1rem;
                        color:var(--text-primary);margin-bottom:1rem;">💡 Pro Tips</div>
            <div class="suggestion-item" style="margin-bottom:0.5rem;">
                <div class="suggestion-icon">📄</div>
                <div class="suggestion-text">
                    <div class="suggestion-title">Use a clean PDF</div>
                    Text-based PDFs extract better than scanned images.
                </div>
            </div>
            <div class="suggestion-item" style="margin-bottom:0.5rem;">
                <div class="suggestion-icon">🎯</div>
                <div class="suggestion-text">
                    <div class="suggestion-title">Add Job Description</div>
                    Enables precise TF-IDF cosine ATS scoring.
                </div>
            </div>
            <div class="suggestion-item">
                <div class="suggestion-icon">📏</div>
                <div class="suggestion-text">
                    <div class="suggestion-title">Sweet spot: 400–800 words</div>
                    Concise resumes score better on ATS systems.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # What happens next
        st.markdown("""
        <div class="glass-card" style="margin-top:1rem;">
            <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:1rem;
                        color:var(--text-primary);margin-bottom:1rem;">⚡ Analysis Pipeline</div>
        """, unsafe_allow_html=True)
        steps = [
            ("1", "NLP Preprocessing", "Tokenize → Stopwords → Lemmatize"),
            ("2", "Role Classification", "Naive Bayes + TF-IDF"),
            ("3", "ATS Scoring", "Cosine similarity with JD"),
            ("4", "Hire Prediction", "Logistic Regression"),
            ("5", "Clustering", "K-Means persona detection"),
        ]
        for num, title, sub in steps:
            st.markdown(f"""
            <div style="display:flex;gap:12px;align-items:flex-start;margin-bottom:0.75rem;">
                <div style="min-width:24px;height:24px;border-radius:50%;
                            background:rgba(129,11,56,0.2);border:1px solid rgba(129,11,56,0.4);
                            display:flex;align-items:center;justify-content:center;
                            font-size:0.7rem;font-weight:700;color:var(--accent);">{num}</div>
                <div>
                    <div style="font-weight:600;font-size:0.88rem;color:var(--text-primary);">{title}</div>
                    <div style="font-size:0.78rem;color:var(--text-muted);">{sub}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Run analysis button ───────────────────────────────
    st.markdown('<div style="height:1.5rem;"></div>', unsafe_allow_html=True)

    if st.session_state.resume_text:
        if st.button("🔮  Run Full Analysis", use_container_width=False):
            st.session_state.current_page = "analysis"
            st.rerun()
    else:
        st.markdown("""
        <div style="text-align:center;padding:1rem;color:var(--text-muted);font-size:0.9rem;">
            Upload a resume above to enable analysis
        </div>
        """, unsafe_allow_html=True)

    # ── Preview extracted text ────────────────────────────
    if st.session_state.resume_text:
        with st.expander("👁️  Preview Extracted Text", expanded=False):
            preview = st.session_state.resume_text[:2000]
            if len(st.session_state.resume_text) > 2000:
                preview += "\n\n... [truncated for preview]"
            st.code(preview, language=None)
