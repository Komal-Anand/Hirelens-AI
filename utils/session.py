"""
utils/session.py — Initialize and manage Streamlit session state.
"""

import streamlit as st


def init_session_state():
    """Initialize all session state variables."""
    defaults = {
        "authenticated": False,
        "username": "",
        "theme": "light",
        "current_page": "home",
        "resume_text": None,
        "resume_filename": None,
        "analysis_done": False,
        "ats_score": None,
        "hire_probability": None,
        "predicted_role": None,
        "candidate_cluster": None,
        "cluster_label": None,
        "extracted_skills": [],
        "missing_skills": [],
        "suggestions": [],
        "preprocessed_tokens": [],
        "role_confidence": {},
        "pca_data": None,
        "dendrogram_fig": None,
        "pca_fig": None,
        "recruiter_mode": False,
        "job_description": "",
        "candidate_name": "",
        "candidates_batch": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
