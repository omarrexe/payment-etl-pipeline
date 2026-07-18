# Pipeline Design

## Unified Schema

| Column | Type | Source mapping |
|---|---|---|
| customer_name | string | Stripe: name, PayPal: payer_name, ACH: account_holder |
| customer_email | string | PayPal: payer_email, others: null |
| customer_id | string | Same across all sources |
| transaction_id | string | Same across all sources |
| amount | float | Stripe: amount, PayPal: total_paid, ACH: transfer_amount |
| currency | string | Same across all sources |
| timestamp_utc | datetime | All converted to UTC |
| status | string | settled→success, returned→refunded |
| source | string | Same across all sources |

## Status Normalization

| Raw value | Unified value |
|---|---|
| success | success |
| failed | failed |
| pending | pending |
| refunded | refunded |
| settled | success |
| returned | refunded |

## Data Flow

```
data/raw/stripe/     ──┐
data/raw/paypal/     ──┼──► Normalize ──► Validate ──► Dedup ──► Parquet
data/raw/bank_ach/   ──┘                      │
                                               └──► rejects/
```

## Phase Checklist

- [x] Phase 1: Fake data generator
- [ ] Phase 2: Ingestion & normalization
- [ ] Phase 3: Schema validation & rejects
- [ ] Phase 4: Deduplication
- [ ] Phase 5: Partitioned Parquet output
- [ ] Phase 6: Late-arriving data
- [ ] Phase 7: Run logging
- [ ] Phase 8: Polish & README