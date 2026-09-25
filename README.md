# Missing Persons ↔ Unidentified Bodies Matching Platform

A minor project prototype that helps connect missing-person reports with
unidentified-body records using text-based and facial similarity matching —
without touching Aadhaar/biometric data.

## Setup

### 1. Install MySQL and create the database
Make sure MySQL is running locally, then run:
```bash
mysql -u root -p < schema.sql
```
This creates the `missing_persons_db` database with all required tables.

### 2. Configure DB credentials
Edit `db_config.py`, or set environment variables:
```bash
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=your_password
export DB_NAME=missing_persons_db
```

### 3. Install Python dependencies
```bash
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```
The app will open in your browser. Use the sidebar to navigate between
the Police Form, Hospital Form, and View Records pages.

## Project Structure
```
missing_persons_project/
├── app.py                     # Home page
├── database.py                # All MySQL queries live here
├── db_config.py                # DB connection settings
├── schema.sql                  # Database schema
├── requirements.txt
├── uploads/                    # Uploaded photos saved here
│   ├── missing/
│   └── unidentified/
└── pages/
    ├── 1_Police_Form.py         # Report a missing person
    ├── 2_Hospital_Form.py       # Report an unidentified body
    └── 3_View_Records.py        # View all records (table)
```

## Status
- [x] Database schema
- [x] Police data entry form
- [x] Hospital data entry form
- [x] Records view page
- [ ] Text-based matching engine (Week 2)
- [ ] Facial matching with DeepFace (Week 2)
- [ ] Match dashboard with confirm action (Week 3)
- [ ] LLM-generated match explanation (Week 3, optional)
