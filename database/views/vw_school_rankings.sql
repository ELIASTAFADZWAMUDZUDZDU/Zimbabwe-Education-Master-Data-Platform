/*
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
File    : 004_reporting_views.sql
View    : vw_school_rankings
Purpose : View ranked schools for reporting and dashboard
Database: PostgreSQL
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
*/

CREATE OR REPLACE VIEW vw_school_rankings AS

SELECT

    s.school_id,

    s.school_name,

    p.province_name AS province,

    s.city,

    s.school_type,

    s.education_level,

    s.o_level_rank,

    s.a_level_rank

FROM schools s

LEFT JOIN provinces p
       ON s.province_id = p.province_id

WHERE

    s.o_level_rank IS NOT NULL

    OR

    s.a_level_rank IS NOT NULL;