import pandas as pd

def read_stripe(file_path):
    df = pd.read_csv(file_path)
    return df


def read_paypal(file_path):
    df = pd.read_json(file_path, lines=True)
    return df


def read_bank(file_path):
    df = pd.read_parquet(file_path)
    return df




