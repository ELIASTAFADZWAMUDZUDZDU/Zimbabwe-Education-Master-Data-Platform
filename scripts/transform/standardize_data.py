"""
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
Module  : Standardize Data
Purpose : Standardize values across all datasets
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
"""

# ==========================
# Imports
# ==========================

import re

from transform.lookup_tables import CITY_TO_PROVINCE

# ==========================
# Standardize Dataset
# ==========================

def standardize_data(dataset):

    print("Standardizing dataset...")

    for school in dataset:

        # ----------------------
        # Province
        # ----------------------

        province = school.get("province")

        if province:

            province = province.title().strip()

            if province.endswith(" Province"):

                province = province.replace(
                    " Province",
                    ""
                ).strip()

            school["province"] = province

        # ----------------------
        # City
        # ----------------------

        city = school.get("city")

        if city:

            school["city"] = city.title().strip()

        # ----------------------
        # Province <-> City
        # ----------------------

        province = school.get("province")
        city = school.get("city")

        if province in ["Harare", "Bulawayo"] and not city:

            school["city"] = province

        elif city and not province:

            if city in ["Harare", "Bulawayo"]:

                school["province"] = city

            else:

                school["province"] = CITY_TO_PROVINCE.get(city)

        # ----------------------
        # Education Level
        # ----------------------

        level = school.get("education_level")

        if level:

            level = level.strip().lower()

            if (
                ("o-level" in level or "o level" in level)
                and
                ("a-level" in level or "a level" in level)
            ):

                school["education_level"] = "Both"

            elif "both" in level:

                school["education_level"] = "Both"

            elif "a-level" in level or "a level" in level:

                school["education_level"] = "A Level"

            elif "o-level" in level or "o level" in level:

                school["education_level"] = "O Level"

            else:

                school["education_level"] = None

        # ----------------------
        # Phone Numbers
        # ----------------------

        phones = school.get("phone_numbers") or []

        cleaned_numbers = []

        for phone in phones:

            # Skip emails accidentally placed here
            if "@" in phone:

                continue

            # Remove labels
            phone = re.sub(
                r"(?i)telephone:|telephone|tel:|tel|phone:|phone|cell:|cell|mobile:|mobile|fax:",
                "",
                phone
            )

            # Split on common separators
            numbers = re.split(
                r"[,/;\n]+",
                phone
            )

            for number in numbers:

                number = number.strip()

                # Remove brackets
                number = number.replace("(", "")
                number = number.replace(")", "")

                # Remove spaces
                number = number.replace(" ", "")

                # Remove hyphens
                number = number.replace("-", "")

                # Remove trailing periods
                number = number.rstrip(".")

                if number:

                    cleaned_numbers.append(number)

        # Remove duplicates while preserving order

        school["phone_numbers"] = list(

            dict.fromkeys(cleaned_numbers)

        )

    return dataset