from faker import Faker
import pandas as pd
import random
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
fake = Faker()


def generate_stripe_data(num_rows, file_name, date):
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    start = date_obj.replace(
        hour=0,  minute=0,  second=0,  tzinfo=timezone.utc)
    end = date_obj.replace(hour=23, minute=59, second=59, tzinfo=timezone.utc)

    rows = []

    for _ in range(num_rows):
        rows.append({
            "name": fake.name(),
            "customer_id": f"cust_{fake.random_number(digits=8, fix_len=True)}",
            "transaction_id": fake.uuid4(),
            "amount": round(float(fake.pydecimal(left_digits=3, right_digits=2, positive=True)), 2),
            "currency": "USD",
            "timestamp": fake.date_time_between(
                start_date=start,
                end_date=end,
                tzinfo=timezone.utc),
            "status": fake.random_element(elements=("success", "failed", "pending", "refunded")),
            "source": "stripe",
        })

   
    df = pd.DataFrame(rows)
    #injct mess
    df = inject_mess(df, date,                       
    nullable_columns=["name"],
    drift_column="name",
    new_name="full_name")
    
    df.to_csv(file_name, index=False)
    return df


def generate_paypal_data(num_rows, file_name, date):

    date_obj = datetime.strptime(date, "%Y-%m-%d")
    local_tz = ZoneInfo("America/New_York")
    start = date_obj.replace(hour=0,  minute=0,  second=0,  tzinfo=local_tz)
    end = date_obj.replace(hour=23, minute=59, second=59, tzinfo=local_tz)
    rows = []

    for _ in range(num_rows):
        rows.append({
            "payer_name": fake.name(),
            "payer_email": fake.email(),
            "customer_id": f"cust_{fake.random_number(digits=8, fix_len=True)}",
            "transaction_id": fake.uuid4(),
            "total_paid": round(float(fake.pydecimal(left_digits=3, right_digits=2, positive=True)), 2),
            "currency": "USD",
            "timestamp": fake.date_time_between(
                    start_date=start,
                    end_date=end,
                    tzinfo=local_tz),
            "status": fake.random_element(elements=("success", "failed", "pending", "refunded")),
            "source": "paypal"

        })

  # injct mess
    df = pd.DataFrame(rows)
    df = inject_mess(df, date,
    nullable_columns=["payer_name", "payer_email"],
    drift_column="payer_name",
    new_name="full_name")
    df.to_csv(file_name, index=False)
    return df


def generate_bank_ach_data(num_rows, file_name, date):

    date_obj = datetime.strptime(date, "%Y-%m-%d")

    rows = []

    for _ in range(num_rows):

        days_late = random.randint(1, 3)
        transaction_date = date_obj - timedelta(days=days_late)
        rows.append({
            "account_holder": fake.name(),
            "customer_id": f"cust_{fake.random_number(digits=8, fix_len=True)}",
            "transaction_id": fake.uuid4(),
            "transfer_amount": round(float(fake.pydecimal(left_digits=3, right_digits=2, positive=True)), 2),
            "currency": "USD",
            "transaction_date": transaction_date.date(),
            "days_late": days_late,

            "status": fake.random_element(elements=("settled", "pending", "failed", "returned")),
            "source": "bank_ach"

        })

    df = pd.DataFrame(rows)
     # injct mess
    df = inject_mess(df, date,
    nullable_columns=["account_holder"],
    drift_column="account_holder",
    new_name="holder_name")
    df.to_csv(file_name, index=False)
    return df


def inject_duplicates(df):
    n = random.randint(1, 5)
    return pd.concat([df,df.sample(n)]).sample(frac=1).reset_index(drop=True)
    

def inject_null(df, nullable_columns):
    for col in nullable_columns:
         n = random.randint(1, 5)
         null_indices = df.sample(n=n).index
         df.loc[null_indices, col] = None
         
    return df
    
    
    
def inject_schema_drift(df, date, drift_column, new_name):
    day = datetime.strptime(date, "%Y-%m-%d").day
    if day % 3 == 0:
        df.rename(columns={drift_column: new_name}, inplace=True)
    return df



def inject_mess(df, date, nullable_columns, drift_column, new_name):
    df = inject_duplicates(df)
    df = inject_null(df, nullable_columns)
    df = inject_schema_drift(df, date, drift_column, new_name)
    return df


 


if __name__ == "__main__":
    date = "2026-07-16"
    
    generate_stripe_data(100, "data/raw/stripe/2026-07-16.csv", date)
    generate_paypal_data(100, "data/raw/paypal/2026-07-16.csv", date)
    generate_bank_ach_data(100, "data/raw/bank_ach/2026-07-16.csv", date)
    
    print("Data generated successfully!")