import pandas as pd
from .helpers import _clean_dates, _clean_amounts, _clean_categories, _clean_transaction_ids
# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def load_data(filepath: str) -> pd.DataFrame:
    """
    Load a transactions CSV and apply full cleaning:
      - Robust multi-format date parsing
      - Amount coercion (strips symbols, removes negatives & junk strings)
      - Category normalisation (case, typos, synonyms)
      - Transaction ID gap-filling
    """
    print(f"\n{'='*60}")
    print(f"Loading: {filepath}")
    print(f"{'='*60}")

    df = pd.read_csv(filepath, dtype=str)   # read everything as str first
    print(f"  Rows loaded: {len(df)}")

    # --- dates ---
    if "date" in df.columns:
        print("\n[date]")
        df["date"] = _clean_dates(df["date"])
    else:
        print("  ⚠  No 'date' column found.")

    # --- amounts ---
    if "amount" in df.columns:
        print("\n[amount]")
        df["amount"] = _clean_amounts(df["amount"])
    else:
        print("  ⚠  No 'amount' column found.")

    # --- categories ---
    if "category" in df.columns:
        print("\n[category]")
        df["category"] = _clean_categories(df["category"])
        print(f"  ✔  Unique categories after normalisation: {len(df['category'].unique())}")
    else:
        print("  ⚠  No 'category' column found.")

    # --- transaction IDs ---
    if "transaction_id" in df.columns:
        print("\n[transaction_id]")
        df["transaction_id"] = _clean_transaction_ids(df["transaction_id"], len(df))

    # --- sort by date ---
    df = df.sort_values("date").reset_index(drop=True)

    print(f"\n  ✔  Final shape: {df.shape}")
    print(df.head(3).to_string())
    return df


def compute_monthly_totals(df: pd.DataFrame) -> pd.Series:
    """
    Sum transaction amounts by calendar month.
    Drops rows where date or amount is NaT/NaN before aggregating.
    """
    clean = df.dropna(subset=["date", "amount"]).copy()
    clean["date"] = pd.to_datetime(clean["date"], utc=True)

    monthly = (
        clean
        .resample("ME", on="date")["amount"]
        .sum()
    )
    return monthly


def detect_large_transactions(df: pd.DataFrame, z_score_threshold: float = 2.0) -> pd.DataFrame:
    """
    Flag transactions whose amount is more than `z_score_threshold` standard
    deviations above the mean.

    Returns a DataFrame with an extra 'z_score' column so callers can see
    how extreme each flagged transaction is.
    Skips rows with NaN amounts to avoid skewing the statistics.
    """
    clean = df.dropna(subset=["amount"]).copy()

    mean = clean["amount"].mean()
    std  = clean["amount"].std()

    if std == 0:
        print("  ⚠  Standard deviation is 0 — all amounts are identical.")
        return clean.iloc[0:0]   # empty frame with correct columns

    threshold = mean + z_score_threshold * std

    clean["z_score"] = ((clean["amount"] - mean) / std).round(2)
    unusual = clean[clean["amount"] > threshold].copy()

    print(f"\n[detect_large_transactions]")
    print(f"  Mean: {mean:.2f} | Std: {std:.2f} | Threshold (z>{z_score_threshold}): {threshold:.2f}")
    print(f"  {len(unusual)} large transaction(s) detected out of {len(clean)} valid rows.")

    return unusual.sort_values("amount", ascending=False).reset_index(drop=True)