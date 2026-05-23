"""
utils/styles.py - Global CSS injection for HireLens AI premium UI.
Supports Dark and Light modes.
"""

import streamlit as st

def inject_global_css():
    colors = {
        "bg_primary": "#DCC3AA",
        "bg_secondary": "#E4CDB7",
        "bg_sidebar": "#200808",
        "bg_card": "#F1E2D1",
        "bg_card_hover": "#FBF4EA",
        "accent": "#810B38",
        "accent_light": "#A21A4F",
        "accent_cyan": "#DCC3AA",
        "accent_mint": "#F1E2D1",
        "accent_glow": "rgba(0,0,0,0)",
        "accent_soft": "rgba(129,11,56,0.15)",
        "text_primary": "#2C0D0D",
        "text_secondary": "rgba(44,13,13,0.7)",
        "text_muted": "rgba(44,13,13,0.5)",
        "sidebar_text": "#F1E2D1",
        "sidebar_muted": "rgba(241,226,209,0.6)",
        "border": "rgba(241,226,209,0.1)",
        "border_accent": "rgba(129,11,56,0.30)",
        "success": "#2F7D55",
        "warning": "#A76516",
        "danger": "#A21A4F",
        "info": "#810B38",
        "bg_grad_1": "transparent",
        "bg_grad_2": "transparent",
        "bg_grad_3": "#DCC3AA",
        "bg_grad_4": "#DCC3AA",
        "sidebar_grad_1": "transparent",
        "sidebar_grad_2": "transparent",
        "sidebar_grad_3": "transparent",
        "sidebar_border": "rgba(241,226,209,0.08)",
        "sidebar_shadow": "rgba(0,0,0,0)",
        "sidebar_logo_shadow": "rgba(0,0,0,0)",
        "sidebar_divider": "rgba(241,226,209,0.1)",
        "nav_hover_bg": "rgba(241,226,209,0.05)",
        "nav_hover_border": "transparent",
        "nav_hover_shadow": "rgba(0,0,0,0)",
        "nav_active_bg_1": "#810B38",
        "nav_active_bg_2": "#810B38",
        "nav_active_border": "#A21A4F",
        "nav_active_shadow": "rgba(0,0,0,0)",
        "nav_icon_bg": "transparent",
        "nav_icon_active_bg": "transparent",
        "skill_missing_bg": "rgba(162,26,79,0.1)",
        "skill_missing_border": "rgba(162,26,79,0.3)",
        "skill_present_bg": "rgba(47,125,85,0.1)",
        "skill_present_border": "rgba(47,125,85,0.3)",
        "progress_bg": "rgba(241,226,209,0.1)",
        "badge_success_bg": "rgba(47,125,85,0.15)",
        "badge_success_border": "rgba(47,125,85,0.3)",
        "badge_warning_bg": "rgba(167,101,22,0.15)",
        "badge_warning_border": "rgba(167,101,22,0.3)",
        "badge_danger_bg": "rgba(162,26,79,0.15)",
        "badge_danger_border": "rgba(162,26,79,0.3)",
        "upload_border": "rgba(129,11,56,0.3)",
        "upload_hover_bg": "rgba(129,11,56,0.1)",
        "input_bg": "#200808",
        "input_focus_shadow": "rgba(129,11,56,0.4)",
        "btn_secondary_hover_bg": "#3D1212",
        "tabs_bg": "transparent",
        "pulse_shadow": "rgba(0,0,0,0)"
    }

    root_vars = """
    :root {{
        --bg-primary:    {bg_primary};
        --bg-secondary:  {bg_secondary};
        --bg-sidebar:    {bg_sidebar};
        --bg-card:       {bg_card};
        --bg-card-hover: {bg_card_hover};
        --accent:        {accent};
        --accent-light:  {accent_light};
        --accent-cyan:   {accent_cyan};
        --accent-mint:   {accent_mint};
        --accent-glow:   {accent_glow};
        --accent-soft:   {accent_soft};
        --text-primary:  {text_primary};
        --text-secondary:{text_secondary};
        --text-muted:    {text_muted};
        --sidebar-text:  {sidebar_text};
        --sidebar-muted: {sidebar_muted};
        --border:        {border};
        --border-accent: {border_accent};
        --success:       {success};
        --warning:       {warning};
        --danger:        {danger};
        --info:          {info};
        --radius-sm:     8px;
        --radius-md:     14px;
        --radius-lg:     20px;
        --radius-xl:     28px;
        --shadow-card:   0 18px 46px rgba(0,0,0,0.14);
        --shadow-glow:   0 18px 42px rgba(0,0,0,0.16);
        --font-display:  'Syne', sans-serif;
        --font-body:     'DM Sans', sans-serif;
        --font-mono:     'JetBrains Mono', monospace;
        --bg-grad-1: {bg_grad_1};
        --bg-grad-2: {bg_grad_2};
        --bg-grad-3: {bg_grad_3};
        --bg-grad-4: {bg_grad_4};
        --sidebar-grad-1: {sidebar_grad_1};
        --sidebar-grad-2: {sidebar_grad_2};
        --sidebar-grad-3: {sidebar_grad_3};
        --sidebar-border: {sidebar_border};
        --sidebar-shadow: {sidebar_shadow};
        --sidebar-logo-shadow: {sidebar_logo_shadow};
        --sidebar-divider: {sidebar_divider};
        --nav-hover-bg: {nav_hover_bg};
        --nav-hover-border: {nav_hover_border};
        --nav-hover-shadow: {nav_hover_shadow};
        --nav-active-bg-1: {nav_active_bg_1};
        --nav-active-bg-2: {nav_active_bg_2};
        --nav-active-border: {nav_active_border};
        --nav-active-shadow: {nav_active_shadow};
        --nav-icon-bg: {nav_icon_bg};
        --nav-icon-active-bg: {nav_icon_active_bg};
        --skill-missing-bg: {skill_missing_bg};
        --skill-missing-border: {skill_missing_border};
        --skill-present-bg: {skill_present_bg};
        --skill-present-border: {skill_present_border};
        --progress-bg: {progress_bg};
        --badge-success-bg: {badge_success_bg};
        --badge-success-border: {badge_success_border};
        --badge-warning-bg: {badge_warning_bg};
        --badge-warning-border: {badge_warning_border};
        --badge-danger-bg: {badge_danger_bg};
        --badge-danger-border: {badge_danger_border};
        --upload-border: {upload_border};
        --upload-hover-bg: {upload_hover_bg};
        --input-bg: {input_bg};
        --input-focus-shadow: {input_focus_shadow};
        --btn-secondary-hover-bg: {btn_secondary_hover_bg};
        --tabs-bg: {tabs_bg};
        --pulse-shadow: {pulse_shadow};
    }}
    """.format(**colors)

    st.markdown("<style>\n" + root_vars + "\n" + """
    /* - Google Fonts - */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Syne:wght@700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* - Base Reset - */
    html, body, [class*="css"] {
        font-family: var(--font-body) !important;
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }
    .stApp,
    .main,
    [data-testid="stAppViewContainer"],
    [data-testid="stMarkdownContainer"],
    [data-testid="stWidgetLabel"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    label {
        color: var(--text-primary) !important;
    }
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4,
    [data-testid="stMarkdownContainer"] strong {
        color: var(--text-primary) !important;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"],
    [data-testid="stSidebar"] label {
        color: var(--sidebar-text) !important;
    }

    .stApp {
        background: var(--bg-primary) !important;
    }
    .main { background: transparent !important; }
    .block-container {
        padding: 2rem 2.5rem 4rem !important;
        max-width: 1280px !important;
    }

    /* - Hide default Streamlit chrome - */
    #MainMenu, footer { visibility: hidden !important; }
    header[data-testid="stHeader"] { background: transparent !important; }
    .stDeployButton { display: none !important; }


    /* - Scrollbar - */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-primary); }
    ::-webkit-scrollbar-thumb {
        background: var(--accent);
        border-radius: 99px;
    }

    /* - Sidebar - */
    [data-testid="stSidebar"] {
        background: var(--bg-sidebar) !important;
        border-right: 1px solid var(--sidebar-border) !important;
        padding-top: 0 !important;
        width: 280px !important;
        box-shadow: 16px 0 42px var(--sidebar-shadow) !important;
        -webkit-
    }
    [data-testid="stSidebar"] > div {
        padding: 1rem 0.95rem 1rem !important;
    }
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        width: 100% !important;
    }
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }

    .sidebar-shell {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: calc(100vh - 2rem);
        width: 100%;
        padding: 0.25rem 0;
        box-sizing: border-box;
    }
    .sidebar-top {
        display: flex;
        flex-direction: column;
        width: 100%;
    }

    .sidebar-logo {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        width: 100%;
        padding: 0.75rem 0.65rem 0.9rem;
        box-sizing: border-box;
        animation: fadeSlideDown 0.5s ease both;
    }
    .logo-mark {
        flex: 0 0 42px;
        display: grid;
        place-items: center;
        width: 42px;
        height: 42px;
        border-radius: 13px;
        background: linear-gradient(135deg, var(--accent), var(--accent-light));
        color: #fff;
        font-family: var(--font-display);
        font-size: 0.9rem;
        font-weight: 800;
        box-shadow: 0 12px 28px var(--sidebar-logo-shadow);
    }
    .logo-copy {
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-width: 0;
        line-height: 1;
    }
    .logo-text {
        font-family: var(--font-display);
        font-size: 1.35rem;
        font-weight: 800;
        color: var(--sidebar-text);
        letter-spacing: 0;
    }
    .logo-accent {
        margin-top: 0.22rem;
        font-family: var(--font-display);
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.16em;
        color: var(--accent-light);
    }

    .sidebar-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--sidebar-divider), transparent);
        margin: 0.65rem 0 0.85rem;
    }
    .sidebar-divider-bottom {
        margin: 0 0 0.8rem;
    }

    .sidebar-nav {
        display: flex;
        flex-direction: column;
        gap: 0.38rem;
        width: 100%;
    }
    .sidebar-nav-item {
        position: relative;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        min-height: 42px;
        width: 100%;
        padding: 0.66rem 0.78rem;
        box-sizing: border-box;
        border: 1px solid transparent;
        border-radius: 12px;
        color: var(--sidebar-muted) !important;
        text-decoration: none !important;
        font-family: var(--font-body);
        font-size: 0.9rem;
        font-weight: 600;
        line-height: 1.2;
        transition:
            background 0.2s ease,
            border-color 0.2s ease,
            color 0.2s ease,
            box-shadow 0.2s ease,
            transform 0.2s ease;
    }
    .sidebar-nav-item:hover {
        background: var(--nav-hover-bg);
        border-color: var(--nav-hover-border);
        color: var(--sidebar-text) !important;
        transform: translateX(3px);
        box-shadow: 0 8px 22px var(--nav-hover-shadow);
    }
    .sidebar-nav-item.active {
        background: linear-gradient(135deg, var(--nav-active-bg-1), var(--nav-active-bg-2));
        border-color: var(--nav-active-border);
        color: var(--sidebar-text) !important;
        box-shadow: inset 3px 0 0 var(--accent-light), 0 14px 32px var(--nav-active-shadow);
    }
    .sidebar-nav-item.active .nav-icon {
        background: var(--nav-icon-active-bg);
        color: #FFFFFF;
    }
    .nav-icon {
        flex: 0 0 26px;
        display: grid;
        place-items: center;
        width: 26px;
        height: 26px;
        border-radius: 8px;
        background: var(--nav-hover-bg);
        color: var(--sidebar-muted);
        font-size: 0.95rem;
        line-height: 1;
        transition: background 0.2s ease, color 0.2s ease;
    }
    .nav-label {
        flex: 1;
        min-width: 0;
        overflow-wrap: anywhere;
    }
    .sidebar-footer-wrap {
        width: 100%;
        padding-top: 1rem;
        box-sizing: border-box;
    }

    .sidebar-footer {
        margin-top: 0;
        text-align: center;
        padding: 0 0.55rem 0.15rem;
    }
    .sidebar-footer p {
        font-size: 0.72rem;
        color: var(--sidebar-muted);
        margin: 0;
        line-height: 1.6;
    }
    .footer-sub { color: var(--accent-light) !important; }

    /* - Glass Card - */
    .glass-card {
        background: var(--bg-card);
        -webkit-
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1.75rem 2rem;
        box-shadow: 0 4px 14px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        animation: fadeSlideUp 0.5s ease both;
    }
    .glass-card:hover {
        background: var(--bg-card-hover);
        border-color: var(--border-accent);
        box-shadow: var(--shadow-card), var(--shadow-glow);
        transform: translateY(-2px);
    }

    /* - Metric Card - */
    .metric-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 1.25rem 1.5rem;
        text-align: center;
        transition: all 0.25s ease;
        position: relative;
        overflow: hidden;
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--accent), var(--accent-light), var(--accent-cyan));
    }
    .metric-card:hover { transform: translateY(-3px); border-color: var(--border-accent); }
    .metric-value {
        font-family: var(--font-display);
        font-size: 2.2rem;
        font-weight: 800;
        color: var(--accent-light);
        line-height: 1;
        margin-bottom: 0.35rem;
    }
    .metric-label {
        font-size: 0.8rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 500;
    }

    /* - Page Headers - */
    .page-header {
        margin-bottom: 2.5rem;
        animation: fadeSlideDown 0.4s ease both;
    }
    .page-title {
        font-family: var(--font-display);
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--text-primary) 16%, var(--accent) 62%, var(--bg-sidebar));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: 0;
        line-height: 1.1;
        margin-bottom: 0.5rem;
    }
    .page-subtitle {
        font-size: 1rem;
        color: var(--text-secondary);
        font-weight: 400;
        margin: 0;
    }

    /* - Section Labels - */
    .section-label {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        color: var(--accent);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-label::after {
        content: '';
        flex: 1;
        height: 1px;
        background: var(--border);
    }

    /* - Skill Pills - */
    .skill-pill {
        display: inline-block;
        padding: 0.3rem 0.85rem;
        background: var(--accent-soft);
        border: 1px solid var(--border);
        border-radius: 99px;
        font-size: 0.78rem;
        font-weight: 600;
        color: var(--accent);
        margin: 3px;
        letter-spacing: 0.02em;
        transition: all 0.2s;
    }
    .skill-pill:hover {
        background: linear-gradient(135deg, var(--accent), var(--accent-light));
        color: #fff;
    }

    .skill-missing {
        background: var(--skill-missing-bg);
        border-color: var(--skill-missing-border);
        color: var(--danger);
    }
    .skill-present {
        background: var(--skill-present-bg);
        border-color: var(--skill-present-border);
        color: #2F7D55;
    }

    /* - Score Meter - */
    .score-ring-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 1rem 0;
    }
    .score-label-top {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: var(--text-muted);
        margin-bottom: 0.75rem;
        font-weight: 600;
    }

    /* - Progress Bar - */
    .custom-progress {
        background: var(--progress-bg);
        border-radius: 99px;
        height: 8px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    .custom-progress-fill {
        height: 100%;
        border-radius: 99px;
        background: linear-gradient(90deg, var(--accent), var(--accent-light));
        transition: width 1.2s cubic-bezier(0.4,0,0.2,1);
    }

    /* - Tag Badges - */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.7rem;
        border-radius: 99px;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .badge-success { background: var(--badge-success-bg); color: #2F7D55; border: 1px solid var(--badge-success-border); }
    .badge-warning { background: var(--badge-warning-bg); color: #8B5A12; border: 1px solid var(--badge-warning-border); }
    .badge-danger  { background: var(--badge-danger-bg); color: var(--accent); border: 1px solid var(--skill-missing-border); }
    .badge-accent  { background: var(--accent-soft);    color: var(--accent-light); border: 1px solid var(--border); }

    /* - Suggestion Card - */
    .suggestion-item {
        display: flex;
        gap: 14px;
        align-items: flex-start;
        padding: 1rem 1.25rem;
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        margin-bottom: 0.75rem;
        transition: all 0.2s ease;
        animation: fadeSlideUp 0.4s ease both;
    }
    .suggestion-item:hover {
        border-color: var(--border-accent);
        background: var(--bg-card-hover);
    }
    .suggestion-icon {
        font-size: 1.2rem;
        min-width: 28px;
        text-align: center;
        margin-top: 1px;
    }
    .suggestion-text { font-size: 0.88rem; color: var(--text-secondary); line-height: 1.55; }
    .suggestion-title { font-weight: 600; color: var(--text-primary); margin-bottom: 2px; font-size: 0.92rem; }

    /* - Upload Zone - */
    [data-testid="stFileUploader"] {
        background: var(--bg-card) !important;
        border: 2px dashed var(--pulse-shadow) !important;
        border-radius: var(--radius-lg) !important;
        padding: 2rem !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: var(--accent-light) !important;
        background: var(--skill-missing-bg) !important;
    }
    [data-testid="stFileUploaderDropzone"] { background: transparent !important; }
    [data-testid="stFileUploaderDropzoneInstructions"] > div > span,
    [data-testid="stFileUploaderDropzoneInstructions"] small,
    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploader"] p {
        color: var(--text-secondary) !important;
    }
    [data-testid="stFileUploaderDropzone"] button {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        color: var(--text-secondary) !important;
    }
    [data-testid="stFileUploaderDropzone"] button * {
        color: var(--text-secondary) !important;
    }

    /* - Inputs - */
    .stTextArea textarea, .stTextInput input, .stSelectbox select {
        background: var(--input-bg) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        font-family: var(--font-body) !important;
        color: #F1E2D1 !important;
    }
    .stTextArea textarea::placeholder, .stTextInput input::placeholder {
        color: rgba(241,226,209,0.4) !important;
        opacity: 1 !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px var(--input-focus-shadow) !important;
    }

    /* - Buttons - */
    .stButton > button,
    [data-testid="stFormSubmitButton"] button,
    [data-testid="stBaseButton-secondary"],
    [data-testid="stBaseButton-primary"] {
        background: var(--accent) !important;
        color: #fff !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        font-family: var(--font-body) !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 0.6rem 1.4rem !important;
        transition: all 0.25s ease !important;
        letter-spacing: 0.02em !important;
    }
    .stButton > button *,
    [data-testid="stFormSubmitButton"] button *,
    [data-testid="stBaseButton-secondary"] *,
    [data-testid="stBaseButton-primary"] * {
        color: #fff !important;
    }
    .stButton > button:hover,
    [data-testid="stFormSubmitButton"] button:hover,
    [data-testid="stBaseButton-secondary"]:hover,
    [data-testid="stBaseButton-primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 28px var(--accent-glow) !important;
        background: var(--accent-light) !important;
        filter: brightness(1.1) !important;
    }
    .stButton > button:active,
    [data-testid="stFormSubmitButton"] button:active,
    [data-testid="stBaseButton-secondary"]:active,
    [data-testid="stBaseButton-primary"]:active { transform: translateY(0) !important; }

    /* Secondary button */
    .btn-secondary > button {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        color: var(--text-secondary) !important;
    }
    .btn-secondary > button * {
        color: var(--text-secondary) !important;
    }
    .btn-secondary > button:hover {
        border-color: var(--accent) !important;
        color: var(--accent-light) !important;
        box-shadow: none !important;
        background: var(--badge-danger-bg) !important;
    }
    .btn-secondary > button:hover * {
        color: var(--accent-light) !important;
    }

    /* - Selectbox - */
    [data-testid="stSelectbox"] > div > div {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
    }

    /* - Tabs - */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--tabs-bg) !important;
        border-radius: var(--radius-md) !important;
        padding: 4px !important;
        gap: 4px !important;
        border: 1px solid var(--border) !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-secondary) !important;
        font-family: var(--font-body) !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        padding: 0.5rem 1.1rem !important;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        background: var(--accent) !important;
        color: #fff !important;
        font-weight: 600 !important;
    }

    /* - Spinner / Loading - */
    .stSpinner > div { border-top-color: var(--accent) !important; }

    /* - Horizontal Rule - */
    hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }

    /* - Code - */
    code {
        background: var(--accent-soft) !important;
        color: var(--accent-light) !important;
        border-radius: 4px !important;
        font-family: var(--font-mono) !important;
        font-size: 0.82rem !important;
        padding: 0.15em 0.45em !important;
    }

    /* - Expander - */
    .streamlit-expanderHeader {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
        font-family: var(--font-body) !important;
    }
    .streamlit-expanderContent {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border) !important;
        border-top: none !important;
    }

    /* - Plotly chart container - */
    .js-plotly-plot .plotly { background: transparent !important; }

    /* - Divider with text - */
    .divider-text {
        display: flex;
        align-items: center;
        gap: 12px;
        color: var(--text-muted);
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin: 1.5rem 0;
    }
    .divider-text::before, .divider-text::after {
        content: '';
        flex: 1;
        height: 1px;
        background: var(--border);
    }

    /* - Animations - */
    @keyframes fadeSlideUp {
        from { opacity: 0; transform: translateY(18px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeSlideDown {
        from { opacity: 0; transform: translateY(-12px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to   { opacity: 1; }
    }
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 20px var(--accent-glow); }
        50%       { box-shadow: 0 0 40px var(--pulse-shadow); }
    }
    @keyframes shimmer {
        0%   { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

    .animate-fade { animation: fadeIn 0.5s ease both; }
    .animate-up   { animation: fadeSlideUp 0.5s ease both; }
    .pulse-glow   { animation: pulse-glow 2.5s ease-in-out infinite; }

    /* - Loading skeleton - */
    .skeleton {
        background: linear-gradient(90deg, var(--bg-card) 25%, var(--badge-danger-bg) 50%, var(--bg-card) 75%);
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
        border-radius: var(--radius-sm);
        height: 16px;
        margin-bottom: 8px;
    }

    /* - Hero gradient orbs - */
    /* - Column spacing - */
    [data-testid="column"] { padding: 0 0.5rem !important; }

    /* - Alert / Info boxes - */
    .stAlert {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-primary) !important;
    }

    /* - Number inputs - */
    .stNumberInput input {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        color: var(--text-primary) !important;
    }

    /* - Slider - */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background: var(--accent) !important;
        border-color: var(--accent) !important;
    }

    /* - Checkbox / Radio - */
    .stCheckbox label, .stRadio label {
        color: var(--text-secondary) !important;
        font-family: var(--font-body) !important;
    }

    /* Dataframe */
    .stDataFrame { border-radius: var(--radius-md) !important; overflow: hidden !important; }


    </style>
    """, unsafe_allow_html=True)
