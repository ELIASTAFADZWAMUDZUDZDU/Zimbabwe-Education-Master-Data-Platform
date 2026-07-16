"""
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
Module  : Save Master Dataset
Purpose : Save processed master dataset
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
"""

# ==========================
# Imports
# ==========================

import json

# ==========================
# Save Master Dataset
# ==========================

def save_master_dataset(dataset, filename):

    print("Saving master dataset...")

    with open(filename, "w", encoding="utf-8") as file:

        json.dump(
            dataset,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"Saved {len(dataset)} schools to {filename}")