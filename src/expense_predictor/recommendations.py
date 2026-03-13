import pandas as pd


def generate_recommendations(df: pd.DataFrame):
    recommendations = []

    category_spending = df.groupby("category")["amount"].sum()

    highest_category = category_spending.idxmax()
    highest_amount = category_spending.max()

    # High spending warning
    recommendations.append(
        f"You spend the most on '{highest_category}' (${highest_amount:.2f}). "
        "Consider reviewing this category to reduce expenses."
    )

    # Average spending check
    avg_spending = df["amount"].mean()

    if avg_spending > 100:
        recommendations.append(
            "Your average transaction amount is relatively high. "
            "Try to track small purchases more carefully."
        )
    else:
        recommendations.append(
            "Your spending per transaction looks reasonable. Keep monitoring it."
        )

    # Category count
    if len(category_spending) > 5:
        recommendations.append(
            "You spend across many categories. Creating a monthly budget could help manage spending."
        )

    return recommendations