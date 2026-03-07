import pandas as pd


def add_transaction(filepath, date,category, amount):
    df = pd.read_csv(filepath) # type: ignore
    new_row = {"date": date,"category":category, "amount": amount}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(filepath, index=False)


def list_transactions(filepath):
    df = pd.read_csv(filepath) # type: ignore
    print(df)


def delete_transaction(filepath, idx):
    df = pd.read_csv(filepath) # type: ignore
    df = df.drop(idx)
    df.to_csv(filepath, index=False)


def update_transaction(filepath, idx, amount):
    df = pd.read_csv(filepath) # type: ignore
    df.loc[idx, "amount"] = amount
    df.to_csv(filepath, index=False)