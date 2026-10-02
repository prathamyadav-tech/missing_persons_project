"""
Matching Dashboard — two tabs:
  1. Find Matches: pick a missing person, run the matching engine, save candidates
  2. Review Queue: see all saved candidate matches, confirm or reject them

Note: facial comparison can take a few seconds per pair the first time
(DeepFace loading the model), so Tab 1 may feel slower than text-only did —
that's expected, not a bug.
"""
import streamlit as st
from database import (
    fetch_all_missing_persons_as_dicts,
    fetch_all_unidentified_bodies_as_dicts,
    save_match,
    fetch_all_saved_matches,
    confirm_match,
)
from matching import find_top_matches_for_missing_person
from style import inject_custom_css, page_header, status_badge

st.set_page_config(page_title="Matching Dashboard", page_icon="🔍", layout="wide")
inject_custom_css()
page_header("🔍 Matching Dashboard", "Find candidate matches and review pending confirmations")

tab1, tab2 = st.tabs(["🔎 Find Matches", "✅ Review Queue"])

# ============================================================
# TAB 1: FIND MATCHES (search + save candidates)
# ============================================================
with tab1:
    missing_persons = fetch_all_missing_persons_as_dicts()
    unidentified_bodies = fetch_all_unidentified_bodies_as_dicts()

    if not missing_persons:
        st.info("No missing person records yet. Add one from the Police Form page first.")
    elif not unidentified_bodies:
        st.info("No unidentified body records yet. Add one from the Hospital Form page first.")
    else:
        options = {
            f"#{p['id']} — {p['name']} ({p['age']}, {p['gender']}) [{p['status']}]": p
            for p in missing_persons
        }
        selected_label = st.selectbox("Select a missing person record to find matches for:", options.keys())
        selected_person = options[selected_label]

        st.divider()
        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader("Selected Record")
            st.markdown(f"**Status:** {status_badge(selected_person['status'])}", unsafe_allow_html=True)
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
            with st.spinner("Running text + facial matching..."):
                top_matches = find_top_matches_for_missing_person(selected_person, unidentified_bodies, top_n=5)

            if not top_matches:
                st.write("No candidate records found.")
            else:
                for match in top_matches:
                    score = match["final_score"]
                    badge = "🟢" if score >= 70 else "🟡" if score >= 40 else "🔴"

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

                            face_display = match["face_score"] if match["face_score"] is not None else "N/A"
                            st.caption(f"Text score: {match['text_final_score']}  |  Face score: {face_display}")
                            st.caption(
                                f"Breakdown — Age: {match['age_score']} | Gender: {match['gender_score']} | "
                                f"Location: {match['location_score']} | Marks: {match['marks_score']} | "
                                f"Clothing: {match['clothing_score']}"
                            )

                        if st.button("Save this as a candidate match", key=f"save_{match['id']}"):
                            save_match(
                                missing_person_id=selected_person["id"],
                                unidentified_body_id=match["id"],
                                text_score=match["text_final_score"],
                                face_score=match["face_score"] if match["face_score"] is not None else 0,
                                final_score=score,
                            )
                            st.success("Saved to review queue — see the 'Review Queue' tab to confirm it.")

# ============================================================
# TAB 2: REVIEW QUEUE (confirm or inspect saved matches)
# ============================================================
with tab2:
    st.subheader("Saved Candidate Matches")

    filter_choice = st.radio("Show:", ["Pending only", "Confirmed only", "All"], horizontal=True)
    confirmed_filter = {"Pending only": False, "Confirmed only": True, "All": None}[filter_choice]

    saved = fetch_all_saved_matches(confirmed=confirmed_filter)

    if saved.empty:
        st.info("No saved matches here yet. Save some from the 'Find Matches' tab first.")
    else:
        for _, row in saved.iterrows():
            status_badge = "✅ Confirmed" if row["confirmed"] else "⏳ Pending Review"
            with st.expander(
                f"{status_badge} — {row['missing_name']} ↔ Body #{row['unidentified_body_id']} "
                f"— Final Score: {row['final_score']}%"
            ):
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.write("**Missing Person**")
                    if row.get("missing_photo"):
                        try:
                            st.image(row["missing_photo"], width=140)
                        except Exception:
                            pass
                    st.write(f"{row['missing_name']}, {row['missing_age']}, {row['missing_gender']}")

                with c2:
                    st.write("**Unidentified Body**")
                    if row.get("body_photo"):
                        try:
                            st.image(row["body_photo"], width=140)
                        except Exception:
                            pass
                    st.write(f"Found at {row['found_location']}, approx age {row['body_age']}, {row['body_gender']}")

                with c3:
                    st.write("**Scores**")
                    st.write(f"Text: {row['text_score']}")
                    st.write(f"Face: {row['face_score']}")
                    st.write(f"**Final: {row['final_score']}**")
                    st.caption(f"Saved: {row['created_at']}")

                if not row["confirmed"]:
                    st.warning(
                        "Confirming marks both records as 'Matched'. Only confirm after real-world "
                        "verification (family ID, DNA, dental records) — a high score is a lead, not proof."
                    )
                    if st.button("✅ Confirm This Match", key=f"confirm_{row['match_id']}"):
                        confirm_match(row["match_id"])
                        st.success("Match confirmed. Records updated to 'Matched' status.")
                        st.rerun()
                else:
                    st.success("This match has been confirmed.")
