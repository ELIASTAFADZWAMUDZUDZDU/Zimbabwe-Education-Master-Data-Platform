"""
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
Module  : Dashboard Database Connection
Purpose : Connect Streamlit Dashboard to PostgreSQL
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
"""

import os

import psycopg2

from dotenv import load_dotenv

# ==========================
# Load Environment Variables
# ==========================

load_dotenv()

# ==========================
# PostgreSQL Connection
# ==========================

def get_connection():

    connection = psycopg2.connect(

        dbname=os.getenv("DB_NAME"),

        user=os.getenv("DB_USER"),

        password=os.getenv("DB_PASSWORD"),

        host=os.getenv("DB_HOST"),

        port=os.getenv("DB_PORT")

    )

    return connection