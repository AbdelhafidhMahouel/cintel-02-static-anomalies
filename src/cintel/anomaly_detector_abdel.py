"""
anomaly_detector_abdel.py - Project script (custom modification).

Author: Abdel Mahouel
Date: 2026-03-16

Static Data

- Data is taken from a pediatric clinic's patient records.
- The data is static, meaning it does not change over time and is not updated with new records.
- The clinic works with children from birth to 16 years old.
- Each row represents a patient visit with two key measurements:
  - age_years: The patient's age in years.
  - height_inches: The patient's height in inches.

Purpose

- Read the data from a CSV (comma-separated values) file.
- Detect anomalies using upper and lower threshold rules.
- Add a reason column to explain why each anomaly was flagged.
- Log the pipeline process to assist with debugging and transparency.

Paths (relative to repo root)

    INPUT FILE: data/clinic_data_abdel.csv
    OUTPUT FILE: artifacts/anomalies_abdel.csv

Terminal command to run this file from the root project folder

    uv run python -m cintel.anomaly_detector_abdel

OBS:
  This file is based on the working example provided in the repo.
  It was modified as part of Phase 4 to make a technical change.
  The custom changes include:
  - different threshold values
  - lower-bound checks
  - an anomaly_reason column in the output
"""

# === DECLARE IMPORTS (packages we will use in this project) ===

# First from the Python standard library (no installation needed)
import logging
from pathlib import Path
from typing import Final

# Third-party packages installed in the project environment
import polars as pl
from datafun_toolkit.logger import get_logger, log_header, log_path

# === CONFIGURE LOGGER ===

LOG: logging.Logger = get_logger("P2", level="DEBUG")

# === DECLARE GLOBAL CONSTANTS FOR FOLDER PATHS (directories) ===

ROOT_DIR: Final[Path] = Path.cwd()
DATA_DIR: Final[Path] = ROOT_DIR / "data"
ARTIFACTS_DIR: Final[Path] = ROOT_DIR / "artifacts"

# === DECLARE GLOBAL CONSTANTS FOR FILE PATHS ===

DATA_FILE: Final[Path] = DATA_DIR / "clinic_data_abdel.csv"
OUTPUT_FILE: Final[Path] = ARTIFACTS_DIR / "anomalies_abdel.csv"


# === DEFINE THE MAIN FUNCTION ===


