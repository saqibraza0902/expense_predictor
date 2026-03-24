import re
import pandas as pd
from datetime import datetime
from dateutil import parser as dateutil_parser


# ---------------------------------------------------------------------------
# Category normalisation map
# Each key is the canonical name; values are all known dirty variants.
# ---------------------------------------------------------------------------
CATEGORY_MAP: dict[str, list[str]] = {
    "Restaurant":       ["restaurant", "restuarant", "restaurent", "resto", "restaurante"],
    "Market":           ["market", "supermarket", "grocery"],
    "Transport":        ["transport", "transportation", "transports"],
    "Coffee":           ["coffee", "coffe", "cafe"],
    "Phone":            ["phone", "phone bill", "mobile"],
    "Communal":         ["communal", "utilities"],
    "Clothing":         ["clothing", "clothes"],
    "Motel":            ["motel", "hotel"],
    "Travel":           ["travel", "travelling"],
    "Rent Car":         ["rent car", "rentcar", "car rental"],
    "Sport":            ["sport", "sports"],
    "Events":           ["events", "event"],
    "Learning":         ["learning", "education"],
    "Health":           ["health", "healthcare"],
    "Taxi":             ["taxi", "cab"],
    "Business Lunch":   ["business lunch", "business_lunch", "biz lunch"],
    "Film/Enjoyment":   ["film/enjoyment", "film", "entertainment"],
    "Tech":             ["tech", "technology"],
    "Fuel":             ["fuel", "gas"],
    "Rent":             ["rent", "rental"],
    "Other":            ["other", "misc", "miscellaneous"],
}

# Build a flat lookup: lowercase dirty variant -> canonical name
_CATEGORY_LOOKUP: dict[str, str] = {}
for canonical, variants in CATEGORY_MAP.items():
    _CATEGORY_LOOKUP[canonical.lower()] = canonical   # canonical itself
    for v in variants:
        _CATEGORY_LOOKUP[v.lower()] = canonical


# ---------------------------------------------------------------------------
# Date helpers
# ---------------------------------------------------------------------------

# Explicit format list — tried in order before falling back to dateutil.
# Ordered from most specific to least to avoid mis-parses.
_DATE_FORMATS = [
    "%Y-%m-%d %H:%M:%S %z",   # 2022-07-06 05:57:10 +0000
    "%Y-%m-%d %H:%M:%S",      # 2022-07-06 05:57:10
    "%m-%d-%Y %H:%M",         # 01-24-2023 18:43  (US with time)
    "%d-%m-%Y %H:%M",         # 24-01-2023 18:43  (EU with time)
    "%m-%d-%Y",               # 01-24-2023
    "%d/%m/%Y",               # 22/11/2024
    "%Y/%m/%d",               # 2023/05/05
    "%Y%m%d",                 # 20231005
    "%d-%b-%Y",               # 16-Nov-2023
    "%B %d, %Y",              # August 27, 2023
    "%b %d, %Y",              # Aug 27, 2023
]


def _parse_single_date(raw: str):
    """Try every known format, then fall back to dateutil."""
    if not isinstance(raw, str) or raw.strip() == "":
        return pd.NaT

    raw = raw.strip()

    # 1. Try explicit formats first (faster and unambiguous)
    for fmt in _DATE_FORMATS:
        try:
            return pd.Timestamp(datetime.strptime(raw, fmt))
        except (ValueError, TypeError):
            continue

    # 2. Compact YYYYMMDD without separators
    if re.fullmatch(r"\d{8}", raw):
        try:
            return pd.Timestamp(datetime.strptime(raw, "%Y%m%d"))
        except ValueError:
            pass

    # 3. Last resort: dateutil (handles many edge cases automatically)
    try:
        return pd.Timestamp(dateutil_parser.parse(raw, dayfirst=False))
    except Exception:
        pass

    return pd.NaT


