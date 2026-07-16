"""
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
Module  : Load Raw Data
Purpose : Load all extracted datasets into memory
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
"""

# ==========================
# Imports
# ==========================

import json
from pathlib import Path

# ==========================
# Raw Data Directory
# ==========================

RAW_DIR = Path("data/raw")

# ==========================
# Load JSON
# ==========================

def load_json(filename):

    filepath = RAW_DIR / filename

    with open(filepath, "r", encoding="utf-8") as file:

        return json.load(file)

# ==========================
# Load All Sources
# ==========================

def load_raw_data():

    print("Loading raw datasets...\n")

    datasets = {

        "wikipedia": load_json("wikipedia_schools.json"),

        "pindula": load_json("pindula_schools.json"),

        "openclass": load_json("openclass_schools.json"),

        "zimbabweyp": load_json("zimbabweyp_schools.json"),

        "ibzim_o_level": load_json("ibzim_o_level_rankings.json"),

        "ibzim_a_level": load_json("ibzim_a_level_rankings.json")

    }

    print("Datasets Loaded Successfully\n")

    for name, data in datasets.items():

        print(f"{name:<20} {len(data)} records")

    return datasets

# ==========================
# Run
# ==========================

def run():

    datasets = load_raw_data()

    return datasets

# ==========================
# Main
# ==========================

if __name__ == "__main__":

    datasets = run()