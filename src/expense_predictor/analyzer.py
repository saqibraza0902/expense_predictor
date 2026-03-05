import pandas as pd


def load_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)

    df["date"] = pd.to_datetime(df["date"])
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
