/*
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
File    : 001_create_tables.sql
Purpose : Create all database tables
Database: PostgreSQL
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
*/

-- =========================================================
-- Provinces
-- =========================================================

CREATE TABLE provinces (

    province_id SERIAL PRIMARY KEY,

    province_name VARCHAR(100) NOT NULL UNIQUE

);

-- =========================================================
-- Sources
-- =========================================================

CREATE TABLE sources (

    source_id SERIAL PRIMARY KEY,

    source_name VARCHAR(100) NOT NULL UNIQUE,

    source_url TEXT,

    reliability_score SMALLINT

);

-- =========================================================
-- ETL Runs
-- =========================================================

CREATE TABLE etl_runs (

    run_id SERIAL PRIMARY KEY,

    start_time TIMESTAMP NOT NULL,

    end_time TIMESTAMP,

    etl_status VARCHAR(20),

    records_extracted INTEGER DEFAULT 0,

    records_loaded INTEGER DEFAULT 0,

    records_failed INTEGER DEFAULT 0

);

-- =========================================================
-- Schools
-- =========================================================

CREATE TABLE schools (

    school_id SERIAL PRIMARY KEY,

    school_name VARCHAR(255) NOT NULL,

    province_id INTEGER,

    city VARCHAR(150),

    physical_address TEXT,

    school_type VARCHAR(100),

    education_level VARCHAR(100),

    o_level_rank INTEGER,

    a_level_rank INTEGER,

    official_website TEXT,

    official_email VARCHAR(255),

    profile TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- =========================================================
-- School Phones
-- =========================================================

CREATE TABLE school_phones (

    phone_id SERIAL PRIMARY KEY,

    school_id INTEGER,

    phone_number VARCHAR(30) NOT NULL,

    is_primary BOOLEAN DEFAULT FALSE

);

-- =========================================================
-- School Sources
-- =========================================================

CREATE TABLE school_sources (

    school_id INTEGER,

    source_id INTEGER,

    last_verified DATE

);

-- =========================================================
-- Quality Issues
-- =========================================================

CREATE TABLE quality_issues (

    issue_id SERIAL PRIMARY KEY,

    school_id INTEGER,

    issue_type VARCHAR(100),

    issue_description TEXT,

    issue_status VARCHAR(30),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- =========================================================
-- Staging Schools
-- =========================================================

CREATE TABLE staging_schools (

    staging_id SERIAL PRIMARY KEY,

    run_id INTEGER,

    source_id INTEGER,

    record_data JSONB,

    processing_status VARCHAR(30),

    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);