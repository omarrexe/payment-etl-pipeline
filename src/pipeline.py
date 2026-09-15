from ingestion.readers import read_stripe, read_paypal, read_bank

stripe_df = read_stripe("data/raw/stripe/2026-07-16.csv")
paypal_df = read_paypal("data/raw/paypal/2026-07-16.json")
bank_df = read_bank("data/raw/bank_ach/2026-07-16.parquet")


print(stripe_df.head())
 