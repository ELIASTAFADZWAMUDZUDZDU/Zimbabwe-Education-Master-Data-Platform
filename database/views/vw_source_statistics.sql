/*
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
File    : vw_source_statistics.sql
Purpose : Statistics for each data source
Database: PostgreSQL
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
*/

CREATE OR REPLACE VIEW vw_source_statistics AS

SELECT

    src.source_name,

    src.reliability_score,

    COUNT(DISTINCT ss.school_id) AS total_schools

FROM sources src

LEFT JOIN school_sources ss

ON src.source_id = ss.source_id

GROUP BY

    src.source_id,

    src.source_name,

    src.reliability_score

ORDER BY

    total_schools DESC,
    src.source_name;