"""
HireLens AI - Premium AI-Powered Resume Analyzer.
Main entry point with custom theming and navigation.
"""

import streamlit as st
from utils.styles import inject_global_css
from utils.session import init_session_state



def get_initials(name):
    if not name:
        return "??"
    words = name.strip().split()
    if len(words) == 1:
        return words[0][:2].upper()
    return (words[0][0] + words[-1][0]).upper()


st.set_page_config(
    page_title="HireLens AI",
    page_icon="HL",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()
init_session_state()

# ── Restore Auth from Query Params ───────────────────────────────────────────
if st.query_params.get("authenticated") == "true" and st.query_params.get("username"):
    st.session_state.authenticated = True
    st.session_state.username = st.query_params.get("username")

# ── Logout Intercept ─────────────────────────────────────────────────────────
if st.query_params.get("logout") == "true":
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.current_page = "home"
    st.query_params.clear()
    st.rerun()

# ── Authentication Check ─────────────────────────────────────────────────────
if not st.session_state.authenticated:
    from pages import login
    login.render()
    st.stop()

PAGES = {
    "home": {"label": "Home", "icon": "&#8962;"},
    "upload": {"label": "Upload Resume", "icon": "&#128196;"},
    "analysis": {"label": "AI Analysis", "icon": "&#129504;"},
    "recruiter": {"label": "Recruiter Dashboard", "icon": "&#128202;"},
    "candidate": {"label": "Candidate Dashboard", "icon": "&#128100;"},
    "report": {"label": "PDF Report", "icon": "&#128209;"},
}

query_page = st.query_params.get("page", "home")
if query_page not in PAGES:
    query_page = "home"

if "last_query_page" not in st.session_state:
    st.session_state.last_query_page = None

# Ensure auth params stay in query parameters when authenticated
if st.session_state.authenticated:
    st.query_params["authenticated"] = "true"
    st.query_params["username"] = st.session_state.username

# If the URL parameter changed (e.g., via sidebar link), update the session state
if query_page != st.session_state.last_query_page:
    st.session_state.current_page = query_page
    st.session_state.last_query_page = query_page
else:
    # If session state changed (e.g., via button click), update the URL
    if st.session_state.current_page != query_page:
        st.query_params["page"] = st.session_state.current_page
        st.session_state.last_query_page = st.session_state.current_page


with st.sidebar:
    username = st.session_state.username
    initials = get_initials(username)
    capitalized_name = username.title()

    nav_items = []
    for key, item in PAGES.items():
        active = " active" if st.session_state.current_page == key else ""
        nav_items.append(
            f'<a class="sidebar-nav-item{active}" href="?page={key}&authenticated=true&username={username}" target="_self">'
            f'<span class="nav-icon">{item["icon"]}</span>'
            f'<span class="nav-label">{item["label"]}</span>'
            "</a>"
        )

    # Append Log Out link to the navigation items
    logout_item = (
        f'<div class="sidebar-divider" style="margin: 0.5rem 0;"></div>'
        f'<a class="sidebar-nav-item" href="?logout=true" target="_self" style="color: var(--danger) !important;">'
        f'<span class="nav-icon" style="color: var(--danger);">🔓</span>'
        f'<span class="nav-label">Log Out</span>'
        f'</a>'
    )

    # Render entire sidebar in a single markdown block using the flex container shell
    st.markdown(
        (
            '<div class="sidebar-shell">'
            '<div class="sidebar-top">'
            '<div class="sidebar-logo">'
            '<div class="logo-mark">HL</div>'
            '<div class="logo-copy">'
            '<span class="logo-text">HireLens</span>'
            '<span class="logo-accent">AI</span>'
            "</div>"
            "</div>"
            
            # User profile card box
            f'<div class="user-profile-card" style="'
            f'background: rgba(241, 226, 209, 0.04);'
            f'border: 1px solid rgba(241, 226, 209, 0.08);'
            f'border-radius: 16px;'
            f'padding: 1.1rem 0.85rem;'
            f'margin: 0.5rem 0.65rem 1rem;'
            f'display: flex;'
            f'flex-direction: column;'
            f'align-items: center;'
            f'justify-content: center;'
            f'gap: 0.65rem;'
            f'">'
            f'<div style="'
            f'width: 44px;'
            f'height: 44px;'
            f'border-radius: 50%;'
            f'background: linear-gradient(135deg, var(--accent), var(--accent-light));'
            f'color: #FFFFFF;'
            f'font-family: var(--font-display);'
            f'font-size: 1.1rem;'
            f'font-weight: 800;'
            f'display: flex;'
            f'align-items: center;'
            f'justify-content: center;'
            f'box-shadow: 0 6px 14px rgba(129, 11, 56, 0.25);'
            f'">{initials}</div>'
            f'<div style="text-align: center;">'
            f'<div style="font-family: var(--font-body); font-size: 0.88rem; font-weight: 700; color: var(--sidebar-text); line-height: 1.25;">'
            f'{capitalized_name}</div>'
            f'<div style="font-size: 0.7rem; color: var(--sidebar-muted); font-weight: 500; margin-top: 0.2rem; letter-spacing: 0.06em; text-transform: uppercase;">'
            f'Authorized User</div>'
            f'</div>'
            f'</div>'
            
            '<div class="sidebar-divider"></div>'
            '<nav class="sidebar-nav" aria-label="Primary navigation">'
            f"{''.join(nav_items)}"
            f"{logout_item}"
            "</nav>"
            "</div>"
            '<div class="sidebar-footer-wrap">'
            '<div class="sidebar-divider sidebar-divider-bottom"></div>'
            '<div class="sidebar-footer">'
            "<p>v1.0.0 &middot; Built with care</p>"
            '<p class="footer-sub">Powered by scikit-learn &amp; NLP</p>'
            "</div>"
            "</div>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )



page = st.session_state.current_page

if page == "home":
    from pages import home

    home.render()
elif page == "upload":
    from pages import upload

    upload.render()
elif page == "analysis":
    from pages import analysis

    analysis.render()
elif page == "recruiter":
    from pages import recruiter

    recruiter.render()
elif page == "candidate":
    from pages import candidate

    candidate.render()
elif page == "report":
    from pages import report

    report.render()
