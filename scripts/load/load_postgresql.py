"""
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
Module  : Load PostgreSQL
Purpose : Load master dataset into PostgreSQL
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
"""

# ==========================================================
# Imports
# ==========================================================

import json

from load.database import connect_database


# ==========================================================
# Load Master Dataset
# ==========================================================

def load_master_dataset():

    with open(

        "data/processed/zimbabwe_master_dataset.json",

        "r",

        encoding="utf-8"

    ) as file:

        return json.load(file)


# ==========================================================
# Load Schools
# ==========================================================

def load_schools(connection, dataset):

    print("Loading schools...")

    cursor = connection.cursor()

    # ------------------------------------------------------
    # Province Lookup
    # ------------------------------------------------------

    cursor.execute("""

        SELECT
            province_id,
            province_name
        FROM provinces;

    """)

    province_lookup = {

        province_name: province_id

        for province_id, province_name

        in cursor.fetchall()

    }

    # ------------------------------------------------------
    # UPSERT Query
    # ------------------------------------------------------

    query = """

        INSERT INTO schools
        (

            school_name,
            province_id,
            city,
            physical_address,
            school_type,
            education_level,
            o_level_rank,
            a_level_rank,
            official_website,
            official_email,
            profile

        )

        VALUES
        (

            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s

        )

        ON CONFLICT (school_name)

        DO UPDATE SET

            province_id = EXCLUDED.province_id,

            city = EXCLUDED.city,

            physical_address = EXCLUDED.physical_address,

            school_type = EXCLUDED.school_type,

            education_level = EXCLUDED.education_level,

            o_level_rank = EXCLUDED.o_level_rank,

            a_level_rank = EXCLUDED.a_level_rank,

            official_website = EXCLUDED.official_website,

            official_email = EXCLUDED.official_email,

            profile = EXCLUDED.profile,

            updated_at = CURRENT_TIMESTAMP

        RETURNING school_id;

    """

    school_ids = {}

    # ------------------------------------------------------
    # Insert / Update Schools
    # ------------------------------------------------------

    for school in dataset:

        province_id = province_lookup.get(

            school.get("province")

        )

        cursor.execute(

            query,

            (

                school.get("school_name"),

                province_id,

                school.get("city"),

                school.get("physical_address"),

                school.get("school_type"),

                school.get("education_level"),

                school.get("ranking_o_level"),

                school.get("ranking_a_level"),

                school.get("website"),

                school.get("email"),

                school.get("profile")

            )

        )

        school_id = cursor.fetchone()[0]

        school_ids[

            school["clean_school_name"]

        ] = school_id

    cursor.close()

    print(f"{len(school_ids)} schools processed.")

    return school_ids
# ==========================================================
# Load Phone Numbers
# ==========================================================

def load_phone_numbers(connection, dataset, school_ids):

    print("Loading phone numbers...")

    cursor = connection.cursor()

    query = """

        INSERT INTO school_phones
        (

            school_id,
            phone_number

        )

        VALUES
        (

            %s,
            %s

        )

        ON CONFLICT (school_id, phone_number)

        DO NOTHING;

    """

    total = 0

    for school in dataset:

        school_id = school_ids.get(

            school["clean_school_name"]

        )

        if not school_id:

            continue

        phones = school.get("phone_numbers") or []

        for phone in phones:

            if not phone:

                continue

            cursor.execute(

                query,

                (

                    school_id,

                    phone

                )

            )

            total += 1

    cursor.close()

    print(f"{total} phone numbers processed.")

# ==========================================================
# Load School Sources
# ==========================================================

