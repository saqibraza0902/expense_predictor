import pandas as pd
import matplotlib.pyplot as plt

def load_data(file_path):
    df = pd.read_csv(file_path)

    # Convert to datetime and force everything into same timezone
    df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)

    # Remove timezone (make it clean datetime)
    df['date'] = df['date'].dt.tz_localize(None)

    # Drop invalid rows
    df = df.dropna(subset=['date'])

    return df


# 🔹 1. Moving Average Visualization
def plot_moving_average(file_path, window=7):
    df = load_data(file_path)
    df = df.sort_values('date')

    df['moving_avg'] = df['amount'].rolling(window=window).mean()

    plt.figure()
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

    plt.figure()
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

    plt.figure()
    monthly.plot()

    plt.title('Monthly Spending Trend')
    plt.xlabel('Month')
    plt.ylabel('Total Spending')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()