def main() -> None:
    """Run the anomaly detection pipeline.

    log_header() logs a standard run header.
    log_path() logs repo-relative paths (privacy-safe).
    """
    log_header(LOG, "CINTEL")

    LOG.info("========================")
    LOG.info("START main()")
    LOG.info("========================")

    # Log the constants to help with debugging and transparency.
    log_path(LOG, "ROOT_DIR", ROOT_DIR)
    log_path(LOG, "DATA_FILE", DATA_FILE)
    log_path(LOG, "OUTPUT_FILE", OUTPUT_FILE)

    # Call the mkdir() method to ensure the artifacts directory exists.
    # The parents=True argument allows it to create any necessary parent directories.
    # The exist_ok=True argument prevents an error if the directory already exists.
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    log_path(LOG, "ARTIFACTS_DIR", ARTIFACTS_DIR)

    # ----------------------------------------------------
    # STEP 1: READ CSV DATA FILE INTO A POLARS DATAFRAME (TABLE)
    # ----------------------------------------------------
    # Polars is great for tabular data.
    # We will use the polars package to
    # read csv (comma-separated values) files
    # into a two dimensional table (DataFrame).

    # Call the polars library read_csv() method.
    # Pass in (provide) the DATA_FILE path of the CSV file.
    # Name the result "df" as is customary.
    df: pl.DataFrame = pl.read_csv(DATA_FILE)

    # Visually inspect the file in the data/ folder.
    # It has columns named `age_years` and `height_inches`.
    # The DataFrame height attribute returns the number of rows.
    LOG.info(f"Loaded {df.height} patient records")

    # ----------------------------------------------------
    # STEP 2: VALIDATE EXPECTED COLUMNS
    # ----------------------------------------------------
    # Before detecting anomalies, verify that the expected columns exist.
    # This helps avoid confusing errors later in the pipeline.
    expected_columns: set[str] = {"age_years", "height_inches"}
    actual_columns: set[str] = set(df.columns)

    if not expected_columns.issubset(actual_columns):
        missing_columns = expected_columns - actual_columns
        raise ValueError(f"Missing required columns: {missing_columns}")

    LOG.info("Required columns are present")

    # ----------------------------------------------------
    # STEP 3: DEFINE THRESHOLDS AND DETECT ANOMALIES
    # ----------------------------------------------------
    # An anomaly is any value outside the threshold range we set.
    # In the example file, only upper limits were checked.
    # In this modified version, we check both lower and upper limits.
    LOG.info("Studying children's ages and heights to find anomalies...")

    # x is age in years
    # For this custom version:
    # - age should not be negative
    # - age 15 or higher will be flagged as suspicious
    MIN_REASONABLE_X_VALUE: Final[float] = 0.0
    MAX_REASONABLE_X_VALUE: Final[float] = 15.0

    # y is height in inches
    # For this custom version:
    # - height below 20 inches is suspicious
    # - height 70 inches or higher is suspicious
    MIN_REASONABLE_Y_VALUE: Final[float] = 20.0
    MAX_REASONABLE_Y_VALUE: Final[float] = 70.0

    LOG.info(f"MIN_REASONABLE_X_VALUE: {MIN_REASONABLE_X_VALUE} in years")
    LOG.info(f"MAX_REASONABLE_X_VALUE: {MAX_REASONABLE_X_VALUE} in years")
    LOG.info(f"MIN_REASONABLE_Y_VALUE: {MIN_REASONABLE_Y_VALUE} in inches")
    LOG.info(f"MAX_REASONABLE_Y_VALUE: {MAX_REASONABLE_Y_VALUE} in inches")

    # Create a new DataFrame named anomalies_df that contains
    # only the rows where EITHER
    # the age is TOO LOW OR
    # the age is TOO HIGH OR
    # the height is TOO LOW OR
    # the height is TOO HIGH.
    #
    # A single pipe (|) is the OR operator in polars.
    #
    # We also add a new column named anomaly_reason
    # to explain why each row was flagged.
    anomalies_df: pl.DataFrame = (
        df.filter(
            (pl.col("age_years") < MIN_REASONABLE_X_VALUE)
            | (pl.col("age_years") >= MAX_REASONABLE_X_VALUE)
            | (pl.col("height_inches") < MIN_REASONABLE_Y_VALUE)
            | (pl.col("height_inches") >= MAX_REASONABLE_Y_VALUE)
        )
        .with_columns(
            pl.when(pl.col("age_years") < MIN_REASONABLE_X_VALUE)
            .then(pl.lit("age too low"))
            .when(pl.col("age_years") >= MAX_REASONABLE_X_VALUE)
            .then(pl.lit("age too high"))
            .when(pl.col("height_inches") < MIN_REASONABLE_Y_VALUE)
            .then(pl.lit("height too low"))
            .when(pl.col("height_inches") >= MAX_REASONABLE_Y_VALUE)
            .then(pl.lit("height too high"))
            .otherwise(pl.lit("unknown"))
            .alias("anomaly_reason")
        )
        .sort(["age_years", "height_inches"])
    )

    LOG.info(f"Count of anomalies found: {anomalies_df.height}")

    # ----------------------------------------------------
    # STEP 4: SAVE THE OUTPUT ANOMALIES AS EVIDENCE
    # ----------------------------------------------------
    # We call generated files "artifacts".
    # They are important evidence of the work we did and the results we found.
    # We will save the anomalies_df DataFrame as a CSV file in the artifacts/ folder.

    # Every Polars DataFrame has a write_csv() method that saves it as a CSV file.
    # Just pass in the full Path to the file you want to create.
    anomalies_df.write_csv(OUTPUT_FILE)
    LOG.info(f"Wrote anomalies file: {OUTPUT_FILE}")

    LOG.info("========================")
    LOG.info("Pipeline executed successfully!")
    LOG.info("========================")
    LOG.info("END main()")


# === CONDITIONAL EXECUTION GUARD ===

if __name__ == "__main__":
    main()
