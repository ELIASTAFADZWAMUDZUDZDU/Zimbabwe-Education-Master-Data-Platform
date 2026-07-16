/*
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
File    : vw_school_directory.sql
Purpose : Complete directory of Zimbabwe secondary schools
Database: PostgreSQL
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
*/

CREATE OR REPLACE VIEW vw_school_directory AS

SELECT

    s.school_id,

    s.school_name,

    p.province_name AS province,

    s.city,

    s.physical_address,

    s.school_type,

    s.education_level,

    s.o_level_rank,

    s.a_level_rank,

    s.official_website,

    s.official_email,

    s.profile,

    STRING_AGG(
        DISTINCT sp.phone_number,
        ', '
    ) AS phone_numbers,

    STRING_AGG(
        DISTINCT src.source_name,
        ', '
    ) AS sources

FROM schools s

LEFT JOIN provinces p

ON s.province_id = p.province_id

LEFT JOIN school_phones sp

ON s.school_id = sp.school_id

LEFT JOIN school_sources ss

ON s.school_id = ss.school_id

LEFT JOIN sources src

ON ss.source_id = src.source_id

GROUP BY

    s.school_id,

    s.school_name,

    p.province_name,

    s.city,

    s.physical_address,

    s.school_type,

    s.education_level,

    s.o_level_rank,

    s.a_level_rank,

    s.official_website,

    s.official_email,

    s.profile;