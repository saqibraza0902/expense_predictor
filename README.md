# Expense Predictor (Python Project)

## Overview

This project is a Python package that analyzes personal spending data and predicts future expenses using machine learning techniques. The goal is to help users understand their spending patterns and estimate upcoming expenses.

## Features

* Load and process expense dataset from CSV
* Clean and prepare financial data
* Perform exploratory data analysis
* Train a machine learning model to predict expenses
* Generate predictions based on historical spending
* Modular Python package structure
* Jupyter Notebook for running and testing the project

## Project Structure

```
expense-predictor/
│
├── data/
│   └── expenses.csv
│
├── src/
│   └── expense_predictor/
│       ├── __init__.py
│       ├── data_loader.py
│       ├── preprocessing.py
│       ├── model.py
│       └── predictor.py
│
├── notebooks/
│   └── experiment.ipynb
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

## How to Run

1. git clone 
2. cd expense-predictor
3. uv pip install -e .
4. uv run -m expense_predictor "command_type" data/transactions.csv

```
python main.py
```

## Purpose

This project demonstrates how Python can be used to build a small data analysis and prediction system using real-world expense data.
