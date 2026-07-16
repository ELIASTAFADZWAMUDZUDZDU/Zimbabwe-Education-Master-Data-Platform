"""
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
Module  : AI Engine
Purpose : Gemini Natural Language to SQL
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
"""

# ==========================================================
# Imports
# ==========================================================

import os

import pandas as pd

from dotenv import load_dotenv

from google import genai

from database import get_connection


# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)


# ==========================================================
# System Prompt
# ==========================================================

SYSTEM_PROMPT = """
You are an expert PostgreSQL assistant.

You are helping users query the
Zimbabwe Education Master Data Platform.

The ONLY table you may query is:

vw_school_directory

Available columns are:

school_name
province
city
school_type
education_level
o_level_rank
a_level_rank
official_website
official_email
phone_numbers

Rules

1. Generate ONLY PostgreSQL SQL.

2. Use ONLY vw_school_directory.

3. Never use any other table.

4. Never generate:

INSERT
UPDATE
DELETE
DROP
ALTER
CREATE
TRUNCATE

5. Return ONLY SQL.

6. Do not explain.

7. Do not use markdown.

8. End with a semicolon.

Examples

Question:
Show schools in Harare

SQL:
SELECT *
FROM vw_school_directory
WHERE province = 'Harare';

Question:
Top 10 O Level schools

SQL:
SELECT
school_name,
o_level_rank
FROM vw_school_directory
WHERE o_level_rank IS NOT NULL
ORDER BY o_level_rank ASC
LIMIT 10;

Question:
Schools with websites

SQL:
SELECT
school_name,
official_website
FROM vw_school_directory
WHERE official_website IS NOT NULL;
"""


# ==========================================================
# Generate SQL
# ==========================================================

def generate_sql(question):

    try:

        response = client.models.generate_content(

            model="gemini-3.5-flash",

            contents=f"""

{SYSTEM_PROMPT}

Question:

{question}

"""

        )

        sql = response.text.strip()

        sql = sql.replace("```sql", "")
        sql = sql.replace("```", "")
        sql = sql.strip()

        return sql

    except Exception as error:

        raise Exception(f"Gemini Error: {error}")

# ==========================================================
# Execute SQL
# ==========================================================

def execute_sql(sql):

    connection = get_connection()

    dataframe = pd.read_sql_query(

        sql,

        connection

    )

    connection.close()

    return dataframe

# ==========================================================
# Explain Results
# ==========================================================

def explain_results(question, dataframe):

    preview = dataframe.head(10).to_string(index=False)

    prompt = f"""
You are an AI assistant for the Zimbabwe Education Master Data Platform.

The user asked:

{question}

The SQL query returned the following results:

{preview}

Total rows returned: {len(dataframe)}

Write a short, friendly response.

Do NOT mention SQL.

Keep it under 100 words.
"""

    response = client.models.generate_content(

        model="gemini-flash-latest",

        contents=prompt

    )

    return response.text.strip()    


# ==========================================================
# Validate SQL
# ==========================================================

def validate_sql(sql):

    sql = sql.strip().lower()

    forbidden = [

        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "truncate",
        "create",
        "grant",
        "revoke"

    ]

    if not sql.startswith("select"):

        return False

    for keyword in forbidden:

        if keyword in sql:

            return False

    if "vw_school_directory" not in sql:

        return False

    return True