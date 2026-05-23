"""
pages/login.py — HireLens AI premium login page.
"""

import streamlit as st
import time

def render():
    # Inject page-specific styles to make the Streamlit form look like a glass card
    st.markdown("""
    <style>
    /* Styling the Streamlit form to match glass-card aesthetics */
    [data-testid="stForm"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 20px !important;
        padding: 2.5rem 2rem !important;
        box-shadow: 0 12px 40px rgba(0,0,0,0.15) !important;
        transition: all 0.3s ease-in-out !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
    }
    [data-testid="stForm"]:hover {
        background: var(--bg-card-hover) !important;
        border-color: var(--border-accent) !important;
        box-shadow: var(--shadow-card), var(--shadow-glow) !important;
    }
    
    /* Ensure the sign-in button is fully visible with white text */
    [data-testid="stFormSubmitButton"] button {
        background-color: var(--accent) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        font-family: var(--font-body) !important;
        font-weight: 700 !important;
        transition: all 0.25s ease !important;
    }
    [data-testid="stFormSubmitButton"] button:hover {
        background-color: var(--accent-light) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(129, 11, 56, 0.4) !important;
    }
    [data-testid="stFormSubmitButton"] button p,
    [data-testid="stFormSubmitButton"] button * {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    
    /* Login subtitle styling */
    .login-subtitle {
        text-align: center;
        font-size: 0.88rem;
        color: var(--text-secondary);
        margin-bottom: 2rem;
    }
    
    /* Center the login box on the page */
    .login-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin-top: 3rem;
    }
    
    /* Credentials card */
    .credentials-box {
        margin-top: 1.5rem;
        background: rgba(129, 11, 56, 0.08);
        border: 1px solid rgba(129, 11, 56, 0.2);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        font-size: 0.8rem;
        color: var(--text-primary);
        width: 100%;
        box-sizing: border-box;
    }
    .credentials-title {
        font-weight: 700;
        color: var(--accent-light);
        margin-bottom: 0.25rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    </style>
    """, unsafe_allow_html=True)

    # Main centering container
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.8, 1])
    
    with col2:
        # Branded Header
        st.markdown("""
        <div style="text-align: center; margin-bottom: 1rem; animation: fadeSlideDown 0.5s ease both;">
            <div style="display: inline-block; width: 64px; height: 64px; border-radius: 18px; 
                        background: linear-gradient(135deg, var(--accent), var(--accent-light));
                        color: #fff; font-family: var(--font-display); font-size: 1.4rem; 
                        font-weight: 800; line-height: 64px; text-align: center;
                        box-shadow: 0 12px 28px rgba(129,11,56,0.3); margin-bottom: 1rem;">HL</div>
            <h1 style="font-family: var(--font-display); font-size: 2.2rem; margin: 0; line-height: 1.1; font-weight: 800;">
                HireLens <span style="color: var(--accent-light);">AI</span>
            </h1>
            <p class="login-subtitle">🔮 Premium AI-Powered Recruitment Intelligence</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Login Form
        with st.form("login_form", clear_on_submit=False):
            st.markdown('<div style="font-family: var(--font-display); font-size: 1.1rem; font-weight: 700; color: var(--text-primary); margin-bottom: 1rem; text-align: center;">Account Login</div>', unsafe_allow_html=True)
            
            username = st.text_input("Username", placeholder="Enter your username", key="login_username")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
            
            submit_btn = st.form_submit_button("Sign In", use_container_width=True)
            
            if submit_btn:
                # Sanitize & check credentials
                username_clean = username.strip()
                if username_clean:
                    st.success(f"Access Granted! Welcome, {username_clean}. Redirecting...")
                    st.session_state.authenticated = True
                    st.session_state.username = username_clean
                    st.session_state.current_page = "home"
                    st.query_params["authenticated"] = "true"
                    st.query_params["username"] = username_clean
                    st.query_params["page"] = "home"
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Please enter a username to sign in.")
        
        # Credentials Help Card
        st.markdown("""
        <div class="credentials-box">
            <div class="credentials-title">👤 User Sign In</div>
            <div>Enter any username and password to log in.</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)
