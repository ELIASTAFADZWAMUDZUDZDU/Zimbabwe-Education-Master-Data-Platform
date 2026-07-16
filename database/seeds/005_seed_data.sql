/*
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
File    : 005_seed_data.sql
Purpose : Populate lookup/reference tables
Database: PostgreSQL
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
*/

-- =========================================================
-- Provinces
-- =========================================================

INSERT INTO provinces
(
    province_name
)
VALUES
('Bulawayo'),
('Harare'),
('Manicaland'),
('Mashonaland Central'),
('Mashonaland East'),
('Mashonaland West'),
('Masvingo'),
('Matabeleland North'),
('Matabeleland South'),
('Midlands');

-- =========================================================
-- Sources
-- =========================================================

INSERT INTO sources
(
    source_name,
    source_url,
    reliability_score
)
VALUES

(
    'Wikipedia',
    'https://en.wikipedia.org',
    5
),

(
    'Pindula',
    'https://www.pindula.co.zw',
    4
),

(
    'OpenClass',
    'https://openclass.co.zw',
    3
),

(
    'ZimbabweYP',
    'https://www.zimyellowpage.com',
    3
),

(
    'IBZIM',
    'https://www.ibzim.com',
    5
);