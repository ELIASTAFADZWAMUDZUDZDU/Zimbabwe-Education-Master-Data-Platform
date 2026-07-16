"""
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
Module  : Fill Missing Values
Purpose : Standardize missing values
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
"""

# ==========================
# Fill Missing Values
# ==========================

def fill_missing_values(dataset):

    print("Standardizing missing values...")

    for school in dataset:

        for column, value in school.items():

            # ----------------------
            # Empty Strings
            # ----------------------

            if isinstance(value, str):

                if value.strip() == "":

                    school[column] = None

            # ----------------------
            # Empty Lists
            # ----------------------

            elif isinstance(value, list):

                if len(value) == 0:

                    school[column] = None

    return dataset