from faker import Faker
import pandas as pd
from datetime import datetime, timezone
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
    df.to_csv(file_name, index=False)
    return df


 

def generate_paypal_data(num_rows, file_name, date):

    date_obj = datetime.strptime(date, "%Y-%m-%d")
    local_tz = ZoneInfo("America/New_York")
    start = date_obj.replace(hour=0,  minute=0,  second=0,  tzinfo=local_tz)
    end= date_obj.replace(hour=23, minute=59, second=59, tzinfo=local_tz)
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

    df = pd.DataFrame(rows)
    df.to_csv(file_name, index=False)
    return df



 


