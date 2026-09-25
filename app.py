"""
app.py — Home page of the Missing Persons <-> Unidentified Bodies matching platform.
Run with:  streamlit run app.py
Streamlit automatically picks up files in the pages/ folder as extra pages
in the sidebar, so you don't need to wire up navigation manually.
"""
import streamlit as st

st.set_page_config(
    page_title="Missing Persons Matching Platform",
    page_icon="🔎",
    layout="wide",
)

st.title("🔎 Missing Persons ↔ Unidentified Bodies Matching Platform")

st.markdown("""
### About this project
India records lakhs of missing-person cases every year, and thousands of
unidentified bodies are never matched back to a missing-person report —
because the two records live in different systems (police vs. hospital/mortuary)
that never talk to each other.

This platform lets police and hospital staff log new records (without touching
Aadhaar or biometric data, which is legally restricted) and uses **text-based
scoring + facial similarity** to suggest possible matches. A human always
confirms the final match — the system only suggests.

**Use the sidebar to navigate:**
- 🚓 **Police Form** — report a missing person
- 🏥 **Hospital Form** — report an unidentified body
- 📊 **Dashboard** — view records and possible matches
""")

st.info("This is a minor project prototype. Data entered here is for demo purposes only.")
