"""
matching.py
Text-based matching engine.

Compares a missing_persons record against an unidentified_bodies record
and returns a 0-100 similarity score based on:
  - age closeness
  - gender match
  - location similarity (fuzzy string match)
  - physical features / distinguishing marks similarity (fuzzy string match)

This is intentionally simple and explainable — every score is easy to
justify in a viva, which matters more for a minor project than a fancier
black-box model.
"""
from rapidfuzz import fuzz

# Weights for each component. Must sum to 1.0 — tune these if you want
# one signal (e.g. distinguishing marks) to matter more than another.
WEIGHTS = {
    "age": 0.20,
    "gender": 0.15,
    "location": 0.25,
    "marks": 0.25,
    "clothing": 0.15,
}


def score_age(age1, age2, max_diff=15):
    """
    Returns 0-100. Full score if ages match exactly, decreasing linearly
    up to max_diff years apart, 0 beyond that.
    Handles None gracefully (missing data = neutral middling score).
    """
    if age1 is None or age2 is None:
        return 50  # neutral score when age data is missing
    diff = abs(age1 - age2)
    if diff >= max_diff:
        return 0
    return round(100 * (1 - diff / max_diff), 2)


def score_gender(gender1, gender2):
    """Binary-ish: 100 if match, 0 if a clear mismatch, 50 if either is Unknown."""
    if not gender1 or not gender2:
        return 50
    if gender1 == "Unknown" or gender2 == "Unknown":
        return 50
    return 100 if gender1 == gender2 else 0


def score_text_similarity(text1, text2):
    """
    Fuzzy string similarity for free-text fields (location, marks, clothing).
    Uses token_sort_ratio so word order doesn't matter
    (e.g. "scar left cheek" vs "left cheek has a scar" still score high).
    """
    if not text1 or not text2:
        return 0
    return round(fuzz.token_sort_ratio(str(text1).lower(), str(text2).lower()), 2)


def compute_text_score(missing_person: dict, unidentified_body: dict) -> dict:
    """
    Takes two dict-like records (rows from the DB) and returns a breakdown
    plus a final weighted score out of 100.
    """
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

    final_score = (
        age_score * WEIGHTS["age"]
        + gender_score * WEIGHTS["gender"]
        + location_score * WEIGHTS["location"]
        + marks_score * WEIGHTS["marks"]
        + clothing_score * WEIGHTS["clothing"]
    )

    return {
        "age_score": age_score,
        "gender_score": gender_score,
        "location_score": location_score,
        "marks_score": marks_score,
        "clothing_score": clothing_score,
        "final_score": round(final_score, 2),
    }


def find_top_matches_for_missing_person(missing_person: dict, unidentified_bodies: list, top_n: int = 5):
    """
    missing_person: a single dict (one row)
    unidentified_bodies: list of dicts (all candidate rows)
    Returns a list of dicts sorted by final_score descending, each including
    the original unidentified_body data plus its score breakdown.
    """
    results = []
    for body in unidentified_bodies:
        breakdown = compute_text_score(missing_person, body)
        results.append({**body, **breakdown})

    results.sort(key=lambda r: r["final_score"], reverse=True)
    return results[:top_n]
