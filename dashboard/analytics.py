"""
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
Module  : Dashboard Analytics
Purpose : Dashboard statistics and analytics
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
"""

# ==========================
# Imports
# ==========================

import pandas as pd

from database import get_connection


# ==========================
# Dashboard Statistics
# ==========================

def get_dashboard_statistics():

    connection = get_connection()

    cursor = connection.cursor()

    queries = {

        "schools": """
            SELECT COUNT(*)
            FROM schools;
        """,

        "provinces": """
            SELECT COUNT(*)
            FROM provinces;
        """,

        "phones": """
            SELECT COUNT(*)
            FROM school_phones;
        """,

        "websites": """
            SELECT COUNT(*)
            FROM schools
            WHERE official_website IS NOT NULL;
        """,

        "emails": """
            SELECT COUNT(*)
            FROM schools
            WHERE official_email IS NOT NULL;
        """,

        "ranked": """
            SELECT COUNT(*)
            FROM schools
            WHERE o_level_rank IS NOT NULL
               OR a_level_rank IS NOT NULL;
        """

    }

    statistics = {}

    for key, query in queries.items():

        cursor.execute(query)

        statistics[key] = cursor.fetchone()[0]

    cursor.close()

    connection.close()

    return statistics


# ==========================
# School Directory
# ==========================

def get_school_directory():

    connection = get_connection()

    query = """
        SELECT

            school_name,
            province,
            city,
            school_type,
            education_level,
            o_level_rank,
            a_level_rank,
            official_website,
            official_email,
            phone_numbers

        FROM vw_school_directory

        ORDER BY school_name;
    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return dataframe


# ==========================
# Schools by Province
# ==========================

def get_schools_by_province():

    connection = get_connection()

    query = """
        SELECT

            province,

            COUNT(*) AS total_schools

        FROM vw_school_directory

        GROUP BY province

        ORDER BY total_schools DESC;
    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return dataframe


# ==========================
# Education Distribution
# ==========================

def get_education_distribution():

    connection = get_connection()

    query = """
        SELECT

            education_level,

            COUNT(*) AS total_schools

        FROM vw_school_directory

        GROUP BY education_level

        ORDER BY total_schools DESC;
    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return dataframe


# ==========================
# Website Coverage
# ==========================

def get_website_coverage():

    connection = get_connection()

    query = """
        SELECT

            CASE

                WHEN official_website IS NULL

                THEN 'No Website'

                ELSE 'Has Website'

            END AS website_status,

            COUNT(*) AS total

        FROM schools

        GROUP BY website_status;
    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return dataframe


# ==========================
# Email Coverage
# ==========================

def get_email_coverage():

    connection = get_connection()

    query = """
        SELECT

            CASE

                WHEN official_email IS NULL

                THEN 'No Email'

                ELSE 'Has Email'

            END AS email_status,

            COUNT(*) AS total

        FROM schools

        GROUP BY email_status;
    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return dataframe


# ==========================
# Ranking Coverage
# ==========================

def get_ranking_coverage():

    connection = get_connection()

    query = """
        SELECT

            CASE

                WHEN o_level_rank IS NOT NULL
                  OR a_level_rank IS NOT NULL

                THEN 'Ranked'

                ELSE 'Not Ranked'

            END AS ranking_status,

            COUNT(*) AS total

        FROM schools

        GROUP BY ranking_status;
    """

    dataframe = pd.read_sql_query(query, connection)

    connection.close()

    return dataframe