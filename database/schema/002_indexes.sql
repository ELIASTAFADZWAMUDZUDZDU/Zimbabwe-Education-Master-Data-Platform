/*
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
File    : 003_indexes.sql
Purpose : Create indexes for query optimization
Database: PostgreSQL
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
*/

-- =========================================================
-- Schools
-- =========================================================

CREATE INDEX idx_school_name
ON schools(school_name);

CREATE INDEX idx_school_province
ON schools(province_id);

CREATE INDEX idx_school_city
ON schools(city);

CREATE INDEX idx_school_type
ON schools(school_type);

CREATE INDEX idx_education_level
ON schools(education_level);

-- =========================================================
-- School Phones
-- =========================================================

CREATE INDEX idx_phone_school
ON school_phones(school_id);

CREATE INDEX idx_phone_number
ON school_phones(phone_number);

-- =========================================================
-- School Sources
-- =========================================================

CREATE INDEX idx_school_sources_school
ON school_sources(school_id);

CREATE INDEX idx_school_sources_source
ON school_sources(source_id);

-- =========================================================
-- Quality Issues
-- =========================================================

CREATE INDEX idx_quality_school
ON quality_issues(school_id);

CREATE INDEX idx_quality_status
ON quality_issues(issue_status);

-- =========================================================
-- Staging Schools
-- =========================================================

CREATE INDEX idx_staging_run
ON staging_schools(run_id);

CREATE INDEX idx_staging_source
ON staging_schools(source_id);

CREATE INDEX idx_processing_status
ON staging_schools(processing_status);

-- =========================================================
-- ETL Runs
-- =========================================================

CREATE INDEX idx_etl_status
ON etl_runs(etl_status);