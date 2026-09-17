import pandas as pd
from datetime import datetime, timezone
import pandas as pd

def _normalize_status(series):
    mapping = {
        "success": "success",
        "failed": "failed",
        "pending": "pending",
        "refunded": "refunded",
        "settled": "success",
        "returned": "refunded",
    }
    return series.replace(mapping)

def normalize_stripe(df):
    df = df.copy()

    if "name" in df.columns:
        df = df.rename(columns={"name": "customer_name"})
    elif "full_name" in df.columns:
        df = df.rename(columns={"full_name": "customer_name"})

    if "amount_cents" in df.columns:
        df = df.rename(columns={"amount_cents": "amount"})
    if "timestamp" in df.columns:
        df = df.rename(columns={"timestamp": "timestamp_utc"})

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce") / 100
    df["timestamp_utc"] = pd.to_datetime(df["timestamp_utc"], errors="coerce", utc=True)
    df["customer_email"] = None
    df["source"] = "stripe"
    df["status"] = _normalize_status(df["status"])

    final_columns = [
        "customer_name",
        "customer_email",
        "customer_id",
        "transaction_id",
        "amount",
        "currency",
        "timestamp_utc",
        "status",
        "source",
    ]

    return df[final_columns]


def normalize_paypal(df):
    df = df.copy()

    if "payer_name" in df.columns:
        df = df.rename(columns={"payer_name": "customer_name"})
    elif "full_name" in df.columns:
        df = df.rename(columns={"full_name": "customer_name"})

    if "payer_email" in df.columns:
        df = df.rename(columns={"payer_email": "customer_email"})
    if "total_paid" in df.columns:
        df = df.rename(columns={"total_paid": "amount"})
    if "timestamp" in df.columns:
        df = df.rename(columns={"timestamp": "timestamp_utc"})

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["timestamp_utc"] = pd.to_datetime(df["timestamp_utc"], errors="coerce", utc=True)
    df["source"] = "paypal"
    df["status"] = _normalize_status(df["status"])

    final_columns = [
        "customer_name",
        "customer_email",
        "customer_id",
        "transaction_id",
        "amount",
        "currency",
        "timestamp_utc",
        "status",
        "source",
    ]

    return df[final_columns]


def normalize_bank(df):
    df = df.copy()

    if "account_holder" in df.columns:
        df = df.rename(columns={"account_holder": "customer_name"})
    elif "holder_name" in df.columns:
        df = df.rename(columns={"holder_name": "customer_name"})

    if "transfer_amount" in df.columns:
        df = df.rename(columns={"transfer_amount": "amount"})
    if "transaction_date" in df.columns:
        df = df.rename(columns={"transaction_date": "timestamp_utc"})

    df["customer_email"] = None
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["timestamp_utc"] = pd.to_datetime(df["timestamp_utc"], errors="coerce", utc=True)
    df["source"] = "bank_ach"
    df["status"] = _normalize_status(df["status"])

    final_columns = [
        "customer_name",
        "customer_email",
        "customer_id",
        "transaction_id",
        "amount",
        "currency",
        "timestamp_utc",
        "status",
        "source",
    ]

    return df[final_columns]