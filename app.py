"""
app.py — Home page of the Missing Persons <-> Unidentified Bodies matching platform.
Run with:  streamlit run app.py
"""
import streamlit as st
from style import inject_custom_css

st.set_page_config(
    page_title="Missing Persons Matching Platform",
    page_icon="🔎",
    layout="wide",
)
inject_custom_css()

# ---------- HERO SECTION ----------
st.markdown("""
<div style="background: linear-gradient(135deg, #1E2761 0%, #3B4FA0 100%);
            border-radius: 16px; padding: 2.8rem 2.5rem; margin-bottom: 2rem;">
    <p style="color: #CADCFC; font-weight: 700; letter-spacing: 2px; font-size: 0.85rem; margin-bottom: 0.5rem;">
        AI-POWERED PUBLIC SAFETY PLATFORM
    </p>
    <h1 style="color: white; font-size: 2.6rem; margin: 0 0 0.6rem 0;">
        🔎 Missing Persons ↔ Unidentified Bodies
    </h1>
    <p style="color: #E8ECFB; font-size: 1.1rem; max-width: 700px; margin: 0;">
        Connecting police and hospital records using facial and physical-description
        matching — without touching Aadhaar or biometric data.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------- STAT CARDS ----------
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="custom-card">
        <p style="color:#5A6178; font-size:0.85rem; font-weight:700; margin-bottom:0.3rem;">REPORTED MISSING (2023)</p>
        <p style="font-size:1.8rem; font-weight:800; color:#1E2761; margin:0;">8.68 Lakh</p>
        <p style="color:#5A6178; font-size:0.85rem; margin-top:0.3rem;">Only 53% ever traced</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="custom-card">
        <p style="color:#5A6178; font-size:0.85rem; font-weight:700; margin-bottom:0.3rem;">UNIDENTIFIED BODIES / YEAR</p>
        <p style="font-size:1.8rem; font-weight:800; color:#1E2761; margin:0;">~50,000</p>
        <p style="color:#5A6178; font-size:0.85rem; margin-top:0.3rem;">80-90% never identified</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="custom-card">
        <p style="color:#5A6178; font-size:0.85rem; font-weight:700; margin-bottom:0.3rem;">OUR APPROACH</p>
        <p style="font-size:1.8rem; font-weight:800; color:#1E2761; margin:0;">0% Aadhaar</p>
        <p style="color:#5A6178; font-size:0.85rem; margin-top:0.3rem;">Fully legally compliant</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# ---------- NAVIGATION CARDS ----------
st.markdown("### Get Started")
nav1, nav2, nav3 = st.columns(3)
with nav1:
    st.markdown("""
    <div class="custom-card" style="text-align:center; padding: 1.8rem 1rem;">
        <p style="font-size:2rem; margin:0;">🚓</p>
        <p style="font-weight:700; color:#1E2761; margin:0.3rem 0;">Police Form</p>
        <p style="color:#5A6178; font-size:0.85rem;">Report a missing person</p>
    </div>
    """, unsafe_allow_html=True)
with nav2:
    st.markdown("""
    <div class="custom-card" style="text-align:center; padding: 1.8rem 1rem;">
        <p style="font-size:2rem; margin:0;">🏥</p>
        <p style="font-weight:700; color:#1E2761; margin:0.3rem 0;">Hospital Form</p>
        <p style="color:#5A6178; font-size:0.85rem;">Report an unidentified body</p>
    </div>
    """, unsafe_allow_html=True)
with nav3:
    st.markdown("""
    <div class="custom-card" style="text-align:center; padding: 1.8rem 1rem;">
        <p style="font-size:2rem; margin:0;">📊</p>
        <p style="font-weight:700; color:#1E2761; margin:0.3rem 0;">Dashboard</p>
        <p style="color:#5A6178; font-size:0.85rem;">View matches and records</p>
    </div>
    """, unsafe_allow_html=True)

st.info("👈 Use the sidebar to navigate between pages.")

st.write("")
st.markdown("### How It Works")
st.markdown("""
1. **Report** — Police and hospital staff log new records with a photo and physical description (under 2 minutes, no training needed)
2. **Match** — Our engine compares every new record against existing ones using text similarity (age, location, marks) + facial recognition
3. **Review** — Staff see ranked, scored match suggestions on the dashboard
4. **Confirm** — A human always makes the final call — the system only suggests, never decides
""")


