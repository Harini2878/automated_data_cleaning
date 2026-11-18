
REQUIRED_COLUMNS = ["name", "email", "amount", "date"]


def validate_data(df):

    report = []

    # Check required columns
    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:
        report.append(
            f"Missing columns: {missing_columns}"
        )
        return False, report

    report.append("Schema validation: PASSED")

    # Check missing values
    null_count = int(df.isnull().sum().sum())

    report.append(
        f"Missing values: {null_count}"
    )

    # Check duplicate records
    duplicate_count = int(df.duplicated().sum())

    report.append(
        f"Duplicate records: {duplicate_count}"
    )

    # Check data types
    report.append(
        f"Data types:\n{df.dtypes.to_string()}"
    )

    report.append("Validation completed successfully.")

    return True, report
