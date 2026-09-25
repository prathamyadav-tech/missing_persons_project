"""
database.py
All MySQL access goes through this file so the Streamlit pages stay clean.
"""
import mysql.connector
import pandas as pd
from db_config import DB_CONFIG


def get_connection():
    """Open a fresh MySQL connection."""
    return mysql.connector.connect(**DB_CONFIG)


# ---------- INSERT FUNCTIONS ----------

def insert_missing_person(data: dict) -> int:
    """
    data keys: name, age, gender, last_seen_location, last_seen_date,
               photo_path, height_cm, distinguishing_marks,
               clothing_description, reported_by
    Returns the new row's id.
    """
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO missing_persons
        (name, age, gender, last_seen_location, last_seen_date, photo_path,
         height_cm, distinguishing_marks, clothing_description, reported_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        data["name"], data["age"], data["gender"], data["last_seen_location"],
        data["last_seen_date"], data["photo_path"], data["height_cm"],
        data["distinguishing_marks"], data["clothing_description"], data["reported_by"],
    )
    cursor.execute(query, values)
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return new_id


def insert_unidentified_body(data: dict) -> int:
    """
    data keys: approx_age, gender, found_location, found_date, photo_path,
               height_cm, distinguishing_marks, clothing_description, reported_by
    Returns the new row's id.
    """
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO unidentified_bodies
        (approx_age, gender, found_location, found_date, photo_path,
         height_cm, distinguishing_marks, clothing_description, reported_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        data["approx_age"], data["gender"], data["found_location"], data["found_date"],
        data["photo_path"], data["height_cm"], data["distinguishing_marks"],
        data["clothing_description"], data["reported_by"],
    )
    cursor.execute(query, values)
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return new_id


# ---------- FETCH FUNCTIONS ----------

def fetch_missing_persons(status: str = None) -> pd.DataFrame:
    conn = get_connection()
    query = "SELECT * FROM missing_persons"
    params = ()
    if status:
        query += " WHERE status = %s"
        params = (status,)
    query += " ORDER BY created_at DESC"
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df


def fetch_unidentified_bodies(status: str = None) -> pd.DataFrame:
    conn = get_connection()
    query = "SELECT * FROM unidentified_bodies"
    params = ()
    if status:
        query += " WHERE status = %s"
        params = (status,)
    query += " ORDER BY created_at DESC"
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df


def fetch_all_missing_persons_as_dicts(status: str = None) -> list:
    """
    Same as fetch_missing_persons but returns a list of plain dicts
    instead of a DataFrame — this is what matching.py expects.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM missing_persons"
    params = ()
    if status:
        query += " WHERE status = %s"
        params = (status,)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def fetch_all_unidentified_bodies_as_dicts(status: str = None) -> list:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM unidentified_bodies"
    params = ()
    if status:
        query += " WHERE status = %s"
        params = (status,)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_missing_person_by_id(mp_id: int) -> pd.Series:
    df = fetch_missing_persons()
    row = df[df["id"] == mp_id]
    return row.iloc[0] if not row.empty else None


def get_unidentified_body_by_id(ub_id: int) -> pd.Series:
    df = fetch_unidentified_bodies()
    row = df[df["id"] == ub_id]
    return row.iloc[0] if not row.empty else None


# ---------- MATCH FUNCTIONS ----------

def save_match(missing_person_id: int, unidentified_body_id: int,
               text_score: float, face_score: float, final_score: float) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO matches
        (missing_person_id, unidentified_body_id, text_score, face_score, final_score)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (missing_person_id, unidentified_body_id, text_score, face_score, final_score))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return new_id


def fetch_top_matches(missing_person_id: int, limit: int = 5) -> pd.DataFrame:
    conn = get_connection()
    query = """
        SELECT m.*, u.found_location, u.found_date, u.photo_path AS body_photo,
               u.distinguishing_marks AS body_marks, u.gender AS body_gender
        FROM matches m
        JOIN unidentified_bodies u ON m.unidentified_body_id = u.id
        WHERE m.missing_person_id = %s
        ORDER BY m.final_score DESC
        LIMIT %s
    """
    df = pd.read_sql(query, conn, params=(missing_person_id, limit))
    conn.close()
    return df


def confirm_match(match_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE matches SET confirmed = TRUE WHERE id = %s", (match_id,))
    # also mark both records as Matched
    cursor.execute("""
        UPDATE missing_persons mp
        JOIN matches m ON mp.id = m.missing_person_id
        SET mp.status = 'Matched' WHERE m.id = %s
    """, (match_id,))
    cursor.execute("""
        UPDATE unidentified_bodies ub
        JOIN matches m ON ub.id = m.unidentified_body_id
        SET ub.status = 'Matched' WHERE m.id = %s
    """, (match_id,))
    conn.commit()
    cursor.close()
    conn.close()
