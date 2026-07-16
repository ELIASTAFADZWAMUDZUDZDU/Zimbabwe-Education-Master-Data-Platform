"""
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
Module  : Validate Merge
Purpose : Validate merged master dataset
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
"""

# ==========================
# Validate Merge
# ==========================

def validate_merge(dataset):

    print("\n" + "=" * 60)
    print("MASTER DATASET VALIDATION REPORT")
    print("=" * 60)

    print(f"\nTotal Schools : {len(dataset)}")

    # ==========================
    # Field Coverage
    # ==========================

    website_count = 0
    email_count = 0
    phone_count = 0
    address_count = 0
    province_count = 0
    city_count = 0
    profile_count = 0
    school_type_count = 0

    o_level_count = 0
    a_level_count = 0
    both_rankings = 0

    multi_source_count = 0

    # ==========================
    # Source Distribution
    # ==========================

    source_counts = {}

    # ==========================
    # Loop Through Schools
    # ==========================

    for school in dataset:

        # ----------------------
        # Field Coverage
        # ----------------------

        if school.get("website"):
            website_count += 1

        if school.get("email"):
            email_count += 1

        if school.get("phone_numbers"):
            phone_count += 1

        if school.get("physical_address"):
            address_count += 1

        if school.get("province"):
            province_count += 1

        if school.get("city"):
            city_count += 1

        if school.get("profile"):
            profile_count += 1

        if school.get("school_type"):
            school_type_count += 1

        # ----------------------
        # Rankings
        # ----------------------

        has_o = school.get("ranking_o_level") is not None
        has_a = school.get("ranking_a_level") is not None

        if has_o:
            o_level_count += 1

        if has_a:
            a_level_count += 1

        if has_o and has_a:
            both_rankings += 1

        # ----------------------
        # Sources
        # ----------------------

        sources = school.get("sources", [])

        if len(sources) > 1:
            multi_source_count += 1

        for source in sources:

            source_counts[source] = (
                source_counts.get(source, 0) + 1
            )

    # ==========================
    # Print Report
    # ==========================

    print("\nField Coverage")
    print("-" * 30)

    print(f"Website                : {website_count}")
    print(f"Email                  : {email_count}")
    print(f"Phone                  : {phone_count}")
    print(f"Address                : {address_count}")
    print(f"Province               : {province_count}")
    print(f"City                   : {city_count}")
    print(f"Profile                : {profile_count}")
    print(f"School Type Available  : {school_type_count}")

    print()

    print(f"O-Level Ranking        : {o_level_count}")
    print(f"A-Level Ranking        : {a_level_count}")
    print(f"Both Rankings          : {both_rankings}")

    print()

    print(f"Multi-source Schools   : {multi_source_count}")

    # ==========================
    # Source Distribution
    # ==========================

    print("\nSource Distribution")
    print("-" * 30)

    for source, count in sorted(source_counts.items()):

        print(f"{source:<20} {count}")

    print("=" * 60)