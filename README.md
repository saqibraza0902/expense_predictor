# 💰 Expense Predictor

### *A Smart Financial Analysis Tool for Personal Spending Management*

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [Data Format](#data-format)
- [Examples](#examples)
- [Technical Details](#technical-details)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

**Expense Predictor** is a sophisticated Python package that transforms raw transaction data into actionable financial insights. By combining robust data cleaning, statistical analysis, and machine learning predictions, it helps users understand spending patterns and make informed financial decisions.

**Key Capabilities:**
- 📊 Automatic data cleaning and normalization
- 🔮 Future spending prediction using linear regression
- 🚨 Detection of anomalous transactions
- 💡 Personalized spending recommendations
- ✏️ Complete transaction management (CRUD operations)
- 📈 Interactive data visualizations

---

## ✨ Key Features

### 1. **Intelligent Data Processing**
- **Multi-format date parsing** - Supports 15+ date formats automatically
- **Smart amount cleaning** - Removes currency symbols, handles negatives, normalizes values
- **Category normalization** - Maps synonyms to canonical categories (e.g., "restuarant" → "Restaurant")
- **Auto-generated transaction IDs** - Intelligently fills missing IDs without conflicts

### 2. **Financial Analytics**
- **Monthly spending trends** - Aggregated by calendar month
- **Statistical anomaly detection** - Identifies unusual transactions using z-score analysis
- **Category breakdown** - Understand where your money goes
- **Moving average analysis** - Smooth out daily fluctuations

### 3. **Predictive Capabilities**
- **Custom linear regression** - Built from scratch (no external ML libraries)
- **Next-month spending forecast** - Based on historical patterns
- **Trend analysis** - Visualize spending trajectories

### 4. **Transaction Management**
- **Create** - Add new transactions via CLI
- **Read** - List and view all transactions
- **Update** - Modify transaction amounts
- **Delete** - Remove erroneous entries

### 5. **Visualization Suite**
- Monthly spending trends with matplotlib
- Category-wise expenditure breakdown
- Moving average overlays for trend detection
- Interactive notebook-based exploration

---

## 📁 Project Structure

```
expense-predictor/
│
├── 📂 src/expense_predictor/          # Main package directory
│   ├── __init__.py                    # Package initializer
│   ├── __main__.py                    # Entry point for module execution
│   ├── analyzer.py                    # Data loading & statistical analysis
│   ├── cli.py                         # Command-line interface handler
│   ├── helpers.py                     # Utility functions (cleaning, parsing)
│   ├── predictor.py                   # Linear regression prediction engine
│   ├── recommendations.py             # Spending recommendation generator
│   ├── transactions.py                # CRUD operations for transactions
│   └── visualizer.py                  # Plotting and visualization functions
│
├── 📂 data/                           # Sample datasets
│   ├── transactions.csv               # Primary transaction data
│   └── transactions_*.csv             # Additional test datasets
│
├── 📂 notebooks/                      # Jupyter notebooks for exploration
│   ├── analysis.ipynb                 # Data analysis walkthrough
│   └── transactions.ipynb             # Transaction management demo
│
├── 📄 main.py                         # Simple entry point script
├── 📄 pyproject.toml                  # Package configuration
└── 📄 README.md                       # This file
```

---

## 🚀 Installation

### Prerequisites
- **Python 3.10** or higher
- **uv** package manager (recommended) or pip

### Step-by-Step Installation

```bash
# 1. Clone the repository
git clone https://github.com/saqibraza0902/expense-predictor.git
cd expense-predictor

# 2. Install using uv (fast, modern Python package manager)
uv pip install -e .

# 3. Verify installation
uv run -m expense_predictor

# 3. Run jupyter notebook
uv run --with jupyter jupyter lab
```

**Alternative installation with pip:**
```bash
pip install -e .
```

---

## ⚡ Quick Start

Get up and running in 30 seconds:

```bash
# Analyze and predict your spending data
uv run -m expense_predictor analyze data/transactions.csv

# Get personalized recommendations
uv run -m expense_predictor recommendations data/transactions.csv
```

---

## 📖 Usage Guide

### Command Line Interface (CLI)

The package provides a comprehensive CLI with multiple commands:

| Command | Description | Example |
|---------|-------------|---------|
| `analyze` | Full analysis with visualizations | `uv run -m expense_predictor analyze data.csv` | |
| `list` | Display all transactions | `uv run -m expense_predictor list data.csv` |
| `add` | Add a new transaction | `uv run -m expense_predictor add data.csv "2024-01-15" "Restaurant" 45.50` |
| `update` | Modify transaction amount | `uv run -m expense_predictor update data.csv 5 60.00` |
| `delete` | Remove a transaction | `uv run -m expense_predictor delete data.csv 5` |
| `recommendations` | Generate spending advice | `uv run -m expense_predictor recommendations data.csv` |
| `visualize` | Show spending charts | `uv run -m expense_predictor visualize data.csv` |

### Python API Usage

```python
from expense_predictor.analyzer import load_data, compute_monthly_totals
from expense_predictor.predictor import predict_next
from expense_predictor.recommendations import generate_recommendations

# Load and clean your data
df = load_data("data/transactions.csv")

# Calculate monthly spending patterns
monthly_totals = compute_monthly_totals(df)
print(f"Average monthly spending: ${monthly_totals.mean():.2f}")

# Predict future spending
next_month_prediction = predict_next(monthly_totals)
print(f"Expected spending next month: ${next_month_prediction:.2f}")

# Get actionable insights
recommendations = generate_recommendations(df)
for rec in recommendations:
    print(f"💡 {rec}")
```



---

## 📊 Data Format

Your CSV file should follow this structure:

| Column | Type | Required | Description | Example |
|--------|------|----------|-------------|---------|
| `date` | string | ✅ Yes | Transaction date (any common format) | `2024-01-15`, `15/01/2024`, `Jan 15, 2024` |
| `amount` | number | ✅ Yes | Transaction amount (positive numbers) | `45.50`, `$89.99`, `-120.00` (negatives become NaN) |
| `category` | string | ✅ Yes | Spending category (auto-normalized) | `Restaurant`, `Market`, `Transport` |


### Supported Date Formats
The parser handles 15+ formats automatically, including:
- `2024-01-15` (ISO format)
- `01/15/2024` (US format)
- `15/01/2024` (European format)
- `January 15, 2024` (Natural language)
- `20240115` (Compact format)

### Category Normalization
Common misspellings and synonyms are automatically mapped:
- `restuarant`, `resto`, `restaurent` → `Restaurant`
- `grocery`, `supermarket` → `Market`
- `uber`, `taxi`, `cab` → `Taxi`

---

## 💡 Examples

### Example 1: Complete Financial Analysis

```bash
$ uv run -m expense_predictor analyze data/transactions.csv

📊 Monthly Totals:
2024-01    1245.50
2024-02    1567.30
2024-03    1123.80

⚠️ Unusual Transactions Detected:
   date       category    amount  z_score
0  2024-02-15 Electronics  950.00     2.45
1  2024-01-20    Rent      800.00     1.98

🔮 Predicted Next Month Spending: 1345.20

💡 Recommendations:
1. You spend the most on 'Rent' ($800.00). Consider reviewing this category.
2. Your average transaction amount is relatively high.
3. You spend across many categories. Creating a budget could help.
```

### Example 2: Managing Transactions

```bash
# Add a coffee expense
$ uv run -m expense_predictor add data/transactions.csv "2024-03-25" "Coffee" 4.50
✅ Added: 2024-03-25 | Coffee | $4.50

# Update a transaction
$ uv run -m expense_predictor update data/transactions.csv 15 65.00
✅ Updated transaction at index 15 from $45.50 to $65.00

# List all transactions
$ uv run -m expense_predictor list data/transactions.csv
    date        category     amount
0   2024-01-15  Restaurant   45.50
1   2024-01-16  Market       89.99
...
```

---

## 🔧 Technical Details

### Core Algorithms

**Linear Regression (from scratch):**
```python
def linear_regression(x, y):
    """Manual implementation of simple linear regression."""
    x_mean, y_mean = np.mean(x), np.mean(y)
    numerator = np.sum((x - x_mean) * (y - y_mean))
    denominator = np.sum((x - x_mean) ** 2)
    slope = numerator / denominator
    intercept = y_mean - slope * x_mean
    return slope, intercept
```

**Z-Score Anomaly Detection:**
```python
z_score = (amount - mean_amount) / std_amount
is_anomaly = z_score > threshold  # Default: 2.0 standard deviations
```

### Data Cleaning Pipeline

1. **Dates:** 15+ formats → Pandas datetime (UTC normalized)
2. **Amounts:** Currency symbols removed → Float conversion → Negative values dropped
3. **Categories:** Lowercase → Synonym mapping → Title case normalization
---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `pandas` | ≥2.0.0 | Data manipulation and analysis |
| `matplotlib` | ≥3.5.0 | Data visualization |
| `numpy` | ≥1.24.0 | Numerical computations |
| `jupyter` | ≥1.0.0 | Notebook environment |

---

## 🤝 Contributing

This project was developed as part of the **"Introduction to Python"** course at **TU Dortmund University**.

**Author:** Saqib Raza  
**Course:** Introduction to Python (3 ECTS)  
**Instructor:** Lars Kühmichel  
**Date:** March 2026

---

## 📄 License

This project is created for educational purposes and is licensed under the MIT License.

---

## 🙏 Acknowledgments

- TU Dortmund University for the excellent Python course
- Open-source community for the amazing libraries
- Everyone who provided feedback and suggestions

---

## 📧 Contact

For questions or feedback:
- **Email:** saqib.raza@tu-dortmund.de
- **GitHub:** [Saqib Raza](https://github.com/saqibraza0902)

---

**Made with ❤️ for better financial decisions**