def load_school_sources(connection, dataset, school_ids):

    print("Loading school sources...")

    cursor = connection.cursor()

    # ------------------------------------------------------
    # Source Lookup
    # ------------------------------------------------------

    cursor.execute("""

        SELECT

            source_id,
            source_name

        FROM sources;

    """)

    source_lookup = {

        source_name: source_id

        for source_id, source_name

        in cursor.fetchall()

    }

    # ------------------------------------------------------
    # UPSERT Query
    # ------------------------------------------------------

    query = """

        INSERT INTO school_sources
        (

            school_id,
            source_id,
            last_verified

        )

        VALUES
        (

            %s,
            %s,
            CURRENT_DATE

        )

        ON CONFLICT (school_id, source_id)

        DO UPDATE SET

            last_verified = CURRENT_DATE;

    """

    total = 0

    for school in dataset:

        school_id = school_ids.get(

            school["clean_school_name"]

        )

        if not school_id:

            continue

        sources = school.get("sources") or []

        for source in sources:

            source_id = source_lookup.get(source)

            if source_id:

                cursor.execute(

                    query,

                    (

                        school_id,

                        source_id

                    )

                )

                total += 1

    cursor.close()

    print(f"{total} school-source relationships processed.")
# ==========================================================
# Main
# ==========================================================

def main():

    print("=" * 60)
    print("Zimbabwe Education Master Data Platform")
    print("PostgreSQL Data Loader")
    print("=" * 60)

    connection = None
    run_id = None

    try:

        # --------------------------------------------------
        # Connect Database
        # --------------------------------------------------

        connection = connect_database()

        print("Database connected.\n")

        # --------------------------------------------------
        # Record ETL Start
        # --------------------------------------------------

        cursor = connection.cursor()

        cursor.execute("""

            INSERT INTO etl_runs
            (

                start_time,
                etl_status

            )

            VALUES
            (

                CURRENT_TIMESTAMP,
                'Running'

            )

            RETURNING run_id;

        """)

        run_id = cursor.fetchone()[0]

        cursor.close()

        # --------------------------------------------------
        # Load Master Dataset
        # --------------------------------------------------

        dataset = load_master_dataset()

        print(f"{len(dataset)} schools loaded from JSON.\n")

        # --------------------------------------------------
        # Load Schools
        # --------------------------------------------------

        school_ids = load_schools(

            connection,

            dataset

        )

        print()

        # --------------------------------------------------
        # Load Phone Numbers
        # --------------------------------------------------

        load_phone_numbers(

            connection,

            dataset,

            school_ids

        )

        print()

        # --------------------------------------------------
        # Load School Sources
        # --------------------------------------------------

        load_school_sources(

            connection,

            dataset,

            school_ids

        )

        print()

        # --------------------------------------------------
        # Update ETL Run (Success)
        # --------------------------------------------------

        cursor = connection.cursor()

        cursor.execute("""

            UPDATE etl_runs

            SET

                end_time = CURRENT_TIMESTAMP,

                etl_status = 'Success',

                records_loaded = %s,

                records_failed = 0

            WHERE run_id = %s;

        """,

        (

            len(dataset),

            run_id

        )

        )

        cursor.close()

        # --------------------------------------------------
        # Commit Everything
        # --------------------------------------------------

        connection.commit()

        print("=" * 60)
        print("PostgreSQL Load Completed Successfully")
        print("=" * 60)

    except Exception as error:

        # --------------------------------------------------
        # Update ETL Run (Failed)
        # --------------------------------------------------

        try:

            if connection and run_id:

                cursor = connection.cursor()

                cursor.execute("""

                    UPDATE etl_runs

                    SET

                        end_time = CURRENT_TIMESTAMP,

                        etl_status = 'Failed'

                    WHERE run_id = %s;

                """,

                (

                    run_id,

                )

                )

                connection.commit()

                cursor.close()

        except:

            pass

        if connection:

            connection.rollback()

        print("\nERROR DURING DATABASE LOAD")
        print("-" * 60)
        print(error)

    finally:

        if connection:

            connection.close()

            print("\nDatabase connection closed.")


# ==========================================================
# Run Program
# ==========================================================

if __name__ == "__main__":

    main()    