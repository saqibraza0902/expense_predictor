# Expense Predictor (Python Project)

## Overview

Expense Predictor is a Python package that analyzes personal spending data and predicts future expenses using machine learning.
It helps users understand their spending habits, manage transactions, and receive recommendations based on spending trends.

## Features

* Load expense data from a CSV file
* Automatic transaction ID generation
* Data cleaning and preprocessing
* Exploratory analysis of spending patterns
* Machine learning model to predict future expenses
* Generate predictions from historical spending data
* Textual recommendations based on spending trends
* CRUD operations for managing transactions (Create, Read, Update, Delete)
* Modular Python package structure
* Jupyter notebooks for experimentation and testing

## Project Structure

```
expense-predictor/
│
├── data/
│   └── transactions.csv
│
├── src/
│   └── expense_predictor/
│       ├── __init__.py
│       ├── __main__.py
│       ├── analyzer.py
│       ├── cli.py
│       ├── predictor.py
│       ├── recommendations.py
│       └── transactions.py
│
├── notebooks/
│   ├── analysis.ipynb
│   └── transactions.ipynb
│
├── main.py
├── pyproject.toml
└── README.md
```

## Requirements

* Python 3.10+
* pandas
* scikit-learn
* matplotlib
* jupyter
* uv

## Installation

Clone the repository and install the package.

```
git clone <repository-url>
cd expense-predictor
uv pip install -e .
```

## Running the Project (Command Line)

Run the expense prediction:

```
uv run -m expense_predictor predict data/transactions.csv
```

Analyze the dataset:

```
uv run -m expense_predictor analyze data/transactions.csv
```

Generate spending recommendations:

```
uv run -m expense_predictor recommendations data/transactions.csv
```

## Running with Python

```
python main.py
```

## Running Jupyter Notebooks

Start Jupyter:

```
jupyter notebook
```

Open one of the notebooks:

```
notebooks/analysis.ipynb
```

or

```
notebooks/transactions.ipynb
```

## Purpose

This project demonstrates how Python can be used to build a small financial analysis system that includes data processing, machine learning prediction, transaction management, and spending recommendations.
