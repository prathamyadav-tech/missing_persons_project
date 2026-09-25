"""
Police Form — report a missing person.
Streamlit picks this up automatically as a sidebar page (filename prefix
controls the order: 1_, 2_, 3_ ...).
"""
import os
import uuid
import streamlit as st
from database import insert_missing_person

st.set_page_config(page_title="Police Form", page_icon="🚓")
st.title("🚓 Report a Missing Person")

UPLOAD_DIR = "uploads/missing"
os.makedirs(UPLOAD_DIR, exist_ok=True)

with st.form("missing_person_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Full Name *")
        age = st.number_input("Age *", min_value=0, max_value=120, step=1)
        gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
        height_cm = st.number_input("Height (cm)", min_value=0, max_value=250, step=1)

    with col2:
        last_seen_location = st.text_input("Last Seen Location *")
        last_seen_date = st.date_input("Last Seen Date *")
        reported_by = st.text_input("Reported By (Police Station / Officer) *")

    distinguishing_marks = st.text_area(
        "Distinguishing Marks",
        placeholder="e.g. scar on left cheek, tattoo on right forearm, mole near right eye"
    )
    clothing_description = st.text_area(
        "Clothing Description (last seen wearing)",
        placeholder="e.g. blue shirt, black jeans"
    )
    photo = st.file_uploader("Upload Photo *", type=["jpg", "jpeg", "png"])

    submitted = st.form_submit_button("Submit Report")

    if submitted:
        # basic validation
        if not name or not last_seen_location or not reported_by or photo is None:
            st.error("Please fill all required fields (*) and upload a photo.")
        else:
            # save photo with a unique filename to avoid collisions
            ext = photo.name.split(".")[-1]
            filename = f"{uuid.uuid4().hex}.{ext}"
            photo_path = os.path.join(UPLOAD_DIR, filename)
            with open(photo_path, "wb") as f:
                f.write(photo.getbuffer())

            data = {
                "name": name,
                "age": int(age),
                "gender": gender,
                "last_seen_location": last_seen_location,
                "last_seen_date": last_seen_date,
                "photo_path": photo_path,
                "height_cm": int(height_cm) if height_cm else None,
                "distinguishing_marks": distinguishing_marks,
                "clothing_description": clothing_description,
                "reported_by": reported_by,
            }

            try:
                new_id = insert_missing_person(data)
                st.success(f"Report submitted successfully. Record ID: {new_id}")
            except Exception as e:
                st.error(f"Database error: {e}")