def _clean_dates(series: pd.Series) -> pd.Series:
    """
    Parse a mixed-format date column robustly.
    Every timestamp is normalised to UTC to avoid tz-aware/tz-naive conflicts.
    """
    def parse_one(val):
        if pd.isna(val) or str(val).strip() == "":
            return pd.NaT
        raw = str(val).strip()
        # Try explicit formats first
        for fmt in _DATE_FORMATS:
            try:
                dt = datetime.strptime(raw, fmt)
                ts = pd.Timestamp(dt)
                return ts.tz_localize("UTC") if ts.tzinfo is None else ts.tz_convert("UTC")
            except (ValueError, TypeError):
                continue
        # Compact YYYYMMDD
        if re.fullmatch(r"\d{8}", raw):
            try:
                ts = pd.Timestamp(datetime.strptime(raw, "%Y%m%d"))
                return ts.tz_localize("UTC")
            except ValueError:
                pass
        # Last resort: dateutil
        try:
            ts = pd.Timestamp(dateutil_parser.parse(raw, dayfirst=False))
            return ts.tz_localize("UTC") if ts.tzinfo is None else ts.tz_convert("UTC")
        except Exception:
            pass
        return pd.NaT

    parsed = pd.to_datetime(series.apply(parse_one), utc=True, errors="coerce")
    unparseable = parsed.isna().sum()
    if unparseable:
        print(f"  ⚠  {unparseable} date(s) could not be parsed and were set to NaT.")
    else:
        print(f"  ✔  All dates parsed successfully.")
    return parsed


# ---------------------------------------------------------------------------
# Amount helpers
# ---------------------------------------------------------------------------

def _clean_amounts(series: pd.Series) -> pd.Series:
    """
    Coerce a mixed amount column to float.
    - Strips whitespace, currency symbols, thousand-separators
    - Drops non-numeric strings ('N/A', 'unknown', '??', ...)
    - Drops negative values (treats them as data errors)
    - Leaves genuine NaN so callers can decide how to impute
    """
    cleaned = (
        series
        .astype(str)
        .str.strip()
        .str.replace(r"[^\d.\-]", "", regex=True)   # keep digits, dot, minus
        .replace("", pd.NA)
    )

    numeric = pd.to_numeric(cleaned, errors="coerce")

    # Negative amounts → NaN (data error, not a credit)
    negative_count = (numeric < 0).sum()
    if negative_count:
        print(f"  ⚠  {negative_count} negative amount(s) replaced with NaN.")
    numeric[numeric < 0] = pd.NA

    null_count = numeric.isna().sum()
    if null_count:
        print(f"  ⚠  {null_count} amount(s) could not be parsed and were set to NaN.")

    print(f"  ✔  Amount range after cleaning: {numeric.min():.2f} → {numeric.max():.2f}")
    return numeric


# ---------------------------------------------------------------------------
# Category helpers
# ---------------------------------------------------------------------------

def _clean_categories(series: pd.Series) -> pd.Series:
    """Normalise free-text categories to canonical names."""
    def normalise(val: str) -> str:
        if not isinstance(val, str) or val.strip() == "":
            return "Other"
        key = val.strip().lower()
        return _CATEGORY_LOOKUP.get(key, val.strip().title())   # unknown → title-case as-is

    cleaned = series.apply(normalise)
    unknown = cleaned[~cleaned.isin(CATEGORY_MAP.keys())]
    if not unknown.empty:
        print(f"  ⚠  {len(unknown.unique())} unrecognised category value(s): {unknown.unique().tolist()}")
    return cleaned


# ---------------------------------------------------------------------------
# Transaction ID helpers
# ---------------------------------------------------------------------------

def _clean_transaction_ids(series: pd.Series, n_rows: int) -> pd.Series:
    """
    Coerce to Int64, fill missing IDs with auto-generated sequential values
    that don't clash with existing IDs.
    """
    numeric = pd.to_numeric(series, errors="coerce").astype("Int64")
    missing_mask = numeric.isna()
    missing_count = missing_mask.sum()

    if missing_count:
        existing_ids = set(numeric.dropna().astype(int))
        max_id = max(existing_ids) if existing_ids else n_rows
        new_ids = []
        candidate = max_id + 1
        for _ in range(missing_count):
            while candidate in existing_ids:
                candidate += 1
            new_ids.append(candidate)
            existing_ids.add(candidate)
            candidate += 1
        numeric.loc[missing_mask] = new_ids
        print(f"  ⚠  {missing_count} missing transaction_id(s) filled with new sequential IDs.")

    return numeric