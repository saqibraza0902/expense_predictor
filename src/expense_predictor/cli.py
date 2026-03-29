import sys
import matplotlib.pyplot as plt

from .analyzer import load_data, compute_monthly_totals, detect_large_transactions
from .predictor import predict_next
from .recommendations import generate_recommendations
from .transactions import list_transactions, add_transaction, delete_transaction, update_transaction
from .visualizer import (plot_moving_average, plot_category_breakdown, plot_monthly_trend)

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m expense_predictor <command> <filepath> [args]")
        print("\nCommands:")
        print("  analyze <filepath>              - Analyze transactions")
        print("  list <filepath>                 - List all transactions")
        print("  add <filepath> <date> <category> <amount> - Add transaction")
        print("  delete <filepath> <index>       - Delete transaction")
        print("  update <filepath> <index> <amount> - Update transaction amount")
        print("  recommendations <filepath>      - Get spending recommendations")
        print("  visualize <filepath>            - Show visualizations")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if len(sys.argv) < 3 and command != "analyze":
        print(f"Error: Missing filepath for command '{command}'")
        sys.exit(1)
    
    filepath = sys.argv[2] if len(sys.argv) > 2 else None
    
    if command == "analyze":
        if not filepath:
            print("Error: Missing filepath for analyze command")
            sys.exit(1)
        
        print(f"Analyzing file: {filepath}")
        df = load_data(filepath)
        
        monthly_totals = compute_monthly_totals(df)
        
        print("\n📊 Monthly Totals:")
        print(monthly_totals)
        
        unusual = detect_large_transactions(df)
        if not unusual.empty:
            print("\n⚠️ Unusual Transactions Detected:")
            print(unusual[['date', 'category', 'amount', 'z_score']].head())
        
        prediction = predict_next(monthly_totals)
        print(f"\n🔮 Predicted Next Month Spending: {prediction:.2f}")
        
        # Ask if user wants to see visualization
        print("\n📈 Generating visualization...")
        plt.figure(figsize=[10, 5])
        plt.plot(monthly_totals.index, monthly_totals.values, marker='o')
        plt.title("Monthly Spending Trend")
        plt.xlabel("Month")
        plt.ylabel("Total Spending ($)")
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        
    elif command == "list":
        list_transactions(filepath)
        
    elif command == "add":
        if len(sys.argv) < 6:
            print("Usage: add <filepath> <date> <category> <amount>")
            sys.exit(1)
        date = sys.argv[3]
        category = sys.argv[4]
        amount = float(sys.argv[5])
        add_transaction(filepath, date, category, amount)
        print(f"✅ Added transaction: {date} - {category} - ${amount:.2f}")
        
    elif command == "delete":
        if len(sys.argv) < 4:
            print("Usage: delete <filepath> <index>")
            sys.exit(1)
        idx = int(sys.argv[3])
        delete_transaction(filepath, idx)
        print(f"✅ Deleted transaction at index {idx}")
        
    elif command == "update":
        if len(sys.argv) < 5:
            print("Usage: update <filepath> <index> <amount>")
            sys.exit(1)
        idx = int(sys.argv[3])
        amount = float(sys.argv[4])
        update_transaction(filepath, idx, amount)
        print(f"✅ Updated transaction at index {idx} to ${amount:.2f}")
        
    elif command == "recommendations":
        df = load_data(filepath)
        recs = generate_recommendations(df)
        print("\n💡 Spending Recommendations:")
        for i, r in enumerate(recs, 1):
            print(f"{i}. {r}")
            
    elif command == "visualize":
        print("📊 Generating visualizations...")
        plot_moving_average(filepath)
        plot_category_breakdown(filepath)
        plot_monthly_trend(filepath)
        
    else:
        print(f"Unknown command: {command}")
        print("Available commands: analyze, list, add, delete, update, recommendations, visualize")
        sys.exit(1)