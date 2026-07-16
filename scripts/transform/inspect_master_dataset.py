"""
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
Module  : Inspect Master Dataset
Purpose : Inspect merged records for debugging
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
"""

# ==========================
# Inspect Master Dataset
# ==========================

def inspect_master_dataset(master_dataset, limit=20):

    print("\n" + "=" * 80)
    print("MASTER DATASET SAMPLE")
    print("=" * 80)

    for i, school in enumerate(master_dataset[:limit], start=1):

        print(f"\nRecord {i}")

        print("-" * 80)

        for key, value in school.items():

            print(f"{key:<22}: {value}")

        print("-" * 80)