"""
Matching Dashboard — pick a missing person, run the combined text + facial
matching engine against all unidentified body records, and see the ranked
results with a full score breakdown.

Note: facial comparison can take a few seconds per pair the first time
(DeepFace loading the model), so this page may feel slower than before —
that's expected, not a bug.
"""
import streamlit as st
from database import fetch_all_missing_persons_as_dicts, fetch_all_unidentified_bodies_as_dicts, save_match
from matching import find_top_matches_for_missing_person

st.set_page_config(page_title="Matching Dashboard", page_icon="🔍", layout="wide")
st.title("🔍 Matching Dashboard")

missing_persons = fetch_all_missing_persons_as_dicts()
unidentified_bodies = fetch_all_unidentified_bodies_as_dicts()

if not missing_persons:
    st.info("No missing person records yet. Add one from the Police Form page first.")
    st.stop()

if not unidentified_bodies:
    st.info("No unidentified body records yet. Add one from the Hospital Form page first.")
    st.stop()

# Let the user pick which missing-person record to find matches for
options = {f"#{p['id']} — {p['name']} ({p['age']}, {p['gender']})": p for p in missing_persons}
selected_label = st.selectbox("Select a missing person record to find matches for:", options.keys())
selected_person = options[selected_label]

st.divider()

col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("Selected Record")
    if selected_person.get("photo_path"):
        try:
            st.image(selected_person["photo_path"], width=200)
        except Exception:
            st.caption("(photo not found on disk)")
    st.write(f"**Name:** {selected_person['name']}")
    st.write(f"**Age:** {selected_person['age']}  |  **Gender:** {selected_person['gender']}")
    st.write(f"**Last Seen:** {selected_person['last_seen_location']} on {selected_person['last_seen_date']}")
    st.write(f"**Marks:** {selected_person.get('distinguishing_marks') or '—'}")
    st.write(f"**Clothing:** {selected_person.get('clothing_description') or '—'}")

with col2:
    st.subheader("Top Matches")
    top_matches = find_top_matches_for_missing_person(selected_person, unidentified_bodies, top_n=5)

    if not top_matches:
        st.write("No candidate records found.")
    else:
        for match in top_matches:
            score = match["final_score"]
            # simple visual cue: color-code the score
            if score >= 70:
                badge = "🟢"
            elif score >= 40:
                badge = "🟡"
            else:
                badge = "🔴"

            with st.expander(f"{badge} Body #{match['id']} — Match Score: {score}%"):
                mcol1, mcol2 = st.columns([1, 2])
                with mcol1:
                    if match.get("photo_path"):
                        try:
                            st.image(match["photo_path"], width=150)
                        except Exception:
                            st.caption("(photo not found on disk)")
                with mcol2:
                    st.write(f"**Found at:** {match['found_location']} on {match['found_date']}")
                    st.write(f"**Approx age:** {match.get('approx_age')}  |  **Gender:** {match.get('gender')}")
                    st.write(f"**Marks:** {match.get('distinguishing_marks') or '—'}")
                    st.write(f"**Clothing:** {match.get('clothing_description') or '—'}")

                    face_display = match["face_score"] if match["face_score"] is not None else "N/A (no face detected or photo missing)"
                    st.caption(
                        f"Text score: {match['text_final_score']}  |  Face score: {face_display}"
                    )
                    st.caption(
                        f"Text breakdown — Age: {match['age_score']} | "
                        f"Gender: {match['gender_score']} | "
                        f"Location: {match['location_score']} | "
                        f"Marks: {match['marks_score']} | "
                        f"Clothing: {match['clothing_score']}"
                    )

                if st.button(f"Save this as a candidate match", key=f"save_{match['id']}"):
                    save_match(
                        missing_person_id=selected_person["id"],
                        unidentified_body_id=match["id"],
                        text_score=match["text_final_score"],
                        face_score=match["face_score"] if match["face_score"] is not None else 0,
                        final_score=score,
                    )
                    st.success("Saved to matches table. Staff can confirm this later.")