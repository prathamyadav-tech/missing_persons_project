"""
View Records — quick pandas-powered table view of both tables.
(The matching dashboard comes later in Week 2 — this page is just for
checking that data entry + DB storage is working correctly.)
"""
import streamlit as st
from database import fetch_missing_persons, fetch_unidentified_bodies

st.set_page_config(page_title="View Records", page_icon="📋", layout="wide")
st.title("📋 All Records")

tab1, tab2 = st.tabs(["Missing Persons", "Unidentified Bodies"])

with tab1:
    df_missing = fetch_missing_persons()
    st.write(f"Total records: {len(df_missing)}")
    if not df_missing.empty:
        st.dataframe(df_missing, use_container_width=True)
    else:
        st.info("No missing person records yet. Add one from the Police Form page.")

with tab2:
    df_unidentified = fetch_unidentified_bodies()
    st.write(f"Total records: {len(df_unidentified)}")
    if not df_unidentified.empty:
        st.dataframe(df_unidentified, use_container_width=True)
    else:
        st.info("No unidentified body records yet. Add one from the Hospital Form page.")
