"""
matching.py
Combined text + facial matching engine.

Compares a missing_persons record against an unidentified_bodies record
and returns a 0-100 similarity score based on:
  - TEXT: age closeness, gender match, location/marks/clothing fuzzy similarity
  - FACE: DeepFace facial similarity between the two uploaded photos

The two are combined into one final weighted score. Facial comparison is
wrapped in error handling — if a photo is missing, corrupted, or no face
is detected, we fall back to text-only for that pair instead of crashing.
"""
from rapidfuzz import fuzz
from deepface import DeepFace
import os

# ---------- TEXT SCORE WEIGHTS (within the text score itself, sums to 1.0) ----------
TEXT_WEIGHTS = {
    "age": 0.20,
    "gender": 0.15,
    "location": 0.25,
    "marks": 0.25,
    "clothing": 0.15,
}

# ---------- OVERALL COMBINATION: how much text vs face counts in the final score ----------
OVERALL_WEIGHTS = {
    "text": 0.5,
    "face": 0.5,
}

FACE_MODEL = "VGG-Face"  # same model we validated in test_deepface.py


def score_age(age1, age2, max_diff=15):
    if age1 is None or age2 is None:
        return 50
    diff = abs(age1 - age2)
    if diff >= max_diff:
        return 0
    return round(100 * (1 - diff / max_diff), 2)


def score_gender(gender1, gender2):
    if not gender1 or not gender2:
        return 50
    if gender1 == "Unknown" or gender2 == "Unknown":
        return 50
    return 100 if gender1 == gender2 else 0


def score_text_similarity(text1, text2):
    if not text1 or not text2:
        return 0
    return round(fuzz.token_sort_ratio(str(text1).lower(), str(text2).lower()), 2)


def compute_text_score(missing_person: dict, unidentified_body: dict) -> dict:
    """Returns a breakdown dict plus 'text_final_score' (0-100)."""
    age_score = score_age(missing_person.get("age"), unidentified_body.get("approx_age"))
    gender_score = score_gender(missing_person.get("gender"), unidentified_body.get("gender"))
    location_score = score_text_similarity(
        missing_person.get("last_seen_location"), unidentified_body.get("found_location")
    )
    marks_score = score_text_similarity(
        missing_person.get("distinguishing_marks"), unidentified_body.get("distinguishing_marks")
    )
    clothing_score = score_text_similarity(
        missing_person.get("clothing_description"), unidentified_body.get("clothing_description")
    )

    text_final_score = (
        age_score * TEXT_WEIGHTS["age"]
        + gender_score * TEXT_WEIGHTS["gender"]
        + location_score * TEXT_WEIGHTS["location"]
        + marks_score * TEXT_WEIGHTS["marks"]
        + clothing_score * TEXT_WEIGHTS["clothing"]
    )

    return {
        "age_score": age_score,
        "gender_score": gender_score,
        "location_score": location_score,
        "marks_score": marks_score,
        "clothing_score": clothing_score,
        "text_final_score": round(text_final_score, 2),
    }


def compute_face_score(photo_path1: str, photo_path2: str):
    """
    Returns a 0-100 facial similarity score, or None if comparison wasn't
    possible (missing file, no face detected, corrupted image, etc).
    None is handled gracefully by the caller — it just falls back to text-only.
    """
    if not photo_path1 or not photo_path2:
        return None
    if not os.path.exists(photo_path1) or not os.path.exists(photo_path2):
        return None

    try:
        result = DeepFace.verify(
            img1_path=photo_path1,
            img2_path=photo_path2,
            model_name=FACE_MODEL,
            enforce_detection=False,  # don't crash on hard-to-detect faces —
                                      # important for real-world photo quality
        )
        distance = result["distance"]
        threshold = result["threshold"]
        similarity_pct = max(0, round((1 - (distance / (threshold * 2))) * 100, 2))
        return similarity_pct
    except Exception:
        # Any DeepFace/OpenCV failure (corrupted file, no face found, etc.)
        # degrades gracefully to "no face score available" rather than crashing
        # the whole matching run.
        return None


def compute_combined_score(missing_person: dict, unidentified_body: dict) -> dict:
    """
    Full breakdown: text sub-scores + text_final_score + face_score + final_score.
    If face_score is None (comparison failed), final_score falls back to
    text_final_score alone so one bad photo doesn't zero out a real match.
    """
    text_result = compute_text_score(missing_person, unidentified_body)
    face_score = compute_face_score(
        missing_person.get("photo_path"), unidentified_body.get("photo_path")
    )

    if face_score is None:
        final_score = text_result["text_final_score"]
    else:
        final_score = (
            text_result["text_final_score"] * OVERALL_WEIGHTS["text"]
            + face_score * OVERALL_WEIGHTS["face"]
        )

    return {
        **text_result,
        "face_score": face_score,  # None if unavailable — shown as "N/A" in UI
        "final_score": round(final_score, 2),
    }


def find_top_matches_for_missing_person(missing_person: dict, unidentified_bodies: list, top_n: int = 5):
    """
    missing_person: a single dict (one row)
    unidentified_bodies: list of dicts (all candidate rows)
    Returns a list of dicts sorted by final_score descending, each including
    the original unidentified_body data plus its full score breakdown.
    """
    results = []
    for body in unidentified_bodies:
        breakdown = compute_combined_score(missing_person, body)
        results.append({**body, **breakdown})

    results.sort(key=lambda r: r["final_score"], reverse=True)
    return results[:top_n]