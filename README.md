# 💳 Payment ETL Pipeline

Incremental ETL pipeline ingesting multi-source payment data (Stripe / PayPal / Bank ACH) with schema validation, deduplication, and partitioned Parquet output.

---

## Quick Start (any machine)

```bash
git clone https://github.com/<your-username>/payment-etl-pipeline.git
cd payment-etl-pipeline
bash setup.sh
```

That's it. `setup.sh` will:
1. Create a `.venv` virtual environment
2. Install all dependencies from `requirements.txt`
3. Create all required folders (`data/`, `rejects/`, `logs/`)
4. Generate sample data for all 3 sources

Then activate the venv in your shell:
```bash
source .venv/bin/activate
```

---

## Project Structure

```
payment-etl-pipeline/
├── src/
│   ├── generator/        # Phase 1 — fake data generator
│   ├── ingestion/        # Phase 2 — readers for each source
│   ├── transforms/       # Phase 3 — validation & cleaning
│   ├── validation/       # Phase 3 — schema validation
│   ├── storage/          # Phase 5 — Parquet output
│   └── pipeline.py       # Main orchestrator
├── data/
│   ├── raw/              # Raw source files (generated, not in git)
│   └── warehouse/        # Clean partitioned output (not in git)
├── rejects/              # Rejected rows with reason codes
├── logs/                 # Pipeline run logs
├── setup.sh              # Bootstrap script
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
| 2 | Ingestion & normalization | 🔄 In progress |
| 3 | Schema validation & rejects | ⬜ Pending |
| 4 | Deduplication & idempotency | ⬜ Pending |
| 5 | Partitioned Parquet output | ⬜ Pending |
| 6 | Late-arriving data / backfill | ⬜ Pending |
| 7 | Run logging & metrics | ⬜ Pending |
| 8 | Polish & optional dashboard | ⬜ Pending |
