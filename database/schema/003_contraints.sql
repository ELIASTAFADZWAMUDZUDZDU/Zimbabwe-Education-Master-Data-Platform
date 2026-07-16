/*
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
File    : 002_constraints.sql
Purpose : Create foreign key and check constraints
Database: PostgreSQL
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
*/

-- =========================================================
-- Schools
-- =========================================================

ALTER TABLE schools
ADD CONSTRAINT fk_school_province
FOREIGN KEY (province_id)
REFERENCES provinces(province_id);

-- =========================================================
-- School Phones
-- =========================================================

ALTER TABLE school_phones
ADD CONSTRAINT fk_phone_school
FOREIGN KEY (school_id)
REFERENCES schools(school_id)
ON DELETE CASCADE;

-- =========================================================
-- School Sources
-- =========================================================

ALTER TABLE school_sources
ADD CONSTRAINT fk_school_sources_school
FOREIGN KEY (school_id)
REFERENCES schools(school_id)
ON DELETE CASCADE;

ALTER TABLE school_sources
ADD CONSTRAINT fk_school_sources_source
FOREIGN KEY (source_id)
REFERENCES sources(source_id);

-- Prevent duplicate source entries for the same school
ALTER TABLE school_sources
ADD CONSTRAINT pk_school_sources
PRIMARY KEY (school_id, source_id);

-- =========================================================
-- Quality Issues
-- =========================================================

ALTER TABLE quality_issues
ADD CONSTRAINT fk_quality_school
FOREIGN KEY (school_id)
REFERENCES schools(school_id)
ON DELETE CASCADE;

-- =========================================================
-- Staging Schools
-- =========================================================

ALTER TABLE staging_schools
ADD CONSTRAINT fk_staging_run
FOREIGN KEY (run_id)
REFERENCES etl_runs(run_id);

ALTER TABLE staging_schools
ADD CONSTRAINT fk_staging_source
FOREIGN KEY (source_id)
REFERENCES sources(source_id);

-- =========================================================
-- CHECK Constraints
-- =========================================================

ALTER TABLE etl_runs
ADD CONSTRAINT chk_etl_status
CHECK (
    etl_status IN
    (
        'Running',
        'Completed',
        'Failed'
    )
);

ALTER TABLE quality_issues
ADD CONSTRAINT chk_issue_status
CHECK (
    issue_status IN
    (
        'Open',
        'Resolved'
    )
);

ALTER TABLE staging_schools
ADD CONSTRAINT chk_processing_status
CHECK (
    processing_status IN
    (
        'Pending',
        'Processed',
        'Failed'
    )
);

-- =========================================================
-- Data Validation
-- =========================================================

ALTER TABLE sources
ADD CONSTRAINT chk_reliability_score
CHECK (
    reliability_score BETWEEN 1 AND 5
);

ALTER TABLE schools
ADD CONSTRAINT chk_o_level_rank
CHECK (
    o_level_rank IS NULL OR o_level_rank > 0
);

ALTER TABLE schools
ADD CONSTRAINT chk_a_level_rank
CHECK (
    a_level_rank IS NULL OR a_level_rank > 0
);