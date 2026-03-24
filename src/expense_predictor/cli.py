import sys
import matplotlib.pyplot as plt

from .analyzer import load_data, compute_monthly_totals, detect_large_transactions
from .predictor import predict_next
from .recommendations import generate_recommendations
from .transactions import list_transactions, add_transaction, delete_transaction, update_transaction
from .visualizer import (plot_moving_average,plot_category_breakdown,plot_monthly_trend)

def main():
    command = sys.argv[1]
    filepath = sys.argv[2]
    print(command, filepath)
    if filepath and command == "analyze":
        print("Usage: python -m expense_predictor <data.csv>")
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
        plt.figure(figsize=[10, 5])
        plt.plot(monthly_totals.index, monthly_totals.values)
        plt.title("Monthly Spending Trend")
        plt.xlabel("Month")
        plt.ylabel("Total Spending")
        plt.xticks(rotation=45)
        plt.show()
        sys.exit(1)
    elif command == "list":
        list_transactions(filepath)

    elif command == "add":
        date = sys.argv[3]
        category = sys.argv[4]
        amount = float(sys.argv[5])
        add_transaction(filepath, date,category, amount)

    elif command == "delete":
        idx = int(sys.argv[3])
        delete_transaction(filepath, idx)

    elif command == "update":
        idx = int(sys.argv[3])
        amount = float(sys.argv[4])
        update_transaction(filepath, idx, amount)
    elif command == "recommendations":
        df = load_data(filepath)
        recs = generate_recommendations(df)

        for r in recs:
            print("-", r)
    elif command == "visualize":
        plot_moving_average(filepath)
        plot_category_breakdown(filepath)
        plot_monthly_trend(filepath)
    else:
        print("Unknown command")