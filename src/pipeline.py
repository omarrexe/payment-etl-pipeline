from ingestion.readers import read_stripe, read_paypal, read_bank
from transforms.normalize import normalize_stripe, normalize_paypal, normalize_bank


stripe_df = read_stripe("data/raw/stripe/2026-07-16.csv")
paypal_df = read_paypal("data/raw/paypal/2026-07-16.json")
bank_df = read_bank("data/raw/bank_ach/2026-07-16.parquet")

stripe_df = normalize_stripe(stripe_df)
paypal_df = normalize_paypal(paypal_df)
bank_df = normalize_bank(bank_df)

print(stripe_df.head())
print(paypal_df.head())
print(bank_df.head())