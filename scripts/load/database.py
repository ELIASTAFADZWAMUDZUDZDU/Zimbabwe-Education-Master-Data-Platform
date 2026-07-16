"""
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
Module  : Database Connection
Purpose : Create PostgreSQL database connection
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
"""

# ==========================
# Imports
# ==========================

import psycopg2

from dotenv import load_dotenv

import os

# ==========================
# Load Environment Variables
# ==========================

load_dotenv()

# ==========================
# Connect Database
# ==========================

def connect_database():

    connection = psycopg2.connect(

        host=os.getenv("DB_HOST"),

        port=os.getenv("DB_PORT"),

        database=os.getenv("DB_NAME"),

        user=os.getenv("DB_USER"),

        password=os.getenv("DB_PASSWORD")

    )

    return connection