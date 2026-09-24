import pandas as pd
from pathlib import Path
from ingestion.readers import read_stripe, read_paypal, read_bank
from transforms.normalize import normalize_stripe, normalize_paypal, normalize_bank
from validation.validate import validate, write_rejects


ROOT = Path(__file__).resolve().parent.parent

day = "2026-07-16"

stripe_df = read_stripe(ROOT / f"data/raw/stripe/{day}.csv")
paypal_df = read_paypal(ROOT / f"data/raw/paypal/{day}.json")
bank_df = read_bank(ROOT / f"data/raw/bank_ach/{day}.parquet")

stripe_df = normalize_stripe(stripe_df)
paypal_df = normalize_paypal(paypal_df)
bank_df = normalize_bank(bank_df)

combined = pd.concat([stripe_df, paypal_df, bank_df], ignore_index=True)

 
clean_df, rejects_df = validate(combined)
print("clean:", clean_df.shape, "rejects:", rejects_df.shape)

write_rejects(rejects_df, day)
