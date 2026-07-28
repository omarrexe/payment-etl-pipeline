# 💳 Multi-Processor Payment ETL Pipeline
### A Data Engineering Learning Project

---

## What Is This Project?

You're building a **data pipeline** that does one job:

> *Collect payment records from 3 different payment companies, clean the mess, validate the data, and store it in one organized place.*

That's it. But the "mess" is what makes it real.

---

## The Story Behind It

Imagine you work at a fintech startup. Your company accepts payments through 3 providers:

| Provider | Type | Why it's messy |
|---|---|---|
| **Stripe** | Credit card payments | Sends amounts in **cents** (5000 = $50), timestamps in UTC |
| **PayPal** | PayPal wallet payments | Sends amounts in **dollars** (50.00), different column names, local timezone |
| **Bank ACH** | Direct bank transfer | Data arrives **1–3 days late**, batched not real-time |

Every day, each provider drops a file. Your pipeline has to process all 3 and produce one clean, unified payment ledger.

---

## What You Will Build (Phase by Phase)

### Phase 1 — Fake Data Generator (4–6 hrs)
**Goal:** Build a script that generates realistic fake payment files with intentional problems baked in.

**You need to figure out:**
- What columns does a payment record need? (think before looking it up)
- How do you make Stripe data look different from PayPal data on purpose?
- How do you inject a duplicate? How do you inject a late record?

**Tools to learn:** `Faker` library, `random` module, `pandas` DataFrame creation, writing to CSV/JSON/Parquet

**What "done" looks like:**
- A `generate_data.py` script that creates one day's worth of fake files for all 3 sources
- Each source has its own format and its own type of mess
- You can run it multiple times to simulate multiple days

---

### Phase 2 — Basic Ingestion & Normalization (3–4 hrs)
**Goal:** Read all 3 files and turn them into one consistent format.

**You need to figure out:**
- How do you read CSV vs JSON vs Parquet with pandas?
- How do you rename columns?
- How do you convert cents to dollars? How do you standardize timestamps to UTC?

**Tools to learn:** `pd.read_csv()`, `pd.read_json()`, `pd.read_parquet()`, `df.rename()`, `pd.to_datetime()`, `pyarrow`

**What "done" looks like:**
- A function per source: `read_stripe()`, `read_paypal()`, `read_bank()`
- Each returns a DataFrame with the same column names and types
- You can `pd.concat()` all three into one unified DataFrame

---

### Phase 3 — Schema Validation & Data Quality Gate (4–6 hrs)
**Goal:** Before saving anything, check that the data meets your rules. Bad rows go to a "rejects" folder with a reason — they don't break the whole pipeline.

**You need to figure out:**
- What rules should a valid payment row follow? (required fields, value ranges, formats)
- How do you separate "good rows" from "bad rows" in pandas?
- What information does a rejected row need to be useful later?

**Tools to learn:** `pandera` library for DataFrame validation, boolean indexing in pandas, writing to a rejects file

**What "done" looks like:**
- A schema defined with `pandera` that describes a valid payment row
- A function that takes a DataFrame, runs validation, returns `(clean_df, rejects_df)`
- Rejected rows written to `rejects/YYYY-MM-DD_rejects.csv` with a `reject_reason` column

---

### Phase 4 — Deduplication & Idempotency (4–5 hrs)
**Goal:** Make sure running your pipeline twice on the same day doesn't create duplicate records.

**You need to figure out:**
- What makes two rows "the same"? (think: which columns together uniquely identify a payment?)
- What's a "watermark" file and why does it help?
- What does "running a pipeline twice should produce the same result" actually mean in code?

