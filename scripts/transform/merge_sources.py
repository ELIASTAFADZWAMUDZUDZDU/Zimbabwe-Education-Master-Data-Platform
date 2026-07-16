"""
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
Module  : Merge Sources
Purpose : Merge all datasets into one master dataset
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
"""

# ==========================
# Merge Datasets
# ==========================

def merge_sources(datasets):

    print("Merging datasets...")

    master = {}

    # ----------------------
    # Loop Through Sources
    # ----------------------

    for source_name, dataset in datasets.items():

        # ----------------------
        # Loop Through Schools
        # ----------------------

        for school in dataset:

            key = school.get("clean_school_name")

            if not key:
                continue

            # ----------------------
            # New School
            # ----------------------

            if key not in master:

                new_school = school.copy()

                # Track contributing sources
                new_school["sources"] = [school["source"]]

                master[key] = new_school

            # ----------------------
            # Existing School
            # ----------------------

            else:

                existing = master[key]

                for column, value in school.items():

                    # ----------------------------------
                    # Merge Phone Numbers
                    # ----------------------------------

                    if column == "phone_numbers":

                        existing_numbers = existing.get("phone_numbers") or []
                        new_numbers = value or []

                        merged_numbers = list(
                            dict.fromkeys(existing_numbers + new_numbers)
                        )

                        existing["phone_numbers"] = merged_numbers

                    # ----------------------------------
                    # Merge Education Levels
                    # ----------------------------------

                    elif column == "education_level":

                        existing_level = existing.get("education_level")
                        new_level = value

                        if existing_level and new_level:

                            levels = []

                            # Existing levels
                            for level in existing_level.split(","):

                                level = level.strip()

                                if level and level not in levels:

                                    levels.append(level)

                            # Incoming levels
                            for level in new_level.split(","):

                                level = level.strip()

                                if level and level not in levels:

                                    levels.append(level)

                            existing["education_level"] = ", ".join(levels)

                        elif new_level:

                            existing["education_level"] = new_level

                    # ----------------------------------
                    # Fill Missing Values
                    # ----------------------------------

                    elif existing.get(column) in [None, "", []]:

                        existing[column] = value

                # ----------------------
                # Track All Sources
                # ----------------------

                source = school.get("source")

                if source and source not in existing["sources"]:

                    existing["sources"].append(source)

    return list(master.values())