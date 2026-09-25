"""
Central DB configuration.
Edit these values to match your local MySQL setup, or better -
set them as environment variables so you don't commit passwords to GitHub.
"""
import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "Pratham@01"),   
    "database": os.getenv("DB_NAME", "missing_persons_db"),
}
