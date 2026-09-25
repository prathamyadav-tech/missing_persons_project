"""
Hospital Form — report an unidentified body.
"""
import os
import uuid
import streamlit as st
from database import insert_unidentified_body

st.set_page_config(page_title="Hospital Form", page_icon="🏥")
st.title("🏥 Report an Unidentified Body")

UPLOAD_DIR = "uploads/unidentified"
os.makedirs(UPLOAD_DIR, exist_ok=True)

with st.form("unidentified_body_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        approx_age = st.number_input("Approximate Age", min_value=0, max_value=120, step=1)
        gender = st.selectbox("Gender", ["Male", "Female", "Other", "Unknown"])
        height_cm = st.number_input("Height (cm)", min_value=0, max_value=250, step=1)

    with col2:
        found_location = st.text_input("Found Location *")
        found_date = st.date_input("Found Date *")
        reported_by = st.text_input("Reported By (Hospital / Mortuary Name) *")

    distinguishing_marks = st.text_area(
        "Distinguishing Marks",
        placeholder="e.g. scar on left cheek, tattoo on right forearm"
    )
    clothing_description = st.text_area(
        "Clothing Description (found wearing)",
        placeholder="e.g. blue shirt, black jeans"
    )
    photo = st.file_uploader("Upload Photo *", type=["jpg", "jpeg", "png"])

    submitted = st.form_submit_button("Submit Report")

    if submitted:
        if not found_location or not reported_by or photo is None:
            st.error("Please fill all required fields (*) and upload a photo.")
        else:
            ext = photo.name.split(".")[-1]
            filename = f"{uuid.uuid4().hex}.{ext}"
            photo_path = os.path.join(UPLOAD_DIR, filename)
            with open(photo_path, "wb") as f:
                f.write(photo.getbuffer())

            data = {
                "approx_age": int(approx_age) if approx_age else None,
                "gender": gender,
                "found_location": found_location,
                "found_date": found_date,
                "photo_path": photo_path,
                "height_cm": int(height_cm) if height_cm else None,
                "distinguishing_marks": distinguishing_marks,
                "clothing_description": clothing_description,
                "reported_by": reported_by,
            }

            try:
                new_id = insert_unidentified_body(data)
                st.success(f"Report submitted successfully. Record ID: {new_id}")
            except Exception as e:
                st.error(f"Database error: {e}")
