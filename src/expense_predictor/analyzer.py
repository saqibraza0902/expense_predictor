import pandas as pd


def load_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)  # type: ignore

    # Try to parse dates with mixed formats
    df["date"] = pd.to_datetime(df["date"], dayfirst=False, errors='coerce')

    # For dates that couldn't be parsed, try with day first=True
    mask = df["date"].isna()
    if mask.any():
        df.loc[mask, "date"] = pd.to_datetime(df.loc[mask, "date"], dayfirst=True, errors='coerce')

    # Clean the amount column
    if 'amount' in df.columns:
        # Convert to string first
        df['amount'] = df['amount'].astype(str)

        # Remove any non-numeric characters EXCEPT decimal point (remove minus sign too)
        df['amount'] = df['amount'].str.replace(r'[^\d.]', '', regex=True)

        # Handle empty strings
        df['amount'] = df['amount'].replace('', '0')

        # Convert to float
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

        print(f"Amount column cleaned. Range: {df['amount'].min()} to {df['amount'].max()}")
        print(f"Sample amounts: {df['amount'].head().tolist()}")
    else:
        print("Warning: No 'amount' column found. Available columns:", df.columns.tolist())

    print(df.head())
    df = df.sort_values("date")

    return df


def compute_monthly_totals(df: pd.DataFrame) -> pd.Series:
    monthly = (
        df.resample("ME", on="date")["amount"]
        .sum()
    )
    return monthly


def detect_large_transactions(df: pd.DataFrame):
    mean = df["amount"].mean()
    std = df["amount"].std()

    threshold = mean + 2 * std

    unusual = df[df["amount"] > threshold]

    return unusual