**Tools to learn:** `df.drop_duplicates()`, file-based checkpointing (reading/writing a simple JSON or text file that tracks what's already been processed)

**What "done" looks like:**
- Your pipeline checks a `checkpoint.json` before processing — skips dates already loaded
- Exact duplicate rows are removed before writing
- Running the pipeline twice on the same day changes nothing in the output

---

### Phase 5 — Partitioned Parquet Output (2–3 hrs)
**Goal:** Write clean data to a "data lake" folder structure organized by date.

**You need to figure out:**
- What does `warehouse/year=2026/month=07/day=11/` structure mean and why do data lakes use it?
- How do you write a partitioned Parquet file with pyarrow?

**Tools to learn:** `pyarrow.parquet.write_to_dataset()`, partition columns concept

**What "done" looks like:**
- Clean data is written to `warehouse/year=YYYY/month=MM/day=DD/payments.parquet`
- You can read back any single day's data by reading just that folder

---

### Phase 6 — Late-Arriving Data / Backfill (3–5 hrs)
**Goal:** Handle the bank ACH records that arrive 1–3 days late by reprocessing older partitions.

**You need to figure out:**
- How do you detect that a record's *event date* is different from the *file date* it arrived in?
- How do you update an already-written Parquet partition without duplicating data?

**This is the hardest phase.** Expect to rethink your approach at least once. That's normal.

**What "done" looks like:**
- Pipeline detects late records (event date ≠ processing date)
- Late records are written to their correct date partition (not the current day's partition)
- Re-running doesn't duplicate late records (dedup logic applies here too)

---

### Phase 7 — Run Logging & Metrics (1–2 hrs)
**Goal:** After every pipeline run, append a summary row to a log file.

**You need to figure out:**
- What information is useful to track per run? (rows processed, rows rejected, duration, date, source)

**What "done" looks like:**
- A `pipeline_runs.csv` that grows by one row after each run
- Columns like: `run_date`, `source`, `rows_ingested`, `rows_rejected`, `duration_seconds`, `status`

---

### Phase 8 — Polish & Optional Dashboard (3–5 hrs)
**Goal:** Make the repo presentable on GitHub.

**Tasks:**
- Write a clear `README.md` with: what the project does, how to run it, folder structure, a screenshot
- Add a `requirements.txt`
- Optional: Build a simple Streamlit dashboard showing pipeline run history and reject breakdown

---

## Folder Structure (Design This Yourself First)

Before looking at any examples, try to sketch the folder structure yourself. Answer:
- Where does raw source data go?
- Where does clean data go?
- Where do rejects go?
- Where does your Python code go?
- Where does the run log go?

Then compare your answer to what you come up with after Phase 1.

---

## Key Concepts to Understand (Not Just Do)

Before starting each phase, make sure you can answer these in your own words:

| Concept | Question to answer yourself |
|---|---|
| **Idempotency** | If I run my pipeline 10 times on the same data, what should happen? |
| **Schema drift** | What breaks in a pipeline if a column gets renamed in the source? |
| **Data quality gate** | Why not just skip bad rows silently instead of quarantining them? |
| **Partitioned storage** | Why organize files by date folder instead of one big file? |
| **Late-arriving data** | Why does it matter *which day* a record belongs to vs which day it arrived? |
| **Watermark/checkpoint** | Why can't you just check if the output file already exists? |

---

## Time Estimate

| Phase | Hours |
|---|---|
| 1. Fake data generator | 4–6 |
| 2. Ingestion & normalization | 3–4 |
| 3. Schema validation & rejects | 4–6 |
| 4. Dedup & idempotency | 4–5 |
| 5. Partitioned Parquet output | 2–3 |
| 6. Late-arriving data | 3–5 |
| 7. Run logging | 1–2 |
| 8. Polish + README + optional dashboard | 3–5 |
| **Total** | **~25–36 hours** |

Realistic pace: **2–3 weeks** doing evenings and weekends.

---

## Suggested Learning Order for Tools

Don't try to learn everything at once. Learn each tool *when you need it*:

1. **Week 1** → `Faker`, `pandas` basics review (read/write CSV/JSON/Parquet, rename, concat, groupby)
2. **Week 2** → `pandera` for validation, `pyarrow` for Parquet output
3. **Week 3** → Backfill logic, run logging, README polish

---

## Interview Talking Points You'll Be Able to Make

Once you finish this project, you'll be able to answer:

- *"Tell me about a time you handled messy or inconsistent data"* → Schema drift + normalization across 3 sources
- *"How do you ensure a pipeline is idempotent?"* → Checkpoint file + dedup logic
- *"How do you handle data quality in your pipelines?"* → Pandera validation + quarantine rejects with reason codes
- *"How is data organized in a data lake?"* → Partitioned Parquet by date
- *"How do you handle late-arriving data?"* → Backfill logic with event-time vs processing-time distinction

---

## Ground Rules for Learning

1. **Design before you code.** For each phase, write down in plain English what you want to happen before touching Python.
2. **Use AI for tool/syntax questions, not design decisions.** Stuck on a Faker method? Ask. Unsure what columns to validate? Figure it out yourself.
3. **Get one source working end-to-end first.** Don't try to handle all 3 sources at once. Get Stripe → validate → dedup → write Parquet working before adding PayPal.
4. **Commit to GitHub often.** Even broken code. The commit history tells the story of your learning.
5. **If it breaks, that's Phase 6's gift.** Late data and edge cases breaking things is the whole point — that's when you learn the most.

---

*Last updated: July 2026*
