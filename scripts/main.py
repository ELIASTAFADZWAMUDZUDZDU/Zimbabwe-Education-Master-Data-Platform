"""
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
Module  : Main ETL Pipeline
Purpose : Execute the complete ETL pipeline
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
"""
import sys

sys.stdout.reconfigure(encoding="utf-8")

# ==========================
# Extract
# ==========================

from extract.wikipedia_extractor import run as wikipedia_extract
from extract.zimbabweyp_extractor import run as zimbabweyp_extract
from extract.ibzim_o_level import run as ibzim_o_extract
from extract.ibzim_a_level import run as ibzim_a_extract

# ==========================
# Transform
# ==========================

from transform.load_raw_data import load_raw_data
from transform.clean_school_names import clean_dataset
from transform.standardize_data import standardize_data
from transform.merge_sources import merge_sources
from transform.fill_missing_values import fill_missing_values
from transform.save_master_dataset import save_master_dataset
from transform.validate_merge import validate_merge
from transform.inspect_master_dataset import inspect_master_dataset

# ==========================
# Load
# ==========================

from load.load_postgresql import main as load_postgresql


# ==========================
# Main Pipeline
# ==========================

def main():

    print("\n" + "=" * 70)
    print("ZIMBABWE EDUCATION MASTER DATA PLATFORM (ZEMDP)")
    print("COMPLETE ETL PIPELINE")
    print("=" * 70)

    # =====================================================
    # EXTRACT
    # =====================================================

    print("STEP:EXTRACT")

    print("\n[1/9] Extracting Wikipedia...")
    wikipedia_extract()
    print("✓ Wikipedia Extraction Completed")

    print("\n[2/9] Extracting ZimbabweYP...")
    zimbabweyp_extract()
    print("✓ ZimbabweYP Extraction Completed")

    print("\n[3/9] Extracting IBZIM O-Level Rankings...")
    ibzim_o_extract()
    print("✓ IBZIM O-Level Extraction Completed")

    print("\n[4/9] Extracting IBZIM A-Level Rankings...")
    ibzim_a_extract()
    print("✓ IBZIM A-Level Extraction Completed")

    # =====================================================
    # LOAD RAW DATA
    # =====================================================

    print("STEP:LOAD_RAW")

    print("\n[5/9] Loading Raw Datasets...")

    datasets = load_raw_data()

    print(f"✓ {len(datasets)} datasets loaded")

    # =====================================================
    # CLEAN
    # =====================================================

    print("STEP:CLEAN")

    print("\nCleaning School Names...")

    for source_name, dataset in datasets.items():

        print(f"   Cleaning {source_name}...")

        datasets[source_name] = clean_dataset(dataset)

    print("✓ School Names Cleaned")

    # =====================================================
    # STANDARDIZE
    # =====================================================

    print("STEP:STANDARDIZE")

    print("\nStandardizing Data...")

    for source_name, dataset in datasets.items():

        print(f"   Standardizing {source_name}...")

        datasets[source_name] = standardize_data(dataset)

    print("✓ Data Standardized")

    # =====================================================
    # MERGE
    # =====================================================

    print("STEP:MERGE")

    print("\n[6/9] Merging Sources...")

    master_dataset = merge_sources(datasets)

    print(f"✓ Master Dataset Created ({len(master_dataset)} schools)")

    # =====================================================
    # FILL MISSING VALUES
    # =====================================================

    print("STEP:FILL")

    print("\n[7/9] Filling Missing Values...")

    master_dataset = fill_missing_values(master_dataset)

    print("✓ Missing Values Filled")

    # =====================================================
    # VALIDATION
    # =====================================================

    print("STEP:VALIDATE")

    print("\n[8/9] Validating Dataset...")

    validate_merge(master_dataset)

    inspect_master_dataset(master_dataset)

    print("✓ Validation Completed")

    # =====================================================
    # SAVE MASTER DATASET
    # =====================================================

    print("STEP:SAVE")

    print("\nSaving Master Dataset...")

    save_master_dataset(
        master_dataset,
        "data/processed/zimbabwe_master_dataset.json"
    )

    print("✓ Master Dataset Saved")

    # =====================================================
    # LOAD POSTGRESQL
    # =====================================================

    print("STEP:POSTGRES")

    print("\n[9/9] Loading PostgreSQL Database...")

    load_postgresql()

    print("✓ PostgreSQL Database Updated")

    # =====================================================
    # COMPLETE
    # =====================================================

    print("STEP:COMPLETE")

    print("\n" + "=" * 70)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 70)
    print("✓ Data Extracted")
    print("✓ Raw Data Loaded")
    print("✓ School Names Cleaned")
    print("✓ Data Standardized")
    print("✓ Sources Merged")
    print("✓ Missing Values Filled")
    print("✓ Data Validated")
    print("✓ Master Dataset Saved")
    print("✓ PostgreSQL Updated")
    print("=" * 70)


# ==========================
# Entry Point
# ==========================

if __name__ == "__main__":

    main()