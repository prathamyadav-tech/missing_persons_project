-- Missing Persons <-> Unidentified Bodies Matching Platform
-- Database schema

CREATE DATABASE IF NOT EXISTS missing_persons_db;
USE missing_persons_db;

-- Table: missing_persons
-- Filled by police stations when a missing person is reported
CREATE TABLE IF NOT EXISTS missing_persons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    last_seen_location VARCHAR(255) NOT NULL,
    last_seen_date DATE NOT NULL,
    photo_path VARCHAR(255),
    height_cm INT,
    distinguishing_marks TEXT,       -- e.g. "scar on left cheek, tattoo on right arm"
    clothing_description TEXT,
    reported_by VARCHAR(150),        -- police station / officer name
    status ENUM('Open', 'Matched', 'Resolved') DEFAULT 'Open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: unidentified_bodies
-- Filled by hospitals / mortuaries when an unidentified body is found
CREATE TABLE IF NOT EXISTS unidentified_bodies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    approx_age INT,
    gender ENUM('Male', 'Female', 'Other', 'Unknown') NOT NULL,
    found_location VARCHAR(255) NOT NULL,
    found_date DATE NOT NULL,
    photo_path VARCHAR(255),
    height_cm INT,
    distinguishing_marks TEXT,
    clothing_description TEXT,
    reported_by VARCHAR(150),        -- hospital / mortuary name
    status ENUM('Open', 'Matched', 'Resolved') DEFAULT 'Open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: matches
-- Stores computed match scores between a missing person and an unidentified body
-- so the dashboard doesn't need to recompute everything every time
CREATE TABLE IF NOT EXISTS matches (
    id INT AUTO_INCREMENT PRIMARY KEY,
    missing_person_id INT NOT NULL,
    unidentified_body_id INT NOT NULL,
    text_score FLOAT DEFAULT 0,      -- 0-100
    face_score FLOAT DEFAULT 0,      -- 0-100
    final_score FLOAT DEFAULT 0,     -- weighted combination
    confirmed BOOLEAN DEFAULT FALSE, -- true once staff confirms the match
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (missing_person_id) REFERENCES missing_persons(id) ON DELETE CASCADE,
    FOREIGN KEY (unidentified_body_id) REFERENCES unidentified_bodies(id) ON DELETE CASCADE
);
