"""
View Records — quick pandas-powered table view of both tables.
(The matching dashboard comes later in Week 2 — this page is just for
checking that data entry + DB storage is working correctly.)
"""
import streamlit as st
from database import fetch_missing_persons, fetch_unidentified_bodies
from style import inject_custom_css, page_header

st.set_page_config(page_title="View Records", page_icon="📋", layout="wide")
inject_custom_css()
page_header("📋 All Records", "Browse every report currently in the system")

tab1, tab2 = st.tabs(["Missing Persons", "Unidentified Bodies"])

with tab1:
    df_missing = fetch_missing_persons()
    c1, c2, c3 = st.columns(3)
    c1.metric("Total", len(df_missing))
    c2.metric("Open", len(df_missing[df_missing["status"] == "Open"]) if not df_missing.empty else 0)
    c3.metric("Matched", len(df_missing[df_missing["status"] == "Matched"]) if not df_missing.empty else 0)
    if not df_missing.empty:
        st.dataframe(df_missing, use_container_width=True)
    else:
        st.info("No missing person records yet. Add one from the Police Form page.")

with tab2:
    df_unidentified = fetch_unidentified_bodies()
    c1, c2, c3 = st.columns(3)
    c1.metric("Total", len(df_unidentified))
    c2.metric("Open", len(df_unidentified[df_unidentified["status"] == "Open"]) if not df_unidentified.empty else 0)
    c3.metric("Matched", len(df_unidentified[df_unidentified["status"] == "Matched"]) if not df_unidentified.empty else 0)
    if not df_unidentified.empty:
        st.dataframe(df_unidentified, use_container_width=True)
    else:
        st.info("No unidentified body records yet. Add one from the Hospital Form page.")
