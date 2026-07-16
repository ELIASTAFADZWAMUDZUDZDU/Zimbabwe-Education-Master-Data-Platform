/*
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
File    : vw_data_quality.sql
Purpose : Monitor completeness of school records
Database: PostgreSQL
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
*/

CREATE OR REPLACE VIEW vw_data_quality AS

SELECT

    s.school_id,

    s.school_name,

    p.province_name AS province,

    CASE
        WHEN s.city IS NULL THEN 'Missing'
        ELSE 'Available'
    END AS city,

    CASE
        WHEN s.physical_address IS NULL THEN 'Missing'
        ELSE 'Available'
    END AS physical_address,

    CASE
        WHEN s.school_type IS NULL THEN 'Missing'
        ELSE 'Available'
    END AS school_type,

    CASE
        WHEN s.education_level IS NULL THEN 'Missing'
        ELSE 'Available'
    END AS education_level,

    CASE
        WHEN s.official_website IS NULL THEN 'Missing'
        ELSE 'Available'
    END AS website,

    CASE
        WHEN s.official_email IS NULL THEN 'Missing'
        ELSE 'Available'
    END AS email,

    CASE
        WHEN s.profile IS NULL THEN 'Missing'
        ELSE 'Available'
    END AS profile,

    CASE
        WHEN s.o_level_rank IS NULL THEN 'Missing'
        ELSE 'Available'
    END AS o_level_rank,

    CASE
        WHEN s.a_level_rank IS NULL THEN 'Missing'
        ELSE 'Available'
    END AS a_level_rank

FROM schools s

LEFT JOIN provinces p

ON s.province_id = p.province_id;