# 💳 Payment ETL Pipeline

Incremental ETL pipeline ingesting multi-source payment data (Stripe / PayPal / Bank ACH) with schema validation, deduplication, and partitioned Parquet output.

 
## Project Structure

```
payment-etl-pipeline/
├── src/
│   ├── generator/        # Phase 1 — fake data generator
│   ├── ingestion/        # Phase 2 — readers for each source
│   ├── transforms/       # Phase 2 — normalization & cleaning
│   ├── validation/       # Phase 3 — schema validation & rejects gate
│   ├── storage/          # Phase 5 — Parquet output (empty for now)
│   ├── config.py         # Shared paths
│   └── pipeline.py       # Main orchestrator
├── data/
│   ├── raw/              # Raw source files (generated, not in git)
│   ├── rejects/          # Rejected rows with reason codes (not in git)
│   └── warehouse/        # Clean partitioned output (not in git, Phase 5)
├── requirements.txt
└── DESIGN.md             # Unified schema & data flow design
```

---

## Requirements

- Python 3.10+
- See `requirements.txt` for packages

---

## Phases

| Phase | Description | Status |
|---|---|---|
| 1 | Fake data generator | ✅ Done |
| 2 | Ingestion & normalization | ✅ Done|
| 3 | Schema validation & rejects | ✅ Done |
| 4 | Deduplication & idempotency | ⬜ Pending |
| 5 | Partitioned Parquet output | ⬜ Pending |
| 6 | Late-arriving data / backfill | ⬜ Pending |
| 7 | Run logging & metrics | ⬜ Pending |
| 8 | Polish & optional dashboard | ⬜ Pending |
