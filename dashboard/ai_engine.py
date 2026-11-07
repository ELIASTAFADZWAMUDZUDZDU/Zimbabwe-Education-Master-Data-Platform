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
from sql_guard import prepare_sql, validate_sql  # noqa: F401  (validate_sql is re-exported)


# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# Model names can be changed in .env without editing the code
SQL_MODEL = os.getenv("GEMINI_SQL_MODEL", "gemini-3.5-flash")
EXPLAIN_MODEL = os.getenv("GEMINI_EXPLAIN_MODEL", "gemini-flash-latest")

_client = None


def get_client():
    """Create the Gemini client on first use, so importing this module never needs a key."""
    global _client
    if _client is None:
        if not API_KEY:
            raise RuntimeError("GEMINI_API_KEY is not set. Add it to your .env file.")
        _client = genai.Client(api_key=API_KEY)
    return _client


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

        response = get_client().models.generate_content(

            model=SQL_MODEL,

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
    """Run a validated query in a read-only transaction and return a DataFrame.

    The SQL is checked again here (defence in depth), capped to a maximum
    number of rows, and given a time limit.
    """

    safe_sql = prepare_sql(sql)

    connection = get_connection()

    try:

        connection.set_session(readonly=True)

        with connection.cursor() as cursor:
            cursor.execute("SET statement_timeout = 10000;")  # 10 seconds

        dataframe = pd.read_sql_query(safe_sql, connection)

    finally:

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

    response = get_client().models.generate_content(

        model=EXPLAIN_MODEL,

        contents=prompt

    )

    return response.text.strip()
