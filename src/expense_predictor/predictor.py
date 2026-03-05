import numpy as np


def linear_regression(x, y):
    """
    Manual simple linear regression.
    y = mx + b
    """

    x = np.array(x)
    y = np.array(y)

    n = len(x)

    x_mean = np.mean(x)
    y_mean = np.mean(y)

    numerator = np.sum((x - x_mean) * (y - y_mean))
    denominator = np.sum((x - x_mean) ** 2)

    m = numerator / denominator
    b = y_mean - m * x_mean

    return m, b


def predict_next(monthly_totals):
    x = list(range(len(monthly_totals)))
    y = monthly_totals.values

    m, b = linear_regression(x, y)

    next_x = len(monthly_totals)
    prediction = m * next_x + b

    return prediction