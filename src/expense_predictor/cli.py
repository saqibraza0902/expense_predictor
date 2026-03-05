import sys
import matplotlib.pyplot as plt

from .analyzer import load_data, compute_monthly_totals, detect_large_transactions
from .predictor import predict_next


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m expense_predictor <data.csv>")
        sys.exit(1)

    filepath = sys.argv[1]

    df = load_data(filepath)

    monthly_totals = compute_monthly_totals(df)

    print("\n📊 Monthly Totals:")
    print(monthly_totals)

    unusual = detect_large_transactions(df)
    if not unusual.empty:
        print("\n⚠️ Unusual Transactions Detected:")
        print(unusual)

    prediction = predict_next(monthly_totals)

    print(f"\n🔮 Predicted Next Month Spending: {prediction:.2f}")

    # Visualization
    plt.figure()
    plt.plot(monthly_totals.index, monthly_totals.values)
    plt.title("Monthly Spending Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Spending")
    plt.show()