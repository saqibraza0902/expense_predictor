import pandas as pd
import matplotlib.pyplot as plt
from .helpers import (
    _clean_dates,
    _clean_amounts,
    _clean_categories,
    _clean_transaction_ids
)

def load_data(file_path):
    df = pd.read_csv(file_path)

    # print("🔄 Cleaning data...\n")

    # --- Apply your helpers ---
    if 'date' in df.columns:
        df['date'] = _clean_dates(df['date'])

    if 'amount' in df.columns:
        df['amount'] = _clean_amounts(df['amount'])

    if 'category' in df.columns:
        df['category'] = _clean_categories(df['category'])

    if 'transaction_id' in df.columns:
        df['transaction_id'] = _clean_transaction_ids(df['transaction_id'], len(df))

    # --- Drop bad rows ---
    df = df.dropna(subset=['date', 'amount'])

    # Remove timezone for plotting (optional but clean)
    df['date'] = df['date'].dt.tz_localize(None)

    # print("\n✅ Data cleaning complete.\n")

    return df


# 🔹 1. Moving Average Visualization
def plot_moving_average(file_path, window=7):
    df = load_data(file_path)
    df = df.sort_values('date')

    df['moving_avg'] = df['amount'].rolling(window=window).mean()

    plt.figure(figsize=(12, 6))
    plt.plot(df['date'], df['amount'], label='Daily Spending')
    plt.plot(df['date'], df['moving_avg'], label=f'{window}-Day Moving Average')

    plt.title('Spending Trend with Moving Average')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# 🔹 2. Category Breakdown
def plot_category_breakdown(file_path):
    df = load_data(file_path)

    category_sum = df.groupby('category')['amount'].sum()

    plt.figure(figsize=(12, 6))
    category_sum.plot(kind='bar')
    plt.title('Spending by Category')
    plt.xlabel('Category')
    plt.ylabel('Total Spending')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# 🔹 3. Monthly Trend
def plot_monthly_trend(file_path):
    df = load_data(file_path)
    df['month'] = df['date'].dt.to_period('M')
    monthly = df.groupby('month')['amount'].sum()
    plt.figure(figsize=(12, 6))
    monthly.plot()
    plt.title('Monthly Spending Trend')
    plt.xlabel('Month')
    plt.ylabel('Total Spending')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()