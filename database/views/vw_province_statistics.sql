/*
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
File    : vw_province_statistics.sql
Purpose : Province-level statistics
Database: PostgreSQL
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
*/

CREATE OR REPLACE VIEW vw_province_statistics AS

SELECT

    p.province_name,

    COUNT(s.school_id) AS total_schools,

    COUNT(s.official_website) AS schools_with_website,

    COUNT(s.official_email) AS schools_with_email,

    COUNT(s.profile) AS schools_with_profile,

    COUNT(s.o_level_rank) AS schools_with_o_level_rank,

    COUNT(s.a_level_rank) AS schools_with_a_level_rank

FROM provinces p

LEFT JOIN schools s

ON p.province_id = s.province_id

GROUP BY

    p.province_name

ORDER BY

    p.province_name;