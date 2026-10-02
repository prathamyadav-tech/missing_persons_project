"""
style.py
Shared custom CSS for the whole app. Call inject_custom_css() at the top
of every page (after st.set_page_config) to apply consistent styling.

This works by injecting raw CSS into the page via st.markdown with
unsafe_allow_html=True — the standard way to customize Streamlit's look
beyond what config.toml alone can do.
"""
import streamlit as st

NAVY = "#1E2761"
ACCENT = "#3B4FA0"
ICE = "#CADCFC"
MUTED = "#5A6178"


def inject_custom_css():
    st.markdown(f"""
    <style>
        /* Overall page padding */
        .block-container {{
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1100px;
        }}

        /* Headings */
        h1 {{
            color: {NAVY};
            font-weight: 800;
            letter-spacing: -0.5px;
        }}
        h2, h3 {{
            color: {NAVY};
            font-weight: 700;
        }}

        /* Sidebar */
        [data-testid="stSidebar"] {{
            background-color: {NAVY};
        }}
        [data-testid="stSidebar"] * {{
            color: #FFFFFF !important;
        }}
        [data-testid="stSidebar"] .st-emotion-cache-1wmy9hl,
        [data-testid="stSidebar"] a {{
            color: #E8ECFB !important;
        }}

        /* Buttons */
        .stButton > button {{
            background-color: {ACCENT};
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.5rem 1.2rem;
            font-weight: 600;
            transition: all 0.15s ease;
        }}
        .stButton > button:hover {{
            background-color: {NAVY};
            color: white;
            transform: translateY(-1px);
        }}

        /* Form submit buttons */
        .stFormSubmitButton > button {{
            background-color: {NAVY};
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.6rem 1.5rem;
            font-weight: 700;
            width: 100%;
        }}
        .stFormSubmitButton > button:hover {{
            background-color: {ACCENT};
        }}

        /* Expander (used heavily in the matching dashboard) */
        [data-testid="stExpander"] {{
            border: 1px solid #E2E6F5;
            border-radius: 10px;
            background-color: #FAFBFF;
        }}

        /* Metric-like cards */
        .custom-card {{
            background-color: #F4F6FC;
            border-radius: 12px;
            padding: 1.2rem 1.4rem;
            border: 1px solid #E2E6F5;
        }}

        /* Status badge pills */
        .badge {{
            display: inline-block;
            padding: 0.2rem 0.7rem;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 700;
        }}
        .badge-open {{ background-color: #FFF1D6; color: #916A00; }}
        .badge-matched {{ background-color: #D8EAFF; color: {NAVY}; }}
        .badge-resolved {{ background-color: #D6F5E0; color: #146C2E; }}

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
        }}
        .stTabs [data-baseweb="tab"] {{
            background-color: #F4F6FC;
            border-radius: 8px 8px 0 0;
            padding: 0.5rem 1.2rem;
            font-weight: 600;
        }}
        .stTabs [aria-selected="true"] {{
            background-color: {ACCENT};
            color: white !important;
        }}

        /* Dataframe header */
        [data-testid="stDataFrame"] {{
            border-radius: 10px;
            overflow: hidden;
        }}
    </style>
    """, unsafe_allow_html=True)


def status_badge(status: str) -> str:
    """Returns an HTML pill badge for a record's status. Use with st.markdown(..., unsafe_allow_html=True)."""
    css_class = {
        "Open": "badge-open",
        "Matched": "badge-matched",
        "Resolved": "badge-resolved",
    }.get(status, "badge-open")
    return f'<span class="badge {css_class}">{status}</span>'


def page_header(title: str, subtitle: str = ""):
    """Consistent page header used across all pages instead of plain st.title()."""
    st.markdown(f"""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="margin-bottom: 0.2rem;">{title}</h1>
        {f'<p style="color: {MUTED}; font-size: 1.05rem; margin-top:0;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)
