
import pandas as pd
import os
from datetime import datetime

from cleaner import clean_data
from validator import validate_data


# File paths
INPUT_FILE = "dirty_dataset.csv"
OUTPUT_FOLDER = "output"

OUTPUT_FILE = os.path.join(
    OUTPUT_FOLDER, "clean_dataset.csv"
)

REPORT_FILE = os.path.join(
    OUTPUT_FOLDER, "validation_report.txt"
)


def main():

    print("AUTOMATED DATA CLEANING STARTED")

    # Create output folder
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Read original dataset
    df = pd.read_csv(INPUT_FILE)

    original_records = len(df)
    original_nulls = int(df.isnull().sum().sum())

    print("Original records:", original_records)

    # Clean dataset
    cleaned_df = clean_data(df)

    # Validate cleaned dataset
    is_valid, report = validate_data(cleaned_df)

    # Save cleaned dataset
    cleaned_df.to_csv(OUTPUT_FILE, index=False)

    # Generate validation report
    with open(REPORT_FILE, "w") as file:

        file.write("AUTOMATED DATA CLEANING REPORT\n")
        file.write("=" * 40 + "\n")

        file.write(
            "Date: " + str(datetime.now()) + "\n"
        )

        file.write(
            f"Original records: {original_records}\n"
        )

        file.write(
            f"Final records: {len(cleaned_df)}\n"
        )

        file.write(
            f"Original missing values: {original_nulls}\n"
        )

        file.write("\nVALIDATION DETAILS\n")
        file.write("-" * 40 + "\n")

        for item in report:
            file.write(item + "\n")

        file.write(
            "\nFinal Status: " +
            ("SUCCESS" if is_valid else "FAILED")
        )

    print("\nDATA CLEANING COMPLETED!")
    print("Cleaned dataset saved:", OUTPUT_FILE)
    print("Validation report saved:", REPORT_FILE)

    print("\nCleaned Data:")
    print(cleaned_df)


if __name__ == "__main__":
    main()
