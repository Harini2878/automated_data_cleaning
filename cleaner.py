
import pandas as pd


def clean_data(df):

    # Handle missing values
    df["name"] = df["name"].fillna("Unknown")
    df["email"] = df["email"].fillna("Not Available")

    # Clean currency values
    def clean_currency(value):
        if pd.isna(value):
            return None

        value = str(value)
        value = value.replace("₹", "")
        value = value.replace("$", "")
        value = value.replace(",", "")
        value = value.strip()

        return pd.to_numeric(value, errors="coerce")

    df["amount"] = df["amount"].apply(clean_currency)

    if df["amount"].notna().any():
        df["amount"] = df["amount"].fillna(df["amount"].median())
    else:
        df["amount"] = df["amount"].fillna(0)

    # Normalize dates
    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce",
        dayfirst=True
    )

    # Remove invalid dates
    df = df.dropna(subset=["date"])

    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    # Remove duplicate records
    df = df.drop_duplicates()

    # Standardize text
    df["name"] = df["name"].astype(str).str.strip().str.title()
    df["email"] = df["email"].astype(str).str.strip().str.lower()

    return df
