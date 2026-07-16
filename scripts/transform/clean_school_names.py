"""
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
Module  : Clean School Names
Purpose : Standardize school names for matching
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
"""

# ==========================
# Imports
# ==========================

import re

# ==========================
# Common Words
# ==========================

COMMON_WORDS = {

    "school",

    "secondary",

    "high"

}

# ==========================
# Clean School Name
# ==========================

def clean_school_names(name):

    if not name:
        return None

    # ----------------------
    # Convert to lowercase
    # ----------------------

    name = name.lower()

    # ----------------------
    # Remove city after comma
    # Example:
    # "Christian Brothers College, Bulawayo"
    # -> "Christian Brothers College"
    # ----------------------

    name = name.split(",")[0]

    # ----------------------
    # Standardize "St."
    # ----------------------

    name = re.sub(r"\bst\.\b", "st", name)

    # ----------------------
    # Remove punctuation
    # ----------------------

    name = re.sub(r"[^\w\s]", "", name)

    # ----------------------
    # Remove common words
    # ----------------------

    words = []

    for word in name.split():

        if word not in COMMON_WORDS:

            words.append(word)

    name = " ".join(words)

    # ----------------------
    # Remove extra spaces
    # ----------------------

    name = re.sub(r"\s+", " ", name)

    # ----------------------
    # Remove leading/trailing spaces
    # ----------------------

    name = name.strip()

    return name


# ==========================
# Clean Entire Dataset
# ==========================

def clean_dataset(dataset):

    print("Cleaning school names...")

    for school in dataset:

        school["clean_school_name"] = clean_school_names(
            school.get("school_name")
        )

    return dataset